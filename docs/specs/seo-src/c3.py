from build import F, M

PAGES = []

# ─────────────────────────────── PYTHAGORE
PAGES.append(dict(
    path='/pythagore-brevet.html', src='pythagore', crumb='Théorème de Pythagore',
    title='Théorème de Pythagore 3e : cours et exercices corrigés | Matheux',
    desc='Théorème de Pythagore au Brevet : calculer l’hypoténuse ou un côté, réciproque et contraposée, rédaction. Exercices corrigés et erreurs fréquentes.',
    eyebrow='Maths 3e · Brevet 2027 · Géométrie',
    h1='Le théorème de Pythagore au Brevet',
    h1_text='Le théorème de Pythagore au Brevet : cours et exercices corrigés',
    lead='Pythagore revient très souvent au Brevet : calculer une longueur dans un triangle rectangle, ou prouver qu’un triangle est (ou n’est pas) rectangle. La formule, tout le monde la connaît. Ce qui fait la différence, c’est de savoir laquelle des trois utiliser et comment la rédiger.',
    teaches=['Calculer l’hypoténuse avec le théorème de Pythagore', 'Calculer un côté de l’angle droit', 'Réciproque du théorème de Pythagore', 'Contraposée : montrer qu’un triangle n’est pas rectangle', 'Rédiger une démonstration'],
    toc=[('theoreme', 'Le théorème'), ('longueur', 'Calculer une longueur'), ('reciproque', 'Réciproque et contraposée'), ('redaction', 'La rédaction attendue'), ('erreurs', 'Erreurs fréquentes'), ('faq', 'Questions fréquentes')],
    body=f'''
<section id="theoreme"><h2>Le théorème</h2>
<div class="key"><p class="t">Théorème de Pythagore</p><p>Si un triangle ABC est rectangle en A, alors {M('BC² = AB² + AC²')}. [BC] est l’<strong>hypoténuse</strong> : le côté en face de l’angle droit, et le plus long des trois.</p></div>
<p>Le théorème relie des <strong>carrés</strong> de longueurs, pas les longueurs elles-mêmes. Géométriquement, l’aire du carré construit sur l’hypoténuse est égale à la somme des aires des carrés construits sur les deux autres côtés. C’est pour cela que {M('3 + 4 ≠ 5')}, alors que {M('3² + 4² = 5²')}.</p>
</section>

<section id="longueur"><h2>Calculer une longueur</h2>
<div class="ex"><h3>Exercice 1 : calculer l’hypoténuse</h3>
<div class="q"><p>ABC est rectangle en A, avec {M('AB = 6')} cm et {M('AC = 8')} cm. Calculer BC.</p></div>
<div class="s"><span class="lbl">Correction</span>
<p>Le triangle ABC est rectangle en A. D’après le théorème de Pythagore : {M('BC² = AB² + AC² = 6² + 8² = 36 + 64 = 100')}.</p>
<p>Donc {M('BC = √100 = 10')}. <strong>BC mesure 10 cm.</strong> Contrôle : 10 est plus grand que 8 (c’est le plus long côté) et plus petit que {M('6 + 8 = 14')}.</p>
</div></div>
<div class="ex"><h3>Exercice 2 : calculer un côté de l’angle droit</h3>
<div class="q"><p>EFG est rectangle en E, avec {M('FG = 13')} cm et {M('EF = 5')} cm. Calculer EG.</p></div>
<div class="s"><span class="lbl">Correction</span>
<p>L’hypoténuse est [FG]. D’après le théorème de Pythagore : {M('FG² = EF² + EG²')}, donc {M('EG² = FG² − EF² = 169 − 25 = 144')}.</p>
<p>{M('EG = √144 = 12')}. <strong>EG mesure 12 cm.</strong> Quand on cherche un petit côté, on <strong>soustrait</strong>.</p>
</div></div>
<p>Si le résultat n’est pas un carré parfait, on donne la valeur exacte avec une <a href="/racine-carree-3eme.html">racine carrée</a> ({M('√13')}), puis une valeur arrondie si l’énoncé la demande.</p>
</section>

<section id="reciproque"><h2>Réciproque et contraposée</h2>
<p>Pour savoir si un triangle est rectangle, on ne peut pas utiliser le théorème lui-même, puisqu’il suppose que le triangle est déjà rectangle. On compare deux calculs :</p>
<ul>
<li>d’un côté, le carré du <strong>plus grand côté</strong> ;</li>
<li>de l’autre, la somme des carrés des deux autres côtés.</li>
</ul>
<p>S’ils sont <strong>égaux</strong>, le triangle est rectangle : c’est la <strong>réciproque</strong>. S’ils sont <strong>différents</strong>, le triangle n’est pas rectangle : c’est la <strong>contraposée</strong>. Des nombres « proches » ne suffisent pas, il faut une égalité exacte.</p>
<div class="ex"><h3>Exercice 3 : rectangle ou pas ?</h3>
<div class="q"><p>Triangle RST : {M('RS = 8')}, {M('ST = 15')}, {M('RT = 17')}. Triangle UVW : {M('UV = 6')}, {M('VW = 9')}, {M('UW = 11')}. Ces triangles sont-ils rectangles ?</p></div>
<div class="s"><span class="lbl">Correction</span>
<p>RST : le plus grand côté est [RT]. {M('RT² = 289')} et {M('RS² + ST² = 64 + 225 = 289')}. Comme {M('RT² = RS² + ST²')}, d’après la réciproque du théorème de Pythagore, <strong>RST est rectangle en S</strong> (le sommet opposé au plus grand côté).</p>
<p>UVW : {M('UW² = 121')} et {M('UV² + VW² = 36 + 81 = 117')}. Comme {M('121 ≠ 117')}, d’après la contraposée du théorème de Pythagore, <strong>UVW n’est pas rectangle</strong>.</p>
</div></div>
</section>

<section id="redaction"><h2>La rédaction attendue au Brevet</h2>
<div class="key"><p class="t">Modèle à recopier</p><p>« Le triangle ABC est rectangle en A. D’après le théorème de Pythagore, {M('BC² = AB² + AC²')}. […] Donc {M('BC = √… ≈ …')} cm. »</p></div>
<p>Les trois éléments qui rapportent des points : l’<strong>hypothèse</strong> (rectangle en quel point), le <strong>nom du théorème</strong> (direct, réciproque ou contraposée), et une <strong>conclusion</strong> avec l’unité. L’épreuve évalue aussi les démarches, même quand elles n’aboutissent pas : écris ce que tu as commencé.</p>
</section>

{{CTA_BOX}}

<section id="erreurs"><h2>Les erreurs les plus fréquentes</h2>
<ul class="errs">
<li><span class="e">Additionner les côtés ({M('3 + 4 = 7')})</span><span class="c">Pythagore porte sur les carrés : {M('3² + 4² = 25')}, donc 5.</span></li>
<li><span class="e">Oublier la racine à la fin ({M('BC = 100')})</span><span class="c">{M('BC² = 100')}, donc {M('BC = √100 = 10')}.</span></li>
<li><span class="e">Écrire {M('√(a² + b²) = a + b')}</span><span class="c">Calcule d’abord la somme des carrés, puis la racine du total.</span></li>
<li><span class="e">Additionner quand on cherche un petit côté ({M('13² + 5²')})</span><span class="c">Petit côté : {M('hypoténuse² − autre côté²')}.</span></li>
<li><span class="e">Mal repérer l’hypoténuse</span><span class="c">Elle est en face de l’angle droit. C’est toujours le plus long côté.</span></li>
<li><span class="e">Utiliser le théorème pour prouver qu’un triangle est rectangle</span><span class="c">On calcule séparément, on compare, puis on cite la réciproque.</span></li>
<li><span class="e">Conclure « rectangle » parce que 289 et 290 sont proches</span><span class="c">L’égalité doit être exacte. Sinon, il n’est pas rectangle.</span></li>
<li><span class="e">Confondre carré et double ({M('9² = 18')})</span><span class="c">Erreur de <a href="/puissances-3eme.html">puissances</a> (4e), à retravailler en premier.</span></li>
</ul>
<p>La dernière erreur est typique d’une cause racine : l’élève « rate Pythagore » alors que c’est le carré qui n’est pas acquis. C’est exactement ce que le diagnostic Matheux cherche à débusquer.</p>
</section>
''',
    faq=[
        ('Comment utiliser le théorème de Pythagore ?', 'Vérifie que le triangle est rectangle et repère l’hypoténuse (en face de l’angle droit). Écris l’égalité hypoténuse² = côté² + côté², remplace les longueurs connues, calcule, puis prends la racine carrée. Termine par une phrase avec l’unité.'),
        ('Quelle est la différence entre Pythagore et sa réciproque ?', 'Le théorème part d’un triangle rectangle pour calculer une longueur. La réciproque part de trois longueurs connues pour prouver qu’un triangle est rectangle. Au Brevet, il faut citer celui qu’on utilise.'),
        ('Comment montrer qu’un triangle n’est pas rectangle ?', 'Calcule le carré du plus grand côté, puis la somme des carrés des deux autres. S’ils sont différents, d’après la contraposée du théorème de Pythagore, le triangle n’est pas rectangle.'),
        ('Faut-il donner une valeur exacte ou arrondie ?', 'Suis la consigne. Sans précision, donne la valeur exacte (par exemple √13 cm) puis, si c’est utile, une valeur approchée (≈ 3,6 cm) en précisant l’arrondi.'),
    ],
    related=['/racine-carree-3eme.html', '/trigonometrie-3eme.html', '/thales-brevet.html', '/puissances-3eme.html', '/exercices-maths-3eme-brevet.html'],
))

