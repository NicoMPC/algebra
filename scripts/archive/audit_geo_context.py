#!/usr/bin/env python3
"""
audit_geo_context.py — Audit des exercices de géométrie trop abstraits
======================================================================
Cherche les exercices géométriques dont l'énoncé est trop court ou
manque de contexte concret (figure, unité, situation réelle).

Usage : python3 audit_geo_context.py
Output : docs/audit-geo-context-2026-03-14.md
"""

import json, re, sys
from datetime import date
from sheets import sh

ONGLETS = ["Curriculum_Officiel", "DiagnosticExos", "BoostExos"]
OUTPUT = "/home/nicolas/Bureau/algebra live/algebra/docs/audit-geo-context-2026-03-14.md"

# Chapitres géométriques (match partiel, insensible à la casse)
GEO_KEYWORDS = [
    "géométrie", "périmètre", "aire", "angle", "pythagore",
    "triangle", "symétri", "thalès", "transformation", "homothétie",
    "section", "volume", "parallèle", "perpendiculaire", "cercle",
    "quadrilatère", "rectangle", "carré", "losange", "trapèze",
    "polygone", "rotation", "translation", "agrandissement", "réduction",
]

# Mots/patterns indiquant un contexte concret
CONTEXT_PATTERNS = [
    # Figures nommées
    r'triangle\s+[A-Z]{3}', r'rectangle\s+[A-Z]{4}', r'cercle\s+[A-Z]',
    r'point\s+[A-Z]', r'droite\s+\(', r'segment\s+\[',
    r'[A-Z]{2,4}', r'figure',
    # Unités
    r'\d+\s*(cm|mm|m|km|dm|°|deg)', r'mètre', r'centi',
    # Contexte réel
    r'jardin', r'terrain', r'piscine', r'chambre', r'salle',
    r'route', r'tour', r'bâtiment', r'maison', r'école',
    r'ballon', r'roue', r'table', r'carte', r'plan',
    r'échelle', r'distance', r'hauteur', r'largeur', r'longueur',
]


def is_geo_chapter(chapter):
    """Vérifie si un chapitre est géométrique."""
    ch_lower = str(chapter).lower()
    return any(kw in ch_lower for kw in GEO_KEYWORDS)


def has_context(q):
    """Vérifie si l'énoncé contient un contexte concret."""
    for pat in CONTEXT_PATTERNS:
        if re.search(pat, str(q), re.IGNORECASE):
            return True
    return False


def audit_onglet(tab_name):
    """Audite un onglet pour les exercices géo abstraits."""
    print(f"  Lecture de {tab_name}...")
    try:
        rows = sh.read(tab_name)
    except Exception as e:
        print(f"  ⚠️ Erreur lecture {tab_name}: {e}")
        return [], 0

    results = []
    geo_count = 0

    for row_idx, row in enumerate(rows):
        chapter = row.get("Chapitre", row.get("Chapter", ""))
        if not is_geo_chapter(chapter):
            continue

        raw = row.get("ExosJSON", "")
        if not raw:
            continue

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
            if not q:
                continue

            geo_count += 1
            warnings = []

            if len(q) < 60:
                warnings.append("WARN_TOO_SHORT")

            if not has_context(q):
                warnings.append("WARN_NO_CONTEXT")

            if warnings:
                results.append({
                    "tab": tab_name,
                    "level": level,
                    "chapter": chapter,
                    "row": row_idx + 2,
                    "exo": ex_idx + 1,
                    "q": q[:120],
                    "q_len": len(q),
                    "warnings": warnings,
                })

    return results, geo_count


def generate_report(all_results, total_geo):
    """Génère le rapport Markdown."""
    total_warnings = sum(len(r["warnings"]) for r in all_results)

    lines = [
        f"# Audit Géométrie — Contexte — {date.today()}",
        "",
        f"Exercices géométriques analysés: **{total_geo}**",
        f"Exercices avec warnings: **{len(all_results)}**",
        f"Total warnings: **{total_warnings}**",
        "",
    ]

    # Stats par type
    counts = {}
    for r in all_results:
        for w in r["warnings"]:
            counts[w] = counts.get(w, 0) + 1

    lines.append("## Résumé")
    lines.append("")
    lines.append("| Type | Count |")
    lines.append("|------|-------|")
    for wtype in sorted(counts):
        lines.append(f"| {wtype} | {counts[wtype]} |")
    lines.append("")

    # Par chapitre
    chap_counts = {}
    for r in all_results:
        key = f"{r['level']} / {r['chapter']}"
        chap_counts[key] = chap_counts.get(key, 0) + len(r["warnings"])

    lines.append("## Par chapitre")
    lines.append("")
    lines.append("| Chapitre | Warnings |")
    lines.append("|----------|----------|")
    for chap in sorted(chap_counts, key=lambda x: -chap_counts[x]):
        lines.append(f"| {chap} | {chap_counts[chap]} |")
    lines.append("")

    # Détails
    lines.append("## Détails")
    lines.append("")

    for r in all_results:
        flags = ", ".join(f"`{w}`" for w in r["warnings"])
        lines.append(
            f"- **{r['tab']}** {r['level']}/{r['chapter']} "
            f"(row {r['row']}, exo {r['exo']}) [{r['q_len']} chars] {flags}"
        )
        lines.append(f"  > {r['q']}")
        lines.append("")

    return "\n".join(lines)


def main():
    print("=== Audit Géométrie — Contexte ===")
    all_results = []
    total_geo = 0

    for tab in ONGLETS:
        results, geo_count = audit_onglet(tab)
        all_results.extend(results)
        total_geo += geo_count
        print(f"  → {len(results)} warnings dans {tab} ({geo_count} exos géo)")

    report = generate_report(all_results, total_geo)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(report)

    total = sum(len(r["warnings"]) for r in all_results)
    print(f"\n✅ Rapport généré : {OUTPUT}")
    print(f"   {total} warnings sur {len(all_results)} exercices ({total_geo} géo total)")


if __name__ == "__main__":
    main()
