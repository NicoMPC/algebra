# 70 — SEO matheux.fr

> Agent : seo · 26/09/2026 · Branche `feat/diagnostic-3e` · Statut : **prêt à relire, pas en prod** (Nicolas pousse `main`)
> Livrables : 9 nouvelles pages, 8 pages réécrites, `assets/seo.css`, `sitemap.xml`, `robots.txt`, redirection `brevet-2026.html`,
> générateur `docs/specs/seo-src/`, captures mobiles `docs/specs/seo-screens/`.

## 0. Résumé

- **Technique** : robots.txt ne bloque plus `app.html` ni `/icons/`. Un `Disallow` empêchait Google de lire le `noindex` de l’app, et bloquait le favicon et le logo de l’Organization. Le sitemap passe de 14 à 23 URL, toutes indexables, et seulement elles. Toutes les pages indexables ont maintenant un canonical, une description et un title unique. `offline.html` et `unsubscribe.html` passent en `noindex`. Il reste 0 lien interne cassé et 0 JSON-LD invalide.
- **Contenu** : les anciennes pages SEO étaient minces (270 à 730 mots) et remplies de chiffres inventés (« 92 % des brevets », « 12-20 points au brevet », « 80 % des points viennent de 5 chapitres »). Leur offre était périmée (« 1 chapitre gratuit », diagnostic de « 5 questions, 1 minute ») et on y trouvait des notions hors programme (systèmes d’équations, quartiles). Elles ont toutes été réécrites. Chaque page fait maintenant 800 à 1 100 mots utiles et suit le même plan : cours court, méthode, 2 à 4 exercices corrigés, erreurs fréquentes tirées de `competences.json`, FAQ visible, CTA diagnostic.
- **Nouvelles pages** (9) : calcul littéral, équations, fonctions (image/antécédent), fonction affine, puissances, racine carrée, arithmétique, trigonométrie, et une page parents « difficultés en maths en 3e ».
- **Cannibalisation résolue** : `exercices-maths-3eme.html` devient le **hub** de toutes les notions. `exercices-maths-3eme-brevet.html` devient la page **Brevet 2027** (format de l’épreuve, automatismes, problèmes type). `brevet-2026.html` redirige vers elle. `comment-reviser-brevet-maths.html` garde l’intention « méthode ».

## 1. Audit technique : avant / après

Outillage : `python3 -m http.server`, script d’audit (titles, descriptions, canonical, h1, alt, JSON-LD, sitemap, liens internes), Chrome headless (puppeteer-core via Deno) en 375 px mobile avec détection des éléments qui débordent.

| Point | Avant (HEAD `ef9ccdb`) | Après |
|---|---|---|
| robots.txt | `Disallow: /app.html` et `/icons/` : Google ne voyait pas le `noindex` de l’app (risque « indexée malgré le blocage » vu le nombre de liens `/app.html#diag-…`), et le favicon et le logo étaient bloqués | `Allow: /`. Seuls `/docs/`, `/dev/`, `/supabase/` et `/node_modules/` sont exclus. Les pages non indexables sont gérées par le `noindex` |
| Sitemap | 14 URL. `lastmod` du 15/03 pour les pages légales | 23 URL = exactement les pages indexables (`lastmod` 2026-09-26). Pas de `changefreq`/`priority` (ignorés par Google) |
| Pages indexables hors sitemap | `brevet-2026.html` (contenu 2026 périmé), `offline.html`, `unsubscribe.html` | 0. Les deux dernières sont en `noindex`, `brevet-2026` redirige |
| Canonical / description manquants | 7 pages (légales, offline, unsubscribe) | 0 sur les pages indexables |
| Descriptions > 160 car. | 6 pages (dont l’accueil, 188) | 0 (137 à 155 car.) |
| Titles > 65 car. | 1 (72) | 0 |
| JSON-LD | `Course` + `Offer` « 1 chapitre gratuit » (périmé, et `Course` mal adapté à une page de cours) | `BreadcrumbList` + `LearningResource` (ou `Article`, ou `CollectionPage` pour le hub) + `FAQPage` généré à partir de la FAQ **visible**. Accueil : ajout de `WebSite` (nom du site dans Google) |
| og:image | `mockup.png` (ancienne app) sur les pages SEO | `assets/og.png` 1200×630, identique à l’accueil |
| Favicon pages SEO | `/icons/icon-192.png` en 192 px | `favicon-32.png` et `apple-touch-icon` (même jeu que l’accueil) |
| Charte | ancienne (indigo/orange, CSS inline de 5 Ko recopié dans chaque page) | charte de la landing. CSS partagé `assets/seo.css` de 8,4 Ko (2,8 Ko gzip), mis en cache d’une page à l’autre |
| Poids d’une page notion | 12-16 Ko HTML | 16-22 Ko HTML (≈ 5 Ko gzip) + CSS partagé. Aucune image bitmap, figures en SVG inline, pas de JS |
| Ressources bloquantes | Google Fonts (3 graisses de Syne + 4 de DM Sans) | Google Fonts réduit à 1 graisse de Syne + 2 de DM Sans, `display=swap`, preconnect |
| Liens internes cassés | 0 | 0 (vérifié sur tous les `.html`, ancres de sommaire comprises) |
| h1 | 1 par page (hors `bilan.html`, qui est en noindex et hors périmètre) | idem |
| Images sans alt | 0 | 0 (logos en `alt=""` décoratif, SVG en `role="img"` + `aria-label`) |
| Mobile 375 px | non vérifié | 17 pages sans débordement horizontal. Captures dans `docs/specs/seo-screens/`. Un h1 trop large (« décomposition ») et 6 formules trop longues ont été corrigés |
| hreflang | aucun | inutile (site 100 % fr-FR, une seule version) : rien à ajouter |
| Redirections | `premium.html` → `/#offres` (meta refresh 0 + JS + noindex) | inchangé. `brevet-2026.html` → `/exercices-maths-3eme-brevet.html` (meta refresh 0 + JS + canonical, que Google traite comme une redirection permanente, sans `noindex`, pour transmettre les signaux) |
| 404 | vanilla, noindex, redirection `/b/<token>` | inchangé (OK) |

