from build import F, M
from svg import graph

PAGES = []

# ─────────────────────────────── CALCUL LITTÉRAL
PAGES.append(dict(
    path='/calcul-litteral-3eme.html', src='calcul_litteral', crumb='Calcul littéral',
    title='Calcul littéral 3e : développer, factoriser | Matheux',
    desc='Calcul littéral en 3e : développer, factoriser, identités remarquables, preuve avec x. Méthode, exercices corrigés et erreurs fréquentes au Brevet.',
    eyebrow='Maths 3e · Nombres et calculs',
    h1='Calcul littéral en 3e : développer et factoriser sans se tromper',
    h1_text='Calcul littéral en 3e : développer et factoriser',
    lead='Développer, c’est transformer un produit en somme. Factoriser, c’est l’inverse. Tout le calcul littéral de 3e tient en cinq formules et quelques réflexes de vérification. Les voici, avec des exercices corrigés pas à pas.',
    teaches=['Développer avec la simple et la double distributivité', 'Identités remarquables', 'Factoriser par un facteur commun', 'Factoriser a² − b²', 'Prouver un résultat général avec le calcul littéral'],
    toc=[('essentiel', 'L’essentiel à retenir'), ('developper', 'Développer'), ('factoriser', 'Factoriser'), ('exemples', 'Exercices corrigés'), ('erreurs', 'Erreurs fréquentes'), ('brevet', 'Au Brevet'), ('faq', 'Questions fréquentes')],
    body=f'''
<section id="essentiel"><h2>L’essentiel à retenir</h2>
<div class="key"><p class="t">Les 5 formules</p><ul>
<li>Simple distributivité : {M('k(a + b) = ka + kb')}</li>
<li>Double distributivité : {M('(a + b)(c + d) = ac + ad + bc + bd')}</li>
<li>{M('(a + b)² = a² + 2ab + b²')}</li>
<li>{M('(a − b)² = a² − 2ab + b²')}</li>
<li>{M('(a − b)(a + b) = a² − b²')}</li>
</ul></div>
<p>Ces formules se lisent dans les deux sens. De gauche à droite, on <strong>développe</strong>. De droite à gauche, on <strong>factorise</strong>. Une lettre comme {M('x')} représente un nombre : tout ce qui est vrai pour les nombres l’est pour les lettres.</p>
</section>

<section id="developper"><h2>Développer une expression</h2>
<p><strong>Développer</strong>, c’est supprimer les parenthèses pour écrire l’expression sous forme de somme, puis <strong>réduire</strong> : regrouper les termes de même nature (les {M('x²')} ensemble, les {M('x')} ensemble, les nombres ensemble).</p>
<h3>La méthode en 3 temps</h3>
<ol>
<li>Repère la forme : un facteur devant une parenthèse, deux parenthèses, ou une identité remarquable.</li>
<li>Fais <strong>tous</strong> les produits en écrivant chaque signe. Avec deux parenthèses, il y a 4 produits.</li>
<li>Réduis, puis vérifie en remplaçant {M('x')} par une valeur simple (par exemple {M('x = 1')}) dans l’expression de départ et dans ton résultat. Si les deux valeurs diffèrent, il y a une erreur.</li>
</ol>
<h3>Le piège du signe moins devant une parenthèse</h3>
<p>{M('−(x − 3) = −x + 3')} : le moins change le signe de <strong>chaque</strong> terme. Quand on soustrait un produit, par exemple {M('A − (x + 1)(x − 4)')}, on développe d’abord le produit <strong>en gardant les parenthèses</strong>, puis on distribue le moins.</p>
</section>

<section id="factoriser"><h2>Factoriser une expression</h2>
<p><strong>Factoriser</strong>, c’est écrire l’expression sous forme de <strong>produit</strong>. On le fait surtout pour résoudre une équation produit nul (voir la page <a href="/equations-3eme.html">équations</a>).</p>
<h3>1. Chercher un facteur commun</h3>
<p>{M('6x + 18 = 6(x + 3)')} : on met en facteur le <strong>plus grand</strong> facteur commun. {M('x² + x = x(x + 1)')} : quand un terme part entièrement, il reste 1.</p>
<p>Le facteur commun peut être une parenthèse entière : {M('(x + 2)(3x − 1) + (x + 2)(x + 5)')} a le facteur commun {M('(x + 2)')}.</p>
<h3>2. Reconnaître a² − b²</h3>
<p>Une différence de deux carrés se factorise toujours : {M('x² − 16 = x² − 4² = (x − 4)(x + 4)')}. Écris d’abord chaque terme comme un carré, c’est ce qui évite les erreurs. Une <strong>somme</strong> de carrés comme {M('x² + 9')} ne se factorise pas de cette façon.</p>
<p>Dans tous les cas, redéveloppe ton résultat : tu dois retomber sur l’expression de départ.</p>
</section>

<section id="exemples"><h2>Exercices corrigés</h2>
<div class="ex"><h3>Exercice 1 : développer et réduire</h3>
<div class="q"><p>Développer et réduire {M('A = (2x − 3)² − (x + 1)(x − 4)')}.</p></div>
<div class="s"><span class="lbl">Correction</span><ol>
<li>Identité remarquable : {M('(2x − 3)² = (2x)² − 2 × 2x × 3 + 3² = 4x² − 12x + 9')}.</li>
<li>Double distributivité : {M('(x + 1)(x − 4) = x² − 4x + x − 4 = x² − 3x − 4')}.</li>
<li>On soustrait le bloc entier : {M('A = 4x² − 12x + 9 − (x² − 3x − 4) = 4x² − 12x + 9 − x² + 3x + 4')}.</li>
<li>On réduit : <strong>{M('A = 3x² − 9x + 13')}</strong>.</li>
<li>Vérification avec {M('x = 1')} : au départ {M('(−1)² − 2 × (−3) = 1 + 6 = 7')} ; à l’arrivée {M('3 − 9 + 13 = 7')}. ✓</li>
</ol></div></div>

<div class="ex"><h3>Exercice 2 : factoriser</h3>
<div class="q"><p>Factoriser {M('B = 9x² − 25')} puis {M('C = (x + 2)(3x − 1) + (x + 2)(x + 5)')}.</p></div>
<div class="s"><span class="lbl">Correction</span>
<p>{M('B = (3x)² − 5²')}, c’est la forme {M('a² − b²')} avec {M('a = 3x')} et {M('b = 5')}. Donc <strong>{M('B = (3x − 5)(3x + 5)')}</strong>.</p>
<p>Dans {M('C')}, le facteur commun est {M('(x + 2)')} : {M('C = (x + 2)[(3x − 1) + (x + 5)] = (x + 2)(4x + 4)')}. On peut aller plus loin : {M('4x + 4 = 4(x + 1)')}, donc <strong>{M('C = 4(x + 2)(x + 1)')}</strong>.</p>
</div></div>

<div class="ex"><h3>Exercice 3 : prouver avec le calcul littéral (type Brevet)</h3>
<div class="q"><p>Programme de calcul : choisir un nombre entier, lui ajouter 3, élever le résultat au carré, puis soustraire le carré du nombre de départ. Montrer que le résultat est toujours un multiple de 3.</p></div>
<div class="s"><span class="lbl">Correction</span>
<p>On appelle {M('n')} le nombre de départ. Le programme donne {M('(n + 3)² − n²')}.</p>
<p>{M('(n + 3)² − n² = n² + 6n + 9 − n² = 6n + 9 = 3(2n + 3)')}.</p>
<p>Comme {M('2n + 3')} est un entier, le résultat est <strong>3 fois un entier : c’est un multiple de 3</strong>. Tester avec 2 ou 3 nombres ne suffit pas pour prouver. Il faut passer par la lettre, puis conclure par une phrase.</p>
</div></div>
</section>

{{CTA_BOX}}

<section id="erreurs"><h2>Les erreurs les plus fréquentes</h2>
<p>Ce sont les erreurs que le diagnostic Matheux repère le plus souvent en calcul littéral. Chacune a une cause précise, et un moyen simple de l’éviter.</p>
<ul class="errs">
<li><span class="e">{M('4(x + 3) = 4x + 3')}</span><span class="c">Le facteur multiplie chaque terme : {M('4x + 12')}.</span></li>
<li><span class="e">{M('−2(3x − 4) = −6x − 8')}</span><span class="c">{M('(−2) × (−4) = +8')} : règle des signes terme à terme.</span></li>
<li><span class="e">{M('(x + 2)(x + 3) = x² + 6')}</span><span class="c">Il y a 4 produits, pas 2 : {M('x² + 3x + 2x + 6 = x² + 5x + 6')}.</span></li>
<li><span class="e">{M('(a + b)² = a² + b²')}</span><span class="c">Oubli du double produit. Contre-exemple : {M('(1 + 2)² = 9')}, alors que {M('1² + 2² = 5')}.</span></li>
<li><span class="e">{M('(3x − 2)² = 3x² − …')}</span><span class="c">{M('(3x)² = 3x × 3x = 9x²')} : le coefficient est aussi au carré.</span></li>
<li><span class="e">{M('x + x = x²')} ou {M('3x + 2 = 5x')}</span><span class="c">{M('x + x = 2x')} ; on n’additionne que des termes de même famille.</span></li>
<li><span class="e">{M('x² − 16 = (x − 4)²')}</span><span class="c">{M('a² − b² = (a − b)(a + b)')} : {M('(x − 4)(x + 4)')}.</span></li>
<li><span class="e">« Je l’ai testé avec 3 nombres, donc c’est prouvé »</span><span class="c">Un exemple peut montrer qu’une affirmation est fausse, jamais qu’elle est toujours vraie.</span></li>
</ul>
</section>

<section id="brevet"><h2>Le calcul littéral au Brevet</h2>
<p>Le calcul littéral sert dans presque tous les sujets, même quand ce n’est pas le thème de l’exercice : programme de calcul, aire d’une figure en fonction de {M('x')}, résolution d’équation, fonction affine. Dans la partie automatismes (sans calculatrice), on peut te demander un développement rapide ou une factorisation simple. Dans la partie raisonnement, on attend souvent une <strong>preuve</strong> comme dans l’exercice 3 : écrire l’expression avec une lettre, la transformer, puis conclure par une phrase.</p>
<p>Si les développements te coûtent des points, la cause est souvent plus ancienne : règle des signes (5e), carrés (4e) ou réduction. C’est justement ce que le diagnostic cherche à identifier.</p>
</section>
''',
    faq=[
        ('Quelle est la différence entre développer et factoriser ?', 'Développer transforme un produit en somme : 3(x + 2) devient 3x + 6. Factoriser fait l’inverse : 3x + 6 devient 3(x + 2). On développe pour simplifier ou comparer des expressions, et on factorise pour résoudre une équation produit nul.'),
        ('Comment savoir s’il faut utiliser une identité remarquable ?', 'Pour développer : un carré de parenthèse, comme (x + 5)², ou un produit (a − b)(a + b). Pour factoriser : trois termes dont deux sont des carrés (x² + 6x + 9), ou une différence de deux carrés (x² − 49).'),
        ('Comment vérifier un développement ?', 'Remplace x par une valeur simple (1 ou 2) dans l’expression de départ et dans ton résultat. Si tu obtiens deux nombres différents, il y a une erreur. Si tu obtiens le même nombre, c’est très probablement juste : ce test ne prouve rien, mais il détecte la plupart des erreurs.'),
        ('Faut-il apprendre les identités remarquables par cœur ?', 'Oui, les trois. Si tu en oublies une le jour J, tu peux la retrouver : (a + b)² = (a + b)(a + b), il suffit de faire les 4 produits.'),
    ],
    related=['/equations-3eme.html', '/fonction-affine-3eme.html', '/puissances-3eme.html', '/fractions-brevet.html', '/exercices-maths-3eme-brevet.html'],
))

