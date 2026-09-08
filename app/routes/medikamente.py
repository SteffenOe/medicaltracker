"""Controller für die Verwaltung des Medikationsplans."""

from flask import Blueprint, render_template, redirect, url_for, flash
from app.models import db, Patient, Medikament
from app.forms import MedikamentForm

medikamente_bp = Blueprint('medikamente', __name__, url_prefix='/medikamente')

@medikamente_bp.route('/')
def index():
    """Index Layout für Medikemante"""
    patient = Patient.query.first()
    medikamente = []

    if patient:
        medikamente = Medikament.query.filter_by(patient_id=patient.id).all()

    return render_template('medikamente/index.html', patient=patient, medikamente=medikamente)

@medikamente_bp.route('/neu', methods=['GET', 'POST'])
def neu():
    """Erfasst ein neues Medikament mit Validierung."""
    patient = Patient.query.first()
    if not patient:
        flash('Bitte legen Sie zuerst einen Patienten an.', 'danger')
        return redirect(url_for('main.dashboard'))
        
    form = MedikamentForm()
    if form.validate_on_submit():
        neues_medikament = Medikament(
            patient_id=patient.id,
            name=form.name.data.strip(),
            dosierung=form.dosierung.data.strip(),
            tageszeit=form.tageszeit.data,
            bestand=form.bestand.data,
            mindestbestand=form.mindestbestand.data
        )
        db.session.add(neues_medikament)
        db.session.commit()
        
        flash(f'Das Medikament "{neues_medikament.name}" wurde erfolgreich gespeichert.', 'success')
        return redirect(url_for('medikamente.index'))
        
    return render_template('medikamente/form.html', form=form, title="Neues Medikament erfassen")

@medikamente_bp.route('/<int:id>/bearbeiten', methods=['GET', 'POST'])
def bearbeiten(id):
    """Bearbeitet ein bestehendes Medikament."""
    medikament = Medikament.query.get_or_404(id)
    
    form = MedikamentForm(obj=medikament)
    
    if form.validate_on_submit():
        form.populate_obj(medikament)
        medikament.name = form.name.data.strip()
        medikament.dosierung = form.dosierung.data.strip()
        
        db.session.commit()
        flash(f'Die Änderungen an "{medikament.name}" wurden erfolgreich übernommen.', 'success')
        return redirect(url_for('medikamente.index'))
        
    return render_template('medikamente/form.html', form=form, title=f'Medikament bearbeiten: {medikament.name}')

@medikamente_bp.route('/<int:id>/loeschen', methods=['POST'])
def loeschen(id):
    """Löscht ein Medikament aus dem System."""
    medikament = Medikament.query.get_or_404(id)
    medikament_name = medikament.name
    
    db.session.delete(medikament)
    db.session.commit()
    
    flash(f'Das Medikament "{medikament_name}" wurde erfolgreich gelöscht.', 'info')
    return redirect(url_for('medikamente.index'))