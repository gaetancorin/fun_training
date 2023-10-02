import random

CODE_LENGTH = 4
MAX_ATTEMPTS = 10
COLORS = [1, 2, 3, 4, 5, 6]  # ou ["R","G","B","Y","O","P"]


def generate_code():
    return [random.choice(COLORS) for _ in range(CODE_LENGTH)]


def get_guess():
    while True:
        guess = input(f"Entrez {CODE_LENGTH} chiffres (1-6) séparés par espace : ").split()
        if len(guess) != CODE_LENGTH:
            print(f"Erreur : il faut {CODE_LENGTH} chiffres.")
            continue
        try:
            guess = [int(x) for x in guess]
            if all(x in COLORS for x in guess):
                return guess
            else:
                print(f"Les chiffres doivent être entre {min(COLORS)} et {max(COLORS)}.")
        except ValueError:
            print("Entrée invalide, uniquement des chiffres.")


def evaluate_guess(code, guess):
    # Comptage des ✅ et ⚪
    correct_pos = sum(c == g for c, g in zip(code, guess))
    # Pour les bons chiffres au mauvais endroit
    code_counts = {x: code.count(x) for x in set(code)}
    guess_counts = {x: guess.count(x) for x in set(guess)}
    correct_color = sum(min(code_counts.get(x, 0), guess_counts.get(x, 0)) for x in guess_counts.values())
    correct_color = correct_color - correct_pos  # enlever les ✅
    return correct_pos, correct_color


def main():
    code = generate_code()
    attempts = 0
    print("Bienvenue dans Mastermind !")
    print(f"Devinez le code secret de {CODE_LENGTH} chiffres (1-6). Vous avez {MAX_ATTEMPTS} essais.\n")

    while attempts < MAX_ATTEMPTS:
        guess = get_guess()
        attempts += 1
        correct_pos = sum(c == g for c, g in zip(code, guess))
        # Calcul des bonnes couleurs au mauvais endroit
        code_counts = {x: code.count(x) for x in set(code)}
        guess_counts = {x: guess.count(x) for x in set(guess)}
        correct_color = sum(min(code_counts.get(x, 0), guess_counts.get(x, 0)) for x in guess_counts)
        correct_color -= correct_pos

        print(f"Résultat : ✅ {correct_pos} | ⚪ {correct_color}  (Tentative {attempts}/{MAX_ATTEMPTS})\n")

        if correct_pos == CODE_LENGTH:
            print(f"🎉 Félicitations ! Vous avez trouvé le code {code} en {attempts} essais !")
            break
    else:
        print(f"😢 Vous avez perdu ! Le code était : {code}")


if __name__ == "__main__":
    main()
