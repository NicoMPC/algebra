# 60 — Nouvelle landing vanilla (remplace le build Next.js)

> Agent : dev-ux (landing) · 24/09/2026 · Branche `feat/diagnostic-3e` · Statut : **prête à relire, pas en prod**
> Livrables : `landing/index.html`, `landing/assets/` (logo ×2, `og.png`), `landing/screens/` (captures).
> Copy reprise de `50-offre-conversion.md` §9 (growth). Charte reprise d'`app.html` (Syne + DM Sans,
> navy `#0F172A`, bleu `#1E40AF`, vert `#10B981`) et des maquettes UX (`maquettes/02-carte-partielle`).

## 1. Chiffres

| | Valeur |
|---|---|
| Poids HTML (CSS + JS inline) | ~60 Ko (≈ 15 Ko gzip) |
| Assets | 2 logos PNG de 0,8 Ko + `og.png` 36 Ko (chargé uniquement par les réseaux sociaux) |
| Requêtes externes | Google Fonts seulement. GA4 uniquement après « Accepter » |
| Framework / Tailwind / KaTeX | aucun |
| Contrastes vérifiés | tous ≥ 4,5:1 (texte gris `#64748B` sur `#F8FAFC` = 4,55, le plus faible) |

## 2. Structure (ordre de la page)

