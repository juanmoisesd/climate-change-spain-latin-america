import pandas as pd
import json
import os

def convert_csv_to_json():
    target_dir = os.path.join(os.getcwd(), 'docs/data')
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # CO2 Emissions
    try:
        df_co2 = pd.read_csv('data/clean/co2_emissions_per_capita.csv')
        co2_json = df_co2.to_json(orient='records')
        with open(os.path.join(target_dir, 'co2_emissions.json'), 'w') as f:
            f.write(co2_json)
    except Exception as e:
        pass

    # Renewable Energy
    try:
        df_ren = pd.read_csv('data/clean/renewable_energy_share.csv')
        ren_json = df_ren.to_json(orient='records')
        with open(os.path.join(target_dir, 'renewable_energy.json'), 'w') as f:
            f.write(ren_json)
    except Exception as e:
        pass

    # Summary Statistics for Index
    summary = {
        "total_countries": 7,
        "period": "2000-2024",
        "key_indicators": [
            {"label": "Spain T Anomaly", "value": "+1.97C"},
            {"label": "Izaña CO2 (2024)", "value": "424.0 ppm"},
            {"label": "Max Renewable Share", "value": "83.4% (Brazil)"}
        ]
    }
    with open(os.path.join(target_dir, 'summary.json'), 'w') as f:
        json.dump(summary, f)

if __name__ == "__main__":
    convert_csv_to_json()
