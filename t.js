// ==================== t.js - NIVEAU TERMINALE ====================
window.db = window.db || {};

window.db.ALGEBRA_TERMINALE = {
  catDisplay: {
    EXP_LOG: "Exponentielle & Logarithme",
    LIMITES: "Limites & Asymptotes",
    PRIMITIVES: "Primitives & Intégrales",
    COMPLEXES: "Nombres Complexes"
  },
  catIcon: {
    EXP_LOG: "📈",
    LIMITES: "🚀",
    PRIMITIVES: "∫",
    COMPLEXES: "ℂ"
  },
  categories: {
    // =========================================================================
    // 1. EXPONENTIELLE ET LOGARITHME NÉPÉRIEN
    // =========================================================================
    EXP_LOG: [
      // NIVEAU 1 (10 exos)
      { lvl: 1, q: "$e^2 \\times e^3$", a: "$e^5$", options: ["$e^5$", "$e^6$", "$e$"], steps: ["La fonction exponentielle transforme les multiplications en additions dans les exposants."], f: "$e^a \\times e^b = e^{a+b}$" },
      { lvl: 1, q: "$\\frac{e^5}{e^2}$", a: "$e^3$", options: ["$e^3$", "$e^{2,5}$", "$e^7$"], steps: ["Lors d'une division, on soustrait l'exposant du bas à celui du haut."], f: "$\\frac{e^a}{e^b} = e^{a-b}$" },
      { lvl: 1, q: "$(e^4)^2$", a: "$e^8$", options: ["$e^8$", "$e^6$", "$e^{16}$"], steps: ["Pour une puissance de puissance, on multiplie les exposants entre eux."], f: "$(e^a)^b = e^{a \\times b}$" },
      { lvl: 1, q: "$\\ln(e^3)$", a: "$3$", options: ["$3$", "$e$", "$1$"], steps: ["La fonction $\\ln$ et la fonction exponentielle sont des réciproques. Elles s'annulent mutuellement !"], f: "$\\ln(e^x) = x$" },
      { lvl: 1, q: "$e^{\\ln(5)}$", a: "$5$", options: ["$5$", "$e^5$", "$\\ln(5)$"], steps: ["L'exponentielle annule le logarithme (valable uniquement pour les nombres strictement positifs)."], f: "$e^{\\ln(x)} = x$" },
      { lvl: 1, q: "$\\ln(A \\times B)$", a: "$\\ln(A) + \\ln(B)$", options: ["$\\ln(A) + \\ln(B)$", "$\\ln(A) \\times \\ln(B)$", "$\\ln(A+B)$"], steps: ["C'est la propriété fondamentale du logarithme : il transforme les produits en sommes !"], f: "$\\ln(a \\times b) = \\ln(a) + \\ln(b)$" },
      { lvl: 1, q: "$\\ln(e)$", a: "$1$", options: ["$1$", "$0$", "$e$"], steps: ["Rappelle-toi que le nombre $e$ peut s'écrire $e^1$."], f: "$\\ln(e) = 1$" },
      { lvl: 1, q: "$\\ln(1)$", a: "$0$", options: ["$0$", "$1$", "$\\text{Impossible}$"], steps: ["Sais-tu à quelle puissance il faut élever $e$ pour obtenir $1$ ? C'est $e^0 = 1$."], f: "$\\ln(1) = 0$" },
      { lvl: 1, q: "$e^x = 1$", a: "$x = 0$", options: ["$x = 0$", "$x = 1$", "$\\text{Pas de solution}$"], steps: ["Pour 'descendre' le $x$, applique la fonction $\\ln$ des deux côtés : $\\ln(e^x) = \\ln(1)$."], f: "$e^x = 1 \\Leftrightarrow x = 0$" },
      { lvl: 1, q: "Dériver $f(x) = e^{3x}$", a: "$f'(x) = 3e^{3x}$", options: ["$f'(x) = 3e^{3x}$", "$f'(x) = e^{3x}$", "$f'(x) = 3xe^{3x}$"], steps: ["C'est une fonction composée $e^u$. La dérivée est $u' \\times e^u$."], f: "$(e^u)' = u' e^u$" },

      // NIVEAU 2 (7 exos)
      { lvl: 2, q: "Résoudre $e^{2x+1} = e^5$", a: "$x = 2$", options: ["$x = 2$", "$x = 3$", "$x = 4$"], steps: ["Puisque la fonction exponentielle est strictement croissante, si $e^A = e^B$, alors obligatoirement $A = B$.", "Résous l'équation $2x + 1 = 5$."], f: "$e^a = e^b \\Leftrightarrow a = b$" },
      { lvl: 2, q: "Résoudre $\\ln(x-2) = 0$", a: "$x = 3$", options: ["$x = 3$", "$x = 2$", "$x = 1$"], steps: ["Remplace le $0$ par une valeur connue : $0 = \\ln(1)$.", "Tu as donc $\\ln(x-2) = \\ln(1)$. L'intérieur doit être égal !"], f: "$\\ln(a) = \\ln(b) \\Leftrightarrow a=b$" },
      { lvl: 2, q: "Simplifier $\\ln(8) - \\ln(2)$", a: "$\\ln(4)$", options: ["$\\ln(4)$", "$\\ln(6)$", "$\\ln(16)$"], steps: ["La différence de deux logarithmes est égale au logarithme de leur quotient : $\\ln(\\frac{8}{2})$."], f: "$\\ln(a) - \\ln(b) = \\ln(\\frac{a}{b})$" },
      { lvl: 2, q: "Simplifier $\\ln(x^2)$", a: "$2\\ln(x)$", options: ["$2\\ln(x)$", "$\\ln(x)^2$", "$\\frac{1}{2}\\ln(x)$"], steps: ["Le logarithme a le pouvoir de faire 'tomber' l'exposant devant en tant que coefficient multiplicateur."], f: "$\\ln(x^n) = n\\ln(x)$" },
      { lvl: 2, q: "Dériver $f(x) = x e^x$", a: "$f'(x) = e^x(x+1)$", options: ["$f'(x) = e^x(x+1)$", "$f'(x) = e^x$", "$f'(x) = x e^x + 1$"], steps: ["C'est un produit $u \\times v$. Applique la formule $u'v + uv'$.", "Ici $u=x$ et $v=e^x$. Factorise toujours ton résultat final par $e^x$ !"], f: "$(uv)' = u'v + uv'$" },
      { lvl: 2, q: "Dériver $f(x) = \\ln(x^2+1)$", a: "$f'(x) = \\frac{2x}{x^2+1}$", options: ["$f'(x) = \\frac{2x}{x^2+1}$", "$f'(x) = \\frac{1}{x^2+1}$", "$f'(x) = \\frac{2x}{\\ln(x^2+1)}$"], steps: ["La dérivée d'une fonction composée $\\ln(u)$ est la fraction $\\frac{u'}{u}$."], f: "$(\\ln(u))' = \\frac{u'}{u}$" },
      { lvl: 2, q: "Résoudre $e^x > 2$", a: "$x > \\ln(2)$", options: ["$x > \\ln(2)$", "$x > 2$", "$x < \\ln(2)$"], steps: ["Applique la fonction $\\ln$ des deux côtés pour annuler l'exponentielle.", "La fonction $\\ln$ étant croissante, on ne change pas le sens de l'inégalité."], f: "$e^x > k \\Leftrightarrow x > \\ln(k)$" },

      // NIVEAU 3 (3 exos)
      { lvl: 3, q: "Résoudre $e^{2x} - 3e^x + 2 = 0$", a: "$x = 0 \\text{ ou } x = \\ln(2)$", options: ["$x = 0 \\text{ ou } x = \\ln(2)$", "$x = 1 \\text{ ou } x = 2$", "$\\text{Pas de solution}$"], steps: ["Pose un changement de variable $X = e^x$.", "L'équation devient $X^2 - 3X + 2 = 0$. Les racines sont $X=1$ et $X=2$.", "Reviens à $x$ en résolvant $e^x = 1$ et $e^x = 2$."], f: "Changement de variable" },
      { lvl: 3, q: "Résoudre $\\ln(x) + \\ln(x-1) = \\ln(2)$", a: "$x = 2$", options: ["$x = 2$", "$x = 2 \\text{ ou } x = -1$", "$x = -1$"], steps: ["Fusionne les ln à gauche : $\\ln(x(x-1)) = \\ln(2)$.", "On en déduit que $x^2 - x = 2$, soit $x^2 - x - 2 = 0$.", "Attention au piège du domaine de définition ! $x$ doit être strictement supérieur à $1$ pour que $\\ln(x-1)$ existe."], f: "Domaine de définition" },
      { lvl: 3, q: "Dériver $f(x) = \\frac{e^x}{x}$", a: "$f'(x) = \\frac{e^x(x-1)}{x^2}$", options: ["$f'(x) = \\frac{e^x(x-1)}{x^2}$", "$f'(x) = \\frac{e^x}{x^2}$", "$f'(x) = \\frac{e^x(1-x)}{x^2}$"], steps: ["Utilise la formule du quotient $\\frac{u'v - u v'}{v^2}$.", "Développe le numérateur et factorise obligatoirement par $e^x$ à la fin."], f: "$(\\frac{u}{v})' = \\frac{u'v-uv'}{v^2}$" }
    ],

    // =========================================================================
    // 2. LIMITES ET ASYMPTOTES
    // =========================================================================
    LIMITES: [
      // NIVEAU 1 (10 exos)
      { lvl: 1, q: "$\\lim_{x \\to +\\infty} x^2$", a: "$+\\infty$", options: ["$+\\infty$", "$-\\infty$", "$0$"], steps: ["Un nombre infiniment grand élevé au carré devient encore plus gigantesque."], f: "Limite usuelle" },
      { lvl: 1, q: "$\\lim_{x \\to +\\infty} \\frac{1}{x}$", a: "$0$", options: ["$0$", "$+\\infty$", "$1$"], steps: ["Imaginons diviser une seule pizza pour toute l'humanité. Chaque personne aura une part qui tend vers zéro."], f: "Limite usuelle" },
      { lvl: 1, q: "$\\lim_{x \\to +\\infty} e^x$", a: "$+\\infty$", options: ["$+\\infty$", "$0$", "$1$"], steps: ["L'exponentielle représente la croissance absolue. Elle explose très vite vers l'infini."], f: "Limite usuelle" },
      { lvl: 1, q: "$\\lim_{x \\to -\\infty} e^x$", a: "$0$", options: ["$0$", "$-\\infty$", "$+\\infty$"], steps: ["Quand on va très loin vers la gauche du graphique (l'infini négatif), la courbe exponentielle s'écrase sur l'axe des abscisses."], f: "Asymptote horizontale" },
      { lvl: 1, q: "$\\lim_{x \\to +\\infty} \\ln(x)$", a: "$+\\infty$", options: ["$+\\infty$", "$0$", "$1$"], steps: ["La croissance du logarithme est extrêmement lente, mais elle ne s'arrête jamais de monter vers l'infini."], f: "Limite usuelle" },
      { lvl: 1, q: "$\\lim_{x \\to 0^+} \\ln(x)$", a: "$-\\infty$", options: ["$-\\infty$", "$0$", "$+\\infty$"], steps: ["En s'approchant de $0$ par la droite, la courbe du logarithme plonge vers les abysses infinies."], f: "Asymptote verticale" },
      { lvl: 1, q: "$\\lim_{x \\to +\\infty} (x^2 + x)$", a: "$+\\infty$", options: ["$+\\infty$", "$0$", "$\\text{Indéterminé}$"], steps: ["C'est l'addition de deux termes qui tendent vers $+\\infty$. L'infini plus l'infini donne... l'infini !"], f: "Somme de limites" },
      { lvl: 1, q: "$\\lim_{x \\to +\\infty} \\frac{-3}{x^2}$", a: "$0$", options: ["$0$", "$-\\infty$", "$+\\infty$"], steps: ["Une petite constante ($-3$) divisée par un nombre infiniment grand donne un résultat qui s'écrase vers zéro."], f: "Quotient limite" },
      { lvl: 1, q: "$\\lim_{x \\to +\\infty} (2 - e^{-x})$", a: "$2$", options: ["$2$", "$+\\infty$", "$0$"], steps: ["Sais-tu vers quoi tend $e^{-x}$ (soit l'inverse de l'exponentielle) en $+\\infty$ ? Ça tend vers $0$.", "Il ne te reste donc que le nombre $2$."], f: "Opérations sur les limites" },
      { lvl: 1, q: "$\\lim_{x \\to -\\infty} x^3$", a: "$-\\infty$", options: ["$-\\infty$", "$+\\infty$", "$0$"], steps: ["Attention aux signes ! Un nombre très négatif mis au cube (puissance impaire) reste très négatif."], f: "Puissance impaire" },

      // NIVEAU 2 (7 exos)
      { lvl: 2, q: "$\\lim_{x \\to +\\infty} (x^2 - x)$", a: "$+\\infty$", options: ["$+\\infty$", "$0$", "$-\\infty$"], steps: ["Alerte Forme Indéterminée (FI) : l'infini moins l'infini !", "Pour lever l'indétermination, factorise par le terme le plus fort ($x^2$).", "Tu obtiens $x^2(1 - \\frac{1}{x})$. Le bloc entre parenthèses tend vers $1$."], f: "Mise en facteur" },
      { lvl: 2, q: "$\\lim_{x \\to +\\infty} \\frac{2x + 1}{x - 3}$", a: "$2$", options: ["$2$", "$+\\infty$", "$0$"], steps: ["Alerte Forme Indéterminée : l'infini sur l'infini !", "La règle d'or des fractions rationnelles en l'infini : prends uniquement la limite du quotient des termes de plus haut degré.", "Calcule la limite de $\\frac{2x}{x}$."], f: "Règle des plus hauts degrés" },
      { lvl: 2, q: "$\\lim_{x \\to +\\infty} \\frac{e^x}{x}$", a: "$+\\infty$", options: ["$+\\infty$", "$0$", "$1$"], steps: ["C'est une 'Croissance Comparée'.", "En $+\\infty$, l'exponentielle est la patronne absolue. Elle l'emporte sur n'importe quel polynôme."], f: "Croissance comparée" },
      { lvl: 2, q: "$\\lim_{x \\to +\\infty} \\frac{\\ln(x)}{x}$", a: "$0$", options: ["$0$", "$+\\infty$", "$1$"], steps: ["Encore une Croissance Comparée.", "Face à un polynôme en $+\\infty$, le logarithme perd toujours. C'est le dénominateur qui gagne et écrase la fraction vers zéro."], f: "Croissance comparée" },
      { lvl: 2, q: "$\\lim_{x \\to 0^+} x \\ln(x)$", a: "$0$", options: ["$0$", "$-\\infty$", "$1$"], steps: ["Forme indéterminée $0 \\times (-\\infty)$. C'est une limite de cours ! (Croissance comparée en $0$).", "Le polynôme (le $x$) impose sa force à la fonction $\\ln$."], f: "Croissance comparée" },
      { lvl: 2, q: "$\\lim_{x \\to +\\infty} \\frac{3x^2 - 1}{x^3 + 2}$", a: "$0$", options: ["$0$", "$3$", "$+\\infty$"], steps: ["Applique la règle des termes de plus haut degré en l'infini.", "Conserve uniquement $\\frac{3x^2}{x^3}$. En simplifiant, cela donne $\\frac{3}{x}$, qui tend vers... ?"], f: "Plus haut degré" },
      { lvl: 2, q: "$\\lim_{x \\to 2} \\frac{x^2 - 4}{x - 2}$", a: "$4$", options: ["$4$", "$0$", "$+\\infty$"], steps: ["En remplaçant $x$ par $2$, tu obtiens l'horrible indétermination $0/0$.", "Mais le numérateur $x^2 - 4$ est une identité remarquable ! Factorise-le en $(x-2)(x+2)$.", "Simplifie ta fraction en barrant les blocs $(x-2)$ puis calcule la limite !"], f: "Factorisation de $0/0$" },

      // NIVEAU 3 (3 exos)
      { lvl: 3, q: "$\\lim_{x \\to +\\infty} (\\sqrt{x^2+1} - x)$", a: "$0$", options: ["$0$", "$+\\infty$", "$1$"], steps: ["Forme $\\infty - \\infty$. Factoriser par $x$ ne suffit pas ici, il faut utiliser 'la quantité conjuguée' !", "Multiplie en haut et en bas par $(\\sqrt{x^2+1} + x)$.", "Le numérateur va se réduire à $1$. Tu auras $\\frac{1}{+\\infty}$."], f: "Quantité conjuguée" },
      { lvl: 3, q: "$\\lim_{x \\to 0} \\frac{e^x - 1}{x}$", a: "$1$", options: ["$1$", "$0$", "$+\\infty$"], steps: ["Indétermination $0/0$. Reconnais-tu la formule du taux d'accroissement ?", "Cette limite est exactement la définition mathématique du 'nombre dérivé' de la fonction $e^x$ au point $0$.", "La dérivée de $e^x$ est $e^x$. Et en $x=0$, cela vaut $e^0 = 1$."], f: "Nombre dérivé (Taux d'accroissement)" },
      { lvl: 3, q: "$\\lim_{x \\to +\\infty} \\frac{e^{2x}}{x^2}$", a: "$+\\infty$", options: ["$+\\infty$", "$0$", "$2$"], steps: ["C'est une croissance comparée de haut niveau.", "Astuce : réécris cette fraction comme le carré d'une autre fraction : $(\\frac{e^x}{x})^2$.", "Conclus avec la croissance comparée classique."], f: "Croissance comparée imbriquée" }
    ],

    // =========================================================================
    // 3. PRIMITIVES ET INTÉGRALES
    // =========================================================================
    PRIMITIVES: [
      // NIVEAU 1 (10 exos)
      { lvl: 1, q: "Primitive de $f(x) = 2x$", a: "$F(x) = x^2 + C$", options: ["$F(x) = x^2 + C$", "$F(x) = 2x^2 + C$", "$F(x) = 2 + C$"], steps: ["Une primitive est une 'dérivée à l'envers'.", "Quelle est la fonction qui, lorsqu'on la dérive, donne $2x$ ?"], f: "$\\int 2x dx = x^2$" },
      { lvl: 1, q: "Primitive de $f(x) = x^2$", a: "$F(x) = \\frac{1}{3}x^3 + C$", options: ["$F(x) = \\frac{1}{3}x^3 + C$", "$F(x) = 2x + C$", "$F(x) = x^3 + C$"], steps: ["La règle d'or pour un polynôme : on augmente la puissance de $1$, puis on divise le tout par cette nouvelle puissance."], f: "$\\int x^n dx = \\frac{x^{n+1}}{n+1}$" },
      { lvl: 1, q: "Primitive de $f(x) = e^x$", a: "$F(x) = e^x + C$", options: ["$F(x) = e^x + C$", "$F(x) = x e^x + C$", "$F(x) = \\frac{1}{2}e^x + C$"], steps: ["C'est la fonction la plus facile du monde à intégrer. Elle ne change jamais."], f: "$\\int e^x dx = e^x$" },
      { lvl: 1, q: "Primitive de $f(x) = \\frac{1}{x}$ sur $]0 ; +\\infty[$", a: "$F(x) = \\ln(x) + C$", options: ["$F(x) = \\ln(x) + C$", "$F(x) = -\\frac{1}{x^2} + C$", "$F(x) = e^x + C$"], steps: ["Si tu connais tes dérivées par cœur, c'est direct : quelle fonction a pour dérivée l'inverse de $x$ ?"], f: "$\\int \\frac{1}{x} dx = \\ln(x)$" },
      { lvl: 1, q: "Primitive de $f(x) = 3$", a: "$F(x) = 3x + C$", options: ["$F(x) = 3x + C$", "$F(x) = 0$", "$F(x) = 3x^2 + C$"], steps: ["Une constante (comme une vitesse stabilisée) donne une fonction affine (une ligne droite) quand on l'intègre."], f: "$\\int k dx = kx$" },
      { lvl: 1, q: "Calculer $\\int_{0}^{1} 2x dx$", a: "$1$", options: ["$1$", "$2$", "$0$"], steps: ["1. Trouve la primitive $F(x) = x^2$.", "2. Calcule la variation $F(1) - F(0)$."], f: "$\\int_a^b f = F(b) - F(a)$" },
      { lvl: 1, q: "Primitive de $f(x) = e^{2x}$", a: "$F(x) = \\frac{1}{2}e^{2x} + C$", options: ["$F(x) = \\frac{1}{2}e^{2x} + C$", "$F(x) = 2e^{2x} + C$", "$F(x) = e^{2x} + C$"], steps: ["Si tu dérives $e^{2x}$, un coefficient $2$ va tomber devant. Il faut l'anticiper !", "Mets un $\\frac{1}{2}$ devant ta primitive pour compenser et neutraliser ce $2$."], f: "$\\int e^{kx} dx = \\frac{1}{k}e^{kx}$" },
      { lvl: 1, q: "Primitive de $f(x) = \\cos(x)$", a: "$F(x) = \\sin(x) + C$", options: ["$F(x) = \\sin(x) + C$", "$F(x) = -\\sin(x) + C$", "$F(x) = -\\cos(x) + C$"], steps: ["Pour dériver en trigonométrie, on tourne dans le sens des aiguilles d'une montre.", "Pour intégrer (primitiver), on tourne dans le sens INVERSE des aiguilles d'une montre."], f: "Trigonométrie (Cercle)" },
      { lvl: 1, q: "Primitive de $f(x) = -\\sin(x)$", a: "$F(x) = \\cos(x) + C$", options: ["$F(x) = \\cos(x) + C$", "$F(x) = -\\cos(x) + C$", "$F(x) = \\sin(x) + C$"], steps: ["Tourne dans le sens inverse des aiguilles d'une montre sur le cercle trigonométrique en partant du sud ($-\\sin$)."], f: "Trigonométrie (Cercle)" },
      { lvl: 1, q: "Calculer $\\int_{1}^{e} \\frac{1}{x} dx$", a: "$1$", options: ["$1$", "$e$", "$0$"], steps: ["La primitive de $\\frac{1}{x}$ est $\\ln(x)$.", "Calcule $\\ln(e) - \\ln(1)$."], f: "$\\int_a^b f = F(b) - F(a)$" },

      // NIVEAU 2 (7 exos)
      { lvl: 2, q: "Primitive de $f(x) = 2x e^{x^2}$", a: "$F(x) = e^{x^2} + C$", options: ["$F(x) = e^{x^2} + C$", "$F(x) = 2e^{x^2} + C$", "$F(x) = x^2 e^{x^2} + C$"], steps: ["Reconnais la forme sacrée $u' \\times e^u$.", "Ici $u = x^2$ et sa dérivée est bien $u' = 2x$. La primitive d'une telle forme est immédiate !"], f: "$\\int u' e^u dx = e^u$" },
      { lvl: 2, q: "Primitive de $f(x) = \\frac{2x}{x^2+1}$", a: "$F(x) = \\ln(x^2+1) + C$", options: ["$F(x) = \\ln(x^2+1) + C$", "$F(x) = \\frac{1}{x^2+1} + C$", "$F(x) = 2\\ln(x^2+1) + C$"], steps: ["Observe bien la fraction. Le numérateur ($2x$) n'est-il pas l'exacte dérivée du dénominateur ($x^2+1$) ?", "C'est la forme magique $\\frac{u'}{u}$. Sa primitive est toujours le logarithme de $u$."], f: "$\\int \\frac{u'}{u} dx = \\ln|u|$" },
      { lvl: 2, q: "Primitive de $f(x) = (2x+1)^3$", a: "$F(x) = \\frac{1}{8}(2x+1)^4 + C$", options: ["$F(x) = \\frac{1}{8}(2x+1)^4 + C$", "$F(x) = \\frac{1}{4}(2x+1)^4 + C$", "$F(x) = \\frac{1}{2}(2x+1)^4 + C$"], steps: ["C'est presque la forme $u' \\times u^n$, mais il manque le $u'$ ! La dérivée de $(2x+1)$ est $2$.", "Ruse : multiplie par $2$ à l'intérieur, et compense en mettant un $\\frac{1}{2}$ à l'extérieur.", "Applique la règle de la puissance : $\\frac{1}{2} \\times \\frac{(2x+1)^4}{4}$."], f: "$\\int u' u^n = \\frac{u^{n+1}}{n+1}$" },
      { lvl: 2, q: "Calculer $\\int_{0}^{\\ln(2)} e^x dx$", a: "$1$", options: ["$1$", "$2$", "$\\ln(2)$"], steps: ["La primitive de $e^x$ est $e^x$.", "Calcule les bornes : $e^{\\ln(2)} - e^0$. Attention, $e^0$ ne fait pas zéro !"], f: "Intégrale usuelle" },
      { lvl: 2, q: "Primitive de $f(x) = \\frac{1}{\\sqrt{x}}$ sur $]0 ; +\\infty[$", a: "$F(x) = 2\\sqrt{x} + C$", options: ["$F(x) = 2\\sqrt{x} + C$", "$F(x) = \\sqrt{x} + C$", "$F(x) = \\frac{1}{2\\sqrt{x}} + C$"], steps: ["Rappelle-toi de tes formules de dérivation : la dérivée de $\\sqrt{x}$ est $\\frac{1}{2\\sqrt{x}}$.", "Il manque le coefficient $2$ en bas. Modifie la fonction pour l'intégrer facilement."], f: "$\\int \\frac{u'}{2\\sqrt{u}} = \\sqrt{u}$" },
      { lvl: 2, q: "Primitive de $f(x) = \\frac{x}{\\sqrt{x^2+1}}$", a: "$F(x) = \\sqrt{x^2+1} + C$", options: ["$F(x) = \\sqrt{x^2+1} + C$", "$F(x) = 2\\sqrt{x^2+1} + C$", "$F(x) = \\frac{1}{2}\\sqrt{x^2+1} + C$"], steps: ["C'est la forme $\\frac{u'}{2\\sqrt{u}}$.", "Pose $u = x^2+1$. Que vaut $u'$ ? Multiplie et divise par les bons nombres pour retrouver la forme exacte de la dérivée."], f: "Forme racine complexe" },
      { lvl: 2, q: "Valeur moyenne de $f(x)=2x$ sur $[0 ; 3]$", a: "$3$", options: ["$3$", "$9$", "$4,5$"], steps: ["La formule de la valeur moyenne est : $\\mu = \\frac{1}{b-a} \\int_a^b f(x) dx$.", "Calcule l'intégrale de $0$ à $3$, puis divise le résultat par $3$."], f: "Valeur moyenne d'une fonction" },

      // NIVEAU 3 (3 exos)
      { lvl: 3, q: "Calculer $\\int_0^1 x e^x dx$ (Indication : intégration par parties)", a: "$1$", options: ["$1$", "$e$", "$e-1$"], steps: ["On pose $u = x$ (donc $u' = 1$) pour le faire disparaître en dérivant, et $v' = e^x$ (donc $v = e^x$).", "Applique la formule magique $[uv] - \\int u'v$ !"], f: "$\\int uv' = [uv] - \\int u'v$" },
      { lvl: 3, q: "Calculer $\\int_1^e \\ln(x) dx$ (Indication : astuce du '1')", a: "$1$", options: ["$1$", "$e$", "$e-1$"], steps: ["Intégration par parties : imagine que $\\ln(x)$ s'écrit $1 \\times \\ln(x)$.", "Pose $u = \\ln(x)$ (donc $u' = 1/x$) et $v' = 1$ (donc $v = x$).", "L'intégrale restante sera $\\int (x \\times \\frac{1}{x})$, ce qui est très facile à calculer !"], f: "$\\int uv' = [uv] - \\int u'v$" },
      { lvl: 3, q: "Primitive de $f(x) = \\cos(x)\\sin^2(x)$", a: "$F(x) = \\frac{1}{3}\\sin^3(x) + C$", options: ["$F(x) = \\frac{1}{3}\\sin^3(x) + C$", "$F(x) = \\sin^3(x) + C$", "$F(x) = -\\frac{1}{3}\\cos^3(x) + C$"], steps: ["Identifie la forme du cours $u' \\times u^n$.", "Ici la fonction de base est $u = \\sin(x)$ élevée à la puissance $n=2$. Et miracle : sa dérivée $u'$ (le cosinus) est juste devant !"], f: "$\\int u' u^n = \\frac{u^{n+1}}{n+1}$" }
    ],

    // =========================================================================
    // 4. NOMBRES COMPLEXES (Maths Expertes)
    // =========================================================================
    COMPLEXES: [
      // NIVEAU 1 (10 exos)
      { lvl: 1, q: "$i^2$", a: "$-1$", options: ["$-1$", "$1$", "$0$"], steps: ["C'est l'axiome fondateur de tous les nombres complexes. Le carré de l'unité imaginaire est négatif !"], f: "$i^2 = -1$" },
      { lvl: 1, q: "$(3 + 2i) + (1 - i)$", a: "$4 + i$", options: ["$4 + i$", "$4 + 3i$", "$2 + i$"], steps: ["L'addition complexe est simple : additionne les parties réelles (les vrais nombres) ensemble, et les parties imaginaires (les $i$) ensemble."], f: "Somme de complexes" },
      { lvl: 1, q: "$(4 + i) - (2 + 3i)$", a: "$2 - 2i$", options: ["$2 - 2i$", "$2 + 4i$", "$6 - 2i$"], steps: ["Attention au signe moins qui distribue sur toute la deuxième parenthèse : $-2$ et $-3i$."], f: "Soustraction de complexes" },
      { lvl: 1, q: "Conjugué de $z = 5 + 4i$", a: "$\\overline{z} = 5 - 4i$", options: ["$\\overline{z} = 5 - 4i$", "$\\overline{z} = -5 - 4i$", "$\\overline{z} = -5 + 4i$"], steps: ["Le conjugué (noté $\\overline{z}$) consiste simplement à inverser le signe de la partie imaginaire (celle avec le $i$)."], f: "$\\overline{a+bi} = a-bi$" },
      { lvl: 1, q: "Conjugué de $z = -2i$", a: "$\\overline{z} = 2i$", options: ["$\\overline{z} = 2i$", "$\\overline{z} = -2i$", "$\\overline{z} = 0$"], steps: ["Même règle : on inverse le signe de la partie avec le $i$. La partie réelle ici vaut $0$."], f: "$\\overline{bi} = -bi$" },
      { lvl: 1, q: "$2i \\times 3i$", a: "$-6$", options: ["$-6$", "$6$", "$6i$"], steps: ["Multiplie les nombres : $2 \\times 3 = 6$.", "Multiplie les $i$ : $i \\times i = i^2$. N'oublie pas de remplacer $i^2$ !"], f: "Multiplication imaginaire pure" },
      { lvl: 1, q: "Module $|3 + 4i|$", a: "$5$", options: ["$5$", "$7$", "$25$"], steps: ["Le module est la distance géométrique par rapport à l'origine du repère.", "C'est le théorème de Pythagore : $\\sqrt{a^2 + b^2}$. Calcule $\\sqrt{3^2 + 4^2}$."], f: "$|z| = \\sqrt{a^2+b^2}$" },
      { lvl: 1, q: "$z \\times \\overline{z}$ pour $z = 3+i$", a: "$10$", options: ["$10$", "$8$", "$9+i$"], steps: ["Propriété magique : un complexe multiplié par son conjugué donne toujours le carré de son module : $a^2 + b^2$ (sans aucun $i$ au final)."], f: "$z\\overline{z} = a^2 + b^2 = |z|^2$" },
      { lvl: 1, q: "Partie réelle de $z = 7 - 5i$", a: "$7$", options: ["$7$", "$-5$", "$7-5i$"], steps: ["Un nombre complexe $z = a + ib$ possède une partie réelle ($a$) et une partie imaginaire ($b$).", "On te demande simplement le nombre sans le $i$."], f: "$\\text{Re}(a+bi) = a$" },
      { lvl: 1, q: "$(1+i)^2$", a: "$2i$", options: ["$2i$", "$2$", "$0$"], steps: ["Développe avec la 1ère identité remarquable : $1^2 + 2i + i^2$.", "Or, que vaut $i^2$ ? Il s'annule magnifiquement avec le $1$."], f: "Identité remarquable complexe" },

      // NIVEAU 2 (7 exos)
      { lvl: 2, q: "$(2 + i)(1 - 3i)$", a: "$5 - 5i$", options: ["$5 - 5i$", "$5 + 5i$", "$2 - 3i$"], steps: ["Fais une double distribution (développement) classique.", "Tu obtiendras un terme en $-3i^2$. Règle d'or : remplace TOUJOURS $i^2$ par $-1$ pour le transformer en un vrai nombre, puis regroupe."], f: "Développement complexe" },
      { lvl: 2, q: "Forme algébrique de $\\frac{1}{i}$", a: "$-i$", options: ["$-i$", "$i$", "$1$"], steps: ["On ne laisse jamais de $i$ au dénominateur !", "L'astuce est de multiplier en haut et en bas par $i$ (ou par son conjugué $-i$). Calcule $\\frac{i}{i^2}$."], f: "Inverse de $i$" },
      { lvl: 2, q: "Forme algébrique de $\\frac{2}{1+i}$", a: "$1 - i$", options: ["$1 - i$", "$1 + i$", "$2 - 2i$"], steps: ["Pour faire disparaître un $i$ en bas, on multiplie la fraction (en haut et en bas) par 'l'expression conjuguée' du bas (ici $1-i$).", "Le dénominateur deviendra un nombre réel pur grâce à l'identité $(a+b)(a-b) = a^2 - b^2$."], f: "Quotient par le conjugué" },
      { lvl: 2, q: "Résoudre $z + 2i = 3 - iz$", a: "$z = \\frac{1-5i}{2}$", options: ["$z = \\frac{1-5i}{2}$", "$z = 1 - 5i$", "$z = \\frac{3-2i}{2}$"], steps: ["Regroupe tous les termes avec $z$ du côté gauche de l'équation, et tous les nombres à droite.", "Factorise par $z$ à gauche pour obtenir $z(1+i) = \\dots$", "Isole $z$ en créant une fraction, puis multiplie par le conjugué pour obtenir la forme finale."], f: "Équation du 1er degré dans $\\mathbb{C}$" },
      { lvl: 2, q: "Résoudre $z^2 = -9$ dans $\\mathbb{C}$", a: "$z = 3i \\text{ ou } z = -3i$", options: ["$z = 3i \\text{ ou } z = -3i$", "$z = 3 \\text{ ou } z = -3$", "$\\text{Pas de solution}$"], steps: ["Dans l'univers des nombres réels, un carré ne peut pas être négatif. Mais chez les complexes, c'est possible !", "Remplace l'esprit du signe moins par un $i^2$. Ton équation devient $z^2 = 9i^2$."], f: "$z^2 = -a \\Rightarrow z = \\pm i\\sqrt{a}$" },
      { lvl: 2, q: "Résoudre $z^2 + 2z + 5 = 0$", a: "$z = -1+2i \\text{ ou } z = -1-2i$", options: ["$z = -1+2i \\text{ ou } z = -1-2i$", "$z = 1+2i \\text{ ou } z = 1-2i$", "$z = -1+4i \\text{ ou } z = -1-4i$"], steps: ["Calcule le discriminant $\\Delta = b^2 - 4ac$. Il sera négatif ($-16$).", "Les racines carrées d'un nombre négatif dans $\\mathbb{C}$ utilisent le $i$. Ici, les racines du delta sont $4i$ et $-4i$.", "Applique les formules classiques $\\frac{-b \\pm i\\sqrt{|\\Delta|}}{2a}$."], f: "Équation du 2nd degré, $\\Delta < 0$" },
      { lvl: 2, q: "Forme exponentielle de $z = 1+i$", a: "$\\sqrt{2} e^{i\\pi/4}$", options: ["$\\sqrt{2} e^{i\\pi/4}$", "$2 e^{i\\pi/4}$", "$\\sqrt{2} e^{i\\pi/2}$"], steps: ["1. Calcule le module $r = |z| = \\sqrt{1^2 + 1^2}$.", "2. Cherche l'angle (l'argument $\\theta$) tel que $\\cos(\\theta) = 1/r$ et $\\sin(\\theta) = 1/r$.", "3. Assemble le tout sous la forme d'Euler : $r e^{i\\theta}$."], f: "$z = |z| e^{i\\theta}$" },

      // NIVEAU 3 (3 exos)
      { lvl: 3, q: "Calculer $(1+i)^8$", a: "$16$", options: ["$16$", "$16i$", "$8$"], steps: ["Interdiction absolue de développer avec la formule du binôme de Newton ! Trop long.", "Astuce de génie : transforme la puissance $8$ en carrés imbriqués. C'est $((1+i)^2)^4$.", "Tu sais que $(1+i)^2$ donne un résultat très simple (vu au niveau 1). Élève ce petit résultat à la puissance $4$."], f: "Puissances complexes" },
      { lvl: 3, q: "Forme algébrique de $\\frac{3+i}{2-i}$", a: "$1 + i$", options: ["$1 + i$", "$1 - i$", "$\\frac{5+i}{5}$"], steps: ["Méthode systématique pour les fractions complexes : multiplie le haut et le bas par le conjugué du bas.", "Le conjugué de $2-i$ est $2+i$. Fais une double distributivité en haut, et utilise Pythagore ($a^2+b^2$) en bas.", "Sépare ensuite la partie réelle et la partie imaginaire."], f: "Quotient complexe" },
      { lvl: 3, q: "Racines cubiques de l'unité ($z^3 = 1$)", a: "$1, e^{i2\\pi/3}, e^{i4\\pi/3}$", options: ["$1, e^{i2\\pi/3}, e^{i4\\pi/3}$", "$1, -1, i$", "$1, e^{i\\pi/3}, e^{i2\\pi/3}$"], steps: ["On cherche 3 points sur le cercle trigonométrique qui forment un triangle équilatéral parfait.", "Passe en forme exponentielle : $z = e^{i\\theta}$. L'équation devient $e^{i3\\theta} = e^{i0}$.", "Cela implique que $3\\theta = 0 + 2k\\pi$. Divise par $3$ et fais varier le petit entier $k$ !"], f: "Racines $n$-ièmes : $z^n = 1$" }
    ]
  }
};