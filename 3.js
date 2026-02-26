// ==================== 3.js - NIVEAU 3ÈME (OBJECTIF BREVET) ====================
window.db = window.db || {};

window.db.ALGEBRA_3EME = {
  catDisplay: {
    ARITHMETIQUE: "Arithmétique & Nombres Premiers",
    LITTERAL: "Calcul Littéral (Brevet)",
    EQUATIONS: "Équations & Inéquations",
    FONCTIONS: "Notion de Fonction"
  },
  catIcon: {
    ARITHMETIQUE: "🔢",
    LITTERAL: "🔤",
    EQUATIONS: "⚖️",
    FONCTIONS: "📈"
  },
  categories: {
    // =========================================================================
    // 1. ARITHMÉTIQUE (Nombres premiers, diviseurs, fractions irréductibles)
    // =========================================================================
    ARITHMETIQUE: [
      // NIVEAU 1 (10 exos) - Bases des nombres premiers et diviseurs
      { lvl: 1, q: "Donner la décomposition en facteurs premiers de $12$", a: "$2^2 \\times 3$", steps: ["$12$ est pair : $12 = 2 \\times 6$.", "$6 = 2 \\times 3$."], f: "Décomposition" },
      { lvl: 1, q: "Donner la décomposition en facteurs premiers de $18$", a: "$2 \\times 3^2$", steps: ["$18 = 2 \\times 9$.", "$9 = 3 \\times 3$."], f: "Décomposition" },
      { lvl: 1, q: "Le nombre $15$ est-il un nombre premier ?", a: "\\text{Non}", steps: ["Un nombre premier n'est divisible que par 1 et lui-même.", "$15$ est divisible par $3$ et $5$."], f: "Définition Nombre Premier" },
      { lvl: 1, q: "Le nombre $17$ est-il un nombre premier ?", a: "\\text{Oui}", steps: ["Il n'est dans aucune table de multiplication (sauf la sienne)."], f: "Définition Nombre Premier" },
      { lvl: 1, q: "Donner la décomposition en facteurs premiers de $20$", a: "$2^2 \\times 5$", steps: ["$20 = 2 \\times 10 = 2 \\times 2 \\times 5$."], f: "Décomposition" },
      { lvl: 1, q: "Simplifier la fraction $\\frac{12}{18}$", a: "$\\frac{2}{3}$", steps: ["Divise en haut et en bas par leur plus grand diviseur commun (6).", "Ou utilise les décompositions : $\\frac{2 \\times 2 \\times 3}{2 \\times 3 \\times 3}$."], f: "Fraction irréductible" },
      { lvl: 1, q: "Donner la liste des diviseurs de $10$", a: "$1, 2, 5, 10$", steps: ["Cherche les paires : $1 \\times 10$ et $2 \\times 5$."], f: "Liste des diviseurs" },
      { lvl: 1, q: "Décomposer $30$ en facteurs premiers", a: "$2 \\times 3 \\times 5$", steps: ["$30 = 3 \\times 10$ et $10 = 2 \\times 5$."], f: "Décomposition" },
      { lvl: 1, q: "Simplifier $\\frac{20}{30}$", a: "$\\frac{2}{3}$", steps: ["Divise directement par $10$ en haut et en bas."], f: "Simplification" },
      { lvl: 1, q: "Le nombre $51$ est-il premier ?", a: "\\text{Non}", steps: ["Astuce : $5 + 1 = 6$. Donc $51$ est divisible par $3$.", "$51 = 3 \\times 17$."], f: "Critère de divisibilité par 3" },

      // NIVEAU 2 (7 exos) - Décompositions plus poussées et PGCD
      { lvl: 2, q: "Décomposer $60$ en facteurs premiers", a: "$2^2 \\times 3 \\times 5$", steps: ["$60 = 6 \\times 10 = (2 \\times 3) \\times (2 \\times 5)$."], f: "Décomposition" },
      { lvl: 2, q: "Décomposer $84$ en facteurs premiers", a: "$2^2 \\times 3 \\times 7$", steps: ["$84 = 2 \\times 42 = 2 \\times 2 \\times 21 = 2 \\times 2 \\times 3 \\times 7$."], f: "Division successive" },
      { lvl: 2, q: "Rendre irréductible $\\frac{60}{84}$", a: "$\\frac{5}{7}$", steps: ["Utilise les décompositions trouvées avant.", "Élimine les facteurs communs : les deux $2$ et le $3$."], f: "Simplification par décomposition" },
      { lvl: 2, q: "Décomposer $100$ en facteurs premiers", a: "$2^2 \\times 5^2$", steps: ["$100 = 10 \\times 10 = (2 \\times 5) \\times (2 \\times 5)$."], f: "Décomposition" },
      { lvl: 2, q: "Quel est le PGCD (Plus Grand Commun Diviseur) de $12$ et $18$ ?", a: "$6$", steps: ["Les diviseurs communs sont 1, 2, 3, 6.", "Le plus grand est 6."], f: "Recherche de PGCD" },
      { lvl: 2, q: "Rendre irréductible $\\frac{45}{60}$", a: "$\\frac{3}{4}$", steps: ["Divise par $5$ : $\\frac{9}{12}$.", "Puis divise par $3$ : $\\frac{3}{4}$."], f: "Divisions successives" },
      { lvl: 2, q: "Décomposer $144$ en facteurs premiers", a: "$2^4 \\times 3^2$", steps: ["$144 = 12 \\times 12 = (2^2 \\times 3) \\times (2^2 \\times 3)$."], f: "Décomposition d'un carré" },

      // NIVEAU 3 (3 exos) - Problèmes d'arithmétique
      { lvl: 3, q: "PGCD de $120$ et $84$", a: "$12$", steps: ["Décomposition de $120$ : $2^3 \\times 3 \\times 5$.", "Décomposition de $84$ : $2^2 \\times 3 \\times 7$.", "Facteurs communs au minimum : $2^2 \\times 3 = 12$."], f: "PGCD par facteurs premiers" },
      { lvl: 3, q: "Rendre irréductible $\\frac{84}{120}$", a: "$\\frac{7}{10}$", steps: ["Divise par leur PGCD qui est $12$.", "Ou supprime les facteurs communs des décompositions."], f: "Fraction irréductible" },
      { lvl: 3, q: "Décomposer $1024$ en facteurs premiers", a: "$2^{10}$", steps: ["C'est une puissance de 2 classique en informatique.", "$1024 = 2 \\times 512 = 2 \\times 2 \\times 256$ etc."], f: "Puissance de 2" }
    ],

    // =========================================================================
    // 2. CALCUL LITTÉRAL (Développement, Factorisation, Identités remarquables)
    // =========================================================================
    LITTERAL: [
      // NIVEAU 1 (10 exos) - Simple & Double distributivité
      { lvl: 1, q: "Développer $3(2x + 5)$", a: "$6x + 15$", steps: ["Distribue le 3 : $3 \\times 2x + 3 \\times 5$."], f: "$k(a+b) = ka + kb$" },
      { lvl: 1, q: "Développer $-2(x - 4)$", a: "$-2x + 8$", steps: ["Attention au signe : $(-2) \\times (-4) = +8$."], f: "Distributivité avec signe moins" },
      { lvl: 1, q: "Développer $x(x + 3)$", a: "$x^2 + 3x$", steps: ["$x \\times x = x^2$."], f: "$x \\times x = x^2$" },
      { lvl: 1, q: "Développer $(x + 2)(x + 4)$", a: "$x^2 + 6x + 8$", steps: ["Double distributivité : $x^2 + 4x + 2x + 8$."], f: "$(a+b)(c+d) = ac+ad+bc+bd$" },
      { lvl: 1, q: "Développer $(x - 1)(x + 5)$", a: "$x^2 + 4x - 5$", steps: ["$x^2 + 5x - x - 5$."], f: "Double distributivité" },
      { lvl: 1, q: "Factoriser $5x + 15$", a: "$5(x + 3)$", steps: ["Le facteur commun est $5$ car $15 = 5 \\times 3$."], f: "$ka + kb = k(a+b)$" },
      { lvl: 1, q: "Factoriser $x^2 + 4x$", a: "$x(x + 4)$", steps: ["Le facteur commun est $x$."], f: "$x^2 = x \\times x$" },
      { lvl: 1, q: "Développer $(x + 3)^2$", a: "$x^2 + 6x + 9$", steps: ["Identité remarquable : Carré du premier + Double produit + Carré du second."], f: "$(a+b)^2 = a^2 + 2ab + b^2$" },
      { lvl: 1, q: "Développer $(x - 5)^2$", a: "$x^2 - 10x + 25$", steps: ["Le double produit est négatif : $-2 \\times 5 \\times x = -10x$."], f: "$(a-b)^2 = a^2 - 2ab + b^2$" },
      { lvl: 1, q: "Développer $(x - 2)(x + 2)$", a: "$x^2 - 4$", steps: ["C'est la 3ème identité remarquable. Les termes en $x$ s'annulent."], f: "$(a-b)(a+b) = a^2 - b^2$" },

      // NIVEAU 2 (7 exos) - Factorisations Brevet (Différence de carrés et Blocs)
      { lvl: 2, q: "Factoriser $x^2 - 16$", a: "$(x - 4)(x + 4)$", steps: ["C'est une différence de deux carrés : $A^2 - B^2$.", "Ici $A=x$ et $B=4$ (car $4^2 = 16$)."], f: "$A^2 - B^2 = (A-B)(A+B)$" },
      { lvl: 2, q: "Factoriser $9x^2 - 25$", a: "$(3x - 5)(3x + 5)$", steps: ["Trouve les racines carrées : $9x^2$ est le carré de $3x$, et $25$ est le carré de $5$."], f: "$A^2 - B^2 = (A-B)(A+B)$" },
      { lvl: 2, q: "Factoriser $(x + 1)(x + 2) + 5(x + 1)$", a: "$(x + 1)(x + 7)$", steps: ["Le facteur commun est le bloc $(x + 1)$.", "Mets-le en facteur : $(x + 1) [ (x + 2) + 5 ]$."], f: "$kA + bA = A(k+b)$" },
      { lvl: 2, q: "Factoriser $(2x - 3)^2 + (2x - 3)(x + 1)$", a: "$(2x - 3)(3x - 2)$", steps: ["Le facteur est $(2x - 3)$.", "Crochet : $[(2x - 3) + (x + 1)] = 3x - 2$."], f: "Mise en facteur d'une parenthèse" },
      { lvl: 2, q: "Développer $(2x + 1)^2 - (x - 3)$", a: "$4x^2 + 3x + 4$", steps: ["Développe le carré : $4x^2 + 4x + 1$.", "Enlève la parenthèse (change les signes) : $-x + 3$."], f: "Priorités opératoires" },
      { lvl: 2, q: "Développer $(3x - 2)^2$", a: "$9x^2 - 12x + 4$", steps: ["Attention au carré du premier terme : $(3x)^2 = 9x^2$.", "Double produit : $2 \\times 3x \\times (-2) = -12x$."], f: "$(a-b)^2 = a^2 - 2ab + b^2$" },
      { lvl: 2, q: "Factoriser $x^2 + 8x + 16$", a: "$(x + 4)^2$", steps: ["C'est une identité remarquable à l'envers.", "$A^2 = x^2$ et $B^2 = 16$. Vérifie le double produit."], f: "$a^2 + 2ab + b^2 = (a+b)^2$" },

      // NIVEAU 3 (3 exos) - Sujet type Brevet
      { lvl: 3, q: "Développer et réduire $(x - 3)(x + 3) - (x - 1)^2$", a: "$2x - 10$", steps: ["1. Identité 3 : $(x - 3)(x + 3) = x^2 - 9$.", "2. Identité 2 : $(x - 1)^2 = x^2 - 2x + 1$.", "3. Soustrais : $(x^2 - 9) - (x^2 - 2x + 1) = x^2 - 9 - x^2 + 2x - 1$."], f: "Soustraction de développement" },
      { lvl: 3, q: "Factoriser $(2x + 5)^2 - 9$", a: "$(2x + 2)(2x + 8)$", steps: ["C'est $A^2 - B^2$ avec $A = (2x+5)$ et $B = 3$.", "Donne : $((2x+5) - 3) \\times ((2x+5) + 3)$."], f: "$A^2 - B^2 = (A-B)(A+B)$" },
      { lvl: 3, q: "Factoriser $(x - 4)(2x + 1) - (x - 4)(x - 5)$", a: "$(x - 4)(x + 6)$", steps: ["Facteur commun : $(x - 4)$.", "Attention au signe MOINS devant la 2ème parenthèse : $[(2x + 1) - (x - 5)] = 2x + 1 - x + 5$."], f: "Soustraction dans le crochet" }
    ],

    // =========================================================================
    // 3. ÉQUATIONS ET INÉQUATIONS
    // =========================================================================
    EQUATIONS: [
      // NIVEAU 1 (10 exos) - Équations 1er degré
      { lvl: 1, q: "Résoudre $x + 7 = 12$", a: "$x = 5$", steps: ["Soustrait 7 de chaque côté."], f: "$x = 12 - 7$" },
      { lvl: 1, q: "Résoudre $4x = 20$", a: "$x = 5$", steps: ["Divise par 4."], f: "$x = \\frac{20}{4}$" },
      { lvl: 1, q: "Résoudre $2x + 3 = 11$", a: "$x = 4$", steps: ["Retire 3 : $2x = 8$.", "Divise par 2."], f: "Opérations inverses" },
      { lvl: 1, q: "Résoudre $5x - 2 = 13$", a: "$x = 3$", steps: ["Ajoute 2 : $5x = 15$."], f: "Opérations inverses" },
      { lvl: 1, q: "Résoudre $-3x = 18$", a: "$x = -6$", steps: ["Divise $18$ par $-3$."], f: "Règle des signes" },
      { lvl: 1, q: "Résoudre $3x = x + 8$", a: "$x = 4$", steps: ["Retire $x$ des deux côtés : $2x = 8$."], f: "Regroupement des $x$" },
      { lvl: 1, q: "Résoudre $(x - 2)(x + 5) = 0$", a: "$x = 2 \\text{ ou } x = -5$", steps: ["Un produit est nul si au moins l'un de ses facteurs est nul.", "Donc $x - 2 = 0$ ou $x + 5 = 0$."], f: "Équation produit nul" },
      { lvl: 1, q: "Résoudre $x(x - 4) = 0$", a: "$x = 0 \\text{ ou } x = 4$", steps: ["Le premier facteur est $x$."], f: "Équation produit nul" },
      { lvl: 1, q: "Résoudre $2x < 10$", a: "$x < 5$", steps: ["Divise par 2. L'inégalité ne change pas de sens."], f: "Inéquation basique" },
      { lvl: 1, q: "Résoudre $x - 4 \\geq 1$", a: "$x \\geq 5$", steps: ["Ajoute 4."], f: "Inéquation basique" },

      // NIVEAU 2 (7 exos) - Des x des deux côtés & Inéquations avec changement de sens
      { lvl: 2, q: "Résoudre $5x - 3 = 2x + 9$", a: "$x = 4$", steps: ["Retire $2x$ : $3x - 3 = 9$.", "Ajoute $3$ : $3x = 12$."], f: "Équation du 1er degré" },
      { lvl: 2, q: "Résoudre $4(x - 1) = 2x + 6$", a: "$x = 5$", steps: ["Développe d'abord : $4x - 4 = 2x + 6$."], f: "Développement puis résolution" },
      { lvl: 2, q: "Résoudre $(2x - 1)(x + 3) = 0$", a: "$x = 0.5 \\text{ ou } x = -3$", steps: ["$2x - 1 = 0 \\Rightarrow 2x = 1 \\Rightarrow x = 0.5$."], f: "Équation produit nul" },
      { lvl: 2, q: "Résoudre $x^2 = 25$", a: "$x = 5 \\text{ ou } x = -5$", steps: ["Attention ! Un carré a toujours DEUX solutions (une positive, une négative)."], f: "$x^2 = a \\Rightarrow x = \\pm \\sqrt{a}$" },
      { lvl: 2, q: "Résoudre $-2x > 8$", a: "$x < -4$", steps: ["PIÈGE ! Quand on divise par un nombre négatif, on INVERSE le signe de l'inégalité !"], f: "Changement de sens" },
      { lvl: 2, q: "Résoudre $3x + 1 \\leq x - 5$", a: "$x \\leq -3$", steps: ["Regroupe : $2x + 1 \\leq -5$.", "Puis : $2x \\leq -6$."], f: "Inéquation complète" },
      { lvl: 2, q: "Résoudre $1 - 3x < 10$", a: "$x > -3$", steps: ["Soustrait 1 : $-3x < 9$.", "Divise par $-3$ et inverse le signe !"], f: "Changement de sens" },

      // NIVEAU 3 (3 exos) - Mises en équation complexes
      { lvl: 3, q: "Résoudre $x^2 - 36 = 0$", a: "$x = 6 \\text{ ou } x = -6$", steps: ["Factorise : $(x - 6)(x + 6) = 0$.", "Ou isole : $x^2 = 36$."], f: "$A^2 - B^2 = 0$" },
      { lvl: 3, q: "Résoudre $(x + 2)^2 = 9$", a: "$x = 1 \\text{ ou } x = -5$", steps: ["Soit $x+2 = 3$, soit $x+2 = -3$.", "N'oublie pas la racine négative !"], f: "$X^2 = 9$" },
      { lvl: 3, q: "Résoudre $\\frac{x}{3} - 1 = \\frac{x}{2}$", a: "$x = -6$", steps: ["Mets tout sur le dénominateur 6.", "$\\frac{2x}{6} - \\frac{6}{6} = \\frac{3x}{6}$, donc $2x - 6 = 3x$."], f: "Équation avec fractions" }
    ],

    // =========================================================================
    // 4. NOTION DE FONCTION (Images, Antécédents)
    // =========================================================================
    FONCTIONS: [
      // NIVEAU 1 (10 exos) - Calcul d'image directe
      { lvl: 1, q: "Soit $f(x) = 2x + 3$. Calculer $f(4)$", a: "$11$", steps: ["Remplace $x$ par $4$ dans la formule.", "$f(4) = 2 \\times 4 + 3 = 8 + 3$."], f: "Calcul d'image" },
      { lvl: 1, q: "Soit $g(x) = x^2 - 1$. Calculer $g(3)$", a: "$8$", steps: ["$g(3) = 3^2 - 1 = 9 - 1$."], f: "Calcul d'image" },
      { lvl: 1, q: "Soit $h(x) = -3x$. Calculer $h(-2)$", a: "$6$", steps: ["$-3 \\times (-2) = 6$."], f: "Règle des signes" },
      { lvl: 1, q: "Soit $f(x) = 5 - x$. Calculer l'image de $7$", a: "$-2$", steps: ["L'image de $7$ se note $f(7)$.", "$5 - 7 = -2$."], f: "Vocabulaire : Image" },
      { lvl: 1, q: "Soit $f(x) = 2x - 4$. Trouver l'antécédent de $10$", a: "$x = 7$", steps: ["L'antécédent, c'est le $x$ de départ.", "Résous l'équation : $2x - 4 = 10$."], f: "Vocabulaire : Antécédent" },
      { lvl: 1, q: "Soit $g(x) = 3x$. Quel est l'antécédent de $15$ ?", a: "$x = 5$", steps: ["Résous $3x = 15$."], f: "Calcul d'antécédent" },
      { lvl: 1, q: "Soit $f(x) = x^2$. Calculer $f(-4)$", a: "$16$", steps: ["Attention : le carré s'applique à tout le nombre.", "$(-4) \\times (-4) = 16$."], f: "Carré d'un négatif" },
      { lvl: 1, q: "Soit $h(x) = \\frac{x}{2} + 1$. Calculer $h(10)$", a: "$6$", steps: ["$\\frac{10}{2} + 1 = 5 + 1$."], f: "Calcul d'image" },
      { lvl: 1, q: "Soit $f(x) = 10 - 2x$. Résoudre $f(x) = 0$", a: "$x = 5$", steps: ["Cela revient à chercher l'antécédent de 0.", "$10 - 2x = 0$."], f: "Équation $f(x) = 0$" },
      { lvl: 1, q: "Soit $g(x) = (x+1)(x-2)$. Calculer $g(2)$", a: "$0$", steps: ["$(2+1)(2-2) = 3 \\times 0 = 0$."], f: "Annulation de produit" },

      // NIVEAU 2 (7 exos) - Images complexes et équations
      { lvl: 2, q: "Soit $f(x) = x^2 - 3x$. Calculer $f(-2)$", a: "$10$", steps: ["$f(-2) = (-2)^2 - 3(-2)$.", "$= 4 + 6 = 10$."], f: "Calcul avec négatifs" },
      { lvl: 2, q: "Soit $g(x) = 2x + 7$. Trouver l'antécédent de $-5$", a: "$x = -6$", steps: ["Résous $2x + 7 = -5$.", "$2x = -12$."], f: "Calcul d'antécédent" },
      { lvl: 2, q: "Soit $f(x) = -x + 4$. Pour quel $x$ a-t-on $f(x) = 8$ ?", a: "$x = -4$", steps: ["$-x + 4 = 8 \\Rightarrow -x = 4$."], f: "Calcul d'antécédent" },
      { lvl: 2, q: "Soit $h(x) = (x-3)^2$. Trouver le(s) antécédent(s) de $0$", a: "$x = 3$", steps: ["$(x-3)^2 = 0 \\Rightarrow x-3 = 0$."], f: "Antécédent d'un carré" },
      { lvl: 2, q: "Soit $f(x) = 5x - 1$ et $g(x) = 2x + 8$. Trouver $x$ tel que $f(x) = g(x)$", a: "$x = 3$", steps: ["Résous l'équation : $5x - 1 = 2x + 8$.", "$3x = 9$."], f: "Égalité de fonctions" },
      { lvl: 2, q: "Soit $f(x) = \\frac{12}{x}$. Calculer l'antécédent de $3$", a: "$x = 4$", steps: ["$\\frac{12}{x} = 3 \\Rightarrow 3x = 12$."], f: "Fonction inverse" },
      { lvl: 2, q: "Soit $f(x) = x^2 + 1$. $f(-3)$ est-il égal à $f(3)$ ?", a: "\\text{Oui (ils valent 10)}", steps: ["$(-3)^2 + 1 = 9 + 1 = 10$.", "La fonction carré est paire."], f: "Symétrie" },

      // NIVEAU 3 (3 exos) - Résolution avancée
      { lvl: 3, q: "Soit $f(x) = x^2 - 4$. Trouver les antécédents de $5$", a: "$x = 3 \\text{ ou } x = -3$", steps: ["Résous $x^2 - 4 = 5$.", "$x^2 = 9$. Attention, il y a deux solutions !"], f: "Antécédents multiples" },
      { lvl: 3, q: "Soit $g(x) = (2x-1)^2$. Calculer $g(\\frac{1}{2})$", a: "$0$", steps: ["Remplace $x$ par $\\frac{1}{2}$.", "$2 \\times \\frac{1}{2} = 1$. L'intérieur fait $1 - 1 = 0$."], f: "Image d'une fraction" },
      { lvl: 3, q: "Trouver l'antécédent de $0$ pour la fonction affine $f(x) = ax + b$", a: "$x = -\\frac{b}{a}$", steps: ["C'est la formule générale.", "$ax + b = 0 \\Rightarrow ax = -b$."], f: "Racine d'une fonction affine" }
    ]
  }
};