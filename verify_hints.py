#!/usr/bin/env python3
"""
verify_hints.py — Audit des indices (steps) d'exercices
========================================================
Cherche les cas où un indice révèle la réponse, contient une formule complète,
est trop court, ou duplique la formule de l'exercice.

Usage : python3 verify_hints.py
Output : docs/audit-hints-2026-03-14.md
"""

import json, re, sys
from datetime import date
from sheets import sh

ONGLETS = ["Curriculum_Officiel", "DiagnosticExos", "BoostExos"]
OUTPUT = "/home/nicolas/Bureau/algebra live/algebra/docs/audit-hints-2026-03-14.md"


def normalize(s):
    """Normalise pour comparaison : strip, supprime $, espaces."""
    if not s:
        return ""
    s = str(s).strip().replace("$", "").replace(" ", "").lower()
    return s


def check_hint_is_answer(steps, answer):
    """CHECK A: un step contient la valeur de 'a' (réponse correcte)."""
    a_norm = normalize(answer)
    if not a_norm or len(a_norm) < 2:
        return []
    warnings = []
    for i, step in enumerate(steps):
        s_norm = normalize(step)
        if a_norm in s_norm:
            warnings.append((i + 1, step, "WARN_HINT_IS_ANSWER"))
    return warnings


def check_hint_is_formula(steps):
    """CHECK B: un step contient une formule complète ($...=...$ avec variable)."""
    warnings = []
    pattern = re.compile(r'\$[^$]*[a-zA-Z][^$]*=[^$]+\$')
    for i, step in enumerate(steps):
        if pattern.search(str(step)):
            warnings.append((i + 1, step, "WARN_HINT_IS_FORMULA"))
    return warnings


def check_hint_too_short(steps):
    """CHECK C: un step fait moins de 10 caractères."""
    warnings = []
    for i, step in enumerate(steps):
        if len(str(step).strip()) < 10:
            warnings.append((i + 1, step, "WARN_HINT_TOO_SHORT"))
    return warnings


def check_hint_duplicate_formula(steps, formula):
    """CHECK D: un step est identique à la formule (f)."""
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


def audit_onglet(tab_name):
    """Audite un onglet et retourne la liste des warnings."""
    print(f"  Lecture de {tab_name}...")
    try:
        rows = sh.read(tab_name)
    except Exception as e:
        print(f"  ⚠️ Erreur lecture {tab_name}: {e}")
        return []

    results = []
    exos_col = "ExosJSON"

    for row_idx, row in enumerate(rows):
        raw = row.get(exos_col, "")
        if not raw:
            continue

        chapter = row.get("Chapitre", row.get("Chapter", "?"))
        level = row.get("Niveau", row.get("Level", "?"))

        try:
            exos = json.loads(raw)
        except (json.JSONDecodeError, TypeError):
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
            warnings.extend(check_hint_is_formula(steps))
            warnings.extend(check_hint_too_short(steps))
            warnings.extend(check_hint_duplicate_formula(steps, f))

            if warnings:
                results.append({
                    "tab": tab_name,
                    "level": level,
                    "chapter": chapter,
                    "row": row_idx + 2,
                    "exo": ex_idx + 1,
                    "q": q[:80],
                    "a": str(a)[:40],
                    "warnings": warnings,
                })

    return results


def generate_report(all_results):
    """Génère le rapport Markdown."""
    lines = [
        f"# Audit Hints — {date.today()}",
        "",
        f"Total warnings: **{sum(len(r['warnings']) for r in all_results)}** "
        f"sur **{len(all_results)}** exercices",
        "",
    ]

    # Stats par type
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

    # Stats par onglet
    tabs = {}
    for r in all_results:
        tabs[r["tab"]] = tabs.get(r["tab"], 0) + len(r["warnings"])

    lines.append("## Par onglet")
    lines.append("")
    for tab, cnt in sorted(tabs.items()):
        lines.append(f"- **{tab}**: {cnt} warnings")
    lines.append("")

    # Détails
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
    print("=== Audit Hints ===")
    all_results = []
    for tab in ONGLETS:
        results = audit_onglet(tab)
        all_results.extend(results)
        print(f"  → {len(results)} exercices avec warnings dans {tab}")

    report = generate_report(all_results)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(report)

    total = sum(len(r["warnings"]) for r in all_results)
    print(f"\n✅ Rapport généré : {OUTPUT}")
    print(f"   {total} warnings sur {len(all_results)} exercices")


if __name__ == "__main__":
    main()
