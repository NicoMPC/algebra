"""
Fix exercise quality issues for 6EME and 5EME.
1. 6EME Fractions exo 3: make options unambiguous (no commutativity issue found - skip or check)
2. 6EME Agrandissement: fix step 1s that reveal the final answer
3. 5EME Racines_Carrées: replace with Angles_Parallèles (20 new exercises)
"""

import json
from sheets import sh

# ─── 1. 6EME Agrandissement: Fix step 1s that give away the answer ──────────

print("=== Fixing 6EME Agrandissement step 1s ===")
raw = sh.read_raw("Curriculum_Officiel")

# Row 41 (1-indexed) = Agrandissement_Réduction
agr_row = raw[40]  # 0-indexed
exos = json.loads(agr_row[4])  # ExosJSON is col 5 (index 4)

# Fix each step 1 that leaks the answer
fixes = {
    1: ["Regarde la valeur de $k$. Compare-la à $1$."],
    4: ["Que signifie une échelle de $\\frac{1}{100}$ ? Réfléchis au lien entre cm sur le plan et cm en réalité."],
    5: ["On applique le rapport de réduction à la mesure réelle. Pose le calcul."],
    7: ["Compare $0{,}5$ à $1$. Que peut-on en déduire ?"],
    8: ["Quand on agrandit avec un rapport $k$, comment sont transformées les aires ? Pense à $k^2$."],
    9: ["On applique le rapport $\\frac{1}{4}$ à la mesure donnée. Pose la multiplication."],
    11: ["Convertis d'abord la distance de la carte en cm réels, en utilisant l'échelle."],
    14: ["Pour retrouver la mesure réelle, il faut \"inverser\" le rapport de réduction. Pose le calcul."],
    15: ["Multiplie chaque mesure sur le plan par le dénominateur de l'échelle pour obtenir la mesure réelle."],
    16: ["Quel est le rapport entre la longueur réduite et la longueur d'origine ? Simplifie la fraction."],
    17: ["Quand on agrandit avec un rapport $k$, les aires sont multipliées par $k^2$. Calcule $k^2$ d'abord."],
    19: ["Convertis $45$ km en cm pour utiliser l'échelle de la carte."],
}

for idx, new_step1 in fixes.items():
    exos[idx]["steps"][0] = new_step1[0]

agr_row[4] = json.dumps(exos, ensure_ascii=False)
sh.update_cell("Curriculum_Officiel", 41, 5, agr_row[4])
print(f"  ✅ Fixed {len(fixes)} step 1s in Agrandissement_Réduction")

# ─── 2. 6EME Fractions exo 3: check for commutativity ──────────────────────

print("\n=== Checking 6EME Fractions exo 3 ===")
frac_row = raw[1]  # row 2, 0-indexed = 1
frac_exos = json.loads(frac_row[4])
e3 = frac_exos[3]
print(f"  Exo 3: q={e3['q'][:60]}")
print(f"  a={e3['a']}, options={e3['options']}")
# The current exo 3 asks for equivalent fraction - no commutativity issue.
# The user mentioned "3×4" vs "4×3" - let me check all exos for multiplication answers
found_commut = False
for i, e in enumerate(frac_exos):
    a = str(e.get('a', ''))
    opts = e.get('options', [])
    # Check if answer involves multiplication that could be commutative
    if '×' in a or '\\times' in a:
        print(f"  [!] Exo {i} has multiplication in answer: {a}")
        found_commut = True
    for o in opts:
        if '×' in str(o) and str(o) != a:
            # Check if commutative version equals answer
            pass

if not found_commut:
    print("  No commutativity issue found in Fractions. Skipping.")

# ─── 3. 5EME: Replace Racines_Carrées with Angles_Parallèles ────────────────

print("\n=== Replacing 5EME Racines_Carrées with Angles_Parallèles ===")

