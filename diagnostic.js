// ==============================================================================
// BASE DE DONNÉES SECRÈTE : LE DIAGNOSTIC IA (Bilan de départ)
// ==============================================================================
// Ce fichier n'est utilisé QUE pour le calibrage du Jour 1.
// Les questions sont courtes, fondamentales et ciblent les erreurs récurrentes.

window.dbDiag = {
  
  // ==========================================
  // NIVEAU 6ÈME
  // ==========================================
  "ALGEBRA_6EME": {
    "DECIMAUX": [
      {
        "q": "Quel est le résultat de $2,5 \\times 10$ ?",
        "options": ["25", "250", "0,25", "2,50"],
        "a": "25",
        "f": "Multiplier par 10 décale la virgule d'un rang vers la droite.",
        "steps": ["Repère la virgule dans 2,5.", "Déplace-la d'une case vers la droite pour agrandir le nombre."],
        "lvl": 1
      }
    ],
    "FRACTIONS_SIMPLES": [
      {
        "q": "Que représente la fraction $\\frac{1}{2}$ ?",
        "options": ["Le double", "La moitié", "Le tiers", "Un virgule deux"],
        "a": "La moitié",
        "f": "La fraction $\\frac{1}{2}$ signifie qu'on divise une unité en 2 parts égales.",
        "steps": ["Le chiffre du bas (dénominateur) indique en combien on coupe.", "Couper en 2, c'est prendre la moitié."],
        "lvl": 1
      }
    ]
  },

  // ==========================================
  // NIVEAU 5ÈME
  // ==========================================
  "ALGEBRA_5EME": {
    "RELATIFS": [
      {
        "q": "Calcule : $-5 + 3$",
        "options": ["-2", "-8", "2", "8"],
        "a": "-2",
        "f": "Addition de relatifs : on garde le signe de celui qui a la plus grande distance à zéro, et on soustrait.",
        "steps": ["Imagine que tu as une dette de 5€ (-5).", "Tu gagnes 3€ (+3).", "Tu as remboursé une partie, mais tu es toujours en dette de 2€ (-2)."],
        "lvl": 1
      },
      {
        "q": "Calcule : $-4 - (-6)$",
        "options": ["2", "-10", "-2", "10"],
        "a": "2",
        "f": "Soustraire un nombre relatif revient à ajouter son opposé : $-(-a) = +a$.",
        "steps": ["Transforme le signe : $-(-6)$ devient $+6$.", "Le calcul devient $-4 + 6$.", "Garde le signe du plus grand : $+2$."],
        "lvl": 2
      }
    ]
  },

  // ==========================================
  // NIVEAU 4ÈME
  // ==========================================
  "ALGEBRA_4EME": {
    "EQUATIONS": [
      {
        "q": "Résous l'équation : $3x - 5 = 10$",
        "options": ["x = 5", "x = 15", "x = -5", "x = 3"],
        "a": "x = 5",
        "f": "Pour isoler $x$, on fait toujours l'opération inverse.",
        "steps": ["Élimine d'abord le $-5$ en faisant $+5$ de chaque côté : $3x = 15$.", "Élimine le $3$ (qui multiplie) en divisant par $3$ : $x = 15 \\div 3 = 5$."],
        "lvl": 1
      }
    ],
    "FRACTIONS": [
      {
        "q": "Calcule : $\\frac{2}{5} + \\frac{1}{5}$",
        "options": ["\\frac{3}{5}", "\\frac{3}{10}", "\\frac{2}{25}", "3"],
        "a": "\\frac{3}{5}",
        "f": "Si le dénominateur (en bas) est le même, on additionne uniquement les numérateurs (en haut).",
        "steps": ["Le chiffre du bas (5) représente la taille des parts de pizza. Elle ne change pas !", "Additionne juste les parts : 2 parts + 1 part = 3 parts.", "Le résultat est $\\frac{3}{5}$."],
        "lvl": 1
      }
    ],
    "PUISSANCES": [
      {
        "q": "Que vaut $10^3 \\times 10^2$ ?",
        "options": ["10^5", "10^6", "100^5", "10^1"],
        "a": "10^5",
        "f": "Produit de puissances de même base : $a^n \\times a^m = a^{n+m}$.",
        "steps": ["Tu multiplies $10$ par lui-même 3 fois, puis encore 2 fois.", "En tout, tu as multiplié $10$ par lui-même $3 + 2 = 5$ fois."],
        "lvl": 2
      }
    ]
  },

  // ==========================================
  // NIVEAU 3ÈME
  // ==========================================
  "ALGEBRA_3EME": {
    "DEVELOPPEMENT": [
      {
        "q": "Développe : $-2(x + 4)$",
        "options": ["-2x - 8", "-2x + 4", "-2x + 8", "2x - 8"],
        "a": "-2x - 8",
        "f": "Distributivité : $k(a+b) = ka + kb$. Attention au signe de $k$ !",
        "steps": ["Multiplie $-2$ par $x$, ce qui donne $-2x$.", "Multiplie $-2$ par $+4$, ce qui donne $-8$.", "Assemble les deux."],
        "lvl": 1
      }
    ],
    "FACTORISATION": [
      {
        "q": "Factorise : $x^2 - 9$",
        "options": ["(x - 3)(x + 3)", "(x - 9)(x + 1)", "(x - 3)^2", "x(x - 9)"],
        "a": "(x - 3)(x + 3)",
        "f": "Identité remarquable : $a^2 - b^2 = (a-b)(a+b)$.",
        "steps": ["Remarque que $9$ est un carré parfait : $3^2$.", "Applique l'identité avec $a=x$ et $b=3$."],
        "lvl": 2
      }
    ]
  },

  // ==========================================
  // NIVEAU SECONDE
  // ==========================================
  "ALGEBRA_SECONDE": {
    "VECTEURS": [
      {
        "q": "Si $A(1 ; 2)$ et $B(4 ; 6)$, quelles sont les coordonnées du vecteur $\\vec{AB}$ ?",
        "options": ["(3 ; 4)", "(5 ; 8)", "(-3 ; -4)", "(4 ; 12)"],
        "a": "(3 ; 4)",
        "f": "Coordonnées de $\\vec{AB} : (x_B - x_A ; y_B - y_A)$. Toujours : Arrivée - Départ.",
        "steps": ["Prends le $x$ de l'arrivée (4) moins le $x$ du départ (1) : $4 - 1 = 3$.", "Prends le $y$ de l'arrivée (6) moins le $y$ du départ (2) : $6 - 2 = 4$."],
        "lvl": 1
      }
    ],
    "EQUATIONS_DROITES": [
      {
        "q": "Quel est le coefficient directeur de la droite d'équation $y = -3x + 5$ ?",
        "options": ["-3", "5", "3", "-3x"],
        "a": "-3",
        "f": "Dans l'équation réduite $y = mx + p$, le coefficient directeur est $m$ (le nombre qui multiplie $x$).",
        "steps": ["Regarde le nombre juste devant le $x$."],
        "lvl": 1
      }
    ]
  },

  // ==========================================
  // NIVEAU PREMIÈRE (Spé)
  // ==========================================
  "ALGEBRA_PREMIERE": {
    "SECOND_DEGRE": [
      {
        "q": "Combien de racines possède l'équation $x^2 + x + 1 = 0$ ?",
        "options": ["0", "1", "2", "Une infinité"],
        "a": "0",
        "f": "Si le discriminant $\\Delta = b^2 - 4ac$ est négatif, l'équation n'a pas de solution réelle.",
        "steps": ["Identifie $a=1, b=1, c=1$.", "Calcule $\\Delta = 1^2 - 4(1)(1) = 1 - 4 = -3$.", "$\\Delta < 0$, la parabole ne coupe jamais l'axe des abscisses."],
        "lvl": 2
      }
    ],
    "DERIVATION": [
      {
        "q": "Quelle est la dérivée de $f(x) = x^3$ ?",
        "options": ["3x^2", "x^2", "3x", "x^4/4"],
        "a": "3x^2",
        "f": "Formule de dérivation : la dérivée de $x^n$ est $n \\cdot x^{n-1}$.",
        "steps": ["L'exposant (3) descend devant le $x$.", "L'ancien exposant diminue de 1 ($3 - 1 = 2$)."],
        "lvl": 1
      }
    ]
  },

  // ==========================================
  // NIVEAU TERMINALE (Spé)
  // ==========================================
  "ALGEBRA_TERMINALE": {
    "LIMITES": [
      {
        "q": "Quelle est la limite de $f(x) = e^x$ quand $x$ tend vers $-\\infty$ ?",
        "options": ["0", "+\\infty", "-\\infty", "1"],
        "a": "0",
        "f": "La fonction exponentielle est strictement positive et s'écrase vers 0 en $-\\infty$.",
        "steps": ["Visualise la courbe de l'exponentielle.", "Quand tu vas tout à gauche du graphique ($-\\infty$), la courbe s'approche de l'axe des abscisses ($y=0$)."],
        "lvl": 1
      }
    ],
    "PRIMITIVES": [
      {
        "q": "Quelle est une primitive de $f(x) = \\cos(x)$ ?",
        "options": ["\\sin(x)", "-\\sin(x)", "-\\cos(x)", "\\tan(x)"],
        "a": "\\sin(x)",
        "f": "La primitive est la fonction qu'il faut dériver pour obtenir $f(x)$.",
        "steps": ["Rappelle-toi le cercle trigonométrique.", "La dérivée de $\\sin(x)$ est $\\cos(x)$."],
        "lvl": 2
      }
    ]
  }
};