# ─────────────────────────────── THALÈS
PAGES.append(dict(
    path='/thales-brevet.html', src='thales', crumb='Théorème de Thalès',
    title='Théorème de Thalès 3e : cours et exercices corrigés | Matheux',
    desc='Théorème de Thalès au Brevet : écrire les rapports, calculer une longueur (emboîtés ou papillon), réciproque et parallélisme. Exercices corrigés.',
    eyebrow='Maths 3e · Brevet 2027 · Géométrie',
    h1='Le théorème de Thalès au Brevet',
    h1_text='Le théorème de Thalès au Brevet : cours et exercices corrigés',
    lead='Thalès permet de calculer une longueur quand deux droites sont parallèles, et sa réciproque permet de prouver qu’elles le sont. Tout repose sur une égalité de rapports bien écrite. Voici comment la poser sans erreur, dans les deux configurations.',
    teaches=['Reconnaître une configuration de Thalès', 'Écrire l’égalité des rapports', 'Calculer une longueur (triangles emboîtés ou papillon)', 'Réciproque du théorème de Thalès', 'Montrer que deux droites ne sont pas parallèles'],
    toc=[('theoreme', 'Le théorème'), ('calcul', 'Calculer une longueur'), ('papillon', 'La configuration papillon'), ('reciproque', 'La réciproque'), ('erreurs', 'Erreurs fréquentes'), ('faq', 'Questions fréquentes')],
    body=f'''
<section id="theoreme"><h2>Le théorème</h2>
<div class="key"><p class="t">Théorème de Thalès</p><p>Les points A, M, B sont alignés, les points A, N, C sont alignés, et les droites (MN) et (BC) sont <strong>parallèles</strong>. Alors {F('AM', 'AB')}{M(' = ')}{F('AN', 'AC')}{M(' = ')}{F('MN', 'BC')}.</p></div>
<p>Autrement dit, le petit triangle AMN est une <strong>réduction</strong> du grand triangle ABC : toutes les longueurs sont multipliées par le même coefficient. Pour ne pas se tromper, écris toujours les rapports dans le même ordre : petit triangle en haut, grand triangle en bas. Chaque rapport compare des côtés qui <strong>partent du même sommet</strong> A, ou qui se correspondent (MN et BC).</p>
</section>

<section id="calcul"><h2>Calculer une longueur</h2>
<div class="ex"><h3>Exercice 1 : triangles emboîtés</h3>
<div class="q"><p>M est sur [AB] et N sur [AC], avec (MN) // (BC). On donne {M('AM = 3')}, {M('AB = 9')}, {M('AC = 12')} et {M('BC = 15')} (en cm). Calculer AN et MN.</p></div>
<div class="s"><span class="lbl">Correction</span>
<p>Les points A, M, B et A, N, C sont alignés, et (MN) // (BC). D’après le théorème de Thalès : {F('AM', 'AB')}{M(' = ')}{F('AN', 'AC')}{M(' = ')}{F('MN', 'BC')}, soit {F('3', '9')}{M(' = ')}{F('AN', '12')}{M(' = ')}{F('MN', '15')}.</p>
<p>{M('AN = 12 × 3 ÷ 9 = 4')} cm et {M('MN = 15 × 3 ÷ 9 = 5')} cm. Le coefficient de réduction est {F('3', '9')}{M(' = ')}{F('1', '3')} : le petit triangle est trois fois plus petit.</p>
</div></div>
</section>

<section id="papillon"><h2>La configuration papillon</h2>
<p>Les deux droites se coupent en un point O, et les deux triangles sont de part et d’autre de O. Le théorème s’applique de la même façon. Il faut seulement bien associer chaque sommet à son correspondant.</p>
<div class="ex"><h3>Exercice 2</h3>
<div class="q"><p>Les droites (AD) et (BC) se coupent en O. Les droites (AB) et (CD) sont parallèles. {M('OA = 4')}, {M('OD = 6')} et {M('OB = 5')} (en cm). Calculer OC.</p></div>
<div class="s"><span class="lbl">Correction</span>
<p>Les points A, O, D sont alignés, ainsi que B, O, C, et (AB) // (CD). D’après le théorème de Thalès : {F('OA', 'OD')}{M(' = ')}{F('OB', 'OC')}{M(' = ')}{F('AB', 'DC')}.</p>
<p>{F('4', '6')}{M(' = ')}{F('5', 'OC')}, donc {M('OC = 6 × 5 ÷ 4 = 7,5')} cm.</p>
</div></div>
</section>

<section id="reciproque"><h2>La réciproque : prouver que deux droites sont parallèles</h2>
<p>On calcule <strong>deux rapports séparément</strong> et on les compare. S’ils sont égaux, et si les points sont alignés <strong>dans le même ordre</strong>, les droites sont parallèles. S’ils sont différents, elles ne le sont pas.</p>
<div class="ex"><h3>Exercice 3</h3>
<div class="q"><p>A, M, B sont alignés dans cet ordre, ainsi que A, N, C. {M('AM = 2,4')}, {M('AB = 6')}, {M('AN = 3')}, {M('AC = 7,5')}. Les droites (MN) et (BC) sont-elles parallèles ?</p></div>
<div class="s"><span class="lbl">Correction</span>
<p>{F('AM', 'AB')}{M(' = ')}{F('2,4', '6')}{M(' = 0,4')} et {F('AN', 'AC')}{M(' = ')}{F('3', '7,5')}{M(' = 0,4')}.</p>
<p>Les rapports sont égaux et les points sont alignés dans le même ordre. D’après la réciproque du théorème de Thalès, <strong>(MN) et (BC) sont parallèles</strong>.</p>
<p>Si on avait eu {M('AN = 3,2')}, on aurait {F('3,2', '7,5')}{M(' ≈ 0,427 ≠ 0,4')}, et les droites ne seraient pas parallèles. Pour comparer, utilise les valeurs exactes (ou le produit en croix), pas des arrondis.</p>
</div></div>
</section>

{{CTA_BOX}}

<section id="erreurs"><h2>Les erreurs les plus fréquentes</h2>
<ul class="errs">
<li><span class="e">Écrire {M('AM/AB = AN/NC')}</span><span class="c">On compare des côtés entiers partant de A : {M('AN/AC')}, pas un morceau {M('NC')}.</span></li>
<li><span class="e">Utiliser MB au lieu de AB</span><span class="c">Colorie le petit et le grand triangle : [AB] est un côté du grand, pas [MB].</span></li>
<li><span class="e">Appliquer Thalès sans droites parallèles</span><span class="c">Écris l’hypothèse (MN) // (BC) avant toute égalité.</span></li>
<li><span class="e">Mal isoler l’inconnue</span><span class="c">{M('3/9 = AN/12')} donne {M('AN = 12 × 3 ÷ 9')}. Vérifie l’ordre de grandeur : AN est plus petit que AC.</span></li>
<li><span class="e">Mal associer les segments en papillon</span><span class="c">Fais « tourner » le petit triangle : chaque sommet a son correspondant de l’autre côté de O.</span></li>
<li><span class="e">« Agrandir, c’est ajouter la même longueur »</span><span class="c">Agrandir, c’est multiplier toutes les longueurs par le même nombre.</span></li>
<li><span class="e">Conclure avec un seul rapport, ou avec des rapports arrondis</span><span class="c">Deux rapports, calculés exactement, puis comparés.</span></li>
</ul>
</section>
''',
    faq=[
        ('Comment appliquer le théorème de Thalès ?', 'Vérifie les deux conditions : deux droites sécantes, et deux droites parallèles qui les coupent. Écris les trois rapports égaux (petit triangle sur grand triangle), remplace par les longueurs connues, puis isole l’inconnue avec un produit en croix.'),
        ('Quelle est la réciproque du théorème de Thalès ?', 'Si les points A, M, B et A, N, C sont alignés dans le même ordre, et si AM/AB = AN/AC, alors les droites (MN) et (BC) sont parallèles. On l’utilise pour prouver un parallélisme.'),
        ('Quelle différence entre Thalès et Pythagore ?', 'Pythagore s’utilise dans un triangle rectangle et relie les trois côtés. Thalès s’utilise avec deux droites parallèles et relie les côtés de deux triangles, dont l’un est une réduction de l’autre. Un même exercice de Brevet peut enchaîner les deux.'),
        ('Qu’est-ce que la configuration papillon ?', 'C’est quand les deux triangles sont de part et d’autre du point d’intersection O des deux droites, comme les ailes d’un papillon. Les rapports s’écrivent de la même façon, avec O comme sommet commun.'),
    ],
    related=['/pythagore-brevet.html', '/trigonometrie-3eme.html', '/fractions-brevet.html', '/equations-3eme.html', '/exercices-maths-3eme-brevet.html'],
))

