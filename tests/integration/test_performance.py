"""
Verifikation der Performanzmetriken (NFA-02) und Skalierbarkeit (NFA-07).
Simuliert eine mehrjährige Chronik mit 10.000 Datensätzen.
"""
import time
from datetime import datetime, timedelta, date
from app.models import db, Vitalwert, EinnahmeProtokoll
from app.services.pdf_generator import erstelle_arztbericht_pdf


def test_nfa07_skalierbarkeit_und_nfa02_latenz(client, sample_patient, sample_medikament):
    """
    NFA-07 / NFA-02: Befüllt die Datenbank mit 10.000 historischen Datensätzen
    und misst Ladezeiten für Datenbank, Dashboard und PDF-Reporting.
    """
    # 1. Massendaten generieren (Bulk-Insert für 10.000 Datensätze)
    print("\n[BENCHMARK] Generiere 10.000 Datensätze...")
    start_seed = time.perf_counter()
    
    basis_zeit = datetime.now()
    vitalwerte_bulk = []
    protokolle_bulk = []

    # 5.000 Vitalwerte und 5.000 Einnahmeprotokolle erzeugen
    for i in range(5000):
        t = basis_zeit - timedelta(hours=i)
        vitalwerte_bulk.append(Vitalwert(
            patient_id=sample_patient.id,
            zeitpunkt=t,
            kategorie="Blutdruck_Systolisch",
            wert=120.0 + (i % 20),
            einheit="mmHg"
        ))
        protokolle_bulk.append(EinnahmeProtokoll(
            patient_id=sample_patient.id,
            medikament_id=sample_medikament.id,
            soll_tageszeit="Morgens",
            einnahme_zeitpunkt=t,
            erledigt=True
        ))

    db.session.bulk_save_objects(vitalwerte_bulk)
    db.session.bulk_save_objects(protokolle_bulk)
    db.session.commit()
    seed_dauer = time.perf_counter() - start_seed
    print(f"[BENCHMARK] 10.000 Datensätze persistiert in: {seed_dauer:.3f} s")

    # Verifikation der Datenmenge
    anzahl_vital = Vitalwert.query.filter_by(patient_id=sample_patient.id).count()
    anzahl_prot = EinnahmeProtokoll.query.filter_by(patient_id=sample_patient.id).count()
    assert (anzahl_vital + anzahl_prot) == 10000

    # 2. Messung der DB-Abfragezeit (Ziel NFA-02: <= 200 ms)
    start_db = time.perf_counter()
    _ = Vitalwert.query.filter_by(patient_id=sample_patient.id)\
        .order_by(Vitalwert.zeitpunkt.desc()).limit(5).all()
    db_latenz_ms = (time.perf_counter() - start_db) * 1000
    print(f"[BENCHMARK] DB-Query Latenz (Top 5 aus 10.000): {db_latenz_ms:.2f} ms")
    assert db_latenz_ms < 200.0, f"DB zu langsam: {db_latenz_ms:.2f} ms"

    # 3. Messung der View-Renderzeit Dashboard (Ziel NFA-02: <= 1,0 s)
    start_render = time.perf_counter()
    response_dash = client.get("/")
    render_dauer_s = time.perf_counter() - start_render
    print(f"[BENCHMARK] Dashboard View-Ladezeit: {render_dauer_s:.3f} s")
    assert response_dash.status_code == 200
    assert render_dauer_s < 1.0, f"Dashboard-Renderzeit überschritten: {render_dauer_s:.3f} s"

    # 4. Messung der PDF-Generierungszeit (Ziel NFA-02: <= 2,0 s für 30-Tage-Historie)
    stichtag = date.today()
    vor_30_tagen = stichtag - timedelta(days=30)
    start_dt = datetime.combine(vor_30_tagen, datetime.min.time())
    
    gefilterte_vital = Vitalwert.query.filter(
        Vitalwert.patient_id == sample_patient.id,
        Vitalwert.zeitpunkt >= start_dt
    ).all()
    gefilterte_einn = EinnahmeProtokoll.query.filter(
        EinnahmeProtokoll.patient_id == sample_patient.id,
        EinnahmeProtokoll.einnahme_zeitpunkt >= start_dt
    ).all()

    start_pdf = time.perf_counter()
    _ = erstelle_arztbericht_pdf(
        patient=sample_patient,
        medikamente=[sample_medikament],
        vitalwerte=gefilterte_vital,
        einnahmen=gefilterte_einn,
        start_datum=vor_30_tagen,
        end_datum=stichtag
    )
    pdf_dauer_s = time.perf_counter() - start_pdf
    print(f"[BENCHMARK] PDF-Generierung ({len(gefilterte_vital)} Vitalwerte): {pdf_dauer_s:.3f} s")
    assert pdf_dauer_s < 2.0, f"PDF-Generierung zu langsam: {pdf_dauer_s:.3f} s"