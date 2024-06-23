from airflow import DAG
from airflow.decorators import task
from airflow.utils.task_group import TaskGroup
from datetime import datetime

with DAG(
    dag_id="example_taskgroup_english",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
):

    @task()
    def start():
        print("🚀 Starting the pipeline")

    @task()
    def end():
        print("🏁 Pipeline finished")

    # Define a TaskGroup to logically group related tasks
    with TaskGroup("data_pipeline") as data_pipeline:
        @task()
        def extract():
            print("Extracting data")

        @task()
        def transform():
            print("Transforming data")

        @task()
            print("Loading data")

        # Define the order of tasks inside the TaskGroup
        extract() >> transform() >> load()

    start() >> data_pipeline >> end()
