#!/usr/bin/env python3
"""Generate 290 boost exercises for AlgèbreBoost."""
import json

data = {}

# ============================================================
# 6EME
# ============================================================
data["6EME"] = {}

data["6EME"]["Fractions"] = [
    {"lvl":1,"q":"Calculer $\\frac{1}{3} + \\frac{1}{6}$.","a":"1/2","options":["1/2","2/9","1/3","2/6"],"f":"\\frac{a}{b}+\\frac{c}{d}=\\frac{ad+bc}{bd}","steps":["Trouver le dénominateur commun : LCD = 6","$\\frac{2}{6}+\\frac{1}{6}=\\frac{3}{6}=\\frac{1}{2}$"]},
    {"lvl":1,"q":"Calculer $\\frac{2}{5} \\times 3$.","a":"6/5","options":["6/5","6/15","5/5","2/15"],"f":"\\frac{a}{b}\\times c=\\frac{a\\times c}{b}","steps":["Multiplier le numérateur par 3","$\\frac{2\\times 3}{5}=\\frac{6}{5}$"]},
    {"lvl":1,"q":"Quelle fraction de 20 représente 5 ?","a":"1/4","options":["1/4","1/5","4/5","5/4"],"f":"\\text{fraction}=\\frac{\\text{partie}}{\\text{total}}","steps":["Écrire la fraction : 5/20","Simplifier par 5 : $\\frac{1}{4}$"]},
    {"lvl":1,"q":"Simplifier $\\frac{8}{12}$.","a":"2/3","options":["2/3","4/6","3/4","8/12"],"f":"\\frac{a}{b}=\\frac{a\\div\\text{PGCD}}{b\\div\\text{PGCD}}","steps":["PGCD(8,12) = 4","$\\frac{8\\div4}{12\\div4}=\\frac{2}{3}$"]},
    {"lvl":1,"q":"Calculer $\\frac{3}{4} - \\frac{1}{4}$.","a":"1/2","options":["1/2","2/4","1/4","3/4"],"f":"\\frac{a}{n}-\\frac{b}{n}=\\frac{a-b}{n}","steps":["Même dénominateur, soustraire les numérateurs","$\\frac{3-1}{4}=\\frac{2}{4}=\\frac{1}{2}$"]},
    {"lvl":2,"q":"Calculer $\\frac{2}{3} + \\frac{3}{4}$.","a":"17/12","options":["17/12","5/7","5/12","6/7"],"f":"\\frac{a}{b}+\\frac{c}{d}=\\frac{ad+bc}{bd}","steps":["LCD = 12","$\\frac{8}{12}+\\frac{9}{12}=\\frac{17}{12}$"]},
    {"lvl":2,"q":"Calculer $\\frac{5}{6} - \\frac{1}{3}$.","a":"1/2","options":["1/2","4/3","4/6","2/3"],"f":"\\frac{a}{b}-\\frac{c}{d}=\\frac{ad-bc}{bd}","steps":["Mettre au dénominateur 6","$\\frac{5}{6}-\\frac{2}{6}=\\frac{3}{6}=\\frac{1}{2}$"]},
    {"lvl":2,"q":"Calculer $\\frac{3}{5}$ de 40.","a":"24","options":["24","20","12","30"],"f":"\\frac{a}{b}\\times n","steps":["Diviser 40 par 5 = 8","Multiplier 8 par 3 = 24"]},
    {"lvl":2,"q":"Calculer $\\frac{7}{8} - \\frac{3}{4}$.","a":"1/8","options":["1/8","4/4","1/2","4/8"],"f":"\\frac{a}{b}-\\frac{c}{d}=\\frac{ad-bc}{bd}","steps":["LCD = 8","$\\frac{7}{8}-\\frac{6}{8}=\\frac{1}{8}$"]},
    {"lvl":2,"q":"Calculer $\\frac{2}{3} + \\frac{5}{6} - \\frac{1}{2}$.","a":"1","options":["1","6/11","7/6","5/6"],"f":"\\text{LCD puis additionner/soustraire}","steps":["LCD = 6","$\\frac{4}{6}+\\frac{5}{6}-\\frac{3}{6}=\\frac{6}{6}=1$"]}
]

data["6EME"]["Nombres_entiers"] = [
    {"lvl":1,"q":"Calculer $347 + 285$.","a":"632","options":["632","622","532","642"],"f":"\\text{addition posée}","steps":["Additionner les unités : 7+5=12, retenue 1","3+2+8+1=14… Total = 632"]},
    {"lvl":1,"q":"Calculer $504 - 278$.","a":"226","options":["226","236","326","216"],"f":"\\text{soustraction posée}","steps":["504 - 278 : emprunter aux centaines","Résultat = 226"]},
    {"lvl":1,"q":"Calculer $15 \\times 12$.","a":"180","options":["180","170","190","162"],"f":"a\\times b","steps":["15 × 10 = 150","15 × 2 = 30, total = 180"]},
    {"lvl":1,"q":"Calculer $144 \\div 12$.","a":"12","options":["12","14","11","13"],"f":"a\\div b","steps":["12 × 12 = 144","Donc 144 ÷ 12 = 12"]},
    {"lvl":1,"q":"Quel est le plus petit multiple commun de 4 et 6 ?","a":"12","options":["12","24","6","18"],"f":"\\text{PPCM}(a,b)","steps":["Multiples de 4 : 4, 8, 12…","Multiples de 6 : 6, 12… → PPCM = 12"]},
    {"lvl":2,"q":"Calculer $23 \\times 17$.","a":"391","options":["391","381","401","371"],"f":"a\\times b=(a\\times10)+(a\\times7)","steps":["23 × 10 = 230","23 × 7 = 161 → 230 + 161 = 391"]},
    {"lvl":2,"q":"Décomposer 60 en produit de facteurs premiers.","a":"2² × 3 × 5","options":["2² × 3 × 5","2 × 3 × 10","4 × 15","2 × 30"],"f":"n=p_1^{a_1}\\times p_2^{a_2}\\times\\ldots","steps":["60 = 2 × 30 = 2 × 2 × 15","15 = 3 × 5 → 60 = 2² × 3 × 5"]},
    {"lvl":2,"q":"Calculer le PGCD de 36 et 48.","a":"12","options":["12","6","24","18"],"f":"\\text{PGCD}(a,b)","steps":["36 = 2² × 3², 48 = 2⁴ × 3","PGCD = 2² × 3 = 12"]},
    {"lvl":2,"q":"Calculer $1024 \\div 16$.","a":"64","options":["64","62","68","56"],"f":"a\\div b","steps":["16 × 60 = 960","16 × 4 = 64 → 960 + 64 = 1024"]},
    {"lvl":2,"q":"Combien y a-t-il de nombres premiers entre 1 et 20 ?","a":"8","options":["8","7","9","10"],"f":"\\text{crible d'Ératosthène}","steps":["Lister : 2, 3, 5, 7, 11, 13, 17, 19","Il y en a 8"]}
]

data["6EME"]["Proportionnalité"] = [
    {"lvl":1,"q":"3 kg coûtent 12 €. Combien coûtent 5 kg ?","a":"20 €","options":["20 €","15 €","25 €","17 €"],"f":"\\text{prix}=\\text{prix unitaire}\\times\\text{quantité}","steps":["Prix au kg : 12 ÷ 3 = 4 €","5 × 4 = 20 €"]},
    {"lvl":1,"q":"Une voiture roule à 90 km/h. Distance parcourue en 3 h ?","a":"270 km","options":["270 km","180 km","300 km","93 km"],"f":"d=v\\times t","steps":["Distance = vitesse × temps","90 × 3 = 270 km"]},
    {"lvl":1,"q":"4 cahiers coûtent 8 €. Prix d'un cahier ?","a":"2 €","options":["2 €","4 €","3 €","1 €"],"f":"\\text{prix unitaire}=\\frac{\\text{total}}{\\text{quantité}}","steps":["Diviser le prix total par le nombre","8 ÷ 4 = 2 €"]},
    {"lvl":1,"q":"Compléter : $\\frac{6}{9} = \\frac{?}{3}$.","a":"2","options":["2","3","6","18"],"f":"\\frac{a}{b}=\\frac{c}{d}\\Rightarrow c=\\frac{a\\times d}{b}","steps":["Simplifier 6/9 par 3","6 ÷ 3 = 2"]},
    {"lvl":1,"q":"200 g de farine pour 4 personnes. Pour 6 personnes ?","a":"300 g","options":["300 g","250 g","400 g","350 g"],"f":"\\frac{200}{4}=\\frac{x}{6}","steps":["Par personne : 200 ÷ 4 = 50 g","Pour 6 : 50 × 6 = 300 g"]},
    {"lvl":2,"q":"Sur une carte, 2 cm représentent 5 km. Distance réelle pour 7 cm ?","a":"17,5 km","options":["17,5 km","14 km","35 km","10 km"],"f":"\\frac{2}{5}=\\frac{7}{x}","steps":["1 cm = 2,5 km","7 × 2,5 = 17,5 km"]},
    {"lvl":2,"q":"Un robinet remplit 15 L en 3 min. Combien de temps pour 40 L ?","a":"8 min","options":["8 min","10 min","12 min","6 min"],"f":"t=\\frac{\\text{volume}}{\\text{débit}}","steps":["Débit = 15 ÷ 3 = 5 L/min","40 ÷ 5 = 8 min"]},
    {"lvl":2,"q":"5 ouvriers mettent 12 jours. Combien pour 10 ouvriers ?","a":"6 jours","options":["6 jours","24 jours","10 jours","8 jours"],"f":"n_1\\times t_1=n_2\\times t_2","steps":["Proportionnalité inverse : 5 × 12 = 60","60 ÷ 10 = 6 jours"]},
    {"lvl":2,"q":"2,5 kg de pommes coûtent 4,50 €. Prix au kg ?","a":"1,80 €","options":["1,80 €","2 €","1,50 €","2,25 €"],"f":"\\text{prix/kg}=\\frac{\\text{prix total}}{\\text{masse}}","steps":["Diviser 4,50 par 2,5","4,50 ÷ 2,5 = 1,80 €"]},
    {"lvl":2,"q":"Plan à l'échelle 1/500. Un mur mesure 3 cm sur le plan. Longueur réelle ?","a":"15 m","options":["15 m","150 m","1,5 m","1500 m"],"f":"d_{\\text{réelle}}=d_{\\text{plan}}\\times\\text{échelle}","steps":["3 cm × 500 = 1500 cm","1500 cm = 15 m"]}
]

