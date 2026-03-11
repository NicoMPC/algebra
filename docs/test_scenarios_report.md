# Rapport test_scenarios.py
Date : 2026-03-11

## ✅ S-E1 · Première inscription + diagnostic
**7/7 assertions OK**


## ✅ S-E3 · Chapitre 20 exercices (persitance + badge demain)
**5/5 assertions OK**


## ✅ S-E4 · Boost quotidien (generate + save + boostConsumed)
**6/6 assertions OK**


## ❌ S-A1/A2 · Login admin + get_admin_overview
**0/5 assertions OK**

- ❌ #19 login admin retourne status:success
  - Proof: `Email ou mot de passe incorrect.`
- ❌ #20 isAdmin=True retourné
  - Proof: ``
- ❌ #21 get_admin_overview retourne status:success
  - Proof: `Accès refusé.`
- ❌ #22 students list retournée (tableau)
  - Proof: `type=<class 'NoneType'>`
- ❌ #23 au moins 1 élève dans la liste
  - Proof: `len=0`

## ❌ S-A5 · Publish admin boost → réception au login élève
**3/7 assertions OK**

- ❌ #26 login admin pour publish
  - Proof: `Email ou mot de passe incorrect.`
- ❌ #27 publish_admin_boost retourne status:success
  - Proof: `Accès refusé.`
- ❌ #29 nextBoost injecté avec insight
  - Proof: `{}`
- ❌ #30 nextBoost contient 5 exos
  - Proof: `len=0`

## ✅ S-A8 · Guards : JSON invalide, accès refusé, email dupliqué
**7/7 assertions OK**


