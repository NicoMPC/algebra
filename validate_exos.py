#!/usr/bin/env python3
"""
validate_exos.py — Contrôle qualité obligatoire avant injection d'exercices.

Usage :
  python3 validate_exos.py exos.json              # Valide un fichier JSON
  python3 validate_exos.py exos.json --inject TAB  # Valide + injecte dans le Sheet
  python3 validate_exos.py --sheet TAB NIVEAU CAT  # Valide des exos déjà dans le Sheet

Gate bloquant : si une erreur CRITIQUE est détectée, l'injection est refusée.
"""

import json
import sys
import re
import os
from datetime import datetime

# ── Helpers ────────────────────────────────────────────────────

def parse_latex_number(s):
    """Extrait un nombre depuis une string potentiellement LaTeX."""
    s = s.replace('$', '').replace('\\,', '').replace(' ', '').replace('{', '').replace('}', '')
    s = s.replace('\\frac', '').replace('\\sqrt', 'sqrt').replace('\\pi', 'pi')
    try:
        return float(s)
    except:
        return None

def has_latex_delimiters(s):
    """Vérifie si une string contient du LaTeX entre $...$."""
    return bool(re.search(r'\$[^$]+\$', s))

def has_unicode_math(s):
    """Détecte des caractères Unicode math mélangés avec du LaTeX."""
    unicode_math = set('×÷²³⁴√≤≥≠±∞∈∉⊂⊃∪∩')
    if not has_latex_delimiters(s):
        return False
    return bool(unicode_math & set(s))

def is_passe_partout(step):
    """Détecte les steps génériques interdits."""
    blacklist = [
        "applique la formule",
        "vérifie ton calcul",
        "identifie les données",
        "relis l'énoncé",
        "utilise la bonne formule",
        "fais attention aux signes",
        "pose le calcul",
    ]
    low = step.lower().strip()
    return any(b in low for b in blacklist)

# ── Validation d'un exercice ──────────────────────────────────

