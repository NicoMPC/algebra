# Rapport — Flow Landing Diagnostic Complet
> Date : 11 mars 2026 · Session autonome

## Problème résolu
La landing utilisait 2 questions DEMO_QS hardcodées (jamais sauvegardées).
L'utilisateur refaisait un vrai diagnostic au 1er login → doublon frustrant.

## Solution implémentée

### Workflow 1 — Première visite
Landing → CTA → classe → chapitres (max 2) → generate_diagnostic GAS → [N exos réels avec MathJax] → résultats → formulaire → register() → save_score en masse → login → dashboard (sans re-diagnostic)

### Workflow 2 — Retour avec localStorage
Landing → détection boost_v23 → auto-login silencieux → dashboard + "Bon retour 🔥"

### Workflow 3 — Mail existant
register() → erreur → switch login silencieux → toast "T'as déjà un compte 🔥"

### Workflow 4 — Abandon diagnostic
guestDiag queue localStorage TTL 24h → bandeau reprise [Continuer / Recommencer]

## Fonctions ajoutées/modifiées
| Fonction | Action |
|----------|--------|
| `_flowStartDiag()` | Nouveau — appel GAS generate_diagnostic, spinner, fallback |
| `_flowRenderDiagExo()` | Nouveau — rendu exo QCM + MathJax + progress bar |
| `_flowCheckOpt()` | Nouveau — feedback ado + queue localStorage |
| `_flowShowResults()` | Nouveau — résumé + confetti + → step 4 |
| `flowRegister()` | Modifié — skip diag si _flowDiagDone, save_score masse, switch login |
| `showOnboarding()` | Modifié — skip slide diagnostic si déjà fait |
| `startTrialFlow()` | Modifié — détection guestDiag abandonné |
| `flowToggleChap()` | Modifié — cap 2 chapitres |

## Fix phase 3 — polish
- save_score masse : champs corrigés (`name`/`level`/`exercice_idx`/`q` conformes au GAS)
- `_flowRenderQ()` + `flowDemoAnswer()` supprimés (code mort DEMO_QS)
- `_flowCheckOpt()` : ajout messages feedback ton ado (Carton plein 🎯 / T'as géré ça 💪 / etc.)
- `_flowRenderDiagExo()` : MathJax.typeset() confirmé présent

## Cas couverts
- ✅ Première visite — diagnostic GAS complet
- ✅ Retour avec session — auto-login silencieux
- ✅ Mail existant — switch login automatique
- ✅ Abandon à mi-diagnostic — reprise 24h
- ✅ Résultats sauvés après inscription (champs GAS corrects)
- ✅ Pas de doublon diagnostic au login
- ✅ MathJax sur les exos landing
- ✅ Messages ton ado dans le flow
- ✅ Mobile-friendly (padding `.flow-opt`)

## Tests API (phase 3)
| Test | Résultat |
|------|---------|
| generate_diagnostic guest (5EME, Fractions+Equations) | ✅ 2 exos |
| register → code élève | ✅ |
| save_score masse (3 exos) | ✅ après correction champs |
| login post-register | ✅ history_len=0, pas de doublon |

## Commit
`61b2924` — feat(landing): diagnostic GAS complet + queue 24h + auto-login + reprise abandon
Phase 3 — docs: rapport + polish (fix save_score champs, suppression code mort DEMO_QS)
