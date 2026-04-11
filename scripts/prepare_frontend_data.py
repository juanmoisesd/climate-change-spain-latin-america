import pandas as pd
import json
import os

# Ensure directory exists
os.makedirs('docs/data', exist_ok=True)

# Load master dataset
df = pd.read_csv('data/clean/climate_indicators_master.csv')

# Unique indicators
indicators = df['code'].unique()

for code in indicators:
    subset = df[df['code'] == code].sort_values('year')
    data = {
        'labels': subset['year'].tolist(),
        'values': subset['value'].tolist(),
        'indicator': subset['indicator'].iloc[0],
        'unit': subset['unit'].iloc[0]
    }
    with open(f'docs/data/{code}.json', 'w') as f:
        json.dump(data, f)

# Create a master index of all variables for the frontend
variables_list = []
for code in indicators:
    subset = df[df['code'] == code]
    variables_list.append({
        'code': code,
        'name': subset['indicator'].iloc[0],
        'unit': subset['unit'].iloc[0],
        'latest_value': round(subset['value'].iloc[-1], 2)
    })

with open('docs/data/variables_index.json', 'w') as f:
    json.dump(variables_list, f, indent=2)

print(f"Prepared 100 JSON files and variables index for the dashboard.")
