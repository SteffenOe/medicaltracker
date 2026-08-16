from flask import Blueprint, render_template
from app.models import Patient, Medikament, Vitalwert, Termin

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def dashboard():
    """Dashboard für die Index Route"""
    patient = Patient.query.first()
    
    medikamente = []
    vitalwerte = []
    termine = []
    
    if patient:
        medikamente = Medikament.query.filter_by(patient_id=patient.id).all()
        vitalwerte = Vitalwert.query.filter_by(patient_id=patient.id).order_by(Vitalwert.zeitpunkt.desc()).limit(5).all()
        termine = Termin.query.filter_by(patient_id=patient.id).order_by(Termin.zeitpunkt.asc()).all()

    return render_template('base.html', 
                           patient=patient, 
                           medikamente=medikamente, 
                           vitalwerte=vitalwerte, 
                           termine=termine)