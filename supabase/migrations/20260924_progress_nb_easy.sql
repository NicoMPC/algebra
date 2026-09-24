-- ════════════════════════════════════════════════════════════
--  Migration : progress.nb_easy (colonne lue/écrite par index.ts depuis la migration Supabase
--  — updateConfidenceScore, save_scores_batch — mais absente de schema.sql).
--  Trouvé par le backend de dev local (dev/, 24/09/2026) : sans elle, PostgREST rejette
--  select/insert/update de progress (PGRST204/42703) et `progress` ne se remplit jamais.
--  100 % additive, rejouable. RLS : inchangée (table progress existante).
-- ════════════════════════════════════════════════════════════
alter table progress add column if not exists nb_easy integer not null default 0;
