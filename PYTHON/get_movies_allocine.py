import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.allocine.fr/films/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/141.0.0.0 Safari/537.36"
}

response = requests.get(URL, headers=HEADERS)
if response.status_code != 200:
    print("Erreur de connexion :", response.status_code)
    exit()

soup = BeautifulSoup(response.text, "html.parser")

films = []
for card in soup.find_all("div", class_="card entity-card entity-card-list cf"):
    title_tag = card.find("a", class_="meta-title-link")
    if title_tag:
        title = title_tag.get_text(strip=True)
        link = "https://www.allocine.fr" + title_tag["href"]

        genre_tag = card.find("span", class_="meta-body-item meta-body-info")
        genre = genre_tag.get_text(strip=True) if genre_tag else "Genre inconnu"

        date_tag = card.find("span", class_="date")
        date = date_tag.get_text(strip=True) if date_tag else "Date inconnue"

        films.append({
            "title": title,
            "link": link,
            "genre": genre,
            "release_date": date
        })

with open("films_a_l_affiche.json", "w", encoding="utf-8") as f:
    json.dump(films, f, ensure_ascii=False, indent=4)

print(f"{len(films)} films récupérés et sauvegardés dans 'films_a_l_affiche.json'")
