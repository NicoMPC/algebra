#!/usr/bin/env python3
"""
push_new_chapters.py — Matheux : pousse les 4 nouveaux chapitres dans Google Sheets.

Chapitres ajoutés :
  - Probabilites (3EME)         → Curriculum_Officiel + DiagnosticExos
  - Racines_carrees (3EME)      → Curriculum_Officiel + DiagnosticExos
  - Nombres_decimaux (6EME)     → Curriculum_Officiel + DiagnosticExos
  - Fonctions_lineaires (4EME)  → Curriculum_Officiel + DiagnosticExos

Usage :
  python3 push_new_chapters.py [--dry-run]

Prérequis :
  - sheets.py configuré avec PROD_SHEET_ID = 1zLBajKVL8FUzy7aV2Myi9gYFEFJjnALkLAg0hbicuDk
  - Fichier de données : /tmp/exos_data.json (généré par les agents)
  - Compte de service : algebra/algebreboost-sheets-2595a71cadfb.json
"""

import json
import sys
import os

sys.path.insert(0, '/home/nicolas/Bureau/algebra live/algebra')

DRY_RUN = '--dry-run' in sys.argv
DATA_FILE = '/tmp/exos_data.json'

# Métadonnées des nouveaux chapitres pour Curriculum_Officiel
CHAPTER_META = {
    'probabilites_3eme': {
        'Niveau':    '3EME',
        'Categorie': 'Probabilites',
        'Titre':     'Probabilités',
        'Icone':     '🎲',
    },
    'racines_carrees_3eme': {
        'Niveau':    '3EME',
        'Categorie': 'Racines_carrees',
        'Titre':     'Racines carrées',
        'Icone':     '√',
    },
    'nombres_decimaux_6eme': {
        'Niveau':    '6EME',
        'Categorie': 'Nombres_decimaux',
        'Titre':     'Nombres décimaux',
        'Icone':     '🔢',
    },
    'fonctions_lineaires_4eme': {
        'Niveau':    '4EME',
        'Categorie': 'Fonctions_lineaires',
        'Titre':     'Fonctions linéaires',
        'Icone':     '📈',
    },
}

# Mapping clé données → clé diagnostic
DIAG_MAP = {
    'probabilites_3eme':      'Probabilités_3EME',
    'racines_carrees_3eme':   'Racines_carrées_3EME',
    'nombres_decimaux_6eme':  'Nombres_décimaux_6EME',
    'fonctions_lineaires_4eme': 'Fonctions_linéaires_4EME',
}


def load_data():
    if not os.path.exists(DATA_FILE):
        print(f"ERREUR : fichier {DATA_FILE} introuvable.")
        print("Lance d'abord le script de génération des exercices.")
        sys.exit(1)
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def check_existing(sh, tab, niveau, categorie):
    """Retourne True si le chapitre existe déjà dans l'onglet."""
    try:
        rows = sh.read(tab)
        for row in rows:
            if (str(row.get('Niveau', '')).upper() == niveau.upper() and
                    row.get('Categorie', '') == categorie):
                return True
    except Exception:
        pass
    return False


def push_curriculum(sh, data):
    print("\n=== CURRICULUM_OFFICIEL ===")
    for key, meta in CHAPTER_META.items():
        exos = data.get(key, [])
        if not exos:
            print(f"  [SKIP] {key} — pas de données")
            continue

        niveau = meta['Niveau']
        categorie = meta['Categorie']

        if check_existing(sh, 'Curriculum_Officiel', niveau, categorie):
            print(f"  [SKIP] {niveau}/{categorie} déjà présent dans Curriculum_Officiel")
            continue

        row = {
            'Niveau':    niveau,
            'Categorie': categorie,
            'Titre':     meta['Titre'],
            'Icone':     meta['Icone'],
            'ExosJSON':  json.dumps(exos, ensure_ascii=False),
        }

        lvl1 = sum(1 for e in exos if e.get('lvl') == 1)
        lvl2 = sum(1 for e in exos if e.get('lvl') == 2)
        print(f"  {'[DRY] ' if DRY_RUN else ''}Ajout {niveau}/{categorie} : {len(exos)} exos (lvl1={lvl1}, lvl2={lvl2})")

        if not DRY_RUN:
            sh.append_row('Curriculum_Officiel', row)
            print(f"    ✅ Inséré")


