from datetime import datetime

ZEITFENSTER_ENDE = {
    'Morgens': 11,      # Ab 11:00 Uhr überfällig
    'Mittags': 15,      # Ab 15:00 Uhr überfällig
    'Abends': 21,       # Ab 21:00 Uhr überfällig
    'Nachts': 5,        # Ab 05:00 Uhr am Folgemorgen
    'Bei Bedarf': 24    # Bedarfmedikation wird nie überfällig
}

def ist_einnahme_ueberfaellig(tageszeit: str, eingenommen: bool) -> bool:
    """Prüft, ob der geplante Einnahmezeitpunkt für den heutigen Tag überschritten ist."""
    if eingenommen or tageszeit not in ZEITFENSTER_ENDE or tageszeit == 'Bei Bedarf':
        return False
    
    aktuelle_stunde = datetime.now().hour
    grenz_stunde = ZEITFENSTER_ENDE[tageszeit]

    if tageszeit == 'Nachts':
        return 5 <= aktuelle_stunde < 22

    return aktuelle_stunde >= grenz_stunde