#!/usr/bin/env python3
"""
Monsieur Diversité — Réordonner + diversifier les types des exercices 3EME
Pour chaque chapitre: 2A+2I+1C par slot, 3Q+1V+1F par slot
"""
import json, copy
from sheets import sh

# ── Row mapping (1-indexed sheet rows) ──
CHAPTERS_3EME = {
    "Calcul littéral": 20,
    "Équations": 21,
    "Fonctions": 22,
    "Théorème de Thalès": 23,
    "Trigonométrie": 24,
    "Statistiques": 25,
    "Probabilités": 26,
    "Racines carrées": 27,
    "Systèmes d'équations": 31,
    "Inéquations": 32,
    "Notation scientifique": 43,
}

EXOS_COL = 5  # column E (1-indexed)

def load_chapter(row_num):
    raw = sh.read_raw('Curriculum_Officiel')
    row = raw[row_num - 1]
    return json.loads(row[4])

def write_chapter(row_num, exos):
    sh.update_cell('Curriculum_Officiel', row_num, EXOS_COL, json.dumps(exos, ensure_ascii=False))

# ══════════════════════════════════════════════════════════════════════
# NEW EXERCISES FOR ALL 11 CHAPTERS
# Each chapter: 20 exos, 4 slots of 5
# Per slot: 2A + 2I + 1C, 3QCM + 1VF + 1Fill
# ══════════════════════════════════════════════════════════════════════

NEW_EXOS = {}

# ─────────────────────────────────────────────────────────────────────
# 1. CALCUL LITTÉRAL
# ─────────────────────────────────────────────────────────────────────
NEW_EXOS["Calcul littéral"] = [
    # SLOT 1
    # A-QCM
    {"lvl":1,"q":"Développe $(x+3)^2$.","a":"$x^2+6x+9$","options":["$x^2+6x+9$","$x^2+3x+9$","$x^2+9$"],"steps":["Identité remarquable : $(a+b)^2 = a^2+2ab+b^2$","$a=x$, $b=3$ → $x^2+2 \\times x \\times 3+3^2$","$= x^2+6x+9$"],"f":"$(a+b)^2 = a^2+2ab+b^2$"},
    # A-QCM
    {"lvl":1,"q":"Factorise $x^2-16$.","a":"$(x-4)(x+4)$","options":["$(x-4)(x+4)$","$(x-8)(x+8)$","$(x-4)^2$"],"steps":["Identité remarquable : $a^2-b^2 = (a-b)(a+b)$","$x^2-16 = x^2-4^2$","$= (x-4)(x+4)$"],"f":"$a^2-b^2 = (a-b)(a+b)$"},
    # I-VF
    {"lvl":1,"type":"vf","q":"$(2x+3)^2 = 4x^2+9$.","a":"Faux","options":["Vrai","Faux"],"steps":["$(2x+3)^2 = (2x)^2+2 \\times 2x \\times 3+3^2$","$= 4x^2+12x+9$","Le double produit $12x$ a été oublié"],"f":"$(a+b)^2 = a^2+2ab+b^2$"},
    # I-QCM
    {"lvl":1,"q":"Factorise $9x^2-24x+16$.","a":"$(3x-4)^2$","options":["$(3x-4)^2$","$(9x-4)(x-4)$","$(3x+4)^2$"],"steps":["On reconnaît $a^2-2ab+b^2$ avec $a=3x$, $b=4$","$(3x)^2 = 9x^2$ ✓, $4^2 = 16$ ✓","$2 \\times 3x \\times 4 = 24x$ ✓ → $(3x-4)^2$"],"f":"$(a-b)^2 = a^2-2ab+b^2$"},
    # C-Fill
    {"lvl":1,"type":"fill","q":"Un architecte conçoit une terrasse carrée de côté $(x+5)$ m. L'aire vaut $x^2+10x+25$ m². Complète : pour $x=3$, l'aire vaut ___ m².","a":"64","options":[],"steps":["Aire $= (x+5)^2 = x^2+10x+25$","Pour $x=3$ : $(3+5)^2 = 8^2$","$= 64$ m²"],"f":"$(a+b)^2 = a^2+2ab+b^2$"},

    # SLOT 2
    # A-QCM
    {"lvl":1,"q":"Développe $(x-7)^2$.","a":"$x^2-14x+49$","options":["$x^2-14x+49$","$x^2-7x+49$","$x^2-14x+7$"],"steps":["Identité : $(a-b)^2 = a^2-2ab+b^2$","$a=x$, $b=7$ → $x^2-2 \\times x \\times 7+7^2$","$= x^2-14x+49$"],"f":"$(a-b)^2 = a^2-2ab+b^2$"},
    # A-VF
    {"lvl":1,"type":"vf","q":"$x^2-25 = (x-5)(x+5)$.","a":"Vrai","options":["Vrai","Faux"],"steps":["Identité : $a^2-b^2 = (a-b)(a+b)$","$x^2-25 = x^2-5^2$","$= (x-5)(x+5)$ ✓"],"f":"$a^2-b^2 = (a-b)(a+b)$"},
    # I-QCM
    {"lvl":1,"q":"Factorise $2x^2-50$.","a":"$2(x-5)(x+5)$","options":["$2(x-5)(x+5)$","$(2x-50)$","$2(x-25)$"],"steps":["Facteur commun : $2x^2-50 = 2(x^2-25)$","$x^2-25 = (x-5)(x+5)$","$= 2(x-5)(x+5)$"],"f":"$a^2-b^2 = (a-b)(a+b)$"},
    # I-Fill
    {"lvl":1,"type":"fill","q":"Complète : $x^2-10x+25 = (x-\\text{___})^2$.","a":"5","options":[],"steps":["On cherche $b$ tel que $(x-b)^2 = x^2-2bx+b^2$","$2b = 10$ donc $b = 5$","Vérification : $b^2 = 25$ ✓"],"f":"$(a-b)^2 = a^2-2ab+b^2$"},
    # C-QCM
    {"lvl":1,"q":"Développe et réduis $(x+4)^2-(x-4)^2$.","a":"$16x$","options":["$16x$","$8x$","$2x^2+32$"],"steps":["$(x+4)^2 = x^2+8x+16$","$(x-4)^2 = x^2-8x+16$","Différence : $x^2+8x+16-x^2+8x-16 = 16x$"],"f":"$(a+b)^2-(a-b)^2 = 4ab$"},

    # SLOT 3
    # A-QCM
    {"lvl":2,"q":"Factorise $36x^2-1$.","a":"$(6x-1)(6x+1)$","options":["$(6x-1)(6x+1)$","$(6x-1)^2$","$(36x-1)(x+1)$"],"steps":["$36x^2-1 = (6x)^2-1^2$","Identité $a^2-b^2 = (a-b)(a+b)$","$= (6x-1)(6x+1)$"],"f":"$a^2-b^2 = (a-b)(a+b)$"},
    # A-VF
    {"lvl":2,"type":"vf","q":"$(5x)^2 = 5x^2$.","a":"Faux","options":["Vrai","Faux"],"steps":["$(5x)^2 = 5^2 \\times x^2 = 25x^2$","$5x^2$ signifie $5 \\times x^2$","$25x^2 \\neq 5x^2$"],"f":"$(ab)^2 = a^2 b^2$"},
    # I-QCM
    {"lvl":2,"q":"Un lotissement carré fait $99$ m de côté. Calcule son aire via $(100-1)^2$.","a":"$9\\,801$","options":["$9\\,801$","$9\\,801$","$9\\,900$","$9\\,801$"],"steps":["$(100-1)^2 = 100^2-2 \\times 100 \\times 1+1^2$","$= 10\\,000-200+1$","$= 9\\,801$ m²"],"f":"$(a-b)^2 = a^2-2ab+b^2$"},
    # I-Fill
    {"lvl":2,"type":"fill","q":"Complète : $4x^2+12x+9 = (\\text{___}x+3)^2$.","a":"2","options":[],"steps":["On cherche $a$ tel que $(ax+3)^2 = a^2x^2+6ax+9$","$a^2 = 4$ donc $a = 2$","Vérification : $6a = 12$ ✓"],"f":"$(a+b)^2 = a^2+2ab+b^2$"},
    # C-QCM
    {"lvl":2,"q":"Simplifie $\\frac{x^2-9}{x+3}$ pour $x \\neq -3$.","a":"$x-3$","options":["$x-3$","$x+3$","$x^2-3$"],"steps":["$x^2-9 = (x-3)(x+3)$","$\\frac{(x-3)(x+3)}{x+3} = x-3$","Condition : $x \\neq -3$"],"f":"$a^2-b^2 = (a-b)(a+b)$"},

    # SLOT 4
    # A-QCM
    {"lvl":2,"q":"Développe $(2x+5)^2$.","a":"$4x^2+20x+25$","options":["$4x^2+20x+25$","$4x^2+10x+25$","$2x^2+20x+25$"],"steps":["$(2x+5)^2 = (2x)^2+2 \\times 2x \\times 5+5^2$","$= 4x^2+20x+25$"],"f":"$(a+b)^2 = a^2+2ab+b^2$"},
    # A-VF
    {"lvl":2,"type":"vf","q":"$49x^2-64 = (7x-8)(7x+8)$.","a":"Vrai","options":["Vrai","Faux"],"steps":["$49x^2 = (7x)^2$, $64 = 8^2$","$a^2-b^2 = (a-b)(a+b)$","$(7x-8)(7x+8)$ ✓"],"f":"$a^2-b^2 = (a-b)(a+b)$"},
    # I-QCM
    {"lvl":2,"q":"Développe et réduis $(a+b)^2+(a-b)^2$.","a":"$2a^2+2b^2$","options":["$2a^2+2b^2$","$2a^2$","$4ab$"],"steps":["$(a+b)^2 = a^2+2ab+b^2$","$(a-b)^2 = a^2-2ab+b^2$","Somme : $2a^2+2b^2$ (les $2ab$ s'annulent)"],"f":"$(a+b)^2+(a-b)^2 = 2a^2+2b^2$"},
    # I-Fill
    {"lvl":2,"type":"fill","q":"Un champ carré fait $103$ m de côté. Via $(100+3)^2$, son aire vaut ___ m².","a":"10609","options":[],"steps":["$(100+3)^2 = 100^2+2 \\times 100 \\times 3+3^2$","$= 10\\,000+600+9$","$= 10\\,609$ m²"],"f":"$(a+b)^2 = a^2+2ab+b^2$"},
    # C-QCM
    {"lvl":2,"q":"Montre que $(n+1)^2-n^2$ est toujours impair. Quelle est sa valeur simplifiée ?","a":"$2n+1$","options":["$2n+1$","$2n$","$n^2+1$"],"steps":["$(n+1)^2 = n^2+2n+1$","$(n+1)^2-n^2 = n^2+2n+1-n^2 = 2n+1$","$2n+1$ est impair pour tout entier $n$"],"f":"$(a+b)^2-a^2 = 2ab+b^2$"},
]

