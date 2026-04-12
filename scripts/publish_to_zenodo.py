import requests
import os
import json

# Fetching the ACCESS_TOKEN from an environment variable for security
ACCESS_TOKEN = os.getenv('ZENODO_ACCESS_TOKEN')
BASE_URL = 'https://zenodo.org/api/deposit/depositions'

def publish_to_zenodo():
    if not ACCESS_TOKEN:
        print("Error: ZENODO_ACCESS_TOKEN environment variable is not set.")
        return

    headers = {"Content-Type": "application/json"}
    params = {'access_token': ACCESS_TOKEN}

    r = requests.post(BASE_URL, params=params, json={}, headers=headers)
    if r.status_code != 201:
        print(f"Error creating deposition: {r.status_code}")
        print(r.json())
        return

    deposition_id = r.json()['id']
    bucket_url = r.json()['links']['bucket']
    print(f"Created deposition {deposition_id}")

    pdf_dir = 'pdfs'
    if not os.path.exists(pdf_dir):
        print(f"Error: {pdf_dir} directory not found. Please run the PDF generation script first.")
        return

    for filename in os.listdir(pdf_dir):
        if filename.endswith('.pdf'):
            filepath = os.path.join(pdf_dir, filename)
            with open(filepath, "rb") as fp:
                r = requests.put(
                    f"{bucket_url}/{filename}",
                    data=fp,
                    params=params,
                )
                if r.status_code != 201 and r.status_code != 200:
                    print(f"Error uploading {filename}: {r.status_code}")
                else:
                    print(f"Uploaded {filename}")

    data = {
        'metadata': {
            'title': 'Metaanálisis de Neurociencia: Del Miedo a la Calma',
            'upload_type': 'publication',
            'publication_type': 'article',
            'description': 'Una colección de 10 metaanálisis científicos que exploran la neurobiología del miedo, la ansiedad, el eje intestino-cerebro y estrategias de regulación emocional.',
            'creators': [{'name': 'De la Serna, Juan Moisés', 'affiliation': 'Universidad Internacional de La Rioja (UNIR)', 'orcid': '0000-0002-8401-8018'}],
            'access_right': 'open',
            'license': 'cc-zero'
        }
    }

    r = requests.put(f"{BASE_URL}/{deposition_id}", params=params, data=json.dumps(data), headers=headers)
    if r.status_code != 200:
        print(f"Error updating metadata: {r.status_code}")
        return
    print("Updated metadata")

    r = requests.post(f"{BASE_URL}/{deposition_id}/actions/publish", params=params)
    if r.status_code != 202:
        print(f"Error publishing: {r.status_code}")
        return

    print("Published successfully!")
    print(f"DOI: {r.json()['doi']}")
    print(f"URL: https://zenodo.org/record/{deposition_id}")

if __name__ == "__main__":
    publish_to_zenodo()
