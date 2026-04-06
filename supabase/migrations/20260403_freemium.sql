-- ════════════════════════════════════════════════════════════
--  Migration : Trial 7j → Freemium (1 chapitre gratuit)
--  Date : 2026-04-03
-- ════════════════════════════════════════════════════════════

-- 1. Ajouter colonne free_chapter (chapitre gratuit identifié par le diagnostic)
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS free_chapter text;

-- 2. Migrer les élèves existants → premium (early adopters)
UPDATE profiles SET premium = true, premium_end = '2026-06-30' WHERE is_test = false AND is_admin = false;

-- 3. Vérifier
-- SELECT code, prenom, premium, premium_end, free_chapter FROM profiles WHERE is_test = false;
