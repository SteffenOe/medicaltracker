"""
Testet den ReportLab-PDF-Generierungsdienst und den HTTP-Download-Endpunkt.
"""
import io
from datetime import date, timedelta
from app.services.pdf_generator import erstelle_arztbericht_pdf


def test_pdf_service_in_memory_generierung(sample_patient, sample_medikament):
    """FA-03 / NFA-03: Überprüft, ob ein valider BytesIO-Bytestrom ohne Dateisystem-Rückstände erzeugt wird."""
    heute = date.today()
    start = heute - timedelta(days=30)
    
    pdf_buffer = erstelle_arztbericht_pdf(
        patient=sample_patient,
        medikamente=[sample_medikament],
        vitalwerte=[],
        einnahmen=[],
        start_datum=start,
        end_datum=heute
    )

    # 1. Puffer ist ein In-Memory-Stream (io.BytesIO)
    assert isinstance(pdf_buffer, io.BytesIO)
    pdf_bytes = pdf_buffer.getvalue()
    
    # 2. Puffer ist gefüllt und beginnt mit der standardisierten PDF-Signatur
    assert len(pdf_bytes) > 0
    assert pdf_bytes.startswith(b"%PDF-")


def test_berichte_route_http_download(client, db_session, sample_patient, sample_medikament):
    """FA-03: Prüft HTTP-Status 200 und PDF-Content-Type beim Absenden des Berichtsformulars."""
    heute = date.today()
    start = heute - timedelta(days=14)
    
    # POST-Request an die existierende Route /berichte/
    response = client.post("/berichte/", data={
        "start_datum": start.strftime("%Y-%m-%d"),
        "end_datum": heute.strftime("%Y-%m-%d")
    })
    
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/pdf"
    assert "attachment" in response.headers.get("Content-Disposition", "")
    assert response.data.startswith(b"%PDF-")