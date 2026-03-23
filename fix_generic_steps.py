#!/usr/bin/env python3
"""
Fix generic steps in 1ERE exercises.
Reads from Curriculum_Officiel, rewrites generic steps with exercise-specific content,
writes back to Sheet.
"""

import json, re, copy
from sheets import sh

# ── Detection ──────────────────────────────────────────────────────────────

GENERIC_PHRASES = [
    "Identifier le type", "Identifier la propriété", "Identifier la formule",
    "Appliquer la formule", "Appliquer la règle",
    "Simplifier.", "Conclure.", "Calculer.",
    "Remplacer.", "Remplacer les valeurs",
    "Lire la coordonnée", "Lire le code",
    "Suivre les variables",
    "Formule du produit.", "Formule de Bayes",
    "À toi de finir", "Multiplier chaque valeur",
    "Additionner les produits",
    "Placer l'angle", "Différences de coordonnées",
    "Élever au carré", "Racine carrée.",
    "Moyenne des abscisses", "Moyenne des ordonnées",
    "Développer et identifier", "Calculer les racines",
    "Écrire la forme factorisée",
    "Vérifier le signe",
    "Le max est au sommet",
    "Coefficient directeur",
    "Vecteur directeur $(1",
    "Multiplier.", "Additionner.",
]

def is_generic_step(s):
    s = s.strip()
    if len(s) < 30 and '$' not in s:
        return True
    for p in GENERIC_PHRASES:
        if p.lower() in s.lower():
            return True
    return False

def is_generic_exercise(exo):
    steps = exo.get('steps', [])
    if not steps:
        return False
    return sum(1 for s in steps if is_generic_step(s)) >= 2


# ── Step rewriting logic per chapter ──────────────────────────────────────

def extract_math(text):
    """Extract all $...$ expressions from text."""
    return re.findall(r'\$[^$]+\$', text)

def rewrite_second_degre(exo):
    q, a, f = exo['q'], exo['a'], exo.get('f', '')
    maths = extract_math(q)

    if 'forme canonique' in q.lower():
        # Extract the polynomial
        poly = maths[0] if maths else 'f(x)'
        return [
            f"On cherche la forme canonique de {poly}. On utilise la formule $\\alpha = -\\frac{{b}}{{2a}}$ pour trouver le sommet.",
            f"Pour {poly}, on identifie $a$, $b$, $c$ et on calcule $\\alpha = -\\frac{{b}}{{2a}}$, puis $\\beta = f(\\alpha)$.",
            "Il reste à écrire $f(x) = a(x - \\alpha)^2 + \\beta$ avec les valeurs trouvées."
        ]
    elif 'racine' in q.lower() or 'combien' in q.lower():
        poly = maths[0] if maths else 'f(x)'
        return [
            f"On détermine le nombre de racines de {poly} en calculant le discriminant $\\Delta = b^2 - 4ac$.",
            f"Pour {poly}, on identifie $a$, $b$, $c$ et on effectue le calcul de $\\Delta$.",
            "Le signe de $\\Delta$ détermine le nombre de racines : $\\Delta > 0$ → deux racines, $\\Delta = 0$ → une racine double, $\\Delta < 0$ → aucune."
        ]
    elif 'sommet' in q.lower() or 'max' in q.lower() or 'hauteur' in q.lower():
        poly = maths[0] if maths else 'h(t)'
        return [
            f"On cherche le maximum de {poly}. Comme $a < 0$, la parabole est tournée vers le bas et le maximum est atteint au sommet.",
            f"Le sommet a pour abscisse $t_s = -\\frac{{b}}{{2a}}$. On remplace dans {poly} pour obtenir la valeur maximale.",
            "On en déduit la coordonnée du sommet qui donne le maximum recherché."
        ]
    elif 'factori' in q.lower():
        poly = maths[0] if maths else 'f(x)'
        return [
            f"On factorise {poly}. On commence par calculer $\\Delta = b^2 - 4ac$ pour trouver les racines.",
            f"On calcule les racines $x_1 = \\frac{{-b - \\sqrt{{\\Delta}}}}{{2a}}$ et $x_2 = \\frac{{-b + \\sqrt{{\\Delta}}}}{{2a}}$ avec les coefficients de {poly}.",
            "La forme factorisée est $a(x - x_1)(x - x_2)$."
        ]
    elif 'signe' in q.lower() or 'positif' in q.lower() or 'négatif' in q.lower() or 'tableau' in q.lower():
        poly = maths[0] if maths else 'f(x)'
        return [
            f"On étudie le signe de {poly}. On calcule d'abord $\\Delta$ et les racines éventuelles.",
            f"Le signe de $a$ détermine le sens de la parabole. Les racines (si elles existent) délimitent les changements de signe.",
            "On dresse le tableau de signes en utilisant la règle : même signe que $a$ à l'extérieur des racines."
        ]
    else:
        poly = maths[0] if maths else 'l\'expression'
        return [
            f"On analyse {poly}. On identifie les coefficients $a$, $b$ et $c$ du trinôme.",
            f"On calcule le discriminant $\\Delta = b^2 - 4ac$ avec les valeurs identifiées.",
            "Le résultat dépend du signe de $\\Delta$."
        ]


