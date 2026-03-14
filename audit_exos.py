#!/usr/bin/env python3
"""
audit_exos.py — Audit et correction des exercices collège (6EME-3EME)
Onglets : Curriculum_Officiel, DiagnosticExos, BoostExos

Usage : python3 audit_exos.py
"""

import json, re, sys, math
from datetime import date
from fractions import Fraction
from sheets import sh

# ══════════════════════════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════════════════════════

NIVEAUX = {"6EME", "5EME", "4EME", "3EME"}

ONGLETS = {
    "Curriculum_Officiel": {"exos_col": "ExosJSON", "expected_count": 20},
    "DiagnosticExos":      {"exos_col": "ExosJSON", "expected_count": None},
    "BoostExos":           {"exos_col": "ExosJSON", "expected_count": 10},
}

FORMULES_REF = {
    # 6EME
    "Nombres_entiers": "Priorité des opérations : parenthèses d'abord, puis $\\times$ et $\\div$, enfin $+$ et $-$.",
    "Fractions": "Pour additionner des fractions : même dénominateur requis. $\\frac{a}{b} + \\frac{c}{b} = \\frac{a+c}{b}$",
    "Proportionnalité": "Règle de trois : $\\frac{a}{b} = \\frac{c}{d} \\Rightarrow a \\times d = b \\times c$",
    "Géométrie": "Propriétés des triangles, quadrilatères, parallèles et perpendiculaires.",
    "Périmètres_Aires": "Aire rectangle = $L \\times l$. Périmètre = $2(L+l)$. Aire triangle = $\\frac{b \\times h}{2}$.",
    "Angles": "Angles complémentaires : somme = $90°$. Angles supplémentaires : somme = $180°$.",
    "Nombres_Décimaux": "Placer la virgule correctement lors des opérations sur les décimaux.",
    "Statistiques_6ème": "Moyenne = somme des valeurs $\\div$ nombre de valeurs.",
    "Symétrie_Axiale": "Le symétrique d'un point par rapport à un axe est à la même distance de l'axe, de l'autre côté.",
    "Volumes": "Volume pavé droit = $L \\times l \\times h$. Volume cube = $c^3$.",
    "Agrandissement_Réduction": "Dans un agrandissement/réduction de rapport $k$ : longueurs $\\times k$, aires $\\times k^2$, volumes $\\times k^3$.",
    "Conversions_Unités": "Pour convertir les unités de longueur : km → hm → dam → m → dm → cm → mm ($\\times 10$ à chaque étape).",
    "Puissances_10": "$10^n$ s'écrit avec un 1 suivi de $n$ zéros. $10^{-n} = \\frac{1}{10^n}$.",
    # 5EME
    "Nombres_relatifs": "Règle des signes : $(-) \\times (-) = (+)$, $(-) \\times (+) = (-)$.",
    "Calcul_Littéral": "Distributivité : $a(b+c) = ab + ac$. Factorisation : opération inverse.",
    "Pythagore": "Théorème de Pythagore : $c^2 = a^2 + b^2$ (c = hypoténuse, le plus grand côté).",
    "Puissances": "$a^m \\times a^n = a^{m+n}$ — $\\frac{a^m}{a^n} = a^{m-n}$ — $(a^m)^n = a^{m \\times n}$",
    "Symétrie_Centrale": "Le symétrique de $A$ par rapport au centre $O$ est le point $A'$ tel que $O$ est le milieu de $[AA']$.",
    "Transformations": "Translation : on décale tous les points de la même direction, même distance. Rotation : on tourne autour d'un centre.",
    "Racines_Carrées": "$\\sqrt{a \\times b} = \\sqrt{a} \\times \\sqrt{b}$ — $\\sqrt{a^2} = |a|$",
    "Triangles_Semblables": "Deux triangles sont semblables si leurs angles sont égaux deux à deux. Les côtés sont proportionnels.",
    # 4EME
    "Équations": "Pour résoudre $ax + b = c$ : isoler $x = \\frac{c-b}{a}$.",
    "Fonctions_Linéaires": "Fonction linéaire : $f(x) = ax$. $a$ = coefficient directeur = $\\frac{f(x)}{x}$.",
    "Inéquations": "Résoudre une inéquation comme une équation, mais attention : on inverse le sens si on multiplie ou divise par un nombre négatif.",
    "Homothétie": "Homothétie de centre $O$ et rapport $k$ : $OM' = k \\times OM$. Si $k > 0$ même côté, si $k < 0$ côté opposé.",
    "Sections_Solides": "Section d'un cube par un plan : triangle, rectangle, ou hexagone selon l'inclinaison du plan.",
    # 3EME
    "Fonctions": "Une fonction associe à chaque $x$ une unique image $f(x)$. $f(x) = 0$ donne les antécédents de 0.",
    "Théorème_de_Thalès": "Si $(BC) \\parallel (DE)$ : $\\frac{AB}{AD} = \\frac{AC}{AE} = \\frac{BC}{DE}$",
    "Trigonométrie": "$\\cos(\\hat{A}) = \\frac{\\text{adj}}{\\text{hyp}}$ — $\\sin(\\hat{A}) = \\frac{\\text{opp}}{\\text{hyp}}$ — $\\tan(\\hat{A}) = \\frac{\\text{opp}}{\\text{adj}}$",
    "Statistiques": "Moyenne = somme des valeurs $\\div$ effectif total. Médiane = valeur qui partage la série en deux groupes égaux.",
    "Probabilités": "$P(A) = \\frac{\\text{cas favorables}}{\\text{cas possibles}}$. $0 \\leq P(A) \\leq 1$.",
    "Systèmes_Équations": "Méthode par substitution ou combinaison pour résoudre $\\begin{cases} ax+by=c \\\\ dx+ey=f \\end{cases}$",
    "Notation_Scientifique": "Écriture scientifique : $a \\times 10^n$ avec $1 \\leq a < 10$.",
}


