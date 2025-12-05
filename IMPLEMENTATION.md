# PyJack - Implementierungsanleitung

## Übersicht

Diese `pyjack.py` ist die vollständige Implementierung des PyJack Blackjack-Spiels gemäß den README-Anforderungen. Das Spiel ist eine interaktive Konsolenanwendung mit Datenvalidierung und Dateiverarbeitung.

## Features (vom README implementiert)

✅ **Interaktive Konsolenanwendung**
- Hauptmenü mit Optionen: Spielen, Spielhistorie, Beenden
- Hit/Stand-Entscheidungen während des Spiels
- Neustart nach jeder Runde

✅ **Datenvalidierung**
- Menüauswahl (1/2/3)
- Gameplay-Entscheidungen (h/s)
- Fortsetzungseingabe (j/n)

✅ **Dateiverarbeitung (game_log.json)**
- Speichert automatisch alle Spielergebnisse
- Protokolliert Zeitstempel, Hände, Kartenwerte, Gewinner
- Berechnet und speichert laufende Statistiken

## Implementierte Funktionen (aus README)

### Deck-Verwaltung
- `deck_erstellen()` - Erstellt und mischt Kartendeck

### Spielzustand
- `kartenwert_berechnen(hand)` - Berechnet Punktzahl mit Ass-Handling
- `spielzustand_anzeigen()` - Zeigt Hände und Werte an

### Spielablauf
- `spieler_zug()` - Hit/Stand mit Validierung
- `dealer_zug()` - Automatik (Hit <17, Stand ≥17)
- `gewinner_ermitteln()` - Bestimmt Gewinner nach Regeln

### Dateiverarbeitung
- `game_log_laden()` - Lädt game_log.json
- `game_log_speichern()` - Speichert game_log.json
- `ergebnis_protokollieren()` - Protokolliert Spielergebnis

### Menü & Validierung
- `menu_hauptmenu()` - Hauptmenü mit Eingabevalidierung
- `menu_spielhistorie_anzeigen()` - Zeigt Statistiken und letzte 5 Spiele
- `frage_neustart()` - Fragt nach Fortsetzung

## Installation & Start

```bash
# Spiel starten
cd /workspaces/PyJack
python3 pyjack.py
```

## Bedienung

1. **Hauptmenü**
   - Geben Sie `1` ein, um ein Spiel zu spielen
   - Geben Sie `2` ein, um Ihre Spielhistorie anzusehen
   - Geben Sie `3` ein, um das Programm zu beenden

2. **Während eines Spiels**
   - Geben Sie `h` (Hit) ein, um eine Karte zu ziehen
   - Geben Sie `s` (Stand) ein, um zu bleiben
   - Nach der Runde: `j` (Ja) für nächstes Spiel, `n` (Nein) zurück zum Menü

## Schwarzjack-Regeln

- **Kartenwerte**: 2-10 = Wert, J/Q/K = 10, A = 11 (oder 1 wenn nötig)
- **Spieler**: Kann Hit/Stand wählen
- **Dealer**: Hit bei <17, Stand bei ≥17 (automatisch)
- **Gewinner**: Höchste Punktzahl ≤ 21 gewinnt
- **Bust**: Über 21 = automatisch verloren

## Dateien

- `pyjack.py` - Hauptprogramm
- `game_log.json` - Wird beim ersten Spiel erstellt, enthält Spielhistorie und Statistiken

## game_log.json Struktur

```json
{
  "spiele": [
    {
      "runde": 1,
      "start_time": "2025-11-29 12:00:00",
      "gewinner": "Spieler",
      "karten": {
        "spieler": ["A", "K"],
        "dealer": ["10", "7"]
      },
      "werte": {
        "spieler": 21,
        "dealer": 17
      }
    }
  ],
  "statistiken": {
    "spiele": 1,
    "gewonnen_spieler": 1,
    "gewonnen_dealer": 0,
    "unentschieden": 0
  }
}
```

## Codequalität

- **PEP8-konform** - Konsistente Formatierung und Namenkonventionen
- **Type Hints** - Vollständige Typannotationen für bessere Wartbarkeit
- **Docstrings** - Kurze, präzise Dokumentation für alle Funktionen
- **Fehlerbehandlung** - Validierung aller Benutzereingaben
- **Modular** - Logische Aufteilung in Funktionen

## Anforderungen für Erstsemester

Der Code ist für ein erstes Semester Wirtschaftsinformatik geeignet:
- Klare Funktionsstruktur
- Deutsche Kommentare und Variablennamen
- Einfache Kontrollstrukturen (if/while/for)
- Dictionary und List Datenstrukturen
- JSON-Dateiverarbeitung
- Einfache Validierungslogik
