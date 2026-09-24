-- ════════════════════════════════════════════════════════════
--  PURGE DES ANCIENS COMPTES ÉLÈVES — décision Nicolas du 24/09/2026 (contrat §7)
--  ⛔ NE PAS EXÉCUTER sans Nicolas, au moment du déploiement de la refonte, APRÈS la migration
--     20260924_diagnostic_3e.sql. Épargne tous les admins (dont KN6CFG).
--
--  Étape 0 (hors SQL, recommandée) : export complet chiffré de la base avant tout :
--     pg_dump "$SUPABASE_DB_URL" --no-owner -Fc -f backup_matheux_20260924.dump
--     gpg -c backup_matheux_20260924.dump && rm backup_matheux_20260924.dump
--  Puis supprimer ce backup à une date fixée (ex. +3 mois), sinon la suppression RGPD n'en est pas
--  une (52-legal.md §5). Idem : Google Sheet legacy, clients Stripe, exports locaux.
--
--  Étape 1 (ci-dessous) : snapshot dans le schéma `backup_20260924` (non exposé à l'API),
--  puis suppression dans une transaction unique. Vérifier les compteurs avant COMMIT.
-- ════════════════════════════════════════════════════════════

begin;

-- ── 0. Garde-fou : l'admin doit exister, sinon on arrête tout ──
do $$
begin
  if not exists (select 1 from public.profiles where code = 'KN6CFG' and is_admin) then
    raise exception 'Compte admin KN6CFG introuvable ou non admin — purge annulée';
  end if;
end $$;

-- ── 1. Backup (snapshot) ──
create schema if not exists backup_20260924;
revoke all on schema backup_20260924 from public, anon, authenticated;

create table backup_20260924.profiles       as select * from public.profiles;
create table backup_20260924.scores         as select * from public.scores;
create table backup_20260924.progress       as select * from public.progress;
create table backup_20260924.daily_boosts   as select * from public.daily_boosts;
create table backup_20260924.suivi          as select * from public.suivi;
create table backup_20260924.brevet_results as select * from public.brevet_results;
create table backup_20260924.insights       as select * from public.insights;
create table backup_20260924.emails         as select * from public.emails;
create table backup_20260924.email_logs     as select * from public.email_logs;
create table backup_20260924.contact        as select * from public.contact;
create table backup_20260924.auth_users     as select id, email, created_at, last_sign_in_at from auth.users;

-- ── 2. Périmètre : tous les profils non admin ──
create temporary table purge_cible on commit drop as
  select id, code, email from public.profiles where not is_admin and code <> 'KN6CFG';

-- Aperçu à relire avant COMMIT
select (select count(*) from purge_cible) as profils_a_supprimer,
       (select count(*) from public.profiles where is_admin) as admins_conserves;

-- ── 3. Données élèves (explicite, même si la plupart des FK sont en cascade) ──
delete from public.scores          where code in (select code from purge_cible);
delete from public.progress        where code in (select code from purge_cible);
delete from public.daily_boosts    where code in (select code from purge_cible);
delete from public.suivi           where code in (select code from purge_cible);
delete from public.brevet_results  where code in (select code from purge_cible);
delete from public.insights        where code in (select code from purge_cible);
-- tables de la refonte (normalement vides à ce stade)
delete from public.maitrise        where code in (select code from purge_cible);
delete from public.reponses_items  where code in (select code from purge_cible);
delete from public.diagnostics     where code in (select code from purge_cible);
delete from public.bilan_partages  where code in (select code from purge_cible);
delete from public.funnel_events   where code in (select code from purge_cible);
delete from public.consentements   where code in (select code from purge_cible);

-- Emails : on supprime l'historique des adresses purgées, MAIS on garde les désinscriptions
-- (liste d'opposition : ne jamais recontacter quelqu'un qui s'est désinscrit).
delete from public.email_logs where email in (select email from purge_cible) and type <> 'UNSUB';
delete from public.emails     where email in (select email from purge_cible) and type <> 'UNSUB';
delete from public.contact    where email in (select email from purge_cible);

-- ── 4. Comptes : auth.users (cascade → profiles), puis profils orphelins éventuels ──
delete from auth.users where id in (select id from purge_cible);
delete from public.profiles where code in (select code from purge_cible);

-- ── 5. Contrôles ──
select (select count(*) from public.profiles) as profils_restants,
       (select count(*) from public.profiles where not is_admin) as non_admins_restants,  -- attendu : 0
       (select count(*) from public.scores)   as scores_restants;

-- SÉCURITÉ : le script se termine par ROLLBACK (une exécution « à l'aveugle » ne supprime rien).
-- Relire les compteurs ci-dessus, puis remplacer la ligne suivante par COMMIT et relancer.
rollback;

-- ── Plus tard (date à fixer, ex. +3 mois) : supprimer le snapshot ──
-- drop schema backup_20260924 cascade;
