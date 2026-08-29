import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Zweistufiger Canvas-Renderer für konsistente Seitenzahlen und Footer."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#7f8c8d"))
        
        self.setStrokeColor(colors.HexColor("#bdc3c7"))
        self.setLineWidth(0.5)
        self.line(40, 45, 555, 45)
        
        hinweis = "Medical Tracker • Privates Pflegedokumentationssystem (Kein zertifiziertes Medizinprodukt)"
        self.drawString(40, 32, hinweis)
        self.drawRightString(555, 32, f"Seite {self._pageNumber} von {page_count}")
        self.restoreState()


def erstelle_arztbericht_pdf(patient, medikamente, vitalwerte, einnahmen, start_datum, end_datum) -> io.BytesIO:
    """Generiert einen dynamischen, druckoptimierten PDF-Arztbericht im Arbeitsspeicher."""
    buffer = io.BytesIO()
    
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=55
    )

    story = []
    styles = getSampleStyleSheet()

    primary_color = colors.HexColor("#2c3e50")
    secondary_color = colors.HexColor("#34495e")
    accent_blue = colors.HexColor("#2980b9")
    light_bg = colors.HexColor("#f8f9fa")

    style_title = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=primary_color,
        spaceAfter=4
    )
    
    style_subtitle = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#7f8c8d"),
        spaceAfter=12
    )

    style_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=secondary_color,
        spaceBefore=12,
        spaceAfter=6
    )

    style_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11
    )

    style_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=style_cell,
        fontName='Helvetica-Bold'
    )

    story.append(Paragraph("ÄRZTLICHER VERLAUFS- UND MEDIKATIONSBERICHT", style_title))
    zeitraum_str = f"Berichtszeitraum: {start_datum.strftime('%d.%m.%Y')} bis {end_datum.strftime('%d.%m.%Y')} • Erstellt am: {datetime.now().strftime('%d.%m.%Y um %H:%M Uhr')}"
    story.append(Paragraph(zeitraum_str, style_subtitle))
    story.append(HRFlowable(width="100%", thickness=1.5, color=accent_blue, spaceBefore=0, spaceAfter=10))

    stammdaten = [
        [
            Paragraph(f"<b>Patient:</b> {patient.nachname}, {patient.vorname}", style_cell),
            Paragraph(f"<b>Geburtsdatum:</b> {patient.geburtsdatum.strftime('%d.%m.%Y')}", style_cell),
            Paragraph(f"<b>Notfallkontakt:</b> {patient.notfallkontakt or 'Nicht hinterlegt'}", style_cell)
        ]
    ]
    t_stamm = Table(stammdaten, colWidths=[180, 150, 185])
    t_stamm.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), light_bg),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#bdc3c7")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#ecf0f1")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_stamm)
    story.append(Spacer(1, 10))

    story.append(Paragraph("1. Aktueller Medikationsplan (Dauermedikation)", style_heading))
    if medikamente:
        med_table_data = [[
            Paragraph("Medikamentenname", style_cell_bold),
            Paragraph("Dosierung", style_cell_bold),
            Paragraph("Einnahmezeit", style_cell_bold),
            Paragraph("Bestand", style_cell_bold)
        ]]
        for med in medikamente:
            med_table_data.append([
                Paragraph(med.name, style_cell_bold),
                Paragraph(med.dosierung, style_cell),
                Paragraph(med.tageszeit, style_cell),
                Paragraph(f"{med.bestand} Stk.", style_cell)
            ])
        t_med = Table(med_table_data, colWidths=[180, 135, 120, 80])
        t_med.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#eaecee")),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#bdc3c7")),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(t_med)
    else:
        story.append(Paragraph("<i>Keine aktiven Medikamente verzeichnet.</i>", style_cell))

    story.append(Spacer(1, 10))

    story.append(Paragraph(f"2. Dokumentierte Vitalwerte im Zeitraum ({len(vitalwerte)} Messungen)", style_heading))
    if vitalwerte:
        vital_table_data = [[
            Paragraph("Datum & Uhrzeit", style_cell_bold),
            Paragraph("Messkategorie", style_cell_bold),
            Paragraph("Messwert", style_cell_bold),
            Paragraph("Einheit", style_cell_bold)
        ]]
        for v in vitalwerte:
            vital_table_data.append([
                Paragraph(v.zeitpunkt.strftime('%d.%m.%Y %H:%M'), style_cell),
                Paragraph(v.kategorie.replace('_', ' '), style_cell),
                Paragraph(f"<b>{v.wert:.1f}</b>" if isinstance(v.wert, float) else f"<b>{v.wert}</b>", style_cell),
                Paragraph(v.einheit, style_cell)
            ])
        t_vital = Table(vital_table_data, colWidths=[130, 175, 130, 80])
        t_vital.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#eaecee")),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
            ('TOPPADDING', (0, 0), (-1, -1), 3.5),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#bdc3c7")),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(t_vital)
    else:
        story.append(Paragraph("<i>Für den gewählten Zeitraum wurden keine Vitaldaten dokumentiert.</i>", style_cell))

    story.append(Spacer(1, 10))

    story.append(Paragraph(f"3. Nachweis Einnahmetreue / Compliance ({len(einnahmen)} Bestätigungen)", style_heading))
    if einnahmen:
        einn_table_data = [[
            Paragraph("Tatsächlicher Zeitpunkt", style_cell_bold),
            Paragraph("Geplante Tageszeit", style_cell_bold),
            Paragraph("Medikament (ID)", style_cell_bold),
            Paragraph("Status", style_cell_bold)
        ]]
        for e in einnahmen:
            einn_table_data.append([
                Paragraph(e.einnahme_zeitpunkt.strftime('%d.%m.%Y %H:%M Uhr'), style_cell),
                Paragraph(e.soll_tageszeit, style_cell),
                Paragraph(f"Medikament #{e.medikament_id}", style_cell),
                Paragraph("<font color='#27ae60'><b>Eingenommen</b></font>", style_cell)
            ])
        t_einn = Table(einn_table_data, colWidths=[150, 135, 130, 100])
        t_einn.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#eaecee")),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
            ('TOPPADDING', (0, 0), (-1, -1), 3.5),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#bdc3c7")),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(t_einn)
    else:
        story.append(Paragraph("<i>Im gewählten Zeitraum liegen keine protokollierten Einnahmebestätigungen vor.</i>", style_cell))

    doc.build(story, canvasmaker=NumberedCanvas)
    buffer.seek(0)
    return buffer