from airflow import DAG
from airflow.decorators import task, task_branch
from datetime import datetime
import random

with DAG(
    dag_id="decision_tree_random",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
):

    @task()
    def generate_number():
        n = random.randint(1, 100)
        print(f"N: {n}")
        return n

    @task_branch()
    def decide_branch(n: int):
        if n <= 30:
            print("Need Branch A: (1–30)")
            return "branch_a"
        elif n <= 70:
            print("Need Branch B : (31–70)")
            return "branch_b"
        else:
            print("Need Branch C : (71–100)")
            return "branch_c"


    n = generate_number()
    next_task = decide_branch(n)
