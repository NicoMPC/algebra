# 41 — Journal d'intégration `app.html` (dev-ux)

> Branche `feat/diagnostic-3e`. Seul agent qui modifie `app.html`. Pas de commit, pas de push, pas d'appel prod.
> Référence : `40-parcours-epuration.md` §5 (lots L1-L10), maquettes `maquettes/*.html`, API `20-moteur.md` §8,
> PDF `30-pdf.md`, copy `50-offre-conversion.md` (+ `51`, `52`), contrat `00-contrat-commun.md` §7-9.
> Mis à jour **à la fin de chaque lot** (une coupure de session est possible).

## Reprise rapide

- **Backend de dev** : `./matheux.sh` → http://localhost:8787 (déjà lancé par l'autre agent). Comptes `dev/seed.ts` : Lina (neuve),
  Tom (express fait), Sarah (programme), mdp `matheux-dev`. **J'utilise ma propre instance** (port 8790,
  `DEV_DATA_DIR=<scratchpad>/devdata`, graine copiée dans `db.seed.json`) pour ne pas toucher à la base partagée du 8787. Paiement simulé : `/dev/pay`, horloge : `/dev/time?jours=1`.
  Script e2e : `tools/e2e.js <scenario.js>` (login par injection du hash dans `boost_v23`, captures dans `tools/shots/`).
- Sauvegarde de départ : `app.html` d'origine = 13 801 lignes (HEAD `cf9d27a` + ligne `SU` localhost).
- Outils de travail : **`/tmp/matheux-devux/`**, hors repo. Le scratchpad de session a été effacé 2 fois par les coupures.
  On y trouve `cut.js`, `refs.js`, `e2e.js` (+ scénarios `s_*.js`, captures `shots/`) et `devserver.sh reset|start` (instance privée du backend de dev
  sur **8790**, base `/tmp/matheux-devux/devdata`). Si ce dossier est perdu, il faut recréer les outils décrits ci-dessous :
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

> Livré le 25/09 par l'ingénieur adaptatif (`supabase/functions/api/index.ts`, migrations `20260925_*.sql`).
> Tests : `./matheux.sh test` (smoke 101 checks dont les attaques, + navigateur) · `deno test -A supabase/tests/`.
> **Règle commune** : toute action élève envoie `code` + `access_token`. Un refus d'authentification renvoie
> `{status:'error', auth_requise:true, message}` → le front tente `refresh_session`, sinon écran de connexion.

1. ✅ **Diagnostic express invité** (table `diagnostics_invites`, jeton hashé, expire 2 j, prolongé de 2 j à la fin).
   - `start_diagnostic {type:'express', prenom?}` **sans `code` ni `access_token`** → `{status, invite:true, diagnostic_id, guest_token (48 hex, 1 seule fois), expires_at, type, repris:false, question, progression, termine, carte:null, droits}` (`droits.acces = 'free'`).
   - Reprise : `start_diagnostic {diagnostic_id, guest_token}` → même forme, `repris:true`, question en attente, pas de nouveau `guest_token`.
   - `answer_diagnostic {diagnostic_id, guest_token, item_id, reponse, temps?}` → `{status, invite:true, question|null, fin_module:null, progression, termine, carte (masquée free, à la fin), corrections (à la fin)}`.
   - Refus : jeton faux / d'un autre diag / expiré / déjà rattaché → `{status:'error', invite_expire:true, message}`. `type` ≠ express sans compte → `auth_requise`.
   - `register {name, email, level, password, objectif?, diagnostic_id, guest_token}` → en plus des champs habituels : `access_token, refresh_token, expires_at, diagnostic_id (nouvel id dans diagnostics), diagnostic_rattache:true, carte (masquée free)`. Les observations sont rejouées dans `maitrise` / `reponses_items` (contexte diag), la carte est recalculée avec le prénom. Session invalide → compte créé quand même, `diagnostic_rattache:false` + `rattachement_erreur`.
   - Rien n'est écrit dans `maitrise` / `reponses_items` avant le compte ; la copie invitée est vidée après rattachement.
