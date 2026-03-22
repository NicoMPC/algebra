#!/usr/bin/env python3
"""
Correcteur qualité exercices 5EME — applique TOUTES les corrections P1/P2.
Usage: python3 fix_exos_5eme.py [--dry-run]
"""

import json, sys, re, copy
from sheets import sh

DRY_RUN = '--dry-run' in sys.argv

# ──────────────────────────────────────────────────────────────────────────────
# LOAD ALL 5EME DATA
# ──────────────────────────────────────────────────────────────────────────────

def load_tab(tab):
    """Returns {categorie: (row_index_1based, exos_list)} for 5EME rows."""
    raw = sh.read_raw(tab)
    headers = raw[0]
    niveau_col = headers.index("Niveau")
    cat_col = headers.index("Categorie")
    json_col = headers.index("ExosJSON")
    result = {}
    for i, row in enumerate(raw[1:], start=2):  # 1-based row in sheet
        if len(row) > niveau_col and row[niveau_col] == "5EME":
            cat = row[cat_col]
            exos = json.loads(row[json_col])
            result[cat] = (i, json_col + 1, exos)  # row_num, col_num (1-based), exos
    return result

print("Loading data...")
curriculum = load_tab("Curriculum_Officiel")
boost = load_tab("BoostExos")
diag = load_tab("DiagnosticExos")

changes_log = []

def log(tab, cat, idx, what):
    changes_log.append(f"  {tab}/{cat} #{idx+1}: {what}")

# ──────────────────────────────────────────────────────────────────────────────
# P1 — STEP 1 QUI DONNE LA RÉPONSE (14 exos)
# ──────────────────────────────────────────────────────────────────────────────

def fix_step1_answer():
    """Fix step1 that gives away the answer."""

    # Curriculum Fractions #17 (idx 16)
    e = curriculum["Fractions"][2][16]
    e["steps"][0] = "Pour multiplier des fractions, on multiplie les numérateurs entre eux et les dénominateurs entre eux."
    log("Curriculum", "Fractions", 16, "step1: méthode multiplication sans donner résultat")

    # Curriculum Nombres_relatifs #6 (idx 5)
    e = curriculum["Nombres_relatifs"][2][5]
    e["steps"][0] = "Convertis chaque valeur en distance par rapport à la surface : plus le nombre est proche de $0$, plus le plongeur est près de la surface."
    log("Curriculum", "Nombres_relatifs", 5, "step1: guide méthode comparaison sans résultat")

    # Curriculum Pythagore #12 (idx 11)
    e = curriculum["Pythagore"][2][11]
    e["steps"][0] = "Un triplet pythagoricien vérifie $a^2 + b^2 = c^2$. Calcule $3^2 + 4^2$ et cherche quel entier a ce carré."
    log("Curriculum", "Pythagore", 11, "step1: guide méthode triplet sans résultat")

    # Curriculum Calcul_Littéral #11 (idx 10)
    e = curriculum["Calcul_Littéral"][2][10]
    e["steps"][0] = "Regroupe les termes en $x$ d'un côté : identifie les coefficients de $x$ dans $4x$ et $2x$."
    log("Curriculum", "Calcul_Littéral", 10, "step1: guide regroupement sans résultat")

    # Curriculum Symétrie_Centrale #16 (idx 15)
    e = curriculum["Symétrie_Centrale"][2][15]
    e["steps"][0] = "Si $E$ est le symétrique de $F$ par rapport à $O$, alors $O$ est le milieu de $[EF]$. Utilise la formule $F = 2O - E$."
    log("Curriculum", "Symétrie_Centrale", 15, "step1: guide formule sans résultat")

    # Curriculum Symétrie_Centrale #19 (idx 18)
    e = curriculum["Symétrie_Centrale"][2][18]
    e["steps"][0] = "Cherche quelle figure se superpose à elle-même après une rotation de $180°$ ET possède au moins un axe de symétrie."
    log("Curriculum", "Symétrie_Centrale", 18, "step1: guide critère sans résultat")

    # Curriculum Transformations #2 (idx 1)
    e = curriculum["Transformations"][2][1]
    e["steps"][0] = "Cherche la transformation qui déplace chaque point dans la même direction, le même sens et la même distance, sans rotation."
    log("Curriculum", "Transformations", 1, "step1: guide définition sans résultat")

    # Curriculum Transformations #3 (idx 2)
    e = curriculum["Transformations"][2][2]
    e["steps"][0] = "Le vecteur de translation se calcule en soustrayant les coordonnées du point de départ à celles du point d'arrivée : $\\vec{v} = B - A$."
    log("Curriculum", "Transformations", 2, "step1: guide méthode vecteur sans résultat")

    # Curriculum Racines_Carrées #11 (idx 10)
    e = curriculum["Racines_Carrées"][2][10]
    e["steps"][0] = "Décompose $72$ en un produit d'un carré parfait par un autre entier : cherche le plus grand carré parfait qui divise $72$."
    log("Curriculum", "Racines_Carrées", 10, "step1: guide décomposition sans résultat")

    # Curriculum Racines_Carrées #19 (idx 18)
    e = curriculum["Racines_Carrées"][2][18]
    e["steps"][0] = "Par définition, $\\sqrt{a}$ est le nombre positif dont le carré vaut $a$. Que vaut $(\\sqrt{a})^2$ ?"
    log("Curriculum", "Racines_Carrées", 18, "step1: guide définition sans résultat")

    # BoostExos Nombres_relatifs #1 (idx 0)
    e = boost["Nombres_relatifs"][2][0]
    e["steps"][0] = "Quand on additionne deux nombres de signes différents, on soustrait les valeurs absolues et on garde le signe du plus grand."
    log("Boost", "Nombres_relatifs", 0, "step1: guide méthode sans résultat")

    # BoostExos Symétrie_Centrale #2 (idx 1)
    e = boost["Symétrie_Centrale"][2][1]
    e["steps"][0] = "Dans un parallélogramme, le centre $O$ est le milieu de chaque diagonale. Quel sommet est à l'autre extrémité de la diagonale passant par $B$ ?"
    log("Boost", "Symétrie_Centrale", 1, "step1: guide méthode sans résultat")

    # BoostExos Transformations #1 (idx 0)
    e = boost["Transformations"][2][0]
    e["steps"][0] = "Pour trouver l'image par translation, ajoute chaque composante du vecteur à la coordonnée correspondante du point."
    log("Boost", "Transformations", 0, "step1: guide méthode sans résultat")

    # BoostExos Transformations #2 (idx 1)
    e = boost["Transformations"][2][1]
    e["steps"][0] = "Cherche la transformation géométrique dont la définition implique un centre fixe et un angle de rotation."
    log("Boost", "Transformations", 1, "step1: guide définition sans résultat")

    # BoostExos Transformations #10 (idx 9)
    e = boost["Transformations"][2][9]
    e["steps"][0] = "Pour chaque sommet, ajoute les composantes du vecteur $\\vec{v}(-2, 1)$ aux coordonnées. Commence par $B(4, 0)$."
    log("Boost", "Transformations", 9, "step1: guide méthode sans résultat")

    # DiagnosticExos Racines_Carrées #1 (idx 0)
    e = diag["Racines_Carrées"][2][0]
    e["steps"][0] = "Cherche le nombre entier positif dont le carré vaut $36$. Teste les carrés parfaits : $1, 4, 9, 16, 25, ...$"
    log("Diag", "Racines_Carrées", 0, "step1: guide méthode sans résultat")