data["6EME"]["Géométrie"] = [
    {"lvl":1,"q":"Combien de côtés possède un hexagone ?","a":"6","options":["6","5","8","7"],"f":"\\text{hexa} = 6","steps":["Le préfixe hexa- signifie 6","Un hexagone a 6 côtés"]},
    {"lvl":1,"q":"Comment appelle-t-on un triangle dont les 3 côtés sont égaux ?","a":"Équilatéral","options":["Équilatéral","Isocèle","Rectangle","Scalène"],"f":"\\text{3 côtés égaux}\\Rightarrow\\text{équilatéral}","steps":["Isocèle = 2 côtés égaux","3 côtés égaux = équilatéral"]},
    {"lvl":1,"q":"Deux droites qui ne se croisent jamais sont dites…","a":"Parallèles","options":["Parallèles","Perpendiculaires","Sécantes","Confondues"],"f":"(d_1)\\parallel(d_2)","steps":["Sécantes = se croisent","Ne se croisent jamais = parallèles"]},
    {"lvl":1,"q":"Combien d'axes de symétrie possède un carré ?","a":"4","options":["4","2","1","8"],"f":"\\text{carré : 4 axes}","steps":["2 diagonales + 2 médiatrices des côtés","Total = 4 axes"]},
    {"lvl":1,"q":"Un cercle a un rayon de 3 cm. Quel est son diamètre ?","a":"6 cm","options":["6 cm","3 cm","9 cm","12 cm"],"f":"d=2r","steps":["Le diamètre est le double du rayon","2 × 3 = 6 cm"]},
    {"lvl":2,"q":"ABCD est un parallélogramme. Si $AB = 7$ cm et $BC = 4$ cm, combien vaut $CD$ ?","a":"7 cm","options":["7 cm","4 cm","11 cm","3 cm"],"f":"AB=CD,\\;BC=AD","steps":["Dans un parallélogramme, les côtés opposés sont égaux","CD = AB = 7 cm"]},
    {"lvl":2,"q":"Un triangle a des côtés de 3 cm, 4 cm et 5 cm. Est-il rectangle ?","a":"Oui","options":["Oui","Non","Isocèle","Équilatéral"],"f":"a^2+b^2=c^2","steps":["Vérifier : 3² + 4² = 9 + 16 = 25 = 5²","L'égalité est vérifiée → rectangle"]},
    {"lvl":2,"q":"Le symétrique du point $A(2\\,;\\,3)$ par rapport à l'axe des abscisses est…","a":"(2 ; -3)","options":["(2 ; -3)","(-2 ; 3)","(-2 ; -3)","(2 ; 3)"],"f":"S_{Ox}(x;y)=(x;-y)","steps":["L'axe Ox inverse le signe de y","(2 ; 3) → (2 ; -3)"]},
    {"lvl":2,"q":"Dans un losange, les diagonales se coupent en formant des angles…","a":"Droits (90°)","options":["Droits (90°)","Aigus","Obtus","De 60°"],"f":"\\text{losange : diagonales perpendiculaires}","steps":["Propriété du losange","Ses diagonales sont perpendiculaires → 90°"]},
    {"lvl":2,"q":"ABCD rectangle, $AB = 6$ cm, $AD = 8$ cm. Longueur de la diagonale AC ?","a":"10 cm","options":["10 cm","14 cm","7 cm","48 cm"],"f":"AC=\\sqrt{AB^2+AD^2}","steps":["6² + 8² = 36 + 64 = 100","√100 = 10 cm"]}
]

data["6EME"]["Périmètres_Aires"] = [
    {"lvl":1,"q":"Périmètre d'un carré de côté 9 cm ?","a":"36 cm","options":["36 cm","18 cm","81 cm","27 cm"],"f":"P=4\\times c","steps":["Périmètre = 4 × côté","4 × 9 = 36 cm"]},
    {"lvl":1,"q":"Aire d'un rectangle de 6 cm par 4 cm ?","a":"24 cm²","options":["24 cm²","20 cm²","10 cm²","48 cm²"],"f":"A=L\\times l","steps":["Aire = longueur × largeur","6 × 4 = 24 cm²"]},
    {"lvl":1,"q":"Périmètre d'un rectangle de 5 cm par 3 cm ?","a":"16 cm","options":["16 cm","15 cm","8 cm","30 cm"],"f":"P=2(L+l)","steps":["P = 2 × (5 + 3)","P = 2 × 8 = 16 cm"]},
    {"lvl":1,"q":"Aire d'un carré de côté 7 cm ?","a":"49 cm²","options":["49 cm²","28 cm²","14 cm²","56 cm²"],"f":"A=c^2","steps":["Aire = côté × côté","7 × 7 = 49 cm²"]},
    {"lvl":1,"q":"Périmètre d'un cercle de rayon 5 cm (arrondi au dixième) ?","a":"31,4 cm","options":["31,4 cm","15,7 cm","78,5 cm","25 cm"],"f":"P=2\\pi r","steps":["P = 2 × π × 5","P ≈ 31,4 cm"]},
    {"lvl":2,"q":"Aire d'un triangle de base 10 cm et hauteur 6 cm ?","a":"30 cm²","options":["30 cm²","60 cm²","16 cm²","36 cm²"],"f":"A=\\frac{b\\times h}{2}","steps":["A = (base × hauteur) / 2","A = (10 × 6) / 2 = 30 cm²"]},
    {"lvl":2,"q":"Aire d'un disque de rayon 4 cm (arrondi au dixième) ?","a":"50,3 cm²","options":["50,3 cm²","25,1 cm²","12,6 cm²","100,5 cm²"],"f":"A=\\pi r^2","steps":["A = π × 4²","A ≈ 3,14 × 16 ≈ 50,3 cm²"]},
    {"lvl":2,"q":"Périmètre d'un demi-cercle de diamètre 10 cm (arrondi au dixième) ?","a":"25,7 cm","options":["25,7 cm","15,7 cm","31,4 cm","20 cm"],"f":"P=\\pi r + d","steps":["Demi-périmètre = π × 5 ≈ 15,7","+ diamètre 10 → 25,7 cm"]},
    {"lvl":2,"q":"Aire d'un terrain rectangulaire de 25 m par 40 m ?","a":"1000 m²","options":["1000 m²","130 m²","650 m²","500 m²"],"f":"A=L\\times l","steps":["A = 25 × 40","A = 1000 m²"]},
    {"lvl":2,"q":"Aire d'un parallélogramme de base 8 cm et hauteur 5 cm ?","a":"40 cm²","options":["40 cm²","13 cm²","26 cm²","80 cm²"],"f":"A=b\\times h","steps":["A = base × hauteur","A = 8 × 5 = 40 cm²"]}
]

data["6EME"]["Angles"] = [
    {"lvl":1,"q":"Combien mesure un angle droit ?","a":"90°","options":["90°","180°","45°","60°"],"f":"\\text{angle droit}=90°","steps":["Un angle droit forme un « L »","Il mesure exactement 90°"]},
    {"lvl":1,"q":"Un angle de 45° est un angle…","a":"Aigu","options":["Aigu","Obtus","Droit","Plat"],"f":"0°<\\alpha<90°\\Rightarrow\\text{aigu}","steps":["Aigu : entre 0° et 90°","45° < 90° → aigu"]},
    {"lvl":1,"q":"Deux angles complémentaires ont une somme de…","a":"90°","options":["90°","180°","360°","270°"],"f":"\\alpha+\\beta=90°","steps":["Complémentaires = somme 90°","Supplémentaires = somme 180°"]},
    {"lvl":1,"q":"Quel est le complément d'un angle de 35° ?","a":"55°","options":["55°","145°","35°","65°"],"f":"\\text{complément}=90°-\\alpha","steps":["90° - 35°","= 55°"]},
    {"lvl":1,"q":"Combien mesure un angle plat ?","a":"180°","options":["180°","90°","360°","270°"],"f":"\\text{angle plat}=180°","steps":["Un angle plat forme une ligne droite","Il mesure 180°"]},
    {"lvl":2,"q":"Quel est le supplément d'un angle de 115° ?","a":"65°","options":["65°","245°","75°","55°"],"f":"\\text{supplément}=180°-\\alpha","steps":["Supplémentaires : somme = 180°","180° - 115° = 65°"]},
    {"lvl":2,"q":"Quelle est la somme des angles d'un triangle ?","a":"180°","options":["180°","360°","270°","90°"],"f":"\\alpha+\\beta+\\gamma=180°","steps":["Propriété fondamentale du triangle","La somme vaut toujours 180°"]},
    {"lvl":2,"q":"Un triangle a deux angles de 50° et 70°. Le troisième angle mesure…","a":"60°","options":["60°","120°","40°","80°"],"f":"\\gamma=180°-\\alpha-\\beta","steps":["Somme = 180°","180° - 50° - 70° = 60°"]},
    {"lvl":2,"q":"Deux droites se coupent. Un angle mesure 130°. L'angle opposé par le sommet mesure…","a":"130°","options":["130°","50°","230°","180°"],"f":"\\text{angles opposés par le sommet sont égaux}","steps":["Propriété : angles opposés par le sommet","Ils sont égaux → 130°"]},
    {"lvl":2,"q":"Quelle est la somme des angles d'un quadrilatère ?","a":"360°","options":["360°","180°","540°","270°"],"f":"\\text{somme angles quadrilatère}=360°","steps":["Un quadrilatère = 2 triangles","2 × 180° = 360°"]}
]

data["6EME"]["Nombres_decimaux"] = [
    {"lvl":1,"q":"Calculer $3{,}5 + 2{,}8$.","a":"6,3","options":["6,3","5,3","6,13","5,13"],"f":"\\text{addition décimale}","steps":["Aligner les virgules","3,5 + 2,8 = 6,3"]},
    {"lvl":1,"q":"Calculer $7{,}2 - 4{,}5$.","a":"2,7","options":["2,7","3,3","2,3","3,7"],"f":"\\text{soustraction décimale}","steps":["Aligner les virgules","7,2 - 4,5 = 2,7"]},
    {"lvl":1,"q":"Calculer $0{,}6 \\times 5$.","a":"3","options":["3","0,3","30","3,5"],"f":"a\\times b","steps":["0,6 × 5","= 3"]},
    {"lvl":1,"q":"Arrondir 4,67 à l'unité.","a":"5","options":["5","4","4,7","4,6"],"f":"\\text{chiffre des dixièmes}\\geq 5\\Rightarrow\\text{arrondir au-dessus}","steps":["Regarder le chiffre des dixièmes : 6 ≥ 5","Arrondir au-dessus : 5"]},
    {"lvl":1,"q":"Quel nombre est le plus grand : $0{,}8$ ou $0{,}75$ ?","a":"0,8","options":["0,8","0,75","Ils sont égaux","On ne peut pas comparer"],"f":"0{,}80 > 0{,}75","steps":["Écrire avec le même nombre de décimales","0,80 > 0,75"]},
    {"lvl":2,"q":"Calculer $3{,}14 \\times 2{,}5$.","a":"7,85","options":["7,85","7,58","78,5","0,785"],"f":"\\text{multiplication décimale}","steps":["314 × 25 = 7850","Replacer la virgule : 7,85"]},
    {"lvl":2,"q":"Calculer $12{,}6 \\div 0{,}3$.","a":"42","options":["42","4,2","420","3,78"],"f":"\\frac{a}{b}=\\frac{a\\times10}{b\\times10}","steps":["Multiplier par 10 : 126 ÷ 3","= 42"]},
    {"lvl":2,"q":"Intercaler un nombre décimal entre $3{,}1$ et $3{,}2$.","a":"3,15","options":["3,15","3,3","3,21","3,09"],"f":"\\frac{a+b}{2}","steps":["Prendre la moyenne ou ajouter une décimale","3,15 est entre 3,1 et 3,2"]},
    {"lvl":2,"q":"Calculer $2{,}4 \\times 0{,}5 + 1{,}3$.","a":"2,5","options":["2,5","3,7","1,85","3,2"],"f":"\\text{priorité : × avant +}","steps":["D'abord 2,4 × 0,5 = 1,2","Puis 1,2 + 1,3 = 2,5"]},
    {"lvl":2,"q":"Écrire $\\frac{3}{8}$ sous forme décimale.","a":"0,375","options":["0,375","0,38","0,35","0,83"],"f":"\\frac{a}{b}=a\\div b","steps":["Poser la division 3 ÷ 8","3 ÷ 8 = 0,375"]}
]

