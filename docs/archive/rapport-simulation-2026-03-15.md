# Rapport de simulation — 2026-03-15 11:51

## Résumé exécutif
- Profils créés : 10/10
- Scénarios OK : 10/10
- Frictions identifiées : 3
- Bugs critiques : 1
- Durée totale : 12min 47s
- Appels GAS : 111

## Résultats par profil

| Profil | Scénario | Statut | Frictions |
|--------|----------|--------|-----------|
| SIM01 - Lucas 6EME | parcours_complet | ✅ | — |
| SIM02 - Emma 5EME | j3_email_due | ✅ | — |
| SIM03 - Hugo 4EME | j7_conversion | ✅ | — |
| SIM04 - Lea 3EME | boost_complete | ✅ | — |
| SIM05 - Nathan 6EME | chapitre_termine | ✅ | — |
| SIM06 - Chloe 1ERE | inactif | ✅ | — |
| SIM07 - Tom 3EME | brevet_pending | ✅ | [SIM07] pendingBrevet absent au login après publish |
| SIM08 - Sofia 5EME | cours_milestone | ✅ | — |
| SIM09 - Remi 4EME | boost_en_cours | ✅ | — |
| SIM10 - Jade 6EME | j5_email_due | ✅ | — |

## Frictions détaillées

### 🔴 Bugs critiques (bloquants)
1. get_admin_overview échoué: {'status': 'error', 'message': 'Erreur serveur : ReferenceError: ss is not defined'}

### 🟡 Incohérences (non bloquantes)
1. [SIM07] pendingBrevet absent au login après publish
2. save_score avec code inexistant accepté → {'status': 'success', 'streakAlert': False}

### 🟢 Comportements vérifiés OK
1. SIM01 inscription OK → UJXXZB
2. SIM01 diagnostic OK — 2 exos
3. SIM01 boost OK — 5 exos
4. SIM01 boostExosDone=5 après 5 scores
5. SIM02 inscription OK → KX7R9G
6. SIM02 diagnostic OK — 4 exos
7. SIM02 boost OK — 5 exos
8. SIM03 inscription OK → VNDC8J
9. SIM03 diagnostic OK — 20 exos
10. SIM03 boost OK — 5 exos
11. SIM04 inscription OK → V76FEQ
12. SIM04 diagnostic OK — 22 exos
13. SIM04 boost OK — 5 exos
14. SIM05 inscription OK → Z5XDE2
15. SIM05 diagnostic OK — 4 exos
16. SIM05 boost OK — 5 exos
17. SIM06 inscription OK → HUP9ML
18. SIM06 diagnostic OK — 4 exos
19. SIM06 boost OK — 5 exos
20. SIM07 inscription OK → ZY9CXS
21. SIM07 diagnostic OK — 22 exos
22. SIM07 boost OK — 5 exos
23. SIM07 brevet publié
24. SIM08 inscription OK → WC9K9K
25. SIM08 diagnostic OK — 2 exos
26. SIM08 boost OK — 5 exos
27. SIM09 inscription OK → PQMPLW
28. SIM09 diagnostic OK — 2 exos
29. SIM09 boost OK — 5 exos
30. SIM10 inscription OK → JEHPK6
31. SIM10 diagnostic OK — 2 exos
32. SIM10 boost OK — 5 exos
33. Users: 10/10 profils trouvés avec IsTest=1
34. Scores: 69 lignes pour 10 profils sim
35. DailyBoosts: 10 entrées sim
36. Progress: SIM05 entrée trouvée
37. Double inscription rejetée
38. Mauvais MDP rejeté
39. Exo invalide (a absent) rejeté
40. Admin sans code rejeté
41. SIM01 J+0 email loggé
42. SIM02 log_manual_email OK
43. SIM03 log_manual_email OK
44. SIM10 log_manual_email OK

## Cohérence des données Sheets

| Onglet | Vérification | Résultat |
|--------|-------------|---------|
| Users | 10 lignes IsTest=1 | ✅ |
| Scores | 69 scores cohérents | ✅ |
| DailyBoosts | 10 entrées | ✅ |
| Progress | SIM05 présent | ✅ |
| 📧 Emails | Vérifié | ✅ |

## Tests edge cases

| Test | Attendu | Reçu | OK? |
|------|---------|------|-----|
| Double inscription | error | error | ✅ |
| Mauvais MDP | error | error | ✅ |
| Code inexistant | error | success | ❌ |
| Exos invalides | error | error | ✅ |
| Admin sans code | error | error | ✅ |

## État des profils après simulation
(pour inspection manuelle dans l'admin panel)

| Code | Profil | État admin attendu |
|------|--------|-------------------|
| UJXXZB | SIM01 Lucas | Élève standard J0 — tout le workflow de bienvenue |
| KX7R9G | SIM02 Emma | J+3 — email de relance doit apparaître dans admin |
| VNDC8J | SIM03 Hugo | J+7 — email de conversion avec lien Stripe |
| V76FEQ | SIM04 Lea | Boost terminé → action admin déclenchée |
| Z5XDE2 | SIM05 Nathan | Chapitre terminé (20 exos) → action admin |
| HUP9ML | SIM06 Chloe | Inactif >7j → statut "Sans nouvelles" dans admin |
| ZY9CXS | SIM07 Tom | Brevet blanc publié → visible côté élève au login |
| WC9K9K | SIM08 Sofia | Milestone 5 exos → cours disponible ou "en préparation" |
| PQMPLW | SIM09 Remi | Boost en cours 2/5 → admin voit "En cours" pas "Terminé" |
| JEHPK6 | SIM10 Jade | J+5 — email urgence avant fin de trial |

## Recommandations
### Priorité haute
- **FIX** get_admin_overview échoué: {'status': 'error', 'message': 'Erreur serveur : ReferenceError: ss is not defined'}
### Priorité moyenne
- [SIM07] pendingBrevet absent au login après publish
- save_score avec code inexistant accepté → {'status': 'success', 'streakAlert': False}
