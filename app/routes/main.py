"""Controller für das zentrale Angehörigen-Dashboard (Verwaltungsmodus)."""

from datetime import date
import locale
from flask import Blueprint, render_template, redirect, url_for, flash
from app.models import db, Patient, Medikament, Vitalwert, Termin, EinnahmeProtokoll
from app.utils import ist_einnahme_ueberfaellig


locale.setlocale(locale.LC_TIME, "de_DE")

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def dashboard():    
    """Dashboard Layout"""
    patient = Patient.query.first()
    if not patient:
            flash('Willkommen beim Medical Tracker! Bitte erfassen Sie zunächst die Stammdaten der zu pflegenden Person.', 'info')
            return redirect(url_for('patient.profil'))


    heute = date.today()
    
    medikamente = []
    vitalwerte = []
    termine = []
    kritische_medikamente = []
    ueberfaellige_einnahmen = []
    
    if patient:
        # Auswertung kritischer Bestände gemäß Schwellenwert-Logik
        medikamente = Medikament.query.filter_by(patient_id=patient.id).all()
        kritische_medikamente = [m for m in medikamente if m.ist_nachbestellung_erforderlich]
        
        einnahmen_heute = EinnahmeProtokoll.query.filter(
            EinnahmeProtokoll.patient_id == patient.id,
            db.func.date(EinnahmeProtokoll.einnahme_zeitpunkt) == heute
        ).all()
        eingenommene_ids = {e.medikament_id for e in einnahmen_heute}

        for m in medikamente:
            if ist_einnahme_ueberfaellig(m.tageszeit, m.id in eingenommene_ids):
                ueberfaellige_einnahmen.append(m)

        # Chronologische Selektion anstehender Pflegetermine und neuester Messwerte
        vitalwerte = Vitalwert.query.filter_by(patient_id=patient.id).order_by(Vitalwert.zeitpunkt.desc()).limit(5).all()
        termine = Termin.query.filter_by(patient_id=patient.id, erledigt=False).order_by(Termin.zeitpunkt.asc()).limit(5).all()

    return render_template('dashboard.html', 
                           patient=patient, 
                           medikamente=medikamente, 
                           kritische_medikamente=kritische_medikamente,
                           ueberfaellige_einnahmen=ueberfaellige_einnahmen,
                           vitalwerte=vitalwerte, 
                           termine=termine)