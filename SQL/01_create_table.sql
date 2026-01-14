-- Tabelle Erstellen für NYC in PGAdmin

DROP TABLE IF EXISTS chicago_airbnb_listings_raw CASCADE;

CREATE TABLE chicago_airbnb_listings_raw (
    -- 1. IDENTIFIKATION UND LAGE
    id BIGINT PRIMARY KEY,
    city VARCHAR(50) NOT NULL, -- Flexibilität für weitere Städte
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,

    -- 2. ZIELVARIABLE UND KATEGORIEN
    price NUMERIC(10, 2) NOT NULL,
    room_type VARCHAR(50) NOT NULL, 
    neighbourhood_group_cleansed VARCHAR(50), 
    
    -- 3. UNTERKUNFT-SPEZIFISCHE FEATURES
    accommodates INTEGER NOT NULL,
    bedrooms INTEGER,
    beds INTEGER,
    bathrooms NUMERIC(3, 1), -- Erlaubt halbe Badezimmer (z.B. 1.5)
    minimum_nights INTEGER NOT NULL,
    availability_365 INTEGER NOT NULL,

    -- 4. BINÄRE UND HOST-INFOS
    instant_bookable BOOLEAN NOT NULL,
    host_is_superhost BOOLEAN, 
    host_total_listings_count INTEGER,

    -- 5. BEWERTUNGEN
    review_scores_rating NUMERIC(4, 2) 
);