Non traité (hors périmètre, signalé) : `bilan.html` a 6 `h1` (noindex, donc sans impact SEO). `cgv.html` affiche encore « 29,99 € — accès jusqu’au Brevet 2026 » (voir ❓).

## 2. Requêtes cibles → une page par intention

Il n’y a pas encore de données Search Console : les niveaux de demande ci-dessous sont des **estimations qualitatives** (fort / moyen / faible), établies d’après la saisonnalité scolaire et la concurrence observable, pas des volumes mesurés. À recaler avec la GSC dès le premier mois.

| Requête type | Qui | Intention | Demande (estim.) | Page |
|---|---|---|---|---|
| diagnostic maths 3e, test niveau maths 3e, évaluation maths 3e en ligne | parent / élève | transactionnelle | faible à moyenne, très qualifiée | `/` (accueil) |
| soutien maths 3e en ligne, aide maths 3e | parent | transactionnelle | moyenne | `/` + `/difficultes-maths-3eme.html` |
| mon enfant est nul en maths 3e, difficultés en maths 3e que faire | parent | informationnelle → conversion | moyenne | `/difficultes-maths-3eme.html` |
| exercices maths 3e, maths 3e, programme maths 3e | élève | informationnelle (navigation) | forte, très concurrentielle | `/exercices-maths-3eme.html` (hub) |
| brevet maths 2027, épreuve maths brevet 2027, automatismes brevet maths | élève / parent | informationnelle | forte (pics en mai et juin) | `/exercices-maths-3eme-brevet.html` |
| révisions brevet maths, comment réviser le brevet de maths | élève / parent | méthode | moyenne (pic de mars à juin) | `/comment-reviser-brevet-maths.html` |
| théorème de pythagore 3e exercice, réciproque pythagore | élève | cours + exercices | forte | `/pythagore-brevet.html` |
| théorème de thalès 3e, réciproque thalès, thalès papillon | élève | cours + exercices | forte | `/thales-brevet.html` |
| trigonométrie 3e, cosinus sinus tangente 3e, soh cah toa | élève | cours + exercices | forte | `/trigonometrie-3eme.html` |
| fonction affine 3e, fonction linéaire 3e, coefficient directeur | élève | cours + exercices | forte | `/fonction-affine-3eme.html` |
| image et antécédent 3e, fonctions 3e | élève | cours + exercices | moyenne à forte | `/fonctions-3eme.html` |
| calcul littéral 3e, développer factoriser 3e, identités remarquables | élève | cours + exercices | forte | `/calcul-litteral-3eme.html` |
| équation 3e, équation produit nul, mise en équation 3e | élève | cours + exercices | forte | `/equations-3eme.html` |
| puissances 3e, notation scientifique 3e | élève | cours + exercices | moyenne | `/puissances-3eme.html` |
| racine carrée 3e | élève | cours + exercices | moyenne | `/racine-carree-3eme.html` |
| nombre premier 3e, décomposition en facteurs premiers | élève | cours + exercices | moyenne | `/arithmetique-3eme.html` |
| fractions 3e exercices, fraction irréductible | élève | cours + exercices | moyenne | `/fractions-brevet.html` |
| probabilités 3e, arbre probabilité 3e | élève | cours + exercices | moyenne à forte | `/probabilites-brevet.html` |
| moyenne médiane étendue 3e, statistiques 3e | élève | cours + exercices | moyenne | `/statistiques-brevet.html` |

