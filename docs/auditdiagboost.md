# Audit Diagnostic & Boost — Exercices géométriques (6EME → 3EME)

> Audit du 17 mars 2026 — Focus : clarté des énoncés + pertinence d'une figure SVG.
> Règle : ajouter une figure quand elle aide la compréhension, SAUF si elle donne la réponse.
> Système existant : `autoDetectFigure(q, cat)` → `renderFig(fig)` → SVG inline.

---

## Légende

| Symbole | Signification |
|---|---|
| ✅ | Énoncé clair, pas de changement nécessaire |
| ⚠️ | Énoncé à reformuler (ambigu, trop abstrait, ou manque de contexte) |
| 🖼️ OUI | Une figure aiderait la compréhension |
| 🖼️ NON | La figure donnerait la réponse |
| 🖼️ INUTILE | Pas de dimension géométrique visuelle |

---

## 1. 6EME

### Géométrie (Diag: 2 / Boost: 10)

| Source | # | Lvl | Question | Clarté | Figure | Commentaire |
|---|---|---|---|---|---|---|
| Diag | 1 | 1 | « Le diamètre d'un cercle est 3 fois son rayon. Vrai ou faux ? » | ✅ | 🖼️ OUI — cercle avec rayon + diamètre annotés | La figure ne donne pas la réponse (il faut savoir que d=2r), mais aide à visualiser |
| Diag | 2 | 2 | « On trace le symétrique d'un triangle par rapport à un axe. Quelle propriété est conservée ? » | ⚠️ | 🖼️ NON — montrer le triangle + son symétrique donnerait la réponse (on verrait que les longueurs/angles sont conservés) | **Reformulation** : « Quand on trace le symétrique d'un triangle par rapport à une droite, qu'est-ce qui est conservé ? » → plus direct |
| Boost | 1 | 1 | « Combien de côtés possède un hexagone ? » | ✅ | 🖼️ NON — montrer l'hexagone donnerait la réponse (on compterait les côtés) | — |
| Boost | 2 | 1 | « Comment appelle-t-on un triangle dont les 3 côtés sont égaux ? » | ✅ | 🖼️ NON — la figure donnerait la réponse | — |
| Boost | 3 | 1 | « Deux droites qui ne se croisent jamais sont dites… » | ✅ | 🖼️ NON — la figure donnerait la réponse (on verrait les droites parallèles) | — |
| Boost | 4 | 1 | « Combien d'axes de symétrie possède un carré ? » | ✅ | 🖼️ NON — montrer les axes donnerait la réponse | — |
| Boost | 5 | 1 | « Un cercle a un rayon de 3 cm. Quel est son diamètre ? » | ✅ | 🖼️ OUI — cercle avec rayon annoté 3 cm | Aide la visualisation sans donner la réponse |
| Boost | 6 | 2 | « ABCD est un parallélogramme. Si AB=7 cm et BC=4 cm, combien vaut CD ? » | ⚠️ | 🖼️ OUI — parallélogramme ABCD avec AB et BC annotés | **Problème** : sans figure, un élève de 6ème peut ne pas savoir quels côtés sont opposés. La figure aide sans donner la réponse (il faut savoir que côtés opposés = égaux) |
| Boost | 7 | 2 | « Un triangle a des côtés de 3, 4 et 5 cm. Est-il rectangle ? » | ✅ | 🖼️ NON — montrer le triangle rectangle donnerait la réponse | — |
| Boost | 8 | 2 | « Le symétrique du point A(2;3) par rapport à l'axe des abscisses est… » | ⚠️ | 🖼️ OUI — repère avec point A et axe des abscisses marqué | **Problème** : un élève de 6ème peut ne pas connaître « axe des abscisses ». Reformuler : « …par rapport à l'axe horizontal (axe des x) » |
| Boost | 9 | 2 | « Dans un losange, les diagonales se coupent en formant des angles… » | ✅ | 🖼️ NON — montrer les angles droits donnerait la réponse | — |
| Boost | 10 | 2 | « ABCD rectangle, AB=6 cm, AD=8 cm. Longueur de la diagonale AC ? » | ✅ | 🖼️ OUI — rectangle ABCD avec côtés annotés, diagonale en pointillé | Aide la visualisation, la réponse nécessite un calcul (Pythagore) |

### Périmètres & Aires (Diag: 2 / Boost: 10)

| Source | # | Lvl | Question | Clarté | Figure | Commentaire |
|---|---|---|---|---|---|---|
| Diag | 1 | 1 | « Un rectangle a L=6 cm et l=4 cm. Son périmètre est : » | ✅ | 🖼️ OUI — rectangle avec dimensions annotées | Simple mais aide les 6èmes à visualiser |
| Diag | 2 | 2 | « Un triangle rectangle a deux côtés de l'angle droit mesurant 6 cm et 8 cm. Quelle est son aire ? » | ✅ | 🖼️ OUI — triangle rectangle avec les deux côtés annotés | Ne donne pas la réponse (il faut calculer b×h/2) |
| Boost | 1 | 1 | « Périmètre d'un carré de côté 9 cm ? » | ✅ | 🖼️ OUI — carré avec côté annoté | — |
| Boost | 2 | 1 | « Aire d'un rectangle de 6 cm par 4 cm ? » | ✅ | 🖼️ OUI — rectangle avec dimensions | — |
| Boost | 3 | 1 | « Périmètre d'un rectangle de 5 cm par 3 cm ? » | ✅ | 🖼️ OUI — rectangle avec dimensions | — |
| Boost | 4 | 1 | « Aire d'un carré de côté 7 cm ? » | ✅ | 🖼️ OUI — carré avec côté annoté | — |
| Boost | 5 | 1 | « Périmètre d'un cercle de rayon 5 cm ? » | ✅ | 🖼️ OUI — cercle avec rayon annoté | — |
| Boost | 6 | 2 | « Aire d'un triangle de base 10 cm et hauteur 6 cm ? » | ✅ | 🖼️ OUI — triangle avec base et hauteur annotées | Essentiel : les élèves confondent souvent base/hauteur |
| Boost | 7 | 2 | « Aire d'un disque de rayon 4 cm ? » | ✅ | 🖼️ OUI — disque avec rayon | — |
| Boost | 8 | 2 | « Périmètre d'un demi-cercle de diamètre 10 cm ? » | ⚠️ | 🖼️ OUI — demi-cercle avec diamètre annoté | **Problème** : l'élève ne sait pas forcément si le diamètre est inclus dans le périmètre. Reformuler : « Calcule le périmètre complet d'un demi-disque (demi-cercle + diamètre) de diamètre 10 cm. » |
| Boost | 9 | 2 | « Aire d'un terrain rectangulaire de 25 m par 40 m ? » | ✅ | 🖼️ INUTILE — contexte concret, pas besoin de figure | — |
| Boost | 10 | 2 | « Aire d'un parallélogramme de base 8 cm et hauteur 5 cm ? » | ✅ | 🖼️ OUI — parallélogramme avec base et hauteur annotées | Important : la hauteur n'est pas un côté, la figure clarifie |

