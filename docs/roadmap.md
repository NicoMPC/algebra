# Roadmap — Matheux

> Priorités de développement. Voir aussi [CLAUDE.md](../CLAUDE.md) pour les règles et [product.md](product.md) pour le produit.

---

## État global — 18 mars 2026

**Matheux LANCÉ.** GAS @97. Tests 74/74. 54 chapitres, 1872 exercices (score 98,3%). Gamification @90. Onboarding @93. Landing @94. Invariants messages @95. Tour guidé @96.

**Reste** : webhook Stripe HMAC (avant J+7), test paiement CB réel, automatisation triggers dès 10 clients.

| Dimension | État |
|---|---|
| Tests automatisés | 74/74 (100%) + simulation 40 élèves 17/17 + simulation 21j 12 profils |
| Couverture programme | ~100% — 54 chapitres (1080 curriculum + 108 diag + 540 boost + 144 brevet) |
| Niveau 1ERE Spé | 10 chapitres expérimentaux — backend prêt, frontend non modifié |
| Juridique | Complet (5 pages + consentement parental + RGPD + TVA art. 293 B CGI) |
| Paiement | Stripe PROD actif (19,99/mois) |
| Emails auto | J+0 auto + reset MDP auto — J+3/J+5/J+7 manuels via admin |
| Admin cockpit | 6 onglets, boost+chapitre 1-clic, JSON complet, profils test |
| Limite bêta | 50 vrais élèves (IsTest=0) |

---

## Actions manuelles — à faire par Nicolas

| # | Action | Où | Priorité |
|---|---|---|---|
| 1 | **Automatiser trigger `triggerDailyMarketing`** — dès 10 clients actifs | Apps Script UI | 🟡 |
| 2 | **Webhook Stripe HMAC-SHA256** — endpoint à finaliser, `SHARED_SECRET` à déplacer vers `PropertiesService` | Stripe dashboard | 🔴 |
| 3 | **Test paiement CB réel** (19,99€ → vérifier Premium=1 → rembourser) | Stripe | 🔴 |
| 4 | Vrais témoignages élèves/parents sur landing | À collecter | 🔵 |
| 5 | **UX sans boost** — bandeau "ton boost arrive bientôt" si aucun boost généré | Frontend | 🟡 |
| 6 | **Centraliser 3 mails matheux.fr** (Thunderbird/alias/redirection) | Ionos | 🟡 |

---

## Priorités code — prochaines sessions