def push_diagnostic(sh, data):
    print("\n=== DIAGNOSTIC_EXOS ===")
    diag_data = data.get('diagnostic_exos', {})
    if not diag_data:
        print("  ERREUR : clé 'diagnostic_exos' absente du fichier de données")
        return

    for key, meta in CHAPTER_META.items():
        diag_key = DIAG_MAP[key]
        exos = diag_data.get(diag_key, [])
        if not exos:
            print(f"  [SKIP] {diag_key} — pas de données diagnostic")
            continue

        niveau = meta['Niveau']
        categorie = meta['Categorie']

        if check_existing(sh, 'DiagnosticExos', niveau, categorie):
            print(f"  [SKIP] {niveau}/{categorie} déjà présent dans DiagnosticExos")
            continue

        row = {
            'Niveau':    niveau,
            'Categorie': categorie,
            'ExosJSON':  json.dumps(exos, ensure_ascii=False),
        }

        print(f"  {'[DRY] ' if DRY_RUN else ''}Ajout diag {niveau}/{categorie} : {len(exos)} exos")

        if not DRY_RUN:
            sh.append_row('DiagnosticExos', row)
            print(f"    ✅ Inséré")


def validate_exos(exos, chapter_name):
    """Validation rapide du format des exercices avant push."""
    errors = []
    for i, ex in enumerate(exos):
        for k in ['q', 'a', 'options']:
            if k not in ex or not ex[k]:
                errors.append(f"  exo#{i+1} : clé '{k}' manquante")
        if isinstance(ex.get('options'), list):
            if str(ex.get('a', '')) not in [str(o) for o in ex['options']]:
                errors.append(f"  exo#{i+1} : réponse '{ex.get('a', '')}' absente des options")
        if ex.get('lvl') not in [1, 2]:
            errors.append(f"  exo#{i+1} : lvl invalide ({ex.get('lvl')})")
    if errors:
        print(f"\n  ⚠️  Validation {chapter_name} : {len(errors)} problèmes")
        for e in errors[:5]:
            print(e)
    return len(errors) == 0


def main():
    print("MATHEUX — Push nouveaux chapitres")
    print(f"Mode : {'DRY RUN (aucune écriture)' if DRY_RUN else 'LIVE (écriture réelle)'}")
    print(f"Source : {DATA_FILE}")

    # Charger les données
    data = load_data()
    print(f"\nDonnées chargées :")
    for key in CHAPTER_META:
        exos = data.get(key, [])
        print(f"  {key} : {len(exos)} exos")
    diag = data.get('diagnostic_exos', {})
    print(f"  diagnostic_exos : {len(diag)} chapitres")

    # Validation
    print("\n=== VALIDATION FORMAT ===")
    all_ok = True
    for key in CHAPTER_META:
        exos = data.get(key, [])
        ok = validate_exos(exos, key)
        status = '✅' if ok else '❌'
        print(f"  {status} {key}")
        if not ok:
            all_ok = False

    if not all_ok:
        print("\n⚠️  Des exercices ont des problèmes de format. Continuer quand même ? (y/n) ", end='')
        if input().strip().lower() != 'y':
            sys.exit(1)

    # Import sheets
    try:
        from sheets import sh
        print(f"\nSheet connecté : {sh.SHEET_ID if hasattr(sh, 'SHEET_ID') else 'ID non exposé'}")
    except Exception as e:
        print(f"\nERREUR import sheets: {e}")
        print("Vérifie que sheets.py pointe vers PROD_SHEET_ID = 1zLBajKVL8FUzy7aV2Myi9gYFEFJjnALkLAg0hbicuDk")
        sys.exit(1)

    # Push
    push_curriculum(sh, data)
    push_diagnostic(sh, data)

    if DRY_RUN:
        print("\n[DRY RUN terminé — aucune donnée écrite. Relancer sans --dry-run pour pousser.]")
    else:
        print("\n✅ Push terminé.")
        print("\nProchaines étapes :")
        print("  1. Dans le Sheet, vérifier Curriculum_Officiel et DiagnosticExos")
        print("  2. clasp push --force && clasp deploy --deploymentId AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF --description 'nouveaux chapitres'")
        print("  3. Lancer python3 audit_formats.py pour vérifier la conformité")


if __name__ == '__main__':
    main()
