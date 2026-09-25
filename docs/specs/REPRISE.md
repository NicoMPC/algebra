# Point de reprise — Refonte « Diagnostic 3e »

> Mis à jour le 24/09/2026 ~22h. À lire EN PREMIER à la reprise, avec
> `docs/specs/00-contrat-commun.md` (contrat + toutes les décisions de Nicolas §7-9).
> Branche : `feat/diagnostic-3e` (locale, jamais pushée). Rien n'est en prod.

## Fait et commité (checkpoints locaux `75dd44f`, `cf9d27a`, `38545ee`)

- Référentiel 3e : 121 compétences, ~300 erreurs types, graphe de prérequis
  (`data/referentiel_3eme/`, `check_referentiel.py` ✅)
- Banque : 363 items diag neufs **relus et corrigés** (3 relecteurs) + 779 items
  d'entraînement legacy taggés (`data/banque_3eme/`, `check_banque.py` ✅,
  `_legacy/check_legacy.py` ✅, `apply_reviews.py`)
- Moteur adaptatif : spec `20-moteur.md`, migration `supabase/migrations/20260924_diagnostic_3e.sql`,
  11 actions dans `index.ts`, tests `deno test -A supabase/tests/` 8/8 ✅,
  `supabase/import_referentiel_banque.py` (dry-run), `supabase/purge_anciens_comptes.sql` (ROLLBACK)
- PDF bilan parent : `js/bilan-pdf.js`, exemples `docs/specs/exemples-pdf/`
- Landing vanilla : `landing/index.html` (testée : liens OK, parcours → diag OK)
- Specs : parcours/épuration (40), offre (50), emails (51), légal (52), landing (60)
- Fixes : `_toNum`/`_normFill` stricts (test `node supabase/tests/fill_match_node.js`),
  action `stripe_webhook` retirée du dispatch sur la branche

## Fait depuis (24/09 soir)

