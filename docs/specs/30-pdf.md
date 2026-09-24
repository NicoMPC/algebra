# 30 — PDF « Bilan de compétences » (livrable Dev PDF)

> Statut : prototype fonctionnel, testé dans Chrome headless (24/09/2026). Pas branché dans `app.html`.
> Fichiers : `js/bilan-pdf.js`, `js/bilan-pdf-assets/`, `bilan-preview.html`, `docs/specs/exemples-pdf/`.

## 1. API

```js
// <script src="js/bilan-pdf.js"></script>  (vanilla, sans module ES, sans bundler)
MatheuxBilanPDF.render(carte, opts) → Promise<{ blob, url, fileName, pageCount, fontsEmbedded }>
```

| `opts` | Défaut | Rôle |
|---|---|---|
| `apercu` | `false` | `true` : couverture + carte, puis 1 page « ce que contient le bilan complet » (sections visibles, contenu remplacé par des barres grises, **aucune donnée réelle dessinée**) + encart d'achat |
| `cta` | `{}` | `{ label, prix, url, texte }` de l'encart d'achat (aperçu uniquement). `url` rend le bouton cliquable dans le PDF. **Le prix n'est pas codé en dur** : l'appelant le passe |
| `maxErreurs` | `3` | nombre de cartes « erreur type » (3 = 1 page A4) |
| `assetBase` | `<dossier du script>/bilan-pdf-assets/` | dossier des polices et logos |
| `loadAsset` | `fetch` | `(fichier) → Promise<base64>` (injection, comme HUMANA) |
| `jsPDFUrl` | jsdelivr `jspdf@2.5.2` UMD | chargé à la demande si `window.jspdf` absent |

Nom de fichier : `Bilan-maths-3e_<Prenom-sans-accent>_<date>[_apercu].pdf`.

## 2. Contrat d'entrée (objet Carte, contrat §5)

Lus : `eleve.prenom`, `eleve.niveau`, `type`, `date` (ISO), `duree_min`, `n_questions`
(→ footer « généré à partir de N réponses »), `score_global` (0-100), `domaines[]`
(`code`, `libelle`, `maitrise`, `statut`, `n_comp`, `n_lacunes`), `competences[]`, `priorites[]`,
`plan_4_semaines[]` (`semaine`, `focus[]`, `objectif`), `points_forts[]`, `message_parent`.

Par compétence : `id`, `titre` (sinon `titre_eleve`), `statut` (`lacune|fragile|acquis|non_evalue`,
sinon déduit de `maitrise` avec les seuils 0.4 / 0.7), `maitrise` (`null` = non évalué),
`cause_racine`, `bloque[]`, `erreurs[]`.

**Champs optionnels ajoutés (le moteur peut les fournir, sinon fallback)** — à valider par le chef de projet :
- `competences[].niveau_origine` (ex. `5EME`) → « notion de 5e » dans le graphe des causes. Copie directe du référentiel.
- `competences[].erreurs[].libelle_parent` et `.remediation` → copie directe du référentiel (§2). Sans eux, le PDF affiche `libelle` seul.
- `carte.phrase_cle` → phrase de couverture. Sinon générée : cause racine n°1 et nombre de notions bloquées, ou nombre de lacunes / fragiles.

Robustesse : un id cité dans `bloque`, `priorites` ou `focus` mais absent de `competences`
s'affiche comme « non évalué » avec son id. Carte minimale `{eleve, date, n_questions, score_global}` : 6 pages
sans crash (testé). Un exemple (`exemple.q`, `exemple.a`) accepte du LaTeX `$…$` ou du texte brut (`7/12`, `x^2`, `sqrt(25)`, `5 cm`).

## 3. Contenu (6 pages en complet, 3 en aperçu)

1. **Couverture** : logo, « Bilan de compétences · maths 3e », prénom, date · durée · N réponses, anneau score global,
   phrase-clé, 4 compteurs par statut (+ « dont N causes racines »), top 3 priorités, 3 points forts, légende de lecture.
2. **La carte** : 5 jauges domaine (repères 40 % / 70 %), puis toutes les compétences en 2 colonnes, groupées par domaine,
   triées lacune → fragile → acquis → non évalué. Pastilles dessinées (pas d'emoji), étiquette « CAUSE RACINE ».
3. **Ce qui bloque vraiment** : un schéma par cause racine (nœud cause → courbes fléchées → notions bloquées colorées
   par statut) + une phrase parent. Ensuite les « autres points à travailler » (lacunes/fragiles sans lien). Sans cause
   racine : encart vert « Aucune cause racine ».
4. **Les erreurs qui reviennent** : jusqu'à 3 cartes (priorités d'abord) : erreur en langage parent, détail technique,
   la vraie question, réponse de l'élève (croix) vs bonne réponse (coche), « ce qui aide ».
5. **Plan 4 semaines** : rythme (15 min · 5 jours/7 · 5 exercices), frise semaine par semaine avec objectif et
   compétences visées, puis « au bout de 4 semaines : nouveau diagnostic ».
6. **Pour les parents** : temps / moment / place, « ce qu'on peut dire » / « ce qu'on évite », 4 réflexes quand
   l'enfant bloque, encart final `message_parent`.

Footer sur chaque page : `matheux.fr` · « Bilan du <date> · généré à partir de N réponses » · pagination.

## 4. Choix de design