# ─────────────────────────────── FRACTIONS
PAGES.append(dict(
    path='/fractions-brevet.html', src='fractions', crumb='Fractions',
    title='Fractions 3e : calculs et exercices corrigés pour le Brevet',
    desc='Fractions pour le Brevet : simplifier, additionner, multiplier, diviser, priorités, fraction d’une quantité. Exercices corrigés et erreurs fréquentes.',
    eyebrow='Maths 3e · Brevet 2027 · Nombres et calculs',
    h1='Les fractions au Brevet : calculer sans erreur',
    h1_text='Les fractions au Brevet : méthodes et exercices corrigés',
    lead='Les fractions ne sont pas un chapitre isolé : on les retrouve dans les probabilités, Thalès, les équations et la partie automatismes. Une hésitation sur les fractions fait perdre des points partout. Voici les quatre opérations, avec la raison de chaque règle.',
    teaches=['Simplifier une fraction', 'Additionner et soustraire des fractions', 'Multiplier des fractions', 'Diviser par une fraction', 'Calculer une fraction d’une quantité', 'Priorités opératoires avec des fractions'],
    toc=[('sens', 'Ce qu’est une fraction'), ('simplifier', 'Simplifier'), ('operations', 'Les quatre opérations'), ('exemples', 'Exercices corrigés'), ('erreurs', 'Erreurs fréquentes'), ('faq', 'Questions fréquentes')],
    body=f'''
<section id="sens"><h2>Ce qu’est une fraction</h2>
<p>{F('3', '4')} est à la fois un partage (3 parts d’une unité coupée en 4) et un <strong>quotient</strong> : {M('3 ÷ 4 = 0,75')}. Garder ces deux sens en tête évite beaucoup d’erreurs, par exemple croire que {F('1', '8')} est plus grand que {F('1', '4')} « parce que 8 est plus grand que 4 ». En réalité, plus on coupe, plus les parts sont petites.</p>
<p>À connaître par cœur : {F('1', '2')}{M(' = 0,5')}, {F('1', '4')}{M(' = 0,25')}, {F('3', '4')}{M(' = 0,75')}, {F('1', '5')}{M(' = 0,2')}, {F('1', '10')}{M(' = 0,1')}. Et {M('25 % = ')}{F('25', '100')}{M(' = 0,25')}.</p>
</section>

<section id="simplifier"><h2>Simplifier une fraction</h2>
<p>On ne change pas une fraction en <strong>multipliant ou divisant</strong> le numérateur et le dénominateur par un même nombre non nul. Ajouter le même nombre en haut et en bas, en revanche, change la fraction.</p>
<p>{F('84', '120')}{M(' = ')}{F('42', '60')}{M(' = ')}{F('21', '30')}{M(' = ')}{F('7', '10')}. Une fraction est <strong>irréductible</strong> quand le numérateur et le dénominateur n’ont plus de diviseur commun autre que 1. La <a href="/arithmetique-3eme.html">décomposition en facteurs premiers</a> permet d’y arriver en une étape.</p>
<p>On ne simplifie que des <strong>facteurs</strong>, jamais des termes : dans {F('3 + 5', '3')}, on ne peut pas « barrer les 3 ».</p>
</section>

<section id="operations"><h2>Les quatre opérations</h2>
<div class="key"><p class="t">À retenir</p><ul>
<li><strong>Addition, soustraction</strong> : même dénominateur d’abord, puis on additionne les numérateurs. {F('1', '3')}{M(' + ')}{F('1', '4')}{M(' = ')}{F('4', '12')}{M(' + ')}{F('3', '12')}{M(' = ')}{F('7', '12')}.</li>
<li><strong>Multiplication</strong> : numérateurs ensemble, dénominateurs ensemble. Pas besoin de même dénominateur. {F('2', '3')}{M(' × ')}{F('5', '7')}{M(' = ')}{F('10', '21')}.</li>
<li><strong>Division</strong> : diviser par une fraction, c’est multiplier par son inverse. {F('a', 'b')}{M(' ÷ ')}{F('c', 'd')}{M(' = ')}{F('a', 'b')}{M(' × ')}{F('d', 'c')}.</li>
<li><strong>Fraction d’une quantité</strong> : « de » veut dire « × ». {F('3', '8')} de 32 = {M('32 ÷ 8 × 3 = 12')}.</li>
</ul></div>
<p>Les priorités restent les mêmes qu’avec les autres nombres : parenthèses, puis multiplications et divisions, puis additions et soustractions.</p>
</section>

<section id="exemples"><h2>Exercices corrigés</h2>
<div class="ex"><h3>Exercice 1 : additionner</h3>
<div class="q"><p>Calculer {M('A = ')}{F('3', '4')}{M(' + ')}{F('2', '5')} et donner le résultat sous forme irréductible.</p></div>
<div class="s"><span class="lbl">Correction</span>
<p>Le dénominateur commun est 20 : {M('A = ')}{F('15', '20')}{M(' + ')}{F('8', '20')}{M(' = ')}{F('23', '20')}. 23 est premier et ne divise pas 20, donc <strong>{F('23', '20')} est irréductible</strong>.</p>
</div></div>
<div class="ex"><h3>Exercice 2 : priorités (automatismes, sans calculatrice)</h3>
<div class="q"><p>Calculer {M('B = ')}{F('2', '3')}{M(' − ')}{F('5', '6')}{M(' × ')}{F('4', '5')}.</p></div>
<div class="s"><span class="lbl">Correction</span>
<p>La multiplication d’abord : {F('5', '6')}{M(' × ')}{F('4', '5')}{M(' = ')}{F('20', '30')}{M(' = ')}{F('2', '3')}. Donc {M('B = ')}{F('2', '3')}{M(' − ')}{F('2', '3')}{M(' = 0')}.</p>
<p>Si on avait calculé de gauche à droite, on aurait trouvé un autre résultat : c’est le piège de l’exercice.</p>
</div></div>
<div class="ex"><h3>Exercice 3 : diviser</h3>
<div class="q"><p>Calculer {M('C = ')}{F('7', '3')}{M(' ÷ ')}{F('14', '9')}.</p></div>
<div class="s"><span class="lbl">Correction</span>
<p>{M('C = ')}{F('7', '3')}{M(' × ')}{F('9', '14')}{M(' = ')}{F('7 × 9', '3 × 14')}{M(' = ')}{F('7 × 3 × 3', '3 × 2 × 7')}{M(' = ')}<strong>{F('3', '2')}</strong>. On simplifie avant de multiplier : les calculs restent petits.</p>
</div></div>
<div class="ex"><h3>Exercice 4 : problème (type Brevet)</h3>
<div class="q"><p>Léa dépense {F('1', '4')} de son argent de poche pour un livre, puis {F('2', '5')} <strong>du reste</strong> pour une place de cinéma. Quelle fraction de son argent lui reste-t-il ?</p></div>
<div class="s"><span class="lbl">Correction</span>
<p>Après le livre, il reste {M('1 − ')}{F('1', '4')}{M(' = ')}{F('3', '4')}. Le cinéma coûte {F('2', '5')} de {F('3', '4')}, soit {F('2', '5')}{M(' × ')}{F('3', '4')}{M(' = ')}{F('6', '20')}{M(' = ')}{F('3', '10')} de l’argent de départ.</p>
<p>Il reste {F('3', '4')}{M(' − ')}{F('3', '10')}{M(' = ')}{F('15', '20')}{M(' − ')}{F('6', '20')}{M(' = ')}<strong>{F('9', '20')}</strong> de son argent de poche.</p>
</div></div>
</section>

{{CTA_BOX}}

<section id="erreurs"><h2>Les erreurs les plus fréquentes</h2>
<ul class="errs">
<li><span class="e">{F('1', '3')}{M(' + ')}{F('1', '4')}{M(' = ')}{F('2', '7')}</span><span class="c">Les parts n’ont pas la même taille : on passe au même dénominateur, {F('7', '12')}.</span></li>
<li><span class="e">{F('1', '3')}{M(' + ')}{F('1', '4')}{M(' = ')}{F('1', '12')}{M(' + ')}{F('1', '12')}</span><span class="c">Ce qu’on fait en bas, on le fait en haut : {F('1', '3')}{M(' = ')}{F('4', '12')}.</span></li>
<li><span class="e">{M('1 + ')}{F('2', '5')}{M(' = ')}{F('3', '6')}</span><span class="c">Écrire {M('1 = ')}{F('5', '5')} : le résultat est {F('7', '5')}.</span></li>
<li><span class="e">{F('2', '3')}{M(' × ')}{F('1', '4')}{M(' = ')}{F('8', '3')} (produit en croix)</span><span class="c">Le produit en croix sert à comparer ou résoudre, pas à multiplier : {F('2', '12')}{M(' = ')}{F('1', '6')}.</span></li>
<li><span class="e">Diviser par {F('3', '4')} en multipliant par {F('3', '4')}</span><span class="c">On multiplie par l’inverse du diviseur : {F('4', '3')}.</span></li>
<li><span class="e">{F('3', '8')} de 32 = {M('32 ÷ 3')}</span><span class="c">On partage en 8 ({M('32 ÷ 8 = 4')}), puis on prend 3 parts : 12.</span></li>
<li><span class="e">S’arrêter à {F('42', '60')}</span><span class="c">Vérifie qu’il ne reste aucun diviseur commun : {F('7', '10')}.</span></li>
<li><span class="e">{M('25 % = 0,025')}</span><span class="c">{M('x %')} = {F('x', '100')} : on décale de deux rangs, {M('0,25')}.</span></li>
</ul>
</section>
''',
    faq=[
        ('Comment additionner deux fractions ?', 'Mets-les au même dénominateur en multipliant le numérateur et le dénominateur de chacune par le même nombre, puis additionne les numérateurs en gardant le dénominateur commun. Simplifie le résultat si possible.'),
        ('Faut-il un dénominateur commun pour multiplier des fractions ?', 'Non. Pour multiplier, on multiplie les numérateurs entre eux et les dénominateurs entre eux. Le dénominateur commun ne sert qu’à additionner ou soustraire.'),
        ('Comment diviser par une fraction ?', 'Multiplie par son inverse : on retourne la fraction qui suit le signe ÷. Par exemple, 5 ÷ 2/3 = 5 × 3/2 = 15/2. Diviser par un nombre plus petit que 1 donne un résultat plus grand, c’est normal.'),
        ('Qu’est-ce qu’une fraction irréductible ?', 'Une fraction qu’on ne peut plus simplifier : son numérateur et son dénominateur n’ont aucun diviseur commun autre que 1, comme 7/10. Au Brevet, on attend généralement le résultat sous cette forme.'),
    ],
    related=['/arithmetique-3eme.html', '/probabilites-brevet.html', '/calcul-litteral-3eme.html', '/equations-3eme.html', '/exercices-maths-3eme-brevet.html'],
))

