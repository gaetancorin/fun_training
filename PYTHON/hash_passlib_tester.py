from passlib.hash import bcrypt

# Stockage du hash en mémoire
PASSWORD_HASH = None

def store_password():
    global PASSWORD_HASH
    pwd = input("Entrez un mot de passe à stocker : ")
    PASSWORD_HASH = bcrypt.hash(pwd)  # génère salt automatiquement
    print("Hash du mot de passe stocké en mémoire.")

def verify_password():
    if PASSWORD_HASH is None:
        print("Aucun mot de passe stocké. Lancez d'abord le mode store.")
        return
    pwd = input("Redonnez le mot de passe : ")
    ok = bcrypt.verify(pwd, PASSWORD_HASH)
    print("✅ Mot de passe correct" if ok else "❌ Mot de passe incorrect")

def main():
    while True:
        mode = input("Mode (store: 's' / verify: 'v' / quit: 'q') : ").strip().lower()
        if mode == 'q':
            break
        elif mode == 's':
            store_password()
        elif mode == 'v':
            verify_password()
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    main()
