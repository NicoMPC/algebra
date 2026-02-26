// ==================== 2.js - NIVEAU SECONDE ====================
window.db = window.db || {};

window.db.ALGEBRA_SECONDE = {
  catDisplay: {
    DEVELOPPEMENT: "Développement & Identités",
    FACTORISATION: "Factorisation Avancée",
    EQUATIONS: "Équations & Inéquations",
    FRACTIONS: "Fractions Algébriques"
  },
  catIcon: {
    DEVELOPPEMENT: "🚀",
    FACTORISATION: "🧩",
    EQUATIONS: "⚖️",
    FRACTIONS: "➗"
  },
  categories: {
    // =========================================================================
    // 1. DÉVELOPPEMENT & IDENTITÉS REMARQUABLES
    // =========================================================================
    DEVELOPPEMENT: [
      // NIVEAU 1 (10 exos) - Double distributivité et identités directes
      { lvl: 1, q: "$(x + 2)(x + 3)$", a: "$x^2 + 5x + 6$", steps: ["Distribue chaque terme : $x \\times x + x \\times 3 + 2 \\times x + 2 \\times 3$."], f: "$(a+b)(c+d) = ac+ad+bc+bd$" },
      { lvl: 1, q: "$(x - 4)(x + 1)$", a: "$x^2 - 3x - 4$", steps: ["Fais attention aux signes lors de la distribution.", "$x^2 + x - 4x - 4$."], f: "$(a+b)(c+d) = ac+ad+bc+bd$" },
      { lvl: 1, q: "$(2x + 1)(x + 2)$", a: "$2x^2 + 5x + 2$", steps: ["Multiplie les coefficients : $2x \\times x = 2x^2$."], f: "Double distributivité" },
      { lvl: 1, q: "$(x + 5)^2$", a: "$x^2 + 10x + 25$", steps: ["C'est la première identité remarquable.", "Le double produit est $2 \\times x \\times 5$."], f: "$(a+b)^2 = a^2 + 2ab + b^2$" },
      { lvl: 1, q: "$(x - 3)^2$", a: "$x^2 - 6x + 9$", steps: ["C'est la deuxième identité remarquable.", "Le double produit prend un signe moins."], f: "$(a-b)^2 = a^2 - 2ab + b^2$" },
      { lvl: 1, q: "$(x + 4)(x - 4)$", a: "$x^2 - 16$", steps: ["C'est la troisième identité remarquable.", "Les termes en $x$ s'annulent."], f: "$(a+b)(a-b) = a^2 - b^2$" },
      { lvl: 1, q: "$(2x + 3)^2$", a: "$4x^2 + 12x + 9$", steps: ["Attention, le carré de $2x$ est $(2x)^2 = 4x^2$."], f: "$(a+b)^2 = a^2 + 2ab + b^2$" },
      { lvl: 1, q: "$(3x - 1)^2$", a: "$9x^2 - 6x + 1$", steps: ["Double produit : $-2 \\times 3x \\times 1 = -6x$."], f: "$(a-b)^2 = a^2 - 2ab + b^2$" },
      { lvl: 1, q: "$(5x - 2)(5x + 2)$", a: "$25x^2 - 4$", steps: ["Carré du premier moins carré du deuxième."], f: "$(a-b)(a+b) = a^2 - b^2$" },
      { lvl: 1, q: "$3x(x - 4) + 2x$", a: "$3x^2 - 10x$", steps: ["Distribue d'abord le $3x$, puis réduis avec le $2x$."], f: "$k(a+b) = ka + kb$" },

      // NIVEAU 2 (7 exos) - Signes moins et mélanges
      { lvl: 2, q: "$(x + 2)^2 - (x^2 - 1)$", a: "$4x + 5$", steps: ["Développe le carré en gardant l'autre partie dans une parenthèse.", "Le signe moins inverse les signes : $-x^2 + 1$."], f: "Soustraction de parenthèses" },
      { lvl: 2, q: "$2(x - 3)^2$", a: "$2x^2 - 12x + 18$", steps: ["Développe l'identité remarquable d'abord (entre parenthèses).", "Ensuite, multiplie tous les termes par 2."], f: "Priorité aux puissances" },
      { lvl: 2, q: "$-(2x + 1)^2$", a: "$-4x^2 - 4x - 1$", steps: ["Le carré ne s'applique pas au signe moins.", "Développe $(2x+1)^2$ puis inverse tous les signes."], f: "$-(A) = -A$" },
      { lvl: 2, q: "$(x - 5)(2x + 3) - x^2$", a: "$x^2 - 7x - 15$", steps: ["Développe la double distributivité.", "$2x^2 + 3x - 10x - 15$, puis soustrais $x^2$."], f: "Réduction de polynômes" },
      { lvl: 2, q: "$(4x - 1)^2 + (x + 2)(x - 2)$", a: "$17x^2 - 8x - 3$", steps: ["Développe la 2ème identité d'un côté, et la 3ème de l'autre.", "$(16x^2 - 8x + 1) + (x^2 - 4)$."], f: "Somme de développements" },
      { lvl: 2, q: "$3x - (x - 2)^2$", a: "$-x^2 + 7x - 4$", steps: ["Le piège classique ! Garde le développement entre parenthèses.", "$3x - (x^2 - 4x + 4)$."], f: "Soustraction et développement" },
      { lvl: 2, q: "$(3 - 2x)^2$", a: "$4x^2 - 12x + 9$", steps: ["L'ordre est inversé mais la règle est la même.", "On l'écrit souvent dans l'ordre décroissant des puissances."], f: "$(a-b)^2 = a^2 - 2ab + b^2$" },

      // NIVEAU 3 (3 exos) - Développements lourds
      { lvl: 3, q: "$(2x - 3)^2 - (x + 4)(3x - 1)$", a: "$x^2 - 23x + 13$", steps: ["1. Carré : $4x^2 - 12x + 9$.", "2. Produit : $3x^2 - x + 12x - 4$.", "3. Soustraction : attention à bien inverser TOUS les signes du produit !"], f: "Parenthèses de sécurité" },
      { lvl: 3, q: "$2(x + 5)^2 - 3(x - 2)^2$", a: "$-x^2 + 32x + 38$", steps: ["Développe chaque carré séparément.", "Distribue le $2$ à gauche et le $-3$ à droite avant d'additionner."], f: "Combinaisons linéaires" },
      { lvl: 3, q: "$(x - 1)(x + 1)(x^2 + 1)$", a: "$x^4 - 1$", steps: ["Commence par les deux premières parenthèses (identité).", "Tu obtiens $(x^2 - 1)$. Que remarques-tu avec la suite ?"], f: "Identités en cascade" }
    ],

    // =========================================================================
    // 2. FACTORISATION AVANCÉE
    // =========================================================================
    FACTORISATION: [
      // NIVEAU 1 (10 exos) - Facteur commun évident et identités
      { lvl: 1, q: "$2x + 4$", a: "$2(x + 2)$", steps: ["Trouve le plus grand diviseur commun.", "$4 = 2 \\times 2$."], f: "$ka + kb = k(a+b)$" },
      { lvl: 1, q: "$x^2 + 3x$", a: "$x(x + 3)$", steps: ["Il y a un $x$ dans les deux termes."], f: "$x \\times x + 3 \\times x = x(x+3)$" },
      { lvl: 1, q: "$5x^2 - 15x$", a: "$5x(x - 3)$", steps: ["Le facteur commun est composé d'un nombre ET d'une lettre : $5x$."], f: "$ka + kb = k(a+b)$" },
      { lvl: 1, q: "$x^2 + 2x + 1$", a: "$(x + 1)^2$", steps: ["Reconnais la première identité remarquable.", "Cherche $a^2$ et $b^2$ pour trouver $a$ et $b$."], f: "$a^2 + 2ab + b^2 = (a+b)^2$" },
      { lvl: 1, q: "$x^2 - 6x + 9$", a: "$(x - 3)^2$", steps: ["Reconnais la deuxième identité remarquable.", "$9 = 3^2$ et le double produit est négatif."], f: "$a^2 - 2ab + b^2 = (a-b)^2$" },
      { lvl: 1, q: "$x^2 - 25$", a: "$(x - 5)(x + 5)$", steps: ["C'est une différence de deux carrés.", "$25 = 5^2$."], f: "$a^2 - b^2 = (a-b)(a+b)$" },
      { lvl: 1, q: "$4x^2 - 9$", a: "$(2x - 3)(2x + 3)$", steps: ["Attention, $4x^2$ est le carré de $2x$."], f: "$a^2 - b^2 = (a-b)(a+b)$" },
      { lvl: 1, q: "$x(x + 2) + 3(x + 2)$", a: "$(x + 2)(x + 3)$", steps: ["Le facteur commun est tout un bloc : la parenthèse $(x + 2)$."], f: "$kA + bA = A(k+b)$" },
      { lvl: 1, q: "$(x - 1)(x + 4) + (x - 1)(2x + 1)$", a: "$(x - 1)(3x + 5)$", steps: ["Factorise par $(x - 1)$.", "Dans le crochet, il reste $(x + 4) + (2x + 1)$."], f: "Mise en facteur de bloc" },
      { lvl: 1, q: "$9x^2 + 12x + 4$", a: "$(3x + 2)^2$", steps: ["Identifie les carrés : $(3x)^2$ et $2^2$."], f: "$a^2 + 2ab + b^2 = (a+b)^2$" },

      // NIVEAU 2 (7 exos) - Facteurs cachés et signes
      { lvl: 2, q: "$(2x + 3)(x - 1) - (2x + 3)(3x + 2)$", a: "$(2x + 3)(-2x - 3)$", steps: ["Le facteur est $(2x + 3)$.", "Crochet : $(x - 1) - (3x + 2)$. Attention au signe moins !"], f: "Soustraction dans le crochet" },
      { lvl: 2, q: "$(x + 5)^2 - (x + 5)(2x - 1)$", a: "$(x + 5)(-x + 6)$", steps: ["Rappel : $(x + 5)^2$ c'est $(x + 5)(x + 5)$.", "Le facteur est donc $(x + 5)$."], f: "$A^2 - AB = A(A-B)$" },
      { lvl: 2, q: "$16x^2 - (x + 1)^2$", a: "$(3x - 1)(5x + 1)$", a: "$(3x - 1)(5x + 1)$", steps: ["Différence de deux carrés : $A^2 - B^2$.", "Ici $A = 4x$ et $B = (x+1)$."], f: "$A^2 - B^2 = (A-B)(A+B)$" },
      { lvl: 2, q: "$x^3 - 4x$", a: "$x(x - 2)(x + 2)$", steps: ["Étape 1 : Factorise d'abord par $x$.", "Étape 2 : Il reste une identité remarquable !"], f: "Factorisations successives" },
      { lvl: 2, q: "$3(x - 2) + x(2 - x)$", a: "$(x - 2)(3 - x)$", steps: ["Astuce : $(2 - x)$ c'est l'opposé de $(x - 2)$.", "Remplace $+ x(2 - x)$ par $- x(x - 2)$."], f: "$(b-a) = -(a-b)$" },
      { lvl: 2, q: "$25 - (3x + 2)^2$", a: "$(3 - 3x)(3x + 7)$", steps: ["Identité remarquable avec $A = 5$ et $B = (3x + 2)$.", "$(5 - (3x+2))(5 + (3x+2))$."], f: "$A^2 - B^2 = (A-B)(A+B)$" },
      { lvl: 2, q: "$(2x - 1)^2 - 9$", a: "$(2x - 4)(2x + 2)$", steps: ["Ici $A = (2x-1)$ et $B = 3$.", "Note : on pourrait encore factoriser par 4 à la fin."], f: "$A^2 - B^2 = (A-B)(A+B)$" },

      // NIVEAU 3 (3 exos) - Factorisations expertes
      { lvl: 3, q: "$(x - 3)^2 - (2x + 1)^2$", a: "$(-x - 4)(3x - 2)$", steps: ["1. C'est $A^2 - B^2$.", "2. Crochet 1 : $(x-3) - (2x+1)$", "3. Crochet 2 : $(x-3) + (2x+1)$."], f: "$A^2 - B^2 = (A-B)(A+B)$" },
      { lvl: 3, q: "$4(x + 1)^2 - 9(2x - 1)^2$", a: "$(-4x + 5)(8x - 1)$", steps: ["Identifie les carrés complets : $A = 2(x+1)$ et $B = 3(2x-1)$."], f: "$A^2 - B^2 = (A-B)(A+B)$" },
      { lvl: 3, q: "$x^2 - 4 + (x - 2)(x + 5)$", a: "$(x - 2)(2x + 7)$", steps: ["Factorise d'abord le $x^2 - 4$.", "Tu fais apparaître le facteur commun $(x - 2)$ !"], f: "Factorisation partielle puis totale" }
    ],

    // =========================================================================
    // 3. ÉQUATIONS ET INÉQUATIONS
    // =========================================================================
    EQUATIONS: [
      // NIVEAU 1 (10 exos) - Équation produit & inéquations basiques
      { lvl: 1, q: "$(x - 2)(x + 3) = 0$", a: "$x = 2 \\text{ ou } x = -3$", steps: ["Un produit est nul si et seulement si l'un de ses facteurs est nul.", "Résous $x - 2 = 0$ et $x + 3 = 0$."], f: "$A \\times B = 0 \\Leftrightarrow A=0 \\text{ ou } B=0$" },
      { lvl: 1, q: "$x(x - 5) = 0$", a: "$x = 0 \\text{ ou } x = 5$", steps: ["Le premier facteur est simplement $x$."], f: "$A \\times B = 0$" },
      { lvl: 1, q: "$(2x - 1)(x + 4) = 0$", a: "$x = 0.5 \\text{ ou } x = -4$", steps: ["Résous $2x - 1 = 0$, donc $2x = 1$."], f: "$A \\times B = 0$" },
      { lvl: 1, q: "$x^2 - 9 = 0$", a: "$x = 3 \\text{ ou } x = -3$", steps: ["Factorise d'abord : $(x - 3)(x + 3) = 0$."], f: "$x^2 = a \\Rightarrow x = \\pm\\sqrt{a}$" },
      { lvl: 1, q: "$2x > 6$", a: "$x > 3$", steps: ["Divise par 2 des deux côtés. Le sens ne change pas car 2 est positif."], f: "$x > \\frac{b}{a}$" },
      { lvl: 1, q: "$-3x < 12$", a: "$x > -4$", steps: ["Règle d'or : Quand on divise par un nombre négatif, on INVERSE le sens de l'inégalité !"], f: "$diviser par (-) \\Rightarrow inverser$" },
      { lvl: 1, q: "$x + 5 \\leq 2$", a: "$x \\leq -3$", steps: ["Soustrais 5. L'addition/soustraction ne change jamais le sens."], f: "$x \\leq b-a$" },
      { lvl: 1, q: "$4x - 1 \\geq 7$", a: "$x \\geq 2$", steps: ["Ajoute 1 : $4x \\geq 8$. Puis divise."], f: "Inéquation classique" },
      { lvl: 1, q: "$-x \\geq 5$", a: "$x \\leq -5$", steps: ["Multiplie par $-1$ et inverse le sens."], f: "$-x \\geq a \\Rightarrow x \\leq -a$" },
      { lvl: 1, q: "$3x = 0$", a: "$x = 0$", steps: ["Divise par 3. Zéro divisé par 3 fait zéro."], f: "$ax = 0 \\Rightarrow x = 0$" },

      // NIVEAU 2 (7 exos) - Factorisation préalable & inéquations composées
      { lvl: 2, q: "$x^2 = 16$", a: "$x = 4 \\text{ ou } x = -4$", steps: ["Ne donne pas que 4 ! Un carré a toujours deux solutions opposées (si positif)."], f: "$x^2 = a \\Rightarrow x = \\sqrt{a} \\text{ ou } x = -\\sqrt{a}$" },
      { lvl: 2, q: "$(x + 1)^2 - 25 = 0$", a: "$x = 4 \\text{ ou } x = -6$", steps: ["Factorise : $((x+1)-5)((x+1)+5) = 0$.", "Devient $(x-4)(x+6) = 0$."], f: "$A^2 - B^2 = 0$" },
      { lvl: 2, q: "$x^2 + 4x = 0$", a: "$x = 0 \\text{ ou } x = -4$", steps: ["Factorise par $x$ : $x(x + 4) = 0$."], f: "Mise en facteur de $x$" },
      { lvl: 2, q: "$5 - 2x \\leq 9$", a: "$x \\geq -2$", steps: ["Retire 5 : $-2x \\leq 4$.", "Divise par $-2$ et INVERSE le signe !"], f: "Changement de sens" },
      { lvl: 2, q: "$3x - 4 < 5x + 2$", a: "$x > -3$", steps: ["Regroupe les $x$ : $3x - 5x < 2 + 4$.", "$-2x < 6$, divise par $-2$ et inverse."], f: "Changement de sens" },
      { lvl: 2, q: "$-2(x + 3) \\geq 4x$", a: "$x \\leq -1$", steps: ["Développe : $-2x - 6 \\geq 4x$.", "Isole : $-6 \\geq 6x$, puis divise."], f: "Développement et inéquation" },
      { lvl: 2, q: "$\\frac{x}{2} - 3 > 1$", a: "$x > 8$", steps: ["Ajoute 3 : $\\frac{x}{2} > 4$.", "Multiplie par 2."], f: "Élimination de fraction" },

      // NIVEAU 3 (3 exos) - Équations complexes
      { lvl: 3, q: "$(2x - 3)^2 = (x + 1)^2$", a: "$x = 4 \\text{ ou } x = \\frac{2}{3}$", steps: ["Attention, on ne 'supprime' pas les carrés !", "Passe tout à gauche et utilise $A^2 - B^2 = 0$."], f: "$A^2 = B^2 \\Leftrightarrow A^2 - B^2 = 0$" },
      { lvl: 3, q: "$\\frac{2x - 1}{3} - \\frac{x + 2}{4} \\leq 1$", a: "$x \\leq \\frac{22}{5}$", steps: ["Mets toutes les fractions sur 12.", "$\\frac{4(2x-1)}{12} - \\frac{3(x+2)}{12} \\leq \\frac{12}{12}$."], f: "Dénominateur commun" },
      { lvl: 3, q: "$x^3 - x = 0$", a: "$x = 0, x = 1, x = -1$", steps: ["1. Factorise par $x$ : $x(x^2 - 1) = 0$.", "2. Factorise l'identité remarquable : $x(x-1)(x+1) = 0$."], f: "Équation à 3 solutions" }
    ],

    // =========================================================================
    // 4. FRACTIONS ALGÉBRIQUES
    // =========================================================================
    FRACTIONS: [
      // NIVEAU 1 (10 exos) - Simplification et dénominateur commun simple
      { lvl: 1, q: "$\\frac{1}{x} + \\frac{2}{x}$", a: "$\\frac{3}{x}$", steps: ["Même dénominateur, on additionne les numérateurs."], f: "$\\frac{a}{c} + \\frac{b}{c} = \\frac{a+b}{c}$" },
      { lvl: 1, q: "$\\frac{x}{x + 1} - \\frac{2}{x + 1}$", a: "$\\frac{x - 2}{x + 1}$", steps: ["On rassemble sur une seule barre de fraction."], f: "$\\frac{a}{c} - \\frac{b}{c} = \\frac{a-b}{c}$" },
      { lvl: 1, q: "$\\frac{3}{x} = 0$", a: "\\text{Impossible}", steps: ["Une fraction est nulle si et seulement si son NUMÉRATEUR est nul.", "Or 3 n'est jamais égal à 0."], f: "$\\frac{a}{b} = 0 \\Leftrightarrow a = 0 \\text{ et } b \\neq 0$" },
      { lvl: 1, q: "$\\frac{x - 2}{x + 3} = 0$", a: "$x = 2 \\text{ (si } x \\neq -3)$", steps: ["Numérateur nul : $x - 2 = 0$.", "Vérifie la valeur interdite : $x+3 \\neq 0$."], f: "Annulation d'un quotient" },
      { lvl: 1, q: "$\\frac{2x}{5} + \\frac{x}{10}$", a: "$\\frac{x}{2}$", steps: ["Mets sur le même dénominateur (10).", "Devient $\\frac{4x}{10} + \\frac{x}{10} = \\frac{5x}{10}$."], f: "Mise au même dénominateur" },
      { lvl: 1, q: "$\\frac{1}{x} \\times \\frac{x^2}{2}$", a: "$\\frac{x}{2}$", steps: ["Multiplie : $\\frac{x^2}{2x}$.", "Simplifie un $x$ en haut et en bas."], f: "Simplification algébrique" },
      { lvl: 1, q: "$\\frac{3}{x} + 1$", a: "$\\frac{x + 3}{x}$", steps: ["Transforme le $1$ en fraction : $1 = \\frac{x}{x}$."], f: "$1 = \\frac{x}{x}$" },
      { lvl: 1, q: "$2 - \\frac{1}{x - 1}$", a: "$\\frac{2x - 3}{x - 1}$", steps: ["Mets le 2 au même dénominateur : $\\frac{2(x-1)}{x-1}$."], f: "Réduction au même dénominateur" },
      { lvl: 1, q: "$\\frac{x^2 - 1}{x - 1}$", a: "$x + 1 \\text{ (si } x \\neq 1)$", steps: ["Factorise le numérateur : $(x-1)(x+1)$.", "Simplifie par le bloc $(x-1)$."], f: "Simplification par factorisation" },
      { lvl: 1, q: "$\\frac{4x}{2x^2}$", a: "$\\frac{2}{x} \\text{ (si } x \\neq 0)$", steps: ["Divise les nombres : $4/2 = 2$.", "Divise les $x$ : $x/x^2 = 1/x$."], f: "Simplification de monômes" },

      // NIVEAU 2 (7 exos) - Équations quotient et sommes complexes
      { lvl: 2, q: "$\\frac{1}{x} + \\frac{1}{x + 1}$", a: "$\\frac{2x + 1}{x(x + 1)}$", steps: ["Le dénominateur commun est le produit des deux : $x(x+1)$.", "Multiplie en croisé : $\\frac{x+1}{x(x+1)} + \\frac{x}{x(x+1)}$."], f: "$\\frac{a}{b} + \\frac{c}{d} = \\frac{ad + bc}{bd}$" },
      { lvl: 2, q: "$\\frac{2}{x - 1} - \\frac{1}{x}$", a: "$\\frac{x + 1}{x(x - 1)}$", steps: ["Multiplie en croisé.", "Attention au signe moins : $2x - (x - 1)$."], f: "Soustraction croisée" },
      { lvl: 2, q: "$\\frac{x}{2} + \\frac{2}{x}$", a: "$\\frac{x^2 + 4}{2x}$", steps: ["Dénominateur commun : $2x$."], f: "Mise au même dénominateur" },
      { lvl: 2, q: "$\\frac{3}{x + 2} = 1$", a: "$x = 1$", steps: ["Produit en croix : $3 = 1(x + 2)$."], f: "$\\frac{A}{B} = C \\Rightarrow A = B \\times C$" },
      { lvl: 2, q: "$\\frac{2x - 1}{x + 3} = 2$", a: "\\text{Impossible}", steps: ["Produit en croix : $2x - 1 = 2(x + 3)$.", "Devient $2x - 1 = 2x + 6$, soit $-1 = 6$. Absurde !"], f: "Résolution d'équation quotient" },
      { lvl: 2, q: "$\\frac{1}{x} = \\frac{2}{x + 1}$", a: "$x = 1$", steps: ["Produit en croix : $1(x + 1) = 2x$."], f: "$\\frac{A}{B} = \\frac{C}{D} \\Rightarrow AD = BC$" },
      { lvl: 2, q: "$\\frac{x + 1}{x - 2} - 1$", a: "$\\frac{3}{x - 2}$", steps: ["Remplace 1 par $\\frac{x-2}{x-2}$.", "Numérateur : $(x+1) - (x-2) = x + 1 - x + 2$."], f: "Réduction" },

      // NIVEAU 3 (3 exos) - Résolutions avancées
      { lvl: 3, q: "$\\frac{2}{x - 1} = \\frac{3}{x + 1}$", a: "$x = 5$", steps: ["1. Vérifie les valeurs interdites : $x \\neq 1$ et $x \\neq -1$.", "2. Produit en croix : $2(x+1) = 3(x-1)$.", "3. Développe et résous."], f: "Égalité de fractions" },
      { lvl: 3, q: "$\\frac{x^2 - 4}{x - 2} = 5$", a: "$x = 3$", steps: ["1. Valeur interdite : $x \\neq 2$.", "2. Factorise en haut : $(x-2)(x+2)$.", "3. Simplifie par $(x-2)$, il reste $x+2 = 5$."], f: "Simplification avant résolution" },
      { lvl: 3, q: "$\\frac{1}{x} + \\frac{1}{x - 1} = \\frac{2x - 1}{x^2 - x}$", a: "\\text{Identité vraie (pour } x \\neq 0, 1)", steps: ["Calcule le terme de gauche en le mettant au même dénominateur $x(x-1)$.", "Le numérateur devient $x - 1 + x = 2x - 1$."], f: "Vérification d'identité" }
    ]
  }
};