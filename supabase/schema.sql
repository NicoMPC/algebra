-- ════════════════════════════════════════════════════════════
--  MATHEUX — Schéma PostgreSQL Supabase
--  Migration depuis Google Sheets
--  Généré le 2026-04-02
-- ════════════════════════════════════════════════════════════

-- Utilise Supabase Auth (auth.users) pour l'authentification.
-- La table profiles stocke les données métier de chaque élève.

-- ── Extensions ──────────────────────────────────────────────
create extension if not exists "pgcrypto";

-- ════════════════════════════════════════════════════════════
--  1. PROFILES (= Users)
--  Lié à auth.users via id (UUID Supabase Auth)
-- ════════════════════════════════════════════════════════════

create table profiles (
  id            uuid primary key references auth.users(id) on delete cascade,
  code          char(6) not null unique,              -- clé métier visible (ex: FP48QF)
  prenom        text not null,
  niveau        text not null check (niveau in ('6EME','5EME','4EME','3EME','1ERE')),
  email         text not null unique,                  -- lowercase, trimmed
  password_hash text,                                  -- SHA-256 hash pour fallback auth (ajouté par fix_schema.sql)
  date_inscription date not null default current_date,
  is_admin      boolean not null default false,
  premium       boolean not null default false,
  trial_start   date,                                  -- début essai (legacy, conservé pour tracking)
  premium_end   date,                                  -- fin premium (Stripe) — ex: 2026-06-30 pour Brevet 2026
  free_chapter  text,                                  -- chapitre gratuit (freemium) — set après diagnostic
  is_test       boolean not null default false,        -- compte test (@matheux.fr)
  pending_brevet jsonb,                                -- JSON {chapitres, message, date}
  revision_chapters jsonb,                             -- JSON [{niveau, categorie}]
  objectif      text,                                  -- lacunes / chapitre_jour / brevet / toutes_matieres
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);

create index idx_profiles_code on profiles(code);
create index idx_profiles_email on profiles(email);
create index idx_profiles_niveau on profiles(niveau);

comment on table profiles is 'Profils élèves — données métier (auth gérée par Supabase Auth)';

-- ════════════════════════════════════════════════════════════
--  2. SCORES (= Scores)
--  Chaque réponse individuelle d'un élève
-- ════════════════════════════════════════════════════════════

create table scores (
  id            bigint generated always as identity primary key,
  code          char(6) not null references profiles(code) on delete cascade,
  prenom        text not null,
  niveau        text not null,
  chapitre      text not null,                         -- identifiant catégorie (ex: Fractions)
  num_exo       integer not null,                      -- index 1-based
  enonce        text,                                  -- texte exact de la question
  resultat      text not null check (resultat in ('EASY','MEDIUM','HARD','SKIP')),
  temps_sec     integer not null default 0,
  nb_indices    integer not null default 0,
  formule_vue   boolean not null default false,
  mauvaise_option text,                                -- option choisie si erreur QCM
  draft         text,                                  -- brouillon élève
  date          date not null default current_date,
  source        text not null default '',               -- 'BOOST' / 'CALIBRAGE' / '' (curriculum)
  created_at    timestamptz not null default now()
);

create index idx_scores_code on scores(code);
create index idx_scores_code_date on scores(code, date);
create index idx_scores_code_chapitre on scores(code, chapitre);
create index idx_scores_chapitre on scores(chapitre);

-- Contrainte de déduplication : même (code, chapitre, num_exo, date, source) = déjà enregistré
-- (source ajouté par fix_schema.sql : BOOST et curriculum peuvent avoir même idx)
create unique index idx_scores_dedup on scores(code, chapitre, num_exo, date, source);

comment on table scores is 'Toutes les réponses individuelles des élèves';

-- ════════════════════════════════════════════════════════════
--  3. PROGRESS (= Progress)
--  Score/statut par chapitre par élève
-- ════════════════════════════════════════════════════════════

create table progress (
  id              bigint generated always as identity primary key,
  code            char(6) not null references profiles(code) on delete cascade,
  niveau          text not null,
  categorie       text not null,
  score           integer not null default 0,          -- score confiance adaptatif 0-100
  nb_exos         integer not null default 0,
  nb_erreurs      integer not null default 0,
  derniere_pratique date,
  statut          text not null default 'en_cours' check (statut in ('en_cours','maitrise')),
  streak          integer not null default 0,
  created_at      timestamptz not null default now(),
  updated_at      timestamptz not null default now(),
  unique(code, categorie)
);