fix_step1_answer()

# ──────────────────────────────────────────────────────────────────────────────
# P1 — STEPS GÉNÉRIQUES "Vérifie que ta fraction..." dans Fractions Curriculum
# ──────────────────────────────────────────────────────────────────────────────

def fix_fractions_generic_steps():
    exos = curriculum["Fractions"][2]

    # #1: 1/2 + 1/3
    exos[0]["steps"][2] = "$\\frac{3}{6} + \\frac{2}{6} = \\frac{5}{6}$. La fraction $\\frac{5}{6}$ est déjà irréductible (PGCD de $5$ et $6$ = $1$)."
    log("Curriculum", "Fractions", 0, "step3: calcul concret")

    # #2: 3/4 - 1/3
    exos[1]["steps"][2] = "$\\frac{9}{12} - \\frac{4}{12} = \\frac{5}{12}$. PGCD de $5$ et $12$ = $1$, donc la fraction est irréductible."
    log("Curriculum", "Fractions", 1, "step3: calcul concret")

    # #3: 2/3 + 1/6 — also fix step2 which is wrong
    exos[2]["steps"][1] = "$\\frac{2}{3} = \\frac{4}{6}$. Le dénominateur commun est $6$."
    exos[2]["steps"][2] = "$\\frac{4}{6} + \\frac{1}{6} = \\frac{5}{6}$. PGCD de $5$ et $6$ = $1$, fraction irréductible."
    log("Curriculum", "Fractions", 2, "step2+3: calcul concret corrigé")

    # #4: 5/6 - 1/4 — step2 is also wrong/confusing
    exos[3]["steps"][1] = "PPCM de $6$ et $4$ = $12$. Donc $\\frac{5}{6} = \\frac{10}{12}$ et $\\frac{1}{4} = \\frac{3}{12}$."
    exos[3]["steps"][2] = "$\\frac{10}{12} - \\frac{3}{12} = \\frac{7}{12}$. PGCD de $7$ et $12$ = $1$, fraction irréductible."
    log("Curriculum", "Fractions", 3, "step2+3: calcul concret corrigé")

    # #5: Simplifier 12/16
    exos[4]["steps"][2] = "$\\frac{12 \\div 4}{16 \\div 4} = \\frac{3}{4}$. PGCD de $3$ et $4$ = $1$, c'est bien irréductible."
    log("Curriculum", "Fractions", 4, "step3: calcul concret")

    # #6: Simplifier 15/25
    exos[5]["steps"][2] = "$\\frac{15 \\div 5}{25 \\div 5} = \\frac{3}{5}$. PGCD de $3$ et $5$ = $1$, c'est bien irréductible."
    log("Curriculum", "Fractions", 5, "step3: calcul concret")

    # #14: 5/6 - 1/3 + 1/4 — step2 is wrong
    exos[13]["steps"][1] = "PPCM de $6$, $3$ et $4$ = $12$. Convertis : $\\frac{10}{12} - \\frac{4}{12} + \\frac{3}{12}$."
    exos[13]["steps"][2] = "$\\frac{10 - 4 + 3}{12} = \\frac{9}{12} = \\frac{3}{4}$. Simplifie par $3$."
    log("Curriculum", "Fractions", 13, "step2+3: calcul concret corrigé")

    # #15: Tarte 1/3 + 1/4, reste? — step2 is wrong
    exos[14]["steps"][1] = "PPCM de $3$ et $4$ = $12$. Total mangé : $\\frac{4}{12} + \\frac{3}{12} = \\frac{7}{12}$."
    exos[14]["steps"][2] = "Reste : $1 - \\frac{7}{12} = \\frac{12}{12} - \\frac{7}{12} = \\frac{5}{12}$."
    log("Curriculum", "Fractions", 14, "step2+3: calcul concret corrigé")

    # #17: 1/2 × 2/3 × 3/4 — steps are out of order
    exos[16]["steps"][0] = "Pour multiplier des fractions, on multiplie les numérateurs entre eux et les dénominateurs entre eux."
    exos[16]["steps"][1] = "$\\frac{1 \\times 2 \\times 3}{2 \\times 3 \\times 4} = \\frac{6}{24}$."
    exos[16]["steps"][2] = "Simplifie par $6$ : $\\frac{6}{24} = \\frac{1}{4}$."
    log("Curriculum", "Fractions", 16, "steps: réordonnés et concrets")

    # #20: Cuve 2/3 + 1/4
    exos[19]["steps"][1] = "PPCM de $3$ et $4$ = $12$. Convertis : $\\frac{2}{3} = \\frac{8}{12}$ et $\\frac{1}{4} = \\frac{3}{12}$."
    exos[19]["steps"][2] = "$\\frac{8}{12} + \\frac{3}{12} = \\frac{11}{12}$. La cuve est remplie aux $\\frac{11}{12}$."
    log("Curriculum", "Fractions", 19, "step2+3: calcul concret")

fix_fractions_generic_steps()

# ──────────────────────────────────────────────────────────────────────────────
# P1 — REWRITE ALL BOOSTEXOS STEPS (100 exos) with concrete values
# ──────────────────────────────────────────────────────────────────────────────

