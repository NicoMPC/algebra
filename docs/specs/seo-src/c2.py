from build import F, M

PAGES = []

# ─────────────────────────────── PUISSANCES
PAGES.append(dict(
    path='/puissances-3eme.html', src='puissances', crumb='Puissances',
    title='Puissances 3e : règles et notation scientifique | Matheux',
    desc='Puissances en 3e : règles de calcul, puissances de 10, exposants négatifs, notation scientifique, préfixes. Exercices corrigés et erreurs fréquentes.',
    eyebrow='Maths 3e · Nombres et calculs',
    h1='Puissances en 3e : les règles et la notation scientifique',
    h1_text='Puissances et notation scientifique en 3e',
    lead='Une puissance compte des facteurs : 2³ = 2 × 2 × 2. Toutes les règles de calcul découlent de cette idée. Si tu l’as en tête, tu n’as presque rien à apprendre par cœur. Cours, exemples et pièges classiques.',
    teaches=['Calculer une puissance', 'Règles de calcul sur les puissances', 'Puissances de 10 et exposants négatifs', 'Notation scientifique', 'Calculer et comparer en notation scientifique'],
    toc=[('definition', 'Définition'), ('regles', 'Les règles de calcul'), ('dix', 'Puissances de 10'), ('scientifique', 'Notation scientifique'), ('exemples', 'Exercices corrigés'), ('erreurs', 'Erreurs fréquentes'), ('faq', 'Questions fréquentes')],
    body=f'''
<section id="definition"><h2>Définition</h2>
<div class="key"><p class="t">À retenir</p><ul>
<li>{M('aⁿ = a × a × … × a')} ({M('n')} facteurs). {M('a')} est la base, {M('n')} l’exposant.</li>
<li>{M('a¹ = a')} et {M('a⁰ = 1')} (pour {M('a ≠ 0')}).</li>
<li>{M('a⁻ⁿ = ')}{F('1', 'aⁿ')} : un exposant négatif donne un inverse, pas un nombre négatif.</li>
</ul></div>
<p>Attention aux signes : {M('(−3)² = (−3) × (−3) = 9')}, mais {M('−3² = −(3 × 3) = −9')}. La parenthèse change tout. Une puissance paire d’un nombre négatif est positive, une puissance impaire est négative : {M('(−2)³ = −8')}.</p>
<p>Et avec les décimaux : {M('0,3² = 0,3 × 0,3 = 0,09')}, pas 0,9.</p>
</section>

<section id="regles"><h2>Les règles de calcul</h2>
<div class="scroll"><table class="t">
<tr><th>Règle</th><th>Exemple</th><th>Pourquoi</th></tr>
<tr><td>{M('aᵐ × aⁿ = aᵐ⁺ⁿ')}</td><td>{M('2³ × 2⁴ = 2⁷')}</td><td>3 facteurs puis 4 facteurs : 7 facteurs</td></tr>
<tr><td>{M('aᵐ ÷ aⁿ = aᵐ⁻ⁿ')}</td><td>{M('5⁶ ÷ 5² = 5⁴')}</td><td>on simplifie 2 facteurs en haut et en bas</td></tr>
<tr><td>{M('(aᵐ)ⁿ = aᵐˣⁿ')}</td><td>{M('(10²)³ = 10⁶')}</td><td>3 fois le bloc de 2 facteurs</td></tr>
</table></div>
<p>Ces règles ne valent que pour la <strong>multiplication et la division de puissances de même base</strong>. Il n’existe pas de règle pour une somme : {M('2³ + 2⁴ = 8 + 16 = 24')}, ce n’est pas {M('2⁷')}.</p>
</section>

<section id="dix"><h2>Puissances de 10</h2>
<ul>
<li>{M('10ⁿ')} s’écrit avec un 1 suivi de {M('n')} zéros : {M('10⁵ = 100 000')}.</li>
<li>{M('10⁻ⁿ')} a le 1 au {M('n')}-ième rang après la virgule : {M('10⁻³ = 0,001')}.</li>
</ul>
<p>Les préfixes d’unités en sont directement tirés : kilo = {M('10³')}, méga = {M('10⁶')}, giga = {M('10⁹')}, milli = {M('10⁻³')}, micro = {M('10⁻⁶')}, nano = {M('10⁻⁹')}. Un disque de 2 To (téraoctets) contient {M('2 × 10¹²')} octets.</p>
</section>

<section id="scientifique"><h2>Notation scientifique</h2>
<div class="key"><p class="t">Définition</p><p>Un nombre est en notation scientifique s’il s’écrit {M('a × 10ⁿ')} avec {M('1 ≤ a < 10')} (un seul chiffre non nul avant la virgule) et {M('n')} entier.</p></div>
<ul>
<li>{M('150 000 000 = 1,5 × 10⁸')} : la virgule s’est déplacée de 8 rangs vers la gauche.</li>
<li>{M('0,000 08 = 8 × 10⁻⁵')} : un nombre plus petit que 1 a un exposant négatif.</li>
<li>{M('0,5 × 10³')} ou {M('45 × 10²')} ne sont <strong>pas</strong> en notation scientifique : on réajuste en {M('5 × 10²')} et {M('4,5 × 10³')}.</li>
</ul>
<p>Pour comparer deux nombres en notation scientifique, on compare d’abord les exposants : {M('1,5 × 10⁸ > 7,8 × 10⁷')}, même si 1,5 est plus petit que 7,8.</p>
</section>

<section id="exemples"><h2>Exercices corrigés</h2>
<div class="ex"><h3>Exercice 1 : appliquer les règles (sans calculatrice)</h3>
<div class="q"><p>Écrire sous la forme d’une seule puissance : {M('A = 2³ × 2⁴')} ; {M('B = ')}{F('10⁻²', '10⁻⁵')} ; {M('C = (10²)³ × 10⁻⁴')}.</p></div>
<div class="s"><span class="lbl">Correction</span>
<p>{M('A = 2³⁺⁴ = 2⁷')} (soit 128). On garde la base 2 : ce n’est pas {M('4⁷')}.</p>
<p>{M('B = 10⁻²⁻⁽⁻⁵⁾ = 10⁻²⁺⁵ = 10³')}. Le piège est dans la soustraction d’un nombre négatif.</p>
<p>{M('C = 10⁶ × 10⁻⁴ = 10²')}.</p>
</div></div>

<div class="ex"><h3>Exercice 2 : calculer en notation scientifique</h3>
<div class="q"><p>Donner l’écriture scientifique de {M('D = (3 × 10⁴) × (5 × 10⁻⁷)')}.</p></div>
<div class="s"><span class="lbl">Correction</span>
<p>On regroupe les nombres et les puissances de 10 : {M('D = (3 × 5) × (10⁴ × 10⁻⁷) = 15 × 10⁻³')}.</p>
<p>15 n’est pas entre 1 et 10 : {M('15 = 1,5 × 10¹')}, donc <strong>{M('D = 1,5 × 10⁻²')}</strong>.</p>
</div></div>

<div class="ex"><h3>Exercice 3 : problème (type Brevet)</h3>
<div class="q"><p>La distance Terre–Soleil est d’environ {M('1,5 × 10⁸')} km. La lumière parcourt environ {M('3 × 10⁵')} km par seconde. Combien de temps met la lumière du Soleil pour nous parvenir ?</p></div>
<div class="s"><span class="lbl">Correction</span>
<p>Temps = distance ÷ vitesse : {F('1,5 × 10⁸', '3 × 10⁵')}{M(' = 0,5 × 10³ = 500')} secondes.</p>
<p>{M('500 s = 8 × 60 s + 20 s')}. <strong>La lumière met environ 8 minutes et 20 secondes.</strong></p>
</div></div>
</section>

{{CTA_BOX}}

<section id="erreurs"><h2>Les erreurs les plus fréquentes</h2>
<ul class="errs">
<li><span class="e">{M('2³ = 6')} ou {M('10⁵ = 50')}</span><span class="c">L’exposant compte les facteurs : {M('2³ = 2 × 2 × 2 = 8')}.</span></li>
<li><span class="e">{M('9² = 18')}</span><span class="c">Carré ≠ double : {M('9² = 9 × 9 = 81')}.</span></li>
<li><span class="e">{M('(−3)² = −9')}</span><span class="c">{M('(−3) × (−3) = 9')}. C’est {M('−3²')} qui vaut −9.</span></li>
<li><span class="e">{M('2³ × 2⁴ = 2¹²')}</span><span class="c">On additionne les exposants dans un produit : {M('2⁷')}.</span></li>
<li><span class="e">{M('2³ × 2⁴ = 4⁷')}</span><span class="c">La base ne change pas.</span></li>
<li><span class="e">{M('10⁻³ = −1000')}</span><span class="c">{M('10⁻³ = 1/1000 = 0,001')} : un nombre positif très petit.</span></li>
<li><span class="e">{M('0,000 08 = 8 × 10⁵')}</span><span class="c">Nombre plus petit que 1 : exposant négatif, {M('8 × 10⁻⁵')}.</span></li>
<li><span class="e">{M('7,8 × 10⁷ > 1,5 × 10⁸')} « car 7,8 > 1,5 »</span><span class="c">On compare d’abord les exposants.</span></li>
</ul>
</section>

<section id="brevet"><h2>Les puissances au Brevet</h2>
<p>Les puissances apparaissent surtout dans la partie automatismes, sans calculatrice : écrire un nombre en notation scientifique, simplifier un produit de puissances de 10, reconnaître un préfixe. Dans les problèmes, elles servent pour les grandes et les petites grandeurs (astronomie, biologie, informatique). Elles sont aussi un prérequis caché de <a href="/pythagore-brevet.html">Pythagore</a> : confondre carré et double y fait perdre des points chaque année.</p>
</section>
''',
    faq=[
        ('Quelle est la différence entre (−2)² et −2² ?', '(−2)² = (−2) × (−2) = 4 : la parenthèse indique que le signe est élevé au carré. −2² = −(2 × 2) = −4 : seul le 2 est au carré, le signe moins reste devant.'),
        ('Combien vaut un nombre à la puissance 0 ?', 'Tout nombre non nul à la puissance 0 vaut 1. Par exemple 10⁰ = 1 et 7⁰ = 1. C’est cohérent avec la règle du quotient : 5² ÷ 5² = 5⁰, et c’est aussi 25 ÷ 25 = 1.'),
        ('Comment écrire un nombre en notation scientifique ?', 'Place la virgule juste après le premier chiffre non nul, puis compte de combien de rangs tu l’as déplacée. Vers la gauche, l’exposant est positif (grand nombre). Vers la droite, il est négatif (nombre plus petit que 1). Exemple : 0,0042 = 4,2 × 10⁻³.'),
        ('Un exposant négatif donne-t-il un nombre négatif ?', 'Non. 10⁻² = 1/100 = 0,01, qui est positif. Un exposant négatif donne l’inverse d’une puissance.'),
    ],
    related=['/racine-carree-3eme.html', '/calcul-litteral-3eme.html', '/arithmetique-3eme.html', '/fractions-brevet.html', '/exercices-maths-3eme-brevet.html'],
))

