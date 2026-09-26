# Audit Hints — 2026-04-10

Total warnings: **124** sur **104** exercices

## Résumé par type

| Type | Count |
|------|-------|
| WARN_HINT_IS_ANSWER | 121 |
| WARN_HINT_TOO_SHORT | 3 |

## Par table

- **curriculum**: 87 warnings
- **diagnostic_exos**: 37 warnings

## Détails

### curriculum — 6EME / Fractions (row 1, exo 6)
- **Q**: Quelle écriture décimale correspond à $\frac{7}{10}$ ?
- **A**: $0{,}7$
- `WARN_HINT_IS_ANSWER` step 2: _$7$ dixièmes s'écrit $0{,}7$._

### curriculum — 6EME / Géométrie (row 4, exo 9)
- **Q**: Un quadrilatère dont les diagonales se coupent en leur milieu est un :
- **A**: parallélogramme
- `WARN_HINT_IS_ANSWER` step 1: _La propriété « diagonales se coupant en leur milieu » caractérise le parallélogramme._

### curriculum — 6EME / Géométrie (row 4, exo 12)
- **Q**: Le terrain de foot de l'école a $4$ côtés. C'est un :
- **A**: quadrilatère
- `WARN_HINT_IS_ANSWER` step 1: _Un polygone à 4 côtés s'appelle un quadrilatère._

### curriculum — 6EME / Angles (row 6, exo 9)
- **Q**: Deux angles opposés par le sommet sont toujours :
- **A**: égaux
- `WARN_HINT_IS_ANSWER` step 1: _Quand deux droites se coupent, les angles opposés sont égaux._

### curriculum — 5EME / Calcul_Littéral (row 10, exo 17)
- **Q**: Développe et réduis $(x + 1)^2 + (x - 1)^2$.
- **A**: $2x^2 + 2$
- `WARN_HINT_IS_ANSWER` step 3: _Somme : $2x^2 + 2$_

### curriculum — 6EME / Statistiques_6ème (row 12, exo 10)
- **Q**: Pour calculer l'étendue d'une série, on fait valeur ___ moins valeur ___. Écris 
- **A**: maximale
- `WARN_HINT_IS_ANSWER` step 1: _Étendue = valeur maximale − valeur minimale._

### curriculum — 6EME / Statistiques_6ème (row 12, exo 11)
- **Q**: Un diagramme en barres montre : lundi 12 absents, mardi 8, mercredi 5. Quel jour
- **A**: Lundi
- `WARN_HINT_IS_ANSWER` step 2: _Lundi a le plus d'absences._

### curriculum — 6EME / Symétrie_Axiale (row 13, exo 5)
- **Q**: Combien d'axes de symétrie possède un cercle ? Réponse : ___ (écris le mot).
- **A**: infini
- `WARN_HINT_IS_ANSWER` step 2: _Il y a une infinité de diamètres possibles._

### curriculum — 6EME / Symétrie_Axiale (row 13, exo 17)
- **Q**: Si $A(2, 1)$ a pour symétrique $A'(8, 1)$ par rapport à un axe vertical, quelle 
- **A**: x = 5
- `WARN_HINT_IS_ANSWER` step 3: _L'axe est $x = 5$._

### curriculum — 6EME / Conversions_Unités (row 18, exo 12)
- **Q**: Un trajet en train dure $2{,}5$ heures. En heures et minutes :
- **A**: 2 h 30 min
- `WARN_HINT_IS_ANSWER` step 3: _Total : $2$ h $30$ min._

### curriculum — 1ERE / Second_Degre (row 20, exo 16)
- **Q**: Déterminer $m$ pour que $x^2 +1x + m = 0$ ait une racine double.
- **A**: $m = 0$
- `WARN_HINT_IS_ANSWER` step 2: _$\Delta = (1)^2 - 4m = 0$._

### curriculum — 1ERE / Suites (row 21, exo 15)
- **Q**: $u_n = n^2 - 4n$. Étudier le sens de variation.
- **A**: Décroissante puis croissante
- `WARN_HINT_IS_ANSWER` step 3: _Signe change : décroissante puis croissante._

### curriculum — 1ERE / Suites (row 21, exo 16)
- **Q**: $u_n = n^2 - 4n$. Étudier le sens de variation.
- **A**: Décroissante puis croissante
- `WARN_HINT_IS_ANSWER` step 3: _Signe change : décroissante puis croissante._

### curriculum — 1ERE / Derivation (row 22, exo 5)
- **Q**: Dériver $f(x) = e^x$.
- **A**: $e^x$
- `WARN_HINT_IS_ANSWER` step 1: _On dérive $f(x) = e^x$. La fonction exponentielle est sa propre dérivée : $(e^x)' = e^x$._
- `WARN_HINT_IS_ANSWER` step 2: _Ici il n'y a qu'un seul terme : $e^x$. Sa dérivée est directement $e^x$._

