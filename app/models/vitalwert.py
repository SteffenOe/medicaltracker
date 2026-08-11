from app import db
from datetime import datetime

class Vitalwert(db.Model):
    __tablename__ = 'vitalwerte'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patienten.id'), nullable=False)
    zeitpunkt = db.Column(db.DateTime, default=datetime.now, nullable=False)
    kategorie = db.Column(db.String(50), nullable=False)  # Blutdruck_Systolisch, Puls, Gewicht
    wert = db.Column(db.Float, nullable=False)
    einheit = db.Column(db.String(20), nullable=False)