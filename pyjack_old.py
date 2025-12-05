#!/usr/bin/env python3
"""
PyJack - Konsolen-Blackjack-Spiel
==================================

PyJack ist ein einfaches Blackjack-Spiel gegen einen Dealer mit Ergebnisverwaltung.
Das Spiel läuft in einer Menüschleife und speichert alle Ergebnisse in game_log.json.

Anforderungen (aus README):
- Interaktive Konsolenanwendung (Menü, Hit/Stand, Neustart)
- Datenvalidierung (Menüauswahl, Spielerentscheidungen, Fortsetzung)
- Dateiverarbeitung (game_log.json mit Zeitstempel)

Implementierte Funktionen:
- Deck mischen und austeilen
- Spielzustand anzeigen (Hände mit Kartenwerten)
- Spielerentscheidung (Hit/Stand)
- Dealer-Automatik (Hit bei <17, Stand bei ≥17)
- Gewinner ermitteln
- Ergebnis protokollieren
- Menü-Navigation und Validierung
"""

import json
import random
import os
from datetime import datetime
from typing import List, Dict, Tuple


# ============================================================================
# KONSTANTEN
# ============================================================================

KARTENWERTE: Dict[str, int] = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
    '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

GAME_LOG_FILE: str = "game_log.json"


# ============================================================================
# FUNKTIONEN: KARTENDECK-VERWALTUNG
# ============================================================================

def deck_erstellen() -> List[str]:
    """
    Erstellt ein Standard-Kartendeck mit 4 Farben und mischt es.

    Rückgabe:
        Liste von Kartenkennzeichen (z.B. ['A', '2', ..., 'K', 'A', ...])
    """
    deck = [karte for karte in KARTENWERTE.keys() for _ in range(4)]
    random.shuffle(deck)
    return deck


def kartenwert_berechnen(hand: List[str]) -> int:
    """
    Berechnet die Blackjack-Punktzahl einer Hand.

    Ass(e) zählen zunächst als 11, werden aber zu 1 (−10) reduziert,
    solange die Gesamtpunktzahl > 21 und noch Asse vorhanden sind.

    Parameter:
        hand: Liste von Kartenkennzeichen (z.B. ['A', 'K', '5'])

    Rückgabe:
        Gesamtpunktzahl als Integer
    """
    total = sum(KARTENWERTE[karte] for karte in hand)
    aces = hand.count('A')
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total


# ============================================================================
# FUNKTIONEN: SPIELABLAUF
# ============================================================================

def spielzustand_anzeigen(
    spieler_hand: List[str],
    dealer_hand: List[str],
    dealer_verborgen: bool = False
) -> None:
    """
    Zeigt den aktuellen Spielzustand an.

    Parameter:
        spieler_hand: Kartenliste des Spielers
        dealer_hand: Kartenliste des Dealers
        dealer_verborgen: True, wenn zweite Karte des Dealers noch verborgen ist
    """
    print("\n" + "="*50)

    # Dealer-Hand anzeigen
    if dealer_verborgen and len(dealer_hand) >= 2:
        print(f"Dealer Hand: [{dealer_hand[0]}, ??]")
    else:
        print(
            f"Dealer Hand: {dealer_hand} → {kartenwert_berechnen(dealer_hand)} Punkte")

    # Spieler-Hand anzeigen
    spieler_punkte = kartenwert_berechnen(spieler_hand)
    print(f"Spieler Hand: {spieler_hand} → {spieler_punkte} Punkte")
    print("="*50)