create index idx_progress_code on progress(code);
create index idx_progress_code_chapitre on progress(code, chapitre);

comment on table progress is 'Score de confiance et statut par chapitre par élève';

-- ════════════════════════════════════════════════════════════
--  4. DAILY_BOOSTS (= DailyBoosts)
--  Historique des boosts quotidiens
-- ════════════════════════════════════════════════════════════

create table daily_boosts (
  id          bigint generated always as identity primary key,
  code        char(6) not null references profiles(code) on delete cascade,
  date        date not null,                           -- date du boost
  boost_json  jsonb not null,                          -- {insight, exos:[...5 exercices]}
  exos_done   integer not null default 0,              -- 0-5
  created_at  timestamptz not null default now(),
  unique(code, date)
);

create index idx_daily_boosts_code on daily_boosts(code);
create index idx_daily_boosts_code_date on daily_boosts(code, date);

comment on table daily_boosts is 'Boosts quotidiens — 5 exercices ciblés sur les lacunes';

-- ════════════════════════════════════════════════════════════
--  5. CURRICULUM (= Curriculum_Officiel)
--  Exercices par chapitre (contenu pédagogique)
-- ════════════════════════════════════════════════════════════

create table curriculum (
  id          bigint generated always as identity primary key,
  niveau      text not null check (niveau in ('6EME','5EME','4EME','3EME','1ERE')),
  categorie   text not null,                           -- identifiant unique (ex: Fractions)
  titre       text not null,                           -- nom affiché (ex: Fractions 🍕)
  icone       text,                                    -- emoji
  exos_json   jsonb not null,                          -- tableau de 20 exercices
  timer       integer default 60,                      -- durée timer en secondes (30 pour Automatismes)
  ordered     boolean not null default false,           -- true = exercices non mélangés (fil narratif)
  unique(niveau, categorie)
);

create index idx_curriculum_niveau on curriculum(niveau);
create index idx_curriculum_categorie on curriculum(categorie);

comment on table curriculum is 'Exercices par chapitre — 54 chapitres × 20 exos = 1080 exercices';

-- ════════════════════════════════════════════════════════════
--  6. DIAGNOSTIC_EXOS (= DiagnosticExos)
--  Exercices de diagnostic (2 par chapitre)
-- ════════════════════════════════════════════════════════════

create table diagnostic_exos (
  id          bigint generated always as identity primary key,
  niveau      text not null,
  categorie   text not null,
  exos_json   jsonb not null,                          -- tableau de 2 exercices
  unique(niveau, categorie)
);

create index idx_diagnostic_exos_niveau on diagnostic_exos(niveau);

comment on table diagnostic_exos is 'Exercices de diagnostic — 54 chapitres × 2 exos = 108 exercices';

-- ════════════════════════════════════════════════════════════
--  7. BREVET_EXOS (= BrevetExos)
--  Exercices style brevet (3EME uniquement)
-- ════════════════════════════════════════════════════════════

create table brevet_exos (
  id          bigint generated always as identity primary key,
  niveau      text not null default '3EME',
  categorie   text not null,                           -- chapitre brevet
  exos_json   jsonb not null,                          -- tableau d'exercices format standard
  unique(niveau, categorie)
);

comment on table brevet_exos is 'Exercices style brevet 3EME — 15 chapitres × 8-16 exos = 144 exercices';

-- ════════════════════════════════════════════════════════════
--  8. BREVET_RESULTS (= BrevetResults)
--  Résultats des brevets blancs
-- ════════════════════════════════════════════════════════════

create table brevet_results (
  id            bigint generated always as identity primary key,
  code          char(6) not null references profiles(code) on delete cascade,
  prenom        text not null,
  niveau        text not null,
  date          date not null default current_date,
  chapitres     text,                                  -- liste chapitres testés
  nb_questions  integer not null default 0,
  nb_correct    integer not null default 0,
  score_pct     numeric(5,2) not null default 0,       -- pourcentage
  detail_json   jsonb,                                 -- détail par chapitre
  message       text,                                  -- message admin si brevet publié
  created_at    timestamptz not null default now()
);

