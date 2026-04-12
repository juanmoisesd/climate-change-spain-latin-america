import requests
import json
import os
import glob

ACCESS_TOKEN = os.environ.get('ZENODO_TOKEN')
BASE_URL = 'https://zenodo.org/api/deposit/depositions'

METADATA_MAP = {
    # Spanish
    "topic_01_arquitectura_miedo.pdf": {"title": "La arquitectura del miedo: Anatomía de la amígdala y el sistema de alerta", "description": "Manuscrito científico sobre la amígdala."},
    "topic_02_cerebro_primitivo.pdf": {"title": "Cerebro primitivo vs. mente moderna: Por qué respondemos a amenazas que no existen", "description": "Manuscrito científico sobre el desajuste evolutivo."},
    "topic_03_guerra_quimica.pdf": {"title": "La guerra química interna: El papel del cortisol, la adrenalina y la serotonina", "description": "Manuscrito científico sobre la neuroquímica del estrés."},
    "topic_04_secuestro_emocional.pdf": {"title": "El secuestro emocional: Cuando la corteza prefrontal pierde el control racional", "description": "Manuscrito científico sobre el secuestro amigdalino."},
    "topic_05_neuroplasticidad_ansiedad.pdf": {"title": "Neuroplasticidad y ansiedad: Cómo los pensamientos repetitivos esculpen el cerebro", "description": "Manuscrito científico sobre neuroplasticidad."},
    "topic_06_cuerpo_cuenta.pdf": {"title": "El cuerpo lleva la cuenta: La conexión física a través del eje intestino-cerebro", "description": "Manuscrito científico sobre el eje microbiota-intestino-cerebro."},
    "topic_07_bucle_preocupacion.pdf": {"title": "El bucle de la preocupación: Entendiendo el circuito neuronal del pensamiento obsesivo", "description": "Manuscrito científico sobre el circuito CSTC."},
    "topic_08_memoria_trauma.pdf": {"title": "Memoria y trauma: La influencia del hipocampo en las fobias y el pánico", "description": "Manuscrito científico sobre el hipocampo y trauma."},
    "topic_09_apagando_alarma.pdf": {"title": "Apagando la alarma: La ciencia de la respiración y la regulación del sistema nervioso", "description": "Manuscrito científico sobre la respiración consciente."},
    "topic_10_reconstruyendo_calma.pdf": {"title": "Reconstruyendo la calma: Estrategias neurocientíficas para reentrenar una mente ansiosa", "description": "Manuscrito científico sobre resiliencia emocional."},
    # English
    "topic_01_architecture_fear.pdf": {"title": "The Architecture of Fear: Functional Anatomy of the Amygdala and the Biological Alert System", "description": "Scientific manuscript on fear processing (English)."},
    "topic_02_primitive_vs_modern.pdf": {"title": "Primitive Brain vs. Modern Mind: Why We Respond to Non-existent Threats", "description": "Scientific manuscript on evolutionary mismatch (English)."},
    "topic_03_chemical_warfare.pdf": {"title": "Internal Chemical Warfare: The Interplay of Cortisol, Adrenaline, and Serotonin in Chronic Stress", "description": "Scientific manuscript on stress neurochemistry (English)."},
    "topic_04_emotional_hijacking.pdf": {"title": "Emotional Hijacking: When the Prefrontal Cortex Loses Rational Control", "description": "Scientific manuscript on emotional hijacking (English)."},
    "topic_05_neuroplasticity_anxiety.pdf": {"title": "Neuroplasticity and Anxiety: How Repetitive Thoughts Sculpt the Anxious Brain", "description": "Scientific manuscript on neuroplasticity (English)."},
    "topic_06_body_keeps_score.pdf": {"title": "The Body Keeps the Score: Exploring the Microbiota-Gut-Brain Axis in Anxiety", "description": "Scientific manuscript on the gut-brain axis (English)."},
    "topic_07_worry_loop.pdf": {"title": "The Worry Loop: Understanding the Neural Circuit of Obsessive Thought", "description": "Scientific manuscript on the CSTC circuit (English)."},
    "topic_08_memory_and_trauma.pdf": {"title": "Memory and Trauma: The Influence of the Hippocampus on Phobias and Panic", "description": "Scientific manuscript on hippocampal trauma (English)."},
    "topic_09_turning_off_alarm.pdf": {"title": "Turning off the Alarm: The Science of Breathing and Nervous System Regulation", "description": "Scientific manuscript on breath regulation (English)."},
    "topic_10_reconstructing_calm.pdf": {"title": "Reconstructing Calm: Neuroscientific Strategies to Retrain an Anxious Mind", "description": "Scientific manuscript on calm strategies (English)."},
    # French
    "topic_01_architecture_peur.pdf": {"title": "L'architecture de la peur : Anatomie fonctionnelle de l'amygdale et le système d'alerte biologique", "description": "Manuscrit scientifique sur l'amygdale (Français)."},
    "topic_02_cerveau_primitif.pdf": {"title": "Cerveau primitif vs esprit moderne : Pourquoi nous répondons à des menaces inexistantes", "description": "Manuscrit scientifique sur le décalage évolutif (Français)."},
    "topic_03_guerre_chimique.pdf": {"title": "La guerre chimique interne : Le rôle du cortisol, de l'adrénaline et de la sérotonine", "description": "Manuscrit scientifique sur la neurochimie du stress (Français)."},
    "topic_04_detournement_emotionnel.pdf": {"title": "Le détournement émotionnel : Quand le cortex préfrontal perd le contrôle rationnel", "description": "Manuscrit scientifique sur le détournement amygdalien (Français)."},
    "topic_05_neuroplasticite_anxiete.pdf": {"title": "Neuroplasticité et anxiété : Comment les pensées répétitives sculptent le cerveau anxieux", "description": "Manuscrit scientifique sur la neuroplasticité (Français)."},
    "topic_06_corps_garde_trace.pdf": {"title": "Le corps garde la trace : Exploration de l'axe microbiote-intestin-cerveau dans l'anxiété", "description": "Manuscrit scientifique sur l'axe intestin-cerveau (Français)."},
    "topic_07_boucle_inquietude.pdf": {"title": "La boucle de l'inquiétude : Comprendre le circuit neuronal de la pensée obsessive", "description": "Manuscrit scientifique sur le circuit CSTC (Français)."},
    "topic_08_memoire_traumatisme.pdf": {"title": "Mémoire et traumatisme : L'influence de l'hippocampe sur les phobies et la panique", "description": "Manuscrit scientifique sur l'hippocampe (Français)."},
    "topic_09_eteindre_alarme.pdf": {"title": "Éteindre l'alarme : La science de la respiration et la régulation du système nerveux", "description": "Manuscrit scientifique sur la respiration (Français)."},
    "topic_10_reconstruire_calme.pdf": {"title": "Reconstruire le calme : Stratégies neuroscientifiques pour réentraîner un esprit anxieux", "description": "Manuscrit scientifique sur les stratégies de calme (Français)."}
}