Règle de maillage : chaque page notion renvoie vers le hub (fil d’Ariane et header), vers 4 à 5 notions liées (prérequis ou notions combinées au Brevet), et vers la page Brevet 2027. Le diagnostic est proposé 3 fois (header, hero, bloc CTA en milieu de page) via `/app.html#diag-seo_<page>`. Le footer commun liste toutes les notions. L’accueil pointe vers le hub, 7 notions, la page Brevet et la page parents (footer + bandeau Brevet).

Sources `cta_click` (à lire dans GA4 / logs) : `seo_calcul_litteral`, `seo_equations`, `seo_fonctions`, `seo_fonction_affine`, `seo_puissances`, `seo_racine_carree`, `seo_arithmetique`, `seo_trigonometrie`, `seo_pythagore`, `seo_thales`, `seo_fractions`, `seo_probabilites`, `seo_statistiques`, `seo_exercices_3eme` (hub), `seo_exercices_brevet`, `seo_guide`, `seo_parents_difficultes`.

## 3. Ce qui a été fait, page par page

| Fichier | Action |
|---|---|
| `calcul-litteral-3eme.html`, `equations-3eme.html`, `fonctions-3eme.html`, `fonction-affine-3eme.html`, `puissances-3eme.html`, `racine-carree-3eme.html`, `arithmetique-3eme.html`, `trigonometrie-3eme.html` | **nouvelles** pages notions (820 à 1 330 mots, corps + FAQ). Figures SVG : courbe (fonctions), droite (fonction affine), triangle légendé (trigo) |
| `difficultes-maths-3eme.html` | **nouvelle** page parents (vouvoiement, factuelle : origine des blocages, cause racine, tableau comparatif des solutions sans dénigrement, bio fondateur validée) |
| `pythagore-brevet.html`, `thales-brevet.html`, `fractions-brevet.html`, `probabilites-brevet.html`, `statistiques-brevet.html` | réécrites, même URL. Chiffres inventés supprimés, contenu doublé, réciproque/contraposée et configuration papillon ajoutées. Quartiles retirés (hors programme de 3e) |
| `exercices-maths-3eme.html` | devient le **hub** (fil d’Ariane « Maths 3e »). Les 13 notions sont classées par thème, avec une section « par où commencer » (causes racines). Supprimés : « Systèmes d’équations » et « Inéquations » comme chapitres (les systèmes ne sont plus au programme), et les compteurs « 11 chapitres / 22 chapitres » contradictoires |
| `exercices-maths-3eme-brevet.html` | devient la page **Brevet de maths 2027** : date et format de l’épreuve (sources citées), 10 automatismes corrigés reliés aux notions, 2 problèmes type corrigés, conseils pour le jour J |
| `comment-reviser-brevet-maths.html` | réécrite. Supprimés : « 90 % des élèves », « 80 % des points », « prouvé par les sciences cognitives », « à 80 jours du brevet », « diagnostic 5 questions / 1 minute », « sans inscription ». Ajoutés : espacement et récupération (formulés prudemment), planning jusqu’en juin 2027, section parents |
| `brevet-2026.html` | redirection vers la page Brevet 2027 (le fichier est gardé pour ne pas casser les anciens liens) |
| `index.html` | description raccourcie, JSON-LD `WebSite`, lien du bandeau Brevet vers la page Brevet 2027, footer étendu (hub, notions, page parents). Aucune autre modification |
| pages légales | meta description + canonical (contenu non modifié) |
| `offline.html`, `unsubscribe.html` | `noindex` |
| `robots.txt`, `sitemap.xml`, `.claspignore` | voir §1. Les 9 nouveaux `.html` sont ajoutés à `.claspignore` (vérifié : tout `.html` et `.js` racine y figure, sauf `backend.js`) |

