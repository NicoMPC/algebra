-- ════════════════════════════════════════════════════════════
--  Migration : Refonte « Diagnostic 3e » (moteur adaptatif)
--  Date : 2026-09-24 · Spec : docs/specs/20-moteur.md · Contrat : docs/specs/00-contrat-commun.md
--  100 % ADDITIVE : aucune table existante supprimée ni modifiée de façon destructive
--  (seulement ADD COLUMN IF NOT EXISTS). Rejouable (IF NOT EXISTS partout).
--  Le nettoyage des anciens comptes est un script séparé : supabase/purge_anciens_comptes.sql
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
