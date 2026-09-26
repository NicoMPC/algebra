# Générateur des pages SEO Matheux (sortie = HTML statique à la racine du repo, committé).
# Usage : python3 docs/specs/seo-src/build.py c1 c2 c3 c4   (c1-c4 = contenus ; voir docs/specs/70-seo.md §5)
# ⚠️ Une page régénérée écrase le HTML : modifier le contenu ICI, pas dans le .html.
import json, re, html, os, sys, importlib
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
SITE = 'https://matheux.fr'
TODAY = '2026-09-26'
HUB = '/exercices-maths-3eme.html'

def F(a, b):
    return f'<span class="fr"><span>{a}</span><span>{b}</span></span>'

def M(s):
    # expressions longues : découpées en morceaux insécables, avec des coupures possibles avant « = », « + », « − »
    if len(s) <= 24:
        return f'<span class="m">{s}</span>'
    parts = s.split(' = ')
    chunks = [parts[0]] + ['= ' + p for p in parts[1:]]
    out = []
    for c in chunks:
        if len(c) <= 26:
            out.append(c); continue
        cur = ''
        for tok in re.split(r'(?= [+−] )', c):
            if cur and len(cur) + len(tok) > 26:
                out.append(cur); cur = tok.lstrip()
            else:
                cur += tok
        out.append(cur)
    return ' '.join(f'<span class="m">{c}</span>' for c in out)

# Pages notions : (url, libellé court, description courte pour le hub/footer)
NOTIONS = [
    ('/calcul-litteral-3eme.html', 'Calcul littéral', 'Développer, factoriser, identités remarquables'),
    ('/equations-3eme.html', 'Équations', 'Premier degré, produit nul, x² = a, mise en équation'),
    ('/fonctions-3eme.html', 'Fonctions', 'Image, antécédent, lecture graphique'),
    ('/fonction-affine-3eme.html', 'Fonction affine et linéaire', 'Coefficients a et b, droite, proportionnalité'),
    ('/puissances-3eme.html', 'Puissances', 'Règles de calcul, puissances de 10, notation scientifique'),
    ('/racine-carree-3eme.html', 'Racine carrée', 'Définition, carrés parfaits, calculs, x² = a'),
    ('/arithmetique-3eme.html', 'Arithmétique', 'Nombres premiers, décomposition, problèmes de partage'),
    ('/fractions-brevet.html', 'Fractions', 'Simplifier, additionner, multiplier, diviser'),
    ('/pythagore-brevet.html', 'Théorème de Pythagore', 'Longueur, réciproque, rédaction'),
    ('/thales-brevet.html', 'Théorème de Thalès', 'Longueur, configuration papillon, réciproque'),
    ('/trigonometrie-3eme.html', 'Trigonométrie', 'Cosinus, sinus, tangente : longueur et angle'),
    ('/probabilites-brevet.html', 'Probabilités', 'Équiprobabilité, événement contraire, arbre'),
    ('/statistiques-brevet.html', 'Statistiques', 'Moyenne, médiane, étendue, comparer deux séries'),
]
RESSOURCES = [
    ('/exercices-maths-3eme.html', 'Toutes les notions de 3e'),
    ('/exercices-maths-3eme-brevet.html', 'Brevet de maths 2027 : exercices type'),
    ('/comment-reviser-brevet-maths.html', 'Comment réviser le Brevet de maths'),
    ('/difficultes-maths-3eme.html', 'Parents : difficultés en maths en 3e'),
]

def strip(h):
    t = re.sub(r'<[^>]+>', ' ', h)
    t = html.unescape(t)
    return re.sub(r'\s+', ' ', t).strip()

def fr_frac_text(h):
    # pour le JSON-LD : 3/4 lisible à la place des fractions empilées
    return re.sub(r'<span class="fr"><span>(.*?)</span><span>(.*?)</span></span>', lambda m: f'{m.group(1)}/{m.group(2)}' if len(strip(m.group(1)))<4 and len(strip(m.group(2)))<4 else f'({m.group(1)})/({m.group(2)})', h)

