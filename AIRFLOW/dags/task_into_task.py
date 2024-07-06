from airflow import DAG
from airflow.decorators import task
from datetime import datetime

with DAG(
        dag_id="task_into_task",
        start_date=datetime(2024, 1, 1),
        schedule=None,
        catchup=False,
):
    @task()
    def generate_number():
        return 30

    @task()
    def print_number(n):
        print(f"The number is {n}")

    print_number(generate_number())