2. ✅ **`err_libelles`** : chaque `get_training.boost.exos[i]` porte `err_libelles: {"NC.FRAC.03#somme_directe": "Additionne numérateurs…"}` (les ids d'erreur de `exos[i].err` ; une erreur d'un prérequis direct est cherchée dans sa compétence). `{}` si l'item n'a pas d'erreur type. Les séances déjà créées sont complétées à la lecture.
3. ✅ **Carte masquée** (free) : chaque `carte.competences[]` masquée = `{id, domaine, statut, titre_eleve, niveau_origine, masque:true}` (ni `maitrise`, ni `erreurs`, ni `bloque`). Le point faible reste détaillé. **En plus** (toutes cartes renvoyées par `get_carte`, `start/answer_diagnostic`, `register`) : `carte.non_mesurees = [{id, titre_eleve, domaine, niveau_origine}]` = compétences de 3e diagnostiquables pas encore conclues (liste « pas encore mesuré »).
4. ✅ **Séance du jour** : `boost.focus_titres = [{id, titre_eleve, niveau_origine, domaine}]` (ordre de `boost.focus`) et `boost.pourquoi` (1 phrase, tutoiement). Règle : cause racine (« On attaque « X » : c'est une notion de 5e qui te freine sur 2 autres points du programme. ») > erreur type déjà vue (« …tu as fait l'erreur classique « … ». ») > statut (à construire / fragile / découverte) ; + « Puis « Y ». » si 2e focus ; + « Et 1 révision de « Z » pour ne pas l'oublier. » ; sans focus : « Ta zone de travail est acquise : séance d'entretien… ». Jamais « prof ».
5. ✅ **Entraînement libre Programme** : `get_training {code, access_token, comp}` → `{status, libre:true, boost:{generatedBy:'libre', libre:true, date, comp, focus:[comp], focus_titres, pourquoi, zone:null, banque_insuffisante, exos:[…même forme que la séance, role:'libre', num ≥ 101]}, exos_done:0, source_score:'LIBRE', streak, droits}`. N'écrit pas `daily_boosts`, hors quota, exclut les items de la séance du jour, évite ce qui vient d'être répondu. Gratuit / diagnostic seul → `{status:'error', paywall:'programme_brevet', droits}`. Compétence inconnue → erreur. **Réponses** : `save_score {…, source:'LIBRE', item_id, reponse}` (réservé au Programme, contexte `train`, pas de `progress` legacy, n'incrémente pas `exos_done`).
6. ✅ **Prix** : la constante `OFFRE` (URL des Payment Links) reste dans `app.html`. `get_acces {code, access_token}` → `produits = {diagnostic_complet:{libelle, prix_cents:1900, offre:'diag_complet'}, programme_brevet:{libelle, prix_cents:4900, offre:'programme_brevet', deduction:{si:'diagnostic_complet', cents:1900}}, programme_upgrade:{libelle, prix_cents:3000, offre:'programme_upgrade', si:'diagnostic_complet'}}` (source unique `MX_PRODUITS`). Ce que **cet** élève paierait : `droits.prix_cents` (inchangé). `offre` = `metadata.produit` à mettre sur chaque Payment Link.
7. ✅ **Bilan express au parent (P-X0)**, remplace `templateJ0` : envoyé quand la carte express existe ET que le compte existe (fin de l'express avec compte, ou `register`/`login` qui rattache un diag invité terminé). Vouvoiement, sans prix, spec `51` §2 ; 1 seule fois par adresse (`email_logs.type = 'D3:P-X0'`, `categorie 'T'`, `code`), jamais si UNSUB. Liens : `https://matheux.fr/b/<token>?src=email_px0` (voir le bilan) et `https://matheux.fr/b/<token>?confirmer=1` (partage dédié `canal='email_parent'`, 30 j). **Nouvelle action publique** pour la page parent : `confirm_parent {token, optin_marketing?, texte_version?, texte_hash?}` → `{status, confirme:true, optin_marketing}` (pose `consentement_parent_at`, l'opt-in, une ligne `consentements` produit `compte`) ; refusée avec un lien créé depuis l'app (`create_share` force `canal='app'`). `register` sans diag n'envoie plus rien au parent (P-X0 partira à la fin du diag).
8. ✅ **Sécurité** : helper unique `mxSessionUid` (jeton → `auth.getUser`), `mxAuth` (le jeton doit être celui du profil `code`) et `requireAdmin` (+ `is_admin`).
   - **Exigent `code` + `access_token`** : `get_carte`, `get_training`, `get_acces`, `start_diagnostic` / `answer_diagnostic` (avec code), `create_share`, `revoke_share`, `set_preferences`, `log_consent` (sauf page parent, ci-dessous), `save_score`, `save_scores_batch`, `save_boost`, `save_calibration_batch`, `get_progress`, `check_trial_status`, `generate_adaptive_boost`, `save_brevet_result`. Lecture admin autorisée (jeton admin + code élève) sur `get_carte`, `get_acces`, `get_progress`, `check_trial_status`, `generate_adaptive_boost` ; jamais d'écriture admin au nom d'un élève (A6).
   - **Admin seulement** (garde centrale `ADMIN_ONLY`, même liste que le hotfix prod `4fc6123`) : `get_admin_overview`, `publish_admin_boost`, `publish_admin_chapter`, `get_cours_admin`, `save_cours`, `send_admin_email`, `send_test_email`, `send_marketing_email`, `log_manual_email`, `send_weekly_report`, `send_custom_email`, `send_session_rapport`. `cron_send_emails {cron_secret}` (secret `CRON_SECRET`, migration `20260925_cron_secret.sql`) ou jeton admin.
   - **Publiques** : `register`, `login`, `login_token`, `refresh_session`, `forgot_password`, `reset_password` (jeton de récupération), `get_bilan_partage`, `confirm_parent` et `log_consent {token}` (jeton de partage), diag invité (`guest_token`), webhook Stripe signé, `unsubscribe`, formulaires (`submit_feedback`, `log_contact`, `send_contact`, `report_exo`), contenus legacy sans donnée élève (`generate_diagnostic`, `get_brevet_chapters`, `generate_brevet_session`). `log_funnel_event` : public, mais le `code` n'est gardé que s'il est prouvé (`access_token`, ou `token` de partage) — sinon événement anonyme.
   - Portés de la prod (audit 11/04, non commité) : whitelist du prénom (`register`, prénom invité), erreurs d'upsert `scores` remontées, `progress` recalculé depuis `scores`, `free_chapter` pondéré (calibrage), `send_admin_email`, `targetCode` dans `publish_admin_*`, `stripe_webhook` hors dispatch.
   - Tests d'attaque (smoke) : 17 actions élève × {code seul, jeton d'un autre élève} refusées ; 13 actions admin/email × {sans jeton, code admin public, jeton élève} refusées, 0 mail parti ; faux `cron_secret` ; prénom XSS.
