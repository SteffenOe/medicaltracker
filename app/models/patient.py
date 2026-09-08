from app import db

class Patient(db.Model):
    __tablename__ = 'patienten'

    id = db.Column(db.Integer, primary_key=True)
    vorname = db.Column(db.String(100), nullable=False)
    nachname = db.Column(db.String(100), nullable=False)
    geburtsdatum = db.Column(db.Date, nullable=False)
    notfallkontakt = db.Column(db.String(200), nullable=True)

    medikamente = db.relationship('Medikament', backref='patient', lazy=True, cascade="all, delete-orphan")
    einnahmen = db.relationship('EinnahmeProtokoll', backref='patient', lazy=True, cascade="all, delete-orphan")
    vitalwerte = db.relationship('Vitalwert', backref='patient', lazy=True, cascade="all, delete-orphan")
    termine = db.relationship('Termin', backref='patient', lazy=True, cascade="all, delete-orphan")