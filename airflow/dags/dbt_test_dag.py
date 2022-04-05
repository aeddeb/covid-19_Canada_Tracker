from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner' : 'airflow'
}

with DAG(
    dag_id = 'dbt_test',
    default_args = default_args,
    description = 'Test dbt',
    schedule_interval="@once",
    start_date=datetime(2022,4,1),
    catchup=True,
    tags=['dbt']
) as dag:

    dbt_test_task = BashOperator(
        task_id = "dbt_test",
        bash_command = "cd /dbt && dbt deps && dbt compile --profiles-dir ."
    )

    