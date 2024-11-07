from airflow import DAG
from airflow.decorators import task
from datetime import datetime
import requests

with DAG(
    dag_id="check_github_status",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    @task()
    def check_github():
        url = "https://github.com/gaetancorin"
        try:
            response = requests.get(url)
            status = response.status_code
            print(f"HTTP status for {url}: {status}")
            return status
        except Exception as e:
            print(f"Error checking {url}: {e}")
            return None

    check_github()