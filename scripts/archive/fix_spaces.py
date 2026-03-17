#!/usr/bin/env python3
"""
fix_spaces.py — Restaure les espaces autour des $ LaTeX dans les exos.
Le bug: clean_latex supprimait '$ ' et ' $', collant mots et formules.
Fix: ajoute un espace avant $ ouvrant et après $ fermant si manquant.
"""
import json, re
from sheets import sh


def fix_latex_spaces(s):
    """Ajoute les espaces manquants autour des $ LaTeX."""
    if not s or '$' not in s:
        return s

    result = []
    i = 0
    in_math = False
    while i < len(s):
        if s[i] == '$':
            if not in_math:
                # Opening $ — ensure space before (unless start of string or after certain chars)
                if i > 0 and s[i-1] not in (' ', '\n', '\t', '(', '[', '{', ':'):
                    result.append(' ')
                result.append('$')
                in_math = True
            else:
                # Closing $ — add it, then ensure space after (unless end or before certain chars)
                result.append('$')
                in_math = False
                if i + 1 < len(s) and s[i+1] not in (' ', '\n', '\t', '.', ',', ')', ']', '}', '?', '!', ';', ':', '-', '/', '\\'):
                    result.append(' ')
            i += 1
        else:
            result.append(s[i])
            i += 1

    return ''.join(result)


def process_tab(tab_name, exos_col_idx):
    """Fix les espaces LaTeX dans un onglet."""
    print(f"\n📋 {tab_name}")
    raw = sh.read_raw(tab_name)
    if not raw:
        return 0

    total_fixed = 0
    for row_idx in range(1, len(raw)):
        row = raw[row_idx]
        if len(row) <= exos_col_idx:
            continue

        try:
            exos = json.loads(row[exos_col_idx])
        except (json.JSONDecodeError, TypeError):
            continue

        if not isinstance(exos, list):
            continue

        modified = False
        for exo in exos:
            if not isinstance(exo, dict):
                continue
            for field in ['q', 'a', 'f']:
                if field in exo and isinstance(exo[field], str) and '$' in exo[field]:
                    fixed = fix_latex_spaces(exo[field])
                    if fixed != exo[field]:
                        exo[field] = fixed
                        modified = True
                        total_fixed += 1
            if 'options' in exo:
                for j, opt in enumerate(exo['options']):
                    if isinstance(opt, str) and '$' in opt:
                        fixed = fix_latex_spaces(opt)
                        if fixed != opt:
                            exo['options'][j] = fixed
                            modified = True
            if 'steps' in exo:
                for j, step in enumerate(exo['steps']):
                    if isinstance(step, str) and '$' in step:
                        fixed = fix_latex_spaces(step)
                        if fixed != step:
                            exo['steps'][j] = fixed
                            modified = True

        if modified:
            row[exos_col_idx] = json.dumps(exos, ensure_ascii=False)
            raw[row_idx] = row

    if total_fixed > 0:
        sh.write_rows(tab_name, raw, include_header=False)
    print(f"  ✅ {total_fixed} espaces restaurés")
    return total_fixed


def main():
    print("🔧 fix_spaces.py — Restauration des espaces LaTeX")
    t1 = process_tab("DiagnosticExos", 2)
    t2 = process_tab("BoostExos", 2)
    t3 = process_tab("Curriculum_Officiel", 4)
    print(f"\n✅ TOTAL: {t1+t2+t3} corrections d'espaces")


if __name__ == "__main__":
    main()