# ─────────────────────────────────────────────────────────────────────
# 2. ÉQUATIONS
# ─────────────────────────────────────────────────────────────────────
NEW_EXOS["Équations"] = [
    # SLOT 1
    {"lvl":1,"q":"Résous $(x-3)(x+5)=0$.","a":"$x=3$ ou $x=-5$","options":["$x=3$ ou $x=-5$","$x=-3$ ou $x=5$","$x=15$"],"steps":["Équation produit : $ab=0 \\Leftrightarrow a=0$ ou $b=0$","$x-3=0 \\Rightarrow x=3$","$x+5=0 \\Rightarrow x=-5$"],"f":"$ab=0 \\Leftrightarrow a=0$ ou $b=0$"},
    {"lvl":1,"q":"Résous $x^2=25$.","a":"$x=5$ ou $x=-5$","options":["$x=5$ ou $x=-5$","$x=5$","$x=25$"],"steps":["$x^2=25$ signifie $x^2-25=0$","$(x-5)(x+5)=0$","$x=5$ ou $x=-5$"],"f":"$x^2=a \\Leftrightarrow x=\\sqrt{a}$ ou $x=-\\sqrt{a}$"},
    {"lvl":1,"type":"vf","q":"L'équation $x^2=-9$ a deux solutions.","a":"Faux","options":["Vrai","Faux"],"steps":["$x^2$ est toujours $\\geq 0$ pour tout réel $x$","$x^2 = -9$ est impossible","Aucune solution"],"f":"$x^2 \\geq 0$ pour tout $x \\in \\mathbb{R}$"},
    {"lvl":1,"q":"Résous $(2x-6)(x+1)=0$.","a":"$x=3$ ou $x=-1$","options":["$x=3$ ou $x=-1$","$x=6$ ou $x=-1$","$x=3$ ou $x=1$"],"steps":["$2x-6=0 \\Rightarrow 2x=6 \\Rightarrow x=3$","$x+1=0 \\Rightarrow x=-1$","Deux solutions : $x=3$ ou $x=-1$"],"f":"$ab=0 \\Leftrightarrow a=0$ ou $b=0$"},
    {"lvl":1,"type":"fill","q":"Les solutions de $(3x-9)(x+4)=0$ sont $x=3$ et $x=$ ___.","a":"-4","options":[],"steps":["$3x-9=0 \\Rightarrow x=3$","$x+4=0 \\Rightarrow x=-4$","Deuxième solution : $x=-4$"],"f":"$ab=0 \\Leftrightarrow a=0$ ou $b=0$"},

    # SLOT 2
    {"lvl":1,"q":"Résous $x^2-x-6=0$.","a":"$x=3$ ou $x=-2$","options":["$x=3$ ou $x=-2$","$x=6$ ou $x=-1$","$x=2$ ou $x=-3$"],"steps":["On cherche deux nombres de produit $-6$ et somme $-1$","$3 \\times (-2) = -6$ et $3+(-2)=1$... non","$(x-3)(x+2)=0$ → $x=3$ ou $x=-2$"],"f":"$x^2+bx+c = (x-x_1)(x-x_2)$"},
    {"lvl":1,"type":"vf","q":"Si $ab=0$, alors $a=0$ ET $b=0$.","a":"Faux","options":["Vrai","Faux"],"steps":["$ab=0$ signifie $a=0$ OU $b=0$ (ou les deux)","Contre-exemple : $a=0$, $b=7$ → $ab=0$","C'est un « ou », pas un « et »"],"f":"$ab=0 \\Leftrightarrow a=0$ ou $b=0$"},
    {"lvl":1,"q":"Au basket, la hauteur d'un ballon est nulle quand $t^2-5t+6=0$. À quels instants le ballon touche-t-il le sol ?","a":"$t=2$ ou $t=3$","options":["$t=2$ ou $t=3$","$t=1$ ou $t=6$","$t=2$ ou $t=6$"],"steps":["$t^2-5t+6 = (t-2)(t-3)=0$","$t-2=0 \\Rightarrow t=2$ s","$t-3=0 \\Rightarrow t=3$ s"],"f":"$ab=0 \\Leftrightarrow a=0$ ou $b=0$"},
    {"lvl":1,"type":"fill","q":"Si $x^2-7x+12=0$, la somme des solutions est ___.","a":"7","options":[],"steps":["$(x-3)(x-4)=0$ → $x=3$ ou $x=4$","Somme : $3+4=7$","Remarque : c'est l'opposé du coefficient de $x$"],"f":"Somme des racines $= -b/a$"},
    {"lvl":1,"q":"Résous $2x^2-8=0$.","a":"$x=2$ ou $x=-2$","options":["$x=2$ ou $x=-2$","$x=4$ ou $x=-4$","$x=2$"],"steps":["$2x^2=8 \\Rightarrow x^2=4$","$x=\\sqrt{4}=2$ ou $x=-\\sqrt{4}=-2$","Deux solutions"],"f":"$x^2=a \\Leftrightarrow x=\\pm\\sqrt{a}$"},

    # SLOT 3
    {"lvl":2,"q":"Résous $x^2+x-12=0$.","a":"$x=3$ ou $x=-4$","options":["$x=3$ ou $x=-4$","$x=4$ ou $x=-3$","$x=12$ ou $x=-1$"],"steps":["On cherche deux nombres de produit $-12$ et somme $1$","$4 \\times (-3) = -12$ et $4+(-3) = 1$ ✓","$(x+4)(x-3)=0$ → $x=-4$ ou $x=3$"],"f":"$x^2+bx+c = (x-x_1)(x-x_2)$"},
    {"lvl":2,"type":"vf","q":"L'équation $(x-1)(x+1)(x-2)=0$ a exactement 3 solutions.","a":"Vrai","options":["Vrai","Faux"],"steps":["$x-1=0 \\Rightarrow x=1$","$x+1=0 \\Rightarrow x=-1$","$x-2=0 \\Rightarrow x=2$ → 3 solutions distinctes"],"f":"$ab=0 \\Leftrightarrow a=0$ ou $b=0$"},
    {"lvl":2,"q":"Le carré de $(x+1)$ vaut $36$. Toutes les valeurs de $x$ ?","a":"$x=5$ ou $x=-7$","options":["$x=5$ ou $x=-7$","$x=5$","$x=35$"],"steps":["$(x+1)^2=36 \\Rightarrow x+1=6$ ou $x+1=-6$","$x=5$ ou $x=-7$","Deux solutions"],"f":"$X^2=a \\Leftrightarrow X=\\pm\\sqrt{a}$"},
    {"lvl":2,"type":"fill","q":"Un ingénieur modélise la résistance par $x^2-2x-3=0$. Les solutions sont $x=3$ et $x=$ ___.","a":"-1","options":[],"steps":["$x^2-2x-3 = (x-3)(x+1)=0$","$x=3$ ou $x=-1$","En contexte physique, on garde souvent $x=3 > 0$"],"f":"$ab=0 \\Leftrightarrow a=0$ ou $b=0$"},
    {"lvl":2,"q":"Un jardin rectangulaire a un périmètre de $26$ m et une aire de $42$ m². Quelles sont ses dimensions ?","a":"$l=6,\\ L=7$","options":["$l=6,\\ L=7$","$l=5,\\ L=8$","$l=4,\\ L=9$"],"steps":["Demi-périmètre : $L+l=13$, aire : $Ll=42$","$L$ et $l$ sont racines de $t^2-13t+42=0$","$(t-6)(t-7)=0$ → $l=6$, $L=7$"],"f":"$ab=0 \\Leftrightarrow a=0$ ou $b=0$"},

    # SLOT 4
    {"lvl":2,"q":"Résous $x^2-9x+20=0$.","a":"$x=4$ ou $x=5$","options":["$x=4$ ou $x=5$","$x=2$ ou $x=10$","$x=-4$ ou $x=-5$"],"steps":["Produit $20$, somme $9$ : $4 \\times 5 = 20$, $4+5=9$ ✓","$(x-4)(x-5)=0$","$x=4$ ou $x=5$"],"f":"$x^2+bx+c = (x-x_1)(x-x_2)$"},
    {"lvl":2,"type":"vf","q":"L'équation $x^2=0$ a exactement une solution.","a":"Vrai","options":["Vrai","Faux"],"steps":["$x^2=0 \\Rightarrow x=0$","C'est une racine double","Une seule valeur : $x=0$"],"f":"$x^2=0 \\Leftrightarrow x=0$"},
    {"lvl":2,"q":"Un stylo et deux cahiers coûtent $7$ €. Deux stylos et un cahier coûtent $8$ €. Quel est le prix d'un stylo ?","a":"$3$ €","options":["$3$ €","$2$ €","$4$ €"],"steps":["$s+2c=7$ et $2s+c=8$","Soustraction : $s-c=1$ → $c=s-1$","$s+2(s-1)=7$ → $3s=9$ → $s=3$ €"],"f":"Mise en équation → résolution"},
    {"lvl":2,"type":"fill","q":"Résous $x^2-5x=0$. Les solutions sont $x=0$ et $x=$ ___.","a":"5","options":[],"steps":["$x^2-5x = x(x-5) = 0$","$x=0$ ou $x-5=0$","$x=0$ ou $x=5$"],"f":"$ab=0 \\Leftrightarrow a=0$ ou $b=0$"},
    {"lvl":2,"q":"Résous $(x^2-4)(x+3)=0$.","a":"$x=2$, $x=-2$ ou $x=-3$","options":["$x=2$, $x=-2$ ou $x=-3$","$x=2$ ou $x=-3$","$x=4$ ou $x=-3$"],"steps":["$x^2-4=0 \\Rightarrow x=2$ ou $x=-2$","$x+3=0 \\Rightarrow x=-3$","Trois solutions : $2$, $-2$, $-3$"],"f":"$ab=0 \\Leftrightarrow a=0$ ou $b=0$"},
]

# ─────────────────────────────────────────────────────────────────────
# 3. FONCTIONS
# ─────────────────────────────────────────────────────────────────────
NEW_EXOS["Fonctions"] = [
    # SLOT 1
    {"lvl":1,"q":"$f(x)=3x-2$. Calcule $f(4)$.","a":"$10$","options":["$10$","$12$","$14$"],"steps":["$f(4) = 3 \\times 4-2$","$= 12-2$","$= 10$"],"f":"$f(x)=ax+b$ : fonction affine"},
    {"lvl":1,"q":"$f(x)=-x+7$. Calcule $f(0)$.","a":"$7$","options":["$7$","$0$","$-7$"],"steps":["$f(0) = -0+7$","$= 7$","C'est l'ordonnée à l'origine"],"f":"$f(0) = b$ pour $f(x)=ax+b$"},
    {"lvl":1,"type":"vf","q":"Si $f(2)=5$, alors $2$ est l'image de $5$ par $f$.","a":"Faux","options":["Vrai","Faux"],"steps":["$f(2)=5$ signifie que $5$ est l'image de $2$","Et $2$ est un antécédent de $5$","L'énoncé inverse image et antécédent"],"f":"$f(a)=b$ : $b$ image de $a$, $a$ antécédent de $b$"},
    {"lvl":1,"q":"$f(x)=2x+1$. La fonction est-elle croissante ou décroissante ?","a":"Croissante","options":["Croissante","Décroissante","Constante"],"steps":["Le coefficient directeur est $a=2 > 0$","Quand $a > 0$, la fonction affine est croissante","$f$ est donc croissante"],"f":"$f(x)=ax+b$ : croissante si $a>0$, décroissante si $a<0$"},
    {"lvl":1,"type":"fill","q":"$f(x)=2x-6$. La fonction s'annule pour $x=$ ___.","a":"3","options":[],"steps":["$f(x)=0 \\Leftrightarrow 2x-6=0$","$2x=6$","$x=3$"],"f":"$f(x)=0$ : résoudre $ax+b=0$"},

    # SLOT 2
    {"lvl":1,"q":"$f(x)=4x-1$. Calcule $f(-2)$.","a":"$-9$","options":["$-9$","$-7$","$7$"],"steps":["$f(-2) = 4 \\times (-2)-1$","$= -8-1$","$= -9$"],"f":"$f(x)=ax+b$ : fonction affine"},
    {"lvl":1,"type":"vf","q":"Une fonction peut associer deux images différentes au même nombre.","a":"Faux","options":["Vrai","Faux"],"steps":["Par définition, une fonction associe à chaque nombre UNE SEULE image","Un nombre a exactement une image","Mais un même $y$ peut avoir plusieurs antécédents"],"f":"Définition d'une fonction"},
    {"lvl":1,"q":"Un forfait téléphone coûte $f(x)=3x+5$ € pour $x$ Go. Quel coût pour $4$ Go ?","a":"$17$ €","options":["$17$ €","$12$ €","$20$ €"],"steps":["$f(4) = 3 \\times 4+5$","$= 12+5$","$= 17$ €"],"f":"$f(x)=ax+b$ : fonction affine"},
    {"lvl":1,"type":"fill","q":"$f(x)=\\frac{1}{2}x+3$. Pour $f(x)=0$, on trouve $x=$ ___.","a":"-6","options":[],"steps":["$\\frac{1}{2}x+3=0$","$\\frac{1}{2}x=-3$","$x=-6$"],"f":"$f(x)=0$ : résoudre $ax+b=0$"},
    {"lvl":1,"q":"Une plante mesure $2$ cm au jour $0$ et $8$ cm au jour $3$. Quel est son taux de croissance quotidien (en cm/jour) ?","a":"$2$","options":["$2$","$3$","$6$"],"steps":["Croissance totale : $8-2=6$ cm","En $3$ jours → $6 \\div 3 = 2$ cm/jour","Taux = coefficient directeur $a=2$"],"f":"$a = \\frac{f(x_2)-f(x_1)}{x_2-x_1}$"},

    # SLOT 3
    {"lvl":2,"q":"$f(x)=ax+b$ passe par $(1\\,;\\,3)$ et $(3\\,;\\,7)$. Trouve $a$ et $b$.","a":"$a=2,\\ b=1$","options":["$a=2,\\ b=1$","$a=3,\\ b=0$","$a=2,\\ b=-1$"],"steps":["$a = \\frac{7-3}{3-1} = \\frac{4}{2} = 2$","$f(1)=3$ : $2 \\times 1+b=3$ → $b=1$","$f(x)=2x+1$"],"f":"$a = \\frac{y_2-y_1}{x_2-x_1}$"},
    {"lvl":2,"type":"vf","q":"La fonction $f(x)=x^2$ est croissante sur $\\mathbb{R}$.","a":"Faux","options":["Vrai","Faux"],"steps":["$f(-2)=4$ et $f(1)=1$ : $-2 < 1$ mais $f(-2) > f(1)$","$f$ est décroissante sur $]-\\infty\\,;\\,0]$","Et croissante sur $[0\\,;\\,+\\infty[$"],"f":"$f(x)=x^2$ : décroissante puis croissante"},
    {"lvl":2,"q":"$f(x)=x^2-4$. Quels sont les antécédents de $0$ ?","a":"$x=2$ et $x=-2$","options":["$x=2$ et $x=-2$","$x=4$","$x=2$"],"steps":["$f(x)=0 \\Leftrightarrow x^2-4=0$","$x^2=4$","$x=2$ ou $x=-2$"],"f":"Antécédent : résoudre $f(x)=k$"},
    {"lvl":2,"type":"fill","q":"$f(x)=x^2-4x+3$. $f(1)=$ ___.","a":"0","options":[],"steps":["$f(1) = 1^2-4 \\times 1+3$","$= 1-4+3$","$= 0$"],"f":"Calculer une image : remplacer $x$"},
    {"lvl":2,"q":"Deux entreprises : $f(x)=2x+1$ et $g(x)=x+4$ (en €). À partir de quelle quantité $f$ est-elle plus chère ?","a":"$x > 3$","options":["$x > 3$","$x > 2$","$x > 5$"],"steps":["$f(x) > g(x) \\Leftrightarrow 2x+1 > x+4$","$x > 3$","Pour $x > 3$, l'entreprise $f$ est plus chère"],"f":"Comparer : résoudre $f(x) > g(x)$"},

    # SLOT 4
    {"lvl":2,"q":"$f(x)=-2x+8$. Pour quelle valeur de $x$ a-t-on $f(x)=0$ ?","a":"$x=4$","options":["$x=4$","$x=-4$","$x=8$"],"steps":["$-2x+8=0$","$-2x=-8$","$x=4$"],"f":"$f(x)=0$ : résoudre $ax+b=0$"},
    {"lvl":2,"type":"vf","q":"Si $f(x)=3x-6$, alors $f$ coupe l'axe des abscisses en $x=2$.","a":"Vrai","options":["Vrai","Faux"],"steps":["Couper l'axe des abscisses = $f(x)=0$","$3x-6=0 \\Rightarrow x=2$","Le point $(2\\,;\\,0)$ est sur la droite ✓"],"f":"$f(x)=0$ : intersection avec l'axe $Ox$"},
    {"lvl":2,"q":"La vitesse d'un cycliste est $v(t)=24-3t$ km/h. À quel moment s'arrête-t-il ?","a":"$t=8$ h","options":["$t=8$ h","$t=6$ h","$t=24$ h"],"steps":["Arrêt quand $v(t)=0$","$24-3t=0 \\Rightarrow t=8$","Le cycliste s'arrête après $8$ h"],"f":"$f(x)=0$ : résoudre $ax+b=0$"},
    {"lvl":2,"type":"fill","q":"$f(x)=ax+b$ passe par $(0\\,;\\,-3)$ et $(2\\,;\\,5)$. Le coefficient directeur $a=$ ___.","a":"4","options":[],"steps":["$a = \\frac{5-(-3)}{2-0} = \\frac{8}{2}$","$a = 4$","$f(x)=4x-3$"],"f":"$a = \\frac{y_2-y_1}{x_2-x_1}$"},
    {"lvl":2,"q":"$f(x)=x^2-x-2$. Factorise et trouve les racines.","a":"$x=2$ ou $x=-1$","options":["$x=2$ ou $x=-1$","$x=1$ ou $x=-2$","$x=2$ ou $x=1$"],"steps":["On cherche $(x-a)(x-b)$ avec $ab=-2$ et $a+b=1$","$2 \\times (-1) = -2$ ✓, $2+(-1)=1$ ✓","$f(x)=(x-2)(x+1)=0$ → $x=2$ ou $x=-1$"],"f":"$x^2+bx+c = (x-x_1)(x-x_2)$"},
]

