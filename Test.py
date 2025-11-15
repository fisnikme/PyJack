# Kartenwerte
import random


karten = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
    '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

# Kartenstapel erstellen


def kartenstapel_erstellen():
    deck = [karte for karte in karten.keys() for _ in range(4)]
    random.shuffle(deck)
    return deck

# Punktzahl berechnen


def punkte(hand):
    """
    Berechnet die Gesamtpunktzahl einer Hand.
    Ass(e) zählen zunächst als 11 Punkte, werden aber zu 1 Punkt umgewandelt,
    falls die Gesamtpunktzahl über 21 liegt, indem für jedes Ass 10 Punkte abgezogen werden,
    bis die Punktzahl 21 oder weniger beträgt oder keine Asse mehr übrig sind.
    """
    total = sum(karten[karte] for karte in hand)
    # Ass als 1 zählen, wenn nötig
    aces = hand.count('A')
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total


def zeige_hand(hand, name):
    """
    Zeigt die aktuelle Hand und Punktzahl eines Spielers oder Dealers an.

    Parameters:
        hand (list): Die Kartenhand des Spielers oder Dealers.
        name (str): Der Name des Spielers oder Dealers.

    Output:
        Gibt die Hand und die berechnete Punktzahl auf der Konsole aus.
    """
    print(f"{name} Hand: {hand} → Punkte: {punkte(hand)}")
# Entfernte fehlerhafte und doppelte blackjack-Definition und zeige_hand-Definition

# Spiel starten


def blackjack():
    deck = kartenstapel_erstellen()
    spieler = [deck.pop(), deck.pop()]
    dealer = [deck.pop(), deck.pop()]

    print("Willkommen bei Blackjack!")
    zeige_hand(spieler, "Spieler")
    # Dealerzug
    while punkte(dealer) < 17:
        if not deck:
            print("Das Deck ist leer. Keine Karten mehr zum Ziehen für den Dealer.")
            break
        dealer.append(deck.pop())
        if zug == 'j':
            if deck:
                spieler.append(deck.pop())
                zeige_hand(spieler, "Spieler")
            else:
                print("Keine Karten mehr im Deck!")
                break
        else:
            break
    while punkte(dealer) < 17:
        if deck:
            dealer.append(deck.pop())
        else:
            print("Keine Karten mehr im Deck für den Dealer!")
            break
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
