# Medical Tracker – Digitales Assistenzsystem für den Pflegealltag

[![Python](https://img.shields.io/badge/Python-3.14%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Flask%203.1%2B-lightgrey.svg)](https://flask.palletsprojects.com/)
[![Database](https://img.shields.io/badge/Database-SQLite%203-green.svg)](https://www.sqlite.org/)
[![UI](https://img.shields.io/badge/UI-Bootstrap%205%20%7C%20WCAG%202.2-purple.svg)](https://getbootstrap.com/)
[![Academic Project](https://img.shields.io/badge/IU%20International%20University-DLMCSPSE01__D-red.svg)](https://www.iu.de/)

> **Wissenschaftliches Entwicklungsprojekt im Modul DLMCSPSE01_D – Projekt: Software Engineering**  
> Master of Science Informatik, IU Internationale Hochschule  
> **Autor:** Steffen Niklas Oehler (Matrikelnummer: IU14142306)  
> **Betreuer / Tutor:** Prof. Dr. Dirk Simon

---

## 1. Problemstellung und Kundennutzen (Customer Value)

Die häusliche Pflege von Angehörigen erfordert eine stringente Koordination: Medikationspläne müssen eingehalten, Vitaldaten überwacht und Konsultationen vorbereitet werden. Häufig genutzte Papieraufzeichnungen führen zu Dokumentationslücken, Einnahmefehlern oder Informationsverlusten bei Arztbesuchen.

Der **Medical Tracker** löst dieses Problem durch ein leichtgewichtiges, lokal betriebenes Assistenzsystem mit einem dualen Schnittstellenkonzept:
1. **Verwaltungsdashboard für pflegende Angehörige:** Effiziente Pflege von Stammdaten, Medikationsplänen, Terminen, Vitalwerten und Export aggregierter Arztberichte.
2. **Barrierefreier Patientenmodus (WCAG 2.2 / NFA-01):** Kognitiv reduzierte Single-Page-Tagesansicht mit Großtypografie, kontrastreicher Gestaltung, sekundengenauer Digitaluhr und einfachen Touch-Schaltflächen zur Einnahme- und Terminbestätigung.

---

## 2. Funktionsumfang & Spezifikationsabdeckung

| Anforderungs-ID | Feature | Technische Realisierung |
| :--- | :--- | :--- |
| **FA-01** | Medikationsverwaltung | Vollständiges CRUD, Lagerbestandsführung, serverseitige Positivitätsprüfung (`bestand >= 0`, GR-01). |
| **FA-02** | Vitaldaten-Tracking | Dokumentation von Blutdruck, Puls und Gewicht inklusive physiologischer Schwellenwertprüfungen (GR-02). |
| **FA-03** | PDF-Arztbericht | In-Memory-Kompilierung (`io.BytesIO`) strukturierter DIN-A4-Berichte via ReportLab über frei wählbare Zeiträume. |
| **FA-04** | Termin- & Aufgabenboard | Terminplanung und interaktive Erledigungsquittierung im Dashboard sowie in der Tagesansicht. |
| **FA-05** | Barrierefreier Patientenmodus | Kognitive Entlastung, WCAG 2.2 Kontrastvorgaben, Touch-Targets, Live-Uhr. |
| **FA-06** | Einnahmebestätigung | Atomare Protokollierung von Ist-Zeitpunkten zur Sicherstellung der Behandlungstreue (Compliance). |
| **FA-07** | Bestandsdekrementierung | Synchrone Lagerbestandsreduktion pro Einnahme und visuelle Mindestbestandswarnungen auf dem Dashboard. |
| **Onboarding** | Stammdatenerfassung | Automatische Weiterleitung zur Patientenerfassung bei initial leerer Datenbank; Vergangenheitsprüfung des Geburtsdatums. |

---

## 3. Architektur & Technologie-Stack

Die Anwendung folgt einer hierarchischen **Drei-Schichten-Architektur** unter konsequenter Umsetzung des **Model-View-Controller-Musters (MVC)**:

* **Backend / Controller:** Python (v3.14+) mit dem Micro-Framework Flask. Strukturierung über modulare Flask-Blueprints (`main`, `medikamente`, `patient`, `vitaldaten`, `termine`, `reports`).
* **Präsentationsschicht (View):** Serverseitig gerenderte Jinja2-HTML5-Templates mit Bootstrap 5. Separation of Concerns durch Auslagerung aller Stile und Verhaltensskripte nach `app/static/css/` und `app/static/js/`.
* **Service-Layer:** Entkoppelte Generierung von PDF-Dokumenten (`app/services/pdf_generator.py`) mittels ReportLab und zweistufiger Paginierung (`NumberedCanvas`).
* **Persistenzschicht (Model):** Lokale relationale SQLite-Datenbank (`medical_tracker.db`), angebunden über das ORM Flask-SQLAlchemy mit kaskadierenden Fremdschlüsseln und Check-Constraints.
* **Formular- und Eingabesicherheit:** Flask-WTF / WTForms zur Durchsetzung kryptographischer CSRF-Token und mehrstufiger serverseitiger Geschäftsregel-Validierungen.
* **Systemzuverlässigkeit:** Automatisiertes Anlegen lokaler Dateibackups (`/database/backups/`) sowie Prüfung der SQLite-Header-Integrität bei jedem Systemstart (`run.py`).

---

## 4. Systemvoraussetzungen

    Betriebssystem: Microsoft Windows 10/11 (oder macOS / Linux)

    Laufzeitumgebung: Python 3.14 oder höher

    Webbrowser: Google Chrome, Mozilla Firefox oder Microsoft Edge in aktueller Version

---

## 6. Installation & Schnellstart

Führen Sie die folgenden Schritte in einem Terminal (z. B. PowerShell unter Windows) aus:
1. Repository klonen
PowerShell

git clone [https://github.com/SteffenOe/medicaltracker.git](https://github.com/SteffenOe/medicaltracker.git)
cd medicaltracker

2. Virtuelle Umgebung erstellen und aktivieren

PowerShell

python -m venv .venv


3. Abhängigkeiten installieren

PowerShell

pip install --upgrade pip
pip install -r requirements.txt

4. Testdaten einspielen (Empfohlen für Prüfungszwecke)

Zur sofortigen Begutachtung aller Funktionalitäten (inklusive 14-tägiger Vitalwert-Historie für den PDF-Export und Bestandswarnungen) wird die Datenbank initial befüllt:

PowerShell

python seed.py

5. Anwendung starten

PowerShell

python run.py

Die Anwendung startet unter der lokalen Adresse:

http://127.0.0.1:5000/

7. Datenschutz und rechtliche Abgrenzung

    Datenschutz (DSGVO): Alle Gesundheitsdaten werden ausschließlich lokal in der SQLite-Datenbank auf dem Hostrechner verarbeitet (Privacy by Design nach Art. 25 DSGVO). Die Verarbeitung fällt unter die Haushaltsausnahme (Art. 2 Abs. 2 lit. c DSGVO). Es erfolgt keinerlei Datentransfer an externe Server oder Cloud-Dienste.

    Medizinprodukte-Disclaimer: Der Medical Tracker dient als privates Organisations- und Dokumentationswerkzeug. Das System ist kein zertifiziertes Medizinprodukt nach EU-MDR 2017/745. Es führt keine automatisierten Diagnosen, Dosisberechnungen oder Therapieentscheidungen durch. Die Verantwortung verbleibt stets bei der behandelnden Ärzteschaft und den Anwendenden.