9. ✅ **Sessions** : `login` et `register` renvoient `access_token`, `refresh_token`, `expires_at` (s). `login_token {access_token, refresh_token?}` → **même réponse que `login`** ; si `access_token` est expiré et `refresh_token` fourni, la session est renouvelée et la réponse porte les **nouveaux** jetons (à re-stocker : le refresh token Supabase est à usage unique). `refresh_session {refresh_token}` → `{status, access_token, refresh_token, expires_at, code}`. Échec → `auth_requise:true`. Garder dans `boost_v23` : `code`, `access_token`, `refresh_token` (plus le hash).
10. ✅ **Monitoring admin** : `get_admin_overview {access_token}` ajoute `diagnostics: [{id, code, type, statut, n_questions, started_at, finished_at, score_global, point_faible, fiabilite}]`, `diagnostics_stats: {express|complet|mensuel: {en_cours, termine, abandonne}}`, `invites: {en_cours, termine, rattache, expires}`, `achats: [lignes achats, récentes d'abord]`, `ca_cents` (hors remboursés), `funnel: {event: {total, j7, j30}}`.
11. ✅ **Question de diagnostic** (fait au passage) : chaque `question` porte `domaine` et `niveau_origine` de sa compétence.
12. ✅ **Rattachement au login** (fait au passage) : `login {email, password, diagnostic_id, guest_token}` rattache comme `register` → en plus : `diagnostic_id`, `diagnostic_rattache`, `rattachement_erreur?`. P-X0 part si c'est la 1re carte express de cette adresse.
13. ⏳ **P-SH (envoi du lien par email via Resend)** : pas fait. À cadrer : l'ado saisit une adresse libre, donc risque de relais de spam → il faut un plafond (ex. 3 envois / jour / élève) et le template `51` §2 P-SH. En attendant : `mailto:`.
14. ✅ **État des partages** (fait au passage) : `get_carte.partages = [{token, created_at, expires_at, vues, dernier_vu_at, canal}]` (liens actifs, récents d'abord ; `canal` = `app`, `whatsapp`… ou `email_parent` pour le lien du mail P-X0).

## Plan des lots (40 §5)

| Lot | Contenu | État |
|---|---|---|
| L1 | Code mort : `_route()` puis teasing, flow-s1/blocs, onboarding legacy/calibrage in-app, panneau DEV, mode lite, `?sim=1`, constantes legacy, stubs figures | ✅ fait |
| L2 | Gamification : XP, slots, milestones, flow, paliers, anneau, onboarding, tour, coach, nudge, « En ligne », confettis ; `mark()` réduit | ✅ fait |
| L3 | Couper l'humain : injections Suivi, motProf, pendingManual, teasing J+1, comptes à rebours, `done_v23`, historique, admin publication, `_MSGS` | ✅ fait (+ dispatcher `render()` avancé de L6) |
| L4 | Accès/paiement : garde premium retirée, `S.acces` + `_can()`, `OFFRE`, paywall E8 (ado sans prix mis en avant + vue parent), retour Stripe | ✅ fait |
| L5 | Diag express adaptatif + carte partielle + inscription fusionnée + login seul | ✅ fait |
| L6 | Accueil quotidien (4 états) + séance + fin de séance + erreur type + « ce qui a bougé » | ✅ fait |
| L7 | Partage parent (Web Share + fallbacks, `create_share`) | ✅ fait |
| L8 | Hub diag complet (3 modules) + carte complète + PDF (`MatheuxBilanPDF.render`) | ✅ fait |
| L9 | Programme : « S'entraîner sur… », check-up mensuel | ✅ fait |
| L10 | Docs | ✅ fait (hors CLAUDE.md, voir propositions) |

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

### L3 — Couper l'humain ✅ (12 305 → 6 381 lignes, −5 924)

- **`initApp` réécrit** (~60 lignes au lieu de ~350). Il garde `LVL[niv].cats` (§1.2-6) et l'historique, filtré pour la séance du jour :
  les clés `BOOST-n` se répètent chaque jour, donc seules les réponses **d'aujourd'hui** sont réinjectées. Retirés :
  - les injections `nextChapter` / `nextBoost` / `pendingBrevet` / `revisionChapters` / `dynamicChapters` ;
  - `pendingManual`, `assignedByProf`, `motProf` ;
  - `done_v23` (purgé au login) et le regroupement historique en passages ;
  - le teasing J+1 et le toast streak local.
- **`chkComp` réduit** : fin de série BOOST → `S.boostInsight`, qui ouvre l'écran fin de séance. Plus d'`enqueue` LLM, d'XP,
  de feedback emojis ni de persistance locale.
- **Dispatcher `render()` écrit dès ce lot**, pour ne pas patcher 700 lignes de hero et de liste de chapitres vouées à partir (§1.2-5).
  Aiguillage : `admin` / fin de séance / `session` / `home`. Nouvelles fonctions :
  - `renderHome` : séance du jour (prête, en cours « Continue, encore n exos », faite), erreur réseau → Réessayer ;
  - `openSession`, `closeSession` (toast « Sauvegardé »), `renderSession` (barre ← Accueil + progression + `rSection` inchangé),
    `renderSeanceFin` ;
  - `togCat` devient un alias d'`openSession`.
- **`loadTraining()`** appelle `get_training` après le login. La séance est servie par le moteur : `S.boost` alimente `LVL.cats.BOOST`,
  streak serveur, droits. 🎯 n/5 = exos faits dans la séance (état serveur), plus de compteur localStorage.
- **Admin = monitoring en lecture seule**. ~2 900 lignes de publication remplacées par ~70 : liste des élèves (inscription, exos 7 j,
  dernier jour, Programme), KPI, et fiche élève via `get_carte`, rendue par `renderCarte` quand elle existera (L5).
  **Sécurité (message coordinateur)** : `login` renvoie `access_token`, que je garde dans `S.token` et dans `boost_v23`, et que
  j'envoie à `get_admin_overview`.
- **Mot de passe oublié** (message coordinateur) : le champ « code 8 caractères » est supprimé. Le mail contient un lien
  `app.html#reset&access_token=…&type=recovery` : `_route()` ouvre le formulaire (email + nouveau mdp), qui envoie `reset_password {email, access_token, password: h256}`.
- Supprimés entièrement :
  - modules 💤/❌ Brevet blanc (~590 L), Progression (E12), Audit (G2, compte supprimé), archives rétro et modales (E14), cours adaptatif (E23) ;
    ils contenaient du texte « ton prof ». Récupérables dans git (`cf9d27a`) pour la v1.1. `_renderRetroExo` est gardé (L8 : revoir ses réponses) ;
  - `renderMotProf`, teasing J+1, comptes à rebours, `launchRevision`, `handleBoost`, `boostFromDiag`, `startTs`, `TS`, modale `m-boost` ;
  - carrousel, tendances, `_catToBloc`, bandeau prérequis, nav 3 onglets (`updNav` vide, `setView` réduit) ;
  - actions parent de l'admin.
- `_MSGS` nettoyé (F8) : les clés `ok_*`/`ko_*`/`net_*` sont gardées, les clés §2.1 ajoutées (`diag_*`, `seance_fin_*`, `err_retour`, `mod_*`,
  `checkup_invite`, `carte_racine`).
- Nouveau bloc CSS `PARCOURS DIAGNOSTIC 3E (v2)` : tokens `--lac/--fra/--acq/--ne` + composants `.mx-*` repris des maquettes, avec
  compatibilité mode nuit via `--mx-card-bg` / `--mx-border`.
- Tests :
  - `cut.js check` OK, grep H2 (`prof prépare|ton prof|Nicolas prépare`) = **0**, `fill_match_node.js` all ok ;
  - e2e (8790), Tom : séance du jour servie par `get_training` → 5 réponses justes/fausses → écran « Séance faite ✓ n sur 5 du premier
    coup ». Rechargement : « Continue, encore 1 exo », puis « Séance faite », 🎯 5/5 ;
  - e2e (8790), admin Nicolas : monitoring (3 inscrits, Sarah Programme, 35 exos / 7 j) avec `access_token` ;
  - 0 erreur console.
- Points ouverts :
  - `boost_v23` contient toujours le **hash du mot de passe** (auto-login par `login` email+hash). Pour ne garder que le jeton, il faudrait
    une action `login_token` (Besoin API n°9) ;
  - le PWA nudge post-login (A11) n'est plus appelé : à rebrancher après la 3e séance (L6).

### L4 — Accès et paiement ✅ (6 381 → ~6 480 lignes)

- **Garde premium retirée en un seul patch** : les 9 modules (`startPremiumGuard`, `_verifyPremiumStatus`, `_sealTrial`, hash d'intégrité,
  boucle 30 s, visibilité, détection DevTools, anti-debugger, `isPremiumOrTrialValid`) et leurs appels, y compris dans `initApp`.
  Le reste d'`_updateIntegrityHash` part avec l'ancien flow en L5. Retirés aussi : `_isChapLocked`, `showLockedOverlay`, `showTrialExpired`,
  `__unlockAll`, `_stripeUrl` (liens par niveau à 29,99 €), les overlays de paiement « Tous les chapitres… Bon courage pour le Brevet ».
- **`S.droits`** = objet `mxDroits` du serveur (`get_training` / `get_acces`). `_acces()`, `_can('diag_complet'|'pdf'|'programme')`,
  `refreshDroits()`. Le front ne fait qu'afficher : c'est le serveur qui refuse (`start_diagnostic` complet → `paywall`).
- **`OFFRE`**, seul endroit des prix affichés et des liens (H5) : `{diag 19, prog 49, upgrade 30, garantie_jours 30}`. Les montants
  effectifs, déduction comprise, viennent de `droits.prix_cents`.
  - **Liens Stripe vides** : à créer par Nicolas (50 §4.1). Redirection de succès à configurer : `app.html?achat=<produit>`.
  - Tant qu'un lien est vide, le bouton affiche « Paiement bientôt disponible : écrivez-nous ». En localhost, un faux lien `buy.stripe.com/dev_*`
    est intercepté par le backend de dev.
  - `client_reference_id` = code élève + `prefilled_email`.
- **Paywall ado (`openPaywall`)** : contrat §7 + 50 §2.3. J'ai écarté l'écran de la maquette 03, qui avait des boutons d'achat.
  - Contenu : « Ce que le diagnostic complet ajoute », « L'express a mesuré n compétences sur N », et le prix cité **une fois** en texte :
    « c'est une décision pour tes parents, pas pour toi ».
  - Boutons : principal « Continuer gratuitement → mes 5 exos du jour », secondaire « 📨 Montrer ma carte à mes parents », et lien « Je suis le parent ».
  - `paywall_view {vue:'ado'}`.
- **Vue parent (`openParentView`)** : 50 §2.4, vouvoiement.
  - Deux offres. Si le diag est déjà payé, une seule offre « Programme — 30 € (19 € déduits) ».
  - **Cases A + B / B' de 52 §2.3**, non cochées : la redirection est bloquée tant qu'elles ne sont pas cochées.
  - `log_consent {produit, texte_version, texte_hash SHA-256 du texte affiché, cases[]}` avant la redirection, puis `checkout_click`.
  - Garantie 30 jours, « paiement unique, pas d'abonnement, accès sans date de fin », bio fondateur (« ancien ingénieur qui accompagne des élèves en maths
    depuis des années »).