| # | Action | Priorité |
|---|---|---|
| 1 | **Doublons 1ERE** : 24 doublons Diag/Boost/Curriculum — non bloquant | 🟡 |
| 2 | **Profil d'apprentissage élève** — page dédiée (3 points forts, 2 lacunes, vitesse, streak record). Cadenas overlay trial J+7. | 🟡 |
| 3 | **Automatisation boosts nuit** — agent qui génère JSON boost depuis Scores, pousse dans Suivi. Dès 30 clients. | 🟡 |
| 4 | Agent analyse lacunes quotidien automatique | 🔵 |
| 5 | **Migration Sheets → Supabase** — à déclencher à 80-100 clients. Stack : Supabase + Node.js Railway. Emails : Brevo/Resend. 3-5 sessions. **Ne pas faire avant d'avoir le problème.** | 🔵 |
| 6 | `replyTo: nicolas@matheux.fr` sur J+3, J+7 et reset MDP | 🟡 |
| 7 | **Séquences J+3/J+5/J+7 activées** — trigger Apps Script (manuel pour l'instant) | 🟡 |
| 8 | Double confirmation mot de passe inscription | 🟡 |
| 9 | Template email inscription + rapport parent (design) | 🟡 |
| 10 | Vérif PWA mobile (install + offline + icône) | 🟡 |

---

### Améliorations exercices — sprints suivants

> Score global 6.3/10 (audit 2026-03-19). Techniquement solide (9/10 intégrité, 10/10 structure). À améliorer : qualité pédagogique + diversité types.

**Fait (audit 2026-03-19/20) :**
- ✅ 22 indices révélateurs reformulés (guidants sans dévoiler)
- ✅ 11 formules manquantes complétées
- ✅ 1 doublon corrigé (6EME/Volumes BoostExos)
- ✅ 3 garde-fous figures géométriques : filtre V/F, exclusion angles opposés, labels fallback masqués (31 figures parasites + 128 labels nettoyés)
- ✅ 3 "erreurs de calcul" vérifiées → faux positifs du script audit

**Reste :**

| Priorité | Action | Chapitres concernés | Volume |
|---|---|---|---|
| 1 | **AMÉLIO-01** : Diversifier types d'exercices (objectif 60% QCM, 20% V/F, 20% fill) | Tous — actuellement 100% QCM | ~280 exos à convertir |
| 2 | **AMÉLIO-02** : Ajouter 3ème indice aux exos à 1 seul indice | Fonctions 3EME, Puissances 5EME, Calcul_Littéral 5EME | ~20 exos |
| 3 | **AMÉLIO-03** : Contextualisation (2% → 20% d'exos en situation réelle) | Priorité 5EME + 3EME | long terme |
| 4 | **AMÉLIO-04** : Mode "résolution guidée" step-by-step (nouveau type exercice) | À définir — priorité fractions/équations | conception |

---

## Couverture programme — chapitres manquants

### Priorité critique (programme officiel, souvent au Brevet)
| Notion | Niveau | Statut |
|---|---|---|
| Systèmes d'équations | 3EME | Sprint 2 — Extension Équations |

### Priorité importante (programme officiel)
| Notion | Niveau | Effort |
|---|---|---|
| Symétrie axiale | 6EME | +1 chapitre |
| Symétrie centrale | 5EME | +1 chapitre |
| Volumes | 6EME | Extension PérimètresAires |
| Transformations (translations, rotations) | 5EME | +1 chapitre |
| Inéquations | 3EME | Extension Équations |
| Notation scientifique | 3EME | Extension Puissances |

Détail complet : [programme-français-verif.md](programme-français-verif.md)

---

## Checklist "Prêt pour 50 élèves"

### Infrastructure
- [x] GAS @88 stable — 30+ actions, simulation 21j OK
- [x] Google Sheet prod + validation inputs + rate limiting
- [ ] **Séquences J+3/J+5/J+7 activées** (trigger Apps Script)

### Acquisition & conversion
- [x] Landing + flow CTA + quiz inline + onboarding + Stripe PROD
- [x] Trial 7j + badge J-X + overlay → Stripe
- [x] Email J+0 auto

### Légal
- [x] 5 pages légales + consentement parental + RGPD + GA4

### Pédagogie
- [x] 1080 exos curriculum + 108 diag + 540 boost + 144 brevet

### UX
- [x] Mobile-first, gamification, messages ado, onboarding premium
- [~] **PWA installable** — code prêt, **à valider en prod** (Lighthouse PWA ≥ 90)

### Admin
- [x] Dashboard trié, modal complet, publish 1-clic, cockpit 6 onglets
- [x] Emails dus, templates marketing, profils test

---

## PHASE 2 — Après 20 clients payants

| # | Feature | Description | Priorité |
|---|---|---|---|
| 1 | Doc vivante par élève/chapitre | Fiche notion + faiblesses identifiées, in-app, adaptée niveau/âge | 🟡 |
| 2 | Graphes de fonctions avancés | Exponentielles, trigo, fonctions par morceaux | 🟡 |
| 3 | Arbres de probabilités post-réponse | Détection auto → arbre pondéré SVG | 🟡 |
| 4 | Types d'exercices enrichis — rollout | VF, fill, compléter — rollout progressif | 🟡 |
| 5 | Audit géométrie contextuelle | Exercices trop courts/abstraits à reformuler | 🔵 |

### Offres différenciées — décision basée sur données réelles

> **Ne pas créer avant d'avoir lu la colonne `Objectif` sur 10-15 clients.**

| Si majorité déclare | Offre envisagée | Prix |
|---|---|---|
| `lacunes` | Offre actuelle — déjà bien positionnée | 19,99€/mois |
| `brevet` | Pack "Prépa Brevet" — accès prioritaire brevets blancs + suivi dédié | 24,99€/mois |
| `chapitre_jour` | Offre "Suivi annuel" — engagement 10 mois, prix réduit | 14,99€/mois |
| `toutes_matieres` | Offre "Multi-niveaux" — accès tous niveaux (fratrie) | 29,99€/mois |

**Workflow de migration** : email personnalisé selon objectif déclaré → lien Stripe vers nouveau plan.
Aucun client existant verrouillé (pas de CB pendant le trial).

**Offre flash de conversion** : à J+2/J+3, si l'élève est engagé (boost fait, streak actif),
envoyer manuellement une offre -50% premier mois ("9,99€ ce mois-ci, sans engagement").
Lien Stripe séparé créé en 2 min. Envoi manuel depuis la fiche admin. Zéro code requis.

**Quand décider** : après 10-15 clients, regarder la répartition `Objectif` dans Users.

### Rétention & FOMO — mécaniques psychologiques

> Objectif : rendre le départ douloureux, pas l'abonnement obligatoire.
> Principe : la valeur accumulée doit être visible et concrète.

**Mécanique 1 — Profil d'apprentissage avec cadenas**
À J+7, overlay trial ne dit pas juste "19,99€/mois".
Il montre le profil construit : points forts, lacunes identifiées, streak, vitesse de progression.
Avec un message : "Ces données disparaissent dans 48h. Continue pour garder ton profil."

**Mécanique 2 — Streak comme identité (pas comme peur)**
Pas "tu vas perdre ton streak" à la Duolingo.
Mais : "Lucas a travaillé 12 jours d'affilée — top 5% des élèves Matheux."

**Mécanique 3 — Rapport parent comme lien émotionnel**
Email hebdo formulé comme bilan humain :
"Cette semaine Hugo a débloqué les fractions — une notion qui lui résistait depuis septembre."

**Mécanique 4 — Personnalisation explicite dans les messages**
"Ton prof a remarqué que tu fais toujours la même erreur sur les fractions
avec dénominateurs différents — voici pourquoi."

**Mécanique 5 — Coût de reconstruction visible**
À J+30 : "Si tu recommences ailleurs, il faudra X semaines pour retrouver
ce niveau de personnalisation."

**À implémenter dans l'ordre** :
1. Profil d'apprentissage dans l'overlay trial (PHASE 2 priorité 1)
2. Rapport parent hebdo automatique (dès 20 clients)
3. Streak comme identité dans les toasts (petit patch, fort impact)
4. Personnalisation explicite dans les messages post-exo (wording uniquement)
