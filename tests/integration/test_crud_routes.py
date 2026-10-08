"""
Integrationstests für die CRUD-Routen von Medikamenten, Vitaldaten und Terminen
"""
from datetime import datetime, timedelta
from app.models.medikament import Medikament
from app.models.vitalwert import Vitalwert
from app.models.termin import Termin


def test_medikamente_crud_flow(client, db_session, sample_patient):
    """FA-01: Vollständiger CRUD-Lebenszyklus für Medikamente."""
    # 1. Index-Ansicht
    resp = client.get("/medikamente/")
    assert resp.status_code == 200

    # 2. Neues Medikament anlegen (POST)
    resp = client.post("/medikamente/neu", data={
        "name": "Amlodipin 5mg",
        "dosierung": "1 Tablette",
        "tageszeit": "Abends",
        "bestand": 28,
        "mindestbestand": 7
    }, follow_redirects=True)
    assert resp.status_code == 200
    med = Medikament.query.filter_by(name="Amlodipin 5mg").first()
    assert med is not None
    assert med.bestand == 28

    # 3. Medikament bearbeiten (POST)
    resp = client.post(f"/medikamente/{med.id}/bearbeiten", data={
        "name": "Amlodipin 10mg",
        "dosierung": "1 Tablette",
        "tageszeit": "Abends",
        "bestand": 30,
        "mindestbestand": 5
    }, follow_redirects=True)
    assert resp.status_code == 200
    db_session.refresh(med)
    assert med.name == "Amlodipin 10mg"

    # 4. Medikament löschen (POST)
    resp = client.post(f"/medikamente/{med.id}/loeschen", follow_redirects=True)
    assert resp.status_code == 200
    assert db_session.get(Medikament, med.id) is None


def test_vitaldaten_flow(client, db_session, sample_patient):
    """FA-02: Erfassung von Blutdruck, Puls und Gewicht über Controller-Routen."""
    # 1. Index-Ansicht
    resp = client.get("/vitaldaten/")
    assert resp.status_code == 200

    # 2. Blutdruck erfassen
    resp = client.post("/vitaldaten/neu", data={
        "kategorie": "Blutdruck",
        "systolisch": 128.0,
        "diastolisch": 84.0
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert Vitalwert.query.filter_by(kategorie="Blutdruck_Systolisch").first() is not None

    # 3. Puls erfassen
    resp = client.post("/vitaldaten/neu", data={
        "kategorie": "Puls",
        "einzelwert": 74.0
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert Vitalwert.query.filter_by(kategorie="Puls").first() is not None

    # 4. Gewicht erfassen
    resp = client.post("/vitaldaten/neu", data={
        "kategorie": "Gewicht",
        "einzelwert": 78.2
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert Vitalwert.query.filter_by(kategorie="Gewicht").first() is not None


def test_termine_flow(client, db_session, sample_patient):
    """FA-04: Erfassung, Bearbeitung, Umschalten und Löschen von Pflegeterminen."""
    # 1. Index-Ansicht
    resp = client.get("/termine/")
    assert resp.status_code == 200

    # 2. Termin anlegen
    zeit_str = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%dT%H:%M")
    resp = client.post("/termine/neu", data={
        "titel": "Zahnarztkontrolle",
        "kategorie": "Arzttermin",
        "zeitpunkt": zeit_str
    }, follow_redirects=True)
    assert resp.status_code == 200
    termin = Termin.query.filter_by(titel="Zahnarztkontrolle").first()
    assert termin is not None
    assert termin.erledigt is False

    # 3. Termin Status umschalten (Toggle erledigt)
    resp = client.post(f"/termine/{termin.id}/toggle", follow_redirects=True)
    assert resp.status_code == 200
    db_session.refresh(termin)
    assert termin.erledigt is True

    # 4. Termin bearbeiten
    resp = client.post(f"/termine/{termin.id}/bearbeiten", data={
        "titel": "Zahnarztkontrolle Dr. Schmidt",
        "kategorie": "Arzttermin",
        "zeitpunkt": zeit_str
    }, follow_redirects=True)
    assert resp.status_code == 200
    db_session.refresh(termin)
    assert termin.titel == "Zahnarztkontrolle Dr. Schmidt"

    # 5. Termin löschen
    resp = client.post(f"/termine/{termin.id}/loeschen", follow_redirects=True)
    assert resp.status_code == 200
    assert db_session.get(Termin, termin.id) is None


def test_patient_profil_und_ansichten(client, db_session, sample_patient):
    """FA-05: Patientenprofil abrufen und Tagesansicht aufrufen."""
    # 1. Tagesansicht aufrufen
    resp = client.get("/patient/")
    assert resp.status_code == 200

    # 2. Profil aktualisieren
    resp = client.post("/patient/profil", data={
        "vorname": "Anna-Maria",
        "nachname": "Musterfrau",
        "geburtsdatum": "1952-03-10",
        "notfallkontakt": "Sohn: 0170-9876543"
    }, follow_redirects=True)
    assert resp.status_code == 200
    db_session.refresh(sample_patient)
    assert sample_patient.vorname == "Anna-Maria"

    # 3. Termin in Patientensicht als erledigt markieren
    termin = Termin(
        patient_id=sample_patient.id,
        titel="Blutabnahme",
        zeitpunkt=datetime.now(),
        kategorie="Pflegedienst",
        erledigt=False
    )
    db_session.add(termin)
    db_session.commit()
    resp = client.post(f"/patient/termin-erledigen/{termin.id}", follow_redirects=True)
    assert resp.status_code == 200
    db_session.refresh(termin)
    assert termin.erledigt is True