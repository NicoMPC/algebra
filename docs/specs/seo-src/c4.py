from build import F, M, NOTIONS

PAGES = []

def cards(urls):
    lab = {u: (l, d) for u, l, d in NOTIONS}
    return '<ul class="grid">' + ''.join(f'<li><a class="card" href="{u}"><b>{lab[u][0]}</b><span>{lab[u][1]}</span></a></li>' for u in urls) + '</ul>'

# ─────────────────────────────── HUB
PAGES.append(dict(
    path='/exercices-maths-3eme.html', src='exercices_3eme', crumb='Maths 3e', kind='hub',
    title='Exercices de maths 3e corrigés : toutes les notions | Matheux',
    desc='Toutes les notions de maths de 3e : cours court, méthode, exercices corrigés et erreurs fréquentes. Calcul littéral, fonctions, Pythagore, Thalès…',
    og_title='Maths 3e : cours et exercices corrigés, notion par notion',
    eyebrow='Maths 3e · Programme · Brevet 2027',
    h1='Maths 3e : toutes les notions, avec exercices corrigés',
    h1_text='Maths 3e : toutes les notions du programme, avec exercices corrigés',
    lead='Une page par notion, construite de la même façon : l’essentiel à retenir, la méthode, des exercices corrigés pas à pas, et les erreurs que les élèves font le plus souvent. Choisis ta notion, ou commence par le diagnostic pour savoir laquelle travailler en premier.',
    body=f'''
<section id="nombres"><h2>Nombres et calculs</h2>
{cards(['/calcul-litteral-3eme.html', '/equations-3eme.html', '/fractions-brevet.html', '/puissances-3eme.html', '/racine-carree-3eme.html', '/arithmetique-3eme.html'])}
</section>
<section id="fonctions"><h2>Fonctions</h2>
{cards(['/fonctions-3eme.html', '/fonction-affine-3eme.html'])}
</section>
<section id="geometrie"><h2>Espace et géométrie</h2>
{cards(['/pythagore-brevet.html', '/thales-brevet.html', '/trigonometrie-3eme.html'])}
</section>
<section id="donnees"><h2>Statistiques et probabilités</h2>
{cards(['/statistiques-brevet.html', '/probabilites-brevet.html'])}
</section>

{{CTA_BOX}}

<section id="commencer"><h2>Par où commencer ?</h2>
<p>En 3e, beaucoup de difficultés ne viennent pas du chapitre en cours, mais d’une notion plus ancienne qui n’a jamais été solide. Quelques exemples typiques :</p>
<ul>
<li>un élève qui « rate Pythagore » confond souvent le carré et le double ({M('9² = 18')}) : le problème vient des <a href="/puissances-3eme.html">puissances</a> ;</li>
<li>un élève bloqué en <a href="/equations-3eme.html">équations</a> se trompe parfois sur les nombres relatifs ou sur le sens de {M('3x')} ;</li>
<li>les <a href="/fractions-brevet.html">fractions</a> reviennent dans les probabilités, Thalès et les automatismes.</li>
</ul>
<p>Si tu ne sais pas par où commencer, reprends tes derniers contrôles et note où tu as perdu des points. Tu peux aussi faire le diagnostic Matheux : il remonte aux notions des années précédentes quand c’est là que se trouve la cause.</p>
</section>

<section id="programme"><h2>Le programme de maths de 3e en bref</h2>
<p>La 3e termine le cycle 4 (5e, 4e, 3e). Le programme est organisé en cinq thèmes : <strong>nombres et calculs</strong>, <strong>organisation et gestion de données, fonctions</strong>, <strong>grandeurs et mesures</strong>, <strong>espace et géométrie</strong>, <strong>algorithmique et programmation</strong>. Le Brevet peut porter sur l’ensemble du cycle 4, pas seulement sur les nouveautés de 3e.</p>
<p>Les pages ci-dessus couvrent les notions qui reviennent le plus dans les exercices. Les grandeurs et mesures (volumes, vitesses, conversions), les transformations et l’algorithmique (Scratch) sont évaluées dans le diagnostic et l’entraînement Matheux. Leurs pages de cours arrivent prochainement.</p>
<p>Pour l’épreuve elle-même, voir <a href="/exercices-maths-3eme-brevet.html">le Brevet de maths 2027 : format et exercices type</a> et <a href="/comment-reviser-brevet-maths.html">comment réviser efficacement</a>.</p>
</section>
''',
    faq=[
        ('Quelles sont les notions les plus importantes en maths en 3e ?', 'Celles qui servent partout : le calcul littéral, les équations, les fractions et les fonctions. En géométrie, Pythagore, Thalès et la trigonométrie reviennent très souvent au Brevet. Mais la notion la plus importante pour toi est celle qui te bloque, et elle peut dater de la 5e ou de la 4e.'),
        ('Comment savoir quelles notions retravailler ?', 'Regarde où tu perds des points dans tes contrôles, en distinguant les erreurs de calcul des erreurs de méthode. Le diagnostic gratuit de Matheux le fait en environ 8 minutes : il donne une carte des compétences et repère les causes probables des erreurs.'),
        ('Les exercices de ces pages sont-ils gratuits ?', 'Oui. Toutes les pages de cours et leurs exercices corrigés sont en accès libre, sans inscription. Le diagnostic express et 5 exercices par jour sont également gratuits dans l’application.'),
        ('Ces pages suivent-elles le programme officiel ?', 'Oui, elles suivent le programme de mathématiques du cycle 4 en vigueur pour les élèves de 3e en 2026-2027, qui passent le Brevet en juin 2027.'),
    ],
))