# ─────────────────────────────── PROBABILITÉS
PAGES.append(dict(
    path='/probabilites-brevet.html', src='probabilites', crumb='Probabilités',
    title='Probabilités 3e : cours et exercices corrigés pour le Brevet',
    desc='Probabilités pour le Brevet : calculer une probabilité, événement contraire, arbre pour deux épreuves, fréquence. Exercices corrigés et pièges.',
    eyebrow='Maths 3e · Brevet 2027 · Probabilités',
    h1='Les probabilités au Brevet : méthodes et exercices',
    h1_text='Les probabilités au Brevet : méthodes et exercices corrigés',
    lead='En probabilités, les calculs sont simples. La difficulté est de bien modéliser : quelles sont les issues, sont-elles équiprobables, faut-il un arbre ? Voici la méthode pour chaque type de question, et les pièges de raisonnement les plus courants.',
    teaches=['Issues et événements', 'Calculer une probabilité en situation d’équiprobabilité', 'Événement contraire', 'Probabilité de « A ou B »', 'Expérience à deux épreuves : arbre et tableau', 'Fréquence et probabilité'],
    toc=[('vocabulaire', 'Le vocabulaire'), ('calculer', 'Calculer une probabilité'), ('deux-epreuves', 'Deux épreuves : l’arbre'), ('frequence', 'Fréquence et probabilité'), ('exemples', 'Exercices corrigés'), ('erreurs', 'Erreurs fréquentes'), ('faq', 'Questions fréquentes')],
    body=f'''
<section id="vocabulaire"><h2>Le vocabulaire</h2>
<ul>
<li>Une <strong>expérience aléatoire</strong> a plusieurs résultats possibles, qu’on ne peut pas prévoir : lancer un dé, tirer une carte.</li>
<li>Chaque résultat est une <strong>issue</strong> : pour un dé, 1, 2, 3, 4, 5 ou 6.</li>
<li>Un <strong>événement</strong> est un ensemble d’issues : « obtenir un nombre pair » = {{2 ; 4 ; 6}}.</li>
<li>Le <strong>contraire</strong> de A, noté « non A », contient toutes les issues qui ne sont pas dans A.</li>
</ul>
</section>

<section id="calculer"><h2>Calculer une probabilité</h2>
<div class="key"><p class="t">À retenir</p><ul>
<li>Si toutes les issues ont la même chance (équiprobabilité) : {M('P(A) = ')}{F('nombre d’issues favorables', 'nombre total d’issues')}.</li>
<li>Une probabilité est toujours comprise entre 0 et 1.</li>
<li>{M('P(non A) = 1 − P(A)')}.</li>
<li>Si A et B ne peuvent pas se produire en même temps : {M('P(A ou B) = P(A) + P(B)')}.</li>
</ul></div>
<p>Attention, « gagner ou perdre » ne fait pas forcément une chance sur deux : il faut compter les issues <strong>réellement</strong> équiprobables.</p>
</section>

<section id="deux-epreuves"><h2>Deux épreuves : l’arbre</h2>
<p>Quand on enchaîne deux expériences (deux tirages, un dé puis une pièce), on dessine un <strong>arbre</strong> ou un <strong>tableau à double entrée</strong>. Deux règles :</p>
<ul>
<li>le long d’une branche, on <strong>multiplie</strong> les probabilités ;</li>
<li>pour un événement qui correspond à plusieurs chemins, on <strong>additionne</strong> les chemins.</li>
</ul>
<p>Si le tirage se fait <strong>sans remise</strong>, le contenu du sac change pour la deuxième épreuve : il faut le mettre à jour sur l’arbre.</p>
</section>

<section id="frequence"><h2>Fréquence et probabilité</h2>
<p>Si on lance une pièce 20 fois et qu’on obtient 13 piles, la <strong>fréquence</strong> observée de pile est {F('13', '20')}{M(' = 0,65')}. La <strong>probabilité</strong>, elle, reste 0,5. Quand on répète l’expérience un grand nombre de fois, la fréquence se rapproche de la probabilité. Sur peu d’essais, elle peut en être loin. Et le hasard n’a pas de mémoire : après 5 piles de suite, la probabilité d’obtenir pile au lancer suivant est toujours 0,5.</p>
</section>

<section id="exemples"><h2>Exercices corrigés</h2>
<div class="ex"><h3>Exercice 1 : un tirage</h3>
<div class="q"><p>Un sac contient 3 boules rouges, 2 vertes et 5 bleues, indiscernables au toucher. On tire une boule au hasard. Calculer la probabilité de tirer une boule rouge, puis celle de ne pas tirer une boule bleue.</p></div>
<div class="s"><span class="lbl">Correction</span>
<p>Il y a {M('3 + 2 + 5 = 10')} boules, et chaque boule a la même chance d’être tirée. {M('P(rouge) = ')}{F('3', '10')}{M(' = 0,3')}.</p>
<p>{M('P(bleue) = ')}{F('5', '10')}, donc {M('P(non bleue) = 1 − ')}{F('5', '10')}{M(' = ')}{F('1', '2')}. On peut vérifier : il y a 5 boules non bleues sur 10.</p>
</div></div>
<div class="ex"><h3>Exercice 2 : deux tirages sans remise (type Brevet)</h3>
<div class="q"><p>Un sac contient 3 boules rouges et 2 vertes. On tire une boule, on ne la remet pas, puis on en tire une seconde. Calculer la probabilité d’obtenir deux boules rouges, puis deux boules de la même couleur.</p></div>
<div class="s"><span class="lbl">Correction</span>
<p>Premier tirage : {M('P(R) = ')}{F('3', '5')}. S’il est rouge, il reste 2 rouges sur 4 boules : {M('P(R au 2e) = ')}{F('2', '4')}.</p>
<p>{M('P(RR) = ')}{F('3', '5')}{M(' × ')}{F('2', '4')}{M(' = ')}{F('6', '20')}{M(' = ')}{F('3', '10')}.</p>
<p>De même, {M('P(VV) = ')}{F('2', '5')}{M(' × ')}{F('1', '4')}{M(' = ')}{F('2', '20')}{M(' = ')}{F('1', '10')}. Deux boules de même couleur : {F('3', '10')}{M(' + ')}{F('1', '10')}{M(' = ')}<strong>{F('4', '10')}{M(' = ')}{F('2', '5')}</strong>.</p>
</div></div>
<div class="ex"><h3>Exercice 3 : deux dés</h3>
<div class="q"><p>On lance deux dés équilibrés et on additionne les résultats. La somme 7 a-t-elle la même probabilité que la somme 2 ?</p></div>
<div class="s"><span class="lbl">Correction</span>
<p>Un tableau à double entrée donne {M('6 × 6 = 36')} issues équiprobables (les couples). La somme 7 est obtenue par 6 couples : (1 ; 6), (2 ; 5), (3 ; 4), (4 ; 3), (5 ; 2), (6 ; 1). Donc {M('P(7) = ')}{F('6', '36')}{M(' = ')}{F('1', '6')}. La somme 2 n’est obtenue que par (1 ; 1) : {M('P(2) = ')}{F('1', '36')}.</p>
<p><strong>Non</strong> : les onze sommes possibles (de 2 à 12) ne sont pas équiprobables.</p>
</div></div>
</section>

{{CTA_BOX}}

<section id="erreurs"><h2>Les erreurs les plus fréquentes</h2>
<ul class="errs">
<li><span class="e">3 rouges et 5 bleues, donc {M('P(rouge) = 3/5')}</span><span class="c">On divise par le nombre total de boules : {F('3', '8')}.</span></li>
<li><span class="e">Donner une probabilité supérieure à 1</span><span class="c">Une probabilité est entre 0 et 1. Au-delà, le calcul est faux.</span></li>
<li><span class="e">{M('P(non A) = 1/P(A)')} ou {M('−P(A)')}</span><span class="c">{M('P(non A) = 1 − P(A)')}.</span></li>
<li><span class="e">Additionner le long d’une branche</span><span class="c">Le long d’une branche on multiplie, entre les branches on additionne.</span></li>
<li><span class="e">Oublier que le tirage est sans remise</span><span class="c">Mets à jour le contenu du sac pour le 2e tirage.</span></li>
<li><span class="e">Dé + pièce : {M('6 + 2 = 8')} issues</span><span class="c">Il y a {M('6 × 2 = 12')} issues : fais un tableau ou un arbre.</span></li>
<li><span class="e">« Après 5 échecs, je vais forcément gagner »</span><span class="c">Chaque lancer est indépendant, le dé n’a pas de mémoire.</span></li>
</ul>
</section>
''',
    faq=[
        ('Comment calculer une probabilité ?', 'Si toutes les issues ont la même chance de se produire, divise le nombre d’issues favorables par le nombre total d’issues. Pour 2 boules rouges sur 8, la probabilité est 2/8 = 1/4.'),
        ('Quand faut-il faire un arbre ?', 'Dès que l’expérience comporte deux étapes ou plus : deux tirages, un dé puis une pièce, deux lancers. L’arbre permet de ne pas oublier d’issue. On multiplie le long des branches et on additionne les chemins.'),
        ('Quelle est la différence entre fréquence et probabilité ?', 'La fréquence est observée après avoir fait l’expérience (13 piles sur 20 lancers). La probabilité est théorique (1/2 pour pile). Plus on répète l’expérience, plus la fréquence se rapproche de la probabilité.'),
        ('Une probabilité peut-elle s’écrire en pourcentage ?', 'Oui : 0,3, 3/10 et 30 % désignent la même probabilité. Donne la forme demandée par l’énoncé, et à défaut une fraction simplifiée.'),
    ],
    related=['/fractions-brevet.html', '/statistiques-brevet.html', '/arithmetique-3eme.html', '/fonctions-3eme.html', '/exercices-maths-3eme-brevet.html'],
))

