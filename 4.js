// ==================== 4.js - NIVEAU 4ÈME ====================
window.db = window.db || {};

window.db.ALGEBRA_4EME = {
  catDisplay: {
    RELATIFS: "Multiplications & Priorités",
    FRACTIONS: "Opérations sur les Fractions",
    PUISSANCES: "Puissances & Règles",
    CALCUL_LITTERAL: "Calcul Littéral",
    EQUATIONS: "Équations (Niveau 2)"
  },
  catIcon: {
    RELATIFS: "✖️➗",
    FRACTIONS: "🍕",
    PUISSANCES: "🚀",
    CALCUL_LITTERAL: "🧩",
    EQUATIONS: "⚖️"
  },
  categories: {
    // =========================================================================
    // 1. RELATIFS (MULTIPLICATIONS, DIVISIONS, PRIORITÉS)
    // =========================================================================
    RELATIFS: [
      // NIVEAU 1
      { lvl: 1, q: "$(-3) \\times (-4)$", a: "$12$", options: ["$12$", "$-12$", "$7$"], steps: ["Règle des signes : un nombre négatif multiplié par un négatif donne... ?", "Maintenant, multiplie simplement $3$ par $4$."], f: "$(-) \\times (-) = (+)$" },
      { lvl: 1, q: "$(-5) \\times (+2)$", a: "$-10$", options: ["$-10$", "$10$", "$-7$"], steps: ["Règle des signes : un négatif par un positif donne un résultat négatif.", "Fais la multiplication des nombres."], f: "$(-) \\times (+) = (-)$" },
      { lvl: 1, q: "$(+6) \\times (-3)$", a: "$-18$", options: ["$-18$", "$18$", "$3$"], steps: ["Les signes sont contraires. Quel sera le signe de ton résultat final ?", "Calcule $6 \\times 3$."], f: "$(+) \\times (-) = (-)$" },
      { lvl: 1, q: "$(-8) \\div (-2)$", a: "$4$", options: ["$4$", "$-4$", "$-16$"], steps: ["La règle des signes pour la division est la même que pour la multiplication.", "Moins divisé par moins donne plus. Calcule $8 \\div 2$."], f: "$\\frac{-a}{-b} = \\frac{a}{b}$" },
      { lvl: 1, q: "$15 \\div (-3)$", a: "$-5$", options: ["$-5$", "$5$", "$12$"], steps: ["Un nombre positif divisé par un négatif donne un nombre négatif.", "Combien de fois $3$ rentre-t-il dans $15$ ?"], f: "$\\frac{a}{-b} = -\\frac{a}{b}$" },
      { lvl: 1, q: "$(-4) \\times (-1)$", a: "$4$", options: ["$4$", "$-4$", "$-5$"], steps: ["Multiplier par $-1$ sert simplement à prendre l'opposé du nombre.", "Quel est l'opposé de $-4$ ?"], f: "$-a \\times (-1) = a$" },
      { lvl: 1, q: "$(-2) \\times (-2) \\times (-2)$", a: "$-8$", options: ["$-8$", "$8$", "$-6$"], steps: ["Compte les signes 'moins' : il y en a $3$ (un nombre impair). Le résultat final sera donc négatif.", "Calcule ensuite $2 \\times 2 \\times 2$."], f: "Règle des signes (impair)" },
      { lvl: 1, q: "$(-5) \\times 0$", a: "$0$", options: ["$0$", "$-5$", "$5$"], steps: ["Zéro est un élément absorbant : tout ce qui est multiplié par zéro disparaît !"], f: "$a \\times 0 = 0$" },
      { lvl: 1, q: "$(-12) \\div (+4)$", a: "$-3$", options: ["$-3$", "$3$", "$-16$"], steps: ["Signes contraires, résultat négatif.", "Effectue la division $12 \\div 4$."], f: "$\\frac{-a}{b} = -\\frac{a}{b}$" },
      { lvl: 1, q: "$(-1) \\times 7 \\times (-2)$", a: "$14$", options: ["$14$", "$-14$", "$-9$"], steps: ["Il y a deux facteurs négatifs. Le produit sera donc positif.", "Multiplie les chiffres : $1 \\times 7 \\times 2$."], f: "Règle des signes (pair)" },

      // NIVEAU 2
      { lvl: 2, q: "$4 - 5 \\times (-2)$", a: "$14$", options: ["$14$", "$2$", "$-14$"], steps: ["Attention, la multiplication est prioritaire sur la soustraction !", "Calcule d'abord $-5 \\times (-2)$.", "Ajoute ce résultat à $4$."], f: "Priorité à la multiplication" },
      { lvl: 2, q: "$(-3) \\times (-4) - 10$", a: "$2$", options: ["$2$", "$22$", "$-2$"], steps: ["Effectue d'abord la multiplication : $(-3) \\times (-4)$.", "Soustrais ensuite $10$ à ton résultat."], f: "Priorité à la multiplication" },
      { lvl: 2, q: "$\\frac{-15}{3} + 2$", a: "$-3$", options: ["$-3$", "$-7$", "$3$"], steps: ["La barre de fraction agit comme une parenthèse invisible, c'est une division prioritaire.", "Calcule $-15 \\div 3$ d'abord, puis ajoute $2$."], f: "Priorité à la division" },
      { lvl: 2, q: "$-4 \\times (2 - 5)$", a: "$12$", options: ["$12$", "$-12$", "$-28$"], steps: ["Les parenthèses sont la priorité absolue.", "Calcule $2 - 5$ (attention, tu as plus de dettes que de gains).", "Multiplie ensuite $-4$ par ce résultat."], f: "Priorité aux parenthèses" },
      { lvl: 2, q: "$10 - (-2) \\times (-3)$", a: "$4$", options: ["$4$", "$16$", "$-4$"], steps: ["Identifie la multiplication : $(-2) \\times (-3)$. Que donne-t-elle ?", "Maintenant, calcule $10 - 6$."], f: "Priorités opératoires" },
      { lvl: 2, q: "$(-2)^3 + 10$", a: "$2$", options: ["$2$", "$18$", "$-16$"], steps: ["La puissance est le roi des opérations, elle est prioritaire.", "Calcule $(-2) \\times (-2) \\times (-2)$, puis ajoute $10$."], f: "Priorité à la puissance" },
      { lvl: 2, q: "$-5 + 2 \\times (-4) + 3$", a: "$-10$", options: ["$-10$", "$15$", "$-16$"], steps: ["Repère le bloc de multiplication : $2 \\times (-4)$.", "L'expression devient $-5 - 8 + 3$. Fais les calculs de gauche à droite."], f: "Priorités opératoires" },

      // NIVEAU 3
      { lvl: 3, q: "$(-2) \\times (-3 + 5) - (-4) \\times 2$", a: "$4$", options: ["$4$", "$-12$", "$-4$"], steps: ["1. Calcule la parenthèse : $(-3 + 5)$.", "2. Effectue les deux multiplications séparément.", "3. L'expression se simplifie en : $-4 - (-8)$. À toi !"], f: "Priorités en chaîne" },
      { lvl: 3, q: "$\\frac{(-4) \\times 3}{-2 + 8}$", a: "$-2$", options: ["$-2$", "$2$", "$12$"], steps: ["Ici, calcule d'abord tout le numérateur en haut.", "Calcule ensuite tout le dénominateur en bas.", "Divise enfin le haut par le bas !"], f: "Fraction = Parenthèses globales" },
      { lvl: 3, q: "$(-3)^2 - (-2)^3$", a: "$17$", options: ["$17$", "$1$", "$5$"], steps: ["Attention aux signes avec les puissances ! Calcule $(-3)^2$.", "Calcule ensuite $(-2)^3$.", "Pose la soustraction finale avec tes deux résultats."], f: "$a - (-b) = a + b$" }
    ],

    // =========================================================================
    // 2. FRACTIONS (PRODUITS & QUOTIENTS)
    // =========================================================================
    FRACTIONS: [
      // NIVEAU 1
      { lvl: 1, q: "$\\frac{2}{3} \\times \\frac{4}{5}$", a: "$\\frac{8}{15}$", options: ["$\\frac{8}{15}$", "$\\frac{6}{8}$", "$\\frac{10}{12}$"], steps: ["C'est l'opération la plus simple : pas besoin de même dénominateur !", "Multiplie les numérateurs ensemble ($2 \\times 4$) et les dénominateurs ensemble ($3 \\times 5$)."], f: "$\\frac{a}{b} \\times \\frac{c}{d} = \\frac{a \\times c}{b \\times d}$" },
      { lvl: 1, q: "$\\frac{-1}{2} \\times \\frac{3}{7}$", a: "$-\\frac{3}{14}$", options: ["$-\\frac{3}{14}$", "$\\frac{2}{9}$", "$\\frac{3}{14}$"], steps: ["Le signe de la fraction finale sera négatif.", "Effectue le produit en haut, et le produit en bas."], f: "Produit de fractions" },
      { lvl: 1, q: "$\\frac{2}{3} \\div \\frac{5}{7}$", a: "$\\frac{14}{15}$", options: ["$\\frac{14}{15}$", "$\\frac{10}{21}$", "$\\frac{15}{14}$"], steps: ["Règle d'or : Diviser par une fraction, c'est multiplier par son inverse.", "Transforme le calcul en : $\\frac{2}{3} \\times \\frac{7}{5}$."], f: "$\\frac{a}{b} \\div \\frac{c}{d} = \\frac{a}{b} \\times \\frac{d}{c}$" },
      { lvl: 1, q: "$4 \\times \\frac{3}{5}$", a: "$\\frac{12}{5}$", options: ["$\\frac{12}{5}$", "$\\frac{12}{20}$", "$\\frac{7}{5}$"], steps: ["Imagine que le nombre $4$ est une fraction : $\\frac{4}{1}$.", "Multiplie donc le $4$ uniquement avec le nombre du haut ($3$)."], f: "$n \\times \\frac{a}{b} = \\frac{n \\times a}{b}$" },
      { lvl: 1, q: "$\\frac{-3}{4} \\times \\frac{-8}{9}$", a: "$\\frac{2}{3}$", options: ["$\\frac{2}{3}$", "$-\\frac{2}{3}$", "$\\frac{11}{13}$"], steps: ["Moins par moins donne un résultat positif.", "Astuce de pro : simplifie en diagonale AVANT de calculer ! Le $8$ se simplifie avec le $4$, le $9$ avec le $3$."], f: "Simplification croisée" },
      { lvl: 1, q: "$\\frac{1}{2} \\div 3$", a: "$\\frac{1}{6}$", options: ["$\\frac{1}{6}$", "$\\frac{3}{2}$", "$\\frac{2}{3}$"], steps: ["Diviser par $3$, c'est pareil que multiplier par l'inverse de $3$ (qui est $\\frac{1}{3}$).", "Calcule $\\frac{1}{2} \\times \\frac{1}{3}$."], f: "$\\frac{a}{b} \\div n = \\frac{a}{b} \\times \\frac{1}{n}$" },
      { lvl: 1, q: "$\\frac{5}{4} \\times \\frac{4}{5}$", a: "$1$", options: ["$1$", "$\\frac{9}{9}$", "$\\frac{20}{9}$"], steps: ["Observe bien ces deux fractions : l'une est l'inverse de l'autre.", "Que se passe-t-il si tout se simplifie en haut et en bas ?"], f: "$\\frac{a}{b} \\times \\frac{b}{a} = 1$" },
      { lvl: 1, q: "$\\frac{7}{8} \\times \\frac{16}{21}$", a: "$\\frac{2}{3}$", options: ["$\\frac{2}{3}$", "$\\frac{3}{2}$", "$\\frac{14}{24}$"], steps: ["Ne calcule pas $7 \\times 16$ ! Simplifie d'abord.", "Dans la table, $16 = 8 \\times 2$ et $21 = 7 \\times 3$.", "Barre le $7$ en haut et en bas, barre le $8$ en haut et en bas. Que reste-t-il ?"], f: "Décomposition en facteurs" },
      { lvl: 1, q: "$\\frac{3}{2} \\div \\frac{3}{4}$", a: "$2$", options: ["$2$", "$\\frac{9}{8}$", "$\\frac{1}{2}$"], steps: ["Transforme la division en multiplication par l'inverse.", "Devient $\\frac{3}{2} \\times \\frac{4}{3}$. Simplifie les $3$ et conclus !"], f: "Division puis simplification" },
      { lvl: 1, q: "$\\frac{-5}{2} \\times \\frac{2}{-5}$", a: "$1$", options: ["$1$", "$-1$", "$\\frac{-10}{-10}$"], steps: ["Règle des signes : un négatif par un négatif donne du positif.", "Tu multiplies une fraction par son inverse complet. Le résultat est évident !"], f: "Produit de l'inverse" },

      // NIVEAU 2
      { lvl: 2, q: "$\\frac{2}{3} + \\frac{1}{3} \\times \\frac{4}{5}$", a: "$\\frac{14}{15}$", options: ["$\\frac{14}{15}$", "$\\frac{4}{5}$", "$\\frac{12}{15}$"], steps: ["Attention, la multiplication est prioritaire sur l'addition !", "Calcule d'abord $\\frac{1}{3} \\times \\frac{4}{5}$.", "Additionne ensuite $\\frac{2}{3}$ en mettant tout au même dénominateur ($15$)."], f: "Priorité opératoire" },
      { lvl: 2, q: "$\\left(\\frac{1}{2} + \\frac{1}{3}\\right) \\times \\frac{6}{5}$", a: "$1$", options: ["$1$", "$\\frac{6}{5}$", "$\\frac{5}{6}$"], steps: ["Les parenthèses sont prioritaires. Mets les fractions sur un dénominateur commun ($6$).", "Tu obtiens $\\frac{5}{6}$.", "Multiplie ce résultat par $\\frac{6}{5}$ et admire la simplification !"], f: "Priorité aux parenthèses" },
      { lvl: 2, q: "$\\frac{\\frac{2}{3}}{\\frac{5}{7}}$", a: "$\\frac{14}{15}$", options: ["$\\frac{14}{15}$", "$\\frac{10}{21}$", "$\\frac{15}{14}$"], steps: ["C'est une \"fraction à étages\". La grande barre centrale représente une division.", "Réécris-le : $\\frac{2}{3} \\div \\frac{5}{7}$, puis applique la règle de l'inverse."], f: "$\\frac{\\frac{a}{b}}{\\frac{c}{d}} = \\frac{a}{b} \\times \\frac{d}{c}$" },
      { lvl: 2, q: "$1 - \\frac{1}{3} \\times \\frac{3}{2}$", a: "$\\frac{1}{2}$", options: ["$\\frac{1}{2}$", "$1$", "$0$"], steps: ["Priorité à la multiplication ! Simplifie les $3$ en diagonale.", "L'expression devient $1 - \\frac{1}{2}$.", "Si tu as un gâteau et que tu en manges la moitié, que reste-t-il ?"], f: "Simplification croisée" },
      { lvl: 2, q: "$\\frac{3}{4} \\div \\left(\\frac{1}{2} - \\frac{1}{4}\\right)$", a: "$3$", options: ["$3$", "$\\frac{3}{16}$", "$\\frac{1}{3}$"], steps: ["Calcule la parenthèse d'abord. Convertis $\\frac{1}{2}$ en quarts.", "Tu obtiens $\\frac{3}{4} \\div \\frac{1}{4}$.", "Transforme en multiplication par l'inverse et simplifie les $4$ !"], f: "Priorités et inverse" },
      { lvl: 2, q: "$\\frac{5}{6} \\times \\frac{12}{25}$", a: "$\\frac{2}{5}$", options: ["$\\frac{2}{5}$", "$\\frac{5}{2}$", "$\\frac{17}{31}$"], steps: ["Ne te lance pas dans des grands calculs ! Décompose.", "$12$ c'est $6 \\times 2$, et $25$ c'est $5 \\times 5$.", "Barre les nombres communs en haut et en bas."], f: "Décomposition avant produit" },
      { lvl: 2, q: "$\\frac{4}{7} \\times \\left(-\\frac{7}{8}\\right)$", a: "$-\\frac{1}{2}$", options: ["$-\\frac{1}{2}$", "$\\frac{1}{2}$", "$-\\frac{4}{8}$"], steps: ["Le résultat sera négatif.", "Simplifie les $7$ en diagonale.", "Il te reste $\\frac{4}{8}$. Comment peux-tu simplifier cette fraction ?"], f: "Simplification finale" },

      // NIVEAU 3
      { lvl: 3, q: "$\\frac{1 - \\frac{1}{3}}{1 + \\frac{1}{3}}$", a: "$\\frac{1}{2}$", options: ["$\\frac{1}{2}$", "$2$", "$\\frac{2}{3}$"], steps: ["Calcule tout le numérateur : $1 - \\frac{1}{3} = \\frac{2}{3}$.", "Calcule tout le dénominateur : $1 + \\frac{1}{3} = \\frac{4}{3}$.", "Il te reste à faire la division finale : $\\frac{2}{3} \\times \\frac{3}{4}$."], f: "Fraction à étages" },
      { lvl: 3, q: "$\\frac{2}{3} - \\frac{4}{3} \\times \\frac{1}{2} + 1$", a: "$1$", options: ["$1$", "$\\frac{2}{3}$", "$0$"], steps: ["Fais la multiplication d'abord : $\\frac{4}{3} \\times \\frac{1}{2}$ (simplifie le 4 avec le 2).", "L'expression devient : $\\frac{2}{3} - \\frac{2}{3} + 1$.", "Conclus !"], f: "Priorités et annulation" },
      { lvl: 3, q: "$\\frac{\\frac{3}{4} - \\frac{1}{2}}{\\frac{5}{8}}$", a: "$\\frac{2}{5}$", options: ["$\\frac{2}{5}$", "$\\frac{5}{2}$", "$\\frac{1}{5}$"], steps: ["Numérateur : $\\frac{3}{4} - \\frac{2}{4}$. Que trouves-tu ?", "Transforme ensuite la grande division en multiplication : multiplie par l'inverse de $\\frac{5}{8}$."], f: "Fraction à étages" }
    ],

    // =========================================================================
    // 3. PUISSANCES (RÈGLES DE CALCUL)
    // =========================================================================
    PUISSANCES: [
      // NIVEAU 1
      { lvl: 1, q: "$x^2 \\times x^5$", a: "$x^7$", options: ["$x^7$", "$x^{10}$", "$x^3$"], steps: ["Quand on multiplie des puissances de la même famille, on garde la base et on additionne les exposants.", "Calcule $2 + 5$."], f: "$x^a \\times x^b = x^{a+b}$" },
      { lvl: 1, q: "$\\frac{x^8}{x^3}$", a: "$x^5$", options: ["$x^5$", "$x^{11}$", "$x^{\\frac{8}{3}}$"], steps: ["Lors d'une division, on soustrait l'exposant du bas à celui du haut.", "Calcule $8 - 3$."], f: "$\\frac{x^a}{x^b} = x^{a-b}$" },
      { lvl: 1, q: "$(x^3)^2$", a: "$x^6$", options: ["$x^6$", "$x^5$", "$x^9$"], steps: ["Il s'agit d'une \"puissance de puissance\". Dans ce cas, on multiplie les exposants.", "Calcule $3 \\times 2$."], f: "$(x^a)^b = x^{a \\times b}$" },
      { lvl: 1, q: "$10^4 \\times 10^3$", a: "$10^7$", options: ["$10^7$", "$10^{12}$", "$10^1$"], steps: ["La règle est la même pour les puissances de 10.", "Additionne les exposants : $4 + 3$."], f: "$10^a \\times 10^b = 10^{a+b}$" },
      { lvl: 1, q: "$\\frac{10^9}{10^2}$", a: "$10^7$", options: ["$10^7$", "$10^{11}$", "$10^{4.5}$"], steps: ["Tu as une division. Soustrais les exposants en partant du haut."], f: "$\\frac{10^a}{10^b} = 10^{a-b}$" },
      { lvl: 1, q: "$2^3$", a: "$8$", options: ["$8$", "$6$", "$5$"], steps: ["Attention au piège classique ! Ce n'est PAS $2 \\times 3$.", "C'est $2$ multiplié par lui-même $3$ fois : $2 \\times 2 \\times 2$. Calcule-le !"], f: "$a^n = a \\times a \\times \\dots \\times a$" },
      { lvl: 1, q: "$10^{-2}$", a: "$0,01$", options: ["$0,01$", "$-20$", "$-100$"], steps: ["Une puissance négative n'a rien à voir avec un nombre négatif : elle indique l'INVERSE.", "C'est donc $\\frac{1}{10^2}$, c'est-à-dire $\\frac{1}{100}$. Mets-le en décimal !"], f: "$10^{-n} = \\frac{1}{10^n}$" },
      { lvl: 1, q: "$x^1$", a: "$x$", options: ["$x$", "$1$", "$0$"], steps: ["L'exposant $1$ veut dire que la lettre apparaît une seule fois.", "Il est invisible mais toujours là en mathématiques !"], f: "$x^1 = x$" },
      { lvl: 1, q: "$x^0$", a: "$1$", options: ["$1$", "$0$", "$x$"], steps: ["Par convention absolue en mathématiques, tout nombre (non nul) élevé à la puissance zéro donne toujours la même chose.", "C'est l'unité de base de la multiplication."], f: "$x^0 = 1$" },
      { lvl: 1, q: "$a^4 \\times a$", a: "$a^5$", options: ["$a^5$", "$a^4$", "$2a^4$"], steps: ["Rappel : écrire $a$ tout seul, c'est comme écrire $a^1$.", "Additionne donc tes exposants : $4 + 1$."], f: "$a^n \\times a^1 = a^{n+1}$" },

      // NIVEAU 2
      { lvl: 2, q: "$2^3 \\times 2^{-5}$", a: "$2^{-2}$", options: ["$2^{-2}$", "$2^{-15}$", "$4^{-2}$"], steps: ["Même si l'un est négatif, la règle de multiplication reste l'addition des exposants.", "Calcule $3 + (-5)$ (tu as un gain de $3$ et une dette de $5$)."], f: "$x^a \\times x^b = x^{a+b}$" },
      { lvl: 2, q: "$\\frac{10^4 \\times 10^5}{10^7}$", a: "$10^2$", options: ["$10^2$", "$10^3$", "$10^1$"], steps: ["Simplifie le haut d'abord en additionnant les exposants : tu obtiens $10^9$.", "Fais maintenant la division en soustrayant l'exposant du bas : $9 - 7$."], f: "Combinaison de règles" },
      { lvl: 2, q: "$(2x)^3$", a: "$8x^3$", options: ["$8x^3$", "$2x^3$", "$6x^3$"], steps: ["Le cube est à l'extérieur de la parenthèse, il s'applique donc à CHAQUE élément à l'intérieur.", "Calcule $2^3$ d'un côté, et garde $x^3$ de l'autre."], f: "$(a \\times b)^n = a^n \\times b^n$" },
      { lvl: 2, q: "$3^2 \\times 3^{-2}$", a: "$1$", options: ["$1$", "$0$", "$3^{-4}$"], steps: ["Additionne les exposants : $2 + (-2) = 0$.", "On obtient $3^0$. Quelle est la valeur de tout nombre à la puissance zéro ?"], f: "$a^0 = 1$" },
      { lvl: 2, q: "$\\frac{x^5 \\times x^{-2}}{x^2}$", a: "$x$", options: ["$x$", "$x^5$", "$x^3$"], steps: ["Haut : additionne $5$ et $-2$. Tu trouves $x^3$.", "Division : soustrais l'exposant du bas ($2$). Tu trouves $x^1$. Simplifie l'écriture !"], f: "Combinaison de règles" },
      { lvl: 2, q: "$(-2)^4$", a: "$16$", options: ["$16$", "$-16$", "$-8$"], steps: ["La puissance $4$ est paire. Elle annule le signe négatif car \"moins par moins fait plus\" deux fois de suite.", "Calcule $2 \\times 2 \\times 2 \\times 2$."], f: "Signe et exposant pair" },
      { lvl: 2, q: "$-2^4$", a: "$-16$", options: ["$-16$", "$16$", "$8$"], steps: ["Attention au piège des parenthèses ! Il n'y en a pas ici.", "La puissance $4$ ne s'applique QU'AU chiffre $2$, le signe moins reste collé devant à la fin.", "Calcule $2^4$ et mets un moins devant."], f: "$-x^n \\neq (-x)^n$" },

      // NIVEAU 3
      { lvl: 3, q: "$\\frac{(10^2)^3 \\times 10^{-4}}{10^5}$", a: "$10^{-3}$", options: ["$10^{-3}$", "$10^3$", "$10^{-1}$"], steps: ["1. Puissance de puissance : $(10^2)^3 = 10^6$.", "2. Produit au numérateur : $10^6 \\times 10^{-4} = 10^2$.", "3. Il te reste $10^2 \\div 10^5$. Fais la soustraction finale !"], f: "Calcul complexe de puissances" },
      { lvl: 3, q: "$\\frac{4 \\times 10^5 \\times 2 \\times 10^{-3}}{2 \\times 10^4}$", a: "$4 \\times 10^{-2}$", options: ["$4 \\times 10^{-2}$", "$4 \\times 10^6$", "$8 \\times 10^{-2}$"], steps: ["Sépare les vrais nombres des puissances de $10$.", "Les nombres : $\\frac{4 \\times 2}{2}$. Simplifie les $2$.", "Les puissances : en haut $10^5 \\times 10^{-3} = 10^2$. Divise ensuite par $10^4$."], f: "Notation scientifique globale" },
      { lvl: 3, q: "$\\frac{(x^2 y^3)^2}{x^3 y}$", a: "$x y^5$", options: ["$x y^5$", "$x y^2$", "$x^7 y^5$"], steps: ["Distribue le carré en haut : les puissances se multiplient. $(x^2)^2 = x^4$ et $(y^3)^2 = y^6$.", "Ensuite, divise chaque lettre séparément en soustrayant l'exposant du bas à celui du haut.", "Attention, le $y$ en bas est un $y^1$ caché !"], f: "Puissances avec plusieurs variables" }
    ],

    // =========================================================================
    // 4. CALCUL LITTÉRAL
    // =========================================================================
    CALCUL_LITTERAL: [
      // NIVEAU 1
      { lvl: 1, q: "Réduire : $2x + 5x$", a: "$7x$", options: ["$7x$", "$10x$", "$7x^2$"], steps: ["Imagine que les $x$ sont des objets (ex: des stylos).", "Tu as $2$ stylos et on t'en donne $5$. Tu as combien de stylos en tout ?"], f: "Addition de termes semblables" },
      { lvl: 1, q: "Réduire : $3x \\times 4x$", a: "$12x^2$", options: ["$12x^2$", "$7x$", "$12x$"], steps: ["Ici c'est une multiplication ! Le comportement est différent.", "Multiplie d'abord les nombres ensemble : $3 \\times 4$.", "Multiplie ensuite les lettres ensemble : $x \\times x$. Que devient $x \\times x$ ?"], f: "Produit littéral ($x \\times x = x^2$)" },
      { lvl: 1, q: "Développer : $2(x + 4)$", a: "$2x + 8$", options: ["$2x + 8$", "$2x + 4$", "$6x$"], steps: ["C'est la simple distributivité. Le $2$ devant doit être multiplié à chaque élément dans la parenthèse.", "Fais : $2 \\times x$ puis ajoute le résultat de $2 \\times 4$."], f: "$k(a+b) = ka + kb$" },
      { lvl: 1, q: "Réduire : $5x - 8x$", a: "$-3x$", options: ["$-3x$", "$3x$", "$-13x$"], steps: ["Tu restes dans la famille des $x$.", "Calcule simplement l'opération sur les nombres : $5 - 8$ (dette de $8$, gain de $5$)."], f: "Soustraction algébrique" },
      { lvl: 1, q: "Développer : $-3(x - 2)$", a: "$-3x + 6$", options: ["$-3x + 6$", "$-3x - 6$", "$-3x - 2$"], steps: ["Attention au signe lors de la distributivité !", "Tu distribues un nombre NÉGATIF : $-3 \\times x$ et $-3 \\times (-2)$.", "Rappelle-toi que moins par moins donne plus."], f: "$k(a-b) = ka - kb$" },
      { lvl: 1, q: "Développer : $x(x + 5)$", a: "$x^2 + 5x$", options: ["$x^2 + 5x$", "$2x + 5$", "$x^2 + 5$"], steps: ["Ici on distribue la lettre $x$ elle-même.", "Multiplie : $x \\times x$ puis $x \\times 5$."], f: "$x(x+a) = x^2 + ax$" },
      { lvl: 1, q: "Réduire : $x + x + x$", a: "$3x$", options: ["$3x$", "$x^3$", "$3x^3$"], steps: ["Une addition répétée de la même chose devient une multiplication !", "C'est la définition même : combien de fois vois-tu $x$ ?"], f: "$x+x+x = 3x$" },
      { lvl: 1, q: "Réduire : $4x - 7 + 2x$", a: "$6x - 7$", options: ["$6x - 7$", "$-x$", "$6x + 7$"], steps: ["On ne mélange jamais les $x$ avec les nombres seuls.", "Regroupe les $x$ ensemble ($4x + 2x$) et laisse le $-7$ tranquille."], f: "Regroupement par familles" },
      { lvl: 1, q: "Développer : $-(x + 3)$", a: "$-x - 3$", options: ["$-x - 3$", "$-x + 3$", "$x - 3$"], steps: ["Un signe moins seul devant une parenthèse, c'est comme distribuer $-1$.", "L'astuce magique : il suffit de changer les signes de TOUT ce qui est à l'intérieur !"], f: "$-(a+b) = -a-b$" },
      { lvl: 1, q: "Réduire : $5x^2 - 2x^2$", a: "$3x^2$", options: ["$3x^2$", "$3x$", "$7x^2$"], steps: ["Les $x^2$ sont une famille à part. Tu en as $5$ et tu en enlèves $2$.", "Combien t'en reste-t-il ? (La puissance ne change pas)."], f: "Réduction des puissances" },

      // NIVEAU 2
      { lvl: 2, q: "Développer : $(x + 2)(x + 3)$", a: "$x^2 + 5x + 6$", options: ["$x^2 + 5x + 6$", "$x^2 + 6$", "$2x + 5$"], steps: ["Double distributivité ! On distribue chaque terme de la première dans la deuxième.", "1. $x \\times x + x \\times 3$.", "2. $+ 2 \\times x + 2 \\times 3$.", "Réduis les termes en $x$ au milieu !"], f: "$(a+b)(c+d)$" },
      { lvl: 2, q: "Développer : $(x - 4)(x + 1)$", a: "$x^2 - 3x - 4$", options: ["$x^2 - 3x - 4$", "$x^2 - 4$", "$x^2 - 5x - 4$"], steps: ["Distribue : $x^2 + 1x - 4x - 4$.", "Il te reste à fusionner les deux termes du milieu ($1x - 4x$)."], f: "Double distributivité (avec relatifs)" },
      { lvl: 2, q: "Développer : $(2x + 1)(x + 3)$", a: "$2x^2 + 7x + 3$", options: ["$2x^2 + 7x + 3$", "$2x^2 + 3$", "$3x^2 + 7x + 3$"], steps: ["Prends ton temps : $2x \\times x = 2x^2$, puis $2x \\times 3 = 6x$.", "Distribue ensuite le $1$ : $1x + 3$.", "Additionne les termes en $x$."], f: "Double distributivité" },
      { lvl: 2, q: "Développer : $(x - 5)(x - 2)$", a: "$x^2 - 7x + 10$", options: ["$x^2 - 7x + 10$", "$x^2 - 3x - 10$", "$x^2 + 7x + 10$"], steps: ["Attention aux signes lors de la distributivité :", "$x^2 - 2x - 5x$ puis la multiplication finale $-5 \\times (-2)$. Moins par moins..."], f: "Double distributivité" },
      { lvl: 2, q: "Développer : $(3x - 1)(2x - 4)$", a: "$6x^2 - 14x + 4$", options: ["$6x^2 - 14x + 4$", "$6x^2 - 4$", "$5x^2 - 14x + 4$"], steps: ["Commence par $3x \\times 2x$. N'oublie pas le carré !", "Tu obtiens : $6x^2 - 12x - 2x + 4$. Réduis la famille des $x$."], f: "Double distributivité complète" },
      { lvl: 2, q: "Réduire : $x(x + 2) + 3x$", a: "$x^2 + 5x$", options: ["$x^2 + 5x$", "$x^2 + 2x + 3$", "$4x^2$"], steps: ["Étape 1 : Développe la petite parenthèse pour faire sauter le bloc : $x^2 + 2x$.", "Étape 2 : Ajoute le $3x$ qui attendait derrière. Fusionne la famille des $x$."], f: "Développer puis réduire" },
      { lvl: 2, q: "Développer : $(x + 1)(x - 1)$", a: "$x^2 - 1$", options: ["$x^2 - 1$", "$x^2 - 2x - 1$", "$x^2 + 1$"], steps: ["Distribue de façon classique : $x^2 - 1x + 1x - 1$.", "Que se passe-t-il au milieu avec $-x + x$ ? Ils disparaissent !"], f: "$(a+b)(a-b) = a^2 - b^2$" },

      // NIVEAU 3
      { lvl: 3, q: "Développer et réduire : $2(x - 3) - (x + 4)$", a: "$x - 10$", options: ["$x - 10$", "$x - 2$", "$3x - 10$"], steps: ["Découpe le calcul. 1) Distribue le $2$ : $2x - 6$.", "2) Applique le signe moins devant la parenthèse : $-x - 4$.", "3) Regroupe les $x$ ($2x - x$) et les nombres ($-6 - 4$)."], f: "Soustraction d'expressions" },
      { lvl: 3, q: "Développer et réduire : $(x + 2)(2x - 1) - x^2$", a: "$x^2 + 3x - 2$", options: ["$x^2 + 3x - 2$", "$3x^2 + 3x - 2$", "$x^2 + x - 2$"], steps: ["Occupe-toi d'abord de la double distributivité : $2x^2 - x + 4x - 2$.", "Une fois réduit, cela donne $2x^2 + 3x - 2$.", "Soustrais maintenant le $-x^2$ de la fin au terme $2x^2$ !"], f: "Double distrib' combinée" },
      { lvl: 3, q: "Factoriser : $6x + 9$", a: "$3(2x + 3)$", options: ["$3(2x + 3)$", "$3(2x + 9)$", "$6(x + 1.5)$"], steps: ["La factorisation est l'inverse du développement.", "Cherche la plus grande table de multiplication commune à $6$ et $9$. C'est $3$.", "Place le $3$ devant une parenthèse : $3(\\dots)$ et pose-toi la question : $3 \\times ? = 6x$ et $3 \\times ? = 9$."], f: "Introduction à la factorisation" }
    ],

    // =========================================================================
    // 5. ÉQUATIONS (INCONNUES DES DEUX CÔTÉS)
    // =========================================================================
    EQUATIONS: [
      // NIVEAU 1
      { lvl: 1, q: "$2x + 3 = 11$", a: "$x = 4$", options: ["$x = 4$", "$x = 7$", "$x = 14$"], steps: ["Règle de la balance : retire $3$ de chaque côté pour isoler le terme en $x$.", "Tu obtiens $2x = 8$.", "Si deux objets coûtent $8$, combien coûte un seul objet ?"], f: "$ax+b=c \\Rightarrow x=\\frac{c-b}{a}$" },
      { lvl: 1, q: "$3x - 4 = 5$", a: "$x = 3$", options: ["$x = 3$", "$x = \\frac{1}{3}$", "$x = 9$"], steps: ["Annule le $-4$ en ajoutant $4$ de chaque côté de la balance.", "Tu obtiens $3x = 9$. Termine !"], f: "Opérations inverses" },
      { lvl: 1, q: "$\\frac{x}{3} = 4$", a: "$x = 12$", options: ["$x = 12$", "$x = \\frac{4}{3}$", "$x = 7$"], steps: ["Ici ton $x$ est divisé par $3$.", "L'opération magique inverse est de multiplier par $3$ des deux côtés."], f: "$\\frac{x}{a}=b \\Rightarrow x=ab$" },
      { lvl: 1, q: "$-2x = 8$", a: "$x = -4$", options: ["$x = -4$", "$x = 4$", "$x = -10$"], steps: ["Divise ton résultat ($8$) par le nombre accroché à $x$ (qui est $-2$).", "Attention à la règle des signes !"], f: "$x = \\frac{b}{a}$" },
      { lvl: 1, q: "$x - 7 = -2$", a: "$x = 5$", options: ["$x = 5$", "$x = -9$", "$x = -5$"], steps: ["Pour garder ton $x$ tout seul, ajoute $7$ des deux côtés.", "Tu te retrouves avec $-2 + 7$. Que donne ton gain final ?"], f: "Opérations inverses" },
      { lvl: 1, q: "$4x + 1 = 1$", a: "$x = 0$", options: ["$x = 0$", "$x = 1$", "$x = -1$"], steps: ["Retire $1$ de chaque côté : l'équation devient $4x = 0$.", "Si je multiplie un nombre par $4$ et que j'obtiens zéro, quel est ce nombre ?"], f: "$ax = 0 \\Rightarrow x = 0$" },
      { lvl: 1, q: "$6x = -18$", a: "$x = -3$", options: ["$x = -3$", "$x = 3$", "$x = -12$"], steps: ["Il suffit de diviser $-18$ par $6$. Reste attentif aux signes."], f: "Division avec relatifs" },
      { lvl: 1, q: "$\\frac{x}{2} + 1 = 5$", a: "$x = 8$", options: ["$x = 8$", "$x = 2$", "$x = 12$"], steps: ["Déshabille le $x$ étape par étape. Retire d'abord le $1$ : tu obtiens $\\frac{x}{2} = 4$.", "La moitié du nombre vaut $4$. Quel est ce nombre entier ?"], f: "Opérations inverses en cascade" },
      { lvl: 1, q: "$10 - x = 3$", a: "$x = 7$", options: ["$x = 7$", "$x = -7$", "$x = 13$"], steps: ["Logique pure : J'ai $10$, j'enlève une certaine somme, et il me reste $3$.", "Combien ai-je enlevé ?"], f: "Équation de différence" },
      { lvl: 1, q: "$-x = -5$", a: "$x = 5$", options: ["$x = 5$", "$x = -5$", "$x = 0$"], steps: ["L'opposé de $x$ vaut l'opposé de $5$.", "Change simplement le signe des deux côtés simultanément !"], f: "$-x = -a \\Rightarrow x = a$" },

      // NIVEAU 2
      { lvl: 2, q: "$3x + 2 = x + 8$", a: "$x = 3$", options: ["$x = 3$", "$x = 5$", "$x = -3$"], steps: ["Objectif : Tous les $x$ d'un côté, tous les nombres de l'autre.", "Retire d'abord $x$ de chaque côté : il te reste $2x + 2 = 8$.", "Retire maintenant $2$ de chaque côté et conclus."], f: "$ax+b=cx+d$" },
      { lvl: 2, q: "$5x - 3 = 2x + 9$", a: "$x = 4$", options: ["$x = 4$", "$x = 2$", "$x = -4$"], steps: ["Retire $2x$ des deux côtés pour réunir la famille des $x$ : $3x - 3 = 9$.", "Ajoute $3$ des deux côtés pour isoler la famille : $3x = 12$. Trouve $x$."], f: "$ax+b=cx+d$" },
      { lvl: 2, q: "$4x + 7 = x - 5$", a: "$x = -4$", options: ["$x = -4$", "$x = 4$", "$x = -12$"], steps: ["Retire $x$ des deux côtés : $3x + 7 = -5$.", "Retire $7$ des deux côtés (attention à la dette cumulative) : $3x = -12$. Divise !"], f: "$ax+b=cx+d$" },
      { lvl: 2, q: "$2x = 5x - 12$", a: "$x = 4$", options: ["$x = 4$", "$x = -4$", "$x = 12$"], steps: ["Astuce de stratège : retire $2x$ des deux côtés pour éviter les $x$ négatifs !", "L'équation devient $0 = 3x - 12$.", "Passe le $-12$ de l'autre côté : $12 = 3x$."], f: "Regroupement stratégique" },
      { lvl: 2, q: "$-3x + 4 = x - 8$", a: "$x = 3$", options: ["$x = 3$", "$x = -3$", "$x = -1$"], steps: ["Même stratégie : ajoute $3x$ des deux côtés pour rendre les $x$ positifs à droite.", "L'équation devient $4 = 4x - 8$.", "Ajoute $8$ de chaque côté pour isoler $4x$."], f: "Rendre le coefficient positif" },
      { lvl: 2, q: "$7x - 1 = 3x + 11$", a: "$x = 3$", options: ["$x = 3$", "$x = 12$", "$x = -3$"], steps: ["Soustrais le plus petit tas de $x$ ($3x$) de chaque côté : $4x - 1 = 11$.", "Ajoute $1$ : $4x = 12$."], f: "$ax+b=cx+d$" },
      { lvl: 2, q: "$x - 2 = 4x + 7$", a: "$x = -3$", options: ["$x = -3$", "$x = 3$", "$x = -1.5$"], steps: ["Retire $x$ de chaque côté : $-2 = 3x + 7$.", "Enlève le $7$ en soustrayant des deux côtés : $-9 = 3x$. Conclus."], f: "Regroupement des inconnues" },

      // NIVEAU 3
      { lvl: 3, q: "$2(x + 3) = 4x - 2$", a: "$x = 4$", options: ["$x = 4$", "$x = -4$", "$x = 2$"], steps: ["Développe toujours les parenthèses en premier ! $2x + 6 = 4x - 2$.", "Retire $2x$ de chaque côté pour les regrouper à droite : $6 = 2x - 2$.", "Ajoute $2$ de chaque côté et divise !"], f: "Développement puis résolution" },
      { lvl: 3, q: "$3(2x - 1) = 2(x + 5)$", a: "$x = 3,25$", options: ["$x = 3,25$", "$x = 2,5$", "$x = -3,25$"], steps: ["Distribue des deux côtés : $6x - 3 = 2x + 10$.", "Ramène les $x$ à gauche ($-2x$) et les nombres à droite ($+3$).", "Tu obtiens $4x = 13$. La division ne tombe pas juste, donne la valeur décimale !"], f: "Double distribution" },
      { lvl: 3, q: "$x - (2x + 3) = 5$", a: "$x = -8$", options: ["$x = -8$", "$x = 8$", "$x = -2$"], steps: ["Attention au signe moins devant la parenthèse ! Il change tout : $x - 2x - 3 = 5$.", "Simplifie le côté gauche : $-x - 3 = 5$.", "Ajoute $3$ des deux côtés : $-x = 8$. Que vaut $x$ positif ?"], f: "Soustraction d'une expression" }
    ]
  }
};