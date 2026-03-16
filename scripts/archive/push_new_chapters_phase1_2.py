#!/usr/bin/env python3
"""
push_new_chapters_phase1_2.py — Matheux : pousse les 12 nouveaux chapitres (Phase 1 + Phase 2).

Phase 1 (5 chapitres) :
  - Systèmes_Équations (3EME) — + brevet
  - Inéquations       (3EME) — + brevet
  - Symétrie_Axiale   (6EME)
  - Symétrie_Centrale (5EME)
  - Volumes           (6EME)

Phase 2 (7 chapitres) :
  - Transformations         (5EME)
  - Racines_Carrées         (5EME)
  - Triangles_Semblables    (5EME)
  - Inéquations             (4EME)
  - Homothétie              (4EME)
  - Agrandissement_Réduction(6EME)
  - Conversions_Unités      (6EME)

Onglets mis à jour :
  Curriculum_Officiel, DiagnosticExos, BoostExos, BrevetExos (3EME uniquement)

Usage :
  python3 push_new_chapters_phase1_2.py [--dry-run]
"""
import json, sys, os
sys.path.insert(0, '/home/nicolas/Bureau/algebra live/algebra')

DRY_RUN = '--dry-run' in sys.argv

SHEET_ID = "1SiE3lHf9dAKbExWPGNrk5cbLhDbKUKM4xvd1Th1frY4"
BASE = '/home/nicolas/Bureau/algebra live/algebra/docs/archive'

from google.oauth2 import service_account
from googleapiclient.discovery import build

creds = service_account.Credentials.from_service_account_file(
    '/home/nicolas/Bureau/algebra live/algebra/algebreboost-sheets-2595a71cadfb.json',
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)
svc = build('sheets', 'v4', credentials=creds, cache_discovery=False)
api = svc.spreadsheets()

# ── Charger les données ────────────────────────────────────────────
with open(f'{BASE}/chapitres_phase1_2026.json', encoding='utf-8') as f:
    p1 = json.load(f)

with open(f'{BASE}/chapitres_phase2_2026.json', encoding='utf-8') as f:
    p2 = json.load(f)

all_chapters = {**p1, **p2}

# ── Préparer les lignes par onglet ─────────────────────────────────
curr_rows  = []   # Curriculum_Officiel : Niveau, Categorie, Titre, Icone, ExosJSON
diag_rows  = []   # DiagnosticExos     : Niveau, Categorie, ExosJSON
boost_rows = []   # BoostExos          : Niveau, Categorie, ExosJSON
brev_rows  = []   # BrevetExos         : Niveau, Categorie, ExosJSON

for key, chap in all_chapters.items():
    meta   = chap['meta']
    niveau = meta['Niveau']
    cat    = meta['Categorie']
    titre  = meta['Titre']
    icone  = meta['Icone']

    curr_rows.append([
        niveau, cat, titre, icone,
        json.dumps(chap['curriculum'], ensure_ascii=False)
    ])
    diag_rows.append([
        niveau, cat,
        json.dumps(chap['diagnostic'], ensure_ascii=False)
    ])
    boost_rows.append([
        niveau, cat,
        json.dumps(chap['boost'], ensure_ascii=False)
    ])
    if chap.get('brevet'):
        brev_rows.append([
            niveau, cat,
            json.dumps(chap['brevet'], ensure_ascii=False)
        ])

# ── Fonction d'append ──────────────────────────────────────────────
def append_rows(tab, rows, label):
    if DRY_RUN:
        print(f'  [DRY-RUN] {tab} ← {len(rows)} lignes ({label})')
        return
    api.values().append(
        spreadsheetId=SHEET_ID,
        range=f'{tab}!A1',
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body={'values': rows}
    ).execute()
    print(f'  ✅ {tab} ← {len(rows)} lignes ({label})')

# ── Push ───────────────────────────────────────────────────────────
print('=== Push Phase 1+2 — 12 chapitres ===\n')

append_rows('Curriculum_Officiel', curr_rows,  '12 chapitres × (Niveau,Categorie,Titre,Icone,ExosJSON)')
append_rows('DiagnosticExos',      diag_rows,  '12 chapitres × (Niveau,Categorie,ExosJSON)')
append_rows('BoostExos',           boost_rows, '12 chapitres × (Niveau,Categorie,ExosJSON)')
append_rows('BrevetExos',          brev_rows,  f'{len(brev_rows)} chapitres 3EME × (Niveau,Categorie,ExosJSON)')

# ── Bilan ──────────────────────────────────────────────────────────
total_exos = (
    sum(len(c['curriculum']) for c in all_chapters.values()) +
    sum(len(c['diagnostic']) for c in all_chapters.values()) +
    sum(len(c['boost'])      for c in all_chapters.values()) +
    sum(len(c.get('brevet', [])) for c in all_chapters.values())
)
print(f'\n{"[DRY-RUN] " if DRY_RUN else ""}Bilan :')
print(f'  Chapitres ajoutés : {len(all_chapters)}')
print(f'  Exercices totaux  : {total_exos}')
print(f'  Curriculum total  : {len(all_chapters)} × 20 = {len(all_chapters)*20}')
print(f'  Diagnostic total  : {len(all_chapters)} × 2  = {len(all_chapters)*2}')
print(f'  Boost total       : {len(all_chapters)} × 10 = {len(all_chapters)*10}')
print(f'  Brevet (3EME)     : {len(brev_rows)} × 8  = {len(brev_rows)*8}')
if DRY_RUN:
    print('\n→ Relance sans --dry-run pour appliquer.')
