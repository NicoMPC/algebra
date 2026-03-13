# test_debug.md — Bugs à corriger (audit 13 mars 2026)

> Résultat de l'audit complet : lecture codebase + simulation 7 jours GAS réel (5 profils).
> **Ne coder qu'après relecture de ce fichier + validation Nicolas.**
> Ordre de correction : Lot 1 → Lot 2 → Lot 3.

---

## LOT 1 — Critique, 30 min, avant tout élève réel

### BUG-01 — `formatDateFR` → Invalid Date → `inactivityDays=9131`

**Confirmé :** `inactivityDays=9131` pour Lucas à J+3 en simulation réelle GAS.
**Symptôme :** champ `inactivityDays` retourne une valeur aberrante dans `getAdminOverview`.

**Cause :**
- `rebuildSuivi` ligne 1343 : prend une date ISO (`"2026-03-13"`) depuis Scores, la passe dans `formatDateFR()` qui retourne `"13/03/2026 00:00"` (dd/MM/yyyy HH:mm), et l'écrit en Suivi col D.
- `getAdminOverview` relit → `.substring(0,10)` = `"13/03/2026"` → `new Date("13/03/2026")` = Invalid Date en V8 → `Math.floor(NaN)` → valeur aberrante.
- Même bug à `rebuildSuivi:1423` et `getAdminOverview:3125` (inactif7jAdmin).

**Fix — backend.js ligne 1343 :**
```javascript
// AVANT :
var lastDate = dates.length ? formatDateFR(dates[dates.length - 1]) : '';
// APRÈS :
var lastDate = dates.length ? dates[dates.length - 1] : '';
```
> Les dates dans Scores sont déjà au format ISO `yyyy-MM-dd` (produites par `today()`). Pas besoin de reformater.

---

### BUG-02 — BLOQUÉ affiché pour tous les nouveaux élèves

**Confirmé :** Emma et Lucas montrés en `🔴 BLOQUÉ` dans le dashboard admin dès J+0.
**Symptôme :** tous les élèves en rouge → dashboard inutilisable.

**Cause :**
- `getAdminOverview` ligne 3129 : si `lastConnection` est vide (élève sans aucun score), le `else` met `inactif7jAdmin = true`.
- Si l'élève a des exos avec score < 40 (normal en début de cursus), la condition BLOQUÉ se déclenche.

**Fix — backend.js ligne 3129 :**
```javascript
// AVANT :
} else {
  inactif7jAdmin = true;
}
// APRÈS :
} else {
  inactif7jAdmin = false;  // Pas encore connecté ≠ inactif depuis 7j
}
```

---

### BUG-03 — `saveBoost` + `saveScore` double-comptage ExosDone

**Symptôme :** admin peut voir "6/5 exos" ou boost jamais marqué terminé.

**Cause :**
- `saveBoost()` ligne ~606 : initialise `ExosDone = exoIdx + 1` dans DailyBoosts.
- Ensuite `saveScore()` avec `source='BOOST'` ligne ~558 : incrémente de +1 à nouveau.
- Résultat : 5 exos faits → ExosDone=6 au lieu de 5.

**Fix — backend.js ligne ~606 — saveBoost() :**
```javascript
// AVANT :
appendRow(SH.BOOSTS, [code, todayStr, JSON.stringify(p.boost), exosDone]);
// APRÈS :
appendRow(SH.BOOSTS, [code, todayStr, JSON.stringify(p.boost), 0]);
// saveScore() avec source=BOOST est la seule source de vérité pour ExosDone
```

---

## LOT 2 — Moyen, 1h, avant usage intensif admin

### BUG-04 — `publishAdminChapter` écrase silencieusement le slot G si >4 chapitres

**Symptôme :** Nicolas publie un 5e chapitre → l'ancien Ch1 disparaît sans avertissement.

**Cause :** `backend.js` ligne ~3420 : si les 4 slots (G/J/M/P) sont pleins, overwrite silencieux sur slot G.

**Fix — backend.js ligne ~3418 :**
```javascript
// Ajouter un flag overwrite dans le return :
if (!written) {
  suiviSh.getRange(si + 1, SLOTS_1[0]).setValue(chapJSON);
  written = true;
  overwriteWarning = true;  // déclarer var overwriteWarning = false; en haut
}
// Dans le return :
return { status: 'success', message: 'Chapitre publié.', overwrite: overwriteWarning || false };
```
**Fix — index.html — toast dans la modale admin après publish_chapter :**
```javascript
// Si resp.overwrite === true :
showToast('⚠️ 4 chapitres déjà en attente — Ch1 remplacé par le nouveau', 'warn');
```

---

### BUG-05 — CHAPITRE TERMINÉ masqué par BOOST TERMINÉ

**Confirmé :** Emma J+5, 20 exos de chapitre terminés, admin voit seulement BOOST TERMINÉ.
**Symptôme :** Nicolas publie le boost, passe à l'élève suivant, oublie d'assigner le chapitre suivant.

**Cause :** `getAdminOverview` ligne 3111-3119 : BOOST TERMINÉ pushé AVANT CHAPITRE TERMINÉ dans `actionsAdmin[]`. `actionPriority = actionsAdmin[0]` → BOOST TERMINÉ prime toujours.

**Fix — backend.js lignes 3111-3119 — inverser l'ordre :**
```javascript
// CHAPITRE TERMINÉ en premier (plus structurel, plus rare)
if (hasChapTermineAdmin) {
  actionsAdmin.push('✅ CHAPITRE TERMINÉ → assigner la suite');
}
if (userBoosts.length >= 1 && lastBoostExosDoneAdmin >= 5 && !boostNewPending && !boostPendingFlag && !boostInProgressFlag) {
  actionsAdmin.push('⚡ BOOST TERMINÉ → préparer le suivant');
}
```

