from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

class PatientForm(FlaskForm):
    """Formular zur Erfassung und Pflege der Patientenstammdaten."""
    vorname = StringField('Vorname', validators=[
        DataRequired(message="Bitte geben Sie den Vornamen an."),
        Length(max=100)
    ])
    nachname = StringField('Nachname', validators=[
        DataRequired(message="Bitte geben Sie den Nachnamen an."),
        Length(max=100)
    ])
    geburtsdatum = DateField('Geburtsdatum', validators=[
        DataRequired(message="Bitte wählen Sie ein Geburtsdatum aus.")
    ])
    notfallkontakt = StringField('Notfallkontakt (z. B. Name & Telefonnummer)', validators=[
        DataRequired(message="Bitte hinterlegen Sie mindestens einen Notfallkontakt."),
        Length(max=200)
    ])
    submit = SubmitField('Patientendaten speichern')

    def validate_geburtsdatum(self, field):
        """Implementierung der Geschäftsregel: geburtsdatum < datum_aktuell."""
        if field.data and field.data >= date.today():
            raise ValidationError("Plausibilitätsfehler: Das Geburtsdatum muss in der Vergangenheit liegen.")