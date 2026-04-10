-- Migration 2026-04-10 : activer pg_cron + schedule daily emails
-- À exécuter UNE SEULE FOIS dans Supabase Dashboard → SQL Editor.
--
-- Prérequis : activer l'extension pg_cron depuis Database → Extensions.
-- pg_net est déjà disponible dans Supabase par défaut.
--
-- Horaire : 7h00 UTC = 9h00 Europe/Paris (heure d'été).
-- L'appel POST { action: "cron_send_emails" } déclenche cronSendEmails dans l'Edge Function.
-- La fonction itère les profils, calcule diffDays, envoie J+1/3/7/14 + dédup via email_logs.

CREATE EXTENSION IF NOT EXISTS pg_cron;
CREATE EXTENSION IF NOT EXISTS pg_net;

-- Supprimer l'ancien job s'il existe (idempotent)
DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM cron.job WHERE jobname = 'matheux-daily-emails') THEN
    PERFORM cron.unschedule('matheux-daily-emails');
  END IF;
END $$;

-- Planifier l'appel quotidien à 7h00 UTC (9h00 Paris en heure d'été)
SELECT cron.schedule(
  'matheux-daily-emails',
  '0 7 * * *',
  $$
  SELECT net.http_post(
    url := 'https://xlfzhcanzmqqlxtavzrd.supabase.co/functions/v1/api',
    headers := jsonb_build_object('Content-Type', 'application/json'),
    body := jsonb_build_object('action', 'cron_send_emails')
  );
  $$
);

-- Vérification :
-- SELECT jobname, schedule, command FROM cron.job WHERE jobname = 'matheux-daily-emails';
-- SELECT * FROM cron.job_run_details WHERE jobid IN (SELECT jobid FROM cron.job WHERE jobname = 'matheux-daily-emails') ORDER BY start_time DESC LIMIT 5;