# ─────────────────────────────── STATISTIQUES
PAGES.append(dict(
    path='/statistiques-brevet.html', src='statistiques', crumb='Statistiques',
    title='Statistiques 3e : moyenne, médiane, étendue | Matheux',
    desc='Statistiques pour le Brevet : moyenne simple et pondérée, médiane (effectif pair, tableau), étendue, comparer deux séries. Exercices corrigés.',
    eyebrow='Maths 3e · Brevet 2027 · Statistiques',
    h1='Les statistiques au Brevet : moyenne, médiane, étendue',
    h1_text='Les statistiques au Brevet : moyenne, médiane, étendue',
    lead='Un exercice de statistiques donne souvent des points faciles, à condition de ne pas confondre les indicateurs. La moyenne, la médiane et l’étendue ne disent pas la même chose. Voici comment les calculer, et surtout comment les interpréter.',
    teaches=['Lire un tableau d’effectifs', 'Calculer une fréquence', 'Moyenne simple et moyenne pondérée', 'Déterminer une médiane', 'Calculer une étendue', 'Comparer deux séries statistiques'],
    toc=[('indicateurs', 'Les trois indicateurs'), ('moyenne', 'Moyenne'), ('mediane', 'Médiane'), ('exemples', 'Exercices corrigés'), ('interpreter', 'Interpréter et comparer'), ('erreurs', 'Erreurs fréquentes'), ('faq', 'Questions fréquentes')],
    body=f'''
<section id="indicateurs"><h2>Les trois indicateurs à connaître</h2>
<div class="key"><p class="t">À retenir</p><ul>
<li><strong>Moyenne</strong> : somme des valeurs ÷ nombre de valeurs. C’est la valeur qu’aurait chacun si on mettait tout en commun, puis qu’on partageait équitablement.</li>
<li><strong>Médiane</strong> : la valeur qui partage la série <strong>rangée</strong> en deux groupes de même effectif.</li>
<li><strong>Étendue</strong> : plus grande valeur − plus petite valeur. Elle mesure la dispersion.</li>
</ul></div>
<p>La <strong>fréquence</strong> d’une valeur est son effectif divisé par l’effectif total. Elle peut s’écrire en fraction, en décimal ou en pourcentage.</p>
</section>

<section id="moyenne"><h2>Moyenne simple et moyenne pondérée</h2>
<p>Quand les valeurs sont données dans un tableau d’effectifs, chaque valeur compte autant de fois que son effectif : on multiplie chaque valeur par son effectif, on additionne, puis on divise par l’<strong>effectif total</strong>. C’est aussi le calcul d’une moyenne avec coefficients : on divise par la somme des coefficients.</p>
</section>

<section id="mediane"><h2>Médiane : la méthode</h2>
<ol>
<li><strong>Range</strong> les valeurs dans l’ordre croissant (étape la plus souvent oubliée).</li>
<li>Si l’effectif {M('N')} est <strong>impair</strong>, la médiane est la valeur de rang {F('N + 1', '2')}.</li>
<li>Si {M('N')} est <strong>pair</strong>, on prend la moyenne des valeurs de rang {F('N', '2')} et {F('N', '2')}{M(' + 1')}.</li>
<li>Avec un tableau d’effectifs, on calcule les <strong>effectifs cumulés</strong> pour trouver ces rangs.</li>
</ol>
</section>

<section id="exemples"><h2>Exercices corrigés</h2>
<div class="ex"><h3>Exercice 1 : une liste de notes</h3>
<div class="q"><p>Notes d’un élève : 8 ; 12 ; 14 ; 9 ; 11 ; 15 ; 7 ; 13 ; 10 ; 11. Calculer la moyenne, la médiane et l’étendue.</p></div>
<div class="s"><span class="lbl">Correction</span>
<p><strong>Moyenne</strong> : la somme vaut 110, pour 10 notes. {M('110 ÷ 10 = 11')}.</p>
<p><strong>Médiane</strong> : série rangée 7 ; 8 ; 9 ; 10 ; <strong>11 ; 11</strong> ; 12 ; 13 ; 14 ; 15. L’effectif est pair (10), on prend la moyenne des 5e et 6e valeurs : {M('(11 + 11) ÷ 2 = 11')}.</p>
<p><strong>Étendue</strong> : {M('15 − 7 = 8')}.</p>
</div></div>
<div class="ex"><h3>Exercice 2 : un tableau d’effectifs</h3>
<div class="q">
<div class="scroll"><table class="t"><tr><th scope="row">Pointure</th><td>36</td><td>37</td><td>38</td><td>39</td></tr><tr><th scope="row">Effectif</th><td>3</td><td>5</td><td>8</td><td>4</td></tr></table></div>
<p>Calculer la pointure moyenne et la pointure médiane de ce groupe de 20 élèves.</p></div>
<div class="s"><span class="lbl">Correction</span>
<p><strong>Moyenne</strong> : {M('(36 × 3 + 37 × 5 + 38 × 8 + 39 × 4) ÷ 20 = (108 + 185 + 304 + 156) ÷ 20 = 753 ÷ 20 = 37,65')}.</p>
<p><strong>Médiane</strong> : l’effectif est 20, on cherche les 10e et 11e valeurs. Effectifs cumulés : 3, 8, 16, 20. Les rangs 9 à 16 correspondent à la pointure 38, donc les 10e et 11e valeurs valent 38. <strong>La médiane est 38.</strong></p>
</div></div>
</section>

<section id="interpreter"><h2>Interpréter et comparer deux séries</h2>
<p>Deux séries peuvent avoir la même moyenne sans se ressembler : l’une peut être très regroupée, l’autre très dispersée. Pour comparer, on regarde <strong>une position</strong> (moyenne ou médiane) et <strong>une dispersion</strong> (étendue).</p>
<div class="ex"><h3>Exercice 3 : moyenne ou médiane ?</h3>
<div class="q"><p>Dans une petite entreprise, les 5 salaires mensuels sont : 1 500 € ; 1 600 € ; 1 700 € ; 1 800 € ; 9 000 €. Quel indicateur décrit le mieux le salaire « typique » ?</p></div>
<div class="s"><span class="lbl">Correction</span>
<p>Moyenne : {M('15 600 ÷ 5 = 3 120')} €. Médiane : 1 700 € (3e valeur sur 5).</p>
<p>Un seul salaire très élevé tire la moyenne vers le haut, alors que la médiane ne bouge pas. Ici, 4 salariés sur 5 gagnent moins de 1 800 € : <strong>la médiane est plus représentative</strong>.</p>
</div></div>
</section>

{{CTA_BOX}}

<section id="erreurs"><h2>Les erreurs les plus fréquentes</h2>
<ul class="errs">
<li><span class="e">Chercher la médiane sans ranger la série</span><span class="c">Toujours ranger dans l’ordre croissant d’abord.</span></li>
<li><span class="e">Prendre le milieu entre la plus petite et la plus grande valeur</span><span class="c">La médiane partage l’<strong>effectif</strong> en deux, pas l’intervalle des valeurs.</span></li>
<li><span class="e">Dans un tableau, prendre la valeur du milieu de la ligne des valeurs</span><span class="c">Utilise les effectifs cumulés pour trouver la valeur de rang {F('N', '2')}.</span></li>
<li><span class="e">Faire la moyenne simple des valeurs d’un tableau</span><span class="c">Chaque valeur compte autant de fois que son effectif.</span></li>
<li><span class="e">Diviser par le nombre de valeurs différentes au lieu de l’effectif total</span><span class="c">Pointures : on divise par 20 élèves, pas par 4 pointures.</span></li>
<li><span class="e">Confondre valeurs et effectifs</span><span class="c">Légende les lignes « valeur » et « effectif » avant de calculer.</span></li>
<li><span class="e">Étendue = dernière − première valeur de la liste non rangée</span><span class="c">Étendue = maximum − minimum.</span></li>
<li><span class="e">« Même moyenne, donc séries identiques »</span><span class="c">Compare aussi la dispersion.</span></li>
</ul>
</section>
''',
    faq=[
        ('Quelle est la différence entre moyenne et médiane ?', 'La moyenne répartit équitablement le total entre toutes les valeurs. La médiane est la valeur du milieu de la série rangée. Une valeur extrême modifie beaucoup la moyenne, mais presque pas la médiane.'),
        ('Comment trouver la médiane quand l’effectif est pair ?', 'Range la série, puis prends la moyenne des deux valeurs centrales, de rang N/2 et N/2 + 1. Pour 10 valeurs, ce sont les 5e et 6e.'),
        ('À quoi sert l’étendue ?', 'Elle mesure l’écart entre la plus grande et la plus petite valeur, donc la dispersion de la série. Deux classes de même moyenne peuvent avoir des étendues très différentes.'),
        ('Les quartiles sont-ils au programme de 3e ?', 'Les indicateurs à maîtriser en 3e sont la moyenne, la médiane et l’étendue. Les quartiles et les diagrammes en boîte sont étudiés au lycée.'),
    ],
    related=['/probabilites-brevet.html', '/fonctions-3eme.html', '/fractions-brevet.html', '/fonction-affine-3eme.html', '/exercices-maths-3eme-brevet.html'],
))
