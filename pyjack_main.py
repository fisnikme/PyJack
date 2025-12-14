import json
import random
import os  # Library um mit dem JSON zu interagieren
from datetime import datetime

# Mapping von Kartenkennzeichen zu Punktwerten
KARTENWERTE = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
    '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

GAME_LOG_FILE = "game_log.json"

# Basisstruktur für den Log zur wiederverwendung im Code
DEFAULT_LOG = {
    "spiele": [],
    "statistiken": {
        "spiele": 0,
        "gewonnen_spieler": 0,
        "gewonnen_dealer": 0,
        "unentschieden": 0
    }
}


def deck_erstellen():
    # Erstellt ein Standard-Kartendeck und mischt es.
    # Rückgabe: Liste von Kartenkennzeichen (['A', '2'])
    deck = [karte for karte in KARTENWERTE.keys() for _ in range(4)]
    random.shuffle(deck)
    return deck


def kartenwert_berechnen(hand):
    punkte = 0  # Sicherheitsaspekt, damit vor Berechnug Punkte = 0
    for karte in hand:
        punkte += KARTENWERTE.get(karte, 0)  # Gibt den Kartenwert zurück
    # Asse bei Bedarf von 11 auf 1 reduzieren, wenn Punkte über 21
    anzahl_asse = hand.count('A')
    while punkte > 21 and anzahl_asse > 0:
        punkte -= 10  # Ein Ass von 11 auf 1 reduzieren
        anzahl_asse -= 1
    return punkte

# FUNKTIONEN: SPIELABLAUF


def spielzustand_anzeigen(spieler_hand, dealer_hand, dealer_verborgen=False):
    # Zeigt den aktuellen Spielzustand an.
    # dealer_verborgen: True wenn zweite Karte des Dealers noch verborgen

    print("\n" + "="*50)

    # Dealer-Hand anzeigen
    if dealer_verborgen and len(dealer_hand) >= 2:
        # Nur die erste Karte wird gezeigt
        print(f"Dealer Hand: [{dealer_hand[0]}, ??]")
    else:
        # Dealer-Hand wird komplett gezeigt
        print(
            f"Dealer Hand: {dealer_hand} → {kartenwert_berechnen(dealer_hand)} Punkte")

    # Spieler-Hand anzeigen
    spieler_punkte = kartenwert_berechnen(spieler_hand)
    print(f"Spieler Hand: {spieler_hand} → {spieler_punkte} Punkte")
    print("="*50)


def spieler_zug(hand, deck):
    # Führt einen Spielerzug durch (Hit/Stand).
    # Der Spieler wird solange nach Hit/Stand gefragt, bis er Stand wählt
    # oder über 21 geht.

    while kartenwert_berechnen(hand) < 21:
        print("\nDeine aktuelle Hand:")
        spieler_punkte = kartenwert_berechnen(hand)
        print(f"Spieler Hand: {hand} → {spieler_punkte} Punkte")
        print("\n")
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


def dealer_zug(hand, deck):
    # Der Dealer zieht so lange Karten, bis die Punktzahl ≥ 17 ist.
    # Rückgabe:
    # Aktualisierte Kartenliste des Dealers
    while kartenwert_berechnen(hand) < 17:
        if deck:
            hand.append(deck.pop())
            print(f"Dealer zieht: {hand[-1]}")
        else:
            print("Keine Karten mehr im Deck für den Dealer!")
            break
    return hand


def gewinner_ermitteln(spieler_punkte, dealer_punkte):
    # Bestimmt den Gewinner basierend auf den Kartenwerten.
    # Rückgabe:
    # String: "Spieler", "Dealer" oder "Unentschieden"
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

# FUNKTIONEN: DATEIVERARBEITUNG & PROTOKOLLIERUNG