def rewrite_suites(exo):
    q, a = exo['q'], exo['a']
    maths = extract_math(q)

    if 'arithmétique' in q.lower() or 'u_0' in q:
        # Extract values from question
        u0_match = re.search(r'u_0\s*=\s*(\S+)', q)
        r_match = re.search(r'r\s*=\s*(\S+)', q)
        n_match = re.search(r'u_\{?(\d+)\}?', q)
        u0 = u0_match.group(1).rstrip('.') if u0_match else '?'
        r_val = r_match.group(1).rstrip('.') if r_match else '?'

        return [
            f"La suite est arithmétique de raison $r = {r_val}$ et de premier terme $u_0 = {u0}$. On utilise la formule $u_n = u_0 + n \\times r$.",
            f"On remplace : $u_n = {u0} + n \\times {r_val}$. Il reste à calculer avec la valeur de $n$ demandée.",
            "On effectue la multiplication puis l'addition pour obtenir le terme cherché."
        ]
    elif 'géométrique' in q.lower() or 'q =' in q.lower():
        v0_match = re.search(r'v_0\s*=\s*(\S+)', q)
        q_match = re.search(r'q\s*=\s*(\S+)', q)
        v0 = v0_match.group(1).rstrip('.') if v0_match else '?'
        q_val = q_match.group(1).rstrip('.') if q_match else '?'

        return [
            f"La suite est géométrique de raison $q = {q_val}$ et de premier terme $v_0 = {v0}$. On utilise la formule $v_n = v_0 \\times q^n$.",
            f"On remplace : $v_n = {v0} \\times {q_val}^n$. Il reste à calculer la puissance pour la valeur de $n$ demandée.",
            "On calcule d'abord la puissance, puis on multiplie par le premier terme."
        ]
    elif 'somme' in q.lower() or 'S_' in q or 'additionner' in q.lower():
        return [
            "On identifie la nature de la suite (arithmétique ou géométrique) et on repère les termes à additionner.",
            "On calcule chaque terme en appliquant la formule du terme général, puis on additionne.",
            "On vérifie le résultat en recalculant un terme intermédiaire."
        ]
    else:
        return [
            "On identifie la nature de la suite et la formule du terme général à utiliser.",
            "On remplace les valeurs connues ($u_0$ ou $v_0$, la raison, et l'indice $n$) dans la formule.",
            "On effectue les calculs étape par étape."
        ]


def rewrite_derivation(exo):
    q, a = exo['q'], exo['a']
    maths = extract_math(q)
    func = maths[0] if maths else 'f(x)'

    if 'tangente' in q.lower():
        x_match = re.search(r'en\s*\$?x\s*=\s*(\S+)', q)
        x_val = x_match.group(1).rstrip('$.') if x_match else 'a'
        return [
            f"L'équation de la tangente en $x = {x_val}$ est $y = f'({x_val})(x - {x_val}) + f({x_val})$. On doit calculer $f({x_val})$ et $f'({x_val})$.",
            f"On dérive {func} pour obtenir $f'(x)$, puis on évalue $f'({x_val})$ et $f({x_val})$.",
            "On remplace dans la formule de la tangente et on simplifie."
        ]
    elif 'croissant' in q.lower() or 'décroissant' in q.lower() or 'variation' in q.lower():
        return [
            f"On étudie les variations de {func}. On commence par calculer $f'(x)$.",
            f"On dérive {func} et on cherche le signe de $f'(x)$ (résoudre $f'(x) = 0$ puis étudier le signe).",
            "Si $f'(x) > 0$, la fonction est croissante ; si $f'(x) < 0$, elle est décroissante."
        ]
    elif 'x^3' in q or 'x^4' in q or 'x^2' in q:
        # Simple power derivation
        power_match = re.search(r'x\^(\d+)', q)
        n = power_match.group(1) if power_match else 'n'
        return [
            f"On dérive {func}. La règle est $(x^n)' = nx^{{n-1}}$.",
            f"Pour $x^{n}$, on multiplie par l'exposant $n = {n}$ et on diminue l'exposant de $1$ : ${n} \\cdot x^{{{int(n)-1}}}$." if n.isdigit() else f"On applique $(x^n)' = nx^{{n-1}}$ à chaque terme de {func}.",
            "On applique cette règle à chaque terme et on additionne les dérivées."
        ]
    elif 'produit' in q.lower() or '\\times' in q or 'u \\cdot v' in q.lower():
        return [
            f"On dérive {func} en utilisant la formule du produit : $(uv)' = u'v + uv'$.",
            f"On identifie $u$ et $v$ dans {func}, puis on calcule $u'$ et $v'$ séparément.",
            "On assemble : $u'v + uv'$ et on simplifie l'expression obtenue."
        ]
    elif 'quotient' in q.lower() or '\\frac' in q:
        return [
            f"On dérive {func} en utilisant la formule du quotient : $\\left(\\frac{{u}}{{v}}\\right)' = \\frac{{u'v - uv'}}{{v^2}}$.",
            f"On identifie $u$ (numérateur) et $v$ (dénominateur) dans {func}, puis on calcule $u'$ et $v'$.",
            "On assemble dans la formule du quotient et on simplifie."
        ]
    else:
        return [
            f"On dérive {func} terme par terme en appliquant les formules : $(x^n)' = nx^{{n-1}}$, $(kx)' = k$, $(c)' = 0$.",
            f"On calcule la dérivée de chaque terme de {func} séparément.",
            "On rassemble les termes pour obtenir $f'(x)$."
        ]


