# Audit complet Matheux — 2026-03-10 21:55

## Résumé

| Scénario | Tests | ✅ | ❌ | Taux |
|----------|-------|----|----|------|
| S1 — Flux nominal complet (Alice) | 19 | 19 | 0 | 100% |
| S2 — Abandon diagnostic (Bob) | 10 | 8 | 2 | 80% |
| S3 — Abandon boost en cours (Bob) | 8 | 8 | 0 | 100% |
| S4 — Abandon chapitre en cours (Clara) | 8 | 8 | 0 | 100% |
| S5 — Reconnexions multiples sans action (Clara) | 3 | 3 | 0 | 100% |
| S6 — Comportements chaos (David) | 12 | 12 | 0 | 100% |
| S7 — Test persistance état (Emma) | 10 | 10 | 0 | 100% |
| S8 — Simulation multi-jours (Alice) | 5 | 4 | 1 | 80% |
| S9 — Injection JSON malformé (David) — cas supplémentaires | 3 | 3 | 0 | 100% |
| S10 — Charge simultanée (5 save_score parallèles) | 3 | 2 | 1 | 67% |
| S11 — Mode Admin (Nicolas) | 12 | 12 | 0 | 100% |
| **TOTAL** | **93** | **89** | **4** | **96%** |

## Détail par scénario

### S1 — Flux nominal complet (Alice)