# ══════════════════════════════════════════════════════════════
# NORMALISATION & COMPARAISON
# ══════════════════════════════════════════════════════════════

def normalize(s):
    """Normalise une chaîne pour comparaison : strip, supprime $, espaces autour opérateurs."""
    if s is None:
        return ""
    s = str(s).strip()
    s = s.replace("$", "")
    s = re.sub(r'\s*([+\-=×÷·])\s*', r'\1', s)
    s = s.strip()
    return s


def latex_to_plain(s):
    """Tente de convertir du LaTeX simple en texte plat pour comparaison."""
    s = normalize(s)
    # \frac{a}{b} → a/b
    s = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'\1/\2', s)
    # \text{...} → contenu
    s = re.sub(r'\\text\{([^}]+)\}', r'\1', s)
    # \times → ×
    s = s.replace('\\times', '×')
    # \div → ÷
    s = s.replace('\\div', '÷')
    # \sqrt{x} → sqrt(x)
    s = re.sub(r'\\sqrt\{([^}]+)\}', r'sqrt(\1)', s)
    # ^{n} → ^n
    s = re.sub(r'\^\{([^}]+)\}', r'^\1', s)
    # supprimer \ restants (ex: \, \;)
    s = re.sub(r'\\[,;!]', '', s)
    s = re.sub(r'\\([a-zA-Z]+)', r'\1', s)
    s = s.strip()
    return s


def compare_answers(a, b):
    """Compare deux réponses avec normalisation progressive."""
    if normalize(a) == normalize(b):
        return True
    if latex_to_plain(a) == latex_to_plain(b):
        return True
    # Comparaison numérique
    try:
        va = eval_numeric(a)
        vb = eval_numeric(b)
        if va is not None and vb is not None and abs(va - vb) < 1e-9:
            return True
    except:
        pass
    return False


def eval_numeric(s):
    """Tente d'évaluer une chaîne comme nombre (fraction, décimal, etc.)."""
    s = latex_to_plain(s).replace('×', '*').replace('÷', '/').replace(',', '.')
    s = s.replace(' ', '')
    try:
        return float(Fraction(s))
    except:
        pass
    try:
        return float(s)
    except:
        pass
    return None


# ══════════════════════════════════════════════════════════════
# CALCUL AUTOMATIQUE
# ══════════════════════════════════════════════════════════════