def rewrite_exponentielle(exo):
    q, a = exo['q'], exo['a']
    maths = extract_math(q)
    expr = maths[0] if maths else "l'expression"

    if 'times' in q or '\\times' in q or 'produit' in q.lower():
        # e^a * e^b
        exp_matches = re.findall(r'e\^\{?([^}$ ]+)\}?', q)
        if len(exp_matches) >= 2:
            return [
                f"On simplifie {expr}. D'après la propriété $e^a \\times e^b = e^{{a+b}}$, on additionne les exposants.",
                f"Les exposants sont ${exp_matches[0]}$ et ${exp_matches[1]}$. On calcule leur somme : ${exp_matches[0]} + {exp_matches[1]}$.",
                "On écrit le résultat sous la forme $e^{{\\text{{somme}}}}$."
            ]
        return [
            f"On utilise la propriété $e^a \\times e^b = e^{{a+b}}$. On additionne les exposants de {expr}.",
            "On identifie les deux exposants et on effectue leur addition.",
            "On écrit le résultat sous la forme $e^k$ avec $k$ la somme trouvée."
        ]
    elif 'frac' in q or 'divis' in q.lower():
        exp_matches = re.findall(r'e\^\{?([^}$ ]+)\}?', q)
        if len(exp_matches) >= 2:
            return [
                f"On simplifie {expr}. D'après la propriété $\\frac{{e^a}}{{e^b}} = e^{{a-b}}$, on soustrait les exposants.",
                f"Les exposants sont ${exp_matches[0]}$ et ${exp_matches[1]}$. On calcule ${exp_matches[0]} - {exp_matches[1]}$.",
                "On écrit le résultat sous la forme $e^{{\\text{{différence}}}}$."
            ]
        return [
            f"On utilise la propriété $\\frac{{e^a}}{{e^b}} = e^{{a-b}}$. On soustrait les exposants de {expr}.",
            "On identifie le numérateur et le dénominateur, puis on soustrait leurs exposants.",
            "On écrit le résultat sous la forme $e^k$."
        ]
    elif 'e^0' in q or '= 1' in q.lower() or 'vaut $e^{0}' in q:
        return [
            f"On évalue {expr}. La propriété fondamentale est $e^0 = 1$.",
            "Tout nombre (non nul) élevé à la puissance $0$ vaut $1$, et l'exponentielle ne fait pas exception.",
            "On conclut directement."
        ]
    elif 'dérivée' in q.lower() or 'dériver' in q.lower():
        return [
            f"On dérive {expr}. La dérivée de $e^u$ est $u' \\cdot e^u$.",
            f"On identifie $u$ dans {expr} et on calcule $u'$.",
            "On multiplie $u'$ par $e^u$ pour obtenir la dérivée."
        ]
    elif 'équation' in q.lower() or 'résoudre' in q.lower():
        return [
            f"On résout {expr}. On utilise le fait que $e^a = e^b \\Leftrightarrow a = b$ (l'exponentielle est injective).",
            "On met l'équation sous la forme $e^{{\\text{{quelque chose}}}} = e^{{\\text{{autre chose}}}}$ et on identifie les exposants.",
            "On résout l'équation obtenue sur les exposants."
        ]
    elif 'ln' in q.lower() or 'log' in q.lower():
        return [
            f"On simplifie {expr} en utilisant la relation $\\ln(e^a) = a$ (le logarithme est la réciproque de l'exponentielle).",
            "On identifie l'exposant à l'intérieur de l'exponentielle.",
            "Le logarithme népérien \"annule\" l'exponentielle et renvoie l'exposant."
        ]
    elif '(e^' in q and ')^' in q:
        # (e^a)^b = e^{ab}
        exp_matches = re.findall(r'e\^\{?([^}$) ]+)\}?', q)
        pow_match = re.search(r'\)\^\{?([^}$ ]+)', q)
        if exp_matches and pow_match:
            return [
                f"On simplifie {expr}. D'après la propriété $(e^a)^b = e^{{a \\times b}}$, on multiplie les exposants.",
                f"L'exposant intérieur est ${exp_matches[0]}$ et l'exposant extérieur est ${pow_match.group(1)}$. On calcule leur produit.",
                "On écrit le résultat sous la forme $e^k$ avec $k$ le produit trouvé."
            ]

    # Fallback for exponentielle
    return [
        f"On simplifie {expr} en identifiant la propriété de l'exponentielle à utiliser ($e^{{a+b}}$, $e^{{a-b}}$, ou $(e^a)^b$).",
        "On repère les exposants dans l'expression et on effectue l'opération correspondante (addition, soustraction ou multiplication d'exposants).",
        "On écrit le résultat simplifié sous la forme $e^k$."
    ]


