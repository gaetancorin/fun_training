from airflow import DAG
from airflow.decorators import task
from datetime import datetime
import random

with DAG("tasks_decision_tree", start_date=datetime(2024,1,1), schedule=None, catchup=False):

    @task()
    def generate_number():
        return random.randint(1,100)

    @task.branch()
    def decide_branch(n: int):
        if n <= 50:
            return "low_number_task"
        else:
            return "high_number_task"

    @task()
    def low_number_task():
        print("Number is low! (-=50)")

    @task()
    def high_number_task():
        print("Number is high! (+50)")

    n = generate_number()
    branch = decide_branch(n)
    low = low_number_task()
    high = high_number_task()

    branch >> [low, high]