### Angles (Diag: 2 / Boost: 10)

| Source | # | Lvl | Question | Clarté | Figure | Commentaire |
|---|---|---|---|---|---|---|
| Diag | 1 | 1 | « Un triangle a deux angles égaux à 65°. Quel est le troisième angle ? » | ✅ | 🖼️ OUI — triangle avec deux angles annotés 65° | Ne donne pas la réponse, aide à visualiser |
| Diag | 2 | 2 | « L'angle complémentaire de α est 30°. Quel est l'angle supplémentaire de α ? » | ⚠️ | 🖼️ INUTILE | **Problème majeur** : l'énoncé est confus. Il faut d'abord trouver α (= 60°) puis son supplémentaire (= 120°). Reformuler : « Un angle α a un complémentaire de 30°. Que vaut α, et quel est son supplémentaire ? » ou mieux : « Si α + 30° = 90°, que vaut 180° − α ? » |
| Boost | 1 | 1 | « Combien mesure un angle droit ? » | ✅ | 🖼️ NON — donnerait la réponse | — |
| Boost | 2 | 1 | « Un angle de 45° est un angle… » | ✅ | 🖼️ NON — donnerait la réponse | — |
| Boost | 3 | 1 | « Deux angles complémentaires ont une somme de… » | ✅ | 🖼️ INUTILE | Définition pure |
| Boost | 4 | 1 | « Quel est le complément d'un angle de 35° ? » | ✅ | 🖼️ INUTILE | Calcul pur |
| Boost | 5 | 1 | « Combien mesure un angle plat ? » | ✅ | 🖼️ NON — donnerait la réponse | — |
| Boost | 6 | 2 | « Quel est le supplément d'un angle de 115° ? » | ✅ | 🖼️ INUTILE | Calcul pur |
| Boost | 7 | 2 | « Quelle est la somme des angles d'un triangle ? » | ✅ | 🖼️ NON — donnerait la réponse | — |
| Boost | 8 | 2 | « Un triangle a deux angles de 50° et 70°. Le troisième mesure… » | ✅ | 🖼️ OUI — triangle avec deux angles annotés | — |
| Boost | 9 | 2 | « Deux droites se coupent. Un angle mesure 130°. L'angle opposé par le sommet mesure… » | ⚠️ | 🖼️ OUI — deux droites sécantes avec un angle annoté 130° | **Problème** : « opposé par le sommet » peut être flou pour un 6ème. La figure clarifie sans donner la réponse (il faut connaître la propriété) |
| Boost | 10 | 2 | « Quelle est la somme des angles d'un quadrilatère ? » | ✅ | 🖼️ INUTILE | Propriété connue |

### Symétrie Axiale (Diag: 2 / Boost: 10)

| Source | # | Lvl | Question | Clarté | Figure | Commentaire |
|---|---|---|---|---|---|---|
| Diag | 1 | 1 | « Quel est le symétrique du point A(3,2) par rapport à l'axe des ordonnées (x=0) ? » | ⚠️ | 🖼️ OUI — repère avec point A et axe vertical marqué | **Reformuler** : préciser « axe vertical (des ordonnées) » — « axe des ordonnées » est jargon pour un 6ème |
| Diag | 2 | 2 | « A(1,5) a pour symétrique A'(7,5). Quelle est l'équation de l'axe de symétrie ? » | ⚠️ | 🖼️ OUI — repère avec A, A' et axe en pointillé | **Reformuler** : « équation de l'axe » est du vocabulaire 3ème. Dire : « Sur quel axe vertical se fait la symétrie ? » ou « Quel est l'axe de symétrie ? (ex: x = …) » |
| Boost | 1 | 1 | « Combien d'axes de symétrie possède un carré ? » | ✅ | 🖼️ NON — donnerait la réponse | Doublon avec Géométrie Boost #4 |
| Boost | 2 | 1 | « Symétrique de C(5,0) par rapport à l'axe des ordonnées ? » | ⚠️ | 🖼️ OUI — repère avec C et axe | Même problème « axe des ordonnées » |
| Boost | 3 | 1 | « Symétrique de D(0,-4) par rapport à l'axe des abscisses ? » | ⚠️ | 🖼️ OUI — repère avec D et axe | Même problème « axe des abscisses » |
| Boost | 4 | 1 | « Un triangle isocèle possède combien d'axes de symétrie ? » | ✅ | 🖼️ NON — donnerait la réponse | — |
| Boost | 5 | 1 | « Vrai ou faux : un trapèze quelconque possède toujours un axe de symétrie. » | ✅ | 🖼️ NON — donnerait la réponse | — |
| Boost | 6 | 2 | « Le symétrique de E(-2,4) par rapport à la droite x=3 est : » | ⚠️ | 🖼️ OUI — repère avec E, droite x=3 marquée | **Important** : la droite x=3 est abstraite sans figure. La figure est quasi-indispensable ici |
| Boost | 7 | 2 | « Sur un quadrillage, si M est à 4 carreaux à droite d'un axe… » | ✅ | 🖼️ OUI — quadrillage avec M et axe | Facile à visualiser mais la figure confirme |
| Boost | 8 | 2 | « La symétrie axiale conserve-t-elle les longueurs ? » | ✅ | 🖼️ INUTILE | Propriété pure |
| Boost | 9 | 2 | « Si F(4,2) a pour symétrique F'(4,-6) par rapport à un axe horizontal… » | ✅ | 🖼️ OUI — repère avec F et F' | — |
| Boost | 10 | 2 | « Combien d'axes de symétrie possède un pentagone régulier ? » | ✅ | 🖼️ NON — donnerait la réponse | — |

