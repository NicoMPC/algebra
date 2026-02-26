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
    // 1. EXPONENTIELLE ET LOGARITHME NEPÉRIEN
    // =========================================================================
    EXP_LOG: [
      // NIVEAU 1 (10 exos)
      { lvl: 1, q: "$e^2 \\times e^3$", a: "$e^5$", steps: ["Les exposants s'additionnent lors d'une multiplication."], f: "$e^a \\times e^b = e^{a+b}$" },
      { lvl: 1, q: "$\\frac{e^5}{e^2}$", a: "$e^3$", steps: ["Les exposants se soustraient lors d'une division."], f: "$\\frac{e^a}{e^b} = e^{a-b}$" },
      { lvl: 1, q: "$(e^4)^2$", a: "$e^8$", steps: ["Puissance de puissance : on multiplie les exposants."], f: "$(e^a)^b = e^{a \\times b}$" },
      { lvl: 1, q: "$\\ln(e^3)$", a: "$3$", steps: ["La fonction ln et l'exponentielle s'annulent mutuellement."], f: "$\\ln(e^x) = x$" },
      { lvl: 1, q: "$e^{\\ln(5)}$", a: "$5$", steps: ["L'exponentielle annule le logarithme (pour $x > 0$)."], f: "$e^{\\ln(x)} = x$" },
      { lvl: 1, q: "$\\ln(A \\times B)$", a: "$\\ln(A) + \\ln(B)$", steps: ["Le logarithme transforme les produits en sommes."], f: "$\\ln(ab) = \\ln(a) + \\ln(b)$" },
      { lvl: 1, q: "$\\ln(e)$", a: "$1$", steps: ["Rappel : $e$ est $e^1$."], f: "$\\ln(e) = 1$" },
      { lvl: 1, q: "$\\ln(1)$", a: "$0$", steps: ["L'exponentielle de 0 vaut 1, donc ln(1) vaut 0."], f: "$\\ln(1) = 0$" },
      { lvl: 1, q: "$e^x = 1$", a: "$x = 0$", steps: ["Applique $\\ln$ des deux côtés : $\\ln(e^x) = \\ln(1)$."], f: "$e^x = 1 \\Leftrightarrow x = 0$" },
      { lvl: 1, q: "Dériver $f(x) = e^{3x}$", a: "$f'(x) = 3e^{3x}$", steps: ["La dérivée de $e^u$ est $u' e^u$."], f: "$(e^u)' = u' e^u$" },

      // NIVEAU 2 (7 exos)
      { lvl: 2, q: "Résoudre $e^{2x+1} = e^5$", a: "$x = 2$", steps: ["Les bases sont identiques, on égalise les exposants : $2x+1 = 5$."], f: "$e^a = e^b \\Leftrightarrow a = b$" },
      { lvl: 2, q: "Résoudre $\\ln(x-2) = 0$", a: "$x = 3$", steps: ["$0 = \\ln(1)$. Donc $x-2 = 1$."], f: "$\\ln(a) = \\ln(b) \\Leftrightarrow a=b$" },
      { lvl: 2, q: "Simplifier $\\ln(8) - \\ln(2)$", a: "$\\ln(4)$", steps: ["Différence de ln = ln du quotient : $\\ln(\\frac{8}{2})$."], f: "$\\ln(a) - \\ln(b) = \\ln(\\frac{a}{b})$" },
      { lvl: 2, q: "Simplifier $\\ln(x^2)$", a: "$2\\ln(x)$", steps: ["L'exposant sort du logarithme."], f: "$\\ln(x^n) = n\\ln(x)$" },
      { lvl: 2, q: "Dériver $f(x) = x e^x$", a: "$f'(x) = e^x(x+1)$", steps: ["Produit $uv$ : $u'v + uv' = 1\\cdot e^x + x\\cdot e^x$."], f: "$(uv)' = u'v + uv'$" },
      { lvl: 2, q: "Dériver $f(x) = \\ln(x^2+1)$", a: "$f'(x) = \\frac{2x}{x^2+1}$", steps: ["La dérivée de $\\ln(u)$ est $\\frac{u'}{u}$."], f: "$(\\ln(u))' = \\frac{u'}{u}$" },
      { lvl: 2, q: "Résoudre $e^x > 2$", a: "$x > \\ln(2)$", steps: ["Applique $\\ln$ (fonction croissante) des deux côtés."], f: "$e^x > k \\Leftrightarrow x > \\ln(k)$" },

      // NIVEAU 3 (3 exos)
      { lvl: 3, q: "Résoudre $e^{2x} - 3e^x + 2 = 0$", a: "$x = 0 \\text{ ou } x = \\ln(2)$", steps: ["Pose $X = e^x$. L'équation devient $X^2 - 3X + 2 = 0$.", "Racines : $X=1$ et $X=2$. Donc $e^x=1$ ou $e^x=2$."], f: "Changement de variable" },
      { lvl: 3, q: "Résoudre $\\ln(x) + \\ln(x-1) = \\ln(2)$", a: "$x = 2$", steps: ["1. Domaine : $x > 1$.", "2. $\\ln(x(x-1)) = \\ln(2) \\Rightarrow x^2-x-2 = 0$.", "3. Racines 2 et -1. Seul 2 est dans le domaine."], f: "Propriétés algébriques du ln" },
      { lvl: 3, q: "Dériver $f(x) = \\frac{e^x}{x}$", a: "$f'(x) = \\frac{e^x(x-1)}{x^2}$", steps: ["Quotient $u/v$ : $u'=e^x, v'=1$.", "$\\frac{e^x \\cdot x - e^x \\cdot 1}{x^2}$."], f: "$(\\frac{u}{v})' = \\frac{u'v-uv'}{v^2}$" }
    ],

    // =========================================================================
    // 2. LIMITES ET ASYMPTOTES
    // =========================================================================
    LIMITES: [
      // NIVEAU 1 (10 exos)
      { lvl: 1, q: "$\\lim_{x \\to +\\infty} x^2$", a: "$+\\infty$", steps: ["Un grand nombre au carré devient encore plus grand."], f: "Limite usuelle" },
      { lvl: 1, q: "$\\lim_{x \\to +\\infty} \\frac{1}{x}$", a: "$0$", steps: ["Un sur l'infini tend vers zéro."], f: "Limite usuelle" },
      { lvl: 1, q: "$\\lim_{x \\to +\\infty} e^x$", a: "$+\\infty$", steps: ["L'exponentielle explose vers l'infini."], f: "Limite usuelle" },
      { lvl: 1, q: "$\\lim_{x \\to -\\infty} e^x$", a: "$0$", steps: ["Vers l'infini négatif, la courbe s'écrase sur l'axe des abscisses."], f: "Limite usuelle" },
      { lvl: 1, q: "$\\lim_{x \\to +\\infty} \\ln(x)$", a: "$+\\infty$", steps: ["La croissance est lente, mais va vers l'infini."], f: "Limite usuelle" },
      { lvl: 1, q: "$\\lim_{x \\to 0^+} \\ln(x)$", a: "$-\\infty$", steps: ["En s'approchant de 0 par la droite, la courbe plonge vers l'infini négatif."], f: "Asymptote verticale" },
      { lvl: 1, q: "$\\lim_{x \\to +\\infty} (x^2 + x)$", a: "$+\\infty$", steps: ["Somme de deux termes tendant vers $+\\infty$."], f: "Somme de limites" },
      { lvl: 1, q: "$\\lim_{x \\to +\\infty} \\frac{-3}{x^2}$", a: "$0$", steps: ["Une constante sur l'infini fait 0."], f: "Quotient limite" },
      { lvl: 1, q: "$\\lim_{x \\to +\\infty} (2 - e^{-x})$", a: "$2$", steps: ["$e^{-x}$ tend vers 0, donc il reste 2."], f: "Opérations sur les limites" },
      { lvl: 1, q: "$\\lim_{x \\to -\\infty} x^3$", a: "$-\\infty$", steps: ["Une puissance impaire conserve le signe négatif."], f: "Puissance impaire" },

      // NIVEAU 2 (7 exos)
      { lvl: 2, q: "$\\lim_{x \\to +\\infty} (x^2 - x)$", a: "$+\\infty$", steps: ["Forme indéterminée $\\infty - \\infty$.", "Factorise par le terme de plus haut degré : $x^2(1 - \\frac{1}{x})$."], f: "Mise en facteur" },
      { lvl: 2, q: "$\\lim_{x \\to +\\infty} \\frac{2x + 1}{x - 3}$", a: "$2$", steps: ["Indétermination $\\frac{\\infty}{\\infty}$.", "Limite des termes de plus haut degré : $\\frac{2x}{x} = 2$."], f: "Règle des plus hauts degrés" },
      { lvl: 2, q: "$\\lim_{x \\to +\\infty} \\frac{e^x}{x}$", a: "$+\\infty$", steps: ["C'est une croissance comparée.", "L'exponentielle l'emporte toujours sur le polynôme."], f: "Croissance comparée" },
      { lvl: 2, q: "$\\lim_{x \\to +\\infty} \\frac{\\ln(x)}{x}$", a: "$0$", steps: ["Croissance comparée.", "Le polynôme l'emporte sur le logarithme."], f: "Croissance comparée" },
      { lvl: 2, q: "$\\lim_{x \\to 0} x \\ln(x)$", a: "$0$", steps: ["Croissance comparée en 0.", "Le polynôme impose sa limite (0)."], f: "Croissance comparée" },
      { lvl: 2, q: "$\\lim_{x \\to +\\infty} \\frac{3x^2 - 1}{x^3 + 2}$", a: "$0$", steps: ["Règle des plus hauts degrés : $\\frac{3x^2}{x^3} = \\frac{3}{x} \\to 0$."], f: "Plus haut degré" },
      { lvl: 2, q: "$\\lim_{x \\to 2} \\frac{x^2 - 4}{x - 2}$", a: "$4$", steps: ["Indétermination $\\frac{0}{0}$.", "Factorise le haut : $\\frac{(x-2)(x+2)}{x-2} = x+2 \\to 4$."], f: "Levée d'indétermination par factorisation" },

      // NIVEAU 3 (3 exos)
      { lvl: 3, q: "$\\lim_{x \\to +\\infty} \\sqrt{x^2+1} - x$", a: "$0$", steps: ["Forme $\\infty - \\infty$. Multiplie par la quantité conjuguée.", "$\\frac{(x^2+1) - x^2}{\\sqrt{x^2+1} + x} = \\frac{1}{\\infty}$."], f: "Quantité conjuguée" },
      { lvl: 3, q: "$\\lim_{x \\to 0} \\frac{e^x - 1}{x}$", a: "$1$", steps: ["C'est le taux d'accroissement de $e^x$ en 0.", "Il vaut la dérivée de $e^x$ en 0, soit $e^0 = 1$."], f: "Taux d'accroissement (Nombre dérivé)" },
      { lvl: 3, q: "$\\lim_{x \\to +\\infty} \\frac{e^{2x}}{x^2}$", a: "$+\\infty$", steps: ["Croissance comparée avancée.", "Peut s'écrire $(\\frac{e^x}{x})^2$."], f: "Croissance comparée" }
    ],

    // =========================================================================
    // 3. PRIMITIVES ET INTÉGRALES
    // =========================================================================
    PRIMITIVES: [
      // NIVEAU 1 (10 exos)
      { lvl: 1, q: "Primitive de $f(x) = 2x$", a: "$F(x) = x^2 + C$", steps: ["La fonction qui, dérivée, donne $2x$ est $x^2$."], f: "$\\int 2x dx = x^2$" },
      { lvl: 1, q: "Primitive de $f(x) = x^2$", a: "$F(x) = \\frac{1}{3}x^3 + C$", steps: ["Augmente la puissance de 1 et divise par la nouvelle puissance."], f: "$\\int x^n dx = \\frac{x^{n+1}}{n+1}$" },
      { lvl: 1, q: "Primitive de $f(x) = e^x$", a: "$F(x) = e^x + C$", steps: ["La dérivée de $e^x$ est $e^x$."], f: "$\\int e^x dx = e^x$" },
      { lvl: 1, q: "Primitive de $f(x) = \\frac{1}{x}$", a: "$F(x) = \\ln(x) + C$", steps: ["C'est la définition de la fonction ln pour $x>0$."], f: "$\\int \\frac{1}{x} dx = \\ln(x)$" },
      { lvl: 1, q: "Primitive de $f(x) = 3$", a: "$F(x) = 3x + C$", steps: ["La dérivée de $3x$ est $3$."], f: "$\\int k dx = kx$" },
      { lvl: 1, q: "Calculer $\\int_{0}^{1} 2x dx$", a: "$1$", steps: ["Primitive $[x^2]_0^1 = 1^2 - 0^2$."], f: "$\\int_a^b f = F(b) - F(a)$" },
      { lvl: 1, q: "Primitive de $f(x) = e^{2x}$", a: "$F(x) = \\frac{1}{2}e^{2x} + C$", steps: ["Il faut compenser le '2' qui sortira lors de la dérivation."], f: "$\\int e^{kx} dx = \\frac{1}{k}e^{kx}$" },
      { lvl: 1, q: "Primitive de $f(x) = \\cos(x)$", a: "$F(x) = \\sin(x) + C$", steps: ["La dérivée de sin est cos."], f: "Trigonométrie" },
      { lvl: 1, q: "Primitive de $f(x) = -\\sin(x)$", a: "$F(x) = \\cos(x) + C$", steps: ["La dérivée de cos est -sin."], f: "Trigonométrie" },
      { lvl: 1, q: "Calculer $\\int_{1}^{e} \\frac{1}{x} dx$", a: "$1$", steps: ["Primitive $[\\ln(x)]_1^e = \\ln(e) - \\ln(1) = 1 - 0$."], f: "$\\int_a^b f = F(b) - F(a)$" },

      // NIVEAU 2 (7 exos)
      { lvl: 2, q: "Primitive de $f(x) = 2x e^{x^2}$", a: "$F(x) = e^{x^2} + C$", steps: ["C'est la forme $u' e^u$ avec $u = x^2$."], f: "$\\int u' e^u dx = e^u$" },
      { lvl: 2, q: "Primitive de $f(x) = \\frac{2x}{x^2+1}$", a: "$F(x) = \\ln(x^2+1) + C$", steps: ["C'est la forme $u'/u$ avec $u = x^2+1$."], f: "$\\int \\frac{u'}{u} dx = \\ln|u|$" },
      { lvl: 2, q: "Primitive de $f(x) = (2x+1)^3$", a: "$F(x) = \\frac{1}{8}(2x+1)^4 + C$", steps: ["Forme $u' u^n$ mais il manque le $u'=2$.", "Multiplie et divise par 2 : $\\frac{1}{2} \\cdot 2(2x+1)^3$."], f: "$\\int u' u^n = \\frac{u^{n+1}}{n+1}$" },
      { lvl: 2, q: "Calculer $\\int_{0}^{\\ln(2)} e^x dx$", a: "$1$", steps: ["$[e^x]_0^{\\ln(2)} = e^{\\ln(2)} - e^0 = 2 - 1$."], f: "Intégrale usuelle" },
      { lvl: 2, q: "Primitive de $f(x) = \\frac{1}{\\sqrt{x}}$", a: "$F(x) = 2\\sqrt{x} + C$", steps: ["Rappel : la dérivée de $\\sqrt{x}$ est $\\frac{1}{2\\sqrt{x}}$."], f: "$\\int \\frac{u'}{\\sqrt{u}} = 2\\sqrt{u}$" },
      { lvl: 2, q: "Primitive de $f(x) = \\frac{x}{\\sqrt{x^2+1}}$", a: "$F(x) = \\sqrt{x^2+1} + C$", steps: ["Forme $\\frac{u'}{2\\sqrt{u}}$ en multipliant/divisant par 2."], f: "Intégration par substitution" },
      { lvl: 2, q: "Valeur moyenne de $f(x)=2x$ sur $[0, 3]$", a: "$3$", steps: ["Formule : $\\frac{1}{3-0} \\int_0^3 2x dx$.", "$\\frac{1}{3} [x^2]_0^3 = \\frac{9}{3}$."], f: "$\\mu = \\frac{1}{b-a} \\int_a^b f$" },

      // NIVEAU 3 (3 exos)
      { lvl: 3, q: "Intégration par parties : $\\int_0^1 x e^x dx$", a: "$1$", steps: ["Pose $u=x \\Rightarrow u'=1$ et $v'=e^x \\Rightarrow v=e^x$.", "Formule : $[x e^x]_0^1 - \\int_0^1 e^x dx = e - (e - 1)$."], f: "$\\int uv' = [uv] - \\int u'v$" },
      { lvl: 3, q: "Intégration par parties : $\\int_1^e \\ln(x) dx$", a: "$1$", steps: ["Astuce : $\\ln(x) = 1 \\times \\ln(x)$. Pose $u=\\ln(x)$ et $v'=1$.", "$[x\\ln(x)]_1^e - \\int_1^e x \\frac{1}{x} dx$."], f: "$\\int uv' = [uv] - \\int u'v$" },
      { lvl: 3, q: "Primitive de $f(x) = \\cos(x)\\sin^2(x)$", a: "$F(x) = \\frac{1}{3}\\sin^3(x) + C$", steps: ["C'est la forme $u' u^n$ avec $u = \\sin(x)$ et $n=2$."], f: "$\\int u' u^n = \\frac{u^{n+1}}{n+1}$" }
    ],

    // =========================================================================
    // 4. NOMBRES COMPLEXES
    // =========================================================================
    COMPLEXES: [
      // NIVEAU 1 (10 exos)
      { lvl: 1, q: "$i^2$", a: "$-1$", steps: ["C'est la définition fondamentale des nombres complexes."], f: "$i^2 = -1$" },
      { lvl: 1, q: "$(3 + 2i) + (1 - i)$", a: "$4 + i$", steps: ["On additionne les parties réelles ensemble (3+1) et imaginaires ensemble (2-1)."], f: "Additions complexes" },
      { lvl: 1, q: "$(4 + i) - (2 + 3i)$", a: "$2 - 2i$", steps: ["Soustraction : $4-2$ et $1-3$."], f: "Soustractions complexes" },
      { lvl: 1, q: "Conjugé de $z = 5 + 4i$", a: "$\\overline{z} = 5 - 4i$", steps: ["Le conjugué $\\overline{z}$ inverse le signe de la partie imaginaire."], f: "$\\overline{a+bi} = a-bi$" },
      { lvl: 1, q: "Conjugé de $z = -2i$", a: "$\\overline{z} = 2i$", steps: ["Partie réelle nulle. On inverse le signe de l'imaginaire."], f: "$\\overline{bi} = -bi$" },
      { lvl: 1, q: "$2i \\times 3i$", a: "$-6$", steps: ["$6i^2$. Or $i^2 = -1$, donc $-6$."], f: "Multiplication de purs imaginaires" },
      { lvl: 1, q: "Module $|3 + 4i|$", a: "$5$", steps: ["Le module est la distance : $\\sqrt{a^2 + b^2}$.", "$\\sqrt{3^2 + 4^2} = \\sqrt{9+16} = \\sqrt{25}$."], f: "$|z| = \\sqrt{a^2+b^2}$" },
      { lvl: 1, q: "$z \\times \\overline{z}$ pour $z = 3+i$", a: "$10$", steps: ["Formule : $a^2 + b^2$. Ici $3^2 + 1^2$."], f: "$z\\overline{z} = |z|^2$" },
      { lvl: 1, q: "Partie réelle de $z = 7 - 5i$", a: "$7$", steps: ["C'est le nombre sans le $i$."], f: "$\\text{Re}(a+bi) = a$" },
      { lvl: 1, q: "$(1+i)^2$", a: "$2i$", steps: ["Développe : $1^2 + 2i + i^2$.", "Comme $i^2 = -1$, il reste $2i$."], f: "Identité remarquable complexe" },

      // NIVEAU 2 (7 exos)
      { lvl: 2, q: "$(2 + i)(1 - 3i)$", a: "$5 - 5i$", steps: ["Double distribution : $2 - 6i + i - 3i^2$.", "Remplace $i^2$ par $-1$ : $2 - 5i + 3$."], f: "Développement complexe" },
      { lvl: 2, q: "Forme algébrique de $\\frac{1}{i}$", a: "$-i$", steps: ["Multiplie en haut et en bas par $i$ : $\\frac{i}{i^2} = \\frac{i}{-1}$."], f: "Inverse de $i$" },
      { lvl: 2, q: "Forme algébrique de $\\frac{2}{1+i}$", a: "$1 - i$", steps: ["Multiplie par le conjugué $(1-i)$ en haut et en bas.", "Bas : $(1+i)(1-i) = 1^2 - i^2 = 2$."], f: "Multiplication par le conjugué" },
      { lvl: 2, q: "Résoudre $z + 2i = 3 - iz$", a: "$z = \\frac{3-2i}{1+i} = \\frac{1-5i}{2}$", steps: ["Regroupe les $z$ : $z + iz = 3 - 2i$.", "Factorise : $z(1+i) = 3-2i$, puis divise."], f: "Équation du 1er degré dans $\\mathbb{C}$" },
      { lvl: 2, q: "Résoudre $z^2 = -9$", a: "$z = 3i \\text{ ou } z = -3i$", steps: ["Dans $\\mathbb{C}$, les nombres négatifs ont des racines carrées imaginaires."], f: "$z^2 = -a \\Rightarrow z = \\pm i\\sqrt{a}$" },
      { lvl: 2, q: "Résoudre $z^2 + 2z + 5 = 0$", a: "$z = -1+2i \\text{ ou } z = -1-2i$", steps: ["$\\Delta = 4 - 20 = -16$.", "Racines de $\\Delta$ : $\\pm 4i$. Racines : $\\frac{-2 \\pm 4i}{2}$."], f: "Équation du 2nd degré, $\\Delta < 0$" },
      { lvl: 2, q: "Forme exponentielle de $z = 1+i$", a: "$\\sqrt{2} e^{i\\pi/4}$", steps: ["Module : $\\sqrt{1^2+1^2} = \\sqrt{2}$.", "Argument : $\\cos(\\theta) = \\frac{1}{\\sqrt{2}}$, $\\sin(\\theta) = \\frac{1}{\\sqrt{2}} \\Rightarrow \\theta = \\frac{\\pi}{4}$."], f: "$z = |z| e^{i\\theta}$" },

      // NIVEAU 3 (3 exos)
      { lvl: 3, q: "Calculer $(1+i)^8$", a: "$16$", steps: ["Astuce : $(1+i)^8 = ((1+i)^2)^4$.", "Or $(1+i)^2 = 2i$. Donc $(2i)^4 = 16 i^4 = 16$."], f: "Puissances complexes" },
      { lvl: 3, q: "Forme algébrique de $\\frac{3+i}{2-i}$", a: "$1 + i$", steps: ["Multiplie par le conjugué $(2+i)$ en haut et en bas.", "Haut : $6 + 3i + 2i - 1 = 5 + 5i$. Bas : $4 + 1 = 5$."], f: "Quotient complexe" },
      { lvl: 3, q: "Racines cubiques de l'unité ($z^3 = 1$)", a: "$1, e^{i2\\pi/3}, e^{i4\\pi/3}$", steps: ["Utilise la forme exponentielle $z = e^{i\\theta}$.", "$\\theta = \frac{2k\\pi}{3}$ avec $k=0,1,2$."], f: "$z^n = 1$" }
    ]
  }
};