def spieler_zug(hand: List[str], deck: List[str]) -> List[str]:
    """
    Führt einen Spielerzug durch (Hit/Stand).

    Der Spieler wird solange nach Hit/Stand gefragt, bis er Stand wählt
    oder über 21 geht.

    Parameter:
        hand: Aktuelle Kartenliste des Spielers
        deck: Verbleibendes Kartendeck

    Rückgabe:
        Aktualisierte Kartenliste des Spielers
    """
    while kartenwert_berechnen(hand) < 21:
        print("\nDeine aktuelle Hand:")
        spielzustand_anzeigen(hand, [], dealer_verborgen=False)

        entscheidung = input("Hit (h) oder Stand (s)? ").strip().lower()

        # Validierung der Eingabe
        while entscheidung not in ['h', 's']:
            print("Ungültige Eingabe. Bitte 'h' (Hit) oder 's' (Stand) eingeben.")
            entscheidung = input("Hit (h) oder Stand (s)? ").strip().lower()

        if entscheidung == 'h':
            if deck:
                hand.append(deck.pop())
                print(f"→ Du erhältst: {hand[-1]}")
            else:
                print("Keine Karten mehr im Deck!")
                break
        else:  # 's'
            print("→ Du bleibst stehen.")
            break

    return hand


def dealer_zug(hand: List[str], deck: List[str]) -> List[str]:
    """
    Führt den Dealer-Automatik durch (Hit bis 17, dann Stand).

    Der Dealer zieht so lange Karten, bis die Punktzahl ≥ 17 ist.
    Dies ist die Standard-Blackjack-Dealer-Regel.

    Parameter:
        hand: Aktuelle Kartenliste des Dealers
        deck: Verbleibendes Kartendeck

    Rückgabe:
        Aktualisierte Kartenliste des Dealers
    """
    while kartenwert_berechnen(hand) < 17:
        if deck:
            hand.append(deck.pop())
            print(f"Dealer zieht: {hand[-1]}")
        else:
            print("Keine Karten mehr im Deck für den Dealer!")
            break
    return hand


def gewinner_ermitteln(
    spieler_punkte: int,
    dealer_punkte: int
) -> str:
    """
    Bestimmt den Gewinner basierend auf den Kartenwerten.

    Blackjack-Regeln:
    - > 21: Bust (automatisch verloren)
    - Dealer > 21: Spieler gewinnt (falls Spieler ≤ 21)
    - Gleiche Punkte: Unentschieden
    - Höhere Punkte: Gewinner

    Parameter:
        spieler_punkte: Kartenwert des Spielers
        dealer_punkte: Kartenwert des Dealers

    Rückgabe:
        String: "Spieler", "Dealer" oder "Unentschieden"
    """
    if spieler_punkte > 21:
        return "Dealer"
    elif dealer_punkte > 21:
        return "Spieler"
    elif spieler_punkte > dealer_punkte:
        return "Spieler"
    elif spieler_punkte < dealer_punkte:
        return "Dealer"
    else:
        return "Unentschieden"


# ============================================================================
# FUNKTIONEN: DATEIVERARBEITUNG & PROTOKOLLIERUNG
# ============================================================================

