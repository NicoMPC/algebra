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
      { lvl: 1, q: "$(-3) + (-5)$", a: "$-8$", steps: ["Imagine que tu as une dette de $3$ € et que tu fais une nouvelle dette de $5$ €.", "Tes dettes se cumulent. Quelle est ta dette totale ?"], f: "$(-a) + (-b) = -(a + b)$" },
      { lvl: 1, q: "$(+4) + (+7)$", a: "$11$", steps: ["C'est une addition classique : tu gagnes $4$ € puis tu gagnes encore $7$ €.", "Quel est ton gain total ?"], f: "$(+a) + (+b) = a + b$" },
      { lvl: 1, q: "$(-8) + (+3)$", a: "$-5$", steps: ["Tu as une dette de $8$ € ($-8$) et tu rembourses $3$ € ($+3$).", "As-tu assez pour tout rembourser ? Que te reste-t-il ?"], f: "Signe de la plus grande distance" },
      { lvl: 1, q: "$(+9) + (-2)$", a: "$7$", steps: ["Tu gagnes $9$ € mais tu dois payer une dette de $2$ €.", "Fais la soustraction pour trouver ton bénéfice."], f: "Signe de la plus grande distance" },
      { lvl: 1, q: "$(-6) - (+4)$", a: "$-10$", steps: ["Soustraire un gain, c'est comme ajouter une dette.", "L'opération se transforme en : $(-6) + (-4)$.", "Tu cumules deux dettes, calcule le total !"], f: "$a - b = a + (-b)$" },
      { lvl: 1, q: "$(+5) - (-3)$", a: "$8$", steps: ["Règle d'or : soustraire une dette ($- (-3)$) revient à gagner de l'argent ($+ 3$).", "L'opération se transforme en : $(+5) + (+3)$."], f: "$a - (-b) = a + b$" },
      { lvl: 1, q: "$(-2) - (-9)$", a: "$7$", steps: ["Comme pour l'exercice précédent, effacer une dette de $9$ revient à gagner $9$.", "Cela devient $(-2) + (+9)$. Que reste-t-il ?"], f: "$a - (-b) = a + b$" },
      { lvl: 1, q: "$(-10) + (+10)$", a: "$0$", steps: ["Tu perds $10$ €, puis tu gagnes $10$ €.", "Où en es-tu financièrement ?"], f: "$(-a) + a = 0$" },
      { lvl: 1, q: "$0 - (-7)$", a: "$7$", steps: ["Enlever du négatif revient à ajouter du positif.", "Le calcul devient $0 + 7$."], f: "$0 - (-a) = a$" },
      { lvl: 1, q: "$(-15) + (-4)$", a: "$-19$", steps: ["Même signe ! On cumule simplement les deux pertes."], f: "$(-a) + (-b) = -(a + b)$" },

      // NIVEAU 2 (7 exos)
      { lvl: 2, q: "$(-3) + (+5) - (-2)$", a: "$4$", steps: ["Transforme d'abord la soustraction en addition : $- (-2)$ devient $+ (+2)$.", "Ton calcul est maintenant $(-3) + (+5) + (+2)$.", "Regroupe tes gains ($5+2$) puis enlève ta dette ($3$)."], f: "$a - (-b) = a + b$" },
      { lvl: 2, q: "$12 - 15 + 4$", a: "$1$", steps: ["Rassemble tes nombres positifs (tes gains) d'un côté.", "Fais $(12 + 4) - 15$."], f: "Commutativité" },
      { lvl: 2, q: "$-8 - (-3) - 5$", a: "$-10$", steps: ["Transforme la soustraction centrale : $- (-3)$ devient $+ 3$.", "Ton calcul : $-8 + 3 - 5$.", "Regroupe tes dettes ensemble ($-8$ et $-5$), puis ajoute ton gain ($+3$)."], f: "Regroupement de termes" },
      { lvl: 2, q: "$(-7) + (-3) - (+4)$", a: "$-14$", steps: ["Soustraire du positif, c'est comme ajouter du négatif.", "Tu n'as que des dettes : $(-7) + (-3) + (-4)$. Additionne tout !"], f: "$a - (+b) = a + (-b)$" },
      { lvl: 2, q: "$20 - 25 - 5$", a: "$-10$", steps: ["Si tu préfères, regroupe les pertes : tu perds $25$ puis tu perds $5$, tu as donc perdu $30$ en tout.", "Il te reste à calculer $20 - 30$."], f: "$a - b - c = a - (b + c)$" },
      { lvl: 2, q: "$(-4,5) + (+2,5)$", a: "$-2$", steps: ["La règle est la même qu'avec les entiers. La perte ($4,5$) est plus grande que le gain ($2,5$).", "Le résultat sera négatif. Fais la différence entre les deux."], f: "Addition de décimaux relatifs" },
      { lvl: 2, q: "$3,2 - (-1,8)$", a: "$5$", steps: ["Enlever un négatif revient à l'ajouter.", "Le calcul devient $3,2 + 1,8$. Utilise les compléments !"], f: "$a - (-b) = a + b$" },

      // NIVEAU 3 (3 exos)
      { lvl: 3, q: "$(-5) - (-8) + (-12) - (+3)$", a: "$-12$", steps: ["Nettoie l'expression en transformant toutes les soustractions : $(-5) + (+8) + (-12) + (-3)$.", "Regroupe les positifs ensemble ($8$) et tous les négatifs ensemble ($5+12+3$).", "Termine le calcul final."], f: "Somme algébrique complexe" },
      { lvl: 3, q: "$15 - 23 + 8 - (-12)$", a: "$12$", steps: ["Simplifie la fin du calcul : $- (-12)$ devient $+ 12$.", "Regroupe les positifs : $15 + 8 + 12 = 35$.", "Calcule $35 - 23$."], f: "Simplification d'écriture" },
      { lvl: 3, q: "$-3,5 + 7,2 - (-2,8) - 10$", a: "$-3,5$", steps: ["Simplifie : $-3,5 + 7,2 + 2,8 - 10$.", "Astuce : $7,2 + 2,8$ forment un nombre entier rond.", "Remplace-les et termine ton calcul."], f: "Regroupements astucieux" }
    ],

    // =========================================================================
    // 2. FRACTIONS SIMPLES
    // =========================================================================
    FRACTIONS: [
      // NIVEAU 1 (10 exos)
      { lvl: 1, q: "$\\frac{3}{7} + \\frac{2}{7}$", a: "$\\frac{5}{7}$", steps: ["Les dénominateurs (en bas) sont identiques, les parts ont la même taille.", "Additionne simplement les parts (en haut) : $3 + 2$."], f: "$\\frac{a}{c} + \\frac{b}{c} = \\frac{a+b}{c}$" },
      { lvl: 1, q: "$\\frac{8}{5} - \\frac{3}{5}$", a: "$1$", steps: ["Soustrait les numérateurs : $8 - 3 = 5$.", "Tu obtiens $\\frac{5}{5}$. Pense à simplifier la fraction finale !"], f: "$\\frac{a}{a} = 1$" },
      { lvl: 1, q: "$\\frac{5}{12} + \\frac{7}{12}$", a: "$1$", steps: ["Même dénominateur, on additionne en haut. Tu obtiens $\\frac{12}{12}$.", "Combien vaut une fraction dont le haut et le bas sont identiques ?"], f: "$\\frac{a}{c} + \\frac{b}{c} = \\frac{a+b}{c}$" },
      { lvl: 1, q: "$\\frac{9}{4} - \\frac{1}{4}$", a: "$2$", steps: ["Fais la soustraction en haut : $9 - 1 = 8$.", "La barre de fraction signifie 'divisé par'. Que vaut $8 \\div 4$ ?"], f: "$\\frac{a}{c} - \\frac{b}{c} = \\frac{a-b}{c}$" },
      { lvl: 1, q: "$\\frac{1}{3} + \\frac{1}{3}$", a: "$\\frac{2}{3}$", steps: ["Attention, on ne touche jamais aux dénominateurs (le chiffre du bas) quand on additionne !"], f: "$\\frac{a}{c} + \\frac{b}{c} = \\frac{a+b}{c}$" },
      { lvl: 1, q: "$\\frac{7}{9} - \\frac{5}{9}$", a: "$\\frac{2}{9}$", steps: ["Soustraction directe des numérateurs. Laisse le $9$ tranquille."], f: "$\\frac{a}{c} - \\frac{b}{c} = \\frac{a-b}{c}$" },
      { lvl: 1, q: "$\\frac{4}{15} + \\frac{6}{15}$", a: "$\\frac{2}{3}$", steps: ["Trouve d'abord $\\frac{10}{15}$.", "Pour rendre la fraction irréductible, cherche une table commune pour diviser $10$ et $15$."], f: "Addition puis simplification" },
      { lvl: 1, q: "$\\frac{11}{8} - \\frac{5}{8}$", a: "$\\frac{3}{4}$", steps: ["Calcule la soustraction : tu obtiens $\\frac{6}{8}$.", "Les deux nombres sont pairs. Divise en haut et en bas par $2$."], f: "Simplification par 2" },
      { lvl: 1, q: "$\\frac{2}{11} + \\frac{9}{11}$", a: "$1$", steps: ["Additionne les numérateurs.", "Si tu as pris toutes les parts du gâteau, tu as l'unité !"], f: "$\\frac{a}{a} = 1$" },
      { lvl: 1, q: "$\\frac{15}{20} - \\frac{5}{20}$", a: "$\\frac{1}{2}$", steps: ["Calcule le nouveau numérateur pour obtenir $\\frac{10}{20}$.", "Simplifie au maximum en divisant par $10$ en haut et en bas."], f: "Simplification de fraction" },

      // NIVEAU 2 (7 exos)
      { lvl: 2, q: "$\\frac{1}{2} + \\frac{1}{4}$", a: "$\\frac{3}{4}$", steps: ["Impossible d'additionner des demis et des quarts directement !", "Transforme d'abord $\\frac{1}{2}$ en multipliant en haut et en bas par $2$.", "Maintenant tu peux calculer $\\frac{2}{4} + \\frac{1}{4}$."], f: "Mettre au même dénominateur" },
      { lvl: 2, q: "$\\frac{2}{3} + \\frac{5}{9}$", a: "$\\frac{11}{9}$", steps: ["Transforme les tiers en neuvièmes.", "Multiplie $\\frac{2}{3}$ par $3$ en haut et en bas, puis fais l'addition."], f: "Mettre au même dénominateur" },
      { lvl: 2, q: "$\\frac{3}{4} - \\frac{3}{8}$", a: "$\\frac{3}{8}$", steps: ["Transforme la première fraction pour que son dénominateur soit $8$.", "Multiplie $\\frac{3}{4}$ par $2$ en haut et en bas."], f: "Mettre au même dénominateur" },
      { lvl: 2, q: "$1 + \\frac{2}{5}$", a: "$\\frac{7}{5}$", steps: ["Astuce : Le nombre $1$ représente un gâteau entier.", "En cinquièmes, un gâteau entier s'écrit $\\frac{5}{5}$."], f: "$1 = \\frac{a}{a}$" },
      { lvl: 2, q: "$\\frac{7}{10} - \\frac{1}{2}$", a: "$\\frac{1}{5}$", steps: ["Transforme les demis en dixièmes en multipliant par $5$.", "Calcule $\\frac{7}{10} - \\frac{5}{10}$ puis simplifie le résultat !"], f: "Mise au même dénominateur + Simplification" },
      { lvl: 2, q: "$2 - \\frac{1}{3}$", a: "$\\frac{5}{3}$", steps: ["Transforme le nombre entier $2$ en une fraction sur $3$.", "Si $1 = \\frac{3}{3}$, alors $2 = \\frac{6}{3}$. Poursuis le calcul."], f: "$n = \\frac{n \\times a}{a}$" },
      { lvl: 2, q: "$\\frac{5}{6} + \\frac{1}{12}$", a: "$\\frac{11}{12}$", steps: ["Trouve le dénominateur commun. Ici, c'est $12$.", "Multiplie la première fraction par $2$ en haut et en bas."], f: "Mettre au même dénominateur" },

      // NIVEAU 3 (3 exos)
      { lvl: 3, q: "$\\frac{1}{2} + \\frac{1}{3} + \\frac{1}{6}$", a: "$1$", steps: ["Trouve un dénominateur commun pour les 3 fractions.", "Le nombre $6$ est dans la table de $2$ et de $3$. Mets tout sur $6$.", "Fais la somme, tu devrais obtenir une belle surprise."], f: "Dénominateur commun multiple" },
      { lvl: 3, q: "$3 - \\frac{1}{4} - \\frac{1}{2}$", a: "$\\frac{9}{4}$", steps: ["Mets tous les termes sur le même dénominateur ($4$).", "Rappel : $3$ entiers, c'est $\\frac{12}{4}$."], f: "Dénominateur commun global" },
      { lvl: 3, q: "$\\frac{5}{8} + \\frac{3}{4} - \\frac{1}{2}$", a: "$\\frac{7}{8}$", steps: ["Mets toutes les fractions sur le plus grand dénominateur : $8$.", "$\\frac{3}{4} = \\frac{6}{8}$ et $\\frac{1}{2} = \\frac{4}{8}$. À toi de jouer !"], f: "Dénominateur commun global" }
    ],

    // =========================================================================
    // 3. CALCUL LITTÉRAL
    // =========================================================================
    LITTERAL: [
      // NIVEAU 1 (10 exos)
      { lvl: 1, q: "$3x + 4x$", a: "$7x$", steps: ["Imagine que $x$ est un objet.", "Tu as $3$ objets et tu en ajoutes $4$. Combien d'objets as-tu en tout ?"], f: "$ax + bx = (a+b)x$" },
      { lvl: 1, q: "$8a - 5a$", a: "$3a$", steps: ["La lettre reste la même, soustrais simplement les nombres devant."], f: "$ax - bx = (a-b)x$" },
      { lvl: 1, q: "$x + x + x$", a: "$3x$", steps: ["Chaque $x$ tout seul compte pour $1x$.", "Calcule $1x + 1x + 1x$."], f: "$x = 1x$" },
      { lvl: 1, q: "$5y - y$", a: "$4y$", steps: ["Souviens-toi qu'écrire $y$ seul, c'est exactement comme écrire $1y$."], f: "$ax - x = (a-1)x$" },
      { lvl: 1, q: "$2x^2 + 5x^2$", a: "$7x^2$", steps: ["Les $x^2$ fonctionnent comme une famille à part.", "Additionne les nombres devant (les coefficients) sans toucher aux puissances."], f: "$ax^2 + bx^2 = (a+b)x^2$" },
      { lvl: 1, q: "$10t - 10t$", a: "$0$", steps: ["Si tu as $10$ objets et qu'on t'en enlève $10$, que reste-t-il ?"], f: "$ax - ax = 0$" },
      { lvl: 1, q: "$4x + 7x - 2x$", a: "$9x$", steps: ["Fais le calcul de gauche à droite.", "D'abord $4x + 7x$, puis enlève $2x$ au résultat."], f: "Réduction successive" },
      { lvl: 1, q: "$x \\times 4$", a: "$4x$", steps: ["En algèbre, on place toujours le nombre avant la lettre pour faire joli.", "On a aussi le droit d'effacer le signe $\\times$."], f: "$x \\times a = ax$" },
      { lvl: 1, q: "$a \\times a$", a: "$a^2$", steps: ["Un nombre multiplié par lui-même s'écrit avec une petite puissance en l'air."], f: "$x \\times x = x^2$" },
      { lvl: 1, q: "$3 \\times 2x$", a: "$6x$", steps: ["Tu as $3$ paquets qui contiennent chacun $2x$.", "Multiplie les nombres entre eux, la lettre suit."], f: "$a \\times bx = (a \\times b)x$" },

      // NIVEAU 2 (7 exos)
      { lvl: 2, q: "$3x + 5 + 2x + 4$", a: "$5x + 9$", steps: ["Règle d'or : on ne mélange pas la famille des $x$ avec la famille des nombres seuls.", "Additionne les $x$ ensemble ($3x + 2x$) et les nombres ensemble ($5 + 4$)."], f: "Regroupement par familles" },
      { lvl: 2, q: "$8a - 3 + 2a - 5$", a: "$10a - 8$", steps: ["Regroupe les $a$ : $8a + 2a$.", "Regroupe les nombres relatifs : $-3 - 5$ (attention, tu cumules deux dettes !)."], f: "Regroupement et relatifs" },
      { lvl: 2, q: "$x^2 + 3x + 2x^2 - x$", a: "$3x^2 + 2x$", steps: ["Chaque puissance a sa famille. Les $x^2$ ne s'additionnent qu'avec les $x^2$.", "Regroupe les $x^2$ ensemble, puis regroupe les $x$ ensemble."], f: "Familles de puissances" },
      { lvl: 2, q: "$5 \\times 2a \\times 3$", a: "$30a$", steps: ["Dans une multiplication, l'ordre n'a pas d'importance.", "Calcule $5 \\times 2 \\times 3$, puis ajoute la lettre $a$ à la fin."], f: "Commutativité du produit" },
      { lvl: 2, q: "$7x - (2x + 3x)$", a: "$2x$", steps: ["Les parenthèses sont prioritaires. Calcule d'abord l'intérieur de la parenthèse.", "Fais ensuite la soustraction."], f: "Priorité des parenthèses" },
      { lvl: 2, q: "$4y + 8 - 4y + 2$", a: "$10$", steps: ["Observe bien les lettres : tu as $4y$ et plus loin $-4y$.", "Ils s'annulent ! Que te reste-t-il ?"], f: "Annulation de termes opposés" },
      { lvl: 2, q: "$-2x + 7 + 5x - 10$", a: "$3x - 3$", steps: ["Regroupe les $x$ : $-2x + 5x$. (Dette de $2$, gain de $5$).", "Regroupe les nombres : $+7 - 10$. (Gain de $7$, dette de $10$)."], f: "Réduction avec signes" },

      // NIVEAU 3 (3 exos)
      { lvl: 3, q: "Calcule $3x - 5$ pour $x=4$", a: "$7$", steps: ["L'expression signifie $3 \\times x - 5$.", "Remplace la lettre $x$ par le nombre $4$ et fais le calcul !"], f: "Substitution algébrique" },
      { lvl: 3, q: "Calcule $x^2 + 2x$ pour $x=3$", a: "$15$", steps: ["Remplace tous les $x$ par le nombre $3$.", "Cela devient : $3^2 + 2 \\times 3$. Priorité aux puissances et multiplications !"], f: "Substitution algébrique" },
      { lvl: 3, q: "$2(x + 4)$", a: "$2x + 8$", steps: ["C'est la règle de la distributivité : le $2$ devant doit être multiplié à CHAQUE terme de la parenthèse.", "Fais : $2 \\times x$ puis ajoute $2 \\times 4$."], f: "$k(a+b) = ka + kb$" }
    ],

    // =========================================================================
    // 4. OPÉRATIONS À TROU (INITIATION ÉQUATIONS)
    // =========================================================================
    EQUATIONS: [
      // NIVEAU 1 (10 exos)
      { lvl: 1, q: "$x + 5 = 12$", a: "$x = 7$", steps: ["Tu cherches le nombre qui, ajouté à $5$, donne $12$.", "Pour faire marche arrière, fais l'opération inverse : $12 - 5$."], f: "$x + a = b \\Rightarrow x = b - a$" },
      { lvl: 1, q: "$y - 4 = 10$", a: "$y = 14$", steps: ["On a enlevé $4$ à ton nombre mystère pour obtenir $10$.", "Pour retrouver le nombre de départ, fais l'opération inverse : $10 + 4$."], f: "$x - a = b \\Rightarrow x = b + a$" },
      { lvl: 1, q: "$3 \\times x = 15$", a: "$x = 5$", steps: ["$3$ paquets coûtent $15$. Combien coûte un paquet ?", "L'opération inverse de la multiplication est la division. Fais $15 \\div 3$."], f: "$a \\times x = b \\Rightarrow x = b \\div a$" },
      { lvl: 1, q: "$x + 8 = 20$", a: "$x = 12$", steps: ["Pour isoler $x$, fais l'opération inverse du $+8$ de l'autre côté."], f: "$x = b - a$" },
      { lvl: 1, q: "$a - 7 = 3$", a: "$a = 10$", steps: ["Fais basculer le $-7$ de l'autre côté en changeant son opération."], f: "$x = b + a$" },
      { lvl: 1, q: "$4x = 24$", a: "$x = 6$", steps: ["Rappel : $4x$ signifie $4 \\times x$.", "Fais l'opération inverse."], f: "$x = b \\div a$" },
      { lvl: 1, q: "$x + 2,5 = 5$", a: "$x = 2,5$", steps: ["Fais la soustraction : $5 - 2,5$."], f: "$x = b - a$" },
      { lvl: 1, q: "$\\frac{x}{2} = 8$", a: "$x = 16$", steps: ["La moitié de ton nombre vaut $8$.", "L'opération inverse de la division par $2$ est la multiplication par $2$ !"], f: "$\\frac{x}{a} = b \\Rightarrow x = a \\times b$" },
      { lvl: 1, q: "$x - 1 = 0$", a: "$x = 1$", steps: ["Quel nombre, si on lui enlève $1$, ne laisse plus rien ($0$) ?"], f: "Évidence logique" },
      { lvl: 1, q: "$10x = 100$", a: "$x = 10$", steps: ["Tu as $10$ objets qui valent $100$ en tout. Divise pour trouver l'unité."], f: "$x = b \\div a$" },

      // NIVEAU 2 (7 exos)
      { lvl: 2, q: "$2x + 1 = 7$", a: "$x = 3$", steps: ["Pense au parcours inverse. Débarrasse-toi d'abord du $+1$ en l'enlevant des deux côtés : $2x = 6$.", "Maintenant que tu as $2x = 6$, divise par $2$."], f: "Opérations inverses" },
      { lvl: 2, q: "$3x - 2 = 10$", a: "$x = 4$", steps: ["Annule le $-2$ en faisant $+2$ des deux côtés.", "Une fois que tu as $3x = 12$, trouve $x$."], f: "Opérations inverses" },
      { lvl: 2, q: "$5x + 5 = 30$", a: "$x = 5$", steps: ["Isole le bloc des $x$ en soustrayant $5$ au résultat.", "Tu obtiens $5x = 25$. Termine le travail."], f: "Opérations inverses" },
      { lvl: 2, q: "$10 + x = 2$", a: "$x = -8$", steps: ["On cherche à isoler $x$. Il faut faire disparaître le $10$.", "Fais $2 - 10$ (attention au signe, ton résultat sera négatif)."], f: "$x = b - a$" },
      { lvl: 2, q: "$-3x = 12$", a: "$x = -4$", steps: ["Divise le nombre de droite ($12$) par le nombre attaché à $x$ ($-3$).", "Attention à la règle des signes lors de la division."], f: "Règle des signes en division" },
      { lvl: 2, q: "$4x - 1 = -9$", a: "$x = -2$", steps: ["Neutralise le $-1$ en faisant $+1$ de l'autre côté. Tu as une dette de $9$ et un gain de $1$.", "Tu obtiens $4x = -8$. Divise par $4$."], f: "Opérations inverses" },
      { lvl: 2, q: "$\\frac{x}{3} + 2 = 7$", a: "$x = 15$", steps: ["Étape 1 : Enlève le $2$. Tu obtiens $\\frac{x}{3} = 5$.", "Étape 2 : Le tiers de $x$ vaut $5$. Multiplie par $3$ pour trouver $x$ entier."], f: "Ordre des opérations inverses" },

      // NIVEAU 3 (3 exos)
      { lvl: 3, q: "$2x + 4 = x + 7$", a: "$x = 3$", steps: ["Règle d'or : regroupe les $x$ à gauche et les nombres à droite.", "Enlève $1x$ de chaque côté : l'équation devient $x + 4 = 7$.", "Termine en isolant $x$."], f: "Équations à 2 inconnues" },
      { lvl: 3, q: "$3x - 5 = x + 5$", a: "$x = 5$", steps: ["Enlève $x$ de chaque côté : $2x - 5 = 5$.", "Fais basculer le $-5$ de l'autre côté en l'ajoutant : $2x = 10$."], f: "Résolution par étapes" },
      { lvl: 3, q: "$2(x + 3) = 14$", a: "$x = 4$", steps: ["Astuce de pro : puisque tout le côté gauche est multiplié par $2$, commence par diviser tout par $2$ !", "L'équation se simplifie instantanément en $x + 3 = 7$."], f: "Simplification globale" }
    ]
  }
};