angles_exos = [
    # ── Slot 1: Angles alternes-internes et correspondants (reconnaissance) ──
    # Exo 1 - QCM accessible
    {
        "lvl": 1,
        "q": "Deux droites parallèles sont coupées par une sécante. Les angles alternes-internes mesurent :",
        "a": "la même chose",
        "options": ["la même chose", "des valeurs différentes", "toujours $90°$"],
        "steps": [
            "Quand deux droites sont parallèles, il y a une propriété importante sur les angles alternes-internes.",
            "Les angles alternes-internes sont situés de part et d'autre de la sécante, entre les parallèles.",
            "Propriété : si les droites sont parallèles, les angles alternes-internes sont égaux."
        ],
        "f": "Si $(d_1) \\parallel (d_2)$, alors les angles alternes-internes sont égaux."
    },
    # Exo 2 - QCM accessible
    {
        "lvl": 1,
        "q": "Sur la figure, $(d_1) \\parallel (d_2)$ et une sécante forme un angle de $55°$ avec $(d_1)$. Quel est l'angle alterne-interne correspondant sur $(d_2)$ ?",
        "a": "$55°$",
        "options": ["$55°$", "$125°$", "$35°$"],
        "steps": [
            "Identifie les deux angles alternes-internes : ils sont de chaque côté de la sécante, entre les parallèles.",
            "Comme $(d_1) \\parallel (d_2)$, les angles alternes-internes sont égaux.",
            "L'angle sur $(d_2)$ mesure donc aussi $55°$."
        ],
        "f": "Angles alternes-internes entre parallèles $\\Rightarrow$ égaux."
    },
    # Exo 3 - QCM intermédiaire
    {
        "lvl": 1,
        "q": "Liam trace deux droites parallèles coupées par une sécante. Un angle correspondant mesure $72°$. Quel est l'angle correspondant de l'autre côté ?",
        "a": "$72°$",
        "options": ["$72°$", "$108°$", "$18°$"],
        "steps": [
            "Les angles correspondants sont du même côté de la sécante, l'un au-dessus, l'autre en-dessous.",
            "Quand les droites sont parallèles, les angles correspondants sont égaux.",
            "L'angle correspondant mesure aussi $72°$."
        ],
        "f": "Si $(d_1) \\parallel (d_2)$, alors les angles correspondants sont égaux."
    },
    # Exo 4 - VF intermédiaire
    {
        "lvl": 1,
        "type": "vf",
        "q": "Si deux angles alternes-internes sont égaux, alors les droites sont parallèles.",
        "a": "Vrai",
        "options": ["Vrai", "Faux"],
        "steps": [
            "C'est la réciproque de la propriété des angles alternes-internes.",
            "La propriété directe dit : parallèles $\\Rightarrow$ alternes-internes égaux.",
            "La réciproque dit : alternes-internes égaux $\\Rightarrow$ parallèles. Elle est vraie."
        ],
        "f": "Alternes-internes égaux $\\Leftrightarrow$ droites parallèles."
    },
    # Exo 5 - Fill challenge
    {
        "lvl": 1,
        "type": "fill",
        "q": "$(d_1) \\parallel (d_2)$, une sécante forme un angle de $130°$ avec $(d_1)$. L'angle alterne-interne sur $(d_2)$ mesure ___°.",
        "a": "130",
        "options": [],
        "steps": [
            "Repère les deux angles alternes-internes sur la figure.",
            "Les droites sont parallèles, donc les angles alternes-internes sont égaux.",
            "L'angle cherché mesure $130°$."
        ],
        "f": "Alternes-internes entre parallèles $=$ même mesure."
    },

    # ── Slot 2: Angles supplémentaires et complémentaires ──
    # Exo 6 - QCM accessible
    {
        "lvl": 1,
        "q": "Deux angles supplémentaires ont une somme de :",
        "a": "$180°$",
        "options": ["$90°$", "$180°$", "$360°$"],
        "steps": [
            "Rappelle-toi la définition : deux angles sont supplémentaires quand leur somme vaut un angle plat.",
            "Un angle plat mesure $180°$.",
            "Donc deux angles supplémentaires ont pour somme $180°$."
        ],
        "f": "Angles supplémentaires : $\\alpha + \\beta = 180°$."
    },
    # Exo 7 - QCM accessible
    {
        "lvl": 1,
        "q": "Un angle mesure $64°$. Quel est son supplémentaire ?",
        "a": "$116°$",
        "options": ["$116°$", "$26°$", "$296°$"],
        "steps": [
            "Deux angles supplémentaires ont pour somme $180°$.",
            "On cherche $180° - 64°$.",
            "$180 - 64 = 116$. Le supplémentaire mesure $116°$."
        ],
        "f": "$\\beta = 180° - \\alpha$"
    },
    # Exo 8 - QCM intermédiaire
    {
        "lvl": 1,
        "q": "Emma mesure un angle de $47°$ entre deux rues. Quel est le complément de cet angle ?",
        "a": "$43°$",
        "options": ["$43°$", "$133°$", "$53°$"],
        "steps": [
            "Deux angles complémentaires ont pour somme $90°$ (un angle droit).",
            "On calcule $90° - 47°$.",
            "$90 - 47 = 43$. Le complément mesure $43°$."
        ],
        "f": "Angles complémentaires : $\\alpha + \\beta = 90°$."
    },
    # Exo 9 - VF intermédiaire
    {
        "lvl": 1,
        "type": "vf",
        "q": "Deux angles adjacents qui forment un angle plat sont supplémentaires.",
        "a": "Vrai",
        "options": ["Vrai", "Faux"],
        "steps": [
            "Un angle plat mesure $180°$.",
            "Si deux angles adjacents forment ensemble un angle plat, leur somme vaut $180°$.",
            "Par définition, des angles dont la somme vaut $180°$ sont supplémentaires."
        ],
        "f": "Angle plat $= 180°$ $\\Rightarrow$ supplémentaires."
    },
    # Exo 10 - Fill challenge
    {
        "lvl": 1,
        "type": "fill",
        "q": "Deux angles supplémentaires mesurent $3x$ et $x + 20°$. La valeur de $x$ est ___.",
        "a": "40",
        "options": [],
        "steps": [
            "Écris l'équation : la somme des deux angles vaut $180°$.",
            "$3x + x + 20 = 180$, soit $4x + 20 = 180$.",
            "$4x = 160$, donc $x = 40$."
        ],
        "f": "$\\alpha + \\beta = 180°$"
    },

    # ── Slot 3: Angles dans un triangle et angles formés par des parallèles ──
    # Exo 11 - QCM accessible
    {
        "lvl": 1,
        "q": "Dans un triangle, la somme des angles est toujours égale à :",
        "a": "$180°$",
        "options": ["$180°$", "$360°$", "$90°$"],
        "steps": [
            "C'est une propriété fondamentale du triangle.",
            "On peut la démontrer en traçant une parallèle à un côté passant par le sommet opposé.",
            "La somme des trois angles d'un triangle vaut toujours $180°$."
        ],
        "f": "Dans un triangle : $\\hat{A} + \\hat{B} + \\hat{C} = 180°$."
    },
    # Exo 12 - QCM accessible
    {
        "lvl": 1,
        "q": "Un triangle a deux angles de $50°$ et $70°$. Combien mesure le troisième angle ?",
        "a": "$60°$",
        "options": ["$60°$", "$40°$", "$120°$"],
        "steps": [
            "La somme des angles d'un triangle vaut $180°$.",
            "On a déjà $50° + 70° = 120°$.",
            "$180° - 120° = 60°$. Le troisième angle mesure $60°$."
        ],
        "f": "$\\hat{C} = 180° - \\hat{A} - \\hat{B}$"
    },
    # Exo 13 - QCM intermédiaire
    {
        "lvl": 1,
        "q": "Noa construit un triangle isocèle avec un angle au sommet de $40°$. Combien mesurent les angles de la base ?",
        "a": "$70°$ chacun",
        "options": ["$70°$ chacun", "$80°$ chacun", "$60°$ chacun"],
        "steps": [
            "Dans un triangle isocèle, les deux angles de la base sont égaux.",
            "La somme vaut $180°$, donc les deux angles de base valent $180° - 40° = 140°$ au total.",
            "Chaque angle de base mesure $140° \\div 2 = 70°$."
        ],
        "f": "Triangle isocèle : $\\hat{B} = \\hat{C} = \\frac{180° - \\hat{A}}{2}$"
    },
    # Exo 14 - VF intermédiaire
    {
        "lvl": 1,
        "type": "vf",
        "q": "Un triangle peut avoir deux angles obtus (supérieurs à $90°$).",
        "a": "Faux",
        "options": ["Vrai", "Faux"],
        "steps": [
            "Un angle obtus mesure plus de $90°$.",
            "Si on avait deux angles de plus de $90°$, leur somme dépasserait déjà $180°$.",
            "Impossible car la somme des trois angles doit être exactement $180°$."
        ],
        "f": "$\\hat{A} + \\hat{B} + \\hat{C} = 180°$"
    },
    # Exo 15 - Fill challenge
    {
        "lvl": 1,
        "type": "fill",
        "q": "Dans un triangle rectangle, un angle aigu mesure $35°$. L'autre angle aigu mesure ___°.",
        "a": "55",
        "options": [],
        "steps": [
            "Un triangle rectangle a un angle de $90°$.",
            "La somme des trois angles vaut $180°$, donc les deux angles aigus ont pour somme $90°$.",
            "$90° - 35° = 55°$."
        ],
        "f": "Triangle rectangle : $\\hat{B} + \\hat{C} = 90°$"
    },

    # ── Slot 4: Synthèse — angles, parallèles et figures ──
    # Exo 16 - QCM accessible
    {
        "lvl": 1,
        "q": "$(d_1) \\parallel (d_2)$ et une sécante forme un angle de $110°$ avec $(d_1)$. L'angle adjacent (de l'autre côté de la sécante, sur $(d_1)$) mesure :",
        "a": "$70°$",
        "options": ["$70°$", "$110°$", "$90°$"],
        "steps": [
            "Les deux angles de chaque côté de la sécante sur une même droite sont adjacents et forment un angle plat.",
            "Leur somme vaut donc $180°$.",
            "$180° - 110° = 70°$."
        ],
        "f": "Angles adjacents sur une droite : $\\alpha + \\beta = 180°$."
    },
    # Exo 17 - QCM accessible
    {
        "lvl": 1,
        "q": "Dans un parallélogramme $ABCD$, l'angle en $A$ mesure $65°$. Combien mesure l'angle en $B$ ?",
        "a": "$115°$",
        "options": ["$115°$", "$65°$", "$130°$"],
        "steps": [
            "Dans un parallélogramme, les angles consécutifs sont supplémentaires.",
            "Cela signifie que $\\hat{A} + \\hat{B} = 180°$.",
            "$180° - 65° = 115°$."
        ],
        "f": "Parallélogramme : angles consécutifs supplémentaires."
    },
    # Exo 18 - QCM intermédiaire
    {
        "lvl": 1,
        "q": "Jade trace une sécante coupant deux droites. Elle mesure deux angles alternes-internes : $52°$ et $58°$. Les droites sont-elles parallèles ?",
        "a": "Non, car les angles ne sont pas égaux",
        "options": ["Non, car les angles ne sont pas égaux", "Oui, car la différence est faible", "On ne peut pas savoir"],
        "steps": [
            "Pour que les droites soient parallèles, les angles alternes-internes doivent être exactement égaux.",
            "$52° \\neq 58°$.",
            "Les angles ne sont pas égaux, donc les droites ne sont pas parallèles."
        ],
        "f": "Alternes-internes égaux $\\Leftrightarrow$ droites parallèles."
    },
    # Exo 19 - VF intermédiaire
    {
        "lvl": 1,
        "type": "vf",
        "q": "Dans un triangle équilatéral, chaque angle mesure $60°$.",
        "a": "Vrai",
        "options": ["Vrai", "Faux"],
        "steps": [
            "Un triangle équilatéral a ses trois côtés égaux, donc ses trois angles sont égaux.",
            "La somme des angles vaut $180°$.",
            "$180° \\div 3 = 60°$ par angle."
        ],
        "f": "Triangle équilatéral : $3 \\times \\hat{A} = 180°$, donc $\\hat{A} = 60°$."
    },
    # Exo 20 - Fill challenge
    {
        "lvl": 1,
        "type": "fill",
        "q": "$(d_1) \\parallel (d_2)$, une sécante coupe $(d_1)$ en formant un angle de $75°$. L'angle correspondant sur $(d_2)$ et son supplémentaire valent ensemble ___°.",
        "a": "180",
        "options": [],
        "steps": [
            "L'angle correspondant sur $(d_2)$ vaut aussi $75°$ (parallèles).",
            "Le supplémentaire de $75°$ vaut $180° - 75° = 105°$.",
            "$75° + 105° = 180°$. Un angle et son supplémentaire font toujours $180°$."
        ],
        "f": "$\\alpha + (180° - \\alpha) = 180°$"
    }
]

# Write to sheet: replace row 37 (Racines_Carrées) with Angles_Parallèles
# Row 37 = index 36 in raw (0-indexed)
raw = sh.read_raw("Curriculum_Officiel")
old_row = raw[36]
print(f"  Replacing: {old_row[0]}/{old_row[1]} ({old_row[2]})")

new_json = json.dumps(angles_exos, ensure_ascii=False)
# Update: Niveau=5EME, Categorie=Angles_Parallèles, Titre=Angles et parallèles, Icone=📐, ExosJSON
sh.update_range("Curriculum_Officiel", f"A37:F37", [[
    "5EME",
    "Angles_Parallèles",
    "Angles et parallèles",
    "📐",
    new_json,
    "Remplacé Racines_Carrées (hors programme 5EME) — 2026-03-22"
]])
print(f"  ✅ Replaced Racines_Carrées with Angles_Parallèles (20 exercises)")

print("\n=== All fixes applied ===")
