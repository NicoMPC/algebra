"""Fix 4EME exercise issues in Curriculum_Officiel:
1. Puissances exo 8: hectomètres → mètres
2. Fonctions_Linéaires → Statistiques (20 new exercises)
"""
import json
from sheets import sh

# ── 1. Fix Puissances exo 8 ──────────────────────────────────────────────────
raw = sh.read_raw('Curriculum_Officiel')
headers = raw[0]

# Puissances is row 15 (index 14)
puissances_row_idx = 14
exos_col = headers.index('ExosJSON')  # should be 4

puissances_exos = json.loads(raw[puissances_row_idx][exos_col])
old_q = puissances_exos[7]['q']
assert 'hectomètres' in old_q, f"Expected hectomètres in exo 8, got: {old_q}"

# Paris-NY ≈ 5800 km = 5,800,000 m = 5.8 × 10^6 m
puissances_exos[7] = {
    "lvl": 1,
    "q": "La distance Paris-New York est d'environ $5{,}8 \\times 10^6$ mètres. Convertir en écriture décimale.",
    "a": "$5\\,800\\,000$",
    "options": [
        "$580\\,000$",
        "$5\\,800\\,000$",
        "$58\\,000\\,000$"
    ],
    "steps": [
        "$5{,}8 \\times 10^6$ : on déplace la virgule de $6$ rangs vers la droite.",
        "$5{,}8 \\to 58 \\to 580 \\to 5\\,800 \\to 58\\,000 \\to 580\\,000 \\to 5\\,800\\,000$.",
        "$= 5\\,800\\,000$ mètres, soit $5\\,800$ km."
    ],
    "f": "$\\times 10^n$ = décaler la virgule de $n$ rangs vers la droite"
}

sh.update_cell('Curriculum_Officiel', puissances_row_idx + 1, exos_col + 1,
               json.dumps(puissances_exos, ensure_ascii=False))
print("✅ Puissances exo 8 fixé (hectomètres → mètres)")

# ── 2. Replace Fonctions_Linéaires with Statistiques ─────────────────────────
# Find the Fonctions_Linéaires row
fl_row_idx = None
for i, row in enumerate(raw):
    if len(row) > 1 and row[0] == '4EME' and row[1] == 'Fonctions_Linéaires':
        fl_row_idx = i
        break
assert fl_row_idx is not None, "Fonctions_Linéaires row not found"
print(f"Fonctions_Linéaires found at row {fl_row_idx + 1}")

# Statistiques avancées 4EME — 20 exercises, 4 slots of 5
# Slot 1: Moyenne (pondérée)
# Slot 2: Médiane et étendue
# Slot 3: Diagrammes et lecture de données
# Slot 4: Synthèse statistique (croiser moyenne, médiane, interprétation)

