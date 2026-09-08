from datetime import date, datetime
from flask import Blueprint, render_template, redirect, url_for, flash
from app import db
from app.models import Patient, Medikament, EinnahmeProtokoll, Termin
from app.utils import ist_einnahme_ueberfaellig
from app.forms import PatientForm

patient_bp = Blueprint('patient', __name__, url_prefix='/patient')

TAGESZEITEN_ORDNUNG = ['Morgens', 'Mittags', 'Abends', 'Nachts', 'Bei Bedarf']

@patient_bp.route('/')
def tagesansicht():
    """Barrierefreie Tagesansicht."""
    patient = Patient.query.first()
    heute = date.today()
    
    gruppierte_medikamente = {}
    gesamt_anzahl = 0
    erledigt_anzahl = 0
    termine_heute = []
    
    if patient:
        termine_heute = Termin.query.filter(
            Termin.patient_id == patient.id,
            db.func.date(Termin.zeitpunkt) == heute
        ).order_by(Termin.zeitpunkt.asc()).all()

        medikamente = Medikament.query.filter_by(patient_id=patient.id).all()
        
        einnahmen_heute = EinnahmeProtokoll.query.filter(
            EinnahmeProtokoll.patient_id == patient.id,
            db.func.date(EinnahmeProtokoll.einnahme_zeitpunkt) == heute
        ).all()
        einnahmen_dict = {e.medikament_id: e for e in einnahmen_heute}
        
        for tz in TAGESZEITEN_ORDNUNG:
            gruppierte_medikamente[tz] = []
            
        for med in medikamente:
            protokoll = einnahmen_dict.get(med.id)
            ist_erledigt = protokoll is not None
            ueberfaellig = ist_einnahme_ueberfaellig(med.tageszeit, ist_erledigt)
            
            gesamt_anzahl += 1
            if ist_erledigt:
                erledigt_anzahl += 1
            
            eintrag = {
                'medikament': med,
                'eingenommen': ist_erledigt,
                'zeitpunkt': protokoll.einnahme_zeitpunkt if protokoll else None,
                'ueberfaellig': ueberfaellig
            }
            
            if med.tageszeit in gruppierte_medikamente:
                gruppierte_medikamente[med.tageszeit].append(eintrag)
            else:
                gruppierte_medikamente.setdefault('Bei Bedarf', []).append(eintrag)
                
        gruppierte_medikamente = {tz: liste for tz, liste in gruppierte_medikamente.items() if liste}

    return render_template(
        'patient/tagesansicht.html', 
        patient=patient, 
        gruppierte_medikamente=gruppierte_medikamente, 
        gesamt_anzahl=gesamt_anzahl,
        erledigt_anzahl=erledigt_anzahl,
        termine_heute=termine_heute,
        heute=heute
    )

@patient_bp.route('/einnehmen/<int:medikament_id>', methods=['POST'])
def einnehmen(medikament_id):
    """Protokollierung & synchrone Bestandsdekrementierung."""
    medikament = Medikament.query.get_or_404(medikament_id)
    heute = date.today()

    bereits_eingenommen = EinnahmeProtokoll.query.filter(
        EinnahmeProtokoll.medikament_id == medikament.id,
        db.func.date(EinnahmeProtokoll.einnahme_zeitpunkt) == heute
    ).first()

    if not bereits_eingenommen:
        try:
            neues_protokoll = EinnahmeProtokoll(
                patient_id=medikament.patient_id,
                medikament_id=medikament.id,
                soll_tageszeit=medikament.tageszeit,
                einnahme_zeitpunkt=datetime.now(),
                erledigt=True
            )
            db.session.add(neues_protokoll)

            if medikament.bestand > 0:
                medikament.bestand -= 1

            db.session.commit()
        except Exception:
            db.session.rollback()
            flash("Fehler bei der Einnahmeverbuchung.", "danger")

    return redirect(url_for('patient.tagesansicht'))


@patient_bp.route('/termin-erledigen/<int:termin_id>', methods=['POST'])
def termin_erledigen(termin_id):
    """Ermöglicht der zu pflegenden Person das Abhaken von Tagesterminen."""
    termin = Termin.query.get_or_404(termin_id)
    
    termin.erledigt = not termin.erledigt
    db.session.commit()
    
    return redirect(url_for('patient.tagesansicht'))


@patient_bp.route('/profil', methods=['GET', 'POST'])
def profil():
    """Erfasst oder bearbeitet die Stammdaten der zu pflegenden Person."""
    patient = Patient.query.first()
    
    form = PatientForm(obj=patient) if patient else PatientForm()

    if form.validate_on_submit():
        if not patient:
            patient = Patient(
                vorname=form.vorname.data.strip(),
                nachname=form.nachname.data.strip(),
                geburtsdatum=form.geburtsdatum.data,
                notfallkontakt=form.notfallkontakt.data.strip()
            )
            db.session.add(patient)
            flash(f'Patient {patient.vorname} {patient.nachname} erfolgreich angelegt.', 'success')
        else:
            form.populate_obj(patient)
            flash('Patientenstammdaten erfolgreich aktualisiert.', 'success')

        db.session.commit()
        return redirect(url_for('main.dashboard'))

    return render_template('patient/profil.html', form=form, patient=patient)