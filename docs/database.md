# Base de données — Matheux

> Depuis le 02/04/2026, la base de données principale est **Supabase PostgreSQL**.
> Google Sheets est conservé en backup/référence historique (plus écrit en prod).
> Voir aussi [architecture.md](architecture.md) pour les flux, [claude.md](claude.md) pour les règles, [product.md](product.md) pour le produit.

---

## Informations de connexion

### Supabase PostgreSQL (PROD — principal)

| Ressource | Valeur |
|---|---|
| **Project** | `matheux-prod` (West EU Paris) |
| **Project ref** | `xlfzhcanzmqqlxtavzrd` |
| **API URL** | `https://xlfzhcanzmqqlxtavzrd.supabase.co/functions/v1/api` |
| **Dashboard** | `https://supabase.com/dashboard/project/xlfzhcanzmqqlxtavzrd` |
| **Schema** | `supabase/schema.sql` (14 tables + RLS) |
| **Auth** | Supabase Auth (bcrypt). SHA-256 frontend = mot de passe Supabase |

### Google Sheets (LEGACY — backup)

| Environnement | Sheet ID |
|---|---|
| **Backup** (emails + référence) | `1SiE3lHf9dAKbExWPGNrk5cbLhDbKUKM4xvd1Th1frY4` |

Service account : `algebreboost-sheets-2595a71cadfb.json` (ignoré par git).

### Script Properties (GAS PropertiesService)

| Clé | Rôle |
|---|---|
| `SHARED_SECRET` | Secret HMAC pour webhook Stripe |
| `ADMIN_MASTER_PWD` | Master password admin — permet de se connecter sur n'importe quel compte élève en mode read-only (ne consomme pas nextChapter/nextBoost, n'écrit pas DailyBoosts, ne rebuildSuivi pas). Configurer dans Apps Script → Paramètres → Propriétés de script |

---

## Supabase PostgreSQL — Schéma actif (14 tables)

> **Source de vérité : `supabase/schema.sql`** — en cas de doute sur les colonnes exactes, lire le SQL.
> Le tableau ci-dessous est un résumé humain, il peut diverger. Si contradiction → schema.sql a raison.

| Table | Équivalent Sheets | Colonnes clés | Index |
|---|---|---|---|
| **profiles** | Users | `code` (PK métier, char 6), `email`, `prenom`, `niveau`, `password_hash`, `is_admin`, `premium`, `premium_end` (date expiration), `trial_start` (legacy), `free_chapter` (chapitre gratuit freemium), `objectif` | code, email, niveau |
| **scores** | Scores | `code`, `chapitre`, `num_exo`, `resultat` (EASY/MEDIUM/HARD/SKIP), `date`, `source` | code+date, code+chapitre, dedup (code,chapitre,num_exo,date,source) |
| **progress** | Progress | `code`, `categorie`, `score` (adaptatif 0-100), `nb_exos`, `nb_erreurs`, `derniere_pratique`, `statut`, `streak` | code+categorie |
| **daily_boosts** | DailyBoosts | `code`, `date`, `boost_json` (JSONB), `exos_done` (0-5) | code+date (unique) |
| **curriculum** | Curriculum_Officiel | `niveau`, `categorie`, `titre`, `exos_json` (JSONB, 20 exos), `timer`, `ordered` | niveau+categorie (unique) |
| **diagnostic_exos** | DiagnosticExos | `niveau`, `categorie`, `exos_json` (JSONB, 2 exos) | niveau+categorie (unique) |
| **brevet_exos** | BrevetExos | `niveau`, `categorie`, `exos_json` | niveau+categorie (unique) |
| **brevet_results** | BrevetResults | `code`, `date`, `score_pct`, `detail_json` | code+date |
| **cours** | Cours | `niveau`, `categorie`, `section_10`, `section_20`, `publish_10`, `publish_20`, `date_maj` | niveau+categorie (unique) |
| **suivi** | 👁 Suivi | `code` (unique), `chap1..chap4` (JSONB), `boost` (JSONB), `action_nicolas` | code |
| **emails** | 📧 Emails | `email`, `type`, `status` (default 'envoyé'), `date` | email |
| **email_logs** | — (nouveau) | `email`, `prenom`, `type` (J+0/J+1/J+3/J+7/J+14/UNSUB), `statut`, `details`, `created_at` | email+type |
| **insights** | Insights | `code`, `type`, `message`, `source`, `ref` | code |
| **rapports** | Rapports | `date`, `contenu` | — |
| **contact** | Contact | `email`, `nom`, `message` | — |

