"""Initialisiert die Datenbank mit konsistenten Testdaten zur Demonstration."""

from datetime import date, datetime, timedelta
from app import create_app, db
from app.models import Patient, Medikament, Vitalwert, Termin

app = create_app()

with app.app_context():
    db.create_all()
    
    if not Patient.query.first():
        patient = Patient(
            vorname="Anna",
            nachname="Muster",
            geburtsdatum=date(1948, 5, 12),
            notfallkontakt="Max Muster (Sohn) - 0170/1234567"
        )
        db.session.add(patient)
        db.session.commit()

        medikamente = [
            Medikament(patient_id=patient.id, name="Ramipril 5mg", dosierung="1 Tablette", tageszeit="Morgens", bestand=14, mindestbestand=5),
            Medikament(patient_id=patient.id, name="Ibuprofen 400mg", dosierung="1 Tablette", tageszeit="Mittags", bestand=3, mindestbestand=5)
        ]
        db.session.add_all(medikamente)

        jetzt = datetime.now()

        vitalwerte = [
            Vitalwert(patient_id=patient.id, kategorie="Blutdruck_Systolisch", wert=128.0, einheit="mmHg"),
            Vitalwert(patient_id=patient.id, kategorie="Puls", wert=72.0, einheit="bpm")
        ]
        db.session.add_all(vitalwerte)

        termine = [
            Termin(patient_id=patient.id, titel="Hausarzt Dr. Weber - Quartals-Check", zeitpunkt=jetzt + timedelta(days=3), kategorie="Arzt"),
            Termin(patient_id=patient.id, titel="Physiotherapie", zeitpunkt=jetzt + timedelta(days=1), kategorie="Therapie"),
            Termin(patient_id=patient.id, titel="Rezeptabholung Apotheke", zeitpunkt=jetzt - timedelta(days=1), kategorie="Pflege", erledigt=True),
        ]
        db.session.add_all(termine)

        db.session.commit()
        print("Testdaten erfolgreich in database/medical_tracker.db eingepflegt.")
    else:
        print("Datenbank enthält bereits Daten.")