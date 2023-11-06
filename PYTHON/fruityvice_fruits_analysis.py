import requests
import matplotlib.pyplot as plt

# --- 1. Récupérer les données depuis l'API ---
url = "https://www.fruityvice.com/api/fruit/all"
response = requests.get(url)
if response.status_code != 200:
    print("Erreur API :", response.status_code)
    exit()

fruits = response.json()

# --- 2. Trier les fruits par calories décroissantes ---
fruits_sorted = sorted(fruits, key=lambda x: x['nutritions']['calories'], reverse=True)

# --- 3. Préparer les données pour le top 10 ---
top_fruits = fruits_sorted[:30]
names = [fruit['name'] for fruit in top_fruits]
calories = [fruit['nutritions']['calories'] for fruit in top_fruits]

# --- 4. Afficher le top 10 dans la console ---
print("Top 10 fruits les plus caloriques :")
for name, cal in zip(names, calories):
    print(f"{name} : {cal} calories")

# --- 5. Graphique ---
plt.figure(figsize=(10,6))
plt.bar(names, calories, color='tomato')
plt.xticks(rotation=45, ha='right')
plt.ylabel("Calories")
plt.title("Top 10 fruits les plus caloriques (Fruityvice API)")
plt.tight_layout()
plt.show()
