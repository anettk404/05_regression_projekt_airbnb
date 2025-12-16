# In Ihrer Datei: src/haversine_distanz.py

import numpy as np
from geopy.geocoders import Nominatim 
import time # Wichtig für die Fehlerbehandlung

# ------------------------------------------------------------
# A. DEFINITION DER KONSTANTEN
# ------------------------------------------------------------
EARTH_RADIUS_KM = 6371

# ------------------------------------------------------------
# B. FUNKTION ZUR ENTFERNUNGSBERECHNUNG (Haversine)
# ------------------------------------------------------------
def calculate_distance(lat1, lon1, lat2, lon2, radius=EARTH_RADIUS_KM):
    """Berechnet die Entfernung zwischen zwei Punkten auf der Erde (km). (Vektorisiert)"""
    
    # !!! KORREKTUR: Alle vier Koordinaten in das Bogenmaß (Radians) umwandeln !!!
    lat1_rad = np.radians(lat1)
    lon1_rad = np.radians(lon1) # <-- Hinzufügen/Korrigieren
    lat2_rad = np.radians(lat2) # <-- Hinzufügen/Korrigieren
    lon2_rad = np.radians(lon2) # <-- Hinzufügen/Korrigieren

    # Berechnung der Differenzen
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    
    # Haversine-Formel
    a = np.sin(dlat / 2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    
    distance = radius * c
    return distance

# ------------------------------------------------------------
# C. FUNKTION ZUR ZENTRUMS-SUCHE (mit Fehlerbehandlung)
# ------------------------------------------------------------
def get_city_center_coords(city_name, max_retries=3):
    """
    Sucht die Koordinaten für eine Stadt über Nominatim (OpenStreetMap) 
    mit eingebauter Wiederholungslogik bei Timeouts.
    """
    geolocator = Nominatim(user_agent="airbnb_center_search") 
    
    for attempt in range(max_retries):
        try:
            location = geolocator.geocode(city_name, timeout=10) 
            
            if location:
                return location.latitude, location.longitude
            else:
                raise ValueError(f"Zentrum für '{city_name}' konnte nicht gefunden werden.")
                
        except Exception as e:
            if attempt < max_retries - 1:
                # Hier können Sie den print-Befehl auskommentieren, wenn Sie keine Meldungen sehen möchten
                # print(f"WARNUNG: Abruf für '{city_name}' fehlgeschlagen (Versuch {attempt + 1}). Warte 5s...")
                time.sleep(5) 
            else:
                raise ConnectionError(f"Fehler bei Geokodierung von '{city_name}' nach {max_retries} Versuchen: {e}")