### RLS (Row Level Security)
- **Données élève** (profiles, scores, progress, daily_boosts, brevet_results) : `code = my_code() OR is_admin()`
- **Contenu** (curriculum, diagnostic_exos, brevet_exos, cours) : lecture pour tout authentifié, écriture admin
- **Admin only** (suivi, emails, rapports) : `is_admin()`
- **Contact** : insertion publique, lecture admin

### Colonnes non utilisées (dead schema, conservées pour usage futur)
- `progress.nb_erreurs`, `progress.statut`, `progress.streak` — jamais lues ni écrites par le code
- `rapports` — table orpheline, aucune écriture depuis Supabase

---

## Onglets Google Sheets — LEGACY (backup uniquement)

> ⚠️ Ces onglets décrivent la structure Google Sheets historique.
> Les données live sont maintenant dans Supabase PostgreSQL (14 tables).
> Google Sheets n'est plus utilisé pour les emails (migration Resend 07/04/2026). Conservé comme backup de référence.

### Onglets Nicolas (lecture + écriture via Admin)

| Onglet | Rôle | Qui y accède |
|---|---|---|
| `👁 Suivi` | Tableau de bord quotidien (1 ligne/élève) | Nicolas (principal), GAS (écriture via rebuildSuivi) |
| `📋 Historique` | Log chronologique exercices (récent en haut) | Nicolas (lecture), GAS (écriture via writeToHistorique) |

### Onglets GAS (ne pas modifier manuellement)

| Onglet | Rôle | Modifier ? |
|---|---|---|
| `Users` | Comptes utilisateurs | ❌ Sauf IsAdmin manuellement |
| `Progress` | Score/statut par chapitre par élève | ❌ |
| `Scores` | Toutes les réponses individuelles | ❌ |
| `DailyBoosts` | Historique des boosts quotidiens | Lecture + admin panel |
| `Curriculum_Officiel` | Exercices par chapitre (440 exos, format parapluie v4 aplati) | ❌ Via scripts Python seulement |
| `DiagnosticExos` | Exercices de diagnostic (54 exos, 3 par chapitre × 18 chapitres) | ❌ Via scripts Python seulement |
| `RemediationChapters` | Chapitres de remédiation (désactivé) | ❌ |
| `BrevetExos` | Exercices brevet 3EME (144 exos, 15 chap, format standard) | ❌ Via script Python seulement |
| `BrevetResults` | Résultats brevets blancs | ❌ |
| `📧 Emails` | Archive des emails envoyés | Lecture seule |
| `Insights` | Feedbacks élèves (signalement erreur + feedback session boost/brevet/chapitre) | Lecture seule |
| `Rapports` | Rapports quotidiens 7h | Lecture seule |
| `Cours` | Cours par chapitre rédigés par admin (4 sections × 54 chap) | ❌ Via admin panel uniquement |

### Onglets temporaires / secondaires

| Onglet | Rôle | Modifier ? |
|---|---|---|
| `Contact` | Log des formulaires de contact (`send_contact`) | Lecture seule |

### Onglets archivés

Supprimés par `cleanup_all` le 14 mars 2026 : `_ARCHIVE_Queue`, `_ARCHIVE_Prerequisites`, `_ARCHIVE_Rapports`, `_ARCHIVE_Pending_Exos`, `Pending_Exos`, `Queue`, `Programme_Officiel`, `Waitlist`.

Supprimés le 2 avril 2026 : `prompts`, `BoostExos`, `AuditExos`, `Prospection`, `Annonces_LBC`, `Annonces_LBC_2`, `RemediationChapters`, `Teasing_Early`, `Webhook_Log`. 11 comptes test (`@matheux.fr`) purgés de Users/DailyBoosts.

### Références mortes dans backend.js (SH constant)

