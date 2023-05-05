# budget_tracker.py
# Pour lancer : python budget_tracker.py

import json
import os
from datetime import datetime
import matplotlib.pyplot as plt

FILE = "budget_data.json"

# Charger les données existantes
if os.path.exists(FILE):
    with open(FILE, "r") as f:
        data = json.load(f)
else:
    data = []

def save_data():
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_transaction():
    type_ = input("Type (revenu/dépense) : ").strip().lower()
    if type_ not in ("revenu", "depense"):
        print("⚠ Type invalide")
        return
    amount = input("Montant : ")
    try:
        amount = float(amount)
    except ValueError:
        print("⚠ Montant invalide")
        return
    description = input("Description : ").strip()
    date = datetime.now().strftime("%Y-%m-%d")
    transaction = {
        "type": type_,
        "amount": amount,
        "description": description,
        "date": date
    }
    data.append(transaction)
    save_data()
    print("✅ Transaction ajoutée !")

def show_summary():
    revenus = sum(t["amount"] for t in data if t["type"] == "revenu")
    depenses = sum(t["amount"] for t in data if t["type"] == "depense")
    solde = revenus - depenses
    print("\n📊 Résumé :")
    print(f"Revenus : {revenus} €")
    print(f"Dépenses : {depenses} €")
    print(f"Solde : {solde} €\n")

def show_transactions():
    if not data:
        print("Aucune transaction.")
        return
    print("\n📝 Transactions :")
    for t in data:
        print(f"{t['date']} - {t['type'].capitalize()} - {t['amount']} € - {t['description']}")
    print()

def plot_graph():
    if not data:
        print("Aucune donnée pour afficher le graphique.")
        return
    dates = [t["date"] for t in data]
    revenus = [t["amount"] if t["type"]=="revenu" else 0 for t in data]
    depenses = [t["amount"] if t["type"]=="depense" else 0 for t in data]
    cum_revenus, cum_depenses, cum_solde = [], [], []
    total_revenus, total_depenses = 0, 0
    for r, d in zip(revenus, depenses):
        total_revenus += r
        total_depenses += d
        cum_revenus.append(total_revenus)
        cum_depenses.append(total_depenses)
        cum_solde.append(total_revenus - total_depenses)
    plt.figure(figsize=(10,5))
    plt.plot(dates, cum_revenus, label="Revenus", color="green", marker="o")
    plt.plot(dates, cum_depenses, label="Dépenses", color="red", marker="o")
    plt.plot(dates, cum_solde, label="Solde", color="blue", marker="o")
    plt.xticks(rotation=45)
    plt.title("Budget Tracker")
    plt.xlabel("Date")
    plt.ylabel("Montant (€)")
    plt.legend()
    plt.tight_layout()
    plt.show()

def main():
    while True:
        print("\n=== Mini Budget Tracker ===")
        print("1. Ajouter une transaction")
        print("2. Afficher résumé")
        print("3. Afficher transactions")
        print("4. Afficher graphique")
        print("5. Quitter")
        choice = input("Choix : ")
        if choice == "1":
            add_transaction()
        elif choice == "2":
            show_summary()
        elif choice == "3":
            show_transactions()
        elif choice == "4":
            plot_graph()
        elif choice == "5":
            print("Au revoir !")
            break
        else:
            print("⚠ Choix invalide")

if __name__ == "__main__":
    main()
