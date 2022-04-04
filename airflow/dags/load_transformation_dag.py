import os
from datetime import datetime

from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator
from airflow.operators.bash import BashOperator


GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
GCP_GCS_BUCKET = os.environ.get("GCP_GCS_BUCKET")
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET")
TABLE_NAME = "covid_ca_raw"

with DAG(
    dag_id = f'load_transformation_dag',
    description = f'Execute only once to create songs table in bigquery',
    schedule_interval="@once",
    start_date=datetime(2022,3,20),
    end_date=datetime(2022,3,20),
    catchup=False,
    tags=['covid-ca']
) as dag:

    create_external_table_task = BigQueryCreateExternalTableOperator(
        task_id = 'create_external_table_task',
        table_resource = {
            'tableReference': {
            'projectId': GCP_PROJECT_ID,
            'datasetId': BIGQUERY_DATASET,
            'tableId': TABLE_NAME,
            },
            'externalDataConfiguration': {
                'sourceFormat': 'CSV',
                'sourceUris': [f'gs://{GCP_GCS_BUCKET}/formatted_csv/covid_ca_data_20*.csv'],
                "csvOptions": {"skipLeadingRows": 1},
            },
        }
    )

    dbt_transformation_task = BashOperator(
        task_id = 'dbt_transformation_task',
        bash_command = 'cd /dbt && dbt run --select stg_covid_timeseries'
    )

create_external_table_task >> dbt_transformation_task