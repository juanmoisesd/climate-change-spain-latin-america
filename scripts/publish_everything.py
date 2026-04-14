import requests, os, json, time

TOKEN = os.getenv('ZENODO_ACCESS_TOKEN')
BASE = 'https://zenodo.org/api/deposit/depositions'
PARAMS = {'access_token': TOKEN}
HEADERS = {"Content-Type": "application/json"}

langs = [
    "es", "en", "fr", "de", "it", "pt", "nl", "pl", "sv", "cs", "hu", "ro", "da", "fi", "sk", "bg", "hr", "lt", "sl", "lv", "et", "ga", "mt", "el",
    "hi", "zh", "ms", "id", "ko", "ja", "ar", "he"
]

iso_map = {
    "es": "spa", "en": "eng", "fr": "fra", "de": "deu", "it": "ita", "pt": "por", "nl": "nld", "pl": "pol", "sv": "swe", "cs": "ces", "hu": "hun", "ro": "ron", "da": "dan", "fi": "fin", "sk": "slk", "bg": "bul", "hr": "hrv", "lt": "lit", "sl": "slv", "lv": "lav", "et": "est", "ga": "gle", "mt": "mlt", "el": "ell", "hi": "hin", "zh": "zho", "ms": "msa", "id": "ind", "ko": "kor", "ja": "jpn", "ar": "ara", "he": "heb"
}

def pub(l):
    print(f"Publishing {l}...")
    # 1. Create
    r = requests.post(BASE, params=PARAMS, json={}, headers=HEADERS)
    if r.status_code != 201:
        print(f"Error {l} create: {r.text}")
        return
    dep = r.json(); d_id = dep['id']; bucket = dep['links']['bucket']

    # 2. Upload PDFs
    pdf_dir = f'pdfs_{l}'
    if not os.path.exists(pdf_dir):
        # Fallback to generating them on the fly if needed
        pass

    for f_name in sorted(os.listdir(pdf_dir)):
        if f_name.endswith('.pdf'):
            with open(os.path.join(pdf_dir, f_name), "rb") as fp:
                requests.put(f"{bucket}/{f_name}", data=fp, params=PARAMS)

    # 3. Metadata
    meta = {
        'metadata': {
            'title': f'Neuroscience Meta-Analysis Collection ({l.upper()} Professional Edition)',
            'upload_type': 'publication', 'publication_type': 'article',
            'description': f'A professional collection of 10 scientific meta-analyses on neuroscience topics in {l}. Authorship: Juan Moises de la Serna.',
            'creators': [{'name': 'De la Serna, Juan Moises', 'affiliation': 'UNIR', 'orcid': '0000-0002-8401-8018'}],
            'access_right': 'open', 'license': 'cc-zero', 'language': iso_map.get(l)
        }
    }
    requests.put(f"{BASE}/{d_id}", params=PARAMS, data=json.dumps(meta), headers=HEADERS)

    # 4. Publish
    r_pub = requests.post(f"{BASE}/{d_id}/actions/publish", params=PARAMS)
    if r_pub.status_code == 202:
        print(f"Published {l} successfully: {r_pub.json().get('doi')}")
    else:
        print(f"Failed {l} publish: {r_pub.text}")

if __name__ == "__main__":
    if not TOKEN:
        print("Token missing")
    else:
        for l in langs:
            try: pub(l); time.sleep(1)
            except Exception as e: print(f"Exc {l}: {e}")