# ─────────────────────────────── BREVET 2027 (format + exercices type)
PAGES.append(dict(
    path='/exercices-maths-3eme-brevet.html', src='exercices_brevet', crumb='Brevet de maths 2027',
    title='Brevet de maths 2027 : épreuve et exercices type corrigés',
    desc='Brevet de maths 2027 : date, durée, partie automatismes sans calculatrice et partie raisonnement. Questions d’automatismes et problèmes type Brevet corrigés.',
    eyebrow='Brevet 2027 · Mathématiques',
    h1='Brevet de maths 2027 : l’épreuve et des exercices type corrigés',
    h1_text='Brevet de maths 2027 : l’épreuve et des exercices type corrigés',
    lead='Deux heures, deux parties : des automatismes sans calculatrice, puis des problèmes où l’on attend un raisonnement rédigé. Voici comment se passe l’épreuve, avec des questions et des problèmes corrigés dans le même esprit.',
    teaches=['Format de l’épreuve de mathématiques du Brevet 2027', 'Automatismes sans calculatrice', 'Résolution de problèmes type Brevet'],
    toc=[('epreuve', 'L’épreuve en bref'), ('automatismes', 'Automatismes : 10 questions corrigées'), ('probleme-1', 'Problème 1 : géométrie'), ('probleme-2', 'Problème 2 : programmes de calcul'), ('conseils', 'Conseils pour le jour J'), ('faq', 'Questions fréquentes')],
    body=f'''
<section id="epreuve"><h2>L’épreuve de maths en bref</h2>
<div class="scroll"><table class="t">
<tr><th scope="row">Date</th><td>Lundi 28 juin 2027 au matin. Les écrits du Brevet ont lieu les 24, 25 et 28 juin 2027.</td></tr>
<tr><th scope="row">Durée</th><td>2 heures</td></tr>
<tr><th scope="row">Notation</th><td>sur 20 points</td></tr>
<tr><th scope="row">Partie 1 : automatismes</th><td>20 minutes, <strong>sans calculatrice</strong>, 6 points. Questions à réponse courte sur l’ensemble du cycle 4.</td></tr>
<tr><th scope="row">Partie 2 : raisonnement et résolution de problèmes</th><td>1 h 40, calculatrice autorisée, 14 points. Exercices souvent ancrés dans des situations concrètes, avec justifications attendues.</td></tr>
</table></div>
<p class="note">Sources : calendrier 2027 publié au Bulletin officiel spécial n° 2 du 25 août 2026 ; présentation de l’épreuve par les académies (par exemple <a href="https://mathematiques.ac-normandie.fr/DNB-2027" rel="noopener">académie de Normandie</a>). En cas de doute, la référence reste eduscol et ton professeur de mathématiques.</p>
<p>Deux points à garder en tête : les démarches sont prises en compte même quand elles n’aboutissent pas, et la qualité de la rédaction compte. Écris ce que tu cherches, même si tu ne finis pas.</p>
</section>

<section id="automatismes"><h2>Automatismes : 10 questions corrigées</h2>
<p>Fais-les sans calculatrice, en moins de 10 minutes, puis vérifie. Chaque question renvoie à la notion à revoir en cas d’erreur.</p>
<div class="scroll"><table class="t">
<tr><th>Question</th><th>Réponse</th><th>À revoir</th></tr>
<tr><td>1. Calculer 25 % de 80.</td><td>20</td><td><a href="/fractions-brevet.html">Fractions</a></td></tr>
<tr><td>2. Calculer {M('3,5 × 1 000')}.</td><td>3 500</td><td><a href="/puissances-3eme.html">Puissances de 10</a></td></tr>
<tr><td>3. Écrire 0,0042 en notation scientifique.</td><td>{M('4,2 × 10⁻³')}</td><td><a href="/puissances-3eme.html">Puissances</a></td></tr>
<tr><td>4. Calculer {M('(−3)²')}.</td><td>9</td><td><a href="/puissances-3eme.html">Puissances</a></td></tr>
<tr><td>5. Développer {M('3(x − 4)')}.</td><td>{M('3x − 12')}</td><td><a href="/calcul-litteral-3eme.html">Calcul littéral</a></td></tr>
<tr><td>6. Résoudre {M('2x + 5 = 17')}.</td><td>{M('x = 6')}</td><td><a href="/equations-3eme.html">Équations</a></td></tr>
<tr><td>7. Écrire {F('18', '24')} sous forme irréductible.</td><td>{F('3', '4')}</td><td><a href="/fractions-brevet.html">Fractions</a></td></tr>
<tr><td>8. On lance un dé équilibré. Probabilité d’obtenir un multiple de 3 ?</td><td>{F('2', '6')}{M(' = ')}{F('1', '3')}</td><td><a href="/probabilites-brevet.html">Probabilités</a></td></tr>
<tr><td>9. Image de −2 par {M('f(x) = x² + 1')} ?</td><td>5</td><td><a href="/fonctions-3eme.html">Fonctions</a></td></tr>
<tr><td>10. Encadrer {M('√50')} entre deux entiers consécutifs.</td><td>{M('7 < √50 < 8')}</td><td><a href="/racine-carree-3eme.html">Racine carrée</a></td></tr>
</table></div>
</section>

<section id="probleme-1"><h2>Problème 1 : une rampe de skate (géométrie)</h2>
<div class="ex"><h3>Énoncé</h3>
<div class="q"><p>Une rampe de skate a la forme d’un triangle rectangle. Sa hauteur est de 1,2 m et sa longueur au sol de 3,5 m.</p><ol><li>Calculer la longueur de la pente de la rampe.</li><li>Calculer l’angle entre la pente et le sol, arrondi au degré.</li><li>On veut une rampe moins raide, de même hauteur, dont la pente fait un angle de 15° avec le sol. Quelle doit être sa longueur au sol, arrondie au dixième de mètre ?</li></ol></div>
<div class="s"><span class="lbl">Correction</span><ol>
<li>Le triangle est rectangle, la pente est l’hypoténuse. D’après le théorème de <a href="/pythagore-brevet.html">Pythagore</a> : {M('pente² = 1,2² + 3,5² = 1,44 + 12,25 = 13,69')}, donc {M('pente = √13,69 = 3,7')} m.</li>
<li>Par rapport à l’angle au sol, 1,2 m est le côté opposé et 3,5 m le côté adjacent. {M('tan(angle) = ')}{F('1,2', '3,5')}, donc {M('angle ≈ 19°')} (touche {M('tan⁻¹')}). Voir <a href="/trigonometrie-3eme.html">trigonométrie</a>.</li>
<li>{M('tan(15°) = ')}{F('1,2', 'sol')}, donc {M('sol = ')}{F('1,2', 'tan(15°)')}{M(' ≈ 4,5')} m. Vérification : pour une rampe moins raide et de même hauteur, il faut plus de longueur au sol. 4,5 m est bien plus grand que 3,5 m.</li>
</ol></div></div>
</section>

<section id="probleme-2"><h2>Problème 2 : deux programmes de calcul</h2>
<div class="ex"><h3>Énoncé</h3>
<div class="q"><p>Programme A : choisir un nombre, le multiplier par 4, puis ajouter 3. Programme B : choisir un nombre, lui ajouter 2, puis multiplier le résultat par 3.</p><ol><li>Quels résultats obtient-on avec le nombre 5 ?</li><li>Quel nombre faut-il choisir pour obtenir le même résultat avec les deux programmes ?</li><li>Montrer que, pour n’importe quel nombre {M('x')}, la différence A − B est égale à {M('x − 3')}.</li></ol></div>
<div class="s"><span class="lbl">Correction</span><ol>
<li>A : {M('5 × 4 + 3 = 23')}. B : {M('(5 + 2) × 3 = 21')}.</li>
<li>Avec {M('x')} : A donne {M('4x + 3')} et B donne {M('3(x + 2) = 3x + 6')}. On résout {M('4x + 3 = 3x + 6')}, soit {M('x = 3')}. Vérification : A donne 15, B donne 15. Voir <a href="/equations-3eme.html">équations</a>.</li>
<li>{M('A − B = (4x + 3) − (3x + 6) = 4x + 3 − 3x − 6 = x − 3')}. Le calcul est valable pour tout {M('x')}, c’est une preuve. Deux exemples chiffrés n’auraient pas suffi. Voir <a href="/calcul-litteral-3eme.html">calcul littéral</a>.</li>
</ol></div></div>
</section>

{{CTA_BOX}}

<section id="conseils"><h2>Conseils pour le jour J</h2>
<ul>
<li><strong>Automatismes</strong> : réponds vite à ce que tu sais, et ne reste pas bloqué sur une question. 20 minutes passent très vite.</li>
<li><strong>Lis tout le sujet</strong> de la partie 2 avant de commencer, et commence par l’exercice où tu te sens le plus à l’aise.</li>
<li><strong>Rédige</strong> : cite le théorème, écris les calculs, conclus par une phrase avec l’unité.</li>
<li><strong>Vérifie l’ordre de grandeur</strong> : une hypoténuse plus courte qu’un côté, ou une probabilité supérieure à 1, signalent une erreur.</li>
<li><strong>Calculatrice en mode degrés</strong> : {M('cos(60)')} doit afficher 0,5.</li>
</ul>
</section>
''',
    faq=[
        ('Quand a lieu l’épreuve de maths du Brevet 2027 ?', 'Les écrits du Brevet 2027 ont lieu les jeudi 24, vendredi 25 et lundi 28 juin 2027. L’épreuve de mathématiques est prévue le lundi 28 juin au matin. Vérifie les horaires définitifs auprès de ton collège.'),
        ('La calculatrice est-elle autorisée au Brevet de maths ?', 'Pas pendant la partie automatismes (20 minutes, 6 points). Elle est autorisée pendant la partie raisonnement et résolution de problèmes (1 h 40, 14 points).'),
        ('Comment s’entraîner aux automatismes ?', 'Un peu chaque jour, sans calculatrice : calcul mental, fractions, puissances de 10, développements simples, équations simples, pourcentages. Dix minutes régulières valent mieux qu’une longue séance la veille.'),
        ('Quelles notions tombent le plus souvent au Brevet de maths ?', 'Sur les sujets des années passées, on retrouve très régulièrement le calcul littéral, les équations, les fonctions, Pythagore, Thalès, la trigonométrie, les statistiques et les probabilités, ainsi qu’un exercice d’algorithmique ou de tableur. Aucun sujet n’est prévisible à l’avance : il vaut mieux consolider ses points faibles que parier sur un chapitre.'),
    ],
    related=['/comment-reviser-brevet-maths.html', '/exercices-maths-3eme.html', '/pythagore-brevet.html', '/calcul-litteral-3eme.html', '/trigonometrie-3eme.html'],
))