create index idx_brevet_results_code on brevet_results(code);
create index idx_brevet_results_code_date on brevet_results(code, date);

comment on table brevet_results is 'Résultats des brevets blancs — isolés de Progress/Scores';

-- ════════════════════════════════════════════════════════════
--  9. COURS (= Cours)
--  Cours par chapitre, débloqués progressivement
-- ════════════════════════════════════════════════════════════

create table cours (
  id          bigint generated always as identity primary key,
  niveau      text not null,
  categorie   text not null,
  section_10  text,                                    -- contenu débloqué à 10 exos
  section_20  text,                                    -- contenu débloqué à 20 exos
  publish_10  date,                                    -- date de publication section_10 (J+1)
  publish_20  date,                                    -- date de publication section_20 (J+1)
  date_maj    date,                                    -- dernière modification
  unique(niveau, categorie)
);

create index idx_cours_niveau on cours(niveau);

comment on table cours is 'Cours par chapitre — 2 sections débloquées à 10 et 20 exos curriculum';

-- ════════════════════════════════════════════════════════════
--  10. EMAILS (= 📧 Emails)
--  Archive des emails envoyés
-- ════════════════════════════════════════════════════════════

create table emails (
  id          bigint generated always as identity primary key,
  date        timestamptz not null default now(),      -- yyyy-MM-dd HH:mm
  email       text not null,
  prenom      text,
  type        text not null,                           -- J+0, J+3, etc.
  status      text not null default 'envoyé',           -- envoyé / erreur
  subject     text,
  created_at  timestamptz not null default now()
);

create index idx_emails_email on emails(email);

comment on table emails is 'Archive des emails envoyés — marketing et transactionnels';

-- ════════════════════════════════════════════════════════════
--  11. INSIGHTS (= Insights)
--  Feedbacks élèves (signalements + feedback session)
-- ════════════════════════════════════════════════════════════

create table insights (
  id          bigint generated always as identity primary key,
  date        timestamptz not null default now(),
  code        char(6) references profiles(code) on delete set null,
  prenom      text,
  niveau      text,
  type        text not null,                           -- difficile/moyen/bien/super/trop_dur/erreur/general/pas_compris/contact_parent
  message     text,                                    -- texte libre optionnel
  enonce_exo  text,                                    -- texte exercice tronqué 80 chars
  note        integer check (note between 1 and 5),    -- rating numérique
  source      text,                                    -- boost/brevet/chapitre/general
  ref         text,                                    -- catégorie ou BOOST/BREVET
  created_at  timestamptz not null default now()
);

create index idx_insights_code on insights(code);

comment on table insights is 'Feedbacks élèves — signalements erreur + feedback session';

-- ════════════════════════════════════════════════════════════
--  12. RAPPORTS (= Rapports)
--  Rapports quotidiens automatiques (7h)
-- ════════════════════════════════════════════════════════════

create table rapports (
  id          bigint generated always as identity primary key,
  date        timestamptz not null default now(),
  contenu     text not null,                           -- contenu du rapport
  created_at  timestamptz not null default now()
);

comment on table rapports is 'Rapports quotidiens générés à 7h';

-- ════════════════════════════════════════════════════════════
--  13. CONTACT (= Contact)
--  Formulaires de contact
-- ════════════════════════════════════════════════════════════

create table contact (
  id          bigint generated always as identity primary key,
  date        timestamptz not null default now(),
  email       text not null,
  nom         text,
  message     text not null,
  created_at  timestamptz not null default now()
);

comment on table contact is 'Log des formulaires de contact (send_contact)';

-- ════════════════════════════════════════════════════════════
--  14. SUIVI (= 👁 Suivi)
--  Vue matérialisée du tableau de bord admin
--  Reconstruit périodiquement (équivalent de rebuildSuivi)
-- ════════════════════════════════════════════════════════════

create table suivi (
  id                  bigint generated always as identity primary key,
  code                char(6) not null references profiles(code) on delete cascade unique,
  prenom              text,
  niveau              text,
  action_nicolas      text,                            -- 🔴 BLOQUÉ / ⚡ BOOST TERMINÉ / ✅ CHAPITRE TERMINÉ / 👍 RAS
  derniere_connexion  date,

  -- Slots chapitres 1-4 (renommés via fix_schema.sql)
  chap1               jsonb,                           -- JSON chapitre assigné par Nicolas (avec publishDate)
  chap2               jsonb,
  chap3               jsonb,
  chap4               jsonb,

  -- Boost (renommé via fix_schema.sql)
  boost_consomme      boolean default false,
  boost               jsonb,                           -- JSON boost assigné par Nicolas (avec publishDate)

  updated_at          timestamptz not null default now()
);

