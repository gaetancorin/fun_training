import random

CODE_LENGTH = 4
MAX_ATTEMPTS = 10
COLORS = [1, 2, 3, 4, 5, 6]  # ou ["R","G","B","Y","O","P"]

def generate_code():
    return [random.choice(COLORS) for _ in range(CODE_LENGTH)]

def get_guess():
    while True:
        guess_input = input(f"Entrez {CODE_LENGTH} chiffres (1-6) sans espaces : ").strip()
        if len(guess_input) != CODE_LENGTH:
            print(f"Erreur : il faut {CODE_LENGTH} chiffres.")
            continue
        try:
            guess = [int(ch) for ch in guess_input]
            if all(x in COLORS for x in guess):
                return guess
            else:
                print(f"Les chiffres doivent être entre {min(COLORS)} et {max(COLORS)}.")
        except ValueError:
            print("Entrée invalide, uniquement des chiffres.")

def evaluate_guess(code, guess):
    # Calcul des ✅
    correct_pos = sum(c == g for c, g in zip(code, guess))

    # Préparer les restes pour ⚪
    code_remaining = []
    guess_remaining = []
    for c, g in zip(code, guess):
        if c != g:
            code_remaining.append(c)
            guess_remaining.append(g)

    # Calcul des ⚪
    correct_color = 0
    for g in guess_remaining:
        if g in code_remaining:
            correct_color += 1
            code_remaining.remove(g)  # retire pour ne pas compter deux fois

    return correct_pos, correct_color

def main():
    code = generate_code()
    attempts = 0
    print("Bienvenue dans Mastermind !")
    print(f"Devinez le code secret de {CODE_LENGTH} chiffres (1-6). Vous avez {MAX_ATTEMPTS} essais.\n")

    while attempts < MAX_ATTEMPTS:
        guess = get_guess()
        attempts += 1

        correct_pos, correct_color = evaluate_guess(code, guess)

        print(f"Résultat : ✅ {correct_pos} | ⚪ {correct_color}  (Tentative {attempts}/{MAX_ATTEMPTS})\n")

        if correct_pos == CODE_LENGTH:
            print(f"🎉 Félicitations ! Vous avez trouvé le code {code} en {attempts} essais !")
            break
    else:
        print(f"😢 Vous avez perdu ! Le code était : {code}")

if __name__ == "__main__":
    main()
