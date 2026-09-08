from datetime import datetime
from app.models import db

class Vitalwert(db.Model):
    """Physiologische Einzelmessung im Zeitverlauf."""
    __tablename__ = 'vitalwerte'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patienten.id'), nullable=False)
    zeitpunkt = db.Column(db.DateTime, default=datetime.now, nullable=False)
    kategorie = db.Column(db.String(50), nullable=False)  # Blutdruck_Systolisch, Puls, Gewicht
    wert = db.Column(db.Float, nullable=False)
    einheit = db.Column(db.String(20), nullable=False)

    def __repr__(self) -> str:
        return f"<Vitalwert {self.kategorie}: {self.wert} {self.einheit}>"