def game_log_laden():
    # Lädt game_log.json oder gibt eine Standardstruktur zurück.
    if not os.path.exists(GAME_LOG_FILE):
        # Rückgabe einer Kopie, damit der Aufrufer das Original nicht verändert
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
            data = json.load(f)
            # Wenn Format nicht stimmt, ersetze durch Default
            if not isinstance(data, dict) or 'spiele' not in data or 'statistiken' not in data:
                print(
                    f"Warnung: {GAME_LOG_FILE} hat unerwartetes Format. Überspringe Inhalte.")
                return {
                    "spiele": [],
                    "statistiken": {
                        "spiele": 0,
                        "gewonnen_spieler": 0,
                        "gewonnen_dealer": 0,
                        "unentschieden": 0
                    }
                }
            return data
    except (IOError, json.JSONDecodeError):
        print(
            f"Warnung: Fehler beim Laden von {GAME_LOG_FILE}. Nutze leeren Log.")
        return {
            "spiele": [],
            "statistiken": {
                "spiele": 0,
                "gewonnen_spieler": 0,
                "gewonnen_dealer": 0,
                "unentschieden": 0
            }
        }


def game_log_speichern(log) -> None:
    # Speichert die Spielhistorie in game_log.json.

    # Parameter:
    # log: Dictionary mit Spielhistorie und Statistiken
    try:
        with open(GAME_LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(log, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"Fehler beim Speichern von {GAME_LOG_FILE}: {e}")


def ergebnis_protokollieren(spieler_hand, dealer_hand, gewinner):
    # Protokolliert ein Spielergebnis in game_log.json.
    # Aktualisiert sowohl die Spielliste als auch die Gesamtstatistiken.
    # gewinner: String ("Spieler", "Dealer" oder "Unentschieden")

    log = game_log_laden()
    rundennummer = len(log.get('spiele', [])) + 1
    spieler_punkte = kartenwert_berechnen(spieler_hand)
    dealer_punkte = kartenwert_berechnen(dealer_hand)

    neuer_eintrag = {
        "runde": rundennummer,
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "gewinner": gewinner,
        "karten": {"spieler": spieler_hand, "dealer": dealer_hand},
        "werte": {"spieler": spieler_punkte, "dealer": dealer_punkte}
    }

    # Anhängen und Statistik einfach erhöhen
    log.setdefault('spiele', []).append(neuer_eintrag)
    stats = log.setdefault('statistiken', {
                           "spiele": 0, "gewonnen_spieler": 0, "gewonnen_dealer": 0, "unentschieden": 0})
    stats['spiele'] = stats.get('spiele', 0) + 1
    # Statistik für Gewinner erhöhen
    gewinner_keys = {
        'Spieler': 'gewonnen_spieler',
        'Dealer': 'gewonnen_dealer',
        'Unentschieden': 'unentschieden'
    }
    if gewinner in gewinner_keys:
        stats[gewinner_keys[gewinner]] = stats.get(
            gewinner_keys[gewinner], 0) + 1

    game_log_speichern(log)

# FUNKTIONEN: MENÜNAVIGATION & VALIDIERUNG


def menu_spielhistorie_anzeigen():
    # Zeigt die Spielhistorie und Statistiken aus game_log.json an.
    # Verwendet .get() für den robusten Zugriff auf JSON-Daten,
    # um KeyErrors zu vermeiden, falls ältere Log-Einträge unvollständig sind.
    log = game_log_laden()

    print("\n" + "="*60)
    print("SPIELHISTORIE & STATISTIKEN")
    print("="*60)

    # Statistiken anzeigen
    # Sichere Abfrage
    stats = log.get("statistiken", DEFAULT_LOG["statistiken"])
    print(f"\nGESAMTSTATISTIK:")
    print(f"  Gesamt gespielte Spiele: {stats.get('spiele', 0)}")
    print(f"  Gewonnen (Spieler): {stats.get('gewonnen_spieler', 0)}")
    print(f"  Gewonnen (Dealer): {stats.get('gewonnen_dealer', 0)}")
    print(f"  Unentschieden: {stats.get('unentschieden', 0)}")

    # Letzte Spiele anzeigen
    spiele_liste = log.get("spiele", [])  # Sichere Abfrage
    if spiele_liste:
        print(f"\nLETZTE {min(5, len(spiele_liste))} SPIELE:")
        print("-"*60)
        # Zeige die letzten 5 Einträge
        for spiel in spiele_liste[-5:]:

            # Verwendung von.get() mit Standardwerten, um KeyErrors abzufangen
            runde = spiel.get('runde', 'N/A')
            start_time = spiel.get('start_time', 'Unbekannt')

            print(f"  Runde {runde}: {start_time}")

            # Sichere Abfrage für verschachtelte Daten
            karten = spiel.get('karten', {})
            werte = spiel.get('werte', {})

            spieler_karten = karten.get('spieler', ['Fehlende Daten'])
            spieler_werte = werte.get('spieler', 'N/A')
            dealer_karten = karten.get('dealer', ['Fehlende Daten'])
            dealer_werte = werte.get('dealer', 'N/A')
            gewinner = spiel.get('gewinner', 'Unbekannt')

            print(f"    Gewinner: {gewinner}")
            print(
                f"    Spieler: {spieler_karten} ({spieler_werte} Punkte)")
            print(
                f"    Dealer: {dealer_karten} ({dealer_werte} Punkte)")
            print()
    else:
        print("\nNoch keine Spiele protokolliert.")

    print("="*60 + "\n")


def menu_hauptmenu():
    # Zeigt das Hauptmenü und gibt die validierte Benutzerauswahl zurück.
    while True:
        print("\n" + "="*60)
        print("PyJack - Hauptmenü")
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


def frage_neustart():
    # Fragt den Spieler, ob er eine neue Runde spielen möchte.
    # .strip= entfernt leezeichen
    while True:
        antwort = input(
            "Möchtest du eine weitere Runde spielen? (j/n): ").strip().lower()
        if antwort == 'j':
            return True
        elif antwort == 'n':
            return False
        else:
            print("Ungültige Eingabe. Bitte 'j' (Ja) oder 'n' (Nein) eingeben.")


# FUNKTIONEN: HAUPTSPIELABLAUF

def spiel_durchfuehren():
    # Führt eine komplette Spielrunde durch.
    # 1. Deck erstellen, Karten austeilen
    deck = deck_erstellen()
    # Das Deck wird als Liste von Strings (Kartenkennzeichen) zurückgegeben
    # .pop entfernt 2 Kartern aus dem Deck und weisst sie spieler_hand zu
    spieler_hand = [deck.pop(), deck.pop()]
    # .pop entfernt 2 Kartern aus dem Deck und weisst sie dealer_hand zu
    dealer_hand = [deck.pop(), deck.pop()]

    print("\n")
    print("Neue Runde gestartet!💸")

    # 2. Spielzustand anzeigen (Dealer-Karte verborgen)
    spielzustand_anzeigen(spieler_hand, dealer_hand, dealer_verborgen=True)

    # 3. Spieler-Zug
    # Die Funktion spieler_zug wird aufgerufen und
    # aktualisiert die Hand direkt (durch Listen-Referenz)
    spieler_hand = spieler_zug(spieler_hand, deck)
    spieler_punkte = kartenwert_berechnen(spieler_hand)

    # Wenn Spieler über 21 ist, endet das Spiel
    if spieler_punkte > 21:
        print("\n❌ BUST! Du hast über 21 Punkte. Du hast verloren!")
        spielzustand_anzeigen(spieler_hand, dealer_hand,
                              dealer_verborgen=False)  # Dealer-Karte aufdecken
        ergebnis_protokollieren(spieler_hand, dealer_hand, "Dealer")
        return

    # 4. Dealer Zug (Automatik)
    print("\nDealer spielt automatisch...")
    # Die Funktion dealer_zug wird aufgerufen und aktualisiert die Hand direkt
    dealer_hand = dealer_zug(dealer_hand, deck)
    dealer_punkte = kartenwert_berechnen(dealer_hand)

    # 5. Gewinner ermitteln und anzeigen
    gewinner = gewinner_ermitteln(spieler_punkte, dealer_punkte)

    print("\n" + "="*50)
    print("RUNDENERGEBNIS")
    print("="*50)
    spielzustand_anzeigen(spieler_hand, dealer_hand, dealer_verborgen=False)

    if gewinner == "Spieler":
        if dealer_punkte > 21:
            print("🎉 DEALER BUST! DU HAST GEWONNEN!")
        else:
            print("🎉 DU HAST GEWONNEN!")
    elif gewinner == "Dealer":
        print("❌ DEALER GEWINNT!")
    else:  # Unentschieden
        print("🤝 UNENTSCHIEDEN!")

    print("="*50 + "\n")

    # 6. Ergebnis protokollieren
    # Protokollieren des Gewinners,(durch gewinner_ermitteln bestimmt)
    ergebnis_protokollieren(spieler_hand, dealer_hand, gewinner)

# Hauptfunktion


def main():
    # Menüschleife

    print("\n")
    print("Willkommen zu PyJack!")

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
