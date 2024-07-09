from airflow import DAG
from airflow.decorators import task
from datetime import datetime

with DAG(
    dag_id="create_docker_into_task",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
):
    @task.docker(
        docker_url="tcp://host.docker.internal:2375",  # Docker TCP host
        image="python:3.12-slim",  # Docker image to use
        auto_remove='force',  # Remove container after execution
        mounts=[],  # Optional: mounts like volume mounts
        environment={"EXAMPLE": "Hello Docker"},  # Environment variables
        network_mode="bridge",  # Network mode
    )
    def docker_task():
        import os
        print("Running inside Docker container!")
        print(f"EXAMPLE env variable: {os.environ['EXAMPLE']}")
        # You can run any Python code here
        import requests
        resp = requests.get("https://api.github.com")
        print(f"GitHub API status: {resp.status_code}")

    docker_task()
