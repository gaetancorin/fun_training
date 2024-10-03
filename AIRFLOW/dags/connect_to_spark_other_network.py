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
        image="quay.io/jupyter/pyspark-notebook",
        auto_remove='force',  # Remove container after execution
        network_mode="spark_cluster_spark_net",  # <-- where spark is
        # mounts=[Mount(source="/tmp", target="/tmp", type="bind")],  # Create space into host for creating container
        environment={"EXAMPLE": "Hello Docker"},  # Environment variables
        mount_tmp_dir=False,
        do_xcom_push=False,
    )
    def spark_task():
        # Installer PySpark dans le container
        # import subprocess
        # subprocess.check_call(["pip", "install", "pyspark==3.5.1"])

        from pyspark.sql import SparkSession

        spark = SparkSession.builder \
            .master("spark://spark-master:7077") \
            .appName("AirflowDockerSparkTest") \
            .getOrCreate()

        print("Spark session started!")

        # Exemple simple : création DataFrame et comptage
        df = spark.createDataFrame([(1, "Alice"), (2, "Bob"), (3, "Charlie")], ["id", "name"])
        print("DataFrame content:")
        df.show()

        count = df.count()
        print(f"Number of rows: {count}")

        spark.stop()
        print("Spark session stopped.")

        return df

    spark_task()