### curriculum — 1ERE / Derivation (row 22, exo 6)
- **Q**: Dériver $f(x) = 3e^x + 2$.
- **A**: $3e^x$
- `WARN_HINT_IS_ANSWER` step 1: _On dérive $f(x) = 3e^x + 2$ terme par terme. On utilise $(e^x)' = e^x$ et $(c)' = 0$._
- `WARN_HINT_IS_ANSWER` step 2: _La dérivée de $3e^x$ est $3 \times e^x = 3e^x$ (le coefficient se conserve). La dérivée de $2$ est $_

### curriculum — 1ERE / Derivation (row 22, exo 13)
- **Q**: $f(x) = xe^x$. Calculer $f'(x)$.
- **A**: $(1+x)e^x$
- `WARN_HINT_IS_ANSWER` step 3: _$f' = e^x + xe^x = (1+x)e^x$._

### curriculum — 1ERE / Exponentielle (row 23, exo 8)
- **Q**: Que vaut $\lim_{x \to +\infty} e^x$?
- **A**: $+\infty$
- `WARN_HINT_IS_ANSWER` step 1: _On étudie $\lim_{x \to +\infty} e^x$. L'exponentielle est strictement croissante sur $\mathbb{R}$._
- `WARN_HINT_IS_ANSWER` step 3: _On en déduit que la limite est $+\infty$ : l'exponentielle "explose" vers l'infini._

### curriculum — 1ERE / Trigonometrie (row 24, exo 17)
- **Q**: $f(x) = \sin(x) + \cos(x)$. Calculer $f(\pi/4)$.
- **A**: $\sqrt{2}$
- `WARN_HINT_IS_ANSWER` step 2: _On sait que $\sin(\pi/4) = \frac{\sqrt{2}}{2}$ et $\cos(\pi/4) = \frac{\sqrt{2}}{2}$. On additionne _
- `WARN_HINT_IS_ANSWER` step 3: _La somme $\frac{\sqrt{2}}{2} + \frac{\sqrt{2}}{2}$ se simplifie._

### curriculum — 1ERE / Geometrie_Repere (row 26, exo 1)
- **Q**: Donner un vecteur directeur de la droite $y = 1x + 2$.
- **A**: $\vec{u}(1;1)$
- `WARN_HINT_IS_ANSWER` step 2: _Ici $m = 1$. Le vecteur directeur est donc $\vec{u}(1; 1)$._

### curriculum — 1ERE / Geometrie_Repere (row 26, exo 2)
- **Q**: Donner un vecteur directeur de la droite $y = 2x + 3$.
- **A**: $\vec{u}(1;2)$
- `WARN_HINT_IS_ANSWER` step 2: _Ici $m = 2$. Le vecteur directeur est donc $\vec{u}(1; 2)$._

### curriculum — 1ERE / Geometrie_Repere (row 26, exo 3)
- **Q**: Donner un vecteur directeur de la droite $y = 3x + 4$.
- **A**: $\vec{u}(1;3)$
- `WARN_HINT_IS_ANSWER` step 2: _Ici $m = 3$. Le vecteur directeur est donc $\vec{u}(1; 3)$._

### curriculum — 1ERE / Geometrie_Repere (row 26, exo 4)
- **Q**: Equation de la droite passant par $A(4;5)$ de pente $6$.
- **A**: $y = 6x + -19$
- `WARN_HINT_IS_ANSWER` step 3: _$y = 6x + -19$._

### curriculum — 1ERE / Geometrie_Repere (row 26, exo 5)
- **Q**: Equation de la droite passant par $A(5;6)$ de pente $7$.
- **A**: $y = 7x + -29$
- `WARN_HINT_IS_ANSWER` step 3: _$y = 7x + -29$._

### curriculum — 1ERE / Probabilites_Cond (row 27, exo 18)
- **Q**: $P(A) = 0{,}3$, $P(B|A) = 0{,}6$, $P(B) = 0{,}3$. Calculer $P(A|B)$.
- **A**: $0{,}6$
- `WARN_HINT_IS_ANSWER` step 1: _$P(A \cap B) = P(A) \times P(B|A) = 0{,}3 \times 0{,}6 = 0{,}18$._

### curriculum — 1ERE / Probabilites_Cond (row 27, exo 19)
- **Q**: Test de dépistage :$P(M) = 0{,}01$, $P(+|M) = 0{,}9$, $P(+|\bar{M}) = 0{,}05$. C
- **A**: $\approx 0{,}154$
- `WARN_HINT_IS_ANSWER` step 3: _$\approx 0{,}154$._