# ─────────────────────────────── GUIDE RÉVISION
PAGES.append(dict(
    path='/comment-reviser-brevet-maths.html', src='guide', crumb='Réviser le Brevet', kind='article',
    title='Comment réviser le Brevet de maths : la méthode | Matheux',
    desc='Réviser le Brevet de maths 2027 : faire le point, traiter les causes des erreurs, s’entraîner peu mais souvent, automatismes. Méthode et planning.',
    eyebrow='Guide · Brevet 2027',
    h1='Comment réviser le Brevet de maths efficacement',
    h1_text='Comment réviser le Brevet de maths efficacement',
    hero_cta='Faire le point avec le diagnostic →',
    lead='Relire son cahier depuis la page 1 rassure, mais fait peu progresser. Ce qui marche, c’est de savoir précisément ce qui coince, de le retravailler un peu chaque jour, et de s’entraîner dans les conditions de l’épreuve. Voici la méthode, étape par étape, et un planning jusqu’en juin 2027.',
    teaches=['Méthode de révision du Brevet de mathématiques'],
    toc=[('point', '1. Faire le point'), ('causes', '2. Traiter les causes'), ('regularite', '3. Peu, mais souvent'), ('automatismes', '4. Les automatismes'), ('sujets', '5. S’entraîner sur des sujets'), ('planning', 'Planning jusqu’en juin'), ('parents', 'Parents : comment aider'), ('faq', 'Questions fréquentes')],
    body=f'''
<section id="point"><h2>1. Faire le point, plutôt que « tout revoir »</h2>
<p>Revoir tout le programme dans l’ordre prend beaucoup de temps, et la plupart de ce temps passe sur des notions déjà acquises. Commence par identifier les 2 ou 3 notions qui te coûtent vraiment des points.</p>
<p>Pour cela, reprends tes derniers contrôles et classe tes erreurs : erreur d’inattention, méthode inconnue, ou notion jamais comprise. Seules les deux dernières catégories méritent une vraie révision. Le diagnostic Matheux fait ce travail en environ 8 minutes, en mesurant chaque compétence séparément.</p>
</section>

<section id="causes"><h2>2. Traiter les causes, pas les symptômes</h2>
<p>Une erreur au Brevet a souvent une cause plus ancienne. Un élève qui échoue sur <a href="/pythagore-brevet.html">Pythagore</a> peut très bien connaître le théorème, mais calculer {M('7² = 14')}. Refaire des exercices de Pythagore ne corrigera rien : il faut retravailler les <a href="/puissances-3eme.html">carrés</a>. De même, beaucoup de difficultés en <a href="/equations-3eme.html">équations</a> viennent des nombres relatifs, et beaucoup d’erreurs en probabilités viennent des <a href="/fractions-brevet.html">fractions</a>.</p>
<p>Quand une erreur revient, pose-toi la question : « quelle notion plus simple dois-je maîtriser pour réussir ça ? » Chaque page notion de ce site liste les erreurs typiques et leur cause.</p>
</section>

<section id="regularite"><h2>3. Peu, mais souvent</h2>
<p>Deux principes sont bien établis par la recherche sur la mémoire. L’<strong>espacement</strong> : répartir les révisions sur plusieurs jours fonctionne mieux que tout faire d’un coup. La <strong>récupération</strong> : essayer de retrouver une méthode ou un résultat par soi-même (faire un exercice, réciter une formule) fixe mieux que relire.</p>
<p>Concrètement, 10 à 15 minutes par jour, avec quelques exercices ciblés, valent mieux qu’une longue séance le dimanche. Quand tu bloques, cherche un indice plutôt que la correction complète : tu continues à raisonner.</p>
</section>

<section id="automatismes"><h2>4. Travailler les automatismes</h2>
<p>La première partie de l’épreuve dure 20 minutes, sans calculatrice, pour 6 points sur 20. Elle récompense les réflexes : calcul mental, fractions, pourcentages, puissances de 10, développements et équations simples, lecture de graphiques. C’est la partie où la régularité paie le plus vite. Quelques questions par jour suffisent. Tu trouveras <a href="/exercices-maths-3eme-brevet.html#automatismes">10 questions corrigées</a> pour te tester.</p>
</section>

<section id="sujets"><h2>5. S’entraîner sur des sujets type Brevet</h2>
<p>La deuxième partie demande autre chose : lire un énoncé long, repérer la notion en jeu, enchaîner des questions liées et <strong>rédiger</strong>. À partir du deuxième trimestre, fais régulièrement des exercices complets de sujets des années précédentes, en temps limité, puis compare ta rédaction à la correction. Cite le théorème utilisé, écris les calculs, conclus par une phrase avec l’unité.</p>
</section>

{{CTA_BOX}}

<section id="planning"><h2>Un planning jusqu’en juin 2027</h2>
<div class="scroll"><table class="t">
<tr><th>Période</th><th>Objectif</th></tr>
<tr><td>Septembre – décembre</td><td>Faire le point, puis consolider les bases qui bloquent : fractions, relatifs, puissances, calcul littéral. 10 minutes par jour.</td></tr>
<tr><td>Janvier – mars</td><td>Suivre les notions de 3e au fil du cours (fonctions, trigonométrie, probabilités…), continuer les automatismes, commencer les exercices de sujets.</td></tr>
<tr><td>Avril – mai</td><td>Un exercice de sujet complet par semaine, en temps limité. Au moins un sujet entier en conditions réelles (2 heures).</td></tr>
<tr><td>Juin</td><td>Révisions légères, ciblées sur les erreurs qui reviennent. Pas de nouvelle notion la dernière semaine.</td></tr>
</table></div>
<p>Si tu commences plus tard, garde la même logique : d’abord le point, puis les causes, puis l’entraînement en conditions réelles.</p>
</section>

<section id="parents"><h2>Parents : comment aider sans faire à la place</h2>
<ul>
<li><strong>Aidez à voir clair</strong> : une moyenne de maths ne dit pas ce qui bloque. Un bilan par compétence permet de savoir quoi travailler.</li>
<li><strong>Protégez la régularité</strong> plutôt que la durée : un créneau court et fixe, tous les jours, fonctionne mieux que de longues séances.</li>
<li><strong>Valorisez l’effort et la méthode</strong>, pas seulement la note. Une erreur comprise est un progrès.</li>
<li><strong>Parlez-en au professeur</strong> de maths : il sait ce qui a été vu en classe et ce qui est attendu.</li>
</ul>
<p>Pour aller plus loin : <a href="/difficultes-maths-3eme.html">mon enfant a des difficultés en maths en 3e, que faire ?</a></p>
</section>
''',
    faq=[
        ('Combien de temps faut-il pour réviser le Brevet de maths ?', 'Il n’y a pas de durée unique. Pour la plupart des élèves, 10 à 15 minutes par jour pendant plusieurs mois, ciblées sur leurs points faibles, sont plus efficaces que de longues séances de dernière minute. Plus tôt tu commences, moins chaque séance a besoin d’être longue.'),
        ('Par quoi commencer ses révisions de maths ?', 'Par un état des lieux : quelles notions te font perdre des points, et pourquoi. Ensuite, retravaille en priorité les bases qui servent partout (fractions, calcul littéral, équations), puis les notions de 3e.'),
        ('Faut-il faire des annales du Brevet ?', 'Oui, surtout à partir du deuxième trimestre, pour s’habituer aux énoncés longs, au temps limité et à la rédaction. Avant, il est plus rentable de consolider les notions qui bloquent.'),
        ('Le Brevet de maths est-il difficile ?', 'Il évalue les connaissances du cycle 4, de la 5e à la 3e. La difficulté vient rarement des notions de 3e elles-mêmes, et plus souvent de lacunes anciennes qui gênent partout. Les identifier tôt change beaucoup de choses.'),
    ],
    related=['/exercices-maths-3eme-brevet.html', '/exercices-maths-3eme.html', '/difficultes-maths-3eme.html', '/calcul-litteral-3eme.html', '/fractions-brevet.html'],
))

