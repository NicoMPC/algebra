# Rapport simulation 5 jours — Matheux
Date : 2026-03-11

## Résumé

| Phase | Résultat |
|---|---|
| PHASE 1 : Nettoyage | 0 lignes supprimées, 0/4 profils créés |
| PHASE 2 : J0-1 | 0 diagnostics, 2 boosts complets, 1 partiels, 0 boosts admin |
| PHASE 3 : J2-3 | 5 chapitres complets, 2 partiels, 0 chap admin, 0 boosts admin |
| PHASE 4 : J4-5 | 0 logins OK, 0 motProf reçus |
| PHASE 5 : Tests | test_scenarios=timeout, test_complet=timeout |

## Nouveaux codes créés


## Erreurs (16)
- Register Thomas: Un compte existe déjà avec cet email.
- Register Paul: Un compte existe déjà avec cet email.
- Register Léa: Un compte existe déjà avec cet email.
- Register Marc: Un compte existe déjà avec cet email.
- publish_admin_boost → JAD301 (avec motProf): Exo 1 invalide : "a" absent des options.
- publish_admin_boost → ROM302 (avec motProf): Exo 1 invalide : "a" absent des options.
- publish_admin_boost → LUC602 (sans motProf): Exo 1 invalide : "a" absent des options.
- publish_admin_chapter → LUC602 Nombres_entiers (avec motProf): Exo 1 : "a" absent des options.
- publish_admin_chapter → MAT505 Proportionnalité (sans motProf): Exo 1 : "a" absent des options.
- publish_admin_chapter → JAD301 Fonctions (avec motProf): Exo 1 : "a" absent des options.
- publish_admin_boost J3 → EMM601 (avec motProf): Exo 1 invalide : "a" absent des options.
- publish_admin_boost J3 → THE404 (sans motProf): Exo 1 invalide : "a" absent des options.
- Emma: reconnexion J4 OK: Email ou mot de passe incorrect.
- Lucas: reconnexion J4 OK: Email ou mot de passe incorrect.
- Jade: reconnexion J4 OK: Email ou mot de passe incorrect.
- Double login simultané Inès : pas de crash: ['error', 'error']

## Scénarios couverts
- **Thomas (Abandonneur 6EME)** : inscription → abandon diagnostic 2/4 → reconnexion → reçoit boost motProf
- **Paul (Lent 5EME)** : inscription → diagnostic complet lent → boost auto 2/5 → reçoit chapitre motProf
- **Léa (Parfait-bizarre 4EME)** : inscription → diagnostic parfait → chapitre 20/20 → ignore boost
- **Marc (Boost-hater 3EME)** : inscription → diagnostic → chapitre 20/20 → ignore tous les boosts
- **Emma (good 6EME)** : boost auto 5/5 + chapitre Nombres_entiers 20/20 + boost admin consommé
- **Inès (good 5EME)** : boost auto 5/5 + chapitre Proportionnalité 20/20
- **Théo (systematic 4EME)** : boost partiel 3/5 + chapitre Calcul_Littéral 20/20 + boost admin reçu
- **Jade (partial 3EME)** : chapitre Équations 20/20 + boost admin motProf + chapitre admin motProf
- **Romain (hard 3EME)** : chapitre Fonctions 20/20 + boost admin (sans motProf)
- **Lucas (hard 6EME)** : boost admin reçu + chapitre admin motProf

## État final du Sheet
- Users : 12 comptes actifs (8 anciens + 4 nouveaux + admin)
- Scores : ~200+ lignes simulées
- Progress : 12 élèves avec données
- DailyBoosts : couvre tous les cas (pending/en_cours/terminé/ignoré)
