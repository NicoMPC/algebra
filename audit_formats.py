#!/usr/bin/env python3
"""
audit_formats.py — Matheux : audit format des exercices du Curriculum_Officiel
Vérifie la conformité de chaque exercice dans les onglets Curriculum_Officiel et DiagnosticExos.

Usage : python3 audit_formats.py
Prérequis : sheets.py configuré avec le bon SHEET_ID (voir CLAUDE.md MAJEUR bug #3)
"""

import json
import sys
from collections import defaultdict

sys.path.insert(0, '/home/nicolas/Bureau/algebra live/algebra')

# ── Critères de conformité ──────────────────────────────────────────────────
#
# Chaque exercice dans ExosJSON DOIT avoir :
#   - "q"       : string non-vide (énoncé)
#   - "a"       : string non-vide (réponse correcte)
#   - "options" : liste d'au moins 3 éléments (MCQ)
#   - "a" dans "options" (la bonne réponse doit être dans les options)
#   - "lvl"     : 1 ou 2 (difficulté)
#
# Recommandé :
#   - "steps"   : liste (explication pas à pas)
#   - "f"       : string (formule LaTeX optionnelle)
#
# Brevet-ready (lvl2 uniquement) :
#   - Contient au moins 1 chiffre ou formule dans l'énoncé
#   - Énoncé > 20 caractères (pas trop court/trivial)

REQUIRED_KEYS = ['q', 'a', 'options']
MIN_OPTIONS   = 3
MIN_ENONCE_LEN = 15

LEVELS = ['6EME', '5EME', '4EME', '3EME']
CHAPS_BY_LEVEL = {
    '6EME': ['Nombres_entiers', 'Fractions', 'Proportionnalité', 'Géométrie', 'PérimètresAires', 'Angles'],
    '5EME': ['Fractions', 'Nombres_relatifs', 'Proportionnalité', 'Puissances', 'Pythagore', 'Calcul_Littéral'],
    '4EME': ['Fractions', 'Puissances', 'Calcul_Littéral', 'Équations', 'Pythagore', 'Proportionnalité'],
    '3EME': ['Calcul_Littéral', 'Équations', 'Fonctions', 'Théorème_de_Thalès', 'Trigonométrie', 'Statistiques'],
}


def audit_exo(exo: dict, idx: int, chap: str, niveau: str) -> list[str]:
    """Retourne une liste d'erreurs pour un exercice. [] = OK."""
    errors = []

    # Clés obligatoires
    for k in REQUIRED_KEYS:
        if k not in exo or not exo[k]:
            errors.append(f"Clé '{k}' manquante ou vide")

    q = str(exo.get('q', ''))
    a = str(exo.get('a', ''))
    opts = exo.get('options', [])

    # Options : liste + taille minimum
    if not isinstance(opts, list):
        errors.append(f"'options' n'est pas une liste")
    elif len(opts) < MIN_OPTIONS:
        errors.append(f"Seulement {len(opts)} options (minimum {MIN_OPTIONS})")

    # La bonne réponse doit être dans les options
    if a and isinstance(opts, list) and opts:
        if a not in [str(o) for o in opts]:
            errors.append(f"Réponse '{a[:30]}' absente des options {[str(o)[:20] for o in opts]}")

    # Énoncé trop court
    if len(q) < MIN_ENONCE_LEN:
        errors.append(f"Énoncé trop court ({len(q)} chars) : '{q}'")

    # Niveau de difficulté
    lvl = exo.get('lvl', None)
    if lvl not in [1, 2]:
        errors.append(f"'lvl' absent ou invalide (valeur: {lvl!r}) — attendu 1 ou 2")

    # Steps recommandé
    if 'steps' not in exo:
        errors.append(f"[WARN] 'steps' absent (explication pas à pas recommandée)")

    return errors