# ─────────────────────────────────────────────────────────────────────
# 4. THÉORÈME DE THALÈS
# ─────────────────────────────────────────────────────────────────────
NEW_EXOS["Théorème de Thalès"] = [
    # SLOT 1
    {"lvl":1,"q":"$(MN)\\parallel(BC)$. $AM=3$, $AB=9$, $MN=5$. Calcule $BC$.","a":"$15$","options":["$15$","$10$","$12$"],"steps":["Thalès : $\\frac{AM}{AB}=\\frac{MN}{BC}$","$\\frac{3}{9}=\\frac{5}{BC}$","$BC = \\frac{5 \\times 9}{3} = 15$"],"f":"$\\frac{AM}{AB}=\\frac{AN}{AC}=\\frac{MN}{BC}$"},
    {"lvl":1,"q":"$(MN)\\parallel(BC)$. $AM=4$, $MB=2$, $MN=6$. Calcule $BC$.","a":"$9$","options":["$9$","$8$","$12$"],"steps":["$AB = AM+MB = 4+2 = 6$","$\\frac{AM}{AB}=\\frac{MN}{BC}$ → $\\frac{4}{6}=\\frac{6}{BC}$","$BC = \\frac{6 \\times 6}{4} = 9$"],"f":"$\\frac{AM}{AB}=\\frac{AN}{AC}=\\frac{MN}{BC}$"},
    {"lvl":1,"type":"vf","q":"Le théorème de Thalès nécessite que deux droites soient parallèles.","a":"Vrai","options":["Vrai","Faux"],"steps":["Thalès s'applique avec deux droites sécantes coupées par deux parallèles","Sans parallélisme, les rapports ne sont pas égaux","Condition indispensable"],"f":"Condition : $(MN) \\parallel (BC)$"},
    {"lvl":1,"q":"$(MN)\\parallel(BC)$. $AM=5$, $MB=3$, $BC=16$. Calcule $MN$.","a":"$10$","options":["$10$","$8$","$12$"],"steps":["$AB = 5+3 = 8$","$\\frac{AM}{AB}=\\frac{MN}{BC}$ → $\\frac{5}{8}=\\frac{MN}{16}$","$MN = \\frac{5 \\times 16}{8} = 10$"],"f":"$\\frac{AM}{AB}=\\frac{MN}{BC}$"},
    {"lvl":1,"type":"fill","q":"$(MN)\\parallel(BC)$, $\\frac{AM}{AB}=\\frac{AN}{AC}=\\frac{2}{5}$, $BC=10$. Alors $MN=$ ___.","a":"4","options":[],"steps":["$\\frac{MN}{BC}=\\frac{2}{5}$","$MN = \\frac{2 \\times 10}{5}$","$MN = 4$"],"f":"$\\frac{AM}{AB}=\\frac{MN}{BC}$"},

    # SLOT 2
    {"lvl":1,"q":"$(MN)\\parallel(BC)$. $AM=6$, $AB=10$, $AN=4{,}5$. Calcule $AC$.","a":"$7{,}5$","options":["$7{,}5$","$8$","$6{,}5$"],"steps":["$\\frac{AM}{AB}=\\frac{AN}{AC}$ → $\\frac{6}{10}=\\frac{4{,}5}{AC}$","$AC = \\frac{4{,}5 \\times 10}{6}$","$AC = 7{,}5$"],"f":"$\\frac{AM}{AB}=\\frac{AN}{AC}$"},
    {"lvl":1,"type":"vf","q":"La réciproque de Thalès permet de prouver que deux droites sont parallèles.","a":"Vrai","options":["Vrai","Faux"],"steps":["Si les rapports sont égaux ET les points dans le bon ordre","Alors on peut conclure au parallélisme","C'est la réciproque de Thalès"],"f":"Réciproque : rapports égaux + ordre → parallélisme"},
    {"lvl":1,"q":"Un poteau de $3$ m projette une ombre de $2$ m. Un arbre projette une ombre de $5$ m. Quelle est la hauteur de l'arbre ?","a":"$7{,}5$ m","options":["$7{,}5$ m","$6$ m","$10$ m"],"steps":["Rayons parallèles → Thalès : $\\frac{3}{h}=\\frac{2}{5}$","$h = \\frac{3 \\times 5}{2}$","$h = 7{,}5$ m"],"f":"$\\frac{AM}{AB}=\\frac{MN}{BC}$"},
    {"lvl":1,"type":"fill","q":"Un élève écrit $\\frac{AM}{AB}=\\frac{AN}{CA}$. L'erreur est dans le rapport $\\frac{AN}{CA}$ : il fallait écrire $\\frac{AN}{\\text{___}}$.","a":"AC","options":[],"steps":["Les rapports doivent être dans le même sens","$\\frac{AM}{AB}$ va du petit vers le grand","Il faut $\\frac{AN}{AC}$ (pas $CA$)"],"f":"$\\frac{AM}{AB}=\\frac{AN}{AC}$ (même sens)"},
    {"lvl":1,"q":"Deux triangles semblables : côtés $6,8,10$ et $3,4,5$. Quel est le rapport de réduction ?","a":"$\\frac{1}{2}$","options":["$\\frac{1}{2}$","$\\frac{1}{3}$","$2$"],"steps":["$\\frac{3}{6}=\\frac{4}{8}=\\frac{5}{10}=\\frac{1}{2}$","Tous les rapports sont égaux","Rapport de réduction : $\\frac{1}{2}$"],"f":"Rapport de similitude $k = \\frac{\\text{petit}}{\\text{grand}}$"},

    # SLOT 3
    {"lvl":2,"q":"Sur un plan d'architecte, $(MN)\\parallel(BC)$ avec $MN=4$ cm, $BC=7$ cm et $MB=3$ cm. Trouve $AM$.","a":"$4$","options":["$4$","$3$","$5$"],"steps":["$\\frac{AM}{AM+3}=\\frac{4}{7}$","$7 \\times AM = 4(AM+3) = 4AM+12$","$3AM = 12$ → $AM = 4$ cm"],"f":"$\\frac{AM}{AB}=\\frac{MN}{BC}$"},
    {"lvl":2,"type":"vf","q":"Si $\\frac{AM}{AB}=\\frac{AN}{AC}$ mais que les points ne sont pas dans le bon ordre, on ne peut pas conclure au parallélisme.","a":"Vrai","options":["Vrai","Faux"],"steps":["La réciproque de Thalès exige deux conditions","1) Rapports égaux","2) Points dans le même ordre sur les droites"],"f":"Réciproque : rapports égaux + ordre"},
    {"lvl":2,"q":"$(MN)\\parallel(BC)$. Rapport $\\frac{AM}{MB}=\\frac{2}{3}$. Si $BC=15$, calcule $MN$.","a":"$6$","options":["$6$","$9$","$10$"],"steps":["$\\frac{AM}{MB}=\\frac{2}{3}$ → $\\frac{AM}{AB}=\\frac{2}{5}$","$\\frac{MN}{BC}=\\frac{2}{5}$","$MN = \\frac{2 \\times 15}{5} = 6$"],"f":"$\\frac{AM}{AB}=\\frac{MN}{BC}$"},
    {"lvl":2,"type":"fill","q":"$(MN)\\parallel(BC)$. Aire de $AMN=4$ cm², aire de $ABC=9$ cm². Le rapport $\\frac{AM}{AB}=$ ___.","a":"2/3","options":[],"steps":["Rapport des aires $= k^2 = \\frac{4}{9}$","$k = \\sqrt{\\frac{4}{9}} = \\frac{2}{3}$","$\\frac{AM}{AB} = \\frac{2}{3}$"],"f":"Rapport des aires $= k^2$"},
    {"lvl":2,"q":"Configuration papillon : $O$ est l'intersection de $(AC)$ et $(BD)$. $OA=3$, $OC=9$, $OB=4$, $OD=12$. Les droites $(AB)$ et $(CD)$ sont-elles parallèles ?","a":"Oui, car $\\frac{OA}{OC}=\\frac{OB}{OD}=\\frac{1}{3}$","options":["Oui, car $\\frac{OA}{OC}=\\frac{OB}{OD}=\\frac{1}{3}$","Non, les rapports sont différents","On ne peut pas conclure"],"steps":["$\\frac{OA}{OC}=\\frac{3}{9}=\\frac{1}{3}$","$\\frac{OB}{OD}=\\frac{4}{12}=\\frac{1}{3}$","Rapports égaux + ordre ✓ → $(AB)\\parallel(CD)$"],"f":"Réciproque de Thalès (config. papillon)"},

    # SLOT 4
    {"lvl":2,"q":"Un pylône de $9$ m est vu depuis un point $A$. Un bâton de $1{,}5$ m placé entre $A$ et le pylône cache exactement le sommet. Le bâton est à $3$ m de $A$, le pylône à $18$ m. Vérifie.","a":"$\\frac{1{,}5}{9}=\\frac{3}{18}=\\frac{1}{6}$ ✓","options":["$\\frac{1{,}5}{9}=\\frac{3}{18}=\\frac{1}{6}$ ✓","Les rapports sont différents","$\\frac{1}{3}$"],"steps":["$\\frac{1{,}5}{9}=\\frac{1}{6}$","$\\frac{3}{18}=\\frac{1}{6}$","Rapports égaux → alignement confirmé par Thalès"],"f":"$\\frac{AM}{AB}=\\frac{AN}{AC}=\\frac{MN}{BC}$"},
    {"lvl":2,"type":"vf","q":"Si le rapport de similitude entre deux triangles est $\\frac{2}{3}$, le rapport des périmètres est aussi $\\frac{2}{3}$.","a":"Vrai","options":["Vrai","Faux"],"steps":["Le périmètre est une somme de longueurs","Si chaque côté est multiplié par $k$, le périmètre aussi","Rapport des périmètres = rapport de similitude $k$"],"f":"Rapport des périmètres $= k$"},
    {"lvl":2,"q":"Deux sécantes coupées par deux parallèles : $AE=3$, $AB=9$, $AD=2$, $AC=6$. Calcule $\\frac{ED}{BC}$.","a":"$\\frac{1}{3}$","options":["$\\frac{1}{3}$","$\\frac{1}{2}$","$\\frac{2}{3}$"],"steps":["$\\frac{AE}{AB}=\\frac{3}{9}=\\frac{1}{3}$","$\\frac{AD}{AC}=\\frac{2}{6}=\\frac{1}{3}$ ✓","$\\frac{ED}{BC}=\\frac{1}{3}$ par Thalès"],"f":"$\\frac{AM}{AB}=\\frac{AN}{AC}=\\frac{MN}{BC}$"},
    {"lvl":2,"type":"fill","q":"$(MN)\\parallel(BC)$, $AM=7$, $AB=21$. Le rapport $\\frac{AM}{AB}=$ ___ (fraction irréductible).","a":"1/3","options":[],"steps":["$\\frac{AM}{AB}=\\frac{7}{21}$","$= \\frac{1}{3}$","Fraction irréductible"],"f":"$\\frac{AM}{AB}=\\frac{MN}{BC}$"},
    {"lvl":2,"q":"$AE=5$, $AB=15$, $AD=4$, $AC=12$. $(ED)$ est-elle parallèle à $(BC)$ ?","a":"Oui, car $\\frac{AE}{AB}=\\frac{AD}{AC}=\\frac{1}{3}$","options":["Oui, car $\\frac{AE}{AB}=\\frac{AD}{AC}=\\frac{1}{3}$","Non, les rapports sont différents","On ne peut pas conclure"],"steps":["$\\frac{AE}{AB}=\\frac{5}{15}=\\frac{1}{3}$","$\\frac{AD}{AC}=\\frac{4}{12}=\\frac{1}{3}$","Rapports égaux + même ordre → $(ED)\\parallel(BC)$"],"f":"Réciproque de Thalès"},
]

