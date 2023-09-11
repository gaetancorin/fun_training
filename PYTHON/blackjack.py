import random

# Création du paquet de cartes (valeurs 2-10, J, Q, K = 10, A = 11)
def create_deck():
    deck = [2,3,4,5,6,7,8,9,10,10,10,10,11]*4
    random.shuffle(deck)
    return deck

# Calcul du score d'une main
def calculate_score(hand):
    score = sum(hand)
    # Ajustement des As (11->1) si score >21
    aces = hand.count(11)
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score

# Affichage main
def show_hand(hand, hide_first=False):
    if hide_first:
        return "[?] " + " ".join(str(card) for card in hand[1:])
    return " ".join(str(card) for card in hand)

# Tour du joueur
def player_turn(deck, player_hand):
    while True:
        score = calculate_score(player_hand)
        print(f"Votre main : {show_hand(player_hand)} | Score : {score}")
        if score > 21:
            print("💥 Vous avez dépassé 21 !")
            return score
        choice = input("Voulez-vous tirer (t) ou rester (r) ? ").lower()
        if choice == 't':
            player_hand.append(deck.pop())
        elif choice == 'r':
            return score
        else:
            print("Choix invalide, tapez 't' ou 'r'.")

# Tour du dealer
def dealer_turn(deck, dealer_hand):
    while calculate_score(dealer_hand) < 17:
        dealer_hand.append(deck.pop())
    return calculate_score(dealer_hand)

# Partie de Blackjack
def play_blackjack():
    deck = create_deck()
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    print(f"Main du dealer : {show_hand(dealer_hand, hide_first=True)}")

    player_score = player_turn(deck, player_hand)
    if player_score > 21:
        print("Le dealer gagne !")
        return

    dealer_score = dealer_turn(deck, dealer_hand)
    print(f"Main du dealer : {show_hand(dealer_hand)} | Score : {dealer_score}")

    if dealer_score > 21 or player_score > dealer_score:
        print("🎉 Vous gagnez !")
    elif player_score < dealer_score:
        print("Le dealer gagne !")
    else:
        print("Égalité !")

# Boucle principale
def main():
    print("Bienvenue au Blackjack !")
    while True:
        play_blackjack()
        again = input("Voulez-vous rejouer ? (o/n) ").lower()
        if again != 'o':
            print("Merci d'avoir joué !")
            break

if __name__ == "__main__":
    main()
