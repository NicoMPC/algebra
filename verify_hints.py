#!/usr/bin/env python3
"""
verify_hints.py — Audit des indices (steps) d'exercices (Supabase)
===================================================================
Cherche les cas où un indice révèle la réponse, contient une formule complète,
est trop court, ou duplique la formule de l'exercice.

Usage : python3 verify_hints.py
Output : docs/audit-hints-YYYY-MM-DD.md
"""

import json, re, sys
from datetime import date
from supabase_helper import sb

# Mapping ancien onglet Sheet → table Supabase + colonne exos
ONGLETS = {
    "curriculum":      {"table": "curriculum",      "exos_col": "exos_json", "cat_col": "categorie", "lvl_col": "niveau"},
    "diagnostic_exos": {"table": "diagnostic_exos", "exos_col": "exos_json", "cat_col": "categorie", "lvl_col": "niveau"},
}

OUTPUT = f"/home/nicolas/Bureau/algebra live/algebra/docs/audit-hints-{date.today()}.md"


_NUMERIC_RE = re.compile(r'^-?\d+(?:[.,]\d+)?(?:°|%|cm|m|km|g|kg)?$')
_TRIVIAL_ANSWERS = {"vrai", "faux", "oui", "non"}


def normalize(s):
    if not s:
        return ""
    s = str(s).strip().replace("$", "").replace(" ", "").lower()
    return s


def _is_numeric_or_trivial(a_norm):
    """Une réponse numérique courte ou Vrai/Faux apparaît naturellement dans
    les calculs intermédiaires et le raisonnement — ce n'est pas un dévoilement."""
    if a_norm in _TRIVIAL_ANSWERS:
        return True
    if _NUMERIC_RE.match(a_norm):
        return True
    return False


def check_hint_is_answer(steps, answer):
    """Détecte un step qui dévoile textuellement la réponse.

    Pédagogiquement : un calcul intermédiaire qui produit la réponse est OK
    (c'est le raisonnement). Un step affirmatif qui contient la réponse
    textuelle (ex: a="parallélogramme") est un dévoilement.

    Règle : on flag uniquement si la réponse est une chaîne non-triviale
    (pas un nombre, pas Vrai/Faux/Oui/Non) et qu'elle apparaît dans un step.
    """
    a_norm = normalize(answer)
    if not a_norm or len(a_norm) < 3:
        return []
    if _is_numeric_or_trivial(a_norm):
        return []
    warnings = []
    for i, step in enumerate(steps):
        s_norm = normalize(step)
        if a_norm in s_norm:
            warnings.append((i + 1, step, "WARN_HINT_IS_ANSWER"))
    return warnings


# Pattern "invitation finale" : uniquement des symboles math/ponctuation
# (ex: `$= $?`, `$= $?.`, `= ?$`, etc.) — pas de lettres, pas de chiffres
_INVITATION_CHARS = re.compile(r'^[\$=\?\.\s]+$')
_CONVENTION_WORDS = re.compile(r'^(vrai|faux|oui|non)\.?$', re.IGNORECASE)


def _is_convention_final(step):
    """Skip les conventions pédago valides : step final invitant à répondre
    (`$= $?`, `= ?`, etc.) ou confirmation V/F (Vrai./Faux.)."""
    s = str(step).strip()
    if _INVITATION_CHARS.match(s):
        return True
    if _CONVENTION_WORDS.match(s):
        return True
    return False


def check_hint_too_short(steps):
    """Un step trop court (<7 chars) est probablement un résidu.
    Skip les conventions d'invitation finale ($= ?$., Vrai./Faux.)."""
    warnings = []
    for i, step in enumerate(steps):
        s = str(step).strip()
        if len(s) < 7 and not _is_convention_final(step):
            warnings.append((i + 1, step, "WARN_HINT_TOO_SHORT"))
    return warnings