# ─────────────────────────────── PAGE PARENTS
PAGES.append(dict(
    path='/difficultes-maths-3eme.html', src='parents_difficultes', crumb='Difficultés en maths', kind='article',
    title='Mon enfant a des difficultés en maths en 3e : que faire ?',
    desc='Votre enfant de 3e est en difficulté en maths ? Comprendre d’où viennent les blocages, repérer la vraie cause, et les solutions concrètes avant le Brevet 2027.',
    og_title='Difficultés en maths en 3e : trouver la cause avant de chercher une solution',
    eyebrow='Pour les parents · 3e',
    h1='Mon enfant a des difficultés en maths en 3e : que faire ?',
    h1_text='Mon enfant a des difficultés en maths en 3e : que faire ?',
    hero_cta='Faire le diagnostic gratuit avec mon enfant →',
    lead='« Il est nul en maths », « elle n’a jamais aimé ça »… En 3e, avec le Brevet en ligne de mire, l’inquiétude monte. Pourtant, un élève en difficulté en maths l’est rarement partout. Le plus souvent, il bute sur quelques notions précises, parfois anciennes. La première étape est de les identifier.',
    teaches=['Identifier l’origine des difficultés en mathématiques en 3e'],
    toc=[('pourquoi', 'Pourquoi ça coince en 3e'), ('signes', 'Les signes à observer'), ('cause', 'Trouver la vraie cause'), ('solutions', 'Les solutions possibles'), ('matheux', 'Ce que propose Matheux'), ('faq', 'Questions fréquentes')],
    cta_title='Commencer par un état des lieux',
    cta_text='Le diagnostic express est gratuit et prend environ 8 minutes. Votre enfant obtient une carte de ses compétences en maths de 3e, qui distingue ce qui est acquis, fragile ou à reprendre, et remonte aux notions des années précédentes quand c’est nécessaire.',
    body=f'''
<section id="pourquoi"><h2>Pourquoi les difficultés apparaissent (ou s’aggravent) en 3e</h2>
<p>Les mathématiques s’empilent : chaque notion s’appuie sur les précédentes. En 3e, presque tout ce qui a été vu depuis la 5e est remobilisé. Le calcul littéral suppose les nombres relatifs, Pythagore suppose les carrés, les probabilités supposent les fractions. Une notion restée fragile en 5e peut passer inaperçue pendant deux ans, puis faire échouer plusieurs chapitres à la fois.</p>
<p>C’est pour cela qu’un élève peut avoir l’impression de « ne rien comprendre ». En réalité, il manque souvent 2 ou 3 briques, et tout le reste est construit par-dessus.</p>
</section>

<section id="signes"><h2>Les signes à observer</h2>
<ul>
<li>Les notes baissent d’un coup sur des chapitres pourtant différents.</li>
<li>Votre enfant comprend la correction, mais ne sait pas refaire seul.</li>
<li>Les erreurs sont « bêtes » et répétées : signes, fractions, carrés.</li>
<li>Il évite les devoirs de maths ou dit que « ça ne sert à rien de travailler, je suis nul ».</li>
</ul>
<p>Aucun de ces signes n’est grave en soi. Ils indiquent surtout qu’il faut regarder <strong>ce qui</strong> bloque, plutôt que de rajouter des heures de travail général.</p>
</section>

<section id="cause"><h2>Trouver la vraie cause</h2>
<p>Prenons un exemple fréquent. Au contrôle, votre enfant écrit {M('BC² = 7² + 5² = 14 + 10 = 24')}. La correction dira « erreur sur Pythagore ». En réalité, il connaît le théorème, mais il confond le carré et le double, une notion de 4e. Refaire des exercices de Pythagore ne réglera rien. Revoir les <a href="/puissances-3eme.html">carrés</a> pendant quelques jours, si.</p>
<p>Pour trouver la cause, regardez les copies avec votre enfant et cherchez les erreurs qui reviennent. Posez-lui une question plus simple sur la même notion. S’il bloque encore, remontez d’un cran. C’est exactement la démarche que suit le diagnostic Matheux, de façon systématique.</p>
</section>

<section id="solutions"><h2>Les solutions possibles</h2>
<div class="scroll"><table class="t">
<tr><th>Solution</th><th>Points forts</th><th>Limites</th></tr>
<tr><td>Échanger avec le professeur de maths</td><td>Gratuit. Il connaît votre enfant et le programme de la classe.</td><td>Peu de temps disponible pour un suivi individuel.</td></tr>
<tr><td>Dispositifs du collège (aide aux devoirs, soutien)</td><td>Gratuit, sur place.</td><td>Variables selon les établissements.</td></tr>
<tr><td>Cours particuliers</td><td>Accompagnement humain et personnalisé.</td><td>Coût élevé sur la durée. La qualité dépend beaucoup de l’intervenant.</td></tr>
<tr><td>Entraînement en ligne</td><td>Disponible tous les jours, à petites doses.</td><td>Utile seulement s’il cible les vraies difficultés, et si l’élève s’y tient.</td></tr>
</table></div>
<p>Ces solutions se combinent. Dans tous les cas, elles sont plus efficaces quand on sait précisément quoi travailler. Et la régularité compte plus que la durée : 10 minutes par jour valent mieux qu’une longue séance par semaine.</p>
</section>

{{CTA_BOX}}

<section id="matheux"><h2>Ce que propose Matheux</h2>
<p>Matheux a été conçu par Nicolas Follezou, ancien ingénieur, qui accompagne des élèves en soutien scolaire de maths depuis des années. Le même constat revenait sans cesse : un élève « nul en maths » ne l’est presque jamais. Il bute sur quelques notions, souvent anciennes.</p>
<ul>
<li><strong>Un diagnostic express gratuit</strong> (environ 8 minutes) : les questions s’adaptent aux réponses et remontent aux prérequis quand c’est utile.</li>
<li><strong>Une carte des compétences</strong> : ce qui est acquis, fragile ou à reprendre, avec les causes probables des erreurs.</li>
<li><strong>5 exercices par jour</strong>, choisis selon cette carte, gratuitement.</li>
<li>Pour aller plus loin, un diagnostic complet avec un bilan PDF pour les parents, et un programme jusqu’au Brevet. Voir <a href="/#offres">les offres</a> : paiement unique, sans abonnement.</li>
</ul>
<p>Pour une question, écrivez à <a href="mailto:contact@matheux.fr">contact@matheux.fr</a>. C’est Nicolas qui répond.</p>
</section>
''',
    faq=[
        ('Mon enfant dit qu’il est nul en maths : est-ce possible de rattraper en 3e ?', 'Oui, dans la grande majorité des cas. Un élève en difficulté a rarement des lacunes partout. Une fois les 2 ou 3 notions qui bloquent identifiées et retravaillées régulièrement, beaucoup d’autres chapitres deviennent accessibles. Plus on s’y prend tôt dans l’année, plus c’est confortable.'),
        ('Faut-il prendre des cours particuliers ?', 'Ce n’est pas toujours nécessaire. Commencez par savoir précisément ce qui bloque. Si les difficultés sont nombreuses ou si votre enfant a besoin d’un accompagnement humain régulier, des cours particuliers peuvent aider, surtout s’ils partent de ce diagnostic.'),
        ('Combien de temps par jour mon enfant doit-il travailler les maths ?', 'Pour consolider, 10 à 15 minutes par jour suffisent souvent, à condition que ce temps porte sur ses vraies difficultés. La régularité est plus importante que la durée.'),
        ('Comment aider mon enfant si je ne suis pas à l’aise en maths ?', 'Vous n’avez pas besoin d’expliquer vous-même. Vous pouvez l’aider à s’organiser (un créneau fixe et court), valoriser ses efforts, et vous appuyer sur des outils qui expliquent et corrigent. Échanger avec son professeur reste très utile.'),
    ],
    related=['/comment-reviser-brevet-maths.html', '/exercices-maths-3eme.html', '/exercices-maths-3eme-brevet.html', '/fractions-brevet.html', '/calcul-litteral-3eme.html'],
))
