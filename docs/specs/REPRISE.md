# Point de reprise — Refonte « Diagnostic 3e »

> Mis à jour le 26/09/2026 14h. À lire EN PREMIER à la reprise, avec `docs/specs/00-contrat-commun.md`
> (contrat + décisions de Nicolas §7-9). Branche : `feat/diagnostic-3e` (locale, jamais pushée).
> Relancer la conversation : « Matheux — Conversation Claude.desktop ». Tester en local : `./matheux.sh`.

## État en une phrase

Le nouveau site (landing, diagnostic, carte, séance adaptative, page parent, PDF, paiement, emails) est
**construit et testé en local** ; la prod (matheux.fr) sert toujours l'ancien site, avec l'API sécurisée.

## ✅ Fait

- **Référentiel 3e** : 121 compétences, ~300 erreurs types, graphe de prérequis (`data/referentiel_3eme/`).
- **Banque** (`data/banque_3eme/`, `check_banque.py` ✅) : 363 items diag (relus) + 779 legacy taggés + 227 items
  train 1er complément (`-tNN`, relus) + 229 items train 2e complément (`-uNN`, relus : 222 ok, 7 corrigés).
  Toutes les compétences diagnosticables ont ≥ 10 items d'entraînement.
  ⚠️ `.gitignore` masquait `*.json` : corrigé le 25/09, la banque est enfin versionnée.
- **Moteur adaptatif + API** (`supabase/functions/api/index.ts`) : diag express invité / complet / mensuel, carte,
  séance du jour « Pourquoi ça ? », entraînement libre, partage parent (lien + email), consentements, jetons de
  session obligatoires, emails pilotés par le diagnostic (`mxPlanEmails`). Migrations `20260924_*`, `20260925_*`.
- **App** (`app.html` 13 801 → ~5 750 lignes), **landing** vanilla (`index.html`), **page parent** `bilan.html`,
  **PDF** `js/bilan-pdf.js`, `sw.js` v14, 404 vanilla, pages SEO recâblées.
- **Tests** : `./matheux.sh test` (smoke 126/126 + navigateur), `deno test -A supabase/tests/` 21/21,
  `node supabase/tests/fill_match_node.js`. E2E visiteur : `deno run -A dev/e2e_parcours.ts <BASE> <N>`
  (aussi lancé par `./matheux.sh test` si le serveur tourne) — 5/5 parcours OK le 26/09 : **5 exos par séance**.
  Backend isolé : `DEV_DATA_DIR=… deno run … dev/server.ts serve --port 8797` ; libérer le port avec
  `fuser -k 8797/tcp`, jamais `pkill -f` (tue le shell courant).
- **Prod** : sécurité API déployée le 25/09 (branche `hotfix/securite-api` poussée : snapshot de la prod
  réellement déployée — audit 11/04 jamais commité — + garde `ADMIN_ONLY`). RGPD : données perso retirées de
  `main`/`root` et de matheux.fr/CLAUDE.md (restent dans l'historique git).
- **Stripe** : lien 19 € créé (`https://buy.stripe.com/9B66oJ3xM4rH4mc0mjb3q07`, metadata produit=diag_complet,
  offre_version=2026-09, niveau=3EME, taxes auto OFF, redirection `app.html?achat=diag_complet&session_id=…`),
  branché dans `OFFRE` (app.html + bilan.html).

## 🚀 Bascule du 26/09 (Nicolas : « push immédiat, l'ancien site et l'ancienne base osef »)

- ✅ Sauvegarde complète de la prod (16 tables + auth.users) : `~/Bureau/projets/matheux-backup-prod-2026-09-26/` (hors git, privé).
- ✅ Migrations appliquées en prod : `20260924_diagnostic_3e`, `20260924_progress_nb_easy`, `20260925_invites_securite`, `20260925_cron_secret`.
- ✅ Secrets `CRON_SECRET` + `UNSUB_SECRET` créés (+ Vault `matheux_cron_secret`) ; cron `matheux-daily-emails` actif 15:00 UTC.
- ✅ Import prod : 121 compétences, 1 598 items (354 diag).
- ✅ Nouvelle API déployée et vérifiée (diag invité OK, actions protégées refusées sans jeton).
- ⛔ Bloqué pour Claude → Nicolas : push `feat/diagnostic-3e` → `main` (mise en ligne du site) ; purge des anciens
  comptes (script prêt : `~/Bureau/projets/matheux-backup-prod-2026-09-26/purge_anciens_comptes_COMMIT.sql`,
  testé à blanc : il reste 1 admin, 0 score). ⚠️ Tant que `main` n'est pas poussé, l'ANCIEN site en ligne parle à la
  NOUVELLE API et ne fonctionne plus (jetons exigés).

## ⏭️ Reste à faire, par priorité

1. ✅ Banque complète et relue ; e2e 5/5 (5 exos par séance). Unités composées (`m/s`, `km/h`) acceptées.
2. **Nicolas** — Stripe : créer les liens 49 € (`programme_brevet`) et 30 € (`programme_upgrade`), mêmes réglages
   que le 19 € (ponctuel, TTC = Oui, taxes auto décochées, metadata produit/offre_version=2026-09/niveau=3EME,
   redirection `https://matheux.fr/app.html?achat=<produit>&session_id={CHECKOUT_SESSION_ID}`). Création bloquée
   pour Claude (classée transaction réelle). Donner les URL à Claude → `OFFRE.prog.url` / `OFFRE.upgrade.url`
   (app.html) et `OFFRE.programme.lien` / `OFFRE.upgrade.lien` (bilan.html).
3. **Nicolas** — secrets Supabase : `CRON_SECRET` (+ même valeur dans Vault `matheux_cron_secret`), option
   `UNSUB_SECRET`. Sans `CRON_SECRET`, aucun email automatique ne part.
4. **Ensemble** — déploiement base (`npx supabase login`) : sauvegarde complète → migrations `20260924_diagnostic_3e`,
   `20260924_progress_nb_easy`, `20260925_invites_securite`, `20260925_cron_secret` → import référentiel + banque
   (`supabase/import_referentiel_banque.py`, `.env` requis) → purge anciens comptes (`supabase/purge_anciens_comptes.sql`,
   admins épargnés, retirer le ROLLBACK final) → déploiement de l'Edge Function de la branche.
   ⚠️ Vérifier que le webhook Stripe de prod pointe vers l'Edge Function et que la metadata du lien arrive dans la session.
5. **Ensemble** — test réel : 1 inscription + 1 paiement 19 € (remboursable) → accès débloqué + email parent reçu.
6. **Nicolas** — mise en ligne : merge `feat/diagnostic-3e` → `main` (le push sur main est bloqué pour Claude,
   classé déploiement prod) puis vérification du site.
7. Après mise en ligne : archiver les 5 anciens liens Stripe à 29,99 € ; réécrire les règles obsolètes de
   `CLAUDE.md` (liste à la fin de `41-integration-log.md`).
8. Décisions non bloquantes : date officielle du Brevet 2027 (emails saisonniers) · re-test pour les acheteurs du
   seul diagnostic · suppression du compte à J+30 sans confirmation parentale · `brevet-2026.html` · photo
   fondateur · relecture CGV par un juriste · 2 erreurs types NC.LIT.01 proposées par le relecteur.
