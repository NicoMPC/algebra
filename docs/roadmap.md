# Roadmap Matheux — ce qui reste à faire

> **Source unique** des tâches restantes. Mise à jour : 26/09/2026.
> Chaque ligne : qui · quoi · pourquoi · où est le détail. Cocher (`✅`) et dater quand c'est fait.
> État détaillé de la dernière session : `docs/specs/REPRISE.md`. Règles du projet : `CLAUDE.md`.

## Où on en est (26/09/2026)

Le **nouveau matheux.fr est en ligne** : diagnostic express gratuit → carte → séance du jour adaptative
(5 exos) → diagnostic complet payant (19 €) + bilan PDF parent → Programme Brevet (49 €). Base prod
migrée, 1 598 exercices, emails automatiques actifs, API sécurisée. Parcours réel vérifié en prod.

## 🔴 Maintenant (bloquant pour vendre le Programme / publier)

| # | Qui | Quoi | Détail |
|---|---|---|---|
| 1 | Nicolas | **Pousser les derniers commits** (SEO, emails, légal, QA) après relecture : terminal normal (Ctrl+Alt+T), sans `!` : `cd /home/liline/Bureau/projets/matheux && git push origin HEAD:main` | Claude vérifie ensuite en ligne |
| 2 | Nicolas | **Stripe : créer les liens 49 € et 30 €** (pas-à-pas clic par clic dans l'agenda) puis donner les 2 URL à Claude | `docs/specs/REPRISE.md` §Reste à faire, agenda |
| 3 | Claude | Brancher les 2 URL dans `OFFRE` (`app.html`, `bilan.html`), tester, faire pousser | — |
| 4 | Nicolas + Claude | **Vérifier le webhook Stripe** (endpoint = Edge Function, `checkout.session.completed`) puis **1 vrai paiement 19 €** à rembourser → accès débloqué + email | Claude lit Stripe en lecture seule via Chrome |
| 5 | Nicolas | **Supprimer les anciens comptes** + le compte de test « Zoé » (script prêt, testé à blanc) — terminal normal : `cd /tmp && npx supabase db query --linked --project-ref xlfzhcanzmqqlxtavzrd -f /home/liline/Bureau/projets/matheux-backup-prod-2026-09-26/purge_anciens_comptes_COMMIT.sql` | Sauvegarde dans le même dossier |

## 🟠 Cette semaine (qualité, confiance, visibilité)

| # | Qui | Quoi | Détail |
|---|---|---|---|
| 6 | Nicolas | **DMARC** : remplacer le CNAME IONOS par un TXT avec `rua` (délivrabilité des emails) | `docs/specs/53-audit-emails.md` §5 |
| 7 | Nicolas | **Google Search Console** (propriété Domaine, TXT IONOS, sitemap) + Bing Webmaster (~30 min) | `docs/specs/70-seo.md` §6 |
| 8 | Nicolas | **Relecture juriste** : CGV/CGU/confidentialité (qualification des produits, parent contractant, achat = confirmation parentale, garantie, prorata) | `docs/specs/52-legal.md` §« ✅ Appliqué le 26/09 » |
| 9 | Nicolas | **Médiateur de la consommation** : obligation légale (L612-1), refusé pour l'instant — à souscrire dès les premières ventes | `cgv.html` art. 11 (TODO) |
| 10 | Nicolas | Vérifier SIRET / adresse dans les mentions légales, compléter hébergeurs | `docs/specs/52-legal.md` |
| 11 | Claude | Expéditeur `nicolas@matheux.fr` au lieu de no-reply ; bounces/plaintes Resend = désinscription | `53-audit-emails.md` §4 |
| 12 | Nicolas | Archiver les 5 anciens liens Stripe à 29,99 € | Stripe → Liens de paiement |

## 🟡 Ce mois-ci (produit)

| # | Qui | Quoi | Détail |
|---|---|---|---|
| 13 | Claude | **Purges de conservation automatiques** promises par la politique de confidentialité (comptes non confirmés J+30, inactifs 12 mois, logs) — 1re échéance ~24/10 | `52-legal.md` §5 |
| 14 | Claude | Email saisonnier de décembre (S-DEC) avant le 30/11 ; trous de séquence (réactivation, fin de programme) | `53-audit-emails.md` §4 |
| 15 | Claude | Compteur **réel** de diagnostics sur la landing (affiché à partir d'un seuil) — pas de faux chiffre | décision Nicolas en attente |
| 16 | Claude | Mise à jour mensuelle SEO : 5 pages notions à écrire, calendrier éditorial | `70-seo.md` §7 |
| 17 | Claude | Rendu de courbes/diagrammes dans l'app (items DF décrits en texte aujourd'hui) | `00-contrat-commun.md` §8 |

## 🟢 Plus tard / décisions

- Brevets blancs (annoncés « en cours d'année ») — à planifier avant janvier (brevets blancs des collèges).
- Re-test pour les acheteurs du seul diagnostic : décider (offrir, vendre, ou rien).
- Réassort de la banque : l'agent `admin-auto` quand le moteur signale `banque_insuffisante` ou chaque mois.
- 2 erreurs types NC.LIT.01 proposées par le relecteur (`#relation_inversee`, `#parentheses_superflues`).
- Photo du fondateur sur la landing (initiales aujourd'hui).
- Réécrire l'historique git pour purger les anciennes données perso (restent dans l'historique du dépôt public), ou passer le dépôt en privé si GitHub Pages le permet sur l'offre.
- `docs/` est servi publiquement par GitHub Pages (exclu du crawl) : sortir les specs du dépôt public si besoin.

## ✅ Fait (récent)

- 26/09 — Bascule prod : sauvegarde, 4 migrations, secrets + cron, import 1 598 exos, nouvelle API, **site en ligne**, e2e réel OK.
- 26/09 — SEO (9 nouvelles pages, 8 réécrites, technique), audit + corrections emails, pages légales à jour, QA multi-profils.
- 25/09 — Sécurité prod (actions admin/emails protégées), RGPD (données perso retirées du dépôt), lien Stripe 19 €.
- 24-25/09 — Refonte complète « Diagnostic 3e » : référentiel, banque relue, moteur adaptatif, app, landing, PDF, emails.
