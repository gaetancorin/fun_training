import requests

# --- Paramètres ---
N = 5  # nombre de paragraphes à récupérer

# --- 1. Appel à l'API Bacon Ipsum ---
url = f"https://baconipsum.com/api/?type=meat-and-filler&paras={N}"
response = requests.get(url)

if response.status_code == 200:
    paragraphs = response.json()  # renvoie une liste de paragraphes
    print(f"{len(paragraphs)} paragraphes récupérés :\n")
    for i, para in enumerate(paragraphs, 1):
        print(f"Paragraphe {i} : {para}\n")
else:
    print("Erreur lors de la récupération :", response.status_code)