def rewrite_trigonometrie(exo):
    q, a = exo['q'], exo['a']
    maths = extract_math(q)

    if 'cos' in q.lower() and ('sin' not in q.lower() or 'cos' in q.lower()):
        angle_match = re.search(r'\\cos\(([^)]+)\)', q)
        angle = angle_match.group(1) if angle_match else '\\theta'
        if angle == '0':
            return [
                "On cherche $\\cos(0)$. Sur le cercle trigonométrique, l'angle $0$ correspond au point $(1; 0)$.",
                "Le cosinus correspond à l'abscisse du point sur le cercle trigonométrique. Pour l'angle $0$, ce point est $(1; 0)$.",
                "L'abscisse est $1$, donc $\\cos(0) = 1$."
            ]
        return [
            f"On cherche $\\cos({angle})$. On place l'angle ${angle}$ sur le cercle trigonométrique et on lit l'abscisse du point correspondant.",
            f"Pour l'angle ${angle}$, on utilise les valeurs remarquables : $\\cos(\\pi/6) = \\frac{{\\sqrt{{3}}}}{{2}}$, $\\cos(\\pi/4) = \\frac{{\\sqrt{{2}}}}{{2}}$, $\\cos(\\pi/3) = \\frac{{1}}{{2}}$, $\\cos(\\pi/2) = 0$.",
            f"On identifie ${angle}$ parmi ces valeurs remarquables et on lit le cosinus correspondant."
        ]

    if 'sin' in q.lower():
        angle_match = re.search(r'\\sin\(([^)]+)\)', q)
        angle = angle_match.group(1) if angle_match else '\\theta'
        return [
            f"On cherche $\\sin({angle})$. On place l'angle ${angle}$ sur le cercle trigonométrique et on lit l'ordonnée du point correspondant.",
            f"Pour l'angle ${angle}$, on utilise les valeurs remarquables : $\\sin(\\pi/6) = \\frac{{1}}{{2}}$, $\\sin(\\pi/4) = \\frac{{\\sqrt{{2}}}}{{2}}$, $\\sin(\\pi/3) = \\frac{{\\sqrt{{3}}}}{{2}}$, $\\sin(\\pi/2) = 1$.",
            f"On identifie ${angle}$ parmi ces valeurs et on lit le sinus correspondant."
        ]

    if 'tan' in q.lower():
        angle_match = re.search(r'\\tan\(([^)]+)\)', q)
        angle = angle_match.group(1) if angle_match else '\\theta'
        return [
            f"On cherche $\\tan({angle})$. On utilise la relation $\\tan(\\theta) = \\frac{{\\sin(\\theta)}}{{\\cos(\\theta)}}$.",
            f"On détermine d'abord $\\sin({angle})$ et $\\cos({angle})$ à partir des valeurs remarquables.",
            "On effectue la division pour obtenir la tangente."
        ]

    if 'identité' in q.lower() or 'cos^2' in q or 'sin^2' in q:
        expr = maths[0] if maths else "l'expression"
        return [
            f"On simplifie {expr} en utilisant l'identité fondamentale $\\cos^2(\\theta) + \\sin^2(\\theta) = 1$.",
            f"On réécrit {expr} en faisant apparaître $\\cos^2 + \\sin^2$ et on remplace par $1$.",
            "On simplifie l'expression résultante."
        ]

    if 'équation' in q.lower() or 'résoudre' in q.lower():
        return [
            f"On résout l'équation trigonométrique. On identifie la valeur remarquable du cosinus ou du sinus cherchée.",
            "On utilise le cercle trigonométrique pour trouver les angles dont le cosinus (ou le sinus) vaut la valeur donnée.",
            "On exprime les solutions sur l'intervalle demandé, en tenant compte de la périodicité."
        ]

    # Fallback
    expr = maths[0] if maths else "l'expression"
    return [
        f"On évalue {expr} en utilisant les valeurs remarquables du cercle trigonométrique.",
        "On repère l'angle parmi les valeurs connues ($0$, $\\pi/6$, $\\pi/4$, $\\pi/3$, $\\pi/2$, $\\pi$) et on lit la valeur correspondante.",
        "On en déduit le résultat."
    ]