Faits Brevet 2027 utilisés, vérifiés le 26/09 : écrits les 24, 25 et 28 juin 2027 (BO spécial n° 2 du 25 août 2026, repris par education.gouv.fr et eduscol). Maths le lundi 28 juin au matin. 2 h sur 20 points : automatismes 20 min sans calculatrice (6 pts), puis raisonnement 1 h 40 avec calculatrice (14 pts) (page DNB 2027 de l’académie de Normandie, recoupée par une seconde source).

Justesse mathématique : chaque calcul des exemples a été recompté (valeurs trigonométriques et racines vérifiées numériquement, arrondis compris). Les erreurs fréquentes reprennent le champ `erreurs` du référentiel. Une relecture par l’agent `relecteur` reste possible si Nicolas le souhaite, mais je n’ai pas de doute identifié.

## 4. Vérifications faites

- Liens internes : 0 cassé, sur tous les `.html` de la racine (href et src), ancres `#…` comprises.
- JSON-LD : tous les blocs parsent. Le FAQPage reprend mot pour mot la FAQ visible. Aucune note ni aucun avis inventé.
- Sitemap : 23 URL = exactement les pages indexables (sans noindex ni redirection).
- HTML : balises équilibrées, ids uniques (contrôle automatique).
- Mobile 375 px : 0 débordement horizontal sur les 17 pages (détection des éléments qui dépassent). Captures pleine page : `docs/specs/seo-screens/*.jpg`.
- À faire après mise en ligne (non testable en local) : test des résultats enrichis Google (`search.google.com/test/rich-results`) sur 2 pages, et PageSpeed Insights mobile sur le hub.

## 5. Maintenance : comment ajouter ou modifier une page

Les pages SEO sont **générées** par `docs/specs/seo-src/build.py`, à partir des contenus `c1.py` à `c4.py` : un dict par page (title, description, h1, corps HTML, FAQ, pages liées). Le gabarit (head, JSON-LD, header, fil d’Ariane, CTA, footer) est centralisé, ce qui évite de modifier 17 footers à la main.

```bash
python3 docs/specs/seo-src/build.py c1 c2 c3 c4   # régénère les 17 pages
```

Ajouter une notion : ajouter un dict dans un `cN.py` et une ligne dans `NOTIONS` (build.py) pour le footer et le hub, puis régénérer. Il faut aussi ajouter l’URL à `sitemap.xml` et le fichier à `.claspignore`. **Ne pas éditer le `.html` directement** : la prochaine génération écraserait la modification.

## 6. Plan SEO des 3 prochains mois (octobre → décembre 2026)

### Semaine 1 (à la mise en ligne) : Nicolas, environ 30 min

**Google Search Console, propriété « Domaine » (couvre http, https et www)**
1. Ouvrir `https://search.google.com/search-console` avec le compte Google de Matheux → « Ajouter une propriété » → type **Domaine** → saisir `matheux.fr` → copier l’enregistrement `google-site-verification=…`.
2. IONOS : « Domaines & SSL » → `matheux.fr` → onglet **DNS** → « Ajouter un enregistrement » → **TXT**, nom d’hôte `@`, valeur = le texte copié → Enregistrer. Ne pas toucher aux enregistrements existants (Resend, GitHub Pages).
3. Revenir dans la GSC → « Valider ». La propagation DNS prend de quelques minutes à quelques heures. Si la validation échoue, réessayer plus tard.
4. Menu **Sitemaps** → saisir `sitemap.xml` → Envoyer. Statut attendu : « Opération effectuée », 23 URL détectées.
5. **Inspection de l’URL** → coller `https://matheux.fr/` → « Demander une indexation ». Répéter pour le hub, la page Brevet 2027, la page parents, Pythagore, Thalès, trigonométrie et fonction affine (environ 10 demandes par jour maximum).
6. Paramètres → Associations → lier la propriété GA4 (`G-7R2DW4585Y`).

**Bing Webmaster Tools** (Bing, Ecosia et DuckDuckGo) : `https://www.bing.com/webmasters` → se connecter → « Importer depuis Google Search Console ». La propriété et le sitemap sont repris automatiquement, sans DNS supplémentaire.

**Contrôles** : test des résultats enrichis sur `/pythagore-brevet.html` (fil d’Ariane et FAQ détectés) et PageSpeed Insights mobile sur `/exercices-maths-3eme.html`.

