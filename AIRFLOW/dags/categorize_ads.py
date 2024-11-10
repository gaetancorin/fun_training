from airflow import DAG
from airflow.decorators import task
from datetime import datetime
import requests

N = 10

categories = {
    "Vente d'objet": ["for sale", "sale", "selling", "buffet", "cabinet", "pony", "skull", "encyclopedia"],
    "Service": ["repair", "service", "auto repair", "delivery", "pick-up", "profit sharing"],
    "Recherche de personne": ["wanted", "contact", "looking for", "please contact"],
    "Offre d'emploi": ["job", "work", "hiring", "hours", "pay"]
}

def categorize_ad(ad_text):
    ad_text_lower = ad_text.lower()
    for category, keywords in categories.items():
        for kw in keywords:
            if kw in ad_text_lower:
                return category
    return "Autre"

with DAG(
    dag_id="categorize_ads",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    @task()
    def fetch_ad(i: int):
        url = "https://api.isevenapi.xyz/api/iseven/1/"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                ad_message = data.get("ad", "Pas de pub disponible")
                category = categorize_ad(ad_message)
                print(f"Pub {i+1} [{category}] : {ad_message}")
                return {"ad": ad_message, "category": category}
            else:
                print(f"Erreur requête {i+1} : {response.status_code}")
                return {"ad": None, "category": None}
        except Exception as e:
            print(f"Erreur requête {i+1} :", e)
            return {"ad": None, "category": None}

    ads_tasks = [fetch_ad.override(task_id=f"fetch_ad_{i+1}")(i) for i in range(N)]
