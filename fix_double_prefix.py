#!/usr/bin/env python3
"""Fix double prefix bug: 'Dans un triangle rectangle, l'dans un triangle rectangle, ...'"""
import json, re
from sheets import sh


def fix_double(s):
    """Remove double 'Dans un triangle rectangle' prefix."""
    # Pattern: "Dans un triangle rectangle, l'dans un triangle rectangle, ..."
    s = re.sub(
        r"Dans un triangle rectangle, l'dans un triangle rectangle, ",
        "Dans un triangle rectangle, ",
        s, flags=re.I
    )
    # Pattern: "Dans un triangle rectangle, dans un triangle rectangle, ..."
    s = re.sub(
        r"Dans un triangle rectangle, dans un triangle rectangle, ",
        "Dans un triangle rectangle, ",
        s, flags=re.I
    )
    return s


def process_tab(tab_name, exos_col_idx):
    raw = sh.read_raw(tab_name)
    if not raw:
        return 0

    total = 0
    for row_idx in range(1, len(raw)):
        row = raw[row_idx]
        if len(row) <= exos_col_idx:
            continue
        try:
            exos = json.loads(row[exos_col_idx])
        except:
            continue
        if not isinstance(exos, list):
            continue

        modified = False
        for exo in exos:
            if not isinstance(exo, dict) or 'q' not in exo:
                continue
            fixed = fix_double(exo['q'])
            if fixed != exo['q']:
                print(f"  🔧 {row[0]} {row[1]}: {fixed[:80]}...")
                exo['q'] = fixed
                modified = True
                total += 1

        if modified:
            row[exos_col_idx] = json.dumps(exos, ensure_ascii=False)
            raw[row_idx] = row

    if total > 0:
        sh.write_rows(tab_name, raw, include_header=False)
    return total


def main():
    print("🔧 Fix double prefix")
    t1 = process_tab("DiagnosticExos", 2)
    t2 = process_tab("BoostExos", 2)
    t3 = process_tab("Curriculum_Officiel", 4)
    print(f"✅ {t1+t2+t3} fixés")


if __name__ == "__main__":
    main()
