#!/usr/bin/env python3
"""
audit_latex.py — Audit LaTeX / KaTeX sur toute la base d'exercices
Vérifie les champs q, a, options, steps, f de chaque exercice
pour détecter les problèmes de rendu côté utilisateur.

Onglets scannés : Curriculum_Officiel, DiagnosticExos, BrevetExos, Cours

Usage : python3 audit_latex.py
"""

import json, re, sys
from sheets import sh

# ══════════════════════════════════════════════════════════════
# ONGLETS À SCANNER
# ══════════════════════════════════════════════════════════════

ONGLETS_EXOS = ["Curriculum_Officiel", "DiagnosticExos", "BrevetExos", "BoostExos"]

# ══════════════════════════════════════════════════════════════
# RÈGLES DE DÉTECTION LATEX
# ══════════════════════════════════════════════════════════════

# Commandes KaTeX supportées (subset — les plus courantes)
KATEX_SUPPORTED = {
    'frac', 'dfrac', 'tfrac', 'sqrt', 'text', 'textbf', 'textit', 'mathrm', 'mathbf',
    'times', 'div', 'cdot', 'pm', 'mp', 'leq', 'geq', 'neq', 'approx', 'equiv',
    'lt', 'gt', 'le', 'ge', 'll', 'gg',
    'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'theta', 'lambda', 'mu', 'pi', 'sigma', 'omega',
    'Delta', 'Sigma', 'Omega', 'Pi',
    'sin', 'cos', 'tan', 'log', 'ln', 'exp', 'lim', 'max', 'min',
    'sum', 'prod', 'int', 'infty',
    'left', 'right', 'big', 'Big', 'bigg', 'Bigg',
    'begin', 'end', 'cases', 'array', 'matrix', 'pmatrix', 'bmatrix',
    'hat', 'bar', 'vec', 'dot', 'ddot', 'tilde', 'overline', 'underline', 'widehat',
    'overset', 'underset', 'stackrel',
    'color', 'boxed', 'cancel', 'bcancel', 'xcancel',
    'quad', 'qquad', 'space', 'enspace', 'hspace',
    'Rightarrow', 'Leftarrow', 'Leftrightarrow', 'rightarrow', 'leftarrow',
    'implies', 'iff', 'to', 'mapsto',
    'forall', 'exists', 'in', 'notin', 'subset', 'supset', 'cup', 'cap',
    'mathbb', 'mathcal', 'mathscr',
    'not', 'neg',
    'ldots', 'cdots', 'vdots', 'ddots',
    'binom', 'dbinom', 'tbinom',
    'overbrace', 'underbrace',
    'phantom', 'hphantom', 'vphantom',
    'smallsetminus', 'setminus', 'backslash',
    'perp', 'parallel', 'angle', 'measuredangle', 'triangle',
    'circ', 'degree',
    'prime',
}

# Espaces LaTeX valides
LATEX_SPACES = {',', ';', '!', ':', ' ', '\\'}