# ─────────────────────────────────────────────────────────────────────
# 5. TRIGONOMÉTRIE
# ─────────────────────────────────────────────────────────────────────
NEW_EXOS["Trigonométrie"] = [
    # SLOT 1
    {"lvl":1,"q":"Triangle rectangle en $B$, $AB=3$, $AC=5$ (hyp.). Calcule $\\cos(\\hat{A})$.","a":"$\\frac{3}{5}$","options":["$\\frac{3}{5}$","$\\frac{4}{5}$","$\\frac{3}{4}$"],"steps":["$\\cos(\\hat{A}) = \\frac{\\text{adjacent}}{\\text{hypoténuse}}$","Côté adjacent à $\\hat{A}$ : $AB=3$, hypoténuse : $AC=5$","$\\cos(\\hat{A}) = \\frac{3}{5}$"],"f":"$\\cos(\\alpha) = \\frac{\\text{adjacent}}{\\text{hypoténuse}}$"},
    {"lvl":1,"q":"Triangle rectangle en $B$, $AB=4$, $AC=5$. Calcule $\\sin(\\hat{A})$.","a":"$\\frac{3}{5}$","options":["$\\frac{3}{5}$","$\\frac{4}{5}$","$\\frac{3}{4}$"],"steps":["$BC = \\sqrt{5^2-4^2} = \\sqrt{9} = 3$","$\\sin(\\hat{A}) = \\frac{\\text{opposé}}{\\text{hypoténuse}} = \\frac{BC}{AC}$","$\\sin(\\hat{A}) = \\frac{3}{5}$"],"f":"$\\sin(\\alpha) = \\frac{\\text{opposé}}{\\text{hypoténuse}}$"},
    {"lvl":1,"type":"vf","q":"$\\cos^2(\\alpha)+\\sin^2(\\alpha)=1$ pour tout angle $\\alpha$.","a":"Vrai","options":["Vrai","Faux"],"steps":["C'est l'identité fondamentale de la trigonométrie","Elle découle du théorème de Pythagore","$\\left(\\frac{a}{c}\\right)^2+\\left(\\frac{b}{c}\\right)^2 = \\frac{a^2+b^2}{c^2} = 1$"],"f":"$\\cos^2(\\alpha)+\\sin^2(\\alpha)=1$"},
    {"lvl":1,"q":"Triangle rectangle en $B$, $AB=3$, $BC=4$, $AC=5$. Calcule $\\tan(\\hat{A})$.","a":"$\\frac{4}{3}$","options":["$\\frac{4}{3}$","$\\frac{3}{4}$","$\\frac{3}{5}$"],"steps":["$\\tan(\\hat{A}) = \\frac{\\text{opposé}}{\\text{adjacent}}$","Opposé à $\\hat{A}$ : $BC=4$, adjacent : $AB=3$","$\\tan(\\hat{A}) = \\frac{4}{3}$"],"f":"$\\tan(\\alpha) = \\frac{\\text{opposé}}{\\text{adjacent}}$"},
    {"lvl":1,"type":"fill","q":"Dans un triangle rectangle, si l'hypoténuse vaut $10$ et $\\sin(\\alpha)=0{,}6$, le côté opposé vaut ___.","a":"6","options":[],"steps":["$\\sin(\\alpha) = \\frac{\\text{opposé}}{\\text{hypoténuse}}$","$\\text{opposé} = \\sin(\\alpha) \\times \\text{hypoténuse}$","$= 0{,}6 \\times 10 = 6$"],"f":"$\\sin(\\alpha) = \\frac{\\text{opposé}}{\\text{hypoténuse}}$"},

    # SLOT 2
    {"lvl":1,"q":"Une rampe de $10$ m forme un angle $\\hat{A}$ avec le sol, $\\cos(\\hat{A})=0{,}8$. Quelle est la longueur au sol ?","a":"$8$","options":["$8$","$6$","$10$"],"steps":["$\\cos(\\hat{A}) = \\frac{\\text{adjacent}}{\\text{hypoténuse}}$","$\\text{adjacent} = 0{,}8 \\times 10$","$= 8$ m"],"f":"$\\cos(\\alpha) = \\frac{\\text{adjacent}}{\\text{hypoténuse}}$"},
    {"lvl":1,"type":"vf","q":"$\\sin(\\alpha) = \\frac{\\text{adjacent}}{\\text{hypoténuse}}$.","a":"Faux","options":["Vrai","Faux"],"steps":["C'est la définition du COSINUS","$\\sin(\\alpha) = \\frac{\\text{opposé}}{\\text{hypoténuse}}$","Confusion fréquente au Brevet"],"f":"$\\sin(\\alpha) = \\frac{\\text{opposé}}{\\text{hypoténuse}}$"},
    {"lvl":1,"q":"$\\sin(\\hat{A})=0{,}5$, hyp. $AC=14$. Calcule le côté opposé $BC$.","a":"$7$","options":["$7$","$14$","$12$"],"steps":["$\\sin(\\hat{A}) = \\frac{BC}{AC}$","$BC = 0{,}5 \\times 14$","$BC = 7$"],"f":"$\\sin(\\alpha) = \\frac{\\text{opposé}}{\\text{hypoténuse}}$"},
    {"lvl":1,"type":"fill","q":"$\\tan(\\alpha) = \\frac{\\sin(\\alpha)}{\\text{___}}$.","a":"cos(α)","options":[],"steps":["$\\tan(\\alpha) = \\frac{\\sin(\\alpha)}{\\cos(\\alpha)}$","C'est une relation fondamentale","$\\frac{\\text{opp}/\\text{hyp}}{\\text{adj}/\\text{hyp}} = \\frac{\\text{opp}}{\\text{adj}}$"],"f":"$\\tan(\\alpha) = \\frac{\\sin(\\alpha)}{\\cos(\\alpha)}$"},
    {"lvl":1,"q":"$\\tan(\\hat{A})=\\frac{3}{4}$, $AB=8$ (adjacent). Calcule $BC$ (opposé).","a":"$6$","options":["$6$","$8$","$10$"],"steps":["$\\tan(\\hat{A}) = \\frac{BC}{AB}$","$BC = \\frac{3}{4} \\times 8$","$BC = 6$"],"f":"$\\tan(\\alpha) = \\frac{\\text{opposé}}{\\text{adjacent}}$"},

    # SLOT 3
    {"lvl":2,"q":"Un câble de $20$ m fait un angle de $60°$ avec le sol. À quelle hauteur est-il accroché ? ($\\sin 60°=\\frac{\\sqrt{3}}{2}$)","a":"$10\\sqrt{3}\\approx17{,}3$ m","options":["$10\\sqrt{3}\\approx17{,}3$ m","$10$ m","$20$ m"],"steps":["$\\sin(60°) = \\frac{h}{20}$","$h = 20 \\times \\frac{\\sqrt{3}}{2} = 10\\sqrt{3}$","$\\approx 17{,}3$ m"],"f":"$\\sin(\\alpha) = \\frac{\\text{opposé}}{\\text{hypoténuse}}$"},
    {"lvl":2,"type":"vf","q":"$\\tan(45°) = 0{,}5$.","a":"Faux","options":["Vrai","Faux"],"steps":["$\\tan(45°) = \\frac{\\sin(45°)}{\\cos(45°)} = 1$","Car $\\sin(45°) = \\cos(45°)$","$\\tan(45°) = 1 \\neq 0{,}5$"],"f":"$\\tan(45°) = 1$"},
    {"lvl":2,"q":"Depuis un point à $50$ m d'un immeuble, on voit le toit sous un angle de $45°$. Quelle est la hauteur ?","a":"$50$ m","options":["$50$ m","$25$ m","$100$ m"],"steps":["$\\tan(45°) = \\frac{h}{50}$","$\\tan(45°) = 1$","$h = 50$ m"],"f":"$\\tan(\\alpha) = \\frac{\\text{opposé}}{\\text{adjacent}}$"},
    {"lvl":2,"type":"fill","q":"Triangle rectangle en $C$, $AC=7$, $AB=25$ (hyp.). $BC=$ ___.","a":"24","options":[],"steps":["Pythagore : $BC^2 = AB^2-AC^2 = 625-49$","$BC^2 = 576$","$BC = 24$"],"f":"$a^2+b^2=c^2$ (Pythagore)"},
    {"lvl":2,"q":"$\\sin(\\hat{A})=0{,}6$. Vérifie que $\\cos(\\hat{A})=0{,}8$ via l'identité fondamentale.","a":"$\\cos(\\hat{A})=0{,}8$ et $0{,}36+0{,}64=1$ ✓","options":["$\\cos(\\hat{A})=0{,}8$ et $0{,}36+0{,}64=1$ ✓","$\\cos(\\hat{A})=0{,}4$","$\\cos(\\hat{A})=0{,}6$"],"steps":["$\\cos^2(\\hat{A}) = 1-\\sin^2(\\hat{A}) = 1-0{,}36$","$\\cos^2(\\hat{A}) = 0{,}64$","$\\cos(\\hat{A}) = 0{,}8$ (angle aigu)"],"f":"$\\cos^2(\\alpha)+\\sin^2(\\alpha)=1$"},

    # SLOT 4
    {"lvl":2,"q":"Une grue soulève une charge à $12$ m de hauteur. Le câble fait un angle $\\hat{A}$ tel que $\\sin(\\hat{A})=0{,}8$. Longueur du câble ?","a":"$15$ m","options":["$15$ m","$12$ m","$10$ m"],"steps":["$\\sin(\\hat{A}) = \\frac{12}{\\text{câble}}$","$\\text{câble} = \\frac{12}{0{,}8}$","$= 15$ m"],"f":"$\\sin(\\alpha) = \\frac{\\text{opposé}}{\\text{hypoténuse}}$"},
    {"lvl":2,"type":"vf","q":"Dans un triangle rectangle, le cosinus d'un angle aigu est toujours compris entre $0$ et $1$.","a":"Vrai","options":["Vrai","Faux"],"steps":["Le côté adjacent est plus court que l'hypoténuse","Donc $0 < \\frac{\\text{adjacent}}{\\text{hypoténuse}} < 1$","$\\cos(\\alpha) \\in ]0\\,;\\,1[$ pour un angle aigu"],"f":"$0 < \\cos(\\alpha) < 1$ pour $\\alpha$ aigu"},
    {"lvl":2,"q":"Un panneau indique une pente de $12\\%$ ($\\tan(\\alpha)=0{,}12$). Sur $100$ m de route, quel dénivelé ?","a":"$12$ m","options":["$12$ m","$1{,}2$ m","$120$ m"],"steps":["$\\tan(\\alpha) = \\frac{\\text{dénivelé}}{\\text{distance horizontale}}$","$\\text{dénivelé} = 0{,}12 \\times 100$","$= 12$ m"],"f":"$\\tan(\\alpha) = \\frac{\\text{opposé}}{\\text{adjacent}}$"},
    {"lvl":2,"type":"fill","q":"$AB=13$, $BC=5$, angle droit en $B$. $\\sin(\\hat{C})=$ ___ (fraction).","a":"12/13","options":[],"steps":["$AC = \\sqrt{13^2-... }$... Non : hyp = $AC$? Non, angle droit en $B$","$AC = \\sqrt{AB^2+BC^2} = \\sqrt{169+25}$... Hmm","$AB=13$, $BC=5$, angle droit en $B$ → hyp $= AC = \\sqrt{169+25} = \\sqrt{194}$... Recalculons: en fait $AC$ est l'hypoténuse, $AC=\\sqrt{13^2+5^2}=\\sqrt{194}$. Mais pour simplifier: opposé à $\\hat{C}$ = $AB=13$, hyp = $AC$... Non, prenons l'approche directe."],"f":"$\\sin(\\alpha) = \\frac{\\text{opposé}}{\\text{hypoténuse}}$"},
    {"lvl":2,"q":"Triangle équilatéral de côté $8$ cm. Calcule sa hauteur via $\\sin(60°)=\\frac{\\sqrt{3}}{2}$.","a":"$4\\sqrt{3}\\approx 6{,}93$ cm","options":["$4\\sqrt{3}\\approx 6{,}93$ cm","$8$ cm","$4$ cm"],"steps":["La hauteur coupe la base en deux : demi-base $= 4$ cm","$\\sin(60°) = \\frac{h}{8}$","$h = 8 \\times \\frac{\\sqrt{3}}{2} = 4\\sqrt{3} \\approx 6{,}93$ cm"],"f":"$\\sin(\\alpha) = \\frac{\\text{opposé}}{\\text{hypoténuse}}$"},
]

# Fix Trigo slot 4 fill exercise - the steps are wrong. Let me redo it properly.
# AB=13, BC=5, angle droit en B. Hypoténuse = AC = sqrt(13²+5²) = sqrt(194) - ugly.
# Let me change to a cleaner exercise.
NEW_EXOS["Trigonométrie"][18] = {"lvl":2,"type":"fill","q":"Triangle rectangle en $B$, $AB=5$, $BC=12$, $AC=13$ (hyp.). $\\sin(\\hat{A})=$ ___ (fraction).","a":"12/13","options":[],"steps":["$\\sin(\\hat{A}) = \\frac{\\text{opposé}}{\\text{hypoténuse}}$","Opposé à $\\hat{A}$ : $BC=12$, hypoténuse : $AC=13$","$\\sin(\\hat{A}) = \\frac{12}{13}$"],"f":"$\\sin(\\alpha) = \\frac{\\text{opposé}}{\\text{hypoténuse}}$"}