def game_log_laden() -> Dict:
    """
    Lädt die Spielhistorie aus game_log.json.

    Wenn die Datei nicht existiert, wird eine neue Struktur erstellt.

    Rückgabe:
        Dictionary mit Struktur:
        {
            "spiele": [...],
            "statistiken": {"spiele": N, "gewonnen_spieler": N, ...}
        }
    """
    if not os.path.exists(GAME_LOG_FILE):
        return {
            "spiele": [],
            "statistiken": {
                "spiele": 0,
                "gewonnen_spieler": 0,
                "gewonnen_dealer": 0,
                "unentschieden": 0
            }
        }

    try:
        with open(GAME_LOG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warnung: Fehler beim Laden von {GAME_LOG_FILE}: {e}")
        return {
            "spiele": [],
            "statistiken": {
                "spiele": 0,
                "gewonnen_spieler": 0,
                "gewonnen_dealer": 0,
                "unentschieden": 0
            }
        }


def game_log_speichern(log: Dict) -> None:
    """
    Speichert die Spielhistorie in game_log.json.

    Parameter:
        log: Dictionary mit Spielhistorie und Statistiken
    """
    try:
        with open(GAME_LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(log, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"Fehler beim Speichern von {GAME_LOG_FILE}: {e}")


def ergebnis_protokollieren(
    spieler_hand: List[str],
    dealer_hand: List[str],
    gewinner: str
) -> None:
    """
    Protokolliert ein Spielergebnis in game_log.json.

    Aktualisiert sowohl die Spielliste als auch die Gesamtstatistiken.

    Parameter:
        spieler_hand: Kartenliste des Spielers
        dealer_hand: Kartenliste des Dealers
        gewinner: String ("Spieler", "Dealer" oder "Unentschieden")
    """
    log = game_log_laden()

    # Neue Spieleinträge
    rundennummer = len(log["spiele"]) + 1
    spieler_punkte = kartenwert_berechnen(spieler_hand)
    dealer_punkte = kartenwert_berechnen(dealer_hand)

    neuer_eintrag = {
        "runde": rundennummer,
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "gewinner": gewinner,
        "karten": {
            "spieler": spieler_hand,
            "dealer": dealer_hand
        },
        "werte": {
            "spieler": spieler_punkte,
            "dealer": dealer_punkte
        }
    }

    log["spiele"].append(neuer_eintrag)

    # Statistiken aktualisieren
    log["statistiken"]["spiele"] += 1
    if gewinner == "Spieler":
        log["statistiken"]["gewonnen_spieler"] += 1
    elif gewinner == "Dealer":
        log["statistiken"]["gewonnen_dealer"] += 1
    else:  # Unentschieden
        log["statistiken"]["unentschieden"] += 1

    game_log_speichern(log)


# ============================================================================
# FUNKTIONEN: MENÜNAVIGATION & VALIDIERUNG
# ============================================================================

def menu_spielhistorie_anzeigen() -> None:
    """
    Zeigt die Spielhistorie und Statistiken aus game_log.json an.

    Wenn keine Spiele vorhanden sind, wird eine Meldung angezeigt.
    """
    log = game_log_laden()

    print("\n" + "="*60)
    print("SPIELHISTORIE & STATISTIKEN")
    print("="*60)

    # Statistiken anzeigen
    stats = log["statistiken"]
    print(f"\nGESAMTSTATISTIK:")
    print(f"  Gesamt gespielte Spiele: {stats['spiele']}")
    print(f"  Gewonnen (Spieler): {stats['gewonnen_spieler']}")
    print(f"  Gewonnen (Dealer): {stats['gewonnen_dealer']}")
    print(f"  Unentschieden: {stats['unentschieden']}")

    # Letzte Spiele anzeigen
    if log["spiele"]:
        print(f"\nLETZTE 5 SPIELE:")
        print("-"*60)
        for spiel in log["spiele"][-5:]:
            print(f"  Runde {spiel['runde']}: {spiel['start_time']}")
            print(f"    Gewinner: {spiel['gewinner']}")
            print(
                f"    Spieler: {spiel['karten']['spieler']} ({spiel['werte']['spieler']} Punkte)")
            print(
                f"    Dealer: {spiel['karten']['dealer']} ({spiel['werte']['dealer']} Punkte)")
            print()
    else:
        print("\nNo games recorded yet.")

    print("="*60 + "\n")


def menu_hauptmenu() -> str:
    """
    Zeigt das Hauptmenü und gibt die validierte Benutzerauswahl zurück.

    Rückgabe:
        String: "spielen", "historie" oder "beenden"
    """
    while True:
        print("\n" + "="*60)
        print("PYJACK - BLACKJACK-SPIEL")
        print("="*60)
        print("1. Spielen")
        print("2. Spielhistorie anzeigen")
        print("3. Beenden")
        print("="*60)

        wahl = input("Wähle eine Option (1/2/3): ").strip()

        if wahl == "1":
            return "spielen"
        elif wahl == "2":
            return "historie"
        elif wahl == "3":
            return "beenden"
        else:
            print("Ungültige Eingabe. Bitte 1, 2 oder 3 eingeben.")


def frage_neustart() -> bool:
    """
    Fragt den Spieler, ob er eine neue Runde spielen möchte.

    Rückgabe:
        True, wenn neue Runde, False sonst
    """
    while True:
        antwort = input(
            "Möchtest du eine weitere Runde spielen? (j/n): ").strip().lower()
        if antwort == 'j':
            return True
        elif antwort == 'n':
            return False
        else:
            print("Ungültige Eingabe. Bitte 'j' (Ja) oder 'n' (Nein) eingeben.")


# ============================================================================
# FUNKTIONEN: HAUPTSPIELABLAUF
# ============================================================================

def spiel_durchfuehren() -> None:
    """
    Führt eine komplette Blackjack-Spielrunde durch.

    Ablauf:
    1. Deck erstellen und Karten austeilen
    2. Spielzustand anzeigen
    3. Spieler-Zug (Hit/Stand)
    4. Dealer-Zug (Automatik)
    5. Gewinner ermitteln und anzeigen
    6. Ergebnis protokollieren
    """
    # 1. Deck erstellen, Karten austeilen
    deck = deck_erstellen()
    spieler_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    print("\n" + "="*50)
    print("NEUE RUNDE GESTARTET!")
    print("="*50)

    # 2. Spielzustand anzeigen (Dealer-Karte verborgen)
    spielzustand_anzeigen(spieler_hand, dealer_hand, dealer_verborgen=True)

    # 3. Spieler-Zug
    spieler_hand = spieler_zug(spieler_hand, deck)
    spieler_punkte = kartenwert_berechnen(spieler_hand)

    # Wenn Spieler über 21 ist, endet das Spiel
    if spieler_punkte > 21:
        print("\n❌ BUST! Du hast über 21 Punkte. Du hast verloren!")
        spielzustand_anzeigen(spieler_hand, dealer_hand,
                              dealer_verborgen=False)
        ergebnis_protokollieren(spieler_hand, dealer_hand, "Dealer")
        return

    # 4. Dealer-Zug (Automatik)
    print("\nDealer spielt automatisch...")
    dealer_hand = dealer_zug(dealer_hand, deck)
    dealer_punkte = kartenwert_berechnen(dealer_hand)

    # 5. Gewinner ermitteln und anzeigen
    gewinner = gewinner_ermitteln(spieler_punkte, dealer_punkte)

    print("\n" + "="*50)
    print("RUNDENERGEBNIS")
    print("="*50)
    spielzustand_anzeigen(spieler_hand, dealer_hand, dealer_verborgen=False)

    if gewinner == "Spieler":
        print("🎉 DU HAST GEWONNEN!")
    elif gewinner == "Dealer":
        if dealer_punkte > 21:
            print("🎉 DEALER BUST! DU HAST GEWONNEN!")
        else:
            print("❌ DEALER GEWINNT!")
    else:  # Unentschieden
        print("🤝 UNENTSCHIEDEN!")

    print("="*50 + "\n")

    # 6. Ergebnis protokollieren
    ergebnis_protokollieren(spieler_hand, dealer_hand, gewinner)


# ============================================================================
# HAUPTPROGRAMM
# ============================================================================

def main() -> None:
    """
    Hauptprogramm: Menüschleife für PyJack.

    Ermöglicht dem Spieler, Spiele zu spielen, Statistiken anzusehen
    oder das Programm zu beenden.
    """
    print("\n" + "="*60)
    print("Willkommen zu PyJack!")
    print("="*60)

    while True:
        wahl = menu_hauptmenu()

        if wahl == "spielen":
            while True:
                spiel_durchfuehren()
                if not frage_neustart():
                    break

        elif wahl == "historie":
            menu_spielhistorie_anzeigen()

        elif wahl == "beenden":
            print("\nAuf Wiedersehen! 👋")
            break


if __name__ == "__main__":
    main()
