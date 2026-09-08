from datetime import datetime
from app.models import db

class Termin(db.Model):
    """Pflegetermin oder Alltagsaufgabe für das Angehörigen-Dashboard (FA-04)."""
    __tablename__ = 'termine'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patienten.id'), nullable=False)
    titel = db.Column(db.String(200), nullable=False)
    zeitpunkt = db.Column(db.DateTime, nullable=False)
    kategorie = db.Column(db.String(50), nullable=False)
    erledigt = db.Column(db.Boolean, default=False, nullable=False)

    @property
    def ist_faellig(self) -> bool:
        return not self.erledigt and self.zeitpunkt < datetime.now()

    def __repr__(self) -> str:
        return f"<Termin {self.id}: {self.titel}>"