`SH.PREREQS` (`Prerequisites`), `SH.QUEUE` (`Queue`), `SH.PENDING` (`Pending_Exos`), `SH.REMEDIATION` (`RemediationChapters`), `SH.BOOSTEXOS` (`BoostExos`) — onglets supprimés mais encore déclarés dans le code. Le helper `getSheet()` gère les tabs manquants sans erreur. À nettoyer dans un futur sprint.

---

## Schéma détaillé par onglet

### Users

| Col | Nom | Type | Description |
|---|---|---|---|
| A | Code | String | ⚠️ **CLÉ PRIMAIRE** — identifiant unique 6 chars (ex: `FP48QF`). FK utilisée par Scores, Progress, DailyBoosts, Suivi. Si cette colonne disparaît, le backend renvoie `history=[]` → quiz diagnostic forcé pour tous les élèves |
| B | Prénom | String | |
| C | Niveau | String | `6EME` / `5EME` / `4EME` / `3EME` / `1ERE` |
| D | Email | String | lowercase, trimmed |
| E | PasswordHash | String | SHA-256(`email::password::AB22`) |
| F | DateInscription | Date | `yyyy-MM-dd` |
| G | IsAdmin | Number | `0` ou `1` (ou `true`/`TRUE`) |
| H | Premium | Number | `0` ou `1` |
| I | TrialStart | Date | Date début essai 7 jours |
| J | PremiumEnd | Date | Date fin premium (futur Stripe) |
| K | IsTest | Number | `0` = vrai élève, `1` = compte test |
| L | PendingBrevet | String | JSON `{chapitres:[], message, date}` quand admin publie un brevet blanc |
| M | RevisionChapters | String | JSON `[{niveau:"5EME", categorie:"Fractions"}]` — chapitres d'une autre année assignés par l'admin. Auto-créée si absente. |
| N | Objectif | String | Objectif déclaré post-quiz : lacunes / chapitre_jour / brevet / toutes_matieres |

**Règles importantes :**
- Emails `@matheux.fr` → `IsTest=1` automatiquement au `register()`
- Limite bêta supprimée 02/04 (migration Supabase)
- `login()` vérifie `isAdmin` et `premium` de façon robuste (`true`/`TRUE`/`1`/`'1'`)

### Scores

| Col | Nom | Type | Description |
|---|---|---|---|
| A | Code | String | FK → Users |
| B | Prénom | String | |
| C | Niveau | String | |
| D | Chapitre | String | Identifiant catégorie (ex: `Fractions`) |
| E | NumExo | Number | Index 1-based |
| F | Énoncé | String | Texte exact de la question (tronqué 60 chars dans Historique) |
| G | Résultat | String | `EASY` / `MEDIUM` / `HARD` |
| H | Temps(sec) | Number | Durée sur l'exercice |
| I | NbIndices | Number | Nombre d'indices demandés |
| J | FormuleVue | Number | `0` ou `1` |
| K | MauvaiseOption | String | Option choisie si erreur QCM |
| L | Draft | String | Texte brouillon de l'élève |
| M | Date | Date | `yyyy-MM-dd` |
| N | Source | String | `BOOST` / `CALIBRAGE` / `` (curriculum) — ajouté BUG-06 fix |

### Progress

| Col | Nom | Type | Description |
|---|---|---|---|
| A | Code | String | FK → Users |
| B | Niveau | String | |
| C | Chapitre | String | Identifiant catégorie |
| D | Score | Number | Score de confiance adaptatif 0-100. **≠ P8** : calculé par `updateConfidenceScore()` avec delta cumulatif (+5/+10/-3/-5 par réponse) + décroissance >14j inactivité. Le score P8 (EASY/total×100) est calculé côté frontend pour pills/sessions retro |
| E | NbExos | Number | Nombre total d'exercices faits |
| F | NbErreurs | Number | Nombre d'erreurs (HARD) |
| G | DernierePratique | Date | Date du dernier exercice |
| H | Statut | String | `en_cours` / `maitrise` |
| I | Streak | Number | Série en cours |

### DailyBoosts

| Col | Nom | Type | Description |
|---|---|---|---|
| A | Code | String | FK → Users |
| B | Date | Date | `yyyy-MM-dd` (date du boost) |
| C | BoostJSON | String | JSON `{insight, exos:[...5 exercices]}` |
| D | ExosDone | Number | Nombre d'exercices complétés (0-5) |