def try_compute(q, a_given):
    """
    Tente de recalculer la réponse depuis l'énoncé.
    CONSERVATEUR : ne flag que quand la question est clairement un calcul direct
    (commence par "Calcule", "Simplifie", "Effectue", etc.) ET que le résultat
    est sans ambiguïté.
    Retourne (True, valeur_calculée) si un calcul a pu être fait et diffère de a_given.
    Retourne (False, None) si non calculable ou correct.
    """
    q_clean = latex_to_plain(q).lower().strip()
    a_str = str(a_given).strip()

    # Ignorer les questions Vrai/Faux, conceptuelles, "Complète", "Où est l'erreur"
    if a_str.lower() in ("vrai", "faux", "true", "false"):
        return False, None
    skip_patterns = [
        r'vrai\s+(ou|/)\s+faux', r'complète', r'compl[eé]ter', r'erreur',
        r'quelle?\s+(est|sont)', r'quel\s+nombre', r'parmi\s+les',
        r'laquelle', r'lequel', r'ordre\s+croissant', r'comparer',
        r'arrondi', r'encadr', r'(dé)?compos', r'classe',
        r'convertir', r'transformer', r'exprimer', r'not(ation|er)',
        r'parallèle', r'perpendiculaire', r'symétri', r'section',
        r'probabilité', r'statistique', r'médiane', r'moyenne',
        r'lecture', r'graphique', r'tableau', r'image', r'antécédent',
        r'fonction', r'coefficient', r'représent', r'proportion',
    ]
    for pat in skip_patterns:
        if re.search(pat, q_clean):
            return False, None

    # Ne tenter le calcul que si la question commence par un verbe de calcul
    calcul_verbs = [r'^calcule', r'^effectue', r'^simplifie', r'^résou', r'^détermine.*valeur']
    is_calcul = any(re.search(v, q_clean) for v in calcul_verbs)
    if not is_calcul:
        return False, None

    # ── Fractions : expression simple a/b OP c/d (exactement 2 termes, pas 3+) ──
    frac_matches = re.findall(r'(\d+)/(\d+)', q_clean)
    frac_ops = re.findall(r'(\d+)/(\d+)\s*([+\-×\*÷])\s*(\d+)/(\d+)', q_clean)
    # Seulement si EXACTEMENT une opération entre 2 fractions (pas de 3e terme)
    if len(frac_ops) == 1 and len(frac_matches) == 2:
        m = frac_ops[0]
        n1, d1, op, n2, d2 = int(m[0]), int(m[1]), m[2], int(m[3]), int(m[4])
        f1, f2 = Fraction(n1, d1), Fraction(n2, d2)
        if op in ('+',):
            result = f1 + f2
        elif op in ('-',):
            result = f1 - f2
        elif op in ('×', '*'):
            result = f1 * f2
        elif op in ('÷',):
            result = f1 / f2 if f2 != 0 else None
        else:
            result = None
        if result is not None:
            expected = f"$\\frac{{{result.numerator}}}{{{result.denominator}}}$" if result.denominator != 1 else str(result.numerator)
            if not compare_answers(a_str, str(result.numerator) + "/" + str(result.denominator)) and \
               not compare_answers(a_str, str(float(result))) and \
               not compare_answers(a_str, expected):
                return True, f"{result.numerator}/{result.denominator}"
        return False, None

    # ── Pourcentages : X% de Y ──
    m = re.search(r'(\d+(?:[.,]\d+)?)\s*%\s*(?:de|of)\s*(\d+(?:[.,]\d+)?)', q_clean)
    if m:
        pct = float(m.group(1).replace(',', '.'))
        val = float(m.group(2).replace(',', '.'))
        result = pct * val / 100
        r_str = str(int(result)) if result == int(result) else str(result)
        if not compare_answers(a_str, r_str):
            return True, r_str
        return False, None

    # ── Puissances simples (seulement "Calcule X^Y" sans division ni notation scientifique) ──
    if re.search(r'\\frac|10\^|×\s*10', q_clean):
        return False, None  # fractions de puissances ou notation scientifique → trop complexe
    m = re.match(r'^(?:calcule|effectue)\s+.*?(\d+)\s*\^\s*(\d+)\s*\.?$', q_clean)
    if m:
        base, exp = int(m.group(1)), int(m.group(2))
        if exp <= 10:
            result = base ** exp
            if not compare_answers(a_str, str(result)):
                return True, str(result)
        return False, None

    return False, None


