SELECT country, AVG(temp_anomaly)
FROM climate_indicators
GROUP BY country;