create index idx_suivi_code on suivi(code);

comment on table suivi is 'Tableau de bord admin — 1 ligne par élève, reconstruit par rebuildSuivi';

-- ════════════════════════════════════════════════════════════
--  TRIGGER : updated_at automatique
-- ════════════════════════════════════════════════════════════

create or replace function update_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

create trigger trg_profiles_updated_at
  before update on profiles
  for each row execute function update_updated_at();

create trigger trg_progress_updated_at
  before update on progress
  for each row execute function update_updated_at();

create trigger trg_suivi_updated_at
  before update on suivi
  for each row execute function update_updated_at();

-- ════════════════════════════════════════════════════════════
--  ROW LEVEL SECURITY (RLS)
-- ════════════════════════════════════════════════════════════

-- Fonction helper : vérifie si l'utilisateur courant est admin
create or replace function is_admin()
returns boolean as $$
  select coalesce(
    (select is_admin from profiles where id = auth.uid()),
    false
  );
$$ language sql security definer stable;

-- Fonction helper : récupère le code de l'utilisateur courant
create or replace function my_code()
returns char(6) as $$
  select code from profiles where id = auth.uid();
$$ language sql security definer stable;

-- ── PROFILES ────────────────────────────────────────────────
alter table profiles enable row level security;

create policy "profiles_select_own"
  on profiles for select
  using (id = auth.uid() or is_admin());

create policy "profiles_update_own"
  on profiles for update
  using (id = auth.uid() or is_admin());

create policy "profiles_insert_self"
  on profiles for insert
  with check (id = auth.uid());

-- Admin peut supprimer
create policy "profiles_delete_admin"
  on profiles for delete
  using (is_admin());

-- ── SCORES ──────────────────────────────────────────────────
alter table scores enable row level security;

create policy "scores_select_own"
  on scores for select
  using (code = my_code() or is_admin());

create policy "scores_insert_own"
  on scores for insert
  with check (code = my_code() or is_admin());

-- Pas de update/delete sur les scores (append-only)

-- ── PROGRESS ────────────────────────────────────────────────
alter table progress enable row level security;

create policy "progress_select_own"
  on progress for select
  using (code = my_code() or is_admin());

create policy "progress_insert_own"
  on progress for insert
  with check (code = my_code() or is_admin());

create policy "progress_update_own"
  on progress for update
  using (code = my_code() or is_admin());

-- ── DAILY_BOOSTS ────────────────────────────────────────────
alter table daily_boosts enable row level security;

create policy "daily_boosts_select_own"
  on daily_boosts for select
  using (code = my_code() or is_admin());

create policy "daily_boosts_insert_admin"
  on daily_boosts for insert
  with check (code = my_code() or is_admin());

create policy "daily_boosts_update_own"
  on daily_boosts for update
  using (code = my_code() or is_admin());

-- ── CURRICULUM (lecture seule pour tous les authentifiés) ────
alter table curriculum enable row level security;

create policy "curriculum_select_authenticated"
  on curriculum for select
  using (auth.uid() is not null);

create policy "curriculum_modify_admin"
  on curriculum for all
  using (is_admin());

-- ── DIAGNOSTIC_EXOS (lecture seule pour tous les authentifiés)
alter table diagnostic_exos enable row level security;

create policy "diagnostic_exos_select_authenticated"
  on diagnostic_exos for select
  using (auth.uid() is not null);

create policy "diagnostic_exos_modify_admin"
  on diagnostic_exos for all
  using (is_admin());

-- ── BREVET_EXOS (lecture seule pour tous les authentifiés) ───
alter table brevet_exos enable row level security;

create policy "brevet_exos_select_authenticated"
  on brevet_exos for select
  using (auth.uid() is not null);

create policy "brevet_exos_modify_admin"
  on brevet_exos for all
  using (is_admin());

-- ── BREVET_RESULTS ──────────────────────────────────────────
alter table brevet_results enable row level security;