# ─────────────────────────────────────────────────────────────────────
# 6. STATISTIQUES
# ─────────────────────────────────────────────────────────────────────
NEW_EXOS["Statistiques"] = [
    # SLOT 1
    {"lvl":1,"q":"Notes d'un élève : $3$, $5$, $9$, $11$, $14$. Quelle est la médiane ?","a":"$9$","options":["$9$","$7$","$11$"],"steps":["$5$ valeurs classées → médiane = 3e valeur","Position : $3, 5, \\mathbf{9}, 11, 14$","Médiane $= 9$"],"f":"Médiane : valeur centrale de la série classée"},
    {"lvl":1,"q":"Notes : $12, 8, 15, 10, 18, 14$. Calcule la moyenne.","a":"$12{,}83$","options":["$12{,}83$","$13$","$11{,}5$"],"steps":["Somme : $12+8+15+10+18+14 = 77$","Effectif : $6$","Moyenne $= \\frac{77}{6} \\approx 12{,}83$"],"f":"$\\bar{x} = \\frac{\\sum x_i}{n}$"},
    {"lvl":1,"type":"vf","q":"La médiane partage toujours la série en deux groupes de même effectif.","a":"Vrai","options":["Vrai","Faux"],"steps":["Par définition, $50\\%$ des valeurs sont $\\leq$ médiane","Et $50\\%$ sont $\\geq$ médiane","C'est la propriété fondamentale de la médiane"],"f":"Médiane : $50\\%$ en dessous, $50\\%$ au-dessus"},
    {"lvl":1,"q":"Températures (°C) : $2$, $5$, $7$, $9$, $12$. Quelle est l'étendue ?","a":"$10$","options":["$10$","$7$","$12$"],"steps":["Étendue = max $-$ min","$= 12-2$","$= 10$"],"f":"Étendue $= x_{\\max}-x_{\\min}$"},
    {"lvl":1,"type":"fill","q":"Série classée : $4, 6, 9, 13$. La médiane vaut ___.","a":"7,5","options":[],"steps":["$4$ valeurs → médiane = moyenne des 2e et 3e","$\\frac{6+9}{2}$","$= 7{,}5$"],"f":"Médiane (effectif pair) : moyenne des deux valeurs centrales"},

    # SLOT 2
    {"lvl":1,"q":"Série : $3, 7, 7, 9, 11, 11, 11, 15$. Quel est le mode ?","a":"$11$","options":["$11$","$7$","$9$"],"steps":["$11$ apparaît $3$ fois (le plus fréquent)","$7$ apparaît $2$ fois","Mode $= 11$"],"f":"Mode : valeur la plus fréquente"},
    {"lvl":1,"type":"vf","q":"L'étendue mesure la dispersion de toutes les valeurs.","a":"Faux","options":["Vrai","Faux"],"steps":["L'étendue ne tient compte que du min et du max","Elle est sensible aux valeurs extrêmes","L'EIQ est un meilleur indicateur de dispersion"],"f":"Étendue $= x_{\\max}-x_{\\min}$"},
    {"lvl":1,"q":"Série classée : $1, 3, 5, 7, 9, 11, 13$. Quelle est la médiane ?","a":"$7$","options":["$7$","$5$","$9$"],"steps":["$7$ valeurs → médiane = 4e valeur","$1, 3, 5, \\mathbf{7}, 9, 11, 13$","Médiane $= 7$"],"f":"Médiane : valeur centrale"},
    {"lvl":1,"type":"fill","q":"La médiane d'une série de $20$ valeurs classées est la moyenne des ___e et 11e valeurs.","a":"10","options":[],"steps":["$20$ valeurs → effectif pair","Médiane = moyenne des $\\frac{20}{2}$e et $\\frac{20}{2}+1$e","= moyenne des 10e et 11e valeurs"],"f":"Médiane (effectif pair)"},
    {"lvl":1,"q":"Moyenne pondérée : $12$ (coeff $2$), $15$ (coeff $3$), $8$ (coeff $1$). Calcule.","a":"$13{,}17$","options":["$13{,}17$","$11{,}67$","$12{,}5$"],"steps":["$\\frac{12 \\times 2+15 \\times 3+8 \\times 1}{2+3+1}$","$= \\frac{24+45+8}{6} = \\frac{77}{6}$... Hmm recalculons","$= \\frac{24+45+8}{6} = \\frac{77}{6} \\approx 12{,}83$"],"f":"$\\bar{x} = \\frac{\\sum x_i n_i}{\\sum n_i}$"},

    # SLOT 3
    {"lvl":2,"q":"Série : $4, 7, 7, 8, 10, 12, 15, 18$. Calcule $Q_1$ et $Q_3$.","a":"$Q_1=7,\\ Q_3=13{,}5$","options":["$Q_1=7,\\ Q_3=13{,}5$","$Q_1=8,\\ Q_3=12$","$Q_1=4,\\ Q_3=18$"],"steps":["$8$ valeurs → $Q_1$ = médiane de la 1re moitié $(4,7,7,8)$","$Q_1 = \\frac{7+7}{2} = 7$","$Q_3$ = médiane de la 2e moitié $(10,12,15,18) = \\frac{12+15}{2} = 13{,}5$"],"f":"$Q_1$ : 25e centile, $Q_3$ : 75e centile"},
    {"lvl":2,"type":"vf","q":"La moyenne est toujours un bon indicateur de tendance centrale.","a":"Faux","options":["Vrai","Faux"],"steps":["La moyenne est sensible aux valeurs extrêmes","Exemple : $1, 2, 3, 4, 100$ → moyenne $= 22$","La médiane ($3$) est plus représentative ici"],"f":"Moyenne vs médiane : sensibilité aux extrêmes"},
    {"lvl":2,"q":"L'équipe a une moyenne de $12$ points sur $8$ matchs. Au 9e match : $21$ points. Nouvelle moyenne ?","a":"$13$","options":["$13$","$12{,}5$","$14$"],"steps":["Total ancien : $12 \\times 8 = 96$","Nouveau total : $96+21 = 117$","Nouvelle moyenne : $\\frac{117}{9} = 13$"],"f":"$\\bar{x} = \\frac{\\sum x_i}{n}$"},
    {"lvl":2,"type":"fill","q":"$Q_1$ est la valeur en dessous de laquelle se trouvent ___% des données.","a":"25","options":[],"steps":["$Q_1$ = premier quartile","$25\\%$ des valeurs sont $\\leq Q_1$","$75\\%$ sont $\\geq Q_1$"],"f":"$Q_1$ : 25e centile"},
    {"lvl":2,"q":"Salaires (k€) : $2, 4, 6, 8, 10, 50$. La moyenne ou la médiane représente-t-elle mieux cette série ?","a":"La médiane car la valeur $50$ est aberrante","options":["La médiane car la valeur $50$ est aberrante","La moyenne car elle utilise toutes les valeurs","Les deux se valent"],"steps":["Moyenne $= \\frac{2+4+6+8+10+50}{6} = \\frac{80}{6} \\approx 13{,}3$","Médiane $= \\frac{6+8}{2} = 7$","$13{,}3$ est tiré vers le haut par $50$ → médiane plus fiable"],"f":"Moyenne vs médiane"},

    # SLOT 4
    {"lvl":2,"q":"Tableau : valeur $5$ (freq $3$), $10$ (freq $2$), $15$ (freq $5$). Calcule la moyenne.","a":"$11$","options":["$11$","$10$","$12$"],"steps":["$\\frac{5 \\times 3+10 \\times 2+15 \\times 5}{3+2+5}$","$= \\frac{15+20+75}{10} = \\frac{110}{10}$","$= 11$"],"f":"$\\bar{x} = \\frac{\\sum x_i n_i}{\\sum n_i}$"},
    {"lvl":2,"type":"vf","q":"L'EIQ (écart interquartile) est toujours inférieur ou égal à l'étendue.","a":"Vrai","options":["Vrai","Faux"],"steps":["EIQ $= Q_3-Q_1$ et étendue $= \\max-\\min$","$\\min \\leq Q_1$ et $Q_3 \\leq \\max$","Donc $Q_3-Q_1 \\leq \\max-\\min$"],"f":"EIQ $= Q_3-Q_1 \\leq$ étendue"},
    {"lvl":2,"q":"Diagramme en boîte : min $=2$, $Q_1=5$, $Q_2=8$, $Q_3=12$, max $=20$. Calcule l'EIQ et l'étendue.","a":"EIQ $=7$, étendue $=18$","options":["EIQ $=7$, étendue $=18$","EIQ $=6$, étendue $=15$","EIQ $=8$, étendue $=20$"],"steps":["EIQ $= Q_3-Q_1 = 12-5 = 7$","Étendue $= \\max-\\min = 20-2 = 18$"],"f":"EIQ $= Q_3-Q_1$, étendue $= \\max-\\min$"},
    {"lvl":2,"type":"fill","q":"Effectif $12$, moyenne $=10$. On retire une valeur de $16$. La nouvelle moyenne est ___ (arrondi au centième).","a":"9,45","options":[],"steps":["Total ancien : $12 \\times 10 = 120$","Nouveau total : $120-16 = 104$, effectif $= 11$","$\\frac{104}{11} \\approx 9{,}45$"],"f":"$\\bar{x} = \\frac{\\sum x_i}{n}$"},
    {"lvl":2,"q":"$10$ élèves, notes classées : $8, 9, 10, 10, 11, 12, 13, 14, 15, 18$. Calcule $Q_1$, $Q_2$, $Q_3$.","a":"$Q_1=10,\\ Q_2=11{,}5,\\ Q_3=14$","options":["$Q_1=10,\\ Q_2=11{,}5,\\ Q_3=14$","$Q_1=9,\\ Q_2=11,\\ Q_3=15$","$Q_1=10,\\ Q_2=12,\\ Q_3=14$"],"steps":["$Q_2$ (médiane) = $\\frac{11+12}{2} = 11{,}5$","$Q_1$ = médiane de $(8,9,10,10,11)$ = $10$","$Q_3$ = médiane de $(12,13,14,15,18)$ = $14$"],"f":"Quartiles : $Q_1$, $Q_2$ (médiane), $Q_3$"},
]

# Fix Statistiques slot 2 last exercise - recalculate
# 12×2 + 15×3 + 8×1 = 24+45+8 = 77, /6 = 12.833...
NEW_EXOS["Statistiques"][9] = {"lvl":1,"q":"Moyenne pondérée : $12$ (coeff $2$), $15$ (coeff $3$), $8$ (coeff $1$). Calcule.","a":"$12{,}83$","options":["$12{,}83$","$11{,}67$","$13{,}17$"],"steps":["$\\frac{12 \\times 2+15 \\times 3+8 \\times 1}{2+3+1}$","$= \\frac{24+45+8}{6} = \\frac{77}{6}$","$\\approx 12{,}83$"],"f":"$\\bar{x} = \\frac{\\sum x_i n_i}{\\sum n_i}$"}

# ─────────────────────────────────────────────────────────────────────
# 7. PROBABILITÉS
# ─────────────────────────────────────────────────────────────────────
NEW_EXOS["Probabilités"] = [
    # SLOT 1
    {"lvl":1,"q":"Une urne contient $3$ boules rouges et $7$ boules bleues. Probabilité de tirer une rouge ?","a":"$\\frac{3}{10}$","options":["$\\frac{3}{10}$","$\\frac{7}{10}$","$\\frac{3}{7}$"],"steps":["Cas favorables : $3$ boules rouges","Cas possibles : $3+7 = 10$ boules","$P = \\frac{3}{10}$"],"f":"$P(A) = \\frac{\\text{cas favorables}}{\\text{cas possibles}}$"},
    {"lvl":1,"q":"On lance un dé à $6$ faces. Probabilité d'obtenir un nombre pair ?","a":"$\\frac{1}{2}$","options":["$\\frac{1}{2}$","$\\frac{1}{3}$","$\\frac{1}{6}$"],"steps":["Nombres pairs : $\\{2, 4, 6\\}$ → $3$ cas","Total : $6$ faces","$P = \\frac{3}{6} = \\frac{1}{2}$"],"f":"$P(A) = \\frac{\\text{cas favorables}}{\\text{cas possibles}}$"},
    {"lvl":1,"type":"vf","q":"La probabilité d'un événement est toujours comprise entre $0$ et $1$.","a":"Vrai","options":["Vrai","Faux"],"steps":["$P(A) = 0$ : événement impossible","$P(A) = 1$ : événement certain","$0 \\leq P(A) \\leq 1$ toujours"],"f":"$0 \\leq P(A) \\leq 1$"},
    {"lvl":1,"q":"Au Monopoly, il faut faire plus de $4$ au dé. Quelle probabilité ?","a":"$\\frac{1}{3}$","options":["$\\frac{1}{3}$","$\\frac{1}{2}$","$\\frac{2}{3}$"],"steps":["Plus de $4$ : $\\{5, 6\\}$ → $2$ cas","Total : $6$ faces","$P = \\frac{2}{6} = \\frac{1}{3}$"],"f":"$P(A) = \\frac{\\text{cas favorables}}{\\text{cas possibles}}$"},
    {"lvl":1,"type":"fill","q":"On tire une carte d'un jeu de $52$. La probabilité d'un as est ___ (fraction irréductible).","a":"1/13","options":[],"steps":["$4$ as dans un jeu de $52$ cartes","$P = \\frac{4}{52} = \\frac{1}{13}$"],"f":"$P(A) = \\frac{\\text{cas favorables}}{\\text{cas possibles}}$"},

    # SLOT 2
    {"lvl":1,"q":"Sac : $5$ vertes, $3$ jaunes, $2$ rouges. Probabilité de NE PAS tirer une rouge ?","a":"$\\frac{4}{5}$","options":["$\\frac{4}{5}$","$\\frac{1}{5}$","$\\frac{3}{5}$"],"steps":["$P(\\text{rouge}) = \\frac{2}{10} = \\frac{1}{5}$","$P(\\overline{\\text{rouge}}) = 1-\\frac{1}{5}$","$= \\frac{4}{5}$"],"f":"$P(\\bar{A}) = 1-P(A)$"},
    {"lvl":1,"type":"vf","q":"$P(A)+P(\\bar{A})=1$.","a":"Vrai","options":["Vrai","Faux"],"steps":["$\\bar{A}$ = événement contraire de $A$","La somme des probabilités de tous les issues = $1$","Donc $P(A)+P(\\bar{A})=1$"],"f":"$P(\\bar{A}) = 1-P(A)$"},
    {"lvl":1,"q":"La probabilité qu'il pleuve est $0{,}6$. Probabilité qu'il ne pleuve pas ?","a":"$0{,}4$","options":["$0{,}4$","$0{,}6$","$1{,}6$"],"steps":["$P(\\overline{\\text{pluie}}) = 1-P(\\text{pluie})$","$= 1-0{,}6$","$= 0{,}4$"],"f":"$P(\\bar{A}) = 1-P(A)$"},
    {"lvl":1,"type":"fill","q":"Pour deux événements indépendants, $P(A \\cap B)=$ ___ (formule).","a":"P(A) × P(B)","options":[],"steps":["Quand $A$ et $B$ sont indépendants","L'occurrence de l'un n'influence pas l'autre","$P(A \\cap B) = P(A) \\times P(B)$"],"f":"$P(A \\cap B) = P(A) \\times P(B)$ si indépendants"},
    {"lvl":1,"q":"Un élève dit : « J'ai lancé un dé $5$ fois sans obtenir $6$, donc j'ai plus de chance au prochain. » A-t-il raison ?","a":"Non, chaque lancer est indépendant : $P=\\frac{1}{6}$","options":["Non, chaque lancer est indépendant : $P=\\frac{1}{6}$","Oui, la probabilité augmente","Oui, c'est la loi des grands nombres"],"steps":["Chaque lancer est indépendant du précédent","La probabilité reste $\\frac{1}{6}$ à chaque lancer","C'est le sophisme du joueur"],"f":"Indépendance : $P$ ne change pas"},

    # SLOT 3
    {"lvl":2,"q":"On lance deux dés. Probabilité d'obtenir une somme de $7$ ?","a":"$\\frac{1}{6}$","options":["$\\frac{1}{6}$","$\\frac{7}{36}$","$\\frac{1}{12}$"],"steps":["Combinaisons donnant $7$ : $(1,6),(2,5),(3,4),(4,3),(5,2),(6,1)$","$6$ combinaisons sur $36$ possibles","$P = \\frac{6}{36} = \\frac{1}{6}$"],"f":"$P = \\frac{\\text{cas favorables}}{\\text{cas possibles}}$"},
    {"lvl":2,"type":"vf","q":"Pour deux événements incompatibles, $P(A \\cup B) = P(A)+P(B)$.","a":"Vrai","options":["Vrai","Faux"],"steps":["Incompatibles : $A$ et $B$ ne peuvent pas arriver en même temps","$P(A \\cap B) = 0$","$P(A \\cup B) = P(A)+P(B)-0 = P(A)+P(B)$"],"f":"$P(A \\cup B) = P(A)+P(B)$ si $A \\cap B = \\emptyset$"},
    {"lvl":2,"q":"$A$ et $B$ incompatibles, $P(A)=0{,}3$, $P(B)=0{,}45$. Calcule $P(A \\cup B)$.","a":"$0{,}75$","options":["$0{,}75$","$0{,}135$","$0{,}15$"],"steps":["Incompatibles → $P(A \\cup B) = P(A)+P(B)$","$= 0{,}3+0{,}45$","$= 0{,}75$"],"f":"$P(A \\cup B) = P(A)+P(B)$ si incompatibles"},
    {"lvl":2,"type":"fill","q":"On tire une carte d'un jeu de $52$. Probabilité d'un roi rouge = ___ (fraction irréductible).","a":"1/26","options":[],"steps":["$2$ rois rouges (cœur et carreau)","$P = \\frac{2}{52} = \\frac{1}{26}$"],"f":"$P = \\frac{\\text{cas favorables}}{\\text{cas possibles}}$"},
    {"lvl":2,"q":"Dé : $A$ = multiple de $2$, $B$ = multiple de $3$. $P(A)=\\frac{1}{2}$, $P(B)=\\frac{1}{3}$, $P(A \\cap B)=\\frac{1}{6}$. Calcule $P(A \\cup B)$.","a":"$\\frac{2}{3}$","options":["$\\frac{2}{3}$","$\\frac{5}{6}$","$\\frac{1}{6}$"],"steps":["$P(A \\cup B) = P(A)+P(B)-P(A \\cap B)$","$= \\frac{1}{2}+\\frac{1}{3}-\\frac{1}{6}$","$= \\frac{3+2-1}{6} = \\frac{4}{6} = \\frac{2}{3}$"],"f":"$P(A \\cup B) = P(A)+P(B)-P(A \\cap B)$"},

    # SLOT 4
    {"lvl":2,"q":"Urne : $3$ rouges, $2$ bleues. On tire $2$ boules SANS remise. Probabilité de $2$ rouges ?","a":"$\\frac{3}{10}$","options":["$\\frac{3}{10}$","$\\frac{9}{25}$","$\\frac{1}{5}$"],"steps":["$P(\\text{1re rouge}) = \\frac{3}{5}$","$P(\\text{2e rouge} | \\text{1re rouge}) = \\frac{2}{4} = \\frac{1}{2}$","$P = \\frac{3}{5} \\times \\frac{1}{2} = \\frac{3}{10}$"],"f":"Sans remise : $P$ change après chaque tirage"},
    {"lvl":2,"type":"vf","q":"$200$ lancers de dé, $36$ fois le $6$. La fréquence $\\frac{36}{200}=0{,}18$ est proche de $\\frac{1}{6} \\approx 0{,}167$.","a":"Vrai","options":["Vrai","Faux"],"steps":["$\\frac{36}{200} = 0{,}18$","$\\frac{1}{6} \\approx 0{,}167$","Écart de $0{,}013$ → normal pour $200$ lancers"],"f":"Loi des grands nombres : fréquence → probabilité"},
    {"lvl":2,"q":"Roue de $8$ cases ($1$ à $8$). Probabilité d'un multiple de $4$ ?","a":"$\\frac{1}{4}$","options":["$\\frac{1}{4}$","$\\frac{1}{8}$","$\\frac{1}{2}$"],"steps":["Multiples de $4$ dans $\\{1,...,8\\}$ : $\\{4, 8\\}$","$2$ cas favorables sur $8$","$P = \\frac{2}{8} = \\frac{1}{4}$"],"f":"$P = \\frac{\\text{cas favorables}}{\\text{cas possibles}}$"},
    {"lvl":2,"type":"fill","q":"$500$ pile ou face, $260$ piles. La fréquence de pile est ___ (en décimal).","a":"0,52","options":[],"steps":["$f = \\frac{260}{500}$","$= 0{,}52$","Proche de $0{,}5$ → pièce probablement non truquée"],"f":"Fréquence $= \\frac{\\text{effectif}}{\\text{total}}$"},
    {"lvl":2,"q":"Au poker, on pioche $1$ carte dans un jeu de $52$. Probabilité d'un as OU un roi ?","a":"$\\frac{2}{13}$","options":["$\\frac{2}{13}$","$\\frac{1}{13}$","$\\frac{4}{13}$"],"steps":["$P(\\text{as}) = \\frac{4}{52}$, $P(\\text{roi}) = \\frac{4}{52}$","Événements incompatibles (une carte ne peut être les deux)","$P = \\frac{4+4}{52} = \\frac{8}{52} = \\frac{2}{13}$"],"f":"$P(A \\cup B) = P(A)+P(B)$ si incompatibles"},
]

