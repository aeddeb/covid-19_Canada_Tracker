import os

from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

import json
import pandas as pd

from google.cloud import storage


PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")

URL_PREFIX = "https://api.opencovid.ca/"
URL_TEMPLATE = URL_PREFIX + "summary?date={{ prev_execution_date.strftime(\"%Y-%m-%d\") }}"
json_file = "covid_ca_data_{{ prev_execution_date.strftime(\"%Y_%m-%d\") }}.json"
csv_file = "covid_ca_data_{{ prev_execution_date.strftime(\"%Y_%m-%d\") }}.csv"
LOCAL_JSON_FILE = path_to_local_home + "/" + json_file
LOCAL_CSV_FILE = path_to_local_home + "/" + csv_file



def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    :param bucket: GCS bucket name
    :param object_name: target path & file-name
    :param local_file: source path & file-name
    :return:
    """
    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # (Ref: https://github.com/googleapis/python-storage/issues/74)
    # storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    # storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    # End of Workaround

    client = storage.Client()
    bucket = client.bucket(bucket)

    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)


def format_to_csv(local_json_file, local_csv_file):
    '''Format json data into a csv format.'''
    with open(local_json_file) as jf:
        data = json.load(jf)

    df = pd.DataFrame(data['summary'])

    df.to_csv(local_csv_file, index=False)


default_args = {
    "owner": "airflow",
    "start_date": datetime(2020, 1, 26), # start from Jan 26
    "depends_on_past": False,
    "retries": 1,
}

# NOTE: DAG declaration - using a Context Manager (an implicit way)
with DAG(
    dag_id="covid_data_ingestion_gcs_dag",
    schedule_interval="0 9 * * *", # 9 AM UTC daily
    default_args=default_args,
    catchup=True,
    tags=['covid-ca'],
) as dag:

    download_dataset_task = BashOperator(
        task_id="download_dataset_task",
        bash_command=f"curl -sS {URL_TEMPLATE} > {LOCAL_JSON_FILE}"
    )

    format_to_csv_task = PythonOperator(
        task_id="format_to_csv_task",
        python_callable=format_to_csv,
        op_kwargs={
            "local_json_file" : LOCAL_JSON_FILE,
            "local_csv_file" : LOCAL_CSV_FILE,
        },
    )

    local_json_to_gcs_task = PythonOperator(
        task_id="local_json_to_gcs_task",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket": BUCKET,
            "object_name": f"raw/{json_file}",
            "local_file": LOCAL_JSON_FILE,
        },
    )

    local_csv_to_gcs_task = PythonOperator(
        task_id="local_csv_to_gcs_task",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket": BUCKET,
            "object_name": f"formatted_csv/{csv_file}",
            "local_file": LOCAL_CSV_FILE,
        },
    )

    remove_local_data_task = BashOperator(
        task_id="remove_local_data_task",
        bash_command=f"rm {LOCAL_JSON_FILE} {LOCAL_CSV_FILE}"
    )

    download_dataset_task >> local_json_to_gcs_task >> remove_local_data_task

    download_dataset_task >> format_to_csv_task >> local_csv_to_gcs_task >> remove_local_data_task