### Octobre : indexation et premières mesures
- Au bout de 2 semaines, rapport GSC « Pages ». Il est normal de voir `app.html`, `bilan.html`, `404`, `offline` et `unsubscribe` en « Exclue par la balise noindex », et `brevet-2026.html` et `premium.html` en « Page avec redirection ». À corriger en revanche : « Explorée, actuellement non indexée » sur une page notion (enrichir la page ou la lier davantage).
- **Contenu (2 pages)** : `proportionnalite-pourcentages-3eme.html` (pourcentages, évolutions, vitesse) et `grandeurs-mesures-3eme.html` (volumes, conversions, agrandissement-réduction). Ce sont les deux thèmes du programme encore sans page.
- **Backlinks honnêtes** : un post LinkedIn de Nicolas (histoire du projet et de la cause racine, lien vers la page parents), une réponse utile et signée sur 2 ou 3 fils de forums parents qui posent la question, et l’envoi de la page Brevet 2027 aux collèges et aux associations de parents d’élèves (FCPE ou PEEP locales) qui connaissent Nicolas.

### Novembre : consolider ce qui démarre
- GSC → Performances → requêtes : repérer les pages en position 8-20 avec des impressions. Pour chacune, retravailler le title et l’intro autour de la requête réelle, et ajouter 1 exercice et 1 question FAQ.
- **Contenu (2 pages)** : `algorithmique-scratch-3eme.html` (un exercice tombe presque chaque année) et `transformations-3eme.html` (symétries, translation, rotation, homothétie).
- **Annuaires éducation** : 3 à 5 inscriptions dans des annuaires ou listes de ressources éducatives **modérés** (pages ressources de CDI ou d’ENT, sites de profs qui recensent des outils gratuits). Éviter les annuaires payants et les échanges de liens, que Google pénalise.
- Recenser les demandes réelles des parents (emails, `contact@`) : chaque question qui revient donne une FAQ ou une page.

### Décembre : préparer le pic du printemps
- **Contenu** : `brevet-blanc-maths-3eme.html` (préparer le brevet blanc de janvier et février : sujet d’entraînement maison corrigé). Mise à jour de la page Brevet 2027 si le BO précise les horaires.
- Maillage : ajouter aux pages notions un lien « exercice type Brevet » vers le problème correspondant de la page Brevet.
- Bilan à 3 mois : impressions, clics et CTR par page, `cta_click` par source `seo_*`, et diagnostics démarrés depuis le SEO. On arbitre ensuite : doubler les pages qui convertissent, fusionner celles qui n’ont aucune impression.

### Calendrier éditorial (repères annuels)
| Mois | Sujet porteur |
|---|---|
| septembre-octobre | rentrée de 3e, parents inquiets (page parents, hub) |
| janvier-février | brevets blancs, « comment réviser » |
| mars-mai | pages notions, automatismes, sujets type |
| juin | page Brevet 2027 (date, format), dernière ligne droite. Après l’épreuve : corrigé maison du sujet 2027, si Nicolas a le temps de le rédiger |

## ❓ Pour Nicolas

1. **Pages générées** : j’ai commité le générateur (`docs/specs/seo-src/`) pour que les 17 pages restent cohérentes. OK ? → Reco : oui. On modifie les `.py` puis on régénère, et on ne touche pas au HTML à la main.
2. **CGV** : `cgv.html` affiche encore « 29,99 € — accès jusqu’au Brevet 2026 ». Ce n’est pas du SEO, mais ce texte est indexé et contredit la landing. → Reco : le faire corriger par l’agent légal (52-legal) avant de pousser `main`.
3. **Date du Brevet sur la landing** : le calendrier 2027 est paru (écrits les 24, 25 et 28 juin 2027). → Reco : remplir `CONFIG.brevet.date = '2027-06-24'` dans `index.html` (agent landing) pour afficher le décompte, et remplacer « date officielle pas encore publiée ».
4. **`docs/` est public** : GitHub Pages sert aussi `matheux.fr/docs/…`. Je l’ai exclu du crawl, mais il reste accessible à qui connaît l’URL. → Reco : OK tant que le dépôt est public de toute façon. Sinon, déplacer la doc hors de la branche servie.
5. **Search Console** : tu la configures en suivant le §6 (environ 30 min) ? → Reco : oui, dès la mise en ligne. Sans elle, on pilote à l’aveugle.
