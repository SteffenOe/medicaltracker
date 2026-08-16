from datetime import date, datetime
from app import create_app, db
from app.models import Patient, Medikament, Vitalwert, Termin

app = create_app()

with app.app_context():
    db.create_all()
    
    if not Patient.query.first():
        p1 = Patient(
            vorname="Anna",
            nachname="Muster",
            geburtsdatum=date(1948, 5, 12),
            notfallkontakt="Max Muster (Sohn) - 0170/1234567"
        )
        db.session.add(p1)
        db.session.commit()

        m1 = Medikament(patient_id=p1.id, name="Ramipril 5mg", dosierung="1 Tablette", tageszeit="Morgens", bestand=14, mindestbestand=5)
        m2 = Medikament(patient_id=p1.id, name="Ibuprofen 400mg", dosierung="1 Tablette", tageszeit="Mittags", bestand=3, mindestbestand=5)
        
        v1 = Vitalwert(patient_id=p1.id, kategorie="Blutdruck_Systolisch", wert=128.0, einheit="mmHg")
        v2 = Vitalwert(patient_id=p1.id, kategorie="Puls", wert=72.0, einheit="bpm")

        db.session.add_all([m1, m2, v1, v2])
        db.session.commit()
        print("Testdaten erfolgreich in database/medical_tracker.db eingepflegt.")
    else:
        print("Datenbank enthält bereits Daten.")