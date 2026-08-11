from app import db

class Termin(db.Model):
    __tablename__ = 'termine'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patienten.id'), nullable=False)
    titel = db.Column(db.String(200), nullable=False)
    zeitpunkt = db.Column(db.DateTime, nullable=False)
    kategorie = db.Column(db.String(50), nullable=False)
    erledigt = db.Column(db.Boolean, default=False, nullable=False)