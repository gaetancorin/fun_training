from airflow import DAG
from airflow.decorators import task
from datetime import datetime
from docker.types import Mount

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
        mounts=[Mount(source="/tmp", target="/tmp", type="bind")], # Create space into host for creating container
        environment={"EXAMPLE": "Hello Docker"},  # Environment variables
        mount_tmp_dir=False,
        do_xcom_push=False,
    )
    def docker_task():
        import os
        print("Running inside Docker container!")
        print(f"EXAMPLE env variable: {os.environ['EXAMPLE']}")

        # Run any Python code here
        import subprocess
        subprocess.check_call(["pip", "install", "requests"])
        import requests
        resp = requests.get("https://api.github.com")
        print(f"GitHub API status: {resp.status_code}")
        return resp.status_code

    docker_task()
