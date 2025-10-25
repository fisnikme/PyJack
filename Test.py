# Kartenwerte
karten = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
    '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

# Kartenstapel erstellen


def kartenstapel_erstellen():
    deck = list(karten.keys()) * 4
    random.shuffle(deck)
    return deck

# Punktzahl berechnen


def punkte(hand):
    total = sum(karten[karte] for karte in hand)
    # Ass als 1 zählen, wenn nötig
    aces = hand.count('A')
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total


while True:

    # Hand anzeigen


def zeige_hand(hand, name):
    print(f"{name} Hand: {hand} → Punkte: {punkte(hand)}")

# Spiel starten


def blackjack():
    deck = kartenstapel_erstellen()
    spieler = [deck.pop(), deck.pop()]
    dealer = [deck.pop(), deck.pop()]

    print("Willkommen bei Blackjack!")
    zeige_hand(spieler, "Spieler")
    print(f"Dealer zeigt: {dealer[0]}")

    # Spielerzug
    while punkte(spieler) < 21:
        zug = input("Möchtest du eine Karte ziehen? (j/n): ").lower()
        if zug == 'j':
            spieler.append(deck.pop())
            zeige_hand(spieler, "Spieler")
        else:
            break

    # Dealerzug
    while punkte(dealer) < 17:
        dealer.append(deck.pop())

    print("\nEndstand:")
    zeige_hand(spieler, "Spieler")
    zeige_hand(dealer, "Dealer")

    # Gewinner bestimmen
    spieler_punkte = punkte(spieler)
    dealer_punkte = punkte(dealer)

    if spieler_punkte > 21:
        print("Du hast verloren – über 21!")
    elif dealer_punkte > 21 or spieler_punkte > dealer_punkte:
        print("Du hast gewonnen!")
    elif spieler_punkte == dealer_punkte:
        print("Unentschieden!")
    else:
        print("Dealer gewinnt!")


# Spiel ausführen
blackjack()
