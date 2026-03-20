#!/usr/bin/env python3
"""
fix_latex.py — Corrige les formules LaTeX sans $...$ dans les exercices
Stratégie : si le champ f n'a AUCUN $ et contient des commandes LaTeX → wrap dans $...$

Usage : python3 fix_latex.py          (dry-run)
        python3 fix_latex.py --apply   (écriture réelle)
"""

import json, re, sys
from sheets import sh

APPLY = "--apply" in sys.argv
ONGLETS = ["Curriculum_Officiel", "DiagnosticExos", "BrevetExos"]

LATEX_CMDS = re.compile(
    r'\\(?:frac|dfrac|sqrt|times|div|cdot|pm|mp|leq|geq|neq|approx|equiv|'
    r'text|textbf|mathrm|mathbf|sum|prod|int|infty|'
    r'alpha|beta|gamma|delta|epsilon|theta|lambda|mu|pi|sigma|omega|Delta|Sigma|'
    r'sin|cos|tan|log|ln|exp|lim|left|right|begin|end|cases|'
    r'overrightarrow|vec|hat|bar|overline|Rightarrow|Leftarrow|implies|'
    r'forall|exists|mathbb|binom|triangle|angle|perp|parallel|circ|'
    r'ell|sim|emptyset|subset|supset|cup|cap|notin|neg|not)\b'
)


def needs_wrap(text):
    """True si le texte contient du LaTeX sans aucun $."""
    if not text or not isinstance(text, str):
        return False
    if '$' in text:
        return False
    return bool(LATEX_CMDS.search(text))


def main():
    total_fixes = 0

    for onglet in ONGLETS:
        print(f"\n📥 {onglet}…")
        rows = sh.read(onglet)
        raw = sh.read_raw(onglet)
        headers = raw[0]
        exos_col_idx = headers.index("ExosJSON")
        modified_count = 0

        for row_idx, row in enumerate(rows):
            exos_json = row.get("ExosJSON", "")
            if not exos_json:
                continue
            try:
                exos = json.loads(exos_json)
            except json.JSONDecodeError:
                continue
            if not isinstance(exos, list):
                continue

            niveau = row.get("Niveau", "?")
            cat = row.get("Categorie", row.get("Chapitre", "?"))
            row_changed = False

            for i, exo in enumerate(exos):
                f_val = exo.get("f", "")
                if needs_wrap(f_val):
                    new_f = f"${f_val.strip()}$"
                    exo["f"] = new_f
                    row_changed = True
                    total_fixes += 1
                    print(f"  ✏️  {niveau}/{cat} exo#{i+1}")
                    print(f"      AVANT: {f_val[:100]}")
                    print(f"      APRÈS: {new_f[:100]}")

            if row_changed:
                modified_count += 1
                new_json = json.dumps(exos, ensure_ascii=False)
                if APPLY:
                    sheet_row = row_idx + 2
                    sh.update_cell(onglet, sheet_row, exos_col_idx + 1, new_json)

        mode = "APPLIQUÉ" if APPLY else "DRY-RUN"
        print(f"  → {modified_count} lignes modifiées ({mode})")

    print(f"\n{'═' * 60}")
    print(f"  TOTAL : {total_fixes} formules corrigées")
    if not APPLY:
        print(f"  ⚠️  Mode DRY-RUN — relancer avec --apply pour écrire")
    else:
        print(f"  ✅ Corrections écrites dans Google Sheets")
    print("═" * 60)


if __name__ == "__main__":
    main()
