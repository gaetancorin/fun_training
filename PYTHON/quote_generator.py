import json
import random
import os

FILE = "quotes.json"

if os.path.exists(FILE):
    with open(FILE, "r", encoding="utf-8") as f:
        quotes = json.load(f)
else:
    quotes = []

def save_quotes():
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(quotes, f, ensure_ascii=False, indent=2)

def add_quote():
    quote = input("Entrez la citation : ").strip()
    author = input("Auteur (optionnel) : ").strip()
    if quote:
        quotes.append({"quote": quote, "author": author})
        save_quotes()
        print("✅ Citation ajoutée !")
    else:
        print("⚠ La citation ne peut pas être vide.")

def random_quote():
    if not quotes:
        print("⚠ Aucune citation disponible.")
        return
    q = random.choice(quotes)
    author = f" — {q['author']}" if q['author'] else ""
    print(f"\n\"{q['quote']}\"{author}\n")

def show_menu():
    print("\n📜 Générateur de citations aléatoires")
    print("1. Afficher une citation aléatoire")
    print("2. Ajouter une citation")
    print("3. Lister toutes les citations")
    print("4. Quitter")

while True:
    show_menu()
    choice = input("Votre choix : ").strip()
    if choice == "1":
        random_quote()
    elif choice == "2":
        add_quote()
    elif choice == "3":
        if quotes:
            print("\nToutes les citations :")
            for i, q in enumerate(quotes, 1):
                author = f" — {q['author']}" if q['author'] else ""
                print(f"{i}. \"{q['quote']}\"{author}")
        else:
            print("⚠ Aucune citation disponible.")
    elif choice == "4":
        print("Au revoir ! 👋")
        break
    else:
        print("⚠ Choix invalide. Réessayez.")