def find_latex_issues(text):
    """Analyse un texte et retourne une liste de problèmes LaTeX détectés."""
    if not text or not isinstance(text, str):
        return []

    issues = []

    # ── 1. Dollars non appariés ──
    # Compter les $ en ignorant les \$
    cleaned = text.replace('\\$', '')
    dollar_count = cleaned.count('$')
    if dollar_count % 2 != 0:
        issues.append(("DOLLAR_IMPAIR", f"Nombre impair de $ ({dollar_count}) — rendu cassé"))

    # ── 2. Extraire tous les blocs $...$ ──
    blocks = re.findall(r'\$([^$]+)\$', cleaned)

    for block in blocks:
        # 2a. Accolades non équilibrées
        depth = 0
        for ch in block:
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
            if depth < 0:
                break
        if depth != 0:
            issues.append(("ACCOLADES", f"Accolades déséquilibrées dans ${block}$"))

        # 2b. Commandes LaTeX inconnues de KaTeX
        cmds = re.findall(r'\\([a-zA-Z]+)', block)
        for cmd in cmds:
            if cmd not in KATEX_SUPPORTED:
                issues.append(("CMD_INCONNUE", f"\\{cmd} potentiellement non supporté par KaTeX dans ${block}$"))

        # 2c. \frac, \sqrt sans accolades
        if re.search(r'\\frac\s*[^{]', block):
            issues.append(("FRAC_SANS_ACCOLADE", f"\\frac sans accolades dans ${block}$"))
        if re.search(r'\\sqrt\s*[^{[\s]', block) and not re.search(r'\\sqrt\[', block):
            # \sqrt peut avoir \sqrt{x} ou \sqrt[n]{x}
            pass  # tricky to detect reliably, skip

        # 2d. ^ ou _ sans accolades pour multi-caractères
        for m in re.finditer(r'[\^_]([^{\\])', block):
            after = m.group(1)
            pos = m.end()
            if pos < len(block) and block[pos:pos+1].isalnum():
                # multi-char sans accolades: x^12 au lieu de x^{12}
                snippet = block[m.start():min(m.start()+10, len(block))]
                issues.append(("EXPOSANT_SANS_ACCOLADE", f"Exposant/indice multi-char sans accolades: {snippet} dans ${block}$"))

        # 2e. Double backslash hors environnement (peut causer erreur KaTeX)
        if '\\\\' in block and not re.search(r'\\begin\{', block):
            issues.append(("DOUBLE_BACKSLASH", f"\\\\ hors environnement dans ${block}$"))

    # ── 3. LaTeX hors dollars (backslash commands en texte brut) ──
    # Chercher des patterns LaTeX qui devraient être dans des $...$
    outside = re.sub(r'\$[^$]*\$', '', cleaned)
    latex_outside = re.findall(r'\\(frac|sqrt|times|div|cdot|pm|leq|geq|neq|alpha|beta|pi|theta|sum|int|infty)\b', outside)
    if latex_outside:
        issues.append(("LATEX_HORS_DOLLAR", f"Commandes LaTeX hors $...$: {', '.join('\\\\'+c for c in latex_outside)}"))

    # ── 4. HTML entities qui ne rendent pas ──
    html_ents = re.findall(r'&[a-zA-Z]+;', text)
    if html_ents:
        issues.append(("HTML_ENTITY", f"HTML entities dans le texte: {', '.join(html_ents)}"))

    # ── 5. Unicode math mal rendu potentiel ──
    # Certains caractères Unicode passent mais d'autres non
    suspect_chars = re.findall(r'[√∑∏∫∞≈≠≤≥±∓×÷∈∉⊂⊃∪∩∀∃→←⇒⇐⇔]', text)
    # Ce n'est pas forcément un problème, mais mixer Unicode et LaTeX est suspect
    if suspect_chars and '$' in text:
        issues.append(("UNICODE_MIX", f"Mix Unicode math + LaTeX $ — rendu potentiellement incohérent: {''.join(set(suspect_chars))}"))

    # ── 6. Backslash isolé (typo courante) ──
    if re.search(r'(?<!\$)\\\s+', outside):
        issues.append(("BACKSLASH_ISOLE", "Backslash suivi d'espace hors LaTeX — probablement une typo"))

    return issues


# ══════════════════════════════════════════════════════════════
# AUDIT
# ══════════════════════════════════════════════════════════════