1. **Header** sticky : logo, ancres (desktop), Connexion (`/app.html#login`), CTA « Diagnostic gratuit ».
2. **Hero** : surtitre `Maths · 3e · Brevet 2027`, H1 ado « Découvre en 8 min où tu en es vraiment en maths. », sous-titre parent (growth §9.1, sans « conçu par un prof » : Nicolas n'est pas prof de maths), CTA `Faire le diagnostic gratuit →`, lien « Je suis parent : comment ça marche ? », micro `~8 min · 15 questions · sans carte bancaire`.
   **Démo animée de la carte** (CSS pur, ~4 s, bouton « Rejouer », coupée si `prefers-reduced-motion`) : 5 domaines, **3 cases colorées par domaine = 15 questions**, le reste en gris « pas encore mesuré », 1 point faible avec cause racine (Pythagore → carrés). Aucun flou appât (growth §2.3).
3. **Bandeau Brevet** : « juin 2027 · date officielle pas encore publiée ». Décompte en **semaines** seulement quand `CONFIG.brevet.date` est rempli.
4. **Comment ça marche** : 3 étapes (growth §9.2) + CTA `Commencer par le gratuit →`.
5. **« On trouve la cause, pas juste la note »** : correction classique vs trace Matheux (BC² = 12 + 16 → question de 5e « 7² ? » → 14 → cause : carré confondu avec ×2).
6. **Aperçu du bilan PDF parent** : feuille stylisée en HTML, étiquetée « Exemple — élève fictif ». Elle reprend l'objet Carte du contrat §5 (score, 5 domaines, 3 priorités, plan sur 4 semaines).
7. **Tarifs** : Gratuit / Diagnostic complet / Programme Brevet (growth §9.4). Sous les cartes : déduction des 19 €, garantie 30 jours, comparaison avec un cours particulier (sourcée par growth), mention TVA 293 B. Le gratuit est affiché en premier sur mobile.
8. **Parents** : 6 engagements (données, zéro pub, vous gardez la main, temps d'écran, pas d'abonnement, garantie 30 j), bloc fondateur (growth §9.5, bio validée le 24/09 : ancien ingénieur, soutien scolaire ; **jamais « prof de maths »**), emplacement photo commenté, **emplacement témoignages vide et commenté**.
9. **FAQ** : 8 questions parent et 5 questions ado (growth §9.6-9.7), en `<details>` visibles dans le DOM.
10. **CTA final** ado + lien parent « Voir un exemple de bilan → » (ancre `#bilan`).
11. **Footer** : liens vers les pages SEO, Ressources, Légal (mentions, CGU, CGV, confidentialité, cookies) + « Gérer les cookies ».
12. **Barre CTA fixe en bas** (mobile uniquement) : visible une fois le hero dépassé, masquée sur le CTA final.

## 3. Choix techniques

- **Point d'entrée diagnostic** : `/app.html#diag-<source>`. C'est le hash routing existant d'`app.html` (l. ~2566), qui appelle `startTrialFlow(source)` et trace `cta_click`. Sources : `nav`, `hero`, `steps`, `offre_free`, `offre_complet`, `offre_brevet`, `final`, `sticky`. `app.html` n'est pas modifié.
- **Les CTA des offres payantes lancent le diagnostic gratuit.** Le paiement se fait dans l'app, sur le paywall parent, une fois la carte express obtenue (growth §2). Il n'existe pas encore de route d'achat directe (le webhook a besoin du profil via `client_reference_id`). Libellé choisi : « Commencer par le diagnostic ».
- **Prix et date du Brevet au même endroit** : l'objet `CONFIG` en tête du script (`prix.diag`, `prix.brevet`, `brevet.date`, `ga4`). Le montant après déduction (`upgrade`) est calculé. Les éléments `data-price` sont remplis par JS, et le HTML contient le même montant en secours pour le SEO et les navigateurs sans JS. **Exception** : la FAQ (question « pour 19 € ») et son JSON-LD sont statiques. À mettre à jour à la main si le prix change.
- **Cookies / GA4** : même clé `mx_cookie_consent` et même ID `G-7R2DW4585Y` qu'`app.html` (même origine, donc un seul consentement pour tout le site). `?notrack` est respecté (`mx_notrack`). Accepter et Refuser ont la même taille et la même couleur (growth §9.8). GA4 ne se charge qu'après « Accepter ».
- **SEO** : title, meta description, canonical `https://matheux.fr/`, OG et Twitter avec `assets/og.png` (1200×630, généré en local). JSON-LD : `Organization` + `FAQPage`. Le `FAQPage` est généré à partir des mêmes textes que la FAQ visible, puisque la FAQ est bien dans le DOM.
- **Accessibilité** : lien d'évitement, `:focus-visible` marqué, `aria-label` sur la démo et l'aperçu PDF (`role="img"`), `<details>` natifs, `prefers-reduced-motion`, cibles tactiles ≥ 40 px.
- **Honnêteté** : aucun avis, aucun compteur d'utilisateurs, aucune fausse rareté, aucun décompte inventé. Les exemples sont étiquetés « Exemple » ou « Exemple — élève fictif ». Aucune phrase ne dit qu'un humain analyse chaque élève. Aucune phrase ne pousse l'ado à payer : la section tarifs vouvoie le parent.

## 4. Reste à aligner

| Sujet | Où | Dépend de |
|---|---|---|
| « sans inscription pour commencer » | micro du hero et du CTA final (`<!-- COPY -->`) | UX 40-parcours : l'express se passe-t-il avant la création du compte ? |
| H1 : consigne du chef de projet ou variante growth « Sache exactement ce qui te bloque en maths. » | hero | Nicolas |
| Photo du fondateur | bloc fondateur (initiales en attendant) | Nicolas |
| Aperçu PDF : le remplacer par une capture du vrai gabarit | section `#bilan` | agent PDF (`js/bilan-pdf.js`, 30-pdf.md) |
| Durées et nombre de questions (8 min / 15 q / 40 min / 3 modules) | texte | moteur (20-moteur.md), à vérifier une fois le diagnostic réel mesuré |
| Formulation légale de la garantie 30 j et mention TVA | tarifs, parents, FAQ | 52-legal.md (pas encore écrit) |
| Date officielle du Brevet 2027 | `CONFIG.brevet.date` | publication au BO |
| Page `bilan.html?t=…` et bouton « partager ma carte » | hors landing | growth §3 / UX |

## 5. Plan de bascule (au merge)

1. `git mv landing/index.html index.html` et `git mv landing/assets assets`. Les chemins `assets/…` sont relatifs, `og:image` pointe déjà vers `https://matheux.fr/assets/og.png`.
2. Supprimer `_next/` **et** `index.txt` (payload RSC Next).
3. **`404.html` est aussi un build Next** : le remplacer par une petite page vanilla (logo, « Page introuvable », lien vers l'accueil et le diagnostic), sinon elle casse dès que `_next/` est supprimé.
4. `sitemap.xml` : `lastmod` de `/` à la date de bascule. Retirer ou réécrire `brevet-2026.html` (contenu 2026 périmé).
5. `.claspignore` : ajouter `assets/` et `assets/**`. On peut garder les lignes `_next/` (sans effet), ce qui protège d'un retour accidentel.
6. Pages SEO (`pythagore-`, `thales-`, `fractions-`, `probabilites-`, `statistiques-brevet.html`, `comment-reviser-brevet-maths.html`, `premium.html`) : leurs CTA pointent vers `app.html?from=…`, un paramètre qu'`app.html` ne lit pas. Ils ouvrent donc l'ancienne landing interne de l'app au lieu du diagnostic. À remplacer par `/app.html#diag-seo_<page>`. Mettre aussi à jour les mentions « Brevet 2026 » et « 29,99 € ». `premium.html` est à réécrire ou à rediriger vers `/#offres` (growth : retirer le badge « rétractation 14 jours »).
7. `app.html` : `showLanding()` affiche encore une landing interne (Tailwind, anciens textes). Hors périmètre, mais à signaler à l'agent UX : quand on arrive sans hash, l'app devrait renvoyer vers `/` ou vers le login.
8. Vérifier en prod : les CTA ouvrent le diagnostic, le bandeau cookies n'apparaît qu'une fois pour le site et l'app, l'aperçu OG s'affiche correctement (debugger Facebook ou LinkedIn).

## ❓ Questions pour Nicolas

1. **H1** : « Découvre en 8 min où tu en es vraiment en maths. » (en place) ou « Sache exactement ce qui te bloque en maths. » (growth) ? → Reco : garder l'actuel. Il est concret (durée) et orienté action.
2. **Photo du fondateur** : tu en fournis une vraie ? → Reco : oui, c'est la seule preuve sociale honnête qu'on a. En attendant, on garde les initiales (pas de photo stock).
3. **Garantie 30 jours** mise en avant à 3 endroits (tarifs, parents, FAQ) : OK ? → Reco : oui, c'est le principal levier de réassurance honnête.
4. **`404.html` et `premium.html`** : je les réécris en vanilla au moment de la bascule ? → Reco : oui pour la 404 (sinon elle casse). `premium.html` redirige vers `/#offres`.
