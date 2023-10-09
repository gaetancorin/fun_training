import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

URL = "https://www.lemonde.fr"  # site à scraper
HEADERS = {"User-Agent": "Mozilla/5.0"}


def fetch_articles(limit=10):
    response = requests.get(URL, headers=HEADERS)
    if response.status_code != 200:
        print("Erreur de connexion :", response.status_code)
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    links_seen = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/article/" in href:
            title = a.get_text(strip=True)
            if len(title) < 5:  # ignore les titres trop courts
                continue
            link = href if href.startswith("http") else URL + href

            if link in links_seen:
                continue
            links_seen.add(link)

            # Petite "feature" utile : résumé (les 50 premiers caractères du titre)
            summary = title[:50] + ("…" if len(title) > 50 else "")

            articles.append({
                "title": title,
                "link": link,
                "summary": summary,
                "timestamp": datetime.now().isoformat()
            })

            if len(articles) >= limit:
                break

    return articles


def save_articles_json(articles, filename="articles_recent.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)
    print(f"{len(articles)} articles sauvegardés dans {filename}")


if __name__ == "__main__":
    articles = fetch_articles(limit=15)
    save_articles_json(articles)
