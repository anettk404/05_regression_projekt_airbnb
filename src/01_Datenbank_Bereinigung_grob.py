import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# Konfiguration (HIER ANPASSEN)
DB_USER = 'postgres'   
DB_PASSWORD = 'Ihr_Passwort'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'airbnb_regression'
TABELLE_NAME = 'listings_gesamt' 

# Verbindung herstellen (wird außerhalb der Funktion für den gesamten Prozess verwendet)
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')


def bereinige_und_lade_stadt(file_path, city_name, country_name, engine):
    """
    Lädt die detaillierte Listings-Datei (listings.csv.gz), bereinigt den Preis,
    fügt die Stadtinformationen hinzu und konvertiert die Spalten.
    """
    # 1. Nur die wichtigsten Spalten laden (mit Geodaten!)
    SPALTEN_ZUM_LADEN = [
        'id', 'price', 'accommodates', 'bedrooms', 'beds', 
        'room_type', 'neighbourhood_group_cleansed', # Oft präziser als 'neighbourhood_group'
        'review_scores_rating', 'minimum_nights',
        'latitude', 'longitude' # Hinzugefügt für Geodaten-Feature Engineering!
    ]
    
    # Fehlerhafte Zeilen ignorieren
    try:
        # Hier wird angenommen, dass die detaillierte (komprimierte) Datei verwendet wird
        df = pd.read_csv(file_path, usecols=SPALTEN_ZUM_LADEN, on_bad_lines='skip')
    except Exception as e:
        print(f"FEHLER beim Laden von {file_path}: {e}")
        return 0

    initial_count = len(df)
    
    # 2. Preis bereinigen und in Float umwandeln
    df['price'] = (
        df['price'].astype(str)
        .str.replace(r'[$,]', '', regex=True)
        .astype(float, errors='coerce')
    )
    
    # 3. ZWINGEND: Zeilen ohne Preis entfernen
    df.dropna(subset=['price'], inplace=True)
    
    # ACHTUNG: Die Log-Transformation wurde hier entfernt, da sie erst im Notebook erfolgt!
    
    # 4. Generieren der Stadt- und Länder-Spalten
    df['city'] = city_name
    df['country'] = country_name
    
    # 5. Typkonvertierung der Schlüssel-Prädiktoren (falls noch nicht Float)
    for col in ['accommodates', 'bedrooms', 'beds', 'minimum_nights', 
                'review_scores_rating', 'latitude', 'longitude']:
        if col in df.columns:
            # Konvertiert die Spalten, nicht konvertierbare Werte werden zu NaN
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    final_count = len(df)
    print(f"  -> {city_name}: {initial_count} initial, {final_count} nach Preisbereinigung.")
    
    # 6. DATENBANK-IMPORT FÜR DIE EINZELNE STADT
    # Importiert die Daten im 'Append'-Modus in die Zieltabelle
    df.to_sql(TABELLE_NAME, engine, if_exists='append', index=False)
    
    return final_count

# ----------------- Anwendung auf mehrere Städte -----------------

# Simulierte Liste der 10 Städte (HIER PFADE ANPASSEN!)
STADTE_DATEN = [
    {"path": "listings_Berlin.csv", "city": "Berlin", "country": "Germany"}, # Beispiel: Wenn dies die detaillierte Datei ist
    {"path": "listings_paris.csv.gz", "city": "Paris", "country": "France"}, 
    # ... 8 weitere Städte hier einfügen ...
]

gesamtzahl = 0
print(f"Starte Datenbereinigung und Import in {TABELLE_NAME}...")

# Zuerst die Zieltabelle leeren (OPTIONAL, aber empfohlen bei Neustart)
with engine.connect() as connection:
     connection.execute(f"DROP TABLE IF EXISTS {TABELLE_NAME}")
     connection.commit()
print(f"Tabelle {TABELLE_NAME} wurde geleert (oder neu erstellt).")


for data in STADTE_DATEN:
    count = bereinige_und_lade_stadt(data['path'], data['city'], data['country'], engine)
    gesamtzahl += count

print(f"\n✅ Datenimport erfolgreich. Gesamteinträge in DB: {gesamtzahl}")
print(f"Die kategorialen Spalten ('room_type', 'city') sind nun als Text gespeichert.")