def audit_tab(sh, tab_name: str, mode: str = 'curriculum') -> dict:
    """
    Audite un onglet complet.
    mode='curriculum' : onglet Curriculum_Officiel (20 exos/chap)
    mode='diagnostic' : onglet DiagnosticExos (2 exos/chap, lvl 1 + lvl 2)
    """
    print(f"\n{'='*60}")
    print(f"Audit {tab_name} ({mode})")
    print('='*60)

    try:
        rows = sh.read(tab_name)
    except Exception as e:
        print(f"ERREUR lecture {tab_name}: {e}")
        return {}

    results = {}
    total_exos = 0
    total_errors = 0
    total_warnings = 0

    for row in rows:
        niveau   = str(row.get('Niveau', '')).strip().upper()
        categorie = str(row.get('Categorie', '') or row.get('Titre', '')).strip()
        exos_json = row.get('ExosJSON', '')

        try:
            exos = json.loads(exos_json) if isinstance(exos_json, str) else exos_json
        except Exception:
            print(f"  [{niveau}][{categorie}] ExosJSON invalide (JSON parse error)")
            continue

        if not isinstance(exos, list):
            print(f"  [{niveau}][{categorie}] ExosJSON n'est pas une liste")
            continue

        key = f"{niveau}::{categorie}"
        results[key] = {'niveau': niveau, 'categorie': categorie, 'exos': len(exos), 'errors': [], 'warnings': []}

        # Nombre d'exos attendu
        if mode == 'curriculum' and len(exos) < 15:
            results[key]['warnings'].append(f"Seulement {len(exos)} exos (attendu 20)")
        elif mode == 'diagnostic' and len(exos) < 2:
            results[key]['errors'].append(f"Seulement {len(exos)} exos (attendu 2 minimum : lvl1+lvl2)")

        # Audit exo par exo
        for i, exo in enumerate(exos):
            errs = audit_exo(exo, i, categorie, niveau)
            for e in errs:
                if '[WARN]' in e:
                    results[key]['warnings'].append(f"  exo#{i+1}: {e}")
                    total_warnings += 1
                else:
                    results[key]['errors'].append(f"  exo#{i+1}: {e}")
                    total_errors += 1
            total_exos += 1

        # Distribution lvl1/lvl2
        if mode == 'curriculum':
            lvl1 = sum(1 for e in exos if e.get('lvl') == 1)
            lvl2 = sum(1 for e in exos if e.get('lvl') == 2)
            if lvl1 == 0:
                results[key]['warnings'].append("Aucun exo lvl1 (exercices de base)")
            if lvl2 == 0:
                results[key]['warnings'].append("Aucun exo lvl2 (exercices avancés)")
            if abs(lvl1 - lvl2) > 10:
                results[key]['warnings'].append(f"Déséquilibre lvl: lvl1={lvl1}, lvl2={lvl2} (idéal: 10+10)")

    # Affichage résultats
    errors_by_chapter = defaultdict(int)
    for key, res in results.items():
        nb_err = len(res['errors'])
        nb_warn = len(res['warnings'])
        status = '✅' if nb_err == 0 else '❌'
        warn_str = f" ({nb_warn} warnings)" if nb_warn > 0 else ""
        print(f"  {status} [{res['niveau']}] {res['categorie']} — {res['exos']} exos, {nb_err} erreurs{warn_str}")
        for e in res['errors']:
            print(f"       {e}")
        for w in res['warnings'][:3]:  # limite à 3 warnings par chap
            print(f"       {w}")
        errors_by_chapter[f"{res['niveau']}::{res['categorie']}"] = nb_err

    print(f"\n  TOTAL : {total_exos} exos audités, {total_errors} erreurs, {total_warnings} warnings")

    # Chapitres manquants
    if mode == 'curriculum':
        found_chaps = {key.split('::') for key in results.keys()}
        for niveau, chaps in CHAPS_BY_LEVEL.items():
            for chap in chaps:
                found = any(
                    r['niveau'] == niveau and r['categorie'] == chap
                    for r in results.values()
                )
                if not found:
                    print(f"  ⚠️  [{niveau}] Chapitre '{chap}' absent du {tab_name}")

    return results


def main():
    try:
        from sheets import sh
    except Exception as e:
        print(f"ERREUR import sheets: {e}")
        print("Vérifie que sheets.py pointe vers le bon SHEET_ID (PROD)")
        print("SHEET_ID prod = 1zLBajKVL8FUzy7aV2Myi9gYFEFJjnALkLAg0hbicuDk")
        sys.exit(1)

    print("MATHEUX — Audit Formats Exercices")
    print(f"Sheet actif: {sh._api.spreadsheets().get(spreadsheetId=sh.SHEET_ID if hasattr(sh, 'SHEET_ID') else 'inconnu').execute().get('properties', {}).get('title', '?')}")

    res1 = audit_tab(sh, 'Curriculum_Officiel', mode='curriculum')
    res2 = audit_tab(sh, 'DiagnosticExos', mode='diagnostic')

    # Score global
    total_errors_curr = sum(len(r['errors']) for r in res1.values())
    total_errors_diag = sum(len(r['errors']) for r in res2.values())

    print(f"\n{'='*60}")
    print(f"RAPPORT FINAL")
    print(f"{'='*60}")
    print(f"  Curriculum_Officiel : {total_errors_curr} erreurs bloquantes")
    print(f"  DiagnosticExos      : {total_errors_diag} erreurs bloquantes")

    if total_errors_curr + total_errors_diag == 0:
        print(f"\n✅ Tous les exercices sont conformes au format attendu.")
    else:
        print(f"\n❌ {total_errors_curr + total_errors_diag} erreurs à corriger dans le Sheet.")
        print(f"   Lance la correction manuelle ou DeepSeek pour regénérer les chapitres en erreur.")


if __name__ == '__main__':
    main()
