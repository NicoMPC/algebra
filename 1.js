// ==================== 1.js - NIVEAU PREMIÈRE (SPÉ MATHS) ====================
window.db = window.db || {};

window.db.ALGEBRA_PREMIERE = {
  catDisplay: {
    SECOND_DEGRE: "Équations du 2nd Degré",
    SIGNE_TRINOME: "Signes & Inéquations",
    DERIVATION: "Dérivation",
    SUITES: "Suites Numériques",
    EXPONENTIELLE: "Fonction Exponentielle",
    VARIATIONS: "Variations & Extremums",
    TRIGONOMETRIE: "Trigonométrie"
  },
  catIcon: {
    SECOND_DEGRE: "🎢",
    SIGNE_TRINOME: "📉",
    DERIVATION: "📈",
    SUITES: "🔢",
    EXPONENTIELLE: "🚀",
    VARIATIONS: "⛰️",
    TRIGONOMETRIE: "📐"
  },
  categories: {
    // =========================================================================
    // 1. ÉQUATIONS DU SECOND DEGRÉ
    // =========================================================================
    SECOND_DEGRE: [
      // NIVEAU 1
      { lvl: 1, q: "$x^2 - 5x + 6 = 0$", a: "$x_1 = 2, x_2 = 3$", options: ["$x_1 = 2, x_2 = 3$", "$x_1 = -2, x_2 = -3$", "$x_1 = 1, x_2 = 6$"], steps: ["Identifie les coefficients : $a=1, b=-5, c=6$.", "Calcule le discriminant : $\\Delta = (-5)^2 - 4(1)(6) = 25 - 24 = 1$.", "Applique les formules des racines : $\\frac{-b \\pm \\sqrt{\\Delta}}{2a}$."], f: "$\\Delta = b^2 - 4ac$" },
      { lvl: 1, q: "$x^2 + 4x + 3 = 0$", a: "$x_1 = -1, x_2 = -3$", options: ["$x_1 = -1, x_2 = -3$", "$x_1 = 1, x_2 = 3$", "$x_1 = 2, x_2 = -2$"], steps: ["$\\Delta = 4^2 - 4(1)(3) = 16 - 12 = 4$.", "$\\sqrt{\\Delta} = 2$. Les racines sont $\\frac{-4 \\pm 2}{2}$."], f: "$x_{1,2} = \\frac{-b \\pm \\sqrt{\\Delta}}{2a}$" },
      { lvl: 1, q: "$x^2 - 2x + 1 = 0$", a: "$x_0 = 1$", options: ["$x_0 = 1$", "$x_0 = -1$", "$x_1 = 1, x_2 = -1$"], steps: ["$\\Delta = (-2)^2 - 4(1)(1) = 0$.", "Une seule racine double : $x_0 = \\frac{-b}{2a}$."], f: "$\\Delta = 0 \\Rightarrow x_0 = \\frac{-b}{2a}$" },
      { lvl: 1, q: "$x^2 + x + 1 = 0$", a: "Pas de solution réelle", options: ["Pas de solution réelle", "$x_0 = 1$", "$x_1 = 1, x_2 = -1$"], steps: ["$\\Delta = 1^2 - 4(1)(1) = -3$.", "Comme $\\Delta < 0$, l'équation n'a pas de solution dans $\\mathbb{R}$."], f: "$\\Delta < 0 \\Rightarrow S = \\emptyset$" },
      { lvl: 1, q: "$2x^2 - 7x + 3 = 0$", a: "$x_1 = 3, x_2 = 0.5$", options: ["$x_1 = 3, x_2 = 0.5$", "$x_1 = -3, x_2 = -0.5$", "$x_1 = 1.5, x_2 = 2$"], steps: ["$\\Delta = (-7)^2 - 4(2)(3) = 49 - 24 = 25$.", "$\\sqrt{\\Delta} = 5$."], f: "$\\Delta = b^2 - 4ac$" },
      { lvl: 1, q: "$x^2 - 9 = 0$", a: "$x_1 = 3, x_2 = -3$", options: ["$x_1 = 3, x_2 = -3$", "$x_0 = 3$", "$x_0 = 9$"], steps: ["Pas besoin de $\\Delta$ ici ! C'est $x^2 = 9$.", "N'oublie pas la racine négative."], f: "$x^2 = k \\Rightarrow x = \\pm \\sqrt{k}$" },
      { lvl: 1, q: "$x^2 + 5x = 0$", a: "$x_1 = 0, x_2 = -5$", options: ["$x_1 = 0, x_2 = -5$", "$x_1 = 1, x_2 = 5$", "$x_0 = -5$"], steps: ["Pas besoin de $\\Delta$. Factorise par $x$.", "$x(x + 5) = 0$."], f: "Équation produit nul" },
      { lvl: 1, q: "$-x^2 + 6x - 5 = 0$", a: "$x_1 = 1, x_2 = 5$", options: ["$x_1 = 1, x_2 = 5$", "$x_1 = -1, x_2 = -5$", "$x_1 = -1, x_2 = 5$"], steps: ["$\\Delta = 6^2 - 4(-1)(-5) = 36 - 20 = 16$.", "Attention aux signes dans $-b / 2a$ : $\\frac{-6 \\pm 4}{-2}$."], f: "$\\Delta = b^2 - 4ac$" },
      { lvl: 1, q: "$3x^2 - 2x - 1 = 0$", a: "$x_1 = 1, x_2 = -\\frac{1}{3}$", options: ["$x_1 = 1, x_2 = -\\frac{1}{3}$", "$x_1 = -1, x_2 = \\frac{1}{3}$", "$x_1 = 1, x_2 = 3$"], steps: ["$\\Delta = (-2)^2 - 4(3)(-1) = 4 + 12 = 16$."], f: "$x_{1,2} = \\frac{-b \\pm \\sqrt{\\Delta}}{2a}$" },
      { lvl: 1, q: "$4x^2 - 12x + 9 = 0$", a: "$x_0 = 1.5$", options: ["$x_0 = 1.5$", "$x_1 = 1.5, x_2 = -1.5$", "$x_0 = -1.5$"], steps: ["$\\Delta = 144 - 144 = 0$. Racine double.", "Remarque : c'était l'identité remarquable $(2x - 3)^2 = 0$."], f: "Racine double" },

      // NIVEAU 2
      { lvl: 2, q: "$-2x^2 + 5x + 3 = 0$", a: "$x_1 = -0.5, x_2 = 3$", options: ["$x_1 = -0.5, x_2 = 3$", "$x_1 = 0.5, x_2 = -3$", "$x_1 = 1, x_2 = 1.5$"], steps: ["$\\Delta = 25 - 4(-2)(3) = 25 + 24 = 49$.", "$\\sqrt{\\Delta} = 7$."], f: "$\\Delta = b^2 - 4ac$" },
      { lvl: 2, q: "$5x^2 - x - 4 = 0$", a: "$x_1 = 1, x_2 = -0.8$", options: ["$x_1 = 1, x_2 = -0.8$", "$x_1 = -1, x_2 = 0.8$", "$x_1 = 1, x_2 = 0.8$"], steps: ["Astuce : si $a+b+c=0$, $x_1=1$ est une racine évidente.", "L'autre racine est $c/a$."], f: "Racines évidentes" },
      { lvl: 2, q: "$\\frac{1}{2}x^2 - 2x + \\frac{3}{2} = 0$", a: "$x_1 = 1, x_2 = 3$", options: ["$x_1 = 1, x_2 = 3$", "$x_1 = -1, x_2 = -3$", "$x_1 = 0.5, x_2 = 1.5$"], steps: ["Multiplie toute l'équation par 2 pour enlever les fractions.", "$x^2 - 4x + 3 = 0$."], f: "Équations équivalentes" },
      { lvl: 2, q: "$x^2 - 2\\sqrt{3}x + 3 = 0$", a: "$x_0 = \\sqrt{3}$", options: ["$x_0 = \\sqrt{3}$", "$x_1 = \\sqrt{3}, x_2 = -\\sqrt{3}$", "$x_0 = 3$"], steps: ["$\\Delta = (-2\\sqrt{3})^2 - 4(1)(3) = 12 - 12 = 0$."], f: "Coefficients irrationnels" },
      { lvl: 2, q: "$x(x - 2) = 3$", a: "$x_1 = 3, x_2 = -1$", options: ["$x_1 = 3, x_2 = -1$", "$x_1 = 3, x_2 = 0$", "$x_1 = -3, x_2 = 1$"], steps: ["Développe et ramène tout à gauche pour avoir $= 0$.", "$x^2 - 2x - 3 = 0$."], f: "Mise sous forme $ax^2+bx+c=0$" },
      { lvl: 2, q: "$(2x-1)^2 = 9$", a: "$x_1 = 2, x_2 = -1$", options: ["$x_1 = 2, x_2 = -1$", "$x_1 = 4, x_2 = -2$", "$x_1 = 2, x_2 = -2$"], steps: ["Évite $\\Delta$ ! Résous $2x-1 = 3$ et $2x-1 = -3$."], f: "$X^2 = k$" },
      { lvl: 2, q: "$2x^2 + 5x - 7 = 0$", a: "$x_1 = 1, x_2 = -3.5$", options: ["$x_1 = 1, x_2 = -3.5$", "$x_1 = -1, x_2 = 3.5$", "$x_1 = 1, x_2 = 3.5$"], steps: ["Racine évidente : la somme des coefficients est nulle, donc 1 est racine."], f: "Racine évidente $x=1$" },

      // NIVEAU 3
      { lvl: 3, q: "$x^4 - 5x^2 + 4 = 0$", a: "$x \\in \\{-2, -1, 1, 2\\}$", options: ["$x \\in \\{-2, -1, 1, 2\\}$", "$x \\in \\{1, 4\\}$", "$x \\in \\{-4, -1, 1, 4\\}$"], steps: ["C'est une équation bicarrée.", "Pose le changement de variable $X = x^2$.", "Résous $X^2 - 5X + 4 = 0$, puis déduis $x$."], f: "Changement de variable" },
      { lvl: 3, q: "$\\frac{2x^2 - 3x + 1}{x - 1} = 0$", a: "$x = 0.5$", options: ["$x = 0.5$", "Pas de solution", "$x = 0.5 \\text{ et } x = 1$"], steps: ["Le numérateur s'annule pour $x=1$ et $x=0.5$.", "Mais attention, $x=1$ est une valeur interdite pour le dénominateur !"], f: "Quotient et ensemble de définition" },
      { lvl: 3, q: "$x^4 - 13x^2 + 36 = 0$", a: "$x \\in \\{-3, -2, 2, 3\\}$", options: ["$x \\in \\{-3, -2, 2, 3\\}$", "$x \\in \\{4, 9\\}$", "$x \\in \\{-9, -4, 4, 9\\}$"], steps: ["Pose $X = x^2$. L'équation devient $X^2 - 13X + 36 = 0$.", "Racines de $X$ : 4 et 9. Donc $x^2 = 4$ ou $x^2 = 9$."], f: "Équation bicarrée" }
    ],

    // =========================================================================
    // 2. SIGNE DU TRINÔME ET INÉQUATIONS
    // =========================================================================
    SIGNE_TRINOME: [
      // NIVEAU 1
      { lvl: 1, q: "Donner le signe de $x^2 - 3x + 2$", a: "Positif à l'extérieur des racines (1 et 2)", options: ["Positif à l'extérieur des racines (1 et 2)", "Positif entre les racines (1 et 2)", "Toujours positif"], steps: ["Racines : $x_1=1, x_2=2$.", "Le coefficient $a=1$ est positif (parabole en U).", "C'est du signe de $a$ à l'extérieur des racines."], f: "Signe de $ax^2+bx+c$" },
      { lvl: 1, q: "Donner le signe de $-x^2 + 4x - 3$", a: "Positif entre les racines (1 et 3)", options: ["Positif entre les racines (1 et 3)", "Positif à l'extérieur des racines (1 et 3)", "Toujours négatif"], steps: ["Racines : 1 et 3.", "$a=-1$ (parabole en cloche). Signe de $-a$ (donc $+$) entre les racines."], f: "Signe du trinôme" },
      { lvl: 1, q: "Résoudre $x^2 - 4 > 0$", a: "$x \\in ]-\\infty; -2[ \\cup ]2; +\\infty[$", options: ["$x \\in ]-\\infty; -2[ \\cup ]2; +\\infty[$", "$x \\in ]-2 ; 2[$", "$x \\in ]2 ; +\\infty[$"], steps: ["Racines : $-2$ et $2$.", "On veut que ce soit strictement positif (signe de $a$)."], f: "Inéquation du 2nd degré" },
      { lvl: 1, q: "Résoudre $-2x^2 + 8 \\geq 0$", a: "$x \\in [-2 ; 2]$", options: ["$x \\in [-2 ; 2]$", "$x \\in ]-\\infty; -2] \\cup [2; +\\infty[$", "$x \\in [0 ; 4]$"], steps: ["Racines : $-2$ et $2$.", "On veut le signe positif, soit le signe opposé à $a=-2$. C'est entre les racines."], f: "Inéquation du 2nd degré" },
      { lvl: 1, q: "Donner le signe de $x^2 + x + 1$", a: "Toujours positif", options: ["Toujours positif", "Toujours négatif", "Positif pour $x > 0$"], steps: ["$\\Delta = -3$ (pas de racine).", "La parabole ne coupe jamais l'axe. Elle est toujours du signe de $a$ (ici 1, positif)."], f: "$\\text{Si } \\Delta < 0$, toujours du signe de $a$" },
      { lvl: 1, q: "Donner le signe de $-2x^2 - 5$", a: "Toujours négatif", options: ["Toujours négatif", "Toujours positif", "Négatif pour $x < 0$"], steps: ["$\\Delta < 0$ et $a = -2$.", "Toujours du signe de $a$."], f: "$\\text{Si } \\Delta < 0$, toujours du signe de $a$" },
      { lvl: 1, q: "Résoudre $x^2 + 6x + 9 \\leq 0$", a: "$x = -3$", options: ["$x = -3$", "$x \\in [-3 ; 3]$", "Pas de solution"], steps: ["C'est l'identité $(x+3)^2 \\leq 0$.", "Un carré n'est jamais strictement négatif. Il ne peut être que nul, en $x=-3$."], f: "Signe d'un carré parfait" },
      { lvl: 1, q: "Résoudre $x^2 - 5x \\leq 0$", a: "$x \\in [0 ; 5]$", options: ["$x \\in [0 ; 5]$", "$x \\in ]-\\infty; 0] \\cup [5; +\\infty[$", "$x = 5$"], steps: ["Racines évidentes : $0$ et $5$.", "On veut $\\leq 0$, donc entre les racines car $a=1>0$."], f: "Racines sans $\\Delta$" },
      { lvl: 1, q: "Résoudre $(x-1)(x-4) > 0$", a: "$x \\in ]-\\infty; 1[ \\cup ]4; +\\infty[$", options: ["$x \\in ]-\\infty; 1[ \\cup ]4; +\\infty[$", "$x \\in ]1 ; 4[$", "$x \\in ]-\\infty; -4[ \\cup ]-1; +\\infty[$"], steps: ["Les racines sont déjà données : 1 et 4.", "En développant, $a = 1 > 0$. Positif à l'extérieur."], f: "Signe forme factorisée" },
      { lvl: 1, q: "Résoudre $-x^2 + 2x - 1 < 0$", a: "$x \\in \\mathbb{R} \\setminus \\{1\\}$", options: ["$x \\in \\mathbb{R} \\setminus \\{1\\}$", "$x \\in \\mathbb{R}$", "Pas de solution"], steps: ["C'est $-(x-1)^2 < 0$.", "C'est toujours strictement négatif, sauf en 1 où ça vaut 0."], f: "$\\Delta = 0$" },

      // NIVEAU 2
      { lvl: 2, q: "Résoudre $x^2 - 3x > 4$", a: "$x \\in ]-\\infty; -1[ \\cup ]4; +\\infty[$", options: ["$x \\in ]-\\infty; -1[ \\cup ]4; +\\infty[$", "$x \\in ]-1 ; 4[$", "$x \\in ]-\\infty; -4[ \\cup ]1; +\\infty[$"], steps: ["Ramène tout à gauche ! $x^2 - 3x - 4 > 0$.", "Racines de $x^2 - 3x - 4 = 0$ : $-1$ et $4$."], f: "Se ramener à $> 0$" },
      { lvl: 2, q: "Résoudre $2x^2 \\leq x + 1$", a: "$x \\in [-0.5 ; 1]$", options: ["$x \\in [-0.5 ; 1]$", "$x \\in ]-\\infty; -0.5] \\cup [1; +\\infty[$", "$x \\in [-1 ; 0.5]$"], steps: ["$2x^2 - x - 1 \\leq 0$.", "Racines : $1$ et $-0.5$. On prend entre les racines."], f: "Se ramener à $\\leq 0$" },
      { lvl: 2, q: "Résoudre $\\frac{x^2 - 4}{x - 1} \\geq 0$", a: "$x \\in [-2; 1[ \\cup [2; +\\infty[$", options: ["$x \\in [-2; 1[ \\cup [2; +\\infty[$", "$x \\in ]-\\infty; -2] \\cup ]1; 2]$", "$x \\in [-2; 2]$"], steps: ["Tableau de signes à deux lignes.", "Ligne 1 : racines -2 et 2. Ligne 2 : racine 1 (valeur interdite)."], f: "Signe d'un quotient" },
      { lvl: 2, q: "Résoudre $\\frac{x^2 + x + 1}{x - 2} > 0$", a: "$x \\in ]2 ; +\\infty[$", options: ["$x \\in ]2 ; +\\infty[$", "$x \\in ]-\\infty ; 2[$", "$x \\in \\mathbb{R} \\setminus \\{2\\}$"], steps: ["Le numérateur a $\\Delta < 0$, il est toujours positif.", "Le signe ne dépend que du dénominateur $x - 2 > 0$."], f: "Simplification d'étude de signe" },
      { lvl: 2, q: "Résoudre $x^3 - 4x \\geq 0$", a: "$x \\in [-2; 0] \\cup [2; +\\infty[$", options: ["$x \\in [-2; 0] \\cup [2; +\\infty[$", "$x \\in ]-\\infty; -2] \\cup [0; 2]$", "$x \\in [2; +\\infty[$"], steps: ["Factorise : $x(x^2 - 4) \\geq 0$.", "Fais un tableau de signes complet avec $x$, $(x-2)$, $(x+2)$."], f: "Inéquation degré 3" },
      { lvl: 2, q: "Résoudre $-3x^2 + 2x - 5 > 0$", a: "Pas de solution", options: ["Pas de solution", "$x \\in \\mathbb{R}$", "$x \\in ]-5; 3[$"], steps: ["$\\Delta = 4 - 60 = -56 < 0$.", "Le trinôme est toujours du signe de $a=-3$, donc toujours négatif."], f: "$\\text{Si } \\Delta < 0$, pas de changement de signe" },
      { lvl: 2, q: "Résoudre $x^2 < 2x$", a: "$x \\in ]0 ; 2[$", options: ["$x \\in ]0 ; 2[$", "$x \\in ]-\\infty; 0[ \\cup ]2; +\\infty[$", "$x \\in ]-2 ; 0[$"], steps: ["$x^2 - 2x < 0$, soit $x(x-2) < 0$.", "Racines 0 et 2. On prend entre les racines."], f: "Factorisation directe" },

      // NIVEAU 3
      { lvl: 3, q: "Résoudre $\\frac{-x^2 + 5x - 6}{x^2 - 1} \\geq 0$", a: "$x \\in ]-1; 1[ \\cup [2; 3]$", options: ["$x \\in ]-1; 1[ \\cup [2; 3]$", "$x \\in ]-\\infty; -1[ \\cup ]1; 2] \\cup [3; +\\infty[$", "$x \\in [2; 3]$"], steps: ["1. Numérateur : racines 2 et 3. (Parabole inversée, positive entre 2 et 3).", "2. Dénominateur : valeurs interdites -1 et 1. (Positif à l'extérieur).", "3. Croise tout dans un grand tableau de signes."], f: "Quotient de trinômes" },
      { lvl: 3, q: "Résoudre $x \\geq \\frac{2}{x - 1}$", a: "$x \\in [-1; 1[ \\cup [2; +\\infty[$", options: ["$x \\in [-1; 1[ \\cup [2; +\\infty[$", "$x \\in ]-\\infty; -1] \\cup ]1; 2]$", "$x \\in [2; +\\infty[$"], steps: ["1. Passe tout à gauche : $x - \\frac{2}{x-1} \\geq 0$.", "2. Même dénominateur : $\\frac{x^2 - x - 2}{x - 1} \\geq 0$.", "3. Tableau de signes avec les racines du haut (-1 et 2) et le bas."], f: "Réduction au même dénominateur" },
      { lvl: 3, q: "Trouver $m$ pour que $x^2 + mx + 1 > 0$ sur $\\mathbb{R}$", a: "$m \\in ]-2 ; 2[$", options: ["$m \\in ]-2 ; 2[$", "$m \\in ]-\\infty; -2[ \\cup ]2; +\\infty[$", "$m \\in ]0 ; 4[$"], steps: ["Pour qu'un trinôme soit toujours strictement positif, il faut $a > 0$ et $\\Delta < 0$.", "$\\Delta = m^2 - 4$. On veut $m^2 - 4 < 0$."], f: "Trinôme paramétré" }
    ],

    // =========================================================================
    // 3. DÉRIVATION
    // =========================================================================
    DERIVATION: [
      // NIVEAU 1
      { lvl: 1, q: "Dériver $f(x) = x^2$", a: "$f'(x) = 2x$", options: ["$f'(x) = 2x$", "$f'(x) = x$", "$f'(x) = 2x^2$"], steps: ["L'exposant 2 'tombe' devant et on baisse l'exposant de 1."], f: "$(x^n)' = n x^{n-1}$" },
      { lvl: 1, q: "Dériver $f(x) = x^3$", a: "$f'(x) = 3x^2$", options: ["$f'(x) = 3x^2$", "$f'(x) = 2x^3$", "$f'(x) = 3x$"], steps: ["L'exposant 3 passe devant, le nouvel exposant est 2."], f: "$(x^n)' = n x^{n-1}$" },
      { lvl: 1, q: "Dériver $f(x) = 5x + 3$", a: "$f'(x) = 5$", options: ["$f'(x) = 5$", "$f'(x) = 5x$", "$f'(x) = 8$"], steps: ["La dérivée de $ax + b$ est simplement $a$."], f: "$(ax+b)' = a$" },
      { lvl: 1, q: "Dériver $f(x) = 7$", a: "$f'(x) = 0$", options: ["$f'(x) = 0$", "$f'(x) = 7x$", "$f'(x) = 1$"], steps: ["La dérivée d'une constante (un nombre seul) est toujours nulle."], f: "$(k)' = 0$" },
      { lvl: 1, q: "Dériver $f(x) = 4x^2$", a: "$f'(x) = 8x$", options: ["$f'(x) = 8x$", "$f'(x) = 4x$", "$f'(x) = 2x$"], steps: ["On garde le coefficient multiplicateur : $4 \\times (2x)$."], f: "$(ku)' = k u'$" },
      { lvl: 1, q: "Dériver $f(x) = x^4 - 2x^3 + x$", a: "$f'(x) = 4x^3 - 6x^2 + 1$", options: ["$f'(x) = 4x^3 - 6x^2 + 1$", "$f'(x) = 4x^3 - 6x^2$", "$f'(x) = x^3 - 6x^2 + 1$"], steps: ["Dérive chaque terme séparément en additionnant."], f: "$(u+v)' = u' + v'$" },
      { lvl: 1, q: "Dériver $f(x) = -3x^2 + 5x - 8$", a: "$f'(x) = -6x + 5$", options: ["$f'(x) = -6x + 5$", "$f'(x) = -3x + 5$", "$f'(x) = -6x - 8$"], steps: ["$-3 \\times 2x + 5$."], f: "$(u+v)' = u' + v'$" },
      { lvl: 1, q: "Dériver $f(x) = \\frac{1}{x}$", a: "$f'(x) = -\\frac{1}{x^2}$", options: ["$f'(x) = -\\frac{1}{x^2}$", "$f'(x) = \\frac{1}{x^2}$", "$f'(x) = -\\frac{1}{x}$"], steps: ["C'est une formule de cours à connaître par cœur."], f: "$(\\frac{1}{x})' = -\\frac{1}{x^2}$" },
      { lvl: 1, q: "Dériver $f(x) = \\sqrt{x}$", a: "$f'(x) = \\frac{1}{2\\sqrt{x}}$", options: ["$f'(x) = \\frac{1}{2\\sqrt{x}}$", "$f'(x) = \\frac{1}{\\sqrt{x}}$", "$f'(x) = -\\frac{1}{2\\sqrt{x}}$"], steps: ["Formule de cours, valable pour $x > 0$."], f: "$(\\sqrt{x})' = \\frac{1}{2\\sqrt{x}}$" },
      { lvl: 1, q: "Dériver $f(x) = \\frac{x^3}{3}$", a: "$f'(x) = x^2$", options: ["$f'(x) = x^2$", "$f'(x) = 3x^2$", "$f'(x) = \\frac{x^2}{3}$"], steps: ["C'est $\\frac{1}{3} \\times x^3$. La dérivée est $\\frac{1}{3} \\times 3x^2 = x^2$."], f: "$(ku)' = k u'$" },

      // NIVEAU 2
      { lvl: 2, q: "Dériver $f(x) = x \\sqrt{x}$", a: "$f'(x) = \\frac{3}{2}\\sqrt{x}$", options: ["$f'(x) = \\frac{3}{2}\\sqrt{x}$", "$f'(x) = \\frac{1}{2\\sqrt{x}}$", "$f'(x) = \\sqrt{x} + \\frac{1}{2\\sqrt{x}}$"], steps: ["Utilise la formule du produit $(uv)' = u'v + uv'$.", "Avec $u = x$ et $v = \\sqrt{x}$."], f: "$(uv)' = u'v + uv'$" },
      { lvl: 2, q: "Dériver $f(x) = (2x+1)(x^2 - 3)$", a: "$f'(x) = 6x^2 + 2x - 6$", options: ["$f'(x) = 6x^2 + 2x - 6$", "$f'(x) = 2x^2 - 6$", "$f'(x) = 6x^2 - 6$"], steps: ["Méthode 1 : utilise $(uv)'$.", "Méthode 2 : Développe d'abord (plus simple ici), puis dérive !"], f: "Développement préalable" },
      { lvl: 2, q: "Dériver $f(x) = \\frac{3}{x^2 + 1}$", a: "$f'(x) = \\frac{-6x}{(x^2 + 1)^2}$", options: ["$f'(x) = \\frac{-6x}{(x^2 + 1)^2}$", "$f'(x) = \\frac{6x}{(x^2 + 1)^2}$", "$f'(x) = \\frac{-3}{(x^2 + 1)^2}$"], steps: ["Formule : $(\\frac{k}{u})' = -\\frac{k u'}{u^2}$.", "Ici $u = x^2+1$, donc $u' = 2x$."], f: "$(\\frac{1}{u})' = -\\frac{u'}{u^2}$" },
      { lvl: 2, q: "Dériver $f(x) = (3x - 5)^2$", a: "$f'(x) = 6(3x - 5)$", options: ["$f'(x) = 6(3x - 5)$", "$f'(x) = 2(3x - 5)$", "$f'(x) = 18x - 15$"], steps: ["Développe d'abord ou utilise la formule des fonctions composées."], f: "$(u^2)' = 2u'u$" },
      { lvl: 2, q: "Dériver $f(x) = \\frac{2x - 1}{x + 4}$", a: "$f'(x) = \\frac{9}{(x + 4)^2}$", options: ["$f'(x) = \\frac{9}{(x + 4)^2}$", "$f'(x) = \\frac{7}{(x + 4)^2}$", "$f'(x) = \\frac{2x - 1}{(x + 4)^2}$"], steps: ["Formule du quotient. $u = 2x-1$, $v = x+4$.", "Numérateur de la dérivée : $u'v - uv' = 2(x+4) - (2x-1)(1)$."], f: "$(\\frac{u}{v})' = \\frac{u'v - uv'}{v^2}$" },
      { lvl: 2, q: "Équation de la tangente à $f(x)=x^2$ en $a=3$", a: "$y = 6x - 9$", options: ["$y = 6x - 9$", "$y = 6x + 9$", "$y = 2x - 3$"], steps: ["$f(3) = 9$.", "$f'(x) = 2x$ donc $f'(3) = 6$.", "Formule : $y = f'(a)(x-a) + f(a)$."], f: "$y = f'(a)(x-a) + f(a)$" },
      { lvl: 2, q: "Équation de la tangente à $f(x)=\\frac{1}{x}$ en $a=-1$", a: "$y = -x - 2$", options: ["$y = -x - 2$", "$y = x + 2$", "$y = -x + 2$"], steps: ["$f(-1) = -1$. $f'(x) = -1/x^2$ donc $f'(-1) = -1$.", "$y = -1(x - (-1)) - 1$."], f: "$y = f'(a)(x-a) + f(a)$" },

      // NIVEAU 3
      { lvl: 3, q: "Dériver $f(x) = \\frac{x^2 - 3x + 1}{2x + 1}$", a: "$f'(x) = \\frac{2x^2 + 2x - 5}{(2x + 1)^2}$", options: ["$f'(x) = \\frac{2x^2 + 2x - 5}{(2x + 1)^2}$", "$f'(x) = \\frac{2x^2 - 2x + 5}{(2x + 1)^2}$", "$f'(x) = \\frac{2x - 3}{(2x + 1)^2}$"], steps: ["Formule $u/v$.", "$u' = 2x-3$, $v' = 2$.", "Développe soigneusement le numérateur : $(2x-3)(2x+1) - (x^2-3x+1)(2)$."], f: "$(\\frac{u}{v})' = \\frac{u'v - uv'}{v^2}$" },
      { lvl: 3, q: "Dériver $f(x) = \\sqrt{x^2 + x + 1}$", a: "$f'(x) = \\frac{2x + 1}{2\\sqrt{x^2 + x + 1}}$", options: ["$f'(x) = \\frac{2x + 1}{2\\sqrt{x^2 + x + 1}}$", "$f'(x) = \\frac{1}{2\\sqrt{x^2 + x + 1}}$", "$f'(x) = \\frac{2x + 1}{\\sqrt{x^2 + x + 1}}$"], steps: ["Formule de la racine d'une fonction : $(\\sqrt{u})' = \\frac{u'}{2\\sqrt{u}}$.", "Ici $u = x^2+x+1$ donc $u' = 2x+1$."], f: "$(\\sqrt{u})' = \\frac{u'}{2\\sqrt{u}}$" },
      { lvl: 3, q: "Dériver $f(x) = (x^2 - x)^3$", a: "$f'(x) = 3(2x - 1)(x^2 - x)^2$", options: ["$f'(x) = 3(2x - 1)(x^2 - x)^2$", "$f'(x) = 3(x^2 - x)^2$", "$f'(x) = (2x - 1)(x^2 - x)^2$"], steps: ["Formule de la puissance d'une fonction : $(u^n)' = n u' u^{n-1}$."], f: "$(u^n)' = n u' u^{n-1}$" }
    ],

    // =========================================================================
    // 4. SUITES NUMÉRIQUES
    // =========================================================================
    SUITES: [
      // NIVEAU 1
      { lvl: 1, q: "Suite arithmétique $u_0 = 5$, $r = 3$. $u_{10} = ?$", a: "$u_{10} = 35$", options: ["$u_{10} = 35$", "$u_{10} = 30$", "$u_{10} = 50$"], steps: ["La formule explicite est $u_n = u_0 + n \\times r$.", "$u_{10} = 5 + 10 \\times 3$."], f: "$u_n = u_0 + nr$" },
      { lvl: 1, q: "Suite géométrique $v_0 = 2$, $q = 3$. $v_4 = ?$", a: "$v_4 = 162$", options: ["$v_4 = 162$", "$v_4 = 54$", "$v_4 = 24$"], steps: ["La formule explicite est $v_n = v_0 \\times q^n$.", "$v_4 = 2 \\times 3^4 = 2 \\times 81$."], f: "$v_n = v_0 \\times q^n$" },
      { lvl: 1, q: "Arithmétique : $u_2 = 10, u_3 = 14$. Trouver la raison $r$.", a: "$r = 4$", options: ["$r = 4$", "$r = 2$", "$r = -4$"], steps: ["Dans une suite arithmétique, on passe d'un terme au suivant en ajoutant $r$.", "$r = u_3 - u_2 = 14 - 10$."], f: "$u_{n+1} - u_n = r$" },
      { lvl: 1, q: "Géométrique : $v_1 = 3, v_2 = 15$. Trouver la raison $q$.", a: "$q = 5$", options: ["$q = 5$", "$q = 12$", "$q = 3$"], steps: ["Dans une suite géométrique, on multiplie par $q$.", "$q = \\frac{v_2}{v_1} = \\frac{15}{3}$."], f: "$\\frac{v_{n+1}}{v_n} = q$" },
      { lvl: 1, q: "Suite $u_n = n^2 - 1$. Calculer $u_5$.", a: "$u_5 = 24$", options: ["$u_5 = 24$", "$u_5 = 25$", "$u_5 = 9$"], steps: ["C'est une suite définie de manière explicite. Remplace juste $n$ par 5.", "$5^2 - 1$."], f: "$u_n = f(n)$" },
      { lvl: 1, q: "Arithmétique : $u_0 = 100, r = -2$. $u_{50} = ?$", a: "$u_{50} = 0$", options: ["$u_{50} = 0$", "$u_{50} = -100$", "$u_{50} = 2$"], steps: ["$u_{50} = 100 + 50 \\times (-2)$."], f: "$u_n = u_0 + nr$" },
      { lvl: 1, q: "Géométrique : $v_0 = 64, q = 0.5$. $v_3 = ?$", a: "$v_3 = 8$", options: ["$v_3 = 8$", "$v_3 = 16$", "$v_3 = 32$"], steps: ["Multiplier par 0.5 revient à diviser par 2.", "$64 \\times (0.5)^3 = 64 / 8$."], f: "$v_n = v_0 \\times q^n$" },
      { lvl: 1, q: "$u_{n+1} = 2u_n + 1$ avec $u_0 = 3$. Calculer $u_2$.", a: "$u_2 = 15$", options: ["$u_2 = 15$", "$u_2 = 7$", "$u_2 = 31$"], steps: ["Calcule d'abord $u_1$ : $2(3) + 1 = 7$.", "Puis $u_2$ : $2(7) + 1 = 15$."], f: "Suite récurrente" },
      { lvl: 1, q: "Arithmétique : $u_5 = 20, r = 3$. Trouver $u_0$.", a: "$u_0 = 5$", options: ["$u_0 = 5$", "$u_0 = 15$", "$u_0 = -5$"], steps: ["Pour reculer de 5 crans, on enlève 5 fois la raison.", "$u_0 = u_5 - 5 \\times 3 = 20 - 15$."], f: "$u_0 = u_n - nr$" },
      { lvl: 1, q: "Exprimer $v_{n+1}$ en fonction de $v_n$ (géométrique de raison 2).", a: "$v_{n+1} = 2v_n$", options: ["$v_{n+1} = 2v_n$", "$v_{n+1} = v_n + 2$", "$v_{n+1} = v_n^2$"], steps: ["C'est la définition même d'une suite géométrique."], f: "$v_{n+1} = q \\times v_n$" },

      // NIVEAU 2
      { lvl: 2, q: "Arithmétique : $u_3 = 12, u_8 = 32$. Trouver $r$.", a: "$r = 4$", options: ["$r = 4$", "$r = 5$", "$r = 20$"], steps: ["Pour aller de $u_3$ à $u_8$, il y a 5 sauts ($8-3$).", "Donc $5r = 32 - 12 = 20$."], f: "$u_p = u_k + (p-k)r$" },
      { lvl: 2, q: "Somme : $S = 1 + 2 + 3 + ... + 100$", a: "$S = 5050$", options: ["$S = 5050$", "$S = 5000$", "$S = 10100$"], steps: ["Formule : $\\text{Nombre de termes} \\times \\frac{\\text{Premier} + \\text{Dernier}}{2}$.", "$100 \\times \\frac{1 + 100}{2}$."], f: "$S = n \\frac{u_0 + u_{n-1}}{2}$" },
      { lvl: 2, q: "Somme : $1 + 2 + 4 + 8 + ... + 1024$", a: "$S = 2047$", options: ["$S = 2047$", "$S = 1024$", "$S = 2048$"], steps: ["C'est une somme géométrique de raison 2. Il y a 11 termes ($2^0$ à $2^{10}$).", "Formule : $\\text{Premier} \\times \\frac{1 - q^{\\text{nb termes}}}{1 - q}$."], f: "$S = u_0 \\frac{1 - q^n}{1 - q}$" },
      { lvl: 2, q: "Suite $u_n = 3n - 5$. Est-elle arithmétique ?", a: "Oui, de raison $r = 3$", options: ["Oui, de raison $r = 3$", "Oui, de raison $r = -5$", "Non"], steps: ["Calcule $u_{n+1} - u_n$.", "$(3(n+1) - 5) - (3n - 5) = 3n + 3 - 5 - 3n + 5 = 3$."], f: "$u_{n+1} - u_n = \\text{constante}$" },
      { lvl: 2, q: "Suite $v_n = 4 \\times 5^n$. Est-elle géométrique ?", a: "Oui, de raison $q = 5$", options: ["Oui, de raison $q = 5$", "Oui, de raison $q = 4$", "Non"], steps: ["Calcule $\\frac{v_{n+1}}{v_n}$.", "$\\frac{4 \\times 5^{n+1}}{4 \\times 5^n} = 5$."], f: "$\\frac{v_{n+1}}{v_n} = \\text{constante}$" },
      { lvl: 2, q: "Somme des 10 premiers termes de $u_n = 2n + 1$ ($u_0$ à $u_9$)", a: "$S = 100$", options: ["$S = 100$", "$S = 120$", "$S = 190$"], steps: ["$u_0 = 1$, $u_9 = 19$.", "Somme : $10 \\times \\frac{1 + 19}{2} = 100$."], f: "$S = n \\frac{\\text{1er} + \\text{Dernier}}{2}$" },
      { lvl: 2, q: "Géométrique : $v_2 = 9, v_4 = 81$ (termes positifs). Trouver $q$.", a: "$q = 3$", options: ["$q = 3$", "$q = 9$", "$q = 81$"], steps: ["$v_4 = v_2 \\times q^2$. Donc $q^2 = 81 / 9 = 9$.", "Comme les termes sont positifs, $q = \\sqrt{9} = 3$."], f: "$v_p = v_k \\times q^{p-k}$" },

      // NIVEAU 3
      { lvl: 3, q: "Soit $u_{n+1} = 2u_n - 3$. On pose $v_n = u_n - 3$. Nature de $v_n$ ?", a: "Géométrique de raison $q = 2$", options: ["Géométrique de raison $q = 2$", "Arithmétique de raison $r = -3$", "Ni l'un ni l'autre"], steps: ["Calcule $v_{n+1} = u_{n+1} - 3$.", "Remplace $u_{n+1}$ : $(2u_n - 3) - 3 = 2u_n - 6$.", "Factorise par 2 : $2(u_n - 3) = 2v_n$."], f: "Suite auxiliaire" },
      { lvl: 3, q: "À partir de quel $n$ a-t-on $2^n > 1000$ ?", a: "$n = 10$", options: ["$n = 10$", "$n = 9$", "$n = 11$"], steps: ["Utilise les puissances de 2 connues.", "$2^{10} = 1024$."], f: "Recherche de seuil" },
      { lvl: 3, q: "Limite de la somme $S = 1 + \\frac{1}{2} + \\frac{1}{4} + \\frac{1}{8} + ...$", a: "$S = 2$", options: ["$S = 2$", "$S = 1.5$", "$S = +\\infty$"], steps: ["Somme géométrique infinie avec $|q| < 1$.", "Formule : $\\frac{\\text{Premier terme}}{1 - q} = \\frac{1}{1 - 0.5}$."], f: "$S_\\infty = \\frac{u_0}{1-q}$" }
    ],

    // =========================================================================
    // 5. FONCTION EXPONENTIELLE
    // =========================================================================
    EXPONENTIELLE: [
      // NIVEAU 1
      { lvl: 1, q: "Simplifier $e^3 \\times e^5$", a: "$e^8$", options: ["$e^8$", "$e^{15}$", "$e^2$"], steps: ["On additionne les exposants lorsqu'on multiplie."], f: "$e^a \\times e^b = e^{a+b}$" },
      { lvl: 1, q: "Simplifier $\\frac{e^7}{e^4}$", a: "$e^3$", options: ["$e^3$", "$e^{11}$", "$e^{7/4}$"], steps: ["On soustrait l'exposant du dénominateur."], f: "$\\frac{e^a}{e^b} = e^{a-b}$" },
      { lvl: 1, q: "Simplifier $(e^{2x})^3$", a: "$e^{6x}$", options: ["$e^{6x}$", "$e^{2x+3}$", "$e^{8x^3}$"], steps: ["Puissance de puissance : on multiplie les exposants."], f: "$(e^a)^b = e^{a \\times b}$" },
      { lvl: 1, q: "Simplifier $e^x \\times e^{-x}$", a: "$1$", options: ["$1$", "$e^{-x^2}$", "$0$"], steps: ["$x + (-x) = 0$. Et tout nombre à la puissance 0 vaut 1."], f: "$e^0 = 1$" },
      { lvl: 1, q: "Dériver $f(x) = e^x + 3x$", a: "$f'(x) = e^x + 3$", options: ["$f'(x) = e^x + 3$", "$f'(x) = xe^x + 3$", "$f'(x) = e^x$"], steps: ["La fonction exponentielle $e^x$ a pour particularité d'être sa propre dérivée."], f: "$(e^x)' = e^x$" },

      // NIVEAU 2
      { lvl: 2, q: "Résoudre $e^{x+2} = e^5$", a: "$x = 3$", options: ["$x = 3$", "$x = 7$", "$x = 2.5$"], steps: ["Si $e^A = e^B$, alors $A = B$.", "Donc $x + 2 = 5$."], f: "$e^a = e^b \\iff a = b$" },
      { lvl: 2, q: "Résoudre $e^{2x} = 1$", a: "$x = 0$", options: ["$x = 0$", "$x = 1$", "Pas de solution"], steps: ["Rappelle-toi que $1 = e^0$.", "Donc $2x = 0$."], f: "$e^0 = 1$" },
      { lvl: 2, q: "Dériver $f(x) = e^{3x+1}$", a: "$f'(x) = 3e^{3x+1}$", options: ["$f'(x) = 3e^{3x+1}$", "$f'(x) = e^{3x+1}$", "$f'(x) = 3xe^{3x+1}$"], steps: ["La dérivée de $e^{u(x)}$ est $u'(x) \\times e^{u(x)}$.", "Ici $u(x) = 3x+1$, sa dérivée est $3$."], f: "$(e^{u})' = u' e^{u}$" },

      // NIVEAU 3
      { lvl: 3, q: "Résoudre $e^{2x} - 3e^x + 2 = 0$", a: "$x = 0 \\text{ ou } x = \\ln(2)$", options: ["$x = 0 \\text{ ou } x = \\ln(2)$", "$x = 1 \\text{ ou } x = 2$", "Pas de solution"], steps: ["Remarque que $e^{2x} = (e^x)^2$. Pose $X = e^x$.", "L'équation devient $X^2 - 3X + 2 = 0$. Les solutions sont $X=1$ et $X=2$.", "Reviens à $x$ : $e^x = 1 \\Rightarrow x = 0$ et $e^x = 2 \\Rightarrow x = \\ln(2)$."], f: "Changement de variable $X=e^x$" },
      { lvl: 3, q: "Dériver $f(x) = x e^x$", a: "$f'(x) = (x+1)e^x$", options: ["$f'(x) = (x+1)e^x$", "$f'(x) = e^x$", "$f'(x) = x e^x + 1$"], steps: ["Formule du produit $(uv)' = u'v + uv'$.", "Avec $u=x$ ($u'=1$) et $v=e^x$ ($v'=e^x$).", "Ça donne $1 \\times e^x + x \\times e^x$. Factorise par $e^x$."], f: "$(uv)' = u'v + uv'$" }
    ],

    // =========================================================================
    // 6. VARIATIONS ET EXTREMUMS (ANALYSE)
    // =========================================================================
    VARIATIONS: [
      // NIVEAU 1
      { lvl: 1, q: "Si $f'(x) > 0$ sur un intervalle $I$, alors $f$ est...", a: "Croissante", options: ["Croissante", "Décroissante", "Constante"], steps: ["Le signe de la dérivée donne le sens de variation de la fonction."], f: "$f'(x) > 0 \\implies f \\nearrow$" },
      { lvl: 1, q: "Si $f'(x) = 0$ en changeant de signe, la courbe de $f$ admet un...", a: "Extremum (minimum ou maximum)", options: ["Extremum (minimum ou maximum)", "Point d'inflexion", "Asymptote"], steps: ["La courbe s'arrête de monter pour descendre (ou l'inverse).", "La tangente y est horizontale."], f: "Extremum local" },
      { lvl: 1, q: "Trouver l'abscisse du sommet de la parabole $f(x) = x^2 - 4x + 1$", a: "$x = 2$", options: ["$x = 2$", "$x = 4$", "$x = -2$"], steps: ["Dérive $f(x)$ et cherche quand $f'(x) = 0$.", "$f'(x) = 2x - 4$.", "$2x - 4 = 0 \\Rightarrow x = 2$."], f: "Extremum $\\iff f'(x) = 0$" },

      // NIVEAU 2
      { lvl: 2, q: "Sur quel intervalle la fonction $f(x) = x^3 - 3x$ est-elle décroissante ?", a: "$[-1 ; 1]$", options: ["$[-1 ; 1]$", "$]-\\infty ; -1]$", "$[1 ; +\\infty[$"], steps: ["Calcule $f'(x) = 3x^2 - 3$.", "Cherche le signe de $f'(x)$ : racines -1 et 1. Parabole en U, négative entre les racines."], f: "Signe de $f'(x)$" },
      { lvl: 2, q: "Valeur du maximum de la fonction $f(x) = -x^2 + 2x + 3$", a: "$4$", options: ["$4$", "$1$", "$3$"], steps: ["$f'(x) = -2x + 2$. S'annule en $x = 1$.", "Calcule l'image du sommet : $f(1) = -1 + 2 + 3 = 4$."], f: "$y = f(x_{sommet})$" },
      { lvl: 2, q: "La dérivée de $f$ est $f'(x) = (x-2)^2$. Que dire de $f$ ?", a: "Elle est toujours croissante", options: ["Elle est toujours croissante", "Elle est décroissante puis croissante", "Elle est toujours décroissante"], steps: ["Un carré est toujours positif ou nul. Donc $f'(x) \\geq 0$.", "Si $f'(x)$ ne change pas de signe, $f$ est strictement monotone."], f: "Signe d'un carré parfait" },

      // NIVEAU 3
      { lvl: 3, q: "Soit $f(x) = (x+2)e^x$. En quel $x$ la fonction atteint-elle son minimum ?", a: "$x = -3$", options: ["$x = -3$", "$x = -2$", "$x = 0$"], steps: ["Dérive avec la formule $(uv)'$ : $f'(x) = 1 \\times e^x + (x+2) \\times e^x$.", "Factorise : $f'(x) = e^x(1 + x + 2) = e^x(x+3)$.", "$e^x$ est toujours positif, donc le signe dépend de $x+3$."], f: "$f'(x) = 0$" },
      { lvl: 3, q: "On sait que $f'(x) = \\frac{1-x}{x^2}$. Sur $]0 ; +\\infty[$, $f$ admet un...", a: "Maximum en $x = 1$", options: ["Maximum en $x = 1$", "Minimum en $x = 1$", "Pas d'extremum"], steps: ["Le dénominateur $x^2$ est toujours positif.", "Le signe de $f'(x)$ dépend du numérateur $1-x$.", "Il est positif avant 1, et négatif après. La fonction monte puis descend."], f: "Changement de signe de $f'$" }
    ],

    // =========================================================================
    // 7. TRIGONOMÉTRIE (ALGÈBRE)
    // =========================================================================
    TRIGONOMETRIE: [
      // NIVEAU 1
      { lvl: 1, q: "Valeur de $\\cos(\\frac{\\pi}{3})$", a: "$0.5$", options: ["$0.5$", "$\\frac{\\sqrt{3}}{2}$", "$\\frac{\\sqrt{2}}{2}$"], steps: ["L'angle $\\pi/3$ correspond à $60^\\circ$.", "Sur l'axe des abscisses, c'est la valeur au milieu."], f: "Valeurs remarquables" },
      { lvl: 1, q: "Valeur de $\\sin(\\frac{\\pi}{2})$", a: "$1$", options: ["$1$", "$0$", "$-1$"], steps: ["L'angle $\\pi/2$ est tout en haut du cercle trigonométrique.", "Son ordonnée (le sinus) y est maximale."], f: "Cercle trigonométrique" },
      { lvl: 1, q: "Simplifier $\\cos^2(x) + \\sin^2(x)$", a: "$1$", options: ["$1$", "$0$", "$\\cos(2x)$"], steps: ["C'est l'identité fondamentale de la trigonométrie.", "Elle vient du théorème de Pythagore dans le cercle de rayon 1."], f: "$\\cos^2(x) + \\sin^2(x) = 1$" },

      // NIVEAU 2
      { lvl: 2, q: "Résoudre $\\sin(x) = 1$ sur $[0 ; 2\\pi]$", a: "$x = \\frac{\\pi}{2}$", options: ["$x = \\frac{\\pi}{2}$", "$x = \\pi$", "$x = 0$"], steps: ["Le sinus se lit sur l'axe vertical.", "Le seul point du cercle de hauteur 1 est le pôle Nord."], f: "Lecture du cercle" },
      { lvl: 2, q: "Résoudre $\\cos(x) = 0$ sur $[0 ; \\pi]$", a: "$x = \\frac{\\pi}{2}$", options: ["$x = \\frac{\\pi}{2}$", "$x = 0$", "$x = \\pi$"], steps: ["Le cosinus se lit sur l'axe horizontal.", "Sur la moitié haute du cercle (de $0$ à $\\pi$), l'abscisse est 0 tout en haut."], f: "Équations trigonométriques" },

      // NIVEAU 3
      { lvl: 3, q: "Résoudre $\\cos(x) = \\frac{1}{2}$ sur $[-\\pi ; \\pi]$", a: "$x = \\frac{\\pi}{3} \\text{ ou } x = -\\frac{\\pi}{3}$", options: ["$x = \\frac{\\pi}{3} \\text{ ou } x = -\\frac{\\pi}{3}$", "$x = \\frac{\\pi}{3}$", "$x = \\frac{\\pi}{6} \\text{ ou } x = -\\frac{\\pi}{6}$"], steps: ["Regarde l'axe horizontal à la graduation $0.5$.", "Il y a deux points correspondants sur le cercle : un en haut, un en bas."], f: "$\\cos(x) = \\cos(\\alpha)$" },
      { lvl: 3, q: "Résoudre $\\sin(x) = -\\frac{\\sqrt{2}}{2}$ sur $]0 ; 2\\pi]$", a: "$x = \\frac{5\\pi}{4} \\text{ ou } x = \\frac{7\\pi}{4}$", options: ["$x = \\frac{5\\pi}{4} \\text{ ou } x = \\frac{7\\pi}{4}$", "$x = -\\frac{\\pi}{4}$", "$x = \\frac{3\\pi}{4} \\text{ ou } x = \\frac{5\\pi}{4}$"], steps: ["Le sinus est négatif, on est dans la moitié basse du cercle.", "La valeur associée à $\\sqrt{2}/2$ est la famille des $\\pi/4$."], f: "$\\sin(x) = \\sin(\\alpha)$" }
    ]
  }
};