from airflow.sdk import dag, task
from datetime import datetime

@dag(start_date=datetime(2024, 1, 1), schedule='@daily')
def my_first_dag_generique_function():

    @task
    def training_model(accuracy: int):
        return accuracy

    @task.branch
    def choose_best_model(accuracies: list[int]):
        if max(accuracies) > 2:
            return "accurate"
        return "inaccurate"

    @task.bash
    def accurate():
        return "echo 'accurate'"

    @task.bash
    def inaccurate():
        return "echo 'inaccurate'"

    accuracies = training_model.expand(accuracy=[1,2,3])
    choose_best_model(accuracies) >> [accurate(), inaccurate()]

my_first_dag_generique_function()