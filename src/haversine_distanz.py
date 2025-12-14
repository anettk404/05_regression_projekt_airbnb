import numpy as np
import pandas as pd

# Wir gehen davon aus, dass df_model nur die ausgewählten Spalten enthält:
# ['ln_price', 'accommodates', 'number_of_reviews_ltm', 'review_scores_rating', 
#  'host_total_listings_count', 'minimum_nights', 'latitude', 'longitude', 
#  'room_type', 'neighbourhood_group_cleansed']

# ------------------------------------------------------------
# A. DEFINITION DES ZENTRUMSPUNKTS (Times Square)
# ------------------------------------------------------------
CENTER_LAT = 40.7580
CENTER_LON = -73.9855
EARTH_RADIUS_KM = 6371

# ------------------------------------------------------------
# B. FUNKTION ZUR ENTFERNUNGSBERECHNUNG (Haversine)
# ------------------------------------------------------------
def calculate_distance(lat1, lon1, lat2, lon2):
    """Berechnet die Entfernung zwischen zwei Punkten auf der Erde (km)."""
    lat1_rad = np.radians(lat1)
    lon1_rad = np.radians(lon1)
    lat2_rad = np.radians(lat2)
    lon2_rad = np.radians(lon2)
    
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    
    a = np.sin(dlat / 2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    
    distance = EARTH_RADIUS_KM * c
    return distance

# ------------------------------------------------------------
# C. ANWENDUNG DER FUNKTION UND ERSTELLEN DER NEUEN SPALTE
# ------------------------------------------------------------
df_model['distance_to_center'] = calculate_distance(
    df_model['latitude'], 
    df_model['longitude'], 
    CENTER_LAT, 
    CENTER_LON
)

# ------------------------------------------------------------
# D. ENTFERNEN DER ROHDATEN
# ------------------------------------------------------------
df_model.drop(columns=['latitude', 'longitude'], inplace=True)

print("✅ Feature Engineering 'distance_to_center' abgeschlossen.")
print(f"latitude und longitude wurden gelöscht. Finale Spalten in df_model: {df_model.columns.tolist()}")