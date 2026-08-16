from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Patient, Medikament

medikamente_bp = Blueprint('medikamente', __name__, url_prefix='/medikamente')

@medikamente_bp.route('/')
def index():
    """Index Layout für Medikemante"""
    patient = Patient.query.first()
    medikamente = []
    
    if patient:
        medikamente = Medikament.query.filter_by(patient_id=patient.id).all()
        
    return render_template('medikamente.html', patient=patient, medikamente=medikamente)