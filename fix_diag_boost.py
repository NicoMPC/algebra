#!/usr/bin/env python3
"""
fix_diag_boost.py — MASTERCLASS fix
Lit DiagnosticExos + BoostExos, applique :
  1. Reformulations d'énoncés (clarté)
  2. Ajout de specs `fig` explicites (géométrie)
  3. Fix doublon Systèmes 3EME
  4. Nettoyage LaTeX
"""

import json, re, copy
from sheets import sh

# ──────────────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────────────

def clean_latex(s):
    """Nettoie les problèmes LaTeX courants — NE TOUCHE PAS aux espaces."""
    if not s:
        return s
    # Fix double backslash en simple
    s = s.replace('\\\\frac', '\\frac').replace('\\\\sqrt', '\\sqrt')
    # Fix $...$ vides
    s = s.replace('$$', '')
    return s

def clean_exo(exo):
    """Nettoie le LaTeX dans tous les champs texte d'un exo."""
    for field in ['q', 'a', 'f']:
        if field in exo and isinstance(exo[field], str):
            exo[field] = clean_latex(exo[field])
    if 'options' in exo:
        exo['options'] = [clean_latex(o) if isinstance(o, str) else o for o in exo['options']]
    if 'steps' in exo:
        exo['steps'] = [clean_latex(s) if isinstance(s, str) else s for s in exo['steps']]
    return exo


# ──────────────────────────────────────────────────────────────────────
# REFORMULATIONS
# ──────────────────────────────────────────────────────────────────────

REFORMULATIONS = {
    # ── 3EME Thalès : contextualiser ──
    ("3EME", "Thales", "diag", 0): {
        "q": "Dans le triangle ABC, le point M est sur le segment [AB] et le point N est sur le segment [AC], avec (MN) parallèle à (BC). On donne AM = 4, MB = 2 et MN = 6. Calculer BC."
    },
    ("3EME", "Thales", "diag", 1): {
        "q": "Dans le triangle ABC, E est sur [AB] et D est sur [AC]. On donne AE = 3, AB = 9, AD = 2 et AC = 6. Les droites (ED) et (BC) sont-elles parallèles ?"
    },
    # ── 3EME Trigonométrie : rapporter à un angle + nommer le triangle ──
    # On fera un pattern matching plus bas pour tous les exos trigo

    # ── 6EME Symétrie axiale : clarifier le vocabulaire ──
    # Pattern matching plus bas

    # ── 6EME Angles Diag #2 : reformuler ──
    ("6EME", "Angles", "diag", 1): {
        "q": "Si un angle $\\alpha$ a un complémentaire de 30°, que vaut $180° - \\alpha$ (son supplémentaire) ?"
    },

    # ── 6EME Périmètres Boost #8 : clarifier demi-cercle ──
    ("6EME", "Perimetres_Aires", "boost", 7): {
        "q": "Calcule le périmètre complet d'un demi-disque (demi-cercle + diamètre) de diamètre 10 cm."
    },

    # ── 6EME Volumes Boost #3 : clarifier ──
    ("6EME", "Volumes", "boost", 2): {
        "q": "Un prisme droit a une aire de base de 20 cm² et une hauteur de 7 cm. Quel est son volume ?"
    },
}


# ──────────────────────────────────────────────────────────────────────
# PATTERN-BASED REFORMULATIONS
# ──────────────────────────────────────────────────────────────────────

