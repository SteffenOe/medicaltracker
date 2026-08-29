from datetime import date, timedelta, datetime
from flask import Blueprint, render_template, send_file, flash, redirect, url_for
from app.models import Patient, Medikament, Vitalwert, EinnahmeProtokoll
from app.forms import BerichtForm
from app.services.pdf_generator import erstelle_arztbericht_pdf

berichte_bp = Blueprint('berichte', __name__, url_prefix='/berichte')

@berichte_bp.route('/', methods=['GET', 'POST'])
def index():
    """Zeigt das Filterformular für den PDF-Export an und verarbeitet den Download."""
    patient = Patient.query.first()
    if not patient:
        flash('Bitte legen Sie zuerst einen Patienten an.', 'danger')
        return redirect(url_for('main.dashboard'))

    heute = date.today()
    vor_30_tagen = heute - timedelta(days=30)
    
    form = BerichtForm(start_datum=vor_30_tagen, end_datum=heute)

    if form.validate_on_submit():
        start_d = form.start_datum.data
        end_d = form.end_datum.data
        
        start_dt = datetime.combine(start_d, datetime.min.time())
        end_dt = datetime.combine(end_d, datetime.max.time())

        medikamente = Medikament.query.filter_by(patient_id=patient.id).all()
        
        vitalwerte = Vitalwert.query.filter(
            Vitalwert.patient_id == patient.id,
            Vitalwert.zeitpunkt >= start_dt,
            Vitalwert.zeitpunkt <= end_dt
        ).order_by(Vitalwert.zeitpunkt.asc()).all()

        einnahmen = EinnahmeProtokoll.query.filter(
            EinnahmeProtokoll.patient_id == patient.id,
            EinnahmeProtokoll.einnahme_zeitpunkt >= start_dt,
            EinnahmeProtokoll.einnahme_zeitpunkt <= end_dt
        ).order_by(EinnahmeProtokoll.einnahme_zeitpunkt.asc()).all()

        pdf_buffer = erstelle_arztbericht_pdf(
            patient=patient,
            medikamente=medikamente,
            vitalwerte=vitalwerte,
            einnahmen=einnahmen,
            start_datum=start_d,
            end_datum=end_d
        )

        dateiname = f"Arztbericht_{patient.nachname}_{start_d.strftime('%Y%m%d')}-{end_d.strftime('%Y%m%d')}.pdf"

        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=dateiname
        )

    return render_template('berichte/index.html', form=form, patient=patient)