### curriculum — 3EME / Racines_Carrees_Brevet (row 44, exo 14)
- **Q**: Simplifie $\dfrac{10}{\sqrt{50}}$.
- **A**: $\sqrt{2}$
- `WARN_HINT_IS_ANSWER` step 1: _Simplifie d'abord $\sqrt{50} = 5\sqrt{2}$._
- `WARN_HINT_IS_ANSWER` step 2: _$\dfrac{10}{5\sqrt{2}} = \dfrac{?}{\sqrt{2}}$._
- `WARN_HINT_IS_ANSWER` step 3: _Rationalise : $\dfrac{? \times \sqrt{2}}{\sqrt{2} \times \sqrt{2}} = \dfrac{?\sqrt{2}}{?} = \sqrt{?}_

### curriculum — 4EME / Puissances (row 46, exo 3)
- **Q**: Une ville compte $45\,000$ habitants. Écrire ce nombre en notation scientifique.
- **A**: $4{,}5\times10^4$
- `WARN_HINT_IS_ANSWER` step 3: _$45\,000 = 4{,}5 \times 10^4$._

### curriculum — 4EME / Puissances (row 46, exo 8)
- **Q**: La distance Paris-New York est d'environ $5{,}8 \times 10^6$ mètres. Convertir e
- **A**: $5\,800\,000$
- `WARN_HINT_IS_ANSWER` step 2: _$5{,}8 \to 58 \to 580 \to 5\,800 \to 58\,000 \to 580\,000 \to 5\,800\,000$._

### curriculum — 4EME / Calcul_Littéral (row 47, exo 5)
- **Q**: Complète : $(n+1)^2 - n^2 = $ ___
- **A**: $2n+1$
- `WARN_HINT_IS_ANSWER` step 1: _$(n+1)^2 = n^2 + 2n + 1$._
- `WARN_HINT_IS_ANSWER` step 2: _$(n^2 + 2n + 1) - n^2 = 2n + 1$._

### curriculum — 4EME / Calcul_Littéral (row 47, exo 10)
- **Q**: Complète : $2x^2 + 8x + 8 = 2(\text{___})^2$
- **A**: x+2
- `WARN_HINT_IS_ANSWER` step 2: _$x^2 + 4x + 4 = (x+2)^2$ (identité remarquable)._
- `WARN_HINT_IS_ANSWER` step 3: _$2x^2 + 8x + 8 = 2(x+2)^2$._

### curriculum — 4EME / Calcul_Littéral (row 47, exo 15)
- **Q**: Complète : $x^4 - 1 = (x^2 - 1)(\text{___})$
- **A**: $x^2+1$
- `WARN_HINT_IS_ANSWER` step 3: _$= (x^2 - 1)(x^2 + 1)$._

### curriculum — 4EME / Calcul_Littéral (row 47, exo 18)
- **Q**: Développe $(a+b)^2+(a-b)^2$.
- **A**: $2a^2+2b^2$
- `WARN_HINT_IS_ANSWER` step 3: _Somme :$2a^2 + 2b^2$._

### curriculum — 4EME / Équations (row 48, exo 6)
- **Q**: On partage un paquet de billes en $4$ parts égales. Chaque part contient $3$ bil
- **A**: $x=12$
- `WARN_HINT_IS_ANSWER` step 3: _$x = 12$ billes._

### curriculum — 4EME / Équations (row 48, exo 8)
- **Q**: Combien de solutions a l'équation $x + 5 = x + 3$ ?
- **A**: Aucune
- `WARN_HINT_IS_ANSWER` step 3: _L'équation n'a aucune solution._

### curriculum — 4EME / Pythagore (row 49, exo 19)
- **Q**: La distance entre $A(1;2)$ et $B(4;6)$ est $5$.
- **A**: Vrai
- `WARN_HINT_TOO_SHORT` step 2: _$= 5$._

### curriculum — 4EME / Pythagore (row 49, exo 20)
- **Q**: Complète : dans un triangle isocèle de côtés $8$ cm, $8$ cm, le troisième côté v
- **A**: $\approx 5{,}7$
- `WARN_HINT_IS_ANSWER` step 3: _Par le théorème d'Al-Kashi ou la trigonométrie : $c \approx 5{,}7$ cm (différent de $4{,}7$)._

### curriculum — 4EME / Statistiques (row 50, exo 3)
- **Q**: Dans une classe, $10$ élèves ont eu $8$, $15$ élèves ont eu $12$ et $5$ élèves o
- **A**: $11{,}3\overline{3}$
- `WARN_HINT_IS_ANSWER` step 3: _$\frac{340}{30} \approx 11{,}3\overline{3}$._

