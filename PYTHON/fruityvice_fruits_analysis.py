import requests
import matplotlib.pyplot as plt

# --- 1. Récupérer les données depuis l'API ---
url = "https://www.fruityvice.com/api/fruit/all"
response = requests.get(url)
if response.status_code != 200:
    print("Erreur API :", response.status_code)
    exit()

fruits = response.json()

# --- 2. Extraire certaines données pour analyse ---
names = [fruit['name'] for fruit in fruits]
calories = [fruit['nutritions']['calories'] for fruit in fruits]
sugar = [fruit['nutritions']['sugar'] for fruit in fruits]

# --- 3. Afficher les 5 fruits les plus caloriques ---
top_calories = sorted(zip(names, calories), key=lambda x: x[1], reverse=True)[:5]
print("Top 5 fruits les plus caloriques :")
for name, cal in top_calories:
    print(f"{name} : {cal} calories")

# --- 4. Graphique calories vs fruits ---
plt.figure(figsize=(12,6))
plt.bar(names, calories, color='orange')
plt.xticks(rotation=45, ha='right')
plt.ylabel("Calories")
plt.title("Calories par fruit (Fruityvice API)")
plt.tight_layout()
plt.show()