def reformulate_trigo(q):
    """Reformule les exos trigo qui ne précisent pas l'angle."""
    # Pattern : "Côté opposé = X, adjacent = Y" sans préciser l'angle
    if re.search(r'(côté\s+)?opposé\s*=?\s*\d', q, re.I) and re.search(r'adjacent\s*=?\s*\d', q, re.I):
        if 'triangle rectangle' not in q.lower() and 'angle' not in q.lower():
            q = "Dans un triangle rectangle, " + q[0].lower() + q[1:]
        if "l'angle" not in q.lower() and "α" not in q and "\\hat" not in q:
            q = q.rstrip('.?! ') + " (par rapport à l'un des angles aigus)."

    # Pattern : "Hypoténuse X, angle Y°. Côté opposé/adjacent ?"
    m = re.search(r'hypoténuse\s*=?\s*(\d+).*angle\s*(\d+)°.*côté\s+(opposé|adjacent)', q, re.I)
    if m and 'triangle rectangle' not in q.lower():
        q = "Dans un triangle rectangle, l'" + q[0].lower() + q[1:]

    # Pattern : "Adjacent = X, hypoténuse = Y. cos(α) = ?"
    if re.search(r'adjacent\s*=\s*\d', q, re.I) and 'triangle rectangle' not in q.lower():
        q = "Dans un triangle rectangle, " + q[0].lower() + q[1:]

    return q


def reformulate_sym_axiale(q):
    """Clarifie le vocabulaire des axes pour les 6èmes."""
    q = re.sub(r"l'axe des ordonnées(?!\s*\()", "l'axe vertical (axe des ordonnées)", q)
    q = re.sub(r"l'axe des abscisses(?!\s*\()", "l'axe horizontal (axe des abscisses)", q)
    return q


def reformulate_thales(q, cat):
    """Contextualise les exos Thalès sans config."""
    if 'thales' not in cat.lower() and 'thalès' not in cat.lower():
        return q
    # Si l'énoncé commence directement par "AB=..." sans intro
    if re.match(r'^[A-Z]{2}\s*=\s*\d', q):
        q = "Dans le triangle ABC, le point M est sur [AB] et N sur [AC], avec (MN) parallèle à (BC). " + q
    # Si "(MN)∥(BC)" sans contexte
    if '∥' in q or 'parallèle' in q.lower():
        if 'triangle' not in q.lower() and 'segment' not in q.lower():
            q = "Dans le triangle ABC, M est sur [AB] et N est sur [AC]. " + q
    return q


def reformulate_sections(q):
    """Précise 'depuis le sommet' pour les sections de solides."""
    # "au tiers de la hauteur" → "au tiers de la hauteur en partant du sommet"
    q = re.sub(r'au tiers de la hauteur(?!\s+en)', 'au tiers de la hauteur en partant du sommet', q)
    q = re.sub(r'à mi-hauteur(?!\s+en|\s+depuis)', 'à mi-hauteur en partant du sommet', q)
    q = re.sub(r'à (\d+) cm du sommet', r'à \1 cm du sommet (en partant du sommet)', q)
    # "rapport k=3/4 depuis le sommet" → clarifier
    q = re.sub(r'rapport\s+k\s*=\s*(\d+/\d+)\s+depuis\s+(?:le\s+)?sommet',
               r'coupée aux \1 de la hauteur en partant du sommet', q)
    return q


# ──────────────────────────────────────────────────────────────────────
# FIGURE SPECS
# ──────────────────────────────────────────────────────────────────────

def make_fig(fig_type, **kwargs):
    """Crée une spec fig."""
    fig = {"type": fig_type, "confidence": "high"}
    fig.update(kwargs)
    return fig


