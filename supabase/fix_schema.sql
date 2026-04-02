-- Fixes post-création schéma — à exécuter dans SQL Editor Supabase

-- 1. Colonne password_hash pour transition auth (SHA-256 → Supabase Auth)
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS password_hash text;

-- 2. Colonne type sur contact (feedback vs contact)
ALTER TABLE contact ADD COLUMN IF NOT EXISTS type text;

-- 3. Fix dedup index scores : ajouter source (BOOST vs curriculum peuvent avoir même idx)
DROP INDEX IF EXISTS idx_scores_dedup;
CREATE UNIQUE INDEX idx_scores_dedup ON scores(code, chapitre, num_exo, date, source);

-- 4. Renommer colonnes suivi pour simplifier (Edge Function utilise chap1..chap4, boost)
ALTER TABLE suivi RENAME COLUMN nouveau_ch_1 TO chap1;
ALTER TABLE suivi RENAME COLUMN nouveau_ch_2 TO chap2;
ALTER TABLE suivi RENAME COLUMN nouveau_ch_3 TO chap3;
ALTER TABLE suivi RENAME COLUMN nouveau_ch_4 TO chap4;
ALTER TABLE suivi RENAME COLUMN prochain_boost TO boost;

-- 5. Emails : ajouter colonne subject si absente (safe)
-- Déjà dans le schéma, no-op

-- Vérification
SELECT 'fix_schema OK' as status;