data["6EME"]["Statistiques_6eme"] = [
    {"lvl":1,"q":"Calculer la moyenne de 12, 8, 10 et 14.","a":"11","options":["11","10","12","44"],"f":"\\bar{x}=\\frac{\\sum x_i}{n}","steps":["Somme = 12+8+10+14 = 44","44 ÷ 4 = 11"]},
    {"lvl":1,"q":"La catégorie A a 15 éléments sur 60. Quel pourcentage ?","a":"25 %","options":["25 %","15 %","40 %","4 %"],"f":"\\%=\\frac{\\text{effectif}}{\\text{total}}\\times100","steps":["15 ÷ 60 = 0,25","0,25 × 100 = 25 %"]},
    {"lvl":1,"q":"Les effectifs sont 5, 8, 12, 5. Effectif total ?","a":"30","options":["30","25","20","35"],"f":"N=\\sum n_i","steps":["Additionner tous les effectifs","5+8+12+5 = 30"]},
    {"lvl":1,"q":"Quel est le mode de la série : 3, 5, 5, 7, 5, 9 ?","a":"5","options":["5","3","7","9"],"f":"\\text{mode = valeur la plus fréquente}","steps":["Compter les occurrences","5 apparaît 3 fois → mode = 5"]},
    {"lvl":1,"q":"Calculer la moyenne de 15 et 9.","a":"12","options":["12","24","6","13"],"f":"\\bar{x}=\\frac{a+b}{2}","steps":["15 + 9 = 24","24 ÷ 2 = 12"]},
    {"lvl":2,"q":"Moyenne pondérée : 12 (coeff 2), 15 (coeff 3), 9 (coeff 1).","a":"13","options":["13","12","14","15"],"f":"\\bar{x}=\\frac{\\sum n_i x_i}{\\sum n_i}","steps":["24 + 45 + 9 = 78","78 ÷ 6 = 13"]},
    {"lvl":2,"q":"Médiane de la série : 3, 7, 2, 9, 5.","a":"5","options":["5","7","3","9"],"f":"\\text{ordonner puis prendre la valeur centrale}","steps":["Ordonner : 2, 3, 5, 7, 9","Valeur centrale (3e sur 5) = 5"]},
    {"lvl":2,"q":"Étendue de la série : 4, 12, 7, 3, 15.","a":"12","options":["12","15","11","3"],"f":"E=x_{\\max}-x_{\\min}","steps":["Max = 15, Min = 3","15 - 3 = 12"]},
    {"lvl":2,"q":"Un élève a 14, 11, 16. Quelle note au 4e contrôle pour avoir 14 de moyenne ?","a":"15","options":["15","14","13","16"],"f":"x=4\\bar{x}-\\sum x_i","steps":["Somme visée : 4 × 14 = 56","56 - (14+11+16) = 56 - 41 = 15"]},
    {"lvl":2,"q":"40 % de 250 élèves font du sport. Combien ?","a":"100","options":["100","90","110","40"],"f":"n=\\frac{\\%}{100}\\times N","steps":["40% de 250","0,4 × 250 = 100"]}
]

# ============================================================
# 5EME
# ============================================================
data["5EME"] = {}

data["5EME"]["Fractions"] = [
    {"lvl":1,"q":"Calculer $\\frac{2}{3} + \\frac{1}{4}$.","a":"11/12","options":["11/12","3/7","5/12","1/2"],"f":"\\frac{a}{b}+\\frac{c}{d}=\\frac{ad+bc}{bd}","steps":["LCD = 12","$\\frac{8}{12}+\\frac{3}{12}=\\frac{11}{12}$"]},
    {"lvl":1,"q":"Calculer $\\frac{3}{5} \\times \\frac{2}{7}$.","a":"6/35","options":["6/35","5/12","6/12","5/35"],"f":"\\frac{a}{b}\\times\\frac{c}{d}=\\frac{ac}{bd}","steps":["Multiplier numérateurs et dénominateurs","$\\frac{3×2}{5×7}=\\frac{6}{35}$"]},
    {"lvl":1,"q":"Simplifier $\\frac{12}{18}$.","a":"2/3","options":["2/3","6/9","3/4","4/6"],"f":"\\frac{a}{b}=\\frac{a\\div\\text{PGCD}}{b\\div\\text{PGCD}}","steps":["PGCD(12,18) = 6","$\\frac{12÷6}{18÷6}=\\frac{2}{3}$"]},
    {"lvl":1,"q":"Calculer $\\frac{5}{6} - \\frac{1}{3}$.","a":"1/2","options":["1/2","4/3","2/3","1/6"],"f":"\\frac{a}{b}-\\frac{c}{d}=\\frac{ad-bc}{bd}","steps":["LCD = 6","$\\frac{5}{6}-\\frac{2}{6}=\\frac{3}{6}=\\frac{1}{2}$"]},
    {"lvl":1,"q":"Calculer $\\frac{4}{9} \\times 3$.","a":"4/3","options":["4/3","12/9","4/27","7/9"],"f":"\\frac{a}{b}\\times c=\\frac{ac}{b}","steps":["$\\frac{4×3}{9}=\\frac{12}{9}$","Simplifier par 3 : $\\frac{4}{3}$"]},
    {"lvl":2,"q":"Calculer $\\frac{3}{4} \\div \\frac{2}{5}$.","a":"15/8","options":["15/8","6/20","5/8","8/15"],"f":"\\frac{a}{b}\\div\\frac{c}{d}=\\frac{a}{b}\\times\\frac{d}{c}","steps":["Inverser et multiplier","$\\frac{3}{4}×\\frac{5}{2}=\\frac{15}{8}$"]},
    {"lvl":2,"q":"Calculer $\\frac{2}{3} + \\frac{5}{4} - \\frac{1}{6}$.","a":"7/4","options":["7/4","6/3","21/12","3/4"],"f":"\\text{LCD puis additionner}","steps":["LCD = 12 : $\\frac{8}{12}+\\frac{15}{12}-\\frac{2}{12}$","$=\\frac{21}{12}=\\frac{7}{4}$"]},
    {"lvl":2,"q":"Calculer $\\frac{7}{10} \\times \\frac{5}{3}$.","a":"7/6","options":["7/6","12/13","35/30","5/7"],"f":"\\frac{a}{b}\\times\\frac{c}{d}=\\frac{ac}{bd}","steps":["$\\frac{7×5}{10×3}=\\frac{35}{30}$","Simplifier par 5 : $\\frac{7}{6}$"]},
    {"lvl":2,"q":"Quel est l'inverse de $\\frac{3}{8}$ ?","a":"8/3","options":["8/3","3/8","-3/8","1/3"],"f":"\\text{inverse de }\\frac{a}{b}=\\frac{b}{a}","steps":["Échanger numérateur et dénominateur","Inverse de 3/8 = 8/3"]},
    {"lvl":2,"q":"Calculer $\\left(\\frac{2}{5}\\right)^2$.","a":"4/25","options":["4/25","4/10","2/10","4/5"],"f":"\\left(\\frac{a}{b}\\right)^2=\\frac{a^2}{b^2}","steps":["Mettre au carré numérateur et dénominateur","$\\frac{2^2}{5^2}=\\frac{4}{25}$"]}
]

data["5EME"]["Nombres_relatifs"] = [
    {"lvl":1,"q":"Calculer $(-3) + 7$.","a":"4","options":["4","-4","10","-10"],"f":"a+b\\text{ (signes différents : soustraire)}","steps":["Signes différents : 7 - 3 = 4","Le plus grand en valeur absolue est positif → +4"]},
    {"lvl":1,"q":"Calculer $(-5) - 3$.","a":"-8","options":["-8","-2","8","2"],"f":"a-b=a+(-b)","steps":["(-5) + (-3)","= -8"]},
    {"lvl":1,"q":"Calculer $(-4) \\times 3$.","a":"-12","options":["-12","12","-7","-1"],"f":"(-)\\times(+)=(-)","steps":["Négatif × positif = négatif","4 × 3 = 12 → -12"]},
    {"lvl":1,"q":"Calculer $6 + (-9)$.","a":"-3","options":["-3","3","15","-15"],"f":"a+(-b)=a-b","steps":["6 - 9","= -3"]},
    {"lvl":1,"q":"Calculer $(-2) \\times (-5)$.","a":"10","options":["10","-10","7","-7"],"f":"(-)\\times(-)=(+)","steps":["Négatif × négatif = positif","2 × 5 = 10 → +10"]},
    {"lvl":2,"q":"Calculer $(-3) \\times 4 + (-2) \\times (-5)$.","a":"-2","options":["-2","-22","2","22"],"f":"\\text{priorité : × avant +}","steps":["(-3)×4 = -12 et (-2)×(-5) = 10","-12 + 10 = -2"]},
    {"lvl":2,"q":"Calculer $(-8) \\div (-2)$.","a":"4","options":["4","-4","16","-16"],"f":"(-)\\div(-)=(+)","steps":["Négatif ÷ négatif = positif","8 ÷ 2 = 4 → +4"]},
    {"lvl":2,"q":"Calculer $5 - (-3) + (-7)$.","a":"1","options":["1","-5","15","-9"],"f":"a-(-b)=a+b","steps":["5 + 3 + (-7) = 8 - 7","= 1"]},
    {"lvl":2,"q":"Calculer $(-6)^2$.","a":"36","options":["36","-36","12","-12"],"f":"(-a)^2=a^2","steps":["(-6)² = (-6) × (-6)","= 36 (négatif × négatif = positif)"]},
    {"lvl":2,"q":"Calculer $(-2)^3$.","a":"-8","options":["-8","8","-6","6"],"f":"(-a)^3=-a^3","steps":["(-2)³ = (-2)×(-2)×(-2)","= 4 × (-2) = -8"]}
]

data["5EME"]["Proportionnalité"] = [
    {"lvl":1,"q":"4 stylos coûtent 6 €. Prix de 10 stylos ?","a":"15 €","options":["15 €","16 €","12 €","20 €"],"f":"\\text{prix}=\\text{prix unitaire}\\times n","steps":["Prix unitaire : 6 ÷ 4 = 1,50 €","10 × 1,50 = 15 €"]},
    {"lvl":1,"q":"250 g de pâtes pour 2 personnes. Pour 5 personnes ?","a":"625 g","options":["625 g","500 g","750 g","1000 g"],"f":"\\frac{250}{2}=\\frac{x}{5}","steps":["Par personne : 250 ÷ 2 = 125 g","5 × 125 = 625 g"]},
    {"lvl":1,"q":"Vitesse = 60 km/h. Distance en 2 h 30 min ?","a":"150 km","options":["150 km","120 km","180 km","62,5 km"],"f":"d=v\\times t","steps":["2 h 30 = 2,5 h","60 × 2,5 = 150 km"]},
    {"lvl":1,"q":"Calculer 20 % de 350.","a":"70","options":["70","35","7","17,5"],"f":"\\frac{20}{100}\\times 350","steps":["20% = 0,20","0,20 × 350 = 70"]},
    {"lvl":1,"q":"Un article passe de 40 € à 50 €. Augmentation en euros ?","a":"10 €","options":["10 €","20 €","25 €","8 €"],"f":"\\text{augmentation}=\\text{nouveau}-\\text{ancien}","steps":["50 - 40","= 10 €"]},
    {"lvl":2,"q":"Pourcentage d'augmentation de 80 € à 100 € ?","a":"25 %","options":["25 %","20 %","80 %","125 %"],"f":"\\%=\\frac{\\text{variation}}{\\text{initial}}\\times100","steps":["Variation : 100 - 80 = 20","20/80 × 100 = 25 %"]},
    {"lvl":2,"q":"Échelle 1/2000. Distance réelle pour 8 cm sur le plan ?","a":"160 m","options":["160 m","16 m","1600 m","250 m"],"f":"d_{\\text{réelle}}=d_{\\text{plan}}\\times\\text{dénominateur}","steps":["8 cm × 2000 = 16 000 cm","16 000 cm = 160 m"]},
    {"lvl":2,"q":"Prix initial 120 €, réduction 15 %. Prix final ?","a":"102 €","options":["102 €","105 €","18 €","108 €"],"f":"\\text{prix final}=\\text{prix}\\times(1-\\frac{r}{100})","steps":["Réduction : 120 × 0,15 = 18 €","120 - 18 = 102 €"]},
    {"lvl":2,"q":"Un cycliste parcourt 45 km en 1 h 30 min. Vitesse en km/h ?","a":"30 km/h","options":["30 km/h","45 km/h","67,5 km/h","15 km/h"],"f":"v=\\frac{d}{t}","steps":["1 h 30 = 1,5 h","45 ÷ 1,5 = 30 km/h"]},
    {"lvl":2,"q":"Coefficient de proportionnalité si $3 \\to 12$ et $5 \\to 20$ ?","a":"4","options":["4","9","15","3"],"f":"k=\\frac{y}{x}","steps":["12 ÷ 3 = 4","20 ÷ 5 = 4 → k = 4"]}
]