def detect_and_add_fig(exo, niveau, cat):
    """Ajoute un champ fig explicite si l'exo en a besoin."""
    q = exo.get('q', '').lower()

    # Skip si fig déjà présent
    if 'fig' in exo and exo['fig']:
        return exo

    # ── THALÈS (toujours figure sauf calcul pur) ──
    if 'thalès' in cat.lower() or 'thales' in cat.lower():
        if 'agrandissement' in q or 'coefficient' in q or 'k=' in q:
            return exo  # calcul pur
        nums = re.findall(r'\d+(?:[.,]\d+)?', q)
        n = [float(x.replace(',', '.')) for x in nums] if nums else []
        pts = re.findall(r'\b([A-Z])\b', exo.get('q', ''))
        pts = [p for p in pts if p not in ('I', 'J', 'L', 'O', 'V', 'F')]
        pts = list(dict.fromkeys(pts))  # dedupe

        # Exo type "ombre" → similar_tri
        if 'ombre' in q:
            exo['fig'] = make_fig('similar_tri',
                a=n[0] if len(n) > 0 else 6,
                b=n[1] if len(n) > 1 else 4,
                c=n[2] if len(n) > 2 else 10,
                pts=pts[:6] if pts else ['A', 'B', 'C'])
            return exo

        exo['fig'] = make_fig('thales',
            a=n[0] if len(n) > 0 else 4,
            b=n[1] if len(n) > 1 else 6,
            c=n[2] if len(n) > 2 else 3,
            d=n[3] if len(n) > 3 else None,
            pts=pts[:4] if pts else ['A', 'B', 'M', 'N'])
        return exo

    # ── TRIGONOMÉTRIE (toujours figure sauf valeurs remarquables) ──
    if 'trigono' in cat.lower():
        # Valeurs remarquables pures : "cos(60°) = ?"
        if re.match(r'^(cos|sin|tan)\(\d+°\)\s*=', q.strip()):
            return exo
        if 'sin(90°)' in q or 'cos(0°)' in q:
            return exo

        nums = re.findall(r'\d+(?:[.,]\d+)?', q)
        n = [float(x.replace(',', '.')) for x in nums] if nums else []
        angle = None
        for v in n:
            if 10 < v < 90:
                angle = v
                break

        pts = re.findall(r'\b([A-Z])\b', exo.get('q', ''))
        pts = [p for p in pts if p not in ('I', 'J', 'L', 'O', 'V', 'F')]
        pts = list(dict.fromkeys(pts))

        exo['fig'] = make_fig('tri_trigo',
            angle=angle or 35,
            a=n[0] if n else 5,
            b=n[1] if len(n) > 1 else None,
            pts=pts[:3] if pts else ['A', 'B', 'C'])
        return exo

    # ── SECTIONS DE SOLIDES ──
    if 'section' in cat.lower():
        nums = re.findall(r'\d+(?:[.,]\d+)?', q)
        n = [float(x.replace(',', '.')) for x in nums] if nums else []

        if 'pyramide' in q:
            exo['fig'] = make_fig('pyramid', a=n[0] if n else 4, h=n[1] if len(n) > 1 else 6)
        elif 'cylindre' in q:
            exo['fig'] = make_fig('cylinder', r=n[0] if n else 3, h=n[1] if len(n) > 1 else 6)
        elif 'sphère' in q or 'boule' in q:
            exo['fig'] = make_fig('sphere', r=n[0] if n else 5)
        elif 'cube' in q or 'pavé' in q or 'prisme' in q:
            exo['fig'] = make_fig('cube', a=n[0] if n else 4,
                b=n[1] if len(n) > 1 else n[0] if n else 3,
                c=n[2] if len(n) > 2 else n[0] if n else 2,
                isCube='cube' in q)
        else:
            exo['fig'] = make_fig('section_solid')
        return exo

    # ── PYTHAGORE (problèmes concrets : mât, échelle, câble) ──
    if 'pythagore' in cat.lower():
        if any(w in q for w in ['mât', 'échelle', 'câble', 'poteau', 'mur', 'escalier', 'rampe']):
            nums = re.findall(r'\d+(?:[.,]\d+)?', q)
            n = [float(x.replace(',', '.')) for x in nums] if nums else []
            exo['fig'] = make_fig('tri_rect',
                a=n[0] if n else 6,
                b=n[1] if len(n) > 1 else 8,
                c=n[2] if len(n) > 2 else None,
                pts=['A', 'B', 'C'])
            return exo
        # "est-il rectangle ?" → triangle neutre (pas d'angle droit marqué = ne donne pas la réponse)
        if 'est-il rectangle' in q or 'est-ce' in q:
            nums = re.findall(r'\d+(?:[.,]\d+)?', q)
            n = [float(x.replace(',', '.')) for x in nums] if nums else []
            if len(n) >= 3:
                exo['fig'] = make_fig('triangle',
                    a=n[0], b=n[1], c=n[2],
                    pts=['A', 'B', 'C'])
                exo['fig']['confidence'] = 'high'
                return exo

    # ── TRIANGLES SEMBLABLES (problème d'ombre) ──
    if 'semblable' in cat.lower() or 'similaire' in cat.lower():
        if 'ombre' in q:
            nums = re.findall(r'\d+(?:[.,]\d+)?', q)
            n = [float(x.replace(',', '.')) for x in nums] if nums else []
            exo['fig'] = make_fig('similar_tri',
                a=n[0] if n else 1.5,
                b=n[1] if len(n) > 1 else 2,
                c=n[2] if len(n) > 2 else 30)
            return exo

    # ── SYMÉTRIE AXIALE : repère pour les coordonnées ──
    if 'symétrie_axiale' in cat.lower() or 'symetrie_axiale' in cat.lower():
        if re.search(r'\(\s*-?\d+\s*[;,]\s*-?\d+\s*\)', q):
            exo['fig'] = make_fig('repere', pts=[])
            return exo

    # ── PÉRIMÈTRES / AIRES ──
    if 'perimetre' in cat.lower() or 'aire' in cat.lower() or 'périmètre' in cat.lower():
        nums = re.findall(r'\d+(?:[.,]\d+)?', q)
        n = [float(x.replace(',', '.')) for x in nums] if nums else []

        if 'triangle' in q:
            exo['fig'] = make_fig('triangle',
                a=n[0] if n else 5,
                b=n[1] if len(n) > 1 else 4,
                c=n[2] if len(n) > 2 else None,
                pts=['A', 'B', 'C'])
        elif 'cercle' in q or 'disque' in q or 'rayon' in q:
            r = n[0] if n else 5
            if 'diamètre' in q and r > 2:
                r = r / 2
            exo['fig'] = make_fig('circle', r=r)
        elif 'parallélogramme' in q:
            exo['fig'] = make_fig('rect',
                w=n[0] if n else 8,
                h=n[1] if len(n) > 1 else 5)
        elif 'carré' in q:
            s = n[0] if n else 5
            exo['fig'] = make_fig('rect', w=s, h=s, square=True)
        elif 'rectangle' in q or ('longueur' in q and 'largeur' in q):
            exo['fig'] = make_fig('rect',
                w=n[0] if n else 6,
                h=n[1] if len(n) > 1 else 4)
        elif 'demi' in q and ('cercle' in q or 'disque' in q):
            exo['fig'] = make_fig('circle', r=n[0]/2 if n and n[0] > 2 else 5)
        return exo

    # ── VOLUMES ──
    if 'volume' in cat.lower():
        nums = re.findall(r'\d+(?:[.,]\d+)?', q)
        n = [float(x.replace(',', '.')) for x in nums] if nums else []

        if 'cylindre' in q:
            exo['fig'] = make_fig('cylinder', r=n[0] if n else 3, h=n[1] if len(n) > 1 else 6)
        elif 'cube' in q:
            s = n[0] if n else 4
            exo['fig'] = make_fig('cube', a=s, b=s, c=s, isCube=True)
        elif 'pavé' in q or 'parallélépipède' in q:
            exo['fig'] = make_fig('cube',
                a=n[0] if n else 4,
                b=n[1] if len(n) > 1 else 3,
                c=n[2] if len(n) > 2 else 2,
                isCube=False)
        elif 'prisme' in q:
            exo['fig'] = make_fig('cube', a=n[0] if n else 4, b=4, c=n[1] if len(n) > 1 else 7, isCube=False)
        elif 'sphère' in q or 'boule' in q:
            exo['fig'] = make_fig('sphere', r=n[0] if n else 4)
        elif 'cône' in q:
            exo['fig'] = make_fig('cone', r=n[0] if n else 3, h=n[1] if len(n) > 1 else 6)
        # Skip si conversion pure / terrain concret
        elif 'convertir' in q or 'terrain' in q or 'piscine' in q or 'litre' in q:
            return exo
        return exo

    # ── HOMOTHÉTIE ──
    if 'homothétie' in cat.lower() or 'homothetie' in cat.lower():
        nums = re.findall(r'\d+(?:[.,]\d+)?', q)
        n = [float(x.replace(',', '.')) for x in nums] if nums else []
        k = None
        for v in n:
            if 0 < v < 10 and v != 1:
                k = v
                break
        if k and ('cercle' not in q and 'carré' not in q and 'périmètre' not in q and 'aire' not in q):
            exo['fig'] = make_fig('homothety', k=k)
        return exo

    # ── GÉOMÉTRIE 6EME ──
    if 'géométrie' in cat.lower() or 'geometrie' in cat.lower():
        if 'parallélogramme' in q:
            nums = re.findall(r'\d+(?:[.,]\d+)?', q)
            n = [float(x.replace(',', '.')) for x in nums] if nums else []
            exo['fig'] = make_fig('rect', w=n[0] if n else 7, h=n[1] if len(n) > 1 else 4)
        elif 'diagonale' in q and 'rectangle' in q:
            nums = re.findall(r'\d+(?:[.,]\d+)?', q)
            n = [float(x.replace(',', '.')) for x in nums] if nums else []
            exo['fig'] = make_fig('rect', w=n[0] if n else 6, h=n[1] if len(n) > 1 else 8)
        elif 'cercle' in q and ('rayon' in q or 'diamètre' in q):
            nums = re.findall(r'\d+(?:[.,]\d+)?', q)
            n = [float(x.replace(',', '.')) for x in nums] if nums else []
            r = n[0] if n else 5
            if 'diamètre' in q and r > 2:
                r = r / 2
            exo['fig'] = make_fig('circle', r=r)
        return exo

    # ── ANGLES (figure seulement si angle donné, pas à trouver) ──
    if 'angle' in cat.lower():
        # "deux droites se coupent, un angle mesure 130°" → figure
        if 'droites' in q and ('coupent' in q or 'sécantes' in q):
            nums = re.findall(r'\d+(?:[.,]\d+)?', q)
            n = [float(x.replace(',', '.')) for x in nums] if nums else []
            deg = None
            for v in n:
                if 5 < v < 180:
                    deg = v
                    break
            if deg:
                exo['fig'] = make_fig('angle', deg=deg)
        # Triangle avec angles connus
        elif 'triangle' in q:
            nums = re.findall(r'\d+(?:[.,]\d+)?', q)
            n = [float(x.replace(',', '.')) for x in nums] if nums else []
            degs = [v for v in n if 5 < v < 180]
            if len(degs) >= 2:
                exo['fig'] = make_fig('triangle', a=5, b=4, c=6)
        return exo

    return exo


