#!/usr/bin/env python3
"""
push_sprint4.py — Matheux : pousse les 3 derniers chapitres (Sprint 4 — 100% programme).

Chapitres :
  - Notation_Scientifique (3EME) — + brevet
  - Sections_Solides      (4EME)
  - Puissances_10         (6EME)

Usage : python3 push_sprint4.py [--dry-run]
"""
import json, sys
sys.path.insert(0, '/home/nicolas/Bureau/algebra live/algebra')

DRY_RUN = '--dry-run' in sys.argv
SHEET_ID = "1SiE3lHf9dAKbExWPGNrk5cbLhDbKUKM4xvd1Th1frY4"
DATA_FILE = '/home/nicolas/Bureau/algebra live/algebra/docs/archive/chapitres_sprint4_2026.json'

from google.oauth2 import service_account
from googleapiclient.discovery import build

creds = service_account.Credentials.from_service_account_file(
    '/home/nicolas/Bureau/algebra live/algebra/algebreboost-sheets-2595a71cadfb.json',
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)
svc = build('sheets', 'v4', credentials=creds, cache_discovery=False)
api = svc.spreadsheets()

with open(DATA_FILE, encoding='utf-8') as f:
    data = json.load(f)

curr_rows, diag_rows, boost_rows, brev_rows = [], [], [], []

for key, chap in data.items():
    meta   = chap['meta']
    niveau = meta['Niveau']
    cat    = meta['Categorie']
    curr_rows.append([niveau, cat, meta['Titre'], meta['Icone'], json.dumps(chap['curriculum'], ensure_ascii=False)])
    diag_rows.append([niveau, cat, json.dumps(chap['diagnostic'], ensure_ascii=False)])
    boost_rows.append([niveau, cat, json.dumps(chap['boost'], ensure_ascii=False)])
    if chap.get('brevet'):
        brev_rows.append([niveau, cat, json.dumps(chap['brevet'], ensure_ascii=False)])

def append_rows(tab, rows, label):
    if DRY_RUN:
        print(f'  [DRY-RUN] {tab} ← {len(rows)} lignes ({label})')
        return
    api.values().append(spreadsheetId=SHEET_ID, range=f'{tab}!A1',
        valueInputOption='RAW', insertDataOption='INSERT_ROWS',
        body={'values': rows}).execute()
    print(f'  ✅ {tab} ← {len(rows)} lignes ({label})')

print('=== Push Sprint 4 — 3 chapitres ===\n')
append_rows('Curriculum_Officiel', curr_rows,  '3 chapitres')
append_rows('DiagnosticExos',      diag_rows,  '3 chapitres')
append_rows('BoostExos',           boost_rows, '3 chapitres')
append_rows('BrevetExos',          brev_rows,  f'{len(brev_rows)} chapitre 3EME')

total = sum(len(c['curriculum'])+len(c['diagnostic'])+len(c['boost'])+len(c.get('brevet',[])) for c in data.values())
print(f'\n{"[DRY-RUN] " if DRY_RUN else ""}Total exercices : {total}')
if DRY_RUN:
    print('→ Relance sans --dry-run pour appliquer.')