data["5EME"]["Puissances"] = [
    {"lvl":1,"q":"Calculer $2^4$.","a":"16","options":["16","8","32","24"],"f":"a^n=a\\times a\\times\\ldots\\times a","steps":["2⁴ = 2×2×2×2","= 16"]},
    {"lvl":1,"q":"Calculer $10^3$.","a":"1000","options":["1000","100","30","10000"],"f":"10^n=1\\underbrace{00\\ldots0}_{n}","steps":["10³ = 10×10×10","= 1000"]},
    {"lvl":1,"q":"Calculer $3^3$.","a":"27","options":["27","9","81","12"],"f":"a^3=a\\times a\\times a","steps":["3³ = 3×3×3","= 27"]},
    {"lvl":1,"q":"Calculer $5^2$.","a":"25","options":["25","10","125","50"],"f":"a^2=a\\times a","steps":["5² = 5×5","= 25"]},
    {"lvl":1,"q":"Écrire 100 000 comme puissance de 10.","a":"10⁵","options":["10⁵","10⁶","10⁴","5¹⁰"],"f":"10^n","steps":["Compter les zéros : 5","100 000 = 10⁵"]},
    {"lvl":2,"q":"Calculer $2^3 \\times 2^4$.","a":"128","options":["128","64","256","48"],"f":"a^m\\times a^n=a^{m+n}","steps":["2³ × 2⁴ = 2⁷","2⁷ = 128"]},
    {"lvl":2,"q":"Calculer $(3^2)^3$.","a":"729","options":["729","243","81","2187"],"f":"(a^m)^n=a^{mn}","steps":["(3²)³ = 3⁶","3⁶ = 729"]},
    {"lvl":2,"q":"Calculer $4{,}5 \\times 10^3$.","a":"4500","options":["4500","450","45000","45"],"f":"a\\times 10^n","steps":["Décaler la virgule de 3 rangs","4,5 × 1000 = 4500"]},
    {"lvl":2,"q":"Calculer $10^6 \\div 10^2$.","a":"10 000","options":["10 000","1000","100 000","100"],"f":"\\frac{a^m}{a^n}=a^{m-n}","steps":["10⁶ ÷ 10² = 10⁴","10⁴ = 10 000"]},
    {"lvl":2,"q":"Calculer $6 \\times 10^{-2}$.","a":"0,06","options":["0,06","0,6","600","0,006"],"f":"10^{-n}=\\frac{1}{10^n}","steps":["10⁻² = 0,01","6 × 0,01 = 0,06"]}
]

data["5EME"]["Pythagore"] = [
    {"lvl":1,"q":"Triangle rectangle : côtés 3 cm et 4 cm. Hypoténuse ?","a":"5 cm","options":["5 cm","7 cm","12 cm","6 cm"],"f":"c=\\sqrt{a^2+b^2}","steps":["3² + 4² = 9 + 16 = 25","√25 = 5 cm"]},
    {"lvl":1,"q":"Triangle rectangle : côtés 6 cm et 8 cm. Hypoténuse ?","a":"10 cm","options":["10 cm","14 cm","48 cm","7 cm"],"f":"c=\\sqrt{a^2+b^2}","steps":["6² + 8² = 36 + 64 = 100","√100 = 10 cm"]},
    {"lvl":1,"q":"Hypoténuse = 13 cm, un côté = 5 cm. L'autre côté ?","a":"12 cm","options":["12 cm","8 cm","18 cm","7 cm"],"f":"b=\\sqrt{c^2-a^2}","steps":["13² - 5² = 169 - 25 = 144","√144 = 12 cm"]},
    {"lvl":1,"q":"$5^2 + 12^2 = ?$. Quelle est l'hypoténuse ?","a":"13 cm","options":["13 cm","17 cm","60 cm","7 cm"],"f":"c=\\sqrt{a^2+b^2}","steps":["25 + 144 = 169","√169 = 13 cm"]},
    {"lvl":1,"q":"Hypoténuse = 10 cm, un côté = 6 cm. L'autre côté ?","a":"8 cm","options":["8 cm","4 cm","16 cm","6 cm"],"f":"b=\\sqrt{c^2-a^2}","steps":["10² - 6² = 100 - 36 = 64","√64 = 8 cm"]},
    {"lvl":2,"q":"Triangle rectangle : côtés 9 cm et 12 cm. Hypoténuse ?","a":"15 cm","options":["15 cm","21 cm","108 cm","10 cm"],"f":"c=\\sqrt{a^2+b^2}","steps":["9² + 12² = 81 + 144 = 225","√225 = 15 cm"]},
    {"lvl":2,"q":"Le triangle de côtés 7, 24 et 25 est-il rectangle ?","a":"Oui","options":["Oui","Non","Isocèle","Impossible à dire"],"f":"a^2+b^2=c^2 ?","steps":["7² + 24² = 49 + 576 = 625","25² = 625 → égalité vérifiée → rectangle"]},
    {"lvl":2,"q":"Un mât de 8 m est fixé par un câble ancré à 6 m du pied. Longueur du câble ?","a":"10 m","options":["10 m","14 m","48 m","7 m"],"f":"c=\\sqrt{a^2+b^2}","steps":["8² + 6² = 64 + 36 = 100","√100 = 10 m"]},
    {"lvl":2,"q":"Hypoténuse = 17 cm, un côté = 8 cm. L'autre côté ?","a":"15 cm","options":["15 cm","9 cm","25 cm","12 cm"],"f":"b=\\sqrt{c^2-a^2}","steps":["17² - 8² = 289 - 64 = 225","√225 = 15 cm"]},
    {"lvl":2,"q":"Le triangle de côtés 5, 6 et 8 est-il rectangle ?","a":"Non","options":["Non","Oui","Isocèle","Équilatéral"],"f":"a^2+b^2=c^2 ?","steps":["5² + 6² = 25 + 36 = 61","8² = 64 ≠ 61 → pas rectangle"]}
]

data["5EME"]["Calcul_Littéral"] = [
    {"lvl":1,"q":"Simplifier $3x + 5x$.","a":"8x","options":["8x","15x","8x²","35x"],"f":"ax+bx=(a+b)x","steps":["Même variable, additionner les coefficients","3 + 5 = 8 → 8x"]},
    {"lvl":1,"q":"Développer $2(x + 4)$.","a":"2x + 8","options":["2x + 8","2x + 4","x + 8","2x² + 8"],"f":"a(b+c)=ab+ac","steps":["Multiplier chaque terme par 2","2×x + 2×4 = 2x + 8"]},
    {"lvl":1,"q":"Calculer $3x$ pour $x = 5$.","a":"15","options":["15","8","35","53"],"f":"\\text{substituer } x","steps":["Remplacer x par 5","3 × 5 = 15"]},
    {"lvl":1,"q":"Réduire $7a - 3a + 2a$.","a":"6a","options":["6a","12a","2a","6a²"],"f":"\\text{regrouper les termes semblables}","steps":["7 - 3 + 2 = 6","= 6a"]},
    {"lvl":1,"q":"Développer $5(2y - 1)$.","a":"10y - 5","options":["10y - 5","10y - 1","7y - 5","10y + 5"],"f":"a(b-c)=ab-ac","steps":["5 × 2y = 10y","5 × (-1) = -5 → 10y - 5"]},
    {"lvl":2,"q":"Développer et réduire $3(2x + 1) + 2(x - 4)$.","a":"8x - 5","options":["8x - 5","8x + 5","8x - 3","5x - 5"],"f":"\\text{développer puis regrouper}","steps":["6x + 3 + 2x - 8","= 8x - 5"]},
    {"lvl":2,"q":"Factoriser $6x + 9$.","a":"3(2x + 3)","options":["3(2x + 3)","6(x + 9)","3(2x + 9)","2(3x + 3)"],"f":"ab+ac=a(b+c)","steps":["PGCD(6,9) = 3","3(2x + 3)"]},
    {"lvl":2,"q":"Calculer $3x^2 - 4x + 1$ pour $x = -2$.","a":"21","options":["21","5","-3","17"],"f":"\\text{substituer } x=-2","steps":["3×4 - 4×(-2) + 1","12 + 8 + 1 = 21"]},
    {"lvl":2,"q":"Réduire $4x + 3 - 2x + 7$.","a":"2x + 10","options":["2x + 10","6x + 10","2x - 4","2x + 4"],"f":"\\text{regrouper les termes semblables}","steps":["4x - 2x = 2x","3 + 7 = 10 → 2x + 10"]},
    {"lvl":2,"q":"Développer $-2(3x - 5)$.","a":"-6x + 10","options":["-6x + 10","-6x - 10","6x + 10","-6x - 5"],"f":"a(b-c)=ab-ac","steps":["-2 × 3x = -6x","-2 × (-5) = +10 → -6x + 10"]}
]

# ============================================================
# 4EME
# ============================================================
data["4EME"] = {}

data["4EME"]["Fractions"] = [
    {"lvl":1,"q":"Calculer $\\frac{3}{7} + \\frac{2}{7}$.","a":"5/7","options":["5/7","5/14","6/7","1/7"],"f":"\\frac{a}{n}+\\frac{b}{n}=\\frac{a+b}{n}","steps":["Même dénominateur","3+2 = 5 → 5/7"]},
    {"lvl":1,"q":"Calculer $\\frac{5}{8} \\times \\frac{4}{3}$.","a":"5/6","options":["5/6","20/24","9/11","20/11"],"f":"\\frac{a}{b}\\times\\frac{c}{d}=\\frac{ac}{bd}","steps":["$\\frac{20}{24}$","Simplifier par 4 : $\\frac{5}{6}$"]},
    {"lvl":1,"q":"Calculer $\\frac{7}{12} - \\frac{1}{4}$.","a":"1/3","options":["1/3","6/8","4/12","2/3"],"f":"\\text{LCD puis soustraire}","steps":["$\\frac{7}{12}-\\frac{3}{12}=\\frac{4}{12}$","Simplifier : $\\frac{1}{3}$"]},
    {"lvl":1,"q":"Quel est l'inverse de $\\frac{5}{7}$ ?","a":"7/5","options":["7/5","-5/7","5/7","-7/5"],"f":"\\text{inverse de }\\frac{a}{b}=\\frac{b}{a}","steps":["Échanger numérateur et dénominateur","Inverse de 5/7 = 7/5"]},
    {"lvl":1,"q":"Simplifier $\\frac{9}{15}$.","a":"3/5","options":["3/5","9/15","3/15","9/5"],"f":"\\frac{a\\div\\text{PGCD}}{b\\div\\text{PGCD}}","steps":["PGCD(9,15) = 3","$\\frac{9÷3}{15÷3}=\\frac{3}{5}$"]},
    {"lvl":2,"q":"Calculer $\\frac{2}{3} \\div \\frac{5}{6}$.","a":"4/5","options":["4/5","10/18","5/4","12/15"],"f":"\\frac{a}{b}\\div\\frac{c}{d}=\\frac{a}{b}\\times\\frac{d}{c}","steps":["$\\frac{2}{3}×\\frac{6}{5}=\\frac{12}{15}$","Simplifier : $\\frac{4}{5}$"]},
    {"lvl":2,"q":"Calculer $\\left(\\frac{3}{4} + \\frac{1}{6}\\right) \\times 2$.","a":"11/6","options":["11/6","4/10","22/12","8/12"],"f":"\\text{LCD, additionner, puis multiplier}","steps":["$\\frac{9}{12}+\\frac{2}{12}=\\frac{11}{12}$","$\\frac{11}{12}×2=\\frac{22}{12}=\\frac{11}{6}$"]},
    {"lvl":2,"q":"Calculer $\\frac{5}{6} - \\frac{3}{4} + \\frac{1}{3}$.","a":"5/12","options":["5/12","3/13","1/3","7/12"],"f":"\\text{LCD = 12}","steps":["$\\frac{10}{12}-\\frac{9}{12}+\\frac{4}{12}$","$=\\frac{5}{12}$"]},
    {"lvl":2,"q":"Calculer $\\frac{-2}{3} \\times \\frac{9}{4}$.","a":"-3/2","options":["-3/2","3/2","-18/12","7/12"],"f":"\\frac{a}{b}\\times\\frac{c}{d}=\\frac{ac}{bd}","steps":["$\\frac{-18}{12}$","Simplifier par 6 : $\\frac{-3}{2}$"]},
    {"lvl":2,"q":"Calculer $\\frac{1}{1 - \\frac{2}{3}}$.","a":"3","options":["3","1/3","-1/3","2/3"],"f":"\\frac{1}{\\frac{a}{b}}=\\frac{b}{a}","steps":["$1-\\frac{2}{3}=\\frac{1}{3}$","$\\frac{1}{\\frac{1}{3}}=3$"]}
]