# ──────────────────────────────────────────────────────────────────────
# FIX DOUBLON SYSTÈMES 3EME
# ──────────────────────────────────────────────────────────────────────

SYSTEMES_BOOST_10_REPLACEMENT = {
    "lvl": 2,
    "q": "Résoudre le système : $\\begin{cases} 3x - y = 5 \\\\ x + 2y = 11 \\end{cases}$",
    "a": "$x = 3, y = 4$",
    "options": ["$x = 3, y = 4$", "$x = 4, y = 3$", "$x = 2, y = 1$", "$x = 5, y = 3$"],
    "f": "Méthode par substitution ou combinaison linéaire",
    "steps": [
        "De la 2e équation : $x = 11 - 2y$",
        "Remplacer dans la 1re : $3(11 - 2y) - y = 5$",
        "Simplifier : $33 - 6y - y = 5$, soit $-7y = -28$, donc $y = 4$ et $x = 3$"
    ]
}


# ──────────────────────────────────────────────────────────────────────
# MAIN PROCESSING
# ──────────────────────────────────────────────────────────────────────

def process_tab(tab_name, exos_col_idx, is_boost=False):
    """Traite un onglet Sheet : reformule + ajoute figures."""
    print(f"\n{'='*60}")
    print(f"📋 Traitement de {tab_name}")
    print(f"{'='*60}")

    raw = sh.read_raw(tab_name)
    if not raw:
        print(f"  ⚠️ Onglet vide")
        return 0, 0

    headers = raw[0]
    total_reformulated = 0
    total_fig_added = 0

    for row_idx in range(1, len(raw)):
        row = raw[row_idx]
        if len(row) <= exos_col_idx:
            continue

        niveau = row[0]
        cat = row[1]

        try:
            exos = json.loads(row[exos_col_idx])
        except (json.JSONDecodeError, TypeError):
            continue

        if not isinstance(exos, list):
            continue

        modified = False

        for i, exo in enumerate(exos):
            if not isinstance(exo, dict) or 'q' not in exo:
                continue

            original_q = exo['q']
            had_fig = 'fig' in exo and exo['fig']

            # 1. Clean LaTeX
            exo = clean_exo(exo)

            # 2. Specific reformulations
            source = "boost" if is_boost else "diag"
            key = (niveau, cat, source, i)
            if key in REFORMULATIONS:
                for field, val in REFORMULATIONS[key].items():
                    exo[field] = val

            # 3. Pattern-based reformulations
            if 'trigono' in cat.lower() or 'Trigono' in cat:
                exo['q'] = reformulate_trigo(exo['q'])

            if 'symétrie_axiale' in cat.lower() or 'Symétrie_Axiale' in cat or 'Symetrie_Axiale' in cat:
                exo['q'] = reformulate_sym_axiale(exo['q'])

            if 'thalès' in cat.lower() or 'thales' in cat.lower() or 'Thales' in cat:
                exo['q'] = reformulate_thales(exo['q'], cat)

            if 'section' in cat.lower() or 'Section' in cat:
                exo['q'] = reformulate_sections(exo['q'])

            # 4. Fix doublon Systèmes 3EME Boost #10
            if is_boost and niveau == '3EME' and 'système' in cat.lower() or 'Systemes' in cat:
                if i == 9:  # index 9 = boost #10
                    # Check if it's a duplicate of #9
                    if i > 0 and exos[i-1].get('q', '') and exo.get('q', ''):
                        if exos[i-1]['q'] == exo['q'] or ('2x+y=7' in exo['q'].replace(' ','') and '2x+y=7' in exos[i-1]['q'].replace(' ','')):
                            exo.update(SYSTEMES_BOOST_10_REPLACEMENT)
                            print(f"  🔧 Fix doublon: {niveau} {cat} Boost #10")
                            modified = True

            # 5. Add fig specs
            exo = detect_and_add_fig(exo, niveau, cat)

            # Track changes
            if exo['q'] != original_q:
                total_reformulated += 1
                modified = True
                q_short = exo['q'][:60] + '...' if len(exo['q']) > 60 else exo['q']
                print(f"  ✏️ Reformulé: {niveau} {cat} #{i+1} → {q_short}")

            if 'fig' in exo and exo['fig'] and not had_fig:
                total_fig_added += 1
                modified = True
                print(f"  🖼️ Figure: {niveau} {cat} #{i+1} → {exo['fig']['type']}")

            exos[i] = exo

        if modified:
            row[exos_col_idx] = json.dumps(exos, ensure_ascii=False)
            raw[row_idx] = row

    # Write back
    if total_reformulated > 0 or total_fig_added > 0:
        sh.write_rows(tab_name, raw, include_header=False)
        print(f"\n  📊 Résultat {tab_name}: {total_reformulated} reformulés, {total_fig_added} figures ajoutées")
    else:
        print(f"\n  ℹ️ {tab_name}: aucune modification nécessaire")

    return total_reformulated, total_fig_added


def main():
    print("🚀 fix_diag_boost.py — MASTERCLASS fix")
    print("="*60)

    # DiagnosticExos: Niveau(0), Categorie(1), ExosJSON(2)
    r1, f1 = process_tab("DiagnosticExos", 2, is_boost=False)

    # BoostExos: Niveau(0), Categorie(1), ExosJSON(2)
    r2, f2 = process_tab("BoostExos", 2, is_boost=True)

    # Curriculum_Officiel: Niveau(0), Categorie(1), Titre(2), Icone(3), ExosJSON(4)
    r3, f3 = process_tab("Curriculum_Officiel", 4, is_boost=True)

    print(f"\n{'='*60}")
    print(f"✅ TOTAL: {r1+r2+r3} reformulations, {f1+f2+f3} figures ajoutées")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
