# Point de reprise — Refonte « Diagnostic 3e »

> Mis à jour le 24/09/2026 ~22h. À lire EN PREMIER à la reprise, avec
> `docs/specs/00-contrat-commun.md` (contrat + toutes les décisions de Nicolas §7-9).
> Branche : `feat/diagnostic-3e` (locale, jamais pushée). Rien n'est en prod.

## Fait et commité (checkpoints locaux `75dd44f`, `cf9d27a`)

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

## En cours au moment de la coupure (agents en arrière-plan, NON commité)

| Chantier | Fichiers | Comment reprendre |
|---|---|---|
| Backend local en mémoire + launcher `matheux.sh` / `Matheux.desktop` | `dev/`, `matheux.sh`, `Matheux.desktop` | Regarder ce qui existe dans `dev/` (+ `dev/README.md`), relancer un agent `ingenieur-adaptatif` avec la même mission (faux PostgREST+GoTrue, index.ts non modifié, seed, `/dev/pay`, outbox emails, smoke test) |
| Intégration du nouveau parcours dans `app.html` (10 lots) | `app.html`, journal `docs/specs/41-integration-log.md` | Lire le journal → reprendre au lot suivant avec un agent `dev-ux`. Vérifier d'abord `git diff --stat app.html` et que l'app charge sans erreur console |
| Page parent `bilan.html` + bascule landing (index.html, 404, SEO, premium, sitemap) | `bilan.html`, `b/`, `index.html`, `404.html`, `_next/` supprimé, pages SEO | `git status` pour voir où en est la bascule ; relancer un agent `dev-ux` |

⚠️ À la reprise : `git status` + `git diff --stat` avant tout, les agents ont pu
s'arrêter au milieu d'un fichier. Au besoin `git stash` pour repartir de `cf9d27a`.

## Ensuite

1. Test de bout en bout du site complet en local (launcher) → donner la main à Nicolas
2. Commit local de la phase « build »
3. **Créneau agenda 25/09 9h-12h** (« Matheux — gros chantiers ») :
   - complément banque ~300 exos (15/compétence sur 30 causes racines), ~0,8 M tokens
   - ⚠️ **3 failles prod sur `main`** : `stripe_webhook` sans signature (premium gratuit),
     `reset_password` sans jeton (prise de contrôle de n'importe quel compte),
     `get_admin_overview` avec le seul code admin (public dans le repo → emails de tous les élèves).
     → hotfix sur `main` (porter les 3 correctifs de la branche) + deploy Edge Function
     (`npx supabase login` requis). Le front prod utilise le reset par code 8 caractères (cassé de toute façon).
   - `sw.js` : cache-first sur les pages HTML + `/scree.png` inexistant → monter la version, network-first pour les navigations, avant bascule landing
   - déploiement Supabase (migration, import, purge avec backup), liens Stripe mode test
4. Mise à jour CLAUDE.md (beaucoup de règles P/G/M/T/A obsolètes — liste dans spec 40), merge `main` sur décision explicite de Nicolas