### curriculum — 4EME / Inéquations (row 51, exo 1)
- **Q**: Tu as déjà $3$ € de frais fixes. Ton budget total doit rester inférieur à $8$ €.
- **A**: x < 5
- `WARN_HINT_IS_ANSWER` step 3: _$x < 5$ €._

### curriculum — 4EME / Inéquations (row 51, exo 8)
- **Q**: Complète :$-5x \geq 15$, donc $x$ ___ $-3$.
- **A**: $\leq$
- `WARN_HINT_IS_ANSWER` step 2: _$x \leq \frac{15}{-5} = -3$._
- `WARN_HINT_IS_ANSWER` step 3: _$x \leq -3$._

### curriculum — 4EME / Inéquations (row 51, exo 15)
- **Q**: Complète : si $2 \leq 3x - 1 < 8$, alors ___ $\leq x <$ ___
- **A**: $1 \leq x < 3$
- `WARN_HINT_IS_ANSWER` step 2: _Diviser par $3$ : $1 \leq x < 3$._

### curriculum — 4EME / Homothétie (row 52, exo 2)
- **Q**: Si k > 1 dans une homothétie, s'agit-il d'un agrandissement ou d'une réduction ?
- **A**: Agrandissement
- `WARN_HINT_IS_ANSWER` step 3: _Le vocabulaire géométrique distingue deux cas : agrandissement ou réduction._

### curriculum — 4EME / Sections_Solides (row 53, exo 1)
- **Q**: On coupe un cube par un plan parallèle à une face. La section obtenue est :
- **A**: Un carré
- `WARN_HINT_IS_ANSWER` step 3: _La section est un carré de même côté que le cube_

### curriculum — 4EME / Sections_Solides (row 53, exo 3)
- **Q**: On coupe un cube par un plan passant par 4 sommets alternés. La section obtenue 
- **A**: Un rectangle
- `WARN_HINT_IS_ANSWER` step 3: _La section est un rectangle (en réalité un rectangle, souvent un carré selon les sommets choisis)_

### curriculum — 4EME / Sections_Solides (row 53, exo 6)
- **Q**: On coupe un prisme droit à base triangulaire par un plan parallèle à sa base. La
- **A**: Un triangle
- `WARN_HINT_IS_ANSWER` step 1: _La base du prisme est un triangle_

### curriculum — 4EME / Sections_Solides (row 53, exo 7)
- **Q**: On coupe une sphère par un plan quelconque. La section obtenue est toujours :
- **A**: Un cercle
- `WARN_HINT_IS_ANSWER` step 1: _Toute section d'une sphère par un plan est un cercle_

### curriculum — 4EME / Sections_Solides (row 53, exo 8)
- **Q**: La section d'un cylindre par un plan perpendiculaire à son axe est :
- **A**: Un cercle
- `WARN_HINT_IS_ANSWER` step 3: _La section est un cercle (disque)._

### curriculum — 4EME / Sections_Solides (row 53, exo 11)
- **Q**: La section d'un cube par un plan parallèle à une face est :
- **A**: Un carré
- `WARN_HINT_IS_ANSWER` step 3: _La section est un carré._

### curriculum — 4EME / Sections_Solides (row 53, exo 12)
- **Q**: Complète : la section d'une sphère par un plan est toujours un ___.
- **A**: cercle
- `WARN_HINT_IS_ANSWER` step 2: _Le rayon du cercle dépend de la distance du plan au centre._
- `WARN_HINT_IS_ANSWER` step 3: _Si le plan passe par le centre : grand cercle. Sinon : cercle plus petit._

### curriculum — 4EME / Sections_Solides (row 53, exo 17)
- **Q**: On coupe un cylindre de révolution (rayon 3 cm, hauteur 10 cm) par un plan incli
- **A**: Une ellipse
- `WARN_HINT_IS_ANSWER` step 1: _Un plan oblique courant un cylindre donne une ellipse_
- `WARN_HINT_IS_ANSWER` step 3: _La section est une ellipse_

### curriculum — 5EME / Puissances (row 56, exo 14)
- **Q**: La distance entre deux villes est de $45\,000$ m. En notation scientifique ?
- **A**: $4{,}5\times10^4$
- `WARN_HINT_IS_ANSWER` step 2: _$= 4{,}5 \times 10^4$_

### curriculum — 5EME / Puissances (row 56, exo 16)
- **Q**: Calcule $(3 \times 10^4) \times (2 \times 10^3)$.
- **A**: $6\times10^7$
- `WARN_HINT_IS_ANSWER` step 3: _$= 6 \times 10^7$_

### curriculum — 5EME / Puissances (row 56, exo 17)
- **Q**: Calcule $\frac{8 \times 10^5}{4 \times 10^2}$.
- **A**: $2\times10^3$
- `WARN_HINT_IS_ANSWER` step 3: _$= 2 \times 10^3$_