data["4EME"]["Puissances"] = [
    {"lvl":1,"q":"Calculer $2^5$.","a":"32","options":["32","16","64","10"],"f":"a^n=a\\times\\ldots\\times a","steps":["2⁵ = 2×2×2×2×2","= 32"]},
    {"lvl":1,"q":"Calculer $10^{-2}$.","a":"0,01","options":["0,01","0,1","100","0,001"],"f":"10^{-n}=\\frac{1}{10^n}","steps":["10⁻² = 1/10²","= 1/100 = 0,01"]},
    {"lvl":1,"q":"Calculer $3^0$.","a":"1","options":["1","0","3","-1"],"f":"a^0=1\\;(a\\neq0)","steps":["Toute puissance zéro vaut 1","3⁰ = 1"]},
    {"lvl":1,"q":"Calculer $(-2)^3$.","a":"-8","options":["-8","8","-6","6"],"f":"(-a)^{\\text{impair}}=-a^n","steps":["(-2)³ = (-2)×(-2)×(-2)","= 4×(-2) = -8"]},
    {"lvl":1,"q":"Écrire 0,001 comme puissance de 10.","a":"10⁻³","options":["10⁻³","10⁻²","10³","10⁻¹"],"f":"0{,}001=\\frac{1}{1000}=10^{-3}","steps":["0,001 = 1/1000","1000 = 10³ → 10⁻³"]},
    {"lvl":2,"q":"Calculer $2^3 \\times 2^5 \\div 2^4$.","a":"16","options":["16","8","64","32"],"f":"a^m\\times a^n\\div a^p=a^{m+n-p}","steps":["2^(3+5-4) = 2⁴","2⁴ = 16"]},
    {"lvl":2,"q":"Écrire $(5 \\times 10^3) \\times (3 \\times 10^2)$ en notation scientifique.","a":"1,5 × 10⁶","options":["1,5 × 10⁶","15 × 10⁵","1,5 × 10⁵","15 × 10⁶"],"f":"(a\\times10^m)(b\\times10^n)=ab\\times10^{m+n}","steps":["5×3 = 15, 10³×10² = 10⁵","15 × 10⁵ = 1,5 × 10⁶"]},
    {"lvl":2,"q":"Calculer $(10^4)^2 \\div 10^3$.","a":"10⁵","options":["10⁵","10⁶","10⁸","10¹¹"],"f":"(a^m)^n=a^{mn}","steps":["(10⁴)² = 10⁸","10⁸ ÷ 10³ = 10⁵"]},
    {"lvl":2,"q":"Calculer $3{,}2 \\times 10^4 + 1{,}8 \\times 10^4$.","a":"5 × 10⁴","options":["5 × 10⁴","5 × 10⁸","50 × 10⁴","4,14 × 10⁴"],"f":"a\\times10^n+b\\times10^n=(a+b)\\times10^n","steps":["3,2 + 1,8 = 5","5 × 10⁴"]},
    {"lvl":2,"q":"Calculer $\\left(\\frac{2}{3}\\right)^{-2}$.","a":"9/4","options":["9/4","4/9","-4/9","6/9"],"f":"\\left(\\frac{a}{b}\\right)^{-n}=\\left(\\frac{b}{a}\\right)^n","steps":["Inverser la fraction : (3/2)²","9/4"]}
]

data["4EME"]["Calcul_Littéral"] = [
    {"lvl":1,"q":"Développer $3(x - 2)$.","a":"3x - 6","options":["3x - 6","3x - 2","3x + 6","x - 6"],"f":"a(b+c)=ab+ac","steps":["3 × x = 3x","3 × (-2) = -6 → 3x - 6"]},
    {"lvl":1,"q":"Factoriser $4x + 12$.","a":"4(x + 3)","options":["4(x + 3)","2(2x + 6)","4(x + 12)","12(x + 4)"],"f":"ab+ac=a(b+c)","steps":["PGCD(4,12) = 4","4(x + 3)"]},
    {"lvl":1,"q":"Réduire $5x - 3 + 2x + 7$.","a":"7x + 4","options":["7x + 4","3x + 4","7x - 4","7x + 10"],"f":"\\text{regrouper les termes semblables}","steps":["5x + 2x = 7x","-3 + 7 = 4 → 7x + 4"]},
    {"lvl":1,"q":"Développer $x(x + 5)$.","a":"x² + 5x","options":["x² + 5x","x² + 5","6x","5x²"],"f":"a(b+c)=ab+ac","steps":["x × x = x²","x × 5 = 5x → x² + 5x"]},
    {"lvl":1,"q":"Développer $(x + 2)(x + 3)$.","a":"x² + 5x + 6","options":["x² + 5x + 6","x² + 6x + 5","x² + 6","2x + 5"],"f":"(a+b)(c+d)=ac+ad+bc+bd","steps":["x² + 3x + 2x + 6","= x² + 5x + 6"]},
    {"lvl":2,"q":"Développer $(2x - 3)(x + 4)$.","a":"2x² + 5x - 12","options":["2x² + 5x - 12","2x² + 11x - 12","2x² - 5x - 12","2x² + 5x + 12"],"f":"(a+b)(c+d)=ac+ad+bc+bd","steps":["2x² + 8x - 3x - 12","= 2x² + 5x - 12"]},
    {"lvl":2,"q":"Factoriser $x^2 - 9$.","a":"(x - 3)(x + 3)","options":["(x - 3)(x + 3)","(x - 9)(x + 1)","(x - 3)²","x(x - 9)"],"f":"a^2-b^2=(a-b)(a+b)","steps":["x² - 9 = x² - 3²","= (x-3)(x+3)"]},
    {"lvl":2,"q":"Développer $(x - 4)^2$.","a":"x² - 8x + 16","options":["x² - 8x + 16","x² - 16","x² + 8x + 16","x² - 4x + 16"],"f":"(a-b)^2=a^2-2ab+b^2","steps":["x² - 2×x×4 + 4²","= x² - 8x + 16"]},
    {"lvl":2,"q":"Factoriser $6x^2 + 3x$.","a":"3x(2x + 1)","options":["3x(2x + 1)","3(2x² + x)","6x(x + 3)","x(6x + 3)"],"f":"ab+ac=a(b+c)","steps":["Facteur commun : 3x","3x(2x + 1)"]},
    {"lvl":2,"q":"Développer $(3x + 1)^2$.","a":"9x² + 6x + 1","options":["9x² + 6x + 1","9x² + 1","3x² + 6x + 1","9x² + 3x + 1"],"f":"(a+b)^2=a^2+2ab+b^2","steps":["(3x)² + 2×3x×1 + 1²","= 9x² + 6x + 1"]}
]

data["4EME"]["Équations"] = [
    {"lvl":1,"q":"Résoudre $2x + 3 = 11$.","a":"4","options":["4","7","3","5,5"],"f":"x=\\frac{c-b}{a}","steps":["2x = 11 - 3 = 8","x = 8 ÷ 2 = 4"]},
    {"lvl":1,"q":"Résoudre $x - 5 = 8$.","a":"13","options":["13","3","-3","40"],"f":"x=c+b","steps":["x = 8 + 5","x = 13"]},
    {"lvl":1,"q":"Résoudre $3x = 18$.","a":"6","options":["6","15","21","54"],"f":"x=\\frac{c}{a}","steps":["Diviser par 3","x = 18 ÷ 3 = 6"]},
    {"lvl":1,"q":"Résoudre $\\frac{x}{4} = 3$.","a":"12","options":["12","0,75","7","3/4"],"f":"x=c\\times a","steps":["Multiplier par 4","x = 3 × 4 = 12"]},
    {"lvl":1,"q":"Résoudre $5x - 2 = 13$.","a":"3","options":["3","2,2","15","5"],"f":"x=\\frac{c+b}{a}","steps":["5x = 13 + 2 = 15","x = 15 ÷ 5 = 3"]},
    {"lvl":2,"q":"Résoudre $3(x + 2) = 2x + 10$.","a":"4","options":["4","8","2","16"],"f":"\\text{développer puis isoler } x","steps":["3x + 6 = 2x + 10","x = 4"]},
    {"lvl":2,"q":"Résoudre $4x - 7 = 2x + 5$.","a":"6","options":["6","-1","12","3"],"f":"\\text{regrouper les } x","steps":["4x - 2x = 5 + 7","2x = 12 → x = 6"]},
    {"lvl":2,"q":"Résoudre $2(3x - 1) = 5x + 4$.","a":"6","options":["6","2","-6","4"],"f":"\\text{développer puis isoler } x","steps":["6x - 2 = 5x + 4","x = 6"]},
    {"lvl":2,"q":"Résoudre $\\frac{x+1}{3} = 5$.","a":"14","options":["14","4","16","2"],"f":"x=3c-1","steps":["x + 1 = 15","x = 14"]},
    {"lvl":2,"q":"Résoudre $7 - 3x = x + 3$.","a":"1","options":["1","-1","4","2,5"],"f":"\\text{regrouper les } x","steps":["7 - 3 = x + 3x","4 = 4x → x = 1"]}
]

