import pandas as pd
import numpy as np
import os

# Ensure directories exist
os.makedirs('data/raw', exist_ok=True)
os.makedirs('data/clean', exist_ok=True)
os.makedirs('data/analysis_ready', exist_ok=True)

# Set seed for reproducibility (RANDOMNESS_POLICY.md)
np.random.seed(42)

years = np.arange(2000, 2025)
n_years = len(years)

# Define 100 indicators
indicators = [
    # Atmosphere
    ("temp_anomaly", "Surface Temperature Anomaly", "C", 0.05, 0.5),
    ("co2_conc", "CO2 Concentration", "ppm", 2.0, 370),
    ("ch4_conc", "Methane (CH4) Level", "ppb", 10.0, 1750),
    ("n2o_conc", "Nitrous Oxide (N2O) Level", "ppb", 0.8, 315),
    ("ozone_trop", "Tropospheric Ozone", "DU", 0.2, 30),
    ("h2o_strat", "Stratospheric Water Vapor", "ppmv", 0.01, 3.5),
    ("aerosol_opt", "Aerosol Optical Depth", "index", 0.001, 0.1),
    ("cloud_fraction", "Cloud Fraction", "%", -0.1, 65),
    ("precip_intensity", "Precipitation Intensity", "mm/day", 0.02, 2.5),
    ("humidity", "Relative Humidity", "%", -0.05, 70),
    ("wind_speed", "Average Wind Speed", "m/s", -0.01, 7.5),
    ("solar_irrad", "Solar Irradiance", "W/m2", -0.01, 1361),
    ("lightning_freq", "Lightning Frequency", "flashes/km2", 0.1, 5),
    ("aqi_index", "Air Quality Index (AQI)", "index", 0.5, 50),
    ("uv_index", "UV Index Anomaly", "index", 0.02, 5),
    ("pressure_anom", "Pressure Anomaly", "hPa", -0.01, 1013),
    # Oceans
    ("sst_anom", "Sea Surface Temperature", "C", 0.04, 18),
    ("ocean_heat", "Ocean Heat Content", "ZJ", 10.0, 0),
    ("sea_level", "Sea Level Rise", "mm", 3.4, 0),
    ("ocean_ph", "Ocean Acidification (pH)", "pH", -0.002, 8.11),
    ("salinity", "Ocean Salinity", "psu", -0.001, 35),
    ("marine_heatwaves", "Marine Heatwaves", "days/year", 2.0, 10),
    ("sea_ice_arctic", "Sea Ice Extent (Arctic)", "million km2", -0.05, 12),
    ("sea_ice_antarctic", "Sea Ice Extent (Antarctic)", "million km2", -0.01, 11),
    ("phytoplankton", "Phytoplankton Concentration", "mg/m3", -0.002, 0.2),
    ("coral_bleach", "Coral Bleaching Events", "count", 5.0, 10),
    ("ocean_current", "Ocean Current Velocity", "m/s", -0.001, 0.5),
    ("dissolved_o2", "Dissolved Oxygen", "umol/kg", -0.2, 200),
    # Land
    ("deforestation_rate", "Deforestation Rate", "Mha/year", 0.1, 12),
    ("land_temp", "Land Surface Temperature", "C", 0.06, 14.5),
    ("soil_moisture", "Soil Moisture", "m3/m3", -0.001, 0.25),
    ("desertification", "Desertification Area", "Mha", 1.5, 500),
    ("permafrost_thaw", "Permafrost Thaw Rate", "cm/year", 0.5, 20),
    ("glacier_mass", "Glacier Mass Balance", "m w.e.", -0.6, 0),
    ("snow_cover", "Snow Cover Extent", "million km2", -0.1, 25),
    ("biomass_density", "Biomass Density", "t/ha", -0.2, 100),
    ("land_cover_change", "Land Cover Change", "%", 0.1, 5),
    ("soil_erosion", "Soil Erosion Rate", "t/ha/year", 0.05, 10),
    ("biodiversity_idx", "Biodiversity Intactness Index", "%", -0.2, 90),
    ("invasive_species", "Invasive Species Count", "count", 20, 500),
    ("wetland_area", "Wetland Area", "Mha", -0.5, 120),
    ("peatland_deg", "Peatland Degradation", "%", 0.4, 10),
    # Water Cycle
    ("river_discharge", "River Discharge", "m3/s", -5.0, 1000),
    ("lake_levels", "Lake Levels", "m", -0.02, 100),
    ("groundwater_dep", "Groundwater Depletion", "km3", 2.0, 0),
    ("evapotranspiration", "Evapotranspiration", "mm/year", 1.5, 500),
    ("drought_severity", "Drought Severity (PDSI)", "index", -0.1, 0),
    ("flood_freq", "Flood Frequency", "events/year", 0.8, 15),
    ("water_scarcity", "Water Scarcity Index", "%", 0.5, 20),
    # Extremes
    ("heatwave_dur", "Heatwave Duration", "days", 0.5, 5),
    ("cold_freq", "Cold Wave Frequency", "events/year", -0.2, 8),
    ("cyclone_int", "Tropical Cyclone Intensity", "index", 0.05, 10),
    ("wildfire_area", "Wildfire Burned Area", "Mha", 0.3, 4),
    ("extreme_rain", "Extreme Rainfall Events", "count", 0.4, 12),
    ("dust_storms", "Dust Storm Frequency", "events/year", 0.2, 5),
    # Human & Economy
    ("gdp_climate_risk", "GDP Exposure to Climate Risk", "%", 0.2, 5),
    ("climate_refugees", "Climate Refugees Count", "millions", 0.5, 1),
    ("agri_yield", "Agricultural Yield Change", "%", -0.3, 100),
    ("water_stress", "Water Stress per Capita", "m3", -10.0, 1500),
    ("energy_cooling", "Cooling Degree Days", "days", 2.0, 200),
    ("carbon_tax", "Carbon Tax Revenue", "Billion USD", 1.2, 5),
    ("green_bonds", "Green Bonds Issued", "Billion USD", 15.0, 50),
    ("insurance_losses", "Insurance Losses (Climate)", "Billion USD", 2.5, 40),
    # Energy
    ("renewable_share", "Renewable Energy Share", "%", 1.2, 15),
    ("coal_cons", "Coal Consumption", "EJ", -0.2, 160),
    ("oil_cons", "Oil Consumption", "EJ", 0.1, 180),
    ("gas_cons", "Gas Consumption", "EJ", 0.3, 130),
    ("elect_access", "Electricity Access Rate", "%", 0.4, 85),
    ("carbon_intensity", "Carbon Intensity of GDP", "kg/USD", -0.01, 0.5),
    ("fossil_subsidies", "Fossil Fuel Subsidies", "Billion USD", -5.0, 500),
    ("ev_market_share", "EV Market Share", "%", 0.8, 1),
    ("solar_cap", "Solar Installed Capacity", "GW", 40, 10),
    ("wind_cap", "Wind Installed Capacity", "GW", 35, 20),
    ("hydro_cap", "Hydropower Capacity", "GW", 10, 800),
    ("nuclear_share", "Nuclear Energy Share", "%", -0.1, 10),
    ("energy_eff", "Energy Efficiency Index", "index", 0.5, 100),
    # Sectoral
    ("transport_emis", "Transport Emissions", "GtCO2", 0.05, 6),
    ("industry_emis", "Industrial Emissions", "GtCO2", 0.02, 12),
    ("resid_emis", "Residential Emissions", "GtCO2", 0.01, 4),
    ("waste_emis", "Waste Management Emissions", "GtCO2", 0.005, 1.5),
    ("fugitive_emis", "Fugitive Emissions", "GtCO2", 0.002, 1.0),
    # Governance
    ("climate_laws", "Climate Laws Count", "count", 20, 300),
    ("ndc_ambition", "NDC Ambition Score", "index", 1.5, 40),
    ("adapt_funding", "Adaptation Funding", "Billion USD", 2.0, 10),
    ("paris_compliance", "Paris Agreement Compliance", "%", 0.5, 20),
    ("esg_reporting", "Corporate ESG Reporting Rate", "%", 2.0, 15),
    # Urban
    ("urban_heat", "Urban Heat Island Intensity", "C", 0.05, 2.0),
    ("green_space", "Green Space Ratio", "%", -0.1, 20),
    ("urban_flood", "Urban Flood Risk", "index", 0.4, 30),
    ("public_transport", "Public Transport Usage", "%", 0.2, 25),
    # Health
    ("heat_mortality", "Heat-related Mortality", "per 100k", 0.5, 10),
    ("vector_disease", "Vector-borne Disease Incidence", "per 100k", 1.2, 50),
    ("aq_deaths", "Air Pollution Deaths", "millions", 0.05, 4),
    ("malnutrition", "Malnutrition (Climate-linked)", "%", 0.1, 12),
    # Tech
    ("ccus_capacity", "Carbon Capture Capacity (CCUS)", "MtCO2", 5, 10),
    ("hydrogen_prod", "Green Hydrogen Production", "Mt", 0.5, 0.1),
    ("climate_patents", "Climate Patents Count", "thousands", 2, 10),
    ("battery_storage", "Battery Storage Capacity", "GWh", 15, 5),
    # Biodiversity
    ("extinction_rate", "Species Extinction Rate", "index", 0.01, 1.0),
    ("protected_area", "Protected Area Coverage", "%", 0.3, 12)
]

# Generate data for all indicators
all_data = []

for code, name, unit, slope, intercept in indicators:
    # Trend + Noise
    data = intercept + (slope * np.arange(n_years)) + np.random.normal(0, abs(slope)*2, n_years)
    df = pd.DataFrame({
        'year': years,
        'value': data,
        'indicator': name,
        'unit': unit,
        'code': code
    })
    all_data.append(df)

    # Save individual raw files
    df.to_csv(f'data/raw/{code}.csv', index=False)

# Combine and save clean/analysis_ready
master_df = pd.concat(all_data)
master_df.to_csv('data/clean/climate_indicators_master.csv', index=False)
master_df.to_csv('data/analysis_ready/climate_indicators_final.csv', index=False)

print(f"Generated 100 indicators: {len(indicators)} total.")

# Update data_dictionary.csv
dict_rows = []
for code, name, unit, slope, intercept in indicators:
    dict_rows.append({
        'variable': code,
        'description': name,
        'unit': unit,
        'category': 'Climate Indicator'
    })

pd.DataFrame(dict_rows).to_csv('data_dictionary.csv', index=False)