create policy "brevet_results_select_own"
  on brevet_results for select
  using (code = my_code() or is_admin());

create policy "brevet_results_insert_own"
  on brevet_results for insert
  with check (code = my_code() or is_admin());

-- ── COURS (lecture pour tous les authentifiés, écriture admin)
alter table cours enable row level security;

create policy "cours_select_authenticated"
  on cours for select
  using (auth.uid() is not null);

create policy "cours_modify_admin"
  on cours for all
  using (is_admin());

-- ── EMAILS (admin seulement) ────────────────────────────────
alter table emails enable row level security;

create policy "emails_admin_only"
  on emails for all
  using (is_admin());

-- Le backend (service_role) peut insérer sans RLS

-- ── INSIGHTS ────────────────────────────────────────────────
alter table insights enable row level security;

create policy "insights_select_admin"
  on insights for select
  using (is_admin());

create policy "insights_insert_authenticated"
  on insights for insert
  with check (auth.uid() is not null);

-- ── RAPPORTS (admin seulement) ──────────────────────────────
alter table rapports enable row level security;

create policy "rapports_admin_only"
  on rapports for all
  using (is_admin());

-- ── CONTACT (insertion publique, lecture admin) ─────────────
alter table contact enable row level security;

create policy "contact_insert_anon"
  on contact for insert
  with check (true);  -- formulaire public

create policy "contact_select_admin"
  on contact for select
  using (is_admin());

-- ── SUIVI (admin seulement) ─────────────────────────────────
alter table suivi enable row level security;

create policy "suivi_admin_only"
  on suivi for all
  using (is_admin());

-- ════════════════════════════════════════════════════════════
--  15-24. REFONTE « DIAGNOSTIC 3E » (migration 20260924_diagnostic_3e.sql)
--  competences, items, maitrise, diagnostics, reponses_items, achats,
--  funnel_events, bilan_partages, consentements, email_logs (+ colonnes profiles)
--  Spec : docs/specs/20-moteur.md
-- ════════════════════════════════════════════════════════════