### Volumes (Diag: 2 / Boost: 10)

| Source | # | Lvl | Question | Clarté | Figure | Commentaire |
|---|---|---|---|---|---|---|
| Diag | 1 | 1 | « Volume du pavé droit de dimensions 4×5×6 cm. » | ✅ | 🖼️ OUI — pavé droit 3D avec dimensions annotées | type `cube` existant dans le système de figures |
| Diag | 2 | 2 | « Un cylindre a un rayon de 4 cm et un volume de 200,96 cm³. Quelle est sa hauteur ? » | ✅ | 🖼️ OUI — cylindre avec rayon annoté | — |
| Boost | 1 | 1 | « Volume d'un pavé droit de 8×2×5 cm. » | ✅ | 🖼️ OUI — pavé droit | — |
| Boost | 2 | 1 | « Convertir 3000 cm³ en litres. » | ✅ | 🖼️ INUTILE | Conversion pure |
| Boost | 3 | 1 | « Un prisme droit a une base de 20 cm² et une hauteur de 7 cm. Volume ? » | ⚠️ | 🖼️ OUI — prisme droit avec base et hauteur | **Problème** : « base de 20 cm² » est abstrait — quelle forme ? Reformuler : « Un prisme droit a une aire de base de 20 cm² et une hauteur de 7 cm. » |
| Boost | 4 | 1 | « Volume d'un cube d'arête 3 cm ? » | ✅ | 🖼️ OUI — cube avec arête annotée | — |
| Boost | 5 | 1 | « Volume d'un cylindre de rayon 1 cm et de hauteur 10 cm. » | ✅ | 🖼️ OUI — cylindre avec dimensions | — |
| Boost | 6 | 2 | « Réservoir cubique d'arête 10 cm rempli à 3/5. Volume d'eau ? » | ✅ | 🖼️ OUI — cube avec niveau d'eau | — |
| Boost | 7 | 2 | « Convertir 0,3 m³ en dm³. » | ✅ | 🖼️ INUTILE | Conversion pure |
| Boost | 8 | 2 | « Pavé droit, volume 90 cm³, largeur 3 cm, hauteur 5 cm. Longueur ? » | ✅ | 🖼️ OUI — pavé avec 2 dimensions annotées, la 3e en « ? » | — |
| Boost | 9 | 2 | « Cylindre rayon 2 cm, volume 100,48 cm³. Hauteur ? » | ✅ | 🖼️ OUI — cylindre avec rayon annoté | — |
| Boost | 10 | 2 | « Contenance en litres d'une piscine de 10×4×1,5 m ? » | ✅ | 🖼️ INUTILE | Contexte concret suffisant |

### Agrandissement & Réduction (Diag: 2 / Boost: 10)

| Source | # | Lvl | Question | Clarté | Figure | Commentaire |
|---|---|---|---|---|---|---|
| Diag | 1 | 1 | « Un segment de 6 cm est agrandi avec k=4. Nouvelle longueur ? » | ✅ | 🖼️ INUTILE | Calcul pur |
| Diag | 2 | 2 | « Carte à l'échelle 1/50 000, deux points à 6 cm. Distance réelle en km ? » | ✅ | 🖼️ INUTILE | — |
| Boost | 1-5 | 1 | Tous calculs k × longueur ou échelle | ✅ | 🖼️ INUTILE | Calculs purs |
| Boost | 6-10 | 2 | Échelles + aires agrandies | ✅ | 🖼️ INUTILE | Calculs purs |

### Conversions d'Unités (Diag: 2 / Boost: 10)

Aucune dimension géométrique visuelle. Tous ✅ clarté. 🖼️ INUTILE partout.

### Puissances de 10 (Diag: 2 / Boost: 10)

Aucune dimension géométrique. Tous ✅. 🖼️ INUTILE.

---

## 2. 5EME

### Pythagore (Diag: 2 / Boost: 10)

