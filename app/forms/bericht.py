from flask_wtf import FlaskForm
from wtforms.fields import  DateField, SubmitField
from wtforms.validators import DataRequired

class BerichtForm(FlaskForm):
    """Formular zur Filterung des Berichtszeitraums für den PDF-Export."""
    start_datum = DateField('Startdatum', validators=[
        DataRequired(message="Bitte wählen Sie ein Startdatum.")
    ])
    end_datum = DateField('Enddatum', validators=[
        DataRequired(message="Bitte wählen Sie ein Enddatum.")
    ])
    submit = SubmitField('PDF-Bericht erstellen')

    def validate(self, extra_validators=None):
        """Prüft, ob das Startdatum chronologisch vor oder auf dem Enddatum liegt."""
        if not super().validate(extra_validators=extra_validators):
            return False
        
        if self.start_datum.data > self.end_datum.data:
            self.start_datum.errors.append("Das Startdatum darf nicht nach dem Enddatum liegen.")
            return False
        return True