-- ── 1. COMPETENCES (référentiel, data/referentiel_3eme/competences.json) ──
create table if not exists competences (
  id               text primary key,                         -- NC.FRAC.03
  domaine          text not null check (domaine in ('NC','DF','GM','EG','AP')),
  theme            text not null,
  titre            text not null,
  titre_eleve      text,
  niveau_origine   text not null check (niveau_origine in ('6EME','5EME','4EME','3EME')),
  prerequis        text[] not null default '{}',             -- graphe acyclique (vérifié à l'import)
  poids_brevet     smallint not null default 1 check (poids_brevet between 1 and 3),
  chapitres_legacy text[] not null default '{}',
  erreurs          jsonb not null default '[]',              -- [{id, libelle, libelle_parent, remediation}]
  diag_autorise    boolean not null default true,            -- false = hors programme : entraînement seulement
  actif            boolean not null default true,
  updated_at       timestamptz not null default now()
);
create index if not exists idx_competences_domaine on competences(domaine);
comment on table competences is 'Référentiel de compétences atomiques 6e→3e (graphe de prérequis, erreurs types)';

-- ── 2. ITEMS (banque atomique, data/banque_3eme/**) ──
create table if not exists items (
  id          text primary key,                               -- NC.FRAC.03-017
  comp        text not null references competences(id) on update cascade,
  type        text not null default 'qcm' check (type in ('qcm','vf','fill')),
  lvl         smallint not null default 1 check (lvl between 1 and 3),
  usage       text[] not null default '{diag,train}',
  item_json   jsonb not null,                                 -- item complet (q, a, options, err, steps, f, alt, figure…)
  source      text,                                           -- chapitre legacy d'origine si repris d'un parapluie v4
  parapluie_id text,                                          -- reconstitution des problèmes Brevet
  num         smallint,
  depend_question_precedente boolean not null default false,  -- jamais servi seul
  actif       boolean not null default true,
  updated_at  timestamptz not null default now()
);
create index if not exists idx_items_comp on items(comp) where actif;
comment on table items is 'Banque d''items atomiques (1 question = 1 compétence), err = mauvaise réponse → erreur type';

-- ── 3. MAITRISE (élève × compétence, contrat §4) ──
create table if not exists maitrise (
  code               char(6) not null references profiles(code) on delete cascade,
  comp               text not null references competences(id) on update cascade on delete cascade,
  maitrise           real not null default 0.5 check (maitrise between 0 and 1),
  alpha              real not null default 1,                 -- Beta(alpha, beta) avec oubli (cf. spec §3)
  beta               real not null default 1,
  n_obs              integer not null default 0,
  n_succes           integer not null default 0,
  derniere_obs       date,
  erreurs_vues       jsonb not null default '{}',             -- {"NC.FRAC.03#somme_directe": 2}
  boite              smallint not null default 0,             -- répétition espacée (Leitner 0-4)
  prochaine_revision date,
  updated_at         timestamptz not null default now(),
  primary key (code, comp)
);
create index if not exists idx_maitrise_revision on maitrise(code, prochaine_revision);
comment on table maitrise is 'Maîtrise par élève et compétence — mise à jour après chaque réponse (diag + entraînement)';

-- ── 4. DIAGNOSTICS (sessions express / complet / mensuel + carte) ──
create table if not exists diagnostics (
  id          uuid primary key default gen_random_uuid(),
  code        char(6) not null references profiles(code) on delete cascade,
  type        text not null check (type in ('express','complet','mensuel')),
  statut      text not null default 'en_cours' check (statut in ('en_cours','termine','abandonne')),
  etat_json   jsonb not null,                                 -- état du moteur (reprise entre modules)
  carte_json  jsonb,                                          -- objet Carte (contrat §5) une fois terminé
  n_questions integer not null default 0,
  started_at  timestamptz not null default now(),
  finished_at timestamptz,
  updated_at  timestamptz not null default now()
);
create index if not exists idx_diagnostics_code on diagnostics(code, statut, finished_at desc);

-- ── 5. REPONSES_ITEMS (journal de toutes les réponses item par item) ──
create table if not exists reponses_items (
  id            bigint generated always as identity primary key,
  code          char(6) not null references profiles(code) on delete cascade,
  item_id       text not null,                                -- pas de FK : un item peut être réécrit/désactivé
  comp          text not null,
  contexte      text not null check (contexte in ('diag','train','legacy')),
  diagnostic_id uuid references diagnostics(id) on delete set null,
  ok            boolean not null,
  resultat      text,
  reponse       text,
  err_id        text,
  temps_sec     integer,
  date          date not null default current_date,
  created_at    timestamptz not null default now()
);
create index if not exists idx_reponses_items_code on reponses_items(code, date);

-- ── 6. ACHATS (droits : free < diagnostic_complet < programme_brevet) ──
create table if not exists achats (
  id                bigint generated always as identity primary key,
  code              char(6) references profiles(code) on delete set null,
  email             text not null,
  produit           text not null check (produit in ('diagnostic_complet','programme_brevet')),
  offre             text,                                     -- metadata.produit brut : diag_complet / programme_brevet / programme_upgrade
  offre_version     text,
  niveau            text,
  montant_cents     integer,
  stripe_session_id text unique,
  rembourse_at      timestamptz,                              -- saisi à la main par Nicolas en cas de remboursement
  created_at        timestamptz not null default now()
);
create index if not exists idx_achats_code on achats(code);
create index if not exists idx_achats_email on achats(email);

-- ── 7. Besoins growth / légal (50-offre-conversion, 51-emails, 52-legal) ──
alter table profiles add column if not exists email_eleve            text;
alter table profiles add column if not exists consentement_parent_at timestamptz;
alter table profiles add column if not exists optin_marketing        boolean not null default false;
alter table profiles add column if not exists optin_marketing_at     timestamptz;
alter table profiles add column if not exists date_brevet_blanc      date;
-- colonnes déjà utilisées par index.ts mais absentes de schema.sql (documentées ici, sans effet si présentes)
alter table profiles add column if not exists premium_niveau text;
alter table profiles add column if not exists mode           text;

create table if not exists funnel_events (
  id         bigint generated always as identity primary key,
  code       char(6) references profiles(code) on delete set null,
  event      text not null,
  meta       jsonb not null default '{}',
  created_at timestamptz not null default now()
);
create index if not exists idx_funnel_events_event on funnel_events(event, created_at);
comment on table funnel_events is 'Funnel minimal (pas d''IP / UA / email) — conservation 13 mois';

create table if not exists bilan_partages (
  token         text primary key,                             -- 192 bits aléatoires (hex 48), jamais le code élève
  code          char(6) not null references profiles(code) on delete cascade,
  diagnostic_id uuid references diagnostics(id) on delete cascade,
  type_carte    text,
  created_at    timestamptz not null default now(),
  expires_at    timestamptz not null default now() + interval '30 days',
  revoked_at    timestamptz,
  vues          integer not null default 0,
  dernier_vu_at timestamptz
);
create index if not exists idx_bilan_partages_code on bilan_partages(code);

create table if not exists consentements (
  id            bigint generated always as identity primary key,
  code          char(6) references profiles(code) on delete set null,
  produit       text not null,
  texte_version text not null,
  texte_hash    text not null,
  cases         text[] not null default '{}',
  created_at    timestamptz not null default now()             -- pas d'IP
);

-- email_logs existe déjà en prod (créée hors schema.sql) : on la documente + 2 colonnes
create table if not exists email_logs (
  id         bigint generated always as identity primary key,
  email      text not null,
  prenom     text,
  type       text not null,                                   -- J+N (legacy), D3:P-X1…, UNSUB
  statut     text,                                            -- envoyé / erreur / unsub
  details    text,
  created_at timestamptz not null default now()
);
alter table email_logs add column if not exists categorie text check (categorie in ('T','P','M'));
alter table email_logs add column if not exists code      char(6);
create index if not exists idx_email_logs_email_type on email_logs(email, type);

-- ── 8. updated_at ──
drop trigger if exists trg_competences_updated_at on competences;
create trigger trg_competences_updated_at before update on competences for each row execute function update_updated_at();
drop trigger if exists trg_items_updated_at on items;
create trigger trg_items_updated_at before update on items for each row execute function update_updated_at();
drop trigger if exists trg_maitrise_updated_at on maitrise;
create trigger trg_maitrise_updated_at before update on maitrise for each row execute function update_updated_at();
drop trigger if exists trg_diagnostics_updated_at on diagnostics;
create trigger trg_diagnostics_updated_at before update on diagnostics for each row execute function update_updated_at();

-- ── 9. RLS (l'Edge Function utilise service_role et contourne RLS ; ces règles protègent
--     un accès direct PostgREST avec un JWT élève). Écritures élève : AUCUNE (tout passe par l'API).
alter table competences enable row level security;
drop policy if exists competences_select_auth on competences;
create policy competences_select_auth on competences for select using (auth.uid() is not null);
drop policy if exists competences_admin on competences;
create policy competences_admin on competences for all using (is_admin());

-- items contient les réponses : jamais lisible par un élève (intégrité du diagnostic)
alter table items enable row level security;
drop policy if exists items_admin on items;
create policy items_admin on items for all using (is_admin());

alter table maitrise enable row level security;
drop policy if exists maitrise_select_own on maitrise;
create policy maitrise_select_own on maitrise for select using (code = my_code() or is_admin());

alter table diagnostics enable row level security;
drop policy if exists diagnostics_select_own on diagnostics;
create policy diagnostics_select_own on diagnostics for select using (code = my_code() or is_admin());

alter table reponses_items enable row level security;
drop policy if exists reponses_items_select_own on reponses_items;
create policy reponses_items_select_own on reponses_items for select using (code = my_code() or is_admin());

alter table achats enable row level security;
drop policy if exists achats_select_own on achats;
create policy achats_select_own on achats for select using (code = my_code() or is_admin());

alter table funnel_events enable row level security;
drop policy if exists funnel_events_admin on funnel_events;
create policy funnel_events_admin on funnel_events for select using (is_admin());

alter table bilan_partages enable row level security;
drop policy if exists bilan_partages_select_own on bilan_partages;
create policy bilan_partages_select_own on bilan_partages for select using (code = my_code() or is_admin());

alter table consentements enable row level security;
drop policy if exists consentements_admin on consentements;
create policy consentements_admin on consentements for select using (is_admin());

alter table email_logs enable row level security;
drop policy if exists email_logs_admin on email_logs;
create policy email_logs_admin on email_logs for all using (is_admin());

-- ════════════════════════════════════════════════════════════
--  FIN DU SCHÉMA
-- ════════════════════════════════════════════════════════════
