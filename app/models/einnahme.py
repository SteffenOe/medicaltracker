from datetime import datetime
from app.models import db


class EinnahmeProtokoll(db.Model):
    """Revisionssichere Dokumentation vollzogener Einnahmen."""
    __tablename__ = 'einnahme_protokolle'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patienten.id'), nullable=False)
    medikament_id = db.Column(db.Integer, db.ForeignKey('medikamente.id'), nullable=False)
    soll_tageszeit = db.Column(db.String(50), nullable=False)
    einnahme_zeitpunkt = db.Column(db.DateTime, default=datetime.now)
    erledigt = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        return f"<EinnahmeProtokoll {self.id}: Med {self.medikament_id} am {self.einnahme_zeitpunkt:%Y-%m-%d %H:%M}>"