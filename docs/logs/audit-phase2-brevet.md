# Audit Phase 2 — 120 exercices Brevet 3EME

> Date : 2026-03-28
> Auditeur : Monsieur Exos (Claude Opus 4.6)
> Fichiers : Equations_Brevet, Fonctions_Brevet, Scratch_Brevet, Auto_Calcul, Auto_Litteral, Auto_Geometrie

---

## Synthese globale

| Fichier | Exos | Bloquants | Warnings | Verdict |
|---|---|---|---|---|
| Equations_Brevet | 20 | 1 | 3 | A CORRIGER |
| Fonctions_Brevet | 20 | 1 | 3 | A CORRIGER |
| Scratch_Brevet | 20 | 0 | 2 | OK (warnings) |
| Auto_Calcul | 20 | 1 | 2 | A CORRIGER |
| Auto_Litteral | 20 | 0 | 1 | OK (warning) |
| Auto_Geometrie | 20 | 0 | 3 | OK (warnings) |

**Total : 3 bloquants, 14 warnings sur 120 exercices.**

---

## 1. Equations_Brevet (20 exos)

### BLOQUANTS

**EQ-B1 : Exo 8 (perimetre rectangle) — question ne correspond pas a la reponse**
- La question demande "quelle equation obtient-on ?" (mise en equation)
- La reponse est `$2(x + 5) + 2x = 34$` ce qui est correct
- MAIS le step 2 donne la RESOLUTION complete `$4x + 10 = 34$, donc $4x = 24$ et $x = ?$`
- Le step donne beaucoup trop d'info pour une question qui demande juste l'equation
- **Fix** : step 2 devrait s'arreter a "On obtient donc l'equation $2x + 2(x+5) = 34$, soit $4x + 10 = ?$"

### WARNINGS

**EQ-W1 : Exos 1 et 2 — meme reponse "5"**
- Exo 1 : $3x + 7 = 22$ -> x = 5
- Exo 2 : $5x - 4 = 21$ -> x = 5
- Deux exos consecutifs avec la meme reponse dans un fill, l'eleve peut croire qu'il s'est trompe ou que c'est un pattern
- **Fix** : changer exo 2 en $5x - 4 = 26$ -> x = 6

