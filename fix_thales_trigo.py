#!/usr/bin/env python3
"""
fix_thales_trigo.py — Fix spécifique Thalès + Trigo
Reformule les énoncés qui manquent de contexte.
"""
import json, re
from sheets import sh


def fix_thales_q(q):
    """Ajoute le contexte géométrique aux exos Thalès."""
    ql = q.lower()
    # Skip si déjà contextualisé
    if 'triangle' in ql or 'dans le' in ql or 'dans un' in ql:
        return q
    # Skip calcul pur
    if 'agrandissement' in ql or 'coefficient' in ql:
        return q
    # Skip ombre (déjà contextuel)
    if 'ombre' in ql or 'poteau' in ql or 'arbre' in ql:
        return q
    # "Deux droites coupées par des parallèles"
    if 'deux droites' in ql or 'droites coupées' in ql:
        q = "Dans une configuration de Thalès, d" + q[1:]
        return q
    # Commence par $AB=... ou AB=...
    q_stripped = q.lstrip('$').strip()
    if re.match(r'^[A-Z]{2}\s*=', q_stripped) or re.match(r'^\$[A-Z]{2}', q):
        prefix = "Dans le triangle ABC, M est sur [AB] et N sur [AC], avec (MN) parallèle à (BC). "
        return prefix + q
    return q


def fix_trigo_q(q):
    """Clarifie les exos trigo : précise l'angle et le triangle."""
    ql = q.lower()
    # Skip valeurs remarquables pures
    if re.match(r'^\s*\$?\s*(cos|sin|tan)\s*\(', ql):
        return q
    # Skip si déjà bien contextualisé
    if 'triangle rectangle' in ql:
        return q
    # "Côté opposé = X, adjacent = Y" → ajouter contexte
    if ('opposé' in ql or 'adjacent' in ql) and 'triangle' not in ql:
        q = "Dans un triangle rectangle, " + q[0].lower() + q[1:]
    # "Hypoténuse X, angle Y°" sans contexte
    if 'hypoténuse' in ql and 'triangle' not in ql:
        q = "Dans un triangle rectangle, l'" + q[0].lower() + q[1:]
    # "angle d'élévation" → ajouter note
    if "angle d'élévation" in ql and 'schéma' not in ql:
        q = q.rstrip('.?! ') + " (l'angle est mesuré depuis l'horizontale)."
    return q


def fix_sym_axiale_q(q):
    """Clarifie le vocabulaire des axes."""
    q = re.sub(r"l'axe des ordonnées(?!\s*\()", "l'axe vertical (axe des ordonnées)", q)
    q = re.sub(r"l'axe des abscisses(?!\s*\()", "l'axe horizontal (axe des abscisses)", q)
    return q


def fix_sections_q(q):
    """Précise 'depuis le sommet'."""
    q = re.sub(r'au tiers de la hauteur(?!\s+(en|depuis))', 'au tiers de la hauteur en partant du sommet', q)
    q = re.sub(r'à mi-hauteur(?!\s+(en|depuis))', 'à mi-hauteur en partant du sommet', q)
    return q


def process_tab(tab_name, exos_col_idx):
    """Applique les reformulations ciblées."""
    print(f"\n📋 {tab_name}")
    raw = sh.read_raw(tab_name)
    if not raw:
        return 0

    total = 0
    for row_idx in range(1, len(raw)):
        row = raw[row_idx]
        if len(row) <= exos_col_idx:
            continue

        cat = row[1]

        try:
            exos = json.loads(row[exos_col_idx])
        except (json.JSONDecodeError, TypeError):
            continue

        if not isinstance(exos, list):
            continue

        modified = False
        for exo in exos:
            if not isinstance(exo, dict) or 'q' not in exo:
                continue

            original = exo['q']

            if 'thalès' in cat.lower():
                exo['q'] = fix_thales_q(exo['q'])

            if 'trigono' in cat.lower():
                exo['q'] = fix_trigo_q(exo['q'])

            if 'symétrie_axiale' in cat.lower():
                exo['q'] = fix_sym_axiale_q(exo['q'])

            if 'section' in cat.lower():
                exo['q'] = fix_sections_q(exo['q'])

            if exo['q'] != original:
                total += 1
                modified = True
                print(f"  ✏️ {row[0]} {cat}: {exo['q'][:80]}...")

        if modified:
            row[exos_col_idx] = json.dumps(exos, ensure_ascii=False)
            raw[row_idx] = row

    if total > 0:
        sh.write_rows(tab_name, raw, include_header=False)
    print(f"  📊 {total} reformulations")
    return total


def main():
    print("🔧 fix_thales_trigo.py — Reformulations ciblées")
    t1 = process_tab("DiagnosticExos", 2)
    t2 = process_tab("BoostExos", 2)
    t3 = process_tab("Curriculum_Officiel", 4)
    print(f"\n✅ TOTAL: {t1+t2+t3} reformulations")


if __name__ == "__main__":
    main()