# ══════════════════════════════════════════════════════════════
# VÉRIFICATIONS PAR EXERCICE
# ══════════════════════════════════════════════════════════════

def audit_exercice(exo, niveau, categorie, exo_idx, onglet):
    """Vérifie un exercice et retourne une liste d'erreurs."""
    errors = []
    loc = f"[{onglet}] {niveau}/{categorie} exo#{exo_idx+1}"

    # CHECK A — Champs obligatoires
    if not exo.get("q", "").strip():
        errors.append(("ERREUR_CHAMP_MANQUANT", loc, "q manquant", "", ""))
    a_val = exo.get("a", "")
    if not str(a_val).strip():
        errors.append(("ERREUR_CHAMP_MANQUANT", loc, "a manquant", "", ""))
    options = exo.get("options")
    if not isinstance(options, list):
        errors.append(("ERREUR_CHAMP_MANQUANT", loc, "options n'est pas une liste", str(type(options)), "list"))
        options = []
    elif len(options) < 2 or len(options) > 4:
        errors.append(("ERREUR_CHAMP_MANQUANT", loc, f"options a {len(options)} éléments (attendu 2-4)", str(len(options)), "2-4"))
    f_val = exo.get("f", "")
    if not str(f_val).strip():
        errors.append(("WARN_FORMULE_VIDE", loc, "f vide", "", ""))
    steps = exo.get("steps")
    if not isinstance(steps, list):
        errors.append(("ERREUR_CHAMP_MANQUANT", loc, "steps n'est pas une liste", str(type(steps)), "list"))
    elif len(steps) < 1 or len(steps) > 3:
        errors.append(("WARN_STEPS", loc, f"steps a {len(steps)} éléments (attendu 1-3)", str(len(steps)), "1-3"))
    lvl = exo.get("lvl")
    if lvl not in (1, 2):
        errors.append(("ERREUR_CHAMP_MANQUANT", loc, f"lvl={lvl} (attendu 1 ou 2)", str(lvl), "1 ou 2"))

    if not str(a_val).strip() or not isinstance(options, list) or len(options) == 0:
        return errors  # pas la peine de continuer

    # CHECK B — Réponse dans les options
    a_str = str(a_val).strip()
    found = any(compare_answers(a_str, str(opt)) for opt in options)
    if not found:
        opts_display = " | ".join(str(o) for o in options)
        errors.append(("ERREUR_REPONSE_ABSENTE", loc, f'a="{a_str}" absent des options', a_str, opts_display))

    # CHECK C — Calcul automatique
    q_val = exo.get("q", "")
    is_wrong, expected = try_compute(q_val, a_val)
    if is_wrong:
        errors.append(("ERREUR_CALCUL", loc, f'calcul auto → {expected}', a_str, expected))

    # CHECK D — Options doublons
    if isinstance(options, list) and len(options) >= 2:
        normed = [normalize(str(o)) for o in options]
        for i in range(len(normed)):
            for j in range(i+1, len(normed)):
                if normed[i] == normed[j] and normed[i]:
                    errors.append(("ERREUR_DOUBLONS_OPTIONS", loc, f'options[{i}] == options[{j}] ("{options[i]}")', str(options[i]), "doublon"))
                    break
        for i, o in enumerate(options):
            if not str(o).strip():
                errors.append(("ERREUR_DOUBLONS_OPTIONS", loc, f"options[{i}] est vide", "", "non vide"))

    # CHECK E — Indice dévoile la réponse
    if isinstance(steps, list):
        for si, step in enumerate(steps):
            if normalize(str(step)) == normalize(a_str):
                errors.append(("WARN_INDICE_DEVOILE", loc, f'steps[{si}] contient la réponse exacte', str(step), ""))

    # CHECK F — Formule vide ou générique
    f_str = str(f_val).strip()
    if f_str and (f_str.lower() in ("formule", "formule clé", "formule-clé") or len(f_str) < 8):
        errors.append(("WARN_FORMULE_VIDE", loc, f'f trop court/générique: "{f_str}"', f_str, "formule détaillée"))

    return errors