# ─────────────────────────────── RACINE CARRÉE
PAGES.append(dict(
    path='/racine-carree-3eme.html', src='racine_carree', crumb='Racine carrée',
    title='Racine carrée 3e : définition, calculs et exercices | Matheux',
    desc='Racine carrée en 3e : définition, carrés parfaits à connaître, encadrement, produit et quotient de racines, lien avec Pythagore et x² = a. Exercices corrigés.',
    eyebrow='Maths 3e · Nombres et calculs',
    h1='La racine carrée en 3e, sans se tromper',
    h1_text='La racine carrée en 3e',
    lead='√25 = 5, parce que 5 × 5 = 25. La racine carrée est l’opération inverse du carré. Elle sert dans presque tous les exercices de Pythagore. Voici ce qu’il faut savoir, et les deux ou trois erreurs qui coûtent le plus cher.',
    teaches=['Définition de la racine carrée', 'Carrés parfaits', 'Encadrer une racine carrée', 'Produit et quotient de racines carrées', 'Utiliser la racine carrée avec Pythagore et x² = a'],
    toc=[('definition', 'Définition'), ('carres', 'Carrés parfaits'), ('regles', 'Règles de calcul'), ('exemples', 'Exercices corrigés'), ('erreurs', 'Erreurs fréquentes'), ('faq', 'Questions fréquentes')],
    body=f'''
<section id="definition"><h2>Définition</h2>
<div class="key"><p class="t">À retenir</p><p>Pour un nombre {M('a ≥ 0')}, {M('√a')} est le nombre <strong>positif</strong> dont le carré est {M('a')}. Autrement dit, {M('(√a)² = a')} et {M('√a ≥ 0')}.</p></div>
<ul>
<li>{M('√49 = 7')} car {M('7² = 49')} et {M('7 ≥ 0')}.</li>
<li>{M('√0 = 0')} et {M('√1 = 1')}.</li>
<li>{M('√(−9)')} n’existe pas : aucun nombre au carré ne donne un résultat négatif.</li>
</ul>
<p>Prendre la racine carrée n’est <strong>pas</strong> diviser par 2 : {M('√64 = 8')}, pas 32.</p>
</section>

<section id="carres"><h2>Les carrés parfaits à connaître</h2>
<div class="scroll"><table class="t">
<tr><th>{M('n')}</th><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td><td>8</td><td>9</td><td>10</td><td>11</td><td>12</td><td>13</td><td>14</td><td>15</td></tr>
<tr><th>{M('n²')}</th><td>1</td><td>4</td><td>9</td><td>16</td><td>25</td><td>36</td><td>49</td><td>64</td><td>81</td><td>100</td><td>121</td><td>144</td><td>169</td><td>196</td><td>225</td></tr>
</table></div>
<p>Les connaître par cœur permet de calculer sans calculatrice, dans la partie automatismes du Brevet, et d’<strong>encadrer</strong> une racine : comme {M('25 < 30 < 36')}, on a {M('5 < √30 < 6')}. C’est aussi un bon moyen de contrôler un résultat de calculatrice.</p>
<p>Avec les décimaux, on compte les décimales : {M('√0,25 = 0,5')} car {M('0,5 × 0,5 = 0,25')}. Et {M('√0,09 = 0,3')}.</p>
</section>

<section id="regles"><h2>Règles de calcul</h2>
<ul>
<li>{M('√a × √b = √(a × b)')} : {M('√8 × √2 = √16 = 4')}.</li>
<li>{M('√a ÷ √b = √(a ÷ b)')} (avec {M('b > 0')}) : {M('√(9/16) = 3/4')}.</li>
<li>{M('√a × √a = a')} : {M('√2 × √2 = 2')}.</li>
<li><strong>Pas de règle pour la somme</strong> : {M('√9 + √16 = 3 + 4 = 7')}, alors que {M('√(9 + 16) = √25 = 5')}.</li>
</ul>
<p class="note">Pour aller plus loin : écrire {M('√50 = √(25 × 2) = 5√2')}, c’est simplifier une racine. Cette technique va au-delà des attendus du Brevet, mais elle resservira au lycée.</p>
</section>

<section id="exemples"><h2>Exercices corrigés</h2>
<div class="ex"><h3>Exercice 1 : sans calculatrice</h3>
<div class="q"><p>Calculer {M('√144')}, {M('√0,49')}, {M('√3 × √12')} et {M('(√7)²')}.</p></div>
<div class="s"><span class="lbl">Correction</span>
<p>{M('√144 = 12')} ; {M('√0,49 = 0,7')} ; {M('√3 × √12 = √36 = 6')} ; {M('(√7)² = 7')}.</p>
</div></div>

<div class="ex"><h3>Exercice 2 : encadrer</h3>
<div class="q"><p>Encadrer {M('√70')} entre deux entiers consécutifs, puis en donner une valeur approchée au dixième.</p></div>
<div class="s"><span class="lbl">Correction</span>
<p>{M('64 < 70 < 81')}, donc {M('8 < √70 < 9')}. À la calculatrice, {M('√70 ≈ 8,37')}, soit <strong>{M('√70 ≈ 8,4')}</strong> au dixième. Le résultat est bien entre 8 et 9.</p>
</div></div>

<div class="ex"><h3>Exercice 3 : avec Pythagore</h3>
<div class="q"><p>Un triangle ABC est rectangle en A, avec AB = 2 cm et AC = 3 cm. Calculer BC, en valeur exacte puis arrondie au millimètre.</p></div>
<div class="s"><span class="lbl">Correction</span>
<p>D’après le théorème de Pythagore : {M('BC² = AB² + AC² = 4 + 9 = 13')}.</p>
<p>BC est une longueur, donc positive : <strong>{M('BC = √13')} cm</strong> (valeur exacte), soit <strong>{M('BC ≈ 3,6')} cm</strong>. Vérification : 3,6 est bien plus grand que 3 (l’hypoténuse est le plus long côté) et plus petit que {M('2 + 3 = 5')}.</p>
</div></div>
</section>

{{CTA_BOX}}

<section id="erreurs"><h2>Les erreurs les plus fréquentes</h2>
<ul class="errs">
<li><span class="e">{M('√64 = 32')}</span><span class="c">Ce n’est pas une division par 2 : {M('8 × 8 = 64')}, donc {M('√64 = 8')}.</span></li>
<li><span class="e">{M('AC² = 25')}, donc {M('AC = 25')}</span><span class="c">Il faut finir le calcul : {M('AC = √25 = 5')}.</span></li>
<li><span class="e">{M('√9 + √16 = √25')}</span><span class="c">La racine ne se distribue pas sur une somme : 7 ≠ 5.</span></li>
<li><span class="e">{M('√8 × √2 = √10')}</span><span class="c">On multiplie sous la racine : {M('√16 = 4')}.</span></li>
<li><span class="e">{M('√(−9) = −3')}</span><span class="c">{M('√a')} n’existe que pour {M('a ≥ 0')}, et c’est toujours un nombre positif.</span></li>
<li><span class="e">{M('√(a² + b²) = a + b')}</span><span class="c">On calcule la somme des carrés d’abord, puis la racine du total.</span></li>
</ul>
</section>
''',
    faq=[
        ('Pourquoi la racine carrée d’un nombre négatif n’existe-t-elle pas ?', 'Parce qu’un carré n’est jamais négatif : un nombre positif ou négatif multiplié par lui-même donne toujours un résultat positif (ou nul). Aucun nombre n’a donc un carré égal à −9.'),
        ('√(x²) est-il toujours égal à x ?', 'Seulement si x est positif ou nul. Pour x = −3, √((−3)²) = √9 = 3, qui est l’opposé de x. En 3e, les racines servent surtout à calculer des longueurs, qui sont positives.'),
        ('Comment calculer une racine carrée sans calculatrice ?', 'Si le nombre est un carré parfait (1, 4, 9, 16, 25…), on reconnaît la racine. Sinon, on l’encadre entre deux carrés parfaits : 40 est entre 36 et 49, donc √40 est entre 6 et 7.'),
        ('Quelle est la différence entre x² = 25 et x = √25 ?', 'x² = 25 est une équation qui a deux solutions, 5 et −5. En revanche, √25 désigne un seul nombre, 5, toujours positif.'),
    ],
    related=['/pythagore-brevet.html', '/puissances-3eme.html', '/equations-3eme.html', '/trigonometrie-3eme.html', '/exercices-maths-3eme-brevet.html'],
))