# ─────────────────────────────── ÉQUATIONS
PAGES.append(dict(
    path='/equations-3eme.html', src='equations', crumb='Équations',
    title='Équations 3e : résoudre, produit nul, mise en équation | Matheux',
    desc='Résoudre une équation en 3e : ax + b = cx + d, équation produit nul, x² = a, mise en équation d’un problème. Méthode, exercices corrigés et erreurs fréquentes.',
    eyebrow='Maths 3e · Nombres et calculs',
    h1='Équations en 3e : la méthode pour résoudre à tous les coups',
    h1_text='Équations en 3e : méthode et exercices corrigés',
    lead='Résoudre une équation, c’est trouver la ou les valeurs de x qui rendent l’égalité vraie. En 3e, quatre types reviennent sans cesse. Voici la méthode pour chacun, avec la vérification qui évite de perdre des points.',
    teaches=['Tester si un nombre est solution', 'Résoudre ax + b = cx + d', 'Équation produit nul', 'Équation x² = a', 'Mettre un problème en équation', 'Inéquation du premier degré'],
    toc=[('principe', 'Le principe de la balance'), ('premier-degre', 'Équations du premier degré'), ('produit-nul', 'Équation produit nul'), ('carre', 'Équation x² = a'), ('probleme', 'Mettre un problème en équation'), ('erreurs', 'Erreurs fréquentes'), ('faq', 'Questions fréquentes')],
    body=f'''
<section id="principe"><h2>Le principe de la balance</h2>
<p>Une équation est une balance en équilibre. Tu peux faire <strong>la même opération des deux côtés</strong> sans la déséquilibrer : ajouter, soustraire, multiplier ou diviser par un même nombre (non nul). L’objectif est d’isoler {M('x')}.</p>
<div class="key"><p class="t">Le réflexe qui rapporte des points</p><p>Une fois la solution trouvée, remplace-la dans l’équation de départ. Calcule le membre de gauche, puis le membre de droite, séparément. S’ils sont égaux, ta solution est juste. C’est aussi comme ça qu’on répond à la question « le nombre 3 est-il solution ? » : on remplace, on ne résout pas.</p></div>
</section>

<section id="premier-degre"><h2>Équations du premier degré</h2>
<h3>Type ax + b = c</h3>
<p>On retire d’abord la constante, puis on divise par le coefficient : {M('3x + 7 = 22')} donne {M('3x = 15')} (on a fait −7 des deux côtés), puis {M('x = 15 ÷ 3 = 5')}.</p>
<h3>Type ax + b = cx + d</h3>
<p>On regroupe les {M('x')} d’un côté et les nombres de l’autre, en écrivant chaque étape.</p>
<div class="ex"><h3>Exercice 1</h3>
<div class="q"><p>Résoudre {M('5x − 3 = 2x + 9')}.</p></div>
<div class="s"><span class="lbl">Correction</span><ol>
<li>On soustrait {M('2x')} des deux côtés : {M('3x − 3 = 9')}.</li>
<li>On ajoute 3 des deux côtés : {M('3x = 12')}.</li>
<li>On divise par 3 : <strong>{M('x = 4')}</strong>.</li>
<li>Vérification : {M('5 × 4 − 3 = 17')} et {M('2 × 4 + 9 = 17')}. ✓ La solution est 4.</li>
</ol></div></div>
</section>

<section id="produit-nul"><h2>Équation produit nul</h2>
<div class="key"><p class="t">Propriété</p><p>Un produit est nul si et seulement si l’un au moins de ses facteurs est nul : {M('A × B = 0')} équivaut à {M('A = 0')} ou {M('B = 0')}.</p></div>
<div class="ex"><h3>Exercice 2</h3>
<div class="q"><p>Résoudre {M('(x − 4)(2x + 6) = 0')}.</p></div>
<div class="s"><span class="lbl">Correction</span>
<p>C’est un produit nul, donc {M('x − 4 = 0')} ou {M('2x + 6 = 0')}.</p>
<p>{M('x − 4 = 0')} donne {M('x = 4')}. {M('2x + 6 = 0')} donne {M('2x = −6')}, donc {M('x = −3')}.</p>
<p><strong>L’équation a deux solutions : 4 et −3.</strong> Surtout ne pas développer : on perdrait la forme produit qui rend la résolution immédiate.</p>
</div></div>
<p>Si l’équation n’est pas déjà sous forme de produit (par exemple {M('x² − 9 = 0')}), on <a href="/calcul-litteral-3eme.html">factorise</a> d’abord : {M('(x − 3)(x + 3) = 0')}.</p>
</section>

<section id="carre"><h2>Équation x² = a</h2>
<ul>
<li>Si {M('a > 0')} : deux solutions, {M('√a')} et {M('−√a')}. Exemple : {M('x² = 49')} donne {M('x = 7')} ou {M('x = −7')}.</li>
<li>Si {M('a = 0')} : une seule solution, {M('x = 0')}.</li>
<li>Si {M('a < 0')} : aucune solution, car un carré n’est jamais négatif. {M('x² = −4')} n’a pas de solution.</li>
</ul>
<p>Si {M('a')} n’est pas un carré parfait, on garde la valeur exacte : {M('x² = 10')} donne {M('x = √10')} ou {M('x = −√10')}. Voir aussi la page <a href="/racine-carree-3eme.html">racine carrée</a>.</p>
</section>

<section id="probleme"><h2>Mettre un problème en équation</h2>
<ol>
<li><strong>Choisir l’inconnue</strong> et l’écrire en toutes lettres : « Soit {M('x')} la somme donnée par Noé, en euros ».</li>
<li><strong>Traduire</strong> chaque information de l’énoncé avec {M('x')}.</li>
<li><strong>Résoudre</strong> l’équation.</li>
<li><strong>Répondre à la question posée</strong>, qui ne porte pas toujours sur {M('x')}, avec une phrase et l’unité.</li>
</ol>
<div class="ex"><h3>Exercice 3 (type Brevet)</h3>
<div class="q"><p>Pour un cadeau, Jade donne 5 € de plus que Noé. À eux deux, ils donnent 37 €. Combien donne Jade ?</p></div>
<div class="s"><span class="lbl">Correction</span>
<p>Soit {M('x')} la somme donnée par Noé, en euros. Jade donne {M('x + 5')}.</p>
<p>{M('x + (x + 5) = 37')}, donc {M('2x + 5 = 37')}, puis {M('2x = 32')} et {M('x = 16')}.</p>
<p>Noé donne 16 €, donc <strong>Jade donne 21 €</strong>. Vérification : {M('16 + 21 = 37')} ✓, et {M('21 − 16 = 5')} ✓.</p>
</div></div>
<h3>Et les inéquations ?</h3>
<p>Même méthode, avec une règle en plus : quand on multiplie ou divise par un nombre <strong>négatif</strong>, on change le sens de l’inégalité. {M('−2x < 6')} donne {M('x > −3')}. Pour vérifier, teste une valeur : {M('x = 0')} vérifie bien {M('−2 × 0 < 6')}.</p>
</section>

{{CTA_BOX}}

<section id="erreurs"><h2>Les erreurs les plus fréquentes</h2>
<ul class="errs">
<li><span class="e">{M('3x = 21')} donc {M('x = 18')}</span><span class="c">{M('3x')} veut dire {M('3 × x')} : on divise par 3, {M('x = 7')}.</span></li>
<li><span class="e">{M('3x = 15')} donc {M('x = 3/15')}</span><span class="c">On divise 15 par 3 : {M('x = 5')}. Vérifie en remplaçant.</span></li>
<li><span class="e">{M('3x + 7 = 22')} donc {M('3x = 29')}</span><span class="c">On fait −7 des deux côtés, et on l’écrit : {M('3x = 15')}.</span></li>
<li><span class="e">{M('5x − 3 = 2x + 9')} donc {M('7x = 12')}</span><span class="c">Pour déplacer {M('2x')}, on le soustrait des deux côtés : {M('3x = 12')}.</span></li>
<li><span class="e">{M('(x − 4)(2x + 6) = 0')} : solutions 4 et 6</span><span class="c">On résout {M('2x + 6 = 0')} : la deuxième solution est −3.</span></li>
<li><span class="e">{M('x² = 9')} : une seule solution, 3</span><span class="c">{M('(−3)² = 9')} aussi : deux solutions, 3 et −3.</span></li>
<li><span class="e">{M('x² = 16')} donc {M('x = 8')}</span><span class="c">On cherche le nombre qui, multiplié par lui-même, donne 16 : 4 (et −4).</span></li>
<li><span class="e">Donner {M('x')} comme réponse finale</span><span class="c">Relire la question : on demandait peut-être la somme de Jade, pas celle de Noé.</span></li>
</ul>
</section>
''',
    faq=[
        ('Comment vérifier la solution d’une équation ?', 'Remplace x par ta solution dans l’équation de départ. Calcule le membre de gauche et le membre de droite séparément. S’ils donnent le même nombre, la solution est juste. Au Brevet, écrire cette vérification montre que tu maîtrises la notion.'),
        ('Pourquoi une équation x² = a a-t-elle deux solutions ?', 'Parce qu’un nombre et son opposé ont le même carré : 5² = 25 et (−5)² = 25. Si a est positif, il y a donc deux solutions, √a et −√a. Si a est négatif, il n’y en a aucune.'),
        ('Qu’est-ce qu’une équation produit nul ?', 'C’est une équation de la forme A × B = 0, par exemple (x − 1)(x + 3) = 0. Un produit est nul si l’un des facteurs est nul : on résout x − 1 = 0 et x + 3 = 0 séparément. Ici, les solutions sont 1 et −3.'),
        ('Comment choisir l’inconnue dans un problème ?', 'Prends la quantité qui permet d’exprimer toutes les autres le plus simplement, souvent la plus petite ou celle dont les autres dépendent. Écris toujours « Soit x … » avec l’unité : c’est attendu au Brevet.'),
    ],
    related=['/calcul-litteral-3eme.html', '/fonction-affine-3eme.html', '/fonctions-3eme.html', '/racine-carree-3eme.html', '/exercices-maths-3eme-brevet.html'],
))

