"""
Prüfung der ORM-Modelle, Relationen und Datenbankabstraktion.
"""
from datetime import datetime
from app.models.medikament import Medikament
from app.models.einnahme import EinnahmeProtokoll
from app.models.vitalwert import Vitalwert


def test_patient_kaskadierte_beziehungen(db_session, sample_patient):
    """Prüft, ob die Assoziationen des Wurzelobjekts Patient korrekt aufgelöst werden."""
    med = Medikament(
        patient_id=sample_patient.id,
        name="Ass 100",
        dosierung="1x tgl.",
        tageszeit="Morgens",
        bestand=50,
        mindestbestand=10
    )
    vital = Vitalwert(
        patient_id=sample_patient.id,
        zeitpunkt=datetime.now(),
        kategorie="Puls",
        wert=68.0,
        einheit="bpm"
    )
    db_session.add_all([med, vital])
    db_session.commit()

    assert len(sample_patient.medikamente) == 1
    assert len(sample_patient.vitalwerte) == 1
    assert sample_patient.medikamente[0].name == "Ass 100"


def test_einnahme_protokoll_unveraenderlichkeit(db_session, sample_patient, sample_medikament):
    """GR-03: Protokolleinträge erfassen historische Ist-Zeitstempel konsistent."""
    jetzt = datetime.now()
    protokoll = EinnahmeProtokoll(
        patient_id=sample_patient.id,
        medikament_id=sample_medikament.id,
        soll_tageszeit="Morgens",
        einnahme_zeitpunkt=jetzt,
        erledigt=True
    )
    db_session.add(protokoll)
    db_session.commit()

    geladen = db_session.get(EinnahmeProtokoll, protokoll.id)
    assert geladen.erledigt is True
    assert geladen.medikament_id == sample_medikament.id
    assert geladen.einnahme_zeitpunkt == jetzt