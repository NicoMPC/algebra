// ==================== 5.js - NIVEAU 5ÈME ====================
window.db = window.db || {};

window.db.ALGEBRA_5EME = {
  catDisplay: {
    RELATIFS: "Nombres Relatifs",
    FRACTIONS: "Fractions simples",
    LITTERAL: "Calcul Littéral",
    EQUATIONS: "Opérations à trou"
  },
  catIcon: {
    RELATIFS: "➕➖",
    FRACTIONS: "🥧",
    LITTERAL: "🔤",
    EQUATIONS: "⚖️"
  },
  categories: {
    // =========================================================================
    // 1. NOMBRES RELATIFS
    // =========================================================================
    RELATIFS: [
      // NIVEAU 1 (10 exos)
      { lvl: 1, q: "$(-3) + (-5)$", a: "$-8$", steps: ["Les deux nombres ont le même signe.", "On additionne les distances à zéro : $3 + 5$."], f: "$(-a) + (-b) = -(a + b)$" },
      { lvl: 1, q: "$(+4) + (+7)$", a: "$11$", steps: ["C'est une addition classique de nombres positifs."], f: "$(+a) + (+b) = a + b$" },
      { lvl: 1, q: "$(-8) + (+3)$", a: "$-5$", steps: ["Les signes sont contraires. Le négatif ($8$) l'emporte sur le positif ($3$).", "On fait la soustraction : $8 - 3$."], f: "Signe du plus éloigné de zéro" },
      { lvl: 1, q: "$(+9) + (-2)$", a: "$7$", steps: ["Les signes sont contraires. Le positif l'emporte.", "Soustraction : $9 - 2$."], f: "Signe du plus éloigné de zéro" },
      { lvl: 1, q: "$(-6) - (+4)$", a: "$-10$", steps: ["Soustraire un nombre revient à ajouter son opposé.", "Cela devient : $(-6) + (-4)$."], f: "$a - b = a + (-b)$" },
      { lvl: 1, q: "$(+5) - (-3)$", a: "$8$", steps: ["Soustraire un nombre négatif revient à l'ajouter.", "Cela devient : $(+5) + (+3)$."], f: "$a - (-b) = a + b$" },
      { lvl: 1, q: "$(-2) - (-9)$", a: "$7$", steps: ["Transforme la soustraction en addition.", "Cela devient : $(-2) + (+9)$."], f: "$a - (-b) = a + b$" },
      { lvl: 1, q: "$(-10) + (+10)$", a: "$0$", steps: ["Ces deux nombres sont opposés."], f: "$(-a) + a = 0$" },
      { lvl: 1, q: "$0 - (-7)$", a: "$7$", steps: ["Soustraire un négatif l'ajoute."], f: "$0 - (-a) = a$" },
      { lvl: 1, q: "$(-15) + (-4)$", a: "$-19$", steps: ["Même signe, on cumule les pertes."], f: "$(-a) + (-b) = -(a + b)$" },

      // NIVEAU 2 (7 exos)
      { lvl: 2, q: "$(-3) + (+5) - (-2)$", a: "$4$", steps: ["Transforme d'abord toutes les soustractions en additions.", "Devient : $(-3) + (+5) + (+2)$", "Regroupe les positifs : $(-3) + 7$."], f: "$a - (-b) = a + b$" },
      { lvl: 2, q: "$12 - 15 + 4$", a: "$1$", steps: ["Regroupe les positifs ensemble.", "Regroupement : $(12 + 4) - 15$."], f: "Commutativité" },
      { lvl: 2, q: "$-8 - (-3) - 5$", a: "$-10$", steps: ["Transforme la soustraction centrale.", "Devient : $-8 + 3 - 5$", "Regroupe les négatifs : $-13 + 3$."], f: "$a - (-b) = a + b$" },
      { lvl: 2, q: "$(-7) + (-3) - (+4)$", a: "$-14$", steps: ["Transforme la soustraction.", "Devient : $(-7) + (-3) + (-4)$."], f: "$a - (+b) = a + (-b)$" },
      { lvl: 2, q: "$20 - 25 - 5$", a: "$-10$", steps: ["On part de 20, on descend de 25, puis encore de 5.", "Ou regroupe les pertes : $20 - 30$."], f: "$a - b - c = a - (b + c)$" },
      { lvl: 2, q: "$(-4.5) + (+2.5)$", a: "$-2$", steps: ["Même règle avec les décimaux. Le négatif l'emporte."], f: "Signe du plus éloigné de zéro" },
      { lvl: 2, q: "$3.2 - (-1.8)$", a: "$5$", steps: ["Moins par moins donne plus.", "Devient : $3.2 + 1.8$."], f: "$a - (-b) = a + b$" },

      // NIVEAU 3 (3 exos)
      { lvl: 3, q: "$(-5) - (-8) + (-12) - (+3)$", a: "$-12$", steps: ["Aligne toutes les additions : $(-5) + (+8) + (-12) + (-3)$", "Regroupe les positifs d'un côté et les négatifs de l'autre."], f: "Somme algébrique" },
      { lvl: 3, q: "$15 - 23 + 8 - (-12)$", a: "$12$", steps: ["Simplifie les signes : $15 - 23 + 8 + 12$", "Regroupe les positifs : $15 + 8 + 12 = 35$."], f: "Somme algébrique" },
      { lvl: 3, q: "$-3.5 + 7.2 - (-2.8) - 10$", a: "$-3.5$", steps: ["Simplifie : $-3.5 + 7.2 + 2.8 - 10$", "Astuce : $7.2 + 2.8$ fait un compte rond ($10$)."], f: "Regroupements astucieux" }
    ],

    // =========================================================================
    // 2. FRACTIONS SIMPLES
    // =========================================================================
    FRACTIONS: [
      // NIVEAU 1 (10 exos)
      { lvl: 1, q: "$\\frac{3}{7} + \\frac{2}{7}$", a: "$\\frac{5}{7}$", steps: ["Les dénominateurs sont identiques.", "Additionne uniquement les numérateurs : $3 + 2$."], f: "$\\frac{a}{c} + \\frac{b}{c} = \\frac{a+b}{c}$" },
      { lvl: 1, q: "$\\frac{8}{5} - \\frac{3}{5}$", a: "$\\frac{5}{5} = 1$", steps: ["Soustrait les numérateurs : $8 - 3 = 5$.", "Pense à simplifier la fraction finale."], f: "$\\frac{a}{a} = 1$" },
      { lvl: 1, q: "$\\frac{5}{12} + \\frac{7}{12}$", a: "$\\frac{12}{12} = 1$", steps: ["Même dénominateur, on additionne en haut."], f: "$\\frac{a}{c} + \\frac{b}{c} = \\frac{a+b}{c}$" },
      { lvl: 1, q: "$\\frac{9}{4} - \\frac{1}{4}$", a: "$\\frac{8}{4} = 2$", steps: ["Numérateur : $9 - 1 = 8$.", "La barre de fraction signifie 'divisé par'."], f: "$\\frac{a}{c} - \\frac{b}{c} = \\frac{a-b}{c}$" },
      { lvl: 1, q: "$\\frac{1}{3} + \\frac{1}{3}$", a: "$\\frac{2}{3}$", steps: ["On ne touche jamais aux dénominateurs quand on additionne !"], f: "$\\frac{a}{c} + \\frac{b}{c} = \\frac{a+b}{c}$" },
      { lvl: 1, q: "$\\frac{7}{9} - \\frac{5}{9}$", a: "$\\frac{2}{9}$", steps: ["Soustraction directe des numérateurs."], f: "$\\frac{a}{c} - \\frac{b}{c} = \\frac{a-b}{c}$" },
      { lvl: 1, q: "$\\frac{4}{15} + \\frac{6}{15}$", a: "$\\frac{10}{15} = \\frac{2}{3}$", steps: ["Trouve d'abord $\\frac{10}{15}$.", "Simplifie en divisant en haut et en bas par $5$."], f: "$\\frac{a \\times k}{b \\times k} = \\frac{a}{b}$" },
      { lvl: 1, q: "$\\frac{11}{8} - \\frac{5}{8}$", a: "$\\frac{6}{8} = \\frac{3}{4}$", steps: ["Calcule la soustraction.", "Simplifie par $2$."], f: "Simplification de fraction" },
      { lvl: 1, q: "$\\frac{2}{11} + \\frac{9}{11}$", a: "$1$", steps: ["Additionne les numérateurs.", "Simplifie si possible."], f: "$\\frac{a}{a} = 1$" },
      { lvl: 1, q: "$\\frac{15}{20} - \\frac{5}{20}$", a: "$\\frac{10}{20} = \\frac{1}{2}$", steps: ["Calcule le nouveau numérateur.", "Simplifie par $10$."], f: "Simplification" },

      // NIVEAU 2 (7 exos)
      { lvl: 2, q: "$\\frac{1}{2} + \\frac{1}{4}$", a: "$\\frac{3}{4}$", steps: ["Les dénominateurs sont différents !", "Multiplie la première fraction par $2$ en haut et en bas pour avoir des quarts."], f: "Mettre au même dénominateur" },
      { lvl: 2, q: "$\\frac{2}{3} + \\frac{5}{9}$", a: "$\\frac{11}{9}$", steps: ["Transforme les tiers en neuvièmes.", "Multiplie $\\frac{2}{3}$ par $3$ en haut et en bas."], f: "Mettre au même dénominateur" },
      { lvl: 2, q: "$\\frac{3}{4} - \\frac{3}{8}$", a: "$\\frac{3}{8}$", steps: ["Transforme les quarts en huitièmes.", "$\\frac{3}{4} = \\frac{6}{8}$."], f: "Mettre au même dénominateur" },
      { lvl: 2, q: "$1 + \\frac{2}{5}$", a: "$\\frac{7}{5}$", steps: ["Astuce : $1$ c't la même chose que $\\frac{5}{5}$."], f: "$1 = \\frac{a}{a}$" },
      { lvl: 2, q: "$\\frac{7}{10} - \\frac{1}{2}$", a: "$\\frac{2}{10} = \\frac{1}{5}$", steps: ["Transforme les demis en dixièmes en multipliant par $5$."], f: "Mettre au même dénominateur" },
      { lvl: 2, q: "$2 - \\frac{1}{3}$", a: "$\\frac{5}{3}$", steps: ["Transforme le nombre $2$ en tiers.", "$2 = \\frac{6}{3}$."], f: "$n = \\frac{n \\times a}{a}$" },
      { lvl: 2, q: "$\\frac{5}{6} + \\frac{1}{12}$", a: "$\\frac{11}{12}$", steps: ["Mets tout sur $12$ en multipliant la première fraction par $2$."], f: "Mettre au même dénominateur" },

      // NIVEAU 3 (3 exos)
      { lvl: 3, q: "$\\frac{1}{2} + \\frac{1}{3} + \\frac{1}{6}$", a: "$\\frac{6}{6} = 1$", steps: ["Trouve un dénominateur commun pour les 3 fractions.", "Ici, $6$ est dans la table de $2$ et de $3$."], f: "Dénominateur commun multiple" },
      { lvl: 3, q: "$3 - \\frac{1}{4} - \\frac{1}{2}$", a: "$\\frac{9}{4}$", steps: ["Mets tous les termes sur le dénominateur $4$.", "Rappel : $3 = \\frac{12}{4}$."], f: "Dénominateur commun" },
      { lvl: 3, q: "$\\frac{5}{8} + \\frac{3}{4} - \\frac{1}{2}$", a: "$\\frac{7}{8}$", steps: ["Mets toutes les fractions sur $8$.", "$\\frac{3}{4} = \\frac{6}{8}$ et $\\frac{1}{2} = \\frac{4}{8}$."], f: "Dénominateur commun" }
    ],

    // =========================================================================
    // 3. CALCUL LITTÉRAL
    // =========================================================================
    LITTERAL: [
      // NIVEAU 1 (10 exos)
      { lvl: 1, q: "$3x + 4x$", a: "$7x$", steps: ["Tu as 3 paquets de x et tu en ajoutes 4.", "Additionne simplement les coefficients : $3 + 4$."], f: "$ax + bx = (a+b)x$" },
      { lvl: 1, q: "$8a - 5a$", a: "$3a$", steps: ["On soustrait les coefficients."], f: "$ax - bx = (a-b)x$" },
      { lvl: 1, q: "$x + x + x$", a: "$3x$", steps: ["Chaque $x$ tout seul compte pour $1x$."], f: "$x = 1x$" },
      { lvl: 1, q: "$5y - y$", a: "$4y$", steps: ["Souviens-toi que $y$ c'est $1y$."], f: "$ax - x = (a-1)x$" },
      { lvl: 1, q: "$2x^2 + 5x^2$", a: "$7x^2$", steps: ["Les $x^2$ fonctionnent comme une famille à part.", "Additionne les coefficients."], f: "$ax^2 + bx^2 = (a+b)x^2$" },
      { lvl: 1, q: "$10t - 10t$", a: "$0$", steps: ["Même chose moins la même chose, il ne reste rien."], f: "$ax - ax = 0$" },
      { lvl: 1, q: "$4x + 7x - 2x$", a: "$9x$", steps: ["Calcule de gauche à droite.", "$11x - 2x$."], f: "Réduction successive" },
      { lvl: 1, q: "$x \\times 4$", a: "$4x$", steps: ["En algèbre, on place toujours le nombre avant la lettre sans le signe $\\times$."], f: "$x \\times a = ax$" },
      { lvl: 1, q: "$a \\times a$", a: "$a^2$", steps: ["Un nombre multiplié par lui-même s'écrit au carré."], f: "$x \\times x = x^2$" },
      { lvl: 1, q: "$3 \\times 2x$", a: "$6x$", steps: ["Multiplie les nombres entre eux."], f: "$a \\times bx = (a \\times b)x$" },

      // NIVEAU 2 (7 exos)
      { lvl: 2, q: "$3x + 5 + 2x + 4$", a: "$5x + 9$", steps: ["On ne mélange pas les serviettes ($x$) et les torchons (nombres).", "Regroupe les $x$ ensemble et les nombres seuls ensemble."], f: "Regroupement par termes" },
      { lvl: 2, q: "$8a - 3 + 2a - 5$", a: "$10a - 8$", steps: ["Regroupe les $a$ : $8a + 2a$.", "Regroupe les nombres : $-3 - 5$."], f: "Regroupement et relatifs" },
      { lvl: 2, q: "$x^2 + 3x + 2x^2 - x$", a: "$3x^2 + 2x$", steps: ["Les $x^2$ ne s'additionnent qu'avec les $x^2$.", "Les $x$ ne s'additionnent qu'avec les $x$."], f: "Familles de puissances" },
      { lvl: 2, q: "$5 \\times 2a \\times 3$", a: "$30a$", steps: ["La multiplication peut se faire dans n'importe quel ordre.", "$5 \\times 2 \\times 3$."], f: "Commutativité" },
      { lvl: 2, q: "$7x - (2x + 3x)$", a: "$2x$", steps: ["Calcule d'abord l'intérieur de la parenthèse.", "Devient : $7x - 5x$."], f: "Priorité des parenthèses" },
      { lvl: 2, q: "$4y + 8 - 4y + 2$", a: "$10$", steps: ["Observe bien les $y$ : $4y - 4y$ s'annulent."], f: "Termes opposés" },
      { lvl: 2, q: "$-2x + 7 + 5x - 10$", a: "$3x - 3$", steps: ["Regroupe les $x$ : $-2x + 5x$.", "Regroupe les nombres : $7 - 10$."], f: "Règles des signes" },

      // NIVEAU 3 (3 exos)
      { lvl: 3, q: "Calcule $3x - 5$ pour $x=4$", a: "$7$", steps: ["Remplace la lettre $x$ par la valeur donnée.", "Cela devient $3 \\times 4 - 5$."], f: "Substitution" },
      { lvl: 3, q: "Calcule $x^2 + 2x$ pour $x=3$", a: "$15$", steps: ["Remplace $x$ par $3$.", "Devient : $3^2 + 2 \\times 3$."], f: "Substitution" },
      { lvl: 3, q: "$2(x + 4)$", a: "$2x + 8$", steps: ["Le $2$ doit être distribué (multiplié) à chaque terme dans la parenthèse.", "Fais : $2 \\times x$ puis $2 \\times 4$."], f: "$k(a+b) = ka + kb$" }
    ],

    // =========================================================================
    // 4. OPÉRATIONS À TROU (INITIATION ÉQUATIONS)
    // =========================================================================
    EQUATIONS: [
      // NIVEAU 1 (10 exos)
      { lvl: 1, q: "$x + 5 = 12$", a: "$x = 7$", steps: ["Tu cherches le nombre qui, ajouté à 5, donne 12.", "Fais l'opération inverse : $12 - 5$."], f: "$x + a = b \\Rightarrow x = b - a$" },
      { lvl: 1, q: "$y - 4 = 10$", a: "$y = 14$", steps: ["On a enlevé 4 pour obtenir 10.", "Fais l'opération inverse : $10 + 4$."], f: "$x - a = b \\Rightarrow x = b + a$" },
      { lvl: 1, q: "$3 \\times x = 15$", a: "$x = 5$", steps: ["L'opération inverse de la multiplication est la division.", "$15 \\div 3$."], f: "$a \\times x = b \\Rightarrow x = \\frac{b}{a}$" },
      { lvl: 1, q: "$x + 8 = 20$", a: "$x = 12$", steps: ["Soustrait 8 de chaque côté."], f: "$x = b - a$" },
      { lvl: 1, q: "$a - 7 = 3$", a: "$a = 10$", steps: ["Ajoute 7 de chaque côté."], f: "$x = b + a$" },
      { lvl: 1, q: "$4x = 24$", a: "$x = 6$", steps: ["Rappel : $4x$ veut dire $4 \\times x$."], f: "$x = \\frac{b}{a}$" },
      { lvl: 1, q: "$x + 2.5 = 5$", a: "$x = 2.5$", steps: ["Fais la soustraction : $5 - 2.5$."], f: "$x = b - a$" },
      { lvl: 1, q: "$\\frac{x}{2} = 8$", a: "$x = 16$", steps: ["L'opération inverse de la division est la multiplication.", "$8 \\times 2$."], f: "$\\frac{x}{a} = b \\Rightarrow x = a \\times b$" },
      { lvl: 1, q: "$x - 1 = 0$", a: "$x = 1$", steps: ["Quel nombre moins 1 fait 0 ?"], f: "Évidence" },
      { lvl: 1, q: "$10x = 100$", a: "$x = 10$", steps: ["Divise par 10."], f: "$x = \\frac{b}{a}$" },

      // NIVEAU 2 (7 exos)
      { lvl: 2, q: "$2x + 1 = 7$", a: "$x = 3$", steps: ["Débarrasse-toi d'abord du $+1$ en l'enlevant des deux côtés : $2x = 6$.", "Ensuite, divise par $2$."], f: "Opérations inverses" },
      { lvl: 2, q: "$3x - 2 = 10$", a: "$x = 4$", steps: ["Ajoute $2$ des deux côtés : $3x = 12$.", "Divise par $3$."], f: "Opérations inverses" },
      { lvl: 2, q: "$5x + 5 = 30$", a: "$x = 5$", steps: ["Soustrait $5$ de chaque côté.", "Tu obtiens $5x = 25$."], f: "Opérations inverses" },
      { lvl: 2, q: "$10 + x = 2$", a: "$x = -8$", steps: ["Ici on rentre dans les relatifs.", "Pour isoler $x$, fais $2 - 10$."], f: "$x = b - a$" },
      { lvl: 2, q: "$-3x = 12$", a: "$x = -4$", steps: ["Divise $12$ par $-3$."], f: "Règle des signes en division" },
      { lvl: 2, q: "$4x - 1 = -9$", a: "$x = -2$", steps: ["Ajoute $1$ : $4x = -8$.", "Divise par $4$."], f: "Opérations inverses" },
      { lvl: 2, q: "$\\frac{x}{3} + 2 = 7$", a: "$x = 15$", steps: ["Enlève $2$ : $\\frac{x}{3} = 5$.", "Multiplie par $3$."], f: "Ordre des opérations" },

      // NIVEAU 3 (3 exos)
      { lvl: 3, q: "$2x + 4 = x + 7$", a: "$x = 3$", steps: ["Regroupe les $x$ d'un côté et les nombres de l'autre.", "Enlève $x$ de chaque côté : $x + 4 = 7$."], f: "Équations à 2 inconnues" },
      { lvl: 3, q: "$3x - 5 = x + 5$", a: "$x = 5$", steps: ["Enlève $x$ de chaque côté : $2x - 5 = 5$.", "Ajoute $5$ de chaque côté : $2x = 10$."], f: "Résolution par étapes" },
      { lvl: 3, q: "$2(x + 3) = 14$", a: "$x = 4$", steps: ["Méthode 1 : Distribue le 2 d'abord ($2x + 6 = 14$).", "Méthode 2 : Divise tout par 2 d'abord ($x + 3 = 7$)."], f: "Distributivité ou Division" }
    ]
  }
};