# ══════════════════════════════════════════════════════════════
# PHASE 1 + 2 — CHARGEMENT & AUDIT
# ══════════════════════════════════════════════════════════════

def load_and_audit():
    """Charge les onglets et audite tous les exercices collège."""
    all_errors = []
    stats = {}

    for onglet, cfg in ONGLETS.items():
        print(f"\n📥 Chargement {onglet}…")
        try:
            rows = sh.read(onglet)
        except Exception as e:
            print(f"  ❌ Erreur lecture : {e}")
            continue

        college_rows = [r for r in rows if r.get("Niveau", "") in NIVEAUX]
        print(f"  → {len(college_rows)} lignes collège (sur {len(rows)} total)")

        onglet_stats = {
            "total": 0, "ok": 0, "chapitres": 0,
            "ERREUR_REPONSE_ABSENTE": 0, "ERREUR_CALCUL": 0,
            "ERREUR_DOUBLONS_OPTIONS": 0, "ERREUR_CHAMP_MANQUANT": 0,
            "WARN_INDICE_DEVOILE": 0, "WARN_FORMULE_VIDE": 0, "WARN_STEPS": 0,
        }

        for row in college_rows:
            niveau = row.get("Niveau", "")
            categorie = row.get("Categorie", "")
            exos_raw = row.get(cfg["exos_col"], "")
            onglet_stats["chapitres"] += 1

            try:
                exos = json.loads(exos_raw) if exos_raw else []
            except json.JSONDecodeError as e:
                all_errors.append(("ERREUR_JSON", f"[{onglet}] {niveau}/{categorie}", f"JSON invalide: {e}", "", ""))
                continue

            if not isinstance(exos, list):
                all_errors.append(("ERREUR_JSON", f"[{onglet}] {niveau}/{categorie}", "ExosJSON n'est pas un tableau", "", ""))
                continue

            for i, exo in enumerate(exos):
                onglet_stats["total"] += 1
                errs = audit_exercice(exo, niveau, categorie, i, onglet)
                if errs:
                    all_errors.extend(errs)
                    for e in errs:
                        etype = e[0]
                        if etype in onglet_stats:
                            onglet_stats[etype] += 1
                else:
                    onglet_stats["ok"] += 1

        stats[onglet] = onglet_stats

    return all_errors, stats


# ══════════════════════════════════════════════════════════════
# PHASE 3 — RAPPORT
# ══════════════════════════════════════════════════════════════

def print_report(all_errors, stats):
    """Affiche le rapport d'audit dans le terminal."""
    print("\n" + "═" * 60)
    print("  AUDIT EXERCICES COLLÈGE — Matheux")
    print("═" * 60)

    critiques = 0
    warnings = 0

    for onglet, s in stats.items():
        print(f"\n📋 {onglet}")
        print(f"   Exercices analysés : {s['total']} ({s['chapitres']} chapitres)")
        print(f"   ✅ Sans erreur      : {s['ok']}")
        for etype, label, is_crit in [
            ("ERREUR_REPONSE_ABSENTE", "ERREUR_REPONSE_ABSENTE", True),
            ("ERREUR_CALCUL", "ERREUR_CALCUL", True),
            ("ERREUR_DOUBLONS_OPTIONS", "ERREUR_DOUBLONS_OPTIONS", True),
            ("ERREUR_CHAMP_MANQUANT", "ERREUR_CHAMP_MANQUANT", True),
            ("WARN_INDICE_DEVOILE", "WARN_INDICE_DEVOILE", False),
            ("WARN_FORMULE_VIDE", "WARN_FORMULE_VIDE", False),
            ("WARN_STEPS", "WARN_STEPS", False),
        ]:
            count = s.get(etype, 0)
            if count > 0:
                icon = "❌" if is_crit else "⚠️ "
                suffix = " ← CRITIQUE" if is_crit else ""
                print(f"   {icon} {label:30s}: {count}{suffix}")
                if is_crit:
                    critiques += count
                else:
                    warnings += count

    # Top erreurs critiques
    crit_errors = [e for e in all_errors if e[0].startswith("ERREUR")]
    if crit_errors:
        print(f"\n{'─' * 60}")
        print(f"TOP {min(20, len(crit_errors))} ERREURS CRITIQUES :")
        print(f"{'─' * 60}")
        for e in crit_errors[:20]:
            etype, loc, desc, found, expected = e
            print(f"  {loc}")
            print(f"    {etype}: {desc}")
            if found and expected:
                print(f"    trouvé: {found} | attendu: {expected}")

    print(f"\n{'═' * 60}")
    print(f"  TOTAL : {critiques} erreurs critiques, {warnings} warnings")
    print(f"{'═' * 60}")

    return critiques, warnings