# ─────────────────────────────────────────────────────────────────────
# 8. RACINES CARRÉES
# ─────────────────────────────────────────────────────────────────────
NEW_EXOS["Racines carrées"] = [
    # SLOT 1
    {"lvl":1,"q":"Calcule $\\sqrt{49}$.","a":"$7$","options":["$7$","$49$","$\\frac{49}{2}$"],"steps":["$\\sqrt{49}$ = nombre positif dont le carré vaut $49$","$7^2 = 49$","$\\sqrt{49} = 7$"],"f":"$\\sqrt{a^2} = a$ pour $a \\geq 0$"},
    {"lvl":1,"q":"Calcule $\\sqrt{4} \\times \\sqrt{9}$.","a":"$6$","options":["$6$","$36$","$\\sqrt{36}$"],"steps":["$\\sqrt{4} = 2$ et $\\sqrt{9} = 3$","$2 \\times 3 = 6$","Ou : $\\sqrt{4 \\times 9} = \\sqrt{36} = 6$"],"f":"$\\sqrt{a} \\times \\sqrt{b} = \\sqrt{ab}$"},
    {"lvl":1,"type":"vf","q":"$\\sqrt{a^2}=a$ pour tout nombre $a$.","a":"Faux","options":["Vrai","Faux"],"steps":["$\\sqrt{(-3)^2} = \\sqrt{9} = 3 \\neq -3$","$\\sqrt{a^2} = |a|$ (valeur absolue)","Vrai seulement si $a \\geq 0$"],"f":"$\\sqrt{a^2} = |a|$"},
    {"lvl":1,"q":"Simplifie $\\sqrt{100}$.","a":"$10$","options":["$10$","$50$","$\\sqrt{10}$"],"steps":["$100 = 10^2$","$\\sqrt{10^2} = 10$"],"f":"$\\sqrt{a^2} = a$ pour $a \\geq 0$"},
    {"lvl":1,"type":"fill","q":"Un terrain carré a une aire de $25$ m². Son côté mesure ___ m.","a":"5","options":[],"steps":["Aire d'un carré = côté²","côté $= \\sqrt{25}$","$= 5$ m"],"f":"côté $= \\sqrt{\\text{aire}}$"},

    # SLOT 2
    {"lvl":1,"q":"Parmi $\\sqrt{4}$, $\\sqrt{7}$, $\\sqrt{9}$, lequel est irrationnel ?","a":"$\\sqrt{7}$","options":["$\\sqrt{7}$","$\\sqrt{4}$","$\\sqrt{9}$"],"steps":["$\\sqrt{4} = 2$ (rationnel), $\\sqrt{9} = 3$ (rationnel)","$7$ n'est pas un carré parfait","$\\sqrt{7}$ est irrationnel"],"f":"$\\sqrt{n}$ irrationnel si $n$ n'est pas un carré parfait"},
    {"lvl":1,"type":"vf","q":"$\\sqrt{2}$ est un nombre rationnel.","a":"Faux","options":["Vrai","Faux"],"steps":["$\\sqrt{2} \\approx 1{,}414...$, décimales infinies non périodiques","On ne peut pas l'écrire sous forme $\\frac{p}{q}$","$\\sqrt{2}$ est irrationnel (démonstration classique)"],"f":"$\\sqrt{2} \\notin \\mathbb{Q}$"},
    {"lvl":1,"q":"$3 < \\sqrt{15} < 4$. Entre quels entiers consécutifs se situe $\\sqrt{15}$ ?","a":"$3$ et $4$","options":["$3$ et $4$","$2$ et $3$","$4$ et $5$"],"steps":["$3^2 = 9 < 15$ et $4^2 = 16 > 15$","Donc $3 < \\sqrt{15} < 4$","$\\sqrt{15} \\approx 3{,}87$"],"f":"$a < \\sqrt{n} < b \\Leftrightarrow a^2 < n < b^2$"},
    {"lvl":1,"type":"fill","q":"$\\sqrt{75} = $ ___$\\sqrt{3}$.","a":"5","options":[],"steps":["$75 = 25 \\times 3$","$\\sqrt{75} = \\sqrt{25} \\times \\sqrt{3}$","$= 5\\sqrt{3}$"],"f":"$\\sqrt{ab} = \\sqrt{a} \\times \\sqrt{b}$"},
    {"lvl":1,"q":"Calcule $2\\sqrt{3}+5\\sqrt{3}$.","a":"$7\\sqrt{3}$","options":["$7\\sqrt{3}$","$7\\sqrt{6}$","$10\\sqrt{3}$"],"steps":["Même radical → on additionne les coefficients","$2\\sqrt{3}+5\\sqrt{3} = (2+5)\\sqrt{3}$","$= 7\\sqrt{3}$"],"f":"$a\\sqrt{n}+b\\sqrt{n} = (a+b)\\sqrt{n}$"},

    # SLOT 3
    {"lvl":2,"q":"Simplifie $\\sqrt{48}$.","a":"$4\\sqrt{3}$","options":["$4\\sqrt{3}$","$2\\sqrt{12}$","$6\\sqrt{2}$"],"steps":["$48 = 16 \\times 3$","$\\sqrt{48} = \\sqrt{16} \\times \\sqrt{3}$","$= 4\\sqrt{3}$"],"f":"$\\sqrt{ab} = \\sqrt{a} \\times \\sqrt{b}$"},
    {"lvl":2,"type":"vf","q":"$\\sqrt{12}+\\sqrt{3} = \\sqrt{15}$.","a":"Faux","options":["Vrai","Faux"],"steps":["$\\sqrt{12} = 2\\sqrt{3}$","$2\\sqrt{3}+\\sqrt{3} = 3\\sqrt{3}$","$3\\sqrt{3} \\neq \\sqrt{15}$ (on n'additionne pas sous les racines)"],"f":"$\\sqrt{a}+\\sqrt{b} \\neq \\sqrt{a+b}$"},
    {"lvl":2,"q":"Calcule $(3\\sqrt{2})^2$.","a":"$18$","options":["$18$","$9\\sqrt{2}$","$6$"],"steps":["$(3\\sqrt{2})^2 = 3^2 \\times (\\sqrt{2})^2$","$= 9 \\times 2$","$= 18$"],"f":"$(a\\sqrt{b})^2 = a^2 \\times b$"},
    {"lvl":2,"type":"fill","q":"$3\\sqrt{2} \\times 4\\sqrt{2} =$ ___.","a":"24","options":[],"steps":["$3 \\times 4 = 12$","$\\sqrt{2} \\times \\sqrt{2} = 2$","$12 \\times 2 = 24$"],"f":"$a\\sqrt{n} \\times b\\sqrt{n} = ab \\times n$"},
    {"lvl":2,"q":"Calcule $\\frac{\\sqrt{50}}{\\sqrt{2}}$.","a":"$5$","options":["$5$","$\\sqrt{25}$","$25$"],"steps":["$\\frac{\\sqrt{50}}{\\sqrt{2}} = \\sqrt{\\frac{50}{2}}$","$= \\sqrt{25}$","$= 5$"],"f":"$\\frac{\\sqrt{a}}{\\sqrt{b}} = \\sqrt{\\frac{a}{b}}$"},

    # SLOT 4
    {"lvl":2,"q":"Rationalise $\\frac{6}{\\sqrt{3}}$.","a":"$2\\sqrt{3}$","options":["$2\\sqrt{3}$","$\\frac{6\\sqrt{3}}{9}$","$6\\sqrt{3}$"],"steps":["$\\frac{6}{\\sqrt{3}} = \\frac{6 \\times \\sqrt{3}}{\\sqrt{3} \\times \\sqrt{3}}$","$= \\frac{6\\sqrt{3}}{3}$","$= 2\\sqrt{3}$"],"f":"$\\frac{a}{\\sqrt{b}} = \\frac{a\\sqrt{b}}{b}$"},
    {"lvl":2,"type":"vf","q":"$\\sqrt{3}+\\sqrt{7} > \\sqrt{10}$.","a":"Vrai","options":["Vrai","Faux"],"steps":["$(\\sqrt{3}+\\sqrt{7})^2 = 3+2\\sqrt{21}+7 = 10+2\\sqrt{21}$","$(\\sqrt{10})^2 = 10$","$10+2\\sqrt{21} > 10$ donc $\\sqrt{3}+\\sqrt{7} > \\sqrt{10}$"],"f":"$(\\sqrt{a}+\\sqrt{b})^2 = a+b+2\\sqrt{ab} > a+b$"},
    {"lvl":2,"q":"Dans un triangle rectangle, côtés $3$ cm et $4$ cm. Longueur de l'hypoténuse ?","a":"$5$ cm","options":["$5$ cm","$7$ cm","$\\sqrt{7}$ cm"],"steps":["Pythagore : $c^2 = 3^2+4^2 = 9+16 = 25$","$c = \\sqrt{25}$","$c = 5$ cm"],"f":"$c = \\sqrt{a^2+b^2}$"},
    {"lvl":2,"type":"fill","q":"Une pièce carrée a une aire de $50$ m². Son côté exact vaut ___$\\sqrt{2}$ m.","a":"5","options":[],"steps":["côté $= \\sqrt{50}$","$50 = 25 \\times 2$","$\\sqrt{50} = 5\\sqrt{2}$ m"],"f":"$\\sqrt{ab} = \\sqrt{a} \\times \\sqrt{b}$"},
    {"lvl":2,"q":"Compare $3\\sqrt{2}$ et $2\\sqrt{5}$.","a":"$3\\sqrt{2} < 2\\sqrt{5}$","options":["$3\\sqrt{2} < 2\\sqrt{5}$","$3\\sqrt{2} > 2\\sqrt{5}$","$3\\sqrt{2} = 2\\sqrt{5}$"],"steps":["$(3\\sqrt{2})^2 = 9 \\times 2 = 18$","$(2\\sqrt{5})^2 = 4 \\times 5 = 20$","$18 < 20$ donc $3\\sqrt{2} < 2\\sqrt{5}$"],"f":"Comparer $a\\sqrt{b}$ : comparer les carrés"},
]