| # | Test | Statut | Preuve |
|---|------|--------|--------|
| 01 | register Alice | ✅ |  |
| 02 | login Alice | ✅ |  |
| 03 | curriculum reçu au login | ✅ | 6 chapitres |
| 04 | generate_diagnostic OK | ✅ | 4 exos |
| 05 | save_score diagnostic (4/4) | ✅ | saved=4 |
| 06 | generate_daily_boost post-diag | ✅ |  |
| 07 | save_boost OK | ✅ |  |
| 08 | Suivi créé après login+scores | ✅ | row=present |
| 09 | Historique contient lignes Alice | ✅ | 4 lignes |
| 10 | Chapitre 1 (Fractions) : 20 exos sauvés | ✅ | 20/20 |
| 11 | Suivi Ch1 contient le nom du chapitre | ✅ | col E='Fractions' |
| 12 | Suivi Ch1 fond vert (terminé) | ✅ | bg=(217, 234, 211) |
| 13 | Suivi →Nouveau Ch1 fond rouge (vide + terminé) | ✅ | bg=(244, 204, 204) |
| 14 | Injection JSON →Nouveau Ch1 dans Suivi | ✅ | via API Sheets |
| 15 | login reçoit nextChapter après injection | ✅ | nextChapter={'categorie': 'Fractions', 'exos': [{'q': 'NouvelExo1', 'a': |
| 16 | Cellule →Nouveau Ch1 vidée après login | ✅ | val='' |
| 17 | Injection JSON →Nouveau Boost dans Suivi | ✅ | via API Sheets |
| 18 | login reçoit nextBoost après injection | ✅ | nextBoost keys=['insight', 'exos'] |
| 19 | Cellule →Nouveau Boost vidée après login | ✅ | val='' |

### S2 — Abandon diagnostic (Bob)

| # | Test | Statut | Preuve |
|---|------|--------|--------|
| 20 | register Bob | ✅ |  |
| 21 | login Bob | ✅ |  |
| 22 | generate_diagnostic reçu | ✅ | 2 exos |
| 23 | 3 scores diagnostic sauvés (abandon) | ❌ | 2/3 |
| 24 | Suivi existe malgré diagnostic incomplet | ✅ |  |
| 25 | Boost actuel = '—' (non déclenché) | ✅ | col Q='—' |
| 26 | Reconnexion Bob OK | ✅ |  |
| 27 | 3 scores CALIBRAGE conservés dans history au login | ❌ | 2 trouvés |
| 28 | Terminer diagnostic (exos restants) | ✅ | 0/0 |
| 29 | Suivi mis à jour après fin diagnostic | ✅ |  |

### S3 — Abandon boost en cours (Bob)

| # | Test | Statut | Preuve |
|---|------|--------|--------|
| 30 | generate_daily_boost Bob | ✅ |  |
| 31 | 2 exos boost sauvés puis abandon | ✅ | 2/2 |
| 32 | Suivi : boost non consommé (2/5) | ✅ | col Q='—' |
| 33 | Suivi →Nouveau Boost pas rouge (non consommé) | ✅ | bg=(255, 255, 255) |
| 34 | Reconnexion : boostExistsInDB=False (partiel, save_boost non appelé) | ✅ | boostExistsInDB=False |
| 35 | Reconnexion : dailyBoost absent (partiel) | ✅ | dailyBoost=absent |
| 36 | Date DailyBoosts modifiée → hier | ✅ | via API Sheets |
| 37 | J+1 : dailyBoost absent (date hier) | ✅ | dailyBoost=absent |

### S4 — Abandon chapitre en cours (Clara)

| # | Test | Statut | Preuve |
|---|------|--------|--------|
| 38 | register Clara | ✅ |  |
| 39 | login Clara | ✅ |  |
| 40 | 8/20 exos chapitre 1 sauvés | ✅ | 8/8 |
| 41 | Scores : 8 exos pour cat1 | ✅ | 8 exos dans Scores |
| 42 | Reconnexion : 8 scores conservés | ✅ | 8 trouvés |
| 43 | 12 exos restants sauvés → chapitre terminé | ✅ | 12/12 |
| 44 | Suivi Ch1 vert (20/20 terminé) | ✅ | bg=(217, 234, 211) |
| 45 | Suivi →Nouveau Ch1 rouge (action requise) | ✅ | bg=(244, 204, 204) |

### S5 — Reconnexions multiples sans action (Clara)

| # | Test | Statut | Preuve |
|---|------|--------|--------|
| 46 | 5 logins consécutifs tous OK | ✅ | 5/5 |
| 47 | Pas de doublons dans Suivi (1 seule ligne) | ✅ | 1 ligne(s) |
| 48 | Scores stables (pas de doublons) | ✅ | 20 scores (attendu 20) |

### S6 — Comportements chaos (David)

| # | Test | Statut | Preuve |
|---|------|--------|--------|
| 49 | register David | ✅ |  |
| 50 | login David | ✅ |  |
| 51 | save_score chapitre inexistant → pas de crash | ✅ | status=success |
| 52 | save_boost sans boost → pas de crash | ✅ | status=success |
| 53 | 3x generate_daily_boost → pas de crash | ✅ | 3/3 OK |
| 54 | login mauvais mdp → erreur propre | ✅ | msg=Email ou mot de passe incorrect. |
| 55 | register email existant → erreur propre | ✅ | msg=Un compte existe déjà avec cet email. |
| 56 | login avec JSON malformé dans Suivi → pas de crash | ✅ | status=success, nextChapter={'categorie': 'PENDING_MANUAL', 'exos': [], 'insight |
| 57 | Login JSON malformé → PENDING_MANUAL retourné | ✅ | nextChapter={'categorie': 'PENDING_MANUAL', 'exos': [], 'insight': 'Ton prof pré |
| 58 | login avec cellule vide → nextChapter=null | ✅ | nextChapter=None |
| 59 | login avec texte non-JSON → nextChapter acceptable (fallback) | ✅ | nextChapter={'categorie': 'PENDING_MANUAL', 'exos': [], 'insight': 'Ton prof pré |
| 60 | Login texte non-JSON → PENDING_MANUAL retourné | ✅ | nextChapter={'categorie': 'PENDING_MANUAL', 'exos': [], 'insight': 'Ton prof pré |

### S7 — Test persistance état (Emma)

| # | Test | Statut | Preuve |
|---|------|--------|--------|
| 61 | register Emma | ✅ |  |
| 62 | login Emma | ✅ |  |
| 63 | 10/20 exos chapitre 1 sauvés | ✅ | 10/10 |
| 64 | Reconnexion : 10 scores conservés | ✅ | 10 trouvés |
| 65 | generate_daily_boost OK | ✅ | 5 exos |
| 66 | Reconnexion après abandon boost : boostExistsInDB=False | ✅ | boostExistsInDB=False |
| 67 | 10 exos restants → chapitre terminé | ✅ | 10/10 |
| 68 | login Emma reçoit nextChapter injecté | ✅ | nextChapter type=dict |
| 69 | 3 exos nouveau chapitre sauvés | ✅ | 3/3 |
| 70 | Reconnexion : 23 scores cat1 conservés (10+10+3) | ✅ | 23 scores cat1 |

### S8 — Simulation multi-jours (Alice)

| # | Test | Statut | Preuve |
|---|------|--------|--------|
| 71 | DailyBoosts date Alice → hier | ✅ |  |
| 72 | J+1 : boostExistsInDB=False (boost expiré) | ✅ | val=False |
| 73 | Suivi : boost actuel cohérent | ✅ | col Q='—' |
| 74 | Nouveau boost généré + sauvé (J+1) | ✅ |  |
| 75 | J+1 : dailyBoost présent après regénération | ❌ | val=False |

### S9 — Injection JSON malformé (David) — cas supplémentaires

| # | Test | Statut | Preuve |
|---|------|--------|--------|
| 76 | JSON sans clé 'exos' → nextChapter=null, string ou PENDING_MANUAL | ✅ | nextChapter={'categorie': 'PENDING_MANUAL', 'exos': [], 'insight': 'Ton prof pré |
| 77 | JSON exos=[] → login OK sans crash | ✅ | status=success, nextChapter={'categorie': 'PENDING_MANUAL', 'exos': [], 'insight |
| 78 | Boost malformé → nextBoost=null, login OK | ✅ | nextBoost=None |

### S10 — Charge simultanée (5 save_score parallèles)

| # | Test | Statut | Preuve |
|---|------|--------|--------|
| 79 | 5 save_score parallèles → 5 lignes Scores ajoutées | ❌ | 4 lignes ajoutées |
| 80 | Pas de doublons (idxs uniques) | ✅ | idxs=[1, 2, 4, 5] |
| 81 | Suivi cohérent après charge parallèle | ✅ |  |

### S11 — Mode Admin (Nicolas)

| # | Test | Statut | Preuve |
|---|------|--------|--------|
| 82 | get_admin_overview avec code admin | ✅ | status=success, msg= |
| 83 | Overview retourne une liste d'élèves | ✅ | 36 élèves |
| 84 | Structure élève complète (code, prenom, action, chapitresDetail) | ✅ | champs présents: ['code', 'prenom', 'action', 'chapitresDetail'] |
| 85 | get_admin_overview code invalide → accès refusé | ✅ | status=error, msg=Accès refusé. |
| 86 | chapitresDetail rempli pour Emma (a fait des exos) | ✅ | detail=1 chap(s) |
| 87 | publish_admin_boost pour Emma → succès | ✅ | status=success, msg=Boost publié. L'élève le recevra à son prochain login. |
| 88 | Suivi Emma : →Nouveau Boost rempli après publish | ✅ | col S='{"insight":"Boost admin test","exos":[{"q":"Exo boost 1","a"' |
| 89 | Emma login → reçoit nextBoost publié par admin | ✅ | nextBoost.exos=5 |
| 90 | Suivi Emma : →Nouveau Boost vidé après login (injecté) | ✅ | col S='' |
| 91 | publish_admin_chapter pour Alice → succès | ✅ | status=success, msg=Chapitre "Fractions" publié. L'élève le recevra à son procha |
| 92 | Alice login → reçoit nextChapter publié par admin | ✅ | nextChapter.categorie=Fractions, exos=20 |
| 93 | Dashboard trié : non-RAS avant RAS | ✅ | 24 non-RAS, 12 RAS |

## Bugs trouvés

_Aucun bug détecté._

## Verdict final

**Score : 89/93**

**⚠️ 4 test(s) échoué(s) — corriger avant lancement**

> ⚠️ Comptes @audit.fr CONSERVÉS comme preuves (nettoyage manuel requis)