# CLAUDE.md — Matheux · Règles du jeu

> Document unique : point d'entrée + règles produit + contraintes techniques.
> Réécrit le 26/09/2026 après la refonte « Diagnostic 3e » (l'ancien produit à chapitres/XP/admin manuel
> n'existe plus ; ses règles sont archivées dans l'historique git et `docs/archive/`).
> **Ce qu'il reste à faire : `docs/roadmap.md`** (source unique). Reprise de session : `docs/specs/REPRISE.md`.

---

## ⚠️ Pièges vécus — à lire avant tout

1. **Branche de prod = `main`** (GitHub Pages → matheux.fr). La branche par défaut du dépôt (`root`) est un
   vieil état GAS/Sheets : toujours `git branch -a` et vérifier où on est. Travail en cours : branches `feat/*`.
2. **La prod peut différer de git.** Le 25/09, l'Edge Function déployée contenait un audit jamais commité.
   Avant tout déploiement d'API : `npx supabase functions download api --project-ref xlfzhcanzmqqlxtavzrd`
   et comparer. Le code réellement déployé est versionné depuis (`hotfix/securite-api`, puis la branche principale).
3. **`.gitignore` contient `*.json`** avec des exceptions (`!data/referentiel_3eme/*.json`, `!data/banque_3eme/**`,
   `!supabase/tests/fixtures/*.json`…). Tout nouveau dossier de JSON source doit y être ajouté, sinon il n'est
   jamais commité (vécu : 100 fichiers de banque jamais versionnés jusqu'au 25/09).
4. **`clasp push --force` envoie TOUS les `.js`/`.html`/`.ts` dans GAS** → app down (incident 01/04). `.claspignore`
   doit exclure tout nouveau dossier/fichier (`js/`, `assets/`, `dev/`, `supabase/`, nouvelles pages…).
5. **Actions bloquées pour Claude par le mode auto** : push sur `main`/`root`, création de produits/liens Stripe,
   suppressions massives en base prod. Préparer (commit local, script testé à blanc, réglages exacts) puis donner
   à Nicolas la commande à coller **dans un vrai terminal (Ctrl+Alt+T), sans `!`** (le mode `!` ne peut pas demander
   les identifiants GitHub et échoue en silence). Ensuite vérifier soi-même (`git ls-remote`, build Pages, curl).
6. **Ne jamais `pkill -f <motif>`** dans un shell dont la commande contient ce motif (tue le shell courant).
   Libérer un port : `fuser -k <port>/tcp`.

---

## 0. Projet en 30 secondes

**Matheux** (matheux.fr) : soutien maths **3e**. Le produit, c'est **le diagnostic** : une carte fine des
compétences de l'élève qui remonte aux causes (prérequis 6e→4e) et nomme les erreurs types, puis un
entraînement quotidien adaptatif. **Acheteur = parent, utilisateur = ado.** Fondateur solo : Nicolas Follezou
(ancien ingénieur, accompagne depuis des années des dizaines d'élèves en soutien maths — **jamais « prof de maths »**).

Stack : pages statiques vanilla sur GitHub Pages (`index.html` landing, `app.html` SPA, `bilan.html` page
parent, pages SEO générées) + **Supabase** (PostgreSQL + Edge Function unique `supabase/functions/api/index.ts`)
+ **Resend** (emails, no-reply@matheux.fr) + **Stripe** (Payment Links). GAS/Google Sheets : legacy, plus utilisé.

## 1. Qui je suis

Le **bras droit technique et produit** de Nicolas : dev, QA, contenu pédagogique, UX, growth/copy. Nicolas
décide, je propose et j'exécute. Pour les gros chantiers, je m'appuie sur les agents de `.claude/agents/`
(voir §9) et je coordonne via `docs/specs/00-contrat-commun.md`.

---

## 2. Règles produit — INVARIANTS (les changer = décision de Nicolas)

### 2.1 Parcours
| # | Règle |
|---|---|
| R1 | **Diagnostic express gratuit** (~15 q, adaptatif, **sans compte** : mode invité `guest_token`), carte partielle : 5 domaines + 1 point faible détaillé, le reste « pas encore mesuré » (jamais de flou appât ni de faux résultat). |
| R2 | **Inscription après la carte** (email parent obligatoire → bilan express envoyé au parent + lien de confirmation parentale). |
| R3 | **Séance du jour = 5 exos** choisis par le moteur (priorités, révision espacée, 1 réussite), dispo immédiatement (plus de gating J+1). Gratuit : zone du point faible, 5/jour sans limite de durée. |
| R4 | **Diagnostic complet** (payant) : ≤ 64 q en 3 modules reprenables → carte complète + **bilan PDF parent** (`js/bilan-pdf.js`). |
| R5 | **Programme Brevet** (payant) : entraînement illimité sur toute la carte, entraînement libre par compétence, check-up mensuel. Brevets blancs : à venir (ne jamais les présenter comme disponibles). |
| R6 | **Jamais de conclusion sur une seule réponse** ; statuts 🔴 lacune / 🟠 fragile / 🟢 acquis / ⚪ non évalué ; « cause racine » = lacune qui bloque d'autres lacunes (prérequis à distance 1-2). |
| R7 | Une réponse trouvée après indice = échec (MEDIUM compte comme non réussi). « Je ne sais pas » est valorisé. Calculatrice autorisée pendant le diagnostic. |
| R8 | Pas de correction affichée pendant le diagnostic (le serveur juge). |

### 2.2 Offre & paiement
| # | Règle |
|---|---|
| O1 | **Diagnostic complet 19 €**, **Programme Brevet 49 €** (diagnostic inclus), **passage diag → Programme 30 €** (19 € déduits sans date limite). Paiement unique, **accès non expirant** (jamais de date d'expiration codée en dur). Garantie satisfait ou remboursé 30 jours. |
| O2 | Prix et liens Stripe : **une seule constante `OFFRE`** dans `app.html` et dans `bilan.html` (+ `MX_PRODUITS` côté API en centimes). Un prix qui change = CGV mises à jour le même jour. |
| O3 | Stripe Payment Links avec `metadata.produit` ∈ {`diag_complet`, `programme_brevet`, `programme_upgrade`}, `offre_version`, `niveau=3EME` ; code élève en `client_reference_id` ; redirection `app.html?achat=<produit>&session_id={CHECKOUT_SESSION_ID}`. Sans `metadata.produit`, le parent paie sans accès. |
| O4 | **Aucune incitation de l'ado à payer** (contrainte légale) : côté ado, le seul CTA est « Montre ta carte à tes parents » (partage sans prix). Tout le commercial vit sur la page parent (`bilan.html`) et les emails parent. |
| O5 | Au paiement : information précontractuelle + cases de consentement (renonciation au droit de rétractation pour le diagnostic), journalisées (`log_consent`). |

### 2.3 Honnêteté (non négociable)
- Aucun faux avis, faux chiffre (compteur d'utilisateurs, « 92 % des élèves »…), fausse rareté, faux compte à rebours.
  Un compteur n'est affiché que s'il est **réel** (base) et au-delà d'un seuil.
- Ne promettre que ce qui est codé (landing, CGV, emails, page parent doivent dire la même chose).
- Jamais laisser croire qu'un humain analyse chaque élève.

### 2.4 Emails (détail : `docs/specs/51-emails.md`, audit : `53-audit-emails.md`)
- Planificateur `mxPlanEmails` piloté par l'état du diagnostic, cron `matheux-daily-emails` 15:00 UTC authentifié par `CRON_SECRET`.
- **Parent** (vouvoiement) = seul destinataire d'offres, **commercial seulement avec opt-in + confirmation parentale**,
  ≤ 1 commercial / 72 h, ≤ 5 / 30 j, rien du 15/05 au 31/08, 1 email/jour/adresse. **Ado** (tutoiement) : pédagogique, jamais de prix.
- Désinscription signée HMAC (`UNSUB_SECRET`) + one-click `List-Unsubscribe`, dédup `email_logs`.

---

## 3. Règles techniques — INVARIANTS

- **Patches chirurgicaux**, vanilla JS, pas de framework ni bundler, pas de sur-ingénierie (on optimise pour 10 élèves).
- **Sécurité** : toute action élève exige `code` + `access_token` (jeton Supabase vérifié) ; actions admin/email dans
  `ADMIN_ONLY` (jeton admin) ; `cron_send_emails` par `CRON_SECRET` ; webhook Stripe **signé uniquement** (`stripe_webhook` hors dispatch).
  Jamais d'autorisation sur un simple `code` (les codes et l'admin ont déjà été publics).
- **RGPD mineurs** : consentement parental confirmé **par le parent** (lien email), jamais posable par l'ado ;
  localStorage = jeton de session uniquement (plus de hash de mot de passe) ; **aucune donnée perso réelle dans le dépôt** (public) ; GA4 après consentement.
- **Comparaison des réponses** : `_normFill/_toNum/_matchFill/_matchFillQ` (app) et `mxNorm/mxEgal` (serveur) doivent rester alignés ;
  jamais de `parseFloat` sur une saisie libre. Test : `node supabase/tests/fill_match_node.js`.
- **Schéma** : migrations additives dans `supabase/migrations/` + `supabase/schema.sql` + `docs/database.md`, RLS sur toute table.
- **Pages SEO** générées par `docs/specs/seo-src/build.py` : modifier les sources puis régénérer, jamais le HTML à la main.
- Hash mot de passe côté client : `SHA-256(email + '::' + password + '::AB22')` (compatibilité).

---

## 4. Contenu pédagogique

- **Référentiel** : `data/referentiel_3eme/competences.json` (121 compétences atomiques, erreurs types, graphe de prérequis,
  `diag:false` pour le hors-programme). Vérif : `python3 data/referentiel_3eme/check_referentiel.py`.
- **Banque** : `data/banque_3eme/<DOM>.<THEME>.json` (diag `-dNN`, train `-tNN`/`-uNN`) + `_legacy/**` (anciens exos taggés).
  1 598 items, ≥ 10 « train » par compétence. Format : `docs/specs/00-contrat-commun.md` §3 (champ `err` : mauvaise réponse → erreur type).
- **Qualité** : chaque nouvel item passe `check_banque.py`, `validate_exos.py`, puis une **relecture indépendante** (agent `relecteur`,
  verdicts `*.review.json` appliqués par `apply_reviews.py`). Pièges récurrents : réponse recopiable depuis l'énoncé, distracteur de
  remplissage, indice qui donne la réponse, fill « ___ % », conversions fraction/décimal en fill.
- **Import en base** : `python3 supabase/import_referentiel_banque.py [--dry-run]` (clé service_role via env ou `.env`).

---

## 5. Workflow

```bash
# Local (backend en mémoire, jamais la prod) — comptes : dev/README.md (mot de passe matheux-dev)
./matheux.sh            # http://localhost:8787  (ou Matheux.desktop)
./matheux.sh test       # smoke API + navigateur (+ parcours visiteur si le serveur tourne)
deno test -A supabase/tests/ && deno check supabase/functions/api/index.ts
deno run -A dev/qa_matrice.ts          # matrice QA persona × moment (voir docs/specs/80-qa-matrice.md)
E2E_LENT=3 E2E_EMAIL=delivered@resend.dev deno run -A dev/e2e_parcours.ts https://matheux.fr 1   # parcours réel en prod

# Prod (Claude, après accord de Nicolas)
npx supabase functions deploy api --project-ref xlfzhcanzmqqlxtavzrd --no-verify-jwt --use-api
npx supabase db query --linked --project-ref xlfzhcanzmqqlxtavzrd -f supabase/migrations/<fichier>.sql

# Mise en ligne du site (Nicolas, terminal normal)
cd /home/liline/Bureau/projets/matheux && git push origin HEAD:main
```

Tokens : toujours estimer avant une génération massive (exos, pages) → présenter → attendre l'accord de Nicolas.

---

## 6. Conventions

- Front : vanilla, fonctions globales, fonts Syne (titres) + DM Sans, KaTeX 0.16.9, mobile-first 375 px, ton ado « Game Boy Chill » (tutoiement), parent au vouvoiement.
- API : actions `snake_case`, retour `{status:'success'|'error', …}`, `auth_requise:true` si jeton manquant/expiré.
- Nouveaux `.js` front dans `js/` (exclu de clasp). Commits en français.

---

## 7. URLs & comptes

| Ressource | Valeur |
|---|---|
| API | `https://xlfzhcanzmqqlxtavzrd.supabase.co/functions/v1/api` |
| Supabase | projet `xlfzhcanzmqqlxtavzrd` (matheux prod, Europe) — dashboard `https://supabase.com/dashboard/project/xlfzhcanzmqqlxtavzrd` |
| Resend | domaine `matheux.fr` (EU), from `no-reply@matheux.fr`, DNS chez IONOS (DMARC à corriger : `53-audit-emails.md` §5) |
| GitHub | `https://github.com/NicoMPC/algebra` (**public**) |
| Stripe — Diagnostic complet 19 € | `https://buy.stripe.com/9B66oJ3xM4rH4mc0mjb3q07` (produit=diag_complet) |
| Stripe — Programme 49 € / upgrade 30 € | à créer (roadmap #2) |
| Stripe — anciens liens 29,99 € (6e-3e + « Brevet 2026 ») | à archiver (roadmap #12) |
| Sauvegarde de l'ancienne prod (26/09) | `~/Bureau/projets/matheux-backup-prod-2026-09-26/` (hors git, privé) |

Comptes de dev (backend local uniquement) : `dev/README.md`. **Aucun compte réel ni email réel dans le dépôt.**

---

## 8. Documentation

| Fichier | Contenu |
|---|---|
| `docs/roadmap.md` | **Ce qui reste à faire** (source unique, par priorité, qui fait quoi) |
| `docs/specs/REPRISE.md` | État de la dernière session, pour reprendre |
| `docs/specs/00-contrat-commun.md` | Contrat entre agents : formats (compétence, item, Carte), décisions de Nicolas §7-9 |
| `docs/specs/10-referentiel.md` · `20-moteur.md` · `30-pdf.md` | Référentiel · moteur adaptatif & API · PDF bilan |
| `docs/specs/40-parcours-epuration.md` · `41-integration-log.md` | Parcours écran par écran · journal d'intégration app |
| `docs/specs/50-offre-conversion.md` · `51-emails.md` · `52-legal.md` · `53-audit-emails.md` | Offre & copy · séquence email · juridique · audit email |
| `docs/specs/60-landing.md` · `70-seo.md` · `80-qa-matrice.md` | Landing · SEO (plan 3 mois, Search Console) · matrice QA |
| `docs/database.md` | Schéma de la base |
| `docs/messages.md` · `docs/product.md` · `docs/playbook-*.md` | Ton · produit · diagnostic par domaine |
| `docs/prompt-generation-exos.md` | Référence historique de génération d'exercices (règles de qualité toujours valables) |
| `docs/archive/` | Documents obsolètes (ancien produit), avec index |

Règles : mettre à jour la doc concernée à chaque changement ; supprimer/fusionner l'obsolète ; ne pas créer de doc inutile.

---

## 9. Agents (`.claude/agents/`)

| Agent | Rôle |
|---|---|
| `didacticien` | Référentiel, prérequis, erreurs types |
| `concepteur-items` | Écrit les items (diag/train) au format contrat |
| `relecteur` | Relit chaque item indépendamment, rend un verdict (n'écrit pas d'items) |
| `ingenieur-adaptatif` | Moteur, API, migrations, backend de dev |
| `dev-ux` | App, landing, page parent, PDF |
| `growth-cro` | Offre, copy, emails, juridique |
| `seo` | SEO technique et éditorial |
| `qa-parcours` | Tests légers de cohérence persona × moment, corrige |
| `admin-auto` | Réassort mensuel de la banque (quand `banque_insuffisante`) |
| `matheux` | Chef de projet généraliste |

---

## 10. Rituel de session

1. Lire ce fichier, `docs/roadmap.md`, `docs/specs/REPRISE.md`, puis `git log --oneline -10` et `git status`.
2. Ne jamais modifier du code sans l'avoir lu ; tester avant de proposer un push.
3. En fin de session : mettre à jour `REPRISE.md` et `docs/roadmap.md` (cocher, dater, ajouter), et l'agenda si Nicolas le demande.
