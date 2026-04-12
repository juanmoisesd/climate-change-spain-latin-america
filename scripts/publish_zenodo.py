import requests
import json
import os
import glob

# Recommended: Set ZENODO_TOKEN in your environment variables.
ACCESS_TOKEN = os.environ.get('ZENODO_TOKEN')
BASE_URL = 'https://zenodo.org/api/deposit/depositions'

TITLES = {
    "topic_01_arquitectura_miedo.pdf": "La arquitectura del miedo: Anatomía de la amígdala y el sistema de alerta",
    "topic_02_cerebro_primitivo.pdf": "Cerebro primitivo vs. mente moderna: Por qué respondemos a amenazas que no existen",
    "topic_03_guerra_quimica.pdf": "La guerra química interna: El papel del cortisol, la adrenalina y la serotonina",
    "topic_04_secuestro_emocional.pdf": "El secuestro emocional: Cuando la corteza prefrontal pierde el control racional",
    "topic_05_neuroplasticidad_ansiedad.pdf": "Neuroplasticidad y ansiedad: Cómo los pensamientos repetitivos esculpen el cerebro",
    "topic_06_cuerpo_cuenta.pdf": "El cuerpo lleva la cuenta: La conexión física a través del eje intestino-cerebro",
    "topic_07_bucle_preocupacion.pdf": "El bucle de la preocupación: Entendiendo el circuito neuronal del pensamiento obsesivo",
    "topic_08_memoria_trauma.pdf": "Memoria y trauma: La influencia del hipocampo en las fobias y el pánico",
    "topic_09_apagando_alarma.pdf": "Apagando la alarma: La ciencia de la respiración y la regulación del sistema nervioso",
    "topic_10_reconstruyendo_calma.pdf": "Reconstruyendo la calma: Estrategias neurocientíficas para reentrenar una mente ansiosa"
}

def publish_to_zenodo(pdf_path):
    if not ACCESS_TOKEN:
        print("Error: ZENODO_TOKEN environment variable not set.")
        return None

    filename = os.path.basename(pdf_path)
    title = TITLES.get(filename, filename)

    print(f"Publishing {filename} - {title}...")

    # 1. Create deposition
    headers = {"Content-Type": "application/json"}
    params = {'access_token': ACCESS_TOKEN}
    r = requests.post(BASE_URL, params=params, json={}, headers=headers)
    if r.status_code != 201:
        print(f"Error creating deposition: {r.status_code} {r.text}")
        return None

    deposition_id = r.json()['id']
    bucket_url = r.json()['links']['bucket']

    # 2. Upload file
    with open(pdf_path, "rb") as fp:
        r = requests.put(f"{bucket_url}/{filename}", data=fp, params=params)

    if r.status_code not in [200, 201]:
        print(f"Error uploading file: {r.status_code} {r.text}")
        return None

    # 3. Update metadata
    data = {
        'metadata': {
            'title': title,
            'upload_type': 'publication',
            'publication_type': 'preprint',
            'description': f"Manuscrito científico sobre {title.lower()}.",
            'creators': [{'name': 'De la Serna, Juan Moisés', 'affiliation': 'Universidad Internacional de La Rioja (UNIR)'}],
            'access_right': 'open',
            'license': 'cc-by-4.0'
        }
    }
    r = requests.put(f"{BASE_URL}/{deposition_id}", params=params, data=json.dumps(data), headers=headers)

    if r.status_code != 200:
        print(f"Error updating metadata: {r.status_code} {r.text}")
        return None

    # 4. Publish
    r = requests.post(f"{BASE_URL}/{deposition_id}/actions/publish", params=params)

    if r.status_code != 202:
        print(f"Error publishing: {r.status_code} {r.text}")
        return None

    html_url = r.json()['links']['html']
    print(f"Successfully published: {html_url}")
    return html_url

if __name__ == "__main__":
    pdf_files = glob.glob("manuscripts/*.pdf")
    results = {}
    for pdf_path in sorted(pdf_files):
        url = publish_to_zenodo(pdf_path)
        if url:
            results[pdf_path] = url

    with open("zenodo_publications.json", "w") as f:
        json.dump(results, f, indent=4)
    print("All publications complete. Results saved to zenodo_publications.json")
