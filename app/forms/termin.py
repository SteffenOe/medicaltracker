from flask_wtf import FlaskForm
from wtforms import  StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.fields import DateTimeLocalField

class TerminForm(FlaskForm):
    """Formular zur Erfassung und Bearbeitung von Pflegeterminen (FA-04)."""
    titel = StringField('Titel / Beschreibung', validators=[
        DataRequired(message="Bitte geben Sie einen Titel für den Termin ein."),
        Length(max=200, message="Der Titel darf maximal 200 Zeichen lang sein.")
    ])
    
    kategorie = SelectField('Kategorie', choices=[
        ('Arzttermin', 'Arzttermin / Facharzt'),
        ('Therapie', 'Physio- / Ergotherapie'),
        ('Pflegedienst', 'Pflegedienst / Beratung'),
        ('Besorgung', 'Apotheke / Hilfsmittel'),
        ('Sonstiges', 'Sonstiges')
    ], validators=[DataRequired()])
    
    zeitpunkt = DateTimeLocalField('Datum und Uhrzeit', format='%Y-%m-%dT%H:%M', validators=[
        DataRequired(message="Bitte wählen Sie Datum und Uhrzeit aus.")
    ])
    
    submit = SubmitField('Termin speichern')