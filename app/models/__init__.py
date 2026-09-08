"""Persistenzschicht und ORM-Modelle"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.models.patient import Patient
from app.models.medikament import Medikament
from app.models.einnahme import EinnahmeProtokoll
from app.models.vitalwert import Vitalwert
from app.models.termin import Termin

__all__ = ['db', 'Patient', 'Medikament', 'EinnahmeProtokoll', 'Vitalwert', 'Termin']