# ─────────────────────────────── FONCTIONS (image / antécédent)
f1 = lambda x: x * x - 2 * x - 1
SVG_F = graph(f1, -2, 4, -2, 7, 'Courbe de la fonction f(x) = x² − 2x − 1 pour x entre −2 et 4. Elle passe par les points (−1 ; 2), (1 ; −2) et (3 ; 2).',
              points=[(3, 2, 'A(3 ; 2)'), (-1, 2, 'B(−1 ; 2)')], marks=[(3, 2)], unit=34)

PAGES.append(dict(
    path='/fonctions-3eme.html', src='fonctions', crumb='Fonctions',
    title='Fonctions 3e : image, antécédent, lecture graphique | Matheux',
    desc='Fonctions en 3e : notation f(x), calculer une image, trouver un antécédent par le calcul ou sur un graphique, lire un tableau de valeurs. Exercices corrigés.',
    eyebrow='Maths 3e · Organisation et gestion de données, fonctions',
    h1='Fonctions en 3e : image et antécédent, enfin clairs',
    h1_text='Fonctions en 3e : image, antécédent et lecture graphique',
    lead='Une fonction est une machine : on y entre un nombre, elle en ressort un autre. Tout le chapitre repose sur une seule distinction, entre l’entrée et la sortie. Une fois qu’elle est claire, les questions du Brevet deviennent mécaniques.',
    teaches=['Notation f(x)', 'Calculer une image', 'Lire une image et un antécédent sur un graphique', 'Déterminer un antécédent par le calcul', 'Lire un tableau de valeurs'],
    toc=[('essentiel', 'Image et antécédent'), ('formule', 'Avec une formule'), ('tableau', 'Avec un tableau'), ('graphique', 'Sur un graphique'), ('erreurs', 'Erreurs fréquentes'), ('faq', 'Questions fréquentes')],
    body=f'''
<section id="essentiel"><h2>Image et antécédent : la seule chose à comprendre</h2>
<div class="key"><p class="t">Vocabulaire</p><ul>
<li>{M('f(3) = 2')} se lit « f de 3 égale 2 ».</li>
<li><strong>2 est l’image de 3</strong> par {M('f')} : c’est la <strong>sortie</strong>.</li>
<li><strong>3 est un antécédent de 2</strong> par {M('f')} : c’est l’<strong>entrée</strong>.</li>
</ul></div>
<p>Un nombre a <strong>une seule image</strong>. En revanche, un nombre peut avoir <strong>plusieurs antécédents</strong>, ou aucun. C’est pour cela qu’on dit « <em>l’</em>image » mais « <em>un</em> antécédent ».</p>
<p>Attention, {M('f(5)')} n’est pas « f fois 5 ». C’est ce que la machine {M('f')} donne quand on y entre 5.</p>
</section>

<section id="formule"><h2>Avec une formule : calculer</h2>
<p>Pour une <strong>image</strong>, on remplace {M('x')} par le nombre, entre parenthèses, puis on calcule. Pour un <strong>antécédent</strong>, on écrit l’équation {M('f(x) = k')} et on la résout.</p>
<div class="ex"><h3>Exercice 1 : calculer une image</h3>
<div class="q"><p>Soit {M('f(x) = x² − 2x − 1')}. Calculer {M('f(3)')} et {M('f(−2)')}.</p></div>
<div class="s"><span class="lbl">Correction</span>
<p>{M('f(3) = 3² − 2 × 3 − 1 = 9 − 6 − 1 = 2')}. L’image de 3 est 2.</p>
<p>{M('f(−2) = (−2)² − 2 × (−2) − 1 = 4 + 4 − 1 = 7')}. Les parenthèses autour de −2 évitent l’erreur {M('−2² = −4')}.</p>
</div></div>
<div class="ex"><h3>Exercice 2 : antécédent par le calcul</h3>
<div class="q"><p>Soit {M('g(x) = 3x − 7')}. Déterminer l’antécédent de 11 par {M('g')}. Puis, pour {M('h(x) = x² − 9')}, déterminer les antécédents de 0.</p></div>
<div class="s"><span class="lbl">Correction</span>
<p>On résout {M('3x − 7 = 11')} : {M('3x = 18')}, donc {M('x = 6')}. Vérification : {M('g(6) = 18 − 7 = 11')} ✓. L’antécédent de 11 est 6.</p>
<p>On résout {M('x² − 9 = 0')}, soit {M('x² = 9')} : {M('x = 3')} ou {M('x = −3')}. <strong>0 a deux antécédents : 3 et −3.</strong> (Voir <a href="/equations-3eme.html#carre">équation x² = a</a>.)</p>
</div></div>
</section>

<section id="tableau"><h2>Avec un tableau de valeurs : lire</h2>
<div class="scroll"><table class="t"><caption class="note" style="caption-side:bottom;text-align:left;padding-top:.3rem">Tableau de valeurs d’une fonction k</caption>
<tr><th scope="row">{M('x')}</th><td>−1</td><td>0</td><td>2</td><td>5</td></tr>
<tr><th scope="row">{M('k(x)')}</th><td>4</td><td>1</td><td>−5</td><td>1</td></tr></table></div>
<p>La première ligne contient les entrées, la seconde les sorties. L’image de 2 est −5 : on part de 2 sur la ligne du haut. Les antécédents de 1 sont 0 et 5 : on part de 1 sur la ligne du bas, et on relève <strong>toutes</strong> les colonnes où il apparaît.</p>
</section>

<section id="graphique"><h2>Sur un graphique : lire sur les bons axes</h2>
{SVG_F}
<p class="note" style="text-align:center">Courbe de {M('f(x) = x² − 2x − 1')}. Un carreau = 1 unité.</p>
<ul>
<li><strong>Image de 3</strong> : on part de 3 sur l’axe horizontal (abscisses), on monte jusqu’à la courbe (point A), puis on lit sur l’axe vertical : {M('f(3) = 2')}.</li>
<li><strong>Antécédents de 2</strong> : on part de 2 sur l’axe vertical (ordonnées), on trace la droite horizontale {M('y = 2')} et on relève <strong>tous</strong> les points d’intersection : A et B. Les antécédents de 2 sont 3 et −1.</li>
</ul>
<p>Avant toute lecture, vérifie la graduation : un carreau ne vaut pas toujours 1. Une lecture graphique donne souvent une valeur approchée. Si l’énoncé donne la formule, le calcul permet de confirmer : {M('f(−1) = 1 + 2 − 1 = 2')} ✓.</p>
</section>

{{CTA_BOX}}

<section id="erreurs"><h2>Les erreurs les plus fréquentes</h2>
<ul class="errs">
<li><span class="e">Lire {M('f(5)')} comme « f × 5 »</span><span class="c">{M('f(5)')} est la sortie quand on entre 5 dans la machine {M('f')}.</span></li>
<li><span class="e">Répondre l’antécédent quand on demande l’image</span><span class="c">Image = sortie, antécédent = entrée. Écris « {M('f(… ) = …')} » et place chaque nombre.</span></li>
<li><span class="e">Partir de l’axe vertical pour lire une image</span><span class="c">Image : on part de l’axe horizontal. Antécédent : on part de l’axe vertical.</span></li>
<li><span class="e">Ne donner qu’un antécédent</span><span class="c">Trace la droite horizontale en entier et relève toutes les intersections.</span></li>
<li><span class="e">Calculer {M('g(27)')} au lieu de résoudre {M('g(x) = 27')}</span><span class="c">« Antécédent de 27 » : 27 est la sortie. On écrit l’équation {M('g(x) = 27')}.</span></li>
<li><span class="e">Supposer qu’un carreau vaut 1</span><span class="c">Repère la valeur d’une graduation avant de lire quoi que ce soit.</span></li>
</ul>
</section>
''',
    faq=[
        ('Quelle est la différence entre image et antécédent ?', 'L’image est le nombre qui sort de la fonction, l’antécédent est le nombre qui y entre. Si f(4) = 10, alors 10 est l’image de 4 et 4 est un antécédent de 10.'),
        ('Un nombre peut-il avoir plusieurs images ?', 'Non. Par une fonction, chaque nombre a une seule image. En revanche, un nombre peut avoir plusieurs antécédents, ou aucun. Par exemple, pour f(x) = x², le nombre 9 a deux antécédents (3 et −3) et le nombre −1 n’en a aucun.'),
        ('Comment trouver un antécédent sur un graphique ?', 'Place le nombre sur l’axe vertical, trace une droite horizontale à cette hauteur, et relève l’abscisse de chaque point où elle coupe la courbe. Chaque abscisse est un antécédent.'),
        ('Quelle est la différence avec une fonction affine ?', 'Une fonction affine est un cas particulier de fonction, de la forme f(x) = ax + b, dont la courbe est une droite. Le vocabulaire image et antécédent s’applique de la même façon.'),
    ],
    related=['/fonction-affine-3eme.html', '/equations-3eme.html', '/statistiques-brevet.html', '/calcul-litteral-3eme.html', '/exercices-maths-3eme-brevet.html'],
))