**Règles :**
- `login()` crée l'entrée avec `ExosDone=0` quand un boost est livré
- `save_score` incrémente `ExosDone` quand `source=BOOST`
- `generateDailyBoost` écrit 4 colonnes (dont `ExosDone=0`)

### Curriculum_Officiel

| Col | Nom | Type | Description |
|---|---|---|---|
| A | Niveau | String | `6EME` / `5EME` / `4EME` / `3EME` / `1ERE` |
| B | Categorie | String | Identifiant unique (ex: `Fractions`) |
| C | Titre | String | Nom affiché (ex: `Fractions 🍕`) |
| D | Icone | String | Emoji |
| E | ExosJSON | String | JSON tableau de 20 exercices |
| F | Timer | Number | *(optionnel)* Durée timer en secondes (défaut 60). `30` pour Automatismes |
| G | Ordered | Boolean | *(optionnel)* `true` = exercices non mélangés (fil narratif) |

**Format exercice :**
```json
{
  "lvl": 1,
  "q": "Calcule : $\\frac{3}{4} + \\frac{1}{2}$",
  "a": "$\\frac{5}{4}$",
  "options": ["$\\frac{5}{4}$", "$\\frac{4}{6}$", "$\\frac{3}{8}$"],
  "f": "Formule clé (floue au début, révélée au tap)",
  "steps": ["Indice 1", "Indice 2", "Indice 3"]
}
```

- 10 exercices `lvl:1` (fondamentaux) + 10 `lvl:2` (avancés) par chapitre
- 54 chapitres × 20 exos = **1080 exercices** en prod

### BoostExos

| Col | Nom | Type | Description |
|---|---|---|---|
| A | Niveau | String | `6EME` / `5EME` / `4EME` / `3EME` / `1ERE` |
| B | Categorie | String | Identifiant catégorie (même noms que Curriculum_Officiel) |
| C | ExosJSON | String | JSON tableau de 10 exercices (5 lvl1 + 5 lvl2) |

Pool d'exercices **dédiée aux boosts quotidiens**, séparée de Curriculum_Officiel pour éviter que les exercices de boost polluent la progression des chapitres. Même format d'exercice, mêmes compétences, mais nombres et wording différents.

54 chapitres × 10 exos = **540 exercices boost** en prod.

**Fallback** : si l'onglet BoostExos est absent ou vide pour un niveau, `generateDailyBoost()` utilise Curriculum_Officiel automatiquement.

### DiagnosticExos

| Col | Nom | Type | Description |
|---|---|---|---|
| A | Niveau | String | |
| B | Categorie | String | Identifiant chapitre |
| C | ExosJSON | String | JSON tableau de 2 exercices (1 lvl1 + 1 lvl2) |

54 chapitres × 2 exos = **108 exercices** de diagnostic.

### BrevetExos

| Col | Nom | Type | Description |
|---|---|---|---|
| A | Niveau | String | (toujours `3EME`) |
| B | Categorie | String | Chapitre brevet |
| C | ExosJSON | String | JSON tableau d'exercices `{lvl, q, a, options:[], f, steps:[]}` (format standard) |

15 chapitres × 8-16 exos = **144 exercices** style brevet (3 chapitres fusionnés à 16 exos).

### Cours

| Col | Nom | Type | Description |
|---|---|---|---|
| A | Niveau | String | `6EME` / `5EME` / `4EME` / `3EME` / `1ERE` |
| B | Categorie | String | Identifiant chapitre (même que Curriculum_Officiel) |
| C | Section10 | String | Contenu cours débloqué à 10 exos — "L'essentiel — Méthode & Exemples" |
| D | Section20 | String | Contenu cours débloqué à 20 exos — "Cours complet ✨" |
| E | Publish10 | Date | Date de publication section_10 (gate J+1) |
| F | Publish20 | Date | Date de publication section_20 (gate J+1) |
| G | DateMaj | Date | Date de dernière modification |

