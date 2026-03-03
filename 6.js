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
      { lvl: 1, q: "$12,4 + 3,5$", a: "$15,9$", steps: ["Aligne mentalement les virgules.", "Ajoute les dixièmes ensemble ($4+5$), puis les unités ($12+3$)."], f: "Addition de décimaux" },
      { lvl: 1, q: "$25,8 - 4,2$", a: "$21,6$", steps: ["Attention à bien aligner les virgules.", "Soustrais d'abord les dixièmes ($8-2$), puis les unités ($25-4$)."], f: "Soustraction de décimaux" },
      { lvl: 1, q: "$4,5 \\times 10$", a: "$45$", steps: ["Multiplier par $10$ agrandit le nombre d'un ordre de grandeur.", "Vers quelle direction dois-tu décaler la virgule pour que le nombre devienne plus grand ?"], f: "$\\times 10$" },
      { lvl: 1, q: "$3,14 \\times 100$", a: "$314$", steps: ["Le nombre $100$ possède deux zéros.", "Décalle la virgule de deux rangs vers la droite pour agrandir le nombre."], f: "$\\times 100$" },
      { lvl: 1, q: "$125 \\div 10$", a: "$12,5$", steps: ["Diviser par $10$ rend le nombre dix fois plus petit.", "Imagine une virgule cachée à la fin de $125$ et décale-la d'un rang vers la gauche."], f: "$\\div 10$" },
      { lvl: 1, q: "$7,2 + 0,8$", a: "$8$", steps: ["Observe les dixièmes : $2$ dixièmes + $8$ dixièmes forment $10$ dixièmes.", "$10$ dixièmes, c'est exactement $1$ unité entière. Ajoute-la à tes $7$ unités."], f: "Complément à l'unité" },
      { lvl: 1, q: "$10 - 2,5$", a: "$7,5$", steps: ["Pense à la monnaie : tu donnes un billet de $10$ € pour un achat de $2,50$ €.", "Combien manque-t-il pour aller de $2,5$ à $3$ ? Puis de $3$ à $10$ ?"], f: "Complément" },
      { lvl: 1, q: "$3 \\times 0,5$", a: "$1,5$", steps: ["Multiplier par $0,5$, c'est exactement la même chose que de prendre la moitié d'un nombre.", "Quelle est la moitié de $3$ ?"], f: "$\\times 0,5 = \\div 2$" },
      { lvl: 1, q: "$14,2 \\times 1000$", a: "$14200$", steps: ["Tu dois décaler la virgule de $3$ rangs vers la droite pour agrandir le nombre.", "Rajoute des zéros imaginaires à droite du $2$ pour pouvoir faire tes trois sauts !"], f: "$\\times 1000$" },
      { lvl: 1, q: "$0,4 \\times 2$", a: "$0,8$", steps: ["Tu as $4$ dixièmes. Si tu en prends le double, combien de dixièmes obtiens-tu ?"], f: "Le double d'un décimal" },

      // NIVEAU 2 (7 exos)
      { lvl: 2, q: "$12,5 \\times 4$", a: "$50$", steps: ["Astuce de calcul mental : multiplier par $4$ revient à doubler, puis doubler encore.", "Quel est le double de $12,5$ ?", "Maintenant, calcule le double de ce résultat !"], f: "$\\times 4$" },
      { lvl: 2, q: "$4,2 \\times 0,1$", a: "$0,42$", steps: ["Multiplier par un dixième ($0,1$) rend le nombre dix fois plus petit.", "Cela revient à diviser ton nombre par $10$."], f: "$\\times 0,1 = \\div 10$" },
      { lvl: 2, q: "$15 \\div 0,5$", a: "$30$", steps: ["Combien y a-t-il de moitiés ($0,5$) dans $1$ unité entière ? Il y en a $2$.", "Diviser par $0,5$ revient donc à multiplier ton nombre par $2$ !"], f: "$\\div 0,5 = \\times 2$" },
      { lvl: 2, q: "$2,5 \\times 3,4$", a: "$8,5$", steps: ["Pose mentalement la multiplication sans te soucier des virgules : $25 \\times 34 = 850$.", "Il y a un chiffre après la virgule dans $2,5$ et un dans $3,4$.", "Tu dois donc placer la virgule pour avoir $2$ chiffres après la virgule dans ton résultat ($850$)."], f: "Produit de décimaux" },
      { lvl: 2, q: "$100 - 34,7$", a: "$65,3$", steps: ["Soustrais d'abord la partie entière : $100 - 34 = 66$.", "Maintenant, enlève encore les $0,7$ restants de ces $66$."], f: "Soustraction mentale" },
      { lvl: 2, q: "$(4 + 6) \\times 2,5$", a: "$25$", steps: ["Les parenthèses sont la priorité absolue ! Calcule d'abord $4 + 6$.", "Multiplie ensuite ce résultat par $2,5$. (Rappelle-toi l'effet d'une multiplication par $10$)."], f: "Priorités opératoires" },
      { lvl: 2, q: "$1,2 \\times 1,2$", a: "$1,44$", steps: ["Si tu ignores les virgules temporairement, tu dois calculer $12 \\times 12$.", "Le résultat est $144$. Replace maintenant la virgule pour avoir $2$ chiffres décimaux au total."], f: "Carré parfait décimal" },

      // NIVEAU 3 (3 exos)
      { lvl: 3, q: "$0,05 \\times 0,08$", a: "$0,004$", steps: ["Multiplie d'abord les chiffres non nuls : $5 \\times 8 = 40$.", "Compte le nombre total de chiffres après la virgule dans $0,05$ et $0,08$. Il y en a $4$.", "Place la virgule dans $40$ pour avoir exactement $4$ chiffres décimaux."], f: "Zéros multiples" },
      { lvl: 3, q: "$\\frac{13,5}{0,5}$", a: "$27$", steps: ["Une fraction est une division. Diviser par $0,5$, c'est chercher combien de moitiés rentrent dans le nombre.", "Cela revient exactement à multiplier le numérateur par $2$ !"], f: "Quotient décimal" },
      { lvl: 3, q: "$12,34 \\times 99$", a: "$1221,66$", steps: ["Astuce de ninja : $99$ c'est proche de $100$. Remplace $99$ par $(100 - 1)$.", "Calcule d'abord $12,34 \\times 100$.", "À ce résultat, soustrais une fois $12,34$."], f: "Distributivité mentale" }
    ],

    // =========================================================================
    // 2. FRACTIONS (Lecture, Partage et Égalités)
    // =========================================================================
    FRACTIONS: [
      // NIVEAU 1 (10 exos)
      { lvl: 1, q: "Le tiers de $12$", a: "$4$", steps: ["Prendre le tiers, c'est partager équitablement en $3$ parts égales.", "Calcule $12 \\div 3$."], f: "Fraction d'une quantité" },
      { lvl: 1, q: "Le quart de $20$", a: "$5$", steps: ["Prendre le quart, c'est diviser par $4$.", "Quel nombre multiplié par $4$ donne $20$ ?"], f: "Fraction d'une quantité" },
      { lvl: 1, q: "La moitié de $50$", a: "$25$", steps: ["Prendre la moitié, c'est diviser par $2$."], f: "Fraction d'une quantité" },
      { lvl: 1, q: "Compléter : $\\frac{1}{2} = \\frac{?}{4}$", a: "$2$", steps: ["Comment passe-t-on de $2$ à $4$ au dénominateur (en bas) ?", "On a multiplié par $2$. Fais la même opération au numérateur (en haut) !"], f: "Fractions égales" },
      { lvl: 1, q: "Compléter : $\\frac{1}{3} = \\frac{2}{?}$", a: "$6$", steps: ["Comment passe-t-on de $1$ à $2$ au numérateur (en haut) ?", "On a multiplié par $2$. Applique la même règle au dénominateur (en bas)."], f: "Fractions égales" },
      { lvl: 1, q: "Valeur décimale de $\\frac{1}{2}$", a: "$0,5$", steps: ["La barre de fraction signifie 'divisé par'.", "Calcule $1 \\div 2$."], f: "Passage fraction / décimal" },
      { lvl: 1, q: "Valeur décimale de $\\frac{1}{4}$", a: "$0,25$", steps: ["Le quart, c'est la moitié de la moitié.", "Quelle est la moitié de $0,50$ ?"], f: "Passage fraction / décimal" },
      { lvl: 1, q: "Calculer $\\frac{5}{5}$", a: "$1$", steps: ["Si tu coupes une pizza en $5$ parts et que tu manges les $5$ parts...", "Tu as mangé la pizza toute entière !"], f: "$\\frac{a}{a} = 1$" },
      { lvl: 1, q: "Calculer les $\\frac{3}{4}$ de $12$", a: "$9$", steps: ["Commence par trouver le quart de $12$ (divise par $4$).", "Maintenant que tu as la valeur d'un quart, multiplie-la par $3$ pour obtenir les trois quarts."], f: "Prendre une fraction d'un nombre" },
      { lvl: 1, q: "Valeur décimale de $\\frac{3}{4}$", a: "$0,75$", steps: ["Tu sais déjà que $\\frac{1}{4} = 0,25$.", "Multiplie cette valeur par $3$."], f: "Fraction usuelle" },

      // NIVEAU 2 (7 exos)
      { lvl: 2, q: "Compléter : $\\frac{2}{5} = \\frac{?}{15}$", a: "$6$", steps: ["Quel multiplicateur permet de passer de $5$ à $15$ en bas ?", "Multiplie le chiffre du haut ($2$) par ce même nombre."], f: "Amplification de fraction" },
      { lvl: 2, q: "Simplifier $\\frac{10}{15}$", a: "$\\frac{2}{3}$", steps: ["Cherche une table de multiplication commune à $10$ et $15$.", "Ils se terminent par $0$ et $5$, donc divise le haut et le bas par $5$."], f: "Simplification" },
      { lvl: 2, q: "Calculer les $\\frac{2}{3}$ de $30$", a: "$20$", steps: ["Trouve d'abord la valeur d'un tiers en divisant $30$ par $3$.", "Prends ensuite ce résultat et multiplie-le par $2$."], f: "Fraction d'une quantité" },
      { lvl: 2, q: "Valeur décimale de $\\frac{1}{10}$", a: "$0,1$", steps: ["Un dixième s'écrit avec un seul chiffre après la virgule."], f: "Fraction décimale" },
      { lvl: 2, q: "Valeur décimale de $\\frac{45}{100}$", a: "$0,45$", steps: ["Quarante-cinq centièmes s'écrit avec deux chiffres après la virgule."], f: "Fraction décimale" },
      { lvl: 2, q: "Mettre $1,5$ sous forme de fraction", a: "$\\frac{3}{2}$", steps: ["$1,5$ représente $1$ unité complète et une moitié.", "Combien cela fait-il de moitiés (de demis) en tout ?"], f: "Décimal vers fraction" },
      { lvl: 2, q: "Simplifier $\\frac{8}{12}$", a: "$\\frac{2}{3}$", steps: ["Tu peux diviser par $2$, puis encore par $2$.", "Ou être plus rapide en trouvant la plus grande table commune à $8$ et $12$ (la table de $4$)."], f: "Simplification" },

      // NIVEAU 3 (3 exos)
      { lvl: 3, q: "Mettre $\\frac{2}{3}$ et $\\frac{1}{6}$ au même dénominateur", a: "$\\frac{4}{6}$ et $\\frac{1}{6}$", steps: ["L'objectif est d'avoir le même chiffre en bas.", "Multiplie le haut et le bas de la première fraction par $2$ pour la transformer en sixièmes."], f: "Dénominateur commun" },
      { lvl: 3, q: "Décomposer $\\frac{7}{4}$ en un entier + une fraction", a: "$1 + \\frac{3}{4}$", steps: ["Dans $7$ quarts, combien peux-tu faire d'unités entières ($4$ quarts) ?", "Il y a une unité entière ($\\frac{4}{4}$), combien de quarts reste-t-il ?"], f: "Décomposition d'une fraction" },
      { lvl: 3, q: "Simplifier au maximum $\\frac{24}{36}$", a: "$\\frac{2}{3}$", steps: ["Trouve le plus grand diviseur commun à $24$ et $36$.", "Si c'est difficile, divise par $2$, puis par $2$, puis par $3$ successivement !"], f: "Fraction irréductible" }
    ],

    // =========================================================================
    // 3. PROPORTIONNALITÉ ET POURCENTAGES
    // =========================================================================
    PROPORTIONNALITE: [
      // NIVEAU 1 (10 exos)
      { lvl: 1, q: "Calculer $10 \\%$ de $50$", a: "$5$", steps: ["Prendre $10 \\%$ d'une quantité, c'est tout simplement la diviser par $10$."], f: "$10 \\% = \\div 10$" },
      { lvl: 1, q: "Calculer $50 \\%$ de $80$", a: "$40$", steps: ["Prendre $50 \\%$, c'est exactement la même chose que prendre la moitié."], f: "$50 \\% = \\div 2$" },
      { lvl: 1, q: "Si $2$ kg coûtent $4$ €, combien coûtent $3$ kg ?", a: "$6$ €", steps: ["Trouve d'abord le prix pour $1$ kg (la moitié de $4$ €).", "Maintenant que tu as le prix d'un kilo, multiplie-le par $3$ !"], f: "Passage à l'unité" },
      { lvl: 1, q: "Calculer $10 \\%$ de $120$", a: "$12$", steps: ["Divise le nombre par $10$ en supprimant un zéro."], f: "$10 \\% = \\div 10$" },
      { lvl: 1, q: "Calculer $25 \\%$ de $40$", a: "$10$", steps: ["Prendre $25 \\%$, c'est prendre le quart.", "Divise $40$ par $4$."], f: "$25 \\% = \\div 4$" },
      { lvl: 1, q: "Si $5$ stylos coûtent $10$ €, $1$ stylo coûte ?", a: "$2$ €", steps: ["Divise le prix total par le nombre de stylos."], f: "Passage à l'unité" },
      { lvl: 1, q: "Si $3$ tickets coûtent $9$ €, combien coûtent $6$ tickets ?", a: "$18$ €", steps: ["Observe bien : $6$ tickets, c'est le double de $3$ tickets.", "Le prix sera donc simplement le double !"], f: "Propriété multiplicative" },
      { lvl: 1, q: "Calculer $100 \\%$ de $45$", a: "$45$", steps: ["$100 \\%$ représente la totalité du nombre."], f: "Totalité" },
      { lvl: 1, q: "Calculer $20 \\%$ de $50$", a: "$10$", steps: ["Astuce : calcule d'abord $10 \\%$ de $50$ (divise par $10$).", "$20 \\%$, c'est le double de $10 \\%$. Double ton résultat !"], f: "Décomposition des pourcentages" },
      { lvl: 1, q: "Quelle fraction représente $50 \\%$ ?", a: "$\\frac{1}{2}$", steps: ["$50 \\%$ représente la moitié d'un objet.", "Comment écrit-on \"un demi\" en fraction ?"], f: "Pourcentage usuel" },

      // NIVEAU 2 (7 exos)
      { lvl: 2, q: "Calculer $75 \\%$ de $40$", a: "$30$", steps: ["$75 \\%$ correspond aux trois quarts de la quantité.", "Trouve d'abord le quart de $40$, puis multiplie par $3$."], f: "$75 \\% = \\frac{3}{4}$" },
      { lvl: 2, q: "Calculer $5 \\%$ de $60$", a: "$3$", steps: ["Calcule $10 \\%$ de $60$ en divisant par $10$.", "Puisque $5 \\%$ est la moitié de $10 \\%$, prends la moitié de ton résultat !"], f: "Déduction par moitié" },
      { lvl: 2, q: "Si on parcourt $60$ km en $4$h à vélo, quelle distance en $2$h ?", a: "$30$ km", steps: ["La vitesse est constante. Le temps de trajet a été divisé par $2$.", "Fais de même avec la distance."], f: "Proportionnalité directe" },
      { lvl: 2, q: "Calculer $30 \\%$ de $50$", a: "$15$", steps: ["Calcule d'abord $10 \\%$ de $50$.", "Multiplie ensuite ce résultat par $3$."], f: "Méthode des $10 \\%$" },
      { lvl: 2, q: "Quelle fraction représente $25 \\%$ ?", a: "$\\frac{1}{4}$", steps: ["Si tu partages $100 \\%$ en $4$ parts égales, tu obtiens $25 \\%$.", "C'est donc un... ?"], f: "Pourcentage usuel" },
      { lvl: 2, q: "Un article à $40$ € est soldé de $-20 \\%$. Quel est son nouveau prix ?", a: "$32$ €", steps: ["Étape 1 : Calcule la réduction ($20 \\%$ de $40$ €). Utilise la méthode des $10 \\%$ !", "Étape 2 : Soustrais cette réduction du prix de départ."], f: "Application d'une remise" },
      { lvl: 2, q: "Si $1,5$ kg coûtent $3$ €, combien coûtent $3$ kg ?", a: "$6$ €", steps: ["Remarque le lien entre les poids : $3$ kg, c'est le double de $1,5$ kg.", "Applique cette même relation au prix."], f: "Règle du double" },

      // NIVEAU 3 (3 exos)
      { lvl: 3, q: "Un article à $50$ € augmente de $10 \\%$. Quel est son nouveau prix ?", a: "$55$ €", steps: ["Calcule l'augmentation : $10 \\%$ de $50$ €.", "Ajoute cette augmentation au prix de départ."], f: "Hausse de prix" },
      { lvl: 3, q: "Calculer $15 \\%$ de $200$", a: "$30$", steps: ["Décompose : $15 \\% = 10 \\% + 5 \\%$.", "Calcule $10 \\%$ de $200$.", "Calcule $5 \\%$ de $200$ (c'est la moitié de l'étape précédente) et additionne les deux !"], f: "Additivité des pourcentages" },
      { lvl: 3, q: "Vitesse : $120$ km/h. Quelle distance est parcourue en $30$ min ?", a: "$60$ km", steps: ["$120$ km/h signifie $120$ km en $1$ heure entière ($60$ min).", "$30$ minutes, c'est une demi-heure. Quelle distance parcourt-on en une demi-heure ?"], f: "Vitesse et durée" }
    ],

    // =========================================================================
    // 4. GÉOMÉTRIE (Périmètres et Aires)
    // =========================================================================
    GEOMETRIE: [
      // NIVEAU 1 (10 exos)
      { lvl: 1, q: "Périmètre d'un carré de côté $4$ cm", a: "$16$ cm", steps: ["Le périmètre est la longueur du tour de la figure.", "Un carré a $4$ côtés de même longueur. Calcule $4 + 4 + 4 + 4$."], f: "$P = 4 \\times c$" },
      { lvl: 1, q: "Aire d'un carré de côté $4$ cm", a: "$16$ cm²", steps: ["L'aire mesure la surface intérieure de la figure.", "Multiplie le côté par lui-même."], f: "$A = c \\times c$" },
      { lvl: 1, q: "Périmètre d'un rectangle de longueur $L=5$ et largeur $l=3$", a: "$16$", steps: ["Calcule le demi-périmètre : Longueur + largeur.", "Double ce résultat pour avoir le tour complet !"], f: "$P = 2 \\times (L + l)$" },
      { lvl: 1, q: "Aire d'un rectangle de longueur $L=5$ et largeur $l=3$", a: "$15$", steps: ["Pour trouver l'aire, multiplie simplement la longueur par la largeur."], f: "$A = L \\times l$" },
      { lvl: 1, q: "Périmètre d'un carré de côté $10$", a: "$40$", steps: ["Multiplie le côté par le nombre de côtés d'un carré."], f: "$P = 4 \\times c$" },
      { lvl: 1, q: "Aire d'un carré de côté $10$", a: "$100$", steps: ["L'aire est le côté multiplié par lui-même."], f: "$A = c^2$" },
      { lvl: 1, q: "Quelle est la formule de la longueur (périmètre) d'un cercle ?", a: "$2 \\times \\pi \\times r$", steps: ["Le périmètre fait intervenir le rayon ($r$), le nombre $\\pi$ et le chiffre $2$.", "Le produit de ces trois éléments te donne le tour du cercle."], f: "$P = 2 \\pi r$" },
      { lvl: 1, q: "Si le diamètre d'un cercle est $10$, que vaut son rayon ?", a: "$5$", steps: ["Le rayon part du centre jusqu'au bord, c'est exactement la moitié du diamètre."], f: "$r = D \\div 2$" },
      { lvl: 1, q: "Aire d'un rectangle avec $L=10$ et $l=2,5$", a: "$25$", steps: ["Multiplie la longueur par la largeur. Rappelle-toi l'astuce de la multiplication par $10$ !"], f: "$A = L \\times l$" },
      { lvl: 1, q: "Périmètre d'un triangle équilatéral de côté $6$", a: "$18$", steps: ["\"Équilatéral\" veut dire que les $3$ côtés sont parfaitement égaux.", "Fais la somme des $3$ côtés."], f: "$P = 3 \\times c$" },

      // NIVEAU 2 (7 exos)
      { lvl: 2, q: "Un carré a pour périmètre $20$. Que vaut son côté ?", a: "$5$", steps: ["Le tour complet ($4$ côtés) fait $20$.", "Quel nombre multiplié par $4$ donne $20$ ?"], f: "$c = P \\div 4$" },
      { lvl: 2, q: "Un rectangle d'aire $24$ a une longueur $L=6$. Que vaut sa largeur $l$ ?", a: "$4$", steps: ["L'aire est Longueur $\\times$ largeur.", "Pose-toi la question : $6$ multiplié par quel nombre donne $24$ ?"], f: "$l = A \\div L$" },
      { lvl: 2, q: "Quelle est la formule de l'aire d'un disque ?", a: "$\\pi \\times r^2$", steps: ["L'aire fait intervenir le nombre $\\pi$ et le rayon ($r$) élevé au carré."], f: "$A = \\pi r^2$" },
      { lvl: 2, q: "Périmètre d'un rectangle avec $L=4,5$ et $l=2,5$", a: "$14$", steps: ["Commence par additionner la longueur et la largeur pour avoir le demi-périmètre.", "Multiplie ce résultat par $2$."], f: "$P = 2 \\times (L+l)$" },
      { lvl: 2, q: "Aire d'un triangle rectangle dont les côtés formant l'angle droit mesurent $3$ et $4$", a: "$6$", steps: ["Un triangle rectangle est exactement la moitié d'un rectangle.", "Calcule l'aire du rectangle ($3 \\times 4$), puis divise par $2$ !"], f: "$A = (b \\times h) \\div 2$" },
      { lvl: 2, q: "Un carré a une aire de $25$. Quel est son périmètre ?", a: "$20$", steps: ["Commence par trouver le côté : quel nombre multiplié par lui-même donne $25$ ?", "Maintenant que tu as la taille d'un côté, calcule le périmètre ($4 \\times$ le côté)."], f: "Côté, puis Périmètre" },
      { lvl: 2, q: "Longueur d'un cercle de rayon $5$ (donner la réponse en fonction de $\\pi$)", a: "$10\\pi$", steps: ["La formule du périmètre est $2 \\times \\pi \\times r$.", "Remplace le rayon par $5$ et calcule $2 \\times 5$ en gardant la lettre $\\pi$ à côté."], f: "$P = 2 \\pi r$" },

      // NIVEAU 3 (3 exos)
      { lvl: 3, q: "Aire d'un disque de rayon $3$ (donner la réponse en fonction de $\\pi$)", a: "$9\\pi$", steps: ["La formule est $\\pi \\times r^2$.", "Calcule le carré du rayon ($3 \\times 3$) et accole la lettre $\\pi$."], f: "$A = \\pi r^2$" },
      { lvl: 3, q: "Un rectangle a un périmètre de $18$ et une longueur $L=6$. Quelle est son aire ?", a: "$18$", steps: ["Étape 1 : Calcule le demi-périmètre en divisant $18$ par $2$.", "Étape 2 : Trouve la largeur. (Demi-périmètre - Longueur).", "Étape 3 : Calcule l'aire (Longueur $\\times$ largeur)."], f: "Problème à étapes" },
      { lvl: 3, q: "Aire d'un triangle de base $10$ et de hauteur correspondante $5$", a: "$25$", steps: ["La formule est $(\\text{Base} \\times \\text{Hauteur}) \\div 2$.", "Fais d'abord la multiplication, puis coupe en deux !"], f: "$A = \\frac{b \\times h}{2}$" }
    ]
  }
};