def check_hint_duplicate_formula(steps, formula):
    if not formula:
        return []
    f_norm = normalize(formula)
    if not f_norm:
        return []
    warnings = []
    for i, step in enumerate(steps):
        if normalize(step) == f_norm:
            warnings.append((i + 1, step, "WARN_DUPLICATE"))
    return warnings


def audit_table(name, config):
    """Audite une table Supabase et retourne la liste des warnings."""
    table = config["table"]
    exos_col = config["exos_col"]
    cat_col = config["cat_col"]
    lvl_col = config["lvl_col"]

    print(f"  Lecture de {table}...")
    try:
        rows = sb.read(table)
    except Exception as e:
        print(f"  ⚠️ Erreur lecture {table}: {e}")
        return []

    results = []
    for row_idx, row in enumerate(rows):
        raw = row.get(exos_col, "")
        if not raw:
            continue

        chapter = row.get(cat_col, "?")
        level = row.get(lvl_col, "?")

        if isinstance(raw, str):
            try:
                exos = json.loads(raw)
            except (json.JSONDecodeError, TypeError):
                continue
        elif isinstance(raw, list):
            exos = raw
        else:
            continue

        if isinstance(exos, dict):
            exos = [exos]
        if not isinstance(exos, list):
            continue

        for ex_idx, ex in enumerate(exos):
            if not isinstance(ex, dict):
                continue

            q = ex.get("q", "")
            a = ex.get("a", "")
            f = ex.get("f", "")
            steps = ex.get("steps", [])

            if not steps or not isinstance(steps, list):
                continue

            warnings = []
            warnings.extend(check_hint_is_answer(steps, a))
            warnings.extend(check_hint_too_short(steps))
            warnings.extend(check_hint_duplicate_formula(steps, f))

            if warnings:
                results.append({
                    "tab": table,
                    "level": level,
                    "chapter": chapter,
                    "row": row_idx + 1,
                    "exo": ex_idx + 1,
                    "q": q[:80],
                    "a": str(a)[:40],
                    "warnings": warnings,
                })

    return results


def generate_report(all_results):
    lines = [
        f"# Audit Hints — {date.today()}",
        "",
        f"Total warnings: **{sum(len(r['warnings']) for r in all_results)}** "
        f"sur **{len(all_results)}** exercices",
        "",
    ]

    counts = {}
    for r in all_results:
        for _, _, wtype in r["warnings"]:
            counts[wtype] = counts.get(wtype, 0) + 1

    lines.append("## Résumé par type")
    lines.append("")
    lines.append("| Type | Count |")
    lines.append("|------|-------|")
    for wtype in sorted(counts):
        lines.append(f"| {wtype} | {counts[wtype]} |")
    lines.append("")

    tabs = {}
    for r in all_results:
        tabs[r["tab"]] = tabs.get(r["tab"], 0) + len(r["warnings"])

    lines.append("## Par table")
    lines.append("")
    for tab, cnt in sorted(tabs.items()):
        lines.append(f"- **{tab}**: {cnt} warnings")
    lines.append("")

    lines.append("## Détails")
    lines.append("")

    for r in all_results:
        lines.append(f"### {r['tab']} — {r['level']} / {r['chapter']} (row {r['row']}, exo {r['exo']})")
        lines.append(f"- **Q**: {r['q']}")
        lines.append(f"- **A**: {r['a']}")
        for step_num, step_text, wtype in r["warnings"]:
            lines.append(f"- `{wtype}` step {step_num}: _{step_text[:100]}_")
        lines.append("")

    return "\n".join(lines)


def main():
    print("=== Audit Hints (Supabase) ===")
    all_results = []
    for name, config in ONGLETS.items():
        results = audit_table(name, config)
        all_results.extend(results)
        print(f"  → {len(results)} exercices avec warnings dans {config['table']}")

    report = generate_report(all_results)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(report)

    total = sum(len(r["warnings"]) for r in all_results)
    print(f"\n✅ Rapport généré : {OUTPUT}")
    print(f"   {total} warnings sur {len(all_results)} exercices")


if __name__ == "__main__":
    main()
