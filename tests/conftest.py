"""
Zentrales Fixture-Management für die pytest-Testsuite von Medical Tracker.
"""
from datetime import date
import pytest

from app import create_app, db
from app.models.patient import Patient
from app.models.medikament import Medikament
from config import Config


class TestConfig(Config):
    """Spezifische Testkonfiguration zur Isolation der Testläufe."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "test-secret-key"


@pytest.fixture(scope="session")
def app():
    """Initialisiert die Flask-Applikationsinstanz im Testmodus."""
    _app = create_app(TestConfig)
    with _app.app_context():
        yield _app


@pytest.fixture(scope="function")
def client(app):
    """Stellt einen Flask-Test-Client für HTTP-Anfragen bereit."""
    return app.test_client()


@pytest.fixture(scope="function")
def runner(app):
    """CLI-Runner für eventuelle Click-Befehle."""
    return app.test_cli_runner()


@pytest.fixture(scope="function")
def db_session(app):
    """
    Erstellt für jeden Testfall eine frische In-Memory-Datenbank
    und bereinigt diese nach Testende (Transaktionsisolation).
    """
    db.create_all()
    yield db.session
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope="function")
def sample_patient(db_session):
    """Erzeugt einen validen Basis-Patienten (Wurzelobjekt)."""
    patient = Patient(
        vorname="Anna",
        nachname="Musterfrau",
        geburtsdatum=date(1950, 5, 15),
        notfallkontakt="Dr. Weber: 0123-456789"
    )
    db_session.add(patient)
    db_session.commit()
    return patient


@pytest.fixture(scope="function")
def sample_medikament(db_session, sample_patient):
    """Erzeugt ein Standard-Medikament für Bestandstests."""
    medikament = Medikament(
        patient_id=sample_patient.id,
        name="Ramipril 5mg",
        dosierung="1 Tablette",
        tageszeit="Morgens",
        bestand=10,
        mindestbestand=3
    )
    db_session.add(medikament)
    db_session.commit()
    return medikament