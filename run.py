"""Haupteinstiegspunkt zum Starten des lokalen Entwicklungsservers"""

import os
import shutil
import sqlite3
from datetime import datetime
from app import create_app
from app.models import db
from config import BASE_DIR, Config

app = create_app()

def pruefe_und_sichere_datenbank():
    """Implementiert automatisierte Integritätsprüfung und Backup."""
    db_pfad = Config.DB_REL_PATH
    backup_ordner = os.path.join(BASE_DIR, 'database', 'backups')
    
    if os.path.exists(db_pfad):
        try:
            conn = sqlite3.connect(db_pfad)
            cursor = conn.cursor()
            cursor.execute("PRAGMA integrity_check;")
            ergebnis = cursor.fetchone()
            conn.close()
            
            if ergebnis and ergebnis[0] == "ok":
                print("[INFO] SQLite-Integritätsprüfung erfolgreich bestanden (Status: OK).")
            else:
                print(f"[WARNUNG] SQLite-Integrität fehlerhaft: {ergebnis}")
        except Exception as e:
            print(f"[FEHLER] Fehler bei der Integritätsprüfung: {e}")

        try:
            os.makedirs(backup_ordner, exist_ok=True)
            zeitstempel = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_datei = os.path.join(backup_ordner, f"medical_tracker_backup_{zeitstempel}.db")
            shutil.copy2(db_pfad, backup_datei)
            print(f"[INFO] Automatisches Backup erstellt: {os.path.basename(backup_datei)}")
        except Exception as e:
            print(f"[FEHLER] Datenbank-Backup fehlgeschlagen: {e}")

if __name__ == '__main__':
    os.makedirs(os.path.join(BASE_DIR, 'database'), exist_ok=True)
    pruefe_und_sichere_datenbank()

    # Automatische Tabellenerstellung im lokalen Entwicklungsbetrieb
    with app.app_context():
        db.create_all()
        print("Datenbanktabellen in 'database/medical_tracker.db' erfolgreich erzeugt.")

    # Lokaler Entwicklungsmodus mit Debugger und automatischem Reload    
    app.run(debug=True, port=5000)