def fix_boost_steps():
    """Rewrite ALL BoostExos steps with concrete values from the exercise."""

    # === FRACTIONS ===
    bfrac = boost["Fractions"][2]

    # #1: 2/3 + 1/4
    bfrac[0]["steps"] = [
        "Il faut un dénominateur commun pour $\\frac{2}{3}$ et $\\frac{1}{4}$. Le PPCM de $3$ et $4$ est $12$.",
        "$\\frac{2}{3} = \\frac{8}{12}$ et $\\frac{1}{4} = \\frac{3}{12}$. Additionne les numérateurs.",
        "$\\frac{8}{12} + \\frac{3}{12} = \\frac{11}{12}$."
    ]

    # #2: 3/5 × 2/7
    bfrac[1]["steps"] = [
        "Pour multiplier deux fractions, multiplie numérateurs entre eux et dénominateurs entre eux.",
        "Numérateurs : $3 \\times 2 = 6$. Dénominateurs : $5 \\times 7 = 35$.",
        "Résultat : $\\frac{6}{35}$. Vérifie si c'est simplifiable (PGCD de $6$ et $35$ = $1$)."
    ]

    # #3: Simplifier 12/18
    bfrac[2]["steps"] = [
        "Cherche le PGCD de $12$ et $18$. Les diviseurs communs sont $1, 2, 3, 6$.",
        "Le PGCD est $6$. Divise numérateur et dénominateur par $6$.",
        "$\\frac{12 \\div 6}{18 \\div 6} = \\frac{2}{3}$."
    ]

    # #4: 5/6 - 1/3
    bfrac[3]["steps"] = [
        "Dénominateur commun de $6$ et $3$ : c'est $6$. Convertis $\\frac{1}{3} = \\frac{2}{6}$.",
        "Soustraction : $\\frac{5}{6} - \\frac{2}{6} = \\frac{3}{6}$.",
        "Simplifie par $3$ : $\\frac{3}{6} = \\frac{1}{2}$."
    ]

    # #5: 4/9 × 3
    bfrac[4]["steps"] = [
        "Multiplie le numérateur par $3$ : $\\frac{4 \\times 3}{9} = \\frac{12}{9}$.",
        "Simplifie : PGCD de $12$ et $9$ = $3$.",
        "$\\frac{12 \\div 3}{9 \\div 3} = \\frac{4}{3}$."
    ]

    # #6: 3/4 ÷ 2/5
    bfrac[5]["steps"] = [
        "Diviser par une fraction = multiplier par son inverse. L'inverse de $\\frac{2}{5}$ est $\\frac{5}{2}$.",
        "$\\frac{3}{4} \\times \\frac{5}{2} = \\frac{3 \\times 5}{4 \\times 2} = \\frac{15}{8}$.",
        "PGCD de $15$ et $8$ = $1$, la fraction est irréductible."
    ]

    # #7: 2/3 + 5/4 - 1/6
    bfrac[6]["steps"] = [
        "PPCM de $3$, $4$ et $6$ = $12$. Convertis : $\\frac{8}{12} + \\frac{15}{12} - \\frac{2}{12}$.",
        "Calcule : $\\frac{8 + 15 - 2}{12} = \\frac{21}{12}$.",
        "Simplifie par $3$ : $\\frac{21}{12} = \\frac{7}{4}$."
    ]

    # #8: 7/10 × 5/3
    bfrac[7]["steps"] = [
        "Multiplie numérateurs et dénominateurs : $\\frac{7 \\times 5}{10 \\times 3} = \\frac{35}{30}$.",
        "PGCD de $35$ et $30$ = $5$.",
        "$\\frac{35 \\div 5}{30 \\div 5} = \\frac{7}{6}$."
    ]

    # #9: Inverse de 3/8
    bfrac[8]["steps"] = [
        "L'inverse d'une fraction $\\frac{a}{b}$ s'obtient en échangeant numérateur et dénominateur.",
        "Ici, on échange $3$ (numérateur) et $8$ (dénominateur).",
        "L'inverse de $\\frac{3}{8}$ est $\\frac{8}{3}$."
    ]

    # #10: (2/5)²
    bfrac[9]["steps"] = [
        "Pour mettre une fraction au carré, on met le numérateur et le dénominateur au carré.",
        "$2^2 = 4$ et $5^2 = 25$.",
        "$\\left(\\frac{2}{5}\\right)^2 = \\frac{4}{25}$."
    ]

    for i in range(10):
        log("Boost", "Fractions", i, "steps réécrits avec valeurs concrètes")

    # === NOMBRES_RELATIFS ===
    bnr = boost["Nombres_relatifs"][2]

    # #1: (-3) + 7
    bnr[0]["steps"] = [
        "Quand on additionne deux nombres de signes différents, on soustrait les valeurs absolues et on garde le signe du plus grand.",
        "Valeurs absolues : $|7| = 7$ et $|-3| = 3$. Différence : $7 - 3 = 4$. Le plus grand est positif.",
        "Donc $(-3) + 7 = +4$."
    ]

    # #2: (-5) - 3
    bnr[1]["steps"] = [
        "Soustraire $3$ revient à ajouter $(-3)$ : $(-5) - 3 = (-5) + (-3)$.",
        "Deux négatifs : on additionne les valeurs absolues $5 + 3 = 8$ et on garde le signe $-$.",
        "Donc $(-5) - 3 = -8$."
    ]

    # #3: (-4) × 3
    bnr[2]["steps"] = [
        "Règle des signes : négatif $\\times$ positif = négatif.",
        "Multiplie les valeurs absolues : $4 \\times 3 = 12$.",
        "Résultat négatif : $(-4) \\times 3 = -12$."
    ]

    # #4: 6 + (-9)
    bnr[3]["steps"] = [
        "Ajouter un nombre négatif revient à soustraire : $6 + (-9) = 6 - 9$.",
        "Le négatif a la plus grande valeur absolue ($9 > 6$). Différence : $9 - 6 = 3$.",
        "Résultat négatif : $6 + (-9) = -3$."
    ]

    # #5: (-2) × (-5)
    bnr[4]["steps"] = [
        "Règle des signes : négatif $\\times$ négatif = positif.",
        "Multiplie les valeurs absolues : $2 \\times 5 = 10$.",
        "Résultat positif : $(-2) \\times (-5) = +10$."
    ]

    # #6: (-3) × 4 + (-2) × (-5)
    bnr[5]["steps"] = [
        "Priorité aux multiplications. Calcule chaque produit séparément.",
        "$(-3) \\times 4 = -12$ (règle des signes). $(-2) \\times (-5) = +10$.",
        "Puis additionne : $-12 + 10 = -2$."
    ]

    # #7: (-8) ÷ (-2)
    bnr[6]["steps"] = [
        "Règle des signes : négatif $\\div$ négatif = positif.",
        "Divise les valeurs absolues : $8 \\div 2 = 4$.",
        "Résultat positif : $(-8) \\div (-2) = +4$."
    ]

    # #8: 5 - (-3) + (-7)
    bnr[7]["steps"] = [
        "Soustraire un négatif = ajouter le positif : $5 - (-3) = 5 + 3 = 8$.",
        "Puis : $8 + (-7) = 8 - 7 = 1$.",
        "Résultat : $5 - (-3) + (-7) = 1$."
    ]

    # #9: (-6)²
    bnr[8]["steps"] = [
        "Le carré d'un nombre négatif : $(-6)^2 = (-6) \\times (-6)$.",
        "Négatif $\\times$ négatif = positif. Valeurs absolues : $6 \\times 6 = 36$.",
        "Donc $(-6)^2 = 36$. Attention : $-6^2 = -(6^2) = -36$ (différent !)."
    ]

    # #10: (-2)³
    bnr[9]["steps"] = [
        "Le cube : $(-2)^3 = (-2) \\times (-2) \\times (-2)$.",
        "D'abord : $(-2) \\times (-2) = +4$. Puis $4 \\times (-2) = -8$.",
        "Un exposant impair conserve le signe : $(-2)^3 = -8$."
    ]

    for i in range(10):
        log("Boost", "Nombres_relatifs", i, "steps réécrits avec valeurs concrètes")

    # === PROPORTIONNALITÉ ===
    bprop = boost["Proportionnalité"][2]

    # #1: 4 stylos 6€, prix de 10
    bprop[0]["steps"] = [
        "Calcule le prix d'un stylo : $6 \\div 4 = 1{,}50$ €.",
        "Multiplie par la quantité : $1{,}50 \\times 10 = 15$ €.",
        "Vérifie : $\\frac{6}{4} = \\frac{15}{10} = 1{,}5$. Les rapports sont égaux."
    ]

    # #2: 250g pour 2 pers, pour 5?
    bprop[1]["steps"] = [
        "Calcule la quantité par personne : $250 \\div 2 = 125$ g.",
        "Pour $5$ personnes : $125 \\times 5 = 625$ g.",
        "Vérifie : $\\frac{250}{2} = \\frac{625}{5} = 125$."
    ]

    # #3: v=60 km/h, d en 2h30
    bprop[2]["steps"] = [
        "Convertis $2$ h $30$ min en heures : $2{,}5$ h.",
        "Formule : $d = v \\times t = 60 \\times 2{,}5$.",
        "$60 \\times 2{,}5 = 150$ km."
    ]

    # #4: 20% de 350
    bprop[3]["steps"] = [
        "$20\\%$ signifie $\\frac{20}{100} = 0{,}2$.",
        "Calcule : $350 \\times 0{,}2 = 70$.",
        "Ou bien : $\\frac{350}{5} = 70$ (car $20\\% = \\frac{1}{5}$)."
    ]

    # #5: augmentation 40→50
    bprop[4]["steps"] = [
        "L'augmentation en euros = prix final $-$ prix initial.",
        "$50 - 40 = 10$ €.",
        "L'augmentation est de $10$ €."
    ]

    # #6: % augmentation 80→100
    bprop[5]["steps"] = [
        "Augmentation en euros : $100 - 80 = 20$ €.",
        "Pourcentage : $\\frac{\\text{augmentation}}{\\text{valeur initiale}} \\times 100 = \\frac{20}{80} \\times 100$.",
        "$\\frac{20}{80} = 0{,}25$, soit $25\\%$."
    ]

    # #7: Échelle 1/2000, 8cm
    bprop[6]["steps"] = [
        "Échelle $\\frac{1}{2000}$ signifie $1$ cm sur le plan = $2000$ cm en réalité.",
        "$8 \\times 2000 = 16\\,000$ cm.",
        "Convertis : $16\\,000$ cm $= 160$ m."
    ]

    # #8: 120€ réduction 15%
    bprop[7]["steps"] = [
        "Calcule la réduction : $120 \\times \\frac{15}{100} = 120 \\times 0{,}15 = 18$ €.",
        "Prix final : $120 - 18 = 102$ €.",
        "Ou directement : $120 \\times 0{,}85 = 102$ €."
    ]

    # #9: 45km en 1h30
    bprop[8]["steps"] = [
        "Convertis : $1$ h $30$ min $= 1{,}5$ h.",
        "Vitesse $= \\frac{d}{t} = \\frac{45}{1{,}5}$.",
        "$\\frac{45}{1{,}5} = 30$ km/h."
    ]

    # #10: coeff proportionnalité 3→12, 5→20
    bprop[9]["steps"] = [
        "Le coefficient de proportionnalité $k = \\frac{y}{x}$.",
        "Vérifie : $\\frac{12}{3} = 4$ et $\\frac{20}{5} = 4$. Les rapports sont égaux.",
        "Le coefficient est $k = 4$."
    ]

    for i in range(10):
        log("Boost", "Proportionnalité", i, "steps réécrits avec valeurs concrètes")

    # === PUISSANCES ===
    bpuis = boost["Puissances"][2]

    # #1: 2^4
    bpuis[0]["steps"] = [
        "$2^4$ signifie $2 \\times 2 \\times 2 \\times 2$.",
        "Calcule pas à pas : $2 \\times 2 = 4$, puis $4 \\times 2 = 8$, puis $8 \\times 2 = 16$.",
        "$2^4 = 16$."
    ]

    # #2: 10^3
    bpuis[1]["steps"] = [
        "$10^3$ signifie $10 \\times 10 \\times 10$.",
        "$10 \\times 10 = 100$, puis $100 \\times 10 = 1000$.",
        "$10^3 = 1000$. Astuce : l'exposant indique le nombre de zéros."
    ]

    # #3: 3^3
    bpuis[2]["steps"] = [
        "$3^3$ signifie $3 \\times 3 \\times 3$.",
        "$3 \\times 3 = 9$, puis $9 \\times 3 = 27$.",
        "$3^3 = 27$."
    ]

    # #4: 5^2
    bpuis[3]["steps"] = [
        "$5^2$ signifie $5 \\times 5$.",
        "Calcule : $5 \\times 5 = 25$.",
        "$5^2 = 25$."
    ]

    # #5: 100 000 en puissance de 10
    bpuis[4]["steps"] = [
        "Compte le nombre de zéros dans $100\\,000$.",
        "Il y a $5$ zéros après le $1$.",
        "$100\\,000 = 10^5$."
    ]

    # #6: 2^3 × 2^4
    bpuis[5]["steps"] = [
        "Même base $2$ : on additionne les exposants. $2^3 \\times 2^4 = 2^{3+4} = 2^7$.",
        "Calcule $2^7$ : $128$ (car $2^7 = 2^4 \\times 2^3 = 16 \\times 8$).",
        "$2^3 \\times 2^4 = 128$."
    ]

    # #7: (3^2)^3
    bpuis[6]["steps"] = [
        "Puissance de puissance : on multiplie les exposants. $(3^2)^3 = 3^{2 \\times 3} = 3^6$.",
        "Calcule $3^6$ : $3^3 = 27$, donc $3^6 = 27 \\times 27 = 729$.",
        "$(3^2)^3 = 729$."
    ]

    # #8: 4,5 × 10^3
    bpuis[7]["steps"] = [
        "Multiplier par $10^3$ = décaler la virgule de $3$ rangs vers la droite.",
        "$4{,}5 \\rightarrow 45 \\rightarrow 450 \\rightarrow 4500$.",
        "$4{,}5 \\times 10^3 = 4500$."
    ]

    # #9: 10^6 ÷ 10^2
    bpuis[8]["steps"] = [
        "Même base $10$ : on soustrait les exposants. $10^6 \\div 10^2 = 10^{6-2} = 10^4$.",
        "$10^4 = 10\\,000$.",
        "$10^6 \\div 10^2 = 10\\,000$."
    ]

    # #10: 6 × 10^{-2}
    bpuis[9]["steps"] = [
        "$10^{-2} = \\frac{1}{10^2} = \\frac{1}{100} = 0{,}01$.",
        "$6 \\times 0{,}01 = 0{,}06$. (Décale la virgule de $2$ rangs vers la gauche.)",
        "$6 \\times 10^{-2} = 0{,}06$."
    ]

    for i in range(10):
        log("Boost", "Puissances", i, "steps réécrits avec valeurs concrètes")

    # === PYTHAGORE ===
    bpyth = boost["Pythagore"][2]

    # #1: côtés 3 et 4
    bpyth[0]["steps"] = [
        "Les deux côtés de l'angle droit sont $3$ cm et $4$ cm. L'hypoténuse est le côté le plus long.",
        "Pythagore : $c^2 = 3^2 + 4^2 = 9 + 16 = 25$.",
        "$c = \\sqrt{25} = 5$ cm."
    ]

    # #2: côtés 6 et 8
    bpyth[1]["steps"] = [
        "Côtés de l'angle droit : $6$ cm et $8$ cm. Applique le théorème de Pythagore.",
        "$c^2 = 6^2 + 8^2 = 36 + 64 = 100$.",
        "$c = \\sqrt{100} = 10$ cm."
    ]

    # #3: hyp 13, côté 5
    bpyth[2]["steps"] = [
        "Tu connais l'hypoténuse ($13$ cm) et un côté ($5$ cm). Isole le côté manquant.",
        "$b^2 = 13^2 - 5^2 = 169 - 25 = 144$.",
        "$b = \\sqrt{144} = 12$ cm."
    ]

    # #4: 5² + 12²
    bpyth[3]["steps"] = [
        "Calcule $5^2 + 12^2 = 25 + 144 = 169$.",
        "L'hypoténuse = $\\sqrt{169}$. Cherche quel entier a pour carré $169$.",
        "$\\sqrt{169} = 13$, donc l'hypoténuse mesure $13$ cm."
    ]

    # #5: hyp 10, côté 6
    bpyth[4]["steps"] = [
        "Hypoténuse $= 10$ cm, un côté $= 6$ cm. Formule : $b^2 = c^2 - a^2$.",
        "$b^2 = 10^2 - 6^2 = 100 - 36 = 64$.",
        "$b = \\sqrt{64} = 8$ cm."
    ]

    # #6: côtés 9 et 12
    bpyth[5]["steps"] = [
        "Côtés de l'angle droit : $9$ cm et $12$ cm.",
        "$c^2 = 9^2 + 12^2 = 81 + 144 = 225$.",
        "$c = \\sqrt{225} = 15$ cm."
    ]

    # #7: triangle 7, 24, 25 rectangle?
    bpyth[6]["steps"] = [
        "Vérifie si $7^2 + 24^2 = 25^2$ (le plus grand côté est l'hypoténuse potentielle).",
        "$7^2 + 24^2 = 49 + 576 = 625$. Et $25^2 = 625$.",
        "$625 = 625$ : l'égalité est vérifiée, le triangle est rectangle."
    ]

    # #8: mât 8m, câble à 6m
    bpyth[7]["steps"] = [
        "Le mât ($8$ m), le sol ($6$ m) et le câble forment un triangle rectangle. Le câble est l'hypoténuse.",
        "$c^2 = 8^2 + 6^2 = 64 + 36 = 100$.",
        "$c = \\sqrt{100} = 10$ m."
    ]

    # #9: hyp 17, côté 8
    bpyth[8]["steps"] = [
        "Hypoténuse $= 17$ cm, un côté $= 8$ cm. Isole le côté manquant.",
        "$b^2 = 17^2 - 8^2 = 289 - 64 = 225$.",
        "$b = \\sqrt{225} = 15$ cm."
    ]

    # #10: triangle 5, 6, 8 rectangle?
    bpyth[9]["steps"] = [
        "Le plus grand côté est $8$. Vérifie si $5^2 + 6^2 = 8^2$.",
        "$5^2 + 6^2 = 25 + 36 = 61$. Et $8^2 = 64$.",
        "$61 \\neq 64$ : l'égalité n'est pas vérifiée, le triangle n'est pas rectangle."
    ]

    for i in range(10):
        log("Boost", "Pythagore", i, "steps réécrits avec valeurs concrètes")

    # === CALCUL_LITTÉRAL ===
    bcl = boost["Calcul_Littéral"][2]

    # #1: 3x + 5x
    bcl[0]["steps"] = [
        "Les deux termes ont la même partie littérale $x$. Additionne les coefficients.",
        "$3 + 5 = 8$, donc $3x + 5x = 8x$.",
        "C'est la propriété : $ax + bx = (a+b)x$."
    ]

    # #2: 2(x+4)
    bcl[1]["steps"] = [
        "Développer = multiplier chaque terme entre parenthèses par $2$.",
        "$2 \\times x = 2x$ et $2 \\times 4 = 8$.",
        "Donc $2(x + 4) = 2x + 8$."
    ]

    # #3: 3x pour x=5
    bcl[2]["steps"] = [
        "Remplace $x$ par $5$ dans l'expression $3x$.",
        "$3 \\times 5 = 15$.",
        "Pour $x = 5$, $3x = 15$."
    ]

    # #4: 7a - 3a + 2a
    bcl[3]["steps"] = [
        "Tous les termes ont la même partie littérale $a$. Regroupe les coefficients.",
        "$7 - 3 + 2 = 6$.",
        "Donc $7a - 3a + 2a = 6a$."
    ]

    # #5: 5(2y-1)
    bcl[4]["steps"] = [
        "Développer : multiplie chaque terme par $5$.",
        "$5 \\times 2y = 10y$ et $5 \\times (-1) = -5$.",
        "Donc $5(2y - 1) = 10y - 5$."
    ]

    # #6: 3(2x+1) + 2(x-4)
    bcl[5]["steps"] = [
        "Développe chaque parenthèse : $3(2x+1) = 6x + 3$ et $2(x-4) = 2x - 8$.",
        "Regroupe : $6x + 2x = 8x$ et $3 - 8 = -5$.",
        "$3(2x+1) + 2(x-4) = 8x - 5$."
    ]

    # #7: Factoriser 6x + 9
    bcl[6]["steps"] = [
        "Cherche le PGCD de $6$ et $9$. C'est $3$.",
        "$6x = 3 \\times 2x$ et $9 = 3 \\times 3$.",
        "Donc $6x + 9 = 3(2x + 3)$."
    ]

    # #8: 3x²-4x+1 pour x=-2
    bcl[7]["steps"] = [
        "Remplace $x$ par $-2$ : $3 \\times (-2)^2 - 4 \\times (-2) + 1$.",
        "$3 \\times 4 = 12$, $-4 \\times (-2) = +8$, $+1$.",
        "$12 + 8 + 1 = 21$."
    ]

    # #9: 4x + 3 - 2x + 7
    bcl[8]["steps"] = [
        "Regroupe les termes en $x$ : $4x - 2x = 2x$.",
        "Regroupe les constantes : $3 + 7 = 10$.",
        "Donc $4x + 3 - 2x + 7 = 2x + 10$."
    ]

    # #10: -2(3x - 5)
    bcl[9]["steps"] = [
        "Développer : multiplie chaque terme par $-2$.",
        "$-2 \\times 3x = -6x$ et $-2 \\times (-5) = +10$.",
        "Donc $-2(3x - 5) = -6x + 10$."
    ]

    for i in range(10):
        log("Boost", "Calcul_Littéral", i, "steps réécrits avec valeurs concrètes")

    # === SYMÉTRIE_CENTRALE ===
    bsc = boost["Symétrie_Centrale"][2]

    # #1: P(4,6) par rapport à O(0,0)
    bsc[0]["steps"] = [
        "Par rapport à l'origine $O(0,0)$, le symétrique a les coordonnées opposées.",
        "$x' = -4$ et $y' = -6$.",
        "Donc $P'(-4, -6)$."
    ]

    # #2: parallélogramme ABCD, sym de B par rapport à O
    bsc[1]["steps"] = [
        "Dans un parallélogramme, le centre $O$ est le milieu de chaque diagonale. Quel sommet est à l'autre extrémité de la diagonale passant par $B$ ?",
        "$O$ est le milieu de $[BD]$, donc $B$ et $D$ sont symétriques par rapport à $O$.",
        "Le symétrique de $B$ par rapport à $O$ est $D$."
    ]

    # #3: Q(-7,0) par rapport à O(0,0)
    bsc[2]["steps"] = [
        "Par rapport à $O(0,0)$, on change le signe de chaque coordonnée.",
        "$x' = -(-7) = 7$ et $y' = -(0) = 0$.",
        "Donc $Q'(7, 0)$."
    ]

    # #4: triangle équilatéral centre de symétrie? (vf)
    bsc[3]["steps"] = [
        "Un centre de symétrie signifie que la figure se superpose après rotation de $180°$.",
        "Tourne mentalement un triangle équilatéral de $180°$ : il ne se superpose pas.",
        "Le triangle équilatéral n'a pas de centre de symétrie."
    ]

    # #5: rotation 180° et symétrie centrale
    bsc[4]["steps"] = [
        "La symétrie centrale de centre $O$ est équivalente à une rotation d'un certain angle autour de $O$.",
        "Si un point $M$ a pour image $M'$, alors $O$ est le milieu de $[MM']$ : c'est un demi-tour.",
        "La rotation de $180°$ autour de $O$ est la bonne transformation."
    ]

    # #6: R(2,1) centre O(5,4)
    bsc[5]["steps"] = [
        "Formule : $R' = 2O - R$. Calcule chaque coordonnée séparément.",
        "$x' = 2 \\times 5 - 2 = 8$ et $y' = 2 \\times 4 - 1 = 7$.",
        "Donc $R'(8, 7)$."
    ]

    # #7: T(-3,5) sym T'(7,-1), trouver O
    bsc[6]["steps"] = [
        "$O$ est le milieu de $[TT']$. Utilise la formule du milieu.",
        "$x_O = \\frac{-3 + 7}{2} = \\frac{4}{2} = 2$. $y_O = \\frac{5 + (-1)}{2} = \\frac{4}{2} = 2$.",
        "Donc $O(2, 2)$."
    ]

    # #8: isométrie distances
    bsc[7]["steps"] = [
        "La symétrie centrale est une isométrie : elle conserve toutes les distances.",
        "Si $AB = 5$ cm, alors $A'B' = 5$ cm aussi.",
        "Oui, les longueurs sont conservées."
    ]

    # #9: hexagone régulier
    bsc[8]["steps"] = [
        "L'hexagone régulier possède une symétrie de rotation d'ordre $6$ (rotation de $60°$).",
        "Une rotation de $180°$ (= $3 \\times 60°$) le ramène sur lui-même.",
        "Son centre géométrique est donc un centre de symétrie."
    ]

    # #10: U(0,3) U'(4,-1) trouver O
    bsc[9]["steps"] = [
        "$O$ est le milieu de $[UU']$.",
        "$x_O = \\frac{0 + 4}{2} = 2$. $y_O = \\frac{3 + (-1)}{2} = 1$.",
        "Donc $O(2, 1)$."
    ]

    for i in range(10):
        log("Boost", "Symétrie_Centrale", i, "steps réécrits avec valeurs concrètes")

    # === TRANSFORMATIONS ===
    btr = boost["Transformations"][2]

    # #1: P(0,5) translaté par (2,-3)
    btr[0]["steps"] = [
        "Pour trouver l'image par translation, ajoute chaque composante du vecteur à la coordonnée correspondante du point.",
        "$x' = 0 + 2 = 2$ et $y' = 5 + (-3) = 2$.",
        "Donc $P'(2, 2)$."
    ]

    # #2: rotation def
    btr[1]["steps"] = [
        "Cherche la transformation géométrique dont la définition implique un centre fixe et un angle de rotation.",
        "Tous les points décrivent des arcs de cercle de même angle autour du centre.",
        "C'est la rotation."
    ]

    # #3: sym centrale Q(-4,2) centre O(0,0)
    btr[2]["steps"] = [
        "Symétrie centrale de centre $O(0,0)$ : on inverse le signe des deux coordonnées.",
        "$x' = -(-4) = 4$ et $y' = -(2) = -2$.",
        "Donc $Q'(4, -2)$."
    ]

    # #4: M(6,4) rotation 180° centre O(0,0)
    btr[3]["steps"] = [
        "Rotation de $180°$ autour de $O(0,0)$ = symétrie centrale.",
        "$x' = -6$ et $y' = -4$.",
        "Donc $M'(-6, -4)$."
    ]

    # #5: translation conserve orientation
    btr[4]["steps"] = [
        "La translation déplace tous les points dans la même direction et le même sens.",
        "L'ordre des sommets est conservé (isométrie directe).",
        "Oui, la translation conserve l'orientation."
    ]

    # #6: N(2,1) translaté par (-3,2) puis rotation 90°
    btr[5]["steps"] = [
        "Étape 1 — Translation : $N'(2 + (-3),\\; 1 + 2) = N'(-1, 3)$.",
        "Étape 2 — Rotation $90°$ anti-horaire autour de l'origine : $(x, y) \\to (-y, x)$.",
        "$N''(-3, -1)$."
    ]

    # #7: carré périmètre 24 + symétrie axiale
    btr[6]["steps"] = [
        "La symétrie axiale est une isométrie : elle conserve toutes les longueurs.",
        "Si chaque côté mesure $24 \\div 4 = 6$ cm, chaque côté image mesure aussi $6$ cm.",
        "Le périmètre image est $24$ cm."
    ]

    # #8: sym centrale R(3,5) centre I(1,2)
    btr[7]["steps"] = [
        "Formule : $R' = 2I - R$. Calcule chaque coordonnée.",
        "$x' = 2 \\times 1 - 3 = -1$ et $y' = 2 \\times 2 - 5 = -1$.",
        "Donc $R'(-1, -1)$."
    ]

    # #9: point T à 5cm du centre, rotation
    btr[8]["steps"] = [
        "La rotation conserve les distances au centre : $OT = OT'$.",
        "$T$ est à $5$ cm du centre, donc $T'$ aussi.",
        "La distance au centre reste $5$ cm, quel que soit l'angle."
    ]

    # #10: triangle ABC translaté par (-2,1), coordonnées de B'
    btr[9]["steps"] = [
        "Pour chaque sommet, ajoute les composantes du vecteur $\\vec{v}(-2, 1)$ aux coordonnées. Commence par $B(4, 0)$.",
        "$x_{B'} = 4 + (-2) = 2$ et $y_{B'} = 0 + 1 = 1$.",
        "Donc $B'(2, 1)$."
    ]

    for i in range(10):
        log("Boost", "Transformations", i, "steps réécrits avec valeurs concrètes")

    # === RACINES_CARRÉES ===
    brc = boost["Racines_Carrées"][2]

    # #1: √25
    brc[0]["steps"] = [
        "Cherche le nombre entier positif dont le carré vaut $25$.",
        "Teste : $5^2 = 25$. C'est le bon !",
        "$\\sqrt{25} = 5$."
    ]

    # #2: √81
    brc[1]["steps"] = [
        "Cherche le nombre positif dont le carré vaut $81$.",
        "Teste : $9^2 = 81$.",
        "$\\sqrt{81} = 9$."
    ]

    # #3: encadrer √10
    brc[2]["steps"] = [
        "Cherche les deux carrés parfaits qui entourent $10$ : $9 < 10 < 16$.",
        "$3^2 = 9$ et $4^2 = 16$. Donc $3 < \\sqrt{10} < 4$.",
        "Encadrement : $3 < \\sqrt{10} < 4$."
    ]

    # #4: carré parfait parmi des nombres
    brc[3]["steps"] = [
        "Un carré parfait est un nombre qui est le carré d'un entier : $1, 4, 9, 16, 25, 36, ...$",
        "Teste : $12^2 = 144$. Est-ce parmi les propositions ?",
        "$144$ est un carré parfait ($12^2$)."
    ]

    # #5: aire 100m², côté
    brc[4]["steps"] = [
        "L'aire d'un carré = côté$^2$. Donc côté $= \\sqrt{\\text{aire}}$.",
        "Côté $= \\sqrt{100}$. Quel entier a pour carré $100$ ?",
        "$10^2 = 100$, donc le côté mesure $10$ m."
    ]

    # #6: √(16×9)
    brc[5]["steps"] = [
        "Propriété : $\\sqrt{a \\times b} = \\sqrt{a} \\times \\sqrt{b}$.",
        "$\\sqrt{16} = 4$ et $\\sqrt{9} = 3$. Donc $\\sqrt{16 \\times 9} = 4 \\times 3$.",
        "$4 \\times 3 = 12$."
    ]

    # #7: triangle rectangle 5 et 12
    brc[6]["steps"] = [
        "Pythagore : hypoténuse$^2 = 5^2 + 12^2$.",
        "$25 + 144 = 169$. L'hypoténuse $= \\sqrt{169}$.",
        "$\\sqrt{169} = 13$ cm."
    ]

    # #8: encadrer √40
    brc[7]["steps"] = [
        "Cherche les carrés parfaits qui entourent $40$ : $36 < 40 < 49$.",
        "$6^2 = 36$ et $7^2 = 49$.",
        "Donc $6 < \\sqrt{40} < 7$."
    ]

    # #9: aire 50cm², encadrer côté
    brc[8]["steps"] = [
        "Côté $= \\sqrt{50}$. Cherche les carrés parfaits autour de $50$.",
        "$49 < 50 < 64$, donc $7 < \\sqrt{50} < 8$.",
        "Le côté est entre $7$ cm et $8$ cm."
    ]

    # #10: (√5)² + (√3)²
    brc[9]["steps"] = [
        "Par définition, $(\\sqrt{a})^2 = a$.",
        "$(\\sqrt{5})^2 = 5$ et $(\\sqrt{3})^2 = 3$.",
        "$5 + 3 = 8$."
    ]

    for i in range(10):
        log("Boost", "Racines_Carrées", i, "steps réécrits avec valeurs concrètes")

    # === TRIANGLES_SEMBLABLES ===
    bts = boost["Triangles_Semblables"][2]

    # #1: k=3, petit côté 4cm
    bts[0]["steps"] = [
        "Triangles semblables de rapport $k = 3$ : le grand côté $= k \\times$ petit côté.",
        "$3 \\times 4 = 12$ cm.",
        "Le côté correspondant du grand triangle mesure $12$ cm."
    ]

    # #2: angles 50,60,70 et 50,60,70
    bts[1]["steps"] = [
        "Deux triangles sont semblables si leurs angles sont les mêmes (critère AA).",
        "Premier : $50°, 60°, 70°$. Second : $50°, 60°, 70°$. Les trois angles sont identiques.",
        "Oui, ils sont semblables (critère AA)."
    ]

    # #3: k=1/4, BC=20cm
    bts[2]["steps"] = [
        "Le rapport $k = \\frac{1}{4}$ relie le petit au grand triangle.",
        "$EF = k \\times BC = \\frac{1}{4} \\times 20 = 5$ cm.",
        "Le côté correspondant mesure $5$ cm."
    ]

    # #4: rapport périmètres si k=5
    bts[3]["steps"] = [
        "Les périmètres de triangles semblables ont le même rapport $k$ que les côtés.",
        "Si $k = 5$, le rapport des périmètres est aussi $5$.",
        "Rapport des périmètres = $5$."
    ]

    # #5: k=1, comment appelle-t-on
    bts[4]["steps"] = [
        "$k = 1$ signifie que tous les côtés correspondants sont égaux.",
        "Même forme ET même taille = mêmes triangles.",
        "On les appelle congruents (isométriques)."
    ]

    # #6: côtés 6 et 9, rapport aires
    bts[5]["steps"] = [
        "Rapport de similitude $k = \\frac{6}{9} = \\frac{2}{3}$.",
        "Le rapport des aires = $k^2 = \\left(\\frac{2}{3}\\right)^2 = \\frac{4}{9}$.",
        "Le rapport des aires est $\\frac{4}{9}$."
    ]

    # #7: ombre 1,5m→2m, bâtiment→30m
    bts[6]["steps"] = [
        "L'objet et le bâtiment forment des triangles semblables (mêmes angles avec le sol).",
        "Rapport : $\\frac{\\text{hauteur}}{\\text{ombre}}$ est constant. $\\frac{1{,}5}{2} = \\frac{h}{30}$.",
        "$h = \\frac{1{,}5 \\times 30}{2} = \\frac{45}{2} = 22{,}5$ m."
    ]

    # #8: périmètres 12 et 18, rapport aires
    bts[7]["steps"] = [
        "Rapport de similitude $k = \\frac{12}{18} = \\frac{2}{3}$.",
        "Rapport des aires = $k^2 = \\left(\\frac{2}{3}\\right)^2 = \\frac{4}{9}$.",
        "Le rapport des aires est $\\frac{4}{9}$."
    ]

    # #9: aire DEF=25cm², k=3
    bts[8]["steps"] = [
        "Le rapport des aires = $k^2 = 3^2 = 9$.",
        "Aire GHI $= 9 \\times$ Aire DEF $= 9 \\times 25 = 225$ cm².",
        "L'aire de GHI est $225$ cm²."
    ]

    # #10: Thalès AD/AB = 2/5
    bts[9]["steps"] = [
        "$\\frac{AD}{AB} = \\frac{AE}{AC} = \\frac{2}{5}$ : les rapports sont égaux.",
        "Par la réciproque de Thalès : $(DE) \\parallel (BC)$.",
        "Angle $A$ commun + $DE \\parallel BC$ : les triangles $ADE$ et $ABC$ sont semblables."
    ]

    for i in range(10):
        log("Boost", "Triangles_Semblables", i, "steps réécrits avec valeurs concrètes")

