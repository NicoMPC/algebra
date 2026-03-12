#!/usr/bin/env python3
"""
push_via_gas.py — Pousse les 5 chapitres via l'endpoint GAS (contourne la permission Sheets).
Usage : python3 push_via_gas.py <admin_code>
"""

import json
import sys
import urllib.request
import urllib.parse
import os

GAS_URL = "https://script.google.com/macros/s/AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF/exec"
DATA_FILE = os.path.join(os.path.dirname(__file__), 'new_chapters_2026-03-12.json')

CHAPTER_META = {
    'probabilites_3eme':      ('3EME', 'Probabilites',       'Probabilités',      '🎲'),
    'racines_carrees_3eme':   ('3EME', 'Racines_carrees',    'Racines carrées',   '√'),
    'nombres_decimaux_6eme':  ('6EME', 'Nombres_decimaux',   'Nombres décimaux',  '🔢'),
    'fonctions_lineaires_4eme':('4EME','Fonctions_lineaires','Fonctions linéaires','📈'),
    'statistiques_6eme':      ('6EME', 'Statistiques_6eme',  'Statistiques',      '📊'),
}
DIAG_MAP = {
    'probabilites_3eme':       'Probabilités_3EME',
    'racines_carrees_3eme':    'Racines_carrées_3EME',
    'nombres_decimaux_6eme':   'Nombres_décimaux_6EME',
    'fonctions_lineaires_4eme':'Fonctions_linéaires_4EME',
    'statistiques_6eme':       'Statistiques_6EME',
}

if len(sys.argv) < 2:
    print("Usage : python3 push_via_gas.py <admin_code>")
    print("Exemple : python3 push_via_gas.py HMD493")
    sys.exit(1)

admin_code = sys.argv[1]

with open(DATA_FILE, encoding='utf-8') as f:
    data = json.load(f)

# Construire la liste chapters
chapters = []
for key, (niveau, categorie, titre, icone) in CHAPTER_META.items():
    exos = data.get(key, [])
    if exos:
        chapters.append({
            'niveau': niveau, 'categorie': categorie,
            'titre': titre, 'icone': icone, 'exos': exos
        })

# Construire la liste diagExos
diag_raw = data.get('diagnostic_exos', {})
diag_exos = []
for key, (niveau, categorie, _, _) in CHAPTER_META.items():
    diag_key = DIAG_MAP[key]
    exos = diag_raw.get(diag_key, [])
    if exos:
        diag_exos.append({'niveau': niveau, 'categorie': categorie, 'exos': exos})

payload = {
    'action': 'import_chapters',
    'adminCode': admin_code,
    'chapters': chapters,
    'diagExos': diag_exos,
}

print(f"Envoi vers GAS : {len(chapters)} chapitres, {len(diag_exos)} diags...")
body = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(GAS_URL, data=body, method='POST')
req.add_header('Content-Type', 'application/json')

try:
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read().decode('utf-8'))
    if result.get('status') == 'success':
        print("✅ Import réussi !")
        for r in result.get('results', []):
            print(" ", r)
    else:
        print("❌ Erreur GAS :", result.get('message'))
except Exception as e:
    print("❌ Erreur réseau :", e)
