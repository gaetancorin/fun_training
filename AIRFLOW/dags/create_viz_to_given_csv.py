from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

DATA_DIR = '/opt/airflow/data'  # volume partagé avec l'hôte
os.makedirs(DATA_DIR, exist_ok=True)

# --- fonctions Python ---
def creer_csv_produits():
    produits = ['Pommes', 'Bananes', 'Cerises']
    data = {produit: np.random.randint(10, 100, 10) for produit in produits}
    df = pd.DataFrame(data)
    df.to_csv(f'{DATA_DIR}/produits_input.csv', index=False)
    print(f"CSV produits créé : {DATA_DIR}/produits_input.csv")

def traiter_csv_produits():
    df = pd.read_csv(f'{DATA_DIR}/produits_input.csv')
    df_result = pd.DataFrame({
        'Produit': df.columns,
        'Total': df.sum(),
        'Moyenne': df.mean(),
        'Max': df.max()
    })
    df_result.to_csv(f'{DATA_DIR}/produits_result.csv', index=False)
    print(f"CSV résultat produit : {DATA_DIR}/produits_result.csv")

def generer_graphique():
    df_result = pd.read_csv(f'{DATA_DIR}/produits_result.csv')
    plt.figure(figsize=(6,4))
    plt.bar(df_result['Produit'], df_result['Total'], color='skyblue')
    plt.title('Total par produit')
    plt.ylabel('Total')
    plt.savefig(f'{DATA_DIR}/produits_graph.png')
    plt.close()
    print(f"Graphique généré : {DATA_DIR}/produits_graph.png")

# --- arguments DAG ---
default_args = {
    'owner': 'gaetan',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# --- définition du DAG ---
with DAG(
    dag_id='create_viz_to_given_csv',
    description='Génère CSV, calcule stats et crée un graphique pour plusieurs produits',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule='@daily',
    catchup=False,
    tags=['airflow3', 'csv', 'graph'],
) as dag:

    tache_creer_csv = PythonOperator(
        task_id='creer_csv_produits',
        python_callable=creer_csv_produits,
    )

    tache_traiter_csv = PythonOperator(
        task_id='traiter_csv_produits',
        python_callable=traiter_csv_produits,
    )

    tache_graphique = PythonOperator(
        task_id='generer_graphique',
        python_callable=generer_graphique,
    )

    # --- ordonnancement ---
    tache_creer_csv >> tache_traiter_csv >> tache_graphique