def rewrite_produit_scalaire(exo):
    q, a = exo['q'], exo['a']
    maths = extract_math(q)

    if 'coordonn' in q.lower() or ('vec{u}' in q and 'vec{v}' in q and 'angle' not in q.lower()):
        # Dot product with coordinates
        coord_matches = re.findall(r'\((\-?\d+)[;,](\-?\d+)\)', q)
        if len(coord_matches) >= 2:
            x1, y1 = coord_matches[0]
            x2, y2 = coord_matches[1]
            return [
                f"On calcule $\\vec{{u}} \\cdot \\vec{{v}}$ avec les coordonnées. La formule est $\\vec{{u}} \\cdot \\vec{{v}} = x_u x_v + y_u y_v$.",
                f"On remplace : $\\vec{{u}} \\cdot \\vec{{v}} = {x1} \\times {x2} + {y1} \\times {y2}$.",
                "On effectue les deux multiplications puis l'addition."
            ]
        return [
            "On calcule le produit scalaire avec la formule des coordonnées : $\\vec{u} \\cdot \\vec{v} = x_u x_v + y_u y_v$.",
            "On remplace par les coordonnées données et on effectue les produits.",
            "On additionne les deux produits pour obtenir le résultat."
        ]

    if 'angle' in q.lower() or 'norme' in q.lower() or '\\|' in q:
        return [
            "On calcule le produit scalaire avec la formule $\\vec{u} \\cdot \\vec{v} = \\|\\vec{u}\\| \\times \\|\\vec{v}\\| \\times \\cos(\\theta)$.",
            f"On remplace par les valeurs données dans l'énoncé : normes et angle.",
            "On effectue la multiplication en calculant d'abord $\\cos(\\theta)$ si nécessaire."
        ]

    if 'orthogon' in q.lower() or 'perpendic' in q.lower():
        return [
            "Deux vecteurs sont orthogonaux si et seulement si leur produit scalaire est nul : $\\vec{u} \\cdot \\vec{v} = 0$.",
            "On calcule $\\vec{u} \\cdot \\vec{v}$ avec les coordonnées ou les normes données.",
            "On vérifie si le résultat est $0$ pour conclure sur l'orthogonalité."
        ]

    if 'norme' in q.lower() or '\\|' in q:
        return [
            "On utilise la relation $\\|\\vec{u}\\|^2 = \\vec{u} \\cdot \\vec{u}$ (le produit scalaire d'un vecteur par lui-même donne le carré de sa norme).",
            "On calcule $\\vec{u} \\cdot \\vec{u} = x_u^2 + y_u^2$ avec les coordonnées données.",
            "On prend la racine carrée pour obtenir $\\|\\vec{u}\\|$."
        ]

    # Fallback
    return [
        "On identifie les données : coordonnées, normes ou angle entre les vecteurs, puis on choisit la formule adaptée.",
        "On remplace les valeurs dans la formule du produit scalaire choisie.",
        "On effectue les calculs pour obtenir le résultat."
    ]