---

### BUG-06 — `rebuildSuivi` compte les exos BOOST dans le compteur chapitre

**Symptôme :** CHAPITRE TERMINÉ peut s'afficher prématurément dans la Sheets Suivi (incohérence avec le dashboard admin qui lui est correct).

**Cause :** `rebuildSuivi` ligne 1350 filtre `cat==='BOOST'` mais les exos boost sont sauvegardés avec `categorie=oC` (nom du chapitre) + `source='BOOST'`. Donc ils passent le filtre et gonflent `chapCount`.

**Fix — backend.js ligne 1350 :**
```javascript
// AVANT :
if (!cat || cat === 'CALIBRAGE' || cat === 'BOOST') return;
// APRÈS :
var src = String(r['Source'] || '');
if (!cat || cat === 'CALIBRAGE' || cat === 'BOOST' || src === 'BOOST') return;
```

---

## LOT 3 — Qualité, 30 min

### BUG-07 — Decay inactivité appliqué N fois par session au lieu de 1

**Symptôme :** élève inactif 30j qui fait 5 exos perd 5× la pénalité au lieu de 1×.

**Cause :** `updateConfidenceScore` ligne 1165 : la soustraction `score -= (daysDiff-14)*0.5` est appliquée à chaque appel de `saveScore`. 5 exos en une session = 5 pénalités.

**Fix — backend.js ligne 1165 :**
```javascript
// Appliquer le decay seulement si lastPractice n'est pas aujourd'hui
if (daysDiff > 14 && lastPractice !== todayStr) {
  score = Math.max(0, score - Math.floor((daysDiff - 14) * 0.5));
}
```

---

### BUG-08 — Email J+0 peut être envoyé 2 fois

**Cause :** `sendMarketingSequence` ligne ~3678 : pas de vérification si J+0 a déjà été envoyé. Si l'élève s'inscrit à 8h (J+0 auto) et le cron passe à 9h, 2 emails de bienvenue.

**Fix — backend.js — case 0 dans sendMarketingSequence :**
```javascript
case 0:
  var alreadySent = getRows(SH.EMAILS).some(function(r) {
    return String(r['Email']||'').toLowerCase() === email.toLowerCase()
      && (r['Type'] === 'J+0' || r['Type'] === 'J+0-manuel')
      && r['Statut'] === 'envoyé';
  });
  if (alreadySent) break;
  _sendWelcomeEmail(user, prenom, niveau);
  _logEmail(email, prenom, 'J+0', 'envoyé');
  break;
```

---

## Cosmétique (5 min total)

### BUG-09 — Message erreur `sendMarketingSequence` oublie J+5
**Ligne :** `backend.js:~3762`
```javascript
// AVANT : 'Valeurs acceptées : 0, 3, 7.'
// APRÈS : 'Valeurs acceptées : 0, 3, 5, 7.'
```

### BUG-10 — `streakAlert` toujours false
**Ligne :** `backend.js:~1176`
Variable déclarée mais jamais mise à `true`. Soit implémenter, soit supprimer du return pour ne pas induire en erreur.

### BUG-11 — Scripts Python : `do_diagnostic()` mauvaise `categorie`
**Fichiers :** `sim_7days.py`, `create_5_students.py`, `create_demo_student.py`
Ces scripts sauvegardent les scores diagnostics avec `categorie=chapter_name` au lieu de `categorie='CALIBRAGE'`.
La prod (`index.html`) utilise bien `'CALIBRAGE'`. À corriger dans tous les scripts de test.

### BUG-12 — `simulateNextDay` erreur sur DailyBoosts vide
**Ligne :** `backend.js:~4022`
Retourne une erreur si l'élève n'a aucun boost. À gérer avec un return silencieux `{ status: 'ok', message: 'Aucun boost.' }`.

---

## Actions non-code (bloquantes avant vrais élèves)

| Action | Où | Priorité |
|---|---|---|
| Configurer alias `no-reply@matheux.fr` dans Gmail | Hébergeur email + Gmail paramètres | 🔴 |
| Activer trigger `triggerDailyMarketing` 9h-10h | Apps Script UI → Triggers | 🔴 |
| Passer Stripe TEST → PROD (3 occurrences) | `index.html`, `backend.js`, `cgv.html` | 🔴 |
| Webhook Stripe → colonne Premium dans Users | Stripe dashboard + GAS | 🟡 |

---

## Déploiement après fixes

```bash
# Backend
cd "/home/nicolas/Bureau/algebra live/algebra"
clasp push --force
clasp deploy --deploymentId AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF --description "@60 bugfixes audit mars"

# Frontend (si index.html modifié)
git add index.html && git commit -m "fix: BUG-04 toast overwrite chapitre" && git push origin main
```

---

## Contexte simulation (pour référence)

5 profils créés le 13 mars 2026, base prod nettoyée (admin HMD493 conservé) :

| Code | Prénom | Niveau | Notes |
|---|---|---|---|
| MNPNYL | Emma | 6EME | 7j simulés complets — BUG-01/02/05 observés |
| CCRWTE | Lucas | 5EME | 7j simulés complets — BUG-01 `inactivityDays=9131` confirmé |
| 3TE3G5 | Inès | 3EME | 1j simulé |

Ces comptes sont dans la base prod (IsTest=0 non admin — attention à la limite 50).