- **Retour Stripe** (`?achat=<produit>`, ou l'ancien `?payment=success`) : `_pollAchat` interroge `get_acces` toutes les 2 s pendant 60 s, puis affiche
  un message par produit : « Diagnostic complet débloqué → Commencer le module 1 » ou « Programme Brevet activé ».
- Badge header (C1) : chip « Gratuit · voir ce qui est inclus » → paywall ; « Diagnostic complet ✓ » → vue parent (upsell) ; rien pour le Programme.
- `openSheet` / `closeSheet` : bottom sheet générique (375 px, 92vh). Stubs `openShare` / `openDiagHub`, remplacés en L7 et L8.
- Tests e2e (8790), Tom :
  - chip → paywall ado → vue parent ;
  - sans les cases, pas de redirection ;
  - avec les cases : `consentements` a 1 ligne (version, hash, 2 cases), le paiement simulé via le faux lien Stripe réussit, et au retour
    `?achat=diag_complet` affiche « Diagnostic complet débloqué » avec `S.droits.acces = diagnostic_complet` ;
  - 0 erreur console.

### L5 — Diagnostic express adaptatif + carte partielle ✅ (→ 5 356 lignes)

- **L'ancien flow est supprimé** (~1 100 lignes) : `startTrialFlow` et toutes les `_flow*`, 5 questions tirées côté client, choix d'objectif,
  upsell avant inscription, `save_calibration_batch`, indices et formule pendant le diag, stepper, `BREVET_PACK`, `CHAP_BLOCS`, IIFE scroll-reveal.
  Le HTML `#landing-screen` est réduit à un conteneur `#dx` : c'est l'écran d'entrée de l'app pour un visiteur.
- **E1 `dxIntro`** : « 8 minutes pour savoir ce qui coince vraiment », 15 questions, pas de note.
  - **🧮 Calculatrice autorisée** (contrat §8), adaptatif, liens « Se connecter » et « C'est pour mon enfant » (feuille parent).
  - Reprise < 24 h : « Tu t'étais arrêté à la question n. On reprend ? ». Seuls `{id, token, type, t, n}` vont en localStorage (`mx_dx`), jamais les réponses.
  - Au boot : `_route()` d'abord, sinon auto-login, sinon E1.
- **E2 `dxRenderQ`** (maquette 01) : barre segmentée n/15, « ≈ x min restantes », domaine, chip niveau (si `niveau_origine`), options A-D,
  ou saisie fill (Entrée = valider), « 🤷 Je ne sais pas » en pointillé qui envoie `reponse: null`, encart « Cette question dépend de tes réponses d'avant »,
  brouillon et calculette accessibles.
  - **Pas d'indice, pas de formule, pas de chrono, pas de correction** : c'est le serveur qui corrige.
  - `temps` est envoyé à chaque réponse (fiabilité). En cas d'erreur réseau : 1 retry, puis toast. L'état reste en place, rien n'est perdu.
  - ✕ ouvre une sheet « pause, tu gardes ta progression ». Messages `diag_mid` (question 8) et `diag_jsp_ok` (1 fois).
- **E3** : « On relie tes réponses… » puis « On cherche d'où viennent les erreurs… », au plus la latence + ~1,3 s.
- **E4 `dxCartePartielle`** + **`renderCarte(carte, mode)`** partagé (`partielle` / `complete` / `mini` / `admin`) :
  - hero sombre avec 3 variantes de titre (lacunes, tout vert, tout ⚪) ;
  - alerte fiabilité, 5 domaines (pastille, barre, statut, « estimation express ») ;
  - **point faible n°1** : titre élève, « Notion de 5e », 🔗 cause racine, **sa réponse fausse réelle** (« Tu as répondu X au lieu de Y. Erreur classique : … »),
    « Ça te bloque aussi sur » (titres, ou « + n notions » si la carte masquée n'a pas de titre : Besoin API n°3) ;
  - repli « Ton point le plus fragile » si aucune lacune ;
  - **pas de flou** (50 §2.2 l'emporte sur la maquette 02) : « L'express a mesuré n compétences sur N » → paywall ;
  - boutons « M'entraîner gratuitement → » et « 📩 Envoyer ma carte à mes parents », lien « Revoir mes n réponses » (récap `corrections` :
    réponse, erreur type, bonne réponse, indices).
- **E5 `dxRegister`** (sheet) : prénom, « Email d'un parent (on lui envoie ta carte) », mot de passe, **case 52 §4.2**.
  - Envoie `register {…, diagnostic_id, guest_token}`, puis `login` (pour l'`access_token`) avec les mêmes champs.
  - Si le compte existe avec le bon mot de passe : connexion silencieuse. Si le mot de passe est faux : « Ce mail a déjà un compte. Connecte-toi ».
  - Intentions : `train` (accueil), `share` (feuille de partage), `diag` (repli).
- **Repli sans mode invité (API actuelle)** : `start_diagnostic` sans code répond « Code élève invalide », donc E5 s'ouvre **avant** le diag
  (« Avant de commencer, crée ton espace »), puis le diag démarre avec le code. Dès que le Besoin API n°1 est livré (`guest_token` renvoyé),
  la carte passe **avant** le compte, sans rien changer au front.
- **Login seul** (B12) : fait en L1. Mode nuit : **par défaut clair** désormais (maquettes). La nuit reste disponible via le bouton 🌙 (A12).
- Contrat §8 : **énoncés multi-lignes** → classe `.mx-q-pre` (`white-space:pre-wrap`, aligné à gauche, indentation conservée) dans le diag,
  dans `rSection` et dans `_renderRetroExo`. **Table affichée aussi en vue rétro** (`_tableHTML`).
- `_api()` envoie désormais `access_token` à toutes les actions (Besoin API n°8, sans effet tant que le serveur ne l'exige pas).
- Tests e2e (8790), visiteur neuf :
  - intro → « Lancer » → repli E5 → register + login → **15 questions** (QCM, fill, 4 JSP) → carte partielle (5 domaines, point faible
    « Reconnaître une fonction affine », cause racine, réponse réelle + erreur classique, alerte fiabilité car réponses au hasard) →
    « M'entraîner » → accueil avec la séance servie ;
  - 0 erreur console, `fill_match_node.js` all ok, `_normFill` / `_toNum` / `_matchFill` intacts.
- Points ouverts :
  - la séance après l'express ne compte que **2 exos** (`banque_insuffisante`, banque « train » trop courte sur la zone) : à remonter au concepteur d'items ;
  - le `%` sans conversion (§8a) sera traité côté appelant (`validateAnswer`) en L6, sans toucher à `_matchFill`.

### L6 — Accueil quotidien + séance + fin de séance ✅ (→ 5 517 lignes)

- **Accueil E7 (`renderHome`)** : date + « Salut Léa », puis la **machine à 4 états**.
  - Les 4 états :
    - diag express en cours → « Reprendre » (`get_carte.en_cours`) ;
    - aucun diag → « Lancer mon diagnostic » (`get_training.diagnostic_requis`) ;
    - séance prête / en cours (« Continue, encore n exos ») ;
    - séance faite (« Prochaine séance demain », streak).
  - État D (`zone_maitrisee`, gratuit) : « Ton point faible est réglé 💪 » + « Montrer ma carte à mes parents », sans prix.
  - Erreur réseau → Réessayer. Pas de repli local.
  - Carte « Ta séance du jour » : titre du focus (`boost.focus_titres`, sinon titre de la compétence dans la carte), « n exos · ~x min »,
    **« 💡 Pourquoi ça ? »** (`boost.pourquoi`, sinon phrase déduite de la carte : cause racine + ce qu'elle débloque / erreur type vue / point faible n°1).
  - Mini-carte des 5 domaines → vue « Ma carte » (`renderCarteView`, carte partielle ou complète + partage).
  - En gratuit : rangée « N compétences pas encore mesurées » → paywall.
- `loadTraining()` + `loadCarte()` en parallèle au login. `S.carte`, `S.enCours`, streak et droits viennent du serveur.
- **Erreur type nommée (D2)** : sur une mauvaise réponse, `item.err` est consulté avec une clé normalisée par `_normFill`, comme la saisie
  (contrat §8c). Le libellé vient de `exo.err_libelles` (Besoin API n°2), sinon des erreurs de la carte. Encart **« Erreur classique : … »**
  au-dessus de la correction (`rSection`).
- **« Ce qui a bougé aujourd'hui »** (fin de séance) :
  - photo des statuts au début de la séance, `get_carte` après le flush des scores, puis diff sur les compétences de la séance (chips Lacune → Fragile) ;
  - « Erreur repérée : … Elle reviendra, pour la faire disparaître » ;
  - message honnête s'il n'y a aucun changement.
- Fin de séance : « n sur 5 du premier coup » (P8), streak serveur, `seance_fin_*`. Ensuite, en gratuit « T'as envie de continuer ? → Voir ce qui est inclus »
  (paywall ado), en Programme « Encore une séance » (L9).
- `save_score` porte désormais **`item_id`, `comp`, `type`, `nbOptions`, `reponse`, `err_id`** (8e paramètre `extra` de `sendScore`) : la maîtrise
  par compétence est mise à jour à chaque réponse.
- **Règle `%` (contrat §8a)**, côté appelant : `_matchFillQ(q, val, a, alt)`. Si l'énoncé porte « ___ % », le `%` est retiré des deux côtés et on compare
  sans conversion : 0,25 ≠ 25. Utilisée à la validation et à l'affichage post-réponse. `_matchFill` reste intact.
- PWA (A11) : nudge d'installation proposé en fin de séance si le streak est ≥ 3. Jamais pendant un diagnostic.
- Tests e2e (8790), Tom :
  - accueil : focus « Démontrer avec x… », pourquoi déduit (« Tu es tombé dans … »), mini-carte ;
  - séance : 5 réponses dont 2 sur une clé `err` → encart « Erreur classique » affiché ; script robot/Scratch **multi-lignes conservé** ;
  - fin : « 4 sur 5 du premier coup », bloc « Ce qui a bougé » ;
  - 0 erreur console.
- Points ouverts :
  - le libellé d'erreur est vide tant que l'API n'envoie pas `err_libelles` et que l'erreur n'est pas déjà dans la carte : l'encart affiche alors « Erreur classique. C'est normal… » ;
  - le header affiche encore « Espace de Tom » en plus de « Salut Tom ».

### L7 — Partage parent ✅ (→ 5 576 lignes)

- **`openShare(src)`** (E6, 50 §3.2) : le lien est créé par `create_share {canal}` et réutilisé tant qu'il n'a pas expiré (`S.share`), pour ne pas créer
  un jeton par clic. Si l'élève n'a pas de compte, on passe par E5 avec l'intention `share`.
  - Sheet : « Ils verront / Ils ne verront pas », aperçu « Le bilan maths de Léa (3e) » avec la mini-carte, message pré-rédigé **modifiable**
    et sans prix (« J'ai fait un diagnostic de maths sur Matheux. Voilà ma carte… »).
  - Canaux : `navigator.share` quand il existe, sinon WhatsApp (`wa.me/?text=`), SMS (`sms:&body=` sur iOS, `sms:?&body=` ailleurs),
    Email (`mailto:` pré-rempli avec l'email du compte = parent), Copier le lien.
  - Toast « Envoyé ✓ ». « Désactiver mes liens » → `revoke_share`. `share_opened_app` loggé.
- Points d'entrée :
  - carte partielle (E4) ;
  - E5 avec l'intention partage ;
  - paywall ado (« 📨 Montrer ma carte à mes parents ») ;
  - vue « Ma carte » ;
  - accueil état D (`zone_maitrisee`) ;
  - bandeau « pas encore vue par tes parents » (si l'API renvoie `partages`, Besoin n°14).
- En localhost, `https://matheux.fr/b/<token>` est réécrit vers `location.origin`, pour tester avec la page `bilan.html` servie par le backend de dev.
- Test e2e (8790), Tom : partage → jeton en base (`bilan_partages`) → le lien ouvre la page parent (« Le bilan maths de Tom… Lien personnel,
  valable jusqu'au 25 octobre ») ; 0 erreur console.

### L8 — Diagnostic complet, carte complète, PDF ✅ (→ 5 785 lignes) + intégration des contrats backend livrés

- **Hub E9 (`openDiagHub` / `renderDiagHub`, maquette 07)** : les 3 modules (NC · DF+AP · EG+GM), chacun à l'état *à faire* / *en cours n/N* / *fait ✓*,
  déduit de `get_carte.en_cours[].progression`. Progression globale (questions et minutes restantes), encarts « on vérifie la base d'avant » et
  « calculatrice autorisée, pas de correction pendant le test », « À la fin : carte complète + PDF ». Un seul bouton : « Commencer / Reprendre le module n → ».
  Carte d'accès sur l'accueil tant que le complet n'est pas fini.
- **Modules** :
  - `dxStartType('complet')`, même écran E2 que l'express (titre « Module n / 3 »), `start_diagnostic` reprend à la question près ;
  - `fin_module` → écran « Module n bouclé en m min. Plus que k. », avec « Enchaîner le module suivant » ou « Faire une pause » (retour au hub) ;
  - `paywall` renvoyé par le serveur → paywall ado ;
  - ✕ pendant le complet ramène au hub.
- **Carte complète E10 (`renderCarteComplete`)** :
  - hero : date, `phrase_cle`, 4 compteurs Acquis / Fragiles / Lacunes / Pas vu ;
  - `alerte` fiabilité, bloc « Depuis ta dernière carte » (`evolution`, pour le mensuel) ;
  - **🔗 causes racines** (notion + niveau → ce qu'elle bloque), **priorités 1-2-3** avec l'erreur réelle ;
  - **par domaine** : `<details>` avec barre de segments, 1 segment = 1 compétence ; dans le détail, les compétences avec leur pastille et
    « S'entraîner » en Programme ;
  - **points forts**, **bilan PDF** (Télécharger / Envoyer), **plan 4 semaines**.
  - Upsell E11 **sans prix côté ado** : j'ai écarté le « Activer mon plan — 30 € » de la maquette 04 (contrat §7). À la place : « Pour suivre
    tout le plan, montre ta carte à tes parents », et c'est la vue parent qui propose l'upgrade à 30 €.
  - Confettis **une seule fois** par carte (clé `mx_confetti_<code>_<diag>`).
- **PDF** : `js/bilan-pdf.js` est chargé à la demande, puis `MatheuxBilanPDF.render(carte, {apercu:false})` → téléchargement par `<a download>` et `pdf_open` loggé.
  Le bouton affiche « On prépare ton PDF… », puis « Réessayer » + message de secours en cas d'erreur. Sans droit PDF : paywall.
- **Contrats backend livrés en cours de route**, intégrés :
  - **mode invité** (n°1) : la carte partielle s'affiche **avant** le compte, et `register` / `login` rattachent la session. Le repli « compte d'abord »
    reste en place si le serveur refuse ;
  - **`access_token` exigé** sur les actions élève (n°8) : `_api()` et le batch de scores l'envoient. Sur `auth_requise`, on appelle `refresh_session`
    puis on retente 1 fois ; sinon toast « session expirée » et retour à la connexion ;
  - **`login_token` / `refresh_token`** (n°9) : `boost_v23` = `{email, access_token, refresh_token}`, **plus de hash du mot de passe**. L'ancien format
    est migré au premier login ;
  - `focus_titres` (objets `{id, titre_eleve, …}`) + `pourquoi` (n°4) utilisés, avec repli sur la carte ;
  - `domaine` / `niveau_origine` sur la question (n°11) : chip « Niveau 5e » ;
  - `partages` dans `get_carte` (n°14) : bandeau « pas encore vue ».
- Test e2e complet (8790), visiteur neuf :
  - diag express **invité**, 15 q, 4 JSP → **carte avant compte** ✓ → E5 → compte créé + rattaché → accueil (focus « Reconnaître une fonction affine… », pourquoi serveur) ;
  - paiement simulé `diag_complet` → hub → **3 modules**, dont 2 écrans « fin de module » → carte complète (0/1/26/94, causes racines, alerte fiabilité
    puisque les réponses sont au hasard) ;
  - PDF réel : **16 pages**, polices intégrées ;
  - 0 erreur console.

### L9 — Programme Brevet ✅ (→ 5 848 lignes) + sessions (point bloquant coordinateur)

- **« S'entraîner sur… » (E12)** :
  - `openLibre(comp)` appelle `get_training {comp}`. La série est une clé `LIBREn` dans `LVL.cats`, même moteur `rSection` / `mark` que la séance du jour ;
  - scores envoyés avec **`source: 'LIBRE'`, `categorie: 'LIBRE'`, `exercice_idx = exo.num`** (numéro unique fourni par le serveur, pour la dédup du jour) ;
  - fin de série : « Série finie : n sur 5 », puis « Encore une série » / « Une autre compétence » / « Retour » ;
  - points d'entrée : sélecteur `_choisirLibre` (priorités puis lacunes / fragiles), bouton de l'accueil, « S'entraîner » dans le détail par domaine
    de la carte complète, « Encore une séance » en fin de séance ;
  - sans Programme : paywall.
- **Check-up mensuel (E13)** :
  - bannière sur l'accueil si `get_training.rediagnostic_du`, « Reprendre » si un mensuel est en cours, sinon « Check-up dans n jours » ;
  - `dxStartType('mensuel')` reprend le même écran E2 (titre « Check-up du mois »), avec la même fin que le complet → carte « check-up » et bloc
    **« Depuis ta dernière carte »** (`evolution`).
- Brevet blanc : rangée « Bientôt » (💤 v1.1, Q7).
- **Sessions (message coordinateur, bloquant)** :
  - `boost_v23` = **`{code, email, access_token, refresh_token}`**, sans hash ;
  - boot par `login_token` (l'ancien format avec hash reste accepté une fois, puis migré) ;
  - `auth_requise` → `refresh_session` puis **1 seul** nouvel essai (dans `_api` et dans le batch de scores). En cas d'échec : toast, puis `#login` ;
  - `register` rattache la session invitée, et le `login` qui suit n'essaie plus de la rattacher une 2e fois.
- `carte.non_mesurees` utilisé dans la carte partielle : bloc « Pas encore mesuré », avec les titres lisibles et le chip ⚪, sans flou.
- Header : « Espace de X » masqué côté élève, puisque « Salut X » est déjà sur l'accueil.
- Tests e2e (8790) :
  - **Programme** : visiteur → express invité → compte → 1 exo de séance (`daily_boosts.exos_done` = 1 côté serveur, jeton OK) → paiement simulé
    `programme_brevet` → accueil Programme (S'entraîner sur…, Brevet blanc bientôt, carte diag complet) → série libre (2 scores `LIBRE` en base) →
    diag complet 64 q → `/dev/time?jours=31` → séance du jour du mois suivant → **check-up mensuel** → carte « Check-up · 26 oct. 2026 » ;
  - **Sessions** : login → reload (`login_token`) → jeton corrompu → reload renouvelé → perte du jeton en cours d'usage → `refresh_session` +
    rejeu → success. Stockage : `code, email, access_token, refresh_token` ;
  - 0 erreur console, `fill_match_node.js` all ok.
- Point ouvert : la série libre a servi 2 items au lieu de 5 sur la compétence choisie (banque « train » courte), comme la séance du jour (déjà signalé).

### L10 — Docs ✅ (app.html final : **5 753 lignes**, contre 13 801 au départ)

- En-tête « ⚠️ Refonte Diagnostic 3e » ajouté en tête de `docs/messages.md` (clés `_MSGS` actuelles, invariants H1-H8, règle « aucune incitation
  côté ado », bio fondateur), de `docs/product.md` et des 5 playbooks. Chaque en-tête dit ce qui fait foi et ce qui, plus bas, est obsolète.
  Je n'ai rien réécrit en profondeur.
- `app.html` `<head>` (A1) : **`noindex`**, titre et description neutres, JSON-LD / OG « Brevet 2026 · 29,99 € · parcours vérifié chaque soir »
  retirés. Le SEO revient à la nouvelle landing.
- Admin : la fiche élève appelle `get_carte {code}` avec le jeton admin et **sans** l'email de l'admin (sinon « identité non vérifiée »).
  Une carte express y est étiquetée « express ».
- **CLAUDE.md non modifié** : c'est au chef de projet ou à Nicolas de le faire (40 §5). Les règles à réécrire :
  - P1 : 15 q adaptatives, QCM + fill, corrigées serveur, sans correction affichée ;
  - P2 : séance du jour `get_training` ;
  - P3 : items atomiques ;
  - P5 et P10 : caduques ;
  - P9 : reprise de séance (serveur) ;
  - P12 et G12 / G14 : 💤 ;
  - T1-T4 : gratuit = séance sur la zone du point faible, puis 2 offres via `OFFRE`, paiement depuis la vue parent ;
  - T2 : 3 Payment Links à créer ;
  - M2 / M7 / M8 / G11 : remplacés par H1 / H4 ;
  - G1, G2, G4-G7, G9, G10, G13, G15 : supprimés ; G3 / G8 : gardés, streak serveur ;
  - **G16 : abandonné** ;
  - A2-A5 et A7 : admin en lecture seule ;
  - note « ghost divs z-index » : caduque ;
  - « Pas de données sensibles dans localStorage » : respecté, `boost_v23` = jetons de session.

## Résumé de l'intégration (25/09)

- Lots **L1 à L10 terminés**. `app.html` passe de **13 801 à 5 753 lignes** (−58 %), vanilla, sans dépendance nouvelle.
  `js/bilan-pdf.js` est chargé à la demande.
- Tests :
  - `node supabase/tests/fill_match_node.js` OK à chaque lot (`_normFill` / `_toNum` / `_matchFill` intacts) ;
  - `./matheux.sh test` : **101 OK / 0 KO** + test navigateur OK ;
  - scénarios e2e réels à 375 px sur backend local (express invité → carte avant compte → compte → séance → erreur type → fin de séance →
    partage → page parent → vue parent + cases + paiement simulé → diag complet 3 modules → carte complète → PDF 16 p → Programme libre →
    check-up à J+31 → sessions / refresh → admin) ;
  - 0 erreur console.
- Bug prod corrigé : `save_scores_batch` partait **sans `code`**, donc aucun score de la file n'était enregistré.
- Reste à faire hors front :
  - créer les 3 Payment Links (redirection `app.html?achat=<produit>`) et remplir `OFFRE.*.url` ;
  - banque « train » trop courte : séances de 1-2 exos observées (`banque_insuffisante`) ;
  - Besoin API n°13 (email P-SH) ;
  - brevet blanc (v1.1).