# ─────────────────────────────────────────────────────────────────────
# 9. SYSTÈMES D'ÉQUATIONS
# ─────────────────────────────────────────────────────────────────────
NEW_EXOS["Systèmes d'équations"] = [
    # SLOT 1
    {"lvl":1,"q":"Résous $\\begin{cases} x+y=7 \\\\ y=2x-2 \\end{cases}$","a":"$x=3,\\ y=4$","options":["$x=3,\\ y=4$","$x=4,\\ y=3$","$x=2,\\ y=5$"],"steps":["Substitution : $x+(2x-2)=7$","$3x-2=7$ → $3x=9$ → $x=3$","$y=2 \\times 3-2=4$"],"f":"Substitution : remplacer une variable"},
    {"lvl":1,"q":"Résous $\\begin{cases} 2x+y=8 \\\\ x=3 \\end{cases}$","a":"$x=3,\\ y=2$","options":["$x=3,\\ y=2$","$x=3,\\ y=5$","$x=2,\\ y=3$"],"steps":["$x=3$ → substituer dans l'autre","$2 \\times 3+y=8$ → $6+y=8$","$y=2$"],"f":"Substitution directe"},
    {"lvl":1,"type":"vf","q":"Graphiquement, la solution d'un système $2 \\times 2$ est le point d'intersection des deux droites.","a":"Vrai","options":["Vrai","Faux"],"steps":["Chaque équation linéaire représente une droite","La solution commune est le point commun","C'est l'intersection des droites"],"f":"Solution = point d'intersection"},
    {"lvl":1,"q":"Résous $\\begin{cases} y=x+1 \\\\ x+y=5 \\end{cases}$","a":"$x=2,\\ y=3$","options":["$x=2,\\ y=3$","$x=3,\\ y=2$","$x=1,\\ y=4$"],"steps":["$x+(x+1)=5$","$2x+1=5$ → $2x=4$ → $x=2$","$y=2+1=3$"],"f":"Substitution"},
    {"lvl":1,"type":"fill","q":"Dans $\\begin{cases} x+y=7 \\\\ x-y=3 \\end{cases}$, en additionnant : $2x=$ ___.","a":"10","options":[],"steps":["$(x+y)+(x-y) = 7+3$","$2x = 10$","$x = 5$, puis $y = 2$"],"f":"Combinaison : additionner les équations"},

    # SLOT 2
    {"lvl":1,"q":"Résous $\\begin{cases} x+2y=10 \\\\ x-y=1 \\end{cases}$","a":"$x=4,\\ y=3$","options":["$x=4,\\ y=3$","$x=3,\\ y=4$","$x=5,\\ y=2$"],"steps":["Soustraction : $(x+2y)-(x-y) = 10-1$","$3y=9$ → $y=3$","$x=1+3=4$"],"f":"Combinaison : soustraire les équations"},
    {"lvl":1,"type":"vf","q":"Si deux droites ont le même coefficient directeur mais des ordonnées à l'origine différentes, le système n'a pas de solution.","a":"Vrai","options":["Vrai","Faux"],"steps":["Même coefficient directeur = droites parallèles","Ordonnées différentes = pas la même droite","Pas d'intersection → pas de solution"],"f":"Droites parallèles : système incompatible"},
    {"lvl":1,"q":"Au marché, pommes et poires coûtent $10$ € ensemble. Les pommes coûtent $2$ € de plus. Prix de chaque ?","a":"$x=6,\\ y=4$","options":["$x=6,\\ y=4$","$x=7,\\ y=3$","$x=5,\\ y=5$"],"steps":["$\\begin{cases} x+y=10 \\\\ x=y+2 \\end{cases}$","$(y+2)+y=10$ → $2y=8$ → $y=4$","$x=6$"],"f":"Mise en système"},
    {"lvl":1,"type":"fill","q":"Résous $\\begin{cases} 2x+3y=12 \\\\ x=3 \\end{cases}$. Alors $y=$ ___.","a":"2","options":[],"steps":["$2 \\times 3+3y=12$","$6+3y=12$ → $3y=6$","$y=2$"],"f":"Substitution directe"},
    {"lvl":1,"q":"Un père a $3$ fois l'âge de son fils. Ensemble : $80$ ans. Âges ?","a":"Fils $20$, père $60$","options":["Fils $20$, père $60$","Fils $15$, père $65$","Fils $25$, père $55$"],"steps":["$\\begin{cases} y=3x \\\\ x+y=80 \\end{cases}$","$x+3x=80$ → $4x=80$ → $x=20$","$y=60$"],"f":"Mise en système"},

    # SLOT 3
    {"lvl":2,"q":"Résous $\\begin{cases} 4x+2y=14 \\\\ x+y=5 \\end{cases}$","a":"$x=2,\\ y=3$","options":["$x=2,\\ y=3$","$x=3,\\ y=2$","$x=4,\\ y=1$"],"steps":["2e éq. $\\times 2$ : $2x+2y=10$","$(4x+2y)-(2x+2y) = 14-10$ → $2x=4$ → $x=2$","$y=5-2=3$"],"f":"Combinaison linéaire"},
    {"lvl":2,"type":"vf","q":"Le système $\\begin{cases} x+y=3 \\\\ 2x+2y=6 \\end{cases}$ a une infinité de solutions.","a":"Vrai","options":["Vrai","Faux"],"steps":["La 2e équation = 2 × la 1re","Ce sont la même droite","Infinité de solutions (tous les points de la droite)"],"f":"Même droite = infinité de solutions"},
    {"lvl":2,"q":"$5$ croissants et $2$ pains au chocolat : $19$ €. Un croissant coûte $1$ € de plus. Prix du croissant ?","a":"$3$ €","options":["$3$ €","$2$ €","$4$ €"],"steps":["$\\begin{cases} 5x+2y=19 \\\\ x=y+1 \\end{cases}$","$5(y+1)+2y=19$ → $7y+5=19$ → $y=2$","$x=3$ €"],"f":"Mise en système + substitution"},
    {"lvl":2,"type":"fill","q":"$\\begin{cases} 3x+4y=24 \\\\ 3x-2y=6 \\end{cases}$. Par soustraction : $6y=$ ___.","a":"18","options":[],"steps":["$(3x+4y)-(3x-2y) = 24-6$","$6y = 18$","$y = 3$, puis $x = 4$"],"f":"Combinaison par soustraction"},
    {"lvl":2,"q":"Poules et lapins : $10$ têtes, $28$ pattes. Combien de lapins ?","a":"$4$","options":["$4$","$6$","$5$"],"steps":["$\\begin{cases} p+l=10 \\\\ 2p+4l=28 \\end{cases}$","$2(10-l)+4l=28$ → $20+2l=28$ → $l=4$","$4$ lapins et $6$ poules"],"f":"Mise en système"},

    # SLOT 4
    {"lvl":2,"q":"Résous $\\begin{cases} \\frac{x}{2}+y=5 \\\\ x-y=4 \\end{cases}$","a":"$x=6,\\ y=2$","options":["$x=6,\\ y=2$","$x=4,\\ y=3$","$x=8,\\ y=1$"],"steps":["De l'éq. 2 : $y=x-4$","$\\frac{x}{2}+(x-4)=5$ → $\\frac{3x}{2}=9$ → $x=6$","$y=6-4=2$"],"f":"Substitution + fraction"},
    {"lvl":2,"type":"vf","q":"On peut toujours résoudre un système $2 \\times 2$ par substitution OU par combinaison.","a":"Vrai","options":["Vrai","Faux"],"steps":["Les deux méthodes sont équivalentes","Substitution : isoler une variable puis remplacer","Combinaison : éliminer une variable par addition/soustraction"],"f":"Substitution ≡ combinaison"},
    {"lvl":2,"q":"Léa a $2$ fois plus d'argent que Noé. Ensemble : $45$ €. Combien a Léa ?","a":"$30$ €","options":["$30$ €","$15$ €","$20$ €"],"steps":["$\\begin{cases} l=2n \\\\ l+n=45 \\end{cases}$","$2n+n=45$ → $3n=15$ → $n=15$","$l=30$ €"],"f":"Mise en système"},
    {"lvl":2,"type":"fill","q":"$\\begin{cases} x+2y=11 \\\\ 3x-y=3 \\end{cases}$. La solution est $x=$ ___ (entier).","a":"1","options":[" "],"steps":["2e éq. $\\times 2$ : $6x-2y=6$","$(x+2y)+(6x-2y) = 11+6$ → $7x=17$... Hmm","Recalculons : de l'éq. 2, $y=3x-3$. Dans éq. 1 : $x+2(3x-3)=11$ → $7x-6=11$ → $7x=17$... $x=17/7$"],"f":"Substitution + combinaison"},
    {"lvl":2,"q":"Résous $\\begin{cases} 2x+y=9 \\\\ x+3y=12 \\end{cases}$","a":"$x=3,\\ y=3$","options":["$x=3,\\ y=3$","$x=4,\\ y=1$","$x=2,\\ y=5$"],"steps":["Éq.1 $\\times 3$ : $6x+3y=27$","$(6x+3y)-(x+3y) = 27-12$ → $5x=15$ → $x=3$","$y=9-2 \\times 3=3$"],"f":"Combinaison linéaire"},
]

# Fix Systèmes slot 4 exercise 4 - x+2y=11, 3x-y=3 gives x=17/7 which is ugly. Replace.
NEW_EXOS["Systèmes d'équations"][18] = {"lvl":2,"type":"fill","q":"$\\begin{cases} 2x+3y=13 \\\\ x-y=1 \\end{cases}$. La solution est $x=$ ___ (entier).","a":"3","options":[],"steps":["De l'éq. 2 : $x=y+1$","$2(y+1)+3y=13$ → $5y+2=13$ → $y=\\frac{11}{5}$... Non"],"f":"Substitution"}

# That still doesn't work cleanly. Let me use x+2y=11, 3x-y=3 → check:
# From eq2: y=3x-3. In eq1: x+2(3x-3)=11 → 7x-6=11 → 7x=17. Not integer. Replace entirely.
NEW_EXOS["Systèmes d'équations"][18] = {"lvl":2,"type":"fill","q":"$\\begin{cases} x+3y=12 \\\\ x+y=6 \\end{cases}$. Alors $y=$ ___.","a":"3","options":[],"steps":["Soustraction : $(x+3y)-(x+y) = 12-6$","$2y = 6$","$y = 3$, puis $x = 3$"],"f":"Combinaison par soustraction"}

# ─────────────────────────────────────────────────────────────────────
# 10. INÉQUATIONS
# ─────────────────────────────────────────────────────────────────────
NEW_EXOS["Inéquations"] = [
    # SLOT 1
    {"lvl":1,"q":"Résous $2x < 10$.","a":"$x < 5$","options":["$x < 5$","$x > 5$","$x < 20$"],"steps":["$2x < 10$","On divise par $2$ (positif → sens conservé)","$x < 5$"],"f":"$ax < b \\Leftrightarrow x < \\frac{b}{a}$ si $a > 0$"},
    {"lvl":1,"q":"Résous $x-5 \\leq 2$.","a":"$x \\leq 7$","options":["$x \\leq 7$","$x \\geq 7$","$x \\leq -3$"],"steps":["$x-5 \\leq 2$","$x \\leq 2+5$","$x \\leq 7$"],"f":"$x+a \\leq b \\Leftrightarrow x \\leq b-a$"},
    {"lvl":1,"type":"vf","q":"$x \\leq 3$ inclut la valeur $x=3$.","a":"Vrai","options":["Vrai","Faux"],"steps":["$\\leq$ signifie « inférieur ou ÉGAL »","$x=3$ vérifie $3 \\leq 3$","Contrairement à $<$ (strictement inférieur)"],"f":"$\\leq$ : inégalité large (inclut l'égalité)"},
    {"lvl":1,"q":"Résous $3x \\geq 12$.","a":"$x \\geq 4$","options":["$x \\geq 4$","$x \\leq 4$","$x \\geq 36$"],"steps":["$3x \\geq 12$","On divise par $3$ (positif)","$x \\geq 4$"],"f":"$ax \\geq b \\Leftrightarrow x \\geq \\frac{b}{a}$ si $a > 0$"},
    {"lvl":1,"type":"fill","q":"L'ensemble solution de $3x-9 \\geq 0$ est $x \\geq$ ___.","a":"3","options":[],"steps":["$3x \\geq 9$","$x \\geq \\frac{9}{3}$","$x \\geq 3$"],"f":"$ax \\geq b \\Leftrightarrow x \\geq \\frac{b}{a}$"},

    # SLOT 2
    {"lvl":1,"q":"Résous $x+8 < 15$.","a":"$x < 7$","options":["$x < 7$","$x > 7$","$x < 23$"],"steps":["$x < 15-8$","$x < 7$"],"f":"$x+a < b \\Leftrightarrow x < b-a$"},
    {"lvl":1,"type":"vf","q":"La solution d'une inéquation est un intervalle.","a":"Vrai","options":["Vrai","Faux"],"steps":["Contrairement à une équation (nombre fini de solutions)","Une inéquation a une infinité de solutions","Elles forment un intervalle sur la droite réelle"],"f":"Solution d'une inéquation : intervalle"},
    {"lvl":1,"q":"Chaque article coûte $5$ €. Avec $20$ € maximum, combien d'articles au plus ?","a":"$4$","options":["$4$","$5$","$3$"],"steps":["$5x \\leq 20$","$x \\leq 4$","Maximum $4$ articles"],"f":"$ax \\leq b \\Leftrightarrow x \\leq \\frac{b}{a}$"},
    {"lvl":1,"type":"fill","q":"L'intersection de $x > 1$ et $x < 5$ est l'intervalle ___.","a":"]1 ; 5[","options":[],"steps":["$x > 1$ : intervalle $]1\\,;\\,+\\infty[$","$x < 5$ : intervalle $]-\\infty\\,;\\,5[$","Intersection : $]1\\,;\\,5[$"],"f":"Intersection d'intervalles"},
    {"lvl":1,"q":"Pour une compétition, il faut avoir plus de $7$ ans dans $3$ ans. Âge minimum actuel ?","a":"$x > 4$","options":["$x > 4$","$x > 7$","$x > 10$"],"steps":["Dans $3$ ans : $x+3 > 7$","$x > 7-3$","$x > 4$ ans"],"f":"$x+a > b \\Leftrightarrow x > b-a$"},

    # SLOT 3
    {"lvl":2,"q":"Résous $-2x+4 > 0$.","a":"$x < 2$","options":["$x < 2$","$x > 2$","$x > -2$"],"steps":["$-2x > -4$","On divise par $-2$ → ON INVERSE le sens","$x < 2$"],"f":"Division par un négatif : sens inversé"},
    {"lvl":2,"type":"vf","q":"Quand on divise par un nombre négatif, le sens de l'inégalité change.","a":"Vrai","options":["Vrai","Faux"],"steps":["Règle fondamentale des inéquations","Exemple : $-2 > -3$ mais $\\frac{-2}{-1} = 2 < 3 = \\frac{-3}{-1}$","Le sens s'inverse"],"f":"$ax < b$ : si $a < 0$, $x > \\frac{b}{a}$"},
    {"lvl":2,"q":"Résous $5-x > 2$.","a":"$x < 3$","options":["$x < 3$","$x > 3$","$x > -3$"],"steps":["$-x > 2-5$ → $-x > -3$","On multiplie par $-1$ → inversion","$x < 3$"],"f":"$-x > a \\Leftrightarrow x < -a$"},
    {"lvl":2,"type":"fill","q":"Résous $-5x+3 > -7$. On trouve $x <$ ___.","a":"2","options":[],"steps":["$-5x > -10$","Division par $-5$ → inversion","$x < 2$"],"f":"Division par un négatif : sens inversé"},
    {"lvl":2,"q":"Deux groupes de $(x+3)$ personnes dans une salle de $14$ places maximum. Combien de personnes par groupe au plus ?","a":"$x \\leq 4$","options":["$x \\leq 4$","$x \\leq 7$","$x < 4$"],"steps":["$2(x+3) \\leq 14$","$x+3 \\leq 7$","$x \\leq 4$"],"f":"$a(x+b) \\leq c$"},

    # SLOT 4
    {"lvl":2,"q":"Résous $3x+5 \\geq 2x+9$.","a":"$x \\geq 4$","options":["$x \\geq 4$","$x \\leq 4$","$x \\geq 14$"],"steps":["$3x-2x \\geq 9-5$","$x \\geq 4$"],"f":"Regrouper les termes en $x$ d'un côté"},
    {"lvl":2,"type":"vf","q":"On peut toujours représenter la solution d'une inéquation sur une droite graduée.","a":"Vrai","options":["Vrai","Faux"],"steps":["Les solutions forment un intervalle","On hachure la partie non-solution","Point plein ($\\leq$/$\\geq$) ou vide ($<$/$>$)"],"f":"Représentation sur droite graduée"},
    {"lvl":2,"q":"Résous $4(x-1) \\leq 2x+6$.","a":"$x \\leq 5$","options":["$x \\leq 5$","$x \\leq 2$","$x \\geq 5$"],"steps":["$4x-4 \\leq 2x+6$","$2x \\leq 10$","$x \\leq 5$"],"f":"Développer puis résoudre"},
    {"lvl":2,"type":"fill","q":"Un élève a eu $10$, $14$, $11$. Note minimale au 4e contrôle pour avoir une moyenne $> 12$ : supérieure à ___.","a":"13","options":[],"steps":["$\\frac{10+14+11+x}{4} > 12$","$35+x > 48$","$x > 13$"],"f":"$\\frac{\\sum+x}{n} > m \\Leftrightarrow x > mn-\\sum$"},
    {"lvl":2,"q":"Résous $2x-7 < x+1$.","a":"$x < 8$","options":["$x < 8$","$x > 8$","$x < 6$"],"steps":["$2x-x < 1+7$","$x < 8$"],"f":"Regrouper les termes"},
]

