from airflow import DAG
from airflow.decorators import task
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime
import random

with DAG(
    dag_id="rule_if_failed_rule_if_sucessed",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    @task()
    def maybe_fail():
        n = random.choice([1, 2])
        print(f"N = {n}")
        if n == 1:
            print("Cette exécution réussit.")
            return "success"
        else:
            raise Exception("Échec volontaire (1 fois sur 2)")

    @task(trigger_rule=TriggerRule.ONE_SUCCESS)
    def run_if_one_success():
        print("Cette tâche s'exécute si au moins une tâche précédente a réussi.")


    @task(trigger_rule=TriggerRule.ALL_FAILED)
    def run_if_all_failed():
        print("Cette tâche s'exécute seulement si toutes les tâches précédentes ont échoué.")

    # Ordonnancement
    t1 = maybe_fail()
    t2 = run_if_one_success()
    t3 = run_if_all_failed()

    t1 >> [t2, t3]