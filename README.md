# Medical Tracker – Digitales Assistenzsystem für den Pflegealltag

[![Python](https://img.shields.io/badge/Python-3.13%2B-blue.svg)](https://www.python.org/)
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

* **Backend / Controller:** Python (v3.13+) mit dem Micro-Framework Flask. Strukturierung über modulare Flask-Blueprints (`main`, `medikamente`, `patient`, `vitaldaten`, `termine`, `reports`).
* **Präsentationsschicht (View):** Serverseitig gerenderte Jinja2-HTML5-Templates mit Bootstrap 5. Separation of Concerns durch Auslagerung aller Stile und Verhaltensskripte nach `app/static/css/` und `app/static/js/`.
* **Service-Layer:** Entkoppelte Generierung von PDF-Dokumenten (`app/services/pdf_generator.py`) mittels ReportLab und zweistufiger Paginierung (`NumberedCanvas`).
* **Persistenzschicht (Model):** Lokale relationale SQLite-Datenbank (`medical_tracker.db`), angebunden über das ORM Flask-SQLAlchemy mit kaskadierenden Fremdschlüsseln und Check-Constraints.
* **Formular- und Eingabesicherheit:** Flask-WTF / WTForms zur Durchsetzung kryptographischer CSRF-Token und mehrstufiger serverseitiger Geschäftsregel-Validierungen.
* **Systemzuverlässigkeit:** Automatisiertes Anlegen lokaler Dateibackups (`/database/backups/`) sowie Prüfung der SQLite-Header-Integrität bei jedem Systemstart (`run.py`).
