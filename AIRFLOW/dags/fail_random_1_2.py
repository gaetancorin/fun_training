from airflow import DAG
from airflow.decorators import task
from datetime import datetime
import random

with DAG(
    dag_id="fail_random_1_or_2",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
):

    @task()
    def maybe_fail():
        n = random.choice([1, 2])
        print(f"N = {n}")
        if n == 1:
            print("Cette exécution réussit.")
        else:
            raise Exception("Échec volontaire (1 fois sur 2)")

    @task()
    def success_message():
        print("Le DAG s’est exécuté avec succès cette fois-ci ! 🎉")

    result = maybe_fail()
    result >> success_message()
