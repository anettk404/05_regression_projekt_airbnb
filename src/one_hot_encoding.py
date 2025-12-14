import pandas as pd

# Wir verwenden das Dataframe df_model

# ------------------------------------------------------------
# A. OHE FÜR KATEGORIALE SPALTEN DURCHFÜHREN
# ------------------------------------------------------------
df_model_encoded = pd.get_dummies(
    df_model, 
    columns=['room_type', 'neighbourhood_group_cleansed'], 
    prefix=['room', 'borough'], # Präfixe für die neuen Spaltennamen
    drop_first=True # WICHTIG: Vermeidung der Dummy-Variablen-Falle
)

# ------------------------------------------------------------
# B. PRÜFUNG DER ERGEBNISSE
# ------------------------------------------------------------
print("✅ One-Hot-Encoding abgeschlossen.")
print(f"Ursprüngliche Spaltenanzahl: {len(df_model.columns)}")
print(f"Neue Spaltenanzahl nach Encoding: {len(df_model_encoded.columns)}")

print("\nKopfzeile der neuen Dummy-Variablen (Beispiele):")
print(df_model_encoded[['room_Private room', 'room_Shared room', 'borough_Brooklyn', 'borough_Manhattan']].head())

# Bestimmung der Baseline-Kategorien (Die Spalten, die gelöscht wurden)
room_baseline = df_model['room_type'].mode().iloc[0] # Häufigste Kategorie als Standard
borough_baseline = df_model['neighbourhood_group_cleansed'].mode().iloc[0]

print("\nBaseline-Kategorien (Referenz für Koeffizienten):")
print(f"  - room_type Baseline: {room_baseline} (Koeffizienten zeigen Differenz zu dieser Kategorie)")
print(f"  - borough Baseline: {borough_baseline} (Koeffizienten zeigen Differenz zu dieser Kategorie)")

# df_model durch die codierte Version ersetzen, um mit dem gleichen Namen weiterzuarbeiten
df_model = df_model_encoded