def rewrite_geometrie_repere(exo):
    q, a = exo['q'], exo['a']
    maths = extract_math(q)

    if 'vecteur directeur' in q.lower():
        m_match = re.search(r'=\s*(\-?\d+)x', q)
        m_val = m_match.group(1) if m_match else 'm'
        return [
            f"Pour une droite $y = mx + p$, un vecteur directeur est $\\vec{{u}}(1; m)$. On lit le coefficient directeur $m$ dans l'équation.",
            f"Ici $m = {m_val}$. Le vecteur directeur est donc $\\vec{{u}}(1; {m_val})$.",
            "On vérifie : si on se déplace de $1$ en abscisse, on se déplace de $m$ en ordonnée, ce qui est bien la pente."
        ]

    if 'distance' in q.lower() or 'longueur' in q.lower():
        coord_matches = re.findall(r'\((\-?\d+)[;,]\s*(\-?\d+)\)', q)
        if len(coord_matches) >= 2:
            x1, y1 = coord_matches[0]
            x2, y2 = coord_matches[1]
            return [
                f"On calcule la distance entre les points de coordonnées $({x1}; {y1})$ et $({x2}; {y2})$ avec la formule $d = \\sqrt{{(x_B - x_A)^2 + (y_B - y_A)^2}}$.",
                f"On calcule les différences : $x_B - x_A = {int(x2)-int(x1)}$ et $y_B - y_A = {int(y2)-int(y1)}$, puis on élève au carré et on additionne.",
                "On prend la racine carrée de la somme pour obtenir la distance."
            ]
        return [
            "On utilise la formule de la distance : $d = \\sqrt{(x_B - x_A)^2 + (y_B - y_A)^2}$.",
            "On calcule les différences de coordonnées, on les élève au carré et on additionne.",
            "On prend la racine carrée du résultat."
        ]

    if 'milieu' in q.lower():
        coord_matches = re.findall(r'\((\-?\d+)[;,]\s*(\-?\d+)\)', q)
        if len(coord_matches) >= 2:
            x1, y1 = coord_matches[0]
            x2, y2 = coord_matches[1]
            return [
                f"On cherche le milieu de $[AB]$ avec $A({x1}; {y1})$ et $B({x2}; {y2})$. La formule est $M = \\left(\\frac{{x_A + x_B}}{{2}}; \\frac{{y_A + y_B}}{{2}}\\right)$.",
                f"On calcule : abscisse $= \\frac{{{x1} + {x2}}}{{2}}$ et ordonnée $= \\frac{{{y1} + {y2}}}{{2}}$.",
                "On effectue les deux divisions pour obtenir les coordonnées du milieu."
            ]
        return [
            "On utilise la formule du milieu : $M = \\left(\\frac{x_A + x_B}{2}; \\frac{y_A + y_B}{2}\\right)$.",
            "On additionne les abscisses et on divise par $2$, puis on fait de même pour les ordonnées.",
            "On obtient les coordonnées du milieu."
        ]

    if 'équation' in q.lower() and 'droite' in q.lower():
        return [
            "On détermine l'équation de la droite. Si on connaît deux points, on calcule le coefficient directeur $m = \\frac{y_B - y_A}{x_B - x_A}$.",
            "On remplace par les coordonnées données pour calculer $m$, puis on utilise $y - y_A = m(x - x_A)$ pour trouver $p$.",
            "On écrit l'équation sous la forme $y = mx + p$."
        ]

    if 'colinéaire' in q.lower() or 'parallèle' in q.lower():
        return [
            "Deux vecteurs $\\vec{u}(a; b)$ et $\\vec{v}(c; d)$ sont colinéaires si et seulement si $ad - bc = 0$.",
            "On calcule le déterminant $ad - bc$ avec les coordonnées des vecteurs donnés.",
            "Si le résultat est $0$, les vecteurs sont colinéaires (et les droites parallèles)."
        ]

    # Fallback
    return [
        "On identifie les coordonnées des points ou des vecteurs donnés dans l'énoncé.",
        "On applique la formule de géométrie repérée correspondante avec ces coordonnées.",
        "On effectue les calculs pour obtenir le résultat."
    ]


def rewrite_probabilites_cond(exo):
    q, a = exo['q'], exo['a']
    maths = extract_math(q)

    if 'cap' in q.lower() or '\\cap' in q:
        # P(A ∩ B) = P(A) × P(B|A)
        prob_matches = re.findall(r'(\d+[{,}]?\d*)', q)
        return [
            "On cherche $P(A \\cap B)$. D'après la formule des probabilités conditionnelles : $P(A \\cap B) = P(A) \\times P(B|A)$.",
            "On identifie $P(A)$ et $P(B|A)$ dans l'énoncé et on effectue la multiplication.",
            "On en déduit $P(A \\cap B)$."
        ]

    if 'B|A' in q or 'sachant' in q.lower():
        return [
            "On cherche une probabilité conditionnelle. La formule est $P(B|A) = \\frac{P(A \\cap B)}{P(A)}$.",
            "On identifie $P(A \\cap B)$ et $P(A)$ dans l'énoncé et on effectue la division.",
            "On en déduit la probabilité conditionnelle."
        ]

    if 'bayes' in q.lower() or 'totale' in q.lower():
        return [
            "On utilise la formule de Bayes : $P(A|B) = \\frac{P(B|A) \\times P(A)}{P(B)}$, éventuellement combinée avec la formule des probabilités totales.",
            "On identifie toutes les probabilités données et on les organise (un arbre pondéré peut aider).",
            "On remplace dans la formule et on effectue le calcul."
        ]

    if 'arbre' in q.lower() or 'indépendant' in q.lower():
        return [
            "On détermine si les événements sont indépendants. Deux événements $A$ et $B$ sont indépendants si $P(A \\cap B) = P(A) \\times P(B)$.",
            "On calcule $P(A) \\times P(B)$ et on compare avec $P(A \\cap B)$.",
            "Si les deux valeurs sont égales, les événements sont indépendants."
        ]

    # Fallback
    return [
        "On identifie les probabilités données dans l'énoncé et la probabilité cherchée.",
        "On choisit la formule adaptée : produit ($P(A \\cap B) = P(A) \\times P(B|A)$) ou conditionnelle ($P(B|A) = \\frac{P(A \\cap B)}{P(A)}$).",
        "On remplace et on calcule."
    ]