**Règles :**
- Géré par l'agent admin-auto (génération) + dashboard admin (édition manuelle via `save_cours`)
- Chargé au login → `coursData` dans la réponse → `S.coursMap` dans le frontend
- `nbExos` calculé depuis l'historique (source ≠ BOOST, catégorie ≠ CALIBRAGE)
- Milestones **10/20** → toast gamification +50 XP + bouton "📖 Mon cours" sur la carte chapitre
- Imprimable/PDF via bouton dans la modale cours (`window.print()`)

### Mécanisme J+1 (publishDate) — NON NÉGOCIABLE

**Principe** : l'élève ne reçoit JAMAIS du contenu fraîchement généré le jour même.

#### Via Suivi (chapitres + boosts admin)
Les JSON des cellules →Nouveau Boost (col S) et →Nouveau Ch (cols G/J/M/P) contiennent un champ `publishDate` (format `yyyy-MM-dd`), auto-ajouté par `publishAdminBoost()` / `publishAdminChapter()`.

`login()` ne délivre le contenu que si `publishDate < today`. Si publié aujourd'hui → `teasingChapter: true` / `teasingBoost: true` dans la réponse, cellule NON vidée. L'élève voit une modale teasing ("Rendez-vous demain 🔥"). Le lendemain, `publishDate < today` → contenu livré normalement et cellule vidée.

#### Via DailyBoosts (agent admin autonome)
L'agent injecte directement dans DailyBoosts avec `Date = demain` et `ExosDone = 0`.

`login()` cherche un boost dont `Date == today` (L487-498). Si `Date = demain`, le boost n'est **pas** trouvé aujourd'hui. Le lendemain, `Date == today` → le boost est livré.

**Rattrapage** (L500-503) : si l'élève se connecte plusieurs jours après, le boost est servi via le fallback `lastUnfinishedBoost` (cherche le dernier boost avec `ExosDone < 5`). Le boost n'est jamais perdu.

| Scénario | Résultat | Mécanisme |
|---|---|---|
| Connexion jour de l'injection | ❌ Pas visible | `Date != today` |
| Connexion le lendemain | ✅ Livré | `Date == today` |
| Connexion J+12 | ✅ Livré en rattrapage | `ExosDone < 5` → fallback |

#### Via Cours (agent admin autonome)
L'agent injecte les cours avec `publish_10` / `publish_20` = TOMORROW. L'Edge Function `login()` ne débloque une section que si `publish_XX <= today`. Si la section existe mais `publish_XX > today` → `teasingCours` dans la réponse → bandeau "📖 Nouvelle section de cours dispo demain matin !" sur la carte chapitre. Les sections déjà publiées restent visibles — seules les **nouvelles** sections sont soumises à J+1.

### BrevetResults

| Col | Nom | Type | Description |
|---|---|---|---|
| A | Code | String | FK → Users |
| B | Prénom | String | |
| C | Niveau | String | |
| D | Date | Date | |
| E | Chapitres | String | Liste chapitres testés |
| F | NbQuestions | Number | |
| G | NbCorrect | Number | |
| H | Score% | Number | |
| I | DetailJSON | String | Détail par chapitre |
| J | Message | String | Message admin si brevet publié |

**Isolation** : BrevetResults est séparé de Progress/Scores → ne perturbe pas l'algorithme adaptatif.

### 👁 Suivi

Structure colonnes (GAS : Code en col U = index 20, 1-based) :

```
A: ⚡ ACTION NICOLAS    B: Prénom    C: Niveau    D: Dernière connexion
E: Chapitre 1    F: Statut 1    G: 📝 Ch1 suite (Nicolas)
H: Chapitre 2    I: Statut 2    J: 📝 Ch2 suite (Nicolas)
K: Chapitre 3    L: Statut 3    M: 📝 Ch3 suite (Nicolas)
N: Chapitre 4    O: Statut 4    P: 📝 Ch4 suite (Nicolas)
Q: Boost consommé?    R: 📝 Prochain boost (Nicolas)
S: 📧 Rapport envoyé / Chap5+    [T: Code masquée]
```

→Nouveau Ch : indices [6, 9, 12, 15] | →Boost : index 18

### Règles ⚡ ACTION NICOLAS (rebuildSuivi)

