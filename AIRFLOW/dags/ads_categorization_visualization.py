from airflow import DAG
from airflow.decorators import task
from datetime import datetime
import requests
import os
import matplotlib.pyplot as plt


N = 10
CATEGORIES = {
    "Vente d'objet": ["for sale", "sale", "selling", "buffet", "cabinet", "pony", "skull","encyclopedia", "mattress", "headstone","furniture", "car", "vehicle", "collection", "nativity"],
    "Service": ["repair", "service", "auto repair", "delivery", "pick-up", "profit sharing", "installation", "cleaning", "painting", "maintenance"],
    "Recherche de personne": ["wanted", "contact", "looking for", "please contact", "lost", "found"],
    "Offre d'emploi": ["job", "work", "hiring", "hours", "pay", "surgeon", "child care", "teacher", "nurse"],
    "Crypto / Invest": ["bitcoin", "crypto", "ethereum", "isEvenCoin", "investment", "token"],
    "Annonce insolite / divertissement": ["scarecrow", "drink", "funny", "essence of life", "unique", "weird", "strange"]
}

with DAG(
    dag_id="ads_categorization_visualization",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
):

    @task()
    def fetch_ads(n: int = N):
        ads = []
        url = "https://api.isevenapi.xyz/api/iseven/1/"
        for i in range(n):
            try:
                resp = requests.get(url)
                if resp.status_code == 200:
                    data = resp.json()
                    ad_message = data.get("ad", "Pas de pub disponible")
                    ads.append(ad_message)
                else:
                    print(f"Erreur requête {i+1} : {resp.status_code}")
            except Exception as e:
                print(f"Erreur requête {i+1} :", e)
        print(f"{len(ads)} pubs récupérées.")
        print("Ads data: -----")
        for ad in ads:
            print(ad)
        return ads


    @task()
    def categorize_ads(ads):
        categorized = []

        def categorize(ad_text):
            ad_lower = ad_text.lower()
            for cat, keywords in CATEGORIES.items():
                for kw in keywords:
                    if kw in ad_lower:
                        return cat
            return "Autre"

        for ad in ads:
            category = categorize(ad)
            categorized.append({"ad": ad, "category": category})

        print(f"{len(categorized)} pubs catégorisées.")
        print("Ads data categories : -----")
        for i, ad in enumerate(categorized, 1):
            print(f"{i}. [{ad['category']}] {ad['ad']}")
        return categorized




    ads = fetch_ads()
    categorized = categorize_ads(ads)
