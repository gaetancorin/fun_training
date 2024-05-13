from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import numpy as np


# --- fonctions des tâches ---
def creer_csv():
    # Create CSV with 10 random numbers
    df = pd.DataFrame({
        'nombre': np.random.randint(1, 100, 10)
    })
    # write one airflow-airflow-worker-1 container into /tmp/input.csv
    df.to_csv('/tmp/input.csv', index=False)
    print("CSV créé : /tmp/input.csv")


def traiter_csv():
    # read one airflow-airflow-worker-1 container into /tmp/input.csv
    df = pd.read_csv('/tmp/input.csv')
    somme = df['nombre'].sum()
    moyenne = df['nombre'].mean()
    df_result = pd.DataFrame({'somme': [somme], 'moyenne': [moyenne]})
    df_result.to_csv('/tmp/result.csv', index=False)
    print(f"Résultat calculé : somme={somme}, moyenne={moyenne}")


# --- arguments par défaut ---
default_args = {
    'owner': 'gaetan',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# --- définition du DAG ---
with DAG(
        dag_id='create_csv',
        description='Exemple DAG Airflow 3 avec traitement CSV',
        default_args=default_args,
        start_date=datetime(2024, 1, 1),
        schedule='@daily',
        catchup=False,
        tags=['airflow3', 'csv', 'exemple'],
) as dag:
    tache_creer_csv = PythonOperator(
        task_id='creer_csv',
        python_callable=creer_csv,
    )

    tache_traiter_csv = PythonOperator(
        task_id='traiter_csv',
        python_callable=traiter_csv,
    )

    # --- ordonnancement ---
    tache_creer_csv >> tache_traiter_csv
