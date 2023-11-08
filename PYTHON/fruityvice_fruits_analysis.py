import requests
import matplotlib.pyplot as plt

# --- 1. Récupérer les données depuis l'API ---
url = "https://www.fruityvice.com/api/fruit/all"
response = requests.get(url)
if response.status_code != 200:
    print("Erreur API :", response.status_code)
    exit()

fruits = response.json()

# --- 2. Top 10 fruits les plus caloriques ---
fruits_by_calories = sorted(fruits, key=lambda x: x['nutritions']['calories'], reverse=True)
top_calories = fruits_by_calories[:10]
names_cal = [fruit['name'] for fruit in top_calories]
calories = [fruit['nutritions']['calories'] for fruit in top_calories]

print("Top 10 fruits les plus caloriques :")
for name, cal in zip(names_cal, calories):
    print(f"{name} : {cal} calories")

# --- 3. Top 10 fruits avec le plus de protéines ---
fruits_by_protein = sorted(fruits, key=lambda x: x['nutritions']['protein'], reverse=True)
top_protein = fruits_by_protein[:10]
names_prot = [fruit['name'] for fruit in top_protein]
proteins = [fruit['nutritions']['protein'] for fruit in top_protein]

print("\nTop 10 fruits les plus riches en protéines :")
for name, prot in zip(names_prot, proteins):
    print(f"{name} : {prot} g de protéines")

# --- 4. Graphiques ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10,12))

# Calories
ax1.bar(names_cal, calories, color='tomato')
ax1.set_ylabel("Calories")
ax1.set_title("Top 10 fruits les plus caloriques")
ax1.set_xticklabels(names_cal, rotation=45, ha='right')

# Protéines
ax2.bar(names_prot, proteins, color='lightgreen')
ax2.set_ylabel("Protéines (g)")
ax2.set_title("Top 10 fruits les plus riches en protéines")
ax2.set_xticklabels(names_prot, rotation=45, ha='right')

plt.tight_layout()
plt.show()