### curriculum — 5EME / Symétrie_Centrale (row 57, exo 17)
- **Q**: Quelle figure a à la fois des axes de symétrie ET un centre de symétrie ?
- **A**: Le rectangle
- `WARN_HINT_IS_ANSWER` step 1: _Le rectangle a 2 axes de symétrie_

### curriculum — 5EME / Transformations (row 58, exo 1)
- **Q**: Sur un quadrillage, le point $A(2, 1)$ est translaté par le vecteur $\vec{v}(3, 
- **A**: $(5, 3)$
- `WARN_HINT_IS_ANSWER` step 3: _Image : $(5, 3)$_

### curriculum — 5EME / Transformations (row 58, exo 2)
- **Q**: Le point $B(4, 3)$ est l'image du point $A(1, 1)$ par une translation. Quelles s
- **A**: $(3, 2)$
- `WARN_HINT_IS_ANSWER` step 3: _$\vec{v}(3, 2)$_

### curriculum — 5EME / Transformations (row 58, exo 6)
- **Q**: Quelle transformation conserve les longueurs et les angles mais déplace une figu
- **A**: La translation
- `WARN_HINT_IS_ANSWER` step 1: _La translation déplace chaque point de la même manière_

### curriculum — 5EME / Transformations (row 58, exo 7)
- **Q**: Par symétrie centrale de centre $O(0, 0)$, quelle est l'image du point $P(2, 5)$
- **A**: $(-2, -5)$
- `WARN_HINT_IS_ANSWER` step 2: _$P'(-2, -5)$_

### curriculum — 5EME / Transformations (row 58, exo 9)
- **Q**: Quelle transformation conserve l'orientation de la figure (sens de lecture des s
- **A**: La translation
- `WARN_HINT_IS_ANSWER` step 1: _La translation conserve l'orientation_

### curriculum — 5EME / Transformations (row 58, exo 12)
- **Q**: Le triangle $ABC$ a une aire de $12$ cm^2. Après une rotation de $45^{\circ}$ au
- **A**: $12$ cm^2
- `WARN_HINT_IS_ANSWER` step 2: _L'aire reste $12$ cm^2_

### curriculum — 5EME / Transformations (row 58, exo 16)
- **Q**: Par symétrie centrale de centre $I(2, 3)$, quelle est l'image du point $P(5, 1)$
- **A**: $(-1, 5)$
- `WARN_HINT_IS_ANSWER` step 3: _$P'(-1, 5)$_

### curriculum — 5EME / Transformations (row 58, exo 19)
- **Q**: Le point $A(0, 4)$ est translaté par $\vec{v}(3, -1)$, puis l'image subit une sy
- **A**: $(-3, -3)$
- `WARN_HINT_IS_ANSWER` step 2: _Symétrie de centre $O$ : $(-3, -3)$_

### curriculum — 5EME / Transformations (row 58, exo 20)
- **Q**: Complète : une rotation de centre $O$ et d'angle $90^{\circ}$ dans le sens anti-
- **A**: directe
- `WARN_HINT_IS_ANSWER` step 2: _Une rotation dans ce sens est dite directe_

### curriculum — 3EME / Probabilites_Brevet (row 59, exo 2)
- **Q**: Quelle est la probabilité de tirer une bille bleue ?
- **A**: $\frac{1}{2}$
- `WARN_HINT_IS_ANSWER` step 3: _Attention : $\frac{6}{12}$ et $\frac{1}{2}$ sont la même valeur, mais on attend la fraction simplifi_

### curriculum — 3EME / Probabilites_Brevet (row 59, exo 9)
- **Q**: Quelle est la probabilité de gagner un stylo ou un livre ?
- **A**: $\frac{1}{4}$
- `WARN_HINT_IS_ANSWER` step 3: _Attention : $\frac{5}{20} = \frac{1}{4}$, pas $\frac{3}{20}$ (qui est « stylo seul »)._

### curriculum — 3EME / Probabilites_Brevet (row 59, exo 17)
- **Q**: Quelle est la fréquence de réussite des lancers francs lors du concours ?
- **A**: $0{,}64$
- `WARN_HINT_IS_ANSWER` step 3: _Attention : $\frac{32}{50}$ est la fraction, $0{,}64$ est la fréquence décimale. $0{,}32$ serait $\f_

### curriculum — 3EME / Probabilites_Brevet (row 59, exo 20)
- **Q**: On simule $500$ tombolas sur ordinateur et on observe $24$ gains. Vers quelle va
- **A**: $\frac{1}{20}$
- `WARN_HINT_IS_ANSWER` step 1: _La fréquence observée est $\frac{24}{500} = 0{,}048$, proche de $\frac{1}{20} = 0{,}05$._
- `WARN_HINT_IS_ANSWER` step 3: _$\frac{24}{500}$ est la fréquence observée (elle varie). La probabilité théorique $\frac{1}{20}$ est_

### curriculum — 3EME / Statistiques_Brevet (row 60, exo 12)
- **Q**: Quelle est la médiane des salaires ?
- **A**: $1800$ €
- `WARN_HINT_IS_ANSWER` step 2: _Effectifs cumulés : $2$, $6$, $12\ldots$ Les $10$ème et $11$ème valeurs sont toutes les deux à $1800_

### curriculum — 3EME / Statistiques_Brevet (row 60, exo 20)
- **Q**: Les deux classes ont la même moyenne et la même médiane. Quelle classe a les rés
- **A**: Classe A
- `WARN_HINT_IS_ANSWER` step 1: _L'écart interquartile de la classe A : $Q_1 = 10$, $Q_3 = 14$, IQR $= 4$. Celui de la classe C : IQR_
- `WARN_HINT_IS_ANSWER` step 2: _Un IQR plus petit signifie que les $50\%$ centraux sont plus resserrés autour de la médiane. Quelle _

### curriculum — 3EME / Trigonometrie_Brevet (row 62, exo 3)
- **Q**: Pour trouver $PH$ en connaissant $BP$ et l'angle $\widehat{PBH}$, quel ratio tri
- **A**: La tangente
- `WARN_HINT_IS_ANSWER` step 2: _$\tan(\alpha) = \frac{\text{opposé}}{\text{adjacent}}$. C'est bien la tangente qui convient ici._

### curriculum — 4EME / Fractions (row 64, exo 4)
- **Q**: Quelle fraction est la plus grande : $\frac{2}{3}$ ou $\frac{3}{5}$ ?
- **A**: $\frac{2}{3}$
- `WARN_HINT_IS_ANSWER` step 3: _$\frac{2}{3} = \frac{10}{15}$ et $\frac{3}{5} = \frac{9}{15}$. Qui est le plus grand ?_

### curriculum — 4EME / Fractions (row 64, exo 8)
- **Q**: Léo mange $\frac{1}{8}$ de pizza au déjeuner, puis $\frac{3}{8}$ au dîner. Quell
- **A**: $\frac{1}{2}$
- `WARN_HINT_IS_ANSWER` step 3: _$\frac{4}{8} = \frac{1}{2}$. Léo a mangé la moitié !_

### curriculum — 4EME / Fractions (row 64, exo 10)
- **Q**: Calcule et simplifie : $\frac{4}{11} + \frac{6}{11}$ = ___
- **A**: $\frac{10}{11}$
- `WARN_HINT_IS_ANSWER` step 3: _$\frac{10}{11}$ — peut-on simplifier ? 10 et 11 n'ont pas de diviseur commun. C'est déjà irréductibl_

### curriculum — 4EME / Fractions (row 64, exo 16)
- **Q**: Calcule $\frac{5}{6} - \frac{1}{6}$.
- **A**: $\frac{2}{3}$
- `WARN_HINT_IS_ANSWER` step 3: _Peut-on simplifier ? $\frac{4}{6} = \frac{2}{3}$._

### curriculum — 4EME / Fractions (row 64, exo 35)
- **Q**: Calcule : $\frac{1}{1 + \frac{1}{2}}$ = ___
- **A**: $\frac{2}{3}$
- `WARN_HINT_IS_ANSWER` step 3: _$1 \times \frac{2}{3} = ?$_

### diagnostic_exos — 6EME / Proportionnalité (row 3, exo 2)
- **Q**: Dans un tableau de proportionnalité :$3 \to 4{,}5$. Alors $7 \to$?
- **A**: $10{,}5$
- `WARN_HINT_IS_ANSWER` step 2: _$7 \times 1{,}5 = 10{,}5$._

### diagnostic_exos — 6EME / Périmètres_Aires (row 5, exo 2)
- **Q**: Un triangle rectangle a deux côtés de l'angle droit mesurant $6$ cm et $8$ cm. Q
- **A**: $24$ cm$^2$
- `WARN_HINT_IS_ANSWER` step 3: _$\frac{6 \times 8}{2} = \frac{48}{2} = 24$ cm$^2$._

### diagnostic_exos — 5EME / Fractions (row 7, exo 1)
- **Q**: Calcule $\frac{1}{3} + \frac{1}{4}$.
- **A**: $\frac{7}{12}$
- `WARN_HINT_IS_ANSWER` step 3: _$\frac{4}{12} + \frac{3}{12} = \frac{7}{12}$._

### diagnostic_exos — 5EME / Fractions (row 7, exo 2)
- **Q**: Calcule $\frac{2}{5} \times \frac{3}{4}$.
- **A**: $\frac{3}{10}$
- `WARN_HINT_IS_ANSWER` step 3: _On simplifie par $2$:$\frac{6}{20} = \frac{3}{10}$._

### diagnostic_exos — 5EME / Proportionnalité (row 9, exo 1)
- **Q**: Un article coûte $80$ €. Son prix augmente de $15\,\%$. Quel est le nouveau prix
- **A**: $92$ €
- `WARN_HINT_IS_ANSWER` step 2: _Nouveau prix $= 80 + 12 = 92$ €._
- `WARN_HINT_IS_ANSWER` step 3: _Ou directement :$80 \times 1{,}15 = 92$ €._

### diagnostic_exos — 5EME / Puissances (row 10, exo 2)
- **Q**: Simplifie $3^4 \times 3^2$.
- **A**: $3^6$
- `WARN_HINT_IS_ANSWER` step 2: _$3^4 \times 3^2 = 3^{4+2} = 3^6$._

### diagnostic_exos — 5EME / Calcul_Littéral (row 12, exo 2)
- **Q**: Développe $2(3x - 4)$.
- **A**: $6x - 8$
- `WARN_HINT_IS_ANSWER` step 3: _$2(3x - 4) = 6x - 8$._

### diagnostic_exos — 4EME / Puissances (row 14, exo 1)
- **Q**: Que vaut $2^{-3}$?
- **A**: $\frac{1}{8}$
- `WARN_HINT_IS_ANSWER` step 2: _$2^{-3} = \frac{1}{2^3} = \frac{1}{8}$._

### diagnostic_exos — 4EME / Puissances (row 14, exo 2)
- **Q**: Écris $0{,}0045$ en notation scientifique.
- **A**: $4{,}5 \times 10^{-3}$
- `WARN_HINT_IS_ANSWER` step 2: _$0{,}0045 = 4{,}5 \times 0{,}001 = 4{,}5 \times 10^{-3}$._

### diagnostic_exos — 4EME / Calcul_Littéral (row 15, exo 1)
- **Q**: Développe $(x + 3)^2$.
- **A**: $x^2 + 6x + 9$
- `WARN_HINT_IS_ANSWER` step 3: _$= x^2 + 6x + 9$._

### diagnostic_exos — 4EME / Calcul_Littéral (row 15, exo 2)
- **Q**: Factorise $6x^2 + 9x$.
- **A**: $3x(2x + 3)$
- `WARN_HINT_IS_ANSWER` step 4: _$6x^2 + 9x = 3x(2x + 3)$._

### diagnostic_exos — 6EME / Nombres_Décimaux (row 16, exo 1)
- **Q**: Calcule $3{,}7 + 1{,}45$.
- **A**: $5{,}15$
- `WARN_HINT_IS_ANSWER` step 2: _$0 + 5 = 5$, $7 + 4 = 11$ (retenue), $3 + 1 + 1 = 5$ $\rightarrow$ $5{,}15$._

### diagnostic_exos — 6EME / Nombres_Décimaux (row 16, exo 2)
- **Q**: Calcule $4{,}5 \times 3{,}2$.
- **A**: $14{,}4$
- `WARN_HINT_IS_ANSWER` step 3: _$4{,}5 \times 3{,}2 = 14{,}40 = 14{,}4$._

### diagnostic_exos — 6EME / Symétrie_Axiale (row 18, exo 1)
- **Q**: Quel est le symétrique du point A(3, 2) par rapport à l'axe des ordonnées (x = 0
- **A**: A'(-3, 2)
- `WARN_HINT_IS_ANSWER` step 3: _y = 2 reste inchangé → A'(-3, 2)_

### diagnostic_exos — 6EME / Symétrie_Axiale (row 18, exo 2)
- **Q**: A(1, 5) a pour symétrique A'(7, 5). Quelle est l'équation de l'axe de symétrie ?
- **A**: x = 4
- `WARN_HINT_IS_ANSWER` step 3: _AA' est horizontal → axe vertical : x = 4_

### diagnostic_exos — 6EME / Volumes (row 20, exo 1)
- **Q**: Calculer le volume du pavé droit de dimensions 4 cm × 5 cm × 6 cm.
- **A**: 120 cm³
- `WARN_HINT_IS_ANSWER` step 3: _V = 120 cm³_

### diagnostic_exos — 4EME / Proportionnalité (row 22, exo 2)
- **Q**: $4$ ouvriers mettent $6$ jours pour finir un chantier. En combien de jours $3$ o
- **A**: $8$ jours
- `WARN_HINT_IS_ANSWER` step 3: _Avec $3$ ouvriers :$24 \div 3 = 8$ jours._

### diagnostic_exos — 5EME / Transformations (row 24, exo 1)
- **Q**: Le point A(1,3) est translaté par le vecteur $\vec{v}$ (4,-2). Quelles sont les 
- **A**: (5,1)
- `WARN_HINT_IS_ANSWER` step 3: _A'y = 3 + (-2) = 1 → A'(5,1)_

### diagnostic_exos — 5EME / Transformations (row 24, exo 2)
- **Q**: Par symétrie centrale de centre O(0,0), l'image de M(3,-2) est M'. Puis M' est t
- **A**: (-2,6)
- `WARN_HINT_IS_ANSWER` step 3: _Image finale : (-2,6)_

### diagnostic_exos — 5EME / Triangles_Semblables (row 26, exo 2)
- **Q**: Deux triangles semblables ont des aires de 16 cm² et 36 cm². Quel est le rapport
- **A**: 2/3
- `WARN_HINT_IS_ANSWER` step 2: _k = √(4/9) = 2/3_
- `WARN_HINT_IS_ANSWER` step 3: _Résultat : 2/3_

### diagnostic_exos — 6EME / Conversions_Unités (row 28, exo 2)
- **Q**: Convertir 2 m² en cm².
- **A**: 20 000 cm²
- `WARN_HINT_IS_ANSWER` step 2: _2 m² = 2 × 10 000 = 20 000 cm²_
- `WARN_HINT_IS_ANSWER` step 3: _Résultat : 20 000 cm²_

### diagnostic_exos — 6EME / Puissances_10 (row 29, exo 2)
- **Q**: Calculer $10^3 \times 10^4$.
- **A**: 10⁷
- `WARN_HINT_IS_ANSWER` step 3: _= 10⁷_
- `WARN_HINT_TOO_SHORT` step 3: _= 10⁷_

### diagnostic_exos — 4EME / Homothétie (row 30, exo 2)
- **Q**: Une homothétie de rapport k = 2 transforme un triangle d'aire 6 cm². Quelle est 
- **A**: 24 cm²
- `WARN_HINT_IS_ANSWER` step 2: _Aire image = 4 × 6 = 24 cm²_
- `WARN_HINT_IS_ANSWER` step 3: _Résultat : 24 cm²_

### diagnostic_exos — 4EME / Sections_Solides (row 31, exo 1)
- **Q**: On coupe un cube par un plan parallèle à une face. Quelle est la forme de la sec
- **A**: Un carré
- `WARN_HINT_IS_ANSWER` step 3: _La section est un carré_

### diagnostic_exos — 4EME / Sections_Solides (row 31, exo 2)
- **Q**: Une pyramide à base carrée de côté 9 cm est coupée par un plan parallèle à la ba
- **A**: 3 cm
- `WARN_HINT_TOO_SHORT` step 3: _= 3 cm_

### diagnostic_exos — 1ERE / Trigonometrie (row 35, exo 1)
- **Q**: Que vaut $\cos(2\pi/3)$?
- **A**: $-1/2$
- `WARN_HINT_IS_ANSWER` step 3: _$\cos(2\pi/3) = -1/2$._

### diagnostic_exos — 1ERE / Trigonometrie (row 35, exo 2)
- **Q**: Résoudre $\sin(x) = -1$ sur $[0; 2\pi]$.
- **A**: $x = 3\pi/2$
- `WARN_HINT_IS_ANSWER` step 3: _Il correspond à $x = 3\pi/2$._

### diagnostic_exos — 1ERE / Variables_Aleatoires (row 39, exo 1)
- **Q**: $X$ prend les valeurs $5, 6, 7$ avec probabilités $0{,}25, 0{,}50, 0{,}25$. $E(X
- **A**: $6{,}00$
- `WARN_HINT_IS_ANSWER` step 3: _$E(X) = 6{,}00$._

### diagnostic_exos — 4EME / Fractions (row 55, exo 2)
- **Q**: Laquelle est la plus grande :$\frac{5}{8}$ ou $\frac{7}{12}$?
- **A**: $\frac{5}{8}$
- `WARN_HINT_IS_ANSWER` step 2: _PPCM de $8$ et $12= 24$:$\frac{5}{8} = \frac{15}{24}$, $\frac{7}{12} = \frac{14}{24}$._
- `WARN_HINT_IS_ANSWER` step 3: _$15 > 14$, donc $\frac{5}{8} > \frac{7}{12}$._

### diagnostic_exos — 4EME / Inéquations (row 57, exo 2)
- **Q**: Résoudre $-4x + 2 \geq 10$.
- **A**: x ≤ -2
- `WARN_HINT_IS_ANSWER` step 2: _Diviser par -4 (sens inverse) : x ≤ -2_
- `WARN_HINT_IS_ANSWER` step 3: _Résultat : x ≤ -2_
