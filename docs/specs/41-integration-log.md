# 41 — Journal d'intégration `app.html` (dev-ux)

> Branche `feat/diagnostic-3e`. Seul agent qui modifie `app.html`. Pas de commit, pas de push, pas d'appel prod.
> Référence : `40-parcours-epuration.md` §5 (lots L1-L10), maquettes `maquettes/*.html`, API `20-moteur.md` §8,
> PDF `30-pdf.md`, copy `50-offre-conversion.md` (+ `51`, `52`), contrat `00-contrat-commun.md` §7-9.
> Mis à jour **à la fin de chaque lot** (une coupure de session est possible).

## Reprise rapide

- **Backend de dev** : `./matheux.sh` → http://localhost:8787 (déjà lancé par l'autre agent). Comptes `dev/seed.ts` : Lina (neuve),
  Tom (express fait), Sarah (programme), mdp `matheux-dev`. Paiement simulé : `/dev/pay`, horloge : `/dev/time?jours=1`.
  Script e2e : `tools/e2e.js <scenario.js>` (login par injection du hash dans `boost_v23`, captures dans `tools/shots/`).
- Sauvegarde de départ : `app.html` d'origine = 13 801 lignes (HEAD `cf9d27a` + ligne `SU` localhost).
- Outils de travail (hors repo, dans le scratchpad de session, à recréer si perdus) :
  - `cut.js` (acorn) : `node cut.js check` (syntaxe de chaque `<script>` inline), `node cut.js rm f1 f2…`
    (supprime des déclarations top-level + commentaires `//` collés), `node cut.js loc f`.
  - `refs.js` : liste les `foo(` appelés mais jamais définis → diff avant/après chaque lot.
  - `smoke.js` (puppeteer-core + `/usr/bin/google-chrome`, 375 px) : erreurs console au chargement + capture.
  - Serveur statique : `python3 -m http.server 8765` à la racine du repo.
- Tests après chaque lot : `node cut.js check` · diff `refs.js` · `node supabase/tests/fill_match_node.js` ·
  smoke navigateur (0 erreur console) · parcours touché.
- Invariant du test fill : la zone `function _normFill` … `// ─── SÉLECTION + VALIDATION QCM` reste intacte.

## Constats d'API (lecture de `supabase/functions/api/index.ts`, 24/09)

- `start_diagnostic` / `answer_diagnostic` **exigent un `code` élève existant** : pas de diagnostic invité.
  Or la spec (Q2, contrat §7) veut la carte partielle **avant** le compte. → Besoin API n°1.
  Front : on tente le mode invité, et si le serveur le refuse on se replie sur « compte d'abord »
  (feuille E5 avant le diag, puis `start_diagnostic` avec le code). Le produit marche donc avec l'API actuelle.
- `get_training` : boost de 5 items complets (`a`, `err`, `steps`, `f`, `comp`, `item_id`, `role`), `focus` = ids,
  `streak`, `droits`, `exos_done`. Pas de libellé d'erreur type ni de titre du focus, et pas de phrase « pourquoi ».
- `get_carte` en accès free : les compétences autres que le point faible gardent seulement `id/domaine/statut`,
  **sans titre**. Du coup on ne peut pas afficher « Ça te bloque aussi sur : … » (titres de `bloque[]`).
- `save_score` : accepte `item_id`, `comp`, `type`, `nbOptions`, `reponse` → maîtrise mise à jour. Dédup
  `code+chapitre+num_exo+date`.
- Prix : `get_acces.produits` (`MX_PRODUITS`, en centimes). Les liens Stripe n'y sont pas → constante `OFFRE` côté app
  (un seul endroit, liens à créer par Nicolas).

## Besoins API (à traiter par l'ingénieur adaptatif / backend dev)

1. **Diagnostic express invité** : `start_diagnostic {type:'express'}` sans `code` → `diagnostic_id` + `guest_token` ;
   `answer_diagnostic {diagnostic_id, guest_token, …}` ; `register {…, diagnostic_id, guest_token}` rattache la session
   (et rejoue les observations dans `maitrise`/`reponses_items`). La carte invité est renvoyée masquée (free).
