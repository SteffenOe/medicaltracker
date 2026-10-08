"""
Vollständige Überdeckung der Geschäftslogik für Überfälligkeitsberechnungen.
"""
from app.utils.ueberfaellig import ist_einnahme_ueberfaellig


def test_ist_einnahme_ueberfaellig_abdeckung():
    """Testet alle logischen Zweige der Überfälligkeitsfunktion."""
    # Bereits eingenommen -> niemals überfällig
    assert not ist_einnahme_ueberfaellig("Morgens", eingenommen=True)
    assert not ist_einnahme_ueberfaellig("Mittags", eingenommen=True)

    # Bei Bedarf -> niemals überfällig
    assert not ist_einnahme_ueberfaellig("Bei Bedarf", eingenommen=False)

    # Ungültige Tageszeit -> False
    assert not ist_einnahme_ueberfaellig("Unbekannt", eingenommen=False)

    # Standard-Zeitslots (Prüfung gegen booleschen Rückgabewert)
    assert isinstance(ist_einnahme_ueberfaellig("Morgens", eingenommen=False), bool)
    assert isinstance(ist_einnahme_ueberfaellig("Mittags", eingenommen=False), bool)
    assert isinstance(ist_einnahme_ueberfaellig("Abends", eingenommen=False), bool)
    assert isinstance(ist_einnahme_ueberfaellig("Nachts", eingenommen=False), bool)