def rewrite_variables_aleatoires(exo):
    q, a = exo['q'], exo['a']
    maths = extract_math(q)

    # Extract values and probabilities if possible
    vals_match = re.findall(r'valeurs?\s+\$?([^$]+)\$?', q)

    if 'E(X)' in q or 'espérance' in q.lower():
        # Try to extract the values
        val_matches = re.findall(r'(\d+)', q)
        return [
            "On calcule l'espérance $E(X) = \\sum x_i \\cdot p_i$. On multiplie chaque valeur de $X$ par sa probabilité.",
            "On effectue chaque produit : pour chaque valeur $x_i$, on calcule $x_i \\times p_i$.",
            "On additionne tous les produits obtenus. Le résultat est $E(X)$."
        ]

    if 'V(X)' in q or 'variance' in q.lower():
        return [
            "On calcule la variance $V(X) = E(X^2) - [E(X)]^2$. On commence par calculer $E(X)$ et $E(X^2)$.",
            "Pour $E(X^2)$, on remplace chaque $x_i$ par $x_i^2$ dans la formule de l'espérance : $E(X^2) = \\sum x_i^2 \\cdot p_i$.",
            "On calcule $V(X) = E(X^2) - [E(X)]^2$ avec les valeurs trouvées."
        ]

    if 'écart' in q.lower() or 'sigma' in q.lower():
        return [
            "L'écart-type est $\\sigma(X) = \\sqrt{V(X)}$. On commence par calculer la variance.",
            "On calcule $V(X) = E(X^2) - [E(X)]^2$ avec les valeurs et probabilités données.",
            "On prend la racine carrée de la variance pour obtenir l'écart-type."
        ]

    if 'loi' in q.lower() or 'binomiale' in q.lower():
        return [
            "On identifie les paramètres de la loi binomiale : $n$ (nombre d'épreuves) et $p$ (probabilité de succès).",
            "On applique la formule $P(X = k) = \\binom{n}{k} p^k (1-p)^{n-k}$ avec les valeurs de l'énoncé.",
            "On effectue le calcul du coefficient binomial puis des puissances."
        ]

    # Fallback
    return [
        "On identifie la loi de probabilité de $X$ : les valeurs prises et leurs probabilités respectives.",
        "On applique la formule demandée ($E(X)$, $V(X)$ ou $P(X = k)$) en remplaçant par les valeurs de l'énoncé.",
        "On effectue les calculs étape par étape."
    ]


