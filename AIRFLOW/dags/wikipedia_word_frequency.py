from airflow import DAG
from airflow.decorators import task
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from collections import Counter
import matplotlib.pyplot as plt
import re
import os
import json
import time

DATA_DIR = "/opt/airflow/data"
os.makedirs(DATA_DIR, exist_ok=True)

NUM_PAGES = 10
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/141.0.0.0 Safari/537.36"
}

with DAG(
    dag_id="wikipedia_word_frequency",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
):

    @task()
    def scrape_pages(num_pages: int = NUM_PAGES):
        all_words = []
        for i in range(num_pages):
            print(f"Scraping page {i+1}/{num_pages}...")
            url = "https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard"
            resp = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(resp.text, "html.parser")
            text = " ".join([p.get_text() for p in soup.find_all("p")]).lower()
            words = re.findall(r'\b\w+\b', text)
            all_words.extend(words)
            time.sleep(1)  # avoid overloading Wikipedia

        words_path = os.path.join(DATA_DIR, "wikipedia_words.json")
        with open(words_path, "w") as f:
            json.dump(all_words, f)
        print(f"✅ Scraping terminé, {len(all_words)} mots récupérés.")
        return words_path

    @task()
    def compute_word_counts(words_path: str):
        with open(words_path) as f:
            words = json.load(f)

        counter = Counter(words)
        most_common = counter.most_common(50)

        counts_path = os.path.join(DATA_DIR, "wikipedia_word_counts.json")
        with open(counts_path, "w") as f:
            json.dump(most_common, f, indent=2)
        print("✅ Comptage des mots terminé.")
        return counts_path


    words_path = scrape_pages()
    counts_path = compute_word_counts(words_path)
