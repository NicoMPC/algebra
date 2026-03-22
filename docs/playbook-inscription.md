# Playbook — Inscription → J+7

> Domaine : tout ce qui se passe entre l'arrivée sur la landing et la fin du trial.
> Déclencheurs : "un élève peut pas s'inscrire", "le quiz marche pas", "le mail J+0 est pas parti", "le badge trial s'affiche pas"

---

## User flow

```
Landing → CTA → Quiz guest (4-10 exos)
  → Résultat + choix objectif
  → Inscription (prénom, email, mdp, CGU)
  → Sauvegarde calibrage (fire-and-forget)
  → Génération 1er boost (depuis erreurs diag)
  → Mail J+0 automatique
  → Tour guidé (8 étapes, 1 seule fois)
  → Badge trial J-5 bleu → J-3 jaune → J-1 orange
  → J+7 overlay bloquant + lien Stripe
```

## Fonctions clés

| Étape | Frontend (index.html) | Backend (backend.js) | Sheet |
|---|---|---|---|
| Quiz guest | `_flowSetStep()`, `_flowRenderQuestion()` L.3505 | `generateDiagnostic()` L.885 | DiagnosticExos |
| Inscription | `_flowGuestRegister()` L.3872 | `register()` L.254 | Users (nouvelle ligne) |
| Calibrage | fire-and-forget L.3935 | `save_calibration_batch()` | Scores (source=CALIBRAGE) |
| 1er boost | `boostFromDiag()` L.5380 | `generateDailyBoost()` L.991 | DailyBoosts |
| Mail J+0 | — | `sendMarketingSequence(email, name, 0)` L.4328 | Emails |
| Badge trial | `renderTrialBadge()` L.4570 | `checkTrialStatus()` L.4935 | Users.TrialStart |
| Overlay J+7 | `showTrialExpired()` L.4597 | — | — |
| Mails J+3/5/7 | admin manuel | `sendMarketingSequence()` L.4401+ | Emails |

## Checklist diagnostic

Quand un problème est signalé dans ce domaine :

1. **Quiz ne se lance pas** → Vérifier DiagnosticExos a des lignes pour le niveau. Vérifier `generate_diagnostic` ne renvoie pas d'erreur.
2. **Inscription échoue** → Vérifier email pas déjà pris. Vérifier limite bêta 50 pas atteinte. Vérifier hash SHA-256 format (64 chars).
3. **Boost pas généré après inscription** → Vérifier `boostFromDiag()` appelé. Vérifier DailyBoosts a une nouvelle ligne.
4. **Mail J+0 pas reçu** → Vérifier onglet Emails dans Sheet (log). Vérifier `_isUnsubscribed()`. Vérifier quota GmailApp GAS.
5. **Badge trial invisible** → Vérifier `S.trial.daysLeft`. Visible uniquement si ≤5 jours restants.
6. **Overlay J+7 ne bloque pas** → Vérifier `checkTrialStatus()` retourne `trialActive=false`. Vérifier colonnes Users.Premium et Users.TrialStart.

## Points de défaillance connus

| Bug | Cause | Fix | Date |
|-----|-------|-----|------|
| Calibrage polluait tri chapitres | Scores CALIBRAGE comptés dans sessions | V7 — filtre `source !== 'CALIBRAGE'` | 2026-03-22 |

## Règles CLAUDE.md

P1 (diagnostic avant tout), T1-T5 (trial 7j, 19.99€, badge, overlay, emails), M1 (toast mutex), G5 (tour guidé)

## Sécurité

- Hash MDP côté client : `SHA-256(email + '::' + password + '::AB22')` — RGPD mineurs
- CGU obligatoires avant inscription
- Pas de données sensibles dans localStorage (auth token uniquement)