- Backend local en mémoire + launcher : `./matheux.sh` (http://localhost:8787), `Matheux.desktop`, `dev/README.md` (comptes, mot de passe `matheux-dev`, `/dev/outbox`, `/dev/pay`, `/dev/time`). `./matheux.sh test` → smoke 45/45 + test navigateur.
- Page parent `bilan.html` + bascule landing (index.html vanilla, `_next/` supprimé, 404 vanilla, SEO, premium, sitemap) — 37/37 tests.
- 3 bugs prod corrigés dans index.ts (login client admin pollué par la session élève, upsert `scores` qui n'écrivait rien, colonne `progress.nb_easy` manquante → migration).
- Failles corrigées sur la branche : `reset_password` sans jeton (prise de contrôle de compte par email), actions admin protégées par le seul `code` (code admin public dans le repo → fuite de tous les profils), `stripe_webhook`. Tests d'attaque dans `dev/smoke_test.ts`.

## Fait 25/09 (backend)

- Besoins API 1-12 + 14 livrés (diag invité, err_libelles, séance « pourquoi », entraînement libre, email parent P-X0 + `confirm_parent`, jetons `access_token`/`refresh_token` obligatoires sur TOUTES les actions élève, `login_token`, `refresh_session`, monitoring admin). Correctifs de l'audit prod 11/04 portés. Smoke 101/101, `deno test` 11/11, `deno check` 0 erreur. Contrats : `41-integration-log.md` § Besoins API.
- Au déploiement : migrations `20260925_*.sql` ; secret `CRON_SECRET` (+ même valeur dans Vault `matheux_cron_secret`) sinon plus aucun email auto ; remplacer les anciens mails J+1..J+14 (29,99 €) ; `bilan.html` doit gérer `?confirmer=1` → `confirm_parent` ; besoin 13 (envoi du lien de partage par email, plafonné 3/jour) pas fait.

## Fait 25/09 (app) — commit `c45c076`

- Nouveau parcours intégré dans `app.html` (L1-L10, 13 801 → 5 753 lignes). Journal : `41-integration-log.md`.
- Vérifié par e2e visiteur réel (landing → diag invité 15 q → carte partielle → inscription → séance → fin de séance) :
  0 erreur console, jeton en localStorage (plus de hash), email parent dans l'outbox.
- ⚠️ Constat : la séance du jour ne sert que 1-2 exos (banque d'entraînement trop mince) → complément banque = priorité.

## En cours (25/09 soir) — 2e complément banque

- Objectif : ≥ 10 items « train » pour chacune des 118 compétences diagnosticables (sinon la séance ne sert
  que 2 exos quand le point faible tombe hors des 30 compétences du 1er complément — constaté en e2e 2 fois sur 3).
- 229 items (ids `-uNN`) : cibles `data/banque_3eme/cibles_complement2.json`, suivi `COMPLEMENT2_NC_DF.md`
  et `COMPLEMENT2_GM_EG_AP.md`. Ensuite : relecture (`*.train-review.json` → `apply_reviews.py --train`),
  puis e2e du parcours visiteur ×3 (la séance doit servir 5 exos).

## ⏭️ Reste à faire (décidé par Nicolas le 25/09 — créneau agenda sam. 26/09 9h-12h)

1. **Complément banque d'entraînement** (~300 exos, 15/compétence sur les 30 causes racines, relecture
   indépendante, ~0,8 M tokens) — reporté faute de tokens. Aujourd'hui la séance ne sert que 1-2 exos.
2. **Mise en ligne** :
   - Stripe : ✅ lien 19 € créé le 25/09 (`https://buy.stripe.com/9B66oJ3xM4rH4mc0mjb3q07`, plink_1UJcp8PwkMLpimxM2ayjh2tU,
     metadata produit=diag_complet / offre_version=2026-09 / niveau=3EME, taxes auto OFF, TTC, redirection
     `https://matheux.fr/app.html?achat=diag_complet&session_id={CHECKOUT_SESSION_ID}`), branché dans `OFFRE` (app.html + bilan.html).
     ⏳ Liens 49 € (`programme_brevet`) et 30 € (`programme_upgrade`) : création bloquée pour Claude (classée transaction réelle) → Nicolas, mêmes réglages.
     ⚠️ Vérifier que le webhook Stripe de prod pointe bien vers l'Edge Function et que `metadata` du lien est bien recopiée dans la session (1er paiement test).
   - `CRON_SECRET` (secrets Supabase + Vault `matheux_cron_secret`)
   - ✅ anciens emails J+1..J+14 (29,99 €) remplacés (25/09) par la séquence `51-emails.md` : planificateur pur
     `mxPlanEmails` (tests `supabase/tests/emails_test.ts`, 300 élèves fictifs) + cron piloté par l'état (P-X0N/R1/R2
     confirmation, P-X1/P-X2/P-X3 commercial avec opt-in, P-X2b usage, A-X0/A-X1 ado, A-MOD/P-MOD, P-UP1/P-UP2,
     P-HEBDO, A-MENS) + emails d'événement P-ACH1/P-ACH2 (confirmation légale au payeur), P-PDF/A-PDF. Plafonds :
     1 commercial/72 h, 5/30 j, conversion ≤ J+30, rien du 15/05 au 31/08, 1 email/jour/adresse, rien le week-end
     (sauf hebdo dimanche, A-MENS samedi). Désinscription signée (HMAC `k`), one-click `List-Unsubscribe`,
     `unsubscribe.html` rebranché sur l'API Supabase (appelait encore GAS). Cron déplacé à 15:00 UTC (17h Paris).
     Non faits (à décider) : saisonniers S-DEC/S-BB/S-AVR (date du Brevet 2027 à fixer), re-test A-RT/P-UP3
     (le re-test n'existe pas pour les acheteurs du seul diagnostic), suppression du compte à J+30 sans confirmation.
     ⚠️ Optionnel : secret `UNSUB_SECRET` (sinon la clé service_role sert de clé HMAC ; la changer invalide les liens).
   - migrations 20260924 + 20260925, import référentiel/banque, purge anciens comptes (backup)
   - ✅ `sw.js` v14 (25/09) : HTML en réseau d'abord, plus de `/scree.png`, anciens caches supprimés ; install testée en Chrome headless (`dev/browser_test.ts`)
   - merge `feat/diagnostic-3e` → `main` sur décision explicite
3. **RGPD dépôt public** : push des commits de retrait des données perso sur `main` et `root` — **bloqué
   pour Claude** (classé déploiement prod), à faire par Nicolas. ✅ Branche locale propre (25/09) : `git grep`
   ne trouve plus aucun email/code réel ; admin de dev = `admin@dev.matheux.local` / `ADMDEV` ; la purge épargne
   `is_admin = true` sans code en dur.
4. ✅ Besoin API n°13 : `send_share_email {code, access_token, to?}` (P-SH, 3 envois/24 h/élève, 1 par adresse/24 h,
   désinscription respectée) — **reste à brancher dans app.html** (aujourd'hui `mailto:`, ligne ~3118).
   ✅ `bilan.html?confirmer=1` : rien n'est écrit à l'ouverture (antivirus de messagerie), le parent clique,
   case d'opt-in non cochée, états déjà confirmé / lien invalide / réseau. `confirm_parent {apercu:true}` en lecture seule.

## Ensuite

1. **Complément banque d'entraînement** (~300 exos, 15/compétence sur les causes racines) — bloquant pour l'expérience
2. Nicolas teste en local (`./matheux.sh`) et valide
3. **Créneau agenda 25/09 9h-12h** (« Matheux — gros chantiers ») :
   - complément banque ~300 exos (15/compétence sur 30 causes racines), ~0,8 M tokens
   - ✅ **Sécurité prod déployée le 25/09 ~12h** (branche locale `hotfix/securite-api`, commits `b4bcfb6` snapshot de
     la prod réellement déployée — audit 11/04 jamais commité sur GitHub — puis `4fc6123` garde `ADMIN_ONLY` : 12 actions
     admin/email exigent un jeton de session admin). Vérifié en prod. Conséquence : le panneau admin de l'ancienne app
     ne marche plus (il n'envoie que le code). Diff audit 11/04 à porter sur la branche : `docs/specs/audit-0411-prod.diff`.
     Branche hotfix pas encore pushée sur GitHub (à décider).
   - `sw.js` : cache-first sur les pages HTML + `/scree.png` inexistant → monter la version, network-first pour les navigations, avant bascule landing
   - déploiement Supabase (migration, import, purge avec backup), liens Stripe mode test
4. Mise à jour CLAUDE.md (beaucoup de règles P/G/M/T/A obsolètes — liste dans spec 40), merge `main` sur décision explicite de Nicolas