# ─────────────────────────────── TRIGONOMÉTRIE
TRI_SVG = '''<svg viewBox="0 0 300 190" width="100%" style="max-width:340px;display:block;margin:0 auto 1rem;background:#fff;border:1px solid #E2E8F0;border-radius:12px" role="img" aria-label="Triangle ABC rectangle en A. Pour l’angle en B : AB est le côté adjacent, AC le côté opposé, BC l’hypoténuse.">
<polygon points="40,150 250,150 250,40" fill="#EEF2FF" stroke="#0F172A" stroke-width="2"/>
<path d="M238 150 V138 H250" fill="none" stroke="#0F172A" stroke-width="1.5"/>
<path d="M75 150 A35 35 0 0 0 71 134" fill="none" stroke="#B91C1C" stroke-width="2.5"/>
<text x="24" y="166" font-size="15" font-weight="700" fill="#0F172A">B</text>
<text x="256" y="166" font-size="15" font-weight="700" fill="#0F172A">A</text>
<text x="256" y="40" font-size="15" font-weight="700" fill="#0F172A">C</text>
<text x="80" y="143" font-size="12" fill="#B91C1C">angle B</text>
<text x="112" y="172" font-size="13" font-weight="700" fill="#1E40AF">adjacent (AB)</text>
<text x="258" y="100" font-size="13" font-weight="700" fill="#047857">opp.</text>
<text x="258" y="115" font-size="12" fill="#047857">(AC)</text>
<text x="92" y="84" font-size="13" font-weight="700" fill="#0F172A" transform="rotate(-27 120 90)">hypoténuse (BC)</text>
</svg>'''

