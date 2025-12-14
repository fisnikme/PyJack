# PyJack ♥️♣️♦️♠️

## 📝 Analyse

**Problem**

Wir helfen Menschen, lange Wartezeiten und Langeweile zu überbrücken. Zusätzlich unterstützen wir Glücksspielende dabei, zu spielen, ohne das Risiko Geld zu verlieren und dennoch die Befriedigung des Spielens zu erleben.

**Szenario**

PyJack ist ein einfach zugängliches Spiel gegen Langeweile. Spielenden können jederzeit und überall ohne Internetverbindung spielen. 

**User stories:**
- Als Nutzer möchte ich sofort nach Sieg oder Niederlage ein neues Spiel starten können. 
- Als Nutzer möchte ich eine Karte ziehen oder bei der aktuellen Hand bleiben können. 
- Als Nutzer möchte ich informiert werden, ob ich gewonnen oder verloren habe. 
- Als Nutzer möchte ich, dass Gewinne und Verluste in einer Datei protokolliert werden, damit ich meine Gewinn-/Verlustrate verfolgen kann. 

**Use cases:**
- Neues Spiel starten (Deck mischen, Karten austeilen) 
- Spielzustand anzeigen (Hände mit Werten) 
- Spielerentscheidung treffen (Hit/Stand mit Validierung) 
- Dealer-Automatik (Standardregeln: Hit bei 16, Stand bei 17) 
- Gewinner ermitteln und bekanntgeben 
- Ergebnis protokollieren (game_log.json) 

---

## ✅ Projektanforderungen

Folgende Anforderungen sind an das Projekt gestellt worden:
1. Interaktive Konsolenanwendung
2. Datenvalidierung
3. Dateiverarbeitung


---

### 1. Interaktive Konsolenanwendung: 

Die Anwendung interagiert mit dem Benutzer durch die Konsole. Benutzer können:
- Menü-Navigation und Spielerentscheidungen 
- Hit/Stand-Auswahl während des Spiels 
- Neustart des Spiels nach jeder Runde 

---


### 2. Validierung von Daten:

Folgende Inputs des Benutzers, werden durch die Applikation geprüft, um ein reibungsloses Spielerlebnis für den Benutzer zu garantieren:
* **Menüauswahl-Validierung (Historie/Spielen):** Stellt sicher, dass im Menü ausschliesslich nummerische Eingaben akzeptiert werden.
* **Gameplay-Entscheidungen (Hit/Stand):** Leere Eingaben, Leerzeichen sowie Gross- und Kleinschreibung werden ignoriert. 
* **Fortsetzungseingabe (Ja/Nein):** 

Beispiele:

```python
 while True:
        antwort = input(
            "Möchtest du eine weitere Runde spielen? (j/n): ").strip().lower()
        if antwort == 'j':
            return True
        elif antwort == 'n':
            return False
        else:
            print("Ungültige Eingabe. Bitte 'j' (Ja) oder 'n' (Nein) eingeben.")
```

```python
wahl = input("Wähle eine Option (1/2/3): ").strip()

        if wahl == "1":
            return "spielen"
        elif wahl == "2":
            return "historie"
        elif wahl == "3":
            return "beenden"
        else:
            print("Ungültige Eingabe. Bitte 1, 2 oder 3 eingeben.")
```
---


### 3. Dateiverarbeitung

Die Applikation verwendet die Datei game_log.json, zum Auslesen der Historie und zum Speichern neuer Spielergebnisse.

- **Output file:** `game_log.json`— Die Datei wird beim ersten Spiel generiert. In der Datei befinden sich die letzten Spielergebnisse. Die Spielergebnisse werden immer mit Zeitstempeln versehen.


## ⚙️ Implementierung

### Technologie
- Python 3.x
- Umgebung: GitHub Codespaces

### 📂 Repository Struktur

```
PyJack
├── pyjack_main.py     # Hauptprogramm (Spielablauf & Menü)
├── game_log.json      # Automatisch generierte Spielhistorie
├── README.md          # Dokumentation
└── .gitignore         # Dateien, welche von Git ignoriert werden sollten
```
---

## 🖥️ Wie startet man die Anwendung
### Windows-Version herunterladen und starten

Die ausführbare Windows-Version von **PyJack** kann direkt über GitHub Releases heruntergeladen werden.

### Download
1. Öffnen Sie die Release-Seite des Projekts:
    https://github.com/fisnikme/PyJack/releases/latest

2. Unter **Assets** finden Sie die Datei:
   **PyJack.exe**

3. Klicken Sie auf **PyJack.exe**, um die Datei herunterzuladen.

### Ausführen unter Windows
1. Öffnen Sie den Ordner, in dem die Datei gespeichert wurde  
2. Doppelklicken Sie auf **PyJack.exe**, um das Spiel zu starten  
3. Es ist **keine Python-Installation** erforderlich

#### Hinweis
Beim ersten Start kann Windows Defener eine Warnung anzeigen.  
In diesem Fall:
- Auf **Weitere Informationen** klicken  
- Dann **Trotzdem ausführen** wählen 

### MacOS-Version/alternativer Zugang - ausführen im Terminal
1.  Öffnen Sie das Terminal Ihres Clients:

2. Klonen Sie das Repository in dem Sie folgenden Command im Terminal eingeben:
  ```bash
git clone https://github.com/fisnikme/PyJack.git
```
3. Wechseln Sie mit folgendem Command in den Projektordner:
```bash
cd PyJack
```
4. Sie können die Anwendung nun mit folgendem Command starten:
```bash
python pyjack_main.py
```

## Verwendete Libraries 
* `json`: Speichern und Laden der Spielhistorie
* `random`: Mischen des Kartendecks und zufälliges Austeilen der Karten
* `os`: Prüfen ob Log-File bereits existiert, bevor sie erstellt wird
* `datetime`: Zeitstempel für jedes gespeicherte Spielergebnis 


## 👥 Gruppe & Contribution
| **Name**  | **Contribution**                                                              |
|-----------|-------------------------------------------------------------------------------|
| **Andri** | Testing, UI-Design, Release, Funktionen programmieren                         |
| **Fisnik**| Kernlogik des Spiels, Funktionen programmieren, GitHub-Verwaltung             |

## 📝 Lizenz

Dieses Projekt dient nur Bildungszwecken als Teil eines Programmiermoduls.
[MIT License](LICENSE)