def rewrite_algorithmique(exo):
    q, a = exo['q'], exo['a']

    # Try to extract the code from the question
    code_match = re.search(r'```python\n(.*?)```', q, re.DOTALL)
    code = code_match.group(1).strip() if code_match else None

    if code:
        # Analyze the code
        lines = code.split('\n')
        has_for = any('for' in l for l in lines)
        has_while = any('while' in l for l in lines)
        has_if = any('if' in l for l in lines)
        has_def = any('def' in l for l in lines)

        # Find initial variable assignments
        init_vars = []
        for l in lines:
            m = re.match(r'\s*(\w+)\s*=\s*(.+)', l)
            if m and 'for' not in l and 'while' not in l:
                init_vars.append((m.group(1), m.group(2).strip()))

        if has_for:
            range_match = re.search(r'range\((\d+)\)', code)
            n_iter = range_match.group(1) if range_match else '?'
            var_str = ', '.join(f'${v} = {val}$' for v, val in init_vars[:2]) if init_vars else 'les variables initiales'
            return [
                f"On exécute le code pas à pas. On initialise {var_str}. La boucle `for` s'exécute ${n_iter}$ fois.",
                f"À chaque passage dans la boucle, on met à jour les variables. On trace les valeurs successives sur les premières itérations.",
                "On lit la valeur affichée par `print` après la dernière itération."
            ]
        elif has_while:
            var_str = ', '.join(f'${v} = {val}$' for v, val in init_vars[:2]) if init_vars else 'les variables initiales'
            return [
                f"On exécute le code pas à pas. On initialise {var_str}. La boucle `while` tourne tant que la condition est vraie.",
                "On trace les valeurs des variables à chaque itération jusqu'à ce que la condition devienne fausse.",
                "On lit la valeur finale affichée par `print`."
            ]
        elif has_def:
            return [
                "On lit la définition de la fonction et on identifie ses paramètres et ce qu'elle renvoie.",
                "On exécute la fonction avec les arguments donnés en suivant les instructions ligne par ligne.",
                "On détermine la valeur renvoyée par `return`."
            ]
        else:
            var_str = ', '.join(f'${v} = {val}$' for v, val in init_vars[:2]) if init_vars else 'les variables'
            return [
                f"On exécute le code ligne par ligne. On commence par {var_str}.",
                "On effectue chaque opération dans l'ordre et on note la valeur des variables après chaque ligne.",
                "On lit la valeur affichée par `print` à la fin."
            ]

    # Question about len, type, etc.
    if 'len' in q:
        list_match = re.search(r'\[([^\]]+)\]', q)
        if list_match:
            elements = list_match.group(1)
            return [
                f"La fonction `len()` renvoie le nombre d'éléments d'une liste. Ici la liste contient : $[{elements}]$.",
                f"On compte les éléments séparés par des virgules dans $[{elements}]$.",
                "Le résultat de `len()` est ce nombre d'éléments."
            ]

    if 'range' in q:
        range_match = re.search(r'range\(([^)]+)\)', q)
        if range_match:
            args = range_match.group(1)
            return [
                f"La fonction `range({args})` génère une séquence d'entiers. On détermine le premier et le dernier élément.",
                f"On liste les entiers générés par `range({args})` (le dernier argument est exclu).",
                "On en déduit la réponse demandée."
            ]

    # Fallback
    return [
        "On lit le code Python attentivement et on identifie les variables, les boucles et les conditions.",
        "On exécute mentalement le code ligne par ligne en notant la valeur de chaque variable à chaque étape.",
        "On détermine la valeur affichée ou renvoyée à la fin de l'exécution."
    ]


REWRITERS = {
    'Second_Degre': rewrite_second_degre,
    'Suites': rewrite_suites,
    'Derivation': rewrite_derivation,
    'Exponentielle': rewrite_exponentielle,
    'Trigonometrie': rewrite_trigonometrie,
    'Produit_Scalaire': rewrite_produit_scalaire,
    'Geometrie_Repere': rewrite_geometrie_repere,
    'Probabilites_Cond': rewrite_probabilites_cond,
    'Variables_Aleatoires': rewrite_variables_aleatoires,
    'Algorithmique': rewrite_algorithmique,
}


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    rows = sh.read_raw('Curriculum_Officiel')
    headers = rows[0]
    exos_col = headers.index('ExosJSON')

    total_fixed = 0
    report = {}

    for i, r in enumerate(rows[1:], 1):
        if not r or r[0] != '1ERE':
            continue

        cat = r[1]
        exos_json = r[exos_col] if exos_col < len(r) else ''
        try:
            exos = json.loads(exos_json)
        except:
            print(f"❌ {cat}: JSON invalide, skip")
            continue

        rewriter = REWRITERS.get(cat)
        if not rewriter:
            print(f"⚠️  {cat}: pas de rewriter, skip")
            continue

        fixed = 0
        for j, exo in enumerate(exos):
            if is_generic_exercise(exo):
                old_steps = exo['steps']
                new_steps = rewriter(exo)

                # Verify: answer must NOT appear in any step
                answer = exo.get('a', '')
                answer_clean = answer.strip().replace('$', '')
                safe = True
                for s in new_steps:
                    s_clean = s.replace('$', '')
                    if answer_clean and answer_clean in s_clean:
                        print(f"  ⚠️  {cat} exo {j}: answer found in step, keeping generic")
                        safe = False
                        break

                if safe:
                    exo['steps'] = new_steps
                    fixed += 1
                    print(f"  ✅ {cat} exo {j}: {old_steps} → {new_steps}")

        if fixed > 0:
            # Write back
            new_json = json.dumps(exos, ensure_ascii=False)
            # Pad row if needed
            while len(rows[i]) <= exos_col:
                rows[i].append('')
            rows[i][exos_col] = new_json

        report[cat] = fixed
        total_fixed += fixed

    # Write back to sheet
    if total_fixed > 0:
        sh.write_rows('Curriculum_Officiel', rows)

    print(f"\n{'='*50}")
    print(f"RAPPORT — Steps génériques corrigés")
    print(f"{'='*50}")
    for cat, count in report.items():
        print(f"  {cat}: {count} exercices corrigés")
    print(f"  TOTAL: {total_fixed}")


if __name__ == '__main__':
    main()
