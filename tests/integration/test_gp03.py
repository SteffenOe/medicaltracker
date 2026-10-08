"""
Integrationstest für den Kernprozess GP-03 (Einnahme & automatisierte Bestandsführung).
"""
from datetime import date
from app.models.einnahme import EinnahmeProtokoll


def test_gp03_erfolgreiche_einnahme_und_bestandsreduktion(client, db_session, sample_medikament):
    """FA-06 & FA-07: POST-Request erzeugt Protokolleintrag und verringert Bestand um 1."""
    initialer_bestand = sample_medikament.bestand

    # 1. Ausführen des Bestätigungs-Requests über den Test-Client
    response = client.post(
        f"/patient/einnehmen/{sample_medikament.id}",
        follow_redirects=True
    )
    assert response.status_code == 200

    # 2. Überprüfung der Persistenzschicht
    db_session.refresh(sample_medikament)
    assert sample_medikament.bestand == initialer_bestand - 1

    # 3. Überprüfung des Protokolleintrags (Audit Trail)
    protokolle = EinnahmeProtokoll.query.filter_by(
        medikament_id=sample_medikament.id
    ).all()
    assert len(protokolle) == 1
    assert protokolle[0].erledigt is True
    assert protokolle[0].einnahme_zeitpunkt.date() == date.today()


def test_gp03_nachbestell_warnung_bei_mindestbestand(client, db_session, sample_medikament):
    """FA-07: Triggert Warnhinweis, wenn Bestand <= Mindestbestand erreicht wird."""
    # Setze Bestand so, dass die nächste Einnahme den Schwellenwert berührt
    sample_medikament.bestand = 4
    sample_medikament.mindestbestand = 3
    db_session.commit()

    # Einnahme ausführen: Bestand sinkt von 4 auf 3 (bestand == mindestbestand)
    response = client.post(
        f"/patient/einnehmen/{sample_medikament.id}",
        follow_redirects=True
    )
    assert response.status_code == 200

    db_session.refresh(sample_medikament)
    assert sample_medikament.bestand == 3

    # Dashboard für Angehörige abrufen und Warnmeldung prüfen
    dash_response = client.get("/")
    assert dash_response.status_code == 200
    # Überprüfung auf visuelle Warnklassen oder Signalwörter im gerenderten HTML
    assert (
        b"Niedrig" in dash_response.data 
        or b"WARNUNG" in dash_response.data 
        or b"badge bg-danger" in dash_response.data
    )


def test_gp03_verhinderung_doppelter_tageseinnahme(client, db_session, sample_medikament):
    """Verhindert versehentliche doppelte Bestätigungen am selben Tag."""
    # Erste Einnahme erfolgreich
    client.post(f"/patient/einnehmen/{sample_medikament.id}", follow_redirects=True)
    db_session.refresh(sample_medikament)
    bestand_nach_erster = sample_medikament.bestand

    # Zweite Einnahme am selben Tag
    response_doppelt = client.post(
        f"/patient/einnehmen/{sample_medikament.id}",
        follow_redirects=True
    )
    assert response_doppelt.status_code == 200

    # Bestand darf sich nicht erneut verringern
    db_session.refresh(sample_medikament)
    assert sample_medikament.bestand == bestand_nach_erster

    # Es darf weiterhin nur genau ein Protokolleintrag für heute existieren
    protokolle = EinnahmeProtokoll.query.filter_by(
        medikament_id=sample_medikament.id
    ).all()
    assert len(protokolle) == 1