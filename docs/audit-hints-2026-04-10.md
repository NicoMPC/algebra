# Audit Hints — 2026-04-10

Total warnings: **1877** sur **1120** exercices

## Résumé par type

| Type | Count |
|------|-------|
| WARN_DUPLICATE | 4 |
| WARN_HINT_IS_ANSWER | 254 |
| WARN_HINT_IS_FORMULA | 1533 |
| WARN_HINT_TOO_SHORT | 86 |

## Par table

- **curriculum**: 1647 warnings
- **diagnostic_exos**: 230 warnings

## Détails

### curriculum — 6EME / Fractions (row 1, exo 1)
- **Q**: Tom reçoit $20$ € d'argent de poche. Il décide de dépenser les $\frac{3}{4}$ de 
- **A**: 15
- `WARN_HINT_IS_FORMULA` step 2: _On divise $20 \div 4 = 5$, puis $5 \times 3 = ?$._

### curriculum — 6EME / Fractions (row 1, exo 5)
- **Q**: Un sac contient $15$ billes. $\frac{2}{5}$ sont rouges. Complète : il y a ___ bi
- **A**: 6
- `WARN_HINT_IS_FORMULA` step 2: _On divise : $15 \div 5 = 3$ (une part sur cinq)._
- `WARN_HINT_IS_FORMULA` step 3: _On multiplie : $3 \times 2 = ?$ billes rouges._

### curriculum — 6EME / Fractions (row 1, exo 6)
- **Q**: Quelle écriture décimale correspond à $\frac{7}{10}$ ?
- **A**: $0{,}7$
- `WARN_HINT_IS_ANSWER` step 2: _$7$ dixièmes s'écrit $0{,}7$._

### curriculum — 6EME / Fractions (row 1, exo 7)
- **Q**: Trois amis se partagent $21$ bonbons à parts égales. Combien de bonbons chacun r
- **A**: 7
- `WARN_HINT_IS_FORMULA` step 2: _$21 \div 3 = ?$._

### curriculum — 6EME / Fractions (row 1, exo 8)
- **Q**: Le double de $\frac{1}{4}$, c'est $\frac{1}{2}$.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 2: _$2 \times \frac{1}{4} = \frac{2}{4} = \frac{1}{2}$._

### curriculum — 6EME / Fractions (row 1, exo 9)
- **Q**: Un élève écrit : $\frac{3}{4}$ de $20 = 20 \div 3 \times 4 = 26{,}7$. Quelle éta
- **A**: Il fallait diviser par 4 puis multiplier
- `WARN_HINT_IS_FORMULA` step 2: _$20 \div 4 = 5$, puis $5 \times 3 = 15$._

### curriculum — 6EME / Fractions (row 1, exo 10)
- **Q**: Complète : $\frac{?}{16} = \frac{3}{8}$. La valeur manquante est ___.
- **A**: 6
- `WARN_HINT_IS_FORMULA` step 2: _$8 \times 2 = 16$, donc on multiplie aussi le numérateur par $2$._
- `WARN_HINT_IS_FORMULA` step 3: _$3 \times 2 = ?$._

### curriculum — 6EME / Fractions (row 1, exo 11)
- **Q**: Une recette pour $5$ personnes nécessite $3$ œufs. Combien d'œufs faut-il pour $
- **A**: 12
- `WARN_HINT_IS_FORMULA` step 1: _On calcule le coefficient : $20 \div 5 = 4$._
- `WARN_HINT_IS_FORMULA` step 2: _On multiplie les œufs : $3 \times 4 = ?$._

### curriculum — 6EME / Fractions (row 1, exo 12)
- **Q**: Quelle est la forme simplifiée de $\frac{6}{9}$ ?
- **A**: $\frac{2}{3}$
- `WARN_HINT_IS_FORMULA` step 2: _$6 = 2 \times 3$ et $9 = 3 \times 3$, donc PGCD = $3$._

### curriculum — 6EME / Fractions (row 1, exo 13)
- **Q**: $\frac{4}{8}$ et $\frac{1}{2}$ représentent la même quantité.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{4 \div 4}{8 \div 4} = \frac{1}{2}$._

### curriculum — 6EME / Fractions (row 1, exo 14)
- **Q**: Sur $30$ élèves, $\frac{3}{10}$ ont les yeux bleus. Combien est-ce ?
- **A**: 9
- `WARN_HINT_IS_FORMULA` step 2: _$30 \div 10 = 3$, puis $3 \times 3 = ?$._

### curriculum — 6EME / Fractions (row 1, exo 15)
- **Q**: Un rectangle a une longueur de $20$ cm. Sa largeur est les $\frac{3}{4}$ de sa l
- **A**: 15
- `WARN_HINT_IS_FORMULA` step 2: _$20 \div 4 = 5$ cm, puis $5 \times 3 = ?$ cm._

### curriculum — 6EME / Fractions (row 1, exo 16)
- **Q**: Un club de sport compte $24$ membres. Les $\frac{5}{6}$ d'entre eux sont présent
- **A**: 20
- `WARN_HINT_IS_FORMULA` step 2: _$24 \div 6 = 4$, puis $4 \times 5 = ?$._

### curriculum — 6EME / Fractions (row 1, exo 17)
- **Q**: Complète : pour simplifier $\frac{12}{18}$, on divise numérateur et dénominateur
- **A**: 6
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{12 \div 6}{18 \div 6} = \frac{2}{3}$._

### curriculum — 6EME / Fractions (row 1, exo 18)
- **Q**: $\frac{4}{6} = \frac{2}{3}$.
- **A**: Vrai
- `WARN_HINT_IS_ANSWER` step 3: _L'égalité est vraie._
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{4 \div 2}{6 \div 2} = \frac{2}{3}$._

### curriculum — 6EME / Fractions (row 1, exo 19)
- **Q**: Si $\frac{x}{12} = \frac{1}{4}$, quelle est la valeur de $x$ ?
- **A**: 3
- `WARN_HINT_IS_FORMULA` step 1: _$\frac{1}{4} = \frac{?}{12}$ : on multiplie par $3$._
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{1 \times 3}{4 \times 3} = \frac{3}{12}$._
- `WARN_HINT_IS_FORMULA` step 3: _Donc $x = ?$._

### curriculum — 6EME / Fractions (row 1, exo 20)
- **Q**: Sur $40$ images, $\frac{3}{8}$ représentent des animaux. Il y a ___ images d'ani
- **A**: 15
- `WARN_HINT_IS_FORMULA` step 2: _$40 \div 8 = 5$, puis $5 \times 3 = ?$._

### curriculum — 6EME / Nombres_entiers (row 2, exo 3)
- **Q**: $5 \times 4 + 3 = 5 \times 7 = 35$.
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 2: _$5 \times 4 + 3 = 20 + 3 = 23$, pas $35$._

### curriculum — 6EME / Nombres_entiers (row 2, exo 5)
- **Q**: Un billet de spectacle coûte $35$ €. Le prix de $100$ billets est ___ €.
- **A**: 3500
- `WARN_HINT_IS_FORMULA` step 2: _$35 \times 100 = ?$._

### curriculum — 6EME / Nombres_entiers (row 2, exo 7)
- **Q**: Dans $45\,372$, le chiffre $3$ représente :
- **A**: $300$
- `WARN_HINT_IS_FORMULA` step 2: _Il représente $3 \times 100 = ?$._

### curriculum — 6EME / Nombres_entiers (row 2, exo 8)
- **Q**: $0$ est un nombre pair.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 2: _$0 \div 2 = 0$, il n'y a pas de reste._

### curriculum — 6EME / Nombres_entiers (row 2, exo 9)
- **Q**: Un élève calcule : $48 \div 6 + 2 = 48 \div 8 = 6$. Où est l'erreur ?
- **A**: Il fallait d'abord diviser, puis additio
- `WARN_HINT_IS_FORMULA` step 2: _$48 \div 6 + 2 = 8 + 2 = 10$._

### curriculum — 6EME / Nombres_entiers (row 2, exo 11)
- **Q**: Quand on multiplie un nombre entier par $10$, que se passe-t-il ?
- **A**: On ajoute un zéro à droite
- `WARN_HINT_IS_FORMULA` step 3: _Exemple : $35 \times 10 = 350$._

### curriculum — 6EME / Nombres_entiers (row 2, exo 16)
- **Q**: Calcule $0{,}045 \times 1000$.
- **A**: 45
- `WARN_HINT_IS_ANSWER` step 2: _$0{,}045 \times 1000 = ?$._
- `WARN_HINT_IS_FORMULA` step 2: _$0{,}045 \times 1000 = ?$._

### curriculum — 6EME / Nombres_entiers (row 2, exo 17)
- **Q**: Une piste d'athlétisme fait $3\,600$ cm de long. Quelle est sa longueur en mètre
- **A**: 36
- `WARN_HINT_IS_FORMULA` step 2: _$3\,600 \div 100 = ?$ m._

### curriculum — 6EME / Nombres_entiers (row 2, exo 19)
- **Q**: Une bibliothèque veut ranger $250$ livres sur des étagères de $12$ places. Combi
- **A**: 21
- `WARN_HINT_IS_ANSWER` step 3: _Il faut $21$ étagères au total._
- `WARN_HINT_IS_FORMULA` step 1: _$250 \div 12 = 20$ reste $10$._

### curriculum — 6EME / Nombres_entiers (row 2, exo 20)
- **Q**: Dans $a = b \times 6 + 4$, si $a = 40$, alors $b =$ ___.
- **A**: 6
- `WARN_HINT_IS_FORMULA` step 2: _$b \times 6 = 40 - 4 = 36$._
- `WARN_HINT_IS_FORMULA` step 3: _$b = 36 \div ? = ?$._

### curriculum — 6EME / Proportionnalité (row 3, exo 2)
- **Q**: $4$ oranges coûtent $2$ €. Combien coûtent $6$ oranges ?
- **A**: 3 €
- `WARN_HINT_IS_FORMULA` step 1: _Prix d'une orange : $2 \div 4 = 0{,}50$ €._

### curriculum — 6EME / Proportionnalité (row 3, exo 3)
- **Q**: Si 3 cahiers coûtent 6 €, alors 6 cahiers coûtent 18 €.
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 1: _Prix d'un cahier : $6 \div 3 = 2$ €._
- `WARN_HINT_IS_FORMULA` step 2: _$6$ cahiers : $2 \times 6 = 12$ €, pas $18$ €._

### curriculum — 6EME / Proportionnalité (row 3, exo 4)
- **Q**: Un élève calcule : « 4 stylos coûtent 6 €. Pour 10 stylos : $6 + 10 = 16$ € ». O
- **A**: Il a additionné au lieu de multiplier pa
- `WARN_HINT_IS_FORMULA` step 1: _Prix d'un stylo : $6 \div 4 = 1{,}50$ €._
- `WARN_HINT_IS_FORMULA` step 2: _$10$ stylos : $1{,}50 \times 10 = 15$ €._

### curriculum — 6EME / Proportionnalité (row 3, exo 5)
- **Q**: 5 kg de pommes coûtent 10 €. Le prix au kilo est ___ €.
- **A**: 2
- `WARN_HINT_IS_FORMULA` step 2: _$10 \div 5 = ?$ €/kg._

### curriculum — 6EME / Proportionnalité (row 3, exo 6)
- **Q**: Calcule $25\%$ de $40$.
- **A**: 10
- `WARN_HINT_IS_ANSWER` step 1: _$25\% = \frac{25}{100} = \frac{1}{4}$._
- `WARN_HINT_IS_FORMULA` step 1: _$25\% = \frac{25}{100} = \frac{1}{4}$._
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{1}{4}$ de $40 = 40 \div 4 = ?$._

### curriculum — 6EME / Proportionnalité (row 3, exo 9)
- **Q**: Un jeu vidéo coûte $80$ € et bénéficie d'une réduction de $10\%$. Combien économ
- **A**: 8
- `WARN_HINT_IS_FORMULA` step 1: _$10\%$ de $80 = \frac{10}{100} \times 80 = ?$€._

### curriculum — 6EME / Proportionnalité (row 3, exo 10)
- **Q**: Sur un plan à l'échelle $\frac{1}{200}$, un mur de 6 m mesure ___ cm sur le plan
- **A**: 3
- `WARN_HINT_IS_FORMULA` step 3: _$600 \div 200 = ?$ cm._

### curriculum — 6EME / Proportionnalité (row 3, exo 11)
- **Q**: Une recette pour $4$ personnes demande $200$ g de farine. Quelle quantité pour $
- **A**: 400 g
- `WARN_HINT_IS_FORMULA` step 1: _Le coefficient est $8 \div 4 = 2$._

### curriculum — 6EME / Proportionnalité (row 3, exo 12)
- **Q**: Une recette pour $2$ personnes demande $6$ tomates. Combien de tomates faut-il p
- **A**: 15
- `WARN_HINT_IS_FORMULA` step 1: _Le coefficient est $5 \div 2 = 2{,}5$._
- `WARN_HINT_IS_FORMULA` step 2: _$6 \times 2{,}5 = ?$ tomates._

### curriculum — 6EME / Proportionnalité (row 3, exo 13)
- **Q**: $40\%$ de $650$ égale $260$.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 2: _$0{,}4 \times 650 = 260$._

### curriculum — 6EME / Proportionnalité (row 3, exo 14)
- **Q**: $7$ cahiers coûtent $8{,}40$ €. Quel est le prix de $3$ cahiers ?
- **A**: 3,60 €
- `WARN_HINT_IS_FORMULA` step 1: _Prix d'un cahier : $8{,}40 \div 7 = 1{,}20$ €._

### curriculum — 6EME / Proportionnalité (row 3, exo 15)
- **Q**: Au restaurant, l'addition est de $60$ €. Le pourboire de $15\%$ est de ___ €.
- **A**: 9
- `WARN_HINT_IS_FORMULA` step 2: _$0{,}15 \times 60 = ?$€._

### curriculum — 6EME / Proportionnalité (row 3, exo 17)
- **Q**: Un sac à dos coûte $45$ € avec $20\%$ de réduction. Combien économise-t-on ?
- **A**: 9
- `WARN_HINT_IS_FORMULA` step 1: _$20\%$ de $45 = \frac{20}{100} \times 45 = ?$€._

### curriculum — 6EME / Proportionnalité (row 3, exo 18)
- **Q**: Dans un tableau proportionnel, si $3 \to 7{,}5$ et $5 \to 12{,}5$, le coefficien
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _$7{,}5 \div 3 = 2{,}5$ et $12{,}5 \div 5 = 2{,}5$._

### curriculum — 6EME / Proportionnalité (row 3, exo 19)
- **Q**: Si $\frac{3}{4} = \frac{x}{12}$, calcule $x$.
- **A**: 9
- `WARN_HINT_IS_FORMULA` step 1: _$12 \div 4 = 3$, donc on multiplie le numérateur par $3$._
- `WARN_HINT_IS_FORMULA` step 2: _$3 \times 3 = ?$, donc $x = ?$._

### curriculum — 6EME / Géométrie (row 4, exo 5)
- **Q**: Le diamètre d'un cercle mesure $14$ cm. Son rayon est ___ cm.
- **A**: 7
- `WARN_HINT_IS_FORMULA` step 2: _$14 \div 2 = ?$ cm._

### curriculum — 6EME / Géométrie (row 4, exo 8)
- **Q**: Un triangle équilatéral a ses trois angles égaux à $60°$.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 2: _Si les 3 angles sont égaux : $180° \div 3 = 60°$._

### curriculum — 6EME / Géométrie (row 4, exo 9)
- **Q**: Un quadrilatère dont les diagonales se coupent en leur milieu est un :
- **A**: parallélogramme
- `WARN_HINT_IS_ANSWER` step 1: _La propriété « diagonales se coupant en leur milieu » caractérise le parallélogramme._

### curriculum — 6EME / Géométrie (row 4, exo 12)
- **Q**: Le terrain de foot de l'école a $4$ côtés. C'est un :
- **A**: quadrilatère
- `WARN_HINT_IS_ANSWER` step 1: _Un polygone à 4 côtés s'appelle un quadrilatère._

### curriculum — 6EME / Géométrie (row 4, exo 14)
- **Q**: Un arbre est planté à $4$ m d'une rivière rectiligne. Son reflet est le symétriq
- **A**: 8 m
- `WARN_HINT_IS_FORMULA` step 2: _Distance arbre-rivière = $4$ m, rivière-reflet = $4$ m._

### curriculum — 6EME / Géométrie (row 4, exo 15)
- **Q**: Une pizza ronde a un diamètre de $30$ cm. Son rayon est ___ cm.
- **A**: 15
- `WARN_HINT_IS_FORMULA` step 2: _$30 \div 2 = ?$ cm._

### curriculum — 6EME / Géométrie (row 4, exo 18)
- **Q**: Un cercle a un diamètre de $2r$. Si $r = 7$ cm, le diamètre est $14$ cm.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _$d = 2 \times r = 2 \times 7 = 14$ cm._

### curriculum — 6EME / Géométrie (row 4, exo 19)
- **Q**: Quel est le nombre de côtés d'un pentagone régulier, et son périmètre si chaque 
- **A**: 5 côtés, périmètre = 20 cm
- `WARN_HINT_IS_FORMULA` step 2: _Périmètre = $5 \times 4 = 20$ cm._

### curriculum — 6EME / Périmètres_Aires (row 5, exo 3)
- **Q**: Si on double le côté d'un carré, son périmètre double aussi.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 2: _Nouveau périmètre : $4 \times 2c = 8c = 2 \times 4c$._

### curriculum — 6EME / Périmètres_Aires (row 5, exo 4)
- **Q**: Un élève calcule l'aire d'un triangle de base 6 cm et hauteur 4 cm : $6 \times 4
- **A**: Il a oublié de diviser par 2
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{6 \times 4}{2} = \frac{24}{2} = 12$ cm$^2$._

### curriculum — 6EME / Périmètres_Aires (row 5, exo 5)
- **Q**: Un carreau de carrelage est un carré de côté $7$ cm. Son aire est ___ cm$^2$.
- **A**: 49
- `WARN_HINT_IS_FORMULA` step 2: _$7 \times 7 = ?$ cm$^2$._

### curriculum — 6EME / Périmètres_Aires (row 5, exo 7)
- **Q**: L'aire d'un triangle de base $b$ et de hauteur $h$ est :
- **A**: $\frac{b \times h}{2}$
- `WARN_HINT_IS_FORMULA` step 2: _$A = ?$._
- `WARN_HINT_TOO_SHORT` step 2: _$A = ?$._

### curriculum — 6EME / Périmètres_Aires (row 5, exo 8)
- **Q**: Si on double le côté d'un carré, son aire double aussi.
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 2: _Nouvelle aire : $(2c)^2 = 4c^2$._

### curriculum — 6EME / Périmètres_Aires (row 5, exo 9)
- **Q**: L'aire d'un disque de rayon 5 cm est $\pi \times$ ___.
- **A**: 25
- `WARN_HINT_IS_ANSWER` step 3: _L'aire est $\pi \times 25 \approx 78{,}5$ cm$^2$._
- `WARN_HINT_IS_FORMULA` step 2: _$r = 5$ cm, donc $r^2 = ?$._

### curriculum — 6EME / Périmètres_Aires (row 5, exo 10)
- **Q**: Le périmètre d'un cercle de diamètre 10 cm est $\pi \times$ ___. Complète le nom
- **A**: 10
- `WARN_HINT_IS_ANSWER` step 3: _Périmètre = $\pi \times 10 \approx 31{,}4$ cm._
- `WARN_HINT_IS_FORMULA` step 2: _$d = ?$ cm._

### curriculum — 6EME / Périmètres_Aires (row 5, exo 11)
- **Q**: Le périmètre d'un rectangle de longueur $L$ et largeur $l$ est :
- **A**: $2(L + l)$
- `WARN_HINT_IS_FORMULA` step 2: _$L + l + L + l = 2L + 2l = ?.$._

### curriculum — 6EME / Périmètres_Aires (row 5, exo 12)
- **Q**: Un potager carré a une aire de $64$ m$^2$. Quel est le côté de ce potager ?
- **A**: 8 m
- `WARN_HINT_IS_FORMULA` step 1: _Aire du carré = $c^2 = 64$._

### curriculum — 6EME / Périmètres_Aires (row 5, exo 14)
- **Q**: Un terrain triangulaire a une base de $20$ m et une hauteur de $15$ m. Quelle es
- **A**: 150 m²
- `WARN_HINT_IS_FORMULA` step 1: _$A = \frac{b \times h}{2} = \frac{20 \times 15}{2}$._

### curriculum — 6EME / Périmètres_Aires (row 5, exo 15)
- **Q**: Convertis $50\,000$ cm$^2$ en m$^2$. La réponse est ___ m$^2$.
- **A**: 5
- `WARN_HINT_IS_FORMULA` step 2: _$50\,000 \div 10\,000 = ?$ m$^2$._

### curriculum — 6EME / Périmètres_Aires (row 5, exo 16)
- **Q**: Une mini-pizza a un rayon de $3$ cm. Quelle est l'aire de cette pizza ? ($\pi \a
- **A**: 28,26 cm²
- `WARN_HINT_IS_FORMULA` step 1: _$A = \pi \times r^2 = 3{,}14 \times 3^2$._

### curriculum — 6EME / Périmètres_Aires (row 5, exo 17)
- **Q**: Calcule le périmètre d'un rectangle de longueur $9$ cm et de largeur $3{,}5$ cm.
- **A**: 25 cm
- `WARN_HINT_IS_FORMULA` step 1: _$P = 2(L + l) = 2(9 + 3{,}5)$._

### curriculum — 6EME / Périmètres_Aires (row 5, exo 20)
- **Q**: Un triangle a la même base ($10$ cm) et hauteur ($6$ cm) qu'un rectangle. L'aire
- **A**: 30
- `WARN_HINT_IS_FORMULA` step 1: _$A_{\text{triangle}} = \frac{b \times h}{2} = \frac{10 \times 6}{2}$._
- `WARN_HINT_IS_FORMULA` step 2: _$= \frac{60}{2} = ?$ cm$^2$._

### curriculum — 6EME / Angles (row 6, exo 2)
- **Q**: Deux angles complémentaires ont une somme de :
- **A**: 90°
- `WARN_HINT_IS_ANSWER` step 2: _Leur somme est $90°$._

### curriculum — 6EME / Angles (row 6, exo 4)
- **Q**: Un élève dit : « L'angle complémentaire de $65°$ est $180° - 65° = 115°$ ». Où e
- **A**: Il a confondu complémentaire (90°) et su
- `WARN_HINT_IS_FORMULA` step 1: _Complémentaire $\rightarrow$ somme = $90°$, supplémentaire $\rightarrow$ somme = $180°$._

### curriculum — 6EME / Angles (row 6, exo 9)
- **Q**: Deux angles opposés par le sommet sont toujours :
- **A**: égaux
- `WARN_HINT_IS_ANSWER` step 1: _Quand deux droites se coupent, les angles opposés sont égaux._

### curriculum — 6EME / Angles (row 6, exo 12)
- **Q**: Le toit d'une maison forme un triangle isocèle. L'angle au sommet mesure $40°$. 
- **A**: 70°
- `WARN_HINT_IS_FORMULA` step 1: _Somme = $180°$, angle au sommet = $40°$._
- `WARN_HINT_IS_FORMULA` step 3: _$140° \div 2 = ?$.._

### curriculum — 6EME / Angles (row 6, exo 13)
- **Q**: Deux angles supplémentaires ont pour somme $180°$.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 2: _$\alpha + \beta = 180°$._

### curriculum — 6EME / Angles (row 6, exo 15)
- **Q**: Dans un triangle, un angle mesure $2x$, un autre $x$ et le troisième $60°$. La v
- **A**: 40
- `WARN_HINT_IS_FORMULA` step 1: _$2x + x + 60° = 180°$._
- `WARN_HINT_IS_FORMULA` step 2: _$3x = 120°$._

### curriculum — 6EME / Angles (row 6, exo 19)
- **Q**: Deux angles supplémentaires : le plus grand est le double du plus petit. Quel es
- **A**: 60°
- `WARN_HINT_IS_FORMULA` step 1: _Soit $x$ le plus petit. Le plus grand = $2x$._
- `WARN_HINT_IS_FORMULA` step 2: _$x + 2x = 180°$, donc $3x = 180°$._
- `WARN_HINT_IS_FORMULA` step 3: _$x = ?.$._
- `WARN_HINT_TOO_SHORT` step 3: _$x = ?.$._

### curriculum — 5EME / Fractions (row 7, exo 1)
- **Q**: Calcule $\frac{1}{2} + \frac{1}{3}$.
- **A**: $\frac{5}{6}$
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{1}{2} = \frac{3}{6}$ et $\frac{1}{3} = \frac{2}{6}$_

### curriculum — 5EME / Fractions (row 7, exo 2)
- **Q**: Calcule $\frac{3}{4} - \frac{1}{3}$.
- **A**: $\frac{5}{12}$
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{3}{4} = \frac{9}{12}$ et $\frac{1}{3} = \frac{4}{12}$_

### curriculum — 5EME / Fractions (row 7, exo 3)
- **Q**: Une playlist contient $35$ morceaux. Les $\frac{2}{5}$ sont du rap. Combien de m
- **A**: 14
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{2}{5} \times 35 = \frac{2 \times 35}{5} = \frac{70}{5}$_
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{70}{5} = ?$ morceaux_

### curriculum — 5EME / Fractions (row 7, exo 5)
- **Q**: Complète : $\frac{5}{6} - \frac{1}{4} = \frac{\boxed{?}}{12}$
- **A**: 7
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{5}{6} = \frac{10}{12}$ et $\frac{1}{4} = \frac{3}{12}$_
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{10}{12} - \frac{3}{12} = \frac{7}{12}$_

### curriculum — 5EME / Fractions (row 7, exo 6)
- **Q**: Calcule $\frac{2}{3} + \frac{1}{6}$.
- **A**: $\frac{5}{6}$
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{2}{3} = \frac{4}{6}$_

### curriculum — 5EME / Fractions (row 7, exo 8)
- **Q**: Multiplier une fraction par un nombre entier ne change jamais le dénominateur.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _$\frac{a}{b} \times n = \frac{a \times n}{b}$_
- `WARN_DUPLICATE` step 1: _$\frac{a}{b} \times n = \frac{a \times n}{b}$_

### curriculum — 5EME / Fractions (row 7, exo 9)
- **Q**: Une recette pour $4$ personnes demande $20$ cl de lait. Quelle quantité faut-il 
- **A**: 15
- `WARN_HINT_IS_FORMULA` step 1: _Pour 1 personne : $\frac{20}{4} = 5$ cl_
- `WARN_HINT_IS_FORMULA` step 2: _Pour 3 personnes : $5 \times 3 = ?$ cl_

### curriculum — 5EME / Fractions (row 7, exo 10)
- **Q**: Complète : $\frac{15}{25}$ simplifié donne $\frac{3}{\boxed{?}}$
- **A**: 5
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{15 \div 5}{25 \div 5} = \frac{3}{5}$_

### curriculum — 5EME / Fractions (row 7, exo 11)
- **Q**: Complète : $\frac{3}{4} - \frac{1}{6}$. Le dénominateur commun le plus simple es
- **A**: 12
- `WARN_HINT_IS_ANSWER` step 1: _Multiples de 4 : 4, 8, 12, 16..._
- `WARN_HINT_IS_ANSWER` step 2: _Multiples de 6 : 6, 12, 18..._
- `WARN_HINT_IS_ANSWER` step 3: _Le plus petit commun multiple est $12$_

### curriculum — 5EME / Fractions (row 7, exo 12)
- **Q**: Calcule $5 \div \frac{1}{4}$.
- **A**: 20
- `WARN_HINT_IS_FORMULA` step 2: _$5 \times 4 = ?$_

### curriculum — 5EME / Fractions (row 7, exo 13)
- **Q**: $\frac{2}{5} \times \frac{3}{4} = \frac{6}{9}$
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 1: _On multiplie numérateurs : $2 \times 3 = 6$_
- `WARN_HINT_IS_FORMULA` step 2: _On multiplie dénominateurs : $5 \times 4 = 20$_
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{2}{5} \times \frac{3}{4} = \frac{6}{20} = \frac{3}{10}$, pas $\frac{6}{9}$_

### curriculum — 5EME / Fractions (row 7, exo 14)
- **Q**: Une planche mesure $\frac{3}{4}$ de mètre. On veut la couper en morceaux de $\fr
- **A**: 2
- `WARN_HINT_IS_FORMULA` step 1: _$\frac{3}{4} \div \frac{3}{8} = \frac{3}{4} \times \frac{8}{3}$_
- `WARN_HINT_IS_FORMULA` step 2: _$= \frac{3 \times 8}{4 \times 3} = \frac{24}{12}$_

### curriculum — 5EME / Fractions (row 7, exo 15)
- **Q**: Complète : $\frac{1}{2} \times \frac{2}{3} \times \frac{3}{4} = \frac{1}{\boxed{
- **A**: 4
- `WARN_HINT_IS_FORMULA` step 1: _Numérateurs : $1 \times 2 \times 3 = 6$_
- `WARN_HINT_IS_FORMULA` step 2: _Dénominateurs : $2 \times 3 \times 4 = 24$_
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{6}{24} = \frac{1}{4}$_

### curriculum — 5EME / Fractions (row 7, exo 18)
- **Q**: $\frac{x}{4} + 1 = 3$ donne $x = 12$.
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 1: _$\frac{x}{4} + 1 = 3$ donc $\frac{x}{4} = 2$_
- `WARN_HINT_IS_FORMULA` step 2: _$x = 2 \times 4 = 8$_
- `WARN_HINT_IS_FORMULA` step 3: _$x = 8$, pas $12$_

### curriculum — 5EME / Fractions (row 7, exo 19)
- **Q**: Un stade accueille $24$ équipes. Les $\frac{2}{3}$ sont qualifiées, et les $\fra
- **A**: 12
- `WARN_HINT_IS_FORMULA` step 1: _Qualifiées : $\frac{2}{3} \times 24 = 16$_
- `WARN_HINT_IS_FORMULA` step 2: _En finale : $\frac{3}{4} \times 16 = ?$_

### curriculum — 5EME / Fractions (row 7, exo 20)
- **Q**: Complète : une cuve remplie aux $\frac{2}{3}$, on ajoute $\frac{1}{4}$ de sa cap
- **A**: 11
- `WARN_HINT_IS_ANSWER` step 2: _$\frac{8}{12} + \frac{3}{12} = \frac{11}{12}$_
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{8}{12} + \frac{3}{12} = \frac{11}{12}$_

### curriculum — 5EME / Nombres_relatifs (row 8, exo 2)
- **Q**: Calcule $(-2) \times 3$.
- **A**: $-6$
- `WARN_HINT_IS_FORMULA` step 2: _$2 \times 3 = 6$_

### curriculum — 5EME / Nombres_relatifs (row 8, exo 4)
- **Q**: $(-4) \times (-3) = -12$
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 2: _$4 \times 3 = 12$_
- `WARN_HINT_IS_FORMULA` step 3: _$(-4) \times (-3) = +12$, pas $-12$_

### curriculum — 5EME / Nombres_relatifs (row 8, exo 5)
- **Q**: Complète : $(-5) \times (-4) = $ ___
- **A**: 20
- `WARN_HINT_IS_FORMULA` step 2: _$5 \times 4 = ?$_
- `WARN_HINT_IS_FORMULA` step 3: _$(-5) \times (-4) = ?$_

### curriculum — 5EME / Nombres_relatifs (row 8, exo 6)
- **Q**: Calcule $(-6) - (-2)$.
- **A**: $-4$
- `WARN_HINT_TOO_SHORT` step 3: _$= $?_

### curriculum — 5EME / Nombres_relatifs (row 8, exo 7)
- **Q**: Un plongeur est à $-3$ m et un autre à $-7$ m sous la surface. Lequel est le plu
- **A**: $-3$
- `WARN_HINT_IS_ANSWER` step 1: _$-3$ est plus proche de $0$ que $-7$_
- `WARN_HINT_IS_ANSWER` step 2: _Sur la droite graduée, $-3 > -7$_
- `WARN_HINT_IS_ANSWER` step 3: _Le plongeur à $-3$ m est plus haut_

### curriculum — 5EME / Nombres_relatifs (row 8, exo 10)
- **Q**: Complète : $(-3)^2 = $ ___
- **A**: 9
- `WARN_HINT_IS_FORMULA` step 3: _$3 \times 3 = ?$_

### curriculum — 5EME / Nombres_relatifs (row 8, exo 11)
- **Q**: Calcule $\frac{-12}{-3}$.
- **A**: $4$
- `WARN_HINT_IS_FORMULA` step 2: _$12 \div 3 = ?$_
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{-12}{-3} = ?$_

### curriculum — 5EME / Nombres_relatifs (row 8, exo 14)
- **Q**: Si $-x = 5$, quelle est la valeur de $x$ ?
- **A**: $-5$
- `WARN_HINT_IS_FORMULA` step 1: _$-x = 5$_
- `WARN_HINT_IS_FORMULA` step 3: _$x = $?_
- `WARN_HINT_TOO_SHORT` step 1: _$-x = 5$_
- `WARN_HINT_TOO_SHORT` step 3: _$x = $?_

### curriculum — 5EME / Nombres_relatifs (row 8, exo 15)
- **Q**: Complète : $(-1 + 2) \times (-3) = $ ___
- **A**: -3
- `WARN_HINT_IS_ANSWER` step 2: _$1 \times (-3) = ?$_
- `WARN_HINT_IS_FORMULA` step 2: _$1 \times (-3) = ?$_

### curriculum — 5EME / Nombres_relatifs (row 8, exo 16)
- **Q**: Complète : $(-6) \times \_ = 42$.
- **A**: $-7$
- `WARN_HINT_IS_ANSWER` step 3: _Vérification : $(-6) \times (-7) = 42$ ✓_
- `WARN_HINT_IS_FORMULA` step 1: _$(-6) \times ? = 42$_
- `WARN_HINT_IS_FORMULA` step 2: _$42 \div (-6) = ?$_
- `WARN_HINT_IS_FORMULA` step 3: _Vérification : $(-6) \times (-7) = 42$ ✓_

### curriculum — 5EME / Nombres_relatifs (row 8, exo 17)
- **Q**: Dans un jeu, on perd $2$ points par mauvaise réponse et on gagne $4$ points par 
- **A**: $2$
- `WARN_HINT_IS_FORMULA` step 1: _Bonnes : $3 \times 4 = 12$ points_
- `WARN_HINT_IS_FORMULA` step 2: _Mauvaises : $5 \times (-2) = -10$ points_

### curriculum — 5EME / Nombres_relatifs (row 8, exo 18)
- **Q**: $(-a) \times (-b) = ab$ pour $a = 2$ et $b = 3$ donne $6$.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 3: _$2 \times 3 = 6$ ✓_

### curriculum — 5EME / Proportionnalité (row 9, exo 1)
- **Q**: $3$ crayons coûtent $1{,}80$ €. Combien coûtent $5$ crayons ?
- **A**: $3$ €
- `WARN_HINT_IS_FORMULA` step 1: _Prix d'un crayon : $1{,}80 \div 3 = 0{,}60$ €_

### curriculum — 5EME / Proportionnalité (row 9, exo 2)
- **Q**: Calcule $15\%$ de $60$.
- **A**: $9$
- `WARN_HINT_IS_FORMULA` step 1: _$15\% = \frac{15}{100} = 0{,}15$_
- `WARN_HINT_IS_FORMULA` step 2: _$0{,}15 \times 60 = ?$_

### curriculum — 5EME / Proportionnalité (row 9, exo 3)
- **Q**: Des baskets coûtent $80$ € et sont soldées à $-20\%$. Combien économise-t-on ?
- **A**: $16$
- `WARN_HINT_IS_FORMULA` step 2: _$= 0{,}20 \times 80 = ?$€_

### curriculum — 5EME / Proportionnalité (row 9, exo 5)
- **Q**: Complète : sur $200$ réponses à un quiz, $25\%$ sont fausses. Nombre de réponses
- **A**: 50
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{25}{100} \times 200 = ?$_

### curriculum — 5EME / Proportionnalité (row 9, exo 6)
- **Q**: $4$ kg de pommes coûtent $6$ €. Prix de $7$ kg ?
- **A**: $10{,}50$ €
- `WARN_HINT_IS_FORMULA` step 1: _Prix au kg : $6 \div 4 = 1{,}50$ €_

### curriculum — 5EME / Proportionnalité (row 9, exo 9)
- **Q**: Une augmentation de $10\%$ suivie d'une diminution de $10\%$ ramène-t-elle au pr
- **A**: Non
- `WARN_HINT_IS_FORMULA` step 2: _$110$ € $-10\% \rightarrow 110 \times 0{,}9 = 99$ €_

### curriculum — 5EME / Proportionnalité (row 9, exo 11)
- **Q**: Un pull de $80$ € est soldé à $-30\%$. Un élève calcule $80 - 30 = 50$ €. Où est
- **A**: Il a soustrait 30 au lieu de calculer 30
- `WARN_HINT_IS_FORMULA` step 1: _$30\%$ de $80 = 0{,}30 \times 80 = 24$ €_

### curriculum — 5EME / Proportionnalité (row 9, exo 13)
- **Q**: Le prix d'un abonnement augmente de $20\%$ puis de $10\%$. L'augmentation totale
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 3: _Total : $1{,}2 \times 1{,}1 = 1{,}32$, soit $+32\%$, pas $30\%$_

### curriculum — 5EME / Proportionnalité (row 9, exo 14)
- **Q**: Prix passe de $40$ € à $50$ €. Taux d'évolution ?
- **A**: $25\%$
- `WARN_HINT_IS_FORMULA` step 2: _Taux : $\frac{10}{40} = 0{,}25$_

### curriculum — 5EME / Proportionnalité (row 9, exo 15)
- **Q**: Complète : Thomas roule $2$ h à $70$ km/h puis $1$ h à $90$ km/h. Distance total
- **A**: 230
- `WARN_HINT_IS_FORMULA` step 1: _$2 \times 70 = 140$ km_
- `WARN_HINT_IS_FORMULA` step 2: _$1 \times 90 = 90$ km_

### curriculum — 5EME / Proportionnalité (row 9, exo 16)
- **Q**: $4$ ouvriers finissent un chantier en $6$ jours. En combien de jours $3$ ouvrier
- **A**: $8$ jours
- `WARN_HINT_IS_FORMULA` step 1: _$4 \times 6 = 24$ jours-ouvrier au total_

### curriculum — 5EME / Proportionnalité (row 9, exo 17)
- **Q**: Sur une carte à l'échelle $\frac{1}{25\,000}$, le sentier mesure $8$ cm. Distanc
- **A**: $2$ km
- `WARN_HINT_IS_FORMULA` step 1: _$8 \times 25\,000 = 200\,000$ cm_

### curriculum — 5EME / Proportionnalité (row 9, exo 18)
- **Q**: $150$ g de sel dans $600$ g d'eau donnent une concentration de $20\%$.
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 2: _Concentration : $\frac{150}{750} = 0{,}2 = 20\%$_
- `WARN_HINT_IS_FORMULA` step 3: _Attention : si on considère la concentration dans l'eau seule : $\frac{150}{600} = 25\%$, pas $20\%$_

### curriculum — 5EME / Proportionnalité (row 9, exo 19)
- **Q**: $120$ € partagés dans le rapport $2:3:5$. Quelle est la plus grande part ?
- **A**: $60$ €
- `WARN_HINT_IS_FORMULA` step 2: _Valeur d'une part : $120 \div 10 = 12$ €_

### curriculum — 5EME / Proportionnalité (row 9, exo 20)
- **Q**: Complète : $3$ robinets remplissent une piscine en $12$ h. Avec $4$ robinets : _
- **A**: 9
- `WARN_HINT_IS_FORMULA` step 1: _$3 \times 12 = 36$ robinets-heures_
- `WARN_HINT_IS_FORMULA` step 2: _$4$ robinets : $36 \div 4 = ?$ h_

### curriculum — 5EME / Puissances (row 10, exo 1)
- **Q**: Calcule $3^4$.
- **A**: $81$
- `WARN_HINT_IS_FORMULA` step 2: _$= 9 \times 9 = ?$_

### curriculum — 5EME / Puissances (row 10, exo 2)
- **Q**: Que vaut $7^0$ ?
- **A**: $1$
- `WARN_HINT_TOO_SHORT` step 2: _$7^0 = $?_

### curriculum — 5EME / Puissances (row 10, exo 4)
- **Q**: $2^4 = 8$
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 2: _$= 4 \times 4 = 16$_

### curriculum — 5EME / Puissances (row 10, exo 5)
- **Q**: Complète : $(-2)^3 = $ ___
- **A**: -8
- `WARN_HINT_IS_FORMULA` step 2: _$= 4 \times (-2) = ?$_

### curriculum — 5EME / Puissances (row 10, exo 6)
- **Q**: Calcule $2^6$.
- **A**: $64$
- `WARN_HINT_TOO_SHORT` step 2: _$= $?_

### curriculum — 5EME / Puissances (row 10, exo 7)
- **Q**: Calcule $(-3)^2$.
- **A**: $9$
- `WARN_HINT_TOO_SHORT` step 3: _$= $?_

### curriculum — 5EME / Puissances (row 10, exo 8)
- **Q**: $5^2 = 10$
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 1: _$5^2 = 5 \times 5 = 25$_

### curriculum — 5EME / Puissances (row 10, exo 9)
- **Q**: $(ab)^3 = $ ?
- **A**: $a^3 \times b^3$
- `WARN_HINT_IS_FORMULA` step 1: _$(ab)^3 = ab \times ab \times ab$_
- `WARN_HINT_TOO_SHORT` step 3: _$= ?$_

### curriculum — 5EME / Puissances (row 10, exo 10)
- **Q**: Complète : $(-2)^4 = $ ___
- **A**: 16
- `WARN_HINT_IS_FORMULA` step 2: _$= 4 \times 4 = ?$_

### curriculum — 5EME / Puissances (row 10, exo 11)
- **Q**: Simplifie $3^2 \times 3^4$.
- **A**: $3^6$
- `WARN_HINT_IS_FORMULA` step 2: _$3^2 \times 3^4 = 3^{2+4} = ?$._

### curriculum — 5EME / Puissances (row 10, exo 12)
- **Q**: Simplifie $(2^3)^2$.
- **A**: $2^6$
- `WARN_HINT_IS_FORMULA` step 2: _$(2^3)^2 = 2^{3 \times 2} = ?$._

### curriculum — 5EME / Puissances (row 10, exo 13)
- **Q**: $\frac{5^6}{5^2} = 5^3$
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 1: _$\frac{5^6}{5^2} = 5^{6-2} = 5^4$_
- `WARN_HINT_IS_FORMULA` step 2: _$5^4 = 625 \neq 5^3 = 125$_

### curriculum — 5EME / Puissances (row 10, exo 14)
- **Q**: La distance entre deux villes est de $45\,000$ m. En notation scientifique ?
- **A**: $4{,}5\times10^4$
- `WARN_HINT_IS_ANSWER` step 2: _$= 4{,}5 \times 10^4$_

### curriculum — 5EME / Puissances (row 10, exo 15)
- **Q**: Complète : en informatique, $1$ Ko $= 2^{10}$ octets $= $ ___ octets
- **A**: 1024
- `WARN_HINT_IS_FORMULA` step 2: _$2^{10} = 2^5 \times 2^5 = 32 \times 32 = 1\,024$_
- `WARN_DUPLICATE` step 1: _$2^{10} = 1\,024$_

### curriculum — 5EME / Puissances (row 10, exo 16)
- **Q**: Calcule $(3 \times 10^4) \times (2 \times 10^3)$.
- **A**: $6\times10^7$
- `WARN_HINT_IS_ANSWER` step 3: _$= 6 \times 10^7$_
- `WARN_HINT_IS_FORMULA` step 1: _Coefficients : $3 \times 2 = 6$_
- `WARN_HINT_IS_FORMULA` step 2: _Puissances de 10 : $10^4 \times 10^3 = 10^7$_

### curriculum — 5EME / Puissances (row 10, exo 17)
- **Q**: Calcule $\frac{8 \times 10^5}{4 \times 10^2}$.
- **A**: $2\times10^3$
- `WARN_HINT_IS_ANSWER` step 3: _$= 2 \times 10^3$_
- `WARN_HINT_IS_FORMULA` step 1: _Coefficients : $\frac{8}{4} = 2$_

### curriculum — 5EME / Puissances (row 10, exo 18)
- **Q**: $2^{10}$ est plus grand que $10^3$.
- **A**: Vrai
- `WARN_DUPLICATE` step 1: _$2^{10} = 1\,024$_

### curriculum — 5EME / Puissances (row 10, exo 19)
- **Q**: Simplifie $(a^3)^4$.
- **A**: $a^{12}$
- `WARN_HINT_IS_FORMULA` step 2: _$(a^3)^4 = a^{3 \times 4} = ?$_

### curriculum — 5EME / Puissances (row 10, exo 20)
- **Q**: Complète : un parallélépipède de dimensions $2^3$ cm, $3^3$ cm et $1$ cm a un pr
- **A**: 216
- `WARN_HINT_IS_FORMULA` step 3: _$8 \times 27 \times 1 = ?$ cm^3_
- `WARN_HINT_TOO_SHORT` step 1: _$2^3 = 8$_

### curriculum — 5EME / Pythagore (row 11, exo 1)
- **Q**: Une échelle est posée à $3$ m du mur. Elle touche le mur à $4$ m de hauteur. Que
- **A**: $5$ m
- `WARN_HINT_IS_FORMULA` step 2: _$c^2 = 3^2 + 4^2 = 9 + 16 = 25$_

### curriculum — 5EME / Pythagore (row 11, exo 2)
- **Q**: Triangle rectangle, côtés $5$ cm et $12$ cm. Calcule l'hypoténuse.
- **A**: $13$ cm
- `WARN_HINT_IS_FORMULA` step 1: _$c^2 = 5^2 + 12^2 = 25 + 144 = 169$_

### curriculum — 5EME / Pythagore (row 11, exo 3)
- **Q**: Un terrain rectangulaire mesure $6$ m par $8$ m. Quelle est la longueur de sa di
- **A**: $10$ m
- `WARN_HINT_IS_FORMULA` step 2: _$d^2 = 6^2 + 8^2 = 36 + 64 = 100$_

### curriculum — 5EME / Pythagore (row 11, exo 5)
- **Q**: Complète : triangle rectangle, côtés $8$ cm et $15$ cm. Hypoténuse = ___ cm
- **A**: 17
- `WARN_HINT_IS_FORMULA` step 1: _$c^2 = 8^2 + 15^2 = 64 + 225 = 289$_
- `WARN_HINT_IS_FORMULA` step 2: _$c = \sqrt{289} = ?$ cm_

### curriculum — 5EME / Pythagore (row 11, exo 6)
- **Q**: Triangle rectangle, côtés $7$ cm et $24$ cm. Calcule l'hypoténuse.
- **A**: $25$ cm
- `WARN_HINT_IS_FORMULA` step 1: _$c^2 = 7^2 + 24^2 = 49 + 576 = 625$_

### curriculum — 5EME / Pythagore (row 11, exo 7)
- **Q**: Triangle rectangle, côtés $9$ cm et $40$ cm. Calcule l'hypoténuse.
- **A**: $41$ cm
- `WARN_HINT_IS_FORMULA` step 1: _$c^2 = 9^2 + 40^2 = 81 + 1600 = 1681$_

### curriculum — 5EME / Pythagore (row 11, exo 10)
- **Q**: Complète : le triplet pythagoricien le plus connu est $3$, $4$, ___
- **A**: 5
- `WARN_HINT_IS_FORMULA` step 2: _$\sqrt{25} = ?$_

### curriculum — 5EME / Pythagore (row 11, exo 11)
- **Q**: Un menuisier vérifie une étagère : la diagonale mesure $10$ cm et la largeur $6$
- **A**: $8$ cm
- `WARN_HINT_IS_FORMULA` step 1: _$h^2 = 10^2 - 6^2 = 100 - 36 = 64$_

### curriculum — 5EME / Pythagore (row 11, exo 12)
- **Q**: Hypoténuse $17$ cm, un côté $8$ cm. Calcule l'autre côté.
- **A**: $15$ cm
- `WARN_HINT_IS_FORMULA` step 1: _$b^2 = 17^2 - 8^2 = 289 - 64 = 225$_

### curriculum — 5EME / Pythagore (row 11, exo 14)
- **Q**: Échelle de $5$ m, pied à $3$ m du mur. À quelle hauteur touche-t-elle le mur ?
- **A**: $4$ m
- `WARN_HINT_IS_FORMULA` step 1: _$h^2 = 5^2 - 3^2 = 25 - 9 = 16$_

### curriculum — 5EME / Pythagore (row 11, exo 15)
- **Q**: Complète : hypoténuse $25$ cm, un côté $7$ cm. L'autre côté = ___ cm
- **A**: 24
- `WARN_HINT_IS_FORMULA` step 1: _$b^2 = 25^2 - 7^2 = 625 - 49 = 576$_
- `WARN_HINT_IS_FORMULA` step 2: _$b = \sqrt{576} = ?$ cm_

### curriculum — 5EME / Pythagore (row 11, exo 16)
- **Q**: Un écran de tablette mesure $12$ cm de large et $5$ cm de haut. Quelle est la di
- **A**: $13$ cm
- `WARN_HINT_IS_FORMULA` step 1: _$d^2 = 12^2 + 5^2 = 144 + 25 = 169$_

### curriculum — 5EME / Pythagore (row 11, exo 17)
- **Q**: Dans un triangle rectangle en $C$ : $AC = 9$ cm, $AB = 15$ cm (hypoténuse). Calc
- **A**: $12$ cm
- `WARN_HINT_IS_FORMULA` step 1: _$BC^2 = AB^2 - AC^2 = 225 - 81 = 144$_

### curriculum — 5EME / Pythagore (row 11, exo 19)
- **Q**: Un triangle isocèle a des côtés égaux de $13$ cm et une base de $10$ cm. Quelle 
- **A**: $12$ cm
- `WARN_HINT_IS_FORMULA` step 2: _$h^2 = 13^2 - 5^2 = 169 - 25 = 144$_

### curriculum — 5EME / Pythagore (row 11, exo 20)
- **Q**: Complète : un élève cherche l'hypoténuse d'un triangle de côtés $6$ et $8$. Il c
- **A**: 10
- `WARN_HINT_IS_ANSWER` step 1: _$6^2 + 8^2 = 36 + 64 = 100$_
- `WARN_HINT_IS_ANSWER` step 2: _$\sqrt{100} = ?$_
- `WARN_HINT_IS_FORMULA` step 2: _$\sqrt{100} = ?$_

### curriculum — 5EME / Calcul_Littéral (row 12, exo 1)
- **Q**: Réduis $3x + 2x$.
- **A**: $5x$
- `WARN_HINT_IS_FORMULA` step 2: _$3x + 2x = (3+2)x = ?$._

### curriculum — 5EME / Calcul_Littéral (row 12, exo 2)
- **Q**: Réduis $4a - a$.
- **A**: $3a$
- `WARN_HINT_IS_FORMULA` step 1: _$4a - a = 4a - 1a$_
- `WARN_HINT_IS_FORMULA` step 2: _$= (4-1)a = ?$._

### curriculum — 5EME / Calcul_Littéral (row 12, exo 3)
- **Q**: L'entrée d'un parc coûte $3$ € plus $2$ € par tour de manège. Si on fait $x = 5$
- **A**: $13$
- `WARN_HINT_IS_FORMULA` step 2: _Pour $x = 5$ : $3 + 2 \times 5 = 3 + 10 = ?$€_

### curriculum — 5EME / Calcul_Littéral (row 12, exo 4)
- **Q**: $3x + 2x = 5x^2$
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 1: _$3x + 2x = 5x$ (on additionne les coefficients)_

### curriculum — 5EME / Calcul_Littéral (row 12, exo 5)
- **Q**: Complète : $2x + 3 + 5x - 1 = $ ___$x + 2$
- **A**: 7
- `WARN_HINT_IS_FORMULA` step 1: _Regrouper les termes en $x$ : $2x + 5x = 7x$_

### curriculum — 5EME / Calcul_Littéral (row 12, exo 6)
- **Q**: Calcule $x^2 - 1$ pour $x = 3$.
- **A**: $8$
- `WARN_HINT_IS_FORMULA` step 1: _$x^2 - 1$ pour $x = 3$_

### curriculum — 5EME / Calcul_Littéral (row 12, exo 7)
- **Q**: On achète $3$ packs contenant chacun $(x + 2)$ bouteilles. Pour $x = 1$, combien
- **A**: $9$
- `WARN_HINT_IS_FORMULA` step 1: _$3(x+2)$ pour $x = 1$_
- `WARN_HINT_IS_FORMULA` step 2: _$3 \times (1+2) = 3 \times 3 = ?$_

### curriculum — 5EME / Calcul_Littéral (row 12, exo 8)
- **Q**: $2(x + 3) = 2x + 3$
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 1: _$2(x+3) = 2 \times x + 2 \times 3 = 2x + 6$_

### curriculum — 5EME / Calcul_Littéral (row 12, exo 10)
- **Q**: Complète : un élève développe $5(2x - 3) = 10x - $ ___
- **A**: 15
- `WARN_HINT_IS_ANSWER` step 2: _$5 \times (-3) = -15$_
- `WARN_HINT_IS_ANSWER` step 3: _$5(2x - 3) = 10x - 15$_
- `WARN_HINT_IS_FORMULA` step 1: _$5 \times 2x = 10x$_
- `WARN_HINT_IS_FORMULA` step 2: _$5 \times (-3) = -15$_
- `WARN_HINT_IS_FORMULA` step 3: _$5(2x - 3) = 10x - 15$_

### curriculum — 5EME / Calcul_Littéral (row 12, exo 11)
- **Q**: Complète : $4x - 7 + 2x + 3 = $ ?
- **A**: $6x - 4$
- `WARN_HINT_IS_FORMULA` step 1: _Termes en $x$ : $4x + 2x = 6x$_
- `WARN_HINT_TOO_SHORT` step 3: _$= ?$._

### curriculum — 5EME / Calcul_Littéral (row 12, exo 12)
- **Q**: Si $x = 3$, calcule $2x^2 - 5x + 1$.
- **A**: $4$
- `WARN_HINT_IS_FORMULA` step 2: _$= 2 \times 9 - 15 + 1 = 18 - 15 + 1$_
- `WARN_HINT_TOO_SHORT` step 3: _$= $?_

### curriculum — 5EME / Calcul_Littéral (row 12, exo 13)
- **Q**: $x(x + 4)$ est la forme factorisée de $x^2 + 4x$.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _$x(x + 4) = x \times x + x \times 4 = x^2 + 4x$ ✓_

### curriculum — 5EME / Calcul_Littéral (row 12, exo 14)
- **Q**: Factorise $6a + 9$.
- **A**: $3(2a + 3)$
- `WARN_HINT_IS_FORMULA` step 2: _$6a \div 3 = 2a$, $9 \div 3 = 3$_
- `WARN_HINT_IS_FORMULA` step 3: _$6a + 9 = ?$._

### curriculum — 5EME / Calcul_Littéral (row 12, exo 15)
- **Q**: Complète : $\frac{3(x+2)}{3} = x + $ ___
- **A**: 2
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{3(x+2)}{3} = x + 2$_

### curriculum — 5EME / Calcul_Littéral (row 12, exo 16)
- **Q**: On dispose des chaises en $n = 5$ rangées de $n + 1 = 6$ chaises. Combien de cha
- **A**: $30$
- `WARN_HINT_IS_FORMULA` step 1: _$n \times (n+1)$ pour $n = 5$_
- `WARN_HINT_IS_FORMULA` step 2: _$5 \times 6 = ?$ chaises_

### curriculum — 5EME / Calcul_Littéral (row 12, exo 17)
- **Q**: Développe et réduis $(x + 1)^2 + (x - 1)^2$.
- **A**: $2x^2 + 2$
- `WARN_HINT_IS_ANSWER` step 3: _Somme : $2x^2 + 2$_
- `WARN_HINT_IS_FORMULA` step 1: _$(x+1)^2 = x^2 + 2x + 1$_
- `WARN_HINT_IS_FORMULA` step 2: _$(x-1)^2 = x^2 - 2x + 1$_

### curriculum — 5EME / Calcul_Littéral (row 12, exo 18)
- **Q**: $(x + 2)^2 - (x - 2)^2 = 8x$
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _$(x+2)^2 = x^2 + 4x + 4$_
- `WARN_HINT_IS_FORMULA` step 2: _$(x-2)^2 = x^2 - 4x + 4$_
- `WARN_HINT_IS_FORMULA` step 3: _Différence : $x^2 + 4x + 4 - x^2 + 4x - 4 = 8x$ ✓_

### curriculum — 5EME / Calcul_Littéral (row 12, exo 19)
- **Q**: Un parterre de fleurs mesure $(x + 3)$ m de long et $(x - 1)$ m de large. Pour $
- **A**: $21$
- `WARN_HINT_IS_FORMULA` step 3: _Aire : $7 \times 3 = ?$ m^2_

### curriculum — 5EME / Calcul_Littéral (row 12, exo 20)
- **Q**: Complète : factorise $4x^2 - 9 = (2x - 3)(2x + $ ___ $)$
- **A**: 3
- `WARN_HINT_IS_FORMULA` step 1: _$4x^2 - 9 = (2x)^2 - 3^2$_
- `WARN_HINT_IS_FORMULA` step 2: _Identité remarquable : $a^2 - b^2 = (a-b)(a+b)$_

### curriculum — 6EME / Nombres_Décimaux (row 13, exo 7)
- **Q**: Calculer $3{,}2 \times 4$.
- **A**: 12,8
- `WARN_HINT_IS_FORMULA` step 1: _$32 \times 4 = 128$._

### curriculum — 6EME / Nombres_Décimaux (row 13, exo 9)
- **Q**: Un coureur parcourt $7{,}8$ km en une heure. S'il court pendant $1{,}3$ heure, q
- **A**: 10,14
- `WARN_HINT_IS_FORMULA` step 1: _$d = v \times t = 7{,}8 \times 1{,}3$_
- `WARN_HINT_IS_FORMULA` step 2: _$78 \times 13 = 1014$, $2$ décimales au total._

### curriculum — 6EME / Nombres_Décimaux (row 13, exo 10)
- **Q**: $6{,}7 \times 100 =$ ___.
- **A**: 670
- `WARN_HINT_IS_FORMULA` step 2: _$6{,}7 \times 100 = ?$._

### curriculum — 6EME / Nombres_Décimaux (row 13, exo 11)
- **Q**: Convertir $0{,}75$ en fraction irréductible.
- **A**: 3/4
- `WARN_HINT_IS_FORMULA` step 2: _On simplifie par $25$ : $\frac{75 \div 25}{100 \div 25} = \frac{3}{4}$._

### curriculum — 6EME / Nombres_Décimaux (row 13, exo 14)
- **Q**: Hugo a $12{,}60$ € et achète $4$ gommes à $0{,}85$ € chacune. Combien lui reste-
- **A**: 9,20 €
- `WARN_HINT_IS_FORMULA` step 1: _$4 \times 0{,}85 = 3{,}40$ €._

### curriculum — 6EME / Nombres_Décimaux (row 13, exo 17)
- **Q**: Un carré de mosaïque a un côté de $2{,}5$ cm. Quelle est son aire ?
- **A**: 6,25
- `WARN_HINT_IS_FORMULA` step 1: _$A = c^2 = 2{,}5 \times 2{,}5$._
- `WARN_HINT_IS_FORMULA` step 2: _$25 \times 25 = 625$, $2$ décimales $\rightarrow$ $6{,}25$ cm$^2$._

### curriculum — 6EME / Nombres_Décimaux (row 13, exo 18)
- **Q**: $\frac{1}{3} \approx 0{,}33$ à $0{,}01$ près.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _$\frac{1}{3} = 0{,}333...$_

### curriculum — 6EME / Nombres_Décimaux (row 13, exo 19)
- **Q**: Sur $1\,000$ m de route, des ouvriers ont asphalté $0{,}375$ de la route. Quelle
- **A**: 625 m
- `WARN_HINT_IS_FORMULA` step 1: _Partie asphaltée : $0{,}375 \times 1000 = 375$ m_

### curriculum — 6EME / Statistiques_6ème (row 14, exo 2)
- **Q**: Hugo a obtenu les notes : $12$, $14$, $10$, $16$, $8$. Quelle est sa moyenne ?
- **A**: 12
- `WARN_HINT_IS_ANSWER` step 1: _Somme : $12 + 14 + 10 + 16 + 8 = 60$._
- `WARN_HINT_IS_FORMULA` step 2: _$5$ notes, donc moyenne = $60 \div 5 = ?$._

### curriculum — 6EME / Statistiques_6ème (row 14, exo 3)
- **Q**: La moyenne de 10, 10 et 10 est 10.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _$(10 + 10 + 10) \div 3 = 30 \div 3 = 10$._

### curriculum — 6EME / Statistiques_6ème (row 14, exo 4)
- **Q**: Un élève calcule la moyenne de 8, 12, 14 : $(8+12+14) \div 2 = 17$. Où est l'err
- **A**: Il a divisé par 2 au lieu de 3
- `WARN_HINT_IS_FORMULA` step 2: _$(8 + 12 + 14) \div 3 = 34 \div 3 \approx 11{,}3$._

### curriculum — 6EME / Statistiques_6ème (row 14, exo 5)
- **Q**: Voici les températures pendant $6$ jours (en °C) : $4$, $9$, $2$, $7$, $11$, $5$
- **A**: 9
- `WARN_HINT_IS_FORMULA` step 2: _Max = $11$, min = $2$._

### curriculum — 6EME / Statistiques_6ème (row 14, exo 6)
- **Q**: Dans une classe de 25 élèves, 10 ont eu plus de 15/20. Quelle est la fréquence (
- **A**: 40 %
- `WARN_HINT_IS_FORMULA` step 1: _Fréquence = $\frac{10}{25} = 0{,}4 = 40\%$._

### curriculum — 6EME / Statistiques_6ème (row 14, exo 9)
- **Q**: La moyenne de 5, 9 et 13 est :
- **A**: 9
- `WARN_HINT_IS_FORMULA` step 1: _$(5 + ? + 13) \div 3 = 27 \div 3 = ?$._

### curriculum — 6EME / Statistiques_6ème (row 14, exo 10)
- **Q**: Pour calculer l'étendue d'une série, on fait valeur ___ moins valeur ___. Écris 
- **A**: maximale
- `WARN_HINT_IS_ANSWER` step 1: _Étendue = valeur maximale − valeur minimale._

### curriculum — 6EME / Statistiques_6ème (row 14, exo 11)
- **Q**: Un diagramme en barres montre : lundi 12 absents, mardi 8, mercredi 5. Quel jour
- **A**: Lundi
- `WARN_HINT_IS_ANSWER` step 2: _Lundi a le plus d'absences._

### curriculum — 6EME / Statistiques_6ème (row 14, exo 12)
- **Q**: Emma a une moyenne de $13$ sur $6$ contrôles. Quelle est la somme de toutes ses 
- **A**: 78
- `WARN_HINT_IS_FORMULA` step 2: _Somme = moyenne $\times$ nombre = $13 \times 6 = ?$._

### curriculum — 6EME / Statistiques_6ème (row 14, exo 14)
- **Q**: Une enquête porte sur les repas préférés de 40 élèves. Le secteur pour « pasta »
- **A**: 10
- `WARN_HINT_IS_FORMULA` step 1: _$\frac{90°}{360°} = \frac{1}{4}$._

### curriculum — 6EME / Statistiques_6ème (row 14, exo 16)
- **Q**: Une classe a une moyenne de 12 avec 20 élèves. Une autre a une moyenne de 15 ave
- **A**: 13
- `WARN_HINT_IS_FORMULA` step 1: _Somme classe 1 : $12 \times 20 = 240$._
- `WARN_HINT_IS_FORMULA` step 2: _Somme classe 2 : $15 \times 10 = 150$._
- `WARN_HINT_IS_FORMULA` step 3: _Moyenne générale : $(240 + 150) \div 30 = ?$._

### curriculum — 6EME / Statistiques_6ème (row 14, exo 18)
- **Q**: Dans une série de 11 valeurs, la médiane est la 6ème valeur quand la série est o
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{11+1}{2} = 6$, c'est la 6ème valeur._

### curriculum — 6EME / Statistiques_6ème (row 14, exo 20)
- **Q**: Sur un diagramme en bâtons : A=15, B=?, C=10, D=5. La fréquence de B est $25\%$ 
- **A**: 10
- `WARN_HINT_IS_ANSWER` step 1: _$25\%$ de $40 = \frac{25}{100} \times 40 = ?$._
- `WARN_HINT_IS_ANSWER` step 2: _L'effectif de B est $10$._
- `WARN_HINT_IS_FORMULA` step 1: _$25\%$ de $40 = \frac{25}{100} \times 40 = ?$._

### curriculum — 6EME / Symétrie_Axiale (row 15, exo 2)
- **Q**: Le symétrique du point $A(2, 3)$ par rapport à l'axe des ordonnées est :
- **A**: A'(-2, 3)
- `WARN_HINT_IS_FORMULA` step 1: _L'axe des ordonnées est la droite $x = 0$._

### curriculum — 6EME / Symétrie_Axiale (row 15, exo 5)
- **Q**: Combien d'axes de symétrie possède un cercle ? Réponse : ___ (écris le mot).
- **A**: infini
- `WARN_HINT_IS_ANSWER` step 2: _Il y a une infinité de diamètres possibles._

### curriculum — 6EME / Symétrie_Axiale (row 15, exo 6)
- **Q**: Le symétrique du point $B(4, -1)$ par rapport à l'axe des abscisses est :
- **A**: B'(4, 1)
- `WARN_HINT_IS_FORMULA` step 1: _L'axe des abscisses est $y = 0$._

### curriculum — 6EME / Symétrie_Axiale (row 15, exo 7)
- **Q**: Quel est le symétrique du point $M(0, 5)$ par rapport à l'axe horizontal ?
- **A**: M'(0, -5)
- `WARN_HINT_IS_FORMULA` step 1: _Axe horizontal = axe des abscisses ($y = 0$)._

### curriculum — 6EME / Symétrie_Axiale (row 15, exo 15)
- **Q**: Le symétrique du point $P(-3, 5)$ par rapport à la droite $x = 1$ est $P'(a, 5)$
- **A**: 5
- `WARN_HINT_IS_FORMULA` step 1: _Distance de $P$ à l'axe $x=1$ : $|{-3} - 1| = 4$._

### curriculum — 6EME / Symétrie_Axiale (row 15, exo 17)
- **Q**: Si $A(2, 1)$ a pour symétrique $A'(8, 1)$ par rapport à un axe vertical, quelle 
- **A**: x = 5
- `WARN_HINT_IS_ANSWER` step 3: _L'axe est $x = 5$._
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{2+8}{2} = 5$._
- `WARN_HINT_IS_FORMULA` step 3: _L'axe est $x = 5$._

### curriculum — 6EME / Symétrie_Axiale (row 15, exo 19)
- **Q**: Quelle est la distance entre $M(2, 3)$ et son symétrique $M'$ par rapport à l'ax
- **A**: 0 (M est sur l'axe)
- `WARN_HINT_IS_FORMULA` step 1: _$M(2, 3)$ a $y = 3$, qui est exactement sur l'axe $y = 3$._

### curriculum — 5EME / Symétrie_Centrale (row 16, exo 1)
- **Q**: Le symétrique du point $A(2, 5)$ par rapport à l'origine $O(0, 0)$ est :
- **A**: $A'(-2, -5)$
- `WARN_HINT_IS_ANSWER` step 3: _$A'(-2, -5)$_
- `WARN_HINT_IS_FORMULA` step 2: _$x' = -2$, $y' = -5$_

### curriculum — 5EME / Symétrie_Centrale (row 16, exo 2)
- **Q**: Le symétrique du point $B(-3, 4)$ par rapport à l'origine $O$ est :
- **A**: $B'(3, -4)$
- `WARN_HINT_IS_ANSWER` step 3: _$B'(3, -4)$_
- `WARN_HINT_IS_FORMULA` step 2: _$x' = 3$, $y' = -4$_

### curriculum — 5EME / Symétrie_Centrale (row 16, exo 5)
- **Q**: Complète : le symétrique de $C(0, -3)$ par rapport à $O(0, 0)$ est $C'(0,$ ___$)
- **A**: 3
- `WARN_HINT_IS_FORMULA` step 2: _$x' = 0$, $y' = -(-?) = $?_

### curriculum — 5EME / Symétrie_Centrale (row 16, exo 7)
- **Q**: Sur un plan de ville, un monument est en $D(4, -2)$ et le centre de la place est
- **A**: $D'(0, 4)$
- `WARN_HINT_IS_ANSWER` step 4: _$D'(0, 4)$_
- `WARN_HINT_IS_FORMULA` step 2: _$x' = 2 \times 2 - 4 = 0$_
- `WARN_HINT_IS_FORMULA` step 3: _$y' = 2 \times 1 - (-2) = 4$_

### curriculum — 5EME / Symétrie_Centrale (row 16, exo 9)
- **Q**: Qu'est-ce que la symétrie centrale par rapport à un point $O$ ?
- **A**: Chaque point M a un image M' telle que O
- `WARN_HINT_IS_FORMULA` step 2: _$OM = OM'$ et $M$, $O$, $M'$ sont alignés_

### curriculum — 5EME / Symétrie_Centrale (row 16, exo 11)
- **Q**: Sur un terrain de jeu, le but est en $A(2, 7)$ et le centre du terrain en $O(4, 
- **A**: $A'(6, 3)$
- `WARN_HINT_IS_ANSWER` step 3: _$A'(6, 3)$_
- `WARN_HINT_IS_FORMULA` step 1: _$x' = 2 \times 4 - 2 = 6$_
- `WARN_HINT_IS_FORMULA` step 2: _$y' = 2 \times 5 - 7 = 3$_

### curriculum — 5EME / Symétrie_Centrale (row 16, exo 14)
- **Q**: Si $E(-5, 3)$ est le symétrique de $F$ par rapport à $O(0, 0)$, quelles sont les
- **A**: $F(5, -3)$
- `WARN_HINT_IS_FORMULA` step 2: _$x_F = 2 \times 0 - (-5) = 5$_
- `WARN_HINT_IS_FORMULA` step 3: _$y_F = 2 \times 0 - 3 = -3$_

### curriculum — 5EME / Symétrie_Centrale (row 16, exo 15)
- **Q**: Complète : $G(3, -1)$ et centre $H(-1, 5)$. L'image de $G$ a pour abscisse ___
- **A**: -5
- `WARN_HINT_IS_ANSWER` step 3: _$G'(-5, 11)$_
- `WARN_HINT_IS_FORMULA` step 1: _$x' = 2 \times (-1) - 3 = -2 - 3 = ?$_
- `WARN_HINT_IS_FORMULA` step 2: _$y' = 2 \times 5 - (-1) = 11$_

### curriculum — 5EME / Symétrie_Centrale (row 16, exo 16)
- **Q**: Un segment $[AB]$ a son symétrique $[A'B']$ par rapport à $O$. Que vaut $A'B'$ ?
- **A**: $A'B' = AB$
- `WARN_HINT_IS_ANSWER` step 2: _$A'B' = AB$_
- `WARN_HINT_IS_FORMULA` step 2: _$A'B' = AB$_

### curriculum — 5EME / Symétrie_Centrale (row 16, exo 17)
- **Q**: Quelle figure a à la fois des axes de symétrie ET un centre de symétrie ?
- **A**: Le rectangle
- `WARN_HINT_IS_ANSWER` step 1: _Le rectangle a 2 axes de symétrie_

### curriculum — 5EME / Symétrie_Centrale (row 16, exo 18)
- **Q**: Si $A(2, 3)$ a pour symétrique $A'(8, -1)$, alors le centre est $O(5, 1)$.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _$x_O = \frac{2 + 8}{2} = 5$_
- `WARN_HINT_IS_FORMULA` step 2: _$y_O = \frac{3 + (-1)}{2} = 1$_

### curriculum — 5EME / Symétrie_Centrale (row 16, exo 20)
- **Q**: Complète : le symétrique de $(x, y)$ par rapport à $O(a, b)$ est $(2a - x, 2b - 
- **A**: y
- `WARN_HINT_IS_FORMULA` step 1: _Formule : $x' = 2a - x$, $y' = 2b - y$_

### curriculum — 6EME / Volumes (row 17, exo 1)
- **Q**: Calculer le volume d'un pavé droit de longueur 5 cm, largeur 3 cm et hauteur 2 c
- **A**: 30 cm³
- `WARN_HINT_IS_FORMULA` step 1: _$V = L \times l \times h$._

### curriculum — 6EME / Volumes (row 17, exo 2)
- **Q**: Un dé géant a la forme d'un cube d'arête $4$ cm. Quel est son volume ?
- **A**: 64 cm³
- `WARN_HINT_IS_FORMULA` step 1: _$V = a^3 = 4^3$._

### curriculum — 6EME / Volumes (row 17, exo 3)
- **Q**: Le volume d'un cube de côté 3 cm est $9$ cm$^3$.
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 1: _$V = 3^3 = 27$ cm$^3$, pas $9$._

### curriculum — 6EME / Volumes (row 17, exo 4)
- **Q**: Un élève écrit : « 1 m³ = 100 cm³ car 1 m = 100 cm ». Où est l'erreur ?
- **A**: 1 m³ = 1 000 000 cm³ (on met au cube le 
- `WARN_HINT_IS_FORMULA` step 1: _$1$ m = $100$ cm, donc $1$ m$^3$ = $(100)^3$ cm$^3$._

### curriculum — 6EME / Volumes (row 17, exo 8)
- **Q**: 1 litre = 1 dm³.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _$1$ dm$^3$ $= 10 \times 10 \times 10 = 1\,000$ cm$^3$._

### curriculum — 6EME / Volumes (row 17, exo 9)
- **Q**: Le volume d'un pavé droit de dimensions 4 cm, 5 cm et 3 cm est :
- **A**: 60
- `WARN_HINT_IS_FORMULA` step 1: _$V = 4 \times 5 \times 3 = ?$ cm$^3$._

### curriculum — 6EME / Volumes (row 17, exo 10)
- **Q**: Un petit aquarium (pavé droit) a une longueur de $10$ cm, largeur $4$ cm et volu
- **A**: 3
- `WARN_HINT_IS_FORMULA` step 1: _$V = L \times l \times h$, donc $h = V \div (L \times l)$._
- `WARN_HINT_IS_FORMULA` step 2: _$h = 120 \div (10 \times 4) = 120 \div 40 = ?$ cm._

### curriculum — 6EME / Volumes (row 17, exo 11)
- **Q**: Si on double les dimensions d'un cube, son volume est multiplié par :
- **A**: 8
- `WARN_HINT_IS_FORMULA` step 2: _Nouveau volume : $(2a)^3 = 8a^3$._

### curriculum — 6EME / Volumes (row 17, exo 12)
- **Q**: Convertir 2,5 m³ en litres.
- **A**: 2500 L
- `WARN_HINT_IS_FORMULA` step 2: _$2{,}5 \times 1\,000 = 2\,500$ L._

### curriculum — 6EME / Volumes (row 17, exo 13)
- **Q**: Si on double les dimensions d'un cube, son volume est multiplié par 8.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _$(2a)^3 = 8a^3$._

### curriculum — 6EME / Volumes (row 17, exo 14)
- **Q**: Un prisme droit triangulaire a une base de 6 cm et hauteur de base 4 cm, hauteur
- **A**: 120 cm³
- `WARN_HINT_IS_FORMULA` step 1: _Aire de la base triangulaire = $\frac{6 \times 4}{2} = 12$ cm$^2$._

### curriculum — 6EME / Volumes (row 17, exo 15)
- **Q**: Combien de cubes de 1 cm³ peut-on ranger dans une boîte cubique d'arête 5 cm ? R
- **A**: 125
- `WARN_HINT_IS_ANSWER` step 3: _On peut en ranger $125$._

### curriculum — 6EME / Volumes (row 17, exo 17)
- **Q**: Un pavé droit a le même volume qu'un cube d'arête 6 cm. Si le pavé mesure 4 cm $
- **A**: 6 cm
- `WARN_HINT_IS_ANSWER` step 1: _Volume du cube : $6^3 = 216$ cm$^3$._
- `WARN_HINT_IS_FORMULA` step 2: _$4 \times 9 \times h = 216$, donc $36h = 216$._

### curriculum — 6EME / Volumes (row 17, exo 19)
- **Q**: Un réservoir cylindrique de rayon 1 m et de hauteur 2 m est rempli à moitié. Que
- **A**: 3,14 m³
- `WARN_HINT_IS_FORMULA` step 1: _Volume total = $\pi r^2 h = 3{,}14 \times 1 \times 2 = 6{,}28$ m$^3$._

### curriculum — 5EME / Transformations (row 18, exo 1)
- **Q**: Sur un quadrillage, le point $A(2, 1)$ est translaté par le vecteur $\vec{v}(3, 
- **A**: $(5, 3)$
- `WARN_HINT_IS_ANSWER` step 3: _Image : $(5, 3)$_
- `WARN_HINT_IS_FORMULA` step 1: _$x' = 2 + 3 = 5$_
- `WARN_HINT_IS_FORMULA` step 2: _$y' = 1 + 2 = 3$_

### curriculum — 5EME / Transformations (row 18, exo 2)
- **Q**: Le point $B(4, 3)$ est l'image du point $A(1, 1)$ par une translation. Quelles s
- **A**: $(3, 2)$
- `WARN_HINT_IS_ANSWER` step 3: _$\vec{v}(3, 2)$_
- `WARN_HINT_IS_FORMULA` step 1: _$a = 4 - 1 = 3$_
- `WARN_HINT_IS_FORMULA` step 2: _$b = 3 - 1 = 2$_

### curriculum — 5EME / Transformations (row 18, exo 3)
- **Q**: Sur un plan de salle, une table est en $A(1, 4)$. On la déplace de $3$ cases ver
- **A**: $(1, 1)$
- `WARN_HINT_IS_ANSWER` step 3: _$(1, 1)$_
- `WARN_HINT_IS_FORMULA` step 2: _$x' = 1$, $y' = 4 - 3 = 1$_
- `WARN_HINT_TOO_SHORT` step 3: _$(1, 1)$_

### curriculum — 5EME / Transformations (row 18, exo 5)
- **Q**: Complète : une rotation de centre $O$ et d'angle $90^{\circ}$ anti-horaire trans
- **A**: 3
- `WARN_DUPLICATE` step 1: _Rotation $90^\circ$ anti-horaire : $(x, y) \to (-y, x)$_

### curriculum — 5EME / Transformations (row 18, exo 6)
- **Q**: Quelle transformation conserve les longueurs et les angles mais déplace une figu
- **A**: La translation
- `WARN_HINT_IS_ANSWER` step 1: _La translation déplace chaque point de la même manière_

### curriculum — 5EME / Transformations (row 18, exo 7)
- **Q**: Par symétrie centrale de centre $O(0, 0)$, quelle est l'image du point $P(2, 5)$
- **A**: $(-2, -5)$
- `WARN_HINT_IS_ANSWER` step 2: _$P'(-2, -5)$_

### curriculum — 5EME / Transformations (row 18, exo 9)
- **Q**: Quelle transformation conserve l'orientation de la figure (sens de lecture des s
- **A**: La translation
- `WARN_HINT_IS_ANSWER` step 1: _La translation conserve l'orientation_

### curriculum — 5EME / Transformations (row 18, exo 10)
- **Q**: Complète : l'image de $A(1, 3)$ par la translation de vecteur $\vec{u}(2, -1)$ e
- **A**: 2
- `WARN_HINT_IS_FORMULA` step 1: _$x' = 1 + 2 = 3$_
- `WARN_HINT_IS_FORMULA` step 2: _$y' = 3 + (-1) = $?_

### curriculum — 5EME / Transformations (row 18, exo 12)
- **Q**: Le triangle $ABC$ a une aire de $12$ cm^2. Après une rotation de $45^{\circ}$ au
- **A**: $12$ cm^2
- `WARN_HINT_IS_ANSWER` step 2: _L'aire reste $12$ cm^2_

### curriculum — 5EME / Transformations (row 18, exo 14)
- **Q**: Un vecteur de translation $\vec{v}$ transforme $P(1, 2)$ en $P'(4, 0)$. Puis on 
- **A**: $(7, -2)$
- `WARN_HINT_IS_FORMULA` step 1: _$\vec{v} = (4-1, 0-2) = (3, -2)$_

### curriculum — 5EME / Transformations (row 18, exo 16)
- **Q**: Par symétrie centrale de centre $I(2, 3)$, quelle est l'image du point $P(5, 1)$
- **A**: $(-1, 5)$
- `WARN_HINT_IS_ANSWER` step 3: _$P'(-1, 5)$_
- `WARN_HINT_IS_FORMULA` step 1: _$x' = 2 \times 2 - 5 = -1$_
- `WARN_HINT_IS_FORMULA` step 2: _$y' = 2 \times 3 - 1 = 5$_

### curriculum — 5EME / Transformations (row 18, exo 19)
- **Q**: Le point $A(0, 4)$ est translaté par $\vec{v}(3, -1)$, puis l'image subit une sy
- **A**: $(-3, -3)$
- `WARN_HINT_IS_ANSWER` step 2: _Symétrie de centre $O$ : $(-3, -3)$_
- `WARN_HINT_IS_FORMULA` step 1: _Translation : $A'(0+3, 4-1) = (3, 3)$_

### curriculum — 5EME / Transformations (row 18, exo 20)
- **Q**: Complète : une rotation de centre $O$ et d'angle $90^{\circ}$ dans le sens anti-
- **A**: directe
- `WARN_HINT_IS_ANSWER` step 2: _Une rotation dans ce sens est dite directe_

### curriculum — 5EME / Angles_Parallèles (row 19, exo 4)
- **Q**: Si deux angles alternes-internes sont égaux, alors les droites sont parallèles.
- **A**: Vrai
- `WARN_HINT_IS_ANSWER` step 3: _La réciproque dit : alternes-internes égaux $\Rightarrow$ parallèles. Elle est vraie._

### curriculum — 5EME / Angles_Parallèles (row 19, exo 10)
- **Q**: Deux angles supplémentaires mesurent $3x$ et $x + 20°$. La valeur de $x$ est ___
- **A**: 40
- `WARN_HINT_IS_FORMULA` step 2: _$3x + x + 20 = 180$, soit $4x + 20 = 180$._
- `WARN_HINT_IS_FORMULA` step 3: _$4x = 160$, donc $x = ?$._

### curriculum — 5EME / Angles_Parallèles (row 19, exo 12)
- **Q**: Un triangle a deux angles de $50°$ et $70°$. Combien mesure le troisième angle ?
- **A**: $60°$
- `WARN_HINT_IS_ANSWER` step 3: _$180° - 120° = ?$. Le troisième angle mesure $60°$._

### curriculum — 5EME / Angles_Parallèles (row 19, exo 13)
- **Q**: Noa construit un triangle isocèle avec un angle au sommet de $40°$. Combien mesu
- **A**: $70°$ chacun
- `WARN_HINT_IS_FORMULA` step 3: _Chaque angle de base mesure $140° \div 2 = 70°$._

### curriculum — 5EME / Angles_Parallèles (row 19, exo 17)
- **Q**: Dans un parallélogramme $ABCD$, l'angle en $A$ mesure $65°$. Combien mesure l'an
- **A**: $115°$
- `WARN_HINT_IS_FORMULA` step 2: _Cela signifie que $\hat{A} + \hat{B} = 180°$._

### curriculum — 5EME / Angles_Parallèles (row 19, exo 19)
- **Q**: Dans un triangle équilatéral, chaque angle mesure $60°$.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 3: _$180° \div 3 = 60°$ par angle._

### curriculum — 5EME / Angles_Parallèles (row 19, exo 20)
- **Q**: $(d_1) \parallel (d_2)$, une sécante coupe $(d_1)$ en formant un angle de $75°$.
- **A**: 180
- `WARN_HINT_IS_ANSWER` step 3: _$75° + 105° = 180°$. Un angle et son supplémentaire font toujours $180°$._

### curriculum — 5EME / Triangles_Semblables (row 20, exo 2)
- **Q**: On construit une maquette agrandie $3$ fois. Un mur de $4$ cm sur le plan mesure
- **A**: $12$ cm
- `WARN_HINT_IS_FORMULA` step 1: _Rapport d'agrandissement $k = 3$_

### curriculum — 5EME / Triangles_Semblables (row 20, exo 5)
- **Q**: Complète : si deux triangles ont deux angles égaux ($40^\circ$ et $70^\circ$), l
- **A**: 70
- `WARN_HINT_IS_ANSWER` step 2: _$180 - 40 - 70 = 70^{\circ}$_

### curriculum — 5EME / Triangles_Semblables (row 20, exo 7)
- **Q**: Deux triangles semblables ont-ils nécessairement la même aire ?
- **A**: Non, les aires sont dans le rapport $k^2
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{\text{Aire}_2}{\text{Aire}_1} = k^2$_

### curriculum — 5EME / Triangles_Semblables (row 20, exo 9)
- **Q**: Le triangle $ABC$ ($AB = 8$, $BC = 6$, $AC = 10$) est semblable au triangle $DEF
- **A**: $4$
- `WARN_HINT_IS_FORMULA` step 1: _$DE = AB \times k = 8 \times \frac{1}{2} = ?$_

### curriculum — 5EME / Triangles_Semblables (row 20, exo 10)
- **Q**: Complète : rapport de similitude $k = 3$, le rapport des aires est ___
- **A**: 9
- `WARN_HINT_TOO_SHORT` step 2: _$3^2 = $?_

### curriculum — 5EME / Triangles_Semblables (row 20, exo 11)
- **Q**: Un logo triangulaire de $9$ cm^2 est agrandi avec un rapport $k = 2$. Quelle est
- **A**: $36$ cm^2
- `WARN_HINT_IS_FORMULA` step 1: _$k^2 = 2^2 = 4$_

### curriculum — 5EME / Triangles_Semblables (row 20, exo 13)
- **Q**: Deux triangles semblables avec des aires de $4$ cm^2 et $9$ cm^2 ont un rapport 
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _$\frac{\text{Aire}_1}{\text{Aire}_2} = \frac{4}{9} = k^2$_
- `WARN_HINT_IS_FORMULA` step 2: _$k = \sqrt{\frac{4}{9}} = \frac{2}{3}$ ✓_

### curriculum — 5EME / Triangles_Semblables (row 20, exo 14)
- **Q**: Un arbre de $4$ m projette une ombre de $6$ m. Un poteau projette une ombre de $
- **A**: $6$ m
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{h}{4} = \frac{9}{6}$_

### curriculum — 5EME / Triangles_Semblables (row 20, exo 15)
- **Q**: Complète : le triangle $ABC$ ($AB = 6$, $BC = 8$, $AC = 10$) est semblable au tr
- **A**: 12
- `WARN_HINT_IS_FORMULA` step 1: _$k = \frac{DE}{AB} = \frac{9}{6} = 1{,}5$_
- `WARN_HINT_IS_FORMULA` step 2: _$EF = BC \times 1{,}5 = 8 \times 1{,}5 = ?$_

### curriculum — 5EME / Triangles_Semblables (row 20, exo 16)
- **Q**: Deux triangles semblables ont un rapport $k = 4$. Si le petit triangle a une air
- **A**: $80$ cm^2
- `WARN_HINT_IS_FORMULA` step 1: _$k^2 = 4^2 = 16$_

### curriculum — 5EME / Triangles_Semblables (row 20, exo 17)
- **Q**: Sur une carte à l'échelle $\frac{1}{50\,000}$, deux villes sont à $3$ cm. Distan
- **A**: $1{,}5$ km
- `WARN_HINT_IS_FORMULA` step 1: _$3 \times 50\,000 = 150\,000$ cm_

### curriculum — 5EME / Triangles_Semblables (row 20, exo 18)
- **Q**: Deux triangles semblables avec des périmètres de $20$ cm et $30$ cm ont un rappo
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _$k = \frac{20}{30} = \frac{2}{3}$_
- `WARN_HINT_IS_FORMULA` step 2: _$k^2 = \frac{4}{9}$_

### curriculum — 5EME / Triangles_Semblables (row 20, exo 19)
- **Q**: Dans un triangle $ABC$, $M$ est le milieu de $AB$ et $N$ est le milieu de $AC$. 
- **A**: $\frac{1}{2}$
- `WARN_HINT_IS_FORMULA` step 1: _$AM = \frac{AB}{2}$ et $AN = \frac{AC}{2}$_

### curriculum — 5EME / Triangles_Semblables (row 20, exo 20)
- **Q**: Complète : le triangle $DEF$ a des angles $30^\circ$, $70^\circ$ et $80^\circ$. 
- **A**: 80
- `WARN_HINT_IS_ANSWER` step 2: _$180 - 30 - 70 = 80^{\circ}$_

### curriculum — 6EME / Agrandissement_Réduction (row 21, exo 2)
- **Q**: Si $k = \frac{1}{2}$, s'agit-il d'un agrandissement ou d'une réduction ?
- **A**: Réduction
- `WARN_HINT_IS_FORMULA` step 3: _$k = 1$ $\rightarrow$ figure identique._

### curriculum — 6EME / Agrandissement_Réduction (row 21, exo 3)
- **Q**: Un agrandissement de rapport 2 double toutes les longueurs.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _Rapport $k = 2$ signifie chaque longueur est multipliée par $2$._

### curriculum — 6EME / Agrandissement_Réduction (row 21, exo 5)
- **Q**: Sur un plan à l'échelle $\frac{1}{100}$, $1$ cm correspond à ___ cm dans la réal
- **A**: 100
- `WARN_HINT_IS_ANSWER` step 1: _Que signifie une échelle de $\frac{1}{100}$ ? Réfléchis au lien entre cm sur le plan et cm en réalit_
- `WARN_HINT_IS_ANSWER` step 2: _$100$ cm $= 1$ m._

### curriculum — 6EME / Agrandissement_Réduction (row 21, exo 13)
- **Q**: Un sticker carré de $5$ cm agrandi $2$ fois a une aire de $100$ cm$^2$.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _Nouveau côté : $5 \times 2 = 10$ cm._

### curriculum — 6EME / Agrandissement_Réduction (row 21, exo 15)
- **Q**: Un dessin de toit triangulaire mesure $3$ cm ($k = \frac{1}{50}$). La longueur r
- **A**: 150
- `WARN_HINT_IS_ANSWER` step 2: _$150$ cm $= 1{,}5$ m._

### curriculum — 6EME / Agrandissement_Réduction (row 21, exo 16)
- **Q**: Sur un plan à l'échelle $\frac{1}{100}$, deux pièces mesurent $3{,}5$ cm et $4{,
- **A**: 3,5 m et 4,2 m
- `WARN_HINT_IS_FORMULA` step 2: _$4{,}2 \times 100 = 420$ cm $= 4{,}2$ m._

### curriculum — 6EME / Agrandissement_Réduction (row 21, exo 17)
- **Q**: Un rectangle de $12 \times 8$ cm est réduit. La longueur réduite est $3$ cm. Le 
- **A**: k = 1/4, largeur = 2 cm
- `WARN_HINT_IS_FORMULA` step 2: _Largeur : $8 \times \frac{1}{4} = 2$ cm._

### curriculum — 6EME / Agrandissement_Réduction (row 21, exo 20)
- **Q**: Deux villes sont à $45$ km. Sur une carte au $\frac{1}{900\,000}$, elles apparai
- **A**: 5
- `WARN_HINT_IS_FORMULA` step 2: _$4\,500\,000 \times \frac{1}{900\,000} = ?$ cm._

### curriculum — 6EME / Conversions_Unités (row 22, exo 1)
- **Q**: Convertir 3 km en mètres.
- **A**: 3 000 m
- `WARN_HINT_IS_FORMULA` step 2: _$3 \times 1\,000 = 3\,000$ m._

### curriculum — 6EME / Conversions_Unités (row 22, exo 4)
- **Q**: Un élève convertit : « 2500 g = 250 kg car on divise par 10 ». Où est l'erreur ?
- **A**: Il faut diviser par 1000, pas par 10
- `WARN_HINT_IS_FORMULA` step 2: _$2\,500 \div 1\,000 = 2{,}5$ kg._

### curriculum — 6EME / Conversions_Unités (row 22, exo 5)
- **Q**: $3{,}5$ m = ___ cm.
- **A**: 350
- `WARN_HINT_IS_FORMULA` step 2: _$3{,}5 \times 100 = ?$ cm._

### curriculum — 6EME / Conversions_Unités (row 22, exo 7)
- **Q**: Un film dure $2$ h $30$ min. Quelle est la durée en minutes ?
- **A**: 150 min
- `WARN_HINT_IS_FORMULA` step 1: _$2$ h $= 2 \times 60 = 120$ min._

### curriculum — 6EME / Conversions_Unités (row 22, exo 10)
- **Q**: Convertir $5\,000$ mm en mètres. Réponse : ___ m.
- **A**: 5
- `WARN_HINT_IS_FORMULA` step 2: _$?\,000 \div 1\,000 = ?$ m._

### curriculum — 6EME / Conversions_Unités (row 22, exo 11)
- **Q**: Convertir 3,5 kg en grammes.
- **A**: 3 500 g
- `WARN_HINT_IS_FORMULA` step 2: _$3{,}5 \times 1\,000 = 3\,500$ g._

### curriculum — 6EME / Conversions_Unités (row 22, exo 12)
- **Q**: Un trajet en train dure $2{,}5$ heures. En heures et minutes :
- **A**: 2 h 30 min
- `WARN_HINT_IS_ANSWER` step 3: _Total : $2$ h $30$ min._
- `WARN_HINT_IS_FORMULA` step 2: _$0{,}5$ h $= 0{,}5 \times 60 = 30$ min._

### curriculum — 6EME / Conversions_Unités (row 22, exo 14)
- **Q**: Convertir 3 m$^3$ en litres ($1$ dm$^3$ $= 1$ L).
- **A**: 3 000 L
- `WARN_HINT_IS_FORMULA` step 2: _$3 \times 1\,000 = 3\,000$ L._

### curriculum — 6EME / Conversions_Unités (row 22, exo 15)
- **Q**: Un train parcourt 270 km en 1 h 30 min. Sa vitesse est ___ km/h.
- **A**: 180
- `WARN_HINT_IS_FORMULA` step 2: _$v = \frac{d}{t} = \frac{270}{1{,}5} = ?$ km/h._

### curriculum — 6EME / Conversions_Unités (row 22, exo 16)
- **Q**: Une piscine rectangulaire fait $5$ m $\times$ $2$ m $\times$ $1{,}5$ m. Son volu
- **A**: 15 000 L
- `WARN_HINT_IS_FORMULA` step 1: _$V = 5 \times 2 \times 1{,}5 = 15$ m$^3$._

### curriculum — 6EME / Conversions_Unités (row 22, exo 20)
- **Q**: Convertir 2,4 cm³ en mm³. Réponse : ___ mm³.
- **A**: 2400
- `WARN_HINT_IS_FORMULA` step 2: _$2{,}4 \times 1\,000 = 2\,400$ mm$^3$._

### curriculum — 6EME / Puissances_10 (row 23, exo 2)
- **Q**: Un collège a exactement $10^2$ élèves. Combien d'élèves cela fait-il ?
- **A**: 100
- `WARN_HINT_IS_FORMULA` step 1: _$10^2 = 10 \times 10 = ?$._

### curriculum — 6EME / Puissances_10 (row 23, exo 3)
- **Q**: $10^3 = 30$.
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 1: _$10^3 = 10 \times 10 \times 10 = 1\,000$, pas $30$._

### curriculum — 6EME / Puissances_10 (row 23, exo 4)
- **Q**: Un élève écrit : $10^2 \times 10^3 = 100^5$. Où est l'erreur ?
- **A**: La base reste 10, on additionne les expo
- `WARN_HINT_IS_FORMULA` step 1: _$10^2 \times 10^3 = 10^{2+3} = 10^5$._

### curriculum — 6EME / Puissances_10 (row 23, exo 5)
- **Q**: Écrire $10\,000$ comme puissance de 10 : $10^{\text{___}}$.
- **A**: 4
- `WARN_HINT_IS_FORMULA` step 1: _$10\,000 = 10 \times 10 \times 10 \times 10 = 10^4$._

### curriculum — 6EME / Puissances_10 (row 23, exo 6)
- **Q**: Que vaut $10^3$ ?
- **A**: 1 000
- `WARN_HINT_IS_FORMULA` step 1: _$10^3 = 10 \times 10 \times 10 = 1\,000$._

### curriculum — 6EME / Puissances_10 (row 23, exo 9)
- **Q**: $10^4 \times 10^3 = 10^{?}$. La valeur de $?$ est :
- **A**: 7
- `WARN_HINT_IS_FORMULA` step 2: _$10^4 \times 10^3 = 10^7$._

### curriculum — 6EME / Puissances_10 (row 23, exo 11)
- **Q**: Un fichier contient $10^2$ lignes. Chaque ligne a $10^3$ caractères. Combien de 
- **A**: 10⁵
- `WARN_HINT_IS_FORMULA` step 1: _$10^2 \times 10^3 = 10^{2+3} = 10^5$._

### curriculum — 6EME / Puissances_10 (row 23, exo 12)
- **Q**: La Terre a environ $8 \times 10^9$ habitants. En écriture décimale :
- **A**: 8 000 000 000
- `WARN_HINT_IS_FORMULA` step 2: _$8 \times 1\,000\,000\,000 = 8\,000\,000\,000$._

### curriculum — 6EME / Puissances_10 (row 23, exo 13)
- **Q**: $3 \times 10^4$ et $30\,000$ sont le même nombre.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _$3 \times 10^4 = 3 \times 10\,000 = 30\,000$._

### curriculum — 6EME / Puissances_10 (row 23, exo 14)
- **Q**: La distance Terre-Lune est $10^6$ m. Un avion vole à $10^4$ m. Combien de fois l
- **A**: 10²
- `WARN_HINT_IS_FORMULA` step 1: _$\frac{10^6}{10^4} = 10^{6-4} = 10^2 = 100$ fois._

### curriculum — 6EME / Puissances_10 (row 23, exo 15)
- **Q**: $1$ méga-octet $= 10^6$ octets. Dans $3$ méga-octets, il y a ___ octets (écritur
- **A**: 3
- `WARN_HINT_IS_FORMULA` step 2: _$a = ?$._
- `WARN_HINT_TOO_SHORT` step 2: _$a = ?$._

### curriculum — 6EME / Puissances_10 (row 23, exo 18)
- **Q**: La vitesse de la lumière ($3 \times 10^8$ m/s) est environ $10^6$ fois plus gran
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _$\frac{3 \times 10^8}{340} \approx \frac{3 \times 10^8}{3 \times 10^2} = 10^6$._

### curriculum — 6EME / Puissances_10 (row 23, exo 19)
- **Q**: Un disque dur a $2 \times 10^{12}$ octets. Combien de fichiers de $4 \times 10^6
- **A**: 5 × 10⁵
- `WARN_HINT_IS_FORMULA` step 1: _$\frac{2 \times 10^{12}}{4 \times 10^6} = \frac{2}{4} \times 10^{12-6}$._
- `WARN_HINT_IS_FORMULA` step 2: _$= 0{,}5 \times 10^6 = 5 \times 10^5$._

### curriculum — 6EME / Puissances_10 (row 23, exo 20)
- **Q**: Un milli-mètre $= 10^{-3}$ m. Dans 1 mètre, il y a ___ millimètres.
- **A**: 1000
- `WARN_HINT_IS_FORMULA` step 2: _$1 \div 0{,}001 = 1\,000$ mm._

### curriculum — 1ERE / Second_Degre (row 24, exo 1)
- **Q**: Calculer le discriminant de $f(x) = 1x^2 -3x +2$.
- **A**: $\Delta = 1$
- `WARN_HINT_IS_FORMULA` step 2: _$\Delta = (-3)^2 - 4 \times 1 \times (2)$._
- `WARN_HINT_IS_FORMULA` step 3: _$\Delta = 9 - 8$._

### curriculum — 1ERE / Second_Degre (row 24, exo 2)
- **Q**: Donner la forme canonique de $f(x) = x^2 +5x -3$.
- **A**: $f(x) = (x -2{,}5)^2 -9{,}2$
- `WARN_HINT_IS_FORMULA` step 1: _Calculer $\alpha = -b/(2a)$._
- `WARN_HINT_IS_FORMULA` step 2: _$\alpha = -2{,}5$._

### curriculum — 1ERE / Second_Degre (row 24, exo 3)
- **Q**: Combien de racines a $f(x) = 1x^2 -4x +4$?
- **A**: Aucune racine réelle
- `WARN_HINT_IS_FORMULA` step 2: _$\Delta = 0 < 0$._
- `WARN_HINT_TOO_SHORT` step 3: _Conclure._

### curriculum — 1ERE / Second_Degre (row 24, exo 4)
- **Q**: Le sommet de la parabole $y = 3x^2 -6x +1$ a pour abscisse :
- **A**: $x_S = 1{,}00$
- `WARN_HINT_IS_FORMULA` step 2: _$a=3$, $b=-6$._
- `WARN_HINT_IS_FORMULA` step 3: _$x_S = -(-6)/(2 \times 3)$._

### curriculum — 1ERE / Second_Degre (row 24, exo 5)
- **Q**: Quel est le signe de $f(x) = 1x^2 +2x -8$ pour $x$ grand ?
- **A**: $f(x) \to +\infty$
- `WARN_HINT_IS_FORMULA` step 1: _$a = 1$._
- `WARN_HINT_TOO_SHORT` step 1: _$a = 1$._

### curriculum — 1ERE / Second_Degre (row 24, exo 6)
- **Q**: Calculer le discriminant de $f(x) = 2x^2 -7x +3$.
- **A**: $\Delta = 25$
- `WARN_HINT_IS_FORMULA` step 2: _$\Delta = (-7)^2 - 4 \times 2 \times (3)$._
- `WARN_HINT_IS_FORMULA` step 3: _$\Delta = 49 - 24$._

### curriculum — 1ERE / Second_Degre (row 24, exo 7)
- **Q**: Donner la forme canonique de $f(x) = x^2 -1x -6$.
- **A**: $f(x) = (x +0{,}5)^2 -6{,}2$
- `WARN_HINT_IS_FORMULA` step 1: _Calculer $\alpha = -b/(2a)$._
- `WARN_HINT_IS_FORMULA` step 2: _$\alpha = 0{,}5$._

### curriculum — 1ERE / Second_Degre (row 24, exo 8)
- **Q**: Combien de racines a $f(x) = 4x^2 -4x +1$?
- **A**: Aucune racine réelle
- `WARN_HINT_IS_FORMULA` step 2: _$\Delta = 0 < 0$._
- `WARN_HINT_TOO_SHORT` step 3: _Conclure._

### curriculum — 1ERE / Second_Degre (row 24, exo 9)
- **Q**: Le sommet de la parabole $y = 1x^2 +6x +9$ a pour abscisse :
- **A**: $x_S = -3{,}00$
- `WARN_HINT_IS_FORMULA` step 2: _$a=1$, $b=6$._
- `WARN_HINT_IS_FORMULA` step 3: _$x_S = -(6)/(2 \times 1)$._

### curriculum — 1ERE / Second_Degre (row 24, exo 10)
- **Q**: Quel est le signe de $f(x) = 1x^2 -2x -15$ pour $x$ grand ?
- **A**: $f(x) \to +\infty$
- `WARN_HINT_IS_FORMULA` step 1: _$a = 1$._
- `WARN_HINT_TOO_SHORT` step 1: _$a = 1$._

### curriculum — 1ERE / Second_Degre (row 24, exo 14)
- **Q**: On lance un objet. Sa hauteur est $h(t) = -1t^2 -6t +8$. Quand atteint-il sa hau
- **A**: $t = -3{,}00$ s
- `WARN_HINT_IS_FORMULA` step 1: _On cherche le maximum de $h(t) = -1t^2 -6t +8$. Comme $a < 0$, la parabole est tournée vers le bas e_
- `WARN_HINT_IS_FORMULA` step 2: _Le sommet a pour abscisse $t_s = -\frac{b}{2a}$. On remplace dans $h(t) = -1t^2 -6t +8$ pour obtenir_

### curriculum — 1ERE / Second_Degre (row 24, exo 15)
- **Q**: On lance un objet. Sa hauteur est $h(t) = -3t^2 +2t -1$. Quand atteint-il sa hau
- **A**: $t = 0{,}33$ s
- `WARN_HINT_IS_FORMULA` step 1: _On cherche le maximum de $h(t) = -3t^2 +2t -1$. Comme $a < 0$, la parabole est tournée vers le bas e_
- `WARN_HINT_IS_FORMULA` step 2: _Le sommet a pour abscisse $t_s = -\frac{b}{2a}$. On remplace dans $h(t) = -3t^2 +2t -1$ pour obtenir_

### curriculum — 1ERE / Second_Degre (row 24, exo 16)
- **Q**: Déterminer $m$ pour que $x^2 +1x + m = 0$ ait une racine double.
- **A**: $m = 0$
- `WARN_HINT_IS_ANSWER` step 2: _$\Delta = (1)^2 - 4m = 0$._
- `WARN_HINT_IS_FORMULA` step 1: _Racine double ⟺ $\Delta = 0$._
- `WARN_HINT_IS_FORMULA` step 2: _$\Delta = (1)^2 - 4m = 0$._

### curriculum — 1ERE / Second_Degre (row 24, exo 17)
- **Q**: Déterminer $m$ pour que $x^2 -4x + m = 0$ ait une racine double.
- **A**: $m = 4$
- `WARN_HINT_IS_FORMULA` step 1: _Racine double ⟺ $\Delta = 0$._
- `WARN_HINT_IS_FORMULA` step 2: _$\Delta = (-4)^2 - 4m = 0$._

### curriculum — 1ERE / Second_Degre (row 24, exo 18)
- **Q**: Factoriser $P(x) = 1x^2 -3x -4$ sachant que $\Delta = 25$.
- **A**: $P(x) = 1(x - x_1)(x - x_2)$
- `WARN_HINT_IS_FORMULA` step 1: _On factorise $P(x) = 1x^2 -3x -4$. On commence par calculer $\Delta = b^2 - 4ac$ pour trouver les ra_
- `WARN_HINT_IS_FORMULA` step 2: _On calcule les racines $x_1 = \frac{-b - \sqrt{\Delta}}{2a}$ et $x_2 = \frac{-b + \sqrt{\Delta}}{2a}_

### curriculum — 1ERE / Second_Degre (row 24, exo 19)
- **Q**: Factoriser $P(x) = 1x^2 +2x +1$ sachant que $\Delta = 0$.
- **A**: $P(x) = 1(x +1{,}0)^2$
- `WARN_HINT_IS_FORMULA` step 1: _On factorise $P(x) = 1x^2 +2x +1$. On commence par calculer $\Delta = b^2 - 4ac$ pour trouver les ra_
- `WARN_HINT_IS_FORMULA` step 2: _On calcule les racines $x_1 = \frac{-b - \sqrt{\Delta}}{2a}$ et $x_2 = \frac{-b + \sqrt{\Delta}}{2a}_

### curriculum — 1ERE / Second_Degre (row 24, exo 20)
- **Q**: La somme et le produit des racines de $x^2 -8x +15 = 0$ valent :
- **A**: $S = 8$, $P = 15$
- `WARN_HINT_IS_FORMULA` step 2: _$S = -b/a$ et $P = c/a$._
- `WARN_HINT_IS_FORMULA` step 3: _Ici $a=1$, $b=-8$, $c=15$._

### curriculum — 1ERE / Suites (row 25, exo 1)
- **Q**: $(u_n)$ est arithmétique avec $u_0 = 3$ et $r = 5$. Calculer $u_{10}$.
- **A**: $u_{10} = 53$
- `WARN_HINT_IS_FORMULA` step 1: _Suite arithmétique :$u_n = u_0 + nr$._
- `WARN_HINT_IS_FORMULA` step 2: _$u_{10} = 3 + 10 \times 5$._
- `WARN_HINT_TOO_SHORT` step 3: _Calculer._

### curriculum — 1ERE / Suites (row 25, exo 2)
- **Q**: $(v_n)$ est géométrique avec $v_0 = 2$ et $q = 3$. Calculer $v_3$.
- **A**: $v_3 = 54$
- `WARN_HINT_IS_FORMULA` step 1: _Suite géométrique :$v_n = v_0 q^n$._
- `WARN_HINT_IS_FORMULA` step 2: _$v_3 = 2 \times 3^3$._
- `WARN_HINT_TOO_SHORT` step 3: _Calculer._

### curriculum — 1ERE / Suites (row 25, exo 3)
- **Q**: $u_n = 2n + 3$. La suite est-elle arithmétique ?
- **A**: Oui, de raison $r = 2$
- `WARN_HINT_IS_FORMULA` step 2: _$u_{n+1} - u_n = 2(n+1)+3 - (2n+3)$._

### curriculum — 1ERE / Suites (row 25, exo 4)
- **Q**: Calculer $S = u_0 + u_1 + \ldots + u_{5}$ avec $u_0=1$, $r=4$.
- **A**: $S = 66$
- `WARN_HINT_IS_FORMULA` step 2: _$u_5 = 21$._

### curriculum — 1ERE / Suites (row 25, exo 5)
- **Q**: $u_{n+1} = u_n + 2$, $u_0 = 1$. Exprimer $u_n$ en fonction de $n$.
- **A**: $u_n = 2n + 1$
- `WARN_HINT_IS_FORMULA` step 1: _Identifier :$r = 2$._
- `WARN_HINT_IS_FORMULA` step 2: _$u_0 = 1$._
- `WARN_HINT_IS_FORMULA` step 3: _Appliquer $u_n = u_0 + nr$._

### curriculum — 1ERE / Suites (row 25, exo 6)
- **Q**: $v_0 = 1$, $v_{n+1} = 2 v_n$. Quelle est la nature de $(v_n)$?
- **A**: Géométrique de raison $q = 2$
- `WARN_HINT_IS_FORMULA` step 1: _$v_{n+1}/v_n = ?$_

### curriculum — 1ERE / Suites (row 25, exo 7)
- **Q**: $u_n = (-1)^n$. La suite est-elle monotone ?
- **A**: Non, elle alterne entre $1$ et $-1$
- `WARN_HINT_IS_FORMULA` step 2: _$u_0=1, u_1=-1, u_2=1$._

### curriculum — 1ERE / Suites (row 25, exo 8)
- **Q**: $u_n = \frac{3n+1}{2n+3}$. Que vaut $\lim_{n \to +\infty} u_n$?
- **A**: $\frac{3}{2}$
- `WARN_HINT_IS_FORMULA` step 3: _$\lim = 3/2$._

### curriculum — 1ERE / Suites (row 25, exo 9)
- **Q**: Si $u_n = 3n - 1$, que vaut $u_5 - u_3$?
- **A**: $6$
- `WARN_HINT_IS_FORMULA` step 1: _$u_5 = 14$._
- `WARN_HINT_IS_FORMULA` step 2: _$u_3 = 8$._

### curriculum — 1ERE / Suites (row 25, exo 11)
- **Q**: Montrer par récurrence que $u_n = 2^n + 1$ vérifie $u_{n+1} = 2u_n - 1$.
- **A**: Vrai par calcul direct
- `WARN_HINT_IS_FORMULA` step 2: _$= 2(2^n + 1) - 1 = 2^{n+1} + 1$._

### curriculum — 1ERE / Suites (row 25, exo 13)
- **Q**: $v_0 = 1$, $q = 2$. Calculer $S = \sum_{k=0}^{6} v_k$.
- **A**: $S = \frac{-127}{-1}$
- `WARN_HINT_IS_FORMULA` step 1: _La suite est géométrique de raison $q = 2$$ et de premier terme $v_0 = 1$,$. On utilise la formule $_
- `WARN_HINT_IS_FORMULA` step 2: _On remplace : $v_n = 1 \times 2^n$. Il reste à calculer la puissance pour la valeur de $n$ demandée._

### curriculum — 1ERE / Suites (row 25, exo 14)
- **Q**: $(u_n)$ arithmétique, $u_2 = 7$ et $u_5 = 16$. Trouver $u_0$ et $r$.
- **A**: $r = 3$, $u_0 = 1$
- `WARN_HINT_IS_FORMULA` step 1: _$u_5 - u_2 = 3r$._
- `WARN_HINT_IS_FORMULA` step 2: _$3r = 16 - 7 = 9$, $r = 3$._
- `WARN_HINT_IS_FORMULA` step 3: _$u_0 = u_2 - 2r = 7 - 6 = 1$._

### curriculum — 1ERE / Suites (row 25, exo 15)
- **Q**: $u_n = n^2 - 4n$. Étudier le sens de variation.
- **A**: Décroissante puis croissante
- `WARN_HINT_IS_ANSWER` step 3: _Signe change : décroissante puis croissante._
- `WARN_HINT_IS_FORMULA` step 1: _$u_{n+1} - u_n = 2n + 1 - 4$._
- `WARN_HINT_IS_FORMULA` step 2: _$= 0$ quand $n = 1{,}5$._

### curriculum — 1ERE / Suites (row 25, exo 16)
- **Q**: $u_n = n^2 - 4n$. Étudier le sens de variation.
- **A**: Décroissante puis croissante
- `WARN_HINT_IS_ANSWER` step 3: _Signe change : décroissante puis croissante._
- `WARN_HINT_IS_FORMULA` step 1: _$u_{n+1} - u_n = 2n + 1 - 4$._
- `WARN_HINT_IS_FORMULA` step 2: _$= 0$ quand $n = 1{,}5$._

### curriculum — 1ERE / Suites (row 25, exo 17)
- **Q**: Un capital de $1000$ € est placé à $2$ % par an. Quelle est sa valeur après 5 an
- **A**: $1000 \times 1{,}02^5$
- `WARN_HINT_IS_FORMULA` step 1: _Taux :$t = 0{,}02$._
- `WARN_HINT_IS_FORMULA` step 2: _$C_n = C_0 \times (1+t)^n$._

### curriculum — 1ERE / Suites (row 25, exo 18)
- **Q**: Un capital de $1000$ € est placé à $2$ % par an. Quelle est sa valeur après 5 an
- **A**: $1000 \times 1{,}02^5$
- `WARN_HINT_IS_FORMULA` step 1: _Taux :$t = 0{,}02$._
- `WARN_HINT_IS_FORMULA` step 2: _$C_n = C_0 \times (1+t)^n$._

### curriculum — 1ERE / Suites (row 25, exo 19)
- **Q**: $u_0 = 2$, $u_{n+1} = \sqrt{u_n + 6}$. Conjecturer la limite.
- **A**: $\ell = \frac{1+\sqrt{25}}{2}$
- `WARN_HINT_IS_FORMULA` step 2: _$\ell^2 = \ell + 6$._

### curriculum — 1ERE / Suites (row 25, exo 20)
- **Q**: $u_0 = 2$, $u_{n+1} = \sqrt{u_n + 6}$. Conjecturer la limite.
- **A**: $\ell = \frac{1+\sqrt{25}}{2}$
- `WARN_HINT_IS_FORMULA` step 2: _$\ell^2 = \ell + 6$._

### curriculum — 1ERE / Derivation (row 26, exo 1)
- **Q**: Dériver $f(x) = x^3$.
- **A**: $3x^2$
- `WARN_HINT_IS_FORMULA` step 1: _On dérive $f(x) = x^3$. La règle est $(x^n)' = nx^{n-1}$._
- `WARN_HINT_IS_FORMULA` step 2: _Pour $x^3$, on multiplie par l'exposant $n = 3$ et on diminue l'exposant de $1$ : $3 \cdot x^{2}$._

### curriculum — 1ERE / Derivation (row 26, exo 2)
- **Q**: Dériver $f(x) = 2x^2 + 3x - 1$.
- **A**: $4x + 3$
- `WARN_HINT_IS_FORMULA` step 1: _On dérive $f(x) = 2x^2 + 3x - 1$. La règle est $(x^n)' = nx^{n-1}$._
- `WARN_HINT_IS_FORMULA` step 2: _Pour $x^2$, on multiplie par l'exposant $n = 2$ et on diminue l'exposant de $1$ : $2 \cdot x^{1}$._

### curriculum — 1ERE / Derivation (row 26, exo 3)
- **Q**: Dériver $f(x) = \frac{1}{x}$.
- **A**: $-\frac{1}{x^2}$
- `WARN_HINT_IS_FORMULA` step 1: _On dérive $f(x) = \frac{1}{x}$ en utilisant la formule du quotient : $\left(\frac{u}{v}\right)' = \f_
- `WARN_HINT_IS_FORMULA` step 2: _On identifie $u$ (numérateur) et $v$ (dénominateur) dans $f(x) = \frac{1}{x}$, puis on calcule $u'$ _

### curriculum — 1ERE / Derivation (row 26, exo 4)
- **Q**: Dériver $f(x) = \sqrt{x}$.
- **A**: $\frac{1}{2\sqrt{x}}$
- `WARN_HINT_IS_FORMULA` step 1: _On dérive $f(x) = \sqrt{x}$ terme par terme en appliquant les formules : $(x^n)' = nx^{n-1}$, $(kx)'_
- `WARN_HINT_IS_FORMULA` step 2: _On calcule la dérivée de chaque terme de $f(x) = \sqrt{x}$ séparément._

### curriculum — 1ERE / Derivation (row 26, exo 5)
- **Q**: Dériver $f(x) = e^x$.
- **A**: $e^x$
- `WARN_HINT_IS_ANSWER` step 1: _On dérive $f(x) = e^x$. La fonction exponentielle est sa propre dérivée : $(e^x)' = e^x$._
- `WARN_HINT_IS_ANSWER` step 2: _Ici il n'y a qu'un seul terme : $e^x$. Sa dérivée est directement $e^x$._
- `WARN_HINT_IS_FORMULA` step 1: _On dérive $f(x) = e^x$. La fonction exponentielle est sa propre dérivée : $(e^x)' = e^x$._

### curriculum — 1ERE / Derivation (row 26, exo 6)
- **Q**: Dériver $f(x) = 3e^x + 2$.
- **A**: $3e^x$
- `WARN_HINT_IS_ANSWER` step 1: _On dérive $f(x) = 3e^x + 2$ terme par terme. On utilise $(e^x)' = e^x$ et $(c)' = 0$._
- `WARN_HINT_IS_ANSWER` step 2: _La dérivée de $3e^x$ est $3 \times e^x = 3e^x$ (le coefficient se conserve). La dérivée de $2$ est $_
- `WARN_HINT_IS_FORMULA` step 1: _On dérive $f(x) = 3e^x + 2$ terme par terme. On utilise $(e^x)' = e^x$ et $(c)' = 0$._
- `WARN_HINT_IS_FORMULA` step 2: _La dérivée de $3e^x$ est $3 \times e^x = 3e^x$ (le coefficient se conserve). La dérivée de $2$ est $_

### curriculum — 1ERE / Derivation (row 26, exo 7)
- **Q**: Dériver $f(x) = 2x^3 - x$.
- **A**: $6x^2 - 1$
- `WARN_HINT_IS_FORMULA` step 1: _On dérive $f(x) = 2x^3 - x$. La règle est $(x^n)' = nx^{n-1}$._
- `WARN_HINT_IS_FORMULA` step 2: _Pour $x^3$, on multiplie par l'exposant $n = 3$ et on diminue l'exposant de $1$ : $3 \cdot x^{2}$._

### curriculum — 1ERE / Derivation (row 26, exo 8)
- **Q**: Dériver $f(x) = (x+1)^2$.
- **A**: $2(x+1)$
- `WARN_HINT_IS_FORMULA` step 1: _On dérive $f(x) = (x+1)^2$ terme par terme en appliquant les formules : $(x^n)' = nx^{n-1}$, $(kx)' _
- `WARN_HINT_IS_FORMULA` step 2: _On calcule la dérivée de chaque terme de $f(x) = (x+1)^2$ séparément._

### curriculum — 1ERE / Derivation (row 26, exo 9)
- **Q**: Dériver $f(x) = \sin(x)$.
- **A**: $\cos(x)$
- `WARN_HINT_IS_FORMULA` step 1: _On dérive $f(x) = \sin(x)$ terme par terme en appliquant les formules : $(x^n)' = nx^{n-1}$, $(kx)' _
- `WARN_HINT_IS_FORMULA` step 2: _On calcule la dérivée de chaque terme de $f(x) = \sin(x)$ séparément._

### curriculum — 1ERE / Derivation (row 26, exo 10)
- **Q**: Dériver $f(x) = \cos(x)$.
- **A**: $-\sin(x)$
- `WARN_HINT_IS_FORMULA` step 1: _On dérive $f(x) = \cos(x)$ terme par terme en appliquant les formules : $(x^n)' = nx^{n-1}$, $(kx)' _
- `WARN_HINT_IS_FORMULA` step 2: _On calcule la dérivée de chaque terme de $f(x) = \cos(x)$ séparément._

### curriculum — 1ERE / Derivation (row 26, exo 11)
- **Q**: Équation de la tangente à $f(x) = x^2$ en $x_0 = 1$.
- **A**: $y = 2x - 1$
- `WARN_HINT_IS_FORMULA` step 1: _$f'(x)=2x$, $f'(1)=2$._
- `WARN_HINT_IS_FORMULA` step 2: _$f(1)=1$._
- `WARN_HINT_IS_FORMULA` step 3: _Appliquer $y=f'(a)(x-a)+f(a)$._
- `WARN_HINT_TOO_SHORT` step 2: _$f(1)=1$._

### curriculum — 1ERE / Derivation (row 26, exo 12)
- **Q**: $f(x) = x^3 - 3x$. Trouver les extrema.
- **A**: $x = \pm\sqrt{\frac{3}{3}}$
- `WARN_HINT_IS_FORMULA` step 1: _On dérive $f(x) = x^3 - 3x$. La règle est $(x^n)' = nx^{n-1}$._
- `WARN_HINT_IS_FORMULA` step 2: _Pour $x^3$, on multiplie par l'exposant $n = 3$ et on diminue l'exposant de $1$ : $3 \cdot x^{2}$._

### curriculum — 1ERE / Derivation (row 26, exo 13)
- **Q**: $f(x) = xe^x$. Calculer $f'(x)$.
- **A**: $(1+x)e^x$
- `WARN_HINT_IS_ANSWER` step 3: _$f' = e^x + xe^x = (1+x)e^x$._
- `WARN_HINT_IS_FORMULA` step 1: _$u=x$, $v=e^x$._
- `WARN_HINT_IS_FORMULA` step 2: _$u'=1$, $v'=e^x$._
- `WARN_HINT_IS_FORMULA` step 3: _$f' = e^x + xe^x = (1+x)e^x$._

### curriculum — 1ERE / Derivation (row 26, exo 14)
- **Q**: $f(x) = \frac{x+1}{x-1}$. Calculer $f'(x)$.
- **A**: $\frac{-2}{(x-1)^2}$
- `WARN_HINT_IS_FORMULA` step 1: _$u = x+1$, $v = x-1$._
- `WARN_HINT_IS_FORMULA` step 2: _$u'v - uv' = 1(x-1) - (x+1)$._
- `WARN_HINT_TOO_SHORT` step 3: _$= -2$._

### curriculum — 1ERE / Derivation (row 26, exo 15)
- **Q**: Dresser le tableau de variation de $f(x) = -x^2 + 4x$ sur $\mathbb{R}$.
- **A**: Croissante puis décroissante, max en $x=
- `WARN_HINT_IS_FORMULA` step 1: _$f'(x) = -2x + 4$._
- `WARN_HINT_IS_FORMULA` step 2: _$f'(x) = 0 \Rightarrow x = 2$._
- `WARN_HINT_IS_FORMULA` step 3: _$a = -1 < 0$ $\rightarrow$ maximum._

### curriculum — 1ERE / Derivation (row 26, exo 16)
- **Q**: $f(x) = (x^2+2)e^x$. Signe de $f'(0)$?
- **A**: Positif ($f'(0) = 2$)
- `WARN_HINT_IS_FORMULA` step 1: _$f'(x) = (2x)e^x + (x^2+2)e^x$._
- `WARN_HINT_IS_FORMULA` step 2: _$f'(x) = (x^2+2x+2)e^x$._
- `WARN_HINT_IS_FORMULA` step 3: _$f'(0) = 2 > 0$._

### curriculum — 1ERE / Derivation (row 26, exo 17)
- **Q**: $f(x) = (x^2+3)e^x$. Signe de $f'(0)$?
- **A**: Positif ($f'(0) = 3$)
- `WARN_HINT_IS_FORMULA` step 1: _$f'(x) = (2x)e^x + (x^2+3)e^x$._
- `WARN_HINT_IS_FORMULA` step 2: _$f'(x) = (x^2+2x+3)e^x$._
- `WARN_HINT_IS_FORMULA` step 3: _$f'(0) = 3 > 0$._

### curriculum — 1ERE / Derivation (row 26, exo 18)
- **Q**: $f(x) = (x^2+4)e^x$. Signe de $f'(0)$?
- **A**: Positif ($f'(0) = 4$)
- `WARN_HINT_IS_FORMULA` step 1: _$f'(x) = (2x)e^x + (x^2+4)e^x$._
- `WARN_HINT_IS_FORMULA` step 2: _$f'(x) = (x^2+2x+4)e^x$._
- `WARN_HINT_IS_FORMULA` step 3: _$f'(0) = 4 > 0$._

### curriculum — 1ERE / Derivation (row 26, exo 19)
- **Q**: $f(x) = (x^2+5)e^x$. Signe de $f'(0)$?
- **A**: Positif ($f'(0) = 5$)
- `WARN_HINT_IS_FORMULA` step 1: _$f'(x) = (2x)e^x + (x^2+5)e^x$._
- `WARN_HINT_IS_FORMULA` step 2: _$f'(x) = (x^2+2x+5)e^x$._
- `WARN_HINT_IS_FORMULA` step 3: _$f'(0) = 5 > 0$._

### curriculum — 1ERE / Derivation (row 26, exo 20)
- **Q**: $f(x) = (x^2+6)e^x$. Signe de $f'(0)$?
- **A**: Positif ($f'(0) = 6$)
- `WARN_HINT_IS_FORMULA` step 1: _$f'(x) = (2x)e^x + (x^2+6)e^x$._
- `WARN_HINT_IS_FORMULA` step 2: _$f'(x) = (x^2+2x+6)e^x$._
- `WARN_HINT_IS_FORMULA` step 3: _$f'(0) = 6 > 0$._

### curriculum — 1ERE / Exponentielle (row 27, exo 1)
- **Q**: Simplifier $e^{2} \times e^{3}$.
- **A**: $e^{5}$
- `WARN_HINT_IS_FORMULA` step 1: _On simplifie $e^{2} \times e^{3}$. D'après la propriété $e^a \times e^b = e^{a+b}$, on additionne le_

### curriculum — 1ERE / Exponentielle (row 27, exo 2)
- **Q**: Simplifier $\frac{e^{5}}{e^{2}}$.
- **A**: $e^3$
- `WARN_HINT_IS_FORMULA` step 1: _On simplifie $\frac{e^{5}}{e^{2}}$. D'après la propriété $\frac{e^a}{e^b} = e^{a-b}$, on soustrait l_

### curriculum — 1ERE / Exponentielle (row 27, exo 3)
- **Q**: Que vaut $e^0$?
- **A**: $1$
- `WARN_HINT_IS_FORMULA` step 1: _On évalue $e^0$. La propriété fondamentale est : pour tout nombre $a \neq 0$, on a $a^0 = 1$._
- `WARN_HINT_IS_FORMULA` step 2: _L'exponentielle vérifie cette propriété : $e^0 = 1$. C'est un cas particulier de $e^{a-a} = e^a / e^_

### curriculum — 1ERE / Exponentielle (row 27, exo 4)
- **Q**: Simplifier $(e^{2})^3$.
- **A**: $e^{6}$
- `WARN_HINT_IS_FORMULA` step 1: _On simplifie $(e^{2})^3$. D'après la propriété $(e^a)^b = e^{a \times b}$, on multiplie les exposant_

### curriculum — 1ERE / Exponentielle (row 27, exo 5)
- **Q**: Résoudre $e^x = e^{3}$.
- **A**: $x = 3$
- `WARN_HINT_IS_FORMULA` step 1: _On résout $e^x = e^{3}$. On utilise le fait que $e^a = e^b \Leftrightarrow a = b$ (l'exponentielle e_
- `WARN_HINT_IS_FORMULA` step 2: _On met l'équation sous la forme $e^{{\text{{quelque chose}}}} = e^{{\text{{autre chose}}}}$ et on id_

### curriculum — 1ERE / Exponentielle (row 27, exo 7)
- **Q**: Calculer $e^{1} \times e^{-1}$.
- **A**: $1$
- `WARN_HINT_IS_FORMULA` step 1: _On calcule $e^{1} \times e^{-1}$. D'après la propriété $e^a \times e^b = e^{a+b}$, on additionne les_
- `WARN_HINT_IS_FORMULA` step 2: _Les exposants sont $1$ et $-1$. Leur somme vaut $1 + (-1) = 0$. Donc $e^1 \times e^{-1} = e^0$._
- `WARN_HINT_IS_FORMULA` step 3: _Or $e^0 = 1$, ce qui donne le résultat._

### curriculum — 1ERE / Exponentielle (row 27, exo 8)
- **Q**: Que vaut $\lim_{x \to +\infty} e^x$?
- **A**: $+\infty$
- `WARN_HINT_IS_ANSWER` step 1: _On étudie $\lim_{x \to +\infty} e^x$. L'exponentielle est strictement croissante sur $\mathbb{R}$._
- `WARN_HINT_IS_ANSWER` step 3: _On en déduit que la limite est $+\infty$ : l'exponentielle "explose" vers l'infini._

### curriculum — 1ERE / Exponentielle (row 27, exo 10)
- **Q**: Résoudre $e^{2x} = e^{2}$.
- **A**: $x = 1$
- `WARN_HINT_IS_FORMULA` step 1: _On résout $e^{2x} = e^{2}$. On utilise le fait que $e^a = e^b \Leftrightarrow a = b$ (l'exponentiell_
- `WARN_HINT_IS_FORMULA` step 2: _On met l'équation sous la forme $e^{{\text{{quelque chose}}}} = e^{{\text{{autre chose}}}}$ et on id_

### curriculum — 1ERE / Exponentielle (row 27, exo 11)
- **Q**: Résoudre $e^{2x} - 3e^x + 2 = 0$.
- **A**: Poser $X = e^x$ et résoudre le trinôme
- `WARN_HINT_IS_FORMULA` step 1: _On résout $e^{2x} - 3e^x + 2 = 0$. On utilise le fait que $e^a = e^b \Leftrightarrow a = b$ (l'expon_
- `WARN_HINT_IS_FORMULA` step 2: _On met l'équation sous la forme $e^{{\text{{quelque chose}}}} = e^{{\text{{autre chose}}}}$ et on id_

### curriculum — 1ERE / Exponentielle (row 27, exo 12)
- **Q**: Étudier le signe de $f(x) = e^x - 2$.
- **A**: $f(x) > 0$ si $x > \ln(2)$
- `WARN_HINT_IS_FORMULA` step 1: _On simplifie $f(x) = e^x - 2$ en identifiant la propriété de l'exponentielle à utiliser ($e^{a+b}$, _

### curriculum — 1ERE / Exponentielle (row 27, exo 13)
- **Q**: Dériver $f(x) = x e^{-x}$.
- **A**: $(1-x)e^{-x}$
- `WARN_HINT_IS_FORMULA` step 1: _On dérive $f(x) = x e^{-x}$. La dérivée de $e^u$ est $u' \cdot e^u$._
- `WARN_HINT_IS_FORMULA` step 2: _On identifie $u$ dans $f(x) = x e^{-x}$ et on calcule $u'$._

### curriculum — 1ERE / Exponentielle (row 27, exo 14)
- **Q**: $f(x) = e^{2x} - 4e^x + 3$. Résoudre $f(x) = 0$.
- **A**: $x = \ln(1)$ ou $x = \ln(3)$
- `WARN_HINT_IS_FORMULA` step 1: _On résout $f(x) = e^{2x} - 4e^x + 3$. On utilise le fait que $e^a = e^b \Leftrightarrow a = b$ (l'ex_
- `WARN_HINT_IS_FORMULA` step 2: _On met l'équation sous la forme $e^{{\text{{quelque chose}}}} = e^{{\text{{autre chose}}}}$ et on id_

### curriculum — 1ERE / Exponentielle (row 27, exo 15)
- **Q**: Montrer que $\lim_{x \to +\infty} xe^{-x} = 0$.
- **A**: Croissance comparée :$e^x \gg x$
- `WARN_HINT_IS_FORMULA` step 1: _On simplifie $\lim_{x \to +\infty} xe^{-x} = 0$ en identifiant la propriété de l'exponentielle à uti_

### curriculum — 1ERE / Exponentielle (row 27, exo 16)
- **Q**: Population modélisée par $P(t) = 1000 e^{0{,}02t}$. Temps de doublement ?
- **A**: $t = \frac{\ln 2}{0{,}02}$
- `WARN_HINT_IS_FORMULA` step 1: _On évalue $P(t) = 1000 e^{0{,}02t}$. La propriété fondamentale est $e^0 = 1$._

### curriculum — 1ERE / Exponentielle (row 27, exo 17)
- **Q**: Résoudre $e^x \geq 1$.
- **A**: $x \geq \ln(1)$
- `WARN_HINT_IS_FORMULA` step 1: _On résout $e^x \geq 1$. On utilise le fait que $e^a = e^b \Leftrightarrow a = b$ (l'exponentielle es_
- `WARN_HINT_IS_FORMULA` step 2: _On met l'équation sous la forme $e^{{\text{{quelque chose}}}} = e^{{\text{{autre chose}}}}$ et on id_

### curriculum — 1ERE / Exponentielle (row 27, exo 18)
- **Q**: Étudier les variations de $f(x) = e^{2x} - 2x$.
- **A**: Décroissante puis croissante
- `WARN_HINT_IS_FORMULA` step 1: _On simplifie $f(x) = e^{2x} - 2x$ en identifiant la propriété de l'exponentielle à utiliser ($e^{a+b_

### curriculum — 1ERE / Exponentielle (row 27, exo 19)
- **Q**: Simplifier $\ln(e^{3})$.
- **A**: $3$
- `WARN_HINT_IS_FORMULA` step 1: _On simplifie $\ln(e^{3})$. Le logarithme népérien est la fonction réciproque de l'exponentielle : $\_
- `WARN_HINT_IS_FORMULA` step 2: _Ici $a = 3$, donc $\ln(e^3) = 3$. Le logarithme "annule" l'exponentielle._

### curriculum — 1ERE / Exponentielle (row 27, exo 20)
- **Q**: Vrai ou faux :$e^{a+b} = e^a + e^b$?
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 1: _On simplifie $e^{a+b} = e^a + e^b$ en identifiant la propriété de l'exponentielle à utiliser ($e^{a+_

### curriculum — 1ERE / Trigonometrie (row 28, exo 2)
- **Q**: Que vaut $\sin(\pi/6)$?
- **A**: $1/2$
- `WARN_HINT_IS_FORMULA` step 2: _Pour l'angle $\pi/6$, on utilise les valeurs remarquables : $\sin(\pi/6) = \frac{1}{2}$, $\sin(\pi/4_

### curriculum — 1ERE / Trigonometrie (row 28, exo 3)
- **Q**: Que vaut $\cos(\pi/4)$?
- **A**: $\sqrt{2}/2$
- `WARN_HINT_IS_FORMULA` step 2: _Pour l'angle $\pi/4$, on utilise les valeurs remarquables : $\cos(\pi/6) = \frac{\sqrt{3}}{2}$, $\co_

### curriculum — 1ERE / Trigonometrie (row 28, exo 5)
- **Q**: Que vaut $\cos(\pi)$?
- **A**: $-1$
- `WARN_HINT_IS_FORMULA` step 2: _Pour l'angle $\pi$, on utilise les valeurs remarquables : $\cos(\pi/6) = \frac{\sqrt{3}}{2}$, $\cos(_

### curriculum — 1ERE / Trigonometrie (row 28, exo 6)
- **Q**: Que vaut $\sin(\pi/3)$?
- **A**: $\sqrt{3}/2$
- `WARN_HINT_IS_FORMULA` step 2: _Pour l'angle $\pi/3$, on utilise les valeurs remarquables : $\sin(\pi/6) = \frac{1}{2}$, $\sin(\pi/4_

### curriculum — 1ERE / Trigonometrie (row 28, exo 7)
- **Q**: Que vaut $\cos(\pi/3)$?
- **A**: $1/2$
- `WARN_HINT_IS_FORMULA` step 2: _Pour l'angle $\pi/3$, on utilise les valeurs remarquables : $\cos(\pi/6) = \frac{\sqrt{3}}{2}$, $\co_

### curriculum — 1ERE / Trigonometrie (row 28, exo 8)
- **Q**: Que vaut $\sin(\pi)$?
- **A**: $0$
- `WARN_HINT_IS_FORMULA` step 2: _Pour l'angle $\pi$, on utilise les valeurs remarquables : $\sin(\pi/6) = \frac{1}{2}$, $\sin(\pi/4) _

### curriculum — 1ERE / Trigonometrie (row 28, exo 9)
- **Q**: Que vaut $\cos(\pi/6)$?
- **A**: $\sqrt{3}/2$
- `WARN_HINT_IS_FORMULA` step 2: _Pour l'angle $\pi/6$, on utilise les valeurs remarquables : $\cos(\pi/6) = \frac{\sqrt{3}}{2}$, $\co_

### curriculum — 1ERE / Trigonometrie (row 28, exo 10)
- **Q**: Quelle est la période de $\cos(x)$?
- **A**: $2\pi$
- `WARN_HINT_IS_FORMULA` step 2: _Pour l'angle $x$, on utilise les valeurs remarquables : $\cos(\pi/6) = \frac{\sqrt{3}}{2}$, $\cos(\p_

### curriculum — 1ERE / Trigonometrie (row 28, exo 11)
- **Q**: Résoudre $\cos(x) = \frac{1}{2}$ sur $[0; 2\pi]$.
- **A**: $x = \pi/3$ ou $x = 5\pi/3$
- `WARN_HINT_IS_FORMULA` step 2: _Pour l'angle $x$, on utilise les valeurs remarquables : $\cos(\pi/6) = \frac{\sqrt{3}}{2}$, $\cos(\p_

### curriculum — 1ERE / Trigonometrie (row 28, exo 12)
- **Q**: Résoudre $\sin(x) = \frac{\sqrt{2}}{2}$ sur $[0; 2\pi]$.
- **A**: $x = \pi/4$ ou $x = 3\pi/4$
- `WARN_HINT_IS_FORMULA` step 2: _Pour l'angle $x$, on utilise les valeurs remarquables : $\sin(\pi/6) = \frac{1}{2}$, $\sin(\pi/4) = _

### curriculum — 1ERE / Trigonometrie (row 28, exo 14)
- **Q**: Résoudre $2\sin(x) - 1 = 0$ sur $[0; 2\pi]$.
- **A**: $\sin(x) = 0{,}5$
- `WARN_HINT_IS_FORMULA` step 2: _Pour l'angle $x$, on utilise les valeurs remarquables : $\sin(\pi/6) = \frac{1}{2}$, $\sin(\pi/4) = _

### curriculum — 1ERE / Trigonometrie (row 28, exo 15)
- **Q**: Exprimer $\cos(2x)$ en fonction de $\cos(x)$.
- **A**: $2\cos^2(x) - 1$
- `WARN_HINT_IS_FORMULA` step 2: _Pour l'angle $2x$, on utilise les valeurs remarquables : $\cos(\pi/6) = \frac{\sqrt{3}}{2}$, $\cos(\_

### curriculum — 1ERE / Trigonometrie (row 28, exo 16)
- **Q**: Donner la dérivée de $\sin(2x)$.
- **A**: $2\cos(2x)$
- `WARN_HINT_IS_FORMULA` step 2: _Pour l'angle $2x$, on utilise les valeurs remarquables : $\sin(\pi/6) = \frac{1}{2}$, $\sin(\pi/4) =_

### curriculum — 1ERE / Trigonometrie (row 28, exo 17)
- **Q**: $f(x) = \sin(x) + \cos(x)$. Calculer $f(\pi/4)$.
- **A**: $\sqrt{2}$
- `WARN_HINT_IS_ANSWER` step 2: _On sait que $\sin(\pi/4) = \frac{\sqrt{2}}{2}$ et $\cos(\pi/4) = \frac{\sqrt{2}}{2}$. On additionne _
- `WARN_HINT_IS_ANSWER` step 3: _La somme $\frac{\sqrt{2}}{2} + \frac{\sqrt{2}}{2}$ se simplifie._
- `WARN_HINT_IS_FORMULA` step 1: _On calcule $f(\pi/4) = \sin(\pi/4) + \cos(\pi/4)$. On utilise les valeurs remarquables pour $\pi/4$._
- `WARN_HINT_IS_FORMULA` step 2: _On sait que $\sin(\pi/4) = \frac{\sqrt{2}}{2}$ et $\cos(\pi/4) = \frac{\sqrt{2}}{2}$. On additionne _

### curriculum — 1ERE / Trigonometrie (row 28, exo 18)
- **Q**: Résoudre $\cos(x) = -\frac{\sqrt{3}}{2}$ sur $[0; 2\pi]$.
- **A**: $x = 5\pi/6$ ou $x = 7\pi/6$
- `WARN_HINT_IS_FORMULA` step 2: _Pour l'angle $x$, on utilise les valeurs remarquables : $\cos(\pi/6) = \frac{\sqrt{3}}{2}$, $\cos(\p_

### curriculum — 1ERE / Trigonometrie (row 28, exo 19)
- **Q**: Montrer que $\sin(\pi - x) = \sin(x)$.
- **A**: Vrai (symétrie par rapport à $\pi/2$)
- `WARN_HINT_IS_FORMULA` step 2: _Pour l'angle $\pi - x$, on utilise les valeurs remarquables : $\sin(\pi/6) = \frac{1}{2}$, $\sin(\pi_

### curriculum — 1ERE / Trigonometrie (row 28, exo 20)
- **Q**: Amplitude et période de $f(x) = 3\sin(2x + \pi/3)$?
- **A**: Amplitude $3$, période $\pi$
- `WARN_HINT_IS_FORMULA` step 2: _Pour l'angle $2x + \pi/3$, on utilise les valeurs remarquables : $\sin(\pi/6) = \frac{1}{2}$, $\sin(_

### curriculum — 1ERE / Produit_Scalaire (row 29, exo 1)
- **Q**: $\vec{u}(2;3)$ et $\vec{v}(1;4)$. Calculer $\vec{u} \cdot \vec{v}$.
- **A**: $14$
- `WARN_HINT_IS_FORMULA` step 1: _On calcule $\vec{u} \cdot \vec{v}$ avec les coordonnées. La formule est $\vec{u} \cdot \vec{v} = x_u_
- `WARN_HINT_IS_FORMULA` step 2: _On remplace : $\vec{u} \cdot \vec{v} = 2 \times 1 + 3 \times 4$._

### curriculum — 1ERE / Produit_Scalaire (row 29, exo 2)
- **Q**: $\|\vec{u}\| = 3$, $\|\vec{v}\| = 2$, angle $60°$. Calculer $\vec{u} \cdot \vec{
- **A**: $3$
- `WARN_HINT_IS_FORMULA` step 1: _On calcule le produit scalaire avec la formule $\vec{u} \cdot \vec{v} = \|\vec{u}\| \times \|\vec{v}_

### curriculum — 1ERE / Produit_Scalaire (row 29, exo 3)
- **Q**: $\vec{u}(1;2)$ et $\vec{v}(-2;1)$. Sont-ils orthogonaux ?
- **A**: Oui
- `WARN_HINT_IS_FORMULA` step 1: _On calcule $\vec{u} \cdot \vec{v}$ avec les coordonnées. La formule est $\vec{u} \cdot \vec{v} = x_u_
- `WARN_HINT_IS_FORMULA` step 2: _On remplace : $\vec{u} \cdot \vec{v} = 1 \times -2 + 2 \times 1$._

### curriculum — 1ERE / Produit_Scalaire (row 29, exo 4)
- **Q**: Calculer $\|\vec{u}\|$ avec $\vec{u}(3;4)$.
- **A**: $\sqrt{25}$
- `WARN_HINT_IS_FORMULA` step 1: _On calcule le produit scalaire avec la formule $\vec{u} \cdot \vec{v} = \|\vec{u}\| \times \|\vec{v}_

### curriculum — 1ERE / Produit_Scalaire (row 29, exo 5)
- **Q**: $\vec{AB} \cdot \vec{AC} = 0$. Que peut-on dire du triangle $ABC$?
- **A**: Rectangle en $A$
- `WARN_HINT_IS_FORMULA` step 1: _On calcule le produit scalaire avec la formule $\vec{u} \cdot \vec{v} = \|\vec{u}\| \times \|\vec{v}_

### curriculum — 1ERE / Produit_Scalaire (row 29, exo 6)
- **Q**: $\vec{u}(1;0)$ et $\vec{v}(0;2)$. Calculer $\vec{u} \cdot \vec{v}$.
- **A**: $0$
- `WARN_HINT_IS_FORMULA` step 1: _$x_u x_v = 1 \times ? = ?.$_
- `WARN_HINT_IS_FORMULA` step 2: _$y_u y_v = ? \times 2 = ?.$_

### curriculum — 1ERE / Produit_Scalaire (row 29, exo 7)
- **Q**: $\vec{u}(2;0)$ et $\vec{v}(0;3)$. Calculer $\vec{u} \cdot \vec{v}$.
- **A**: $0$
- `WARN_HINT_IS_FORMULA` step 1: _$x_u x_v = 2 \times ? = ?.$_
- `WARN_HINT_IS_FORMULA` step 2: _$y_u y_v = ? \times 3 = ?.$_

### curriculum — 1ERE / Produit_Scalaire (row 29, exo 8)
- **Q**: $\vec{u}(3;0)$ et $\vec{v}(0;4)$. Calculer $\vec{u} \cdot \vec{v}$.
- **A**: $0$
- `WARN_HINT_IS_FORMULA` step 1: _$x_u x_v = 3 \times ? = ?.$_
- `WARN_HINT_IS_FORMULA` step 2: _$y_u y_v = ? \times 4 = ?.$_

### curriculum — 1ERE / Produit_Scalaire (row 29, exo 9)
- **Q**: $\vec{u}(4;0)$ et $\vec{v}(0;5)$. Calculer $\vec{u} \cdot \vec{v}$.
- **A**: $0$
- `WARN_HINT_IS_FORMULA` step 1: _$x_u x_v = 4 \times ? = ?.$_
- `WARN_HINT_IS_FORMULA` step 2: _$y_u y_v = ? \times 5 = ?.$_

### curriculum — 1ERE / Produit_Scalaire (row 29, exo 10)
- **Q**: $\vec{u}(5;0)$ et $\vec{v}(0;6)$. Calculer $\vec{u} \cdot \vec{v}$.
- **A**: $0$
- `WARN_HINT_IS_FORMULA` step 1: _$x_u x_v = 5 \times ? = ?.$_
- `WARN_HINT_IS_FORMULA` step 2: _$y_u y_v = ? \times 6 = ?.$_

### curriculum — 1ERE / Produit_Scalaire (row 29, exo 11)
- **Q**: Triangle $ABC$ avec $AB=3$, $AC=4$, $BC=5$. Calculer $\vec{AB} \cdot \vec{AC}$ (
- **A**: $0$
- `WARN_HINT_IS_FORMULA` step 1: _On calcule le produit scalaire avec la formule $\vec{u} \cdot \vec{v} = \|\vec{u}\| \times \|\vec{v}_

### curriculum — 1ERE / Produit_Scalaire (row 29, exo 12)
- **Q**: Projeté orthogonal de $\vec{u}(4;2)$ sur $\vec{v}(1;0)$.
- **A**: $4$
- `WARN_HINT_IS_FORMULA` step 1: _On projette $\vec{u}(4;2)$ sur $\vec{v}(1;0)$. La formule est $\text{proj} = \frac{\vec{u} \cdot \ve_
- `WARN_HINT_IS_FORMULA` step 2: _On calcule $\vec{u} \cdot \vec{v} = 4 \times 1 + 2 \times 0 = 4$ et $\|\vec{v}\|^2 = 1^2 + 0^2 = 1$._
- `WARN_HINT_IS_FORMULA` step 3: _Le projeté vaut $\frac{4}{1} = 4$ (composante de $\vec{u}$ dans la direction de $\vec{v}$)._

### curriculum — 1ERE / Produit_Scalaire (row 29, exo 13)
- **Q**: $A(0;0)$, $B(2;0)$, $C(1;2)$. L'angle $\widehat{BAC}$ est-il droit ?
- **A**: Non, $\vec{AB} \cdot \vec{AC} = 2 \neq 0
- `WARN_HINT_IS_FORMULA` step 1: _On calcule le produit scalaire avec la formule $\vec{u} \cdot \vec{v} = \|\vec{u}\| \times \|\vec{v}_

### curriculum — 1ERE / Produit_Scalaire (row 29, exo 14)
- **Q**: $\vec{u}(2;3)$, $\vec{v}(1;-1)$. Trouver l'angle entre $\vec{u}$ et $\vec{v}$.
- **A**: $\cos(\theta) = \frac{-1}{\sqrt{26}}$
- `WARN_HINT_IS_FORMULA` step 1: _On calcule le produit scalaire avec la formule $\vec{u} \cdot \vec{v} = \|\vec{u}\| \times \|\vec{v}_

### curriculum — 1ERE / Produit_Scalaire (row 29, exo 15)
- **Q**: $\vec{u}(3;4)$, $\vec{v}(1;-1)$. Trouver l'angle entre $\vec{u}$ et $\vec{v}$.
- **A**: $\cos(\theta) = \frac{-1}{\sqrt{50}}$
- `WARN_HINT_IS_FORMULA` step 1: _On calcule le produit scalaire avec la formule $\vec{u} \cdot \vec{v} = \|\vec{u}\| \times \|\vec{v}_

### curriculum — 1ERE / Produit_Scalaire (row 29, exo 16)
- **Q**: $\vec{u}(4;5)$, $\vec{v}(1;-1)$. Trouver l'angle entre $\vec{u}$ et $\vec{v}$.
- **A**: $\cos(\theta) = \frac{-1}{\sqrt{82}}$
- `WARN_HINT_IS_FORMULA` step 1: _On calcule le produit scalaire avec la formule $\vec{u} \cdot \vec{v} = \|\vec{u}\| \times \|\vec{v}_

### curriculum — 1ERE / Produit_Scalaire (row 29, exo 17)
- **Q**: $\vec{u}(5;6)$, $\vec{v}(1;-1)$. Trouver l'angle entre $\vec{u}$ et $\vec{v}$.
- **A**: $\cos(\theta) = \frac{-1}{\sqrt{122}}$
- `WARN_HINT_IS_FORMULA` step 1: _On calcule le produit scalaire avec la formule $\vec{u} \cdot \vec{v} = \|\vec{u}\| \times \|\vec{v}_

### curriculum — 1ERE / Produit_Scalaire (row 29, exo 18)
- **Q**: $\vec{u}(6;7)$, $\vec{v}(1;-1)$. Trouver l'angle entre $\vec{u}$ et $\vec{v}$.
- **A**: $\cos(\theta) = \frac{-1}{\sqrt{170}}$
- `WARN_HINT_IS_FORMULA` step 1: _On calcule le produit scalaire avec la formule $\vec{u} \cdot \vec{v} = \|\vec{u}\| \times \|\vec{v}_

### curriculum — 1ERE / Produit_Scalaire (row 29, exo 19)
- **Q**: $\vec{u}(7;8)$, $\vec{v}(1;-1)$. Trouver l'angle entre $\vec{u}$ et $\vec{v}$.
- **A**: $\cos(\theta) = \frac{-1}{\sqrt{226}}$
- `WARN_HINT_IS_FORMULA` step 1: _On calcule le produit scalaire avec la formule $\vec{u} \cdot \vec{v} = \|\vec{u}\| \times \|\vec{v}_

### curriculum — 1ERE / Produit_Scalaire (row 29, exo 20)
- **Q**: $\vec{u}(8;9)$, $\vec{v}(1;-1)$. Trouver l'angle entre $\vec{u}$ et $\vec{v}$.
- **A**: $\cos(\theta) = \frac{-1}{\sqrt{290}}$
- `WARN_HINT_IS_FORMULA` step 1: _On calcule le produit scalaire avec la formule $\vec{u} \cdot \vec{v} = \|\vec{u}\| \times \|\vec{v}_

### curriculum — 1ERE / Geometrie_Repere (row 30, exo 1)
- **Q**: Donner un vecteur directeur de la droite $y = 1x + 2$.
- **A**: $\vec{u}(1;1)$
- `WARN_HINT_IS_ANSWER` step 2: _Ici $m = 1$. Le vecteur directeur est donc $\vec{u}(1; 1)$._
- `WARN_HINT_IS_FORMULA` step 1: _Pour une droite $y = mx + p$, un vecteur directeur est $\vec{u}(1; m)$. On lit le coefficient direct_
- `WARN_HINT_IS_FORMULA` step 2: _Ici $m = 1$. Le vecteur directeur est donc $\vec{u}(1; 1)$._

### curriculum — 1ERE / Geometrie_Repere (row 30, exo 2)
- **Q**: Donner un vecteur directeur de la droite $y = 2x + 3$.
- **A**: $\vec{u}(1;2)$
- `WARN_HINT_IS_ANSWER` step 2: _Ici $m = 2$. Le vecteur directeur est donc $\vec{u}(1; 2)$._
- `WARN_HINT_IS_FORMULA` step 1: _Pour une droite $y = mx + p$, un vecteur directeur est $\vec{u}(1; m)$. On lit le coefficient direct_
- `WARN_HINT_IS_FORMULA` step 2: _Ici $m = 2$. Le vecteur directeur est donc $\vec{u}(1; 2)$._

### curriculum — 1ERE / Geometrie_Repere (row 30, exo 3)
- **Q**: Donner un vecteur directeur de la droite $y = 3x + 4$.
- **A**: $\vec{u}(1;3)$
- `WARN_HINT_IS_ANSWER` step 2: _Ici $m = 3$. Le vecteur directeur est donc $\vec{u}(1; 3)$._
- `WARN_HINT_IS_FORMULA` step 1: _Pour une droite $y = mx + p$, un vecteur directeur est $\vec{u}(1; m)$. On lit le coefficient direct_
- `WARN_HINT_IS_FORMULA` step 2: _Ici $m = 3$. Le vecteur directeur est donc $\vec{u}(1; 3)$._

### curriculum — 1ERE / Geometrie_Repere (row 30, exo 4)
- **Q**: Equation de la droite passant par $A(4;5)$ de pente $6$.
- **A**: $y = 6x + -19$
- `WARN_HINT_IS_ANSWER` step 3: _$y = 6x + -19$._
- `WARN_HINT_IS_FORMULA` step 1: _$y - 5 = 6(x - 4)$._
- `WARN_HINT_IS_FORMULA` step 2: _$y = 6x - 24 + 5$._
- `WARN_HINT_IS_FORMULA` step 3: _$y = 6x + -19$._

### curriculum — 1ERE / Geometrie_Repere (row 30, exo 5)
- **Q**: Equation de la droite passant par $A(5;6)$ de pente $7$.
- **A**: $y = 7x + -29$
- `WARN_HINT_IS_ANSWER` step 3: _$y = 7x + -29$._
- `WARN_HINT_IS_FORMULA` step 1: _$y - 6 = 7(x - 5)$._
- `WARN_HINT_IS_FORMULA` step 2: _$y = 7x - 35 + 6$._
- `WARN_HINT_IS_FORMULA` step 3: _$y = 7x + -29$._

### curriculum — 1ERE / Geometrie_Repere (row 30, exo 6)
- **Q**: Vecteur normal à la droite $6x + 7y + 8 = 0$?
- **A**: $\vec{n}(6;7)$
- `WARN_HINT_IS_FORMULA` step 1: _Forme $ax+by+c=0$._
- `WARN_HINT_TOO_SHORT` step 3: _$(6;7)$._

### curriculum — 1ERE / Geometrie_Repere (row 30, exo 7)
- **Q**: Vecteur normal à la droite $7x + 8y + 9 = 0$?
- **A**: $\vec{n}(7;8)$
- `WARN_HINT_IS_FORMULA` step 1: _Forme $ax+by+c=0$._
- `WARN_HINT_TOO_SHORT` step 3: _$(7;8)$._

### curriculum — 1ERE / Geometrie_Repere (row 30, exo 8)
- **Q**: Distance entre $A(8;9)$ et $B(10;10)$.
- **A**: $\sqrt{5}$
- `WARN_HINT_IS_FORMULA` step 1: _On calcule la distance entre les points de coordonnées $(8; 9)$ et $(10; 10)$ avec la formule $d = \_
- `WARN_HINT_IS_FORMULA` step 2: _On calcule les différences : $x_B - x_A = 2$ et $y_B - y_A = 1$, puis on élève au carré et on additi_

### curriculum — 1ERE / Geometrie_Repere (row 30, exo 9)
- **Q**: Distance entre $A(9;10)$ et $B(11;11)$.
- **A**: $\sqrt{5}$
- `WARN_HINT_IS_FORMULA` step 1: _On calcule la distance entre les points de coordonnées $(9; 10)$ et $(11; 11)$ avec la formule $d = _
- `WARN_HINT_IS_FORMULA` step 2: _On calcule les différences : $x_B - x_A = 2$ et $y_B - y_A = 1$, puis on élève au carré et on additi_

### curriculum — 1ERE / Geometrie_Repere (row 30, exo 10)
- **Q**: Milieu de $[A(10;11), B(12;10)]$?
- **A**: $M(11{,}0;10{,}5)$
- `WARN_HINT_IS_FORMULA` step 1: _On cherche le milieu de $[AB]$ avec $A(10; 11)$ et $B(12; 10)$. La formule est $M = \left(\frac{x_A _

### curriculum — 1ERE / Geometrie_Repere (row 30, exo 14)
- **Q**: Les droites $y = 4x + 1$ et $y = -0{,}25x + 6$ sont-elles perpendiculaires ?
- **A**: Oui
- `WARN_HINT_IS_FORMULA` step 1: _$m_1 = 4$, $m_2 = -0{,}25$._
- `WARN_HINT_IS_FORMULA` step 2: _$m_1 \times m_2 = -1$._
- `WARN_HINT_TOO_SHORT` step 3: _Conclure._

### curriculum — 1ERE / Geometrie_Repere (row 30, exo 15)
- **Q**: Les droites $y = 5x + 1$ et $y = -0{,}20x + 7$ sont-elles perpendiculaires ?
- **A**: Oui
- `WARN_HINT_IS_FORMULA` step 1: _$m_1 = 5$, $m_2 = -0{,}20$._
- `WARN_HINT_IS_FORMULA` step 2: _$m_1 \times m_2 = -1$._
- `WARN_HINT_TOO_SHORT` step 3: _Conclure._

### curriculum — 1ERE / Geometrie_Repere (row 30, exo 16)
- **Q**: Intersection des droites $y = 6x + 8$ et $y = 7x + 7$.
- **A**: $(1; 14)$
- `WARN_HINT_IS_FORMULA` step 2: _$6x + 8 = 7x + 7$._
- `WARN_HINT_TOO_SHORT` step 3: _Résoudre._

### curriculum — 1ERE / Geometrie_Repere (row 30, exo 17)
- **Q**: Intersection des droites $y = 7x + 9$ et $y = 8x + 8$.
- **A**: $(1; 16)$
- `WARN_HINT_IS_FORMULA` step 2: _$7x + 9 = 8x + 8$._
- `WARN_HINT_TOO_SHORT` step 3: _Résoudre._

### curriculum — 1ERE / Geometrie_Repere (row 30, exo 18)
- **Q**: Distance du point $P(8;10)$ à la droite $9x + 11y + 1 = 0$.
- **A**: $\frac{|183|}{\sqrt{202}}$
- `WARN_HINT_TOO_SHORT` step 3: _Calculer._

### curriculum — 1ERE / Geometrie_Repere (row 30, exo 19)
- **Q**: Distance du point $P(9;11)$ à la droite $10x + 12y + 1 = 0$.
- **A**: $\frac{|223|}{\sqrt{244}}$
- `WARN_HINT_TOO_SHORT` step 3: _Calculer._

### curriculum — 1ERE / Geometrie_Repere (row 30, exo 20)
- **Q**: Distance du point $P(10;12)$ à la droite $11x + 13y + 1 = 0$.
- **A**: $\frac{|267|}{\sqrt{290}}$
- `WARN_HINT_TOO_SHORT` step 3: _Calculer._

### curriculum — 1ERE / Probabilites_Cond (row 31, exo 1)
- **Q**: $P(A) = 0{,}5$, $P(B|A) = 0{,}3$. Calculer $P(A \cap B)$.
- **A**: $0{,}15$
- `WARN_HINT_IS_FORMULA` step 1: _On cherche $P(A \cap B)$. D'après la formule des probabilités conditionnelles : $P(A \cap B) = P(A) _

### curriculum — 1ERE / Probabilites_Cond (row 31, exo 2)
- **Q**: $P(A \cap B) = 0{,}2$, $P(A) = 0{,}5$. Calculer $P(B|A)$.
- **A**: $\frac{0{,}2}{0{,}5}$
- `WARN_HINT_IS_FORMULA` step 1: _On cherche $P(A \cap B)$. D'après la formule des probabilités conditionnelles : $P(A \cap B) = P(A) _

### curriculum — 1ERE / Probabilites_Cond (row 31, exo 3)
- **Q**: Un test est positif à $40$ % si malade. $P(\text{malade}) = 0{,}01$. $P(\text{po
- **A**: $0{,}0040$
- `WARN_HINT_IS_FORMULA` step 1: _On cherche $P(A \cap B)$. D'après la formule des probabilités conditionnelles : $P(A \cap B) = P(A) _

### curriculum — 1ERE / Probabilites_Cond (row 31, exo 4)
- **Q**: Un test est positif à $50$ % si malade. $P(\text{malade}) = 0{,}01$. $P(\text{po
- **A**: $0{,}0050$
- `WARN_HINT_IS_FORMULA` step 1: _On cherche $P(A \cap B)$. D'après la formule des probabilités conditionnelles : $P(A \cap B) = P(A) _

### curriculum — 1ERE / Probabilites_Cond (row 31, exo 5)
- **Q**: Un test est positif à $60$ % si malade. $P(\text{malade}) = 0{,}01$. $P(\text{po
- **A**: $0{,}0060$
- `WARN_HINT_IS_FORMULA` step 1: _On cherche $P(A \cap B)$. D'après la formule des probabilités conditionnelles : $P(A \cap B) = P(A) _

### curriculum — 1ERE / Probabilites_Cond (row 31, exo 6)
- **Q**: $A$ et $B$ indépendants, $P(A) = 0{,}3$, $P(B) = 0{,}4$. $P(A \cap B)$ = ?
- **A**: $0{,}12$
- `WARN_HINT_IS_FORMULA` step 2: _$P(A \cap B) = P(A) \times P(B)$._
- `WARN_HINT_TOO_SHORT` step 3: _Calculer._

### curriculum — 1ERE / Probabilites_Cond (row 31, exo 7)
- **Q**: Dans un lycée, $60\%$ des élèves font du sport. Parmi eux, $70\%$ ont une bonne 
- **A**: $0{,}42$
- `WARN_HINT_IS_FORMULA` step 1: _$P(\text{sport}) = 0{,}6$, $P(\text{bonne note}|\text{sport}) = 0{,}7$._
- `WARN_HINT_IS_FORMULA` step 2: _$P(\text{sport} \cap \text{bonne note}) = 0{,}6 \times 0{,}7$._

### curriculum — 1ERE / Probabilites_Cond (row 31, exo 8)
- **Q**: On lance un dé. $A$ = obtenir un nombre pair, $B$ = obtenir un nombre $\geq 4$. 
- **A**: $\frac{2}{3}$
- `WARN_HINT_IS_FORMULA` step 1: _$B = \{4, 5, 6\}$, $P(B) = \frac{3}{6} = \frac{1}{2}$._
- `WARN_HINT_IS_FORMULA` step 2: _$A \cap B = \{4, 6\}$, $P(A \cap B) = \frac{2}{6} = \frac{1}{3}$._

### curriculum — 1ERE / Probabilites_Cond (row 31, exo 9)
- **Q**: Probabilité de pluie :$P(\text{pluie}) = 0{,}4$. Si pluie, $P(\text{retard}) = 0
- **A**: $0{,}38$
- `WARN_HINT_IS_FORMULA` step 1: _$P(\text{retard}) = P(\text{pluie}) \times P(\text{retard}|\text{pluie}) + P(\overline{\text{pluie}}_

### curriculum — 1ERE / Probabilites_Cond (row 31, exo 10)
- **Q**: Dans un sondage :$P(A) = 0{,}5$, $P(B) = 0{,}4$, $P(A \cap B) = 0{,}25$. $A$ et 
- **A**: Non
- `WARN_HINT_IS_FORMULA` step 1: _$P(A) \times P(B) = 0{,}5 \times 0{,}4 = 0{,}2$._
- `WARN_HINT_IS_FORMULA` step 2: _$P(A \cap B) = 0{,}25 \neq 0{,}2$._

### curriculum — 1ERE / Probabilites_Cond (row 31, exo 11)
- **Q**: Tableau de contingence :$120$ élèves, dont $70$ filles. Parmi les filles, $40$ f
- **A**: $\frac{4}{7}$
- `WARN_HINT_IS_FORMULA` step 1: _$P(\text{fille}) = \frac{70}{120}$._
- `WARN_HINT_IS_FORMULA` step 2: _$P(\text{musique} \cap \text{fille}) = \frac{40}{120}$._

### curriculum — 1ERE / Probabilites_Cond (row 31, exo 12)
- **Q**: Lot A :$30\%$ des pièces ($3\%$ défectueuses). Lot B :$70\%$ ($5\%$ défectueuses
- **A**: $0{,}044$
- `WARN_HINT_IS_FORMULA` step 1: _$P(D) = 0{,}3 \times 0{,}03 + 0{,}7 \times 0{,}05$._

### curriculum — 1ERE / Probabilites_Cond (row 31, exo 13)
- **Q**: Urne : 4 boules rouges et 6 boules bleues. On tire 2 boules avec remise. Calcule
- **A**: $\frac{4}{25}$
- `WARN_HINT_IS_FORMULA` step 1: _$P(R_1) = \frac{4}{10} = \frac{2}{5}$._
- `WARN_HINT_IS_FORMULA` step 2: _Avec remise :$P(R_2) = \frac{2}{5}$ aussi._

### curriculum — 1ERE / Probabilites_Cond (row 31, exo 14)
- **Q**: Maladie rare :$P(M) = 0{,}02$. Test :$P(+|M) = 0{,}95$, $P(+|\bar{M}) = 0{,}05$.
- **A**: $0{,}068$
- `WARN_HINT_IS_FORMULA` step 1: _$P(+) = 0{,}02 \times 0{,}95 + 0{,}98 \times 0{,}05$._

### curriculum — 1ERE / Probabilites_Cond (row 31, exo 15)
- **Q**: On tire une carte. $A$ = cœur, $B$ = figure (roi/dame/valet). $P(A) = \frac{1}{4
- **A**: Oui
- `WARN_HINT_IS_FORMULA` step 1: _$A \cap B$ = figure de cœur :$3$ cartes sur $52$, soit $P(A \cap B) = \frac{3}{52}$._
- `WARN_HINT_IS_FORMULA` step 2: _$P(A) \times P(B) = \frac{1}{4} \times \frac{3}{13} = \frac{3}{52}$._
- `WARN_HINT_IS_FORMULA` step 3: _$P(A \cap B) = P(A) \times P(B)$ $\rightarrow$ indépendants._

### curriculum — 1ERE / Probabilites_Cond (row 31, exo 16)
- **Q**: Un sportif s'entraîne le matin avec probabilité $0{,}7$. S'il s'entraîne, $P(\te
- **A**: $0{,}75$
- `WARN_HINT_IS_FORMULA` step 1: _$P(B) = 0{,}7 \times 0{,}9 + 0{,}3 \times 0{,}4$._

### curriculum — 1ERE / Probabilites_Cond (row 31, exo 17)
- **Q**: Urne : 2 rouges, 3 bleues, 5 vertes. Tirage de 2 boules sans remise. $P(\text{un
- **A**: $\frac{6}{45}$
- `WARN_HINT_IS_FORMULA` step 2: _$P(RB) = \frac{2}{10} \times \frac{3}{9} = \frac{6}{90}$, $P(BR) = \frac{3}{10} \times \frac{2}{9} =_
- `WARN_HINT_IS_FORMULA` step 3: _$P(R \cap B) = \frac{6}{90} + \frac{6}{90} = \frac{12}{90} = \frac{2}{15}$._

### curriculum — 1ERE / Probabilites_Cond (row 31, exo 18)
- **Q**: $P(A) = 0{,}3$, $P(B|A) = 0{,}6$, $P(B) = 0{,}3$. Calculer $P(A|B)$.
- **A**: $0{,}6$
- `WARN_HINT_IS_ANSWER` step 1: _$P(A \cap B) = P(A) \times P(B|A) = 0{,}3 \times 0{,}6 = 0{,}18$._
- `WARN_HINT_IS_FORMULA` step 1: _$P(A \cap B) = P(A) \times P(B|A) = 0{,}3 \times 0{,}6 = 0{,}18$._
- `WARN_HINT_IS_FORMULA` step 2: _$P(A|B) = \frac{P(A \cap B)}{P(B)} = \frac{0{,}18}{0{,}3}$._

### curriculum — 1ERE / Probabilites_Cond (row 31, exo 19)
- **Q**: Test de dépistage :$P(M) = 0{,}01$, $P(+|M) = 0{,}9$, $P(+|\bar{M}) = 0{,}05$. C
- **A**: $\approx 0{,}154$
- `WARN_HINT_IS_ANSWER` step 3: _$\approx 0{,}154$._
- `WARN_HINT_IS_FORMULA` step 1: _$P(+) = 0{,}01 \times 0{,}9 + 0{,}99 \times 0{,}05 = 0{,}009 + 0{,}0495 = 0{,}0585$._
- `WARN_HINT_IS_FORMULA` step 2: _$P(M|+) = \frac{0{,}01 \times 0{,}9}{0{,}0585} = \frac{0{,}009}{0{,}0585}$._

### curriculum — 1ERE / Probabilites_Cond (row 31, exo 20)
- **Q**: Vrai ou faux : si $A$ et $B$ sont indépendants, alors $P(A|B) = P(A)$.
- **A**: Vrai
- `WARN_HINT_IS_ANSWER` step 3: _$= P(A)$. Vrai._
- `WARN_HINT_IS_FORMULA` step 1: _Par définition de l'indépendance :$P(A \cap B) = P(A) \times P(B)$._
- `WARN_HINT_IS_FORMULA` step 2: _$P(A|B) = \frac{P(A \cap B)}{P(B)} = \frac{P(A) \times P(B)}{P(B)}$._

### curriculum — 1ERE / Variables_Aleatoires (row 32, exo 1)
- **Q**: $X$ prend les valeurs $0, 1, 2$ avec probabilités $0{,}20, 0{,}50, 0{,}30$. $E(X
- **A**: $1{,}10$
- `WARN_HINT_IS_FORMULA` step 1: _On calcule l'espérance $E(X) = \sum x_i \cdot p_i$. On multiplie chaque valeur de $X$ par sa probabi_

### curriculum — 1ERE / Variables_Aleatoires (row 32, exo 2)
- **Q**: $X$ prend les valeurs $1, 2, 3$ avec probabilités $0{,}20, 0{,}50, 0{,}30$. $E(X
- **A**: $2{,}10$
- `WARN_HINT_IS_FORMULA` step 1: _On calcule l'espérance $E(X) = \sum x_i \cdot p_i$. On multiplie chaque valeur de $X$ par sa probabi_

### curriculum — 1ERE / Variables_Aleatoires (row 32, exo 3)
- **Q**: $X$ prend les valeurs $2, 3, 4$ avec probabilités $0{,}20, 0{,}50, 0{,}30$. $E(X
- **A**: $3{,}10$
- `WARN_HINT_IS_FORMULA` step 1: _On calcule l'espérance $E(X) = \sum x_i \cdot p_i$. On multiplie chaque valeur de $X$ par sa probabi_

### curriculum — 1ERE / Variables_Aleatoires (row 32, exo 4)
- **Q**: $E(X) = 3$. Calculer $E(2X + 1)$.
- **A**: $7$
- `WARN_HINT_IS_FORMULA` step 1: _$E(aX+b) = aE(X) + b$._
- `WARN_HINT_TOO_SHORT` step 3: _Calculer._

### curriculum — 1ERE / Variables_Aleatoires (row 32, exo 5)
- **Q**: $E(X) = 3$. Calculer $E(2X + 1)$.
- **A**: $7$
- `WARN_HINT_IS_FORMULA` step 1: _$E(aX+b) = aE(X) + b$._
- `WARN_HINT_TOO_SHORT` step 3: _Calculer._

### curriculum — 1ERE / Variables_Aleatoires (row 32, exo 6)
- **Q**: La somme des probabilités d'une loi est toujours égale à :
- **A**: $1$
- `WARN_HINT_TOO_SHORT` step 3: _$= ?$._

### curriculum — 1ERE / Variables_Aleatoires (row 32, exo 7)
- **Q**: La somme des probabilités d'une loi est toujours égale à :
- **A**: $1$
- `WARN_HINT_TOO_SHORT` step 3: _$= ?$._

### curriculum — 1ERE / Variables_Aleatoires (row 32, exo 8)
- **Q**: $V(X) = 4$. Calculer $\sigma(X)$.
- **A**: $2$
- `WARN_HINT_IS_FORMULA` step 1: _$\sigma = \sqrt{V(X)}$._
- `WARN_HINT_TOO_SHORT` step 3: _$= ?$._

### curriculum — 1ERE / Variables_Aleatoires (row 32, exo 9)
- **Q**: $V(X) = 4$. Calculer $\sigma(X)$.
- **A**: $2$
- `WARN_HINT_IS_FORMULA` step 1: _$\sigma = \sqrt{V(X)}$._
- `WARN_HINT_TOO_SHORT` step 3: _$= ?$._

### curriculum — 1ERE / Variables_Aleatoires (row 32, exo 10)
- **Q**: $V(X) = 4$. Calculer $\sigma(X)$.
- **A**: $2$
- `WARN_HINT_IS_FORMULA` step 1: _$\sigma = \sqrt{V(X)}$._
- `WARN_HINT_TOO_SHORT` step 3: _$= ?$._

### curriculum — 1ERE / Variables_Aleatoires (row 32, exo 11)
- **Q**: $X \sim B(5; 0{,}3)$. Calculer $P(X = 1)$.
- **A**: $\binom{5}{1} (0{,}3)^1(0{,}7)^{4}$
- `WARN_HINT_IS_FORMULA` step 1: _$\binom{5}{1} = 5$._
- `WARN_HINT_IS_FORMULA` step 2: _$p = 0{,}3$, $1-p = 0{,}7$._
- `WARN_HINT_TOO_SHORT` step 3: _Calculer._

### curriculum — 1ERE / Variables_Aleatoires (row 32, exo 12)
- **Q**: $X \sim B(5; 0{,}3)$. Calculer $P(X = 2)$.
- **A**: $\binom{5}{2} (0{,}3)^2(0{,}7)^{3}$
- `WARN_HINT_IS_FORMULA` step 1: _$\binom{5}{2} = 10$._
- `WARN_HINT_IS_FORMULA` step 2: _$p = 0{,}3$, $1-p = 0{,}7$._
- `WARN_HINT_TOO_SHORT` step 3: _Calculer._

### curriculum — 1ERE / Variables_Aleatoires (row 32, exo 13)
- **Q**: $X \sim B(5; 0{,}3)$. Calculer $P(X = 3)$.
- **A**: $\binom{5}{3} (0{,}3)^3(0{,}7)^{2}$
- `WARN_HINT_IS_FORMULA` step 1: _$\binom{5}{3} = 10$._
- `WARN_HINT_IS_FORMULA` step 2: _$p = 0{,}3$, $1-p = 0{,}7$._
- `WARN_HINT_TOO_SHORT` step 3: _Calculer._

### curriculum — 1ERE / Variables_Aleatoires (row 32, exo 14)
- **Q**: $X \sim B(5; 0{,}3)$. Calculer $P(X = 4)$.
- **A**: $\binom{5}{4} (0{,}3)^4(0{,}7)^{1}$
- `WARN_HINT_IS_FORMULA` step 1: _$\binom{5}{4} = 5$._
- `WARN_HINT_IS_FORMULA` step 2: _$p = 0{,}3$, $1-p = 0{,}7$._
- `WARN_HINT_TOO_SHORT` step 3: _Calculer._

### curriculum — 1ERE / Variables_Aleatoires (row 32, exo 15)
- **Q**: $X$: valeurs $0,1,2,3$ avec probas $0{,}1, 0{,}3, 0{,}4, 0{,}2$. $V(X)$ = ?
- **A**: $0{,}81$
- `WARN_HINT_IS_FORMULA` step 1: _$E(X) = 1{,}7$._
- `WARN_HINT_IS_FORMULA` step 2: _$E(X^2) = 3{,}7$._

### curriculum — 1ERE / Variables_Aleatoires (row 32, exo 16)
- **Q**: $X$: valeurs $0,1,2,3$ avec probas $0{,}1, 0{,}3, 0{,}4, 0{,}2$. $V(X)$ = ?
- **A**: $0{,}81$
- `WARN_HINT_IS_FORMULA` step 1: _$E(X) = 1{,}7$._
- `WARN_HINT_IS_FORMULA` step 2: _$E(X^2) = 3{,}7$._

### curriculum — 1ERE / Variables_Aleatoires (row 32, exo 17)
- **Q**: $X$: valeurs $0,1,2,3$ avec probas $0{,}1, 0{,}3, 0{,}4, 0{,}2$. $V(X)$ = ?
- **A**: $0{,}81$
- `WARN_HINT_IS_FORMULA` step 1: _$E(X) = 1{,}7$._
- `WARN_HINT_IS_FORMULA` step 2: _$E(X^2) = 3{,}7$._

### curriculum — 1ERE / Variables_Aleatoires (row 32, exo 18)
- **Q**: $X \sim B(8; 0{,}3)$. $E(X)$ et $V(X)$?
- **A**: $E = 2{,}4$, $V = 1{,}68$
- `WARN_HINT_IS_FORMULA` step 1: _$n=8$, $p=0{,}3$._
- `WARN_HINT_IS_FORMULA` step 2: _$E = 8 \times 0{,}3 = 2{,}4$._
- `WARN_HINT_IS_FORMULA` step 3: _$V = 2{,}4 \times 0{,}7 = 1{,}68$._

### curriculum — 1ERE / Variables_Aleatoires (row 32, exo 19)
- **Q**: $X \sim B(8; 0{,}3)$. $E(X)$ et $V(X)$?
- **A**: $E = 2{,}4$, $V = 1{,}68$
- `WARN_HINT_IS_FORMULA` step 1: _$n=8$, $p=0{,}3$._
- `WARN_HINT_IS_FORMULA` step 2: _$E = 8 \times 0{,}3 = 2{,}4$._
- `WARN_HINT_IS_FORMULA` step 3: _$V = 2{,}4 \times 0{,}7 = 1{,}68$._

### curriculum — 1ERE / Variables_Aleatoires (row 32, exo 20)
- **Q**: $X \sim B(8; 0{,}3)$. $E(X)$ et $V(X)$?
- **A**: $E = 2{,}4$, $V = 1{,}68$
- `WARN_HINT_IS_FORMULA` step 1: _$n=8$, $p=0{,}3$._
- `WARN_HINT_IS_FORMULA` step 2: _$E = 8 \times 0{,}3 = 2{,}4$._
- `WARN_HINT_IS_FORMULA` step 3: _$V = 2{,}4 \times 0{,}7 = 1{,}68$._

### curriculum — 1ERE / Algorithmique (row 33, exo 1)
- **Q**: Que renvoie ce code ?
```python
x = 3
for i in range(4):
    x = x + 2
print(x)

- **A**: $11$
- `WARN_HINT_IS_FORMULA` step 1: _On exécute le code pas à pas. On initialise $x = 3$, $x = x + 2$. La boucle `for` s'exécute $4$ fois_

### curriculum — 1ERE / Algorithmique (row 33, exo 12)
- **Q**: Que renvoie ce code ?
```python
n = 20
while n > 1:
    if n % 2 == 0:
        n
- **A**: $10$
- `WARN_HINT_IS_FORMULA` step 1: _On exécute le code pas à pas. On initialise $n = 20$, $n = n // 2$. La boucle `while` tourne tant qu_

### curriculum — 1ERE / Algorithmique (row 33, exo 16)
- **Q**: Combien d'itérations fait `while n > 0: n = n // 2` si $n = 4$?
- **A**: $3$
- `WARN_HINT_IS_FORMULA` step 1: _$n = 4, 2, ..., 1, 0$._

### curriculum — 1ERE / Algorithmique (row 33, exo 17)
- **Q**: Combien d'itérations fait `while n > 0: n = n // 2` si $n = 8$?
- **A**: $4$
- `WARN_HINT_IS_FORMULA` step 1: _$n = 8, 4, ..., 1, 0$._

### curriculum — 1ERE / Algorithmique (row 33, exo 18)
- **Q**: Combien d'itérations fait `while n > 0: n = n // 2` si $n = 16$?
- **A**: $5$
- `WARN_HINT_IS_FORMULA` step 1: _$n = 16, 8, ..., 1, 0$._

### curriculum — 1ERE / Algorithmique (row 33, exo 19)
- **Q**: Combien d'itérations fait `while n > 0: n = n // 2` si $n = 32$?
- **A**: $6$
- `WARN_HINT_IS_FORMULA` step 1: _$n = 32, 16, ..., 1, 0$._

### curriculum — 1ERE / Algorithmique (row 33, exo 20)
- **Q**: Combien d'itérations fait `while n > 0: n = n // 2` si $n = 64$?
- **A**: $7$
- `WARN_HINT_IS_FORMULA` step 1: _$n = 64, 32, ..., 1, 0$._

### curriculum — 3EME / Arithmetique_Brevet (row 34, exo 2)
- **Q**: Parmi les tailles de groupes suivantes, laquelle permet une répartition exacte d
- **A**: $7$
- `WARN_HINT_IS_FORMULA` step 1: _Teste chaque valeur : $84 \div 7 = ?$, $84 \div 8 = ?$, $84 \div 5 = ?$_

### curriculum — 3EME / Arithmetique_Brevet (row 34, exo 3)
- **Q**: Combien de diviseurs le nombre $84$ possède-t-il au total ? ___
- **A**: 12
- `WARN_HINT_IS_FORMULA` step 2: _Le nombre de diviseurs est $(2+1) \times (1+1) \times (1+1) = ?$_

### curriculum — 3EME / Arithmetique_Brevet (row 34, exo 5)
- **Q**: Mme Duval veut des groupes de plus de $10$ élèves. Quelle est la seule taille de
- **A**: 12
- `WARN_HINT_IS_ANSWER` step 1: _Les diviseurs de $84$ sont : $1, 2, 3, 4, 6, 7, 12, 14, 21, 28, 42, 84$._
- `WARN_HINT_IS_ANSWER` step 2: _Parmi ceux strictement supérieurs à $10$ et inférieurs à $84$ (taille raisonnable d'un groupe) : $12_

### curriculum — 3EME / Arithmetique_Brevet (row 34, exo 6)
- **Q**: Quelle est la décomposition en facteurs premiers de $126$ ? ___
- **A**: 2 \times 3^2 \times 7
- `WARN_HINT_IS_FORMULA` step 1: _$126 \div 2 = 63$. Puis $63 \div 3 = 21$, $21 \div 3 = 7$, et $7$ est premier._

### curriculum — 3EME / Arithmetique_Brevet (row 34, exo 7)
- **Q**: Quelle est la décomposition en facteurs premiers de $90$ ?
- **A**: $2 \times 3^2 \times 5$
- `WARN_HINT_IS_FORMULA` step 1: _$90 \div 2 = 45$. Puis $45 \div 3 = 15$, $15 \div 3 = 5$, et $5$ est premier._

### curriculum — 3EME / Arithmetique_Brevet (row 34, exo 8)
- **Q**: Le nombre $126$ est-il divisible par $4$ ?
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 2: _Les deux derniers chiffres de $126$ sont $26$. Or $26 \div 4 = 6{,}5$. Est-ce un entier ?_

### curriculum — 3EME / Arithmetique_Brevet (row 34, exo 9)
- **Q**: En utilisant les décompositions, quel est le PGCD de $126$ et $90$ ? ___
- **A**: 18
- `WARN_HINT_IS_FORMULA` step 2: _Le PGCD prend les facteurs communs avec le plus petit exposant : $2^{?} \times 3^{?} = ?$_

### curriculum — 3EME / Arithmetique_Brevet (row 34, exo 10)
- **Q**: Combien de carrés Hugo obtient-il en découpant une tablette avec des carrés de c
- **A**: $35$
- `WARN_HINT_IS_FORMULA` step 1: _Nombre de carrés en largeur : $126 \div 18 = ?$. Nombre de carrés en hauteur : $90 \div 18 = ?$._
- `WARN_HINT_IS_FORMULA` step 2: _Nombre total de carrés $= ? \times ? = ?$_

### curriculum — 3EME / Arithmetique_Brevet (row 34, exo 11)
- **Q**: Jade peut-elle faire exactement $10$ bouquets identiques avec toutes ses fleurs 
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 1: _Si $10$ bouquets : $120 \div 10 = 12$ roses par bouquet. $84 \div 10 = ?$_
- `WARN_HINT_IS_FORMULA` step 2: _$84 \div 10 = 8{,}4$. Ce n'est pas un nombre entier. Que peut-on conclure ?_

### curriculum — 3EME / Arithmetique_Brevet (row 34, exo 12)
- **Q**: Quel est le plus grand nombre de bouquets identiques que Jade peut composer ? __
- **A**: 12
- `WARN_HINT_IS_ANSWER` step 1: _On cherche le PGCD de $120$ et $84$. Décompose : $120 = 2^3 \times 3 \times 5$ et $84 = 2^2 \times 3_
- `WARN_HINT_IS_ANSWER` step 2: _$\text{PGCD}(120 ; 84) = 2^{?} \times 3^{?} = ?$_
- `WARN_HINT_IS_FORMULA` step 2: _$\text{PGCD}(120 ; 84) = 2^{?} \times 3^{?} = ?$_

### curriculum — 3EME / Arithmetique_Brevet (row 34, exo 13)
- **Q**: Avec ce nombre maximal de bouquets, combien y a-t-il de tulipes par bouquet ?
- **A**: $7$
- `WARN_HINT_IS_FORMULA` step 1: _Nombre de bouquets $= 12$. Tulipes par bouquet $= 84 \div 12 = ?$_
- `WARN_HINT_IS_FORMULA` step 2: _Roses par bouquet $= 120 \div 12 = ?$. Vérifie que les deux quotients sont entiers._

### curriculum — 3EME / Arithmetique_Brevet (row 34, exo 14)
- **Q**: La fraction $\frac{84}{120}$ est-elle irréductible ?
- **A**: Faux, on peut simplifier par $12$
- `WARN_HINT_IS_FORMULA` step 2: _$\text{PGCD}(84 ; 120) = 12 \neq 1$. Peut-on simplifier ? Par quel nombre ?_

### curriculum — 3EME / Arithmetique_Brevet (row 34, exo 15)
- **Q**: Quelle est la forme irréductible de $\frac{84}{120}$ ? ___
- **A**: 7/10
- `WARN_HINT_IS_FORMULA` step 1: _On divise numérateur et dénominateur par leur PGCD : $\frac{84 \div 12}{120 \div 12} = \frac{?}{?}$_
- `WARN_HINT_IS_FORMULA` step 2: _Vérifie que $\text{PGCD}(? ; ?) = 1$ pour confirmer que la fraction est bien irréductible._

### curriculum — 3EME / Arithmetique_Brevet (row 34, exo 16)
- **Q**: Quelle est la décomposition en facteurs premiers de $180$ ?
- **A**: $2^2 \times 3^2 \times 5$
- `WARN_HINT_IS_FORMULA` step 1: _$180 \div 2 = 90$, $90 \div 2 = 45$, $45 \div 3 = 15$, $15 \div 3 = 5$, $5$ est premier._

### curriculum — 3EME / Arithmetique_Brevet (row 34, exo 17)
- **Q**: Quel est le PGCD de $180$ et $150$ ? ___
- **A**: 30
- `WARN_HINT_IS_FORMULA` step 2: _$\text{PGCD} = 2^{\min(2;1)} \times 3^{\min(2;1)} \times 5^{\min(1;2)} = 2 \times 3 \times 5 = ?$_

### curriculum — 3EME / Arithmetique_Brevet (row 34, exo 18)
- **Q**: Le côté du plus grand carreau possible est donc de $30$ cm. Combien de carreaux 
- **A**: 6
- `WARN_HINT_IS_FORMULA` step 2: _$180 \div 30 = ?$_

### curriculum — 3EME / Arithmetique_Brevet (row 34, exo 19)
- **Q**: Les nombres $180$ et $150$ sont-ils premiers entre eux ?
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 2: _$\text{PGCD}(180 ; 150) = 30$. Est-ce que $30 = 1$ ?_

### curriculum — 3EME / Arithmetique_Brevet (row 34, exo 20)
- **Q**: Combien de carreaux de $30$ cm de côté Lucas doit-il commander au total ?
- **A**: $30$
- `WARN_HINT_IS_ANSWER` step 1: _En longueur : $180 \div 30 = 6$ carreaux. En largeur : $150 \div 30 = ?$ carreaux._
- `WARN_HINT_IS_FORMULA` step 1: _En longueur : $180 \div 30 = 6$ carreaux. En largeur : $150 \div 30 = ?$ carreaux._
- `WARN_HINT_IS_FORMULA` step 2: _Nombre total $= 6 \times ? = ?$_

### curriculum — 3EME / Auto_Calcul (row 35, exo 1)
- **Q**: Un paquet de céréales coûte $4$ €. Il est à $-50\%$. Quel est le prix réduit ? _
- **A**: 2
- `WARN_HINT_IS_FORMULA` step 1: _$50\%$ de $4$ € $= \frac{4}{2} = $ ?_

### curriculum — 3EME / Auto_Calcul (row 35, exo 2)
- **Q**: Une pizza coûte $12$ €. Tu en manges $\frac{3}{4}$. Combien coûte la part que tu
- **A**: 9
- `WARN_HINT_IS_FORMULA` step 1: _$\frac{3}{4} \times 12 = \frac{3 \times 12}{4} = \frac{36}{4} = $ ?_

### curriculum — 3EME / Auto_Calcul (row 35, exo 3)
- **Q**: Un lot de $6$ yaourts coûte $3$ €. Quel est le prix d'un yaourt ?
- **A**: $0{,}50$ €
- `WARN_HINT_IS_FORMULA` step 1: _$\frac{3}{6} = $ ?_

### curriculum — 3EME / Auto_Calcul (row 35, exo 4)
- **Q**: $\frac{1}{3} + \frac{1}{6}$ de la recette est payé par toi. Cela fait $\frac{1}{
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _Dénominateur commun $6$ : $\frac{2}{6} + \frac{1}{6} = \frac{3}{6} = $ ?_

### curriculum — 3EME / Auto_Calcul (row 35, exo 6)
- **Q**: Calcule : $9^2 = $ ___
- **A**: 81
- `WARN_HINT_IS_FORMULA` step 1: _$9^2 = 9 \times 9 = $ ?_

### curriculum — 3EME / Auto_Calcul (row 35, exo 7)
- **Q**: Calcule : $\sqrt{144} = $ ___
- **A**: 12
- `WARN_HINT_IS_ANSWER` step 1: _Quel nombre au carré donne $144$ ? $12 \times 12 = $ ?_
- `WARN_HINT_IS_FORMULA` step 1: _Quel nombre au carré donne $144$ ? $12 \times 12 = $ ?_

### curriculum — 3EME / Auto_Calcul (row 35, exo 9)
- **Q**: $\sqrt{64} + \sqrt{36} = \sqrt{100}$.
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 1: _$\sqrt{64} = 8$ et $\sqrt{36} = 6$, donc $8 + 6 = 14$._
- `WARN_HINT_IS_FORMULA` step 2: _Or $\sqrt{100} = 10$. Et $14 \neq 10$, donc ?_

### curriculum — 3EME / Auto_Calcul (row 35, exo 11)
- **Q**: Peut-on répartir $36$ invités en groupes de $4$ sans qu'il en reste ?
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _$36 \div 4 = 9$. Le reste est $0$, donc ?_

### curriculum — 3EME / Auto_Calcul (row 35, exo 12)
- **Q**: Parmi ces nombres, lequel est un diviseur de $36$ ?
- **A**: $9$
- `WARN_HINT_IS_FORMULA` step 1: _$36 \div 9 = 4$ (reste $0$), $36 \div 7 = 5$ reste $1$, $36 \div 8 = 4$ reste $4$. Donc ?_

### curriculum — 3EME / Auto_Calcul (row 35, exo 14)
- **Q**: Lequel de ces nombres est premier ?
- **A**: $29$
- `WARN_HINT_IS_ANSWER` step 2: _$29$ : pas divisible par $2, 3, 5$. Et $\sqrt{29} < 6$, donc on teste jusqu'à $5$. Aucun diviseur tr_

### curriculum — 3EME / Auto_Calcul (row 35, exo 15)
- **Q**: Tu veux faire des équipes égales avec $36$ invités ET $24$ lots de tombola (même
- **A**: 12
- `WARN_HINT_IS_ANSWER` step 2: _Diviseurs de $36$ : $1, 2, 3, 4, 6, 9, 12, 18, 36$. Diviseurs de $24$ : $1, 2, 3, 4, 6, 8, 12, 24$._

### curriculum — 3EME / Auto_Calcul (row 35, exo 16)
- **Q**: Calcule : $\frac{3}{4} \times 100 = $ ___
- **A**: 75
- `WARN_HINT_IS_FORMULA` step 1: _$\frac{3 \times 100}{4} = \frac{300}{4} = $ ?_

### curriculum — 3EME / Auto_Calcul (row 35, exo 17)
- **Q**: $0{,}001$ est égal à :
- **A**: $10^{-3}$
- `WARN_HINT_IS_FORMULA` step 1: _$0{,}001 = \frac{1}{1000} = \frac{1}{10^3} = 10^{?}$_

### curriculum — 3EME / Auto_Calcul (row 35, exo 18)
- **Q**: $2{,}5 \times 10^3 = 250$.
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 1: _$2{,}5 \times 10^3 = 2{,}5 \times 1000 = $ ?_

### curriculum — 3EME / Auto_Calcul (row 35, exo 19)
- **Q**: Convertis : $3{,}5$ km $= $ ___ m
- **A**: 3500
- `WARN_HINT_IS_FORMULA` step 1: _$1$ km $= 1000$ m, donc $3{,}5 \times 1000 = $ ?_

### curriculum — 3EME / Auto_Calcul (row 35, exo 20)
- **Q**: Quel nombre est à la fois un carré parfait ET un multiple de $9$ ?
- **A**: $36$
- `WARN_HINT_IS_ANSWER` step 1: _$36 = 6^2$ (carré parfait) et $36 = 9 \times 4$ (multiple de $9$)._
- `WARN_HINT_IS_FORMULA` step 2: _$27 = 9 \times 3$ mais $\sqrt{27}$ n'est pas entier. $49 = 7^2$ mais $49 \div 9 = 5$ reste $4$. Donc_

### curriculum — 3EME / Auto_Geometrie (row 36, exo 3)
- **Q**: Le milieu du segment $[OT]$ a pour coordonnées $(2\,;\,0{,}5)$.
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 1: _Milieu de $[OT]$ : $\left(\frac{0+4}{2}\,;\,\frac{0+(-1)}{2}\right) = (2\,;\,?)$._
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{-1}{2} = -0{,}5$, pas $0{,}5$._

### curriculum — 3EME / Auto_Geometrie (row 36, exo 4)
- **Q**: Quelles sont les coordonnées du milieu $I$ du segment $[MG]$ ?
- **A**: (1;4,5)
- `WARN_HINT_IS_FORMULA` step 1: _$I = \left(\frac{4+(-2)}{2}\,;\,\frac{3+6}{2}\right) = \left(\frac{?}{2}\,;\,\frac{?}{2}\right)$._

### curriculum — 3EME / Auto_Geometrie (row 36, exo 5)
- **Q**: On place un kiosque au point $K$ tel que $I(1\,;\,4{,}5)$ soit le milieu de $[OK
- **A**: 2
- `WARN_HINT_IS_FORMULA` step 1: _Si $I$ est milieu de $[OK]$ : $x_I = \frac{x_O + x_K}{2}$, donc $1 = \frac{0 + x_K}{2}$._
- `WARN_HINT_IS_FORMULA` step 2: _$x_K = 2 \times 1 = \,?$_

### curriculum — 3EME / Auto_Geometrie (row 36, exo 6)
- **Q**: Dans un triangle, la somme des angles vaut ___ degrés.
- **A**: 180
- `WARN_HINT_IS_ANSWER` step 1: _Propriété fondamentale : la somme des angles d'un triangle est toujours $180°$._

### curriculum — 3EME / Auto_Geometrie (row 36, exo 7)
- **Q**: Le triangle $OAB$ est rectangle en $O$ (intersection des diagonales). L'angle $\
- **A**: 40
- `WARN_HINT_IS_FORMULA` step 1: _Triangle rectangle en $O$ : $90° + 50° + \widehat{ABO} = 180°$._
- `WARN_HINT_IS_FORMULA` step 2: _$\widehat{ABO} = 180° - 90° - 50° = \,?$_

### curriculum — 3EME / Auto_Geometrie (row 36, exo 8)
- **Q**: Deux angles sont complémentaires quand leur somme vaut $90°$. Les angles $50°$ e
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _$50° + 40° = 90°$. Complémentaires = somme $90°$. Vérifie si c'est le cas._

### curriculum — 3EME / Auto_Geometrie (row 36, exo 11)
- **Q**: L'échelle mesure $5$ m et le pied est à $3$ m du mur. À quelle hauteur l'échelle
- **A**: 4
- `WARN_HINT_IS_FORMULA` step 1: _Triangle rectangle : $AB^2 + 3^2 = 5^2$, donc $AB^2 = 25 - 9 = ?$._
- `WARN_HINT_IS_FORMULA` step 2: _$AB = \sqrt{?}$_

### curriculum — 3EME / Auto_Geometrie (row 36, exo 13)
- **Q**: Un poteau de $1{,}5$ m projette une ombre de $2$ m. Un arbre voisin projette une
- **A**: 6
- `WARN_HINT_IS_FORMULA` step 1: _Thalès : $\frac{\text{hauteur arbre}}{\text{hauteur poteau}} = \frac{\text{ombre arbre}}{\text{ombre_
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{h}{1{,}5} = \frac{8}{2} = 4$, donc $h = 1{,}5 \times ? = \,?$_

### curriculum — 3EME / Auto_Geometrie (row 36, exo 14)
- **Q**: Hugo déplace l'échelle. Le pied est maintenant à $5$ m du mur et l'échelle touch
- **A**: 13
- `WARN_HINT_IS_FORMULA` step 1: _Triangle rectangle : $c^2 = 5^2 + 12^2 = 25 + 144 = ?$._
- `WARN_HINT_IS_FORMULA` step 2: _$c = \sqrt{?}$_

### curriculum — 3EME / Auto_Geometrie (row 36, exo 15)
- **Q**: Un piquet de $2$ m projette une ombre de $3$ m. À côté, une antenne projette une
- **A**: 8
- `WARN_HINT_IS_FORMULA` step 1: _$\frac{h}{2} = \frac{12}{3} = ?$._
- `WARN_HINT_IS_FORMULA` step 2: _$h = 2 \times ? = \,?$_

### curriculum — 3EME / Auto_Geometrie (row 36, exo 16)
- **Q**: Combien de cm$^3$ y a-t-il dans $1$ L ?
- **A**: 1000
- `WARN_HINT_IS_FORMULA` step 1: _$1$ L $= 1$ dm$^3$. Et $1$ dm$^3 = 10 \times 10 \times 10 = ?$ cm$^3$._

### curriculum — 3EME / Auto_Geometrie (row 36, exo 17)
- **Q**: Une boîte de céréales est un pavé droit de $20$ cm $\times$ $8$ cm $\times$ $30$
- **A**: $4800$ cm$^3$
- `WARN_HINT_IS_FORMULA` step 1: _$V = L \times l \times h = 20 \times 8 \times 30 = ?$_

### curriculum — 3EME / Auto_Geometrie (row 36, exo 18)
- **Q**: Une boîte de conserve est un cylindre de rayon $4$ cm et de hauteur $10$ cm. Son
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _$V = \pi \times r^2 \times h = \pi \times 4^2 \times 10 = \pi \times ?$._

### curriculum — 3EME / Auto_Geometrie (row 36, exo 19)
- **Q**: Un cône de glace a un rayon de $3$ cm et une hauteur de $12$ cm. Quel est son vo
- **A**: $36\pi$
- `WARN_HINT_IS_FORMULA` step 1: _$V = \frac{1}{3} \times \pi \times r^2 \times h = \frac{1}{3} \times \pi \times 9 \times 12$._
- `WARN_HINT_IS_FORMULA` step 2: _$= \frac{1}{3} \times \pi \times ? = ?\pi$_

### curriculum — 3EME / Auto_Geometrie (row 36, exo 20)
- **Q**: Un ballon (sphère) a un rayon de $3$ cm. Quel est son volume ?
- **A**: $36\pi$ cm$^3$
- `WARN_HINT_IS_FORMULA` step 1: _$V = \frac{4}{3} \times \pi \times r^3 = \frac{4}{3} \times \pi \times 27$._
- `WARN_HINT_IS_FORMULA` step 2: _$= \frac{?}{3} \pi = ?\pi$_

### curriculum — 3EME / Auto_Litteral (row 37, exo 1)
- **Q**: La distance est donnée par $d = v \times t$. Si $v = 4$ km/h et $t = 3$ h, que v
- **A**: 12
- `WARN_HINT_IS_FORMULA` step 1: _$d = 4 \times 3 = $ ?_

### curriculum — 3EME / Auto_Litteral (row 37, exo 2)
- **Q**: L'aire d'un rectangle est $A = L \times l$. Si $L = 7$ et $l = 6$, que vaut $A$ 
- **A**: 42
- `WARN_HINT_IS_FORMULA` step 1: _$A = 7 \times 6 = $ ?_

### curriculum — 3EME / Auto_Litteral (row 37, exo 3)
- **Q**: Le périmètre d'un carré est $P = 4c$. Si $c = 8$ cm, combien vaut $P$ ?
- **A**: $32$ cm
- `WARN_HINT_IS_FORMULA` step 1: _$P = 4 \times 8 = $ ?_

### curriculum — 3EME / Auto_Litteral (row 37, exo 4)
- **Q**: On calcule l'énergie avec $E = m \times v^2$. Si $m = 3$ et $v = 5$, combien vau
- **A**: $75$
- `WARN_HINT_IS_FORMULA` step 1: _$E = 3 \times 5^2 = 3 \times 25 = $ ?_

### curriculum — 3EME / Auto_Litteral (row 37, exo 5)
- **Q**: La formule $C = 2x + 5$ donne le coût d'un trajet de $x$ km. Pour $x = 10$, on o
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 1: _$C = 2 \times 10 + 5 = 20 + 5 = $ ? Est-ce bien $20$ ?_

### curriculum — 3EME / Auto_Litteral (row 37, exo 6)
- **Q**: Développe : $5(x + 3) = $ ___
- **A**: $5x + 15$
- `WARN_HINT_IS_FORMULA` step 1: _$5 \times x + 5 \times 3 = $ ?_

### curriculum — 3EME / Auto_Litteral (row 37, exo 7)
- **Q**: Développe : $-2(3x - 4) = $ ___
- **A**: $-6x + 8$
- `WARN_HINT_IS_FORMULA` step 1: _$-2 \times 3x + (-2) \times (-4) = $ ? Attention au signe !_

### curriculum — 3EME / Auto_Litteral (row 37, exo 8)
- **Q**: Quel est le développement de $4(2x - 1)$ ?
- **A**: $8x - 4$
- `WARN_HINT_IS_FORMULA` step 1: _$4 \times 2x - 4 \times 1 = $ ? On distribue le $4$ sur chaque terme._

### curriculum — 3EME / Auto_Litteral (row 37, exo 9)
- **Q**: Factorise : $6x + 18 = $ ?
- **A**: $6(x + 3)$
- `WARN_HINT_IS_FORMULA` step 1: _Le facteur commun de $6x$ et $18$ est $6$. Donc $6x + 18 = 6(\ldots + \ldots)$ ?_

### curriculum — 3EME / Auto_Litteral (row 37, exo 10)
- **Q**: $-3(x - 5) = -3x - 15$
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 1: _$-3 \times x = -3x$ ✓. Mais $-3 \times (-5) = +15$, pas $-15$. Résultat : $-3x + 15$._

### curriculum — 3EME / Auto_Litteral (row 37, exo 11)
- **Q**: Développe : $(x + 4)^2 = $ ___
- **A**: $x^2 + 8x + 16$
- `WARN_HINT_IS_FORMULA` step 1: _$(a + b)^2 = a^2 + 2ab + b^2$. Ici $a = x$, $b = 4$. Donc $x^2 + 2 \times x \times 4 + 4^2 = $ ?_

### curriculum — 3EME / Auto_Litteral (row 37, exo 12)
- **Q**: $(x - 3)^2 = x^2 - 9$
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 1: _$(x - 3)^2 = x^2 - 2 \times x \times 3 + 9 = x^2 - 6x + 9$. Il manque le terme $-6x$ !_

### curriculum — 3EME / Auto_Litteral (row 37, exo 13)
- **Q**: Quel est le développement de $(x + 5)(x - 5)$ ?
- **A**: $x^2 - 25$
- `WARN_HINT_IS_FORMULA` step 1: _$(a + b)(a - b) = a^2 - b^2$. Ici $a = x$ et $b = 5$, donc $x^2 - 5^2 = $ ?_

### curriculum — 3EME / Auto_Litteral (row 37, exo 14)
- **Q**: Factorise $x^2 - 16$ en utilisant une identité remarquable : ___
- **A**: $(x - 4)(x + 4)$
- `WARN_HINT_IS_FORMULA` step 1: _$x^2 - 16 = x^2 - 4^2$. C'est la forme $a^2 - b^2 = (a - b)(a + b)$. Donc ?_

### curriculum — 3EME / Auto_Litteral (row 37, exo 15)
- **Q**: Quel est le développement de $(2x - 3)^2$ ?
- **A**: $4x^2 - 12x + 9$
- `WARN_HINT_IS_FORMULA` step 1: _$(a - b)^2 = a^2 - 2ab + b^2$ avec $a = 2x$ et $b = 3$. Donc $(2x)^2 - 2 \times 2x \times 3 + 3^2 = _

### curriculum — 3EME / Auto_Litteral (row 37, exo 16)
- **Q**: Résous mentalement : $3x = 21$. Que vaut $x$ ? ___
- **A**: 7
- `WARN_HINT_IS_FORMULA` step 1: _$x = \frac{21}{3} = $ ?_

### curriculum — 3EME / Auto_Litteral (row 37, exo 17)
- **Q**: Quelle est la solution de $2x + 1 = 9$ ?
- **A**: $x = 4$
- `WARN_HINT_IS_FORMULA` step 1: _$2x = 9 - 1 = 8$, donc $x = \frac{8}{2} = $ ?_

### curriculum — 3EME / Auto_Litteral (row 37, exo 18)
- **Q**: Si $x = -2$, l'expression $x^2 - 3x + 1$ vaut $11$.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _$(-2)^2 - 3 \times (-2) + 1 = 4 + 6 + 1 = $ ? Compare avec $11$._

### curriculum — 3EME / Auto_Litteral (row 37, exo 19)
- **Q**: Développe et réduis : $(x + 2)(x - 3) = $ ___
- **A**: $x^2 - x - 6$
- `WARN_HINT_IS_FORMULA` step 1: _$x \times x + x \times (-3) + 2 \times x + 2 \times (-3) = x^2 - 3x + 2x - 6 = $ ?_

### curriculum — 3EME / Auto_Litteral (row 37, exo 20)
- **Q**: Quelle est la solution de $5x - 3 = 2x + 9$ ?
- **A**: $x = 4$
- `WARN_HINT_IS_FORMULA` step 1: _$5x - 2x = 9 + 3$, donc $3x = 12$, donc $x = $ ?_

### curriculum — 3EME / Auto_Stats_Probas (row 38, exo 4)
- **Q**: La probabilité de tirer un jeton rouge est $\frac{1}{5}$.
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 1: _$P(\text{rouge}) = \frac{5}{20} = \frac{1}{4}$, pas $\frac{1}{5}$_

### curriculum — 3EME / Auto_Stats_Probas (row 38, exo 5)
- **Q**: Quelle est la probabilité de NE PAS tirer un jeton vert ?
- **A**: $\frac{17}{20}$
- `WARN_HINT_IS_FORMULA` step 1: _$P(\text{pas vert}) = 1 - P(\text{vert}) = 1 - \frac{3}{20} = $ ?_

### curriculum — 3EME / Auto_Stats_Probas (row 38, exo 8)
- **Q**: Quel pourcentage des élèves préfèrent le Foot ?
- **A**: 40 %
- `WARN_HINT_IS_FORMULA` step 1: _$\frac{20}{50} = \frac{40}{100}$. Donc ?_

### curriculum — 3EME / Auto_Stats_Probas (row 38, exo 9)
- **Q**: La Natation représente $25\%$ des réponses.
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 1: _$\frac{10}{50} = \frac{20}{100} = 20\%$, pas $25\%$_

### curriculum — 3EME / Auto_Stats_Probas (row 38, exo 10)
- **Q**: Si on interroge un élève au hasard, quelle est la probabilité qu'il préfère le T
- **A**: $\frac{1}{10}$
- `WARN_HINT_IS_FORMULA` step 1: _$P(\text{Tennis}) = \frac{5}{50} = $ ? Simplifie par $5$._

### curriculum — 3EME / Auto_Stats_Probas (row 38, exo 13)
- **Q**: Quelle est la moyenne de Jade ?
- **A**: 12
- `WARN_HINT_IS_ANSWER` step 1: _$\frac{12 + 8 + 14 + 16 + 10}{5} = \frac{60}{5} = $ ?_
- `WARN_HINT_IS_FORMULA` step 1: _$\frac{12 + 8 + 14 + 16 + 10}{5} = \frac{60}{5} = $ ?_

### curriculum — 3EME / Auto_Stats_Probas (row 38, exo 15)
- **Q**: Si Jade obtient $18$ au DS6, quelle sera sa nouvelle moyenne ?
- **A**: 13
- `WARN_HINT_IS_FORMULA` step 1: _$\frac{60 + 18}{6} = \frac{78}{6} = $ ?_

### curriculum — 3EME / Auto_Stats_Probas (row 38, exo 17)
- **Q**: Quelle est la moyenne de victoires par joueur ?
- **A**: 6,5
- `WARN_HINT_IS_FORMULA` step 1: _$\frac{7 + 5 + 8 + 6}{4} = \frac{26}{4} = $ ?_

### curriculum — 3EME / Auto_Stats_Probas (row 38, exo 19)
- **Q**: Quel pourcentage de ses matchs Inès a-t-elle gagnés ?
- **A**: 50 %
- `WARN_HINT_IS_FORMULA` step 1: _$\frac{5}{10} = \frac{50}{100} = $ ?_

### curriculum — 3EME / Calcul_Litteral_Brevet (row 39, exo 1)
- **Q**: Rachid veut poser une clôture sur l'un des grands côtés du terrain. Il dispose d
- **A**: $4x + 12$
- `WARN_HINT_IS_FORMULA` step 2: _$4 \times x = 4x$ et $4 \times 3 = ?$. Le résultat est $4x + ?$._

### curriculum — 3EME / Calcul_Litteral_Brevet (row 39, exo 2)
- **Q**: Rachid agrandit son terrain de $2$ m en longueur. La nouvelle aire est $(x + 2)(
- **A**: $x^2 + 5x + 6$
- `WARN_HINT_IS_FORMULA` step 2: _$x \times x = x^2$, $x \times 3 = 3x$, $2 \times x = 2x$, $2 \times 3 = 6$. On regroupe les termes e_

### curriculum — 3EME / Calcul_Litteral_Brevet (row 39, exo 3)
- **Q**: Rachid affirme : « $4(x + 3) = 4x + 3$ ». A-t-il raison ?
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 2: _$4 \times x = 4x$ et $4 \times 3 = 12$. Le résultat correct est-il $4x + 3$ ou $4x + 12$ ?_

### curriculum — 3EME / Calcul_Litteral_Brevet (row 39, exo 4)
- **Q**: Le périmètre du terrain initial est $2(x + 3) + 2x$. Développe et réduis cette e
- **A**: $4x + 6$
- `WARN_HINT_IS_FORMULA` step 1: _On développe d'abord $2(x + 3) = 2x + 6$._
- `WARN_HINT_IS_FORMULA` step 2: _Le périmètre vaut donc $2x + 6 + 2x$. On regroupe les termes en $x$ : $2x + 2x = ?$._

### curriculum — 3EME / Calcul_Litteral_Brevet (row 39, exo 5)
- **Q**: L'aire du terrain agrandi est $(x + 2)(x + 3)$. L'aire de l'ancien terrain est $
- **A**: $2x + 6$
- `WARN_HINT_IS_FORMULA` step 2: _On développe chacune : $x^2 + 5x + 6$ et $x^2 + 3x$. La différence donne $5x + 6 - 3x = ?$._

### curriculum — 3EME / Calcul_Litteral_Brevet (row 39, exo 6)
- **Q**: Le coût de production de $x$ panneaux est $6x + 18$ euros. Inès factorise cette 
- **A**: $6(x + 3)$
- `WARN_HINT_IS_FORMULA` step 2: _On met $6$ en facteur : $6x = 6 \times x$ et $18 = 6 \times ?$. Donc $6x + 18 = 6(x + ?)$._

### curriculum — 3EME / Calcul_Litteral_Brevet (row 39, exo 7)
- **Q**: Les frais de livraison sont modélisés par $3x^2 - 12x$. Quelle est la forme fact
- **A**: $3x(x - 4)$
- `WARN_HINT_IS_FORMULA` step 1: _On identifie le facteur commun : $3x^2 = 3x \times x$ et $12x = 3x \times 4$._
- `WARN_HINT_IS_FORMULA` step 2: _Le facteur commun est $3x$. On factorise : $3x^2 - 12x = 3x(x - ?)$._

### curriculum — 3EME / Calcul_Litteral_Brevet (row 39, exo 8)
- **Q**: Inès affirme que $x^2 - 16$ peut s'écrire $(x - 4)(x + 4)$. A-t-elle raison ?
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _On reconnaît la forme $a^2 - b^2$ avec $a = x$ et $b = 4$, car $16 = 4^2$._
- `WARN_HINT_IS_FORMULA` step 2: _L'identité $a^2 - b^2 = (a - b)(a + b)$ donne $(x - 4)(x + 4)$. Le résultat d'Inès est-il correct ?_

### curriculum — 3EME / Calcul_Litteral_Brevet (row 39, exo 9)
- **Q**: Le bénéfice annuel est modélisé par $4x^2 + 20x + 25$. Factorise cette expressio
- **A**: $(2x + 5)^2$
- `WARN_HINT_IS_FORMULA` step 1: _On remarque que $4x^2 = (2x)^2$ et $25 = 5^2$. On vérifie le double produit : $2 \times 2x \times 5 _
- `WARN_HINT_IS_FORMULA` step 2: _Le double produit vaut $20x$, c'est bien le terme du milieu. L'identité $(a + b)^2 = a^2 + 2ab + b^2_

### curriculum — 3EME / Calcul_Litteral_Brevet (row 39, exo 10)
- **Q**: Inès doit aussi factoriser $x^2 - 6x + 9$. Quelle est la forme factorisée ?
- **A**: $(x - 3)^2$
- `WARN_HINT_IS_FORMULA` step 1: _On identifie $x^2 = x^2$, $9 = 3^2$. Le double produit : $2 \times x \times 3 = 6x$. Le signe du mil_
- `WARN_HINT_IS_FORMULA` step 2: _L'identité $(a - b)^2 = a^2 - 2ab + b^2$ s'applique. Avec le signe $-$, la forme factorisée est $(x _

### curriculum — 3EME / Calcul_Litteral_Brevet (row 39, exo 11)
- **Q**: Développe $(x + 4)^2$.
- **A**: $x^2 + 8x + 16$
- `WARN_HINT_IS_FORMULA` step 1: _On applique l'identité $(a + b)^2 = a^2 + 2ab + b^2$ avec $a = x$ et $b = 4$._
- `WARN_HINT_IS_FORMULA` step 2: _$x^2 + 2 \times x \times 4 + 4^2 = x^2 + 8x + ?$._

### curriculum — 3EME / Calcul_Litteral_Brevet (row 39, exo 12)
- **Q**: Développe $(x - 3)^2$.
- **A**: $x^2 - 6x + 9$
- `WARN_HINT_IS_FORMULA` step 1: _On applique $(a - b)^2 = a^2 - 2ab + b^2$ avec $a = x$ et $b = 3$._
- `WARN_HINT_IS_FORMULA` step 2: _$x^2 - 2 \times x \times 3 + 3^2 = x^2 - 6x + ?$. Attention : $x^2 - 9$ est la forme $a^2 - b^2$, pa_

### curriculum — 3EME / Calcul_Litteral_Brevet (row 39, exo 14)
- **Q**: Développe $(3x - 2)^2$.
- **A**: $9x^2 - 12x + 4$
- `WARN_HINT_IS_FORMULA` step 1: _On applique $(a - b)^2$ avec $a = 3x$ et $b = 2$ : $(3x)^2 - 2 \times 3x \times 2 + 2^2$._

### curriculum — 3EME / Calcul_Litteral_Brevet (row 39, exo 15)
- **Q**: Jade revient au programme de calcul. Le résultat final est $(x + 4)^2 - (x - 3)^
- **A**: $7(2x + 1)$
- `WARN_HINT_IS_FORMULA` step 1: _On pose $a = (x + 4)$ et $b = (x - 3)$. L'identité $a^2 - b^2 = (a - b)(a + b)$ donne $((x+4)-(x-3))_
- `WARN_HINT_IS_FORMULA` step 2: _$a - b = x + 4 - x + 3 = 7$ et $a + b = x + 4 + x - 3 = 2x + 1$. Le résultat factorisé est $? \times_

### curriculum — 3EME / Calcul_Litteral_Brevet (row 39, exo 16)
- **Q**: Développe et réduis l'expression de l'aire de la cour : $(x + 3)(x + 1)$.
- **A**: $x^2 + 4x + 3$
- `WARN_HINT_IS_FORMULA` step 2: _$x^2 + x + 3x + 3$. On regroupe les termes en $x$ : $x + 3x = ?$._

### curriculum — 3EME / Calcul_Litteral_Brevet (row 39, exo 17)
- **Q**: Emma veut retrouver les dimensions à partir de l'aire. Factorise $x^2 + 4x + 3$.
- **A**: $(x + 1)(x + 3)$
- `WARN_HINT_IS_FORMULA` step 2: _Les nombres $1$ et $3$ vérifient : $1 \times 3 = 3$ et $1 + 3 = ?$. Donc $x^2 + 4x + 3 = (x + ?)(x +_

### curriculum — 3EME / Calcul_Litteral_Brevet (row 39, exo 19)
- **Q**: Le client veut une cour de $35$ m² exactement. On résout $(x + 3)(x + 1) = 35$, 
- **A**: 4
- `WARN_HINT_IS_FORMULA` step 1: _$(x + 8)(x - 4) = 0$ donne deux solutions : $x = -8$ ou $x = 4$._

### curriculum — 3EME / Equations_Brevet (row 40, exo 1)
- **Q**: Quelle équation traduit la situation ? ___
- **A**: x+2x+x+5=45
- `WARN_HINT_IS_FORMULA` step 2: _L'équation est $x + 2x + (x + 5) = ?$_

### curriculum — 3EME / Equations_Brevet (row 40, exo 2)
- **Q**: En simplifiant le membre de gauche, on obtient $4x + 5 = 45$. Quelle est la vale
- **A**: $10$
- `WARN_HINT_IS_FORMULA` step 1: _On isole $4x$ : $4x = 45 - 5 = ?$_
- `WARN_HINT_IS_FORMULA` step 2: _Puis $x = \frac{?}{4}$_

### curriculum — 3EME / Equations_Brevet (row 40, exo 3)
- **Q**: Noé a donc donné $20$ €.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _Noé donne $2x$. On a trouvé $x = 10$._
- `WARN_HINT_IS_FORMULA` step 2: _Donc Noé donne $2 \times 10 = ?$. Compare avec $20$ €._

### curriculum — 3EME / Equations_Brevet (row 40, exo 4)
- **Q**: Combien Jade a-t-elle donné ? ___
- **A**: 15
- `WARN_HINT_IS_FORMULA` step 2: _Avec $x = 10$, on calcule $10 + 5 = ?$_

### curriculum — 3EME / Equations_Brevet (row 40, exo 5)
- **Q**: Si le cadeau coûte $50$ € au lieu de $45$ €, et que chacun garde la même règle d
- **A**: $11{,}25$ €
- `WARN_HINT_IS_FORMULA` step 1: _L'équation devient $4x + 5 = 50$, donc $4x = ?$_
- `WARN_HINT_IS_FORMULA` step 2: _$x = \frac{?}{4}$. Calcule le résultat._

### curriculum — 3EME / Equations_Brevet (row 40, exo 6)
- **Q**: Hugo achète un t-shirt $x$ euros et le revend avec une marge de $\frac{1}{3}$ du
- **A**: x+x/3=24
- `WARN_HINT_IS_FORMULA` step 2: _Mets au même dénominateur : $\frac{3x}{3} + \frac{x}{3} = \frac{?}{3} = 24$_

### curriculum — 3EME / Equations_Brevet (row 40, exo 7)
- **Q**: Résous l'équation $\frac{4x}{3} = 24$. Quel est le prix d'achat du t-shirt ?
- **A**: $18$ €
- `WARN_HINT_IS_FORMULA` step 1: _On multiplie les deux membres par $3$ : $4x = ?$_
- `WARN_HINT_IS_FORMULA` step 2: _Puis $x = \frac{?}{4}$_

### curriculum — 3EME / Equations_Brevet (row 40, exo 8)
- **Q**: Pour un jean, Hugo fixe le prix de vente à $2(x - 5) + 15 = 55$ où $x$ est le pr
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 1: _Développe $2(x - 5) + 15$ : $2x - 10 + 15 = ?$_

### curriculum — 3EME / Equations_Brevet (row 40, exo 9)
- **Q**: Résous l'équation correcte $2x + 5 = 55$. Quel est le prix d'achat du jean ? ___
- **A**: 25
- `WARN_HINT_IS_FORMULA` step 1: _On isole $2x$ : $2x = 55 - 5 = ?$_
- `WARN_HINT_IS_FORMULA` step 2: _Puis $x = \frac{?}{2}$_

### curriculum — 3EME / Equations_Brevet (row 40, exo 10)
- **Q**: Pour une veste, Hugo écrit $\frac{3(x + 10)}{2} = 75$. Quel est le prix d'achat 
- **A**: $40$ €
- `WARN_HINT_IS_FORMULA` step 1: _Multiplie les deux membres par $2$ : $3(x + 10) = ?$_
- `WARN_HINT_IS_FORMULA` step 2: _Divise par $3$ : $x + 10 = ?$. Puis $x = ?$_

### curriculum — 3EME / Equations_Brevet (row 40, exo 12)
- **Q**: On cherche les valeurs de $x$ telles que $x^2 - 9 = 0$. Quelle est la forme fact
- **A**: $(x - 3)(x + 3)$
- `WARN_HINT_IS_FORMULA` step 1: _On reconnaît une différence de deux carrés : $x^2 - 9 = x^2 - 3^2$._
- `WARN_HINT_IS_FORMULA` step 2: _On applique $a^2 - b^2 = (a - b)(a + b)$ avec $a = x$ et $b = ?$_

### curriculum — 3EME / Equations_Brevet (row 40, exo 13)
- **Q**: L'équation $(x - 3)(x + 3) = 0$ admet exactement deux solutions.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 2: _Soit $x - 3 = 0$ (donc $x = ?$), soit $x + 3 = 0$ (donc $x = ?$). Combien de solutions ?_

### curriculum — 3EME / Equations_Brevet (row 40, exo 14)
- **Q**: Quelles sont les solutions de $x^2 - 9 = 0$ ? ___
- **A**: 3 et -3
- `WARN_HINT_IS_FORMULA` step 1: _D'après la factorisation : $(x - 3)(x + 3) = 0$._
- `WARN_HINT_IS_FORMULA` step 2: _$x - 3 = 0 \Rightarrow x = ?$ et $x + 3 = 0 \Rightarrow x = ?$_

### curriculum — 3EME / Equations_Brevet (row 40, exo 15)
- **Q**: Lucas modifie le programme : « Choisis $x$. Calcule $(2x - 1)(x + 4)$. » Pour qu
- **A**: $-4$
- `WARN_HINT_IS_FORMULA` step 1: _$(2x - 1)(x + 4) = 0$ donne $2x - 1 = 0$ ou $x + 4 = 0$._
- `WARN_HINT_IS_FORMULA` step 2: _$2x - 1 = 0 \Rightarrow x = ?$ (est-ce un entier ?) et $x + 4 = 0 \Rightarrow x = ?$ (est-ce un enti_

### curriculum — 3EME / Equations_Brevet (row 40, exo 17)
- **Q**: Le périmètre d'un rectangle est $2(L + l)$. Quelle équation obtient-on ?
- **A**: $2(x + x + 8) = 52$
- `WARN_HINT_IS_FORMULA` step 1: _Le périmètre = $2 \times (\text{largeur} + \text{longueur}) = 2(x + (x + 8))$._

### curriculum — 3EME / Equations_Brevet (row 40, exo 18)
- **Q**: En développant et simplifiant, on obtient $4x + 16 = 52$. La largeur du terrain 
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _$2(2x + 8) = 52 \Rightarrow 4x + 16 = 52 \Rightarrow 4x = ?$_
- `WARN_HINT_IS_FORMULA` step 2: _$x = \frac{?}{4}$. Compare avec $9$._

### curriculum — 3EME / Equations_Brevet (row 40, exo 19)
- **Q**: Quelle est l'aire du terrain en $\text{m}^2$ ? ___
- **A**: 153
- `WARN_HINT_IS_FORMULA` step 2: _L'aire = largeur $\times$ longueur = $9 \times ? = ?$ $\text{m}^2$_

### curriculum — 3EME / Equations_Brevet (row 40, exo 20)
- **Q**: Adam veut installer un filet qui partage le terrain en deux rectangles égaux dan
- **A**: $61$ m
- `WARN_HINT_IS_FORMULA` step 1: _Le périmètre total est $52$ m. Le filet traverse le terrain dans le sens de la largeur, donc il mesu_

### curriculum — 3EME / Fonctions_Affines_Brevet (row 41, exo 1)
- **Q**: Dans l'expression $f(x) = 0{,}15x + 12$, que représente le nombre $0{,}15$ ?
- **A**: Le prix par minute d'appel
- `WARN_HINT_IS_FORMULA` step 1: _Dans $f(x) = ax + b$, le coefficient $a$ est le nombre qui multiplie $x$._

### curriculum — 3EME / Fonctions_Affines_Brevet (row 41, exo 2)
- **Q**: Calcule le coût mensuel de Noé s'il appelle $40$ minutes. $f(40) = $ ___
- **A**: 18
- `WARN_HINT_IS_FORMULA` step 1: _On remplace $x$ par $40$ dans $f(x) = 0{,}15x + 12$._
- `WARN_HINT_IS_FORMULA` step 2: _$f(40) = 0{,}15 \times 40 + 12 = 6 + 12 = $ ?_

### curriculum — 3EME / Fonctions_Affines_Brevet (row 41, exo 3)
- **Q**: Même sans passer le moindre appel, Noé paie $12~€$ avec ce forfait.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _Si Noé ne téléphone pas, $x = 0$. On calcule $f(0) = 0{,}15 \times 0 + 12$._
- `WARN_HINT_IS_FORMULA` step 2: _$f(0) = 12$. Ce montant correspond à l'abonnement fixe. Que peut-on en conclure ?_

### curriculum — 3EME / Fonctions_Affines_Brevet (row 41, exo 4)
- **Q**: Noé a reçu une facture de $27~€$. Combien de minutes a-t-il appelé ? ___ minutes
- **A**: 100
- `WARN_HINT_IS_FORMULA` step 1: _On résout $f(x) = 27$, soit $0{,}15x + 12 = 27$._
- `WARN_HINT_IS_FORMULA` step 2: _$0{,}15x = 27 - 12 = 15$, donc $x = \frac{15}{0{,}15} = $ ?_

### curriculum — 3EME / Fonctions_Affines_Brevet (row 41, exo 5)
- **Q**: Le forfait "Premium" coûte $25~€$ par mois, appels illimités. À partir de combie
- **A**: À partir de $87$ minutes
- `WARN_HINT_IS_FORMULA` step 2: _$0{,}15x > 13$, donc $x > \frac{13}{0{,}15} = 86{,}\overline{6}$._

### curriculum — 3EME / Fonctions_Affines_Brevet (row 41, exo 6)
- **Q**: En lisant le graphique, combien de litres la piscine contient-elle à $t = 0$ ? _
- **A**: 400
- `WARN_HINT_IS_FORMULA` step 1: _À $t = 0$, on lit l'ordonnée du point de départ de la droite sur l'axe vertical._

### curriculum — 3EME / Fonctions_Affines_Brevet (row 41, exo 7)
- **Q**: Quel est le coefficient directeur de la droite $V(t)$ ? Que représente-t-il ?
- **A**: $250$ L/h — c'est le débit du tuyau
- `WARN_HINT_IS_FORMULA` step 2: _On peut lire sur le graphique : entre $t = 0$ et $t = 2$, le volume passe de $400$ à $900$. Donc $a _

### curriculum — 3EME / Fonctions_Affines_Brevet (row 41, exo 8)
- **Q**: Au bout de $8$ heures de remplissage, la piscine est pleine.
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 1: _On calcule $V(8) = 250 \times 8 + 400 = 2\,000 + 400 = 2\,400$ L._

### curriculum — 3EME / Fonctions_Affines_Brevet (row 41, exo 9)
- **Q**: Au bout de combien d'heures la piscine sera-t-elle pleine ? $t = $ ___ h
- **A**: 8,4
- `WARN_HINT_IS_FORMULA` step 1: _La piscine est pleine quand $V(t) = 2\,500$. On résout $250t + 400 = 2\,500$._
- `WARN_HINT_IS_FORMULA` step 2: _$250t = 2\,100$, donc $t = \frac{2\,100}{250} = $ ?_

### curriculum — 3EME / Fonctions_Affines_Brevet (row 41, exo 10)
- **Q**: Après $3$ heures de remplissage, quel pourcentage de la capacité totale a été at
- **A**: $46~\%$
- `WARN_HINT_IS_FORMULA` step 1: _On calcule $V(3) = 250 \times 3 + 400 = 750 + 400 = 1\,150$ L._
- `WARN_HINT_IS_FORMULA` step 2: _Le pourcentage est $\frac{V(3)}{2\,500} \times 100 = \frac{1\,150}{2\,500} \times 100 = $ ?_

### curriculum — 3EME / Fonctions_Affines_Brevet (row 41, exo 11)
- **Q**: En utilisant le tableau, combien de livres Jade reçoit-elle si elle change $100~
- **A**: 78
- `WARN_HINT_IS_FORMULA` step 2: _Le taux est $\frac{16}{20} = 0{,}8$. Pour $100~€$ : $f(100) = 0{,}8 \times 100 - 2 = $ ?_

### curriculum — 3EME / Fonctions_Affines_Brevet (row 41, exo 12)
- **Q**: Quel est le coefficient directeur $a$ de la fonction $f$ ? Que représente-t-il ?
- **A**: $0{,}8$ — c'est le taux de change
- `WARN_HINT_IS_FORMULA` step 2: _$a = \frac{22 - 6}{30 - 10} = \frac{16}{20} = $ ?_

### curriculum — 3EME / Fonctions_Affines_Brevet (row 41, exo 13)
- **Q**: Pour obtenir $46~£$, Jade doit changer $60~€$.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _On calcule $f(60) = 0{,}8 \times 60 - 2 = 48 - 2 = 46$._

### curriculum — 3EME / Fonctions_Affines_Brevet (row 41, exo 14)
- **Q**: Détermine l'expression complète de $f(x)$. $f(x) = $ ___
- **A**: 0,8x - 2
- `WARN_HINT_IS_FORMULA` step 1: _On sait que $a = 0{,}8$. On utilise le point $(10 ; 6)$ : $6 = 0{,}8 \times 10 + b$._
- `WARN_HINT_IS_FORMULA` step 2: _$6 = 8 + b$, donc $b = 6 - 8 = -2$. L'expression est $f(x) = $ ?_

### curriculum — 3EME / Fonctions_Affines_Brevet (row 41, exo 15)
- **Q**: Jade veut recevoir au moins $100~£$. Combien d'euros minimum doit-elle changer ?
- **A**: $128~€$
- `WARN_HINT_IS_FORMULA` step 2: _$0{,}8x \geq 102$, donc $x \geq \frac{102}{0{,}8} = 127{,}5$._

### curriculum — 3EME / Fonctions_Affines_Brevet (row 41, exo 16)
- **Q**: Calcule le coût mensuel chez l'opérateur A pour $60$ minutes hors forfait. $f(60
- **A**: 21
- `WARN_HINT_IS_FORMULA` step 1: _On remplace $x$ par $60$ dans $f(x) = 0{,}10x + 15$._
- `WARN_HINT_IS_FORMULA` step 2: _$f(60) = 0{,}10 \times 60 + 15 = 6 + 15 = $ ?_

### curriculum — 3EME / Fonctions_Affines_Brevet (row 41, exo 17)
- **Q**: Pour $60$ minutes hors forfait, quel opérateur est le moins cher ?
- **A**: Opérateur A ($21~€$ contre $23~€$)
- `WARN_HINT_IS_FORMULA` step 1: _On a $f(60) = 21~€$. On calcule $g(60) = 0{,}05 \times 60 + 20 = 3 + 20 = 23~€$._

### curriculum — 3EME / Fonctions_Affines_Brevet (row 41, exo 18)
- **Q**: L'opérateur B est toujours plus cher que l'opérateur A, quel que soit le nombre 
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 1: _Teste avec un grand nombre de minutes, par exemple $x = 200$ : $f(200) = 0{,}10 \times 200 + 15 = 35_

### curriculum — 3EME / Fonctions_Affines_Brevet (row 41, exo 19)
- **Q**: À partir de combien de minutes hors forfait les deux opérateurs coûtent-ils le m
- **A**: 100
- `WARN_HINT_IS_FORMULA` step 1: _On résout $f(x) = g(x)$, soit $0{,}10x + 15 = 0{,}05x + 20$._
- `WARN_HINT_IS_FORMULA` step 2: _$0{,}10x - 0{,}05x = 20 - 15$, donc $0{,}05x = 5$, soit $x = $ ?_

### curriculum — 3EME / Fonctions_Affines_Brevet (row 41, exo 20)
- **Q**: Hugo consomme $200$ minutes hors forfait par mois. Quel opérateur doit-il choisi
- **A**: Opérateur B — il économise $5~€$
- `WARN_HINT_IS_FORMULA` step 1: _$f(200) = 0{,}10 \times 200 + 15 = 35~€$ et $g(200) = 0{,}05 \times 200 + 20 = 30~€$._

### curriculum — 3EME / Fonctions_Brevet (row 42, exo 1)
- **Q**: Quelle est l'expression de $f(d)$ ? Calcule le prix pour une course de 10 km.
- **A**: 15
- `WARN_HINT_IS_FORMULA` step 1: _Le prix est : prise en charge + prix au km $\times$ distance, soit $f(d) = 1{,}2d + 3$._
- `WARN_HINT_IS_FORMULA` step 2: _$f(10) = 1{,}2 \times 10 + 3 = 12 + 3 = \;?$._

### curriculum — 3EME / Fonctions_Brevet (row 42, exo 2)
- **Q**: Quel est le prix d'une course de 25 km ?
- **A**: $33$ €
- `WARN_HINT_IS_FORMULA` step 1: _On calcule $f(25) = 1{,}2 \times 25 + 3$._
- `WARN_HINT_IS_FORMULA` step 2: _$f(25) = 30 + 3 = \;?$._

### curriculum — 3EME / Fonctions_Brevet (row 42, exo 3)
- **Q**: Quelle est l'image de 0 par $f$ ? Que représente cette valeur concrètement ?
- **A**: 3
- `WARN_HINT_IS_FORMULA` step 1: _$f(0) = 1{,}2 \times 0 + 3 = 3$. C'est le prix quand la distance est nulle._
- `WARN_HINT_IS_FORMULA` step 2: _Ce montant correspond à la prise en charge (prix fixe au départ). $f(0) = \;?$._

### curriculum — 3EME / Fonctions_Brevet (row 42, exo 4)
- **Q**: Un client a payé 27 €. Quelle distance a-t-il parcourue ?
- **A**: $20$ km
- `WARN_HINT_IS_FORMULA` step 1: _On cherche $d$ tel que $f(d) = 27$, soit $1{,}2d + 3 = 27$._
- `WARN_HINT_IS_FORMULA` step 2: _$1{,}2d = 24$, donc $d = \frac{24}{1{,}2} = \;?$._

### curriculum — 3EME / Fonctions_Brevet (row 42, exo 5)
- **Q**: Un concurrent propose un tarif sans prise en charge mais à 1,50 € par km. Pour u
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _Premier taxi : $f(20) = 1{,}2 \times 20 + 3 = 27$ €. Concurrent : $1{,}5 \times 20 = 30$ €._

### curriculum — 3EME / Fonctions_Brevet (row 42, exo 6)
- **Q**: Quelle est la température de la pièce à 14 h ? (lecture graphique)
- **A**: 22
- `WARN_HINT_IS_FORMULA` step 1: _On repère $t = 14$ sur l'axe horizontal, puis on lit l'ordonnée du point correspondant sur la courbe_

### curriculum — 3EME / Fonctions_Brevet (row 42, exo 7)
- **Q**: Quelle est l'image de 4 par la fonction $T$ ?
- **A**: $15$ °C
- `WARN_HINT_IS_FORMULA` step 2: _Sur la courbe (ou le tableau), à $t = 4$ on lit $T = \;?$._

### curriculum — 3EME / Fonctions_Brevet (row 42, exo 8)
- **Q**: À quelle(s) heure(s) la température vaut-elle 19 °C ? Donne l'antécédent le plus
- **A**: 20
- `WARN_HINT_IS_FORMULA` step 1: _On trace la droite horizontale $T = 19$ et on cherche les intersections avec la courbe._
- `WARN_HINT_IS_FORMULA` step 2: _La courbe coupe $T = 19$ en deux points : vers $t \approx 11$ h (montée) et $t = \;?$ h (descente)._

### curriculum — 3EME / Fonctions_Brevet (row 42, exo 9)
- **Q**: Sur quel intervalle de temps la température est-elle supérieure ou égale à 20 °C
- **A**: De 12 h à 18 h
- `WARN_HINT_IS_FORMULA` step 1: _On cherche quand la courbe est au-dessus (ou sur) la droite $T = 20$._
- `WARN_HINT_IS_FORMULA` step 2: _D'après le tableau et la courbe, $T \geq 20$ entre $t = 12$ et $t = \;?$._

### curriculum — 3EME / Fonctions_Brevet (row 42, exo 10)
- **Q**: La température maximale est atteinte à 16 h. La fonction $T$ est-elle croissante
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 2: _Entre $t = 0$ (16 °C) et $t = 4$ (15 °C), la température descend. Peut-on dire que $T$ est croissant_

### curriculum — 3EME / Fonctions_Brevet (row 42, exo 12)
- **Q**: Quelle est l'image de 5 par la fonction $h$ ?
- **A**: $45$ cm
- `WARN_HINT_IS_FORMULA` step 2: _On lit dans le tableau : $h(5) = \;?$._

### curriculum — 3EME / Fonctions_Brevet (row 42, exo 13)
- **Q**: De combien de centimètres la plante a-t-elle grandi entre la semaine 2 et la sem
- **A**: 24
- `WARN_HINT_IS_FORMULA` step 1: _On calcule la différence : $h(4) - h(2) = 32 - 8$._

### curriculum — 3EME / Fonctions_Brevet (row 42, exo 14)
- **Q**: La croissance est-elle plus rapide entre la semaine 1 et la semaine 3 qu'entre l
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _Semaine 1→3 : $h(3) - h(1) = 18 - 2 = 16$ cm en 2 semaines. Semaine 5→7 : $h(7) - h(5) = 60 - 45 = 1_

### curriculum — 3EME / Fonctions_Brevet (row 42, exo 15)
- **Q**: La croissance hebdomadaire moyenne entre la semaine 0 et la semaine 8 est de :
- **A**: $7{,}875$ cm/semaine
- `WARN_HINT_IS_FORMULA` step 1: _La croissance totale est $h(8) - h(0) = 63 - 0 = 63$ cm sur 8 semaines._
- `WARN_HINT_IS_FORMULA` step 2: _Croissance moyenne $= \frac{63}{8} = \;?$ cm/semaine._

### curriculum — 3EME / Fonctions_Brevet (row 42, exo 16)
- **Q**: Exprime $B(x)$ en fonction de $x$ (avec $p = 7$) et calcule $B(20)$.
- **A**: 20
- `WARN_HINT_IS_ANSWER` step 2: _$B(20) = 5 \times 20 - 80 = 100 - 80 = \;?$._
- `WARN_HINT_IS_FORMULA` step 1: _$B(x) = R(x) - C(x) = 7x - (2x + 80) = 5x - 80$._
- `WARN_HINT_IS_FORMULA` step 2: _$B(20) = 5 \times 20 - 80 = 100 - 80 = \;?$._

### curriculum — 3EME / Fonctions_Brevet (row 42, exo 17)
- **Q**: Pour combien de coques vendues le bénéfice est-il nul (seuil de rentabilité) ?
- **A**: $16$ coques
- `WARN_HINT_IS_FORMULA` step 1: _On résout $B(x) = 0$, soit $5x - 80 = 0$._
- `WARN_HINT_IS_FORMULA` step 2: _$5x = 80$, donc $x = \frac{80}{5} = \;?$._

### curriculum — 3EME / Fonctions_Brevet (row 42, exo 18)
- **Q**: Complète le tableau de valeurs du bénéfice. Quel est $B(30)$ ?
- **A**: 70
- `WARN_HINT_IS_FORMULA` step 1: _$B(30) = 5 \times 30 - 80 = 150 - 80$._
- `WARN_HINT_IS_FORMULA` step 2: _$B(30) = \;?$ €._

### curriculum — 3EME / Fonctions_Brevet (row 42, exo 19)
- **Q**: L'entreprise veut un bénéfice d'au moins 120 €. Combien de coques minimum doit-e
- **A**: $40$ coques
- `WARN_HINT_IS_FORMULA` step 2: _$5x \geq 200$, donc $x \geq \frac{200}{5} = \;?$._

### curriculum — 3EME / Fonctions_Brevet (row 42, exo 20)
- **Q**: Si le prix unitaire passe à 6 € au lieu de 7 €, le seuil de rentabilité augmente
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _Avec $p = 6$ : $B(x) = 6x - (2x + 80) = 4x - 80$. Seuil : $4x - 80 = 0 \Rightarrow x = 20$._

### curriculum — 3EME / Fractions_Brevet (row 43, exo 1)
- **Q**: Inès mélange $\frac{1}{3}$ de litre de lait et $\frac{1}{4}$ de litre de crème. 
- **A**: 7/12
- `WARN_HINT_IS_FORMULA` step 1: _Dénominateur commun de $3$ et $4$ : $\text{PPCM}(3, 4) = 12$._
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{1}{3} = \frac{4}{12}$ et $\frac{1}{4} = \frac{3}{12}$. Donc $\frac{4}{12} + \frac{3}{12} = \f_
- `WARN_HINT_IS_FORMULA` step 3: _$\text{PGCD}(7, 12) = 1$ : la fraction est-elle déjà irréductible ?_

### curriculum — 3EME / Fractions_Brevet (row 43, exo 2)
- **Q**: Elle doit aussi ajouter $\frac{3}{4}$ de litre d'eau puis retirer $\frac{1}{6}$ 
- **A**: 7/12
- `WARN_HINT_IS_FORMULA` step 1: _Dénominateur commun de $4$ et $6$ : $\text{PPCM}(4, 6) = 12$._
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{3}{4} = \frac{9}{12}$ et $\frac{1}{6} = \frac{2}{12}$. Donc $\frac{9}{12} - \frac{2}{12} = \f_
- `WARN_HINT_IS_FORMULA` step 3: _Simplifie si possible : $\text{PGCD}(?, 12) = \,?$_

### curriculum — 3EME / Fractions_Brevet (row 43, exo 3)
- **Q**: Inès a besoin de $\frac{2}{5}$ de kg de farine et $\frac{1}{3}$ de kg de sucre. 
- **A**: $\frac{11}{15}$
- `WARN_HINT_IS_FORMULA` step 1: _Dénominateur commun de $5$ et $3$ : $\text{PPCM}(5, 3) = 15$._
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{2}{5} = \frac{6}{15}$ et $\frac{1}{3} = \frac{5}{15}$. Calcule $\frac{6}{15} + \frac{5}{15} =_

### curriculum — 3EME / Fractions_Brevet (row 43, exo 4)
- **Q**: Inès affirme : « $\frac{5}{6} - \frac{2}{3} = \frac{3}{3} = 1$ ». A-t-elle raiso
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 2: _Il faut d'abord mettre au même dénominateur : $\frac{2}{3} = \frac{4}{6}$. Donc $\frac{5}{6} - \frac_

### curriculum — 3EME / Fractions_Brevet (row 43, exo 5)
- **Q**: Pour sa pâte à crêpes, Inès mélange $\frac{1}{2}$ L de lait, $\frac{1}{4}$ L de 
- **A**: $\frac{7}{8}$
- `WARN_HINT_IS_FORMULA` step 1: _Dénominateur commun : $\text{PPCM}(2, 4, 8) = 8$._
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{1}{2} = \frac{4}{8}$, $\frac{1}{4} = \frac{2}{8}$, $\frac{1}{8} = \frac{1}{8}$. Calcule $\fra_

### curriculum — 3EME / Fractions_Brevet (row 43, exo 6)
- **Q**: Hugo reçoit $\frac{1}{3}$ du terrain, puis il en revend $\frac{1}{4}$ à sa sœur.
- **A**: 1/4
- `WARN_HINT_IS_FORMULA` step 2: _Il garde $1 - \frac{1}{4} = \frac{3}{4}$ de sa part. Donc il possède $\frac{3}{4} \times \frac{1}{3}_
- `WARN_HINT_IS_FORMULA` step 3: _Simplifie : $\frac{3}{12} = \frac{?}{?}$_

### curriculum — 3EME / Fractions_Brevet (row 43, exo 7)
- **Q**: La part de Jade représente $\frac{2}{5}$ du terrain. Elle divise cette part en $
- **A**: 80
- `WARN_HINT_IS_FORMULA` step 1: _Part de Jade : $\frac{2}{5} \times 600 = \frac{?}{?} = ?\text{ m}^2$._
- `WARN_HINT_IS_FORMULA` step 2: _Elle divise par $3$ : $\frac{240}{3} = ?\text{ m}^2$. Ou bien directement $\frac{2}{5} \times \frac{_
- `WARN_HINT_IS_FORMULA` step 3: _Vérifie : $\frac{2}{15} \times 600 = ?$_

### curriculum — 3EME / Fractions_Brevet (row 43, exo 8)
- **Q**: Adam possède $\frac{3}{8}$ du terrain. Il vend $\frac{2}{3}$ de sa part. Quelle 
- **A**: $\frac{1}{4}$
- `WARN_HINT_IS_FORMULA` step 1: _Fraction vendue du terrain total : $\frac{2}{3} \times \frac{3}{8} = \frac{2 \times 3}{3 \times 8} =_
- `WARN_HINT_IS_FORMULA` step 2: _Simplifie $\frac{6}{24}$ : $\text{PGCD}(6, 24) = 6$. Donc $\frac{6 \div 6}{24 \div 6} = \frac{?}{?}$_

### curriculum — 3EME / Fractions_Brevet (row 43, exo 10)
- **Q**: Le terrain de $600\text{ m}^2$ est divisé en parcelles de $\frac{3}{4}\text{ m}^
- **A**: $800$
- `WARN_HINT_IS_FORMULA` step 2: _Diviser par $\frac{3}{4}$, c'est multiplier par $\frac{4}{3}$ : $600 \times \frac{4}{3} = \frac{?}{?_
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{2400}{3} = ?$. Le distracteur $450$ vient de $600 \times \frac{3}{4}$ (multiplier au lieu de _

### curriculum — 3EME / Fractions_Brevet (row 43, exo 11)
- **Q**: Une veste coûte $80$ €. Elle est soldée à $\frac{3}{4}$ de son prix. Quel est le
- **A**: 60
- `WARN_HINT_IS_FORMULA` step 1: _Prendre $\frac{3}{4}$ d'un prix, c'est multiplier : $\frac{3}{4} \times 80 = \frac{3 \times 80}{4}$._
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{240}{4} = ?$ €._
- `WARN_HINT_IS_FORMULA` step 3: _Autre méthode : $80 \div 4 = 20$, puis $20 \times 3 = ?$ €._

### curriculum — 3EME / Fractions_Brevet (row 43, exo 12)
- **Q**: Un pantalon affiché à $60$ € bénéficie d'une réduction de $\frac{1}{5}$. Quel es
- **A**: $12$ €
- `WARN_HINT_IS_FORMULA` step 1: _La réduction est $\frac{1}{5}$ du prix : $\frac{1}{5} \times 60 = \frac{?}{?}$._
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{60}{5} = ?$ €. Attention : on demande la réduction, pas le prix final._

### curriculum — 3EME / Fractions_Brevet (row 43, exo 13)
- **Q**: Emma dit : « Un article soldé à $-25\%$, c'est comme payer $\frac{3}{4}$ du prix
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _$-25\%$ signifie qu'on retire $\frac{25}{100} = \frac{1}{4}$ du prix._
- `WARN_HINT_IS_FORMULA` step 2: _On paie donc $1 - \frac{1}{4} = \frac{3}{4}$ du prix initial._

### curriculum — 3EME / Fractions_Brevet (row 43, exo 14)
- **Q**: Un pull à $90$ € est soldé à $-30\%$. Lucas paie avec un bon de réduction supplé
- **A**: 54
- `WARN_HINT_IS_FORMULA` step 1: _Prix après solde : $90 \times (1 - 0{,}30) = 90 \times 0{,}70 = ?$ €. Ou bien : $90 \times \frac{7}{_
- `WARN_HINT_IS_FORMULA` step 2: _Bon supplémentaire de $\frac{1}{7}$ : réduction = $\frac{1}{7} \times 63 = ?$ €. Prix final = $63 - _
- `WARN_HINT_IS_FORMULA` step 3: _Ou directement : $63 \times \frac{6}{7} = \frac{?}{?} = ?$ €._

### curriculum — 3EME / Fractions_Brevet (row 43, exo 15)
- **Q**: Léa achète $3$ articles : un t-shirt à $\frac{2}{3}$ de $45$ €, un jean à $\frac
- **A**: $153$ €
- `WARN_HINT_IS_FORMULA` step 1: _T-shirt : $\frac{2}{3} \times 45 = \frac{90}{3} = ?$ €. Jean : $\frac{4}{5} \times 75 = \frac{300}{5_
- `WARN_HINT_IS_FORMULA` step 2: _Baskets : $\frac{7}{10} \times 90 = \frac{630}{10} = ?$ €._

### curriculum — 3EME / Fractions_Brevet (row 43, exo 16)
- **Q**: La recette nécessite $\frac{3}{4}$ de litre de bouillon pour $4$ personnes. Le c
- **A**: 9/8
- `WARN_HINT_IS_FORMULA` step 1: _Coefficient multiplicateur : $\frac{6}{4} = \frac{3}{2}$._
- `WARN_HINT_IS_FORMULA` step 2: _Quantité pour $6$ : $\frac{3}{4} \times \frac{3}{2} = \frac{? \times ?}{? \times ?} = \frac{?}{?}$._
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{9}{8}$ est-il irréductible ? $\text{PGCD}(9, 8) = ?$_

### curriculum — 3EME / Fractions_Brevet (row 43, exo 17)
- **Q**: La recette demande $\frac{2}{3}$ kg de viande et $\frac{5}{6}$ kg de légumes pou
- **A**: $\frac{15}{4}$ kg
- `WARN_HINT_IS_FORMULA` step 1: _Coefficient : $\frac{10}{4} = \frac{5}{2}$. Viande : $\frac{2}{3} \times \frac{5}{2} = \frac{10}{6} _
- `WARN_HINT_IS_FORMULA` step 2: _Légumes : $\frac{5}{6} \times \frac{5}{2} = \frac{25}{12}$ kg. Total : $\frac{5}{3} + \frac{25}{12} _
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{5}{3} = \frac{20}{12}$. Donc $\frac{20}{12} + \frac{25}{12} = \frac{?}{12}$. Simplifie._

### curriculum — 3EME / Fractions_Brevet (row 43, exo 18)
- **Q**: Le chef affirme : « Pour passer de $4$ à $12$ convives, il suffit de multiplier 
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _Coefficient multiplicateur : $\frac{12}{4} = ?$._

### curriculum — 3EME / Fractions_Brevet (row 43, exo 19)
- **Q**: Le chef adapte pour $7$ personnes. Il lui faut $\frac{2}{3}$ L de crème (quantit
- **A**: 7/6
- `WARN_HINT_IS_FORMULA` step 1: _Coefficient : $\frac{7}{4}$. Crème pour $7$ : $\frac{2}{3} \times \frac{7}{4} = \frac{2 \times 7}{3 _
- `WARN_HINT_IS_FORMULA` step 2: _Simplifie $\frac{14}{12}$ : $\text{PGCD}(14, 12) = 2$. Donc $\frac{14 \div 2}{12 \div 2} = \frac{?}{_

### curriculum — 3EME / Fractions_Brevet (row 43, exo 20)
- **Q**: Le chef a $\frac{5}{3}$ kg de farine. Sa recette pour $4$ personnes en demande $
- **A**: $17$
- `WARN_HINT_IS_ANSWER` step 3: _On ne peut servir qu'un nombre entier de personnes. $\frac{160}{9} = 17{,}7\ldots$ Donc au maximum $_
- `WARN_HINT_IS_FORMULA` step 1: _Nombre de « portions de $4$ » : $\frac{5}{3} \div \frac{3}{8} = \frac{5}{3} \times \frac{8}{3} = \fr_
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{40}{9} \approx 4{,}44$ portions de $4$ personnes. Nombre de personnes : $\frac{40}{9} \times _
- `WARN_HINT_IS_FORMULA` step 3: _On ne peut servir qu'un nombre entier de personnes. $\frac{160}{9} = 17{,}7\ldots$ Donc au maximum $_

### curriculum — 3EME / Geometrie_Espace_Brevet (row 44, exo 1)
- **Q**: Calcule le volume exact d'une boule de glace de rayon $3$ cm. Donne ta réponse e
- **A**: 36π
- `WARN_HINT_IS_FORMULA` step 1: _La boule est une sphère → formule $V = \frac{4}{3}\pi r^3$ avec $r = 3$._
- `WARN_HINT_IS_FORMULA` step 2: _$V = \frac{4}{3} \times \pi \times 3^3 = \frac{4}{3} \times 27\pi = \;?\;\pi$ cm$^3$._

### curriculum — 3EME / Geometrie_Espace_Brevet (row 44, exo 2)
- **Q**: Quel est le volume exact du cône en gaufrette ?
- **A**: 30π cm³
- `WARN_HINT_IS_FORMULA` step 1: _Le cône a pour rayon $r = 3$ et hauteur $h = 10$ → formule $V = \frac{1}{3}\pi r^2 h$._
- `WARN_HINT_IS_FORMULA` step 2: _$V = \frac{1}{3} \times \pi \times 9 \times 10 = \frac{90\pi}{3} = \;?\;\pi$ cm$^3$._

### curriculum — 3EME / Geometrie_Espace_Brevet (row 44, exo 3)
- **Q**: Le volume du présentoir cylindrique est $108\pi$ cm$^3$.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _Le cylindre a $r = 3$ cm et $h = 12$ cm → $V = \pi r^2 h = \pi \times 9 \times 12$._
- `WARN_HINT_IS_FORMULA` step 2: _$V = 108\pi$ cm$^3$. Compare avec l'affirmation — sont-ils égaux ?_

### curriculum — 3EME / Geometrie_Espace_Brevet (row 44, exo 4)
- **Q**: Enzo veut connaître le volume total de glace quand il sert un cône rempli surmon
- **A**: 207
- `WARN_HINT_IS_FORMULA` step 1: _Le volume total = volume du cône + volume de la boule = $30\pi + 36\pi = 66\pi$._

### curriculum — 3EME / Geometrie_Espace_Brevet (row 44, exo 5)
- **Q**: Combien de boules de glace de rayon $3$ cm peut-on empiler exactement dans le pr
- **A**: 3
- `WARN_HINT_IS_FORMULA` step 1: _Chaque boule a un diamètre de $2 \times 3 = 6$ cm. La hauteur du cylindre est $12$ cm._
- `WARN_HINT_IS_FORMULA` step 2: _$12 \div 6 = \;?$ boules. Vérifie aussi que le rayon du cylindre ($3$ cm) = rayon de la boule._

### curriculum — 3EME / Geometrie_Espace_Brevet (row 44, exo 6)
- **Q**: Calcule le périmètre de la base circulaire de la boîte, arrondi au dixième.
- **A**: 31,4
- `WARN_HINT_IS_FORMULA` step 1: _Le périmètre d'un cercle est $P = 2\pi r$ avec $r = 5$ cm._
- `WARN_HINT_IS_FORMULA` step 2: _$P = 2 \times \pi \times 5 = 10\pi \approx \;?$ cm._

### curriculum — 3EME / Geometrie_Espace_Brevet (row 44, exo 7)
- **Q**: Sur le patron, le rectangle qui forme la surface latérale a pour longueur le pér
- **A**: 10π cm × 15 cm
- `WARN_HINT_IS_FORMULA` step 1: _La longueur du rectangle = périmètre de la base = $2\pi r = 2\pi \times 5 = \;?\;\pi$ cm._

### curriculum — 3EME / Geometrie_Espace_Brevet (row 44, exo 8)
- **Q**: Si on coupe la boîte par un plan parallèle à la base, la section obtenue est un 
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 2: _Ce cercle a le même rayon que la base. Ici $r = 5$ cm — l'affirmation est-elle correcte ?_

### curriculum — 3EME / Geometrie_Espace_Brevet (row 44, exo 9)
- **Q**: Calcule l'aire de la surface latérale de la boîte, arrondie à l'unité en cm$^2$.
- **A**: 471
- `WARN_HINT_IS_FORMULA` step 1: _L'aire latérale d'un cylindre est $A = 2\pi r h$ avec $r = 5$ et $h = 15$._
- `WARN_HINT_IS_FORMULA` step 2: _$A = 2 \times \pi \times 5 \times 15 = 150\pi \approx \;?$ cm$^2$._

### curriculum — 3EME / Geometrie_Espace_Brevet (row 44, exo 10)
- **Q**: Jade veut connaître l'aire totale de carton nécessaire (surface latérale + les d
- **A**: 628 cm²
- `WARN_HINT_IS_FORMULA` step 1: _Aire totale = aire latérale + $2 \times$ aire d'un disque = $150\pi + 2 \times \pi \times 5^2 = 150\_

### curriculum — 3EME / Geometrie_Espace_Brevet (row 44, exo 11)
- **Q**: Calcule la hauteur de la maquette en centimètres.
- **A**: 20
- `WARN_HINT_IS_FORMULA` step 2: _Hauteur maquette = $\frac{10}{50} = 0{,}2$ m. Convertis en cm : $0{,}2 \times 100 = \;?$ cm._

### curriculum — 3EME / Geometrie_Espace_Brevet (row 44, exo 12)
- **Q**: Quel est le rayon de la tour sur la maquette ?
- **A**: 4 cm
- `WARN_HINT_IS_FORMULA` step 1: _Rayon réel = $2$ m. Échelle = $\frac{1}{50}$._
- `WARN_HINT_IS_FORMULA` step 2: _Rayon maquette = $\frac{2}{50} = 0{,}04$ m = $\;?$ cm._

### curriculum — 3EME / Geometrie_Espace_Brevet (row 44, exo 13)
- **Q**: Hugo affirme : « Le volume de ma maquette est $50$ fois plus petit que le volume
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 2: _Ici $k = \frac{1}{50}$, donc les volumes sont multipliés par $\left(\frac{1}{50}\right)^3 = \frac{1}_

### curriculum — 3EME / Geometrie_Espace_Brevet (row 44, exo 14)
- **Q**: Calcule le volume réel de la tour cylindrique, arrondi au dixième en m$^3$.
- **A**: 125,7
- `WARN_HINT_IS_FORMULA` step 1: _Volume du cylindre : $V = \pi r^2 h = \pi \times 2^2 \times 10 = 40\pi$._

### curriculum — 3EME / Geometrie_Espace_Brevet (row 44, exo 15)
- **Q**: Quel est le volume de la maquette, arrondi à l'unité en cm$^3$ ?
- **A**: 1005 cm³
- `WARN_HINT_IS_FORMULA` step 1: _Volume maquette = $k^3 \times V_{\text{réel}}$. Avec $k^3 = \frac{1}{125\,000}$ : $V = \frac{40\pi}{_
- `WARN_HINT_IS_FORMULA` step 2: _Convertis en cm$^3$ : $1$ m$^3$ = $1\,000\,000$ cm$^3$. Donc $V = \frac{40\pi \times 1\,000\,000}{12_

### curriculum — 3EME / Geometrie_Espace_Brevet (row 44, exo 16)
- **Q**: Calcule le volume du cylindre, arrondi à l'unité en m$^3$.
- **A**: 226
- `WARN_HINT_IS_FORMULA` step 1: _Volume du cylindre : $V = \pi r^2 h$ avec $r = 3$ et $h = 8$._
- `WARN_HINT_IS_FORMULA` step 2: _$V = \pi \times 9 \times 8 = 72\pi \approx \;?$ m$^3$._

### curriculum — 3EME / Geometrie_Espace_Brevet (row 44, exo 17)
- **Q**: Quel est le volume du cône arrondi au dixième ?
- **A**: 37,7 m³
- `WARN_HINT_IS_FORMULA` step 1: _Volume du cône : $V = \frac{1}{3}\pi r^2 h = \frac{1}{3} \times \pi \times 9 \times 4 = 12\pi$._

### curriculum — 3EME / Geometrie_Espace_Brevet (row 44, exo 18)
- **Q**: La génératrice du cône (segment allant du sommet à un point du cercle de base) m
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 2: _Par Pythagore : $g^2 = r^2 + h^2 = 3^2 + 4^2 = 9 + 16 = \;?$. Puis $g = \sqrt{?}$ — compare avec $5$_

### curriculum — 3EME / Geometrie_Espace_Brevet (row 44, exo 19)
- **Q**: Calcule le volume total du château d'eau (cylindre + cône), arrondi à l'unité en
- **A**: 264
- `WARN_HINT_IS_FORMULA` step 1: _Volume total = $V_{\text{cylindre}} + V_{\text{cône}} = 72\pi + 12\pi = 84\pi$._

### curriculum — 3EME / Geometrie_Espace_Brevet (row 44, exo 20)
- **Q**: Inès veut convertir le volume total en litres. Sachant que $1$ m$^3$ = $1\,000$ 
- **A**: 264 000 L
- `WARN_HINT_IS_FORMULA` step 2: _$264 \times 1\,000 = \;?$ L._

### curriculum — 3EME / Inequations_Brevet (row 45, exo 2)
- **Q**: Résous $3{,}50n + 10 \leq 45$. Combien de cahiers Inès peut-elle acheter au maxi
- **A**: 10
- `WARN_HINT_IS_ANSWER` step 1: _Isole $n$ : $3{,}50n \leq 45 - 10 = 35$_
- `WARN_HINT_IS_FORMULA` step 1: _Isole $n$ : $3{,}50n \leq 45 - 10 = 35$_
- `WARN_HINT_IS_FORMULA` step 2: _Divise par $3{,}50$ (positif, le sens ne change pas) : $n \leq \frac{35}{3{,}50} = ?$_

### curriculum — 3EME / Inequations_Brevet (row 45, exo 3)
- **Q**: Inès affirme : « Si j'achète 11 cahiers à $3{,}50$ € et le lot de stylos à 10 €,
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 1: _Calcule le coût pour 11 cahiers : $3{,}50 \times 11 + 10 = ?$_

### curriculum — 3EME / Inequations_Brevet (row 45, exo 4)
- **Q**: Le prix d'un cahier augmente à 4 €. Inès a toujours 45 € et achète le lot de sty
- **A**: 8
- `WARN_HINT_IS_FORMULA` step 2: _Divise par 4 : $n \leq \frac{35}{4} = 8{,}75$ — comme $n$ est entier, prends la partie entière_

### curriculum — 3EME / Inequations_Brevet (row 45, exo 5)
- **Q**: Inès veut aussi acheter une trousse à 7 €. Avec les cahiers à $3{,}50$ € et le l
- **A**: 8
- `WARN_HINT_IS_FORMULA` step 2: _Divise : $n \leq \frac{28}{3{,}50} = ?$ — prends la partie entière_

### curriculum — 3EME / Inequations_Brevet (row 45, exo 6)
- **Q**: Exprime $T$ en fonction du nombre de minutes $t$ : $T =$ ___
- **A**: 2t + 8
- `WARN_HINT_IS_FORMULA` step 1: _Au départ ($t = 0$), la température est 8°C_
- `WARN_HINT_IS_FORMULA` step 2: _Chaque minute ajoute 2°C : $T = 2 \times t + ?$_

### curriculum — 3EME / Inequations_Brevet (row 45, exo 7)
- **Q**: La réaction ne fonctionne que si $T > 15$°C. Sachant que $T = 2t + 8$, au bout d
- **A**: 4
- `WARN_HINT_IS_FORMULA` step 1: _Isole $t$ : $2t > 15 - 8 = 7$, soit $t > ?$_

### curriculum — 3EME / Inequations_Brevet (row 45, exo 8)
- **Q**: Hugo affirme : « Au bout de 3 minutes, la température atteint $T = 2 \times 3 + 
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 1: _Calcule : $T = 2 \times 3 + 8 = 14$°C — c'est correct_

### curriculum — 3EME / Inequations_Brevet (row 45, exo 9)
- **Q**: La réaction doit aussi rester sous 40°C ($T \leq 40$). Résous $2t + 8 \leq 40$. 
- **A**: 16
- `WARN_HINT_IS_FORMULA` step 1: _Isole $t$ : $2t \leq 40 - 8 = ?$_

### curriculum — 3EME / Inequations_Brevet (row 45, exo 10)
- **Q**: La réaction fonctionne pour $15 < T \leq 40$, soit de $t = 4$ min à $t = 16$ min
- **A**: 12
- `WARN_HINT_IS_FORMULA` step 1: _La réaction commence à $t = 4$ (car $T = 16 > 15$) et finit à $t = 16$ (car $T = 40 \leq 40$)_

### curriculum — 3EME / Inequations_Brevet (row 45, exo 12)
- **Q**: Résous $12{,}5p + 150 \leq 800$. Combien de planches Adam peut-il charger au max
- **A**: 52
- `WARN_HINT_IS_FORMULA` step 1: _Isole $p$ : $12{,}5p \leq 800 - 150 = 650$_
- `WARN_HINT_IS_FORMULA` step 2: _Divise par $12{,}5$ : $p \leq \frac{650}{12{,}5} = ?$_

### curriculum — 3EME / Inequations_Brevet (row 45, exo 13)
- **Q**: Pour la sécurité, Adam ne doit pas charger plus des $\frac{3}{4}$ de 800 kg. Que
- **A**: 600
- `WARN_HINT_IS_FORMULA` step 1: _Calcule $\frac{3}{4} \times 800 = ?$_

### curriculum — 3EME / Inequations_Brevet (row 45, exo 15)
- **Q**: Adam affirme : « Même avec la règle de sécurité ($\leq 600$ kg), je peux transpo
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 1: _Calcule le poids pour 40 planches + outillage : $12{,}5 \times 40 + 150 = ?$_

### curriculum — 3EME / Inequations_Brevet (row 45, exo 17)
- **Q**: Jade veut couvrir les 550 € de coûts. Résous $8x \geq 550$. Quel est le nombre m
- **A**: 69
- `WARN_HINT_IS_FORMULA` step 1: _Divise par 8 : $x \geq \frac{550}{8} = 68{,}75$_

### curriculum — 3EME / Inequations_Brevet (row 45, exo 18)
- **Q**: Jade affirme : « Avec 68 places vendues à 8 €, je couvre les 550 € de coûts du c
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 1: _Calcule les recettes pour 68 places : $8 \times 68 = ?$_

### curriculum — 3EME / Inequations_Brevet (row 45, exo 19)
- **Q**: Jade veut dégager un bénéfice d'au moins 100 €. Résous $8x - 550 \geq 100$. Comb
- **A**: 82
- `WARN_HINT_IS_FORMULA` step 1: _Isole $x$ : $8x \geq 550 + 100 = ?$_
- `WARN_HINT_IS_FORMULA` step 2: _Divise par 8 : $x \geq \frac{650}{8} = ?$ — arrondis à l'entier supérieur_

### curriculum — 3EME / Inequations_Brevet (row 45, exo 20)
- **Q**: Jade propose une promo : les 20 premières places sont à 5 € au lieu de 8 €. Comb
- **A**: 57
- `WARN_HINT_IS_FORMULA` step 1: _Recettes des 20 premières places : $20 \times 5 = 100$ €. Il reste à couvrir : $550 - 100 = ?$_
- `WARN_HINT_IS_FORMULA` step 2: _Inéquation : $8y \geq 450$. Divise par 8 : $y \geq \frac{450}{8} = ?$ — arrondis à l'entier supérieu_

### curriculum — 3EME / Probabilites_Brevet (row 46, exo 1)
- **Q**: Combien y a-t-il de billes au total dans le sac ? ___
- **A**: 12
- `WARN_HINT_IS_ANSWER` step 2: _Il y a $12$ billes en tout._

### curriculum — 3EME / Probabilites_Brevet (row 46, exo 2)
- **Q**: Quelle est la probabilité de tirer une bille bleue ?
- **A**: $\frac{1}{2}$
- `WARN_HINT_IS_ANSWER` step 3: _Attention : $\frac{6}{12}$ et $\frac{1}{2}$ sont la même valeur, mais on attend la fraction simplifi_
- `WARN_HINT_IS_FORMULA` step 2: _$P(\text{bleue}) = \frac{6}{12}$. On simplifie par $6$ : $\frac{6}{12} = $ ?_

### curriculum — 3EME / Probabilites_Brevet (row 46, exo 3)
- **Q**: La probabilité de tirer une bille verte est $\frac{1}{4}$.
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 2: _$P(\text{verte}) = \frac{2}{12} = \frac{1}{6}$, pas $\frac{1}{4}$._

### curriculum — 3EME / Probabilites_Brevet (row 46, exo 4)
- **Q**: Quelle est la probabilité de tirer une bille rouge ? ___
- **A**: 1/3
- `WARN_HINT_IS_FORMULA` step 2: _$P(\text{rouge}) = \frac{4}{12}$. On simplifie par $4$ : $\frac{4}{12} = $ ?_

### curriculum — 3EME / Probabilites_Brevet (row 46, exo 5)
- **Q**: Léa ajoute $3$ billes jaunes dans le sac. Quelle est maintenant la probabilité d
- **A**: $\frac{4}{15}$
- `WARN_HINT_IS_ANSWER` step 2: _$P(\text{rouge}) = \frac{4}{15}$._
- `WARN_HINT_IS_FORMULA` step 2: _$P(\text{rouge}) = \frac{4}{15}$._
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{4}{12} = \frac{1}{3}$ c'était la probabilité AVANT d'ajouter les billes jaunes. Attention au _

### curriculum — 3EME / Probabilites_Brevet (row 46, exo 6)
- **Q**: Quelle est la probabilité de tomber sur un secteur jaune ? ___
- **A**: 7/20
- `WARN_HINT_IS_FORMULA` step 2: _$P(\text{jaune}) = \frac{7}{20}$. Cette fraction est-elle simplifiable ?_

### curriculum — 3EME / Probabilites_Brevet (row 46, exo 7)
- **Q**: Quelle est la probabilité de gagner un lot (n'importe lequel) ?
- **A**: $\frac{3}{5}$
- `WARN_HINT_IS_FORMULA` step 2: _$P(\text{gagner}) = \frac{12}{20}$. On simplifie par $4$ : $\frac{12}{20} = $ ?_

### curriculum — 3EME / Probabilites_Brevet (row 46, exo 8)
- **Q**: La probabilité de perdre est $\frac{2}{5}$.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _$P(\text{perdre}) = 1 - P(\text{gagner}) = 1 - \frac{3}{5} = \frac{2}{5}$._
- `WARN_HINT_IS_FORMULA` step 2: _Ou directement : $\frac{8}{20} = \frac{2}{5}$._

### curriculum — 3EME / Probabilites_Brevet (row 46, exo 9)
- **Q**: Quelle est la probabilité de gagner un stylo ou un livre ?
- **A**: $\frac{1}{4}$
- `WARN_HINT_IS_ANSWER` step 3: _Attention : $\frac{5}{20} = \frac{1}{4}$, pas $\frac{3}{20}$ (qui est « stylo seul »)._
- `WARN_HINT_IS_FORMULA` step 2: _$P(\text{stylo ou livre}) = \frac{3}{20} + \frac{2}{20} = \frac{5}{20}$. On simplifie : $\frac{5}{20_
- `WARN_HINT_IS_FORMULA` step 3: _Attention : $\frac{5}{20} = \frac{1}{4}$, pas $\frac{3}{20}$ (qui est « stylo seul »)._

### curriculum — 3EME / Probabilites_Brevet (row 46, exo 11)
- **Q**: Combien de menus différents sont possibles au total ? ___
- **A**: 6
- `WARN_HINT_IS_FORMULA` step 2: _Nombre total de menus : $3 \times 2 = $ ?_

### curriculum — 3EME / Probabilites_Brevet (row 46, exo 12)
- **Q**: Quelle est la probabilité d'avoir le menu « Salade + Yaourt » ?
- **A**: $\frac{1}{6}$
- `WARN_HINT_IS_ANSWER` step 2: _$P(\text{S-Y}) = \frac{1}{6}$._
- `WARN_HINT_IS_FORMULA` step 2: _$P(\text{S-Y}) = \frac{1}{6}$._

### curriculum — 3EME / Probabilites_Brevet (row 46, exo 13)
- **Q**: La probabilité d'avoir un fruit en dessert est $\frac{1}{3}$.
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 2: _$P(\text{fruit}) = \frac{3}{6} = \frac{1}{2}$, pas $\frac{1}{3}$._

### curriculum — 3EME / Probabilites_Brevet (row 46, exo 14)
- **Q**: Quelle est la probabilité de ne pas avoir de soupe en entrée ? ___
- **A**: 2/3
- `WARN_HINT_IS_FORMULA` step 2: _$P(\text{pas soupe}) = \frac{4}{6}$. On simplifie : $\frac{4}{6} = $ ?_
- `WARN_HINT_IS_FORMULA` step 3: _Autre méthode : $P(\text{pas soupe}) = 1 - P(\text{soupe}) = 1 - \frac{1}{3} = \frac{2}{3}$._

### curriculum — 3EME / Probabilites_Brevet (row 46, exo 15)
- **Q**: Emma veut une salade ou des crudités en entrée, avec un yaourt en dessert. Quell
- **A**: $\frac{1}{3}$
- `WARN_HINT_IS_FORMULA` step 2: _$P = \frac{2}{6}$. On simplifie : $\frac{2}{6} = $ ?_

### curriculum — 3EME / Probabilites_Brevet (row 46, exo 16)
- **Q**: Quelle est la probabilité de gagner un lot (n'importe lequel) avec un billet ? _
- **A**: 1/20
- `WARN_HINT_IS_FORMULA` step 2: _$P(\text{gagner}) = \frac{10}{200}$. On simplifie par $10$ : $\frac{10}{200} = $ ?_

### curriculum — 3EME / Probabilites_Brevet (row 46, exo 17)
- **Q**: Quelle est la fréquence de réussite des lancers francs lors du concours ?
- **A**: $0{,}64$
- `WARN_HINT_IS_ANSWER` step 3: _Attention : $\frac{32}{50}$ est la fraction, $0{,}64$ est la fréquence décimale. $0{,}32$ serait $\f_
- `WARN_HINT_IS_FORMULA` step 1: _Fréquence = $\frac{\text{nombre de réussites}}{\text{nombre total de lancers}} = \frac{32}{50}$._
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{32}{50} = \frac{64}{100} = $ ?_

### curriculum — 3EME / Probabilites_Brevet (row 46, exo 18)
- **Q**: Si on achète un billet, la probabilité de gagner le vélo est $\frac{1}{200}$.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 2: _$P(\text{vélo}) = \frac{1}{200}$._

### curriculum — 3EME / Probabilites_Brevet (row 46, exo 19)
- **Q**: Le club organise un nouveau concours de lancers francs. En se basant sur la fréq
- **A**: 96
- `WARN_HINT_IS_FORMULA` step 2: _$150 \times 0{,}64 = $ ?_

### curriculum — 3EME / Probabilites_Brevet (row 46, exo 20)
- **Q**: On simule $500$ tombolas sur ordinateur et on observe $24$ gains. Vers quelle va
- **A**: $\frac{1}{20}$
- `WARN_HINT_IS_ANSWER` step 1: _La fréquence observée est $\frac{24}{500} = 0{,}048$, proche de $\frac{1}{20} = 0{,}05$._
- `WARN_HINT_IS_ANSWER` step 3: _$\frac{24}{500}$ est la fréquence observée (elle varie). La probabilité théorique $\frac{1}{20}$ est_
- `WARN_HINT_IS_FORMULA` step 1: _La fréquence observée est $\frac{24}{500} = 0{,}048$, proche de $\frac{1}{20} = 0{,}05$._

### curriculum — 3EME / Proportionnalite_Brevet (row 47, exo 1)
- **Q**: D'après le tableau, quel est le prix au kilo des pommes ?
- **A**: $3{,}50$ €
- `WARN_HINT_IS_FORMULA` step 2: _$2$ kg coûtent $7$ €, donc $1$ kg coûte $\frac{7}{2} = ?$ €_

### curriculum — 3EME / Proportionnalite_Brevet (row 47, exo 2)
- **Q**: Le prix des bananes est-il proportionnel à la masse achetée si $1$ kg coûte $2{,
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{8{,}40}{3} = ?$. Compare avec $2{,}80$ €/kg._

### curriculum — 3EME / Proportionnalite_Brevet (row 47, exo 3)
- **Q**: Les poires coûtent $4{,}20$ € le kilo. Combien Jade paie-t-elle pour $1{,}5$ kg 
- **A**: 6,30
- `WARN_HINT_IS_FORMULA` step 2: _$4{,}20 \times 1{,}5 = ?$_

### curriculum — 3EME / Proportionnalite_Brevet (row 47, exo 4)
- **Q**: Jade achète $2{,}5$ kg de pommes et $1$ kg de bananes. Combien paie-t-elle en to
- **A**: 11,55
- `WARN_HINT_IS_FORMULA` step 1: _Pommes : $2{,}5 \times 3{,}50 = ?$ €. Bananes : $1 \times 2{,}80 = ?$ €._

### curriculum — 3EME / Proportionnalite_Brevet (row 47, exo 5)
- **Q**: Un autre primeur vend les pommes $9{,}80$ € les $2{,}5$ kg. Quel étal propose le
- **A**: Le premier étal ($3{,}50$ €/kg)
- `WARN_HINT_IS_FORMULA` step 1: _Second étal : prix au kilo $= \frac{9{,}80}{2{,}5} = ?$ €/kg._

### curriculum — 3EME / Proportionnalite_Brevet (row 47, exo 6)
- **Q**: Un sweat à $45$ € est soldé à $-20\%$. Quel est le montant de la réduction ? ___
- **A**: 9
- `WARN_HINT_IS_FORMULA` step 1: _Réduction $= 45 \times \frac{20}{100} = ?$ €_
- `WARN_HINT_IS_FORMULA` step 2: _On calcule $45 \times 0{,}20 = ?$_

### curriculum — 3EME / Proportionnalite_Brevet (row 47, exo 7)
- **Q**: Quel est le prix soldé du sweat après la réduction de $20\%$ ?
- **A**: $36$ €
- `WARN_HINT_IS_FORMULA` step 2: _Ou directement : $45 \times (1 - 0{,}20) = 45 \times ? = ?$_

### curriculum — 3EME / Proportionnalite_Brevet (row 47, exo 8)
- **Q**: Des baskets coûtaient $80$ € et sont maintenant vendues $60$ €. Le taux de réduc
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 2: _Taux $= \frac{20}{80} \times 100 = ?\%$. Compare avec $25\%$._

### curriculum — 3EME / Proportionnalite_Brevet (row 47, exo 9)
- **Q**: Un sac à dos est affiché à $56$ € après une remise de $30\%$. Quel était son pri
- **A**: 80
- `WARN_HINT_IS_FORMULA` step 2: _$\text{prix initial} = \frac{56}{0{,}70} = ?$_

### curriculum — 3EME / Proportionnalite_Brevet (row 47, exo 10)
- **Q**: Hugo hésite entre deux magasins. SportMax affiche $-30\%$ sur un article à $90$ 
- **A**: SportMax ($63$ €)
- `WARN_HINT_IS_FORMULA` step 1: _SportMax : $90 \times 0{,}70 = ?$ €._
- `WARN_HINT_IS_FORMULA` step 2: _SportPlus : d'abord $90 \times 0{,}80 = ?$ €, puis $? \times 0{,}90 = ?$ €. Compare les deux résulta_

### curriculum — 3EME / Proportionnalite_Brevet (row 47, exo 11)
- **Q**: Sur la carte, la distance Lyon–Valence mesure $5{,}5$ cm. Quelle est la distance
- **A**: 110
- `WARN_HINT_IS_FORMULA` step 2: _$5{,}5 \times 2\,000\,000 = ?$ cm $= ?$ km (diviser par $100\,000$)._

### curriculum — 3EME / Proportionnalite_Brevet (row 47, exo 12)
- **Q**: Léa roule à une vitesse moyenne de $110$ km/h. Combien de temps met-elle pour pa
- **A**: $1$ h
- `WARN_HINT_IS_FORMULA` step 1: _Temps $= \frac{\text{distance}}{\text{vitesse}} = \frac{110}{110} = ?$_

### curriculum — 3EME / Proportionnalite_Brevet (row 47, exo 13)
- **Q**: D'après le tableau, la vitesse moyenne entre Valence et Montélimar est-elle supé
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 2: _$v = \frac{70}{\frac{50}{60}} = 70 \times \frac{60}{50} = ?$ km/h. Compare avec $100$._

### curriculum — 3EME / Proportionnalite_Brevet (row 47, exo 14)
- **Q**: Léa met $1$ h $30$ min pour le tronçon Montélimar–Marseille ($135$ km). Quelle e
- **A**: 90
- `WARN_HINT_IS_FORMULA` step 2: _$v = \frac{135}{1{,}5} = ?$ km/h_

### curriculum — 3EME / Proportionnalite_Brevet (row 47, exo 15)
- **Q**: Quelle est la vitesse moyenne de Léa sur l'ensemble du trajet Lyon–Marseille ($3
- **A**: $94{,}5$ km/h
- `WARN_HINT_IS_FORMULA` step 1: _Temps total $= 3$ h $20$ min $= 3 + \frac{20}{60} = \frac{?}{?}$ h._
- `WARN_HINT_IS_FORMULA` step 2: _$v = \frac{315}{\frac{10}{3}} = 315 \times \frac{3}{10} = ?$ km/h_

### curriculum — 3EME / Proportionnalite_Brevet (row 47, exo 16)
- **Q**: Si Adam fait $4$ séances dans le mois, combien paie-t-il avec la formule A ? ___
- **A**: 37
- `WARN_HINT_IS_FORMULA` step 2: _$25 + 3 \times 4 = 25 + ? = ?$ €_

### curriculum — 3EME / Proportionnalite_Brevet (row 47, exo 17)
- **Q**: Pour $4$ séances, quelle formule est la moins chère ?
- **A**: Formule B ($32$ €)
- `WARN_HINT_IS_FORMULA` step 1: _Formule B : $8 \times 4 = ?$ €._

### curriculum — 3EME / Proportionnalite_Brevet (row 47, exo 18)
- **Q**: À partir de combien de séances la formule A devient-elle plus avantageuse que la
- **A**: 6
- `WARN_HINT_IS_FORMULA` step 2: _$n > \frac{25}{5} = ?$. Quel est le plus petit entier qui convient ?_

### curriculum — 3EME / Proportionnalite_Brevet (row 47, exo 19)
- **Q**: Adam fait $8$ séances. Le mois suivant, la salle augmente l'abonnement de $15\%$
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _Nouvel abonnement : $25 \times 1{,}15 = ?$ €._
- `WARN_HINT_IS_FORMULA` step 2: _Nouveau coût A : $? + 3 \times 8 = ? + 24 = ?$ €. Compare avec $52$ €._

### curriculum — 3EME / Proportionnalite_Brevet (row 47, exo 20)
- **Q**: La salle propose une formule C : $60$ € pour $10$ séances (pack). Adam fait exac
- **A**: Formule A est $8{,}3\%$ moins chère
- `WARN_HINT_IS_FORMULA` step 1: _Formule A : $25 + 3 \times 10 = ?$ €. Formule C : $60$ €._
- `WARN_HINT_IS_FORMULA` step 2: _Différence $= 60 - ? = ?$ €. Pourcentage par rapport à C : $\frac{?}{60} \times 100 = ?\%$_

### curriculum — 3EME / Puissances_Brevet (row 48, exo 1)
- **Q**: Le diamètre d'un atome d'hydrogène est environ $0{,}000\,000\,000\,1$ m. Écris c
- **A**: 1 × 10^{-10}
- `WARN_HINT_IS_FORMULA` step 1: _La notation scientifique s'écrit $a \times 10^{n}$ avec $1 \leqslant a < 10$. Ici $a = ?$._

### curriculum — 3EME / Puissances_Brevet (row 48, exo 2)
- **Q**: Un globule rouge mesure environ $7 \times 10^{-6}$ m. Combien cela fait-il en mè
- **A**: $0{,}000\,007$ m
- `WARN_HINT_IS_FORMULA` step 2: _$7 \times 10^{-6} = 0{,}000\,00?$._

### curriculum — 3EME / Puissances_Brevet (row 48, exo 3)
- **Q**: Le diamètre de la Terre est $12\,742$ km, soit $12\,742\,000$ m. Ce nombre en no
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _On vérifie : $a = 1{,}2742$. Est-ce que $1 \leqslant 1{,}2742 < 10$ ? $?$._

### curriculum — 3EME / Puissances_Brevet (row 48, exo 4)
- **Q**: Combien de fois le globule rouge ($7 \times 10^{-6}$ m) est-il plus grand que l'
- **A**: $70\,000$
- `WARN_HINT_IS_FORMULA` step 1: _On divise la taille du globule par celle de l'atome : $\frac{7 \times 10^{-6}}{1 \times 10^{-10}} = _
- `WARN_HINT_IS_FORMULA` step 2: _On utilise la règle $\frac{10^{a}}{10^{b}} = 10^{a-b}$ : $10^{-6-(-10)} = 10^{?}$._
- `WARN_HINT_IS_FORMULA` step 3: _$7 \times 10^{?} = ?$._

### curriculum — 3EME / Puissances_Brevet (row 48, exo 6)
- **Q**: Après $3$ heures, il y a $2^{3}$ bactéries. Après $4$ heures supplémentaires, ch
- **A**: 2^{7}
- `WARN_HINT_IS_FORMULA` step 2: _$2^{3} \times 2^{4} = 2^{3+?}$._

### curriculum — 3EME / Puissances_Brevet (row 48, exo 7)
- **Q**: Yanis compare deux cultures. La culture A a $2^{10}$ bactéries, la culture B en 
- **A**: $2^{4}$
- `WARN_HINT_IS_FORMULA` step 1: _On divise : $\frac{2^{10}}{2^{6}} = 2^{10-?}$._

### curriculum — 3EME / Puissances_Brevet (row 48, exo 10)
- **Q**: Simplifie : $\frac{2^{8} \times 2^{5}}{(2^{3})^{4}}$.
- **A**: $2^{1}$
- `WARN_HINT_IS_FORMULA` step 1: _Numérateur : $2^{8} \times 2^{5} = 2^{?}$._
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{2^{?}}{2^{?}} = 2^{?}$._

### curriculum — 3EME / Puissances_Brevet (row 48, exo 11)
- **Q**: Écris $10^{-3}$ sous forme de fraction. ___
- **A**: 1/1000
- `WARN_HINT_IS_FORMULA` step 1: _$10^{-n}$ signifie $\frac{1}{10^{n}}$. Ici $n = ?$._

### curriculum — 3EME / Puissances_Brevet (row 48, exo 12)
- **Q**: Un cheveu humain mesure environ $80$ micromètres, soit $80 \times 10^{-6}$ m. En
- **A**: $8 \times 10^{-5}$ m
- `WARN_HINT_IS_FORMULA` step 2: _Donc $80 \times 10^{-6} = 8 \times 10^{?} \times 10^{-6} = 8 \times 10^{?+(-6)}$._

### curriculum — 3EME / Puissances_Brevet (row 48, exo 13)
- **Q**: $\frac{10^{-2}}{10^{-5}}$ est égal à $10^{-7}$.
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 1: _On applique la règle $\frac{10^{a}}{10^{b}} = 10^{a-b}$._
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{10^{-2}}{10^{-5}} = 10^{-2-(-5)} = 10^{-2+?}$._

### curriculum — 3EME / Puissances_Brevet (row 48, exo 14)
- **Q**: Un virus mesure $120$ nm. Un globule blanc mesure $12$ µm. Combien de fois le gl
- **A**: 100
- `WARN_HINT_IS_FORMULA` step 1: _Convertis le globule blanc en nm : $12\text{ µm} = 12 \times 10^{3}\text{ nm} = ?\text{ nm}$._
- `WARN_HINT_IS_FORMULA` step 2: _Divise : $\frac{12\,000}{120} = ?$._

### curriculum — 3EME / Puissances_Brevet (row 48, exo 15)
- **Q**: Simplifie $\frac{5 \times 10^{-3} \times 4 \times 10^{-5}}{2 \times 10^{-4}}$ et
- **A**: $1 \times 10^{-3}$
- `WARN_HINT_IS_FORMULA` step 1: _Numérateur : $5 \times 4 = ?$ et $10^{-3} \times 10^{-5} = 10^{?}$. Donc numérateur $= ? \times 10^{_
- `WARN_HINT_IS_FORMULA` step 2: _Division : $\frac{20}{2} = ?$ et $\frac{10^{-8}}{10^{-4}} = 10^{?}$._

### curriculum — 3EME / Puissances_Brevet (row 48, exo 16)
- **Q**: Écris la distance Terre-Soleil ($1{,}5 \times 10^{8}$ km) en km sans puissance d
- **A**: 150000000
- `WARN_HINT_TOO_SHORT` step 3: _$= ?$ km._

### curriculum — 3EME / Puissances_Brevet (row 48, exo 18)
- **Q**: La distance Terre-Mars ($7{,}8 \times 10^{7}$ km en notation scientifique) est s
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 2: _Ramène au même exposant : $7{,}8 \times 10^{7} = 0{,}78 \times 10^{?}$._

### curriculum — 3EME / Puissances_Brevet (row 48, exo 19)
- **Q**: La lumière parcourt $3 \times 10^{5}$ km/s. Combien de secondes met-elle pour al
- **A**: 2,6 × 10^{3}
- `WARN_HINT_IS_FORMULA` step 1: _Temps $= \frac{\text{distance}}{\text{vitesse}} = \frac{7{,}78 \times 10^{8}}{3 \times 10^{5}}$._

### curriculum — 3EME / Puissances_Brevet (row 48, exo 20)
- **Q**: Voyager 1 est à $2{,}4 \times 10^{10}$ km du Soleil. Combien de fois est-elle pl
- **A**: $\approx 30{,}8$
- `WARN_HINT_IS_FORMULA` step 1: _$\frac{2{,}4 \times 10^{10}}{7{,}78 \times 10^{8}} = \frac{2{,}4}{7{,}78} \times 10^{10-?}$._
- `WARN_HINT_IS_FORMULA` step 3: _$\approx ? \times ? = ?$._

### curriculum — 3EME / Pythagore_Brevet (row 49, exo 1)
- **Q**: L'écran mesure $AB = 3$ m de large et $BC = 4$ m de haut. Calcule la longueur de
- **A**: 5
- `WARN_HINT_IS_FORMULA` step 1: _Le triangle $ABC$ est rectangle en $B$. L'hypoténuse est $AC$. On applique le théorème de Pythagore _
- `WARN_HINT_IS_FORMULA` step 2: _$AC^2 = 3^2 + 4^2 = 9 + 16 = ?$._
- `WARN_HINT_IS_FORMULA` step 3: _$AC = \sqrt{?} = \;?$ m._

### curriculum — 3EME / Pythagore_Brevet (row 49, exo 2)
- **Q**: Samir mesure un second écran : $AB = 4{,}8$ m et $BC = 3{,}6$ m. Quelle est la l
- **A**: $6$ m
- `WARN_HINT_IS_FORMULA` step 1: _Triangle rectangle en $B$ : $AC^2 = 4{,}8^2 + 3{,}6^2$._
- `WARN_HINT_IS_FORMULA` step 2: _$AC^2 = 23{,}04 + 12{,}96 = ?$._
- `WARN_HINT_IS_FORMULA` step 3: _$AC = \sqrt{?} = \;?$ m._

### curriculum — 3EME / Pythagore_Brevet (row 49, exo 3)
- **Q**: Un troisième écran mesure $6{,}4$ m de large et $4{,}8$ m de haut. Calcule sa di
- **A**: 8
- `WARN_HINT_IS_FORMULA` step 1: _On applique Pythagore : $AC^2 = 6{,}4^2 + 4{,}8^2$._
- `WARN_HINT_IS_FORMULA` step 2: _$AC^2 = 40{,}96 + 23{,}04 = ?$._
- `WARN_HINT_IS_FORMULA` step 3: _$AC = \sqrt{?} = \;?$ m._

### curriculum — 3EME / Pythagore_Brevet (row 49, exo 4)
- **Q**: Samir affirme : « La diagonale d'un écran de $2{,}4$ m par $3{,}2$ m mesure exac
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 2: _$\sqrt{?} = \;?$ — compare avec $4$ m._

### curriculum — 3EME / Pythagore_Brevet (row 49, exo 5)
- **Q**: En coupant l'écran de $3$ m par $4$ m le long de sa diagonale, on obtient un tri
- **A**: $12$ m
- `WARN_HINT_IS_FORMULA` step 1: _Le triangle a pour côtés $AB = 3$ m, $BC = 4$ m et $AC = 5$ m (calculé en Q1)._

### curriculum — 3EME / Pythagore_Brevet (row 49, exo 6)
- **Q**: L'échelle mesure $BC = 5$ m. Le pied de l'échelle est à $AC = 3$ m du mur. À que
- **A**: 4
- `WARN_HINT_IS_FORMULA` step 1: _Triangle rectangle en $A$. L'hypoténuse est $BC = 5$ m. On cherche $AB$ (côté de l'angle droit)._
- `WARN_HINT_IS_FORMULA` step 2: _$AB^2 = BC^2 - AC^2 = 5^2 - 3^2 = 25 - 9 = ?$._
- `WARN_HINT_IS_FORMULA` step 3: _$AB = \sqrt{?} = \;?$ m._

### curriculum — 3EME / Pythagore_Brevet (row 49, exo 7)
- **Q**: Avec une échelle de $10$ m posée à une hauteur de $8$ m, à quelle distance du mu
- **A**: $6$ m
- `WARN_HINT_IS_FORMULA` step 1: _Triangle rectangle en $A$ : $AC^2 = BC^2 - AB^2 = 10^2 - 8^2$._
- `WARN_HINT_IS_FORMULA` step 2: _$AC^2 = 100 - 64 = ?$._
- `WARN_HINT_IS_FORMULA` step 3: _$AC = \sqrt{?} = \;?$ m._

### curriculum — 3EME / Pythagore_Brevet (row 49, exo 8)
- **Q**: Jade affirme : « Avec une échelle de $13$ m et le pied à $5$ m du mur, j'atteins
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _On vérifie : $AB^2 = 13^2 - 5^2 = 169 - 25 = ?$._
- `WARN_HINT_IS_FORMULA` step 2: _$AB = \sqrt{?} = \;?$ — compare avec $12$ m._

### curriculum — 3EME / Pythagore_Brevet (row 49, exo 9)
- **Q**: Une échelle de $8{,}5$ m est posée à $4$ m du mur. Calcule la hauteur atteinte s
- **A**: 7,5
- `WARN_HINT_IS_FORMULA` step 1: _$AB^2 = 8{,}5^2 - 4^2 = 72{,}25 - 16 = ?$._
- `WARN_HINT_IS_FORMULA` step 2: _$AB = \sqrt{?} = \;?$ m._

### curriculum — 3EME / Pythagore_Brevet (row 49, exo 10)
- **Q**: Jade dispose d'une échelle de $6{,}5$ m et veut atteindre une fenêtre à $6$ m de
- **A**: $2{,}5$ m
- `WARN_HINT_IS_FORMULA` step 1: _$AC^2 = 6{,}5^2 - 6^2 = 42{,}25 - 36 = ?$._
- `WARN_HINT_IS_FORMULA` step 2: _$AC = \sqrt{?} = \;?$ m._

### curriculum — 3EME / Pythagore_Brevet (row 49, exo 11)
- **Q**: Un terrain rectangulaire mesure $40$ m de long et $30$ m de large. Quelle est la
- **A**: $50$ m
- `WARN_HINT_IS_FORMULA` step 2: _$d^2 = 40^2 + 30^2 = 1600 + 900 = ?$._
- `WARN_HINT_IS_FORMULA` step 3: _$d = \sqrt{?} = \;?$ m._

### curriculum — 3EME / Pythagore_Brevet (row 49, exo 12)
- **Q**: Lucas mesure un triangle tracé au sol : ses côtés mesurent $5$ m, $12$ m et $13$
- **A**: 30
- `WARN_HINT_IS_FORMULA` step 2: _L'angle droit est entre les côtés $5$ m et $12$ m. Aire $= \frac{1}{2} \times 5 \times 12 = ?$ m²._

### curriculum — 3EME / Pythagore_Brevet (row 49, exo 16)
- **Q**: Une cloison rectangulaire mesure $6$ m de large et $8$ m de haut. Inès tend un c
- **A**: 10
- `WARN_HINT_IS_FORMULA` step 2: _$d^2 = 6^2 + 8^2 = 36 + 64 = ?$._
- `WARN_HINT_IS_FORMULA` step 3: _$d = \sqrt{?} = \;?$ m._

### curriculum — 3EME / Pythagore_Brevet (row 49, exo 17)
- **Q**: Une poutre diagonale de $13$ m est posée dans un cadre rectangulaire de $5$ m de
- **A**: $12$ m
- `WARN_HINT_IS_FORMULA` step 2: _$h^2 = 13^2 - 5^2 = 169 - 25 = ?$._
- `WARN_HINT_IS_FORMULA` step 3: _$h = \sqrt{?} = \;?$ m._

### curriculum — 3EME / Pythagore_Brevet (row 49, exo 19)
- **Q**: La dalle triangulaire de la question précédente ($6$ m, $8$ m, $10$ m) est recta
- **A**: 24
- `WARN_HINT_IS_FORMULA` step 2: _Aire $= \frac{1}{2} \times 6 \times 8 = ?$ m²._

### curriculum — 3EME / Pythagore_Brevet (row 49, exo 20)
- **Q**: Inès doit tendre un câble entre deux coins opposés d'une pièce en forme de L. En
- **A**: $15$ m
- `WARN_HINT_IS_FORMULA` step 2: _$d^2 = 9^2 + 12^2 = 81 + 144 = ?$._
- `WARN_HINT_IS_FORMULA` step 3: _$d = \sqrt{?} = \;?$ m._

### curriculum — 3EME / Racines_Carrees_Brevet (row 50, exo 1)
- **Q**: Simplifie $\sqrt{50}$.
- **A**: 5sqrt(2)
- `WARN_HINT_IS_FORMULA` step 2: _$\sqrt{50} = \sqrt{25 \times ?} = \sqrt{25} \times \sqrt{?}$._
- `WARN_HINT_IS_FORMULA` step 3: _$\sqrt{25} = \;?$, donc $\sqrt{50} = ? \times \sqrt{?}$._

### curriculum — 3EME / Racines_Carrees_Brevet (row 50, exo 2)
- **Q**: Simplifie $\sqrt{72}$.
- **A**: 6sqrt(2)
- `WARN_HINT_IS_FORMULA` step 2: _$\sqrt{72} = \sqrt{36} \times \sqrt{?}$._
- `WARN_HINT_IS_FORMULA` step 3: _$\sqrt{36} = \;?$, donc $\sqrt{72} = ? \times \sqrt{?}$._

### curriculum — 3EME / Racines_Carrees_Brevet (row 50, exo 3)
- **Q**: Quelle est la forme simplifiée de $\sqrt{98}$ ?
- **A**: $7\sqrt{2}$
- `WARN_HINT_IS_FORMULA` step 2: _$\sqrt{98} = \sqrt{49} \times \sqrt{?} = ? \times \sqrt{?}$._

### curriculum — 3EME / Racines_Carrees_Brevet (row 50, exo 4)
- **Q**: Une parcelle carrée a une aire de $200$ m². Quelle est la longueur exacte de son
- **A**: $10\sqrt{2}$ m
- `WARN_HINT_IS_FORMULA` step 2: _$200 = 100 \times ?$. Donc $\sqrt{200} = \sqrt{100} \times \sqrt{?}$._
- `WARN_HINT_IS_FORMULA` step 3: _$\sqrt{100} = \;?$, donc le côté = $? \times \sqrt{?}$ m._

### curriculum — 3EME / Racines_Carrees_Brevet (row 50, exo 5)
- **Q**: Théo affirme : « $\sqrt{9} + \sqrt{16} = \sqrt{25}$ ».
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _Calcule chaque terme : $\sqrt{9} = ?$, $\sqrt{16} = ?$, $\sqrt{25} = ?$._

### curriculum — 3EME / Racines_Carrees_Brevet (row 50, exo 6)
- **Q**: Calcule $\sqrt{3} \times \sqrt{12}$.
- **A**: 6
- `WARN_HINT_IS_FORMULA` step 1: _On utilise la règle : $\sqrt{a} \times \sqrt{b} = \sqrt{a \times b}$._
- `WARN_HINT_IS_FORMULA` step 2: _$\sqrt{3} \times \sqrt{12} = \sqrt{3 \times 12} = \sqrt{?}$._
- `WARN_HINT_IS_FORMULA` step 3: _$\sqrt{?} = \;?$._

### curriculum — 3EME / Racines_Carrees_Brevet (row 50, exo 7)
- **Q**: Simplifie $\sqrt{5} \times \sqrt{20}$.
- **A**: 10
- `WARN_HINT_IS_FORMULA` step 1: _$\sqrt{5} \times \sqrt{20} = \sqrt{5 \times 20} = \sqrt{?}$._
- `WARN_HINT_IS_FORMULA` step 2: _$\sqrt{?} = \;?$._

### curriculum — 3EME / Racines_Carrees_Brevet (row 50, exo 8)
- **Q**: Quelle est la forme simplifiée de $\sqrt{\dfrac{48}{3}}$ ?
- **A**: $4$
- `WARN_HINT_IS_FORMULA` step 1: _Simplifie d'abord la fraction sous la racine : $\dfrac{48}{3} = ?$._
- `WARN_HINT_IS_FORMULA` step 2: _$\sqrt{?} = \;?$._

### curriculum — 3EME / Racines_Carrees_Brevet (row 50, exo 9)
- **Q**: Développe et simplifie $\sqrt{2}(3 + \sqrt{2})$.
- **A**: $3\sqrt{2} + 2$
- `WARN_HINT_IS_FORMULA` step 2: _$\sqrt{2} \times 3 = ?$ et $\sqrt{2} \times \sqrt{2} = ?$._

### curriculum — 3EME / Racines_Carrees_Brevet (row 50, exo 10)
- **Q**: Fatima affirme : « $\sqrt{8} \times \sqrt{2} = \sqrt{10}$ ».
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 1: _$\sqrt{8} \times \sqrt{2} = \sqrt{8 \times 2} = \sqrt{?}$._
- `WARN_HINT_IS_FORMULA` step 2: _$\sqrt{?} = \;?$ — compare avec $\sqrt{10} \approx 3{,}16$._

### curriculum — 3EME / Racines_Carrees_Brevet (row 50, exo 11)
- **Q**: Rationalise le dénominateur de $\dfrac{1}{\sqrt{3}}$.
- **A**: sqrt(3)/3
- `WARN_HINT_IS_FORMULA` step 2: _$\dfrac{1}{\sqrt{3}} \times \dfrac{\sqrt{3}}{\sqrt{3}} = \dfrac{\sqrt{3}}{?}$._
- `WARN_HINT_IS_FORMULA` step 3: _$\sqrt{3} \times \sqrt{3} = ?$._

### curriculum — 3EME / Racines_Carrees_Brevet (row 50, exo 12)
- **Q**: Rationalise $\dfrac{6}{\sqrt{2}}$.
- **A**: 3sqrt(2)
- `WARN_HINT_IS_FORMULA` step 1: _Multiplie haut et bas par $\sqrt{2}$ : $\dfrac{6\sqrt{2}}{\sqrt{2} \times \sqrt{2}} = \dfrac{6\sqrt{_
- `WARN_HINT_IS_FORMULA` step 2: _Simplifie : $\dfrac{6\sqrt{2}}{?} = ? \times \sqrt{2}$._

### curriculum — 3EME / Racines_Carrees_Brevet (row 50, exo 13)
- **Q**: Quelle est la forme rationalisée de $\dfrac{4}{\sqrt{5}}$ ?
- **A**: $\dfrac{4\sqrt{5}}{5}$
- `WARN_HINT_IS_FORMULA` step 2: _$\sqrt{5} \times \sqrt{5} = ?$, donc le résultat est $\dfrac{4\sqrt{5}}{?}$._

### curriculum — 3EME / Racines_Carrees_Brevet (row 50, exo 14)
- **Q**: Simplifie $\dfrac{10}{\sqrt{50}}$.
- **A**: $\sqrt{2}$
- `WARN_HINT_IS_ANSWER` step 1: _Simplifie d'abord $\sqrt{50} = 5\sqrt{2}$._
- `WARN_HINT_IS_ANSWER` step 2: _$\dfrac{10}{5\sqrt{2}} = \dfrac{?}{\sqrt{2}}$._
- `WARN_HINT_IS_ANSWER` step 3: _Rationalise : $\dfrac{? \times \sqrt{2}}{\sqrt{2} \times \sqrt{2}} = \dfrac{?\sqrt{2}}{?} = \sqrt{?}_
- `WARN_HINT_IS_FORMULA` step 1: _Simplifie d'abord $\sqrt{50} = 5\sqrt{2}$._
- `WARN_HINT_IS_FORMULA` step 2: _$\dfrac{10}{5\sqrt{2}} = \dfrac{?}{\sqrt{2}}$._
- `WARN_HINT_IS_FORMULA` step 3: _Rationalise : $\dfrac{? \times \sqrt{2}}{\sqrt{2} \times \sqrt{2}} = \dfrac{?\sqrt{2}}{?} = \sqrt{?}_

### curriculum — 3EME / Racines_Carrees_Brevet (row 50, exo 15)
- **Q**: Léa affirme : « $\dfrac{\sqrt{2}}{\sqrt{8}} = \dfrac{1}{2}$ ».
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _$\dfrac{\sqrt{2}}{\sqrt{8}} = \sqrt{\dfrac{2}{8}} = \sqrt{?}$._
- `WARN_HINT_IS_FORMULA` step 2: _$\sqrt{\dfrac{1}{?}} = \dfrac{1}{\sqrt{?}} = \dfrac{1}{?}$ — vérifie._

### curriculum — 3EME / Racines_Carrees_Brevet (row 50, exo 16)
- **Q**: Simplifie $3\sqrt{8} + \sqrt{18}$.
- **A**: 9sqrt(2)
- `WARN_HINT_IS_FORMULA` step 1: _Simplifie chaque terme : $\sqrt{8} = 2\sqrt{2}$ et $\sqrt{18} = 3\sqrt{2}$._
- `WARN_HINT_IS_FORMULA` step 2: _$3 \times 2\sqrt{2} + 3\sqrt{2} = ?\sqrt{2} + ?\sqrt{2}$._
- `WARN_HINT_IS_FORMULA` step 3: _Additionne : $(? + ?)\sqrt{2} = ?\sqrt{2}$._

### curriculum — 3EME / Racines_Carrees_Brevet (row 50, exo 17)
- **Q**: Développe $(2 + \sqrt{3})^2$.
- **A**: $7 + 4\sqrt{3}$
- `WARN_HINT_IS_FORMULA` step 1: _Identité remarquable : $(a+b)^2 = a^2 + 2ab + b^2$._
- `WARN_HINT_IS_FORMULA` step 2: _$2^2 + 2 \times 2 \times \sqrt{3} + (\sqrt{3})^2 = 4 + ?\sqrt{3} + ?$._

### curriculum — 3EME / Racines_Carrees_Brevet (row 50, exo 18)
- **Q**: Développe et simplifie $(\sqrt{5} - 1)(\sqrt{5} + 1)$.
- **A**: 4
- `WARN_HINT_IS_FORMULA` step 1: _Identité remarquable : $(a-b)(a+b) = a^2 - b^2$._
- `WARN_HINT_IS_FORMULA` step 2: _$(\sqrt{5})^2 - 1^2 = ? - ? = ?$._

### curriculum — 3EME / Racines_Carrees_Brevet (row 50, exo 19)
- **Q**: Factorise $5\sqrt{3} + \sqrt{75}$.
- **A**: $10\sqrt{3}$
- `WARN_HINT_IS_FORMULA` step 1: _Simplifie $\sqrt{75}$ : $75 = 25 \times 3$, donc $\sqrt{75} = ?\sqrt{3}$._
- `WARN_HINT_IS_FORMULA` step 2: _$5\sqrt{3} + ?\sqrt{3} = (5 + ?)\sqrt{3} = ?\sqrt{3}$._

### curriculum — 3EME / Racines_Carrees_Brevet (row 50, exo 20)
- **Q**: Nadia affirme : « $(3 - \sqrt{2})(3 + \sqrt{2}) = 7$ ».
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _Identité remarquable $(a-b)(a+b) = a^2 - b^2$._
- `WARN_HINT_IS_FORMULA` step 2: _$3^2 - (\sqrt{2})^2 = 9 - ? = ?$ — compare avec $7$._

### curriculum — 3EME / Scratch_Brevet (row 51, exo 1)
- **Q**: Léa choisit $x = 4$. Quel résultat affiche le programme ?
- **A**: 17
- `WARN_HINT_IS_FORMULA` step 1: _On remplace $x$ par $4$ : première étape, on multiplie par $3$ → $4 \times 3 = 12$._

### curriculum — 3EME / Scratch_Brevet (row 51, exo 2)
- **Q**: Léa choisit maintenant $x = -2$. Quel résultat obtient-elle ?
- **A**: $-1$
- `WARN_HINT_IS_FORMULA` step 1: _On remplace $x$ par $-2$ : $(-2) \times 3 = -6$._

### curriculum — 3EME / Scratch_Brevet (row 51, exo 3)
- **Q**: Voici les résultats obtenus pour plusieurs valeurs de $x$. Complète le tableau.
- **A**: 32
- `WARN_HINT_IS_FORMULA` step 1: _On applique le programme à $x = 9$ : $9 \times 3 = 27$._

### curriculum — 3EME / Scratch_Brevet (row 51, exo 4)
- **Q**: Affirmation : « Si on choisit $x = 10$, le résultat est $35$. »
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _On applique le programme : $10 \times 3 = 30$, puis $30 + 5 = \;?$._

### curriculum — 3EME / Scratch_Brevet (row 51, exo 5)
- **Q**: Quel nombre $x$ faut-il choisir pour que le programme affiche $20$ ?
- **A**: $5$
- `WARN_HINT_IS_FORMULA` step 1: _On cherche $x$ tel que $3x + 5 = 20$, donc $3x = 15$._
- `WARN_HINT_IS_FORMULA` step 2: _On divise : $x = \;?$._

### curriculum — 3EME / Scratch_Brevet (row 51, exo 6)
- **Q**: Inès choisit $x = 6$. Quel résultat annonce-t-elle à Samir ?
- **A**: 19
- `WARN_HINT_IS_FORMULA` step 1: _On applique : $6 \times 2 = 12$._

### curriculum — 3EME / Scratch_Brevet (row 51, exo 8)
- **Q**: Affirmation : « Si le résultat annoncé est $25$, le nombre de départ est $8$. »
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 1: _On résout $2x + 7 = 25$ : $2x = 18$, donc $x = \;?$._

### curriculum — 3EME / Scratch_Brevet (row 51, exo 10)
- **Q**: Samir modifie son programme : au lieu d'ajouter $7$, il ajoute $8$. Quel résulta
- **A**: 14
- `WARN_HINT_IS_FORMULA` step 1: _Le nouveau programme donne $2x + 8$. Pour $x = 3$ : $2 \times 3 = 6$._

### curriculum — 3EME / Scratch_Brevet (row 51, exo 11)
- **Q**: On exécute : AVANCER, AVANCER, AVANCER. Sur quelle case se trouve le robot ?
- **A**: $(0 ; 3)$
- `WARN_HINT_IS_FORMULA` step 2: _Après $3$ pas : $x = 0$, $y = 0 + 3 = \;?$._

### curriculum — 3EME / Scratch_Brevet (row 51, exo 16)
- **Q**: Teste le programme avec $x = 5$. Quel résultat obtient Raphaël ?
- **A**: 15
- `WARN_HINT_IS_FORMULA` step 1: _$x + 3 = 5 + 3 = 8$. Puis on multiplie par $x$ : $8 \times 5 = 40$._
- `WARN_HINT_IS_FORMULA` step 2: _On soustrait $x^2 = 25$ : $40 - 25 = \;?$._

### curriculum — 3EME / Scratch_Brevet (row 51, exo 17)
- **Q**: Teste maintenant avec $x = -2$. Quel résultat le programme affiche-t-il ?
- **A**: $-6$
- `WARN_HINT_IS_FORMULA` step 1: _$x + 3 = -2 + 3 = 1$. Puis $1 \times (-2) = -2$._
- `WARN_HINT_IS_FORMULA` step 2: _On soustrait $x^2 = (-2)^2 = 4$ : $-2 - 4 = \;?$._

### curriculum — 3EME / Scratch_Brevet (row 51, exo 18)
- **Q**: Raphaël teste plusieurs nombres et note les résultats dans un tableau. Quelle co
- **A**: $3x$
- `WARN_HINT_IS_FORMULA` step 1: _Observe le tableau : pour $x = 1$, résultat $= 3$ ; pour $x = 4$, résultat $= 12$._

### curriculum — 3EME / Scratch_Brevet (row 51, exo 19)
- **Q**: Développe l'expression $x(x + 3) - x^2$ pour prouver la conjecture.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _Développe : $x(x+3) = x^2 + 3x$._
- `WARN_HINT_IS_FORMULA` step 2: _Puis $x^2 + 3x - x^2 = \;?$. La conjecture est-elle prouvée ?_

### curriculum — 3EME / Scratch_Brevet (row 51, exo 20)
- **Q**: Raphaël modifie son tour : il remplace « Ajoute $3$ » par « Ajoute $k$ ». Pour q
- **A**: 10
- `WARN_HINT_IS_ANSWER` step 2: _On veut $kx = 10x$, donc $k = \;?$._
- `WARN_HINT_IS_FORMULA` step 1: _Le programme donne $x(x + k) - x^2 = x^2 + kx - x^2 = kx$._
- `WARN_HINT_IS_FORMULA` step 2: _On veut $kx = 10x$, donc $k = \;?$._

### curriculum — 4EME / Puissances (row 52, exo 3)
- **Q**: Une ville compte $45\,000$ habitants. Écrire ce nombre en notation scientifique.
- **A**: $4{,}5\times10^4$
- `WARN_HINT_IS_ANSWER` step 3: _$45\,000 = 4{,}5 \times 10^4$._

### curriculum — 4EME / Puissances (row 52, exo 4)
- **Q**: $0{,}0045 = 4{,}5 \times 10^{-3}$ en notation scientifique.
- **A**: Vrai
- `WARN_HINT_IS_ANSWER` step 3: _Vrai. $0{,}0045 = 4{,}5 \times 10^{-3}$._

### curriculum — 4EME / Puissances (row 52, exo 5)
- **Q**: Complète : $3 \times 10^4 \times 2 \times 10^3 = $ ___
- **A**: $6 \times 10^7$
- `WARN_HINT_IS_FORMULA` step 1: _$(3 \times 2) = 6$ pour les mantisses._
- `WARN_HINT_IS_FORMULA` step 2: _$10^4 \times 10^3 = 10^{4+3} = 10^7$._
- `WARN_HINT_TOO_SHORT` step 3: _$= ?$._

### curriculum — 4EME / Puissances (row 52, exo 7)
- **Q**: Que vaut $(-2)^3$ ?
- **A**: $-8$
- `WARN_HINT_IS_FORMULA` step 2: _$(-2) \times (-2) = 4$, puis $4 \times (-2) = ?$._

### curriculum — 4EME / Puissances (row 52, exo 8)
- **Q**: La distance Paris-New York est d'environ $5{,}8 \times 10^6$ mètres. Convertir e
- **A**: $5\,800\,000$
- `WARN_HINT_IS_ANSWER` step 2: _$5{,}8 \to 58 \to 580 \to 5\,800 \to 58\,000 \to 580\,000 \to 5\,800\,000$._

### curriculum — 4EME / Puissances (row 52, exo 9)
- **Q**: $(3^2)^4 = 3^8$.
- **A**: Vrai
- `WARN_HINT_IS_ANSWER` step 3: _Vrai. $(3^2)^4 = 3^{2 \times 4} = 3^8$._
- `WARN_HINT_IS_FORMULA` step 1: _$(a^m)^n = a^{m \times n}$._
- `WARN_HINT_IS_FORMULA` step 2: _$2 \times 4 = 8$._
- `WARN_HINT_IS_FORMULA` step 3: _Vrai. $(3^2)^4 = 3^{2 \times 4} = 3^8$._

### curriculum — 4EME / Puissances (row 52, exo 10)
- **Q**: Complète : $\frac{a^{-2} \times a^5}{a^3} = a^{\text{___}}$
- **A**: 0
- `WARN_HINT_IS_FORMULA` step 1: _Au numérateur : $a^{-2} \times a^5 = a^{-2+5} = a^3$._
- `WARN_HINT_IS_FORMULA` step 2: _Quotient : $\frac{a^3}{a^3} = a^{3-3} = a^0$._
- `WARN_HINT_IS_FORMULA` step 3: _$a^0 = 1$ pour tout $a \neq 0$._

### curriculum — 4EME / Puissances (row 52, exo 12)
- **Q**: Que vaut $7^0$ ?
- **A**: $1$
- `WARN_HINT_IS_FORMULA` step 1: _$a^0 = ?$ pour tout $a \neq 0$._

### curriculum — 4EME / Puissances (row 52, exo 13)
- **Q**: Un élève calcule :$5^4 \times 5^{-2} = 5^{-8}$. Où est l'erreur ?
- **A**: On additionne les exposants :$5^{4+(-2)}
- `WARN_HINT_IS_FORMULA` step 3: _$5^4 \times 5^{-2} = 5^2 = 25$._

### curriculum — 4EME / Puissances (row 52, exo 14)
- **Q**: $\frac{6 \times 10^8}{3 \times 10^5} = 2 \times 10^3$.
- **A**: Vrai
- `WARN_HINT_IS_ANSWER` step 3: _Vrai. $= 2 \times 10^3$._
- `WARN_HINT_IS_FORMULA` step 1: _$6 \div 3 = 2$._
- `WARN_HINT_IS_FORMULA` step 2: _$10^8 \div 10^5 = 10^{8-5} = 10^3$._

### curriculum — 4EME / Puissances (row 52, exo 15)
- **Q**: Complète : $5{,}3 \times 10^{-11}$ m $=$ ___ nm (sachant $1$ nm $= 10^{-9}$ m).
- **A**: $0{,}053$
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{5{,}3 \times 10^{-11}}{10^{-9}} = 5{,}3 \times 10^{-11-(-9)} = 5{,}3 \times 10^{-2}$._

### curriculum — 4EME / Puissances (row 52, exo 16)
- **Q**: Complète :$10^{-3} =$ ___.
- **A**: 0,001
- `WARN_HINT_IS_FORMULA` step 1: _$10^{-3} = \frac{1}{10^3} = \frac{1}{1000}$._

### curriculum — 4EME / Puissances (row 52, exo 18)
- **Q**: Ordonne du plus petit au plus grand :$2{,}5\times10^3$, $3\times10^2$, $1{,}8\ti
- **A**: $3\times10^2 < 2{,}5\times10^3 < 1{,}8\t
- `WARN_HINT_IS_FORMULA` step 1: _$3\times 10^2 = 300$_
- `WARN_HINT_IS_FORMULA` step 2: _$2,5\times 10^3 = 2\ 500$_
- `WARN_HINT_IS_FORMULA` step 3: _$1,8\times 10^4 = 18\ 000$_

### curriculum — 4EME / Puissances (row 52, exo 19)
- **Q**: $2^{-1} + 2^{-2} = \frac{3}{4}$.
- **A**: Vrai
- `WARN_HINT_IS_ANSWER` step 3: _Vrai._
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{1}{2} + \frac{1}{4} = \frac{2}{4} + \frac{1}{4} = \frac{3}{4}$._
- `WARN_HINT_TOO_SHORT` step 3: _Vrai._

### curriculum — 4EME / Puissances (row 52, exo 20)
- **Q**: Complète : $\frac{1}{4}$ de $8 \times 10^9 = $ ___
- **A**: $2 \times 10^9$
- `WARN_HINT_IS_FORMULA` step 1: _$\frac{8}{4} = 2$._
- `WARN_HINT_TOO_SHORT` step 3: _$= ?$._

### curriculum — 4EME / Calcul_Littéral (row 53, exo 1)
- **Q**: Développe $(x+3)^2$.
- **A**: $x^2+6x+9$
- `WARN_HINT_IS_FORMULA` step 2: _Identifie $a$ et $b$ dans l expression, puis développe avec $(a+b)^2 = a^2 + 2ab + b^2$._

### curriculum — 4EME / Calcul_Littéral (row 53, exo 4)
- **Q**: $(x+5)(x-5) = x^2 - 25$.
- **A**: Vrai
- `WARN_HINT_IS_ANSWER` step 3: _Vrai._
- `WARN_HINT_IS_FORMULA` step 1: _C'est l'identité $(a+b)(a-b) = a^2 - b^2$._
- `WARN_HINT_IS_FORMULA` step 2: _Avec $a = x$ et $b = 5$ : $x^2 - 25$._
- `WARN_HINT_TOO_SHORT` step 3: _Vrai._

### curriculum — 4EME / Calcul_Littéral (row 53, exo 5)
- **Q**: Complète : $(n+1)^2 - n^2 = $ ___
- **A**: $2n+1$
- `WARN_HINT_IS_ANSWER` step 1: _$(n+1)^2 = n^2 + 2n + 1$._
- `WARN_HINT_IS_ANSWER` step 2: _$(n^2 + 2n + 1) - n^2 = 2n + 1$._
- `WARN_HINT_IS_FORMULA` step 1: _$(n+1)^2 = n^2 + 2n + 1$._
- `WARN_HINT_IS_FORMULA` step 2: _$(n^2 + 2n + 1) - n^2 = 2n + 1$._

### curriculum — 4EME / Calcul_Littéral (row 53, exo 8)
- **Q**: Un élève développe :$(x+3)^2 = x^2 + 9$. Où est l'erreur ?
- **A**: Il a oublié le double produit :$(x+3)^2 
- `WARN_HINT_IS_FORMULA` step 1: _$(a+b)^2 = a^2 + 2ab + b^2$._
- `WARN_HINT_IS_FORMULA` step 2: _Ici $a=x$, $b=3$:$x^2 + 2 \times x \times 3 + 9 = x^2 + 6x + 9$._

### curriculum — 4EME / Calcul_Littéral (row 53, exo 9)
- **Q**: $x^2 - 16 = (x-4)^2$.
- **A**: Faux
- `WARN_HINT_IS_ANSWER` step 3: _Faux. C'est $a^2 - b^2 = (a-b)(a+b)$, pas $(a-b)^2$._
- `WARN_HINT_IS_FORMULA` step 1: _$(x-4)^2 = x^2 - 8x + 16 \neq x^2 - 16$._
- `WARN_HINT_IS_FORMULA` step 2: _$x^2 - 16 = x^2 - 4^2 = (x-4)(x+4)$._
- `WARN_HINT_IS_FORMULA` step 3: _Faux. C'est $a^2 - b^2 = (a-b)(a+b)$, pas $(a-b)^2$._

### curriculum — 4EME / Calcul_Littéral (row 53, exo 10)
- **Q**: Complète : $2x^2 + 8x + 8 = 2(\text{___})^2$
- **A**: x+2
- `WARN_HINT_IS_ANSWER` step 2: _$x^2 + 4x + 4 = (x+2)^2$ (identité remarquable)._
- `WARN_HINT_IS_ANSWER` step 3: _$2x^2 + 8x + 8 = 2(x+2)^2$._
- `WARN_HINT_IS_FORMULA` step 2: _$x^2 + 4x + 4 = (x+2)^2$ (identité remarquable)._
- `WARN_HINT_IS_FORMULA` step 3: _$2x^2 + 8x + 8 = 2(x+2)^2$._

### curriculum — 4EME / Calcul_Littéral (row 53, exo 11)
- **Q**: Que vaut $(a+b)^2$ ?
- **A**: $a^2 + 2ab + b^2$
- `WARN_HINT_IS_FORMULA` step 1: _$(a+b)^2 = (a+b)(a+b)$._
- `WARN_HINT_IS_FORMULA` step 2: _$= a^2 + ab + ba + b^2 = ?.$._

### curriculum — 4EME / Calcul_Littéral (row 53, exo 12)
- **Q**: Que vaut $(a-b)(a+b)$ ?
- **A**: $a^2 - b^2$
- `WARN_HINT_IS_FORMULA` step 1: _$(a-b)(a+b) = a^2 + ab - ab - b^2$._
- `WARN_HINT_TOO_SHORT` step 3: _$= ?.$._

### curriculum — 4EME / Calcul_Littéral (row 53, exo 13)
- **Q**: Complète :$(2x-5)^2 = 4x^2 - \text{___}x + 25$.
- **A**: 20
- `WARN_HINT_IS_ANSWER` step 2: _$a = 2x$, $b = 5$:$2ab = 2 \times 2x \times 5 = 20x$._
- `WARN_HINT_IS_ANSWER` step 3: _Le coefficient est 20._
- `WARN_HINT_IS_FORMULA` step 1: _$(a-b)^2 = a^2 - 2ab + b^2$._
- `WARN_HINT_IS_FORMULA` step 2: _$a = 2x$, $b = 5$:$2ab = 2 \times 2x \times 5 = 20x$._

### curriculum — 4EME / Calcul_Littéral (row 53, exo 14)
- **Q**: $(100+1)^2 = 10\,201$.
- **A**: Vrai
- `WARN_HINT_IS_ANSWER` step 3: _Vrai._
- `WARN_HINT_TOO_SHORT` step 3: _Vrai._

### curriculum — 4EME / Calcul_Littéral (row 53, exo 15)
- **Q**: Complète : $x^4 - 1 = (x^2 - 1)(\text{___})$
- **A**: $x^2+1$
- `WARN_HINT_IS_ANSWER` step 3: _$= (x^2 - 1)(x^2 + 1)$._
- `WARN_HINT_IS_FORMULA` step 1: _$x^4 - 1 = (x^2)^2 - 1^2$._
- `WARN_HINT_IS_FORMULA` step 2: _Identité $a^2 - b^2 = (a-b)(a+b)$ avec $a = x^2$, $b = 1$._

### curriculum — 4EME / Calcul_Littéral (row 53, exo 16)
- **Q**: Complète :$3x(2x-4) = 6x^2 - \text{___}x$.
- **A**: 12
- `WARN_HINT_IS_ANSWER` step 2: _$3x \times (-4) = -12x$._
- `WARN_HINT_IS_ANSWER` step 3: _$3x(2x-4) = 6x^2 - 12x$._
- `WARN_HINT_IS_FORMULA` step 1: _On distribue :$3x \times 2x = 6x^2$._
- `WARN_HINT_IS_FORMULA` step 2: _$3x \times (-4) = -12x$._
- `WARN_HINT_IS_FORMULA` step 3: _$3x(2x-4) = 6x^2 - 12x$._

### curriculum — 4EME / Calcul_Littéral (row 53, exo 18)
- **Q**: Développe $(a+b)^2+(a-b)^2$.
- **A**: $2a^2+2b^2$
- `WARN_HINT_IS_ANSWER` step 3: _Somme :$2a^2 + 2b^2$._
- `WARN_HINT_IS_FORMULA` step 1: _$(a+b)^2 = a^2 + 2ab + b^2$_
- `WARN_HINT_IS_FORMULA` step 2: _$(a-b)^2 = a^2 - 2ab + b^2$_

### curriculum — 4EME / Calcul_Littéral (row 53, exo 19)
- **Q**: $(2a+3b)^2 = 4a^2 + 12ab + 9b^2$.
- **A**: Vrai
- `WARN_HINT_IS_ANSWER` step 3: _Vrai. $(2a+3b)^2 = 4a^2 + 12ab + 9b^2$._
- `WARN_HINT_IS_FORMULA` step 1: _$(2a)^2 = 4a^2$, $(3b)^2 = 9b^2$._
- `WARN_HINT_IS_FORMULA` step 2: _$2 \times 2a \times 3b = 12ab$._
- `WARN_HINT_IS_FORMULA` step 3: _Vrai. $(2a+3b)^2 = 4a^2 + 12ab + 9b^2$._

### curriculum — 4EME / Calcul_Littéral (row 53, exo 20)
- **Q**: Complète : si $(x+2)^2 - (x-1)^2 = 15$, alors $x = $ ___
- **A**: $2$
- `WARN_HINT_IS_FORMULA` step 1: _$(x+2)^2 = x^2 + 4x + 4$ et $(x-1)^2 = x^2 - 2x + 1$._
- `WARN_HINT_IS_FORMULA` step 2: _Différence : $(x^2 + 4x + 4) - (x^2 - 2x + 1) = 6x + 3 = 15$._
- `WARN_HINT_IS_FORMULA` step 3: _$6x = 12$, donc $x = ?$._

### curriculum — 4EME / Équations (row 54, exo 1)
- **Q**: Trois places de cinéma plus $5$ € de pop-corn coûtent $17$ €. Quel est le prix d
- **A**: $x=4$
- `WARN_HINT_IS_FORMULA` step 1: _$3x + 5 = 17$. On isole $x$._
- `WARN_HINT_IS_FORMULA` step 2: _$3x = 17 - 5 = 12$._
- `WARN_HINT_IS_FORMULA` step 3: _$x = 12 \div 3 = 4$ €._

### curriculum — 4EME / Équations (row 54, exo 4)
- **Q**: La solution de $4(x-2) = 12$ est $x = 5$.
- **A**: Vrai
- `WARN_HINT_IS_ANSWER` step 3: _Vrai._
- `WARN_HINT_IS_FORMULA` step 1: _$4(x-2) = 12 \Rightarrow x - 2 = 3 \Rightarrow x = 5$._
- `WARN_HINT_IS_FORMULA` step 2: _Vérification : $4(5-2) = 4 \times 3 = 12$. ✓_
- `WARN_HINT_TOO_SHORT` step 3: _Vrai._

### curriculum — 4EME / Équations (row 54, exo 5)
- **Q**: Complète : si $\frac{2x-1}{3} + 1 = x$, alors $x = $ ___
- **A**: $2$
- `WARN_HINT_IS_FORMULA` step 1: _Multiplie par $3$ : $2x - 1 + 3 = 3x$._
- `WARN_HINT_IS_FORMULA` step 2: _$2x + 2 = 3x$._
- `WARN_HINT_IS_FORMULA` step 3: _$x = ?$._
- `WARN_HINT_TOO_SHORT` step 3: _$x = ?$._

### curriculum — 4EME / Équations (row 54, exo 6)
- **Q**: On partage un paquet de billes en $4$ parts égales. Chaque part contient $3$ bil
- **A**: $x=12$
- `WARN_HINT_IS_ANSWER` step 3: _$x = 12$ billes._
- `WARN_HINT_IS_FORMULA` step 1: _$\frac{x}{4} = 3$._
- `WARN_HINT_IS_FORMULA` step 2: _$x = 3 \times 4$._
- `WARN_HINT_IS_FORMULA` step 3: _$x = 12$ billes._

### curriculum — 4EME / Équations (row 54, exo 8)
- **Q**: Combien de solutions a l'équation $x + 5 = x + 3$ ?
- **A**: Aucune
- `WARN_HINT_IS_ANSWER` step 3: _L'équation n'a aucune solution._
- `WARN_HINT_IS_FORMULA` step 1: _$x + 5 - x = x + 3 - x$ donne $5 = 3$._

### curriculum — 4EME / Équations (row 54, exo 9)
- **Q**: Pour résoudre $2x - 6 = 10$, on écrit $2x = 10 + 6 = 16$.
- **A**: Vrai
- `WARN_HINT_IS_ANSWER` step 3: _Vrai. En passant $-6$ de l'autre côté, il devient $+6$._
- `WARN_HINT_IS_FORMULA` step 1: _On ajoute $6$ des deux côtés : $2x = 10 + 6$._
- `WARN_HINT_IS_FORMULA` step 2: _$2x = 16$, donc $x = 8$._

### curriculum — 4EME / Équations (row 54, exo 10)
- **Q**: Complète : l'âge de Jules vérifie $x + 5 = 2x - 3$, donc $x = $ ___
- **A**: $8$
- `WARN_HINT_IS_FORMULA` step 1: _$x + 5 = 2x - 3$._

### curriculum — 4EME / Équations (row 54, exo 11)
- **Q**: Quelle est la solution de $3x = 12$ ?
- **A**: $x = 4$
- `WARN_HINT_IS_FORMULA` step 1: _$3x = 12$._
- `WARN_HINT_IS_FORMULA` step 2: _$x = \frac{12}{3} = 4$._
- `WARN_HINT_IS_FORMULA` step 3: _Vérification : $3 \times 4 = 12$. ✓_

### curriculum — 4EME / Équations (row 54, exo 12)
- **Q**: Complète : si $-4x = 20$, alors $x =$ ___.
- **A**: $-5$
- `WARN_HINT_IS_ANSWER` step 3: _Vérification :$-4 \times (-5) = 20$. ✓_
- `WARN_HINT_IS_FORMULA` step 1: _On divise par $-4$:$x = \frac{20}{-4}$._
- `WARN_HINT_IS_FORMULA` step 2: _$x = ?$._
- `WARN_HINT_IS_FORMULA` step 3: _Vérification :$-4 \times (-5) = 20$. ✓_
- `WARN_HINT_TOO_SHORT` step 2: _$x = ?$._

### curriculum — 4EME / Équations (row 54, exo 13)
- **Q**: Un élève résout :$\frac{x}{3} = 5$ $\rightarrow$ $x = 5 - 3 = 2$. Où est l'erreu
- **A**: Il faut multiplier par 3, pas soustraire
- `WARN_HINT_IS_FORMULA` step 1: _$\frac{x}{3} = 5$ signifie $x \div 3 = 5$._
- `WARN_HINT_IS_FORMULA` step 3: _$x = 5 \times 3 = 15$._

### curriculum — 4EME / Équations (row 54, exo 14)
- **Q**: Dans l'équation $5x + 3 = 2x + 18$, en regroupant on obtient $3x = 15$.
- **A**: Vrai
- `WARN_HINT_IS_ANSWER` step 3: _Vrai. $x = 5$._
- `WARN_HINT_IS_FORMULA` step 1: _$5x - 2x = 18 - 3$._
- `WARN_HINT_IS_FORMULA` step 2: _$3x = 15$._
- `WARN_HINT_IS_FORMULA` step 3: _Vrai. $x = 5$._

### curriculum — 4EME / Équations (row 54, exo 15)
- **Q**: Complète : Marie a $x$ ans, Paul a $3x$ ans. Dans $5$ ans : $(x+5) + (3x+5) = 38
- **A**: $7$
- `WARN_HINT_IS_FORMULA` step 1: _$(x+5) + (3x+5) = 4x + 10 = 38$._
- `WARN_HINT_IS_FORMULA` step 2: _$4x = 28$._
- `WARN_HINT_IS_FORMULA` step 3: _$x = ?$ ans._

### curriculum — 4EME / Équations (row 54, exo 19)
- **Q**: Si $\frac{x}{2} - \frac{x}{3} = 2$, alors $x = 12$.
- **A**: Vrai
- `WARN_HINT_IS_ANSWER` step 3: _Vrai._
- `WARN_HINT_IS_FORMULA` step 1: _Dénominateur commun $6$ : $\frac{3x}{6} - \frac{2x}{6} = \frac{x}{6} = 2$._
- `WARN_HINT_IS_FORMULA` step 2: _$x = 12$._
- `WARN_HINT_TOO_SHORT` step 2: _$x = 12$._
- `WARN_HINT_TOO_SHORT` step 3: _Vrai._

### curriculum — 4EME / Équations (row 54, exo 20)
- **Q**: Complète : si $\begin{cases}x+y=10\\x-y=4\end{cases}$, alors $x = $ ___
- **A**: $7$
- `WARN_HINT_IS_FORMULA` step 1: _Additionne les deux équations : $2x = 14$._
- `WARN_HINT_IS_FORMULA` step 2: _$x = ?$._
- `WARN_HINT_IS_FORMULA` step 3: _$y = 10 - 7 = 3$._
- `WARN_HINT_TOO_SHORT` step 2: _$x = ?$._

### curriculum — 4EME / Pythagore (row 55, exo 3)
- **Q**: Une porte fait $10$ dm de diagonale et $6$ dm de large. Quelle est sa hauteur ?
- **A**: $8$ cm
- `WARN_HINT_IS_FORMULA` step 3: _Côté $= \sqrt{64} = 8$ dm._

### curriculum — 4EME / Pythagore (row 55, exo 4)
- **Q**: Dans un triangle rectangle d'hypoténuse $13$ cm et d'un côté $5$ cm, l'autre côt
- **A**: Vrai
- `WARN_HINT_IS_ANSWER` step 3: _Vrai. Triplet pythagoricien $(5, 12, 13)$._
- `WARN_HINT_IS_FORMULA` step 1: _$b^2 = 13^2 - 5^2 = 169 - 25 = 144$._
- `WARN_HINT_IS_FORMULA` step 2: _$b = \sqrt{144} = 12$ cm._

### curriculum — 4EME / Pythagore (row 55, exo 5)
- **Q**: Complète : la hauteur d'un triangle équilatéral de côté $6$ cm vaut ___ cm.
- **A**: $3\sqrt{3}$
- `WARN_HINT_IS_FORMULA` step 2: _$h^2 = 6^2 - 3^2 = 36 - 9 = 27$._

### curriculum — 4EME / Pythagore (row 55, exo 8)
- **Q**: Un élève calcule dans un triangle rectangle de côtés 7 et 24 : hypoténuse = $\sq
- **A**: Il faut mettre au carré avant d'addition
- `WARN_HINT_IS_FORMULA` step 1: _$c = \sqrt{a^2 + b^2}$, pas $\sqrt{a + b}$._
- `WARN_HINT_IS_FORMULA` step 2: _$\sqrt{49 + 576} = \sqrt{625} = 25$._

### curriculum — 4EME / Pythagore (row 55, exo 9)
- **Q**: Un écran de $5$ dm de haut et $12$ dm de large a une diagonale de $13$ dm.
- **A**: Vrai
- `WARN_HINT_IS_ANSWER` step 3: _Vrai. C'est le triplet $(5, 12, 13)$._
- `WARN_HINT_IS_FORMULA` step 1: _$d^2 = 5^2 + 12^2 = 25 + 144 = 169$._
- `WARN_HINT_IS_FORMULA` step 2: _$d = \sqrt{169} = 13$ dm._

### curriculum — 4EME / Pythagore (row 55, exo 10)
- **Q**: Complète : si $AM = \sqrt{13}$, $A(0,0)$ et $x_M = 2$, alors $y_M = $ ___
- **A**: $3$
- `WARN_HINT_IS_FORMULA` step 1: _$AM^2 = x^2 + y^2 = 13$._
- `WARN_HINT_IS_FORMULA` step 2: _$4 + y^2 = 13$, donc $y^2 = 9$._
- `WARN_HINT_IS_FORMULA` step 3: _$y = ?$._
- `WARN_HINT_TOO_SHORT` step 3: _$y = ?$._

### curriculum — 4EME / Pythagore (row 55, exo 11)
- **Q**: Le théorème de Pythagore permet de calculer :
- **A**: Des longueurs de côtés
- `WARN_HINT_IS_FORMULA` step 2: _$c^2 = a^2 + b^2$ ne fait intervenir que des longueurs._

### curriculum — 4EME / Pythagore (row 55, exo 14)
- **Q**: Dans un triangle $ABC$ rectangle en $C$ avec $AC = 7$ cm et $BC = 24$ cm, $AB = 
- **A**: Vrai
- `WARN_HINT_IS_ANSWER` step 3: _Vrai. Triplet $(7, 24, 25)$._
- `WARN_HINT_IS_FORMULA` step 1: _$AB^2 = AC^2 + BC^2 = 49 + 576 = 625$._
- `WARN_HINT_IS_FORMULA` step 2: _$AB = \sqrt{625} = 25$ cm._

### curriculum — 4EME / Pythagore (row 55, exo 15)
- **Q**: Complète : un escalier de $10$ marches ($20$ cm de haut, $25$ cm de profondeur c
- **A**: $320$
- `WARN_HINT_IS_ANSWER` step 3: _Rampe $= \sqrt{200^2 + 250^2} = \sqrt{102\,500} \approx 320$ cm._
- `WARN_HINT_IS_FORMULA` step 1: _Hauteur totale : $10 \times 20 = 200$ cm._
- `WARN_HINT_IS_FORMULA` step 2: _Profondeur totale : $10 \times 25 = 250$ cm._
- `WARN_HINT_IS_FORMULA` step 3: _Rampe $= \sqrt{200^2 + 250^2} = \sqrt{102\,500} \approx 320$ cm._

### curriculum — 4EME / Pythagore (row 55, exo 16)
- **Q**: Complète : dans un triangle rectangle, si l'hypoténuse vaut 10 et un côté vaut 6
- **A**: 8
- `WARN_HINT_IS_FORMULA` step 1: _$b = \sqrt{c^2 - a^2} = \sqrt{100 - 36}$._
- `WARN_HINT_TOO_SHORT` step 3: _$= ?$._

### curriculum — 4EME / Pythagore (row 55, exo 17)
- **Q**: Un triangle a les côtés $10$ cm, $10$ cm et $10\sqrt{2}$ cm. Est-il rectangle ?
- **A**: Oui, car $10^2+10^2=(10\sqrt{2})^2$
- `WARN_HINT_IS_FORMULA` step 1: _$(10\sqrt{2})^2 = 100 \times  2 = 200$._

### curriculum — 4EME / Pythagore (row 55, exo 18)
- **Q**: Sur un plan de ville, ta maison est en $A(0, 0)$ et l'école en $B(3, 4)$. Quelle
- **A**: $5$
- `WARN_HINT_IS_FORMULA` step 1: _Distance $= \sqrt{(3-0)^2 + (4-0)^2} = \sqrt{9+16}$._

### curriculum — 4EME / Pythagore (row 55, exo 19)
- **Q**: La distance entre $A(1;2)$ et $B(4;6)$ est $5$.
- **A**: Vrai
- `WARN_HINT_IS_ANSWER` step 3: _Vrai. Triplet $(3, 4, 5)$._
- `WARN_HINT_IS_FORMULA` step 1: _$AB = \sqrt{(4-1)^2 + (6-2)^2} = \sqrt{9 + 16} = \sqrt{25}$._
- `WARN_HINT_TOO_SHORT` step 2: _$= 5$._

### curriculum — 4EME / Pythagore (row 55, exo 20)
- **Q**: Complète : dans un triangle isocèle de côtés $8$ cm, $8$ cm, le troisième côté v
- **A**: $\approx 5{,}7$
- `WARN_HINT_IS_ANSWER` step 3: _Par le théorème d'Al-Kashi ou la trigonométrie : $c \approx 5{,}7$ cm (différent de $4{,}7$)._

### curriculum — 4EME / Statistiques (row 56, exo 2)
- **Q**: Emma a eu $8$, $11$, $14$, $13$ et $9$ en histoire. Quelle est sa moyenne ?
- **A**: $11$
- `WARN_HINT_IS_ANSWER` step 1: _On additionne les $5$ notes : $8 + 11 + 14 + 13 + 9$._
- `WARN_HINT_IS_ANSWER` step 2: _$8 + 11 + 14 + 13 + 9 = 55$._
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{55}{5} = ?$. La moyenne d'Emma est $?$._

### curriculum — 4EME / Statistiques (row 56, exo 3)
- **Q**: Dans une classe, $10$ élèves ont eu $8$, $15$ élèves ont eu $12$ et $5$ élèves o
- **A**: $11{,}3\overline{3}$
- `WARN_HINT_IS_ANSWER` step 3: _$\frac{340}{30} \approx 11{,}3\overline{3}$._
- `WARN_HINT_IS_FORMULA` step 2: _$10 \times 8 + 15 \times 12 + 5 \times 16 = 80 + 180 + 80 = 340$. Effectif total : $10 + 15 + 5 = 30_

### curriculum — 4EME / Statistiques (row 56, exo 4)
- **Q**: Jade a obtenu $10$, $10$, $10$, $10$ et $20$. Sa moyenne est $12$.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{60}{5} = 12$. La moyenne est bien $12$._

### curriculum — 4EME / Statistiques (row 56, exo 5)
- **Q**: Noé a $11$ de moyenne après $4$ contrôles. Il veut $12$ de moyenne après le $5$è
- **A**: 16
- `WARN_HINT_IS_FORMULA` step 1: _Après $4$ contrôles à $11$ de moyenne, le total des points est $4 \times 11 = 44$._
- `WARN_HINT_IS_FORMULA` step 2: _Pour avoir $12$ de moyenne sur $5$ contrôles, il faut un total de $5 \times 12 = 60$._

### curriculum — 4EME / Statistiques (row 56, exo 7)
- **Q**: Voici les tailles en cm de $6$ élèves : $152$, $158$, $161$, $165$, $170$, $174$
- **A**: $163$
- `WARN_HINT_IS_FORMULA` step 2: _$3$ème valeur = $161$, $4$ème valeur = $165$._
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{161 + 165}{2} = \frac{326}{2} = ?$._

### curriculum — 4EME / Statistiques (row 56, exo 8)
- **Q**: Adam a relevé les températures sur une semaine : $-2$, $1$, $3$, $5$, $5$, $8$, 
- **A**: $14$
- `WARN_HINT_IS_FORMULA` step 2: _Maximum = $12$, minimum = $-2$._

### curriculum — 4EME / Statistiques (row 56, exo 9)
- **Q**: Dans la série $4$, $7$, $10$, $13$, $16$, $19$, la médiane vaut $11{,}5$.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 2: _$3$ème = $10$, $4$ème = $13$._
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{10 + 13}{2} = \frac{23}{2} = 11{,}5$. À toi de conclure !_

### curriculum — 4EME / Statistiques (row 56, exo 10)
- **Q**: La série triée est : $3$, $5$, $x$, $11$, $15$. La médiane vaut $8$. Que vaut $x
- **A**: 8
- `WARN_HINT_IS_FORMULA` step 3: _Donc $x = ?$. On vérifie : $3, 5, ?, 11, 15$ — la série reste triée._

### curriculum — 4EME / Statistiques (row 56, exo 12)
- **Q**: Un diagramme circulaire montre que $25\%$ des élèves préfèrent le foot et $40\%$
- **A**: $80$
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{40}{100} \times 200 = 0{,}4 \times 200$._

### curriculum — 4EME / Statistiques (row 56, exo 13)
- **Q**: Inès relève les durées d'appels (en min) : $[0;5[$ $\rightarrow$ $8$ appels, $[5
- **A**: $48\%$
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{12}{25} = 0{,}48 = ?$._

### curriculum — 4EME / Statistiques (row 56, exo 14)
- **Q**: Un diagramme en barres montre $3$ catégories d'effectifs $10$, $20$ et $30$. La 
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{30}{60} = 0{,}5 = 50\%$. À toi de conclure !_

### curriculum — 4EME / Statistiques (row 56, exo 16)
- **Q**: Léa a les notes : $8$, $12$, $14$, $6$, $10$. Quelle est la moyenne et la médian
- **A**: Moyenne $= 10$, médiane $= 10$
- `WARN_HINT_IS_FORMULA` step 1: _Moyenne : $\frac{8 + 12 + 14 + 6 + 10}{5} = \frac{50}{5} = 10$._

### curriculum — 4EME / Statistiques (row 56, exo 17)
- **Q**: Les scores d'un jeu sont : $2$, $5$, $5$, $8$, $100$. La moyenne est-elle un bon
- **A**: Non, la médiane ($5$) est plus représent
- `WARN_HINT_IS_FORMULA` step 1: _Moyenne : $\frac{2+5+5+8+100}{5} = \frac{120}{5} = 24$. Cette valeur est tirée vers le haut par $100_
- `WARN_HINT_IS_FORMULA` step 2: _Médiane (série déjà triée, $5$ valeurs) : $3$ème valeur = $5$._

### curriculum — 4EME / Statistiques (row 56, exo 18)
- **Q**: Dans une classe, les notes pondérées sont : contrôle (coeff $3$) = $14$, DM (coe
- **A**: $12$
- `WARN_HINT_IS_FORMULA` step 2: _$= \frac{42 + 8 + 22}{6} = \frac{72}{6}$._
- `WARN_HINT_TOO_SHORT` step 3: _$= ?$._

### curriculum — 4EME / Statistiques (row 56, exo 20)
- **Q**: Une série de $7$ valeurs triées est : $4$, $6$, $8$, $m$, $12$, $15$, $18$. La m
- **A**: 7
- `WARN_HINT_IS_FORMULA` step 1: _Somme totale pour une moyenne de $10$ sur $7$ valeurs : $7 \times 10 = 70$._
- `WARN_HINT_IS_FORMULA` step 3: _$m = 70 - 63 = ?$. On vérifie : $4, 6, ?, 8, 12, 15, 18$ — la série reste triée._

### curriculum — 4EME / Inéquations (row 57, exo 1)
- **Q**: Tu as déjà $3$ € de frais fixes. Ton budget total doit rester inférieur à $8$ €.
- **A**: x < 5
- `WARN_HINT_IS_ANSWER` step 3: _$x < 5$ €._

### curriculum — 4EME / Inéquations (row 57, exo 2)
- **Q**: Résoudre $x - 4 \geq 2$.
- **A**: x ≥ 6
- `WARN_HINT_TOO_SHORT` step 2: _x ≥ 2 + 4_

### curriculum — 4EME / Inéquations (row 57, exo 4)
- **Q**: La solution de $-3x < 12$ est $x > -4$.
- **A**: Vrai
- `WARN_HINT_IS_ANSWER` step 3: _Vrai. Diviser par un négatif inverse l'inégalité._
- `WARN_HINT_IS_FORMULA` step 2: _$x > \frac{12}{-3} = -4$._

### curriculum — 4EME / Inéquations (row 57, exo 5)
- **Q**: Complète : si $3(x-2) > 9$, alors $x > $ ___
- **A**: $5$
- `WARN_HINT_TOO_SHORT` step 2: _$x > 5$._

### curriculum — 4EME / Inéquations (row 57, exo 6)
- **Q**: Résoudre $2x < 10$.
- **A**: x < 5
- `WARN_HINT_TOO_SHORT` step 2: _x < 10/2_

### curriculum — 4EME / Inéquations (row 57, exo 7)
- **Q**: Résoudre $3x > 9$.
- **A**: x > 3
- `WARN_HINT_TOO_SHORT` step 2: _x > 9/3_

### curriculum — 4EME / Inéquations (row 57, exo 8)
- **Q**: Complète :$-5x \geq 15$, donc $x$ ___ $-3$.
- **A**: $\leq$
- `WARN_HINT_IS_ANSWER` step 2: _$x \leq \frac{15}{-5} = -3$._
- `WARN_HINT_IS_ANSWER` step 3: _$x \leq -3$._
- `WARN_HINT_IS_FORMULA` step 2: _$x \leq \frac{15}{-5} = -3$._

### curriculum — 4EME / Inéquations (row 57, exo 9)
- **Q**: L'offre $5x - 3$ est moins chère que $2x + 9$ pour tout $x \leq 4$.
- **A**: Vrai
- `WARN_HINT_IS_ANSWER` step 3: _Vrai. A est avantageuse quand $x \leq 4$._
- `WARN_HINT_IS_FORMULA` step 2: _Pour $x = 4$ : $A = 17$, $B = 17$ (égalité)._

### curriculum — 4EME / Inéquations (row 57, exo 10)
- **Q**: Complète : si $\frac{x+1}{2} < 3$, alors $x < $ ___
- **A**: $5$
- `WARN_HINT_TOO_SHORT` step 2: _$x < 5$._

### curriculum — 4EME / Inéquations (row 57, exo 14)
- **Q**: La solution de $\frac{x}{3} \geq 4$ est $x \geq 12$.
- **A**: Vrai
- `WARN_HINT_IS_ANSWER` step 3: _Vrai._
- `WARN_HINT_IS_FORMULA` step 1: _$\frac{x}{3} \geq 4 \Rightarrow x \geq 4 \times 3 = 12$._
- `WARN_HINT_TOO_SHORT` step 3: _Vrai._

### curriculum — 4EME / Inéquations (row 57, exo 15)
- **Q**: Complète : si $2 \leq 3x - 1 < 8$, alors ___ $\leq x <$ ___
- **A**: $1 \leq x < 3$
- `WARN_HINT_IS_ANSWER` step 2: _Diviser par $3$ : $1 \leq x < 3$._

### curriculum — 4EME / Inéquations (row 57, exo 17)
- **Q**: Complète : la solution de $2x + 1 \leq 9$ est $x \leq$ ___.
- **A**: 4
- `WARN_HINT_IS_FORMULA` step 1: _$2x \leq 9 - 1 = 8$._
- `WARN_HINT_IS_FORMULA` step 2: _$x \leq 8 \div 2 = ?$._

### curriculum — 4EME / Inéquations (row 57, exo 19)
- **Q**: Les entiers vérifiant $1 < x \leq 4$ sont $2$, $3$ et $4$.
- **A**: Vrai
- `WARN_HINT_IS_ANSWER` step 3: _Vrai. Les entiers sont $\{2, 3, 4\}$._

### curriculum — 4EME / Homothétie (row 58, exo 2)
- **Q**: Si k > 1 dans une homothétie, s'agit-il d'un agrandissement ou d'une réduction ?
- **A**: Agrandissement
- `WARN_HINT_IS_ANSWER` step 3: _Le vocabulaire géométrique distingue deux cas : agrandissement ou réduction._

### curriculum — 4EME / Homothétie (row 58, exo 4)
- **Q**: Une homothétie de rapport négatif retourne la figure. Vrai ou Faux ?
- **A**: Vrai
- `WARN_HINT_IS_ANSWER` step 3: _Vrai. Un rapport négatif place l'image de l'autre côté du centre, ce qui retourne la figure._

### curriculum — 4EME / Homothétie (row 58, exo 5)
- **Q**: Complète : l'image de $A(1,2)$ par l'homothétie de centre $O(0,0)$ et rapport $k
- **A**: $-3 ; -6$
- `WARN_HINT_IS_FORMULA` step 1: _$x_{A'} = -3 \times 1 = -3$._
- `WARN_HINT_IS_FORMULA` step 2: _$y_{A'} = -3 \times 2 = -6$._

### curriculum — 4EME / Homothétie (row 58, exo 7)
- **Q**: On agrandit un plan au rapport $k = 2$. Un mur de $4$ cm sur le plan mesure comb
- **A**: 8 cm
- `WARN_HINT_IS_FORMULA` step 1: _Rapport $k = 2$: les longueurs sont multipliées par $2$._
- `WARN_HINT_IS_FORMULA` step 2: _$A'B' = k \times AB = 2 \times 4$._

### curriculum — 4EME / Homothétie (row 58, exo 8)
- **Q**: Complète : une homothétie de rapport $-2$ multiplie les distances par ___.
- **A**: 2
- `WARN_HINT_IS_FORMULA` step 1: _Les distances sont multipliées par $|k| = |-?| = ?$._

### curriculum — 4EME / Homothétie (row 58, exo 9)
- **Q**: Une homothétie de rapport $\frac{1}{3}$ divise les aires par $9$.
- **A**: Vrai
- `WARN_HINT_IS_ANSWER` step 3: _Vrai. Pas par $3$ !_
- `WARN_HINT_IS_FORMULA` step 1: _Rapport des aires $= k^2 = (\frac{1}{3})^2 = \frac{1}{9}$._

### curriculum — 4EME / Homothétie (row 58, exo 10)
- **Q**: Complète : une photo de $10$ cm $\times$ $6$ cm agrandie avec $k = 2{,}5$ mesure
- **A**: $25 \times 15$
- `WARN_HINT_IS_FORMULA` step 1: _$10 \times 2{,}5 = 25$ cm._
- `WARN_HINT_IS_FORMULA` step 2: _$6 \times 2{,}5 = 15$ cm._

### curriculum — 4EME / Homothétie (row 58, exo 12)
- **Q**: Que fait une homothétie de rapport $k = 1$ ?
- **A**: Elle laisse chaque point à sa place
- `WARN_HINT_IS_FORMULA` step 1: _$k = 1$ : $OA' = 1 \times OA = OA$._

### curriculum — 4EME / Homothétie (row 58, exo 13)
- **Q**: Un poster triangulaire agrandi $3$ fois a une aire de $45$ cm$^2$. Quelle était 
- **A**: 5 cm²
- `WARN_HINT_IS_FORMULA` step 1: _L'aire est multipliée par $k^2 = 9$._

### curriculum — 4EME / Homothétie (row 58, exo 14)
- **Q**: Si $A'B' = 14$ cm et le rapport est $k = 2$, alors $AB = 7$ cm.
- **A**: Vrai
- `WARN_HINT_IS_ANSWER` step 3: _Vrai._
- `WARN_HINT_IS_FORMULA` step 1: _$A'B' = k \times AB \Rightarrow AB = \frac{A'B'}{k}$._
- `WARN_HINT_IS_FORMULA` step 2: _$AB = \frac{14}{2} = 7$ cm._
- `WARN_HINT_TOO_SHORT` step 3: _Vrai._

### curriculum — 4EME / Homothétie (row 58, exo 15)
- **Q**: Complète : un triangle image a un périmètre de $18$ cm (rapport $k = 3$). Le pér
- **A**: $6$
- `WARN_HINT_IS_FORMULA` step 2: _$P_{\text{orig}} = \frac{18}{3} = ?$ cm._

### curriculum — 4EME / Homothétie (row 58, exo 19)
- **Q**: Une roue de rayon $4$ cm agrandie $3$ fois a un rayon de $12$ cm.
- **A**: Vrai
- `WARN_HINT_IS_ANSWER` step 3: _Vrai._
- `WARN_HINT_IS_FORMULA` step 1: _$r' = k \times r = 3 \times 4 = 12$ cm._
- `WARN_HINT_TOO_SHORT` step 3: _Vrai._

### curriculum — 4EME / Homothétie (row 58, exo 20)
- **Q**: Complète : si $OA = 3$ cm, $OA' = 9$ cm et $A'$ du même côté que $A$, alors $k =
- **A**: $3$
- `WARN_HINT_IS_FORMULA` step 1: _$k = \frac{OA'}{OA} = \frac{9}{?} = ?$._
- `WARN_HINT_IS_FORMULA` step 3: _$k = ?$ (agrandissement)._

### curriculum — 4EME / Sections_Solides (row 59, exo 1)
- **Q**: On coupe un cube par un plan parallèle à une face. La section obtenue est :
- **A**: Un carré
- `WARN_HINT_IS_ANSWER` step 3: _La section est un carré de même côté que le cube_

### curriculum — 4EME / Sections_Solides (row 59, exo 3)
- **Q**: On coupe un cube par un plan passant par 4 sommets alternés. La section obtenue 
- **A**: Un rectangle
- `WARN_HINT_IS_ANSWER` step 3: _La section est un rectangle (en réalité un rectangle, souvent un carré selon les sommets choisis)_

### curriculum — 4EME / Sections_Solides (row 59, exo 4)
- **Q**: La section d'un pavé droit par un plan passant par deux arêtes latérales opposée
- **A**: Vrai
- `WARN_HINT_IS_ANSWER` step 3: _Vrai. La section est un rectangle._

### curriculum — 4EME / Sections_Solides (row 59, exo 5)
- **Q**: Complète : un cône coupé à mi-hauteur donne une section dont l'aire vaut ___ de 
- **A**: $\frac{1}{4}$
- `WARN_HINT_IS_FORMULA` step 1: _À mi-hauteur, $k = \frac{1}{2}$._

### curriculum — 4EME / Sections_Solides (row 59, exo 6)
- **Q**: On coupe un prisme droit à base triangulaire par un plan parallèle à sa base. La
- **A**: Un triangle
- `WARN_HINT_IS_ANSWER` step 1: _La base du prisme est un triangle_

### curriculum — 4EME / Sections_Solides (row 59, exo 7)
- **Q**: On coupe une sphère par un plan quelconque. La section obtenue est toujours :
- **A**: Un cercle
- `WARN_HINT_IS_ANSWER` step 1: _Toute section d'une sphère par un plan est un cercle_

### curriculum — 4EME / Sections_Solides (row 59, exo 8)
- **Q**: La section d'un cylindre par un plan perpendiculaire à son axe est :
- **A**: Un cercle
- `WARN_HINT_IS_ANSWER` step 3: _La section est un cercle (disque)._

### curriculum — 4EME / Sections_Solides (row 59, exo 9)
- **Q**: La section d'un cône par un plan parallèle à la base est un cercle.
- **A**: Vrai
- `WARN_HINT_IS_ANSWER` step 3: _Vrai. C'est une réduction de la base._

### curriculum — 4EME / Sections_Solides (row 59, exo 10)
- **Q**: Complète : une sphère de rayon $5$ cm coupée à $3$ cm du centre donne un cercle 
- **A**: $4$
- `WARN_HINT_IS_FORMULA` step 2: _$r^2 = 5^2 - 3^2 = 25 - 9 = 16$._
- `WARN_HINT_IS_FORMULA` step 3: _$r = ?$ cm._

### curriculum — 4EME / Sections_Solides (row 59, exo 11)
- **Q**: La section d'un cube par un plan parallèle à une face est :
- **A**: Un carré
- `WARN_HINT_IS_ANSWER` step 3: _La section est un carré._

### curriculum — 4EME / Sections_Solides (row 59, exo 12)
- **Q**: Complète : la section d'une sphère par un plan est toujours un ___.
- **A**: cercle
- `WARN_HINT_IS_ANSWER` step 2: _Le rayon du cercle dépend de la distance du plan au centre._
- `WARN_HINT_IS_ANSWER` step 3: _Si le plan passe par le centre : grand cercle. Sinon : cercle plus petit._

### curriculum — 4EME / Sections_Solides (row 59, exo 14)
- **Q**: Une pyramide (base carrée $8$ cm, hauteur $12$ cm) coupée à $4$ cm du sommet don
- **A**: Vrai
- `WARN_HINT_IS_ANSWER` step 3: _Vrai._
- `WARN_HINT_IS_FORMULA` step 1: _$k = \frac{4}{12} = \frac{1}{3}$._
- `WARN_HINT_IS_FORMULA` step 2: _Côté section $= k \times 8 = \frac{8}{3}$ cm._
- `WARN_HINT_TOO_SHORT` step 3: _Vrai._

### curriculum — 4EME / Sections_Solides (row 59, exo 15)
- **Q**: Complète : une pyramide (base $4 \times 3$ cm) coupée à mi-hauteur depuis la bas
- **A**: $3$
- `WARN_HINT_IS_FORMULA` step 1: _À mi-hauteur depuis la base $= $ mi-hauteur depuis le sommet, $k = \frac{1}{2}$._
- `WARN_HINT_IS_FORMULA` step 2: _Aire section $= k^2 \times$ aire base $= \frac{1}{4} \times 12 = ?$ cm$^2$._

### curriculum — 4EME / Sections_Solides (row 59, exo 17)
- **Q**: On coupe un cylindre de révolution (rayon 3 cm, hauteur 10 cm) par un plan incli
- **A**: Une ellipse
- `WARN_HINT_IS_ANSWER` step 1: _Un plan oblique courant un cylindre donne une ellipse_
- `WARN_HINT_IS_ANSWER` step 3: _La section est une ellipse_

### curriculum — 4EME / Sections_Solides (row 59, exo 19)
- **Q**: La section d'un cube par un plan passant par les milieux de $3$ arêtes issues d'
- **A**: Vrai
- `WARN_HINT_IS_ANSWER` step 3: _Vrai. La symétrie du cube garantit un triangle équilatéral._

### curriculum — 4EME / Sections_Solides (row 59, exo 20)
- **Q**: Complète : une pyramide (base carrée $10$ cm, hauteur $15$ cm) a une section de 
- **A**: $6$
- `WARN_HINT_IS_FORMULA` step 1: _$k = \frac{4}{10} = \frac{2}{5}$._
- `WARN_HINT_IS_FORMULA` step 2: _Distance au sommet $= k \times H = \frac{2}{5} \times 15 = ?$ cm._

### curriculum — 3EME / Statistiques_Brevet (row 60, exo 2)
- **Q**: Quelle est la moyenne pondérée de Samir ?
- **A**: $13{,}3$
- `WARN_HINT_IS_FORMULA` step 1: _Calcule la somme pondérée : $13 \times 3 + 16 \times 3 + 10 \times 2 + 14 \times 1 + 12 \times 1 = 3_
- `WARN_HINT_IS_FORMULA` step 2: _Divise par la somme des coefficients : $\frac{133}{10} = $ ?_

### curriculum — 3EME / Statistiques_Brevet (row 60, exo 4)
- **Q**: Samir repasse son épreuve d'histoire et obtient $14$ au lieu de $10$. Calcule sa
- **A**: 14,1
- `WARN_HINT_IS_FORMULA` step 1: _Nouvelle somme pondérée : remplace $10 \times 2 = 20$ par $14 \times 2 = 28$. Ancienne somme $= 133$_
- `WARN_HINT_IS_FORMULA` step 2: _Nouvelle moyenne : $\frac{141}{10} = $ ?_

### curriculum — 3EME / Statistiques_Brevet (row 60, exo 8)
- **Q**: « La médiane de cette série est $12{,}5$ minutes. »
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 2: _Effectifs cumulés : $2$, $5$, $10$, $14\ldots$ La $10$ème valeur est $12$ et la $11$ème est $13$. Ca_

### curriculum — 3EME / Statistiques_Brevet (row 60, exo 9)
- **Q**: Calcule la moyenne des temps de course (arrondie au dixième). ___
- **A**: 12,6
- `WARN_HINT_IS_FORMULA` step 1: _Somme pondérée : $10 \times 2 + 11 \times 3 + 12 \times 5 + 13 \times 4 + 14 \times 3 + 15 \times 3 _
- `WARN_HINT_IS_FORMULA` step 2: _Moyenne : $\frac{252}{20} = $ ?_

### curriculum — 3EME / Statistiques_Brevet (row 60, exo 10)
- **Q**: Un $21$ème élève, absent le jour du cross, le court une semaine plus tard et ter
- **A**: $13$ min
- `WARN_HINT_IS_FORMULA` step 1: _Avec $21$ valeurs (impair), la médiane est la valeur en position $\frac{21+1}{2} = 11$._

### curriculum — 3EME / Statistiques_Brevet (row 60, exo 11)
- **Q**: Combien d'employés gagnent $1800$ € ou moins par mois ? ___
- **A**: 12
- `WARN_HINT_IS_ANSWER` step 1: _Repère les salaires inférieurs ou égaux à $1800$ € : $1200$ €, $1500$ € et $1800$ €._

### curriculum — 3EME / Statistiques_Brevet (row 60, exo 12)
- **Q**: Quelle est la médiane des salaires ?
- **A**: $1800$ €
- `WARN_HINT_IS_ANSWER` step 2: _Effectifs cumulés : $2$, $6$, $12\ldots$ Les $10$ème et $11$ème valeurs sont toutes les deux à $1800_

### curriculum — 3EME / Statistiques_Brevet (row 60, exo 13)
- **Q**: Calcule l'écart interquartile $Q_3 - Q_1$. ___
- **A**: 600
- `WARN_HINT_IS_FORMULA` step 1: _Sous-série inférieure (positions $1$ à $10$) : effectifs cumulés $2$, $6$, $12$. $Q_1 = \frac{\text{_
- `WARN_HINT_IS_FORMULA` step 2: _Sous-série supérieure (positions $11$ à $20$) : positions $15$ et $16$ → $Q_3 = \frac{2100 + 2100}{2_
- `WARN_HINT_IS_FORMULA` step 3: _$Q_3 - Q_1 = 2100 - 1500 = $ ?_

### curriculum — 3EME / Statistiques_Brevet (row 60, exo 15)
- **Q**: « La moyenne des salaires ($1980$ €) est supérieure à la médiane ($1800$ €). Cel
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _Calcule la moyenne : $\frac{2 \times 1200 + 4 \times 1500 + 6 \times 1800 + 4 \times 2100 + 2 \times_

### curriculum — 3EME / Statistiques_Brevet (row 60, exo 16)
- **Q**: Calcule la moyenne de la classe A. ___
- **A**: 12
- `WARN_HINT_IS_ANSWER` step 1: _Somme pondérée : $8 \times 2 + 10 \times 4 + 12 \times 8 + 14 \times 4 + 16 \times 2 = 16 + 40 + 96 _
- `WARN_HINT_IS_FORMULA` step 1: _Somme pondérée : $8 \times 2 + 10 \times 4 + 12 \times 8 + 14 \times 4 + 16 \times 2 = 16 + 40 + 96 _
- `WARN_HINT_IS_FORMULA` step 2: _Moyenne : $\frac{240}{20} = $ ?_

### curriculum — 3EME / Statistiques_Brevet (row 60, exo 17)
- **Q**: Quelle est la moyenne de la classe C ?
- **A**: $12$
- `WARN_HINT_IS_ANSWER` step 1: _Somme pondérée : $4 \times 2 + 8 \times 4 + 12 \times 8 + 16 \times 4 + 20 \times 2 = 8 + 32 + 96 + _
- `WARN_HINT_IS_FORMULA` step 1: _Somme pondérée : $4 \times 2 + 8 \times 4 + 12 \times 8 + 16 \times 4 + 20 \times 2 = 8 + 32 + 96 + _
- `WARN_HINT_IS_FORMULA` step 2: _Moyenne : $\frac{240}{20} = $ ?_

### curriculum — 3EME / Statistiques_Brevet (row 60, exo 19)
- **Q**: Calcule l'écart interquartile de la classe C. ___
- **A**: 8
- `WARN_HINT_IS_FORMULA` step 1: _Sous-série inférieure de C (positions $1$ à $10$) : cumuls $2$, $6$. Positions $5$ et $6$ = $8$. Don_
- `WARN_HINT_IS_FORMULA` step 2: _Sous-série supérieure (positions $11$ à $20$) : positions $15$ et $16$ = $16$. Donc $Q_3 = 16$._
- `WARN_HINT_IS_FORMULA` step 3: _$Q_3 - Q_1 = 16 - 8 = $ ?_

### curriculum — 3EME / Statistiques_Brevet (row 60, exo 20)
- **Q**: Les deux classes ont la même moyenne et la même médiane. Quelle classe a les rés
- **A**: Classe A
- `WARN_HINT_IS_ANSWER` step 1: _L'écart interquartile de la classe A : $Q_1 = 10$, $Q_3 = 14$, IQR $= 4$. Celui de la classe C : IQR_
- `WARN_HINT_IS_ANSWER` step 2: _Un IQR plus petit signifie que les $50\%$ centraux sont plus resserrés autour de la médiane. Quelle _
- `WARN_HINT_IS_FORMULA` step 1: _L'écart interquartile de la classe A : $Q_1 = 10$, $Q_3 = 14$, IQR $= 4$. Celui de la classe C : IQR_

### curriculum — 3EME / Thales_Brevet (row 61, exo 1)
- **Q**: Calcule le rapport $\frac{BM}{BH}$. Donne le résultat sous forme de fraction irr
- **A**: 1/6
- `WARN_HINT_IS_FORMULA` step 1: _On lit sur la figure : $BM = 3$ m et $BH = 18$ m._
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{BM}{BH} = \frac{3}{18}$. Simplifie par le PGCD de $3$ et $18$ — quel est-il ?_

### curriculum — 3EME / Thales_Brevet (row 61, exo 2)
- **Q**: Quelle égalité de rapports permet d'appliquer le théorème de Thalès dans cette c
- **A**: $\frac{BM}{BH} = \frac{MN}{AH}$
- `WARN_HINT_IS_FORMULA` step 2: _Le théorème de Thalès donne $\frac{BM}{BH} = \frac{BN}{BA} = \frac{?}{?}$. Quels segments correspond_

### curriculum — 3EME / Thales_Brevet (row 61, exo 3)
- **Q**: Calcule la hauteur $AH$ du clocher en mètres.
- **A**: 12
- `WARN_HINT_IS_FORMULA` step 1: _D'après Thalès : $\frac{MN}{AH} = \frac{BM}{BH}$, soit $\frac{2}{AH} = \frac{3}{18}$._
- `WARN_HINT_IS_FORMULA` step 2: _Donc $AH = \frac{2 \times 18}{3} = \frac{?}{3} = \;?$ m._

### curriculum — 3EME / Thales_Brevet (row 61, exo 4)
- **Q**: Si l'ombre du poteau mesurait $6$ m au lieu de $3$ m (le poteau gardant la même 
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 1: _Avec $BM = 6$ m : $\frac{MN}{AH} = \frac{BM}{BH}$ donne $\frac{2}{AH} = \frac{6}{18}$._

### curriculum — 3EME / Thales_Brevet (row 61, exo 5)
- **Q**: Un arbre de $8$ m de haut se trouve à côté du clocher. Quelle est la longueur de
- **A**: $12$ m
- `WARN_HINT_IS_FORMULA` step 2: _Pour le poteau : $\frac{\text{ombre}}{\text{hauteur}} = \frac{3}{2}$. Pour l'arbre : $\frac{x}{8} = _

### curriculum — 3EME / Thales_Brevet (row 61, exo 6)
- **Q**: Calcule la longueur $OD$.
- **A**: 4,5
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{OA}{OC} = \frac{OB}{OD}$ donne $\frac{4}{3} = \frac{6}{OD}$, donc $OD = \frac{6 \times 3}{4} _

### curriculum — 3EME / Thales_Brevet (row 61, exo 7)
- **Q**: Calcule la longueur $CD$.
- **A**: $6$ cm
- `WARN_HINT_IS_FORMULA` step 1: _On utilise la 3ème égalité de Thalès : $\frac{AB}{CD} = \frac{OA}{OC}$._
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{8}{CD} = \frac{4}{3}$, donc $CD = \frac{8 \times 3}{4} = \;?$_

### curriculum — 3EME / Thales_Brevet (row 61, exo 8)
- **Q**: Le triangle $OCD$ est une réduction du triangle $OAB$.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _Le rapport de réduction est $\frac{OC}{OA} = \frac{3}{4}$. Vérifie que $\frac{OD}{OB}$ donne le même_
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{OD}{OB} = \frac{4{,}5}{6} = \;?$. Ce rapport est-il égal à $\frac{3}{4}$ ?_

### curriculum — 3EME / Thales_Brevet (row 61, exo 9)
- **Q**: L'échelle de la maquette est $\frac{1}{20}$. Si $AB = 8$ cm sur la maquette, que
- **A**: 160
- `WARN_HINT_IS_FORMULA` step 1: _Échelle = $\frac{\text{maquette}}{\text{réel}}$, soit $\frac{1}{20} = \frac{8}{\text{réel}}$._
- `WARN_HINT_IS_FORMULA` step 2: _Longueur réelle $= 8 \times 20 = \;?$ cm._

### curriculum — 3EME / Thales_Brevet (row 61, exo 10)
- **Q**: Si le rapport d'agrandissement du triangle $OAB$ par rapport au triangle $OCD$ e
- **A**: $\frac{16}{9}$
- `WARN_HINT_IS_FORMULA` step 2: _$k = \frac{4}{3}$, donc $k^2 = \left(\frac{4}{3}\right)^2 = \;?$_

### curriculum — 3EME / Thales_Brevet (row 61, exo 11)
- **Q**: Calcule la longueur $DE$.
- **A**: 6
- `WARN_HINT_IS_FORMULA` step 1: _$G$ est sur le segment $[DE]$, donc $DE = DG + GE$._
- `WARN_HINT_IS_FORMULA` step 2: _$DE = 4{,}5 + 1{,}5 = \;?$ m._

### curriculum — 3EME / Thales_Brevet (row 61, exo 12)
- **Q**: Calcule le rapport $\frac{DG}{DE}$.
- **A**: $\frac{3}{4}$
- `WARN_HINT_IS_FORMULA` step 1: _$DG = 4{,}5$ m et $DE = 6$ m._
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{DG}{DE} = \frac{4{,}5}{6}$. Multiplie numérateur et dénominateur par $2$ pour supprimer la vi_

### curriculum — 3EME / Thales_Brevet (row 61, exo 13)
- **Q**: Les droites $(GH)$ et $(EF)$ sont-elles parallèles ? Justifie à l'aide de la réc
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _Calcule $\frac{DH}{DF}$ : $DF = DH + HF = 6 + 2 = 8$ m, donc $\frac{DH}{DF} = \frac{6}{8} = \frac{3}_

### curriculum — 3EME / Thales_Brevet (row 61, exo 14)
- **Q**: Samir modifie son plan : il déplace $H$ pour que $DH = 5$ m (et $HF = 3$ m), en 
- **A**: Non, car $\frac{DG}{DE} \neq \frac{DH}{D
- `WARN_HINT_IS_FORMULA` step 1: _$\frac{DG}{DE} = \frac{4{,}5}{6} = \frac{3}{4} = 0{,}75$. Calcule $\frac{DH}{DF} = \frac{5}{8} = \;?_

### curriculum — 3EME / Thales_Brevet (row 61, exo 15)
- **Q**: Dans la configuration initiale (où $(GH) \parallel (EF)$), on sait que $GH = 9$ 
- **A**: 12
- `WARN_HINT_IS_FORMULA` step 1: _$(GH) \parallel (EF)$ avec $\frac{DG}{DE} = \frac{3}{4}$. D'après Thalès : $\frac{GH}{EF} = \frac{DG_
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{9}{EF} = \frac{3}{4}$, donc $EF = \frac{9 \times 4}{3} = \;?$ m._

### curriculum — 3EME / Thales_Brevet (row 61, exo 16)
- **Q**: Calcule la distance $EH$ entre l'oeil de Noa et le pied du phare.
- **A**: 42
- `WARN_HINT_IS_FORMULA` step 1: _$E$, $C$ et $H$ sont alignés sur le sol. $EH = EC + CH$._
- `WARN_HINT_IS_FORMULA` step 2: _$EH = 2 + 40 = \;?$ m._

### curriculum — 3EME / Thales_Brevet (row 61, exo 17)
- **Q**: En appliquant le théorème de Thalès dans le triangle $EPH$, quelle est la hauteu
- **A**: $31{,}5$ m
- `WARN_HINT_IS_FORMULA` step 1: _$(CD) \parallel (PH)$, sécantes issues de $E$. Thalès : $\frac{EC}{EH} = \frac{CD}{PH}$._
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{2}{42} = \frac{1{,}5}{PH}$, donc $PH = \frac{1{,}5 \times 42}{2} = \frac{63}{2} = \;?$_

### curriculum — 3EME / Thales_Brevet (row 61, exo 18)
- **Q**: Le rapport $\frac{EC}{EH} = \frac{2}{42}$ est aussi égal au rapport $\frac{CD}{P
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _$\frac{2}{42} = \frac{1}{21}$ après simplification par $2$._
- `WARN_HINT_IS_FORMULA` step 2: _Vérifie : $\frac{CD}{PH} = \frac{1{,}5}{31{,}5}$. Simplifie cette fraction — retrouves-tu $\frac{1}{_

### curriculum — 3EME / Thales_Brevet (row 61, exo 19)
- **Q**: Noa déplace le piquet à $10$ m du pied du phare (au lieu de $40$ m). Elle reste 
- **A**: 5,25
- `WARN_HINT_IS_FORMULA` step 1: _Nouvelle configuration : $EC' = 2$ m, $C'H = 10$ m, donc $E'H = 12$ m. Thalès : $\frac{EC'}{E'H} = \_
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{2}{12} = \frac{CD'}{31{,}5}$, donc $CD' = \frac{2 \times 31{,}5}{12} = \frac{63}{12} = \;?$_

### curriculum — 3EME / Thales_Brevet (row 61, exo 20)
- **Q**: Le phare a une base carrée de côté $4$ m. La maquette du phare est à l'échelle $
- **A**: $363$ cm$^2$
- `WARN_HINT_IS_FORMULA` step 1: _Côté réel = $4$ m = $400$ cm. Côté maquette = $\frac{400}{21} \approx 19{,}05$ cm._

### curriculum — 3EME / Transformations_Brevet (row 62, exo 1)
- **Q**: Quel est l'abscisse de l'image $A'$ de $A$ par la translation de vecteur $\vec{u
- **A**: 6
- `WARN_HINT_IS_FORMULA` step 2: _$x_{A'} = x_A + 4 = 2 + 4 = $ ?_

### curriculum — 3EME / Transformations_Brevet (row 62, exo 2)
- **Q**: Quelles sont les coordonnées complètes de $A'$, image de $A(2 ; 3)$ par la trans
- **A**: $(6 ; 2)$
- `WARN_HINT_IS_FORMULA` step 1: _On applique la formule pour chaque coordonnée : $x_{A'} = x_A + a$ et $y_{A'} = y_A + b$._
- `WARN_HINT_IS_FORMULA` step 2: _$x_{A'} = 2 + 4 = 6$ et $y_{A'} = 3 + (-1) = $ ?_

### curriculum — 3EME / Transformations_Brevet (row 62, exo 4)
- **Q**: Pixel est maintenant en $B(5 ; 1)$. Après une translation, il arrive en $B'(1 ; 
- **A**: $\vec{v}(-4 ; 3)$
- `WARN_HINT_IS_FORMULA` step 2: _$x_v = 1 - 5 = -4$ et $y_v = 4 - 1 = $ ?_

### curriculum — 3EME / Transformations_Brevet (row 62, exo 5)
- **Q**: On applique la translation de vecteur $\vec{u}(4 ; -1)$ au segment $[AC]$ avec $
- **A**: 2
- `WARN_HINT_IS_FORMULA` step 2: _Donc $A'C' = AC = $ ? unités._

### curriculum — 3EME / Transformations_Brevet (row 62, exo 6)
- **Q**: Le siège $A$ subit une rotation de centre $O$ et d'angle $90°$ dans le sens anti
- **A**: 3
- `WARN_HINT_IS_FORMULA` step 2: _$OA' = OA = $ ? m._

### curriculum — 3EME / Transformations_Brevet (row 62, exo 8)
- **Q**: Une rotation de $360°$ ramène chaque point à sa position initiale.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 2: _Donc $A' = A$. Que peut-on en conclure ?_

### curriculum — 3EME / Transformations_Brevet (row 62, exo 9)
- **Q**: Un engrenage fait tourner la roue de $90°$ dans le sens horaire, puis de $90°$ d
- **A**: $0°$
- `WARN_HINT_IS_ANSWER` step 1: _La première rotation déplace de $+90°$ (horaire), la seconde de $-90°$ (anti-horaire)._
- `WARN_HINT_IS_ANSWER` step 2: _$90° - 90° = $ ? La roue revient à sa position initiale._

### curriculum — 3EME / Transformations_Brevet (row 62, exo 10)
- **Q**: Le point $A(3 ; 0)$ subit une rotation de centre $O(0 ; 0)$ et d'angle $90°$ dan
- **A**: $(0 ; 3)$
- `WARN_HINT_IS_ANSWER` step 3: _$A'(0 ; 3)$._
- `WARN_HINT_IS_FORMULA` step 2: _Pour $A(3 ; 0)$ : $x_{A'} = -0 = 0$ et $y_{A'} = 3$. Donc $A' = $ ?_

### curriculum — 3EME / Transformations_Brevet (row 62, exo 11)
- **Q**: Le photographe applique une homothétie de centre $O(0 ; 0)$ et de rapport $k = 2
- **A**: $(4 ; 2)$
- `WARN_HINT_IS_FORMULA` step 2: _$x_{A'} = 2 \times 2 = 4$ et $y_{A'} = 2 \times 1 = $ ?_

### curriculum — 3EME / Transformations_Brevet (row 62, exo 12)
- **Q**: Quelles sont les coordonnées de $C'$, image de $C(3 ; 3)$ par la même homothétie
- **A**: (6 ; 6)
- `WARN_HINT_IS_FORMULA` step 2: _$x_{C'} = 2 \times 3 = 6$ et $y_{C'} = 2 \times 3 = $ ?_

### curriculum — 3EME / Transformations_Brevet (row 62, exo 13)
- **Q**: Le côté $AB$ mesure $2$ unités. Après l'homothétie de rapport $k = 2$, le côté $
- **A**: 4
- `WARN_HINT_IS_FORMULA` step 2: _$A'B' = |k| \times AB = 2 \times 2 = $ ?_

### curriculum — 3EME / Transformations_Brevet (row 62, exo 14)
- **Q**: L'aire du triangle $ABC$ est $2$ unités d'aire. Quelle est l'aire du triangle $A
- **A**: $8$ unités d'aire
- `WARN_HINT_IS_FORMULA` step 2: _Aire$(A'B'C') = k^2 \times$ Aire$(ABC) = 2^2 \times 2 = 4 \times 2 = $ ?_

### curriculum — 3EME / Transformations_Brevet (row 62, exo 16)
- **Q**: L'artiste translate le losange $ABCD$ par le vecteur $\vec{u}(4 ; 0)$. Quelles s
- **A**: $(6 ; 1)$
- `WARN_HINT_IS_FORMULA` step 2: _$x_{B'} = 2 + 4 = 6$ et $y_{B'} = 1 + 0 = $ ?_

### curriculum — 3EME / Transformations_Brevet (row 62, exo 17)
- **Q**: L'artiste applique une rotation de $180°$ de centre $C(4 ; 0)$ au point $A(0 ; 0
- **A**: (8 ; 0)
- `WARN_HINT_IS_FORMULA` step 2: _Les coordonnées du symétrique : $x_{A''} = 2 \times x_C - x_A = 2 \times 4 - 0 = 8$ et $y_{A''} = 2 _

### curriculum — 3EME / Transformations_Brevet (row 62, exo 19)
- **Q**: L'artiste applique une homothétie de centre $A(0 ; 0)$ et de rapport $k = \frac{
- **A**: $(2 ; 0)$
- `WARN_HINT_IS_FORMULA` step 2: _$x_{C'} = \frac{1}{2} \times 4 = 2$ et $y_{C'} = \frac{1}{2} \times 0 = $ ?_

### curriculum — 3EME / Trigonometrie_Brevet (row 63, exo 1)
- **Q**: Calcule la hauteur $PH$ du phare (arrondi au dixième).
- **A**: 63,8
- `WARN_HINT_IS_FORMULA` step 1: _On connaît le côté adjacent à l'angle ($BP = 120$ m) et on cherche le côté opposé ($PH$). Quel ratio_
- `WARN_HINT_IS_FORMULA` step 2: _$\tan(28°) = \frac{PH}{BP}$, donc $PH = 120 \times \tan(28°) = 120 \times 0{,}5317$._

### curriculum — 3EME / Trigonometrie_Brevet (row 63, exo 2)
- **Q**: Calcule la distance $BH$ entre le bateau et le sommet du phare (arrondi au dixiè
- **A**: 135,9
- `WARN_HINT_IS_FORMULA` step 1: _On connaît le côté adjacent ($BP = 120$ m) et on cherche l'hypoténuse ($BH$). Quel ratio relie adjac_
- `WARN_HINT_IS_FORMULA` step 2: _$\cos(28°) = \frac{BP}{BH}$, donc $BH = \frac{120}{\cos(28°)} = \frac{120}{0{,}8829}$._

### curriculum — 3EME / Trigonometrie_Brevet (row 63, exo 3)
- **Q**: Pour trouver $PH$ en connaissant $BP$ et l'angle $\widehat{PBH}$, quel ratio tri
- **A**: La tangente
- `WARN_HINT_IS_ANSWER` step 2: _$\tan(\alpha) = \frac{\text{opposé}}{\text{adjacent}}$. C'est bien la tangente qui convient ici._
- `WARN_HINT_IS_FORMULA` step 2: _$\tan(\alpha) = \frac{\text{opposé}}{\text{adjacent}}$. C'est bien la tangente qui convient ici._

### curriculum — 3EME / Trigonometrie_Brevet (row 63, exo 4)
- **Q**: Le bateau recule à $200$ m du phare. Quel est le nouvel angle d'élévation $\wide
- **A**: $18°$
- `WARN_HINT_IS_FORMULA` step 1: _La hauteur du phare ne change pas : $PH \approx 63{,}8$ m. La nouvelle distance est $BP = 200$ m._
- `WARN_HINT_IS_FORMULA` step 2: _$\tan(\widehat{PBH}) = \frac{63{,}8}{200} = 0{,}319$, donc $\widehat{PBH} = \arctan(0{,}319)$._

### curriculum — 3EME / Trigonometrie_Brevet (row 63, exo 5)
- **Q**: En doublant la distance bateau-phare (de $120$ m à $240$ m), l'angle d'élévation
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 2: _À $240$ m : $\tan(\alpha) = \frac{63{,}8}{240} = 0{,}266$, donc $\alpha = \arctan(0{,}266) \approx 1_

### curriculum — 3EME / Trigonometrie_Brevet (row 63, exo 6)
- **Q**: Calcule l'angle $\alpha$ de la rampe avec le sol (arrondi au degré).
- **A**: 8
- `WARN_HINT_IS_FORMULA` step 1: _On connaît le côté opposé à $\alpha$ ($BC = 1{,}4$ m) et l'hypoténuse ($AC = 10$ m). Quel ratio util_
- `WARN_HINT_IS_FORMULA` step 2: _$\sin(\alpha) = \frac{BC}{AC} = \frac{1{,}4}{10} = 0{,}14$, donc $\alpha = \arcsin(0{,}14)$._

### curriculum — 3EME / Trigonometrie_Brevet (row 63, exo 8)
- **Q**: Quelle longueur minimale de rampe faudrait-il pour respecter la norme avec la mê
- **A**: 16,1
- `WARN_HINT_IS_FORMULA` step 1: _On veut $\alpha = 5°$ (angle maximal autorisé) avec $BC = 1{,}4$ m. On cherche la longueur de la ram_
- `WARN_HINT_IS_FORMULA` step 2: _$\sin(5°) = \frac{1{,}4}{AC}$, donc $AC = \frac{1{,}4}{\sin(5°)} = \frac{1{,}4}{0{,}0872}$._

### curriculum — 3EME / Trigonometrie_Brevet (row 63, exo 9)
- **Q**: Quelle est la longueur de la base horizontale $AB$ de la rampe actuelle (arrondi
- **A**: $9{,}9$ m
- `WARN_HINT_IS_FORMULA` step 1: _On connaît $AC = 10$ m et $BC = 1{,}4$ m. On peut utiliser le théorème de Pythagore ou le cosinus._
- `WARN_HINT_IS_FORMULA` step 2: _$AB = AC \times \cos(\alpha) = 10 \times \cos(8°) = 10 \times 0{,}9903$._

### curriculum — 3EME / Trigonometrie_Brevet (row 63, exo 10)
- **Q**: Le côté adjacent à l'angle $\alpha$ dans ce triangle est la rampe de $10$ m.
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 1: _La rampe ($AC = 10$ m) est le côté le plus long du triangle rectangle : c'est l'hypoténuse._

### curriculum — 3EME / Trigonometrie_Brevet (row 63, exo 11)
- **Q**: Calcule le dénivelé $BC$ de cette première portion (arrondi au dixième de km).
- **A**: 0,6
- `WARN_HINT_IS_FORMULA` step 1: _$BC$ est le côté opposé à l'angle de $18°$ et $AC = 2$ km est l'hypoténuse. Quel ratio utiliser ?_
- `WARN_HINT_IS_FORMULA` step 2: _$\sin(18°) = \frac{BC}{AC}$, donc $BC = 2 \times \sin(18°) = 2 \times 0{,}3090$._

### curriculum — 3EME / Trigonometrie_Brevet (row 63, exo 12)
- **Q**: Quelle est la distance horizontale $AB$ parcourue (arrondi au dixième de km) ?
- **A**: $1{,}9$ km
- `WARN_HINT_IS_FORMULA` step 1: _$AB$ est le côté adjacent à l'angle de $18°$ et $AC = 2$ km est l'hypoténuse._
- `WARN_HINT_IS_FORMULA` step 2: _$\cos(18°) = \frac{AB}{AC}$, donc $AB = 2 \times \cos(18°) = 2 \times 0{,}9511$._

### curriculum — 3EME / Trigonometrie_Brevet (row 63, exo 13)
- **Q**: Une deuxième portion du sentier couvre $1{,}5$ km à l'horizontale et $600$ m de 
- **A**: 22
- `WARN_HINT_IS_FORMULA` step 2: _$\tan(\beta) = \frac{0{,}6}{1{,}5} = 0{,}4$, donc $\beta = \arctan(0{,}4)$._

### curriculum — 3EME / Trigonometrie_Brevet (row 63, exo 16)
- **Q**: Calcule la distance au sol $PA$ entre la projection du drone et le point $A$ (ar
- **A**: 56,0
- `WARN_HINT_IS_FORMULA` step 1: _Dans le triangle $DPA$ rectangle en $P$, l'angle $\widehat{PDA} = 35°$. Le côté adjacent est $DP = 8_
- `WARN_HINT_IS_FORMULA` step 2: _$\tan(35°) = \frac{PA}{DP}$, donc $PA = 80 \times \tan(35°) = 80 \times 0{,}7002$._

### curriculum — 3EME / Trigonometrie_Brevet (row 63, exo 17)
- **Q**: Quelle est la distance $DA$ entre le drone et le point $A$ (arrondi au dixième) 
- **A**: $97{,}7$ m
- `WARN_HINT_IS_FORMULA` step 1: _On connaît le côté adjacent $DP = 80$ m et on cherche l'hypoténuse $DA$._
- `WARN_HINT_IS_FORMULA` step 2: _$\cos(35°) = \frac{DP}{DA}$, donc $DA = \frac{80}{\cos(35°)} = \frac{80}{0{,}8192}$._

### curriculum — 3EME / Trigonometrie_Brevet (row 63, exo 18)
- **Q**: Le drone repère un second point $B$ au sol. La distance $DB = 110$ m. Calcule l'
- **A**: 43
- `WARN_HINT_IS_FORMULA` step 1: _On connaît le côté adjacent $DP = 80$ m et l'hypoténuse $DB = 110$ m._
- `WARN_HINT_IS_FORMULA` step 2: _$\cos(\widehat{PDB}) = \frac{DP}{DB} = \frac{80}{110} \approx 0{,}7273$._
- `WARN_HINT_IS_FORMULA` step 3: _$\widehat{PDB} = \arccos(0{,}7273) \approx\;?°$._

### curriculum — 3EME / Trigonometrie_Brevet (row 63, exo 19)
- **Q**: On vérifie $DA$ par le théorème de Pythagore : $DA = \sqrt{DP^2 + PA^2}$. Quel r
- **A**: $97{,}7$ m
- `WARN_HINT_IS_FORMULA` step 1: _$DA = \sqrt{80^2 + 56{,}0^2} = \sqrt{6400 + 3136}$._
- `WARN_HINT_IS_FORMULA` step 2: _$DA = \sqrt{9536} \approx\;?$ m._

### curriculum — 3EME / Trigonometrie_Brevet (row 63, exo 20)
- **Q**: On peut retrouver la distance $DA$ aussi bien par le théorème de Pythagore que p
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _Par trigonométrie : $DA = \frac{80}{\cos(35°)} \approx 97{,}7$ m._
- `WARN_HINT_IS_FORMULA` step 2: _Par Pythagore : $DA = \sqrt{80^2 + 56^2} = \sqrt{9536} \approx 97{,}7$ m._

### curriculum — 4EME / Proportionnalité (row 64, exo 3)
- **Q**: Sur une carte routière à l'échelle $1:50\,000$, la distance entre deux villages 
- **A**: $1{,}5$ km
- `WARN_HINT_IS_FORMULA` step 1: _$3$ cm sur la carte $= 3 \times 50\,000 = 150\,000$ cm réels._

### curriculum — 4EME / Proportionnalité (row 64, exo 4)
- **Q**: De $120$ € à $150$ €, le taux d'augmentation est $25\%$.
- **A**: Vrai
- `WARN_HINT_IS_ANSWER` step 3: _Vrai._
- `WARN_HINT_IS_FORMULA` step 2: _Taux : $\frac{30}{120} \times 100 = 25\%$._
- `WARN_HINT_TOO_SHORT` step 3: _Vrai._

### curriculum — 4EME / Proportionnalité (row 64, exo 5)
- **Q**: Complète : la lumière ($3 \times 10^5$ km/s) met ___ secondes pour parcourir $1{
- **A**: $500$
- `WARN_HINT_IS_FORMULA` step 1: _$t = \frac{d}{v} = \frac{1{,}5 \times 10^8}{3 \times 10^5}$._
- `WARN_HINT_IS_FORMULA` step 2: _$= \frac{1{,}5}{3} \times 10^{8-5} = 0{,}5 \times 10^3$._

### curriculum — 4EME / Proportionnalité (row 64, exo 8)
- **Q**: Si deux grandeurs sont inversement proportionnelles et que l'une double, l'autre
- **A**: Est divisée par $2$
- `WARN_HINT_IS_FORMULA` step 1: _Inversement proportionnel : $x \times y = k$ constant._

### curriculum — 4EME / Proportionnalité (row 64, exo 9)
- **Q**: À $60$ km/h pendant $3$ h, la distance parcourue est $180$ km.
- **A**: Vrai
- `WARN_HINT_IS_ANSWER` step 3: _Vrai._
- `WARN_HINT_IS_FORMULA` step 1: _$d = v \times t = 60 \times 3 = 180$ km._
- `WARN_HINT_TOO_SHORT` step 3: _Vrai._

### curriculum — 4EME / Proportionnalité (row 64, exo 10)
- **Q**: Complète : $25$ km aller à $20$ km/h, $25$ km retour à $30$ km/h. Vitesse moyenn
- **A**: $24$
- `WARN_HINT_IS_FORMULA` step 1: _Temps aller : $\frac{25}{20} = 1{,}25$ h. Temps retour : $\frac{25}{30} \approx 0{,}833$ h._
- `WARN_HINT_IS_FORMULA` step 3: _$v = \frac{50}{2{,}083} = ?$ km/h._

### curriculum — 4EME / Proportionnalité (row 64, exo 11)
- **Q**: La représentation graphique d'une situation de proportionnalité est :
- **A**: Une droite passant par l'origine
- `WARN_HINT_IS_FORMULA` step 1: _Proportionnalité : $y = kx$._

### curriculum — 4EME / Proportionnalité (row 64, exo 12)
- **Q**: Un élève calcule 20% de hausse puis 20% de baisse et dit qu'on revient au prix i
- **A**: On ne revient pas au prix initial :$1{,}
- `WARN_HINT_IS_FORMULA` step 2: _$1{,}2 \times 0{,}8 = 0{,}96$._

### curriculum — 4EME / Proportionnalité (row 64, exo 13)
- **Q**: Complète : si 8 ouvriers mettent 6 jours, alors 12 ouvriers mettent ___ jours.
- **A**: 4
- `WARN_HINT_IS_FORMULA` step 2: _$8 \times 6 = 48$ jours-ouvriers au total._
- `WARN_HINT_IS_FORMULA` step 3: _$48 \div 12 = ?$ jours._

### curriculum — 4EME / Proportionnalité (row 64, exo 14)
- **Q**: Un article augmenté de $20\%$ puis soldé de $20\%$ revient à son prix initial.
- **A**: Faux
- `WARN_HINT_IS_ANSWER` step 3: _Faux. Les pourcentages ne se compensent pas._
- `WARN_HINT_IS_FORMULA` step 1: _$100 \times 1{,}2 = 120$. Puis $120 \times 0{,}8 = 96$._

### curriculum — 4EME / Proportionnalité (row 64, exo 15)
- **Q**: Complète : un robinet remplit une cuve en $4$ h, un autre en $6$ h. Ensemble, il
- **A**: $2$ h $24$ min
- `WARN_HINT_IS_FORMULA` step 2: _Ensemble : $\frac{1}{4} + \frac{1}{6} = \frac{5}{12}$ cuve/h._

### curriculum — 4EME / Proportionnalité (row 64, exo 19)
- **Q**: Deux démarques successives de $-30\%$ et $-20\%$ font une réduction totale de $5
- **A**: Faux
- `WARN_HINT_IS_ANSWER` step 3: _Faux. $-30\% - 20\% \neq -50\%$. C'est $-44\%$._
- `WARN_HINT_IS_FORMULA` step 1: _$100 \times 0{,}7 = 70$. Puis $70 \times 0{,}8 = 56$._

### curriculum — 4EME / Proportionnalité (row 64, exo 20)
- **Q**: Complète : un bien de $10\,000$ € perd $15\%$ par an. Sa valeur dans $2$ ans est
- **A**: $7\,225$
- `WARN_HINT_IS_FORMULA` step 2: _Après 2 ans : $10\,000 \times 0{,}85^2 = 10\,000 \times 0{,}7225$._

### curriculum — 4EME / Fractions (row 65, exo 2)
- **Q**: $\frac{6}{8}$ et $\frac{3}{4}$ représentent le même nombre.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{6 \div 2}{8 \div 2} = \frac{3}{4}$. C'est bien la même chose !_

### curriculum — 4EME / Fractions (row 65, exo 3)
- **Q**: Simplifie $\frac{10}{15}$ en fraction irréductible : ___
- **A**: $\frac{2}{3}$
- `WARN_HINT_IS_FORMULA` step 2: _5 divise les deux : $10 \div 5 = 2$ et $15 \div 5 = 3$._
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{10}{15} = \frac{?}{?}$_

### curriculum — 4EME / Fractions (row 65, exo 4)
- **Q**: Quelle fraction est la plus grande : $\frac{2}{3}$ ou $\frac{3}{5}$ ?
- **A**: $\frac{2}{3}$
- `WARN_HINT_IS_ANSWER` step 3: _$\frac{2}{3} = \frac{10}{15}$ et $\frac{3}{5} = \frac{9}{15}$. Qui est le plus grand ?_
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{2}{3} = \frac{10}{15}$ et $\frac{3}{5} = \frac{9}{15}$. Qui est le plus grand ?_

### curriculum — 4EME / Fractions (row 65, exo 8)
- **Q**: Léo mange $\frac{1}{8}$ de pizza au déjeuner, puis $\frac{3}{8}$ au dîner. Quell
- **A**: $\frac{1}{2}$
- `WARN_HINT_IS_ANSWER` step 3: _$\frac{4}{8} = \frac{1}{2}$. Léo a mangé la moitié !_
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{4}{8} = \frac{1}{2}$. Léo a mangé la moitié !_

### curriculum — 4EME / Fractions (row 65, exo 10)
- **Q**: Calcule et simplifie : $\frac{4}{11} + \frac{6}{11}$ = ___
- **A**: $\frac{10}{11}$
- `WARN_HINT_IS_ANSWER` step 3: _$\frac{10}{11}$ — peut-on simplifier ? 10 et 11 n'ont pas de diviseur commun. C'est déjà irréductibl_

### curriculum — 4EME / Fractions (row 65, exo 11)
- **Q**: Calcule $\frac{1}{2} + \frac{1}{4}$.
- **A**: $\frac{3}{4}$
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{1}{2} = \frac{2}{4}$. Maintenant : $\frac{2}{4} + \frac{1}{4} = ?$_

### curriculum — 4EME / Fractions (row 65, exo 12)
- **Q**: Calcule $\frac{1}{3} + \frac{1}{6}$.
- **A**: $\frac{1}{2}$
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{1}{3} = \frac{2}{6}$. Donc $\frac{2}{6} + \frac{1}{6} = \frac{3}{6}$. Simplifie !_

### curriculum — 4EME / Fractions (row 65, exo 13)
- **Q**: Calcule : $\frac{2}{3} + \frac{1}{4}$ = ___
- **A**: $\frac{11}{12}$
- `WARN_HINT_IS_FORMULA` step 1: _Dénominateur commun de 3 et 4 ? Ni l'un ni l'autre n'est multiple → on prend $3 \times 4 = 12$._
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{2}{3} = \frac{8}{12}$ et $\frac{1}{4} = \frac{3}{12}$._
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{8}{12} + \frac{3}{12} = ?$_

### curriculum — 4EME / Fractions (row 65, exo 14)
- **Q**: La playlist de Léo c'est $\frac{1}{3}$ de rap et $\frac{1}{4}$ de pop. Quelle fr
- **A**: $\frac{7}{12}$
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{1}{3} = \frac{4}{12}$ et $\frac{1}{4} = \frac{3}{12}$. Additionne !_

### curriculum — 4EME / Fractions (row 65, exo 16)
- **Q**: Calcule $\frac{5}{6} - \frac{1}{6}$.
- **A**: $\frac{2}{3}$
- `WARN_HINT_IS_ANSWER` step 3: _Peut-on simplifier ? $\frac{4}{6} = \frac{2}{3}$._
- `WARN_HINT_IS_FORMULA` step 3: _Peut-on simplifier ? $\frac{4}{6} = \frac{2}{3}$._

### curriculum — 4EME / Fractions (row 65, exo 17)
- **Q**: Calcule : $\frac{3}{4} - \frac{1}{3}$ = ___
- **A**: $\frac{5}{12}$
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{3}{4} = \frac{9}{12}$ et $\frac{1}{3} = \frac{4}{12}$._
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{9}{12} - \frac{4}{12} = ?$_

### curriculum — 4EME / Fractions (row 65, exo 18)
- **Q**: Le téléphone de Léo est chargé à $\frac{4}{5}$. Après une partie de jeu, la batt
- **A**: $\frac{7}{15}$
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{4}{5} = \frac{12}{15}$ et $\frac{1}{3} = \frac{5}{15}$. Soustrais !_

### curriculum — 4EME / Fractions (row 65, exo 19)
- **Q**: Calcule $\frac{7}{10} - \frac{2}{5}$.
- **A**: $\frac{3}{10}$
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{2}{5} = \frac{4}{10}$._
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{7}{10} - \frac{4}{10} = ?$_

### curriculum — 4EME / Fractions (row 65, exo 21)
- **Q**: Calcule : $\frac{2}{5} + \frac{1}{10}$ = ___
- **A**: $\frac{1}{2}$
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{2}{5} = \frac{4}{10}$._
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{4}{10} + \frac{1}{10} = \frac{5}{10}$. Simplifie !_

### curriculum — 4EME / Fractions (row 65, exo 22)
- **Q**: Calcule $\frac{1}{2} + \frac{1}{3} - \frac{1}{6}$.
- **A**: $\frac{2}{3}$
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{1}{2} = \frac{3}{6}$, $\frac{1}{3} = \frac{2}{6}$, $\frac{1}{6} = \frac{1}{6}$._
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{3}{6} + \frac{2}{6} - \frac{1}{6} = \frac{4}{6}$. Simplifie !_

### curriculum — 4EME / Fractions (row 65, exo 23)
- **Q**: Pour une recette il faut $\frac{3}{4}$ L de lait. Léo n'a que $\frac{1}{2}$ L. C
- **A**: $\frac{1}{4}$ L
- `WARN_HINT_IS_FORMULA` step 2: _Dénominateur commun = 4. $\frac{1}{2} = \frac{2}{4}$._
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{3}{4} - \frac{2}{4} = ?$_

### curriculum — 4EME / Fractions (row 65, exo 24)
- **Q**: Calcule : $2 + \frac{3}{4}$ = ___
- **A**: $\frac{11}{4}$
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{8}{4} + \frac{3}{4} = ?$_

### curriculum — 4EME / Fractions (row 65, exo 25)
- **Q**: Un élève écrit : $\frac{2}{3} + \frac{5}{6} = \frac{7}{9}$. Où est son erreur ?
- **A**: Il a additionné les dénominateurs au lie
- `WARN_HINT_IS_FORMULA` step 3: _Le vrai calcul : $\frac{4}{6} + \frac{5}{6} = \frac{9}{6} = \frac{3}{2}$._

### curriculum — 4EME / Fractions (row 65, exo 26)
- **Q**: L'inverse de $\frac{3}{5}$ est $\frac{5}{3}$.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 2: _Vérification : $\frac{3}{5} \times \frac{5}{3} = \frac{15}{15} = 1$. ✓_

### curriculum — 4EME / Fractions (row 65, exo 27)
- **Q**: Calcule $\frac{2}{3} \div \frac{4}{5}$.
- **A**: $\frac{5}{6}$
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{2}{3} \times \frac{5}{4} = \frac{10}{12}$. Simplifie !_

### curriculum — 4EME / Fractions (row 65, exo 28)
- **Q**: Calcule : $\frac{3}{4} \div 2$ = ___
- **A**: $\frac{3}{8}$
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{3}{4} \times \frac{1}{2} = ?$_

### curriculum — 4EME / Fractions (row 65, exo 29)
- **Q**: Léo partage $\frac{3}{5}$ d'un gâteau entre ses 3 potes. Chacun reçoit combien ?
- **A**: $\frac{1}{5}$
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{3}{5} \div 3 = \frac{3}{5} \times \frac{1}{3} = \frac{3}{15}$._

### curriculum — 4EME / Fractions (row 65, exo 30)
- **Q**: Diviser par $\frac{1}{2}$ revient à multiplier par 2.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _L'inverse de $\frac{1}{2}$ est $\frac{2}{1} = 2$._
- `WARN_HINT_IS_FORMULA` step 3: _Exemple : $6 \div \frac{1}{2} = 6 \times 2 = 12$. C'est logique : dans 6, il y a 12 moitiés !_

### curriculum — 4EME / Fractions (row 65, exo 31)
- **Q**: Calcule $\frac{5}{6} \div \frac{1}{3}$.
- **A**: $\frac{5}{2}$
- `WARN_HINT_IS_FORMULA` step 1: _L'inverse de $\frac{1}{3}$ c'est $\frac{3}{1} = 3$._
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{5}{6} \times 3 = \frac{15}{6}$._
- `WARN_HINT_IS_FORMULA` step 3: _Simplifie : $\frac{15}{6} = ?$ (divise par 3)_

### curriculum — 4EME / Fractions (row 65, exo 32)
- **Q**: Calcule : $\frac{7}{8} \div \frac{7}{4}$ = ___
- **A**: $\frac{1}{2}$
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{7}{8} \times \frac{4}{7} = \frac{28}{56}$._
- `WARN_HINT_IS_FORMULA` step 3: _Astuce : les 7 se simplifient ! $\frac{7 \times 4}{8 \times 7} = \frac{4}{8} = ?$_

### curriculum — 4EME / Fractions (row 65, exo 33)
- **Q**: Léo découpe une planche de 3 m en morceaux de $\frac{3}{5}$ m. Combien de morcea
- **A**: $5$
- `WARN_HINT_IS_FORMULA` step 2: _$3 \div \frac{3}{5} = 3 \times \frac{5}{3} = \frac{15}{3}$._
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{15}{3} = ?$_

### curriculum — 4EME / Fractions (row 65, exo 34)
- **Q**: $\frac{a}{b} \div \frac{c}{d} = \frac{a \times c}{b \times d}$
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 3: _La vraie formule : $\frac{a}{b} \div \frac{c}{d} = \frac{a \times d}{b \times c}$, pas $\frac{a \tim_

### curriculum — 4EME / Fractions (row 65, exo 35)
- **Q**: Calcule : $\frac{1}{1 + \frac{1}{2}}$ = ___
- **A**: $\frac{2}{3}$
- `WARN_HINT_IS_ANSWER` step 3: _$1 \times \frac{2}{3} = ?$_
- `WARN_HINT_IS_FORMULA` step 1: _Commence par le dénominateur : $1 + \frac{1}{2} = \frac{2}{2} + \frac{1}{2} = \frac{3}{2}$._
- `WARN_HINT_IS_FORMULA` step 3: _$1 \times \frac{2}{3} = ?$_

### curriculum — 4EME / Fractions (row 65, exo 36)
- **Q**: $\frac{5}{8}$ des 32 élèves de la classe de Léo font du sport. Combien font du s
- **A**: $20$
- `WARN_HINT_IS_FORMULA` step 1: _$\frac{5}{8}$ de 32 = $\frac{5}{8} \times 32$._
- `WARN_HINT_IS_FORMULA` step 2: _Méthode rapide : $32 \div 8 = 4$, puis $4 \times 5 = ?$_

### curriculum — 4EME / Fractions (row 65, exo 37)
- **Q**: Calcule : $\frac{7}{12} - \frac{1}{4}$ = ___
- **A**: $\frac{1}{3}$
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{1}{4} = \frac{3}{12}$._
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{7}{12} - \frac{3}{12} = \frac{4}{12}$. Simplifie !_

### curriculum — 4EME / Fractions (row 65, exo 38)
- **Q**: Léo a $\frac{3}{4}$ L d'eau. Il boit $\frac{1}{3}$ de ce qu'il a. Combien lui re
- **A**: $\frac{1}{2}$ L
- `WARN_HINT_IS_FORMULA` step 1: _D'abord : combien il boit ? « $\frac{1}{3}$ de $\frac{3}{4}$ » = $\frac{1}{3} \times \frac{3}{4} = \_
- `WARN_HINT_IS_FORMULA` step 2: _Ensuite : ce qui reste = $\frac{3}{4} - \frac{1}{4} = \frac{2}{4}$._
- `WARN_HINT_IS_FORMULA` step 3: _Simplifie : $\frac{2}{4} = ?$_

### curriculum — 4EME / Fractions (row 65, exo 39)
- **Q**: Si $\frac{x}{3} = \frac{4}{9}$, que vaut $x$ ?
- **A**: $\frac{4}{3}$
- `WARN_HINT_IS_FORMULA` step 1: _Produit en croix : $x \times 9 = 4 \times 3$._
- `WARN_HINT_IS_FORMULA` step 2: _$9x = 12$, donc $x = \frac{12}{9}$._
- `WARN_HINT_IS_FORMULA` step 3: _Simplifie : $\frac{12}{9} = ?$ (divise par 3)_

### curriculum — 4EME / Fractions (row 65, exo 40)
- **Q**: Calcule : $\frac{\frac{2}{3} + \frac{1}{6}}{\frac{5}{6}}$ = ___
- **A**: $1$
- `WARN_HINT_IS_FORMULA` step 1: _D'abord le numérateur : $\frac{2}{3} + \frac{1}{6} = \frac{4}{6} + \frac{1}{6} = \frac{5}{6}$._
- `WARN_HINT_IS_FORMULA` step 2: _Ensuite la division : $\frac{5/6}{5/6} = \frac{5}{6} \div \frac{5}{6}$._

### diagnostic_exos — 6EME / Nombres_entiers (row 1, exo 1)
- **Q**: Une division donne : diviseur $= 7$, quotient $= 6$, reste $= 4$. Quel est le di
- **A**: $46$
- `WARN_HINT_IS_ANSWER` step 2: _Ici :$7 \times 6 = 42$, puis $42 + 4 = 46$._
- `WARN_HINT_IS_ANSWER` step 3: _Le dividende est $46$._
- `WARN_HINT_IS_FORMULA` step 2: _Ici :$7 \times 6 = 42$, puis $42 + 4 = 46$._

### diagnostic_exos — 6EME / Fractions (row 2, exo 1)
- **Q**: Tom mange $\frac{1}{4}$ d'une tablette de $24$ carrés. Combien de carrés mange-t
- **A**: $6$
- `WARN_HINT_IS_FORMULA` step 2: _$24 \div 4 = 6$._

### diagnostic_exos — 6EME / Proportionnalité (row 3, exo 1)
- **Q**: Dans un tableau de proportionnalité :$4 \to 10$. Alors $8 \to$?
- **A**: $20$
- `WARN_HINT_IS_ANSWER` step 3: _$10 \times 2 = 20$._
- `WARN_HINT_IS_FORMULA` step 3: _$10 \times 2 = 20$._

### diagnostic_exos — 6EME / Proportionnalité (row 3, exo 2)
- **Q**: Dans un tableau de proportionnalité :$3 \to 4{,}5$. Alors $7 \to$?
- **A**: $10{,}5$
- `WARN_HINT_IS_ANSWER` step 2: _$7 \times 1{,}5 = 10{,}5$._
- `WARN_HINT_IS_FORMULA` step 1: _Coefficient de proportionnalité :$4{,}5 \div 3 = 1{,}5$._
- `WARN_HINT_IS_FORMULA` step 2: _$7 \times 1{,}5 = 10{,}5$._

### diagnostic_exos — 6EME / Géométrie (row 4, exo 1)
- **Q**: Le diamètre d'un cercle est $3$ fois son rayon. Vrai ou faux ?
- **A**: Faux — le diamètre est $2$ fois le rayon
- `WARN_HINT_IS_FORMULA` step 1: _La relation entre diamètre et rayon :$D = 2 \times R$._

### diagnostic_exos — 6EME / Périmètres_Aires (row 5, exo 1)
- **Q**: Un rectangle a une longueur de $6$ cm et une largeur de $4$ cm. Son périmètre es
- **A**: $20$ cm
- `WARN_HINT_IS_ANSWER` step 2: _$P = 20$ cm._
- `WARN_HINT_IS_FORMULA` step 1: _Le périmètre $= 2 \times (L + l) = 2 \times (6 + 4) = 2 \times 10$._
- `WARN_HINT_IS_FORMULA` step 2: _$P = 20$ cm._
- `WARN_HINT_IS_FORMULA` step 3: _Attention :$6 \times 4 = 24$ cm$^2$, c'est l'AIRE, pas le périmètre !_

### diagnostic_exos — 6EME / Périmètres_Aires (row 5, exo 2)
- **Q**: Un triangle rectangle a deux côtés de l'angle droit mesurant $6$ cm et $8$ cm. Q
- **A**: $24$ cm$^2$
- `WARN_HINT_IS_ANSWER` step 3: _$\frac{6 \times 8}{2} = \frac{48}{2} = 24$ cm$^2$._
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{6 \times 8}{2} = \frac{48}{2} = 24$ cm$^2$._

### diagnostic_exos — 6EME / Angles (row 6, exo 1)
- **Q**: Un triangle a deux angles égaux à $65°$. Quel est le troisième angle ?
- **A**: $50°$
- `WARN_HINT_IS_ANSWER` step 3: _Troisième angle $= 180° - 130° = 50°$._

### diagnostic_exos — 6EME / Angles (row 6, exo 2)
- **Q**: Si un angle $\alpha$ a un complémentaire de 30°, que vaut $180° - \alpha$ (son s
- **A**: $120°$
- `WARN_HINT_IS_ANSWER` step 2: _Deux angles supplémentaires ont une somme de $180°$: supplémentaire de $60°= 180° - 60° = 120°$._
- `WARN_HINT_IS_FORMULA` step 1: _Deux angles complémentaires ont une somme de $90°$:$\alpha + 30° = 90°$ $\rightarrow$ $\alpha = 60°$_

### diagnostic_exos — 5EME / Fractions (row 7, exo 1)
- **Q**: Calcule $\frac{1}{3} + \frac{1}{4}$.
- **A**: $\frac{7}{12}$
- `WARN_HINT_IS_ANSWER` step 3: _$\frac{4}{12} + \frac{3}{12} = \frac{7}{12}$._
- `WARN_HINT_IS_FORMULA` step 2: _PPCM de $3$ et $4= 12$:$\frac{1}{3} = \frac{4}{12}$, $\frac{1}{4} = \frac{3}{12}$._
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{4}{12} + \frac{3}{12} = \frac{7}{12}$._

### diagnostic_exos — 5EME / Fractions (row 7, exo 2)
- **Q**: Calcule $\frac{2}{5} \times \frac{3}{4}$.
- **A**: $\frac{3}{10}$
- `WARN_HINT_IS_ANSWER` step 3: _On simplifie par $2$:$\frac{6}{20} = \frac{3}{10}$._
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{2 \times 3}{5 \times 4} = \frac{6}{20}$._
- `WARN_HINT_IS_FORMULA` step 3: _On simplifie par $2$:$\frac{6}{20} = \frac{3}{10}$._

### diagnostic_exos — 5EME / Nombres_relatifs (row 8, exo 1)
- **Q**: Calcule $(-8) + 3$.
- **A**: $-5$
- `WARN_HINT_IS_ANSWER` step 3: _$(-8) + 3 = -5$._

### diagnostic_exos — 5EME / Nombres_relatifs (row 8, exo 2)
- **Q**: Calcule $(-4) \times (-5)$.
- **A**: $20$
- `WARN_HINT_IS_ANSWER` step 3: _$4 \times 5 = 20$, donc $(-4) \times (-5) = +20$._
- `WARN_HINT_IS_FORMULA` step 2: _$(-) \times (-) = (+)$: moins fois moins donne plus._
- `WARN_HINT_IS_FORMULA` step 3: _$4 \times 5 = 20$, donc $(-4) \times (-5) = +20$._

### diagnostic_exos — 5EME / Proportionnalité (row 9, exo 1)
- **Q**: Un article coûte $80$ €. Son prix augmente de $15\,\%$. Quel est le nouveau prix
- **A**: $92$ €
- `WARN_HINT_IS_ANSWER` step 2: _Nouveau prix $= 80 + 12 = 92$ €._
- `WARN_HINT_IS_ANSWER` step 3: _Ou directement :$80 \times 1{,}15 = 92$ €._
- `WARN_HINT_IS_FORMULA` step 1: _$15\%$ de $80= 80 \times 0{,}15 = 12$ €._
- `WARN_HINT_IS_FORMULA` step 3: _Ou directement :$80 \times 1{,}15 = 92$ €._

### diagnostic_exos — 5EME / Proportionnalité (row 9, exo 2)
- **Q**: Un article augmente de $10\,\%$, puis diminue de $10\,\%$. Le prix final est-il 
- **A**: Non, il est légèrement inférieur
- `WARN_HINT_IS_FORMULA` step 2: _Après $+10\%$:$100 \times 1{,}1 = 110$ €._
- `WARN_HINT_IS_FORMULA` step 3: _Après $-10\%$:$110 \times 0{,}9 = 99$ €._

### diagnostic_exos — 5EME / Puissances (row 10, exo 1)
- **Q**: Calcule $2^5$.
- **A**: $32$
- `WARN_HINT_IS_ANSWER` step 2: _$2 \times 2 = 4$, $4 \times 2 = 8$, $8 \times 2 = 16$, $16 \times 2 = 32$._
- `WARN_HINT_IS_FORMULA` step 2: _$2 \times 2 = 4$, $4 \times 2 = 8$, $8 \times 2 = 16$, $16 \times 2 = 32$._

### diagnostic_exos — 5EME / Puissances (row 10, exo 2)
- **Q**: Simplifie $3^4 \times 3^2$.
- **A**: $3^6$
- `WARN_HINT_IS_ANSWER` step 2: _$3^4 \times 3^2 = 3^{4+2} = 3^6$._
- `WARN_HINT_IS_FORMULA` step 2: _$3^4 \times 3^2 = 3^{4+2} = 3^6$._

### diagnostic_exos — 5EME / Pythagore (row 11, exo 1)
- **Q**: Un triangle rectangle a ses deux côtés de l'angle droit mesurant $3$ cm et $4$ c
- **A**: $5$ cm
- `WARN_HINT_IS_ANSWER` step 3: _$c = \sqrt{25} = 5$ cm._
- `WARN_HINT_IS_FORMULA` step 1: _Théorème de Pythagore :$c^2 = a^2 + b^2$._
- `WARN_HINT_IS_FORMULA` step 2: _$c^2 = 3^2 + 4^2 = 9 + 16 = 25$._
- `WARN_HINT_IS_FORMULA` step 3: _$c = \sqrt{25} = 5$ cm._

### diagnostic_exos — 5EME / Pythagore (row 11, exo 2)
- **Q**: Dans un triangle rectangle, l'hypoténuse mesure $13$ cm et un côté de l'angle dr
- **A**: $12$ cm
- `WARN_HINT_IS_ANSWER` step 3: _$b = \sqrt{144} = 12$ cm._
- `WARN_HINT_IS_FORMULA` step 1: _On cherche un côté de l'angle droit, donc on soustrait :$b^2 = c^2 - a^2$._
- `WARN_HINT_IS_FORMULA` step 2: _$b^2 = 13^2 - 5^2 = 169 - 25 = 144$._
- `WARN_HINT_IS_FORMULA` step 3: _$b = \sqrt{144} = 12$ cm._

### diagnostic_exos — 5EME / Calcul_Littéral (row 12, exo 1)
- **Q**: Si $x = 4$, quelle est la valeur de $3x - 5$?
- **A**: $7$
- `WARN_HINT_IS_FORMULA` step 2: _$3 \times 4 - 5 = 12 - 5 = 7$._

### diagnostic_exos — 5EME / Calcul_Littéral (row 12, exo 2)
- **Q**: Développe $2(3x - 4)$.
- **A**: $6x - 8$
- `WARN_HINT_IS_ANSWER` step 3: _$2(3x - 4) = 6x - 8$._
- `WARN_HINT_IS_FORMULA` step 2: _$2 \times 3x = 6x$ et $2 \times (-4) = -8$._
- `WARN_HINT_IS_FORMULA` step 3: _$2(3x - 4) = 6x - 8$._

### diagnostic_exos — 1ERE / Second_Degre (row 13, exo 1)
- **Q**: Calculer le discriminant de $f(x) = 6x^2 -8x +7$.
- **A**: $\Delta = -104$
- `WARN_HINT_IS_FORMULA` step 2: _$\Delta = (-8)^2 - 4 \times 6 \times (7)$._
- `WARN_HINT_IS_FORMULA` step 3: _$\Delta = 64 - 168$._

### diagnostic_exos — 4EME / Puissances (row 14, exo 1)
- **Q**: Que vaut $2^{-3}$?
- **A**: $\frac{1}{8}$
- `WARN_HINT_IS_ANSWER` step 2: _$2^{-3} = \frac{1}{2^3} = \frac{1}{8}$._
- `WARN_HINT_IS_FORMULA` step 2: _$2^{-3} = \frac{1}{2^3} = \frac{1}{8}$._

### diagnostic_exos — 4EME / Puissances (row 14, exo 2)
- **Q**: Écris $0{,}0045$ en notation scientifique.
- **A**: $4{,}5 \times 10^{-3}$
- `WARN_HINT_IS_ANSWER` step 2: _$0{,}0045 = 4{,}5 \times 0{,}001 = 4{,}5 \times 10^{-3}$._
- `WARN_HINT_IS_FORMULA` step 2: _$0{,}0045 = 4{,}5 \times 0{,}001 = 4{,}5 \times 10^{-3}$._

### diagnostic_exos — 4EME / Calcul_Littéral (row 15, exo 1)
- **Q**: Développe $(x + 3)^2$.
- **A**: $x^2 + 6x + 9$
- `WARN_HINT_IS_ANSWER` step 3: _$= x^2 + 6x + 9$._
- `WARN_HINT_IS_FORMULA` step 1: _$(a + b)^2 = a^2 + 2ab + b^2$._
- `WARN_HINT_IS_FORMULA` step 2: _$(x + 3)^2 = x^2 + 2 \times x \times 3 + 3^2$._
- `WARN_HINT_IS_FORMULA` step 4: _Erreur classique : oublier le terme croisé $2ab = 6x$._

### diagnostic_exos — 4EME / Calcul_Littéral (row 15, exo 2)
- **Q**: Factorise $6x^2 + 9x$.
- **A**: $3x(2x + 3)$
- `WARN_HINT_IS_ANSWER` step 4: _$6x^2 + 9x = 3x(2x + 3)$._
- `WARN_HINT_IS_FORMULA` step 3: _$6x^2 = 3x \times 2x$ et $9x = 3x \times 3$._
- `WARN_HINT_IS_FORMULA` step 4: _$6x^2 + 9x = 3x(2x + 3)$._

### diagnostic_exos — 6EME / Nombres_Décimaux (row 16, exo 1)
- **Q**: Calcule $3{,}7 + 1{,}45$.
- **A**: $5{,}15$
- `WARN_HINT_IS_ANSWER` step 2: _$0 + 5 = 5$, $7 + 4 = 11$ (retenue), $3 + 1 + 1 = 5$ $\rightarrow$ $5{,}15$._

### diagnostic_exos — 6EME / Nombres_Décimaux (row 16, exo 2)
- **Q**: Calcule $4{,}5 \times 3{,}2$.
- **A**: $14{,}4$
- `WARN_HINT_IS_ANSWER` step 3: _$4{,}5 \times 3{,}2 = 14{,}40 = 14{,}4$._
- `WARN_HINT_IS_FORMULA` step 1: _$45 \times 32 = 1440$._
- `WARN_HINT_IS_FORMULA` step 3: _$4{,}5 \times 3{,}2 = 14{,}40 = 14{,}4$._

### diagnostic_exos — 6EME / Statistiques_6ème (row 17, exo 1)
- **Q**: Calcule la moyenne des valeurs :$6, 10, 8, 12, 4$.
- **A**: $8$
- `WARN_HINT_IS_FORMULA` step 2: _Moyenne $= \frac{40}{5} = 8$._

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

### diagnostic_exos — 6EME / Volumes (row 20, exo 2)
- **Q**: Un cylindre a un rayon de 4 cm et un volume de 200,96 cm³. Quelle est sa hauteur
- **A**: 4 cm
- `WARN_HINT_IS_ANSWER` step 3: _h = 4 cm_
- `WARN_HINT_TOO_SHORT` step 3: _h = 4 cm_

### diagnostic_exos — 4EME / Pythagore (row 21, exo 2)
- **Q**: Dans un triangle rectangle, l'hypoténuse mesure $10$ cm et un côté de l'angle dr
- **A**: $8$ cm
- `WARN_HINT_IS_ANSWER` step 3: _$b = \sqrt{64} = 8$ cm._
- `WARN_HINT_IS_FORMULA` step 1: _On cherche un côté de l'angle droit :$b^2 = c^2 - a^2$._
- `WARN_HINT_IS_FORMULA` step 2: _$b^2 = 10^2 - 6^2 = 100 - 36 = 64$._
- `WARN_HINT_IS_FORMULA` step 3: _$b = \sqrt{64} = 8$ cm._

### diagnostic_exos — 4EME / Proportionnalité (row 22, exo 1)
- **Q**: Une voiture roule à $90$ km/h. Quelle distance parcourt-elle en $2$ h $30$ min ?
- **A**: $225$ km
- `WARN_HINT_IS_ANSWER` step 3: _$= 225$ km._

### diagnostic_exos — 4EME / Proportionnalité (row 22, exo 2)
- **Q**: $4$ ouvriers mettent $6$ jours pour finir un chantier. En combien de jours $3$ o
- **A**: $8$ jours
- `WARN_HINT_IS_ANSWER` step 3: _Avec $3$ ouvriers :$24 \div 3 = 8$ jours._
- `WARN_HINT_IS_FORMULA` step 2: _Total de travail $= 4 \times 6 = 24$ jours-ouvrier._
- `WARN_HINT_IS_FORMULA` step 3: _Avec $3$ ouvriers :$24 \div 3 = 8$ jours._

### diagnostic_exos — 4EME / Fonctions_Linéaires (row 23, exo 1)
- **Q**: $f(x) = 5x$ est une fonction linéaire. Calcule $f(3)$.
- **A**: $15$
- `WARN_HINT_IS_ANSWER` step 2: _$f(3) = 15$._
- `WARN_HINT_IS_FORMULA` step 1: _On remplace $x$ par $3$:$f(3) = 5 \times 3$._
- `WARN_HINT_IS_FORMULA` step 2: _$f(3) = 15$._

### diagnostic_exos — 4EME / Fonctions_Linéaires (row 23, exo 2)
- **Q**: $f(x) = ax$ est une fonction linéaire. On sait que $f(4) = 10$. Calcule $f(6)$.
- **A**: $15$
- `WARN_HINT_IS_ANSWER` step 2: _$f(6) = 2{,}5 \times 6 = 15$._
- `WARN_HINT_IS_FORMULA` step 1: _$f(4) = 10$ $\rightarrow$ $a = \frac{10}{4} = 2{,}5$._
- `WARN_HINT_IS_FORMULA` step 2: _$f(6) = 2{,}5 \times 6 = 15$._

### diagnostic_exos — 5EME / Transformations (row 24, exo 1)
- **Q**: Le point A(1,3) est translaté par le vecteur $\vec{v}$ (4,-2). Quelles sont les 
- **A**: (5,1)
- `WARN_HINT_IS_ANSWER` step 3: _A'y = 3 + (-2) = 1 → A'(5,1)_

### diagnostic_exos — 5EME / Transformations (row 24, exo 2)
- **Q**: Par symétrie centrale de centre O(0,0), l'image de M(3,-2) est M'. Puis M' est t
- **A**: (-2,6)
- `WARN_HINT_IS_ANSWER` step 3: _Image finale : (-2,6)_

### diagnostic_exos — 5EME / Racines_Carrées (row 25, exo 1)
- **Q**: Quelle est la valeur de $\sqrt{36}$?
- **A**: 6
- `WARN_HINT_IS_FORMULA` step 3: _$6^2 = 36$, donc $\sqrt{36} = 6$._

### diagnostic_exos — 5EME / Racines_Carrées (row 25, exo 2)
- **Q**: Dans un triangle rectangle, les deux côtés de l'angle droit mesurent 9 cm et 12 
- **A**: 15 cm
- `WARN_HINT_IS_ANSWER` step 2: _hyp = √225 = 15 cm_
- `WARN_HINT_IS_ANSWER` step 3: _Résultat : 15 cm_

### diagnostic_exos — 5EME / Triangles_Semblables (row 26, exo 1)
- **Q**: Le triangle ABC est semblable au triangle DEF avec un rapport k = 2. Si AB = 5 c
- **A**: 10 cm
- `WARN_HINT_IS_ANSWER` step 2: _DE = k × AB = 2 × 5 = 10 cm_
- `WARN_HINT_IS_ANSWER` step 3: _Résultat : 10 cm_

### diagnostic_exos — 5EME / Triangles_Semblables (row 26, exo 2)
- **Q**: Deux triangles semblables ont des aires de 16 cm² et 36 cm². Quel est le rapport
- **A**: 2/3
- `WARN_HINT_IS_ANSWER` step 2: _k = √(4/9) = 2/3_
- `WARN_HINT_IS_ANSWER` step 3: _Résultat : 2/3_

### diagnostic_exos — 6EME / Agrandissement_Réduction (row 27, exo 1)
- **Q**: Un segment de 6 cm est agrandi avec k = 4. Quelle est sa nouvelle longueur ?
- **A**: 24 cm
- `WARN_HINT_IS_ANSWER` step 3: _Résultat : 24 cm_
- `WARN_HINT_IS_FORMULA` step 1: _Pour agrandir un segment, multiplie sa longueur par le facteur $k$. Pose le calcul avec $k = 4$ et l_

### diagnostic_exos — 6EME / Agrandissement_Réduction (row 27, exo 2)
- **Q**: Sur une carte à l'échelle 1/50 000, deux points sont à 6 cm de distance. Quelle 
- **A**: 3 km
- `WARN_HINT_IS_ANSWER` step 3: _Résultat : 3 km_

### diagnostic_exos — 6EME / Conversions_Unités (row 28, exo 1)
- **Q**: Convertir 4 km en mètres.
- **A**: 4 000 m
- `WARN_HINT_IS_ANSWER` step 2: _4 km = 4 000 m_
- `WARN_HINT_IS_ANSWER` step 3: _Résultat : 4 000 m_

### diagnostic_exos — 6EME / Conversions_Unités (row 28, exo 2)
- **Q**: Convertir 2 m² en cm².
- **A**: 20 000 cm²
- `WARN_HINT_IS_ANSWER` step 2: _2 m² = 2 × 10 000 = 20 000 cm²_
- `WARN_HINT_IS_ANSWER` step 3: _Résultat : 20 000 cm²_

### diagnostic_exos — 6EME / Puissances_10 (row 29, exo 1)
- **Q**: Que vaut $10^4$?
- **A**: 10 000
- `WARN_HINT_IS_ANSWER` step 2: _= 10 000_
- `WARN_HINT_TOO_SHORT` step 2: _= 10 000_

### diagnostic_exos — 6EME / Puissances_10 (row 29, exo 2)
- **Q**: Calculer $10^3 \times 10^4$.
- **A**: 10⁷
- `WARN_HINT_IS_ANSWER` step 3: _= 10⁷_
- `WARN_HINT_TOO_SHORT` step 3: _= 10⁷_

### diagnostic_exos — 4EME / Homothétie (row 30, exo 1)
- **Q**: Une homothétie de centre O et de rapport k = 4 transforme A avec OA = 3 cm. Quel
- **A**: 12 cm
- `WARN_HINT_IS_FORMULA` step 1: _Dans une homothétie, la distance image vaut $OA' = k \times OA$. Ici $k = 4$ et $OA = 3$ cm._
- `WARN_HINT_IS_FORMULA` step 2: _Calcule : $OA' = 4 \times 3$._

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
- `WARN_HINT_IS_ANSWER` step 3: _= 3 cm_
- `WARN_HINT_TOO_SHORT` step 3: _= 3 cm_

### diagnostic_exos — 1ERE / Suites (row 32, exo 1)
- **Q**: $(u_n)$ est arithmétique avec $u_0 = 8$ et $r = 10$. Calculer $u_{10}$.
- **A**: $u_{10} = 108$
- `WARN_HINT_IS_FORMULA` step 1: _Suite arithmétique :$u_n = u_0 + nr$._
- `WARN_HINT_IS_FORMULA` step 2: _$u_{10} = 8 + 10 \times 10$._
- `WARN_HINT_TOO_SHORT` step 3: _Calculer._

### diagnostic_exos — 1ERE / Suites (row 32, exo 2)
- **Q**: Montrer par récurrence que $u_n = 2^n + 6$ vérifie $u_{n+1} = 2u_n - 6$.
- **A**: Vrai par calcul direct
- `WARN_HINT_IS_FORMULA` step 2: _$= 2(2^n + 6) - 6 = 2^{n+1} + 6$._

### diagnostic_exos — 1ERE / Derivation (row 33, exo 2)
- **Q**: Équation de la tangente à $f(x) = x^2$ en $x_0 = 6$.
- **A**: $y = 12x - 36$
- `WARN_HINT_IS_FORMULA` step 1: _$f'(x)=2x$, $f'(6)=12$._
- `WARN_HINT_IS_FORMULA` step 2: _$f(6)=36$._
- `WARN_HINT_IS_FORMULA` step 3: _Appliquer $y=f'(a)(x-a)+f(a)$._

### diagnostic_exos — 1ERE / Exponentielle (row 34, exo 2)
- **Q**: Résoudre $e^{2x} - 8e^x + 7 = 0$.
- **A**: Poser $X = e^x$ et résoudre le trinôme
- `WARN_HINT_TOO_SHORT` step 3: _Conclure._

### diagnostic_exos — 1ERE / Trigonometrie (row 35, exo 1)
- **Q**: Que vaut $\cos(2\pi/3)$?
- **A**: $-1/2$
- `WARN_HINT_IS_ANSWER` step 3: _$\cos(2\pi/3) = -1/2$._
- `WARN_HINT_IS_FORMULA` step 3: _$\cos(2\pi/3) = -1/2$._

### diagnostic_exos — 1ERE / Trigonometrie (row 35, exo 2)
- **Q**: Résoudre $\sin(x) = -1$ sur $[0; 2\pi]$.
- **A**: $x = 3\pi/2$
- `WARN_HINT_IS_ANSWER` step 3: _Il correspond à $x = 3\pi/2$._
- `WARN_HINT_IS_FORMULA` step 3: _Il correspond à $x = 3\pi/2$._

### diagnostic_exos — 1ERE / Produit_Scalaire (row 36, exo 1)
- **Q**: $\vec{u}(7;8)$ et $\vec{v}(6;9)$. Calculer $\vec{u} \cdot \vec{v}$.
- **A**: $114$
- `WARN_HINT_TOO_SHORT` step 3: _Calculer._

### diagnostic_exos — 1ERE / Produit_Scalaire (row 36, exo 2)
- **Q**: Triangle $ABC$ avec $AB=8$, $AC=9$, $BC=10$. Calculer $\vec{AB} \cdot \vec{AC}$ 
- **A**: $22$
- `WARN_HINT_TOO_SHORT` step 2: _Calculer._
- `WARN_HINT_TOO_SHORT` step 3: _Conclure._

### diagnostic_exos — 1ERE / Geometrie_Repere (row 37, exo 1)
- **Q**: Donner un vecteur directeur de la droite $y = 6x + 7$.
- **A**: $\vec{u}(1;6)$
- `WARN_HINT_IS_FORMULA` step 1: _Coefficient directeur $m = 6$._
- `WARN_HINT_TOO_SHORT` step 3: _$(1; 6)$._

### diagnostic_exos — 1ERE / Probabilites_Cond (row 38, exo 1)
- **Q**: $P(A) = 0{,}10$, $P(B|A) = 0{,}8$. Calculer $P(A \cap B)$.
- **A**: $0{,}80$
- `WARN_HINT_TOO_SHORT` step 3: _Calculer._

### diagnostic_exos — 1ERE / Variables_Aleatoires (row 39, exo 1)
- **Q**: $X$ prend les valeurs $5, 6, 7$ avec probabilités $0{,}25, 0{,}50, 0{,}25$. $E(X
- **A**: $6{,}00$
- `WARN_HINT_IS_ANSWER` step 3: _$E(X) = 6{,}00$._
- `WARN_HINT_IS_FORMULA` step 3: _$E(X) = 6{,}00$._

### diagnostic_exos — 1ERE / Variables_Aleatoires (row 39, exo 2)
- **Q**: $X \sim B(10; 0{,}8)$. Calculer $P(X = 1)$.
- **A**: $\binom{10}{1} (0{,}8)^1(0{,}2)^{9}$
- `WARN_HINT_IS_FORMULA` step 1: _$\binom{10}{1} = 10$._
- `WARN_HINT_IS_FORMULA` step 2: _$p = 0{,}8$, $1-p = 0{,}2$._
- `WARN_HINT_TOO_SHORT` step 3: _Calculer._

### diagnostic_exos — 1ERE / Algorithmique (row 40, exo 1)
- **Q**: Que renvoie ce code ?
```python
x = 8
for i in range(4):
    x = x + 2
print(x)

- **A**: $16$
- `WARN_HINT_TOO_SHORT` step 3: _Conclure._

### diagnostic_exos — 1ERE / Algorithmique (row 40, exo 2)
- **Q**: Écrire un algo Python qui calcule $\sum_{k=1}^{15} k^2$.
- **A**: `sum(k**2 for k in range(1, 16))`
- `WARN_HINT_TOO_SHORT` step 3: _Conclure._

### diagnostic_exos — 3EME / Arithmetique_Brevet (row 41, exo 1)
- **Q**: Quel est le plus grand diviseur commun de $60$ et $96$ ?
- **A**: $12$
- `WARN_HINT_IS_FORMULA` step 3: _$4 \times 3 = ?$._

### diagnostic_exos — 3EME / Arithmetique_Brevet (row 41, exo 2)
- **Q**: $119$ est un nombre premier.
- **A**: Faux
- `WARN_HINT_IS_FORMULA` step 2: _$119 \div 7 = 17$ : la division tombe juste._

### diagnostic_exos — 3EME / Arithmetique_Brevet (row 41, exo 3)
- **Q**: On veut répartir $108$ billes et $144$ cartes en paquets identiques (même nombre
- **A**: $36$
- `WARN_HINT_IS_FORMULA` step 3: _$4 \times 9 = ?$._

### diagnostic_exos — 3EME / Calcul_Litteral_Brevet (row 42, exo 1)
- **Q**: Développe $3(2x - 5)$.
- **A**: $6x - 15$
- `WARN_HINT_IS_FORMULA` step 2: _$3 \times 2x = 6x$ et $3 \times (-5) = ?$._

### diagnostic_exos — 3EME / Calcul_Litteral_Brevet (row 42, exo 2)
- **Q**: Factorise $4x + 12$.
- **A**: $4(x + 3)$
- `WARN_HINT_IS_FORMULA` step 2: _On met $4$ en facteur : $4 \times x + 4 \times ? = 4(x + ?)$._

### diagnostic_exos — 3EME / Calcul_Litteral_Brevet (row 42, exo 3)
- **Q**: $(x + 3)^2 = x^2 + 6x + 9$.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _L'identité remarquable $(a+b)^2 = a^2 + 2ab + b^2$._
- `WARN_HINT_IS_FORMULA` step 2: _Ici $a = x$ et $b = 3$, donc $2ab = 2 \times x \times 3 = ?$._

### diagnostic_exos — 3EME / Equations_Brevet (row 43, exo 1)
- **Q**: Résous $3x + 7 = 22$.
- **A**: $x = 5$
- `WARN_HINT_IS_FORMULA` step 1: _On isole le terme en $x$ : $3x = 22 - 7$._
- `WARN_HINT_IS_FORMULA` step 2: _$3x = 15$, donc $x = \frac{15}{?}$._

### diagnostic_exos — 3EME / Equations_Brevet (row 43, exo 2)
- **Q**: Un nombre augmenté de $8$ donne $35$. Quel est ce nombre ?
- **A**: 27
- `WARN_HINT_IS_FORMULA` step 1: _On appelle $x$ le nombre cherché. L'équation est $x + 8 = ?$._
- `WARN_HINT_IS_FORMULA` step 2: _On résout : $x = 35 - ?$._

### diagnostic_exos — 3EME / Equations_Brevet (row 43, exo 3)
- **Q**: Résous $(x - 4)(2x + 6) = 0$.
- **A**: $x = 4$ ou $x = -3$
- `WARN_HINT_IS_FORMULA` step 2: _$x - 4 = 0 \Rightarrow x = ?$ et $2x + 6 = 0 \Rightarrow 2x = -6 \Rightarrow x = ?$._

### diagnostic_exos — 3EME / Fonctions_Affines_Brevet (row 44, exo 1)
- **Q**: Soit $f(x) = -2x + 5$. Calcule $f(3)$.
- **A**: $-1$
- `WARN_HINT_IS_FORMULA` step 1: _On remplace $x$ par $3$ dans $f(x) = -2x + 5$._
- `WARN_HINT_IS_FORMULA` step 2: _$f(3) = -2 \times 3 + 5 = -6 + 5 = \;?$._

### diagnostic_exos — 3EME / Fonctions_Affines_Brevet (row 44, exo 2)
- **Q**: Une droite passe par $A(0 ; 3)$ et $B(4 ; 11)$. Quel est son coefficient directe
- **A**: $2$
- `WARN_HINT_IS_FORMULA` step 1: _Le coefficient directeur se calcule : $a = \frac{y_B - y_A}{x_B - x_A}$._
- `WARN_HINT_IS_FORMULA` step 2: _$a = \frac{11 - 3}{4 - 0} = \frac{8}{4} = \;?$._

### diagnostic_exos — 3EME / Fonctions_Affines_Brevet (row 44, exo 3)
- **Q**: La droite $d$ a pour équation $y = 3x - 2$ et la droite $d'$ a pour équation $y 
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _Au point d'intersection, les deux fonctions sont égales : $3x - 2 = -x + 6$._
- `WARN_HINT_IS_FORMULA` step 2: _$3x + x = 6 + 2$, soit $4x = 8$, donc $x = \;?$. Est-ce bien $2$ ?_

### diagnostic_exos — 3EME / Fonctions_Brevet (row 45, exo 1)
- **Q**: On donne $f(x) = 3x + 1$. Calcule $f(5)$.
- **A**: $16$
- `WARN_HINT_IS_FORMULA` step 2: _$f(5) = 3 \times 5 + 1 = 15 + 1 = \;?$._

### diagnostic_exos — 3EME / Fonctions_Brevet (row 45, exo 2)
- **Q**: Sur le graphique d'une fonction $f$, le point $(3 ; 7)$ est sur la courbe. Quell
- **A**: $7$
- `WARN_HINT_IS_FORMULA` step 1: _Si le point $(3 ; 7)$ est sur la courbe, cela signifie que $f(3) = 7$._

### diagnostic_exos — 3EME / Fonctions_Brevet (row 45, exo 3)
- **Q**: Soit $h(x) = x^2 - 9$. Un antécédent de $0$ par $h$ est $x = 3$.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _Un antécédent de $0$, c'est un nombre $x$ tel que $h(x) = 0$._
- `WARN_HINT_IS_FORMULA` step 2: _On vérifie : $h(3) = 3^2 - 9 = 9 - 9 = \;?$. Est-ce bien $0$ ?_

### diagnostic_exos — 3EME / Fractions_Brevet (row 46, exo 1)
- **Q**: Calcule $\frac{5}{6} - \frac{3}{4}$.
- **A**: $\frac{1}{12}$
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{5}{6} = \frac{10}{12}$ et $\frac{3}{4} = \frac{9}{12}$._
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{10}{12} - \frac{9}{12} = \frac{?}{12}$._

### diagnostic_exos — 3EME / Fractions_Brevet (row 46, exo 2)
- **Q**: Dans une classe de $32$ élèves, les $\frac{3}{8}$ pratiquent un sport. Combien d
- **A**: 12
- `WARN_HINT_IS_FORMULA` step 1: _On calcule $\frac{3}{8}$ de $32$ : $\frac{3}{8} \times 32 = \frac{3 \times 32}{8}$._
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{96}{8} = ?$._

### diagnostic_exos — 3EME / Fractions_Brevet (row 46, exo 3)
- **Q**: Calcule $\frac{7}{9} \times \frac{3}{14}$.
- **A**: $\frac{1}{6}$
- `WARN_HINT_IS_FORMULA` step 1: _On multiplie : $\frac{7 \times 3}{9 \times 14} = \frac{21}{126}$._
- `WARN_HINT_IS_FORMULA` step 2: _On simplifie par $21$ : $\frac{21}{126} = \frac{1}{?}$._

### diagnostic_exos — 3EME / Geometrie_Espace_Brevet (row 47, exo 1)
- **Q**: Un cylindre a un rayon de $3$ cm et une hauteur de $10$ cm. Quel est son volume 
- **A**: $283$ cm³
- `WARN_HINT_IS_FORMULA` step 1: _$V = \pi \times r^2 \times h = \pi \times 3^2 \times 10$._
- `WARN_HINT_IS_FORMULA` step 2: _$V = 90\pi \approx 282{,}7$._

### diagnostic_exos — 3EME / Geometrie_Espace_Brevet (row 47, exo 3)
- **Q**: Une boule de rayon $6$ cm est agrandie par un coefficient $k = 2$. Par combien s
- **A**: 8
- `WARN_HINT_IS_FORMULA` step 2: _$k^3 = 2^3 = ?$._

### diagnostic_exos — 3EME / Inequations_Brevet (row 48, exo 2)
- **Q**: L'ensemble des solutions de $x \geq -2$ est représenté par une demi-droite parta
- **A**: Vrai
- `WARN_HINT_IS_ANSWER` step 3: _Le crochet est fermé en $-2$ car $-2$ est inclus. Vrai ou faux ?_

### diagnostic_exos — 3EME / Inequations_Brevet (row 48, exo 3)
- **Q**: Un cinéma propose des places a $8$ euros. Avec un budget de $50$ euros, combien 
- **A**: 6
- `WARN_HINT_IS_FORMULA` step 2: _$n \leq \frac{50}{8} = ?$ (calcule la division)._

### diagnostic_exos — 3EME / Probabilites_Brevet (row 49, exo 1)
- **Q**: Un sac contient $3$ boules rouges et $5$ boules bleues. On tire une boule au has
- **A**: $\frac{3}{8}$
- `WARN_HINT_IS_FORMULA` step 3: _$P(\text{rouge}) = \frac{?}{8}$._

### diagnostic_exos — 3EME / Probabilites_Brevet (row 49, exo 2)
- **Q**: La probabilité qu'il pleuve demain est $0{,}3$. Quelle est la probabilité qu'il 
- **A**: $0{,}7$
- `WARN_HINT_IS_FORMULA` step 2: _$P(\overline{A}) = 1 - P(A)$._
- `WARN_HINT_IS_FORMULA` step 3: _$P(\text{pas de pluie}) = 1 - 0{,}3 = ?$._

### diagnostic_exos — 3EME / Probabilites_Brevet (row 49, exo 3)
- **Q**: On lance un dé équilibré puis on tire une carte (rouge ou noire). Combien d'issu
- **A**: $12$
- `WARN_HINT_IS_FORMULA` step 3: _Nombre total d'issues $= 6 \times ? = ?$._

### diagnostic_exos — 3EME / Proportionnalite_Brevet (row 50, exo 1)
- **Q**: Un pantalon affiché à $65$ euros est soldé à $-20\%$. Quel est le prix soldé en 
- **A**: 52
- `WARN_HINT_IS_FORMULA` step 1: _La réduction vaut $65 \times \frac{20}{100} = 13$ euros._

### diagnostic_exos — 3EME / Proportionnalite_Brevet (row 50, exo 2)
- **Q**: $4$ kg de pommes coûtent $6$ euros. Combien coûtent $10$ kg ?
- **A**: $15$ euros
- `WARN_HINT_IS_FORMULA` step 1: _Le prix est proportionnel à la masse. Le prix au kg est $\frac{6}{4} = 1{,}5$ euros._
- `WARN_HINT_IS_FORMULA` step 2: _Pour $10$ kg : $10 \times 1{,}5 = ?$ euros._

### diagnostic_exos — 3EME / Proportionnalite_Brevet (row 50, exo 3)
- **Q**: Un article passe de $120$ euros à $150$ euros. Quel est le pourcentage d'augment
- **A**: $25\%$
- `WARN_HINT_IS_FORMULA` step 2: _Le taux est $\frac{30}{120} = \frac{1}{4} = 0{,}25$._
- `WARN_HINT_IS_FORMULA` step 3: _$0{,}25 \times 100 = ?\%$._

### diagnostic_exos — 3EME / Puissances_Brevet (row 51, exo 3)
- **Q**: Calcule $\frac{3 \times 10^4}{6 \times 10^{-2}}$ et donne le résultat en notatio
- **A**: $5 \times 10^5$
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{3}{6} = 0{,}5$ et $10^{4-(-2)} = 10^6$._
- `WARN_HINT_IS_FORMULA` step 3: _$0{,}5 \times 10^6 = ? \times 10^?$ en notation scientifique._

### diagnostic_exos — 3EME / Pythagore_Brevet (row 52, exo 1)
- **Q**: Dans un triangle rectangle, les deux côtés de l'angle droit mesurent $6$ cm et $
- **A**: $10$ cm
- `WARN_HINT_IS_FORMULA` step 1: _On applique le théorème de Pythagore : $h^2 = 6^2 + 8^2$._
- `WARN_HINT_IS_FORMULA` step 2: _$h^2 = 36 + 64 = 100$._
- `WARN_HINT_IS_FORMULA` step 3: _$h = \sqrt{?}$_

### diagnostic_exos — 3EME / Pythagore_Brevet (row 52, exo 2)
- **Q**: Un triangle rectangle a une hypoténuse de $13$ cm et un côté de $5$ cm. Quelle e
- **A**: 12
- `WARN_HINT_IS_FORMULA` step 1: _On isole le côté inconnu : $c^2 = 13^2 - 5^2$._
- `WARN_HINT_IS_FORMULA` step 2: _$c^2 = 169 - 25 = 144$._
- `WARN_HINT_IS_FORMULA` step 3: _$c = \sqrt{?}$_

### diagnostic_exos — 3EME / Racines_Carrees_Brevet (row 53, exo 1)
- **Q**: Simplifie $\sqrt{75}$.
- **A**: $5\sqrt{3}$
- `WARN_HINT_IS_FORMULA` step 2: _$\sqrt{75} = \sqrt{25} \times \sqrt{3} = ?\sqrt{3}$._

### diagnostic_exos — 3EME / Racines_Carrees_Brevet (row 53, exo 2)
- **Q**: $\sqrt{9 \times 16} = \sqrt{9} \times \sqrt{16}$.
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _La propriété $\sqrt{a \times b} = \sqrt{a} \times \sqrt{b}$ est valable pour $a \geq 0$ et $b \geq 0_
- `WARN_HINT_IS_FORMULA` step 2: _Vérifions : $\sqrt{144} = 12$ et $3 \times 4 = 12$. Les deux sont-ils égaux ?_

### diagnostic_exos — 3EME / Racines_Carrees_Brevet (row 53, exo 3)
- **Q**: Calcule $3\sqrt{2} \times 4\sqrt{2}$.
- **A**: $24$
- `WARN_HINT_IS_FORMULA` step 1: _On multiplie les coefficients : $3 \times 4 = 12$._
- `WARN_HINT_IS_FORMULA` step 2: _On multiplie les racines : $\sqrt{2} \times \sqrt{2} = 2$._
- `WARN_HINT_IS_FORMULA` step 3: _$12 \times 2 = ?$._

### diagnostic_exos — 3EME / Scratch_Brevet (row 54, exo 1)
- **Q**: Un programme de calcul dit : « Prends un nombre, multiplie-le par $3$, puis ajou
- **A**: $17$
- `WARN_HINT_IS_FORMULA` step 1: _On part de $4$. Première étape : $4 \times 3 = ?$._

### diagnostic_exos — 3EME / Scratch_Brevet (row 54, exo 3)
- **Q**: Un script Scratch initialise une variable $n$ à $1$ puis répète $4$ fois : « rem
- **A**: $16$
- `WARN_HINT_IS_FORMULA` step 1: _Au départ $n = 1$. Après la 1ère répétition : $n = 1 \times 2 = 2$._
- `WARN_HINT_IS_FORMULA` step 2: _Après la 2ème : $n = 4$. Après la 3ème : $n = ?$._
- `WARN_HINT_IS_FORMULA` step 3: _Après la 4ème répétition : $n = 8 \times 2 = ?$._

### diagnostic_exos — 3EME / Statistiques_Brevet (row 55, exo 1)
- **Q**: Les notes d'un élève sont : $8$, $12$, $14$, $10$, $6$. Quelle est sa moyenne ?
- **A**: $10$
- `WARN_HINT_IS_ANSWER` step 1: _Additionne toutes les notes : $8 + 12 + 14 + 10 + 6 = ?$._

### diagnostic_exos — 3EME / Statistiques_Brevet (row 55, exo 2)
- **Q**: Voici une série ordonnée de $7$ valeurs : $3$, $5$, $7$, $9$, $11$, $13$, $15$. 
- **A**: $9$
- `WARN_HINT_IS_FORMULA` step 2: _Il y a $7$ valeurs, donc la médiane est la valeur en position $\frac{7+1}{2} = ?$._

### diagnostic_exos — 3EME / Statistiques_Brevet (row 55, exo 3)
- **Q**: Voici $8$ valeurs ordonnées : $4$, $6$, $8$, $10$, $12$, $14$, $16$, $18$. Le pr
- **A**: $7$
- `WARN_HINT_IS_FORMULA` step 3: _$Q_1 = \frac{6 + 8}{2} = ?$._

### diagnostic_exos — 3EME / Thales_Brevet (row 56, exo 1)
- **Q**: Dans un triangle $ABC$, $M \in [AB]$ et $N \in [AC]$ avec $(MN) \parallel (BC)$.
- **A**: $6$ cm
- `WARN_HINT_IS_FORMULA` step 1: _Par le théorème de Thalès : $\frac{AM}{AB} = \frac{MN}{BC}$._
- `WARN_HINT_IS_FORMULA` step 2: _$\frac{4}{10} = \frac{MN}{15}$._
- `WARN_HINT_IS_FORMULA` step 3: _$MN = 15 \times \frac{4}{?}$_

### diagnostic_exos — 3EME / Thales_Brevet (row 56, exo 2)
- **Q**: Deux droites sécantes sont coupées par deux parallèles. On a $\frac{OA}{OB} = \f
- **A**: 6
- `WARN_HINT_IS_FORMULA` step 1: _On utilise le rapport donné : $\frac{OA}{10} = \frac{3}{5}$._
- `WARN_HINT_IS_FORMULA` step 2: _$OA = 10 \times \frac{3}{5}$._
- `WARN_HINT_IS_FORMULA` step 3: _$OA = ?$ cm_

### diagnostic_exos — 3EME / Thales_Brevet (row 56, exo 3)
- **Q**: Configuration papillon : deux droites se coupent en $O$. On a $OA = 3$, $OB = 6$
- **A**: Vrai
- `WARN_HINT_IS_FORMULA` step 1: _On compare les rapports : $\frac{OA}{OB} = \frac{3}{6} = \frac{1}{2}$ et $\frac{OC}{OD} = \frac{4}{8_

### diagnostic_exos — 3EME / Transformations_Brevet (row 57, exo 1)
- **Q**: Le point $A(2\,;\,3)$ est translaté par le vecteur $\vec{u}(4\,;\,-1)$. Quelles 
- **A**: $(6\,;\,2)$
- `WARN_HINT_IS_FORMULA` step 2: _$x' = 2 + 4 = 6$ et $y' = 3 + (-1) = ?$._
- `WARN_HINT_IS_FORMULA` step 3: _$A' = (? \,;\, ?)$_

### diagnostic_exos — 3EME / Transformations_Brevet (row 57, exo 3)
- **Q**: Un segment $[AB]$ de longueur $5$ cm subit une homothétie de centre $O$ et de ra
- **A**: 10
- `WARN_HINT_IS_FORMULA` step 2: _$A'B' = |{-2}| \times 5$._
- `WARN_HINT_IS_FORMULA` step 3: _$A'B' = ?$ cm_

### diagnostic_exos — 3EME / Trigonometrie_Brevet (row 58, exo 1)
- **Q**: Dans un triangle rectangle, l'angle $\widehat{A} = 35°$, le côté adjacent mesure
- **A**: $10 \times \tan(35°)$
- `WARN_HINT_IS_FORMULA` step 3: _$\tan(\widehat{A}) = \frac{\text{opposé}}{\text{adjacent}}$, donc opposé $= \text{adjacent} \times \_

### diagnostic_exos — 3EME / Trigonometrie_Brevet (row 58, exo 2)
- **Q**: Triangle rectangle : hypoténuse $= 20$ cm, $\cos(\widehat{B}) = 0{,}6$. Quelle e
- **A**: 12
- `WARN_HINT_IS_FORMULA` step 1: _$\cos(\widehat{B}) = \frac{\text{adjacent}}{\text{hypoténuse}}$._

### diagnostic_exos — 3EME / Trigonometrie_Brevet (row 58, exo 3)
- **Q**: Dans un triangle rectangle, le côté opposé à l'angle $\widehat{C}$ mesure $7$ cm
- **A**: $30°$
- `WARN_HINT_IS_FORMULA` step 1: _$\sin(\widehat{C}) = \frac{\text{opposé}}{\text{hypoténuse}} = \frac{7}{14} = 0{,}5$._
- `WARN_HINT_IS_FORMULA` step 3: _$\widehat{C} = ?°$_

### diagnostic_exos — 4EME / Fractions (row 59, exo 1)
- **Q**: Calcule $\frac{3}{4} \div \frac{3}{8}$.
- **A**: $2$
- `WARN_HINT_IS_FORMULA` step 2: _Inverse de $\frac{3}{8}= \frac{8}{3}$._
- `WARN_HINT_IS_FORMULA` step 3: _$\frac{3}{4} \times \frac{8}{3} = \frac{24}{12} = 2$._

### diagnostic_exos — 4EME / Fractions (row 59, exo 2)
- **Q**: Laquelle est la plus grande :$\frac{5}{8}$ ou $\frac{7}{12}$?
- **A**: $\frac{5}{8}$
- `WARN_HINT_IS_ANSWER` step 2: _PPCM de $8$ et $12= 24$:$\frac{5}{8} = \frac{15}{24}$, $\frac{7}{12} = \frac{14}{24}$._
- `WARN_HINT_IS_ANSWER` step 3: _$15 > 14$, donc $\frac{5}{8} > \frac{7}{12}$._
- `WARN_HINT_IS_FORMULA` step 2: _PPCM de $8$ et $12= 24$:$\frac{5}{8} = \frac{15}{24}$, $\frac{7}{12} = \frac{14}{24}$._

### diagnostic_exos — 4EME / Équations (row 60, exo 1)
- **Q**: Résous $3x + 5 = 17$.
- **A**: $x = 4$
- `WARN_HINT_IS_FORMULA` step 1: _On isole $x$:$3x = 17 - 5 = 12$._
- `WARN_HINT_IS_FORMULA` step 2: _On divise par $3$:$x = 12 \div 3 = 4$._
- `WARN_HINT_IS_FORMULA` step 3: _Vérification :$3 \times 4 + 5 = 17$ ✓_

### diagnostic_exos — 4EME / Équations (row 60, exo 2)
- **Q**: Résous $2x + 3 = 5x - 6$.
- **A**: $x = 3$
- `WARN_HINT_IS_FORMULA` step 3: _$x = 9 \div 3 = 3$._
- `WARN_HINT_IS_FORMULA` step 4: _Vérification :$2 \times 3 + 3 = 9$ et $5 \times 3 - 6 = 9$ ✓_

### diagnostic_exos — 4EME / Inéquations (row 61, exo 2)
- **Q**: Résoudre $-4x + 2 \geq 10$.
- **A**: x ≤ -2
- `WARN_HINT_IS_ANSWER` step 2: _Diviser par -4 (sens inverse) : x ≤ -2_
- `WARN_HINT_IS_ANSWER` step 3: _Résultat : x ≤ -2_
