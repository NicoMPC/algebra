// ==================== 6.js - NIVEAU 6ÈME ====================
window.db = window.db || {};

window.db.ALGEBRA_6EME = {
  catDisplay: {
    DECIMAUX: "Opérations & Décimaux",
    FRACTIONS: "Sens de la Fraction",
    PROPORTIONNALITE: "Proportions & Pourcentages",
    GEOMETRIE: "Périmètres & Aires"
  },
  catIcon: {
    DECIMAUX: "🧮",
    FRACTIONS: "🍕",
    PROPORTIONNALITE: "⚖️",
    GEOMETRIE: "📏"
  },
  categories: {
    // =========================================================================
    // 1. DÉCIMAUX ET OPÉRATIONS
    // =========================================================================
    DECIMAUX: [
      // NIVEAU 1 (10 exos)
      { lvl: 1, q: "$12,4 + 3,5$", a: "$15,9$", steps: ["Aligne les virgules pour additionner."], f: "Addition de décimaux" },
      { lvl: 1, q: "$25,8 - 4,2$", a: "$21,6$", steps: ["Aligne les virgules et soustrais chiffre par chiffre."], f: "Soustraction de décimaux" },
      { lvl: 1, q: "$4,5 \\times 10$", a: "$45$", steps: ["Multiplier par 10 décale la virgule d'un rang vers la droite."], f: "$\\times 10$" },
      { lvl: 1, q: "$3,14 \\times 100$", a: "$314$", steps: ["Multiplier par 100 décale la virgule de deux rangs vers la droite."], f: "$\\times 100$" },
      { lvl: 1, q: "$125 \\div 10$", a: "$12,5$", steps: ["Diviser par 10 décale la virgule d'un rang vers la gauche."], f: "$\\div 10$" },
      { lvl: 1, q: "$7,2 + 0,8$", a: "$8,0 = 8$", steps: ["Compléments à l'unité : 2 dixièmes + 8 dixièmes = 1 unité."], f: "Calcul mental" },
      { lvl: 1, q: "$10 - 2,5$", a: "$7,5$", steps: ["Pense à la monnaie : 10€ - 2,50€."], f: "Complément" },
      { lvl: 1, q: "$3 \\times 0,5$", a: "$1,5$", steps: ["Multiplier par 0,5 revient à prendre la moitié."], f: "$\\times 0,5 = \\div 2$" },
      { lvl: 1, q: "$14,2 \\times 1000$", a: "$14200$", steps: ["Rajoute des zéros si besoin pour décaler de 3 rangs."], f: "$\\times 1000$" },
      { lvl: 1, q: "$0,4 \\times 2$", a: "$0,8$", steps: ["Le double de 4 dixièmes est 8 dixièmes."], f: "Multiplication simple" },

      // NIVEAU 2 (7 exos)
      { lvl: 2, q: "$12,5 \\times 4$", a: "$50$", steps: ["Astuce : multiplie par 2, puis encore par 2.", "Double de 12,5 = 25. Double de 25 = 50."], f: "$\\times 4$" },
      { lvl: 2, q: "$4,2 \\times 0,1$", a: "$0,42$", steps: ["Multiplier par 0,1 revient à diviser par 10."], f: "$\\times 0,1 = \\div 10$" },
      { lvl: 2, q: "$15 \\div 0,5$", a: "$30$", steps: ["Diviser par 0,5 revient à multiplier par 2.", "Combien de demis dans 15 ? Il y en a 30."], f: "$\\div 0,5 = \\times 2$" },
      { lvl: 2, q: "$2,5 \\times 3,4$", a: "$8,5$", steps: ["Pose la multiplication sans les virgules ($25 \\times 34 = 850$).", "Place la virgule (2 chiffres après la virgule au total)."], f: "Produit de décimaux" },
      { lvl: 2, q: "$100 - 34,7$", a: "$65,3$", steps: ["Fais $100 - 34 = 66$, puis enlève encore $0,7$."], f: "Soustraction mentale" },
      { lvl: 2, q: "$(4 + 6) \\times 2,5$", a: "$25$", steps: ["Priorité aux parenthèses : $10 \\times 2,5$."], f: "Priorités" },
      { lvl: 2, q: "$1,2 \\times 1,2$", a: "$1,44$", steps: ["Comme $12 \\times 12 = 144$, avec deux chiffres après la virgule."], f: "Carré parfait décimal" },

      // NIVEAU 3 (3 exos)
      { lvl: 3, q: "$0,05 \\times 0,08$", a: "$0,004$", steps: ["$5 \\times 8 = 40$.", "Il y a $2+2=4$ chiffres après la virgule au total. $0,0040$."], f: "Zéros multiples" },
      { lvl: 3, q: "$\\frac{13,5}{0,5}$", a: "$27$", steps: ["Diviser par 0,5 c'est multiplier par 2.", "$13,5 \\times 2 = 27$."], f: "Quotient décimal" },
      { lvl: 3, q: "$12,34 \\times 99$", a: "$1221,66$", steps: ["Astuce : $99 = 100 - 1$.", "$1234 - 12,34$."], f: "Distributivité mentale" }
    ],

    // =========================================================================
    // 2. FRACTIONS (Lecture, Partage et Égalités)
    // =========================================================================
    FRACTIONS: [
      // NIVEAU 1 (10 exos)
      { lvl: 1, q: "Le tiers de $12$", a: "$4$", steps: ["Divise par le dénominateur : $12 \\div 3 = 4$."], f: "Fraction de quantité" },
      { lvl: 1, q: "Le quart de $20$", a: "$5$", steps: ["$20 \\div 4 = 5$."], f: "Fraction de quantité" },
      { lvl: 1, q: "La moitié de $50$", a: "$25$", steps: ["$50 \\div 2$."], f: "Fraction de quantité" },
      { lvl: 1, q: "Compléter : $\\frac{1}{2} = \\frac{?}{4}$", a: "$2$", steps: ["On a multiplié le bas par 2, on fait pareil en haut.", "$1 \\times 2 = 2$."], f: "Fractions égales" },
      { lvl: 1, q: "Compléter : $\\frac{1}{3} = \\frac{2}{?}$", a: "$6$", steps: ["On a multiplié le haut par 2, on fait pareil en bas.", "$3 \\times 2 = 6$."], f: "Fractions égales" },
      { lvl: 1, q: "Valeur décimale de $\\frac{1}{2}$", a: "$0,5$", steps: ["1 divisé par 2."], f: "Passage fraction / décimal" },
      { lvl: 1, q: "Valeur décimale de $\\frac{1}{4}$", a: "$0,25$", steps: ["La moitié de la moitié."], f: "Passage fraction / décimal" },
      { lvl: 1, q: "$\\frac{5}{5}$", a: "$1$", steps: ["Si on prend toutes les parts d'un gâteau, on a 1 gâteau entier."], f: "$\\frac{a}{a} = 1$" },
      { lvl: 1, q: "Calculer $\\frac{3}{4}$ de $12$", a: "$9$", steps: ["Le quart est 3 ($12 \\div 4$). On en prend trois : $3 \\times 3 = 9$."], f: "Fraction appliquée" },
      { lvl: 1, q: "Valeur décimale de $\\frac{3}{4}$", a: "$0,75$", steps: ["$3 \\times 0,25 = 0,75$."], f: "Fraction usuelle" },

      // NIVEAU 2 (7 exos)
      { lvl: 2, q: "Compléter : $\\frac{2}{5} = \\frac{?}{15}$", a: "$6$", steps: ["On multiplie par 3 en haut et en bas.", "$2 \\times 3 = 6$."], f: "Amplification" },
      { lvl: 2, q: "Simplifier $\\frac{10}{15}$", a: "$\\frac{2}{3}$", steps: ["Les deux nombres sont dans la table de 5.", "Divise en haut et en bas par 5."], f: "Simplification" },
      { lvl: 2, q: "Calculer $\\frac{2}{3}$ de $30$", a: "$20$", steps: ["Divise par 3 ($30/3 = 10$), puis multiplie par 2 ($10 \\times 2$)."], f: "Fraction de quantité" },
      { lvl: 2, q: "Valeur décimale de $\\frac{1}{10}$", a: "$0,1$", steps: ["Un dixième s'écrit avec 1 chiffre après la virgule."], f: "Fraction décimale" },
      { lvl: 2, q: "Valeur de $\\frac{45}{100}$", a: "$0,45$", steps: ["Quarante-cinq centièmes = 2 chiffres après la virgule."], f: "Fraction décimale" },
      { lvl: 2, q: "Mettre $1,5$ en fraction", a: "$\\frac{3}{2}$", steps: ["$1,5$ c'est un gâteau et demi.", "Soit 3 moitiés : $\\frac{3}{2}$."], f: "Décimal vers fraction" },
      { lvl: 2, q: "Simplifier $\\frac{8}{12}$", a: "$\\frac{2}{3}$", steps: ["Divise par 4 en haut et en bas."], f: "Simplification" },

      // NIVEAU 3 (3 exos)
      { lvl: 3, q: "Mettre $\\frac{2}{3}$ et $\\frac{1}{6}$ au même dénominateur", a: "$\\frac{4}{6}$ et $\\frac{1}{6}$", steps: ["Multiplie $\\frac{2}{3}$ par 2 en haut et en bas pour avoir des sixièmes."], f: "Dénominateur commun" },
      { lvl: 3, q: "$\\frac{7}{4}$ en nombre entier + fraction", a: "$1 + \\frac{3}{4}$", steps: ["Dans $7$, il y a une fois $4$, et il reste $3$.", "Donc $\\frac{4}{4} + \\frac{3}{4}$."], f: "Décomposition" },
      { lvl: 3, q: "Simplifier $\\frac{24}{36}$", a: "$\\frac{2}{3}$", steps: ["Divise directement par 12, ou par 2 puis par 6..."], f: "Simplification maximum" }
    ],

    // =========================================================================
    // 3. PROPORTIONNALITÉ ET POURCENTAGES
    // =========================================================================
    PROPORTIONNALITE: [
      // NIVEAU 1 (10 exos)
      { lvl: 1, q: "10% de $50$", a: "$5$", steps: ["Prendre 10%, c'est diviser par 10."], f: "$\\div 10$" },
      { lvl: 1, q: "50% de $80$", a: "$40$", steps: ["Prendre 50%, c'est prendre la moitié."], f: "$\\div 2$" },
      { lvl: 1, q: "Si 2kg coûtent 4€, combien coûtent 3kg ?", a: "$6$€", steps: ["Passage à l'unité : 1kg coûte 2€.", "Donc 3kg coûtent $3 \\times 2 = 6$€."], f: "Retour à l'unité" },
      { lvl: 1, q: "10% de $120$", a: "$12$", steps: ["Divise par 10."], f: "$\\div 10$" },
      { lvl: 1, q: "25% de $40$", a: "$10$", steps: ["Prendre 25%, c'est diviser par 4 (le quart)."], f: "$\\div 4$" },
      { lvl: 1, q: "Si 5 stylos coûtent 10€, 1 stylo coûte ?", a: "$2$€", steps: ["$10 \\div 5 = 2$."], f: "Retour à l'unité" },
      { lvl: 1, q: "Si 3 tickets = 9€, 6 tickets = ?", a: "$18$€", steps: ["C'est le double de tickets, donc le double du prix.", "$9 \\times 2$."], f: "Multiplicateur" },
      { lvl: 1, q: "100% de $45$", a: "$45$", steps: ["100% représente la totalité."], f: "Totalité" },
      { lvl: 1, q: "20% de $50$", a: "$10$", steps: ["Astuce : calcule 10% (c'est 5) et double le résultat."], f: "Décomposition" },
      { lvl: 1, q: "Quelle fraction représente 50% ?", a: "$\\frac{1}{2}$", steps: ["La moitié de 100."], f: "Pourcentage usuel" },

      // NIVEAU 2 (7 exos)
      { lvl: 2, q: "75% de $40$", a: "$30$", steps: ["75% c'est les trois quarts.", "Un quart = 10. Trois quarts = 30."], f: "$\\frac{3}{4}$" },
      { lvl: 2, q: "5% de $60$", a: "$3$", steps: ["Calcule 10% (c'est 6), et prends la moitié pour avoir 5%."], f: "Moitié de 10%" },
      { lvl: 2, q: "Si 4h de vélo font 60km, 2h font ?", a: "$30$ km", steps: ["La moitié du temps = la moitié de la distance."], f: "Division proportionnelle" },
      { lvl: 2, q: "30% de $50$", a: "$15$", steps: ["10% = 5. Donc 30% = $3 \\times 5 = 15$."], f: "Proportion" },
      { lvl: 2, q: "Fraction pour 25%", a: "$\\frac{1}{4}$", steps: ["C'est le quart de 100."], f: "Pourcentage usuel" },
      { lvl: 2, q: "Un article à 40€ est soldé -20%. Prix final ?", a: "$32$€", steps: ["Réduction : 20% de 40€ = 8€.", "Nouveau prix : $40 - 8 = 32$."], f: "Application d'une remise" },
      { lvl: 2, q: "Si 1,5kg = 3€, alors 3kg = ?", a: "$6$€", steps: ["3kg c'est le double de 1,5kg. Double le prix."], f: "Doublement" },

      // NIVEAU 3 (3 exos)
      { lvl: 3, q: "Un article à 50€ augmente de 10%. Prix final ?", a: "$55$€", steps: ["Augmentation : 10% de 50 = 5.", "$50 + 5 = 55$."], f: "Hausse" },
      { lvl: 3, q: "15% de $200$", a: "$30$", steps: ["10% = 20. Et 5% = 10.", "$20 + 10 = 30$."], f: "Additivité" },
      { lvl: 3, q: "Vitesse : 120 km/h. Distance en 30 min ?", a: "$60$ km", steps: ["30 min = une demi-heure.", "Prends la moitié de 120."], f: "Vitesse constante" }
    ],

    // =========================================================================
    // 4. GÉOMÉTRIE (Périmètres et Aires)
    // =========================================================================
    GEOMETRIE: [
      // NIVEAU 1 (10 exos)
      { lvl: 1, q: "Périmètre carré, côté $4$", a: "$16$", steps: ["Le périmètre est le tour.", "$4 + 4 + 4 + 4 = 16$."], f: "$P = 4 \\times c$" },
      { lvl: 1, q: "Aire d'un carré, côté $4$", a: "$16$", steps: ["L'aire est la surface intérieure.", "$4 \\times 4 = 16$."], f: "$A = c \\times c$" },
      { lvl: 1, q: "Périmètre rectangle $L=5, l=3$", a: "$16$", steps: ["$2 \\times (5 + 3) = 2 \\times 8 = 16$."], f: "$P = 2(L + l)$" },
      { lvl: 1, q: "Aire rectangle $L=5, l=3$", a: "$15$", steps: ["Longueur multipliée par largeur.", "$5 \\times 3 = 15$."], f: "$A = L \\times l$" },
      { lvl: 1, q: "Périmètre carré, côté $10$", a: "$40$", steps: ["$4 \\times 10 = 40$."], f: "$P = 4c$" },
      { lvl: 1, q: "Aire carré, côté $10$", a: "$100$", steps: ["$10 \\times 10 = 100$."], f: "$A = c^2$" },
      { lvl: 1, q: "Formule de la longueur (périmètre) d'un cercle", a: "$2 \\times \\pi \\times r$", steps: ["Le rayon multiplié par 2pi."], f: "$P = 2 \\pi r$" },
      { lvl: 1, q: "Si le diamètre est $10$, le rayon est ?", a: "$5$", steps: ["Le rayon est la moitié du diamètre."], f: "$r = \\frac{D}{2}$" },
      { lvl: 1, q: "Aire rectangle $L=10, l=2,5$", a: "$25$", steps: ["$10 \\times 2,5 = 25$."], f: "$A = L \\times l$" },
      { lvl: 1, q: "Périmètre triangle équilatéral, côté $6$", a: "$18$", steps: ["Trois côtés égaux : $3 \\times 6 = 18$."], f: "$P = 3c$" },

      // NIVEAU 2 (7 exos)
      { lvl: 2, q: "Un carré a pour périmètre $20$. Son côté ?", a: "$5$", steps: ["On divise le périmètre par 4.", "$20 \\div 4 = 5$."], f: "$c = \\frac{P}{4}$" },
      { lvl: 2, q: "Un rectangle d'aire $24$ a $L=6$. Sa largeur $l$ ?", a: "$4$", steps: ["On cherche le nombre qui multiplié par 6 fait 24.", "$24 \\div 6 = 4$."], f: "$l = \\frac{A}{L}$" },
      { lvl: 2, q: "Formule de l'aire d'un disque", a: "$\\pi \\times r^2$", steps: ["Pi multiplié par le rayon au carré."], f: "$A = \\pi r^2$" },
      { lvl: 2, q: "Périmètre rectangle $L=4,5, l=2,5$", a: "$14$", steps: ["Demi-périmètre : $4,5 + 2,5 = 7$.", "Total : $7 \\times 2 = 14$."], f: "$P = 2(L+l)$" },
      { lvl: 2, q: "Aire d'un triangle rectangle (côtés droits $3$ et $4$)", a: "$6$", steps: ["C'est la moitié de l'aire d'un rectangle.", "$(3 \\times 4) \\div 2 = 6$."], f: "$A = \\frac{base \\times hauteur}{2}$" },
      { lvl: 2, q: "Un carré a une aire de $25$. Son périmètre ?", a: "$20$", steps: ["Si l'aire est 25, son côté est 5.", "Son périmètre est $4 \\times 5 = 20$."], f: "Déduction croisée" },
      { lvl: 2, q: "Longueur cercle rayon $5$ (en fonction de $\\pi$)", a: "$10\\pi$", steps: ["$2 \\times \\pi \\times 5 = 10\\pi$."], f: "$P = 2\\pi r$" },

      // NIVEAU 3 (3 exos)
      { lvl: 3, q: "Aire disque de rayon $3$ (en fonction de $\\pi$)", a: "$9\\pi$", steps: ["$\\pi \\times 3^2 = 9\\pi$."], f: "$A = \\pi r^2$" },
      { lvl: 3, q: "Un rectangle a un périmètre de $18$ et $L=6$. Son aire ?", a: "$18$", steps: ["1. Demi-périmètre = 9.", "2. $l = 9 - 6 = 3$.", "3. Aire = $6 \\times 3 = 18$."], f: "Problème à étapes" },
      { lvl: 3, q: "Aire d'un triangle de base $10$ et hauteur $5$", a: "$25$", steps: ["Formule : $(\\text{Base} \\times \\text{Hauteur}) \\div 2$.", "$(10 \\times 5) \\div 2 = 25$."], f: "$A = \\frac{b \\times h}{2}$" }
    ]
  }
};