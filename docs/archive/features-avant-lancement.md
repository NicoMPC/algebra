# Features avant lancement — Matheux

> Dernière mise à jour : 9 mars 2026. Réponse honnête à : "Qu'est-ce qui doit encore être fait avant le premier vrai lancement public ?"

---

## 1. Audit des features existantes

| Feature | Statut actuel | Impact conversion free→payant | À corriger avant lancement ? |
|---|---|---|---|
| Mode "Contrôle demain" | Implémenté (GAS + front) | Fort — déclencheur d'urgence, forte valeur perçue | Non, mais tester le flux bout en bout sur mobile |
| Rapport parents | Fondateur uniquement (email interne) | Fort — les parents paient, pas les élèves | Oui — au moins un email automatique au parent après 7 jours d'essai |
| Mode "Préparation Brevet" | Non implémenté | Moyen — différenciant mais pas déclencheur d'achat immédiat | Non — à reporter après 50 clients |
| Classements / badges | XP + streak + mastery ring côté front | Faible à court terme — plaisant mais ne justifie pas un paiement | Non — ne pas toucher |
| Vue Progression | Implémentée (barres de confiance, dates, statuts) | Moyen — rassure les parents si on leur montre | Non — fonctionnelle, suffisante au lancement |
| Notification "Reviens faire ton boost" | Non implémentée | Fort sur la rétention — mais ne bloque pas la conversion J1 | Non — reporter après les premiers clients |
| Export PDF résultats | Non implémenté | Faible — personne ne l'a demandé encore | Non — piège à éviter |

---

## 2. Ce qui DOIT être là avant le premier client payant

### Fonctionnel — zéro bug bloquant sur ce flux
- [ ] Inscription → sélection niveau/chapitres → diagnostic (8 questions) sans plantage silencieux
- [ ] Diagnostic → chapitres accessibles immédiatement
- [ ] Faire 20 exos d'un chapitre → score sauvé → visible dans Vue Progression
- [ ] Boost quotidien → 5 exos ciblés → sauvegarde
- [ ] Mode "Contrôle demain" → fonctionne sur mobile sans erreur JS
- [ ] Vue Progression → charge correctement, pas d'écran blanc
- [ ] Auto-login → fonctionne sur mobile (localStorage persistant)
- Tester ces 7 scénarios sur iPhone + Android avant tout lancement. Un seul bug bloquant = 0 conversion.

### Légal — minimum légal pour données de mineurs (RGPD renforcé)
- [ ] **Mentions légales** : nom, prénom ou raison sociale, email de contact, hébergeur (Google)
- [ ] **Case à cocher à l'inscription** : "J'ai l'autorisation d'un parent ou tuteur légal" — obligatoire, pas pré-cochée
- [ ] **Politique de confidentialité minimaliste** : quelles données, où stockées (Google Sheets EU), durée de conservation, droit de suppression (email contact)
- [ ] **Politique cookies** : aucun cookie tiers → une bannière simple "ce site utilise localStorage uniquement" suffit
- Sans ce minimum légal, une seule plainte d'un parent peut fermer le projet.

### Paiement — encaisser avant de convaincre
- [ ] **A minima : lien PayPal ou virement manuel** avec email de contact visible sur la landing
- [ ] Message clair sur la landing : "7 jours gratuits, puis 9,99€/mois — paiement par [méthode]"
- [ ] Stripe peut attendre la 5ème vente — intégrer Stripe avant d'avoir validé la proposition de valeur est une perte de temps
- [ ] Processus manuel acceptable pour les 10 premiers clients : email + PayPal + activation manuelle de la colonne `Premium`

### Support — la confiance se gagne par une adresse email visible
- [ ] Adresse email de contact visible sur la landing (pas cachée dans les mentions légales)
- [ ] Temps de réponse affiché : "Réponse sous 24h en semaine"
- [ ] Pas besoin de chat en temps réel — un email suffit pour le MVP

---

## 3. Ce qu'il ne faut PAS ajouter avant 50 clients

| Fonctionnalité | Pourquoi l'éviter maintenant |
|---|---|
| Tableau de bord parents | Représente 3-5 jours de dev pour un bénéfice incertain. Les parents payeurs veulent une promesse simple : "mon enfant progresse". La Vue Progression suffit. |
| Mode multi-élèves (compte prof) | Inutile avant d'avoir des profs comme clients. Le fondateur est son propre cas de test. |
| Application mobile native (iOS/Android) | La SPA est déjà mobile-first. Une app native coûte 2-4 semaines et nécessite un compte développeur Apple (99$/an). La PWA suffit largement avant 50 clients. |
| Recommandations IA en temps réel | La génération nocturne (Pending_Exos validés le matin) répond au besoin. L'IA temps réel nécessite une API permanente, des coûts variables, et une infra hors Google Sheets. |
| Forum / communauté | Aucune masse critique avant 50 clients. Un forum vide fait fuir. |
| Import depuis l'ENT (Pronote, etc.) | Bureaucratie lourde, aucun bénéfice au MVP. Les parents s'inscrivent directement — c'est un avantage, pas un manque. |
| Export PDF résultats | Personne n'a demandé. À construire uniquement sur demande explicite d'un client payant. |
| Système de parrainage / affiliate | Distraction. Acquérir les 50 premiers clients manuellement (parents d'élèves connus). |

---

## 4. Recommandation finale : lancer maintenant ou attendre ?

**Attendre. Mais pas longtemps : 5 à 7 jours de travail ciblé.**

Le flux technique existe et fonctionne dans les grandes lignes. Mais trois points bloquent un vrai lancement :

1. **Le flux mobile n'est pas validé bout en bout** — un seul bug silencieux à l'inscription détruit la confiance du premier client. Il faut tester les 7 scénarios listés en section 2 et corriger ce qui casse.
2. **Le cadre légal pour les mineurs est absent** — sans case consentement parental et mentions légales, le risque juridique est réel et immédiat dès la première famille.
3. **Le paiement n'est pas visible sur la landing** — sans prix affiché et moyen d'encaisser, un parent intéressé ne peut pas acheter même s'il le veut.

Plan concret : 2 jours de tests + corrections bugs, 1 jour légal (mentions légales + case consentement), 1 jour landing (prix + email contact + PayPal). Total : 4 jours. Ensuite contacter les 5 premiers parents d'élèves connus directement.

---

## 5. Classement priorisé des features à implémenter (après 50 clients)

| Feature | Impact MRR | Effort (j-h) | Priorité |
|---|---|---|---|
| Email automatique au parent (récap semaine + progression) | Fort — les parents renouvellent si informés | 1-2j | P1 |
| Stripe + abonnement automatique | Fort — supprime le paiement manuel, réduit le churn | 2-3j | P1 |
| Notification push / email "Reviens faire ton boost" | Fort — rétention décisive après J7 | 1j (email via GAS + Gmail) | P1 |
| Mode "Préparation Brevet" | Fort — saisonnalité mai-juin, fort argument marketing | 3-4j | P2 |
| Tableau de bord parents (simple) | Moyen — différenciant mais pas déclencheur seul | 3-5j | P2 |
| Notifications push navigateur (PWA) | Moyen — complément email, pas de remplacement | 1j | P3 |
| Export PDF bilan mensuel | Faible — nice-to-have, demandé parfois | 1j | P3 |
| Mode multi-élèves (compte prof) | Moyen — nouveau segment, mais différent du B2C actuel | 5-7j | P4 |
| Application mobile native | Faible à ce stade — PWA suffit | 10-15j | P5 — ne pas faire avant 200 clients |
