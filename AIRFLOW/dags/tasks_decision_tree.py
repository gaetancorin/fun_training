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

    @task()
    def branch_a():
        print("Branch A working")

    @task()
    def branch_b():
        print("Branch B working")

    @task()
    def branch_c():
        print("Branch C working")

    @task()
    def end():
        print("End task")

    n = generate_number()
    next_task = decide_branch(n)
    a = branch_a()
    b = branch_b()
    c = branch_c()
    end_task = end()

    next_task >> [a, b, c]
    [a, b, c] >> end_task