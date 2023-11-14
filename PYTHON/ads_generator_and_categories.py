import requests

N = 10

ads = []

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

for i in range(N):
    url = "https://api.isevenapi.xyz/api/iseven/1/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            ad_message = data.get("ad", "Pas de pub disponible")
            category = categorize_ad(ad_message)
            ads.append((ad_message, category))
            print(f"Pub {i+1} [{category}] : {ad_message}")
        else:
            print(f"Erreur requête {i+1} : {response.status_code}")
    except Exception as e:
        print(f"Erreur requête {i+1} :", e)