data["4EME"]["Pythagore"] = [
    {"lvl":1,"q":"Triangle rectangle : côtés 5 cm et 12 cm. Hypoténuse ?","a":"13","options":["13","17","60","7"],"f":"c=\\sqrt{a^2+b^2}","steps":["5² + 12² = 25 + 144 = 169","√169 = 13"]},
    {"lvl":1,"q":"Hypoténuse = 10, un côté = 8. L'autre côté ?","a":"6","options":["6","2","18","12,8"],"f":"b=\\sqrt{c^2-a^2}","steps":["10² - 8² = 100 - 64 = 36","√36 = 6"]},
    {"lvl":1,"q":"Calculer $3^2 + 4^2$.","a":"25","options":["25","7","12","14"],"f":"a^2+b^2","steps":["9 + 16","= 25"]},
    {"lvl":1,"q":"Hypoténuse = 15, un côté = 9. L'autre côté ?","a":"12","options":["12","6","24","18"],"f":"b=\\sqrt{c^2-a^2}","steps":["15² - 9² = 225 - 81 = 144","√144 = 12"]},
    {"lvl":1,"q":"Dans un triangle rectangle, l'hypoténuse est…","a":"le plus grand côté","options":["le plus grand côté","le plus petit côté","un côté de l'angle droit","la hauteur"],"f":"\\text{hypoténuse = côté opposé à l'angle droit}","steps":["C'est le côté face à l'angle droit","C'est toujours le plus long"]},
    {"lvl":2,"q":"$A(1\\,;\\,2)$ et $B(4\\,;\\,6)$. Distance AB ?","a":"5","options":["5","7","√7","25"],"f":"AB=\\sqrt{(x_B-x_A)^2+(y_B-y_A)^2}","steps":["(4-1)² + (6-2)² = 9 + 16 = 25","√25 = 5"]},
    {"lvl":2,"q":"Le triangle 8, 15, 17 est-il rectangle ?","a":"Oui","options":["Oui","Non","Isocèle","Quelconque"],"f":"a^2+b^2=c^2 ?","steps":["8² + 15² = 64 + 225 = 289","17² = 289 → rectangle"]},
    {"lvl":2,"q":"Diagonale d'un rectangle 9 cm × 12 cm ?","a":"15","options":["15","21","108","10,5"],"f":"d=\\sqrt{L^2+l^2}","steps":["9² + 12² = 81 + 144 = 225","√225 = 15"]},
    {"lvl":2,"q":"Échelle de 6 m contre un mur, pied à 3,6 m. Hauteur atteinte ?","a":"4,8 m","options":["4,8 m","2,4 m","9,6 m","6,84 m"],"f":"h=\\sqrt{c^2-d^2}","steps":["6² - 3,6² = 36 - 12,96 = 23,04","√23,04 = 4,8 m"]},
    {"lvl":2,"q":"$A(0;0)$, $B(3;0)$, $C(3;4)$. Triangle rectangle en quel sommet ?","a":"Oui, en B","options":["Oui, en B","Oui, en A","Oui, en C","Non"],"f":"\\text{vérifier les distances}","steps":["AB=3, BC=4, AC=5","3² + 4² = 25 = 5² → rectangle en B"]}
]

data["4EME"]["Proportionnalité"] = [
    {"lvl":1,"q":"Calculer 30 % de 200.","a":"60","options":["60","30","6","600"],"f":"\\frac{p}{100}\\times N","steps":["30% = 0,30","0,30 × 200 = 60"]},
    {"lvl":1,"q":"Un prix passe de 50 € à 60 €. Pourcentage d'augmentation ?","a":"20 %","options":["20 %","10 %","12 %","16,7 %"],"f":"\\%=\\frac{\\text{variation}}{\\text{initial}}\\times100","steps":["Variation : 60-50 = 10","10/50 × 100 = 20 %"]},
    {"lvl":1,"q":"Coefficient multiplicateur d'une hausse de 25 % ?","a":"1,25","options":["1,25","0,25","1,75","25"],"f":"CM=1+\\frac{t}{100}","steps":["1 + 25/100","= 1,25"]},
    {"lvl":1,"q":"Prix TTC si HT = 80 € et TVA = 20 % ?","a":"96 €","options":["96 €","100 €","16 €","64 €"],"f":"\\text{TTC}=\\text{HT}\\times 1{,}20","steps":["80 × 1,20","= 96 €"]},
    {"lvl":1,"q":"Réduction de 15 % sur 120 €. Prix final ?","a":"102 €","options":["102 €","105 €","18 €","108 €"],"f":"\\text{prix}=\\text{initial}\\times(1-\\frac{t}{100})","steps":["120 × 0,85","= 102 €"]},
    {"lvl":2,"q":"Hausse de 10 % puis baisse de 10 %. Prix final pour 100 € ?","a":"99 €","options":["99 €","100 €","101 €","90 €"],"f":"CM=1{,}10\\times0{,}90","steps":["100 × 1,10 = 110","110 × 0,90 = 99 €"]},
    {"lvl":2,"q":"Deux baisses successives de 20 % et 10 %. Coefficient global ?","a":"0,72","options":["0,72","0,70","0,30","0,28"],"f":"CM=CM_1\\times CM_2","steps":["0,80 × 0,90","= 0,72"]},
    {"lvl":2,"q":"Après une hausse de 15 %, quel % de baisse pour revenir au prix initial ?","a":"≈ 13 %","options":["≈ 13 %","15 %","≈ 17 %","85 %"],"f":"\\text{baisse}=1-\\frac{1}{CM}","steps":["1/1,15 ≈ 0,8696","1 - 0,8696 ≈ 0,13 → ≈ 13 %"]},
    {"lvl":2,"q":"Population 5000, croissance 3 %/an. Population après 2 ans ?","a":"5305","options":["5305","5300","5600","5150"],"f":"P=P_0\\times(1+t)^n","steps":["5000 × 1,03²","= 5000 × 1,0609 ≈ 5305"]},
    {"lvl":2,"q":"Aller à 60 km/h, retour à 40 km/h (120 km chaque). Vitesse moyenne ?","a":"48 km/h","options":["48 km/h","50 km/h","100 km/h","45 km/h"],"f":"v_m=\\frac{d_{\\text{totale}}}{t_{\\text{total}}}","steps":["Temps : 120/60 + 120/40 = 2+3 = 5 h","240/5 = 48 km/h"]}
]

data["4EME"]["Fonctions_lineaires"] = [
    {"lvl":1,"q":"$f(x) = 3x$. Calculer $f(4)$.","a":"12","options":["12","7","34","0,75"],"f":"f(x)=ax","steps":["Remplacer x par 4","3 × 4 = 12"]},
    {"lvl":1,"q":"$f(x) = -2x$. Calculer $f(-3)$.","a":"6","options":["6","-6","1","-1"],"f":"f(x)=ax","steps":["(-2) × (-3)","= 6"]},
    {"lvl":1,"q":"$g(x) = 5x$. Image de 0 ?","a":"0","options":["0","5","-5","1"],"f":"f(0)=a\\times0=0","steps":["5 × 0","= 0"]},
    {"lvl":1,"q":"$f(x) = 4x$. Antécédent de 20 ?","a":"5","options":["5","80","16","24"],"f":"ax=y\\Rightarrow x=\\frac{y}{a}","steps":["4x = 20","x = 20 ÷ 4 = 5"]},
    {"lvl":1,"q":"Le graphique d'une fonction linéaire passe toujours par…","a":"L'origine (0;0)","options":["L'origine (0;0)","(1;1)","(0;1)","(1;0)"],"f":"f(0)=a\\times0=0","steps":["f(0) = a × 0 = 0","Donc la droite passe par (0;0)"]},
    {"lvl":2,"q":"$f$ est linéaire et $f(3) = 12$. Quel est le coefficient ?","a":"4","options":["4","36","9","15"],"f":"a=\\frac{f(x)}{x}","steps":["a = 12 ÷ 3","a = 4"]},
    {"lvl":2,"q":"$f(x) = -3x + 7$. Est-ce une fonction linéaire ?","a":"Non, c'est affine","options":["Non, c'est affine","Oui","Non, c'est constante","Impossible à dire"],"f":"\\text{linéaire : }f(x)=ax\\text{ ; affine : }f(x)=ax+b","steps":["Il y a une ordonnée à l'origine (+7)","Donc c'est une fonction affine, pas linéaire"]},
    {"lvl":2,"q":"$f(x) = 2x$ et $g(x) = -x$. Pour quel $x$ a-t-on $f(x) = g(x)$ ?","a":"0","options":["0","2","-1","1"],"f":"2x=-x\\Rightarrow3x=0","steps":["2x = -x → 3x = 0","x = 0"]},
    {"lvl":2,"q":"$f$ linéaire, $f(5) = -15$. Exprimer $f(x)$.","a":"f(x) = -3x","options":["f(x) = -3x","f(x) = -15x","f(x) = 3x","f(x) = -5x"],"f":"a=\\frac{f(x)}{x}","steps":["a = -15 ÷ 5 = -3","f(x) = -3x"]},
    {"lvl":2,"q":"$f(x) = 2{,}5x$. Pour quel $x$ a-t-on $f(x) = 100$ ?","a":"40","options":["40","250","97,5","4"],"f":"x=\\frac{y}{a}","steps":["2,5x = 100","x = 100 ÷ 2,5 = 40"]}
]

# ============================================================
# 3EME
# ============================================================
data["3EME"] = {}

data["3EME"]["Calcul_Littéral"] = [
    {"lvl":1,"q":"Développer $(x + 3)(x - 3)$.","a":"x² - 9","options":["x² - 9","x² + 9","x² - 6x + 9","2x"],"f":"(a+b)(a-b)=a^2-b^2","steps":["Identité remarquable : a²-b²","x² - 3² = x² - 9"]},
    {"lvl":1,"q":"Développer $(2x + 1)^2$.","a":"4x² + 4x + 1","options":["4x² + 4x + 1","4x² + 1","2x² + 4x + 1","4x² + 2x + 1"],"f":"(a+b)^2=a^2+2ab+b^2","steps":["(2x)² + 2×2x×1 + 1²","= 4x² + 4x + 1"]},
    {"lvl":1,"q":"Factoriser $5x^2 + 10x$.","a":"5x(x + 2)","options":["5x(x + 2)","5(x² + 2x)","x(5x + 10)","10x(x + 5)"],"f":"ab+ac=a(b+c)","steps":["Facteur commun : 5x","5x(x + 2)"]},
    {"lvl":1,"q":"Développer $(x - 5)^2$.","a":"x² - 10x + 25","options":["x² - 10x + 25","x² - 25","x² + 10x + 25","x² - 5x + 25"],"f":"(a-b)^2=a^2-2ab+b^2","steps":["x² - 2×x×5 + 5²","= x² - 10x + 25"]},
    {"lvl":1,"q":"Factoriser $4x^2 - 16$.","a":"4(x - 2)(x + 2)","options":["4(x - 2)(x + 2)","(4x - 4)(x + 4)","4(x² - 4)","(2x - 4)²"],"f":"a^2-b^2=(a-b)(a+b)","steps":["4(x² - 4) = 4(x² - 2²)","= 4(x-2)(x+2)"]},
    {"lvl":2,"q":"Factoriser $x^2 - 6x + 9$.","a":"(x - 3)²","options":["(x - 3)²","(x + 3)²","(x - 9)(x + 1)","x(x - 6) + 9"],"f":"a^2-2ab+b^2=(a-b)^2","steps":["x² - 2×x×3 + 3²","= (x - 3)²"]},
    {"lvl":2,"q":"Développer $(3x - 2)(2x + 5)$.","a":"6x² + 11x - 10","options":["6x² + 11x - 10","6x² + 19x - 10","6x² - 11x - 10","5x² + 11x - 10"],"f":"(a+b)(c+d)=ac+ad+bc+bd","steps":["6x² + 15x - 4x - 10","= 6x² + 11x - 10"]},
    {"lvl":2,"q":"Factoriser $9x^2 - 4$.","a":"(3x - 2)(3x + 2)","options":["(3x - 2)(3x + 2)","(9x - 2)(x + 2)","(3x - 4)(3x + 1)","3(3x² - 4)"],"f":"a^2-b^2=(a-b)(a+b)","steps":["(3x)² - 2²","= (3x-2)(3x+2)"]},
    {"lvl":2,"q":"Développer puis réduire $(x+1)^2 - (x-1)^2$.","a":"4x","options":["4x","2","2x² + 2","0"],"f":"(a+b)^2-(a-b)^2=4ab","steps":["(x²+2x+1) - (x²-2x+1)","= 4x"]},
    {"lvl":2,"q":"Factoriser $x^2 + 8x + 16$.","a":"(x + 4)²","options":["(x + 4)²","(x + 8)(x + 2)","(x + 16)(x + 1)","x(x + 8) + 16"],"f":"a^2+2ab+b^2=(a+b)^2","steps":["x² + 2×x×4 + 4²","= (x + 4)²"]}
]