def footer():
    notions = ''.join(f'<li><a href="{u}">{l}</a></li>' for u, l, _ in NOTIONS)
    res = ''.join(f'<li><a href="{u}">{l}</a></li>' for u, l in RESSOURCES)
    return f'''<footer class="ftr">
  <div class="wrap">
    <div class="ftr-g">
      <div>
        <a class="brand" href="/"><img src="/assets/mark-white.png" alt="" width="29" height="24">Matheux</a>
        <p style="margin-top:.7rem">Diagnostic et entraînement en maths pour la 3e, conçus par un ancien ingénieur qui accompagne des élèves en maths depuis des années.<br><a href="mailto:contact@matheux.fr">contact@matheux.fr</a></p>
      </div>
      <nav aria-label="Notions de 3e"><h2>Notions de 3e</h2><ul>{notions}</ul></nav>
      <nav aria-label="Brevet"><h2>Brevet</h2><ul>{res}<li><a href="/app.html#login">Connexion</a></li></ul></nav>
      <nav aria-label="Informations légales"><h2>Légal</h2><ul><li><a href="/mentions-legales.html">Mentions légales</a></li><li><a href="/cgu.html">CGU</a></li><li><a href="/cgv.html">CGV</a></li><li><a href="/politique-confidentialite.html">Confidentialité</a></li><li><a href="/politique-cookies.html">Cookies</a></li></ul></nav>
    </div>
    <div class="copy">© 2026 Matheux · Nicolas Follezou · Fait en France</div>
  </div>
</footer>'''

def page(p):
    url = SITE + p['path']
    src = p['src']
    cta = f'/app.html#diag-seo_{src}'
    crumbs = [('Accueil', SITE + '/')]
    if p['path'] != HUB:
        crumbs.append(('Maths 3e', SITE + HUB))
    crumbs.append((p['crumb'], url))
    crumbs_html = ''.join(
        (f'<li><a href="{u.replace(SITE, "") or "/"}">{n}</a></li>' if i < len(crumbs) - 1 else f'<li aria-current="page">{n}</li>')
        for i, (n, u) in enumerate(crumbs))
    graph = [{
        '@type': 'BreadcrumbList',
        'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u} for i, (n, u) in enumerate(crumbs)]
    }]
    org = {'@type': 'Organization', 'name': 'Matheux', 'url': SITE + '/', 'logo': SITE + '/icons/icon-512.png'}
    author = {'@type': 'Person', 'name': 'Nicolas Follezou', 'description': "Ancien ingénieur, accompagne des élèves en maths (soutien scolaire) depuis des années"}
    kind = p.get('kind', 'learning')
    if kind == 'learning':
        graph.append({
            '@type': 'LearningResource', '@id': url + '#ressource', 'name': p['h1_text'], 'description': p['desc'], 'url': url,
            'inLanguage': 'fr-FR', 'educationalLevel': '3e (collège, cycle 4)',
            'learningResourceType': ['Cours', 'Exercices corrigés'],
            'teaches': p['teaches'], 'isAccessibleForFree': True,
            'audience': {'@type': 'EducationalAudience', 'educationalRole': 'student'},
            'author': author, 'publisher': org, 'dateModified': TODAY
        })
    elif kind == 'article':
        graph.append({'@type': 'Article', 'headline': p['h1_text'], 'description': p['desc'], 'url': url, 'inLanguage': 'fr-FR',
                      'author': author, 'publisher': org, 'dateModified': TODAY, 'image': SITE + '/assets/og.png'})
    elif kind == 'hub':
        graph.append({'@type': 'CollectionPage', 'name': p['h1_text'], 'description': p['desc'], 'url': url, 'inLanguage': 'fr-FR',
                      'publisher': org, 'dateModified': TODAY,
                      'mainEntity': {'@type': 'ItemList', 'itemListElement': [
                          {'@type': 'ListItem', 'position': i + 1, 'url': SITE + u, 'name': l} for i, (u, l, _) in enumerate(NOTIONS)]}})
    faq = p.get('faq', [])
    if faq:
        graph.append({'@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': strip(q), 'acceptedAnswer': {'@type': 'Answer', 'text': strip(fr_frac_text(a))}} for q, a in faq]})
    ld = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=1)
    toc = ''
    if p.get('toc'):
        toc = '<nav class="toc" aria-label="Sommaire"><p>Sommaire</p><ol>' + ''.join(f'<li><a href="#{i}">{t}</a></li>' for i, t in p['toc']) + '</ol></nav>'
    faq_html = ''
    if faq:
        faq_html = '<section id="faq"><h2>Questions fréquentes</h2>' + ''.join(
            f'<details><summary>{q}</summary><div><p>{a}</p></div></details>' for q, a in faq) + '</section>'
    rel = p.get('related', [])
    rel_html = ''
    if rel:
        lab = {u: l for u, l, _ in NOTIONS}
        lab.update({u: l for u, l in RESSOURCES})
        rel_html = '<section id="aussi"><h2>À réviser aussi</h2><ul class="pills">' + ''.join(
            f'<li><a href="{u}">{lab[u]}</a></li>' for u in rel) + '</ul></section>'
    cta_box = p.get('cta_box') or (
        f'<div class="cta-box"><h2>{p.get("cta_title", "Et toi, où tu en es ?")}</h2>'
        f'<p>{p.get("cta_text", "Le diagnostic Matheux teste tes compétences de 3e et remonte aux notions des années précédentes quand c’est là que ça coince. Tu obtiens ta carte de compétences, puis 5 exercices par jour sur tes vrais points faibles.")}</p>'
        f'<a class="btn btn-cta" href="{cta}">Faire le diagnostic gratuit →</a><p class="micro">~8 min · 15 questions · sans carte bancaire</p></div>')
    nb = lambda h: re.sub(r' ([?!;:»])', '&nbsp;\\1', h).replace('« ', '«&nbsp;')
    body = nb(p['body'].replace('{CTA_BOX}', cta_box).replace('{CTA}', cta))
    faq_html = nb(faq_html)
    og_title = p.get('og_title', p['title'].split(' | ')[0])
    out = f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{p['title']}</title>