- **Architecture HUMANA reprise** : état `ctx.y`, un dessinateur par section, `ensure()` pour les sauts de page
  (en-tête redessiné), footer posé à la fin sur toutes les pages, polices injectées dans le VFS jsPDF à chaque document.
  Pas la charte HUMANA : charte Matheux d'`app.html` (`--mx-primary #1E40AF`, navy `#0F172A`, vert `#059669`,
  ambre `#F59E0B`, rouge `#DC2626`, gris ardoise).
- **Polices** : Syne Bold (titres) et DM Sans Regular/SemiBold/Bold (texte). Instances **statiques** extraites des fontes
  variables Google Fonts (jsPDF ne gère pas les axes variables), sous-ensemblées (latin étendu + `× ÷ − ≤ ≥ ≠ ≈ π √ → € « » ’ …`),
  ~135 Ko au total, licence OFL jointe. Accents français corrects (encodage Identity-H).
- **Fallback** : si les TTF ne se chargent pas (`file://`, réseau), Helvetica avec translittération des seuls caractères
  hors WinAnsi (`−`→`-`, `≤`→`<=`…). Accents conservés. `fontsEmbedded:false` permet de le détecter.
- **Maths sans KaTeX** : mini-moteur maison (≈200 lignes) pour un sous-ensemble LaTeX : `\frac` empilée, `^` et `_`,
  `\sqrt` (radical dessiné), `\widehat`/`\overline`/`\vec`, `\times \div \le \ge \neq \approx \pi \cdot`, `\text`,
  `\left( \right)`, espaces `\, \; \quad`, espacement des opérateurs binaires et moins unaire (U+2212).
  Réponses brutes converties : `7/12` → fraction, `sqrt(25)`, `x^2`, `5 cm` (unité gardée à part).
- **Typo française** : espaces insécables automatiques dans « … » et avant `: ; ! ? %`.
- **Ton parent** : vouvoiement, pas d'emoji, pas de jargon (« base », « bloque », « erreur type »), prénom partout (pas de il/elle).
- **Aperçu** : aucune donnée des pages payantes n'est dessinée (juste les titres, des compteurs du type « 2 causes racines
  identifiées » et des barres grises). Pas de vrai flou possible en jsPDF, et un flou sur du vrai texte resterait extractible.

## 5. Appel depuis `app.html` (à faire plus tard, pas touché ici)

```html
<script src="js/bilan-pdf.js" defer></script>
```
```js
async function downloadBilan(carte, apercu) {
  const r = await MatheuxBilanPDF.render(carte, {
    apercu,
    cta: { label: 'Débloquer le bilan', prix: PRIX_DIAGNOSTIC, url: _stripeUrl() } // prix : source unique côté app
  });
  const a = document.createElement('a');
  a.href = r.url; a.download = r.fileName; a.click();
  setTimeout(() => URL.revokeObjectURL(r.url), 10000);
}
```
Sur iOS Safari, `download` peut ouvrir le PDF dans un onglet (comportement normal). Le premier appel charge jsPDF
(~350 Ko) et les polices (~135 Ko), le PDF fait environ 250 Ko. Génération < 1 s sur desktop.

Test local : `python3 -m http.server` à la racine puis `http://localhost:8000/bilan-preview.html` (2 cartes fictives,
boutons complet / aperçu, rendu dans un iframe).

## 6. Vérifications faites

- Rendu réel via Chrome headless (puppeteer-core hors repo), PDF → PNG (`pdftoppm`), relu page par page.
- 4 exemples dans `docs/specs/exemples-pdf/` (PDF + planche PNG) : Léa (2 causes racines relatifs/fractions, 49 %), Hugo (81 %, 2 fragiles, aucune cause racine), versions complète et aperçu.
- Cas limites : prénom long (taille réduite automatiquement), 55 compétences (la carte passe sur 2 pages avec en-têtes
  « (suite) »), carte minimale vide, polices indisponibles (fallback) : aucun crash, aucun débordement vu.

## 7. Limites connues

- Pages 3 et 4 : beaucoup de causes racines ou de points isolés = page supplémentaire (le PDF passe à 7-8 pages, sans casse).
- LaTeX hors sous-ensemble (matrices, `\begin{…}`, `\overbrace`…) : le nom de la commande s'affiche en texte. Suffisant pour le collège.
- Pas d'italique mathématique (variables en romain) : choix de lisibilité, pas de 5e fonte à charger.
- Pas de figure géométrique dans les exemples (une question qui dépend d'un schéma est peu lisible) : le moteur devrait privilégier des exemples sans figure.
- Graphe des causes : 1 niveau (cause → bloquées). Les chaînes plus profondes (A→B→C) ne sont pas dessinées.
- Seuils 40/70 % dupliqués ici (légende + déduction du statut) : ils doivent rester alignés sur le contrat §4.

## ❓ Questions pour Nicolas

1. **Aperçu : carte complète visible ?** Aujourd'hui l'aperçu montre les 2 premières pages en entier (toutes les compétences).
   Reco : garder comme ça, c'est ce qui prouve le sérieux. La valeur payante, ce sont les causes, les erreurs expliquées et le plan.
2. **Vouvoiement du parent** dans le PDF (l'app tutoie l'ado). Reco : oui, vouvoiement.
3. **« Notre regard sur <prénom> »** : signé « l'équipe Matheux » ou « Nicolas, prof de maths » ? Reco : pas de signature
   nominative tant que le texte est généré automatiquement.
4. **3 erreurs types max** pour tenir sur 1 page. Reco : 3.
5. **Mention légale en pied de page** (« document indicatif, ne remplace pas l'avis de l'enseignant ») ? Reco : oui, une ligne en page 6, à caler avec `52-legal.md`.
