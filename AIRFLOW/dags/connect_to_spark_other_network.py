from airflow import DAG
from airflow.decorators import task
from datetime import datetime
from docker.types import Mount

with DAG(
    dag_id="connect_to_spark_other_network",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
) as dag:
    @task.docker(
        docker_url="tcp://host.docker.internal:2375",
        image="python:3.12-slim",
        auto_remove='force',  # Remove container after execution
        network_mode="spark_cluster_spark_net",  # <-- where spark is
        mounts=[Mount(source="/tmp", target="/tmp", type="bind")],  # Create space into host for creating container
        environment={"EXAMPLE": "Hello Docker"},  # Environment variables
        mount_tmp_dir=False,
        do_xcom_push=False,
    )
    def docker_task():
        import socket

        spark_host = "spark-master"  # remplace par le hostname de ton master Spark
        spark_port = 7077

        print(f"Trying to connect to Spark at {spark_host}:{spark_port}...")
        try:
            sock = socket.create_connection((spark_host, spark_port), timeout=5)
            print("Spark reachable!")
            sock.close()
        except Exception as e:
            print(f"Cannot reach Spark: {e}")

    docker_task()
