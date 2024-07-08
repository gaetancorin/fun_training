from airflow import DAG
from airflow.decorators import task
from datetime import datetime

with DAG(
        dag_id="create_venv_into_task",
        start_date=datetime(2024, 1, 1),
        schedule=None,
        catchup=False,
):
    @task.virtualenv(requirements=["requests==2.31.0"])
    def isolated_task():
        import requests
        print("result of https://api.github.com calling :", requests.get("https://api.github.com").status_code)

    isolated_task()