**EQ-W2 : Exo 18 — reponse "43" discutable pour une inequation**
- $7n \geq 300$ -> $n \geq 42.86$ -> $n \geq 43$
- C'est un fill, l'eleve doit taper "43"
- L'inequation n'est pas au programme strict du brevet (c'est au programme de 3eme mais rarement teste sous forme fill)
- **Acceptable** mais noter que _normFill() devra matcher "43"

**EQ-W3 : Step 3 de l'exo 1 donne la reponse**
- Step 2 : "On divise par $3$ : $x = \frac{15}{3} = \;?$."
- Bien que le `?` remplace la reponse, le calcul $15/3$ est trivial — c'est quasi donner la reponse
- Pattern recurrent sur tous les fill simples. **Acceptable** pour un chapitre de confiance/entree.

### CALCULS VERIFIES

| Exo | Calcul | OK |
|---|---|---|
| 1 | 3x+7=22 -> x=5 | OK |
| 2 | 5x-4=21 -> x=5 | OK |
| 3 | 2x+9=3x-1 -> x=10 | OK |
| 4 | 4x+3=2x+11 -> x=4 | OK |
| 5 | 7x-5=3x+11 -> x=4 | OK |
| 6 | 2x+3=27 -> x=12 | OK |
| 7 | 5x+6=21 -> x=3 | OK |
| 8 | 2(x+5)+2x=34 (equation) | OK |
| 9 | 3x+5=50 -> x=15 | OK |
| 10 | 4x=56 -> x=14 | OK |
| 11 | (x-3)(x+5)=0 -> 3 ou -5 | OK |
| 12 | (2x+1)(x-4)=0 -> -1/2 ou 4 | OK |
| 13 | x^2-16=0 -> 4 ou -4 | OK |
| 14 | x^2-6x+9=(x-3)^2 -> solution double 3 | OK |
| 15 | 4x^2-25=0 -> 5/2 ou -5/2 | OK |
| 16 | 30x+50=260 -> x=7 | OK |
| 17 | 2x+80=120 -> x=20 | OK |
| 18 | 7n>=300 -> n>=42.86 -> n=43 | OK |
| 19 | 40*7-200=80 < 100 -> Faux | OK |
| 20 | 7n=200+3n -> 4n=200 -> n=50 | OK |

### FORMAT

- Tous les fill ont `options: []` : OK
- Tous les V/F ont `type: "vf"` + `options: ["Vrai","Faux"]` : OK
- Tous les QCM ont 3 options : OK
- `a` in options pour tous les QCM : OK
- LaTeX $ pairs : OK

---

## 2. Fonctions_Brevet (20 exos)

### BLOQUANTS

**FN-B1 : Exo 10 — question/reponse incoherente**
- Question : "Cette fonction est-elle affine ?"
- Reponse : `$h(x) = x^2$`
- La question appelle une reponse Oui/Non, pas une expression
- Les options sont `[$h(x) = x^2$, $h(x) = 3x$, $h(x) = 2x - 1$]`
- La question devrait etre "Quelle est l'expression de cette fonction ?" au lieu de "Cette fonction est-elle affine ?"
- **Fix** : reformuler la question en "Quelle est l'expression de $h$ ?"

### WARNINGS

**FN-W1 : Exo 4 — option $\frac{25}{5}$ = 5 = bonne reponse**
- Options : `[$5$, $7$, $\frac{25}{5}$]`
- $\frac{25}{5} = 5$ = la bonne reponse. Deux options sont identiques en valeur.
- **Fix** : remplacer `$\frac{25}{5}$` par `$3$`

**FN-W2 : Exo 20 — reponse "101" debatable**
- "A partir de combien de minutes le forfait B devient-il avantageux ?"
- A 100 min ils sont egaux, a 101 min B est moins cher -> 101
- Correct mathematiquement mais suppose des minutes entieres
- **Acceptable** mais l'enonce pourrait preciser "en minutes entieres"

**FN-W3 : Doublons potentiels avec Fonctions_Affines_Brevet (Phase 1)**
- Phase 1 exo 1 : "coefficient directeur de $f(x) = -3x + 7$" (fill, a=-3)
- Phase 2 exo 11 : "coefficient directeur de $f(x) = 3x - 7$" (fill, a=3)
- Meme structure exacte, valeurs proches (3 vs -3, 7 vs -7). Pas un doublon strict mais tres similaire.
- Phase 2 exos 16-20 (forfaits telephone) forment un mini-probleme file qui est bien concu et n'a pas d'equivalent Phase 1 : OK

### CALCULS VERIFIES

| Exo | Calcul | OK |
|---|---|---|
| 1 | f(5)=4*5-3=17 | OK |
| 2 | g(3)=9+1=10 | OK |
| 3 | -2x+9=3 -> x=3 | OK |
| 4 | 5x+2=27 -> x=5 | OK |
| 5 | f(-3)=9-4=5 | OK |
| 6 | f(2)=7 (lecture) | OK |
| 7 | g(2)=3 -> antecedent=2 | OK |
| 8 | f(x)=-2x+5 (tableau) | OK |
| 9 | -2x+3=0 -> x=1.5 | OK |
| 10 | 0,1,4,9 -> x^2 | OK |
| 11 | coeff dir de 3x-7 = 3 | OK |
| 12 | f(x)=4x lineaire | OK |
| 13 | g(x)=2x+3 pas lineaire | OK |
| 14 | ordonnee a l'origine = 8 | OK |
| 15 | a=(20-11)/(5-2)=3 | OK |
| 16 | f(100)=0.2*100+5=25 | OK |
| 17 | f(200)=45, g(200)=35, B moins cher | OK |
| 18 | 0.2x+5=0.1x+15 -> x=100 | OK |
| 19 | A moins cher avant 100, B apres -> Faux | OK |
| 20 | B strictement < A a partir de 101 | OK |

### FORMAT
- V/F ont type:"vf" : OK
- Fill ont options:[] : OK
- QCM ont 3 options : OK
- a in options : OK

---

## 3. Scratch_Brevet (20 exos)

### BLOQUANTS

Aucun.

### WARNINGS

**SC-W1 : Exo 1 step 3 donne la reponse**
- Step 3 : "On obtient $x = 20$."
- Le step final ne devrait pas donner la reponse sur un QCM. L'eleve peut lire le step puis choisir.
- **Fix** : supprimer le step 3, ne garder que les 2 premiers (suffisants)

**SC-W2 : Exos avec step 3 redondants (pattern recurrent)**
- Exos 1, 2, 3, 4, 6, 7, 8 ont un step 3 qui repete ou confirme ce que le step 2 donne deja
- Ex: step 2 "Tour 3 : $n = ?$" puis step 3 "On obtient $n = 14$" -> le step 3 donne la reponse
- Pour un chapitre Scratch c'est moins grave car l'execution pas-a-pas est pedagogique, mais les steps 3 qui donnent la reponse directement violent la regle
- **Fix** : sur les QCM, retirer le step 3. Sur les fill, remplacer le nombre par `?`

### CALCULS VERIFIES

| Exo | Trace | OK |
|---|---|---|
| 1 | x=7, 7*3-1=20 | OK |
| 2 | a=4, b=7, a=14 | OK |
| 3 | n=10, 7, 14 | OK |
| 4 | x=3, 15, 17 | OK |
| 5 | x=2, 4, 5 (pas 6) -> Faux | OK |
| 6 | s=0, 4, 8, 12 | OK |
| 7 | c=1, 2, 4, 8, 16 | OK |
| 8 | n=5, 10, 20, 40 | OK |
| 9 | k=0+1+2+3+4+5=15 | OK |
| 10 | t=1+12=13 (pas 12) -> Faux | OK |
| 11 | x=15>10, x=10 | OK |
| 12 | 3*3=9<10 -> "Petit" | OK |
| 13 | p=0+2+4=6 | OK |
| 14 | x=-2: r=(-2)*(-1)=2>=0 -> Vrai | OK |
| 15 | m=100,70,40,50 | OK |
| 16 | 4 cotes 90deg = carre | OK |
| 17 | 360/90=4 | OK |
| 18 | 6*60=360 = hexagone | OK |
| 19 | 3*90=270 != 360 -> Faux | OK |
| 20 | x, x+3, 2(x+3), 2x+6, 2x+6-6=2x | OK |

### FORMAT
- V/F : type:"vf" present : OK
- Fill : options:[] : OK
- QCM : 3 options : OK
- Pseudo-code lisible avec $\leftarrow$ : OK

---

## 4. Auto_Calcul (20 exos)

### BLOQUANTS

**AC-B1 : Exo 11 — reponse fill "$10^{-2}$" probleme _normFill()**
- La reponse est `$10^{-2}$` avec les dollars
- _normFill() supprime les `$` et normalise, mais l'eleve devrait taper quoi ? "10^(-2)" ? "10^-2" ? "0.01" ?
- Meme probleme exo 12 (`$5{,}6 \times 10^{-4}$`), exo 15 (`$10^{-1}$`), exo 18 (`$5\sqrt{2}$`), exo 20 (`$5\sqrt{3}$`)
- **Fix** : pour les automatismes fill avec notation complexe, soit passer en QCM, soit s'assurer que _normFill accepte les variantes. A verifier avec le code front.

### WARNINGS

**AC-W1 : Exos 11, 12, 15, 18, 20 — reponses LaTeX dans des fill**
- Voir AC-B1 ci-dessus. La normalisation _normFill() fait:
  - `\frac{a}{b}` -> `a/b` : OK pour exos 6, 7, 8, 10
  - `\times` -> `x` : pas clair que ca marche pour `5,6 x 10^{-4}`
  - Supprime `$` : OK
- Les reponses simples comme "49", "144", "25", "14/3" sont OK
- Les reponses avec `\sqrt`, `\pi`, `10^{-n}` posent probleme

**AC-W2 : Exo 6 et exo 7 — reponses fill fractions**
- Exo 6 : a = "11/12" -> _normFill accepte "11/12" : OK
- Exo 7 : a = "3/2" -> OK
- Exo 8 : a = "14/3" -> OK (28/6 simplifie)
- _normFill normalise correctement ces formes

### CALCULS VERIFIES

| Exo | Calcul | OK |
|---|---|---|
| 1 | 7^2=49 | OK |
| 2 | 12^2=144 | OK |
| 3 | (-5)^2=25 | OK |
| 4 | (-3)^3=-27 | OK |
| 5 | 15*8-20=100 | OK |
| 6 | 3/4+1/6 = 9/12+2/12 = 11/12 | OK |
| 7 | 5/3 * 9/10 = 45/30 = 3/2 | OK |
| 8 | 7/2 / 3/4 = 7/2 * 4/3 = 28/6 = 14/3 | OK |
| 9 | 6/8 irreductible? Non (=3/4) -> Faux | OK |
| 10 | 5/6-3/8 = 20/24-9/24 = 11/24 | OK |
| 11 | 10^3 * 10^-5 = 10^-2 | OK |
| 12 | 0.00056 = 5.6 * 10^-4 | OK |
| 13 | 3.2 * 10^5 = 320000 | OK |
| 14 | 6.8>=5, ordre de grandeur 10^-2 | OK |
| 15 | 10^4*10^-2/10^3 = 10^2/10^3 = 10^-1 | OK |
| 16 | sqrt(49)=7 | OK |
| 17 | sqrt(144)=12 | OK |
| 18 | sqrt(50)=5sqrt(2) | OK |
| 19 | sqrt(25)=5 != 3+4=7 -> Faux | OK |
| 20 | sqrt(12)+sqrt(27) = 2sqrt3+3sqrt3 = 5sqrt3 | OK |

---

## 5. Auto_Litteral (20 exos)

### BLOQUANTS

Aucun.

### WARNINGS

**AL-W1 : Exos 6, 7, 9, 10, 11, 15 — reponses LaTeX dans des fill**
- Meme problematique que Auto_Calcul : `$3x + 6$`, `$(x - 3)(x + 3)$`, `$10x^2 - 5x$`, etc.
- _normFill() supprime les `$` et normalise, mais l'eleve doit deviner le format
- Cependant ces exercices sont des automatismes d'algebre, la notation est attendue
- **A verifier** : que _normFill accepte les espaces et les variantes de notation

### CALCULS VERIFIES

| Exo | Calcul | OK |
|---|---|---|
| 1 | x=3: 2*9-5=13 | OK |
| 2 | a=-2: -6+7=1 | OK |
| 3 | x=-4: 16-12=4 | OK |
| 4 | t=5: (10-3)^2=49 | OK |
| 5 | x=2: 16-2+1=15 | OK |
| 6 | 3(x+2)=3x+6 | OK |
| 7 | x^2-9=(x-3)(x+3) | OK |
| 8 | 3(x+2)=3x+6 != 3x+2 -> Faux | OK |
| 9 | 5x(2x-1)=10x^2-5x | OK |
| 10 | 4x^2-25=(2x-5)(2x+5) | OK |
| 11 | (x+5)^2=x^2+10x+25 | OK |
| 12 | x^2-16=x^2-4^2 -> Vrai | OK |
| 13 | 9x^2+6x+1=(3x+1)^2 | OK |
| 14 | (2x-3)^2=4x^2-12x+9 != 4x^2-6x+9 -> Faux | OK |
| 15 | x^2+8x+16=(x+4)^2 | OK |
| 16 | 2x+1=7 -> x=3 | OK |
| 17 | 5x=-15 -> x=-3 | OK |
| 18 | x^2=49 -> x=7 ou x=-7 | OK |
| 19 | 3x-4=11 -> x=5 | OK |
| 20 | (x-2)(x+3)=0 -> x=2 ou x=-3 | OK |

---

## 6. Auto_Geometrie (20 exos)

### BLOQUANTS

Aucun.

### WARNINGS

**AG-W1 : Exo 6 — reponse "$36\pi$" dans un fill**
- L'eleve doit taper "36pi" ? "36*pi" ? Meme probleme pour exos 7, 8, 10 ($25\pi$, $48\pi$, $90\pi$)
- _normFill() ne gere probablement pas le symbole pi
- **Fix** : passer ces exos en QCM, ou accepter "36pi" / "36*pi" dans _normFill

**AG-W2 : Exos 3, 11, 12, 16 — reponses textuelles dans des fill**
- Exo 3 : "l'hypotenuse" — l'eleve tape "hypotenuse" sans accent ? avec article ?
- Exo 11 : "sinus" — OK plus simple
- Exo 12 : "tangente" — OK
- Exo 16 : "semblables" — OK
- Exo 19 : "Thales" — avec accent ?
- _normFill() est concu pour des reponses numeriques/algebriques, pas du texte libre
- **Fix** : passer exos 3, 16, 19 en QCM pour eviter les problemes de normalisation texte

**AG-W3 : Exo 13 — cos(60) = 1/2 en fill**
- Reponse "1/2" — _normFill gere `a/b` donc OK
- Mais l'eleve pourrait taper "0.5" ou "0,5" — a verifier

### CALCULS VERIFIES

| Exo | Calcul | OK |
|---|---|---|
| 1 | 5^2+12^2=25+144=169=13^2 -> rectangle Vrai | OK |
| 2 | 3^2+5^2=34 != 49=7^2 -> Faux | OK |
| 3 | Hypotenuse (vocabulaire) | OK |
| 4 | 8^2+15^2=64+225=289=17^2 -> Vrai | OK |
| 5 | 6^2+8^2=100, sqrt(100)=10 | OK |
| 6 | V=4/3*pi*27=36pi | OK |
| 7 | A=pi*25=25pi | OK |
| 8 | V=1/3*pi*16*9=48pi | OK |
| 9 | Volume pyramide = 1/3*B*h | OK |
| 10 | V=pi*9*10=90pi | OK |
| 11 | sin = oppose/hypotenuse | OK |
| 12 | tan = oppose/adjacent | OK |
| 13 | cos(60)=1/2 | OK |
| 14 | sin(30)=1/2 != sqrt(3)/2 -> Faux | OK |
| 15 | adjacent+hypotenuse -> cosinus | OK |
| 16 | Memes angles -> semblables | OK |
| 17 | k=2, aires*k^2=4 | OK |
| 18 | Paralleles + secantes -> Thales | OK |
| 19 | k<0 -> sens inverse -> Vrai | OK |
| 20 | k=3, volumes*k^3=27 | OK |

---

## 7. Doublons inter-phases

### Equations_Brevet vs Phase 1
- Pas de fichier Equations en Phase 1 : **pas de doublons possibles**

### Fonctions_Brevet vs Fonctions_Affines_Brevet (Phase 1)
- Phase 1 exo 1 : coeff directeur de $-3x+7$ (fill)
- Phase 2 exo 11 : coeff directeur de $3x-7$ (fill)
- **Similaire** mais valeurs differentes (signe inverse). Acceptable.
- Phase 2 exos 16-20 = probleme forfaits telephone. Pas d'equivalent Phase 1. OK.

### Auto_Calcul vs diagnostic_3eme
- Diagnostic contient des exos sur fractions et puissances
- Phase 2 Auto_Calcul exo 6 : $3/4 + 1/6$ vs diagnostic exo 1 : $2/3 + 5/6$
- Valeurs differentes. OK.

### Auto_Litteral vs Calcul_Litteral_Brevet (Phase 1)
- Phase 1 contient des developpements/factorisations
- Phase 2 exo 7 : "Factorise $x^2 - 9$" pourrait etre dans Phase 1
- A verifier dans Calcul_Litteral_Brevet, mais les automatismes sont par nature des flash cards courtes, differents des chapitres complets

### Auto_Geometrie vs Phase 1 (Pythagore, Thales, Trigo)
- Exos Pythagore V/F (5,12,13 et 3,5,7 et 8,15,17) : a verifier si identiques aux exos Phase 1
- Les triplets pythagoriciens classiques PEUVENT se retrouver, mais les automatismes testent la reconnaissance rapide, pas la resolution

---

## 8. Resume des actions

### BLOQUANTS (3) — a corriger avant injection

| # | Fichier | Exo | Probleme | Fix |
|---|---|---|---|---|
| 1 | Equations_Brevet | 8 | Steps resolvent l'equation alors que la question demande juste l'equation | Raccourcir step 2 |
| 2 | Fonctions_Brevet | 10 | Question "est-elle affine?" vs reponse "$h(x)=x^2$" | Reformuler question |
| 3 | Fonctions_Brevet | 4 | Option $\frac{25}{5}$ = 5 = bonne reponse (doublon d'option) | Remplacer par $3$ |

### WARNINGS PRIORITAIRES (a traiter idealement)

| # | Fichier | Exos | Probleme |
|---|---|---|---|
| 1 | Auto_Calcul | 11,12,15,18,20 | Reponses LaTeX complexes dans fill — _normFill peut ne pas matcher |
| 2 | Auto_Geometrie | 6,7,8,10 | Reponses avec $\pi$ dans fill |
| 3 | Auto_Geometrie | 3,16,19 | Reponses textuelles dans fill — normalisation incertaine |
| 4 | Scratch_Brevet | 1,2,3,4,6,7,8 | Step 3 donne la reponse directement |
| 5 | Equations_Brevet | 1,2 | Meme reponse "5" sur 2 fill consecutifs |

### WARNINGS ACCEPTABLES

| # | Fichier | Exo | Probleme |
|---|---|---|---|
| 1 | Equations_Brevet | 18 | Fill avec inequation (43) |
| 2 | Fonctions_Brevet | 20 | Fill "101" (minutes entieres implicite) |
| 3 | Fonctions_Brevet | 11 | Similaire a Phase 1 exo (coeff directeur) |

---

## 9. Verdict global

**Qualite des calculs : 120/120 corrects.** Zero erreur de calcul. Excellent.

**Qualite pedagogique : bonne.** Les slots sont bien structures, les distracteurs sont plausibles, les contextes sont varies. Les chapitres Brevet (Equations, Fonctions, Scratch) sont bien construits avec des fils rouges (spectacle, forfaits, lutin).

**Point de vigilance majeur : les fill avec reponses LaTeX complexes.** C'est le probleme numero 1 des automatismes. Il faut soit :
1. Verifier que _normFill() gere `\sqrt`, `\pi`, `10^{-n}`, expressions algebriques
2. Soit convertir ces exos en QCM

**3 bloquants a corriger, puis injection possible.**