def save_report(all_errors, stats, critiques, warnings):
    """Sauvegarde le rapport complet dans docs/."""
    today_str = date.today().isoformat()
    filename = f"docs/audit-exos-{today_str}.md"

    lines = [
        f"# Audit exercices collège — {today_str}",
        "",
        "## Résumé",
        "",
    ]

    for onglet, s in stats.items():
        lines.append(f"### {onglet}")
        lines.append(f"- Exercices analysés : {s['total']} ({s['chapitres']} chapitres)")
        lines.append(f"- Sans erreur : {s['ok']}")
        for etype in ["ERREUR_REPONSE_ABSENTE", "ERREUR_CALCUL", "ERREUR_DOUBLONS_OPTIONS",
                       "ERREUR_CHAMP_MANQUANT", "WARN_INDICE_DEVOILE", "WARN_FORMULE_VIDE", "WARN_STEPS"]:
            count = s.get(etype, 0)
            if count > 0:
                lines.append(f"- {etype} : {count}")
        lines.append("")

    lines.append(f"**Total : {critiques} erreurs critiques, {warnings} warnings**")
    lines.append("")

    # Détail par type
    if all_errors:
        lines.append("## Détail des erreurs")
        lines.append("")

        # Grouper par onglet/niveau/chapitre
        grouped = {}
        for e in all_errors:
            etype, loc, desc, found, expected = e
            if loc not in grouped:
                grouped[loc] = []
            grouped[loc].append((etype, desc, found, expected))

        for loc in sorted(grouped.keys()):
            lines.append(f"### {loc}")
            for etype, desc, found, expected in grouped[loc]:
                icon = "CRITIQUE" if etype.startswith("ERREUR") else "WARNING"
                lines.append(f"- **{icon}** `{etype}` : {desc}")
                if found and expected:
                    lines.append(f"  - trouvé : `{found}`")
                    lines.append(f"  - attendu : `{expected}`")
            lines.append("")

    with open(filename, "w") as f:
        f.write("\n".join(lines))
    print(f"\n📄 Rapport sauvegardé : {filename}")
    return filename


# ══════════════════════════════════════════════════════════════
# PHASE 4 — CORRECTION AUTOMATIQUE
# ══════════════════════════════════════════════════════════════

