# Relecture NC : items de diagnostic 3e

Relecteur : agent `relecteur`, 24/09/2026, branche `feat/diagnostic-3e`. Les items n'ont pas été modifiés.
Détail par item : `NC.<THEME>.review.json`. Chaque item `corrige` y porte l'item complet corrigé (`correction`).

## Bilan

| Fichier | Items | ok | corrigé | rejet |
|---|---|---|---|---|
| NC.ENT | 9 | 7 | 2 | 0 |
| NC.PRIO | 3 | 3 | 0 | 0 |
| NC.REL | 9 | 5 | 4 | 0 |
| NC.ARITH | 12 | 10 | 2 | 0 |
| NC.FRAC | 21 | 16 | 5 | 0 |
| NC.PUIS | 15 | 14 | 1 | 0 |
| NC.RAC | 12 | 9 | 3 | 0 |
| NC.INEQ | 6 | 5 | 1 | 0 |
| NC.EQUA | 18 | 11 | 7 | 0 |
| NC.LIT | 30 | 28 | 2 | 0 |
| **Total** | **135** | **108** | **27** | **0** |

**Ce que j'ai vérifié :**
- J'ai refait tous les calculs à la main. Aucune réponse `a` n'est fausse.
- Les 1 385 segments LaTeX passent dans KaTeX 0.16.9. Cela couvre les originaux et les corrections, y compris les `\text{___}` une fois remplacés par `\boxed{\phantom{xx}}`.
- J'ai simulé les réponses fill dans Node avec `_normFill`, `_toNum` et `_matchFill` extraits d'`app.html`. Le portage serveur `mxEgal` (index.ts) a aussi été simulé : les deux donnent le même résultat.
- `check_banque.py` passe sur la banque NC corrigée : ✅.

## Erreurs graves (le bilan envoyé au parent serait faux)

1. **Faux positifs dans les fills de conversion.**
   - `NC.FRAC.01-d02` : l'élève qui recopie `3/5` est compté juste (`_toNum` = 0,6).
   - `NC.FRAC.07-d01` : l'élève qui recopie `25%` est compté juste (= 0,25).
   - Dans les deux cas, c'est justement l'élève visé par l'erreur type qui passe. Je les passe en QCM.
2. **Faux négatif sur `NC.FRAC.07-d03` (`___ %`).**
   - L'élève qui tape `35 %` est compté faux : `_toNum('35%')` vaut 0,35 et ne correspond pas à 35.
   - Ajouter un alt ne marche pas : un alt `35%` ferait passer `0,35` à cause de l'égalité numérique côté serveur.
   - Je le passe en QCM.
3. **Bonne réponse identique à celle de la règle erronée (`NC.ENT.02-d01`).**
   - La bonne réponse 2,5 est aussi celle que donne `#plus_court_plus_grand`. L'élève qui a cette erreur réussit donc l'item.
4. **Deux bonnes réponses possibles (`NC.LIT.01-d03`).**
   - « Le prix de 5 objets » décrit aussi correctement 3s + 2c.
5. **Faux négatifs de saisie.**
   - `NC.EQUA.06-d02` : « pas de solution » est refusé. J'élargis les `alt`.
   - Cinq fills « $x = $ ___ » refusent `x=7`. J'ajoute un `alt` `x=…`, et j'ai vérifié par simulation qu'il ne laisse passer aucune autre réponse.

## Tendances

- **Distracteurs de remplissage tagués comme une vraie erreur.** Le cas typique est un QCM « le plus grand de ces nombres ». La règle erronée ne prédit qu'une seule option, mais les deux autres portent le même tag. Items concernés : `ENT.02-d01/d02`, `REL.01-d01`, `FRAC.01-d01`, `PUIS.05-d01`.
  - Correction : reformuler en « Laquelle de ces comparaisons est vraie ? ». Chaque distracteur applique alors exactement la règle erronée, et la bonne réponse la contredit.
- **Tag qui ne correspond pas à l'erreur réellement commise.** Items concernés :
  - `REL.02-d02` (−2) ;
  - `REL.02-d03` (9 → 13) ;
  - `REL.03-d01` (−7 est une somme) ;
  - `FRAC.04-d02` (48 € est une hausse) ;
  - `RAC.01-d02` (625 = élève au carré) ;
  - `LIT.01-d02` (x + 7).
- **Indices qui donnent la réponse.** Items concernés : `ARITH.01-d01` (l'exemple pris est la bonne option), `ARITH.04-d01` (l'indice élimine tous les distracteurs), `FRAC.01-d02`.
- Les autres items sont bons. Les distracteurs multiples sur `FRAC.02-d01/d02` et `REL.03-d02` sont chacun une application exacte de l'erreur : ils sont justifiés.

## Points signalés par l'auteur

| Point | Verdict |
|---|---|
| QCM à 3 options `LIT.07-d01`, `LIT.08-d02`, `RAC.04-d03` | ok : aucun 4e distracteur honnête sans sortir de la compétence (poids serveur 0,67) |
| Distracteurs multiples `ENT.02-d01` / `REL.01-d01` / `FRAC.02-d02` | corrigé / corrigé / ok |
| Blank dans le LaTeX `LIT.04-d03`, `LIT.06-d03` | ok, le rendu KaTeX est vérifié |
| `EQUA.06-d02` (« 0 » + alt « aucune ») | corrigé : alt élargi, aucune réponse fausse ne passe |
| Mapping `EQUA.04` | ok : le libellé parent de `#inconnue_floue` (« Ne sait pas par où commencer ») couvre les équations incohérentes |
| `LIT.10` | ok (3/3) |
| `EQUA.01` | d02 corrigé : question de méthode avec un distracteur absurde, transformée en vrai test chiffré. d01 et d03 ok |
| `INEQ.02` | d01 corrigé (deux distracteurs équivalents : n ≥ 120 et 120 ≤ n). d02 et d03 ok |

## Problèmes transversaux (code, hors items) — à transmettre au dev

- Le signe moins typographique « − » (U+2212) et le tiret « – » ne sont normalisés ni dans `_normFill` ni dans `mxNorm`. Résultat : `−5` est refusé sur REL.01-d02, REL.02-d01, PUIS.04-d01, EQUA.03-d03 et EQUA.05-d02.
- Un « + » en tête de réponse (`+15`) est refusé.
- Une mauvaise réponse saisie « x=18 » ne retrouve pas son erreur type. Correctif proposé : retirer un préfixe `x=` dans `mxNorm`.
- La clé d'erreur `\sqrt{10}` n'est pas atteinte quand l'élève tape `√10`. J'ai ajouté la clé dans RAC.02-d02.

## ❓ Questions pour Nicolas

1. **`NC.RAC.04` (rationaliser un dénominateur)** n'est pas au programme du cycle 4 ni au Brevet. Faut-il la garder en diagnostic ? Ma reco : `train` seulement, et la retirer du bilan.
2. **QCM à 3 options** : j'en propose 10 nouveaux, pour éviter des distracteurs sans erreur type. Est-ce accepté ? Ma reco : oui, le poids serveur 1 − 1/k compense déjà le hasard.
3. **Référentiel** (à transmettre au didacticien) : ajouter les erreurs types `NC.EQUA.04` « oublie une des quantités » et `NC.LIT.01` « "de moins" traduit par + » ? Ma reco : oui.