fix_boost_steps()

# ──────────────────────────────────────────────────────────────────────────────
# P2 — FORMULES SPÉCIFIQUES → GÉNÉRALES
# ──────────────────────────────────────────────────────────────────────────────

def fix_specific_formulas():
    # Curriculum Symétrie_Centrale #3, #5, #16, #18
    sc = curriculum["Symétrie_Centrale"][2]
    sc[2]["f"] = "$M' = 2O - M$"
    sc[4]["f"] = "$M' = 2O - M$"
    sc[15]["f"] = "$M' = 2O - M$"
    sc[17]["f"] = "$M' = 2O - M$"
    for i in [2,4,15,17]:
        log("Curriculum", "Symétrie_Centrale", i, "f: formule générale $M' = 2O - M$")

    # Boost Symétrie_Centrale #1, #6
    bsc = boost["Symétrie_Centrale"][2]
    bsc[0]["f"] = "$M' = 2O - M$"
    bsc[5]["f"] = "$M' = 2O - M$"
    for i in [0,5]:
        log("Boost", "Symétrie_Centrale", i, "f: formule générale $M' = 2O - M$")

    # Boost Transformations #1, #10
    btr = boost["Transformations"][2]
    btr[0]["f"] = "$M'(x + a,\\; y + b)$"
    btr[9]["f"] = "$M'(x + a,\\; y + b)$"
    for i in [0,9]:
        log("Boost", "Transformations", i, "f: formule générale translation")

    # Boost Racines_Carrées #1, #2, #3, #5, #7
    brc = boost["Racines_Carrées"][2]
    brc[0]["f"] = "$\\sqrt{a^2} = a$ pour $a \\geq 0$"
    brc[1]["f"] = "$\\sqrt{a^2} = a$ pour $a \\geq 0$"
    brc[2]["f"] = "$n^2 < a < (n+1)^2 \\Rightarrow n < \\sqrt{a} < n+1$"
    brc[4]["f"] = "$c = \\sqrt{\\text{Aire}}$"
    brc[6]["f"] = "$c = \\sqrt{a^2 + b^2}$ (Pythagore)"
    for i in [0,1,2,4,6]:
        log("Boost", "Racines_Carrées", i, "f: formule générale")

