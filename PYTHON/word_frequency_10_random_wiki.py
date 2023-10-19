import requests
from bs4 import BeautifulSoup
from collections import Counter
import matplotlib.pyplot as plt
import re
import time

NUM_PAGES = 10
all_words = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/141.0.0.0 Safari/537.36"
}

for i in range(NUM_PAGES):
    print(f"Scraping page {i+1}/{NUM_PAGES}...")
    url = "https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard"
    resp = requests.get(url, headers=headers, allow_redirects=True)
    soup = BeautifulSoup(resp.text, "html.parser")

    # Extraire texte des paragraphes
    text = " ".join([p.get_text() for p in soup.find_all("p")]).lower()
    words = re.findall(r'\b\w+\b', text)
    all_words.extend(words)

    time.sleep(1)  # éviter de surcharger Wikipedia

# Compter la fréquence globale
counter = Counter(all_words)
most_common = counter.most_common(50)

# Préparer les données pour le graphique
labels, values = zip(*most_common)

# Afficher l'histogramme
plt.figure(figsize=(12,6))
plt.bar(labels, values, color='skyblue')
plt.xticks(rotation=45, ha='right')
plt.title(f"Top 20 mots les plus fréquents sur {NUM_PAGES} pages Wikipedia aléatoires")
plt.ylabel("Occurrences")
plt.tight_layout()
plt.show()