<meta name="description" content="{html.escape(p['desc'], quote=True)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0F172A">
<meta property="og:type" content="{'website' if kind == 'hub' else 'article'}">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Matheux">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{html.escape(og_title, quote=True)}">
<meta property="og:description" content="{html.escape(p['desc'], quote=True)}">
<meta property="og:image" content="{SITE}/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="32x32" href="/icons/favicon-32.png">
<link rel="apple-touch-icon" href="/icons/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,700&family=Syne:wght@800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/seo.css">
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
<a class="skip" href="#contenu">Aller au contenu</a>
<header class="hdr">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Matheux, accueil"><img src="/assets/mark-white.png" alt="" width="29" height="24">Matheux</a>
    <nav aria-label="Navigation principale">
      <a class="l hide-xs" href="{HUB}">Notions 3e</a>
      <a class="btn btn-cta btn-sm" href="{cta}">Diagnostic gratuit</a>
    </nav>
  </div>
</header>
<main id="contenu">
<div class="hero">
  <div class="wrap narrow">
    <nav class="crumbs" aria-label="Fil d’Ariane"><ol>{crumbs_html}</ol></nav>
    <p class="eyebrow">{p['eyebrow']}</p>
    <h1>{nb(p['h1'])}</h1>
    <p class="lead">{nb(p['lead'])}</p>
    <a class="btn btn-cta" href="{cta}">{p.get('hero_cta', 'Tester mon niveau gratuitement →')}</a>
    <p class="micro">~8 min · 15 questions · sans carte bancaire</p>
  </div>
</div>
<div class="wrap narrow art">
<p class="updated">Mis à jour le 26 septembre 2026 · par Nicolas Follezou, fondateur de Matheux</p>
{toc}
{body}
{faq_html}
{rel_html}
</div>
</main>
{footer()}
</body>
</html>
'''
    path = os.path.join(ROOT, p['path'].lstrip('/'))
    open(path, 'w', encoding='utf-8').write(out)
    words = len(strip(p['body'] + ''.join(q + a for q, a in faq)).split())
    print(f"{p['path']:40s} {len(out)/1024:5.1f} Ko  ~{words} mots (corps+FAQ)")

if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(__file__))
    for modname in sys.argv[1:]:
        mod = importlib.import_module(modname)
        for p in mod.PAGES:
            page(p)