def audit_all():
    total_exos = 0
    total_issues = 0
    results = []  # (severity, location, issue_type, detail)

    # ── Exercices ──
    for onglet in ONGLETS_EXOS:
        print(f"\n📥 Chargement {onglet}…")
        try:
            rows = sh.read(onglet)
        except Exception as e:
            print(f"  ❌ Erreur lecture : {e}")
            continue

        print(f"  → {len(rows)} lignes")

        for row in rows:
            niveau = row.get("Niveau", "?")
            cat = row.get("Categorie", row.get("Chapitre", "?"))
            exos_json = row.get("ExosJSON", "")
            if not exos_json:
                continue

            try:
                exos = json.loads(exos_json)
            except json.JSONDecodeError as e:
                results.append(("🔴", f"[{onglet}] {niveau}/{cat}", "JSON_INVALIDE", str(e)))
                continue

            if not isinstance(exos, list):
                exos = [exos]

            for i, exo in enumerate(exos):
                total_exos += 1
                loc = f"[{onglet}] {niveau}/{cat} exo#{i+1}"

                # Champs à vérifier
                fields = {
                    "q": exo.get("q", ""),
                    "a": str(exo.get("a", "")),
                    "f": exo.get("f", ""),
                }
                # Options
                opts = exo.get("options", [])
                if isinstance(opts, list):
                    for j, o in enumerate(opts):
                        fields[f"options[{j}]"] = str(o)
                # Steps (indices)
                steps = exo.get("steps", [])
                if isinstance(steps, list):
                    for j, s in enumerate(steps):
                        fields[f"steps[{j}]"] = str(s)

                for field_name, field_val in fields.items():
                    issues = find_latex_issues(field_val)
                    for issue_type, detail in issues:
                        sev = "🔴" if issue_type in ("DOLLAR_IMPAIR", "ACCOLADES", "FRAC_SANS_ACCOLADE", "LATEX_HORS_DOLLAR", "JSON_INVALIDE") else "🟡"
                        results.append((sev, f"{loc} [{field_name}]", issue_type, detail))
                        total_issues += 1

    # ── Cours ──
    print(f"\n📥 Chargement Cours…")
    try:
        cours_rows = sh.read("Cours")
        print(f"  → {len(cours_rows)} lignes")
        for row in cours_rows:
            niveau = row.get("Niveau", "?")
            cat = row.get("Categorie", "?")
            for col in ["Section1", "Section2", "Section3", "Section4"]:
                val = row.get(col, "")
                if val:
                    issues = find_latex_issues(val)
                    for issue_type, detail in issues:
                        loc = f"[Cours] {niveau}/{cat} [{col}]"
                        sev = "🔴" if issue_type in ("DOLLAR_IMPAIR", "ACCOLADES", "FRAC_SANS_ACCOLADE", "LATEX_HORS_DOLLAR") else "🟡"
                        results.append((sev, loc, issue_type, detail))
                        total_issues += 1
    except Exception as e:
        print(f"  ❌ Erreur lecture Cours : {e}")

    # ── Formules de référence dans audit_exos.py ──
    # (déjà hardcodées, pas besoin de les re-scanner)

    # ══════════════════════════════════════════════════════════════
    # RAPPORT
    # ══════════════════════════════════════════════════════════════

    print("\n" + "═" * 70)
    print(f"  AUDIT LATEX — {total_exos} exercices scannés")
    print("═" * 70)

    if not results:
        print("\n✅ Aucun problème LaTeX détecté !")
        return

    # Trier : 🔴 d'abord, puis 🟡
    results.sort(key=lambda r: (0 if r[0] == "🔴" else 1, r[2], r[1]))

    # Stats par type
    from collections import Counter
    type_counts = Counter(r[2] for r in results)

    print(f"\n📊 {total_issues} problèmes détectés :\n")
    for t, c in type_counts.most_common():
        print(f"  {c:4d} × {t}")

    print(f"\n{'─' * 70}")
    print(f"{'SEV':4} {'TYPE':30} LOCATION")
    print(f"{'─' * 70}")

    for sev, loc, issue_type, detail in results:
        print(f"{sev:4} {issue_type:30} {loc}")
        # Truncate detail for readability
        if len(detail) > 120:
            detail = detail[:120] + "…"
        print(f"     → {detail}")

    # Résumé
    critiques = sum(1 for r in results if r[0] == "🔴")
    warnings = sum(1 for r in results if r[0] == "🟡")
    print(f"\n{'═' * 70}")
    print(f"  🔴 {critiques} critiques  |  🟡 {warnings} warnings  |  {total_exos} exos scannés")
    print("═" * 70)


if __name__ == "__main__":
    audit_all()
