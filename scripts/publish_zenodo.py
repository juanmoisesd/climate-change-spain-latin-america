import requests
import json
import os
import glob

ACCESS_TOKEN = os.environ.get('ZENODO_TOKEN')
BASE_URL = 'https://zenodo.org/api/deposit/depositions'

# Metadata mapping for all manuscripts
METADATA_MAP = {
    # Spanish
    "topic_01_arquitectura_miedo.pdf": {
        "title": "La arquitectura del miedo: Anatomía de la amígdala y el sistema de alerta",
        "description": "Manuscrito científico sobre la arquitectura del miedo y la amígdala."
    },
    "topic_02_cerebro_primitivo.pdf": {
        "title": "Cerebro primitivo vs. mente moderna: Por qué respondemos a amenazas que no existen",
        "description": "Manuscrito científico sobre el desajuste evolutivo y la ansiedad."
    },
    "topic_03_guerra_quimica.pdf": {
        "title": "La guerra química interna: El papel del cortisol, la adrenalina y la serotonina",
        "description": "Manuscrito científico sobre la neuroquímica del estrés."
    },
    "topic_04_secuestro_emocional.pdf": {
        "title": "El secuestro emocional: Cuando la corteza prefrontal pierde el control racional",
        "description": "Manuscrito científico sobre el secuestro amigdalino."
    },
    "topic_05_neuroplasticidad_ansiedad.pdf": {
        "title": "Neuroplasticidad y ansiedad: Cómo los pensamientos repetitivos esculpen el cerebro",
        "description": "Manuscrito científico sobre neuroplasticidad y rumiación."
    },
    "topic_06_cuerpo_cuenta.pdf": {
        "title": "El cuerpo lleva la cuenta: La conexión física a través del eje intestino-cerebro",
        "description": "Manuscrito científico sobre el eje microbiota-intestino-cerebro."
    },
    "topic_07_bucle_preocupacion.pdf": {
        "title": "El bucle de la preocupación: Entendiendo el circuito neuronal del pensamiento obsesivo",
        "description": "Manuscrito científico sobre el circuito CSTC y la preocupación."
    },
    "topic_08_memoria_trauma.pdf": {
        "title": "Memoria y trauma: La influencia del hipocampo en las fobias y el pánico",
        "description": "Manuscrito científico sobre el hipocampo y la memoria traumática."
    },
    "topic_09_apagando_alarma.pdf": {
        "title": "Apagando la alarma: La ciencia de la respiración y la regulación del sistema nervioso",
        "description": "Manuscrito científico sobre la respiración y el nervio vago."
    },
    "topic_10_reconstruyendo_calma.pdf": {
        "title": "Reconstruyendo la calma: Estrategias neurocientíficas para reentrenar una mente ansiosa",
        "description": "Manuscrito científico sobre estrategias para la calma."
    },
    # English
    "topic_01_architecture_fear.pdf": {
        "title": "The Architecture of Fear: Functional Anatomy of the Amygdala and the Biological Alert System",
        "description": "Scientific manuscript on the architecture of fear and the amygdala (English version)."
    },
    "topic_02_primitive_vs_modern.pdf": {
        "title": "Primitive Brain vs. Modern Mind: Why We Respond to Non-existent Threats",
        "description": "Scientific manuscript on evolutionary mismatch and anxiety (English version)."
    },
    "topic_03_chemical_warfare.pdf": {
        "title": "Internal Chemical Warfare: The Interplay of Cortisol, Adrenaline, and Serotonin in Chronic Stress",
        "description": "Scientific manuscript on the neurochemistry of stress (English version)."
    },
    "topic_04_emotional_hijacking.pdf": {
        "title": "Emotional Hijacking: When the Prefrontal Cortex Loses Rational Control",
        "description": "Scientific manuscript on emotional hijacking (English version)."
    },
    "topic_05_neuroplasticity_anxiety.pdf": {
        "title": "Neuroplasticity and Anxiety: How Repetitive Thoughts Sculpt the Anxious Brain",
        "description": "Scientific manuscript on neuroplasticity and rumination (English version)."
    },
    "topic_06_body_keeps_score.pdf": {
        "title": "The Body Keeps the Score: Exploring the Microbiota-Gut-Brain Axis in Anxiety",
        "description": "Scientific manuscript on the gut-brain axis (English version)."
    },
    "topic_07_worry_loop.pdf": {
        "title": "The Worry Loop: Understanding the Neural Circuit of Obsessive Thought",
        "description": "Scientific manuscript on the CSTC circuit and worry (English version)."
    },
    "topic_08_memory_and_trauma.pdf": {
        "title": "Memory and Trauma: The Influence of the Hippocampus on Phobias and Panic",
        "description": "Scientific manuscript on the hippocampus and trauma (English version)."
    },
    "topic_09_turning_off_alarm.pdf": {
        "title": "Turning off the Alarm: The Science of Breathing and Nervous System Regulation",
        "description": "Scientific manuscript on breathing and the vagus nerve (English version)."
    },
    "topic_10_reconstructing_calma.pdf": {
        "title": "Reconstructing Calm: Neuroscientific Strategies to Retrain an Anxious Mind",
        "description": "Scientific manuscript on strategies for calm (English version)."
    }
}

def publish_to_zenodo(pdf_path):
    if not ACCESS_TOKEN:
        print("Error: ZENODO_TOKEN environment variable not set.")
        return None

    filename = os.path.basename(pdf_path)
    meta = METADATA_MAP.get(filename, {"title": filename, "description": "Scientific manuscript."})

    print(f"Publishing {filename} - {meta['title']}...")

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
            'title': meta['title'],
            'upload_type': 'publication',
            'publication_type': 'preprint',
            'description': meta['description'],
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
    folders = ["manuscripts", "manuscripts/en"]
    results = {}
    for folder in folders:
        pdf_files = glob.glob(os.path.join(folder, "*.pdf"))
        for pdf_path in sorted(pdf_files):
            url = publish_to_zenodo(pdf_path)
            if url:
                results[pdf_path] = url

    with open("zenodo_publications.json", "w") as f:
        json.dump(results, f, indent=4)
    print("All publications complete. Results saved to zenodo_publications.json")
