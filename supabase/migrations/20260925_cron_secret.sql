-- ════════════════════════════════════════════════════════════
--  Migration : cron emails authentifié (Besoin API n°8, 25/09/2026)
--  Avant : l'action cron_send_emails était publique (n'importe qui pouvait déclencher l'envoi de la
--  séquence). Désormais elle exige `cron_secret` = secret Edge Function CRON_SECRET (ou un admin connecté).
--  À faire UNE FOIS au déploiement (Nicolas), dans cet ordre :
--    1. openssl rand -hex 32                                  → le secret (ne pas le committer)
--    2. npx supabase secrets set CRON_SECRET=<secret> --project-ref xlfzhcanzmqqlxtavzrd
--    3. SQL Editor : select vault.create_secret('<secret>', 'matheux_cron_secret');
--    4. exécuter ce fichier (re-planifie le job en lisant le secret dans Vault, jamais en clair ici)
--  Sans les étapes 1-3, le cron est refusé (fail-closed) : aucun email automatique ne part.
-- ════════════════════════════════════════════════════════════

DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM cron.job WHERE jobname = 'matheux-daily-emails') THEN
    PERFORM cron.unschedule('matheux-daily-emails');
  END IF;
END $$;

SELECT cron.schedule(
  'matheux-daily-emails',
  '0 7 * * *',
  $$
  SELECT net.http_post(
    url := 'https://xlfzhcanzmqqlxtavzrd.supabase.co/functions/v1/api',
    headers := jsonb_build_object('Content-Type', 'application/json'),
    body := jsonb_build_object(
      'action', 'cron_send_emails',
      'cron_secret', (SELECT decrypted_secret FROM vault.decrypted_secrets WHERE name = 'matheux_cron_secret' LIMIT 1)
    )
  );
  $$
);
