import requests
import os
import json

ACCESS_TOKEN = os.getenv('ZENODO_ACCESS_TOKEN')
BASE_URL = 'https://zenodo.org/api/deposit/depositions'

def publish_to_zenodo_fr():
    if not ACCESS_TOKEN:
        print("Error: ZENODO_ACCESS_TOKEN environment variable is not set.")
        return

    headers = {"Content-Type": "application/json"}
    params = {'access_token': ACCESS_TOKEN}

    r = requests.post(BASE_URL, params=params, json={}, headers=headers)
    if r.status_code != 201:
        print(f"Error creating deposition: {r.status_code}")
        return

    deposition_id = r.json()['id']
    bucket_url = r.json()['links']['bucket']
    print(f"Created French deposition {deposition_id}")

    pdf_dir = 'pdfs_fr'
    for filename in sorted(os.listdir(pdf_dir)):
        if filename.endswith('.pdf'):
            filepath = os.path.join(pdf_dir, filename)
            with open(filepath, "rb") as fp:
                r = requests.put(f"{bucket_url}/{filename}", data=fp, params=params)
                if r.status_code in [200, 201]:
                    print(f"Uploaded {filename}")

    data = {
        'metadata': {
            'title': 'Collection de Méta-analyses en Neurosciences : De la Peur au Calme (Édition Française)',
            'upload_type': 'publication',
            'publication_type': 'article',
            'description': 'Une collection professionnelle de 10 méta-analyses scientifiques explorant la neurobiologie de la peur, de l\'anxiété, de l\'axe intestin-cerveau et des stratégies de régulation basées sur la neuroplasticité.',
            'creators': [{'name': 'De la Serna, Juan Moises', 'affiliation': 'Universidad Internacional de La Rioja (UNIR)', 'orcid': '0000-0002-8401-8018'}],
            'access_right': 'open',
            'license': 'cc-zero',
            'language': 'fra'
        }
    }

    r = requests.put(f"{BASE_URL}/{deposition_id}", params=params, data=json.dumps(data), headers=headers)
    if r.status_code == 200:
        print("Updated French metadata")
        r = requests.post(f"{BASE_URL}/{deposition_id}/actions/publish", params=params)
        if r.status_code == 202:
            print("Published French collection successfully!")
            print(f"DOI: {r.json()['doi']}")
            print(f"URL: https://zenodo.org/record/{deposition_id}")

if __name__ == "__main__":
    publish_to_zenodo_fr()
