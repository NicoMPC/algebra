---
name: Option B — Next.js quiz + auth
description: Migration future du quiz diagnostic + auth en Next.js (quand 30+ clients)
type: project
---

## Option B : Next.js landing + quiz + auth (15-20h)

Prérequis : Option A live et stable (landing Next.js only).

### Ce qui migre
- Quiz diagnostic complet (_pickDiagExos, _flowRenderQuestion, _flowAnswerOpt, _flowAnswerFill, _matchFill, hints, formulas, KaTeX)
- Modale auth (register/login/reset, hash SHA-256, appels GAS)
- Trial flow stepper (3 steps)

### Challenges
- ~500 lignes de logique métier à réécrire en React/TS
- Session cross-domain (localStorage ne se partage pas entre domaines)
- KaTeX rendering en React (next-katex ou react-katex)
- Double maintenance si logique quiz change

### Quand déclencher
- 30+ clients (le "wow" visuel du quiz justifie l'effort)
- Ou si le taux de conversion quiz → inscription est < 20% (le polish pourrait aider)

**Why:** À 10 clients le quiz vanilla marche. À 30+, chaque % de conversion compte. Le quiz est le moment critique — c'est là que l'élève décide de s'inscrire ou pas.

**How to apply:** Ne pas rouvrir avant d'avoir validé Option A en prod + 30 clients actifs.
