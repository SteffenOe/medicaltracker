from flask_wtf import FlaskForm
from wtforms import  FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange,  Optional

class VitalwertForm(FlaskForm):
    """Formular zur Erfassung von Vitaldaten mit Schwellenwertprüfung."""
    kategorie = SelectField('Messkategorie', choices=[
        ('Blutdruck', 'Blutdruck (Systolisch / Diastolisch in mmHg)'),
        ('Puls', 'Pulsfrequenz (in bpm)'),
        ('Gewicht', 'Körpergewicht (in kg)')
    ], validators=[DataRequired()])

    systolisch = FloatField('Systolischer Wert (mmHg)', validators=[
        Optional(),
        NumberRange(min=30.0, max=300.0, message="Systole muss zwischen 30 und 300 mmHg liegen.")
    ])
    diastolisch = FloatField('Diastolischer Wert (mmHg)', validators=[
        Optional(),
        NumberRange(min=30.0, max=300.0, message="Diastole muss zwischen 30 und 300 mmHg liegen.")
    ])

    einzelwert = FloatField('Messwert', validators=[Optional()])

    submit = SubmitField('Messwert speichern')

    def validate(self, extra_validators=None):
        """Erweiterte Validierungslogik für physiologische Plausibilitätsregeln."""
        initial_validation = super().validate(extra_validators=extra_validators)
        if not initial_validation:
            return False

        kat = self.kategorie.data

        if kat == 'Blutdruck':
            if self.systolisch.data is None or self.diastolisch.data is None:
                self.systolisch.errors.append("Für die Blutdruckmessung müssen Systole und Diastole angegeben werden.")
                return False
            if self.systolisch.data <= self.diastolisch.data:
                self.systolisch.errors.append("Plausibilitätsfehler: Der systolische Wert muss größer als der diastolische Wert sein.")
                return False

        elif kat == 'Puls':
            if self.einzelwert.data is None:
                self.einzelwert.errors.append("Bitte geben Sie die Pulsfrequenz an.")
                return False
            if not (30.0 <= self.einzelwert.data <= 250.0):
                self.einzelwert.errors.append("Pulsfrequenz muss zwischen 30 und 250 bpm liegen.")
                return False

        elif kat == 'Gewicht':
            if self.einzelwert.data is None:
                self.einzelwert.errors.append("Bitte erfassen Sie das Körpergewicht.")
                return False
            if not (2.0 <= self.einzelwert.data <= 300.0):
                self.einzelwert.errors.append("Körpergewicht muss zwischen 2,0 und 300,0 kg liegen.")
                return False

        return True