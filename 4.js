// ==================== 4.js - NIVEAU 4ÈME ====================
window.db = window.db || {};

window.db.ALGEBRA_4EME = {
  catDisplay: {
    RELATIFS: "Multiplications & Priorités",
    FRACTIONS: "Opérations sur les Fractions",
    PUISSANCES: "Puissances & Règles",
    EQUATIONS: "Équations (Niveau 2)"
  },
  catIcon: {
    RELATIFS: "✖️➗",
    FRACTIONS: "🍕",
    PUISSANCES: "🚀",
    EQUATIONS: "⚖️"
  },
  categories: {
    // =========================================================================
    // 1. RELATIFS (MULTIPLICATIONS, DIVISIONS, PRIORITÉS)
    // =========================================================================
    RELATIFS: [
      // NIVEAU 1 (10 exos) - Règle des signes de base
      { lvl: 1, q: "$(-3) \\times (-4)$", a: "$12$", steps: ["Produit de deux nombres de même signe.", "Le résultat est positif : $3 \\times 4$."], f: "$(-) \\times (-) = (+)$" },
      { lvl: 1, q: "$(-5) \\times (+2)$", a: "$-10$", steps: ["Produit de deux nombres de signes contraires.", "Le résultat est négatif."], f: "$(-) \\times (+) = (-)$" },
      { lvl: 1, q: "$(+6) \\times (-3)$", a: "$-18$", steps: ["Signes contraires, résultat négatif."], f: "$(+) \\times (-) = (-)$" },
      { lvl: 1, q: "$(-8) \\div (-2)$", a: "$4$", steps: ["Quotient de deux nombres de même signe.", "Le résultat est positif : $8 \\div 2$."], f: "$\\frac{-a}{-b} = \\frac{a}{b}$" },
      { lvl: 1, q: "$15 \\div (-3)$", a: "$-5$", steps: ["Quotient de nombres de signes contraires.", "Résultat négatif."], f: "$\\frac{a}{-b} = -\\frac{a}{b}$" },
      { lvl: 1, q: "$(-4) \\times (-1)$", a: "$4$", steps: ["Multiplier par $-1$ donne l'opposé du nombre."], f: "$-a \\times (-1) = a$" },
      { lvl: 1, q: "$(-2) \\times (-2) \\times (-2)$", a: "$-8$", steps: ["Il y a 3 facteurs négatifs (un nombre impair).", "Le résultat final sera négatif."], f: "Règle des signes (impair)" },
      { lvl: 1, q: "$(-5) \\times 0$", a: "$0$", steps: ["Zéro absorbant : tout nombre multiplié par zéro donne zéro."], f: "$a \\times 0 = 0$" },
      { lvl: 1, q: "$(-12) \\div (+4)$", a: "$-3$", steps: ["Signes contraires, division classique."], f: "$\\frac{-a}{b} = -\\frac{a}{b}$" },
      { lvl: 1, q: "$(-1) \\times 7 \\times (-2)$", a: "$14$", steps: ["Il y a 2 facteurs négatifs (pair).", "Le résultat est positif : $1 \\times 7 \\times 2$."], f: "Règle des signes (pair)" },

      // NIVEAU 2 (7 exos) - Priorités opératoires
      { lvl: 2, q: "$4 - 5 \\times (-2)$", a: "$14$", steps: ["La multiplication est prioritaire sur la soustraction !", "Calcule d'abord $-5 \\times (-2)$."], f: "Priorité à la multiplication" },
      { lvl: 2, q: "$(-3) \\times (-4) - 10$", a: "$2$", steps: ["La multiplication est prioritaire.", "Devient : $12 - 10$."], f: "Priorité à la multiplication" },
      { lvl: 2, q: "$\\frac{-15}{3} + 2$", a: "$-3$", steps: ["La division (fraction) est prioritaire.", "Calcule $-15 \\div 3$ d'abord."], f: "Priorité à la division" },
      { lvl: 2, q: "$-4 \\times (2 - 5)$", a: "$12$", steps: ["Les parenthèses sont prioritaires absolues.", "Calcule $2 - 5$ d'abord, ce qui fait $-3$."], f: "Priorité aux parenthèses" },
      { lvl: 2, q: "$10 - (-2) \\times (-3)$", a: "$4$", steps: ["Multiplication d'abord : $(-2) \\times (-3) = 6$.", "Il reste : $10 - 6$."], f: "Priorités opératoires" },
      { lvl: 2, q: "$(-2)^3 + 10$", a: "$2$", steps: ["La puissance est prioritaire.", "$(-2)^3 = (-2) \\times (-2) \\times (-2) = -8$."], f: "Priorité à la puissance" },
      { lvl: 2, q: "$-5 + 2 \\times (-4) + 3$", a: "$-10$", steps: ["Calcule le bloc multiplication : $2 \\times (-4)$.", "Devient $-5 - 8 + 3$."], f: "Priorités opératoires" },

      // NIVEAU 3 (3 exos) - Expressions complexes
      { lvl: 3, q: "$(-2) \\times (-3 + 5) - (-4) \\times 2$", a: "$4$", steps: ["1. Parenthèse : $(-3 + 5) = 2$.", "2. Multiplications : $(-2) \\times 2$ et $(-4) \\times 2$.", "Devient : $-4 - (-8)$."], f: "Priorités en chaîne" },
      { lvl: 3, q: "$\\frac{(-4) \\times 3}{-2 + 8}$", a: "$-2$", steps: ["Calcule tout le numérateur, puis tout le dénominateur.", "Numérateur : $-12$. Dénominateur : $6$."], f: "Fraction comme parenthèse globale" },
      { lvl: 3, q: "$(-3)^2 - (-2)^3$", a: "$17$", steps: ["Calcule les puissances : $(-3)^2 = 9$ et $(-2)^3 = -8$.", "Devient : $9 - (-8)$."], f: "$a - (-b) = a + b$" }
    ],

    // =========================================================================
    // 2. FRACTIONS (PRODUITS & QUOTIENTS)
    // =========================================================================
    FRACTIONS: [
      // NIVEAU 1 (10 exos) - Multiplication et division simples
      { lvl: 1, q: "$\\frac{2}{3} \\times \\frac{4}{5}$", a: "$\\frac{8}{15}$", steps: ["Multiplie les numérateurs entre eux.", "Multiplie les dénominateurs entre eux."], f: "$\\frac{a}{b} \\times \\frac{c}{d} = \\frac{a \\times c}{b \\times d}$" },
      { lvl: 1, q: "$\\frac{-1}{2} \\times \\frac{3}{7}$", a: "$-\\frac{3}{14}$", steps: ["Numérateurs : $-1 \\times 3$.", "Dénominateurs : $2 \\times 7$."], f: "$\\frac{a}{b} \\times \\frac{c}{d} = \\frac{a \\times c}{b \\times d}$" },
      { lvl: 1, q: "$\\frac{2}{3} \\div \\frac{5}{7}$", a: "$\\frac{14}{15}$", steps: ["Diviser par une fraction, c'est multiplier par son inverse.", "Devient : $\\frac{2}{3} \\times \\frac{7}{5}$."], f: "$\\frac{a}{b} \\div \\frac{c}{d} = \\frac{a}{b} \\times \\frac{d}{c}$" },
      { lvl: 1, q: "$4 \\times \\frac{3}{5}$", a: "$\\frac{12}{5}$", steps: ["Un nombre entier $4$ c'est comme $\\frac{4}{1}$.", "Multiplie $4 \\times 3$ en haut."], f: "$n \\times \\frac{a}{b} = \\frac{n \\times a}{b}$" },
      { lvl: 1, q: "$\\frac{-3}{4} \\times \\frac{-8}{9}$", a: "$\\frac{2}{3}$", steps: ["Le produit de deux négatifs est positif.", "Simplifie avant de calculer : $8$ avec $4$, et $9$ avec $3$."], f: "Simplification croisée" },
      { lvl: 1, q: "$\\frac{1}{2} \\div 3$", a: "$\\frac{1}{6}$", steps: ["Diviser par $3$, c'est multiplier par son inverse $\\frac{1}{3}$."], f: "$\\frac{a}{b} \\div n = \\frac{a}{b} \\times \\frac{1}{n}$" },
      { lvl: 1, q: "$\\frac{5}{4} \\times \\frac{4}{5}$", a: "$1$", steps: ["On multiplie une fraction par son inverse.", "Tout se simplifie et devient $1$."], f: "$\\frac{a}{b} \\times \\frac{b}{a} = 1$" },
      { lvl: 1, q: "$\\frac{7}{8} \\times \\frac{16}{21}$", a: "$\\frac{2}{3}$", steps: ["Ne calcule pas $7 \\times 16$ ! Simplifie d'abord.", "Le $16$ en haut se simplifie avec le $8$ en bas.", "Le $21$ en bas se simplifie avec le $7$ en haut."], f: "Décomposition en facteurs" },
      { lvl: 1, q: "$\\frac{3}{2} \\div \\frac{3}{4}$", a: "$2$", steps: ["Transforme en multiplication : $\\frac{3}{2} \\times \\frac{4}{3}$.", "Simplifie les $3$ en haut et en bas."], f: "$\\frac{a}{b} \\div \\frac{c}{d} = \\frac{a}{b} \\times \\frac{d}{c}$" },
      { lvl: 1, q: "$\\frac{-5}{2} \\times \\frac{2}{-5}$", a: "$1$", steps: ["Signes : Moins par moins = Plus.", "Fractions : un nombre multiplié par son inverse = 1."], f: "Inverse fractionnaire" },

      // NIVEAU 2 (7 exos) - Mix additions/multiplications
      { lvl: 2, q: "$\\frac{2}{3} + \\frac{1}{3} \\times \\frac{4}{5}$", a: "$\\frac{14}{15}$", steps: ["Priorité à la multiplication !", "Calcule d'abord $\\frac{1}{3} \\times \\frac{4}{5} = \\frac{4}{15}$.", "Ensuite mets $\\frac{2}{3}$ sur $15$."], f: "Priorité opératoire" },
      { lvl: 2, q: "$\\left(\\frac{1}{2} + \\frac{1}{3}\\right) \\times \\frac{6}{5}$", a: "$1$", steps: ["Priorité à la parenthèse.", "Mets au même dénominateur (sur 6) : $\\frac{3}{6} + \\frac{2}{6}$."], f: "Priorité aux parenthèses" },
      { lvl: 2, q: "$\\frac{\\frac{2}{3}}{\\frac{5}{7}}$", a: "$\\frac{14}{15}$", steps: ["Une fraction sur une fraction est une division.", "C'est exactement pareil que $\\frac{2}{3} \\div \\frac{5}{7}$."], f: "$\\frac{\\frac{a}{b}}{\\frac{c}{d}} = \\frac{a}{b} \\times \\frac{d}{c}$" },
      { lvl: 2, q: "$1 - \\frac{1}{3} \\times \\frac{3}{2}$", a: "$\\frac{1}{2}$", steps: ["Priorité à la multiplication.", "Simplifie les $3$ : $\\frac{1}{3} \\times \\frac{3}{2} = \\frac{1}{2}$."], f: "Simplification croisée" },
      { lvl: 2, q: "$\\frac{3}{4} \\div \\left(\\frac{1}{2} - \\frac{1}{4}\\right)$", a: "$3$", steps: ["Parenthèse d'abord : $\\frac{1}{2} = \\frac{2}{4}$.", "On obtient $\\frac{3}{4} \\div \\frac{1}{4}$."], f: "Division = Inverse" },
      { lvl: 2, q: "$\\frac{5}{6} \\times \\frac{12}{25}$", a: "$\\frac{2}{5}$", steps: ["Décompose avant de multiplier.", "$12 = 6 \\times 2$ et $25 = 5 \\times 5$."], f: "Décomposition en facteurs" },
      { lvl: 2, q: "$\\frac{4}{7} \\times \\left(-\\frac{7}{8}\\right)$", a: "$-\\frac{1}{2}$", steps: ["Résultat négatif.", "Simplifie les $7$, et simplifie le $4$ avec le $8$."], f: "Simplification croisée" },

      // NIVEAU 3 (3 exos) - Fractions à étages
      { lvl: 3, q: "$\\frac{1 - \\frac{1}{3}}{1 + \\frac{1}{3}}$", a: "$\\frac{1}{2}$", steps: ["Calcule tout le numérateur : $1 - \\frac{1}{3} = \\frac{2}{3}$.", "Calcule tout le dénominateur : $1 + \\frac{1}{3} = \\frac{4}{3}$.", "Divise les deux résultats : $\\frac{2}{3} \\times \\frac{3}{4}$."], f: "Fraction à étages" },
      { lvl: 3, q: "$\\frac{2}{3} - \\frac{4}{3} \\times \\frac{1}{2} + 1$", a: "$1$", steps: ["Priorité multiplication : $\\frac{4}{3} \\times \\frac{1}{2} = \\frac{2}{3}$.", "L'expression devient : $\\frac{2}{3} - \\frac{2}{3} + 1$."], f: "Priorités et annulation" },
      { lvl: 3, q: "$\\frac{\\frac{3}{4} - \\frac{1}{2}}{\\frac{5}{8}}$", a: "$\\frac{2}{5}$", steps: ["Numérateur : $\\frac{3}{4} - \\frac{2}{4} = \\frac{1}{4}$.", "Division : $\\frac{1}{4} \\times \\frac{8}{5}$."], f: "Fraction à étages" }
    ],

    // =========================================================================
    // 3. PUISSANCES (RÈGLES DE CALCUL)
    // =========================================================================
    PUISSANCES: [
      // NIVEAU 1 (10 exos) - Règles de base
      { lvl: 1, q: "$x^2 \\times x^5$", a: "$x^7$", steps: ["Quand on multiplie des puissances de même base, on additionne les exposants."], f: "$x^a \\times x^b = x^{a+b}$" },
      { lvl: 1, q: "$\\frac{x^8}{x^3}$", a: "$x^5$", steps: ["Quand on divise, on soustrait l'exposant du bas à celui du haut.", "$8 - 3 = 5$."], f: "$\\frac{x^a}{x^b} = x^{a-b}$" },
      { lvl: 1, q: "$(x^3)^2$", a: "$x^6$", steps: ["Une puissance de puissance : on multiplie les exposants.", "$3 \\times 2 = 6$."], f: "$(x^a)^b = x^{a \\times b}$" },
      { lvl: 1, q: "$10^4 \\times 10^3$", a: "$10^7$", steps: ["Même règle pour les puissances de 10.", "$4 + 3 = 7$."], f: "$10^a \\times 10^b = 10^{a+b}$" },
      { lvl: 1, q: "$\\frac{10^9}{10^2}$", a: "$10^7$", steps: ["Soustraction des exposants : $9 - 2$."], f: "$\\frac{10^a}{10^b} = 10^{a-b}$" },
      { lvl: 1, q: "$2^3$", a: "$8$", steps: ["Attention, ce n'est pas $2 \\times 3$.", "C'est $2 \\times 2 \\times 2$."], f: "$a^n = a \\times a \\times \\dots \\times a$" },
      { lvl: 1, q: "$10^{-2}$", a: "$0.01$", steps: ["Une puissance négative indique l'inverse.", "$10^{-2} = \\frac{1}{10^2} = \\frac{1}{100}$."], f: "$10^{-n} = \\frac{1}{10^n}$" },
      { lvl: 1, q: "$x^1$", a: "$x$", steps: ["L'exposant 1 est invisible mais toujours là."], f: "$x^1 = x$" },
      { lvl: 1, q: "$x^0$", a: "$1$", steps: ["Par convention, tout nombre (non nul) à la puissance 0 vaut 1."], f: "$x^0 = 1$" },
      { lvl: 1, q: "$a^4 \\times a$", a: "$a^5$", steps: ["Rappel : $a$ c'est $a^1$.", "Donc $4 + 1 = 5$."], f: "$a^n \\times a^1 = a^{n+1}$" },

      // NIVEAU 2 (7 exos) - Exposants négatifs & compositions
      { lvl: 2, q: "$2^3 \\times 2^{-5}$", a: "$2^{-2}$", steps: ["Additionne les exposants, même s'ils sont négatifs.", "$3 + (-5) = -2$."], f: "$x^a \\times x^b = x^{a+b}$" },
      { lvl: 2, q: "$\\frac{10^4 \\times 10^5}{10^7}$", a: "$10^2$", steps: ["Calcule le haut d'abord : $10^{4+5} = 10^9$.", "Ensuite la division : $10^{9-7}$."], f: "Combinaison de règles" },
      { lvl: 2, q: "$(2x)^3$", a: "$8x^3$", steps: ["Le cube s'applique au chiffre ET à la lettre.", "$2^3 \\times x^3$."], f: "$(a \\times b)^n = a^n \\times b^n$" },
      { lvl: 2, q: "$3^2 \\times 3^{-2}$", a: "$1$", steps: ["Addition : $2 + (-2) = 0$.", "On obtient $3^0$. Et tout nombre à la puissance 0 vaut 1."], f: "$a^0 = 1$" },
      { lvl: 2, q: "$\\frac{x^5 \\times x^{-2}}{x^2}$", a: "$x^1 = x$", steps: ["Haut : $5 + (-2) = 3$.", "Division : $3 - 2 = 1$."], f: "Combinaison de règles" },
      { lvl: 2, q: "$(-2)^4$", a: "$16$", steps: ["Une puissance paire annule le signe négatif.", "$(-2) \\times (-2) \\times (-2) \\times (-2)$."], f: "Signe et exposant pair" },
      { lvl: 2, q: "$-2^4$", a: "$-16$", steps: ["Attention au piège ! Il n'y a pas de parenthèses.", "La puissance 4 ne s'applique qu'au 2, pas au signe moins."], f: "$-x^n \\neq (-x)^n$" },

      // NIVEAU 3 (3 exos) - Expressions complètes
      { lvl: 3, q: "$\\frac{(10^2)^3 \\times 10^{-4}}{10^5}$", a: "$10^{-3}$", steps: ["1. Puissance de puissance : $(10^2)^3 = 10^6$.", "2. Produit au numérateur : $10^6 \\times 10^{-4} = 10^2$.", "3. Division finale : $10^2 \\div 10^5 = 10^{2-5}$."], f: "Toutes les règles de puissances" },
      { lvl: 3, q: "$\\frac{4 \\times 10^5 \\times 2 \\times 10^{-3}}{2 \\times 10^4}$", a: "$4 \\times 10^{-2}$", steps: ["Sépare les nombres et les puissances de 10.", "Nombres : $\\frac{4 \\times 2}{2} = 4$.", "Puissances : $\\frac{10^5 \\times 10^{-3}}{10^4}$."], f: "Calcul scientifique" },
      { lvl: 3, q: "$\\frac{(x^2 y^3)^2}{x^3 y}$", a: "$x^1 y^5$", steps: ["Distribue le carré en haut : $x^{2\\times2} y^{3\\times2} = x^4 y^6$.", "Divise chaque lettre : $x^{4-3}$ et $y^{6-1}$."], f: "Puissances avec 2 variables" }
    ],

    // =========================================================================
    // 4. ÉQUATIONS (INCONNUES DES DEUX CÔTÉS)
    // =========================================================================
    EQUATIONS: [
      // NIVEAU 1 (10 exos) - Rappel et structures simples
      { lvl: 1, q: "$2x + 3 = 11$", a: "$x = 4$", steps: ["Retire 3 des deux côtés : $2x = 8$.", "Divise par 2."], f: "$ax+b=c \\Rightarrow x=\\frac{c-b}{a}$" },
      { lvl: 1, q: "$3x - 4 = 5$", a: "$x = 3$", steps: ["Ajoute 4 des deux côtés : $3x = 9$.", "Divise par 3."], f: "Opérations inverses" },
      { lvl: 1, q: "$\\frac{x}{3} = 4$", a: "$x = 12$", steps: ["L'inverse de la division, c'est la multiplication.", "Multiplie par 3 des deux côtés."], f: "$\\frac{x}{a}=b \\Rightarrow x=ab$" },
      { lvl: 1, q: "$-2x = 8$", a: "$x = -4$", steps: ["Divise par $-2$."], f: "$x = \\frac{b}{a}$" },
      { lvl: 1, q: "$x - 7 = -2$", a: "$x = 5$", steps: ["Ajoute 7 des deux côtés.", "$-2 + 7 = 5$."], f: "Opérations inverses" },
      { lvl: 1, q: "$4x + 1 = 1$", a: "$x = 0$", steps: ["Retire 1 : $4x = 0$.", "Si $4$ fois un nombre vaut zéro, ce nombre est zéro."], f: "$ax = 0 \\Rightarrow x = 0$" },
      { lvl: 1, q: "$6x = -18$", a: "$x = -3$", steps: ["Divise $-18$ par $6$."], f: "Division avec relatifs" },
      { lvl: 1, q: "$\\frac{x}{2} + 1 = 5$", a: "$x = 8$", steps: ["Retire 1 : $\\frac{x}{2} = 4$.", "Multiplie par 2."], f: "Opérations inverses" },
      { lvl: 1, q: "$10 - x = 3$", a: "$x = 7$", steps: ["Si j'ai 10 et qu'il m'en reste 3, j'en ai enlevé 7.", "Ou : ajoute $x$ à droite, retire 3 à gauche."], f: "$-x = b-a \\Rightarrow x = a-b$" },
      { lvl: 1, q: "$-x = -5$", a: "$x = 5$", steps: ["Change le signe des deux côtés (multiplie par -1)."], f: "$-x = -a \\Rightarrow x = a$" },

      // NIVEAU 2 (7 exos) - Des x des deux côtés
      { lvl: 2, q: "$3x + 2 = x + 8$", a: "$x = 3$", steps: ["Mets tous les x à gauche et les nombres à droite.", "Retire $x$ à gauche : $2x + 2 = 8$.", "Retire 2 à droite : $2x = 6$."], f: "$ax+b=cx+d$" },
      { lvl: 2, q: "$5x - 3 = 2x + 9$", a: "$x = 4$", steps: ["Retire $2x$ : $3x - 3 = 9$.", "Ajoute $3$ : $3x = 12$."], f: "$ax+b=cx+d$" },
      { lvl: 2, q: "$4x + 7 = x - 5$", a: "$x = -4$", steps: ["Retire $x$ : $3x + 7 = -5$.", "Retire $7$ : $3x = -12$."], f: "$ax+b=cx+d$" },
      { lvl: 2, q: "$2x = 5x - 12$", a: "$x = 4$", steps: ["Passe les $x$ à droite pour éviter les nombres négatifs.", "$12 = 5x - 2x$, donc $12 = 3x$."], f: "Regroupement stratégique" },
      { lvl: 2, q: "$-3x + 4 = x - 8$", a: "$x = 3$", steps: ["Ajoute $3x$ à droite : $4 = 4x - 8$.", "Ajoute $8$ à gauche : $12 = 4x$."], f: "Regroupement stratégique" },
      { lvl: 2, q: "$7x - 1 = 3x + 11$", a: "$x = 3$", steps: ["Retire $3x$ : $4x - 1 = 11$.", "Ajoute $1$ : $4x = 12$."], f: "$ax+b=cx+d$" },
      { lvl: 2, q: "$x - 2 = 4x + 7$", a: "$x = -3$", steps: ["Retire $x$ à droite : $-2 = 3x + 7$.", "Retire $7$ à gauche : $-9 = 3x$."], f: "Regroupement stratégique" },

      // NIVEAU 3 (3 exos) - Équations avec développement
      { lvl: 3, q: "$2(x + 3) = 4x - 2$", a: "$x = 4$", steps: ["1. Distribue le 2 : $2x + 6 = 4x - 2$.", "2. Regroupe les $x$ : $6 = 2x - 2$.", "3. Isole $x$ : $8 = 2x$."], f: "Développement puis résolution" },
      { lvl: 3, q: "$3(2x - 1) = 2(x + 5)$", a: "$x = 3.25$", steps: ["1. Distribue : $6x - 3 = 2x + 10$.", "2. Regroupe les $x$ : $4x - 3 = 10$.", "3. Isole $x$ : $4x = 13$."], f: "Double distribution" },
      { lvl: 3, q: "$x - (2x + 3) = 5$", a: "$x = -8$", steps: ["1. Le signe moins devant la parenthèse change les signes : $x - 2x - 3 = 5$.", "2. Simplifie : $-x - 3 = 5$.", "3. Isole $x$ : $-x = 8$."], f: "Soustraction d'une parenthèse" }
    ]
  }
};