fix_specific_formulas()

# ──────────────────────────────────────────────────────────────────────────────
# P2 — FORMULES SANS $...$ → ENCAPSULER EN LATEX
# ──────────────────────────────────────────────────────────────────────────────

def fix_formula_latex():
    """Wrap all formulas that contain math but no $ delimiters."""
    count = 0
    for name, data in [("Curriculum", curriculum), ("Boost", boost), ("Diag", diag)]:
        for cat, (row, col, exos) in data.items():
            for i, e in enumerate(exos):
                f = e.get("f", "")
                if f and "$" not in f:
                    # Check if it has math content
                    if any(c in f for c in "=+\\^") or "sqrt" in f or "frac" in f or "text" in f:
                        e["f"] = f"${f}$"
                        count += 1
                        log(name, cat, i, f"f: encapsulé dans $...$")
    print(f"  Formulas wrapped in $: {count}")

fix_formula_latex()

# ──────────────────────────────────────────────────────────────────────────────
# P2 — HARMONISER À 3 OPTIONS QCM
# ──────────────────────────────────────────────────────────────────────────────

def fix_options_to_3():
    """For QCM exercises with 4 options, remove the least plausible distractor."""
    count = 0

    # Categories that need harmonization per the task:
    # Curriculum: Symétrie_Centrale, Transformations, Racines_Carrées, Triangles_Semblables
    # ALL BoostExos and ALL DiagnosticExos

    curriculum_cats_to_fix = {"Symétrie_Centrale", "Transformations", "Racines_Carrées", "Triangles_Semblables"}

    for name, data, cats_filter in [
        ("Curriculum", curriculum, curriculum_cats_to_fix),
        ("Boost", boost, None),  # All categories
        ("Diag", diag, None),    # All categories
    ]:
        for cat, (row, col, exos) in data.items():
            if cats_filter and cat not in cats_filter:
                continue
            for i, e in enumerate(exos):
                typ = e.get("type", "")
                if typ in ("vf", "fill"):
                    continue
                opts = e.get("options", [])
                if len(opts) != 4:
                    continue

                answer = e["a"]
                # Find the answer index
                ans_idx = None
                for j, o in enumerate(opts):
                    if o == answer or o.strip() == answer.strip():
                        ans_idx = j
                        break

                if ans_idx is None:
                    # Answer might be formatted differently, try to find it
                    for j, o in enumerate(opts):
                        # Strip $ and whitespace for comparison
                        o_clean = o.replace("$", "").strip()
                        a_clean = answer.replace("$", "").strip()
                        if o_clean == a_clean:
                            ans_idx = j
                            break

                if ans_idx is None:
                    print(f"  WARNING: answer '{answer}' not found in options of {name}/{cat} #{i+1}: {opts}")
                    continue

                # Remove the last distractor that is NOT the answer
                # Strategy: remove the option furthest from the answer (least plausible)
                # Simple heuristic: remove the last non-answer option
                removed_idx = None
                for j in range(len(opts) - 1, -1, -1):
                    if j != ans_idx:
                        removed_idx = j
                        break

                if removed_idx is not None:
                    removed = opts.pop(removed_idx)
                    count += 1
                    log(name, cat, i, f"options: 4→3 (retiré '{removed[:30]}')")

    print(f"  Exercises harmonized to 3 options: {count}")

