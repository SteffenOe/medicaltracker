from app import db
from datetime import datetime

class EinnahmeProtokoll(db.Model):
    __tablename__ = 'einnahme_protokolle'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patienten.id'), nullable=False)
    medikament_id = db.Column(db.Integer, db.ForeignKey('medikamente.id'), nullable=False)
    soll_tageszeit = db.Column(db.String(50), nullable=False)
    einnahme_zeitpunkt = db.Column(db.DateTime, default=datetime.now)
    erledigt = db.Column(db.Boolean, default=False, nullable=False)