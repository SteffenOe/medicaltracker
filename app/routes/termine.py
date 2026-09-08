"""Controller für den Alltags- und Pflegeterminkalender."""

from flask import Blueprint, render_template, redirect, url_for, flash
from app.models import db, Patient, Termin
from app.forms import TerminForm

termine_bp = Blueprint('termine', __name__, url_prefix='/termine')

@termine_bp.route('/')
def index():
    """Übersicht aller anstehenden und erledigten Termine."""
    patient = Patient.query.first()
    offene_termine = []
    erledigte_termine = []

    if patient:
        offene_termine = Termin.query.filter_by(patient_id=patient.id, erledigt=False)\
            .order_by(Termin.zeitpunkt.asc()).all()
        erledigte_termine = Termin.query.filter_by(patient_id=patient.id, erledigt=True)\
            .order_by(Termin.zeitpunkt.desc()).all()

    return render_template('termine/index.html', 
                           patient=patient, 
                           offene_termine=offene_termine, 
                           erledigte_termine=erledigte_termine)

@termine_bp.route('/neu', methods=['GET', 'POST'])
def neu():
    """Erfasst einen neuen Pflegetermin."""
    patient = Patient.query.first()
    if not patient:
        flash('Bitte legen Sie zuerst einen Patienten an.', 'danger')
        return redirect(url_for('main.dashboard'))

    form = TerminForm()
    if form.validate_on_submit():
        neuer_termin = Termin(
            patient_id=patient.id,
            titel=form.titel.data.strip(),
            kategorie=form.kategorie.data,
            zeitpunkt=form.zeitpunkt.data,
            erledigt=False
        )
        db.session.add(neuer_termin)
        db.session.commit()

        flash(f'Termin "{neuer_termin.titel}" erfolgreich angelegt.', 'success')
        return redirect(url_for('termine.index'))

    return render_template('termine/form.html', form=form, title="Neuen Termin anlegen")

@termine_bp.route('/<int:id>/bearbeiten', methods=['GET', 'POST'])
def bearbeiten(id):
    """Bearbeitet einen bestehenden Termin."""
    termin = Termin.query.get_or_404(id)
    form = TerminForm(obj=termin)

    if form.validate_on_submit():
        termin.titel = form.titel.data.strip()
        termin.kategorie = form.kategorie.data
        termin.zeitpunkt = form.zeitpunkt.data
        db.session.commit()

        flash(f'Änderungen am Termin "{termin.titel}" gespeichert.', 'success')
        return redirect(url_for('termine.index'))

    return render_template('termine/form.html', form=form, title=f"Termin bearbeiten: {termin.titel}")

@termine_bp.route('/<int:id>/toggle', methods=['POST'])
def toggle(id):
    """Schaltet den Status (erledigt / offen) eines Termins um."""
    termin = Termin.query.get_or_404(id)
    termin.erledigt = not termin.erledigt
    db.session.commit()

    status_text = "als erledigt markiert" if termin.erledigt else "wieder als offen markiert"
    flash(f'Termin "{termin.titel}" wurde {status_text}.', 'info')
    return redirect(url_for('termine.index'))

@termine_bp.route('/<int:id>/loeschen', methods=['POST'])
def loeschen(id):
    """Löscht einen Termin dauerhaft."""
    termin = Termin.query.get_or_404(id)
    titel = termin.titel

    db.session.delete(termin)
    db.session.commit()

    flash(f'Termin "{titel}" wurde gelöscht.', 'info')
    return redirect(url_for('termine.index'))