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
--  FIN DU SCHÉMA
-- ════════════════════════════════════════════════════════════