def apply_corrections(all_errors):
    """Applique les corrections automatiques sur les exercices."""
    # Organiser les erreurs par onglet/ligne pour modification batch
    corrections_by_onglet = {}  # onglet → { (niveau, categorie) → [ (exo_idx, corrections) ] }

    for e in all_errors:
        etype, loc, desc, found, expected = e

        # Parser le loc : [Onglet] NIVEAU/CATEGORIE exo#N
        m = re.match(r'\[([^\]]+)\]\s+(\w+)/(\S+)\s+exo#(\d+)', loc)
        if not m:
            continue
        onglet, niveau, categorie, exo_num = m.group(1), m.group(2), m.group(3), int(m.group(4)) - 1

        if onglet not in corrections_by_onglet:
            corrections_by_onglet[onglet] = {}
        key = (niveau, categorie)
        if key not in corrections_by_onglet[onglet]:
            corrections_by_onglet[onglet][key] = {}
        if exo_num not in corrections_by_onglet[onglet][key]:
            corrections_by_onglet[onglet][key][exo_num] = []
        corrections_by_onglet[onglet][key][exo_num].append((etype, desc, found, expected))

    total_fixed = 0
    manual_list = []

    for onglet, chapters in corrections_by_onglet.items():
        cfg = ONGLETS[onglet]
        print(f"\n🔧 Correction {onglet}…")

        try:
            raw = sh.read_raw(onglet)
        except Exception as e:
            print(f"  ❌ Erreur lecture raw : {e}")
            continue

        if len(raw) < 2:
            continue

        headers = raw[0]
        exos_col_idx = None
        niv_col_idx = None
        cat_col_idx = None

        for i, h in enumerate(headers):
            if h == cfg["exos_col"]:
                exos_col_idx = i
            if h == "Niveau":
                niv_col_idx = i
            if h == "Categorie":
                cat_col_idx = i

        if exos_col_idx is None:
            print(f"  ❌ Colonne {cfg['exos_col']} introuvable")
            continue

        modified_rows = set()

        for row_idx in range(1, len(raw)):
            row = raw[row_idx]
            if niv_col_idx is None or cat_col_idx is None:
                continue
            if row_idx >= len(raw):
                continue
            niv = row[niv_col_idx] if niv_col_idx < len(row) else ""
            cat = row[cat_col_idx] if cat_col_idx < len(row) else ""

            if niv not in NIVEAUX:
                continue

            key = (niv, cat)
            if key not in chapters:
                continue

            exos_json = row[exos_col_idx] if exos_col_idx < len(row) else ""
            try:
                exos = json.loads(exos_json) if exos_json else []
            except:
                continue

            changed = False
            for exo_idx, correction_list in chapters[key].items():
                if exo_idx >= len(exos):
                    continue
                exo = exos[exo_idx]

                for etype, desc, found, expected in correction_list:

                    if etype == "ERREUR_REPONSE_ABSENTE":
                        # Mettre a dans options[0]
                        a_val = str(exo.get("a", "")).strip()
                        if a_val and isinstance(exo.get("options"), list) and len(exo["options"]) >= 1:
                            exo["options"][0] = a_val
                            changed = True
                            total_fixed += 1
                            print(f"  ✅ {niv}/{cat} exo#{exo_idx+1}: a mis dans options[0]")

                    elif etype == "ERREUR_CALCUL":
                        # Correction auto seulement si expected est disponible
                        if expected:
                            manual_list.append(f"{onglet} {niv}/{cat} exo#{exo_idx+1}: calcul auto suggère '{expected}' mais réponse actuelle '{found}' — vérification manuelle recommandée")

                    elif etype == "ERREUR_DOUBLONS_OPTIONS":
                        if isinstance(exo.get("options"), list):
                            normed = [normalize(str(o)) for o in exo["options"]]
                            seen = set()
                            for oi in range(len(exo["options"])):
                                if normed[oi] in seen:
                                    # Remplacer le doublon par une variante
                                    orig = str(exo["options"][oi])
                                    replacement = _generate_distractor(exo, oi)
                                    if replacement:
                                        exo["options"][oi] = replacement
                                        changed = True
                                        total_fixed += 1
                                        print(f"  ✅ {niv}/{cat} exo#{exo_idx+1}: doublon options[{oi}] remplacé '{orig}' → '{replacement}'")
                                else:
                                    seen.add(normed[oi])

                    elif etype == "WARN_FORMULE_VIDE":
                        # Remplacer par la formule de référence du chapitre
                        ref = FORMULES_REF.get(cat)
                        if ref:
                            exo["f"] = ref
                            changed = True
                            total_fixed += 1
                            print(f"  ✅ {niv}/{cat} exo#{exo_idx+1}: formule remplacée par référence")

            if changed:
                modified_rows.add(row_idx)
                # Réécrire le JSON validé
                try:
                    new_json = json.dumps(exos, ensure_ascii=False)
                    json.loads(new_json)  # validation
                    raw[row_idx][exos_col_idx] = new_json
                except Exception as e:
                    print(f"  ❌ {niv}/{cat}: JSON invalide après correction: {e}")

        # Écriture batch si modifications
        if modified_rows:
            print(f"  📤 Écriture {len(modified_rows)} lignes modifiées dans {onglet}…")
            try:
                sh.write_rows(onglet, raw, include_header=False)
            except Exception as e:
                print(f"  ❌ Erreur écriture : {e}")

    return total_fixed, manual_list