| Valeur | Condition | Priorité |
|---|---|---|
| `🔴 BLOQUÉ` | inactif >7j ET score <40 sur tous chapitres | 1 |
| `⚡ BOOST TERMINÉ → préparer le suivant` | ExosDone==5 ET pas de boost pending (inclut boost du jour) | 2 |
| `✅ CHAPITRE TERMINÉ → assigner la suite` | Progress NbExos ≥20 ET colonnes 📝 Nicolas vides | 3 |
| `📝 BREVET EN ATTENTE → à faire` | PendingBrevet non vide ET niveau 3EME | 3b |
| `👍 RAS` | sinon | 4 |

Plusieurs règles simultanées → toutes affichées en pills, couleur card = plus urgente.

### Insights

| Col | Nom | Type | Description |
|---|---|---|---|
| A | Date | DateTime | `yyyy-MM-dd HH:mm` |
| B | Code | String | FK → Users |
| C | Prénom | String | |
| D | Niveau | String | |
| E | Type | String | `difficile` / `moyen` / `bien` / `super` / `trop_dur` / `erreur` / `general` / `pas_compris` / `contact_parent` |
| F | Message | String | Texte libre optionnel |
| G | Énoncé exo | String | Texte de l'exercice tronqué 80 chars (si signalement) |
| H | Note (1-5) | Number | Rating numérique |
| I | Source | String | `boost` / `brevet` / `chapitre` / `general` (vide = signalement erreur) |
| J | Ref | String | Catégorie concernée ou `BOOST` / `BREVET` |

---

## Relations entre onglets

```
Users (Code) ──┬── Scores (Code)
               ├── Progress (Code)
               ├── DailyBoosts (Code)
               ├── BrevetResults (Code)
               └── 👁 Suivi (Code en col T)

Curriculum_Officiel (Niveau, Categorie) ── DiagnosticExos (Niveau, Categorie)
BoostExos (Niveau, Categorie) ── même structure que Curriculum (pool séparée)
BrevetExos (Niveau, Categorie) ── standalone (pas de FK vers Curriculum)
Insights ── standalone (feedback élève : signalement + session)
📧 Emails ── standalone (archive)
Rapports ── standalone (archive)
```

---

## Chapitres disponibles — 54 chapitres en prod (màj 14 mars 2026)

| Niveau | Chapitres |
|---|---|
| 6EME (13) | Nombres_entiers, Fractions, Proportionnalité, Géométrie, Périmètres_Aires, Angles, Nombres_Décimaux, Statistiques_6ème, Symétrie_Axiale, Volumes, Agrandissement_Réduction, Conversions_Unités, Puissances_10 |
| 5EME (10) | Fractions, Nombres_relatifs, Proportionnalité, Calcul_Littéral, Pythagore, Puissances, Symétrie_Centrale, Transformations, Racines_Carrées, Triangles_Semblables |
| 4EME (10) | Puissances, Fractions, Proportionnalité, Calcul_Littéral, Équations, Pythagore, Fonctions_Linéaires, Inéquations, Homothétie, Sections_Solides |
| 3EME (11) | Calcul_Littéral, Équations, Fonctions, Théorème_de_Thalès, Trigonométrie, Statistiques, Probabilités, Racines_Carrées, Systèmes_Équations, Inéquations, Notation_Scientifique |
| 1ERE (10) | Second_Degre, Suites, Derivation, Exponentielle, Trigonometrie, Produit_Scalaire, Geometrie_Repere, Probabilites_Cond, Variables_Aleatoires, Algorithmique |

Total : **54 chapitres × 20 exos = 1080 exercices** + **54 × 10 = 540 boost (BoostExos)** + **54 × 2 = 108 diagnostics** + **15 chap × 8-16 = 144 brevet** (3EME uniquement)

**Audit qualité @77 (15 mars 2026)** : 1872 exercices audités et corrigés. Score qualité global ~98% (correction mathématique 100%, notation française, indices S1 reformulés, doublons 1ERE réécrits). Voir `docs/archive/audit-exercices-2026-03.md` pour le détail complet.

**Flux boost auto** : diagnostic ne teste que les chapitres sélectionnés → P5 filtre BoostExos aux mêmes chapitres → boost ciblé, pas de dispersion cross-chapitre.