stats_exos = [
    # ── SLOT 1: Moyenne (pondérée) ──────────────────────────────────────
    # Exo 1 - Accessible - QCM
    {
        "lvl": 1,
        "q": "Lucas a obtenu les notes suivantes en maths : $12$, $15$, $9$ et $14$. Quelle est sa moyenne ?",
        "a": "$12{,}5$",
        "options": ["$12{,}5$", "$12$", "$13$"],
        "steps": [
            "Pour calculer la moyenne, on additionne toutes les notes puis on divise par le nombre de notes.",
            "$12 + 15 + 9 + 14 = 50$, et il y a $4$ notes.",
            "$\\frac{50}{4} = 12{,}5$. La moyenne de Lucas est $12{,}5$."
        ],
        "f": "$\\bar{x} = \\frac{x_1 + x_2 + \\cdots + x_n}{n}$"
    },
    # Exo 2 - Accessible - QCM
    {
        "lvl": 1,
        "q": "Emma a eu $8$, $11$, $14$, $13$ et $9$ en histoire. Quelle est sa moyenne ?",
        "a": "$11$",
        "options": ["$10$", "$11$", "$11{,}5$"],
        "steps": [
            "On additionne les $5$ notes : $8 + 11 + 14 + 13 + 9$.",
            "$8 + 11 + 14 + 13 + 9 = 55$.",
            "$\\frac{55}{5} = 11$. La moyenne d'Emma est $11$."
        ],
        "f": "$\\bar{x} = \\frac{x_1 + x_2 + \\cdots + x_n}{n}$"
    },
    # Exo 3 - Intermédiaire - QCM
    {
        "lvl": 1,
        "q": "Dans une classe, $10$ élèves ont eu $8$, $15$ élèves ont eu $12$ et $5$ élèves ont eu $16$. Quelle est la moyenne pondérée ?",
        "a": "$11{,}3\\overline{3}$",
        "options": ["$12$", "$11{,}3\\overline{3}$", "$10{,}8$"],
        "steps": [
            "La moyenne pondérée se calcule en multipliant chaque valeur par son effectif, puis en divisant par l'effectif total.",
            "$10 \\times 8 + 15 \\times 12 + 5 \\times 16 = 80 + 180 + 80 = 340$. Effectif total : $10 + 15 + 5 = 30$.",
            "$\\frac{340}{30} \\approx 11{,}3\\overline{3}$."
        ],
        "f": "$\\bar{x} = \\frac{\\sum n_i \\cdot x_i}{\\sum n_i}$"
    },
    # Exo 4 - Intermédiaire - VF
    {
        "lvl": 1,
        "type": "vf",
        "q": "Jade a obtenu $10$, $10$, $10$, $10$ et $20$. Sa moyenne est $12$.",
        "a": "Vrai",
        "options": ["Vrai", "Faux"],
        "steps": [
            "On calcule : $10 + 10 + 10 + 10 + 20 = 60$.",
            "$\\frac{60}{5} = 12$. La moyenne est bien $12$."
        ],
        "f": "$\\bar{x} = \\frac{x_1 + x_2 + \\cdots + x_n}{n}$"
    },
    # Exo 5 - Challenge - Fill
    {
        "lvl": 1,
        "type": "fill",
        "q": "Noé a $11$ de moyenne après $4$ contrôles. Il veut $12$ de moyenne après le $5$ème. Quelle note minimale doit-il obtenir ? ___",
        "a": "16",
        "options": [],
        "steps": [
            "Après $4$ contrôles à $11$ de moyenne, le total des points est $4 \\times 11 = 44$.",
            "Pour avoir $12$ de moyenne sur $5$ contrôles, il faut un total de $5 \\times 12 = 60$.",
            "Note nécessaire : $60 - 44 = 16$."
        ],
        "f": "$\\bar{x} = \\frac{\\text{somme}}{n} \\Rightarrow \\text{somme} = \\bar{x} \\times n$"
    },

    # ── SLOT 2: Médiane et étendue ──────────────────────────────────────
    # Exo 6 - Accessible - QCM
    {
        "lvl": 1,
        "q": "Voici une série de données triées : $3$, $5$, $7$, $9$, $11$. Quelle est la médiane ?",
        "a": "$7$",
        "options": ["$5$", "$7$", "$9$"],
        "steps": [
            "La médiane est la valeur qui sépare la série en deux moitiés égales.",
            "Il y a $5$ valeurs (nombre impair). La médiane est la $3$ème valeur.",
            "La $3$ème valeur est $7$."
        ],
        "f": "Médiane : valeur centrale d'une série triée"
    },
    # Exo 7 - Accessible - QCM
    {
        "lvl": 1,
        "q": "Voici les tailles en cm de $6$ élèves : $152$, $158$, $161$, $165$, $170$, $174$. Quelle est la médiane ?",
        "a": "$163$",
        "options": ["$161$", "$163$", "$165$"],
        "steps": [
            "Il y a $6$ valeurs (nombre pair). La médiane est la moyenne des $3$ème et $4$ème valeurs.",
            "$3$ème valeur = $161$, $4$ème valeur = $165$.",
            "$\\frac{161 + 165}{2} = \\frac{326}{2} = 163$."
        ],
        "f": "Si $n$ pair : médiane $= \\frac{x_{n/2} + x_{n/2+1}}{2}$"
    },
    # Exo 8 - Intermédiaire - QCM
    {
        "lvl": 1,
        "q": "Adam a relevé les températures sur une semaine : $-2$, $1$, $3$, $5$, $5$, $8$, $12$. Quelle est l'étendue de cette série ?",
        "a": "$14$",
        "options": ["$10$", "$14$", "$12$"],
        "steps": [
            "L'étendue est la différence entre la plus grande et la plus petite valeur.",
            "Maximum = $12$, minimum = $-2$.",
            "$12 - (-2) = 12 + 2 = 14$."
        ],
        "f": "Étendue $= x_{\\max} - x_{\\min}$"
    },
    # Exo 9 - Intermédiaire - VF
    {
        "lvl": 1,
        "type": "vf",
        "q": "Dans la série $4$, $7$, $10$, $13$, $16$, $19$, la médiane vaut $11{,}5$.",
        "a": "Vrai",
        "options": ["Vrai", "Faux"],
        "steps": [
            "$6$ valeurs (pair) : la médiane est la moyenne des $3$ème et $4$ème valeurs.",
            "$3$ème = $10$, $4$ème = $13$.",
            "$\\frac{10 + 13}{2} = \\frac{23}{2} = 11{,}5$. C'est vrai."
        ],
        "f": "Si $n$ pair : médiane $= \\frac{x_{n/2} + x_{n/2+1}}{2}$"
    },
    # Exo 10 - Challenge - Fill
    {
        "lvl": 1,
        "type": "fill",
        "q": "La série triée est : $3$, $5$, $x$, $11$, $15$. La médiane vaut $8$. Que vaut $x$ ? ___",
        "a": "8",
        "options": [],
        "steps": [
            "Il y a $5$ valeurs. La médiane est la $3$ème valeur de la série triée.",
            "La $3$ème valeur est $x$, et la médiane vaut $8$.",
            "Donc $x = 8$. On vérifie : $3, 5, 8, 11, 15$ — la série reste triée."
        ],
        "f": "Médiane : valeur centrale d'une série triée"
    },

    # ── SLOT 3: Diagrammes et lecture de données ────────────────────────
    # Exo 11 - Accessible - QCM
    {
        "lvl": 1,
        "q": "Dans un diagramme en barres, les fréquences des notes sont : $8$ → $5$ élèves, $12$ → $10$ élèves, $16$ → $5$ élèves. Quel est l'effectif total ?",
        "a": "$20$",
        "options": ["$15$", "$20$", "$25$"],
        "steps": [
            "L'effectif total est la somme de tous les effectifs.",
            "$5 + 10 + 5 = 20$.",
            "Il y a $20$ élèves au total."
        ],
        "f": "$N = n_1 + n_2 + \\cdots + n_k$"
    },
    # Exo 12 - Accessible - QCM
    {
        "lvl": 1,
        "q": "Un diagramme circulaire montre que $25\\%$ des élèves préfèrent le foot et $40\\%$ le basket. Sur $200$ élèves, combien préfèrent le basket ?",
        "a": "$80$",
        "options": ["$50$", "$80$", "$100$"],
        "steps": [
            "$40\\%$ de $200$ élèves préfèrent le basket.",
            "$\\frac{40}{100} \\times 200 = 0{,}4 \\times 200$.",
            "$= 80$ élèves."
        ],
        "f": "$\\text{Effectif} = \\frac{\\text{fréquence}}{100} \\times N$"
    },
    # Exo 13 - Intermédiaire - QCM
    {
        "lvl": 1,
        "q": "Inès relève les durées d'appels (en min) : $[0;5[$ → $8$ appels, $[5;10[$ → $12$ appels, $[10;15[$ → $5$ appels. Quelle est la fréquence de la classe $[5;10[$ ?",
        "a": "$48\\%$",
        "options": ["$48\\%$", "$40\\%$", "$52\\%$"],
        "steps": [
            "Effectif total : $8 + 12 + 5 = 25$.",
            "Fréquence de $[5;10[$ : $\\frac{12}{25}$.",
            "$\\frac{12}{25} = 0{,}48 = 48\\%$."
        ],
        "f": "$f_i = \\frac{n_i}{N} \\times 100$"
    },
    # Exo 14 - Intermédiaire - VF
    {
        "lvl": 1,
        "type": "vf",
        "q": "Un diagramme en barres montre $3$ catégories d'effectifs $10$, $20$ et $30$. La fréquence de la plus grande catégorie est $50\\%$.",
        "a": "Vrai",
        "options": ["Vrai", "Faux"],
        "steps": [
            "Effectif total : $10 + 20 + 30 = 60$.",
            "Fréquence de la plus grande catégorie ($30$) : $\\frac{30}{60}$.",
            "$\\frac{30}{60} = 0{,}5 = 50\\%$. C'est vrai."
        ],
        "f": "$f_i = \\frac{n_i}{N} \\times 100$"
    },
    # Exo 15 - Challenge - Fill
    {
        "lvl": 1,
        "type": "fill",
        "q": "Hugo a relevé les couleurs de $50$ voitures : rouge = $15$, bleu = $20$, noir = ___. Sachant que ces $3$ couleurs représentent toutes les voitures, combien sont noires ? ___",
        "a": "15",
        "options": [],
        "steps": [
            "Le total est $50$ voitures et il n'y a que $3$ couleurs.",
            "Rouge + bleu = $15 + 20 = 35$.",
            "Noir = $50 - 35 = 15$."
        ],
        "f": "$N = n_1 + n_2 + \\cdots + n_k$"
    },

    # ── SLOT 4: Synthèse statistique ────────────────────────────────────
    # Exo 16 - Accessible - QCM
    {
        "lvl": 1,
        "q": "Léa a les notes : $8$, $12$, $14$, $6$, $10$. Quelle est la moyenne et la médiane ?",
        "a": "Moyenne $= 10$, médiane $= 10$",
        "options": [
            "Moyenne $= 10$, médiane $= 10$",
            "Moyenne $= 10$, médiane $= 12$",
            "Moyenne $= 12$, médiane $= 10$"
        ],
        "steps": [
            "Moyenne : $\\frac{8 + 12 + 14 + 6 + 10}{5} = \\frac{50}{5} = 10$.",
            "Série triée : $6, 8, 10, 12, 14$. La $3$ème valeur est $10$.",
            "Moyenne $= 10$ et médiane $= 10$."
        ],
        "f": "$\\bar{x} = \\frac{\\sum x_i}{n}$ ; médiane = valeur centrale"
    },
    # Exo 17 - Accessible - QCM
    {
        "lvl": 1,
        "q": "Les scores d'un jeu sont : $2$, $5$, $5$, $8$, $100$. La moyenne est-elle un bon indicateur du score typique ?",
        "a": "Non, la médiane ($5$) est plus représentative",
        "options": [
            "Oui, la moyenne ($24$) résume bien",
            "Non, la médiane ($5$) est plus représentative",
            "Non, l'étendue ($98$) est le meilleur indicateur"
        ],
        "steps": [
            "Moyenne : $\\frac{2+5+5+8+100}{5} = \\frac{120}{5} = 24$. Cette valeur est tirée vers le haut par $100$.",
            "Médiane (série déjà triée, $5$ valeurs) : $3$ème valeur = $5$.",
            "La valeur extrême $100$ fausse la moyenne. La médiane ($5$) représente mieux le score typique."
        ],
        "f": "La médiane résiste aux valeurs extrêmes, pas la moyenne"
    },
    # Exo 18 - Intermédiaire - QCM
    {
        "lvl": 1,
        "q": "Dans une classe, les notes pondérées sont : contrôle (coeff $3$) = $14$, DM (coeff $1$) = $8$, oral (coeff $2$) = $11$. Quelle est la moyenne pondérée ?",
        "a": "$12$",
        "options": ["$11$", "$12$", "$12{,}5$"],
        "steps": [
            "Moyenne pondérée : $\\frac{3 \\times 14 + 1 \\times 8 + 2 \\times 11}{3 + 1 + 2}$.",
            "$= \\frac{42 + 8 + 22}{6} = \\frac{72}{6}$.",
            "$= 12$."
        ],
        "f": "$\\bar{x} = \\frac{\\sum n_i \\cdot x_i}{\\sum n_i}$"
    },
    # Exo 19 - Intermédiaire - VF
    {
        "lvl": 1,
        "type": "vf",
        "q": "Si on ajoute $3$ à chaque valeur d'une série, la moyenne augmente de $3$ mais l'étendue ne change pas.",
        "a": "Vrai",
        "options": ["Vrai", "Faux"],
        "steps": [
            "Ajouter $3$ à chaque valeur augmente la somme de $3n$, donc la moyenne de $3$.",
            "Le max et le min augmentent chacun de $3$, donc leur différence reste la même.",
            "La moyenne augmente de $3$, l'étendue est inchangée. C'est vrai."
        ],
        "f": "Si $y_i = x_i + c$ alors $\\bar{y} = \\bar{x} + c$ et étendue inchangée"
    },
    # Exo 20 - Challenge - Fill
    {
        "lvl": 1,
        "type": "fill",
        "q": "Une série de $7$ valeurs triées est : $4$, $6$, $8$, $m$, $12$, $15$, $18$. La moyenne vaut $10$. Que vaut $m$ ? ___",
        "a": "7",
        "options": [],
        "steps": [
            "Somme totale pour une moyenne de $10$ sur $7$ valeurs : $7 \\times 10 = 70$.",
            "Somme des valeurs connues : $4 + 6 + 8 + 12 + 15 + 18 = 63$.",
            "$m = 70 - 63 = 7$. On vérifie : $4, 6, 7, 8, 12, 15, 18$ — la série reste triée."
        ],
        "f": "$\\bar{x} = \\frac{\\sum x_i}{n} \\Rightarrow \\sum x_i = n \\times \\bar{x}$"
    }
]

# Update the row: change Categorie, Titre, Icone, ExosJSON
row_num = fl_row_idx + 1  # 1-indexed
sh.update_cell('Curriculum_Officiel', row_num, 2, 'Statistiques')  # Categorie
sh.update_cell('Curriculum_Officiel', row_num, 3, 'Statistiques')  # Titre
sh.update_cell('Curriculum_Officiel', row_num, 4, '📊')  # Icone
sh.update_cell('Curriculum_Officiel', row_num, 5, json.dumps(stats_exos, ensure_ascii=False))  # ExosJSON

print(f"✅ Fonctions_Linéaires (row {row_num}) remplacé par Statistiques (20 exos)")
print("   Slot 1: Moyenne (pondérée)")
print("   Slot 2: Médiane et étendue")
print("   Slot 3: Diagrammes et lecture de données")
print("   Slot 4: Synthèse statistique")
print("\nDone!")
