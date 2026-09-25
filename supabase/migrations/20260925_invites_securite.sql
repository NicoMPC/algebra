-- ════════════════════════════════════════════════════════════
--  Migration : diagnostic express invité + sécurité des actions élève (Besoins API n°1, 7, 8)
--  Date : 2026-09-25 · Spec : docs/specs/20-moteur.md §8 bis · Journal : docs/specs/41-integration-log.md
--  100 % ADDITIVE, rejouable (IF NOT EXISTS partout). Aucune table existante modifiée de façon
--  destructive : diagnostics.code reste NOT NULL, la session invitée vit dans sa propre table.
-- ════════════════════════════════════════════════════════════

-- ── 1. DIAGNOSTICS_INVITES : diagnostic express passé AVANT la création du compte ──
-- La carte partielle s'affiche avant l'inscription (contrat §7). Le jeton invité (192 bits) n'est jamais
-- stocké en clair : seulement son SHA-256. Au register, la session est recopiée dans `diagnostics`
-- (avec le code élève), les observations sont rejouées dans maitrise / reponses_items, puis la copie
-- invitée est vidée (etat_json, carte_json, prenom = null : minimisation RGPD).
create table if not exists diagnostics_invites (
  id               uuid primary key default gen_random_uuid(),
  guest_token_hash text not null,                                -- sha256(guest_token), hex
  type             text not null default 'express' check (type in ('express')),
  statut           text not null default 'en_cours' check (statut in ('en_cours','termine','rattache')),
  prenom           text,                                         -- facultatif, pour la carte invitée
  etat_json        jsonb,                                        -- état du moteur (null après rattachement)
  carte_json       jsonb,                                        -- carte express (null après rattachement)
  n_questions      integer not null default 0,
  code             char(6) references profiles(code) on delete set null,  -- compte rattaché
  diagnostic_id    uuid references diagnostics(id) on delete set null,     -- diagnostic créé au rattachement
  expires_at       timestamptz not null default now() + interval '2 days', -- prolongé de 2 j à la fin du diag
  started_at       timestamptz not null default now(),
  finished_at      timestamptz,
  rattache_at      timestamptz,
  updated_at       timestamptz not null default now()
);
create index if not exists idx_diagnostics_invites_expires on diagnostics_invites(statut, expires_at);
comment on table diagnostics_invites is 'Diagnostic express invité (sans compte), jeton hashé, expire en 2 j ; purge : delete where statut <> ''rattache'' and expires_at < now() - interval ''7 days''';

drop trigger if exists trg_diagnostics_invites_updated_at on diagnostics_invites;
create trigger trg_diagnostics_invites_updated_at before update on diagnostics_invites for each row execute function update_updated_at();

-- RLS : aucune lecture élève (l'Edge Function passe par service_role). Admin seulement.
alter table diagnostics_invites enable row level security;
drop policy if exists diagnostics_invites_admin on diagnostics_invites;
create policy diagnostics_invites_admin on diagnostics_invites for select using (is_admin());

-- ── 2. BILAN_PARTAGES.canal : d'où vient le lien ──
-- 'email_parent' = lien du mail P-X0 envoyé au parent : il sert aussi de preuve pour confirm_parent.
-- Jamais créé depuis l'app (create_share remplace 'email_parent' par 'app').
alter table bilan_partages add column if not exists canal text;
