import pandas as pd
import numpy as np

# Wir gehen davon aus, dass df_model nun die Spalte 'distance_to_center' enthält 
# und 'latitude'/'longitude' NICHT mehr enthält (wie im letzten Output)

# ------------------------------------------------------------
# A. NUMERISCHE SPALTEN MIT FEHLENDEN WERTEN IDENTIFIZIEREN
# ------------------------------------------------------------
# Wir nutzen die Liste der numerischen Spalten, die wahrscheinlich NaNs enthalten:
IMPUTATIONS_SPALTEN = [
    'review_scores_rating', 
    'host_total_listings_count',
    # Weitere numerische Spalten, die Sie behalten haben und NaNs enthalten könnten, 
    # wie z.B. estimated_occupancy_l365d, falls Sie diese noch in df_model hätten
]

print("Fehlende Werte (Anzahl) vor der Imputation:")
print(df_model[IMPUTATIONS_SPALTEN].isnull().sum())

# ------------------------------------------------------------
# B. IMPUTATION DURCH DEN MEDIAN DURCHFÜHREN
# ------------------------------------------------------------
for col in IMPUTATIONS_SPALTEN:
    # Berechnung des Medians NUR auf den vorhandenen Werten
    median_wert = df_model[col].median()
    
    # Ersetzen der NaNs durch den Median
    df_model[col].fillna(median_wert, inplace=True)
    
    print(f"  - Spalte '{col}': NaNs durch Median ({median_wert:.2f}) ersetzt.")

# ------------------------------------------------------------
# C. PRÜFUNG NACH DER IMPUTATION
# ------------------------------------------------------------
print("\nFehlende Werte (Anzahl) nach der Imputation:")
print(df_model[IMPUTATIONS_SPALTEN].isnull().sum())

print("\n✅ Imputation abgeschlossen. Der Datensatz ist nun frei von NaN in den gewählten Spalten.")