# ─────────────────────────────── FONCTION AFFINE
f2 = lambda x: 2 * x - 1
SVG_A = graph(f2, -2, 4, -4, 6, 'Droite représentant f(x) = 2x − 1. Elle coupe l’axe vertical en −1 et passe par le point (2 ; 3).',
              points=[(0, -1, 'B(0 ; −1)'), (2, 3, 'C(2 ; 3)')], unit=34)

PAGES.append(dict(
    path='/fonction-affine-3eme.html', src='fonction_affine', crumb='Fonction affine',
    title='Fonction affine et linéaire 3e : cours et exercices | Matheux',
    desc='Fonction affine et linéaire en 3e : sens de a et b, proportionnalité, droite, trouver f(x) = ax + b avec deux points. Exercices corrigés.',
    eyebrow='Maths 3e · Fonctions',
    h1='Fonction affine et fonction linéaire en 3e',
    h1_text='Fonction affine et fonction linéaire en 3e',
    lead='f(x) = ax + b : deux nombres suffisent à décrire la fonction. Au Brevet, on te demande de les interpréter (un forfait, un prix par unité), de tracer la droite ou de comparer deux offres. Voici comment faire, exemples corrigés à l’appui.',
    teaches=['Reconnaître une fonction affine ou linéaire', 'Interpréter les coefficients a et b', 'Représenter une fonction affine par une droite', 'Déterminer une fonction affine à partir de deux valeurs', 'Comparer deux fonctions affines'],
    toc=[('definition', 'Définitions'), ('a-et-b', 'Le sens de a et b'), ('droite', 'La droite représentative'), ('deux-points', 'Trouver a et b'), ('comparer', 'Comparer deux offres'), ('erreurs', 'Erreurs fréquentes'), ('faq', 'Questions fréquentes')],
    body=f'''
<section id="definition"><h2>Définitions</h2>
<div class="key"><p class="t">À retenir</p><ul>
<li><strong>Fonction affine</strong> : {M('f(x) = ax + b')}, où {M('a')} et {M('b')} sont deux nombres fixés.</li>
<li><strong>Fonction linéaire</strong> : le cas {M('b = 0')}, soit {M('f(x) = ax')}. Elle traduit une situation de <strong>proportionnalité</strong>, de coefficient {M('a')}.</li>
<li>Une fonction affine est représentée par une <strong>droite</strong>. Si elle est linéaire, la droite passe par l’origine.</li>
</ul></div>
<p>{M('f(x) = 3x − 5')} est affine ({M('a = 3')}, {M('b = −5')}). {M('g(x) = −x')} est linéaire ({M('a = −1')}). En revanche, {M('h(x) = x² + 1')} et {M('k(x) = 3/x')} ne sont <strong>pas</strong> affines : dans une fonction affine, {M('x')} n’apparaît qu’à la puissance 1 et jamais au dénominateur.</p>
</section>

<section id="a-et-b"><h2>Le sens de a et b dans une situation</h2>
<p>{M('b')} est la valeur de départ, pour {M('x = 0')} : un forfait, un abonnement, une hauteur initiale. {M('a')} est ce qui s’ajoute à chaque fois que {M('x')} augmente de 1 : un prix par minute, une vitesse, un tarif par séance.</p>
<div class="ex"><h3>Exercice 1 : interpréter a et b</h3>
<div class="q"><p>Un forfait de téléphone coûte 12 € par mois, plus 0,15 € par minute de communication hors forfait. On note {M('x')} le nombre de minutes hors forfait.</p><ol><li>Exprimer le prix {M('p(x)')}.</li><li>Calculer le prix pour 100 minutes.</li><li>La fonction est-elle linéaire ?</li></ol></div>
<div class="s"><span class="lbl">Correction</span><ol>
<li>{M('p(x) = 0,15x + 12')} : {M('a = 0,15')} (prix d’une minute) et {M('b = 12')} (le forfait). L’ordre d’écriture ne change rien : {M('12 + 0,15x')} est la même fonction, et {M('a')} est toujours le nombre qui multiplie {M('x')}.</li>
<li>{M('p(100) = 0,15 × 100 + 12 = 15 + 12 = 27')}. Le prix est de 27 €.</li>
<li>Non, car {M('b = 12 ≠ 0')}. Le prix n’est pas proportionnel au nombre de minutes : 200 minutes coûtent 42 €, pas le double de 27 €.</li>
</ol></div></div>
</section>

<section id="droite"><h2>La droite représentative</h2>
{SVG_A}
<p class="note" style="text-align:center">Droite de {M('f(x) = 2x − 1')}. Un carreau = 1 unité.</p>
<ul>
<li>{M('b')} est l’<strong>ordonnée à l’origine</strong> : la droite coupe l’axe vertical en {M('b')}. Ici, en −1 (point B).</li>
<li>{M('a')} est le <strong>coefficient directeur</strong> : quand on avance de 1 vers la droite, on monte de {M('a')}. Ici, de B à C, on avance de 2 et on monte de 4, soit {M('a = 4 ÷ 2 = 2')}.</li>
<li>Si {M('a > 0')}, la droite monte. Si {M('a < 0')}, elle descend. Si {M('a = 0')}, elle est horizontale.</li>
</ul>
<p>Pour tracer une droite, deux points suffisent. Calcule deux images, par exemple {M('f(0) = −1')} et {M('f(2) = 3')}, puis relie les points. Un troisième point sert de vérification.</p>
</section>

<section id="deux-points"><h2>Trouver a et b à partir de deux valeurs</h2>
<div class="key"><p class="t">Méthode</p><p>{M('a = ')}{F('f(x₂) − f(x₁)', 'x₂ − x₁')} (variation des images divisée par la variation des antécédents). Puis on trouve {M('b')} en remplaçant les coordonnées d’un point dans {M('f(x) = ax + b')}.</p></div>
<div class="ex"><h3>Exercice 2</h3>
<div class="q"><p>{M('f')} est une fonction affine telle que {M('f(2) = 5')} et {M('f(6) = −3')}. Déterminer {M('f(x)')}.</p></div>
<div class="s"><span class="lbl">Correction</span><ol>
<li>{M('a = ')}{F('−3 − 5', '6 − 2')}{M(' = ')}{F('−8', '4')}{M(' = −2')}.</li>
<li>{M('f(2) = 5')} donne {M('−2 × 2 + b = 5')}, donc {M('b = 9')}.</li>
<li><strong>{M('f(x) = −2x + 9')}</strong>. Vérification : {M('f(6) = −12 + 9 = −3')} ✓.</li>
</ol></div></div>
</section>

<section id="comparer"><h2>Comparer deux offres (classique du Brevet)</h2>
<div class="ex"><h3>Exercice 3</h3>
<div class="q"><p>Une piscine propose deux tarifs. Tarif A : 15 € la séance. Tarif B : une carte annuelle de 30 €, puis 9 € la séance. À partir de combien de séances le tarif B est-il plus avantageux ?</p></div>
<div class="s"><span class="lbl">Correction</span>
<p>Pour {M('x')} séances : {M('A(x) = 15x')} (linéaire) et {M('B(x) = 9x + 30')} (affine).</p>
<p>Les deux tarifs sont égaux quand {M('15x = 9x + 30')}, soit {M('6x = 30')} et {M('x = 5')}. Pour 5 séances, les deux coûtent 75 €.</p>
<p>Pour 4 séances : A coûte 60 € et B coûte 66 €. A est moins cher. Pour 6 séances : A coûte 90 € et B coûte 84 €. B est moins cher. <strong>Le tarif B devient plus avantageux à partir de 6 séances.</strong> Sur un graphique, c’est l’abscisse du point d’intersection des deux droites qui marque le changement.</p>
</div></div>
</section>

{{CTA_BOX}}

<section id="erreurs"><h2>Les erreurs les plus fréquentes</h2>
<ul class="errs">
<li><span class="e">Dans {M('0,15x + 12')}, prendre 12 pour le prix par minute</span><span class="c">{M('b')} est la valeur pour {M('x = 0')} (le forfait). {M('a')} multiplie {M('x')}.</span></li>
<li><span class="e">Dans {M('12 + 0,15x')}, dire que {M('a = 12')}</span><span class="c">{M('a')} n’est pas « le premier nombre écrit », c’est le coefficient de {M('x')}.</span></li>
<li><span class="e">Croire qu’une fonction affine avec {M('b ≠ 0')} est proportionnelle</span><span class="c">Proportionnalité ↔ fonction linéaire ↔ droite passant par l’origine.</span></li>
<li><span class="e">Calculer {M('a = Δx ÷ Δy')}</span><span class="c">C’est l’inverse : variation des images (verticale) ÷ variation des antécédents (horizontale).</span></li>
<li><span class="e">Calculer {M('a = y ÷ x')} avec un seul point</span><span class="c">Il faut deux points, sauf si la fonction est linéaire.</span></li>
<li><span class="e">Trouver {M('a')} et oublier {M('b')}</span><span class="c">Remplace les coordonnées d’un point dans {M('y = ax + b')}.</span></li>
<li><span class="e">Tracer une droite qui monte avec {M('a < 0')}</span><span class="c">{M('a')} négatif : la droite descend quand on va vers la droite.</span></li>
</ul>
</section>
''',
    faq=[
        ('Quelle est la différence entre fonction affine et fonction linéaire ?', 'Une fonction linéaire s’écrit f(x) = ax. C’est une fonction affine avec b = 0. Elle modélise une proportionnalité, et sa droite passe par l’origine. Une fonction affine f(x) = ax + b avec b ≠ 0 ne passe pas par l’origine.'),
        ('Comment trouver le coefficient directeur a ?', 'Avec deux points de la droite : a = (différence des ordonnées) ÷ (différence des abscisses). Sur un graphique, on avance de 1 carreau vers la droite et on compte de combien on monte (a positif) ou on descend (a négatif).'),
        ('Comment savoir si un point est sur la droite ?', 'Calcule l’image de son abscisse. Pour le point M(4 ; 7) et f(x) = 2x − 1, f(4) = 7 : le point est sur la droite. Si tu trouves un autre nombre, il n’y est pas.'),
        ('Une fonction affine peut-elle être constante ?', 'Oui, si a = 0 : f(x) = b pour tout x. Sa représentation est une droite horizontale.'),
    ],
    related=['/fonctions-3eme.html', '/equations-3eme.html', '/calcul-litteral-3eme.html', '/statistiques-brevet.html', '/exercices-maths-3eme-brevet.html'],
))