data["3EME"]["Équations"] = [
    {"lvl":1,"q":"Résoudre $5x - 3 = 2x + 9$.","a":"4","options":["4","2","6","12"],"f":"\\text{regrouper les } x","steps":["5x - 2x = 9 + 3","3x = 12 → x = 4"]},
    {"lvl":1,"q":"Résoudre $x^2 = 49$.","a":"7 ou -7","options":["7 ou -7","7","-7","49"],"f":"x=\\pm\\sqrt{c}","steps":["x² = 49","x = 7 ou x = -7"]},
    {"lvl":1,"q":"Résoudre $4(x - 1) = 3x + 2$.","a":"6","options":["6","2","-2","3"],"f":"\\text{développer puis isoler } x","steps":["4x - 4 = 3x + 2","x = 6"]},
    {"lvl":1,"q":"Résoudre $2x + 1 = 0$.","a":"-1/2","options":["-1/2","1/2","-2","2"],"f":"x=-\\frac{b}{a}","steps":["2x = -1","x = -1/2"]},
    {"lvl":1,"q":"Résoudre $3x + 5 = 3x + 8$.","a":"Aucune solution","options":["Aucune solution","0","1","Infinité de solutions"],"f":"\\text{si } 0x=c\\neq0\\text{ : impossible}","steps":["3x - 3x = 8 - 5","0 = 3 → impossible"]},
    {"lvl":2,"q":"Résoudre $(x+3)(x-2) = 0$.","a":"-3 ou 2","options":["-3 ou 2","3 ou -2","-6","1"],"f":"A\\times B=0\\Leftrightarrow A=0\\text{ ou }B=0","steps":["x+3=0 → x=-3","x-2=0 → x=2"]},
    {"lvl":2,"q":"Résoudre $x^2 - 5x + 6 = 0$.","a":"2 ou 3","options":["2 ou 3","-2 ou -3","6 ou 1","-6"],"f":"\\text{factoriser : }(x-a)(x-b)=0","steps":["(x-2)(x-3) = 0","x = 2 ou x = 3"]},
    {"lvl":2,"q":"Résoudre $(2x-1)^2 = 9$.","a":"2 ou -1","options":["2 ou -1","2","5","4 ou -4"],"f":"A^2=c\\Rightarrow A=\\pm\\sqrt{c}","steps":["2x-1 = 3 → x=2","2x-1 = -3 → x=-1"]},
    {"lvl":2,"q":"Résoudre $x^2 + 4 = 0$.","a":"Aucune solution réelle","options":["Aucune solution réelle","2","-2","2 ou -2"],"f":"x^2=-c<0\\Rightarrow\\text{pas de solution réelle}","steps":["x² = -4","Un carré est toujours ≥ 0 → impossible"]},
    {"lvl":2,"q":"Résoudre $3x^2 = 48$.","a":"4 ou -4","options":["4 ou -4","16","4","-4"],"f":"x=\\pm\\sqrt{\\frac{c}{a}}","steps":["x² = 16","x = 4 ou x = -4"]}
]

data["3EME"]["Fonctions"] = [
    {"lvl":1,"q":"$f(x) = 2x + 3$. Calculer $f(4)$.","a":"11","options":["11","9","14","8"],"f":"f(x)=ax+b","steps":["f(4) = 2×4 + 3","= 8 + 3 = 11"]},
    {"lvl":1,"q":"$f(x) = x^2 - 1$. Calculer $f(3)$.","a":"8","options":["8","5","10","2"],"f":"f(x)=x^2-1","steps":["f(3) = 3² - 1 = 9 - 1","= 8"]},
    {"lvl":1,"q":"$f(x) = -x + 5$. Image de 2 ?","a":"3","options":["3","7","-3","10"],"f":"f(x)=-x+5","steps":["f(2) = -2 + 5","= 3"]},
    {"lvl":1,"q":"$f(x) = 3x - 6$. Antécédent de 0 ?","a":"2","options":["2","0","-2","6"],"f":"f(x)=0\\Rightarrow x=-\\frac{b}{a}","steps":["3x - 6 = 0","x = 2"]},
    {"lvl":1,"q":"$f(x) = x^2$. Est-elle croissante sur $\\mathbb{R}$ ?","a":"Non","options":["Non","Oui","Seulement pour x > 0","Seulement pour x < 0"],"f":"f'(x)=2x","steps":["f décroît pour x < 0, croît pour x > 0","Elle n'est pas croissante sur ℝ entier"]},
    {"lvl":2,"q":"$f(x)=2x-1$ et $g(x)=-x+5$. Point d'intersection ?","a":"(2 ; 3)","options":["(2 ; 3)","(3 ; 2)","(2 ; 5)","(1 ; 1)"],"f":"f(x)=g(x)","steps":["2x-1 = -x+5 → 3x = 6 → x = 2","f(2) = 3 → (2 ; 3)"]},
    {"lvl":2,"q":"$f(x) = x^2 - 4x + 3$. Calculer $f(1)$.","a":"0","options":["0","-6","8","2"],"f":"\\text{substituer}","steps":["f(1) = 1 - 4 + 3","= 0"]},
    {"lvl":2,"q":"$f(x) = -2x + 8$. Pour quels $x$ a-t-on $f(x) > 0$ ?","a":"x < 4","options":["x < 4","x > 4","x < -4","x > -4"],"f":"-2x+8>0","steps":["-2x > -8","x < 4"]},
    {"lvl":2,"q":"$f$ affine, $f(0) = 3$ et $f(2) = 7$. Exprimer $f(x)$.","a":"f(x) = 2x + 3","options":["f(x) = 2x + 3","f(x) = 3x + 2","f(x) = 2x + 7","f(x) = 3,5x"],"f":"a=\\frac{f(x_2)-f(x_1)}{x_2-x_1}","steps":["a = (7-3)/(2-0) = 2","b = f(0) = 3 → f(x) = 2x + 3"]},
    {"lvl":2,"q":"Maximum de $f(x) = -x^2 + 6x - 5$ ?","a":"4","options":["4","3","5","-5"],"f":"x_s=-\\frac{b}{2a}","steps":["Sommet : x = -6/(2×(-1)) = 3","f(3) = -9 + 18 - 5 = 4"]}
]

data["3EME"]["Théorème_de_Thalès"] = [
    {"lvl":1,"q":"$AB=6$, $AC=9$, $AM=4$, $(MN)\\parallel(BC)$. Calculer $AN$.","a":"6","options":["6","4,5","13,5","2,67"],"f":"\\frac{AM}{AB}=\\frac{AN}{AC}","steps":["AN/9 = 4/6","AN = 9 × 4/6 = 6"]},
    {"lvl":1,"q":"$AB=10$, $AM=4$, $AC=15$. Calculer $AN$ (Thalès).","a":"6","options":["6","8","37,5","9"],"f":"\\frac{AM}{AB}=\\frac{AN}{AC}","steps":["AN/15 = 4/10","AN = 15 × 0,4 = 6"]},
    {"lvl":1,"q":"$AB=8$, $AM=2$, $MN=3$, $(MN)\\parallel(BC)$. Calculer $BC$.","a":"12","options":["12","6","24","0,75"],"f":"\\frac{MN}{BC}=\\frac{AM}{AB}","steps":["3/BC = 2/8","BC = 3 × 8/2 = 12"]},
    {"lvl":1,"q":"$AM=3$, $AB=9$, $AN=5$. Calculer $AC$ (Thalès).","a":"15","options":["15","45","5","1,67"],"f":"\\frac{AM}{AB}=\\frac{AN}{AC}","steps":["5/AC = 3/9","AC = 5 × 9/3 = 15"]},
    {"lvl":1,"q":"Deux droites coupées par des parallèles : segments 4 et 6 d'un côté, 8 de l'autre. Segment manquant ?","a":"12","options":["12","8","3","48"],"f":"\\frac{a}{b}=\\frac{c}{d}","steps":["4/6 = 8/x","x = 6 × 8/4 = 12"]},
    {"lvl":2,"q":"$AB=12$, $AM=4$, $BC=9$, $(MN)\\parallel(BC)$. Calculer $MN$.","a":"3","options":["3","27","6","36"],"f":"\\frac{MN}{BC}=\\frac{AM}{AB}","steps":["MN/9 = 4/12","MN = 9 × 1/3 = 3"]},
    {"lvl":2,"q":"$AM=3$, $AB=7{,}5$, $AN=4$, $AC=10$. $(MN)\\parallel(BC)$ ?","a":"Oui, parallèles","options":["Oui, parallèles","Non","Perpendiculaires","Données insuffisantes"],"f":"\\frac{AM}{AB}=\\frac{AN}{AC}\\;?","steps":["3/7,5 = 0,4 et 4/10 = 0,4","Égaux → parallèles (réciproque de Thalès)"]},
    {"lvl":2,"q":"Agrandissement de rapport $k = 2{,}5$. Si $AB = 4$, l'image $A'B'$ ?","a":"10","options":["10","6,5","1,6","100"],"f":"A'B'=k\\times AB","steps":["A'B' = 2,5 × 4","= 10"]},
    {"lvl":2,"q":"$AM=5$, $MB=7$, $AN=10$, $NC=14$. $(MN)\\parallel(BC)$ ?","a":"Oui","options":["Oui","Non","AM/MB ≠ AN/NC","Données insuffisantes"],"f":"\\frac{AM}{AB}=\\frac{AN}{AC}\\;?","steps":["AM/AB = 5/12, AN/AC = 10/24 = 5/12","Égaux → parallèles"]},
    {"lvl":2,"q":"Ombre : poteau 6 m, ombre 4 m. Arbre : ombre 10 m. Hauteur de l'arbre ?","a":"15 m","options":["15 m","24 m","6,67 m","2,4 m"],"f":"\\frac{h_1}{o_1}=\\frac{h_2}{o_2}","steps":["6/4 = h/10","h = 6 × 10/4 = 15 m"]}
]

data["3EME"]["Trigonométrie"] = [
    {"lvl":1,"q":"Triangle rectangle, hypoténuse 10, angle 30°. Côté opposé ?","a":"5","options":["5","8,66","10","20"],"f":"\\sin(\\alpha)=\\frac{\\text{opposé}}{\\text{hypoténuse}}","steps":["sin(30°) = 0,5","Opposé = 10 × 0,5 = 5"]},
    {"lvl":1,"q":"$\\cos(60°) = ?$","a":"0,5","options":["0,5","1","0,866","0"],"f":"\\cos(60°)=0{,}5","steps":["Valeur remarquable","cos(60°) = 0,5"]},
    {"lvl":1,"q":"Côté opposé = 6, adjacent = 6. L'angle vaut…","a":"45°","options":["45°","30°","60°","90°"],"f":"\\tan(\\alpha)=\\frac{\\text{opposé}}{\\text{adjacent}}","steps":["tan(α) = 6/6 = 1","arctan(1) = 45°"]},
    {"lvl":1,"q":"Adjacent = 8, hypoténuse = 10. $\\cos(\\alpha) = ?$","a":"0,8","options":["0,8","0,6","1,25","0,4"],"f":"\\cos(\\alpha)=\\frac{\\text{adjacent}}{\\text{hypoténuse}}","steps":["cos(α) = 8/10","= 0,8"]},
    {"lvl":1,"q":"$\\sin(90°) = ?$","a":"1","options":["1","0","-1","0,5"],"f":"\\sin(90°)=1","steps":["Valeur remarquable","sin(90°) = 1"]},
    {"lvl":2,"q":"Angle 40°, hypoténuse 12. Côté adjacent ?","a":"≈ 9,19","options":["≈ 9,19","≈ 7,71","≈ 15,66","≈ 12,77"],"f":"\\text{adj}=\\text{hyp}\\times\\cos(\\alpha)","steps":["cos(40°) ≈ 0,766","12 × 0,766 ≈ 9,19"]},
    {"lvl":2,"q":"Opposé = 7, adjacent = 7. L'angle vaut…","a":"45°","options":["45°","30°","60°","90°"],"f":"\\tan(\\alpha)=\\frac{\\text{opp}}{\\text{adj}}","steps":["tan(α) = 7/7 = 1","arctan(1) = 45°"]},
    {"lvl":2,"q":"$\\sin(\\alpha) = \\frac{3}{5}$. Calculer $\\cos(\\alpha)$.","a":"0,8","options":["0,8","0,6","0,4","0,75"],"f":"\\cos^2+\\sin^2=1","steps":["cos² = 1 - (3/5)² = 1 - 9/25 = 16/25","cos = 4/5 = 0,8"]},
    {"lvl":2,"q":"Distance 20 m, angle d'élévation 35°. Hauteur de l'arbre ?","a":"≈ 14 m","options":["≈ 14 m","≈ 11,47 m","≈ 7 m","≈ 28 m"],"f":"h=d\\times\\tan(\\alpha)","steps":["tan(35°) ≈ 0,7","20 × 0,7 ≈ 14 m"]},
    {"lvl":2,"q":"Hypoténuse = 13, opposé = 5. L'angle vaut…","a":"≈ 22,6°","options":["≈ 22,6°","≈ 67,4°","≈ 45°","≈ 30°"],"f":"\\alpha=\\arcsin\\left(\\frac{\\text{opp}}{\\text{hyp}}\\right)","steps":["sin(α) = 5/13 ≈ 0,385","α ≈ 22,6°"]}
]

