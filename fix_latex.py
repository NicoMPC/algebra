#!/usr/bin/env python3
"""
fix_latex.py — Corrige les formules LaTeX dans les exercices
  1) Champs avec commandes LaTeX sans $...$ → wrap dans $...$
  2) UNICODE_MIX : caractères Unicode math hors $...$ quand le champ contient du LaTeX

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

# Unicode math → LaTeX equivalents
UNICODE_TO_LATEX = {
    '×': r'\times',
    '÷': r'\div',
    '±': r'\pm',
    '∓': r'\mp',
    '≤': r'\leq',
    '≥': r'\geq',
    '≠': r'\neq',
    '≈': r'\approx',
    '√': r'\sqrt{}',
    '∑': r'\sum',
    '∏': r'\prod',
    '∫': r'\int',
    '∞': r'\infty',
    '∈': r'\in',
    '∉': r'\notin',
    '⊂': r'\subset',
    '⊃': r'\supset',
    '∪': r'\cup',
    '∩': r'\cap',
    '∀': r'\forall',
    '∃': r'\exists',
    '→': r'\rightarrow',
    '←': r'\leftarrow',
    '⇒': r'\Rightarrow',
    '⇐': r'\Leftarrow',
    '⇔': r'\Leftrightarrow',
    '²': r'^2',
    '³': r'^3',
}

SUSPECT_CHARS = re.compile(r'[√∑∏∫∞≈≠≤≥±∓×÷∈∉⊂⊃∪∩∀∃→←⇒⇐⇔²³]')

# Same chars but only ones that make sense to replace inside $...$
UNICODE_INSIDE_LATEX = {
    '×': r'\times ',
    '÷': r'\div ',
    '±': r'\pm ',
    '∓': r'\mp ',
    '≤': r'\leq ',
    '≥': r'\geq ',
    '≠': r'\neq ',
    '≈': r'\approx ',
    '∞': r'\infty ',
    '∈': r'\in ',
    '∉': r'\notin ',
    '⊂': r'\subset ',
    '⊃': r'\supset ',
    '∪': r'\cup ',
    '∩': r'\cap ',
    '∀': r'\forall ',
    '∃': r'\exists ',
    '→': r'\rightarrow ',
    '←': r'\leftarrow ',
    '⇒': r'\Rightarrow ',
    '⇐': r'\Leftarrow ',
    '⇔': r'\Leftrightarrow ',
}


def needs_wrap(text):
    """True si le texte contient du LaTeX sans aucun $."""
    if not text or not isinstance(text, str):
        return False
    if '$' in text:
        return False
    return bool(LATEX_CMDS.search(text))


def fix_unicode_inside_latex(text):
    """Replace Unicode math chars inside $...$ with LaTeX commands."""
    if not text or not isinstance(text, str):
        return text, False
    if '$' not in text:
        return text, False

    parts = []
    pos = 0
    changed = False
    while pos < len(text):
        dollar = text.find('$', pos)
        if dollar == -1:
            parts.append(text[pos:])
            break
        if dollar > pos:
            parts.append(text[pos:dollar])
        end = text.find('$', dollar + 1)
        if end == -1:
            parts.append(text[dollar:])
            pos = len(text)
            break
        # This is a $...$ block
        inner = text[dollar + 1:end]
        new_inner = inner
        for uchar, latex in UNICODE_INSIDE_LATEX.items():
            if uchar in new_inner:
                new_inner = new_inner.replace(uchar, latex)
                changed = True
        parts.append('$' + new_inner + '$')
        pos = end + 1

    if changed:
        return ''.join(parts), True
    return text, False


def fix_unicode_mix(text):
    """Replace Unicode math chars outside $...$ with LaTeX equivalents wrapped in $...$."""
    if not text or not isinstance(text, str):
        return text, False
    if '$' not in text:
        return text, False
    if not SUSPECT_CHARS.search(text):
        return text, False

    # Split text into segments: inside $...$ and outside
    parts = []
    pos = 0
    changed = False
    while pos < len(text):
        dollar = text.find('$', pos)
        if dollar == -1:
            # Rest is outside LaTeX
            parts.append(('out', text[pos:]))
            break
        # Text before $
        if dollar > pos:
            parts.append(('out', text[pos:dollar]))
        # Find closing $
        end = text.find('$', dollar + 1)
        if end == -1:
            # Unclosed $ — treat rest as inside
            parts.append(('in', text[dollar:]))
            pos = len(text)
            break
        parts.append(('in', text[dollar:end + 1]))
        pos = end + 1

    # Replace Unicode chars in 'out' segments
    result = []
    for kind, segment in parts:
        if kind == 'out' and SUSPECT_CHARS.search(segment):
            new_seg = segment
            for uchar, latex in UNICODE_TO_LATEX.items():
                if uchar in new_seg:
                    new_seg = new_seg.replace(uchar, f'${latex}$')
                    changed = True
            result.append(new_seg)
        else:
            result.append(segment)

    if changed:
        return ''.join(result), True
    return text, False


# Fields to check in each exercise
FIELDS_SIMPLE = ['q', 'a', 'f']


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
                # Fix 1: fields without any $ that contain LaTeX commands
                f_val = exo.get("f", "")
                if needs_wrap(f_val):
                    new_f = f"${f_val.strip()}$"
                    exo["f"] = new_f
                    row_changed = True
                    total_fixes += 1
                    print(f"  ✏️  [WRAP] {niveau}/{cat} exo#{i+1} [f]")
                    print(f"      AVANT: {f_val[:120]}")
                    print(f"      APRÈS: {new_f[:120]}")

                # Fix 2: UNICODE_MIX — replace Unicode math outside $...$ AND inside $...$
                for field in FIELDS_SIMPLE:
                    val = exo.get(field, "")
                    # Outside $...$
                    new_val, did_fix = fix_unicode_mix(val)
                    if did_fix:
                        exo[field] = new_val
                        row_changed = True
                        total_fixes += 1
                        print(f"  ✏️  [UNI-OUT] {niveau}/{cat} exo#{i+1} [{field}]")
                        print(f"      AVANT: {val[:120]}")
                        print(f"      APRÈS: {new_val[:120]}")
                        val = new_val
                    # Inside $...$
                    new_val2, did_fix2 = fix_unicode_inside_latex(val)
                    if did_fix2:
                        exo[field] = new_val2
                        row_changed = True
                        total_fixes += 1
                        print(f"  ✏️  [UNI-IN]  {niveau}/{cat} exo#{i+1} [{field}]")
                        print(f"      AVANT: {val[:120]}")
                        print(f"      APRÈS: {new_val2[:120]}")

                # Fix 2b: options array
                opts = exo.get("options", [])
                if isinstance(opts, list):
                    for oi, opt in enumerate(opts):
                        if isinstance(opt, str):
                            new_opt, did1 = fix_unicode_mix(opt)
                            if did1:
                                opts[oi] = new_opt
                                row_changed = True
                                total_fixes += 1
                                print(f"  ✏️  [UNI-OUT] {niveau}/{cat} exo#{i+1} [options[{oi}]]")
                                opt = new_opt
                            new_opt2, did2 = fix_unicode_inside_latex(opt)
                            if did2:
                                opts[oi] = new_opt2
                                row_changed = True
                                total_fixes += 1
                                print(f"  ✏️  [UNI-IN]  {niveau}/{cat} exo#{i+1} [options[{oi}]]")

                # Fix 2c: steps array
                steps = exo.get("steps", [])
                if isinstance(steps, list):
                    for si, step in enumerate(steps):
                        if isinstance(step, str):
                            new_step, did1 = fix_unicode_mix(step)
                            if did1:
                                steps[si] = new_step
                                row_changed = True
                                total_fixes += 1
                                print(f"  ✏️  [UNI-OUT] {niveau}/{cat} exo#{i+1} [steps[{si}]]")
                                step = new_step
                            new_step2, did2 = fix_unicode_inside_latex(step)
                            if did2:
                                steps[si] = new_step2
                                row_changed = True
                                total_fixes += 1
                                print(f"  ✏️  [UNI-IN]  {niveau}/{cat} exo#{i+1} [steps[{si}]]")

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