2. **Libellé d'erreur type dans l'entraînement** : dans `get_training.boost.exos[]`, ajouter `err_libelles: {err_id: libelle}`
   (depuis le référentiel), pour le feedback « Erreur classique : … » (40 §2.2 E7b).
3. **Titres dans la carte masquée** : garder `titre_eleve` (et `niveau_origine`) sur toutes les compétences de la carte
   free. Ce ne sont pas des résultats (50 §2.2 : « titres lisibles »), et il en faut pour `bloque[]` + la liste « pas encore mesuré ».
4. **Séance du jour** : `boost.focus_titres` (ou titres dans `focus`) + `boost.pourquoi` (phrase déterministe : cause racine /
   erreur vue / révision), pour la carte « Ta séance du jour ». En attendant, le front déduit une phrase de la carte.
5. **Entraînement libre Programme** : `get_training {code, comp}` → 5 items sur une compétence (E12 « S'entraîner sur… »),
   hors quota, sans écrire dans `daily_boosts`.
6. **Liens de paiement** : exposer les URL Payment Links dans `get_acces.produits` (ou garder la constante `OFFRE` d'app.html,
   choix actuel). À aligner avec `MX_PRODUITS`.
7. **Envoi auto du bilan express au parent (P-X0)** à la création du compte / à la fin du diag : l'app l'annonce
   (« Ta carte part aussi par mail à ton parent »). Aujourd'hui `register` envoie encore l'ancien `templateJ0`.

## Plan des lots (40 §5)

| Lot | Contenu | État |
|---|---|---|
| L1 | Code mort : `_route()` puis teasing, flow-s1/blocs, onboarding legacy/calibrage in-app, panneau DEV, mode lite, `?sim=1`, constantes legacy, stubs figures | ✅ fait |
| L2 | Gamification : XP, slots, milestones, flow, paliers, anneau, onboarding, tour, coach, nudge, « En ligne », confettis ; `mark()` réduit | ✅ fait |
| L3 | Couper l'humain : injections Suivi, motProf, pendingManual, teasing J+1, comptes à rebours, `done_v23`, historique, admin publication, `_MSGS` | à faire |
| L4 | Accès/paiement : garde premium retirée, `S.acces` + `_can()`, `OFFRE`, paywall E8 (ado sans prix mis en avant + vue parent), retour Stripe | à faire |
| L5 | Diag express adaptatif + carte partielle + inscription fusionnée + login seul | à faire |
| L6 | Accueil quotidien (4 états) + séance + fin de séance + erreur type + « ce qui a bougé » | à faire |
| L7 | Partage parent (Web Share + fallbacks, `create_share`) | à faire |
| L8 | Hub diag complet (3 modules) + carte complète + PDF (`MatheuxBilanPDF.render`) | à faire |
| L9 | Programme : « S'entraîner sur… », check-up mensuel | à faire |
| L10 | Docs | à faire |

## Journal par lot

### L1 — Code mort ✅ (13 801 → 13 222 lignes, −579)

- Le **routage est sorti de l'IIFE teasing** : il vit dans `_route()`, appelée au `DOMContentLoaded`, qui affiche aussi le
  `#landing-screen` (l'IIFE ne le fait plus). Routes : `#diag`, `#diag?src=x`, `#diag-x` (ancien format), `#trial-x`, `#login`. `?src=` est
  accepté dans le hash ou dans la query.
- Supprimés :
  - la page teasing (HTML + IIFE compte à rebours + waitlist) ;
  - flow-s1 « Comment on t'aide ? » avec ses blocs (HTML + 4 fonctions `_flowPick*` / `_flowToggleBloc` / `_flowBackToChoice`) ;
  - l'onboarding legacy `auth-step-2`, `finalizeOnboarding`, `updateLevelChapters`, `startCal`, les branches `calState` `sel` / `test`
    de `render()`, la branche `CALIBRAGE` de `chkComp`, `renderDiagInsight` et `dismissDiagInsight` ;
  - le panneau DEV (HTML, CSS, `triggerAdmin` / `logAdmin` / `simTime` / `forceFailChap`), la branche `S.forceFail` de `mark()` et
    `S.timeOffset` de `sendScore` ;
  - `?sim=1` et `_simulateNextDay` ;
  - `DEMO_QS`, `CHAPS_BY_LEVEL`, les stubs `autoDetectFigure` / `renderFig` / `isGeoCat` ;
  - le mode lite : affectation `S.lite` et gardes simples retirées. Il reste des `S.lite` inertes (toujours `undefined`) dans des
    fonctions qui partent en L2, L3 et L6.
- **Auth = connexion seule** (B12) : onglets et formulaire d'inscription retirés de `#auth-screen`, `submitAuth` ne fait plus que le
  login, `switchTab` réduit. Titre « Se connecter ».
- Gardés volontairement jusqu'à L5/L6 : `BREVET_PACK` (utilisé par l'ancien flow diag), `CHAP_BLOCS` (utilisé par le rendu de la liste
  de chapitres) et `TS` (utilisé par le loader boost).
- Tests : `cut.js check` OK · aucune nouvelle référence indéfinie (diff `refs.js` vide) · `fill_match_node.js` all ok · smoke 375 px :
  `/app.html`, `#login` (modale connexion affichée) et `#diag?src=hero` sans erreur JS. La seule erreur console est le 501 du serveur statique
  sur `POST /api`, attendue sans backend.


### L2 — Gamification ✅ (13 222 → 12 305 lignes, −917)

- **`mark()` réécrit** (23 lignes au lieu de ~110) : score → `sendScore(…, xp=0, …)` → mission du jour → `chkComp` → avance.
  L'auto-avance ne dépend plus des slots (piège §1.2-2). J'ai aussi retiré le calcul local du streak (écriture `LK`) : le streak
  passe côté serveur en L6. En attendant, `S.stk` garde la valeur locale de l'`initApp`.
- **M4** : dans `validateAnswer`, la branche coach est retirée et seul le toast ko reste, sans condition (QCM et fill).
- Supprimés (34 déclarations) :
  - XP : `showXP`, `#ui-xp`, bonus de `chkComp` ;
  - slots : `_slotCount`, `_checkSlotReward`, `_showSlotReward` ;
  - `_showDailyReward` et `_cycleDailyTarget` (cible fixe 5) ;
  - milestones et coach marks (`_coKey`, `_markCoach`, `_needsCoach` + tous les tips T1-T8, brouillon, formule, indice, timer, auto,
    boost_first) ;
  - mode Flow, paliers `_chapTier`, anneau `rMastery` + `#mastery-w`, onboarding, tour guidé (8 fonctions + variables), nudge
    `startNudge` / `clearNudge` ;
  - `_boostInsightConfetti`, `_checkCoursMilestone`, `verify` et la flashcard d'auto-évaluation (D3) ;
  - « En ligne » et `#flow-box`.
- Timer (D10 💤) : code gardé mais **débranché** (plus de `_startTimer` dans `goEx` / `togCat`, plus de `_renderTimerSVG` dans `rSection`).
- `launchConfetti` gardée pour la carte complète (L8). Tous ses appels de fin de chapitre ont été retirés, sauf celui de l'ancien écran
  diag du flow, qui part en L5.
- **Bug corrigé (prod aussi)** : `flushQ` envoyait `save_scores_batch` **sans `code`** (ni email, nom ou niveau). Le serveur répond
  « code et scores[] requis. » : aucun score de la file ne partait, avec des retries à l'infini. Désormais, 1 batch = 1 élève, avec
  `code`, `email`, `name` et `level` à la racine. Vérifié : `daily_boosts.exos_done` passe à 2 côté serveur après 2 réponses.
- Tests :
  - `cut.js check` OK, aucune nouvelle référence indéfinie, `fill_match_node.js` all ok ;
  - e2e sur le backend de dev (Tom) : login, ouverture du boost, 2 réponses justes. Résultat : EASY ×2, 🎯 2/5, auto-avance vers l'exo 3,
    file vide, 0 erreur console.
- Constaté au passage, traité en L6 : énoncé multi-lignes aplati (programme Raphaël en une ligne) → exigence contrat §8.
