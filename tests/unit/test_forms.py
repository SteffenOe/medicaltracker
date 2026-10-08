"""
Verifikation der mehrstufigen Formularvalidierung und Durchsetzung der Geschäftsregeln.
"""
from datetime import date, timedelta
from werkzeug.datastructures import MultiDict
from app.forms.medikament import MedikamentForm
from app.forms.vitalwert import VitalwertForm
from app.forms.patient import PatientForm
from app.forms.bericht import BerichtForm


def test_gr01_medikament_bestand_nicht_negativ(app):
    """GR-01: Verhindert negative Bestands- und Mindestbestandswerte."""
    with app.test_request_context():
        # Ungültiger Fall: Negativer Bestand
        form_invalid = MedikamentForm(formdata=MultiDict({
            "name": "Bisoprolol 2.5mg",
            "dosierung": "1 Tablette",
            "tageszeit": "Morgens",
            "bestand": "-1",
            "mindestbestand": "2"
        }))
        assert not form_invalid.validate()
        assert "bestand" in form_invalid.errors

        # Ungültiger Fall: Negativer Mindestbestand
        form_invalid_min = MedikamentForm(formdata=MultiDict({
            "name": "Bisoprolol 2.5mg",
            "dosierung": "1 Tablette",
            "tageszeit": "Morgens",
            "bestand": "10",
            "mindestbestand": "-5"
        }))
        assert not form_invalid_min.validate()
        assert "mindestbestand" in form_invalid_min.errors

        # Valider Fall: Grenzwerte bei 0 (muss dank InputRequired gültig sein)
        form_valid = MedikamentForm(formdata=MultiDict({
            "name": "Bisoprolol 2.5mg",
            "dosierung": "1 Tablette",
            "tageszeit": "Morgens",
            "bestand": "0",
            "mindestbestand": "0"
        }))
        assert form_valid.validate(), f"Validierung fehlgeschlagen: {form_valid.errors}"


def test_gr02_vitalwert_blutdruck_physiologische_grenzen(app):
    """GR-02: Erzwingt systolisch > diastolisch im Bereich [30, 300] mmHg."""
    with app.test_request_context():
        # Ungültig: Diastolisch höher als Systolisch
        form_paradox = VitalwertForm(formdata=MultiDict({
            "kategorie": "Blutdruck",
            "systolisch": "80.0",
            "diastolisch": "120.0"
        }))
        assert not form_paradox.validate()
        alle_fehler = [err.lower() for fehlerliste in form_paradox.errors.values() for err in fehlerliste]
        assert any("systolisch" in err for err in alle_fehler)

        # Ungültig: Außerhalb des technischen Messbereichs (> 300)
        form_unrealistisch = VitalwertForm(formdata=MultiDict({
            "kategorie": "Blutdruck",
            "systolisch": "320.0",
            "diastolisch": "80.0"
        }))
        assert not form_unrealistisch.validate()
        assert "systolisch" in form_unrealistisch.errors

        # Valider Blutdruckwert
        form_valide = VitalwertForm(formdata=MultiDict({
            "kategorie": "Blutdruck",
            "systolisch": "125.0",
            "diastolisch": "82.0"
        }))
        assert form_valide.validate(), f"Validierung fehlgeschlagen: {form_valide.errors}"


def test_gr02_vitalwert_puls_und_gewicht(app):
    """GR-02: Validiert Pulsfrequenz (30-250 bpm) und Körpergewicht (2-300 kg)."""
    with app.test_request_context():
        # Ungültiger Puls zu niedrig (< 30)
        form_puls_low = VitalwertForm(formdata=MultiDict({"kategorie": "Puls", "einzelwert": "25.0"}))
        assert not form_puls_low.validate()

        # Ungültiges Gewicht zu hoch (> 300)
        form_gewicht_high = VitalwertForm(formdata=MultiDict({"kategorie": "Gewicht", "einzelwert": "350.0"}))
        assert not form_gewicht_high.validate()

        # Valider Puls
        form_puls_ok = VitalwertForm(formdata=MultiDict({"kategorie": "Puls", "einzelwert": "72.0"}))
        assert form_puls_ok.validate(), f"Puls-Validierung fehlgeschlagen: {form_puls_ok.errors}"

        # Valides Gewicht
        form_gew_ok = VitalwertForm(formdata=MultiDict({"kategorie": "Gewicht", "einzelwert": "75.5"}))
        assert form_gew_ok.validate(), f"Gewicht-Validierung fehlgeschlagen: {form_gew_ok.errors}"


def test_gr04_patient_geburtsdatum_in_der_vergangenheit(app):
    """GR-04: Das Geburtsdatum darf nicht in der Zukunft liegen."""
    with app.test_request_context():
        morgen = date.today() + timedelta(days=1)
        form_zukunft = PatientForm(formdata=MultiDict({
            "vorname": "Max",
            "nachname": "Mustermann",
            "geburtsdatum": morgen.strftime("%Y-%m-%d"),
            "notfallkontakt": "112"
        }))
        assert not form_zukunft.validate()
        assert "geburtsdatum" in form_zukunft.errors

        # Valides Geburtsdatum
        gestern = date.today() - timedelta(days=365 * 40)
        form_valide = PatientForm(formdata=MultiDict({
            "vorname": "Max",
            "nachname": "Mustermann",
            "geburtsdatum": gestern.strftime("%Y-%m-%d"),
            "notfallkontakt": "112"
        }))
        assert form_valide.validate()


def test_bericht_form_chronologie(app):
    """FA-03: Überprüft die Datumsbereichsvalidierung des PDF-Berichts."""
    with app.test_request_context():
        heute = date.today()
        gestern = heute - timedelta(days=1)
        
        # Ungültig: Startdatum nach Enddatum
        form_invalid = BerichtForm(formdata=MultiDict({
            "start_datum": heute.strftime("%Y-%m-%d"),
            "end_datum": gestern.strftime("%Y-%m-%d")
        }))
        assert not form_invalid.validate()
        assert "start_datum" in form_invalid.errors

        # Gültig: Startdatum vor Enddatum
        form_valid = BerichtForm(formdata=MultiDict({
            "start_datum": gestern.strftime("%Y-%m-%d"),
            "end_datum": heute.strftime("%Y-%m-%d")
        }))
        assert form_valid.validate()