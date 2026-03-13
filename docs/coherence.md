# Cohérence Boost Auto — Diagnostic & Résolution

> Document de contexte pour reprendre le debug si le problème persiste après déploiement @54.

---

## Le problème

**Symptôme** : le boost automatique (premier boost post-diagnostic) affichait des exercices de chapitres que l'élève n'avait PAS sélectionnés. Par exemple, un élève choisissant "Fractions" voyait des exercices d'Angles et Périmètres dans son boost.

**Impact** : le tableau de bord montrait ces chapitres comme "commencés", ce qui désoriente l'élève.

---

## Causes racines identifiées (3 bugs)

### Bug 1 — Diagnostic : `selectedChapters: []`

**Fichier** : `index.html`, fonction `_flowStartDiag()` (ligne ~1783)

**Avant** : le diagnostic envoyait `selectedChapters: []` au backend → GAS retournait des exercices de TOUS les chapitres du niveau (6-8 chapitres).

**Fix** : `selectedChapters: _flowChaps` → diagnostic limité aux chapitres sélectionnés.

### Bug 2 — boostFromDiag : pas de chapitres explicites

**Fichier** : `index.html`, fonction `boostFromDiag()` (ligne ~2837)

**Avant** : l'appel `generate_daily_boost` ne transmettait que `code`, `level`, `errors`. Le backend devait DEVINER les chapitres via les Scores (filtre P5).

**Fix** : ajout `chapters: _flowChaps` dans le payload → le backend sait exactement quels chapitres cibler.

### Bug 3 — P5 backend : filtre Scores pollué

**Fichier** : `backend.js`, fonction `generateDailyBoost()` (ligne ~764)

**Avant** : le filtre P5 lisait TOUS les Scores de l'élève pour déduire les chapitres diagnostiqués. Problèmes :
- Les scores du diagnostic avaient `Chapitre = nom réel` (pas 'CALIBRAGE'), donc TOUS les chapitres testés étaient inclus
- Les scores de boost précédents (`Chapitre = 'BOOST'`) n'étaient pas exclus

**Fix** :
1. Priorité à `p.chapters` quand fourni (source de vérité directe, pas de devinette)
2. Fallback Scores exclut maintenant `'BOOST'` ET `'CALIBRAGE'`

---

## Flux corrigé — traçabilité complète

```
1. Élève sélectionne chapitres A, B     → _flowChaps = ['A', 'B']
2. _flowStartDiag()                      → selectedChapters: ['A', 'B']
3. GAS generateDiagnostic()              → exos de A et B uniquement
4. Scores sauvegardés                    → categorie: 'A'/'B', source: 'CALIBRAGE'
                                            → Progress NON mis à jour ✅
5. boostFromDiag()                       → chapters: ['A', 'B'] envoyé au backend
6. GAS generateDailyBoost()
   a. Lit BoostExos (pool dédiée)        → 10 exos/chapitre, séparés de Curriculum
   b. P5 : p.chapters = ['A','B']        → filtre BoostExos à A et B uniquement
   c. Tri par faiblesse                  → chapitres les plus faibles en premier
   d. Pioche 5 exercices                 → uniquement dans A et B
7. loadBoost()                           → exercices taggés oC:'BOOST'
8. save_score(source:'BOOST')            → Progress NON mis à jour ✅
                                            → Aucun autre chapitre touché ✅
```

---

## Vérification effectuée (13 mars 2026)

**Profil test** : WK2PHM (NICOLAS, 5EME, inscrit 13 mars)
- Chapitres sélectionnés : Nombres_relatifs, Puissances
- Boost généré : 5 exercices — **100% Nombres_relatifs + Puissances**
- Source des 5 exercices : **100% BoostExos** (matchés un par un)
- Collision avec Curriculum_Officiel : **0**
- Chapitres dans Scores : **uniquement** Nombres_relatifs + Puissances
- Chapitres parasites (Angles, Périmètres, etc.) : **aucun**

---

## Si le problème persiste

### Checklist de debug

1. **Cache navigateur** : Ctrl+Shift+R (hard refresh). Vérifier que le JS contient `chapters:_flowChaps` (DevTools → Sources → index.html → chercher "chapters:")

2. **Vérifier le code live** :
   ```bash
   curl -s 'https://matheux.fr/' | grep -o 'chapters:_flowChaps'
   # Doit retourner "chapters:_flowChaps"
   ```

3. **Inspecter le boost en base** :
   ```bash
   cd "/home/nicolas/Bureau/algebra live/algebra"
   python3 -c "
   from sheets import Sheets; import json; sh = Sheets()
   code = 'CODE_ELEVE'
   for b in sh.read('DailyBoosts'):
       if b.get('Code') == code:
           data = json.loads(b.get('BoostJSON','{}'))
           cats = set(e.get('_cat','?') for e in data.get('exos',[]))
           print(f'Chapitres boost: {cats}')
           for e in data.get('exos',[]): print(f'  _cat={e.get(\"_cat\")} q={e.get(\"q\",\"\")[:50]}')
   "
   ```

