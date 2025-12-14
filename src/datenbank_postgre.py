pip install psycopg2-binary
import psycopg2


# Verbindung aufbauen
conn = psycopg2.connect(
    host="localhost",        # Lokaler Rechner
    database="berlin_db",    # Deine Datenbank
    user="postgres",         # Dein PostgreSQL-Benutzer
    password="123connection" # Passwort
)

# Cursor erstellen
cur = conn.cursor()


