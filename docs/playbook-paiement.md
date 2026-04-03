# Playbook — Paiement & Freemium

> Domaine : freemium (1 chapitre gratuit), chapitres verrouillés, Stripe one-time 29,99€, activation premium auto.
> Déclencheurs : "il peut accéder à un chapitre bloqué", "le paiement active pas le compte", "le badge free s'affiche pas"

> ⚠️ **Depuis 02/04/2026** : l'API est Supabase Edge Functions (`index.ts`). Les références `backend.js` / lignes GAS sont legacy (emails uniquement).
> ⚠️ **Depuis 03/04/2026** : modèle freemium (plus de trial 7 jours). Paiement unique 29,99€.

---

## User flow

```
Inscription → Diagnostic 5 questions
  → free_chapter = chapitre le plus faible (auto)
  → 1 chapitre débloqué + boost quotidien illimité
  → Autres chapitres : visibles mais 🔒 grisés
  → Clic chapitre bloqué → overlay "Débloque tout" + CTA Stripe
  → Paiement Stripe 29,99€ → webhook auto → premium=true, premium_end=2026-06-30
  → Tous les chapitres débloqués
```

## Fonctions clés

| Étape | Frontend (app.html) | Backend (index.ts) |
|---|---|---|
| Chapitre verrouillé ? | `_isChapLocked(cat)` | Guard dans `saveScore()` / `saveScoresBatch()` |
| free_chapter auto | Callback `save_calibration_batch` | `saveCalibrationBatch()` → weakest chapter |
| Badge free/premium | `renderTrialBadge()` | — |
| Overlay locked | `showLockedOverlay()` | — |
| Premium guard | `startPremiumGuard()` / `_verifyPremiumStatus()` | `checkTrialStatus()` → isPremium + freeChapter |
| Webhook Stripe | — | `stripeWebhook()` (natif checkout.session.completed) |
| Lien Stripe | `showLockedOverlay()`, `premium.html` | — |

## Guard freemium — 2 niveaux

### Frontend (`_isChapLocked`)
- Retourne `false` si : premium, admin, cat = BOOST/CALIBRAGE/BREVET/REVISION, ou cat = freeChapter
- Utilisé dans : `togCat()`, `openFromProgress()`, rendu cartes, hero CTA

### Backend (`saveScore` / `saveScoresBatch`)
- Si `!premium && source !== 'CALIBRAGE' && source !== 'BOOST'` → vérifie `categorie === free_chapter`
- Sinon → reject "Chapitre verrouillé"

## 3 couches de protection premium

1. **Check serveur toutes les 5 min** : `_verifyPremiumStatus()`
2. **Intégrité localStorage** : `_sealTrial()` + hash — si modifié manuellement → reset + re-verify
3. **Détection DevTools** : si panel ouvert → vérification immédiate

## Webhook Stripe (auto)

- Endpoint : `https://xlfzhcanzmqqlxtavzrd.supabase.co/functions/v1/api`
- Event : `checkout.session.completed`
- L'Edge Function détecte `p.type === "checkout.session.completed"` → extrait `customer_details.email` → `UPDATE profiles SET premium=true, premium_end='2026-06-30'`
- Pas de signature verification pour l'instant (OK pour <50 élèves)

## Checklist diagnostic

1. **Élève clique chapitre bloqué** → Vérifier `_isChapLocked()` retourne true. Overlay s'affiche avec CTA Stripe.
2. **Paiement Stripe ne s'active pas** → Vérifier webhook reçu (Stripe Dashboard → Developers → Events). Vérifier que l'email Stripe matche l'email du profil Supabase.
3. **Badge free invisible** → Visible uniquement si `!S.trial.isPremium`. Admin ne le voit jamais.
4. **free_chapter null** → L'élève n'a pas fait le diagnostic. UI doit bloquer tant que diag pas terminé.

## Sécurité

- Lien Stripe PROD : `https://buy.stripe.com/3cI5kFfgu9M19Gwd95b3q02`
- Prix : 29,99€ TTC (TVA non applicable, art. 293 B CGI)
- Pas de signature webhook (à ajouter au-delà de 50 élèves)

## Règles CLAUDE.md

T1 (freemium 1 chapitre), T2 (29,99€ one-time), T3 (badge freemium), T4 (chapitres bloqués)