def _generate_distractor(exo, dup_idx):
    """Génère un distracteur de remplacement pour un doublon."""
    a_val = str(exo.get("a", ""))
    options = exo.get("options", [])

    # Tenter de modifier numériquement
    num = eval_numeric(a_val)
    if num is not None:
        # Générer des variantes numériques
        candidates = [
            str(int(num + 1)) if num == int(num) else str(round(num + 0.5, 2)),
            str(int(num - 1)) if num == int(num) else str(round(num - 0.5, 2)),
            str(int(num * 2)) if num == int(num) else str(round(num * 2, 2)),
            str(int(num + 3)) if num == int(num) else str(round(num + 1.5, 2)),
        ]
        existing = {normalize(str(o)) for o in options}
        for c in candidates:
            if normalize(c) not in existing and normalize(c) != normalize(a_val):
                return c

    # Fallback : ajouter un suffixe
    return None


# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════

def main():
    print("🔍 AUDIT EXERCICES COLLÈGE — Matheux")
    print("Niveaux : " + ", ".join(sorted(NIVEAUX)))
    print("Onglets : " + ", ".join(ONGLETS.keys()))

    # Phase 1+2 : Chargement & audit
    all_errors, stats = load_and_audit()

    # Phase 3 : Rapport
    critiques, warnings = print_report(all_errors, stats)
    report_file = save_report(all_errors, stats, critiques, warnings)

    if critiques == 0 and warnings == 0:
        print("\n🎉 Aucune erreur détectée ! Les exercices sont 100% propres.")
        return

    # Demander confirmation pour correction
    print(f"\n{'═' * 60}")
    print(f"  {critiques} erreurs critiques, {warnings} warnings détectés.")
    print(f"  Lancer la correction automatique ? (oui/non)")
    print(f"{'═' * 60}")

    response = input("\n> ").strip().lower()
    if response not in ("oui", "o", "yes", "y"):
        print("❌ Correction annulée.")
        return

    # Phase 4 : Correction
    total_fixed, manual_list = apply_corrections(all_errors)

    # Phase 5 : Rapport post-correction
    print(f"\n{'═' * 60}")
    print(f"  CORRECTIONS APPLIQUÉES")
    print(f"{'═' * 60}")
    print(f"  Erreurs corrigées auto     : {total_fixed}")
    print(f"  À corriger manuellement    : {len(manual_list)}")
    if manual_list:
        print(f"\n  📋 CORRECTIONS MANUELLES REQUISES :")
        for m in manual_list:
            print(f"    → {m}")
    print(f"  Données 1ERE               : ✅ non touchées")
    print(f"{'═' * 60}")

    # Compléter le rapport
    with open(report_file, "a") as f:
        f.write("\n\n## Corrections appliquées\n\n")
        f.write(f"- Erreurs corrigées automatiquement : {total_fixed}\n")
        f.write(f"- À corriger manuellement : {len(manual_list)}\n")
        if manual_list:
            f.write("\n### Corrections manuelles requises\n\n")
            for m in manual_list:
                f.write(f"- {m}\n")
        f.write(f"\n- Données 1ERE : non touchées\n")
        f.write(f"- Données autres élèves : non touchées\n")
    print(f"\n📄 Rapport complété : {report_file}")

    # Re-audit pour vérifier
    print("\n🔄 Re-vérification post-correction…")
    all_errors2, stats2 = load_and_audit()
    critiques2, warnings2 = print_report(all_errors2, stats2)
    if critiques2 < critiques:
        print(f"\n✅ Amélioration : {critiques} → {critiques2} erreurs critiques")
    elif critiques2 == 0:
        print("\n🎉 100% propre après correction !")


if __name__ == "__main__":
    main()
