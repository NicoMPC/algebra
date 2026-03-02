window.dbDiag = {
  "ALGEBRA_6EME": {
    "CALCULS": [
      { "q": "Quel est le résultat de $2,5 \\times 10$ ?", "options": ["25", "250", "0,25", "2,50"], "a": "25", "f": "Multiplier par 10 décale la virgule d'un rang vers la droite.", "steps": ["Repère la virgule dans 2,5.", "Déplace-la d'une case vers la droite pour agrandir le nombre."], "lvl": 1 },
      { "q": "Calcule : $12 + 3 \\times 2$", "options": ["30", "18", "17", "24"], "a": "18", "f": "La multiplication est prioritaire sur l'addition.", "steps": ["Fais d'abord $3 \\times 2 = 6$.", "Ensuite ajoute 12 : $12 + 6 = 18$."], "lvl": 2 }
    ],
    "FRACTIONS": [
      { "q": "Que représente la fraction $\\frac{1}{2}$ ?", "options": ["Le double", "La moitié", "Le tiers", "Un quart"], "a": "La moitié", "f": "Diviser par 2, c'est prendre la moitié.", "steps": ["Le chiffre du bas indique en combien on coupe l'unité."], "lvl": 1 },
      { "q": "Parmi ces fractions, laquelle est égale à 1 ?", "options": ["\\frac{1}{2}", "\\frac{4}{4}", "\\frac{0}{1}", "\\frac{1}{10}"], "a": "\\frac{4}{4}", "f": "Une fraction vaut 1 quand le numérateur est égal au dénominateur.", "steps": ["Si tu manges 4 parts d'une pizza coupée en 4, tu as mangé 1 pizza entière."], "lvl": 2 }
    ],
    "GEOMETRIE": [
      { "q": "Combien de côtés possède un hexagone ?", "options": ["5", "6", "7", "8"], "a": "6", "f": "Hexa = 6.", "steps": ["Pense à la forme de la France (l'Hexagone)."], "lvl": 1 },
      { "q": "Quel est le périmètre d'un carré de côté 3 cm ?", "options": ["9 cm", "12 cm", "6 cm", "3 cm"], "a": "12 cm", "f": "Périmètre = $4 \\times côté$.", "steps": ["Additionne les 4 côtés : $3+3+3+3 = 12$."], "lvl": 2 }
    ],
    "PROPORTIONS": [
      { "q": "Si 2 stylos coûtent 4€, combien coûtent 3 stylos ?", "options": ["5€", "6€", "8€", "7€"], "a": "6€", "f": "Trouve d'abord le prix à l'unité.", "steps": ["1 stylo coûte $4 \\div 2 = 2$€.", "3 stylos coûtent $3 \\times 2 = 6$€."], "lvl": 1 },
      { "q": "Que vaut $50\\%$ de 200 ?", "options": ["100", "50", "25", "150"], "a": "100", "f": "50% représente la moitié.", "steps": ["Divise 200 par 2."], "lvl": 2 }
    ]
  },

  "ALGEBRA_5EME": {
    "RELATIFS": [
      { "q": "Calcule : $-5 + 3$", "options": ["-2", "-8", "2", "8"], "a": "-2", "f": "Garde le signe de la plus grande distance à zéro.", "steps": ["Dette de 5, gain de 3 = Dette de 2."], "lvl": 1 },
      { "q": "Calcule : $-4 - (-6)$", "options": ["2", "-10", "-2", "10"], "a": "2", "f": "Soustraire revient à ajouter l'opposé : $-(-a) = +a$.", "steps": ["Transforme : $-4 + 6 = 2$."], "lvl": 2 }
    ],
    "FRACTIONS": [
      { "q": "Calcule : $\\frac{3}{7} + \\frac{2}{7}$", "options": ["\\frac{5}{14}", "\\frac{5}{7}", "\\frac{6}{7}", "\\frac{1}{7}"], "a": "\\frac{5}{7}", "f": "Même dénominateur : on additionne les numérateurs.", "steps": ["On garde le 7 en bas.", "On fait $3+2=5$ en haut."], "lvl": 1 },
      { "q": "Simplifie $\\frac{15}{20}$", "options": ["\\frac{3}{4}", "\\frac{5}{10}", "\\frac{3}{5}", "\\frac{1}{2}"], "a": "\\frac{3}{4}", "f": "Divise le haut et le bas par le même nombre.", "steps": ["15 et 20 sont dans la table de 5.", "$15 \\div 5 = 3$ et $20 \\div 5 = 4$."], "lvl": 2 }
    ],
    "PRIORITES": [
      { "q": "Calcule : $2 + 5 \\times 4$", "options": ["28", "22", "40", "11"], "a": "22", "f": "La multiplication se fait avant l'addition.", "steps": ["Calcule $5 \\times 4 = 20$.", "Fais $2 + 20 = 22$."], "lvl": 1 },
      { "q": "Calcule : $(3+4) \\times 2$", "options": ["14", "11", "10", "24"], "a": "14", "f": "Les parenthèses sont la priorité absolue.", "steps": ["Calcule $3+4 = 7$.", "Fais $7 \\times 2 = 14$."], "lvl": 2 }
    ],
    "GEOMETRIE": [
      { "q": "Quelle est la somme des angles d'un triangle ?", "options": ["90°", "360°", "180°", "100°"], "a": "180°", "f": "C'est une règle absolue pour tout triangle plat.", "steps": ["Mémorise cette valeur : 180°."], "lvl": 1 },
      { "q": "L'aire d'un rectangle de 5 cm par 4 cm est :", "options": ["18 cm²", "20 cm²", "9 cm²", "40 cm²"], "a": "20 cm²", "f": "Aire d'un rectangle = Longueur $\\times$ largeur.", "steps": ["Multiplie $5 \\times 4 = 20$."], "lvl": 1 }
    ]
  },

  "ALGEBRA_4EME": {
    "EQUATIONS": [
      { "q": "Résous : $x + 4 = 10$", "options": ["6", "14", "40", "-6"], "a": "6", "f": "Fais l'opération inverse.", "steps": ["Soustrait 4 de chaque côté : $x = 10 - 4 = 6$."], "lvl": 1 },
      { "q": "Résous : $3x - 5 = 10$", "options": ["5", "15", "-5", "3"], "a": "5", "f": "Pour isoler $x$, fais l'opération inverse étape par étape.", "steps": ["Fais $+5$ : $3x = 15$.", "Divise par 3 : $x = 5$."], "lvl": 2 }
    ],
    "FRACTIONS": [
      { "q": "Calcule : $\\frac{2}{3} \\times \\frac{4}{5}$", "options": ["\\frac{6}{8}", "\\frac{8}{15}", "\\frac{10}{12}", "\\frac{2}{15}"], "a": "\\frac{8}{15}", "f": "Multiplication de fractions : haut $\\times$ haut et bas $\\times$ bas.", "steps": ["Fais $2 \\times 4 = 8$ et $3 \\times 5 = 15$."], "lvl": 1 },
      { "q": "Calcule : $\\frac{1}{2} + \\frac{1}{4}$", "options": ["\\frac{2}{6}", "\\frac{3}{4}", "\\frac{2}{4}", "\\frac{1}{6}"], "a": "\\frac{3}{4}", "f": "Mets au même dénominateur avant d'additionner.", "steps": ["Transforme $\\frac{1}{2}$ en $\\frac{2}{4}$.", "Calcule $\\frac{2}{4} + \\frac{1}{4} = \\frac{3}{4}$."], "lvl": 2 }
    ],
    "PUISSANCES": [
      { "q": "Que vaut $10^3 \\times 10^2$ ?", "options": ["10^5", "10^6", "100^5", "10^1"], "a": "10^5", "f": "Produit : $a^n \\times a^m = a^{n+m}$.", "steps": ["Additionne les exposants : $3+2=5$."], "lvl": 1 },
      { "q": "Que vaut $(10^2)^3$ ?", "options": ["10^5", "10^6", "10^8", "100^3"], "a": "10^6", "f": "Puissance d'une puissance : $(a^n)^m = a^{n \\times m}$.", "steps": ["Multiplie les exposants : $2 \\times 3 = 6$."], "lvl": 2 }
    ],
    "PYTHAGORE": [
      { "q": "Dans un triangle rectangle, le plus grand côté s'appelle :", "options": ["La diagonale", "L'hypoténuse", "Le côté adjacent", "La médiane"], "a": "L'hypoténuse", "f": "C'est le côté face à l'angle droit.", "steps": [], "lvl": 1 },
      { "q": "Si les côtés de l'angle droit valent 3 et 4, l'hypoténuse vaut :", "options": ["5", "7", "25", "12"], "a": "5", "f": "Théorème de Pythagore : $a^2 + b^2 = c^2$.", "steps": ["$3^2 + 4^2 = 9 + 16 = 25$.", "La racine carrée de 25 est 5."], "lvl": 2 }
    ]
  },

  "ALGEBRA_3EME": {
    "DEVELOPPEMENT": [
      { "q": "Développe : $-2(x + 4)$", "options": ["-2x - 8", "-2x + 4", "-2x + 8", "2x - 8"], "a": "-2x - 8", "f": "Distributivité : $k(a+b) = ka + kb$. Attention au signe.", "steps": ["$-2 \\times x = -2x$.", "$-2 \\times 4 = -8$."], "lvl": 1 },
      { "q": "Développe : $(x + 2)^2$", "options": ["x^2 + 4", "x^2 + 2x + 4", "x^2 + 4x + 4", "x^2 + 4x + 2"], "a": "x^2 + 4x + 4", "f": "Identité remarquable : $(a+b)^2 = a^2 + 2ab + b^2$.", "steps": ["$a=x$, $b=2$.", "$2ab = 2 \\times x \\times 2 = 4x$."], "lvl": 2 }
    ],
    "FACTORISATION": [
      { "q": "Factorise : $3x + 12$", "options": ["3(x + 4)", "x(3 + 12)", "3(x + 9)", "12(x + 3)"], "a": "3(x + 4)", "f": "Trouve le facteur commun (ici, 3).", "steps": ["$3x = 3 \\times x$.", "$12 = 3 \\times 4$.", "On factorise par 3."], "lvl": 1 },
      { "q": "Factorise : $x^2 - 9$", "options": ["(x - 3)(x + 3)", "(x - 9)(x + 1)", "(x - 3)^2", "x(x - 9)"], "a": "(x - 3)(x + 3)", "f": "Identité : $a^2 - b^2 = (a-b)(a+b)$.", "steps": ["Remarque que $9 = 3^2$."], "lvl": 2 }
    ],
    "FONCTIONS": [
      { "q": "L'image de $2$ par $f(x) = 3x - 1$ est :", "options": ["5", "6", "2", "7"], "a": "5", "f": "Remplace $x$ par 2 dans la formule.", "steps": ["$3 \\times 2 - 1 = 6 - 1 = 5$."], "lvl": 1 },
      { "q": "L'antécédent de 8 par $f(x) = 2x$ est :", "options": ["4", "16", "6", "10"], "a": "4", "f": "On cherche $x$ tel que $2x = 8$.", "steps": ["Résous $2x = 8 \\implies x = 4$."], "lvl": 1 }
    ],
    "ARITHMETIQUE": [
      { "q": "Un nombre premier n'est divisible que par :", "options": ["Lui-même et 2", "Lui-même et 1", "Les nombres pairs", "10"], "a": "Lui-même et 1", "f": "C'est la définition d'un nombre premier.", "steps": [], "lvl": 1 },
      { "q": "Le plus petit multiple commun (PPCM) de 4 et 6 est :", "options": ["24", "12", "10", "2"], "a": "12", "f": "Le plus petit nombre dans la table de 4 ET de 6.", "steps": ["Multiples de 4 : 4, 8, 12, 16...", "Multiples de 6 : 6, 12, 18..."], "lvl": 2 }
    ]
  },

  "ALGEBRA_SECONDE": {
    "VECTEURS": [
      { "q": "Si $A(1 ; 2)$ et $B(4 ; 6)$, $\\vec{AB}$ vaut :", "options": ["(3 ; 4)", "(5 ; 8)", "(-3 ; -4)", "(4 ; 12)"], "a": "(3 ; 4)", "f": "$(x_B - x_A ; y_B - y_A)$.", "steps": ["$4-1=3$ et $6-2=4$."], "lvl": 1 },
      { "q": "Que vaut $\\vec{u} + \\vec{v}$ si $\\vec{u}(1; 3)$ et $\\vec{v}(2; -1)$ ?", "options": ["(3; 2)", "(-1; 4)", "(2; -3)", "(3; 4)"], "a": "(3; 2)", "f": "On additionne les $x$ entre eux et les $y$ entre eux.", "steps": ["$1+2 = 3$ et $3+(-1) = 2$."], "lvl": 1 }
    ],
    "DROITES": [
      { "q": "Le coefficient directeur de $y = -3x + 5$ est :", "options": ["-3", "5", "3", "-3x"], "a": "-3", "f": "C'est le facteur devant $x$.", "steps": [], "lvl": 1 },
      { "q": "Si $m=2$ et passe par l'origine, l'équation est :", "options": ["y = 2", "y = 2x", "y = x+2", "y = -2x"], "a": "y = 2x", "f": "Passe par l'origine = ordonnée à l'origine nulle ($p=0$).", "steps": [], "lvl": 2 }
    ],
    "FONCTIONS": [
      { "q": "L'ensemble de définition de $f(x) = \\frac{1}{x-2}$ est :", "options": ["\\mathbb{R}", "\\mathbb{R} \\setminus \\{2\\}", "\\mathbb{R} \\setminus \\{0\\}", "[2 ; +\\infty["], "a": "\\mathbb{R} \\setminus \\{2\\}", "f": "Le dénominateur ne peut pas être nul.", "steps": ["On doit avoir $x - 2 \\neq 0$ donc $x \\neq 2$."], "lvl": 2 },
      { "q": "Si $f(x)$ est paire, sa courbe est symétrique par rapport à :", "options": ["L'axe des ordonnées", "L'axe des abscisses", "L'origine", "La droite $y=x$"], "a": "L'axe des ordonnées", "f": "$f(-x) = f(x)$.", "steps": [], "lvl": 1 }
    ],
    "PROBABILITES": [
      { "q": "La probabilité d'un événement certain est :", "options": ["100", "1", "0", "0.5"], "a": "1", "f": "Une probabilité est toujours comprise entre 0 et 1.", "steps": [], "lvl": 1 },
      { "q": "Probabilité d'obtenir un multiple de 3 avec un dé classique :", "options": ["1/6", "1/3", "1/2", "2/3"], "a": "1/3", "f": "Il y a deux multiples de 3 : le 3 et le 6.", "steps": ["2 chances sur 6, ce qui se simplifie en 1/3."], "lvl": 2 }
    ]
  },

  "ALGEBRA_PREMIERE": {
    "SECOND_DEGRE": [
      { "q": "Combien de racines si $\\Delta = -3$ ?", "options": ["0", "1", "2", "Une infinité"], "a": "0", "f": "Un carré de réels ne peut pas être négatif.", "steps": [], "lvl": 1 },
      { "q": "Calcule le discriminant de $x^2 + 3x + 2 = 0$", "options": ["1", "9", "17", "0"], "a": "1", "f": "$\\Delta = b^2 - 4ac$.", "steps": ["$3^2 - 4(1)(2) = 9 - 8 = 1$."], "lvl": 2 }
    ],
    "DERIVATION": [
      { "q": "La dérivée de $f(x) = x^3$ est :", "options": ["3x^2", "x^2", "3x", "x^4/4"], "a": "3x^2", "f": "$(x^n)' = n x^{n-1}$.", "steps": [], "lvl": 1 },
      { "q": "La dérivée de $f(x) = \\frac{1}{x}$ est :", "options": ["-\\frac{1}{x^2}", "\\frac{1}{x^2}", "\\ln(x)", "0"], "a": "-\\frac{1}{x^2}", "f": "Formule de base à connaître par cœur.", "steps": [], "lvl": 2 }
    ],
    "SUITES": [
      { "q": "Dans une suite arithmétique $u_n$, on passe au suivant en :", "options": ["Ajoutant $r$", "Multipliant par $q$", "Élevant au carré", "Soustrayant $u_0$"], "a": "Ajoutant $r$", "f": "$u_{n+1} = u_n + r$.", "steps": [], "lvl": 1 },
      { "q": "Si $u_0=2$ et $q=3$ (suite géométrique), que vaut $u_2$ ?", "options": ["8", "18", "6", "12"], "a": "18", "f": "$u_n = u_0 \\times q^n$.", "steps": ["$u_1 = 2 \\times 3 = 6$.", "$u_2 = 6 \\times 3 = 18$."], "lvl": 2 }
    ],
    "TRIGONOMETRIE": [
      { "q": "Que vaut $\\cos(\\pi)$ ?", "options": ["-1", "0", "1", "0.5"], "a": "-1", "f": "À gauche du cercle trigonométrique.", "steps": [], "lvl": 1 },
      { "q": "Convertis 180° en radians :", "options": ["\\pi", "2\\pi", "\\pi/2", "\\pi/4"], "a": "\\pi", "f": "Le demi-tour du cercle.", "steps": [], "lvl": 1 }
    ]
  },

  "ALGEBRA_TERMINALE": {
    "LIMITES": [
      { "q": "Limite de $e^x$ quand $x \\to -\\infty$ ?", "options": ["0", "+\\infty", "-\\infty", "1"], "a": "0", "f": "L'exponentielle s'écrase sur l'axe.", "steps": [], "lvl": 1 },
      { "q": "Limite de $\\ln(x)$ quand $x \\to 0^+$ ?", "options": ["-\\infty", "0", "1", "+\\infty"], "a": "-\\infty", "f": "Le logarithme plonge le long de l'axe des ordonnées.", "steps": [], "lvl": 2 }
    ],
    "PRIMITIVES": [
      { "q": "Une primitive de $\\cos(x)$ est :", "options": ["\\sin(x)", "-\\sin(x)", "-\\cos(x)", "\\tan(x)"], "a": "\\sin(x)", "f": "Car la dérivée de $\\sin$ est $\\cos$.", "steps": [], "lvl": 1 },
      { "q": "Une primitive de $e^{2x}$ est :", "options": ["\\frac{1}{2}e^{2x}", "2e^{2x}", "e^{2x}", "e^x"], "a": "\\frac{1}{2}e^{2x}", "f": "Il faut compenser la dérivée interne (2).", "steps": [], "lvl": 2 }
    ],
    "LOGARITHME": [
      { "q": "Que vaut $\\ln(e)$ ?", "options": ["1", "0", "e", "10"], "a": "1", "f": "$ln$ et $exp$ sont des fonctions réciproques.", "steps": [], "lvl": 1 },
      { "q": "Simplifie $\\ln(a) + \\ln(b)$", "options": ["\\ln(a \\times b)", "\\ln(a+b)", "a \\times b", "\\ln(a/b)"], "a": "\\ln(a \\times b)", "f": "Le logarithme transforme les produits en sommes.", "steps": [], "lvl": 2 }
    ],
    "GEOMETRIE_DANS_L_ESPACE": [
      { "q": "Deux vecteurs sont colinéaires s'ils sont :", "options": ["Proportionnels", "Orthogonaux", "De même norme", "Coplanaires"], "a": "Proportionnels", "f": "Il existe un réel $k$ tel que $\\vec{u} = k\\vec{v}$.", "steps": [], "lvl": 1 },
      { "q": "Si le produit scalaire $\\vec{u} \\cdot \\vec{v} = 0$, les vecteurs sont :", "options": ["Orthogonaux", "Colinéaires", "Nuls", "Égaux"], "a": "Orthogonaux", "f": "Leur angle forme 90°.", "steps": [], "lvl": 1 }
    ]
  }
};