fix_options_to_3()

# ──────────────────────────────────────────────────────────────────────────────
# P2 — UNITÉS INCOHÉRENTES PYTHAGORE
# ──────────────────────────────────────────────────────────────────────────────

def fix_pythagore_units():
    pyth = curriculum["Pythagore"][2]

    # #1: "5 cm" → "5 m" (and options)
    pyth[0]["a"] = "$5$ m"
    pyth[0]["options"] = [o.replace("cm", "m") for o in pyth[0]["options"]]
    log("Curriculum", "Pythagore", 0, "a + options: cm → m")

    # #3: "10 cm" → "10 m" (and options)
    pyth[2]["a"] = "$10$ m"
    pyth[2]["options"] = [o.replace("cm", "m") for o in pyth[2]["options"]]
    log("Curriculum", "Pythagore", 2, "a + options: cm → m")

fix_pythagore_units()

# ──────────────────────────────────────────────────────────────────────────────
# VERIFY: answer still in options
# ──────────────────────────────────────────────────────────────────────────────

def verify():
    errors = 0
    for name, data in [("Curriculum", curriculum), ("Boost", boost), ("Diag", diag)]:
        for cat, (row, col, exos) in data.items():
            for i, e in enumerate(exos):
                typ = e.get("type", "")
                if typ in ("vf", "fill"):
                    continue
                opts = e.get("options", [])
                answer = e["a"]
                found = False
                for o in opts:
                    if o == answer or o.strip() == answer.strip():
                        found = True
                        break
                    o_clean = o.replace("$", "").strip()
                    a_clean = answer.replace("$", "").strip()
                    if o_clean == a_clean:
                        found = True
                        break
                if not found:
                    print(f"  ERROR: answer '{answer}' not in options of {name}/{cat} #{i+1}: {opts}")
                    errors += 1
    print(f"  Verification: {errors} error(s)")
    return errors == 0

print("\nVerifying...")
ok = verify()

# ──────────────────────────────────────────────────────────────────────────────
# WRITE BACK TO SHEET
# ──────────────────────────────────────────────────────────────────────────────

if not ok:
    print("\n❌ Errors found, aborting write.")
    sys.exit(1)

if DRY_RUN:
    print(f"\n🔍 DRY RUN — {len(changes_log)} changes would be applied:")
    for c in changes_log:
        print(c)
    sys.exit(0)

print(f"\nWriting {len(changes_log)} changes to sheets...")

for name, data, tab in [
    ("Curriculum", curriculum, "Curriculum_Officiel"),
    ("Boost", boost, "BoostExos"),
    ("Diag", diag, "DiagnosticExos"),
]:
    for cat, (row_num, col_num, exos) in data.items():
        json_str = json.dumps(exos, ensure_ascii=False)
        sh.update_cell(tab, row_num, col_num, json_str)
        print(f"  ✅ {tab}/{cat} (row {row_num})")

print(f"\n✅ Done! {len(changes_log)} corrections applied.")
print("\nRésumé des corrections :")
for c in changes_log:
    print(c)