def publish_to_zenodo(pdf_path):
    if not ACCESS_TOKEN:
        print("Error: ZENODO_TOKEN not set.")
        return None
    filename = os.path.basename(pdf_path)
    meta = METADATA_MAP.get(filename, {"title": filename, "description": "Scientific manuscript."})
    print(f"Publishing {filename}...")
    headers = {"Content-Type": "application/json"}
    params = {'access_token': ACCESS_TOKEN}
    r = requests.post(BASE_URL, params=params, json={}, headers=headers)
    if r.status_code != 201: return None
    dep_id = r.json()['id']
    bucket_url = r.json()['links']['bucket']
    with open(pdf_path, "rb") as fp:
        r = requests.put(f"{bucket_url}/{filename}", data=fp, params=params)
    if r.status_code not in [200, 201]: return None
    data = {'metadata': {
        'title': meta['title'], 'upload_type': 'publication', 'publication_type': 'preprint',
        'description': meta['description'], 'creators': [{'name': 'De la Serna, Juan Moisés', 'affiliation': 'UNIR'}],
        'access_right': 'open', 'license': 'cc-by-4.0'
    }}
    r = requests.put(f"{BASE_URL}/{dep_id}", params=params, data=json.dumps(data), headers=headers)
    if r.status_code != 200: return None
    r = requests.post(f"{BASE_URL}/{dep_id}/actions/publish", params=params)
    if r.status_code != 202: return None
    print(f"Published: {r.json()['links']['html']}")
    return r.json()['links']['html']

if __name__ == "__main__":
    folders = ["manuscripts", "manuscripts/en", "manuscripts/fr"]
    results = {}
    for folder in folders:
        if not os.path.exists(folder): continue
        pdf_files = glob.glob(os.path.join(folder, "*.pdf"))
        for pdf_path in sorted(pdf_files):
            url = publish_to_zenodo(pdf_path)
            if url: results[pdf_path] = url
    with open("zenodo_publications.json", "w") as f:
        json.dump(results, f, indent=4)
    print("Done.")