# ─────────────────────────────────────────────────────────────────────
# 11. NOTATION SCIENTIFIQUE
# ─────────────────────────────────────────────────────────────────────
NEW_EXOS["Notation scientifique"] = [
    # SLOT 1
    {"lvl":1,"q":"Écris $52\\,000$ en notation scientifique.","a":"$5{,}2 \\times 10^4$","options":["$5{,}2 \\times 10^4$","$52 \\times 10^3$","$0{,}52 \\times 10^5$"],"steps":["On place la virgule après le premier chiffre non nul : $5{,}2$","On compte les décalages : $4$ positions","$52\\,000 = 5{,}2 \\times 10^4$"],"f":"$a \\times 10^n$ avec $1 \\leq a < 10$"},
    {"lvl":1,"q":"Convertis $4{,}8 \\times 10^2$ en écriture décimale.","a":"$480$","options":["$480$","$48$","$4\\,800$"],"steps":["$10^2 = 100$","$4{,}8 \\times 100 = 480$"],"f":"$a \\times 10^n$ : décaler la virgule de $n$ positions"},
    {"lvl":1,"type":"vf","q":"$35{,}2 \\times 10^3$ est en notation scientifique.","a":"Faux","options":["Vrai","Faux"],"steps":["En notation scientifique, $1 \\leq a < 10$","$35{,}2 \\geq 10$ → pas en notation scientifique","Correct : $3{,}52 \\times 10^4$"],"f":"$a \\times 10^n$ avec $1 \\leq a < 10$"},
    {"lvl":1,"q":"Écris $900$ en notation scientifique.","a":"$9 \\times 10^2$","options":["$9 \\times 10^2$","$90 \\times 10^1$","$0{,}9 \\times 10^3$"],"steps":["$900 = 9 \\times 100$","$= 9 \\times 10^2$","$1 \\leq 9 < 10$ ✓"],"f":"$a \\times 10^n$ avec $1 \\leq a < 10$"},
    {"lvl":1,"type":"fill","q":"$150\\,000$ habitants en notation scientifique : $1{,}5 \\times 10^{\\text{___}}$.","a":"5","options":[],"steps":["$150\\,000 = 1{,}5 \\times 10^?$","$1{,}5 \\times 10^5 = 150\\,000$ ✓","Exposant $= 5$"],"f":"$a \\times 10^n$"},

    # SLOT 2
    {"lvl":1,"q":"Convertis $7{,}1 \\times 10^3$ en écriture décimale.","a":"$7\\,100$","options":["$7\\,100$","$710$","$71\\,000$"],"steps":["$10^3 = 1\\,000$","$7{,}1 \\times 1\\,000 = 7\\,100$"],"f":"Décaler la virgule de $n$ positions à droite"},
    {"lvl":1,"type":"vf","q":"$4\\,500 = 45 \\times 10^2$ est une notation scientifique correcte.","a":"Faux","options":["Vrai","Faux"],"steps":["$45 \\geq 10$ → pas en notation scientifique","Il faut $4{,}5 \\times 10^3$","$1 \\leq 4{,}5 < 10$ ✓"],"f":"$a \\times 10^n$ avec $1 \\leq a < 10$"},
    {"lvl":1,"q":"Lequel est en notation scientifique : $63 \\times 10^4$, $6{,}3 \\times 10^5$, $0{,}63 \\times 10^6$ ?","a":"$6{,}3 \\times 10^5$","options":["$6{,}3 \\times 10^5$","$63 \\times 10^4$","$0{,}63 \\times 10^6$"],"steps":["$63 \\geq 10$ ✗, $0{,}63 < 1$ ✗","$6{,}3$ : $1 \\leq 6{,}3 < 10$ ✓","Seul $6{,}3 \\times 10^5$ est correct"],"f":"$a \\times 10^n$ avec $1 \\leq a < 10$"},
    {"lvl":1,"type":"fill","q":"$0{,}00047$ g/L en notation scientifique : $4{,}7 \\times 10^{\\text{___}}$.","a":"-4","options":[],"steps":["On décale la virgule de $4$ positions à droite","$0{,}00047 = 4{,}7 \\times 10^{-4}$","Exposant négatif car nombre $< 1$"],"f":"$a \\times 10^{-n}$ pour les nombres $< 1$"},
    {"lvl":1,"q":"La distance Paris-Lyon est d'environ $370\\,000$ m. En notation scientifique ?","a":"$3{,}7 \\times 10^5$","options":["$3{,}7 \\times 10^5$","$37 \\times 10^4$","$3{,}7 \\times 10^4$"],"steps":["$370\\,000 = 3{,}7 \\times 10^5$","$1 \\leq 3{,}7 < 10$ ✓","Exposant $5$ car $5$ décalages"],"f":"$a \\times 10^n$ avec $1 \\leq a < 10$"},

    # SLOT 3
    {"lvl":2,"q":"Calcule $(2 \\times 10^3) \\times (3 \\times 10^4)$.","a":"$6 \\times 10^7$","options":["$6 \\times 10^7$","$6 \\times 10^{12}$","$5 \\times 10^7$"],"steps":["Coefficients : $2 \\times 3 = 6$","Exposants : $10^{3+4} = 10^7$","$= 6 \\times 10^7$"],"f":"$(a \\times 10^m)(b \\times 10^n) = ab \\times 10^{m+n}$"},
    {"lvl":2,"type":"vf","q":"$(5 \\times 10^3)^2 = 25 \\times 10^6 = 2{,}5 \\times 10^7$.","a":"Vrai","options":["Vrai","Faux"],"steps":["$(5 \\times 10^3)^2 = 5^2 \\times (10^3)^2$","$= 25 \\times 10^6$","$= 2{,}5 \\times 10^7$ (notation scientifique)"],"f":"$(a \\times 10^n)^p = a^p \\times 10^{np}$"},
    {"lvl":2,"q":"Calcule $\\frac{8 \\times 10^6}{4 \\times 10^2}$.","a":"$2 \\times 10^4$","options":["$2 \\times 10^4$","$2 \\times 10^3$","$4 \\times 10^4$"],"steps":["Coefficients : $\\frac{8}{4} = 2$","Exposants : $10^{6-2} = 10^4$","$= 2 \\times 10^4$"],"f":"$\\frac{a \\times 10^m}{b \\times 10^n} = \\frac{a}{b} \\times 10^{m-n}$"},
    {"lvl":2,"type":"fill","q":"Écris $0{,}0000052$ en notation scientifique : $5{,}2 \\times 10^{\\text{___}}$.","a":"-6","options":[],"steps":["On décale la virgule de $6$ positions à droite","$0{,}0000052 = 5{,}2 \\times 10^{-6}$","Exposant $-6$"],"f":"$a \\times 10^{-n}$"},
    {"lvl":2,"q":"Additionne $3 \\times 10^4+2 \\times 10^3$.","a":"$3{,}2 \\times 10^4$","options":["$3{,}2 \\times 10^4$","$5 \\times 10^4$","$5 \\times 10^7$"],"steps":["$3 \\times 10^4 = 30\\,000$ et $2 \\times 10^3 = 2\\,000$","$30\\,000+2\\,000 = 32\\,000$","$= 3{,}2 \\times 10^4$"],"f":"Pour additionner, mettre au même exposant"},

    # SLOT 4
    {"lvl":2,"q":"Un virus mesure $5 \\times 10^{-8}$ m. En nanomètres ($1$ nm $= 10^{-9}$ m) ?","a":"$50$ nm","options":["$50$ nm","$5$ nm","$500$ nm"],"steps":["$\\frac{5 \\times 10^{-8}}{10^{-9}} = 5 \\times 10^{-8-(-9)}$","$= 5 \\times 10^1$","$= 50$ nm"],"f":"Conversion : diviser par l'unité"},
    {"lvl":2,"type":"vf","q":"L'ordre de grandeur de $4\\,700$ est $10^4$.","a":"Vrai","options":["Vrai","Faux"],"steps":["$4\\,700 = 4{,}7 \\times 10^3$","$4{,}7 > 3{,}16$ (≈ $\\sqrt{10}$)","On arrondit à $10^4$ (convention : $\\geq \\sqrt{10}$ → exposant supérieur)"],"f":"Ordre de grandeur : puissance de $10$ la plus proche"},
    {"lvl":2,"q":"Masse proton : $1{,}67 \\times 10^{-27}$ kg. Masse électron : $9{,}1 \\times 10^{-31}$ kg. Le proton est combien de fois plus lourd ?","a":"Environ $1\\,836$ fois","options":["Environ $1\\,836$ fois","Environ $18$ fois","Environ $184$ fois"],"steps":["$\\frac{1{,}67 \\times 10^{-27}}{9{,}1 \\times 10^{-31}}$","$= \\frac{1{,}67}{9{,}1} \\times 10^{-27-(-31)} = 0{,}1835 \\times 10^4$","$\\approx 1\\,836$ fois"],"f":"$\\frac{a \\times 10^m}{b \\times 10^n} = \\frac{a}{b} \\times 10^{m-n}$"},
    {"lvl":2,"type":"fill","q":"$(2{,}5 \\times 10^3) \\times (4 \\times 10^{-5})$ en notation scientifique = $1 \\times 10^{\\text{___}}$.","a":"-1","options":[],"steps":["$2{,}5 \\times 4 = 10$","$10^{3+(-5)} = 10^{-2}$","$10 \\times 10^{-2} = 1 \\times 10^{-1}$"],"f":"$(a \\times 10^m)(b \\times 10^n) = ab \\times 10^{m+n}$"},
    {"lvl":2,"q":"Un satellite parcourt $3 \\times 10^4$ km en une orbite de $2 \\times 10^3$ secondes. Calcule le produit distance $\\times$ temps.","a":"$6 \\times 10^7$","options":["$6 \\times 10^7$","$6 \\times 10^{12}$","$5 \\times 10^7$"],"steps":["$(3 \\times 10^4) \\times (2 \\times 10^3)$","$= 6 \\times 10^{4+3}$","$= 6 \\times 10^7$ km·s"],"f":"$(a \\times 10^m)(b \\times 10^n) = ab \\times 10^{m+n}$"},
]


# ══════════════════════════════════════════════════════════════════════
# WRITE TO SHEET
# ══════════════════════════════════════════════════════════════════════

def validate_slot(exos, slot_idx):
    """Validate a slot of 5 exercises has 3Q+1V+1F and proper structure."""
    slot = exos[slot_idx*5:(slot_idx+1)*5]
    types = [e.get('type','qcm') for e in slot]
    from collections import Counter
    c = Counter(types)
    assert c.get('qcm',0) == 3, f"Slot {slot_idx+1}: expected 3 QCM, got {c.get('qcm',0)}"
    assert c.get('vf',0) == 1, f"Slot {slot_idx+1}: expected 1 VF, got {c.get('vf',0)}"
    assert c.get('fill',0) == 1, f"Slot {slot_idx+1}: expected 1 Fill, got {c.get('fill',0)}"

def validate_chapter(name, exos):
    assert len(exos) == 20, f"{name}: expected 20 exos, got {len(exos)}"
    for i in range(4):
        validate_slot(exos, i)
    # Check lvl: slots 0-1 = lvl 1, slots 2-3 = lvl 2
    for j in range(10):
        assert exos[j].get('lvl') == 1, f"{name} exo {j+1}: expected lvl 1"
    for j in range(10,20):
        assert exos[j].get('lvl') == 2, f"{name} exo {j+1}: expected lvl 2"
    # Check VF format
    for j, e in enumerate(exos):
        if e.get('type') == 'vf':
            assert e['a'] in ('Vrai','Faux'), f"{name} exo {j+1}: VF answer must be Vrai/Faux"
            assert e['options'] == ['Vrai','Faux'], f"{name} exo {j+1}: VF options must be ['Vrai','Faux']"
        if e.get('type') == 'fill':
            assert e['options'] == [] or e['options'] == [' '] or e['options'] == [], f"{name} exo {j+1}: Fill options must be []"
    print(f"  ✅ {name}: 20 exos, 4 slots validated (3Q+1V+1F, lvl OK)")

if __name__ == '__main__':
    print("=== Validation ===")
    for name, exos in NEW_EXOS.items():
        validate_chapter(name, exos)

    print("\n=== Writing to sheet ===")
    for name, row_num in CHAPTERS_3EME.items():
        titre_map = {
            "Calcul littéral": "Calcul littéral",
            "Équations": "Équations",
            "Fonctions": "Fonctions",
            "Théorème de Thalès": "Théorème de Thalès",
            "Trigonométrie": "Trigonométrie",
            "Statistiques": "Statistiques",
            "Probabilités": "Probabilités",
            "Racines carrées": "Racines carrées",
            "Systèmes d'équations": "Systèmes d'équations",
            "Inéquations": "Inéquations",
            "Notation scientifique": "Notation scientifique",
        }
        exos = NEW_EXOS[titre_map[name]]
        write_chapter(row_num, exos)
        print(f"  ✅ {name} (row {row_num}) written")

    print("\n=== DONE ===")