PAGES.append(dict(
    path='/trigonometrie-3eme.html', src='trigonometrie', crumb='Trigonométrie',
    title='Trigonométrie 3e : cosinus, sinus, tangente | Matheux',
    desc='Trigonométrie en 3e : nommer les côtés, choisir cos, sin ou tan (SOH CAH TOA), calculer une longueur ou un angle. Exercices corrigés type Brevet.',
    eyebrow='Maths 3e · Espace et géométrie',
    h1='Trigonométrie en 3e : cosinus, sinus et tangente',
    h1_text='Trigonométrie en 3e : cosinus, sinus et tangente',
    lead='Dans un triangle rectangle, la trigonométrie relie un angle et deux longueurs. Trois formules, une méthode en quatre étapes, et une vérification de la calculatrice : c’est tout ce qu’il faut pour réussir ces questions du Brevet.',
    teaches=['Nommer côté adjacent, côté opposé et hypoténuse', 'Choisir cosinus, sinus ou tangente', 'Calculer une longueur avec la trigonométrie', 'Calculer un angle avec la trigonométrie'],
    toc=[('cotes', 'Nommer les côtés'), ('formules', 'Les trois formules'), ('methode', 'La méthode'), ('exemples', 'Exercices corrigés'), ('erreurs', 'Erreurs fréquentes'), ('faq', 'Questions fréquentes')],
    body=f'''
<section id="cotes"><h2>Nommer les côtés par rapport à l’angle</h2>
{TRI_SVG}
<p>La trigonométrie ne s’utilise que dans un <strong>triangle rectangle</strong>, et toujours par rapport à un <strong>angle aigu</strong> choisi (ici l’angle en B) :</p>
<ul>
<li>l’<strong>hypoténuse</strong> est en face de l’angle droit, c’est le plus long côté ;</li>
<li>le côté <strong>adjacent</strong> touche l’angle choisi, et ce n’est pas l’hypoténuse ;</li>
<li>le côté <strong>opposé</strong> est en face de l’angle choisi.</li>
</ul>
<p>Si on change d’angle (l’angle en C), l’adjacent et l’opposé s’échangent. L’hypoténuse, elle, ne change jamais.</p>
</section>

<section id="formules"><h2>Les trois formules</h2>
<div class="key"><p class="t">SOH CAH TOA</p><ul>
<li>{M('sin = ')}{F('opposé', 'hypoténuse')} (<strong>S</strong>inus = <strong>O</strong>pposé / <strong>H</strong>ypoténuse)</li>
<li>{M('cos = ')}{F('adjacent', 'hypoténuse')} (<strong>C</strong>osinus = <strong>A</strong>djacent / <strong>H</strong>ypoténuse)</li>
<li>{M('tan = ')}{F('opposé', 'adjacent')} (<strong>T</strong>angente = <strong>O</strong>pposé / <strong>A</strong>djacent)</li>
</ul></div>
<p>Le cosinus et le sinus d’un angle aigu sont toujours compris entre 0 et 1, car l’hypoténuse est au dénominateur et c’est le plus long côté. Si tu trouves un cosinus égal à 1,4, c’est que la fraction est à l’envers.</p>
</section>

<section id="methode"><h2>La méthode en 4 étapes</h2>
<ol>
<li><strong>Repère</strong> le triangle rectangle et l’angle connu (ou cherché).</li>
<li><strong>Nomme</strong> les deux côtés en jeu : celui qu’on connaît et celui qu’on cherche.</li>
<li><strong>Choisis</strong> la formule qui contient exactement ces deux côtés.</li>
<li><strong>Calcule</strong> avec la calculatrice en mode degrés. Pour vérifier le mode, {M('cos(60)')} doit afficher 0,5.</li>
</ol>
</section>

<section id="exemples"><h2>Exercices corrigés</h2>
<div class="ex"><h3>Exercice 1 : calculer une longueur</h3>
<div class="q"><p>ABC est rectangle en A, {M('BC = 8')} cm et l’angle {M('ABC')} mesure 35°. Calculer AB, arrondi au dixième.</p></div>
<div class="s"><span class="lbl">Correction</span>
<p>Par rapport à l’angle en B, [BC] est l’hypoténuse et [AB] le côté adjacent. On utilise le cosinus :</p>
<p>{M('cos(35°) = ')}{F('AB', 'BC')}, donc {M('AB = 8 × cos(35°) ≈ 6,6')} cm.</p>
</div></div>

<div class="ex"><h3>Exercice 2 : l’inconnue au dénominateur</h3>
<div class="q"><p>DEF est rectangle en E, {M('DE = 5')} cm et l’angle {M('EDF')} mesure 40°. Calculer DF, arrondi au dixième.</p></div>
<div class="s"><span class="lbl">Correction</span>
<p>Par rapport à l’angle en D, [DE] est le côté adjacent et [DF] l’hypoténuse : {M('cos(40°) = ')}{F('DE', 'DF')}{M(' = ')}{F('5', 'DF')}.</p>
<p>On isole DF, qui est au dénominateur : {M('DF = ')}{F('5', 'cos(40°)')}{M(' ≈ 6,5')} cm. Vérification : l’hypoténuse (6,5) est bien plus longue que DE (5).</p>
</div></div>

<div class="ex"><h3>Exercice 3 : calculer un angle (type Brevet)</h3>
<div class="q"><p>Une échelle de 5 m est posée contre un mur vertical. Son pied est à 1,5 m du mur, sur un sol horizontal. Quel angle l’échelle fait-elle avec le sol, au degré près ?</p></div>
<div class="s"><span class="lbl">Correction</span>
<p>Le mur, le sol et l’échelle forment un triangle rectangle (le mur est perpendiculaire au sol). L’échelle est l’hypoténuse (5 m). Pour l’angle au sol, la distance au mur est le côté adjacent (1,5 m).</p>
<p>{M('cos(angle) = ')}{F('1,5', '5')}{M(' = 0,3')}, donc {M('angle = cos⁻¹(0,3) ≈ 73°')}.</p>
<p>On connaît le cosinus et on cherche l’angle : il faut la touche <strong>{M('cos⁻¹')}</strong> (parfois notée Arccos ou « 2nde cos »), pas la touche cos.</p>
</div></div>
</section>

{{CTA_BOX}}

<section id="erreurs"><h2>Les erreurs les plus fréquentes</h2>
<ul class="errs">
<li><span class="e">Prendre l’hypoténuse pour le côté adjacent</span><span class="c">L’adjacent touche l’angle et n’est pas l’hypoténuse. Colorie l’angle avant de nommer les côtés.</span></li>
<li><span class="e">Nommer les côtés par rapport à l’angle droit</span><span class="c">On nomme toujours par rapport à l’angle aigu de l’exercice.</span></li>
<li><span class="e">Écrire {M('cos = hypoténuse ÷ adjacent')}</span><span class="c">L’hypoténuse est au dénominateur : un cosinus est toujours inférieur ou égal à 1.</span></li>
<li><span class="e">{M('DF = 5 × cos(40°)')} quand DF est au dénominateur</span><span class="c">{M('cos = 5/DF')} donne {M('DF = 5 ÷ cos(40°)')}.</span></li>
<li><span class="e">Calculatrice en radians ou en grades</span><span class="c">Test : {M('cos(60)')} doit afficher 0,5.</span></li>
<li><span class="e">Utiliser cos au lieu de {M('cos⁻¹')} pour trouver l’angle</span><span class="c">On connaît le rapport, on cherche l’angle : fonction réciproque {M('cos⁻¹')}.</span></li>
</ul>
</section>

<section id="brevet"><h2>La trigonométrie au Brevet</h2>
<p>Elle apparaît souvent dans un problème concret : hauteur d’un arbre ou d’un bâtiment, pente d’une rampe, angle d’une échelle. Elle est fréquemment combinée avec <a href="/pythagore-brevet.html">Pythagore</a> ou <a href="/thales-brevet.html">Thalès</a> dans le même exercice. Pour choisir : Pythagore relie trois longueurs, la trigonométrie relie un angle et deux longueurs. La calculatrice est autorisée dans la partie raisonnement de l’épreuve, et c’est là que la trigonométrie apparaît le plus souvent.</p>
</section>
''',
    faq=[
        ('Comment savoir s’il faut utiliser cosinus, sinus ou tangente ?', 'Repère les deux côtés qui interviennent : celui que tu connais et celui que tu cherches. Adjacent et hypoténuse : cosinus. Opposé et hypoténuse : sinus. Opposé et adjacent : tangente. SOH CAH TOA aide à s’en souvenir.'),
        ('Comment vérifier que ma calculatrice est en degrés ?', 'Calcule cos(60) : la calculatrice doit afficher 0,5. Si elle affiche un autre nombre (environ −0,95 en radians), change le mode d’angle dans les réglages.'),
        ('Quelle est la différence entre Pythagore et la trigonométrie ?', 'Les deux s’utilisent dans un triangle rectangle. Pythagore relie les trois longueurs, sans angle. La trigonométrie relie un angle aigu et deux longueurs. S’il y a un angle dans l’énoncé ou dans la question, c’est de la trigonométrie.'),
        ('Peut-on utiliser la trigonométrie dans un triangle quelconque ?', 'Pas avec les formules de 3e : cosinus, sinus et tangente sont définis ici dans un triangle rectangle. Si le triangle n’est pas rectangle, cherche une hauteur qui le découpe en triangles rectangles.'),
    ],
    related=['/pythagore-brevet.html', '/thales-brevet.html', '/racine-carree-3eme.html', '/equations-3eme.html', '/exercices-maths-3eme-brevet.html'],
))

