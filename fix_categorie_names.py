#!/usr/bin/env python3
"""
fix_categorie_names.py — Matheux : renomme les 5 catégories sans accents → accents corrects.

Les 5 chapitres poussés le 12 mars utilisaient des clés sans accents.
Le frontend CHAPS_BY_LEVEL génère des clés avec accents (regex À-ÿ conserve les accents).
Ce script aligne les Categorie dans les 3 onglets concernés.

Renames :
  Probabilites       → Probabilités
  Racines_carrees    → Racines_Carrées
  Fonctions_lineaires→ Fonctions_Linéaires
  Nombres_decimaux   → Nombres_Décimaux
  Statistiques_6eme  → Statistiques_6ème

Onglets mis à jour : Curriculum_Officiel, DiagnosticExos, BoostExos

Usage :
  python3 fix_categorie_names.py [--dry-run]
"""
import sys
sys.path.insert(0, '/home/nicolas/Bureau/algebra live/algebra')

DRY_RUN = '--dry-run' in sys.argv

SHEET_ID = "1SiE3lHf9dAKbExWPGNrk5cbLhDbKUKM4xvd1Th1frY4"

RENAMES = {
    'Probabilites':        'Probabilités',
    'Racines_carrees':     'Racines_Carrées',
    'Fonctions_lineaires': 'Fonctions_Linéaires',
    'Nombres_decimaux':    'Nombres_Décimaux',
    'Statistiques_6eme':   'Statistiques_6ème',
}

TABS = ['Curriculum_Officiel', 'DiagnosticExos', 'BoostExos']
# Colonne B = Categorie (index 1, 0-based)
CATEGORIE_COL = 'B'

from google.oauth2 import service_account
from googleapiclient.discovery import build

creds = service_account.Credentials.from_service_account_file(
    '/home/nicolas/Bureau/algebra live/algebra/algebreboost-sheets-2595a71cadfb.json',
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)
svc = build('sheets', 'v4', credentials=creds, cache_discovery=False)
api = svc.spreadsheets()

total_fixed = 0

for tab in TABS:
    # Lire toute la colonne B
    range_name = f"{tab}!B:B"
    result = api.values().get(spreadsheetId=SHEET_ID, range=range_name).execute()
    values = result.get('values', [])

    updates = []
    for row_idx, row in enumerate(values):
        if not row:
            continue
        cell_val = row[0]
        if cell_val in RENAMES:
            new_val = RENAMES[cell_val]
            row_num = row_idx + 1  # 1-based
            cell_ref = f"{tab}!B{row_num}"
            updates.append({'range': cell_ref, 'values': [[new_val]]})
            print(f"  {'[DRY-RUN] ' if DRY_RUN else ''}{'✅' if not DRY_RUN else '🔍'} {tab}!B{row_num} : {cell_val} → {new_val}")
            total_fixed += 1

    if updates and not DRY_RUN:
        api.values().batchUpdate(
            spreadsheetId=SHEET_ID,
            body={'valueInputOption': 'RAW', 'data': updates}
        ).execute()

    if not updates:
        print(f"  ℹ️  {tab} : aucune valeur à renommer")

print(f"\n{'[DRY-RUN] ' if DRY_RUN else ''}Total cellules {'à renommer' if DRY_RUN else 'renommées'} : {total_fixed}")
if DRY_RUN:
    print("  → Relance sans --dry-run pour appliquer.")
