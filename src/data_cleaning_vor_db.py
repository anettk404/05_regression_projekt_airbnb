# === src/data_cleaning.py ===

import pandas as pd
import numpy as np
import re

# ----------------------------------------------------------------------
# I. GLOBALE KONSTANTEN (Zentral für Feature Engineering)
# ----------------------------------------------------------------------

# Definiert irrelevante Spalten (URLs, Freitext etc.) für die Grob-Reinigung (DB-Phase)
SPALTEN_FUER_GROBE_LOESCHUNG = [
    'listing_url', 'scrape_id', 'last_scraped', 'name', 
    'summary', 'space', 'description', 'experiences_offered', 
    'transit', 'access', 'interaction', 'house_rules', 
    'thumbnail_url', 'medium_url', 'picture_url', 'xl_picture_url',
    'host_url', 'host_about', 'host_thumbnail_url', 'host_picture_url', 
    'calendar_updated', 'has_availability', 'license', 
    'jurisdiction_names'
]

# Konstanten für die Haversine-Berechnung (Times Square)
CENTER_LAT = 40.7580
CENTER_LON = -73.9855
EARTH_RADIUS_KM = 6371

# Numerische Spalten, die in der Regressions-Phase imputiert werden müssen
IMPUTATIONS_SPALTEN = [
    'review_scores_rating', 
    'host_total_listings_count'
    # Fügen Sie hier weitere numerische Spalten hinzu, die im df_model enthalten sind
]

# ----------------------------------------------------------------------
# II. HILFSFUNKTIONEN
# ----------------------------------------------------------------------

def calculate_distance(lat1, lon1, lat2, lon2):
    """Berechnet die Entfernung zwischen zwei Punkten auf der Erde (km) (Haversine)."""
    lat1_rad = np.radians(lat1)
    lon1_rad = np.radians(lon1)
    lat2_rad = np.radians(lat2)
    lon2_rad = np.radians(lon2)
    
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    
    a = np.sin(dlat / 2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    
    return EARTH_RADIUS_KM * c


# ----------------------------------------------------------------------
# III. PIPELINE FUNKTIONEN (Phase 1: ETL/Datenbank)
# ----------------------------------------------------------------------

def prepare_for_database(df, city_name, country_name='USA'):
    """
    Führt die grundlegende ETL-Transformation (Phase 1) durch.
    (Preis-Parsing, Log-Transformation, Orts-Metadaten, Grob-Löschung).
    """
    print(f"--- Vorbereitung für die Datenbank ({city_name}, {country_name}) ---")
    
    # A. PREIS-PARSING UND BEREINIGUNG
    if 'price' in df.columns:
        df['price'] = df['price'].astype(str).str.replace(r'[$,]', '', regex=True)
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df.dropna(subset=['price'], inplace=True)
        
    # B. ERSTELLEN DER ZIELVARIABLEN (price und ln_price)
    if 'price' in df.columns:
        # np.log1p(x) ist gleichbedeutend mit log(1+x), um log(0) zu vermeiden.
        df['ln_price'] = np.log1p(df['price'])
        
    # C. HINZUFÜGEN VON ORTS-METADATEN (city & country)
    df['city'] = city_name
    df['country'] = country_name
    
    # D. LÖSCHEN DER IRRELEVANTEN SPALTEN (Freitext/URLs)
    df.drop(columns=SPALTEN_FUER_GROBE_LOESCHUNG, inplace=True, errors='ignore')

    print("--- Datenbank-Vorbereitung erfolgreich abgeschlossen. ---")
    return df


# ----------------------------------------------------------------------
# IV. PIPELINE FUNKTIONEN (Phase 2: Regressions-Modellierung)
# ----------------------------------------------------------------------

def prepare_for_regression(df_model):
    """
    Führt Feature Engineering, Imputation und OHE durch, um den 
    DataFrame für die Lineare Regression vorzubereiten.
    """
    print("--- Vorbereitung für Lineare Regression (Feature Engineering) ---")
    
    # 1. FEATURE ENGINEERING (Haversine)
    if 'latitude' in df_model.columns and 'longitude' in df_model.columns:
        df_model['distance_to_center'] = calculate_distance(
            df_model['latitude'], 
            df_model['longitude'], 
            CENTER_LAT, 
            CENTER_LON
        )
        # Rohdaten löschen, da Feature erstellt wurde
        df_model.drop(columns=['latitude', 'longitude'], inplace=True)
        print("1. Feature 'distance_to_center' erstellt und Rohkoordinaten gelöscht.")

    # 2. IMPUTATION (Median)
    print("2. Imputation fehlender Werte (Median)...")
    for col in IMPUTATIONS_SPALTEN:
        if col in df_model.columns and df_model[col].isnull().sum() > 0:
            median_wert = df_model[col].median()
            df_model[col].fillna(median_wert, inplace=True)
            print(f"   -> {col}: {df_model[col].isnull().sum()} NaNs durch Median ({median_wert:.2f}) ersetzt.")

    # 3. ONE-HOT-ENCODING (OHE)
    print("3. One-Hot-Encoding (OHE) der kategorialen Variablen...")
    kategoriale_spalten = [
        col for col in ['room_type', 'neighbourhood_group_cleansed'] 
        if col in df_model.columns
    ]
    
    df_model_encoded = pd.get_dummies(
        df_model, 
        columns=kategoriale_spalten, 
        prefix=['room', 'borough'], 
        drop_first=True # Vermeidet die Dummy-Variablen-Falle
    )
    
    # df_model durch die codierte Version ersetzen
    df_model = df_model_encoded
    
    print(f"--- Vorbereitung abgeschlossen. Finale Spaltenanzahl: {len(df_model.columns)} ---")
    return df_model