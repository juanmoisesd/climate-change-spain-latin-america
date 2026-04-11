CREATE TABLE climate_indicators (
    id SERIAL PRIMARY KEY,
    country VARCHAR(100) NOT NULL,
    year INTEGER NOT NULL,
    co2_per_capita NUMERIC,
    temp_anomaly NUMERIC,
    glacier_area_loss NUMERIC,
    amazon_deforestation NUMERIC,
    sea_level_rise NUMERIC,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_country_year ON climate_indicators (country, year);
