import requests

# Nombre de pubs à récupérer
N = 10

print("Récupération des pubs :\n")

for i in range(N):
    url = "https://api.isevenapi.xyz/api/iseven/1/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            ad_message = data.get("ad", "Pas de pub disponible")
            print(f"Pub {i+1} : {ad_message}")
        else:
            print(f"Erreur requête {i+1} : {response.status_code}")
    except Exception as e:
        print(f"Erreur requête {i+1} :", e)