def validate_exo(exo, idx, errors, warnings):
    """Valide un exercice et ajoute les erreurs/warnings aux listes."""
    prefix = f"Exo #{idx+1}"

    # ── Champs obligatoires ──
    for field in ['q', 'a', 'steps']:
        if field not in exo or not exo[field]:
            errors.append(f"{prefix} — Champ obligatoire manquant : '{field}'")
            return
    # options obligatoire sauf pour fill
    if exo.get('type') != 'fill' and (not exo.get('options')):
        errors.append(f"{prefix} — Champ obligatoire manquant : 'options'")
        return

    q = str(exo.get('q', ''))
    a = str(exo.get('a', ''))
    options = exo.get('options', [])
    steps = exo.get('steps', [])
    f = str(exo.get('f', ''))
    lvl = exo.get('lvl', 1)
    exo_type = exo.get('type', '')

    # ── a ∈ options ──
    if exo_type == 'fill':
        # Fill : pas d'options, juste vérifier que a existe et est non vide
        if not a.strip():
            errors.append(f"{prefix} — Fill sans réponse (a vide)")
    elif a not in options:
        # Essai tolérant (strip)
        stripped_opts = [o.strip() for o in options]
        if a.strip() not in stripped_opts:
            errors.append(f"{prefix} — RÉPONSE ABSENTE DES OPTIONS : a=\"{a}\" pas dans {options}")
        else:
            warnings.append(f"{prefix} — Espaces parasites entre a et options (corrigé par strip)")

    # ── Nombre d'options ──
    if exo_type == 'vf':
        if len(options) != 2:
            errors.append(f"{prefix} — VF doit avoir exactement 2 options, trouvé {len(options)}")
    elif exo_type == 'fill':
        pass  # fill n'a pas d'options
    else:
        if len(options) < 3:
            errors.append(f"{prefix} — QCM doit avoir au moins 3 options, trouvé {len(options)}")
        if len(options) > 4:
            warnings.append(f"{prefix} — {len(options)} options (attendu 3 ou 4)")

    # ── Doublons d'options ──
    if len(options) != len(set(options)):
        dupes = [o for o in set(options) if options.count(o) > 1]
        errors.append(f"{prefix} — OPTIONS EN DOUBLE : {dupes}")

    # ── Steps ──
    if len(steps) == 0:
        errors.append(f"{prefix} — Aucun step (indice)")
    elif len(steps) > 3:
        warnings.append(f"{prefix} — {len(steps)} steps (max recommandé : 3)")

    # Steps dupliqués
    for i in range(len(steps) - 1):
        if steps[i].strip() == steps[i+1].strip():
            errors.append(f"{prefix} — Step {i+1} et {i+2} sont identiques (copier-coller)")

    # Steps passe-partout
    for i, step in enumerate(steps):
        if is_passe_partout(step):
            errors.append(f"{prefix} — Step {i+1} est générique/passe-partout : \"{step[:60]}...\"")

    # Step trop court (probablement creux)
    for i, step in enumerate(steps):
        clean = re.sub(r'\$[^$]*\$', '', step).strip()
        if len(clean) < 10 and len(step) < 20:
            warnings.append(f"{prefix} — Step {i+1} très court ({len(step)} chars) : \"{step}\"")

    # ── LaTeX ──
    # Vérifier que les expressions math sont en LaTeX
    math_patterns = re.compile(r'(?<!\$)\b(\d+/\d+|\d+\^[\d{]|sqrt\(|pi\b)')
    if math_patterns.search(q) and not has_latex_delimiters(q):
        warnings.append(f"{prefix} — Énoncé contient des maths sans LaTeX $...$")

    # Unicode mix
    for field_name, field_val in [('q', q), ('a', a), ('f', f)] + [('options[{}]'.format(i), o) for i, o in enumerate(options)] + [('steps[{}]'.format(i), s) for i, s in enumerate(steps)]:
        if has_unicode_math(str(field_val)):
            errors.append(f"{prefix} — UNICODE_MIX dans {field_name} : mélange Unicode math + LaTeX")

    # LaTeX non fermé
    for field_name, field_val in [('q', q), ('a', a), ('f', f)]:
        dollar_count = str(field_val).count('$')
        if dollar_count % 2 != 0:
            errors.append(f"{prefix} — LaTeX non fermé dans {field_name} (nombre impair de $)")

    # ── Formule ──
    if f and a == f:
        warnings.append(f"{prefix} — Formule identique à la réponse (f devrait être générale)")

    # ── Level ──
    if lvl not in (1, 2):
        warnings.append(f"{prefix} — lvl={lvl} (attendu 1 ou 2)")

    # ── Longueur énoncé ──
    if len(q) < 15:
        warnings.append(f"{prefix} — Énoncé très court ({len(q)} chars)")
    if len(q) > 500:
        warnings.append(f"{prefix} — Énoncé très long ({len(q)} chars)")


# ── Validation d'un batch (20 exos = 4 slots) ────────────────

def validate_batch(exos, errors, warnings):
    """Validations au niveau du batch (cohérence inter-exos)."""
    n = len(exos)

    if n == 0:
        errors.append("BATCH — Aucun exercice")
        return

    if n != 20 and n != 5:
        warnings.append(f"BATCH — {n} exercices (attendu 20 pour un chapitre ou 5 pour un boost)")

    # Vérifier la variété des contextes (prénoms)
    prenoms = []
    for exo in exos:
        q = str(exo.get('q', ''))
        # Extraire les prénoms français courants
        found = re.findall(r'\b([A-Z][a-zéèêëàâäùûüïîôö]+)\b', q)
        prenoms.extend([p for p in found if len(p) > 2 and p not in ('Calcule', 'Détermine', 'Résoudre', 'Simplifie', 'Développe', 'Factorise', 'Soit', 'Dans', 'Une', 'Sur', 'Les', 'Par', 'Pour', 'Que', 'Est', 'Son', 'Des', 'Avec', 'Quel', 'Quelle', 'Combien', 'Trouve', 'Vrai', 'Faux')])
    if len(prenoms) > 0 and len(set(prenoms)) < len(prenoms) * 0.7:
        dupes = [p for p in set(prenoms) if prenoms.count(p) > 1]
        warnings.append(f"BATCH — Prénoms répétés : {dupes}")

    # Vérifier que les formules ne sont pas toutes identiques (sauf si même chapitre simple)
    formulas = [str(exo.get('f', '')) for exo in exos if exo.get('f')]
    if len(set(formulas)) == 1 and len(formulas) > 10:
        warnings.append(f"BATCH — Toutes les formules sont identiques (sous-compétences variées ?)")


# ── Main ──────────────────────────────────────────────────────

