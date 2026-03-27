# Audit Phase 1 — Refonte Brevet 2026
Date : 2026-03-27

## Resume
- **101/104 exos OK** sur le plan des calculs
- **0 erreur de calcul** — toutes les reponses sont mathematiquement correctes
- **1 erreur de format critique** (distracteurs doublons)
- **4 problemes pedagogiques** (steps qui donnent la reponse)
- **Quelques warnings mineurs** (prenoms, formules)

## Erreurs de calcul (CRITIQUES)
**Aucune.** Tous les 104 calculs ont ete verifies a la main. Les reponses `a` sont correctes.

## Problemes de format

### CRITIQUE
- **diagnostic_3eme.json** — Transformations_Brevet exo #2 (lvl 2, aire homothetie) : les options `"$18$ cm$^2$"` et `"$\frac{54}{3}$ cm$^2$"` ont la MEME VALEUR (18). Le distracteur `54/3` n'est pas un vrai distracteur puisque 54/3 = 18. Il faut changer l'une des deux options (par ex. remplacer `$\frac{54}{3}$ cm$^2$` par `$\frac{54}{9}$ cm$^2$` soit `$6$ cm$^2$`... mais c'est deja la bonne reponse. Mieux : remplacer par `$2$ cm$^2$` ou `$3$ cm$^2$` comme erreur de rapport).

### WARNINGS
- **diagnostic_3eme.json** : le format est un tableau de chapitres (pas un objet `{exos:[...]}`), donc `validate_exos.py` ne le parse pas correctement. Le script doit etre adapte pour ce format, ou le fichier restructure.
- **Pythagore_Brevet.json** : prenom "Lucas" utilise 2 fois (exos 16 et 17+18+19+20 — fil narratif skate park, donc acceptable).
- **Pythagore_Brevet.json** : toutes les formules sont `$a^2 + b^2 = c^2$` — normal pour un chapitre mono-theoreme.
- **Thales_Brevet.json** : prenom "Lea" utilise 2 fois (exos 16 et 17+18+19+20 — fil narratif maquette, donc acceptable).
- **Calcul_Litteral_Brevet.json** : exos 6-10 (identites remarquables) ont `"f": ""` — c'est un choix delibere (test de restitution), mais a confirmer car le diagnostic_3eme a la meme categorie avec formule affichee.

## Problemes pedagogiques

### Steps qui donnent la reponse directement (violation regle "? au lieu du resultat")
- **Thales_Brevet.json** exo #2 (RST, RF) : step 3 = `"$RF = 6$ cm."` — donne la reponse au lieu de `?`
- **Thales_Brevet.json** exo #4 (DEF, DF) : step 3 = `"$DF = 12$ cm."` — idem
- **Thales_Brevet.json** exo #7 (papillon EF/GH, OF) : step 3 = `"$OF = 6$ cm."` — idem
- **Thales_Brevet.json** exo #9 (papillon PQ/RS, PQ) : step 3 = `"$PQ = 9$ cm."` — idem

> Ces 4 exos ont un step 2 qui pose correctement le calcul avec `= ?`, puis un step 3 superflu qui donne la reponse. **Solution : supprimer le step 3** sur ces 4 exos (le step 2 suffit comme dernier indice).

### Steps donnant la conclusion sur V/F et reciproque
- **Thales_Brevet.json** exo #14 (GHI, reponse "Oui, les rapports sont egaux") : step 3 = `"D'apres la reciproque de Thales, les droites (ST) et (HI) sont paralleles."` — donne la reponse directement au lieu de poser la question ("Que peut-on en conclure ?"). Les exos #11, #12, #13 font bien la question ouverte. Le #15 aussi donne la reponse directement (`"Les droites (DE) et (BC) ne sont pas paralleles."`).
- **Thales_Brevet.json** exo #20 (diagonale facade) : step 3 = `"La diagonale reelle mesure $15$ m."` — donne la reponse.

### Formule generique sur contexte non-Thales
- **Thales_Brevet.json** exo #16 (echelle maquette) : la formule est `$\frac{AM}{AB} = \frac{AN}{AC} = \frac{MN}{BC}$` mais l'exo est un simple calcul d'echelle (pas de Thales a proprement parler). `"f": ""` serait plus honnete, ou alors `$\text{echelle} = \frac{\text{maquette}}{\text{reel}}$`.

### Homogeneite lvl
- **Pythagore_Brevet.json** exo #10 (KLM, LM=12, lvl:2) : c'est un calcul de cote simple (15^2 - 9^2 = 144), identique en difficulte aux exos lvl:1 (#6, #8). Le lvl:2 ne semble pas justifie.
- **Calcul_Litteral_Brevet.json** : la progression lvl est correcte globalement. Slot 1 (1-5) tout lvl:1, slot 2 (6-10) mix 1/2, slot 3 (11-15) mix, slot 4 (16-20) mix. Conforme aux regles.

## Coherence inter-fichiers

- **Doublon potentiel** : diagnostic_3eme Pythagore lvl1 (6,8,10) et Pythagore_Brevet exo #3 (EFG, 6,8,10) et exo #11 (V/F 6,8,10) — memes valeurs numeriques sur 3 exos. Ce n'est pas un vrai doublon (contextes differents), mais a surveiller si un eleve enchaine diagnostic + chapitre.
- **Doublon potentiel** : diagnostic_3eme Pythagore lvl2 (7,24,25) et Pythagore_Brevet exo #4 (7,24, hypotenuse 25) — memes valeurs.
- **Doublon potentiel** : diagnostic_3eme Thales lvl2 (AM=4, AB=10, MN=3) et Thales_Brevet exo #9 (OP=3.5, OR=7, rapport 1/2 aussi). Pas identique.
- **Doublon potentiel** : diagnostic_3eme Calcul_Litteral lvl2 (9x^2-16) et Calcul_Litteral_Brevet exo #13 (9x^2-49). Meme technique, valeurs differentes. OK.

## Structure diagnostic_3eme

Chaque chapitre a bien 1 exo lvl:1 + 1 exo lvl:2. 22 chapitres * 2 = 44 exos. Conforme.

## Synthese des corrections a faire

| Priorite | Fichier | Exo | Action |
|---|---|---|---|
| CRITIQUE | diagnostic_3eme.json | Transformations #2 | Changer option `$\frac{54}{3}$ cm$^2$` en une vraie erreur (ex: `$3$ cm$^2$`) |
| HAUTE | Thales_Brevet.json | #2, #4, #7, #9 | Supprimer le step 3 qui donne la reponse |
| HAUTE | Thales_Brevet.json | #14, #15 | Remplacer le step final par une question ouverte |
| HAUTE | Thales_Brevet.json | #20 | Supprimer step 3 ou remplacer par `?` |
| MOYENNE | Pythagore_Brevet.json | #3, #11 + diag | Varier les triplets (6,8,10) entre diagnostic et chapitre |
| BASSE | Pythagore_Brevet.json | #10 | Envisager lvl:1 au lieu de lvl:2 |
| BASSE | Thales_Brevet.json | #16 | Formule plus adaptee au contexte echelle |

## Verdict

**Mathematiquement : 104/104 calculs justes.** Aucune erreur de calcul. C'est solide.

**Format/Pedagogie : 1 erreur critique (doublon options) + 7 steps a corriger.**

**Verdict global : PASS CONDITIONNEL** -- corriger le doublon d'options (Transformations) et les 7 steps qui donnent la reponse avant mise en production.
