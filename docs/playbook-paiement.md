# Playbook — Paiement & Trial

> Domaine : trial 7 jours, badge progressif, overlay bloquant, Stripe, activation premium.
> Déclencheurs : "il peut encore jouer après J+7", "le paiement active pas le compte", "le badge trial s'affiche pas"

> ⚠️ **Depuis 02/04/2026** : l'API est Supabase Edge Functions (`index.ts`). Les références `backend.js` / lignes GAS sont legacy (emails uniquement).

---

## User flow

```
Inscription → TrialStart = today
  → J-5 à J-1 : badge progressif (bleu → jaune → orange)
  → J-3 : toast "Plus que N jours"
  → J+7 : overlay bloquant + lien Stripe
  → Paiement Stripe → webhook → Premium=1
  → Accès illimité
```

## Fonctions clés

| Étape | Frontend (index.html) | Backend (backend.js) | Sheet |
|---|---|---|---|
| Calcul trial | — | `checkTrialStatus()` L.4935 | Users.Premium, Users.TrialStart |
| Badge trial | `renderTrialBadge()` L.4570 | — | — |
| Overlay J+7 | `showTrialExpired()` L.4597 | — | — |
| Premium guard | `startPremiumGuard()` L.4960 | `checkTrialStatus()` | Users |
| Webhook Stripe | — | `stripeWebhook()` + `_verifyWebhookHmac()` | Users.Premium |
| Lien Stripe | L.4624 | — | — |

## 3 couches de protection premium

1. **Check serveur toutes les 5 min** : `_verifyPremiumStatus()` L.4978
2. **Intégrité localStorage** : `_sealTrial()` + hash — si modifié manuellement → reset + re-verify
3. **Détection DevTools** : si panel ouvert → vérification immédiate

## Checklist diagnostic

1. **Élève accède après J+7** → Vérifier `checkTrialStatus()` retourne `trialActive=false`. Vérifier Users.TrialStart est bien la date d'inscription. Vérifier Users.Premium n'est pas à 1 par erreur.
2. **Overlay ne s'affiche pas** → Vérifier `S.trial.trialActive === false && S.trial.isPremium === false`. L'overlay se déclenche 300ms après `initApp()`.
3. **Paiement Stripe ne s'active pas** → Vérifier webhook reçu dans GAS logs. Vérifier `_verifyWebhookHmac()` ne rejette pas (secret dans PropertiesService). Vérifier que le webhook écrit `Premium=1` dans Users.
4. **Badge trial invisible** → Visible uniquement si `daysLeft ≤ 5`. Admin et Premium ne le voient jamais.

## Sécurité

- Webhook Stripe : HMAC-SHA256 via `_sig/_ts` payload (limitation GAS : pas d'accès aux headers HTTP)
- `SHARED_SECRET` dans `PropertiesService` (plus hardcodé)
- Lien Stripe PROD : `https://buy.stripe.com/cNicN7b0ebU9bOE9WTb3q01`

## Points de défaillance connus

| Bug | Cause | Fix | Date |
|-----|-------|-----|------|
| Webhook sans vérification | GAS n'expose pas les headers HTTP | V1 — `_verifyWebhookHmac()` + fallback metadata.secret | 2026-03-22 |
| Secret hardcodé | SHARED_SECRET en clair dans backend.js | V2 — PropertiesService | 2026-03-22 |

## Règles CLAUDE.md

T1 (7 jours gratuits), T2 (19.99€/mois), T3 (badge progressif), T4 (overlay bloquant)
