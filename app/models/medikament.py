from app import db

class Medikament(db.Model):
    __tablename__ = 'medikamente'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patienten.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    dosierung = db.Column(db.String(50), nullable=False)
    tageszeit = db.Column(db.String(50), nullable=False)
    bestand = db.Column(db.Integer, nullable=False, default=0)
    mindestbestand = db.Column(db.Integer, nullable=False, default=5)

    einnahmen = db.relationship('EinnahmeProtokoll', backref='medikament', lazy=True, cascade="all, delete-orphan")