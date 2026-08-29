from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length

class MedikamentForm(FlaskForm):
    """Formular zur Erfassung und Bearbeitung von Medikamenten."""
    name = StringField('Medikamentenname', validators=[
        DataRequired(message="Bitte geben Sie den Namen des Medikaments an."),
        Length(max=150, message="Der Name darf maximal 150 Zeichen lang sein.")
    ])
    
    dosierung = StringField('Dosierung (z. B. 1 Tablette, 10 Tropfen)', validators=[
        DataRequired(message="Bitte geben Sie die verordnete Dosierung an."),
        Length(max=50)
    ])
    
    tageszeit = SelectField('Einnahmezeitpunkt', choices=[
        ('Morgens', 'Morgens'),
        ('Mittags', 'Mittags'),
        ('Abends', 'Abends'),
        ('Nachts', 'Nachts'),
        ('Bei Bedarf', 'Bei Bedarf')
    ], validators=[DataRequired()])
    
    bestand = IntegerField('Aktueller Bestand (Packungsinhalt)', validators=[
        DataRequired(message="Bitte erfassen Sie den Anfangsbestand."),
        NumberRange(min=0, message="Der Bestand darf nicht negativ sein.")
    ], default=20)
    
    mindestbestand = IntegerField('Mindestbestand (Warnschwelle)', validators=[
        DataRequired(message="Bitte definieren Sie einen Mindestbestand."),
        NumberRange(min=0, message="Der Mindestbestand darf nicht negativ sein.")
    ], default=5)
    
    submit = SubmitField('Medikament speichern')