| Source | # | Lvl | Question | Clarté | Figure | Commentaire |
|---|---|---|---|---|---|---|
| Diag | 1 | 1 | « Triangle rectangle, côtés 3 et 4 cm. Hypoténuse ? » | ✅ | 🖼️ OUI — triangle rectangle avec 2 côtés annotés, hypoténuse en « ? » | Ne donne pas la réponse |
| Diag | 2 | 2 | « Hypoténuse 13 cm, un côté 5 cm. L'autre côté ? » | ✅ | 🖼️ OUI — triangle rectangle avec hypoténuse et un côté annotés | — |
| Boost | 1 | 1 | « Triangle rectangle : côtés 3 et 4 cm. Hypoténuse ? » | ✅ | 🖼️ OUI — tri_rect | Quasi-doublon du diag mais niveaux différents |
| Boost | 2 | 1 | « Triangle rectangle : côtés 6 et 8 cm. Hypoténuse ? » | ✅ | 🖼️ OUI | — |
| Boost | 3 | 1 | « Hypoténuse = 13, un côté = 5. L'autre ? » | ✅ | 🖼️ OUI | — |
| Boost | 4 | 1 | « $5^2 + 12^2 = ?$. Quelle est l'hypoténuse ? » | ⚠️ | 🖼️ INUTILE | **Problème** : la question mélange deux choses. Reformuler : « Calcule $5^2 + 12^2$ puis déduis l'hypoténuse du triangle rectangle de côtés 5 et 12 cm. » ou simplement « Hypoténuse du triangle rectangle de côtés 5 et 12 cm ? » |
| Boost | 5 | 1 | « Hypoténuse = 10, un côté = 6. L'autre ? » | ✅ | 🖼️ OUI | — |
| Boost | 6 | 2 | « Triangle rectangle : côtés 9 et 12 cm. Hypoténuse ? » | ✅ | 🖼️ OUI | — |
| Boost | 7 | 2 | « Le triangle 7, 24, 25 est-il rectangle ? » | ✅ | 🖼️ NON — la figure donnerait la réponse (montrerait l'angle droit) | — |
| Boost | 8 | 2 | « Un mât de 8 m est fixé par un câble ancré à 6 m du pied. Longueur du câble ? » | ⚠️ | 🖼️ OUI — schéma mât + sol + câble en triangle rectangle | **Important** : sans figure, l'élève peut ne pas voir que c'est un triangle rectangle. La figure est quasi-indispensable. Type possible : `tri_rect` |
| Boost | 9 | 2 | « Hypoténuse = 17, un côté = 8. L'autre ? » | ✅ | 🖼️ OUI | — |
| Boost | 10 | 2 | « Le triangle 5, 6, 8 est-il rectangle ? » | ✅ | 🖼️ NON — la figure donnerait la réponse | — |

### Symétrie Centrale (Diag: 2 / Boost: 10)

| Source | # | Lvl | Question | Clarté | Figure | Commentaire |
|---|---|---|---|---|---|---|
| Diag | 1 | 1 | « Symétrique de A(3,-2) par rapport à O(0,0) » | ✅ | 🖼️ OUI — repère avec A et O | — |
| Diag | 2 | 2 | « A(1,4) et O(3,2) est le centre. Trouver A'. » | ✅ | 🖼️ OUI — repère avec A et O | — |
| Boost | 1 | 1 | « Symétrique de P(4,6) par rapport à O(0,0) » | ✅ | 🖼️ OUI — repère | — |
| Boost | 2 | 1 | « ABCD parallélogramme de centre O. Symétrique de B par rapport à O ? » | ⚠️ | 🖼️ OUI — parallélogramme ABCD avec centre O | **Important** : sans figure, il faut connaître la disposition des sommets d'un parallélogramme. Figure quasi-indispensable mais ne donne pas la réponse (il faut savoir la propriété) |
| Boost | 3 | 1 | « Symétrique de Q(-7,0) par rapport à O(0,0) » | ✅ | 🖼️ OUI — repère | — |
| Boost | 4 | 1 | « V/F : le triangle équilatéral a un centre de symétrie. » | ✅ | 🖼️ NON — montrer le triangle donnerait un indice trop fort | — |
| Boost | 5 | 1 | « Si O est le centre de symétrie, quelle rotation ramène la figure sur elle-même ? » | ✅ | 🖼️ INUTILE | Propriété pure |
| Boost | 6 | 2 | « R(2,1) et O(5,4) centre. Trouver R'. » | ✅ | 🖼️ OUI — repère | — |
| Boost | 7 | 2 | « T(-3,5) et T'(7,-1). Trouver le centre O. » | ✅ | 🖼️ OUI — repère avec T et T' | — |
| Boost | 8 | 2 | « La symétrie centrale conserve-t-elle les distances ? » | ✅ | 🖼️ INUTILE | Propriété pure |
| Boost | 9 | 2 | « Un hexagone régulier possède-t-il un centre de symétrie ? » | ✅ | 🖼️ NON — montrer l'hexagone avec son centre donnerait la réponse | — |
| Boost | 10 | 2 | « U(0,3) et U'(4,-1). Trouver O. » | ✅ | 🖼️ OUI — repère | — |

### Transformations (Diag: 2 / Boost: 10)

| Source | # | Lvl | Question | Clarté | Figure | Commentaire |
|---|---|---|---|---|---|---|
| Diag | 1 | 1 | « A(1,3) translaté par $\vec{v}$(4,-2). Coordonnées de A' ? » | ✅ | 🖼️ OUI — repère avec A et vecteur | — |
| Diag | 2 | 2 | « Symétrie centrale de M(3,-2), puis translation par $\vec{v}$(1,4). Image finale ? » | ⚠️ | 🖼️ OUI — repère avec étapes | **Problème** : deux transformations enchaînées, l'énoncé est dense. Reformuler : « Le point M(3;−2) subit d'abord une symétrie de centre O(0;0), puis une translation de vecteur $\vec{v}$(1;4). Quelles sont les coordonnées de l'image finale ? » |
| Boost | 1 | 1 | « P(0,5) translaté par $\vec{u}$(2,-3). Image P' ? » | ✅ | 🖼️ OUI — repère | — |
| Boost | 2 | 1 | « Quelle transformation fait tourner une figure autour d'un point fixe ? » | ✅ | 🖼️ NON — donnerait la réponse | — |
| Boost | 3 | 1 | « Symétrie centrale de centre O(0,0), image de Q(-4,2) ? » | ✅ | 🖼️ OUI | — |
| Boost | 4 | 1 | « M(6,4) subit une rotation de 180° autour de O(0,0). Image ? » | ✅ | 🖼️ OUI — repère avec M | — |
| Boost | 5 | 1 | « Une translation conserve-t-elle l'orientation ? » | ✅ | 🖼️ INUTILE | Propriété pure |
| Boost | 6 | 2 | « N(2,1) translaté par $\vec{w}$(-3,2), puis rotation 90° anti-horaire. Position finale ? » | ⚠️ | 🖼️ OUI — repère étape par étape | **Problème** : même souci que Diag #2, très dense. Bien séparer les deux étapes dans l'énoncé |
| Boost | 7 | 2 | « Carré périmètre 24 cm, symétrie axiale. Périmètre image ? » | ✅ | 🖼️ INUTILE | Propriété pure (conservation) |
| Boost | 8 | 2 | « Symétrie centrale centre I(1,2), image de R(3,5) ? » | ✅ | 🖼️ OUI — repère | — |
| Boost | 9 | 2 | « Point T à 5 cm du centre de rotation. Distance après rotation ? » | ✅ | 🖼️ INUTILE | Propriété pure |
| Boost | 10 | 2 | « Triangle ABC translaté par $\vec{v}$(-2,1). Coordonnées de B' ? » | ✅ | 🖼️ OUI — repère avec triangle | — |

### Triangles Semblables (Diag: 2 / Boost: 10)

| Source | # | Lvl | Question | Clarté | Figure | Commentaire |
|---|---|---|---|---|---|---|
| Diag | 1 | 1 | « Triangle ABC semblable à DEF, k=2. Si AB=5, DE=? » | ✅ | 🖼️ OUI — deux triangles semblables avec AB annoté | Aide à visualiser le rapport |
| Diag | 2 | 2 | « Deux triangles semblables, aires 16 et 36 cm². Rapport k ? » | ✅ | 🖼️ INUTILE | Calcul pur |
| Boost | 1-5 | 1 | Rapports, côtés homologues, définitions | ✅ | 🖼️ INUTILE pour la plupart | — |
| Boost | 6 | 2 | « Côtés homologues 6 et 9 cm. Rapport des aires ? » | ✅ | 🖼️ INUTILE | Calcul pur |
| Boost | 7 | 2 | « Objet 1,5 m, ombre 2 m. Bâtiment, ombre 30 m. Hauteur ? » | ⚠️ | 🖼️ OUI — schéma deux triangles semblables (soleil, ombres) | **Important** : sans figure, l'élève peut ne pas voir les triangles semblables. Type : `thales` ou `similar_tri` |
| Boost | 8-9 | 2 | Rapports périmètres/aires | ✅ | 🖼️ INUTILE | — |
| Boost | 10 | 2 | « D sur [AB] avec AD/AB=2/5, E sur [AC] avec AE/AC=2/5. DE parallèle à BC ? » | ⚠️ | 🖼️ OUI — triangle ABC avec D et E positionnés | **Quasi-indispensable** : sans figure, la configuration est très abstraite |

### Racines Carrées — exercices géo (Boost #7)

| Source | # | Lvl | Question | Clarté | Figure | Commentaire |
|---|---|---|---|---|---|---|
| Boost | 7 | 2 | « Triangle rectangle, côtés 5 et 12 cm. Hypoténuse ? » | ✅ | 🖼️ OUI — triangle rectangle | Identique à un exo Pythagore |

---

## 3. 4EME

### Pythagore (Diag: 2 / Boost: 10)

| Source | # | Lvl | Question | Clarté | Figure | Commentaire |
|---|---|---|---|---|---|---|
| Diag | 1 | 1 | « Triangle côtés 5, 12, 13 cm. Est-il rectangle ? » | ✅ | 🖼️ NON — la figure montrerait l'angle droit | — |
| Diag | 2 | 2 | « Hypoténuse 10, un côté 6. L'autre ? » | ✅ | 🖼️ OUI — triangle rectangle | — |
| Boost | 1-5 | 1 | Calculs hypoténuse / côtés / définition | ✅ | 🖼️ OUI pour #1,2,4 (triangles avec dimensions) / NON pour #5 (définition) / INUTILE pour #3 (calcul pur) | — |
| Boost | 6 | 2 | « A(1;2) et B(4;6). Distance AB ? » | ✅ | 🖼️ OUI — repère avec A et B | — |
| Boost | 7 | 2 | « Le triangle 8, 15, 17 est-il rectangle ? » | ✅ | 🖼️ NON — donnerait la réponse | — |
| Boost | 8 | 2 | « Diagonale d'un rectangle 9×12 cm ? » | ✅ | 🖼️ OUI — rectangle avec diagonale en pointillé | — |
| Boost | 9 | 2 | « Échelle de 6 m contre un mur, pied à 3,6 m. Hauteur atteinte ? » | ⚠️ | 🖼️ OUI — schéma échelle/mur/sol en triangle rectangle | **Quasi-indispensable** : même problème qu'en 5EME. Sans figure, l'élève peut ne pas identifier le triangle rectangle |
| Boost | 10 | 2 | « A(0;0), B(3;0), C(3;4). Rectangle en quel sommet ? » | ✅ | 🖼️ OUI — repère avec les 3 points | Aide beaucoup à visualiser |

### Homothétie (Diag: 2 / Boost: 10)

| Source | # | Lvl | Question | Clarté | Figure | Commentaire |
|---|---|---|---|---|---|---|
| Diag | 1 | 1 | « Homothétie centre O, k=4, OA=3. OA'=? » | ✅ | 🖼️ OUI — O, A et A' alignés avec distances | — |
| Diag | 2 | 2 | « Homothétie k=2, triangle aire 6 cm². Aire image ? » | ✅ | 🖼️ INUTILE | Calcul pur (k² × aire) |
| Boost | 1 | 1 | « k=5, OA=2. OA'=? » | ✅ | 🖼️ OUI — O, A, A' alignés | — |
| Boost | 2 | 1 | « k=1/3, segment 12 cm. Image ? » | ✅ | 🖼️ INUTILE | Calcul pur |
| Boost | 3 | 1 | « k=2 : agrandissement ou réduction ? » | ✅ | 🖼️ NON — donnerait la réponse | — |
| Boost | 4 | 1 | « L'homothétie conserve-t-elle la forme ? » | ✅ | 🖼️ NON — donnerait la réponse | — |
| Boost | 5 | 1 | « k=-1. OA'=? » | ⚠️ | 🖼️ OUI — O, A et A' avec A' de l'autre côté | **Problème** : le rapport négatif est un concept difficile. La figure aide sans donner la réponse (l'élève doit comprendre que k<0 = côté opposé) |
| Boost | 6 | 2 | « Centre O(0,0), k=3. Image de B(2,-1) ? » | ✅ | 🖼️ OUI — repère | — |
| Boost | 7 | 2 | « Cercle rayon 6, k=1/2. Rayon image ? » | ✅ | 🖼️ OUI — deux cercles concentriques | — |
| Boost | 8 | 2 | « Carré aire 16 cm², k=3. Aire image ? » | ✅ | 🖼️ INUTILE | Calcul pur |
| Boost | 9 | 2 | « O, A, A' alignés, OA=4, OA'=6, même côté. k=? » | ✅ | 🖼️ OUI — O, A, A' avec distances | — |
| Boost | 10 | 2 | « Périmètre 12→20 cm. k=? » | ✅ | 🖼️ INUTILE | Calcul pur |

### Sections de Solides (Diag: 2 / Boost: 10)

| Source | # | Lvl | Question | Clarté | Figure | Commentaire |
|---|---|---|---|---|---|---|
| Diag | 1 | 1 | « On coupe un cube par un plan parallèle à une face. Forme de la section ? » | ✅ | 🖼️ OUI — cube avec plan de coupe en pointillé | **Important** : « plan parallèle à une face » est abstrait sans figure. La figure ne donne pas la réponse car la forme n'est pas évidente pour un 4ème |
| Diag | 2 | 2 | « Pyramide base carrée côté 9 cm, coupée au tiers de la hauteur depuis le sommet. Côté section ? » | ⚠️ | 🖼️ OUI — pyramide avec plan de coupe et dimensions | **Reformuler** : « …au tiers de la hauteur en partant du sommet » → ajouter « en partant du sommet » pour clarifier. La figure est quasi-indispensable |
| Boost | 1 | 1 | « Plan coupe un cylindre parallèlement à sa base. Forme ? » | ✅ | 🖼️ OUI — cylindre avec plan de coupe | — |
| Boost | 2 | 1 | « Sphère coupée par un plan passant par son centre. Section ? » | ✅ | 🖼️ OUI — sphère avec plan | — |
| Boost | 3 | 1 | « Prisme droit base carrée, plan parallèle à la base. Section ? » | ✅ | 🖼️ OUI — prisme avec plan | — |
| Boost | 4 | 1 | « Pavé 6×4×3, plan parallèle à la face 6×4. Section ? » | ✅ | 🖼️ OUI — pavé avec plan de coupe | — |
| Boost | 5 | 1 | « Cylindre, plan perpendiculaire à l'axe. Section ? » | ✅ | 🖼️ OUI — cylindre avec plan | Doublon conceptuel avec Boost #1 |
| Boost | 6 | 2 | « Pyramide base carrée côté 12, coupée à mi-hauteur depuis sommet. Côté ? » | ✅ | 🖼️ OUI — pyramide avec plan et dimensions | — |
| Boost | 7 | 2 | « Sphère rayon 10, plan à 6 cm du centre. Rayon section ? » | ✅ | 🖼️ OUI — coupe de sphère avec distance au centre | **Important** : sans figure, la relation Pythagore sur la coupe de sphère est très abstraite |
| Boost | 8 | 2 | « Pyramide base carrée, plan parallèle à mi-hauteur. Forme ? » | ✅ | 🖼️ NON — montrer la section carrée donnerait la réponse | — |
| Boost | 9 | 2 | « Pyramide côté 10, hauteur 20, plan à 5 cm du sommet. Côté ? » | ✅ | 🖼️ OUI — pyramide avec dimensions et plan de coupe | — |
| Boost | 10 | 2 | « Pyramide côté 8, rapport k=3/4 depuis sommet. Aire section ? » | ⚠️ | 🖼️ OUI — pyramide avec plan | **Problème** : « rapport k = 3/4 depuis le sommet » est ambigu — c'est le rapport de la hauteur de coupe sur la hauteur totale ? Reformuler : « …coupée à 3/4 de la hauteur en partant du sommet » |

### Fonctions Linéaires — pas de géométrie visuelle

---

## 4. 3EME

### Théorème de Thalès (Diag: 2 / Boost: 10)

| Source | # | Lvl | Question | Clarté | Figure | Commentaire |
|---|---|---|---|---|---|---|
| Diag | 1 | 1 | « (MN)∥(BC). AM=4, MB=2, MN=6. BC=? » | ⚠️ | 🖼️ OUI — triangle avec droites parallèles | **CRITIQUE** : sans figure, la configuration de Thalès est incompréhensible. L'élève ne sait pas où sont M et N. **Figure indispensable** type `thales` |
| Diag | 2 | 2 | « E sur [AB], D sur [AC]. AE=3, AB=9, AD=2, AC=6. (ED)∥(BC) ? » | ⚠️ | 🖼️ OUI — triangle ABC avec E et D positionnés | **CRITIQUE** : même problème — sans figure, la configuration est abstraite. **Figure indispensable** |
| Boost | 1 | 1 | « AB=6, AC=9, AM=4, (MN)∥(BC). AN=? » | ⚠️ | 🖼️ OUI | **CRITIQUE** : TOUS les exos Thalès nécessitent une figure |
| Boost | 2 | 1 | « AB=10, AM=4, AC=15. AN=? » | ⚠️ | 🖼️ OUI | Même problème |
| Boost | 3 | 1 | « AB=8, AM=2, MN=3, (MN)∥(BC). BC=? » | ⚠️ | 🖼️ OUI | Même problème |
| Boost | 4 | 1 | « AM=3, AB=9, AN=5. AC=? » | ⚠️ | 🖼️ OUI | Même problème |
| Boost | 5 | 1 | « Deux droites coupées par des parallèles : segments 4 et 6, 8 de l'autre. Manquant ? » | ⚠️ | 🖼️ OUI | **CRITIQUE** : sans figure, l'exercice est quasi-impossible à comprendre |
| Boost | 6 | 2 | « AB=12, AM=4, BC=9, (MN)∥(BC). MN=? » | ⚠️ | 🖼️ OUI | — |
| Boost | 7 | 2 | « AM=3, AB=7,5, AN=4, AC=10. (MN)∥(BC) ? » | ⚠️ | 🖼️ OUI | — |
| Boost | 8 | 2 | « Agrandissement k=2,5. AB=4, A'B'=? » | ✅ | 🖼️ INUTILE | Calcul pur |
| Boost | 9 | 2 | « AM=5, MB=7, AN=10, NC=14. (MN)∥(BC) ? » | ⚠️ | 🖼️ OUI | — |
| Boost | 10 | 2 | « Ombre : poteau 6 m, ombre 4 m. Arbre : ombre 10 m. Hauteur ? » | ⚠️ | 🖼️ OUI — schéma soleil/poteau/arbre/ombres | **Important** : sans figure, les triangles semblables sont invisibles |

### Trigonométrie (Diag: 2 / Boost: 10)

| Source | # | Lvl | Question | Clarté | Figure | Commentaire |
|---|---|---|---|---|---|---|
| Diag | 1 | 1 | « Triangle rectangle en B, AB=4, AC=5 (hypoténuse). cos(Â)=? » | ⚠️ | 🖼️ OUI — triangle rectangle en B avec côtés annotés et angle  | **CRITIQUE** : sans figure, l'élève ne sait pas quel côté est adjacent/opposé à Â. **Figure indispensable** type `tri_trigo` |
| Diag | 2 | 2 | « cos(Â)=0,6, hypoténuse AC=10. AB (adjacent à Â)=? » | ✅ | 🖼️ OUI — triangle rectangle avec angle et hypoténuse annotés | La figure clarifie énormément la situation |
| Boost | 1 | 1 | « Hypoténuse 10, angle 30°. Côté opposé ? » | ⚠️ | 🖼️ OUI — triangle rectangle avec angle et hypoténuse | **Problème** : « côté opposé » à quoi ? À l'angle de 30° — mais l'énoncé ne le dit pas explicitement. Reformuler : « Dans un triangle rectangle, l'hypoténuse mesure 10 cm et un angle aigu vaut 30°. Quel est le côté opposé à cet angle ? » |
| Boost | 2 | 1 | « cos(60°) = ? » | ✅ | 🖼️ INUTILE | Valeur remarquable |
| Boost | 3 | 1 | « Côté opposé = 6, adjacent = 6. L'angle vaut… » | ⚠️ | 🖼️ OUI — triangle rectangle avec côtés annotés | **Problème** : opposé et adjacent à quel angle ? L'énoncé suppose que l'élève sait. **Reformuler** : « Dans un triangle rectangle, le côté opposé à l'angle α mesure 6 cm et le côté adjacent mesure 6 cm. Que vaut α ? » |
| Boost | 4 | 1 | « Adjacent = 8, hypoténuse = 10. cos(α) = ? » | ⚠️ | 🖼️ OUI — triangle rectangle | Même problème : adjacent à quel angle ? Figure indispensable |
| Boost | 5 | 1 | « sin(90°) = ? » | ✅ | 🖼️ INUTILE | Valeur remarquable |
| Boost | 6 | 2 | « Angle 40°, hypoténuse 12. Côté adjacent ? » | ⚠️ | 🖼️ OUI — triangle rectangle | Même problème — reformuler comme Boost #1 |
| Boost | 7 | 2 | « Opposé = 7, adjacent = 7. L'angle vaut… » | ⚠️ | 🖼️ OUI | Doublon conceptuel de Boost #3 |
| Boost | 8 | 2 | « sin(α)=3/5. Calculer cos(α). » | ✅ | 🖼️ OUI — triangle rectangle 3-4-5 | Aide à comprendre la relation |
| Boost | 9 | 2 | « Distance 20 m, angle d'élévation 35°. Hauteur de l'arbre ? » | ⚠️ | 🖼️ OUI — schéma observateur/arbre/angle d'élévation | **Important** : « angle d'élévation » est un terme technique. Figure quasi-indispensable |
| Boost | 10 | 2 | « Hypoténuse = 13, opposé = 5. L'angle vaut… » | ⚠️ | 🖼️ OUI — triangle rectangle | Même problème : opposé à quel angle ? |

---

## Synthèse des problèmes identifiés

### Problèmes critiques (à corriger avant lancement)

| # | Niveau | Chapitre | Problème | Action |
|---|---|---|---|---|
| 1 | 3EME | **Thalès** (Diag + Boost : 12 exos) | Aucun exo n'a de figure — la configuration est incompréhensible sans schéma | **Ajouter une figure `thales` à TOUS les exos** (sauf Boost #8 calcul pur) |
| 2 | 3EME | **Trigonométrie** (Diag + Boost : 12 exos) | « opposé / adjacent » non rapportés à un angle précis + aucune figure | **Reformuler les énoncés** + **ajouter figure `tri_trigo`** à tous les exos géométriques |
| 3 | 4EME | **Sections Solides** (Diag + Boost : 12 exos) | « plan parallèle à la base » est abstrait sans figure 3D | **Ajouter figures 3D** type `pyramid`, `cylinder`, `sphere`, `cube` |

### Problèmes importants (à corriger idéalement)

| # | Niveau | Chapitre | Problème | Action |
|---|---|---|---|---|
| 4 | 6EME | **Symétrie Axiale** | « axe des ordonnées / abscisses » = jargon pour un 6ème | **Reformuler** : « axe vertical (des ordonnées) » |
| 5 | 5EME | **Pythagore** Boost #8 | « Mât de 8 m fixé par un câble à 6 m du pied » — triangle rectangle invisible | **Ajouter figure** type `tri_rect` |
| 6 | 4EME | **Pythagore** Boost #9 | « Échelle contre un mur » — même problème | **Ajouter figure** |
| 7 | 5EME | **Triangles Semblables** Boost #7 | Ombre/soleil — triangles semblables invisibles sans schéma | **Ajouter figure** |
| 8 | 5EME | **Triangles Semblables** Boost #10 | Configuration D/E sur triangle — abstraite | **Ajouter figure** |

### Problèmes mineurs (polish)

| # | Niveau | Chapitre | Problème | Action |
|---|---|---|---|---|
| 9 | 6EME | Angles Diag #2 | Énoncé confus (complémentaire → supplémentaire en 2 étapes) | Reformuler |
| 10 | 6EME | Périmètres Boost #8 | « Périmètre d'un demi-cercle » — ambigu (inclut le diamètre ?) | Reformuler : « périmètre complet du demi-disque » |
| 11 | 6EME | Volumes Boost #3 | « base de 20 cm² » — quelle forme ? | Dire « aire de base = 20 cm² » |
| 12 | 5EME | Pythagore Boost #4 | « $5^2+12^2=?$. Hypoténuse ? » — mélange deux questions | Reformuler en une seule question |
| 13 | 5EME | Transformations Diag #2 et Boost #6 | Deux transformations enchaînées — dense | Séparer les étapes dans l'énoncé |
| 14 | 4EME | Sections Diag #2 et Boost #10 | « au tiers de la hauteur » / « rapport k=3/4 » — ambigu (depuis le sommet ou la base ?) | Toujours préciser « en partant du sommet » |
| 15 | 3EME | Thalès Boost #5 | « Deux droites coupées par des parallèles » — très abstrait | Reformuler + figure obligatoire |
| 16 | 3EME | Systèmes Boost #9 et #10 | **Doublon exact** (même système 2x+y=7, x+2y=8 deux fois) | **Supprimer le doublon** et remplacer par un nouvel exercice |

---

## Comptage : exercices nécessitant une figure

| Niveau | Chapitre | Nb exos avec figure recommandée | Nb exos figure = donnerait réponse |
|---|---|---|---|
| 6EME | Géométrie | 4 / 12 | 6 / 12 |
| 6EME | Périmètres_Aires | 9 / 12 | 0 |
| 6EME | Angles | 2 / 12 | 4 / 12 |
| 6EME | Symétrie_Axiale | 6 / 12 | 3 / 12 |
| 6EME | Volumes | 8 / 12 | 0 |
| 5EME | Pythagore | 9 / 12 | 2 / 12 |
| 5EME | Symétrie_Centrale | 7 / 12 | 2 / 12 |
| 5EME | Transformations | 6 / 12 | 1 / 12 |
| 5EME | Triangles_Semblables | 3 / 12 | 0 |
| 4EME | Pythagore | 7 / 12 | 2 / 12 |
| 4EME | Homothétie | 5 / 12 | 2 / 12 |
| 4EME | Sections_Solides | 8 / 12 | 1 / 12 |
| 3EME | Thalès | 10 / 12 | 0 |
| 3EME | Trigonométrie | 9 / 12 | 0 |
| **TOTAL** | | **93 / 168** | **23 / 168** |

> **93 exercices** bénéficieraient d'une figure SVG.
> **23 exercices** ne doivent PAS avoir de figure (réponse visible).
> **52 exercices** n'ont pas besoin de figure (calculs purs, propriétés).

---

## Priorité d'implémentation des figures

### P0 — Indispensable (les premières minutes de l'app)

1. **3EME Thalès** — 10 exos sans figure = incompréhensible → `thales`
2. **3EME Trigonométrie** — 9 exos → `tri_trigo`
3. **4EME Sections Solides** — 8 exos → `pyramid`, `cylinder`, `sphere`, `cube`

### P1 — Très important (améliore significativement la clarté)

4. **5EME Pythagore** — 9 exos → `tri_rect`
5. **4EME Pythagore** — 7 exos → `tri_rect`
6. **6EME Périmètres/Aires** — 9 exos → `rect`, `triangle`, `circle`
7. **6EME Volumes** — 8 exos → `cube`, `cylinder`

### P2 — Utile (améliore l'expérience)

8. **5EME/6EME Symétrie** — 13 exos → `repere` (repère avec points)
9. **5EME Transformations** — 6 exos → `repere`
10. **4EME Homothétie** — 5 exos → `homothety`
11. **6EME Géométrie** — 4 exos → `circle`, `rect`

---

## Reformulations prioritaires

### 3EME Trigonométrie — pattern systématique

**Avant** : « Côté opposé = 6, adjacent = 6. L'angle vaut… »
**Après** : « Dans un triangle rectangle en C, le côté opposé à l'angle $\hat{A}$ mesure 6 cm et le côté adjacent à $\hat{A}$ mesure 6 cm. Que vaut l'angle $\hat{A}$ ? »

### 6EME Symétrie Axiale — vocabulaire

**Avant** : « par rapport à l'axe des ordonnées »
**Après** : « par rapport à l'axe vertical (axe des ordonnées, la droite x = 0) »

### 3EME Thalès — contextualisation

**Avant** : « AB=6, AC=9, AM=4, (MN)∥(BC). AN=? »
**Après** : « Dans le triangle ABC, le point M est sur le segment [AB] et le point N est sur le segment [AC], avec (MN) parallèle à (BC). On donne AB = 6, AC = 9 et AM = 4. Calculer AN. »

---

## Bug trouvé

**3EME Systèmes_Équations Boost #9 et #10** : exercices identiques (même système `2x+y=7, x+2y=8`, même réponse `x=2, y=3`, mêmes options). → **Remplacer le #10 par un exercice différent.**