data["3EME"]["Statistiques"] = [
    {"lvl":1,"q":"Moyenne de 8, 12, 14, 10, 16.","a":"12","options":["12","10","60","14"],"f":"\\bar{x}=\\frac{\\sum x_i}{n}","steps":["8+12+14+10+16 = 60","60 ÷ 5 = 12"]},
    {"lvl":1,"q":"Médiane de 3, 5, 7, 9, 11.","a":"7","options":["7","5","9","35"],"f":"\\text{valeur centrale}","steps":["Série déjà ordonnée, 5 valeurs","Valeur centrale (3e) = 7"]},
    {"lvl":1,"q":"Étendue de 2, 8, 15, 4, 11.","a":"13","options":["13","15","8","40"],"f":"E=x_{\\max}-x_{\\min}","steps":["Max = 15, Min = 2","15 - 2 = 13"]},
    {"lvl":1,"q":"Effectifs : 12, 8, 15, 5. Effectif total ?","a":"40","options":["40","35","48","10"],"f":"N=\\sum n_i","steps":["12 + 8 + 15 + 5","= 40"]},
    {"lvl":1,"q":"Effectif de A = 6, total = 30. Fréquence de A ?","a":"20 %","options":["20 %","6 %","24 %","5 %"],"f":"f=\\frac{n}{N}\\times100","steps":["6/30 = 0,2","0,2 × 100 = 20 %"]},
    {"lvl":2,"q":"Moyenne pondérée : 10 (coeff 2), 14 (coeff 3), 8 (coeff 5).","a":"10,2","options":["10,2","10,67","32","12"],"f":"\\bar{x}=\\frac{\\sum n_i x_i}{\\sum n_i}","steps":["20 + 42 + 40 = 102","102 ÷ 10 = 10,2"]},
    {"lvl":2,"q":"12 valeurs ordonnées, 6e = 14 et 7e = 16. Médiane ?","a":"15","options":["15","14","16","30"],"f":"\\text{médiane}=\\frac{v_{n/2}+v_{n/2+1}}{2}","steps":["Nombre pair : moyenne des 2 valeurs centrales","(14 + 16)/2 = 15"]},
    {"lvl":2,"q":"20 valeurs ordonnées, 5e valeur = 8. Premier quartile Q1 ?","a":"8","options":["8","5","10","4"],"f":"Q_1=v_{n/4}","steps":["Q1 = valeur de rang n/4 = 20/4 = 5e","Q1 = 8"]},
    {"lvl":2,"q":"Diagramme en boîte : Q1=5, Q3=12. Écart interquartile ?","a":"7","options":["7","16","10","3"],"f":"EIQ=Q_3-Q_1","steps":["Q3 - Q1","12 - 5 = 7"]},
    {"lvl":2,"q":"Notes : 6, 8, 10, 10, 12, 14, 16, 18. Médiane ?","a":"11","options":["11","10","12","10,5"],"f":"\\text{médiane}=\\frac{v_4+v_5}{2}","steps":["8 valeurs : moyenne des 4e et 5e","(10 + 12)/2 = 11"]}
]

data["3EME"]["Probabilites"] = [
    {"lvl":1,"q":"On lance un dé équilibré. Probabilité d'obtenir 6 ?","a":"1/6","options":["1/6","1/3","6","1/2"],"f":"P=\\frac{\\text{cas favorables}}{\\text{cas possibles}}","steps":["1 face sur 6","P = 1/6"]},
    {"lvl":1,"q":"Sac : 3 boules rouges, 7 bleues. Probabilité de tirer une rouge ?","a":"3/10","options":["3/10","3/7","7/10","1/3"],"f":"P=\\frac{n_R}{n_{\\text{total}}}","steps":["Total = 3 + 7 = 10","P = 3/10"]},
    {"lvl":1,"q":"Probabilité d'un événement certain ?","a":"1","options":["1","0","0,5","100"],"f":"P(\\Omega)=1","steps":["Événement certain = toujours réalisé","Sa probabilité vaut 1"]},
    {"lvl":1,"q":"Sac de 5 billes dont 2 vertes. Probabilité de tirer une verte ?","a":"2/5","options":["2/5","5/2","1/5","3/5"],"f":"P=\\frac{n_{\\text{fav}}}{n_{\\text{total}}}","steps":["2 vertes sur 5","P = 2/5"]},
    {"lvl":1,"q":"Pile ou face. Probabilité d'obtenir pile ?","a":"1/2","options":["1/2","1/4","1","2"],"f":"P=\\frac{1}{2}","steps":["2 issues équiprobables","P(pile) = 1/2"]},
    {"lvl":2,"q":"Deux lancers de pièce. Probabilité d'obtenir 2 piles ?","a":"1/4","options":["1/4","1/2","1/8","3/4"],"f":"P=P_1\\times P_2","steps":["P(pile) × P(pile) = 1/2 × 1/2","= 1/4"]},
    {"lvl":2,"q":"$P(A) = 0{,}3$. Probabilité de l'événement contraire ?","a":"0,7","options":["0,7","0,3","-0,3","1,3"],"f":"P(\\bar{A})=1-P(A)","steps":["1 - 0,3","= 0,7"]},
    {"lvl":2,"q":"On lance un dé. Probabilité d'obtenir un nombre pair ?","a":"1/2","options":["1/2","1/3","1/6","3"],"f":"P=\\frac{\\text{cas favorables}}{6}","steps":["Nombres pairs : 2, 4, 6 → 3 cas","3/6 = 1/2"]},
    {"lvl":2,"q":"Urne : 4 rouges, 3 vertes, 3 bleues. Probabilité de NE PAS tirer rouge ?","a":"3/5","options":["3/5","2/5","4/10","7/10"],"f":"P(\\bar{R})=1-P(R)","steps":["Total = 10, P(rouge) = 4/10","P(non rouge) = 6/10 = 3/5"]},
    {"lvl":2,"q":"On lance 2 dés. Probabilité que la somme soit 7 ?","a":"1/6","options":["1/6","7/36","1/12","2/12"],"f":"P=\\frac{\\text{cas favorables}}{36}","steps":["Combinaisons donnant 7 : (1,6)(2,5)(3,4)(4,3)(5,2)(6,1) = 6","6/36 = 1/6"]}
]

data["3EME"]["Racines_carrees"] = [
    {"lvl":1,"q":"Calculer $\\sqrt{36}$.","a":"6","options":["6","18","12","√6"],"f":"\\sqrt{a^2}=a","steps":["6 × 6 = 36","√36 = 6"]},
    {"lvl":1,"q":"Calculer $\\sqrt{81}$.","a":"9","options":["9","81","√9","27"],"f":"\\sqrt{a^2}=a","steps":["9 × 9 = 81","√81 = 9"]},
    {"lvl":1,"q":"Calculer $\\sqrt{100}$.","a":"10","options":["10","50","1000","√10"],"f":"\\sqrt{a^2}=a","steps":["10 × 10 = 100","√100 = 10"]},
    {"lvl":1,"q":"Calculer $(\\sqrt{5})^2$.","a":"5","options":["5","25","√25","10"],"f":"(\\sqrt{a})^2=a","steps":["Par définition de la racine carrée","(√5)² = 5"]},
    {"lvl":1,"q":"Calculer $\\sqrt{0}$.","a":"0","options":["0","1","Impossible","-1"],"f":"\\sqrt{0}=0","steps":["0 × 0 = 0","√0 = 0"]},
    {"lvl":2,"q":"Simplifier $\\sqrt{50}$.","a":"5√2","options":["5√2","25√2","√50","10√5"],"f":"\\sqrt{a\\times b}=\\sqrt{a}\\times\\sqrt{b}","steps":["50 = 25 × 2","√50 = √25 × √2 = 5√2"]},
    {"lvl":2,"q":"Calculer $\\sqrt{12} + \\sqrt{27}$.","a":"5√3","options":["5√3","√39","6√3","√15"],"f":"\\sqrt{a}+\\sqrt{b}\\neq\\sqrt{a+b}","steps":["√12 = 2√3, √27 = 3√3","2√3 + 3√3 = 5√3"]},
    {"lvl":2,"q":"Calculer $\\sqrt{8} \\times \\sqrt{2}$.","a":"4","options":["4","√10","16","2√4"],"f":"\\sqrt{a}\\times\\sqrt{b}=\\sqrt{ab}","steps":["√8 × √2 = √16","√16 = 4"]},
    {"lvl":2,"q":"Rationaliser $\\frac{1}{\\sqrt{3}}$.","a":"√3/3","options":["√3/3","3/√3","1/3","√3"],"f":"\\frac{1}{\\sqrt{a}}=\\frac{\\sqrt{a}}{a}","steps":["Multiplier haut et bas par √3","$\\frac{\\sqrt{3}}{3}$"]},
    {"lvl":2,"q":"Calculer $\\sqrt{75} - \\sqrt{48}$.","a":"√3","options":["√3","√27","3","9√3"],"f":"\\text{simplifier chaque racine}","steps":["√75 = 5√3, √48 = 4√3","5√3 - 4√3 = √3"]}
]

# ============================================================
# Validation
# ============================================================
total = 0
errors = []
for niveau, cats in data.items():
    for cat, exos in cats.items():
        total += len(exos)
        if len(exos) != 10:
            errors.append(f"{niveau}/{cat}: {len(exos)} exercices (attendu 10)")
        for i, ex in enumerate(exos):
            keys = {"lvl","q","a","options","f","steps"}
            if set(ex.keys()) != keys:
                errors.append(f"{niveau}/{cat}[{i}]: clés manquantes/extras {set(ex.keys()) ^ keys}")
            if len(ex.get("options",[])) != 4:
                errors.append(f"{niveau}/{cat}[{i}]: {len(ex.get('options',[]))} options (attendu 4)")
            if ex["a"] not in ex.get("options",[]):
                errors.append(f"{niveau}/{cat}[{i}]: réponse '{ex['a']}' absente des options")

print(f"Total exercices: {total}")
if errors:
    print(f"\n❌ {len(errors)} erreurs:")
    for e in errors:
        print(f"  - {e}")
else:
    print("✅ Validation OK — aucune erreur")

# Write JSON
with open("/home/nicolas/Bureau/algebra live/algebra/boost_exos.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("✅ boost_exos.json écrit")
