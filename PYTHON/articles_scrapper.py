# scrap_recent_articles.py
import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.lemonde.fr"  # site à scraper
HEADERS = {"User-Agent": "Mozilla/5.0"}  # éviter les blocages


def fetch_articles():
    response = requests.get(URL, headers=HEADERS)
    if response.status_code != 200:
        print("Erreur de connexion :", response.status_code)
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    # Ici on prend les liens dans les <a> contenant 'article' dans l'URL
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/article/" in href:
            title = a.get_text(strip=True)
            link = href if href.startswith("http") else URL + href
            if title and link not in [x["link"] for x in articles]:
                articles.append({"title": title, "link": link})

    return articles[:10]  # on garde les 10 premiers articles


def save_articles(articles, filename="articles_recent.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)
    print(f"{len(articles)} articles sauvegardés dans {filename}")


if __name__ == "__main__":
    articles = fetch_articles()
    save_articles(articles)
