from airflow.decorators import dag, task
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

DATA_DIR = '/opt/airflow/data'
os.makedirs(DATA_DIR, exist_ok=True)

default_args = {
    'owner': 'gaetan',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

@dag(
    dag_id='create_viz_to_given_csv',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
)
def create_viz_to_given_csv():
    """DAG using the modern Airflow 3 TaskFlow API"""

    @task
    def create_csv():
        produits = ['Pommes', 'Bananes', 'Cerises']
        data = {p: np.random.randint(10, 100, 10) for p in produits}
        df = pd.DataFrame(data)
        path = f"{DATA_DIR}/produits_input.csv"
        df.to_csv(path, index=False)
        print(f"✅ CSV created: {path}")
        return path

    @task
    def process_csv(path: str):
        df = pd.read_csv(path)
        result = pd.DataFrame({
            'Produit': df.columns,
            'Total': df.sum(),
            'Moyenne': df.mean(),
            'Max': df.max(),
        })
        out_path = f"{DATA_DIR}/produits_result.csv"
        result.to_csv(out_path, index=False)
        print(f"✅ Processed CSV: {out_path}")
        return out_path

    @task
    def plot_graph(result_path: str):
        df = pd.read_csv(result_path)
        plt.bar(df['Produit'], df['Total'], color='skyblue')
        plt.title('Total par produit')
        plt.ylabel('Total')
        graph_path = f"{DATA_DIR}/produits_graph.png"
        plt.savefig(graph_path)
        plt.close()
        print(f"✅ Graph saved: {graph_path}")

    # --- Workflow ---
    csv_path = create_csv()
    result_path = process_csv(csv_path)
    plot_graph(result_path)

create_viz_to_given_csv()
