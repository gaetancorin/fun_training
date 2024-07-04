from airflow import DAG
from airflow.decorators import task
from airflow.utils.task_group import TaskGroup
from datetime import datetime

with DAG(
        dag_id="dynamique_task",
        start_date=datetime(2024, 1, 1),
        schedule=None,
        catchup=False,
):

    @task()
    def get_files():
        return ["file1.csv", "file2.csv", "file3.csv"]

    @task()
    def process_file(filename):
        print(f"Processing {filename}")

    files = get_files()
    process_file.expand(filename=files)