# ─────────────────────────────── ARITHMÉTIQUE
PAGES.append(dict(
    path='/arithmetique-3eme.html', src='arithmetique', crumb='Arithmétique',
    title='Arithmétique 3e : nombres premiers, décomposition | Matheux',
    desc='Arithmétique en 3e : diviseurs, critères de divisibilité, nombres premiers, décomposition en facteurs premiers, problèmes de partage. Exercices corrigés.',
    eyebrow='Maths 3e · Nombres et calculs',
    h1='Arithmétique en 3e : nombres premiers et décomposition',
    h1_text='Arithmétique en 3e : nombres premiers et décomposition en facteurs premiers',
    lead='Multiples, diviseurs, nombres premiers : l’arithmétique paraît simple, mais au Brevet elle sert à résoudre de vrais problèmes de partage et à simplifier des fractions. La méthode tient en une idée : décomposer en facteurs premiers.',
    teaches=['Multiples et diviseurs', 'Critères de divisibilité', 'Division euclidienne', 'Reconnaître un nombre premier', 'Décomposer un entier en facteurs premiers', 'Résoudre un problème de partage avec les diviseurs communs'],
    toc=[('bases', 'Multiples et diviseurs'), ('premiers', 'Nombres premiers'), ('decomposer', 'Décomposer en facteurs premiers'), ('exemples', 'Exercices corrigés'), ('erreurs', 'Erreurs fréquentes'), ('faq', 'Questions fréquentes')],
    body=f'''
<section id="bases"><h2>Multiples, diviseurs et division euclidienne</h2>
<p>{M('36 = 4 × 9')} : on dit que 36 est un <strong>multiple</strong> de 4, et que 4 est un <strong>diviseur</strong> de 36. La phrase modèle évite de confondre les deux mots.</p>
<div class="key"><p class="t">Critères de divisibilité</p><ul>
<li>par 2 : le dernier chiffre est pair ; par 5 : il finit par 0 ou 5 ; par 10 : il finit par 0 ;</li>
<li>par 3 : la <strong>somme des chiffres</strong> est divisible par 3 ; par 9 : elle est divisible par 9 ;</li>
<li>par 4 : le nombre formé par les deux derniers chiffres est divisible par 4.</li>
</ul></div>
<p>La <strong>division euclidienne</strong> de {M('a')} par {M('b')} s’écrit {M('a = b × q + r')} avec {M('0 ≤ r < b')}. Exemple : {M('42 = 5 × 8 + 2')}. Le quotient est 8 et le reste est 2. Le reste n’est pas la partie décimale de {M('42 ÷ 5 = 8,4')}.</p>
</section>

<section id="premiers"><h2>Nombres premiers</h2>
<div class="key"><p class="t">Définition</p><p>Un nombre premier a <strong>exactement deux diviseurs</strong> distincts : 1 et lui-même. Les nombres premiers inférieurs à 50 sont : 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47.</p></div>
<ul>
<li>1 n’est pas premier : il n’a qu’un seul diviseur.</li>
<li>2 est premier, et c’est le seul nombre premier pair.</li>
<li>Un nombre impair n’est pas forcément premier : {M('21 = 3 × 7')}, {M('91 = 7 × 13')}.</li>
</ul>
<p>Pour tester si {M('n')} est premier, on essaie de le diviser par les nombres premiers 2, 3, 5, 7, 11… jusqu’à ce que leur carré dépasse {M('n')}. Si aucune division ne tombe juste, {M('n')} est premier.</p>
</section>

<section id="decomposer"><h2>Décomposer en produit de facteurs premiers</h2>
<p>Tout entier supérieur ou égal à 2 s’écrit comme un produit de nombres premiers, et cette écriture est unique (à l’ordre près). On divise successivement par 2, puis 3, puis 5… tant que c’est possible.</p>
<p>{M('360 = 2 × 180 = 2 × 2 × 90 = 2 × 2 × 2 × 45 = 2 × 2 × 2 × 3 × 3 × 5')}, donc <strong>{M('360 = 2³ × 3² × 5')}</strong>. On vérifie en recalculant : {M('8 × 9 × 5 = 360')} ✓.</p>
<p>La décomposition sert à trouver des diviseurs communs et à <strong>simplifier une fraction</strong> jusqu’à la forme irréductible (voir <a href="/fractions-brevet.html">fractions</a>).</p>
</section>

<section id="exemples"><h2>Exercices corrigés</h2>
<div class="ex"><h3>Exercice 1 : premier ou pas ?</h3>
<div class="q"><p>Les nombres 97 et 119 sont-ils premiers ?</p></div>
<div class="s"><span class="lbl">Correction</span>
<p>97 : il n’est divisible ni par 2, ni par 3 (somme des chiffres 16), ni par 5, ni par 7 ({M('7 × 13 = 91')}, {M('7 × 14 = 98')}). Comme {M('11² = 121 > 97')}, on peut s’arrêter : <strong>97 est premier</strong>.</p>
<p>119 : pas divisible par 2, 3 ou 5, mais {M('119 = 7 × 17')}. <strong>119 n’est pas premier.</strong></p>
</div></div>

<div class="ex"><h3>Exercice 2 : simplifier une fraction</h3>
<div class="q"><p>Rendre irréductible la fraction {F('84', '120')}.</p></div>
<div class="s"><span class="lbl">Correction</span>
<p>{M('84 = 2² × 3 × 7')} et {M('120 = 2³ × 3 × 5')}. Les facteurs communs sont {M('2² × 3 = 12')}.</p>
<p>{F('84', '120')}{M(' = ')}{F('12 × 7', '12 × 10')}{M(' = ')}<strong>{F('7', '10')}</strong>. 7 et 10 n’ont plus de diviseur commun autre que 1.</p>
</div></div>

<div class="ex"><h3>Exercice 3 : problème de partage (type Brevet)</h3>
<div class="q"><p>Un fleuriste a 60 tulipes et 96 roses. Il veut composer le plus grand nombre possible de bouquets identiques, en utilisant toutes les fleurs. Combien de bouquets peut-il faire, et que contient chaque bouquet ?</p></div>
<div class="s"><span class="lbl">Correction</span>
<p>Le nombre de bouquets doit diviser 60 <strong>et</strong> 96 : on cherche le plus grand diviseur commun.</p>
<p>{M('60 = 2² × 3 × 5')} et {M('96 = 2⁵ × 3')}. On garde les facteurs communs avec le plus petit exposant : {M('2² × 3 = 12')}.</p>
<p><strong>Il peut faire 12 bouquets</strong>, contenant chacun {M('60 ÷ 12 = 5')} tulipes et {M('96 ÷ 12 = 8')} roses.</p>
</div></div>
</section>

{{CTA_BOX}}

<section id="erreurs"><h2>Les erreurs les plus fréquentes</h2>
<ul class="errs">
<li><span class="e">« 23 est divisible par 3 car il finit par 3 »</span><span class="c">Par 3 et par 9, on regarde la somme des chiffres : {M('2 + 3 = 5')}, donc non.</span></li>
<li><span class="e">« 36 est un diviseur de 4 »</span><span class="c">{M('36 = 4 × 9')} : 36 est un multiple de 4, et 4 est un diviseur de 36.</span></li>
<li><span class="e">{M('42 ÷ 5 = 8,4')}, donc le reste est 4</span><span class="c">{M('42 = 5 × 8 + 2')} : le reste est 2, toujours plus petit que le diviseur.</span></li>
<li><span class="e">« 1 est premier »</span><span class="c">Un nombre premier a exactement deux diviseurs. 1 n’en a qu’un.</span></li>
<li><span class="e">Arrêter le test après 2, 3 et 5 (et déclarer 91 premier)</span><span class="c">Continuer avec 7, 11, 13… : {M('91 = 7 × 13')}.</span></li>
<li><span class="e">{M('126 = 2 × 9 × 7')}</span><span class="c">9 n’est pas premier : {M('126 = 2 × 3² × 7')}.</span></li>
<li><span class="e">Prendre les plus grands exposants pour un diviseur commun</span><span class="c">Un diviseur commun ne peut pas avoir plus de facteurs que chacun des nombres : on prend le plus petit exposant.</span></li>
<li><span class="e">Donner le nombre de fleurs par bouquet quand on demande le nombre de bouquets</span><span class="c">Relire la question et répondre par une phrase avec l’unité.</span></li>
</ul>
</section>
''',
    faq=[
        ('Le nombre 1 est-il un nombre premier ?', 'Non. Un nombre premier a exactement deux diviseurs distincts, 1 et lui-même. Le nombre 1 n’a qu’un seul diviseur, lui-même. Le plus petit nombre premier est 2.'),
        ('Comment savoir rapidement si un nombre est premier ?', 'Essaie de le diviser par 2, 3, 5, 7, 11, 13… Tu peux t’arrêter dès que le carré du diviseur testé dépasse le nombre. Par exemple, pour 97, on s’arrête après 7 car 11² = 121 est plus grand que 97.'),
        ('À quoi sert la décomposition en facteurs premiers ?', 'À trouver les diviseurs communs de deux nombres, donc à résoudre des problèmes de partage équitable, et à simplifier une fraction jusqu’à la forme irréductible.'),
        ('Qu’est-ce que le PGCD ?', 'C’est le plus grand diviseur commun à deux nombres. Pour 60 et 96, c’est 12. On l’obtient en multipliant les facteurs premiers communs aux deux décompositions, chacun avec son plus petit exposant.'),
    ],
    related=['/fractions-brevet.html', '/puissances-3eme.html', '/calcul-litteral-3eme.html', '/probabilites-brevet.html', '/exercices-maths-3eme-brevet.html'],
))
