from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash
from app import db
from app.models import Patient, Vitalwert
from app.forms import VitalwertForm

vitaldaten_bp = Blueprint('vitaldaten', __name__, url_prefix='/vitaldaten')

@vitaldaten_bp.route('/')
def index():
    """Rendert die chronologische Verlaufshistorie aller Vitalwerte."""
    patient = Patient.query.first()
    vitalwerte = []
    
    if patient:
        vitalwerte = Vitalwert.query.filter_by(patient_id=patient.id)\
            .order_by(Vitalwert.zeitpunkt.desc()).all()
            
    return render_template('vitaldaten/index.html', patient=patient, vitalwerte=vitalwerte)

@vitaldaten_bp.route('/neu', methods=['GET', 'POST'])
def neu():
    """Erfasst neue Vitalwerte mit Schwellenwert- und Plausibilitätsprüfung."""
    patient = Patient.query.first()
    if not patient:
        flash('Bitte legen Sie zuerst einen Patienten an.', 'danger')
        return redirect(url_for('main.dashboard'))

    form = VitalwertForm()
    if form.validate_on_submit():
        kat = form.kategorie.data
        jetzt = datetime.now()

        try:
            if kat == 'Blutdruck':
                v_sys = Vitalwert(
                    patient_id=patient.id,
                    zeitpunkt=jetzt,
                    kategorie='Blutdruck_Systolisch',
                    wert=form.systolisch.data,
                    einheit='mmHg'
                )
                v_dia = Vitalwert(
                    patient_id=patient.id,
                    zeitpunkt=jetzt,
                    kategorie='Blutdruck_Diastolisch',
                    wert=form.diastolisch.data,
                    einheit='mmHg'
                )
                db.session.add_all([v_sys, v_dia])
                flash(f'Blutdruckmessung ({form.systolisch.data:.0f}/{form.diastolisch.data:.0f} mmHg) erfolgreich erfasst.', 'success')

            elif kat == 'Puls':
                v_puls = Vitalwert(
                    patient_id=patient.id,
                    zeitpunkt=jetzt,
                    kategorie='Puls',
                    wert=form.einzelwert.data,
                    einheit='bpm'
                )
                db.session.add(v_puls)
                flash(f'Pulsfrequenz ({form.einzelwert.data:.0f} bpm) erfolgreich dokumentiert.', 'success')

            elif kat == 'Gewicht':
                v_gew = Vitalwert(
                    patient_id=patient.id,
                    zeitpunkt=jetzt,
                    kategorie='Gewicht',
                    wert=form.einzelwert.data,
                    einheit='kg'
                )
                db.session.add(v_gew)
                flash(f'Körpergewicht ({form.einzelwert.data:.1f} kg) erfolgreich gespeichert.', 'success')

            db.session.commit()
            return redirect(url_for('vitaldaten.index'))

        except Exception:
            db.session.rollback()
            flash('Fehler beim Speichern der Vitaldaten. Transaktion zurückgesetzt.', 'danger')

    return render_template('vitaldaten/form.html', form=form)