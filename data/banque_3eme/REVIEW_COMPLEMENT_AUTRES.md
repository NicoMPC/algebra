# Relecture — complément d'entraînement DF, GM, EG, AP (items `-tNN`)

> Relecteur · 25/09/2026 · branche `feat/diagnostic-3e`. Relu : les 107 items `-t` de `COMPLEMENT_AUTRES.md`.
> Verdicts par item dans `data/banque_3eme/<DOM>.<THEME>.train-review.json` (corrections = item complet). Aucun item édité.

## Bilan : 104 ok · 3 corrige · 0 rejet

| Fichier | Items | ok | corrige | rejet |
|---|---|---|---|---|
| EG.REP | 10 | 10 | 0 | 0 |
| DF.STAT (STAT.01 + STAT.03) | 12 | 11 | 1 | 0 |
| DF.FONC | 8 | 7 | 1 | 0 |
| DF.AFF | 7 | 7 | 0 | 0 |
| GM.CONV | 11 | 11 | 0 | 0 |
| EG.THAL | 9 | 9 | 0 | 0 |
| DF.PROP | 7 | 7 | 0 | 0 |
| GM.VOL (VOL.02 + VOL.03) | 16 | 16 | 0 | 0 |
| EG.TRIG | 9 | 8 | 1 | 0 |
| AP.PROG | 10 | 10 | 0 | 0 |
| EG.ANG | 8 | 8 | 0 | 0 |

## Corrections proposées

- **DF.STAT.01-t03** : la réponse 13 est aussi la valeur « 13 ans » de l'énoncé. Un élève qui confond valeur et effectif (« moins de 14 ans → 13 ») serait compté juste. On passe à des effectifs 3 et 8 : la réponse devient 11, et la clé 25 est conservée.
- **DF.FONC.02-t03** : on peut recopier la réponse, car l'énoncé ne donne que « hauteur −3 ». On donne à la place les deux points d'intersection avec les axes, (2 ; 0) et (0 ; −3). La clé 2 correspond à `axes_inverses` et la clé 3 à `quadrant`.
- **EG.TRIG.02-t08** : le distracteur « cos(40°) = BH/AH » place l'opposé en hypoténuse. Il ne relève pas de `EG.TRIG.01#adjacent_hypotenuse`. On le retague `EG.TRIG.02#mauvais_rapport`.

## Contrôles effectués

- Tous les calculs ont été refaits, y compris les arrondis π à la calculatrice (GM.VOL, EG.TRIG), les triplets de Pythagore des cônes et pyramides (6-8-10, 15-20-25, 3-4-5) et chaque valeur de distracteur.
- Les 10 scripts Scratch ont été exécutés pas à pas. Chaque valeur `err` (±1 tour, corps exécuté une fois, bloc final répété) correspond exactement.
- `_matchFillQ` a été extrait d'`app.html` et testé en Node :
  - `a` et `alt` sont acceptés pour tous les fill ;
  - aucune clé `err` n'est acceptée ;
  - des mauvaises réponses prévisibles ont été testées (lettres en minuscules, `(DE)`, signes, formes 0,6 / 6/10 / 60 %) : pas d'acceptation abusive.
- Chaque `err` pointe vers la compétence ou vers un prérequis direct du référentiel, et l'id d'erreur existe (script de contrôle).
- KaTeX `strict:'error'` : 1118 segments (items et corrections, `\text{___}` substitué), 0 erreur. Testé avec KaTeX 0.16.22 local, même API que 0.16.9.
- Pas de doublon avec les items `-d` : certains items reprennent la même structure avec d'autres nombres (DF.STAT.03-t05 / d03, EG.ANG.01-t02 / d02, DF.FONC.02-t01 / d01, EG.THAL.01-t01 / d03). C'est acceptable en entraînement.

## Remarques mineures (non bloquantes)

- GM.VOL.02-t07 refuse « 2,827 », une valeur non arrondie, alors que la consigne demande un arrondi. C'est acceptable.
- DF.AFF.02-t04 refuse « −1,5 » à la question « de combien raccourcit-elle ». C'est défendable.
- EG.TRIG.02-t03, t06 et t09 sont des fill où l'énoncé propose « cos, sin ou tan ». Ce sont en pratique des QCM à 3 choix, ce qui est acceptable.
- Les champs `f` d'AP.PROG.03 sont vides, comme dans tous les items AP existants. C'est conforme à la convention actuelle.
- Rappel du contrat §8 : les `\n` des scripts Scratch ne doivent pas être perdus au rendu. Ce point dépend du front (dev-ux), pas des items.