4. **Vérifier les Scores du profil** :
   ```bash
   python3 -c "
   from sheets import Sheets; sh = Sheets()
   code = 'CODE_ELEVE'
   cats = set(s.get('Chapitre','') for s in sh.read('Scores') if s.get('Code')==code)
   print(f'Chapitres dans Scores: {cats}')
   "
   ```

5. **Vérifier que BoostExos est lu par GAS** : dans Apps Script UI, exécuter manuellement :
   ```javascript
   function testBoostExos() {
     var rows = getRows('BoostExos');
     Logger.log('BoostExos rows: ' + rows.length);
     rows.forEach(function(r) { Logger.log(r['Niveau'] + ' | ' + r['Categorie']); });
   }
   ```

### Pistes si toujours cassé

- **Ancien boost en DailyBoosts** : si un boost a été généré AVANT le fix, il est stocké et re-servi par `login()`. Solution : supprimer la ligne du profil dans DailyBoosts et retester.
- **Deux fonctions register** : `_flowGuestRegister()` (post-diagnostic) et `flowRegister()` (direct). Vérifier que c'est bien `_flowGuestRegister` qui est appelée (line 2019 remplace le onclick après le diagnostic).
- **`_flowChaps` vide** : si l'élève n'a sélectionné aucun chapitre avant le diagnostic (ne devrait pas arriver, vérifié par `flowToStep3()`).

---

## Fichiers modifiés

| Fichier | Lignes clés | Modification |
|---|---|---|
| `index.html:1783` | `_flowStartDiag()` | `selectedChapters: _flowChaps` |
| `index.html:2837` | `boostFromDiag()` | ajout `chapters: _flowChaps` |
| `backend.js:764-784` | `generateDailyBoost()` P5 | priorité `p.chapters`, exclusion BOOST |
| `backend.js:751-758` | `generateDailyBoost()` source | BoostExos prioritaire, fallback Curriculum |
| `index.html:2095` | `_flowGuestRegister()` save diag | `categorie: 'CALIBRAGE'` (était `exo.oC \|\| exo.categorie`) |
| `index.html:2205` | modal registration save diag | `categorie: 'CALIBRAGE'` (était `exo.categorie \|\| ...`) |
| `backend.js:364-372` | `login()` history filter | exclut `Chapitre === 'CALIBRAGE'` de l'historique |

---

## Bug 4 — Chapitres "entamés" fantômes après diagnostic (fix @55)

### Symptôme

Après le flux CTA "essayez" (diagnostic → boost auto → inscription), certains chapitres apparaissaient comme "entamés" sur le dashboard, alors que l'élève n'avait fait aucun exercice curriculum. En passant par la modale inscription, le dashboard était vierge.

### Cause racine

Les scores de diagnostic étaient sauvegardés avec `categorie = nom_réel_du_chapitre` (ex: 'Fractions') au lieu de 'CALIBRAGE'. Le champ `source: 'CALIBRAGE'` n'étant **jamais stocké** dans la table Scores (pas de colonne Source), `login()` retournait ces scores indistinctement du curriculum dans `d.history`.

`initApp()` les chargeait dans `S.res` avec des clés comme `'5EME-Fractions-0'` qui **collidaient** avec les index des exercices curriculum du même chapitre. Le dashboard voyait `S.res['5EME-Fractions-0']` non-nul → chapitre marqué "entamé".

### Pourquoi la modale ne posait pas le problème

Le flux modale inscrit l'utilisateur AVANT le diagnostic → aucun score n'existe dans Scores au moment du login → `S.res` vierge → dashboard propre.

### Fix (3 patches)

1. **Frontend guest flow** (`index.html:2095`): `categorie: 'CALIBRAGE'` → les scores de diagnostic sont maintenant sauvegardés sous le chapitre 'CALIBRAGE', pas sous le vrai nom
2. **Frontend modal flow** (`index.html:2205`): idem
3. **Backend login** (`backend.js:364-372`): filtre `Chapitre === 'CALIBRAGE'` de `d.history` → défense en profondeur, ces scores ne servent pas au frontend

### Cohérence vérifiée

| Composant | Filtre CALIBRAGE | Statut |
|---|---|---|
| `saveScore()` — skip Progress update | `source !== 'CALIBRAGE'` ✅ | Déjà OK (@54) |
| `rebuildSuivi()` — skip chapitre | `cat === 'CALIBRAGE'` ✅ | Déjà OK |
| `getAdminOverview()` — skip chapitre | `cat === 'CALIBRAGE'` ✅ | Déjà OK |
| `login()` — exclut de history | `chap === 'CALIBRAGE'` ✅ | **Nouveau** |
| `renderProgress()` — skip catégorie | `k !== 'CALIBRAGE'` ✅ | Déjà OK |
| Guest flow — categorie sauvée | `'CALIBRAGE'` ✅ | **Fixé** |
| Modal flow — categorie sauvée | `'CALIBRAGE'` ✅ | **Fixé** |

## Déploiements

- GAS @54 : `fix: boost ciblé — chapters explicites dans boostFromDiag + filtre BOOST exclus P5`
- Git : `bdb2118` sur main
- GAS @55 : `fix: chapitres entamés fantômes — diagnostic categorie CALIBRAGE + filtre login history`