def validate_json_file(filepath):
    """Valide un fichier JSON d'exercices."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Accepter un array ou un objet avec clé "exos"
    if isinstance(data, dict):
        exos = data.get('exos', [])
    elif isinstance(data, list):
        exos = data
    else:
        print("❌ Format JSON invalide : attendu un array ou {exos: [...]}")
        return False

    errors = []
    warnings = []

    # Validation individuelle
    for i, exo in enumerate(exos):
        validate_exo(exo, i, errors, warnings)

    # Validation batch
    validate_batch(exos, errors, warnings)

    # ── Rapport ──
    print()
    print("=" * 60)
    print(f"  VALIDATION EXERCICES — {len(exos)} exos")
    print("=" * 60)
    print()

    if errors:
        print(f"🔴 {len(errors)} ERREURS CRITIQUES (bloquantes) :")
        for e in errors:
            print(f"   ❌ {e}")
        print()

    if warnings:
        print(f"🟡 {len(warnings)} WARNINGS :")
        for w in warnings:
            print(f"   ⚠️  {w}")
        print()

    if not errors and not warnings:
        print("✅ Aucune erreur, aucun warning.")
        print()

    print("=" * 60)
    if errors:
        print(f"  🔴 BLOQUÉ — {len(errors)} erreurs critiques. Corriger avant injection.")
    else:
        print(f"  ✅ VALIDÉ — {len(warnings)} warnings (non bloquants).")
    print("=" * 60)
    print()

    # ── Log ──
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"validate-{datetime.now().strftime('%Y-%m-%d-%H%M')}.md")
    with open(log_file, 'w', encoding='utf-8') as lf:
        lf.write(f"# Validation exercices — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        lf.write(f"- Fichier : `{filepath}`\n")
        lf.write(f"- Exercices : {len(exos)}\n")
        lf.write(f"- Erreurs : {len(errors)}\n")
        lf.write(f"- Warnings : {len(warnings)}\n\n")
        if errors:
            lf.write("## Erreurs critiques\n\n")
            for e in errors:
                lf.write(f"- {e}\n")
            lf.write("\n")
        if warnings:
            lf.write("## Warnings\n\n")
            for w in warnings:
                lf.write(f"- {w}\n")
    print(f"📄 Log : {log_file}")

    return len(errors) == 0


def validate_from_sheet(tab, niveau, categorie):
    """Valide des exercices directement depuis le Google Sheet."""
    from sheets import sh
    rows = sh.read(tab)
    target = None
    for r in rows:
        if r.get('Niveau', '').upper() == niveau.upper() and r.get('Categorie', '') == categorie:
            target = r
            break
    if not target:
        print(f"❌ Pas trouvé : {niveau}/{categorie} dans {tab}")
        return False

    exos_json = target.get('ExosJSON', '')
    try:
        exos = json.loads(exos_json)
    except json.JSONDecodeError as e:
        print(f"❌ JSON invalide dans {tab}/{niveau}/{categorie} : {e}")
        return False

    errors = []
    warnings = []
    for i, exo in enumerate(exos):
        validate_exo(exo, i, errors, warnings)
    validate_batch(exos, errors, warnings)

    print()
    print("=" * 60)
    print(f"  VALIDATION — {tab} / {niveau} / {categorie} — {len(exos)} exos")
    print("=" * 60)

    if errors:
        print(f"\n🔴 {len(errors)} ERREURS CRITIQUES :")
        for e in errors:
            print(f"   ❌ {e}")

    if warnings:
        print(f"\n🟡 {len(warnings)} WARNINGS :")
        for w in warnings:
            print(f"   ⚠️  {w}")

    if not errors and not warnings:
        print("\n✅ Tout est propre.")

    print()
    print("=" * 60)
    if errors:
        print(f"  🔴 BLOQUÉ — {len(errors)} erreurs.")
    else:
        print(f"  ✅ VALIDÉ — {len(warnings)} warnings.")
    print("=" * 60)

    return len(errors) == 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage :")
        print("  python3 validate_exos.py exos.json")
        print("  python3 validate_exos.py --sheet TAB NIVEAU CATEGORIE")
        sys.exit(1)

    if sys.argv[1] == '--sheet':
        if len(sys.argv) < 5:
            print("Usage : python3 validate_exos.py --sheet TAB NIVEAU CATEGORIE")
            sys.exit(1)
        ok = validate_from_sheet(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        ok = validate_json_file(sys.argv[1])

    sys.exit(0 if ok else 1)
