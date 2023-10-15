import requests
from bs4 import BeautifulSoup
from collections import Counter
import matplotlib.pyplot as plt
import re

# --- 1. Page Wikipedia aléatoire ---
url = "https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/141.0.0.0 Safari/537.36"
}
resp = requests.get(url, headers=headers, allow_redirects=True)
soup = BeautifulSoup(resp.text, "html.parser")

# --- 2. Récupérer le titre ---
h1_tag = soup.find("h1")
title = h1_tag.get_text() if h1_tag else "Titre inconnu"

# --- 3. Récupérer le texte ---
text = " ".join([p.get_text() for p in soup.find_all("p")]).lower()

# --- 4. Nettoyer et extraire les mots ---
words = re.findall(r'\b\w+\b', text)

# --- 5. Compter la fréquence ---
counter = Counter(words)
most_common = counter.most_common(20)

# --- 6. Préparer les données pour le graphique ---
if most_common:
    labels, values = zip(*most_common)

    # --- 7. Afficher l'histogramme ---
    plt.figure(figsize=(12,6))
    plt.bar(labels, values, color='skyblue')
    plt.xticks(rotation=45, ha='right')
    plt.title(f"Top 20 mots fréquents - {title}")
    plt.ylabel("Occurrences")
    plt.tight_layout()
    plt.show()
else:
    print("Aucun mot trouvé dans l'article.")
