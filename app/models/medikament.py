from app.models import db

class Medikament(db.Model):
    """Verordnetes Medikament mit Bestandsführung und Schwellenwert-Logik."""
    __tablename__ = 'medikamente'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patienten.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    dosierung = db.Column(db.String(50), nullable=False)
    tageszeit = db.Column(db.String(50), nullable=False)
    bestand = db.Column(db.Integer, nullable=False, default=0)
    mindestbestand = db.Column(db.Integer, nullable=False, default=5)

    einnahmen = db.relationship('EinnahmeProtokoll', backref='medikament', lazy=True, cascade="all, delete-orphan")

    @property
    def ist_nachbestellung_erforderlich(self) -> bool:
        """Prüft Schwellenwert für Warnmeldung auf dem Dashboard."""
        return self.bestand <= self.mindestbestand

    def __repr__(self) -> str:
        return f"<Medikament {self.id}: {self.name} ({self.bestand} Stk.)>"