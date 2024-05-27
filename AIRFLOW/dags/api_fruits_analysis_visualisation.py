from airflow import DAG
from airflow.decorators import task
from datetime import datetime
import requests
import os
import json

DATA_DIR = "/opt/airflow/data"
os.makedirs(DATA_DIR, exist_ok=True)

with DAG(
    dag_id="api_fruits_analysis_visualisation",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
):
    @task()
    def fetch_data():
        """Récupère les données JSON depuis l’API Fruityvice"""
        url = "https://www.fruityvice.com/api/fruit/all"
        response = requests.get(url)
        response.raise_for_status()
        fruits = response.json()

        raw_path = os.path.join(DATA_DIR, "fruits_raw.json")
        with open(raw_path, "w") as f:
            json.dump(fruits, f)
        print(f"{len(fruits)} fruits récupérés.")
        return raw_path

    @task()
    def compute_stats(raw_path: str):
        """Calcule les tops 10 et sauvegarde les résultats"""
        with open(raw_path) as f:
            fruits = json.load(f)

        top_calories = sorted(fruits, key=lambda x: x['nutritions']['calories'], reverse=True)[:10]
        top_protein = sorted(fruits, key=lambda x: x['nutritions']['protein'], reverse=True)[:10]

        stats = {"top_calories": top_calories, "top_protein": top_protein}
        stats_path = os.path.join(DATA_DIR, "fruits_stats.json")

        with open(stats_path, "w") as f:
            json.dump(stats, f, indent=2)

        print("Top 10 enregistrés.")
        return stats_path


    raw = fetch_data()
    stats = compute_stats(raw)
