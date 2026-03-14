#!/usr/bin/env python3
"""
insert_1ere.py — Insère le niveau 1ERE Spé Maths + compte Auguste.
Idempotent : nettoie les données 1ERE existantes avant réinsertion.
Usage : python3 insert_1ere.py
"""

import json, hashlib, random, sys
from datetime import date, timedelta
from sheets import sh

TODAY = date.today().isoformat()
YESTERDAY = (date.today() - timedelta(days=1)).isoformat()
TOMORROW_30 = (date.today() + timedelta(days=30)).isoformat()

# ════════════════════════════════════════════════════════════
#  CHAPITRES 1ERE
# ════════════════════════════════════════════════════════════

CHAPTERS = [
    ("Second_Degre",         "Second degré 📐",                "📐"),
    ("Suites",               "Suites numériques 🔢",           "🔢"),
    ("Derivation",           "Dérivation 📈",                  "📈"),
    ("Exponentielle",        "Fonction exponentielle 🌿",      "🌿"),
    ("Trigonometrie",        "Trigonométrie 🔵",               "🔵"),
    ("Produit_Scalaire",     "Produit scalaire ✕",             "✕"),
    ("Geometrie_Repere",     "Géométrie repérée 📍",           "📍"),
    ("Probabilites_Cond",    "Probabilités conditionnelles 🎲","🎲"),
    ("Variables_Aleatoires", "Variables aléatoires 🎯",        "🎯"),
    ("Algorithmique",        "Algorithmique & Python 💻",      "💻"),
]

# ════════════════════════════════════════════════════════════
#  GÉNÉRATEURS D'EXERCICES PAR CHAPITRE
# ════════════════════════════════════════════════════════════

def _exo(lvl, q, a, opts, f, steps):
    """Construit un dict exercice. Valide que a ∈ options."""
    assert a in opts, f"BUG: a={a!r} pas dans options={opts!r} (q={q[:60]})"
    return {"lvl": lvl, "q": q, "a": a, "options": opts, "f": f, "steps": steps}

def _gen_second_degre(variant=0):
    """20 exercices Second degré."""
    V = variant  # décalage pour varier entre curriculum/diag/boost
    exos = []
    # lvl 1 — 10 exos
    params_l1 = [
        (1+V, -3-V, 2+V), (2+V, 5+V, -3-V), (1, -4-V, 4+V), (3+V, -6, 1),
        (1, 2+V, -8-V), (2, -7-V, 3+V), (1, -1-V, -6-V), (4+V, -4, 1),
        (1, 6+V, 9+V), (1, -2-V, -15-V)
    ]
    for i, (a, b, c) in enumerate(params_l1):
        delta = b*b - 4*a*c
        if i % 5 == 0:
            exos.append(_exo(1,
                f"Calculer le discriminant de $f(x) = {a}x^2 {b:+d}x {c:+d}$.",
                f"$\\Delta = {delta}$",
                [f"$\\Delta = {delta}$", f"$\\Delta = {abs(delta-4)}$", f"$\\Delta = {b*b}$"],
                "$\\Delta = b^2 - 4ac$",
                ["Identifier $a$, $b$, $c$.", f"$\\Delta = ({b})^2 - 4 \\times {a} \\times ({c})$.", f"$\\Delta = {b*b} - {4*a*c}$."]
            ))
        elif i % 5 == 1:
            exos.append(_exo(1,
                f"Donner la forme canonique de $f(x) = x^2 {b:+d}x {c:+d}$.",
                f"$f(x) = (x {-b/2:+.1f})^2 {c - b*b/4:+.1f}$",
                [f"$f(x) = (x {-b/2:+.1f})^2 {c - b*b/4:+.1f}$", f"$f(x) = (x {b/2:+.1f})^2 {c:+d}$", f"$f(x) = (x {-b:+d})^2 + {c}$"],
                "$f(x) = a(x - \\alpha)^2 + \\beta$ avec $\\alpha = -\\frac{b}{2a}$",
                ["Calculer $\\alpha = -b/(2a)$.", f"$\\alpha = {-b/2:.1f}$.", "Développer et identifier $\\beta$."]
            ))
        elif i % 5 == 2:
            if delta > 0:
                import math
                x1 = (-b - math.sqrt(delta)) / (2*a)
                x2 = (-b + math.sqrt(delta)) / (2*a)
                exos.append(_exo(1,
                    f"Résoudre $x^2 {b:+d}x {c:+d} = 0$.",
                    f"$x_1 = {x1:.2f}$ et $x_2 = {x2:.2f}$",
                    [f"$x_1 = {x1:.2f}$ et $x_2 = {x2:.2f}$", f"$x = {-b/(2*a):.2f}$", "Pas de solution"],
                    "$x = \\frac{-b \\pm \\sqrt{\\Delta}}{2a}$",
                    ["Calculer $\\Delta$.", f"$\\Delta = {delta}$, donc 2 racines.", "Appliquer la formule."]
                ))
            else:
                exos.append(_exo(1,
                    f"Combien de racines a $f(x) = {a}x^2 {b:+d}x {c:+d}$ ?",
                    "Aucune racine réelle",
                    ["Aucune racine réelle", "Une racine double", "Deux racines"],
                    "$\\Delta < 0 \\Rightarrow$ pas de racine réelle",
                    ["Calculer $\\Delta$.", f"$\\Delta = {delta} < 0$.", "Conclure."]
                ))
        elif i % 5 == 3:
            exos.append(_exo(1,
                f"Le sommet de la parabole $y = {a}x^2 {b:+d}x {c:+d}$ a pour abscisse :",
                f"$x_S = {-b/(2*a):.2f}$",
                [f"$x_S = {-b/(2*a):.2f}$", f"$x_S = {b/(2*a):.2f}$", f"$x_S = {-b:.0f}$"],
                "$x_S = -\\frac{b}{2a}$",
                ["Formule du sommet.", f"$a={a}$, $b={b}$.", f"$x_S = -({b})/(2 \\times {a})$."]
            ))
        else:
            sign = "positif" if a > 0 else "négatif"
            exos.append(_exo(1,
                f"Quel est le signe de $f(x) = {a}x^2 {b:+d}x {c:+d}$ pour $x$ grand ?",
                f"$f(x) \\to +\\infty$" if a > 0 else f"$f(x) \\to -\\infty$",
                [f"$f(x) \\to +\\infty$" if a > 0 else f"$f(x) \\to -\\infty$",
                 f"$f(x) \\to 0$", f"$f(x) \\to -\\infty$" if a > 0 else f"$f(x) \\to +\\infty$"],
                "Le signe de $f(x)$ pour $|x|$ grand est celui de $a$.",
                [f"$a = {a}$.", f"$a$ est {sign}.", "Donc $f(x)$ tend vers $+\\infty$." if a > 0 else "Donc $f(x)$ tend vers $-\\infty$."]
            ))

    # lvl 2 — 10 exos
    params_l2 = [
        (1, -5-V, 6+V), (2+V, -3, -2-V), (1, -2*V-4, V*V+4*V+3),
        (1, -6-V, 8+V), (3, 2+V, -1-V), (1, V+1, -V-2),
        (2, -4-V, V+1), (1, -3-V, -4-V), (1, 2+V, 1+V), (1, -8-V, 15+V)
    ]
    for i, (a, b, c) in enumerate(params_l2):
        delta = b*b - 4*a*c
        if i < 3:
            exos.append(_exo(2,
                f"Résoudre l'inéquation ${a}x^2 {b:+d}x {c:+d} \\geq 0$.",
                f"Étudier le signe selon $\\Delta = {delta}$",
                [f"Étudier le signe selon $\\Delta = {delta}$", "$x \\in \\mathbb{{R}}$", "$\\emptyset$"],
                "Tableau de signes du trinôme : signe de $a$ à l'extérieur des racines.",
                ["Calculer $\\Delta$.", "Trouver les racines si $\\Delta \\geq 0$.", "Dresser le tableau de signes."]
            ))
        elif i < 5:
            exos.append(_exo(2,
                f"On lance un objet. Sa hauteur est $h(t) = -{a}t^2 {b:+d}t {c:+d}$. Quand atteint-il sa hauteur max ?",
                f"$t = {-b/(2*(-a)):.2f}$ s",
                [f"$t = {-b/(2*(-a)):.2f}$ s", f"$t = {b:.0f}$ s", f"$t = {-c/b:.2f}$ s"],
                "$t_{max} = -\\frac{b}{2a}$",
                ["$h(t)$ est un trinôme du 2nd degré.", "Le max est au sommet.", "Appliquer la formule du sommet."]
            ))
        elif i < 7:
            exos.append(_exo(2,
                f"Déterminer $m$ pour que $x^2 {b:+d}x + m = 0$ ait une racine double.",
                f"$m = {b*b//4}$",
                [f"$m = {b*b//4}$", f"$m = {b}$", f"$m = {b*b}$"],
                "$\\Delta = 0 \\Leftrightarrow b^2 - 4ac = 0$",
                ["Racine double ⟺ $\\Delta = 0$.", f"$\\Delta = ({b})^2 - 4m = 0$.", "Isoler $m$."]
            ))
        elif i < 9:
            exos.append(_exo(2,
                f"Factoriser $P(x) = {a}x^2 {b:+d}x {c:+d}$ sachant que $\\Delta = {delta}$.",
                f"$P(x) = {a}(x - x_1)(x - x_2)$" if delta > 0 else f"$P(x) = {a}(x {b/(2*a):+.1f})^2$",
                [f"$P(x) = {a}(x - x_1)(x - x_2)$" if delta > 0 else f"$P(x) = {a}(x {b/(2*a):+.1f})^2$",
                 f"$(x {b:+d})(x {c:+d})$", f"Non factorisable$"],
                "$P(x) = a(x - x_1)(x - x_2)$ si $\\Delta > 0$",
                ["Vérifier le signe de $\\Delta$.", "Calculer les racines.", "Écrire la forme factorisée."]
            ))
        else:
            exos.append(_exo(2,
                f"La somme et le produit des racines de $x^2 {b:+d}x {c:+d} = 0$ valent :",
                f"$S = {-b}$, $P = {c}$",
                [f"$S = {-b}$, $P = {c}$", f"$S = {b}$, $P = {-c}$", f"$S = {c}$, $P = {b}$"],
                "$S = -b/a$, $P = c/a$",
                ["Relations de Viète.", "$S = -b/a$ et $P = c/a$.", f"Ici $a=1$, $b={b}$, $c={c}$."]
            ))
    return exos[:20]


def _gen_suites(variant=0):
    V = variant
    exos = []
    # lvl 1
    for i in range(10):
        if i == 0:
            u0, r = 3+V, 5+V
            exos.append(_exo(1, f"$(u_n)$ est arithmétique avec $u_0 = {u0}$ et $r = {r}$. Calculer $u_{{10}}$.",
                f"$u_{{10}} = {u0 + 10*r}$",
                [f"$u_{{10}} = {u0 + 10*r}$", f"$u_{{10}} = {u0 + 9*r}$", f"$u_{{10}} = {u0*10 + r}$"],
                "$u_n = u_0 + nr$",
                ["Suite arithmétique : $u_n = u_0 + nr$.", f"$u_{{10}} = {u0} + 10 \\times {r}$.", "Calculer."]))
        elif i == 1:
            u0, q = 2+V, 3+V
            exos.append(_exo(1, f"$(v_n)$ est géométrique avec $v_0 = {u0}$ et $q = {q}$. Calculer $v_3$.",
                f"$v_3 = {u0 * q**3}$",
                [f"$v_3 = {u0 * q**3}$", f"$v_3 = {u0 * q * 3}$", f"$v_3 = {u0 + 3*q}$"],
                "$v_n = v_0 \\times q^n$",
                ["Suite géométrique : $v_n = v_0 q^n$.", f"$v_3 = {u0} \\times {q}^3$.", "Calculer."]))
        elif i == 2:
            exos.append(_exo(1, f"$u_n = 2n + {3+V}$. La suite est-elle arithmétique ?",
                "Oui, de raison $r = 2$",
                ["Oui, de raison $r = 2$", "Oui, de raison $r = " + str(3+V) + "$", "Non"],
                "$u_{{n+1}} - u_n = \\text{cte} \\Rightarrow$ arithmétique",
                ["Calculer $u_{n+1} - u_n$.", f"$u_{{n+1}} - u_n = 2(n+1)+{3+V} - (2n+{3+V})$.", "$= 2$, constant."]))
        elif i == 3:
            u0, r, n = 1+V, 4+V, 5+V
            S = (n+1)*(2*u0 + n*r)//2
            exos.append(_exo(1, f"Calculer $S = u_0 + u_1 + \\ldots + u_{{{n}}}$ avec $u_0={u0}$, $r={r}$.",
                f"$S = {S}$",
                [f"$S = {S}$", f"$S = {(n+1)*u0}$", f"$S = {n*r}$"],
                "$S = \\frac{(n+1)(u_0 + u_n)}{2}$",
                ["Nombre de termes : $n+1$.", f"$u_{n} = {u0 + n*r}$.", "Appliquer la formule."]))
        elif i == 4:
            exos.append(_exo(1, f"$u_{{n+1}} = u_n + {2+V}$, $u_0 = {V+1}$. Exprimer $u_n$ en fonction de $n$.",
                f"$u_n = {2+V}n + {V+1}$",
                [f"$u_n = {2+V}n + {V+1}$", f"$u_n = {V+1}n + {2+V}$", f"$u_n = ({2+V})^n$"],
                "Suite arithmétique : $u_n = u_0 + nr$",
                ["Identifier : $r = " + str(2+V) + "$.", "$u_0 = " + str(V+1) + "$.", "Appliquer $u_n = u_0 + nr$."]))
        elif i == 5:
            q = 2 + V
            exos.append(_exo(1, f"$v_0 = 1$, $v_{{n+1}} = {q} v_n$. Quelle est la nature de $(v_n)$ ?",
                f"Géométrique de raison $q = {q}$",
                [f"Géométrique de raison $q = {q}$", f"Arithmétique de raison $r = {q}$", "Ni l'un ni l'autre"],
                "$v_{{n+1}} = q \\cdot v_n \\Rightarrow$ géométrique",
                ["$v_{n+1}/v_n = ?$", f"$= {q}$, constant.", "Donc géométrique."]))
        elif i == 6:
            exos.append(_exo(1, f"$u_n = (-1)^n$. La suite est-elle monotone ?",
                "Non, elle alterne entre $1$ et $-1$",
                ["Non, elle alterne entre $1$ et $-1$", "Oui, croissante", "Oui, décroissante"],
                "Une suite monotone est toujours croissante ou toujours décroissante.",
                ["Calculer $u_0, u_1, u_2$.", "$u_0=1, u_1=-1, u_2=1$.", "Pas monotone."]))
        elif i == 7:
            a, b = 3+V, 2+V
            exos.append(_exo(1, f"$u_n = \\frac{{{a}n+1}}{{{b}n+{V+3}}}$. Que vaut $\\lim_{{n \\to +\\infty}} u_n$ ?",
                f"$\\frac{{{a}}}{{{b}}}$",
                [f"$\\frac{{{a}}}{{{b}}}$", "$+\\infty$", "$0$"],
                "Limite = rapport des coefficients dominants.",
                ["Diviser num. et dén. par $n$.", "Les termes $1/n$ tendent vers $0$.", f"$\\lim = {a}/{b}$."]))
        elif i == 8:
            r = 3 + V
            exos.append(_exo(1, f"Si $u_n = {r}n - 1$, que vaut $u_5 - u_3$ ?",
                f"${2*r}$",
                [f"${2*r}$", f"${r}$", f"${5*r - 3*r - 1}$"],
                "$u_p - u_q = (p-q)r$ pour une suite arithmétique.",
                ["$u_5 = " + str(5*r-1) + "$.", "$u_3 = " + str(3*r-1) + "$.", "Soustraire."]))
        else:
            q = V + 2
            exos.append(_exo(1, f"$v_n = 3 \\times {q}^n$. Calculer $v_0 + v_1 + v_2$.",
                f"${3 + 3*q + 3*q**2}$",
                [f"${3 + 3*q + 3*q**2}$", f"${3*3*q}$", f"${3*q**3}$"],
                "$S = v_0 \\frac{1 - q^n}{1 - q}$",
                ["Calculer chaque terme.", f"$v_0={3}, v_1={3*q}, v_2={3*q**2}$.", "Additionner."]))

    # lvl 2
    for i in range(10):
        if i == 0:
            exos.append(_exo(2, f"Montrer par récurrence que $u_n = 2^n + {V+1}$ vérifie $u_{{n+1}} = 2u_n - {V+1}$.",
                "Vrai par calcul direct",
                ["Vrai par calcul direct", "Faux", "Vrai seulement pour $n$ pair"],
                "Récurrence : vérifier P(0), supposer P(n), montrer P(n+1).",
                ["Calculer $2u_n - " + str(V+1) + "$.", f"$= 2(2^n + {V+1}) - {V+1} = 2^{{n+1}} + {V+1}$.", "$= u_{n+1}$. ✓"]))
        elif i == 1:
            u0, r = 100+V*10, -(5+V)
            n = -(u0 // r)
            exos.append(_exo(2, f"$u_n = {u0} {r:+d}n$. À partir de quel rang $u_n < 0$ ?",
                f"$n \\geq {int(-u0/r)+1}$",
                [f"$n \\geq {int(-u0/r)+1}$", f"$n \\geq {int(-u0/r)}$", f"$n \\geq {u0}$"],
                "Résoudre $u_n < 0$.",
                ["$" + str(u0) + str(r) + "n < 0$.", f"$n > {-u0/r:.1f}$.", "Premier entier au-dessus."]))
        elif i == 2:
            q = V + 2
            exos.append(_exo(2, f"$v_0 = 1$, $q = {q}$. Calculer $S = \\sum_{{k=0}}^{{6}} v_k$.",
                f"$S = \\frac{{{1-q**7}}}{{{1-q}}}$",
                [f"$S = \\frac{{{1-q**7}}}{{{1-q}}}$", f"$S = 7 \\times {q}$", f"$S = {q}^7$"],
                "$S = v_0 \\frac{1-q^{n+1}}{1-q}$",
                ["7 termes ($k=0$ à $6$).", "Appliquer la formule de somme géométrique.", "Calculer."]))
        elif i == 3:
            exos.append(_exo(2, f"$(u_n)$ arithmétique, $u_2 = {7+V}$ et $u_5 = {16+V}$. Trouver $u_0$ et $r$.",
                f"$r = 3$, $u_0 = {1+V}$",
                [f"$r = 3$, $u_0 = {1+V}$", f"$r = {9+V}$, $u_0 = 0$", f"$r = 2$, $u_0 = {3+V}$"],
                "$u_p - u_q = (p-q)r$",
                ["$u_5 - u_2 = 3r$.", f"$3r = {16+V} - {7+V} = 9$, $r = 3$.", f"$u_0 = u_2 - 2r = {7+V} - 6 = {1+V}$."]))
        elif i < 6:
            exos.append(_exo(2, f"$u_n = n^2 - {4+V}n$. Étudier le sens de variation.",
                "Décroissante puis croissante",
                ["Décroissante puis croissante", "Toujours croissante", "Toujours décroissante"],
                "Étudier le signe de $u_{n+1} - u_n$.",
                ["$u_{n+1} - u_n = 2n + 1 - " + str(4+V) + "$.", f"$= 0$ quand $n = {(3+V)/2:.1f}$.", "Signe change : décroissante puis croissante."]))
        elif i < 8:
            exos.append(_exo(2, f"Un capital de ${1000+V*100}$€ est placé à ${2+V}$% par an. Quelle est sa valeur après 5 ans ?",
                f"${1000+V*100} \\times {1+(2+V)/100:.2f}^5$",
                [f"${1000+V*100} \\times {1+(2+V)/100:.2f}^5$", f"${1000+V*100} + 5 \\times {(1000+V*100)*(2+V)//100}$", f"${1000+V*100} \\times 5$"],
                "Suite géométrique : $C_n = C_0 \\times (1+t)^n$.",
                ["Taux : $t = " + str((2+V)/100) + "$.", "$C_n = C_0 \\times (1+t)^n$.", "Calculer $C_5$."]))
        else:
            exos.append(_exo(2, f"$u_0 = {V+2}$, $u_{{n+1}} = \\sqrt{{u_n + {V+6}}}$. Conjecturer la limite.",
                f"$\\ell = \\frac{{1+\\sqrt{{{1+4*(V+6)}}}}}{{2}}$",
                [f"$\\ell = \\frac{{1+\\sqrt{{{1+4*(V+6)}}}}}{{2}}$", "$\\ell = " + str(V+6) + "$", "$+\\infty$"],
                "Si $\\ell$ existe : $\\ell = \\sqrt{\\ell + c}$, donc $\\ell^2 - \\ell - c = 0$.",
                ["Supposer $u_n \\to \\ell$.", "$\\ell^2 = \\ell + " + str(V+6) + "$.", "Résoudre l'équation du 2nd degré."]))
    return exos[:20]


def _gen_derivation(variant=0):
    V = variant
    exos = []
    # lvl 1
    derivees = [
        (f"$f(x) = x^{3+V}$", f"$f'(x) = {3+V}x^{2+V}$", f"${3+V}x^{2+V}$", f"${2+V}x^{3+V}$", f"$x^{2+V}$", "$(x^n)' = nx^{n-1}$"),
        (f"$f(x) = {2+V}x^2 + {3+V}x - 1$", f"$f'(x) = {2*(2+V)}x + {3+V}$", f"${2*(2+V)}x + {3+V}$", f"${2+V}x + {3+V}$", f"${2*(2+V)}x$", "$(ax^2+bx+c)' = 2ax+b$"),
        (f"$f(x) = \\frac{{1}}{{x}}$", "$f'(x) = -\\frac{1}{x^2}$", "$-\\frac{1}{x^2}$", "$\\frac{1}{x^2}$", "$-\\frac{1}{x}$", "$(1/x)' = -1/x^2$"),
        (f"$f(x) = \\sqrt{{x}}$", "$f'(x) = \\frac{1}{2\\sqrt{x}}$", "$\\frac{1}{2\\sqrt{x}}$", "$\\frac{1}{\\sqrt{x}}$", "$2\\sqrt{x}$", "$(\\sqrt{x})' = \\frac{1}{2\\sqrt{x}}$"),
        (f"$f(x) = e^x$", "$f'(x) = e^x$", "$e^x$", "$xe^{x-1}$", "$e^{x-1}$", "$(e^x)' = e^x$"),
        (f"$f(x) = {3+V}e^x + {2+V}$", f"$f'(x) = {3+V}e^x$", f"${3+V}e^x$", f"$e^x + {2+V}$", f"${3+V}e^x + {2+V}$", "$(ke^x)' = ke^x$, constante disparaît"),
        (f"$f(x) = {2+V}x^3 - x$", f"$f'(x) = {3*(2+V)}x^2 - 1$", f"${3*(2+V)}x^2 - 1$", f"${2*(2+V)}x^2 - 1$", f"${3*(2+V)}x^3$", "Dériver terme à terme."),
        (f"$f(x) = (x+{V+1})^2$", f"$f'(x) = 2(x+{V+1})$", f"$2(x+{V+1})$", f"$2x+{V+1}$", f"$(x+{V+1})$", "Développer puis dériver, ou $(u^2)'=2u'u$."),
        (f"$f(x) = \\sin(x)$", "$f'(x) = \\cos(x)$", "$\\cos(x)$", "$-\\sin(x)$", "$-\\cos(x)$", "$(\\sin x)' = \\cos x$"),
        (f"$f(x) = \\cos(x)$", "$f'(x) = -\\sin(x)$", "$-\\sin(x)$", "$\\sin(x)$", "$\\cos(x)$", "$(\\cos x)' = -\\sin x$"),
    ]
    for func, deriv, good, bad1, bad2, form in derivees:
        exos.append(_exo(1, f"Dériver {func}.",
            good, [good, bad1, bad2], form,
            ["Identifier le type de fonction.", "Appliquer la formule de dérivation.", "Simplifier."]))

    # lvl 2
    l2 = [
        ("Équation de la tangente à $f(x) = x^2$ en $x_0 = " + str(1+V) + "$.",
         f"$y = {2*(1+V)}x - {(1+V)**2}$",
         [f"$y = {2*(1+V)}x - {(1+V)**2}$", f"$y = {2*(1+V)}x$", f"$y = x - {(1+V)**2}$"],
         "$y = f'(a)(x-a)+f(a)$",
         [f"$f'(x)=2x$, $f'({1+V})={2*(1+V)}$.", f"$f({1+V})={(1+V)**2}$.", "Appliquer $y=f'(a)(x-a)+f(a)$."]),
        (f"$f(x) = x^3 - {3+V}x$. Trouver les extrema.",
         f"$x = \\pm\\sqrt{{\\frac{{{3+V}}}{{3}}}}$",
         [f"$x = \\pm\\sqrt{{\\frac{{{3+V}}}{{3}}}}$", f"$x = \\pm{3+V}$", f"$x = 0$"],
         "$f'(x) = 0$ aux extrema.",
         ["Dériver.", f"$3x^2 = {3+V}$.", "Résoudre et vérifier le signe de $f'$."]),
        (f"$f(x) = xe^x$. Calculer $f'(x)$.",
         "$(1+x)e^x$",
         ["$(1+x)e^x$", "$xe^x + 1$", "$e^x$"],
         "$(uv)' = u'v + uv'$",
         ["$u=x$, $v=e^x$.", "$u'=1$, $v'=e^x$.", "$f' = e^x + xe^x = (1+x)e^x$."]),
        (f"$f(x) = \\frac{{x+{V+1}}}{{x-1}}$. Calculer $f'(x)$.",
         f"$\\frac{{-{V+2}}}{{(x-1)^2}}$",
         [f"$\\frac{{-{V+2}}}{{(x-1)^2}}$", f"$\\frac{{1}}{{(x-1)^2}}$", f"$\\frac{{{V+1}}}{{x-1}}$"],
         "$(u/v)' = (u'v - uv')/v^2$",
         ["$u = x+{0}$, $v = x-1$.".format(V+1), "$u'v - uv' = 1(x-1) - (x+{0})$.".format(V+1), f"$= -{V+2}$."]),
        (f"Dresser le tableau de variation de $f(x) = -x^2 + {2*(V+2)}x$ sur $\\mathbb{{R}}$.",
         f"Croissante puis décroissante, max en $x={V+2}$",
         [f"Croissante puis décroissante, max en $x={V+2}$", "Toujours décroissante", f"Décroissante puis croissante, min en $x={V+2}$"],
         "$f'(x) = 0$ donne le sommet, $a<0$ → max.",
         [f"$f'(x) = -2x + {2*(V+2)}$.", f"$f'(x) = 0 \\Rightarrow x = {V+2}$.", "$a = -1 < 0$ → maximum."]),
    ]
    for q, a, opts, f, steps in l2:
        exos.append(_exo(2, q, a, opts, f, steps))

    # Compléter à 10 lvl2
    for i in range(5):
        k = 2 + V + i
        exos.append(_exo(2, f"$f(x) = (x^2+{k})e^x$. Signe de $f'(0)$ ?",
            f"Positif ($f'(0) = {k}$)",
            [f"Positif ($f'(0) = {k}$)", "Négatif", "Nul"],
            "$(uv)' = u'v + uv'$",
            [f"$f'(x) = (2x)e^x + (x^2+{k})e^x$.", "$f'(x) = (x^2+2x+{0})e^x$.".format(k), f"$f'(0) = {k} > 0$."]))
    return exos[:20]


def _gen_exponentielle(variant=0):
    V = variant
    exos = []
    # lvl 1
    l1_data = [
        (f"Simplifier $e^{{{2+V}}} \\times e^{{{3+V}}}$.", f"$e^{{{5+2*V}}}$",
         [f"$e^{{{5+2*V}}}$", f"$e^{{{(2+V)*(3+V)}}}$", f"${2+V}e^{{{3+V}}}$"],
         "$e^a \\times e^b = e^{a+b}$"),
        (f"Simplifier $\\frac{{e^{{{5+V}}}}}{{e^{{{2+V}}}}}$.", "$e^3$",
         ["$e^3$", f"$e^{{{(5+V)//(2+V)}}}$", f"$e^{{{(5+V)*(2+V)}}}$"],
         "$e^a / e^b = e^{a-b}$"),
        ("Que vaut $e^0$ ?", "$1$", ["$1$", "$0$", "$e$"], "$e^0 = 1$ pour tout réel."),
        (f"Simplifier $(e^{{{V+2}}})^3$.", f"$e^{{{3*(V+2)}}}$",
         [f"$e^{{{3*(V+2)}}}$", f"$3e^{{{V+2}}}$", f"$e^{{{(V+2)**3}}}$"],
         "$(e^a)^n = e^{na}$"),
        (f"Résoudre $e^x = e^{{{V+3}}}$.", f"$x = {V+3}$",
         [f"$x = {V+3}$", f"$x = \\ln({V+3})$", "$x = 1$"],
         "$e^a = e^b \\Leftrightarrow a = b$"),
        ("La fonction $e^x$ est-elle croissante ou décroissante ?", "Croissante sur $\\mathbb{R}$",
         ["Croissante sur $\\mathbb{R}$", "Décroissante sur $\\mathbb{R}$", "Croissante sur $]0;+\\infty[$ seulement"],
         "$(e^x)' = e^x > 0$ pour tout $x$."),
        (f"Calculer $e^{{{V+1}}} \\times e^{{-{V+1}}}$.", "$1$",
         ["$1$", "$0$", "$e^0 = 0$"],
         "$e^a \\times e^{-a} = e^0 = 1$"),
        (f"Que vaut $\\lim_{{x \\to +\\infty}} e^x$ ?", "$+\\infty$",
         ["$+\\infty$", "$0$", "$1$"], "$\\lim_{x \\to +\\infty} e^x = +\\infty$"),
        (f"Que vaut $\\lim_{{x \\to -\\infty}} e^x$ ?", "$0$",
         ["$0$", "$-\\infty$", "$1$"], "$\\lim_{x \\to -\\infty} e^x = 0$"),
        (f"Résoudre $e^{{2x}} = e^{{{2*(V+1)}}}$.", f"$x = {V+1}$",
         [f"$x = {V+1}$", f"$x = {2*(V+1)}$", f"$x = \\frac{{e^{{{2*(V+1)}}}}}{{2}}$"],
         "$e^{2x} = e^k \\Leftrightarrow 2x = k$"),
    ]
    for q, a, opts, f in l1_data:
        exos.append(_exo(1, q, a, opts, f, ["Identifier la propriété de l'exponentielle.", "Appliquer la règle.", "Simplifier."]))

    # lvl 2
    l2_data = [
        (f"Résoudre $e^{{2x}} - {V+3}e^x + {V+2} = 0$.", "Poser $X = e^x$ et résoudre le trinôme",
         ["Poser $X = e^x$ et résoudre le trinôme", f"$x = {V+2}$", f"$x = \\ln({V+3})$"],
         "Changement de variable $X = e^x$ → équation du 2nd degré."),
        (f"Étudier le signe de $f(x) = e^x - {V+2}$.",
         f"$f(x) > 0$ si $x > \\ln({V+2})$",
         [f"$f(x) > 0$ si $x > \\ln({V+2})$", "$f(x) > 0$ pour tout $x$", f"$f(x) > 0$ si $x > {V+2}$"],
         "$e^x > k \\Leftrightarrow x > \\ln(k)$ si $k > 0$."),
        (f"Dériver $f(x) = x e^{{-x}}$.",
         "$(1-x)e^{-x}$",
         ["$(1-x)e^{-x}$", "$-xe^{-x}$", "$e^{-x}$"],
         "$(uv)' = u'v + uv'$, $(e^{-x})' = -e^{-x}$."),
        (f"$f(x) = e^{{2x}} - {2*(V+2)}e^x + {(V+2)**2 - 1}$. Résoudre $f(x) = 0$.",
         f"$x = \\ln({V+1})$ ou $x = \\ln({V+3})$",
         [f"$x = \\ln({V+1})$ ou $x = \\ln({V+3})$", f"$x = {V+1}$", "Pas de solution"],
         "Poser $X = e^x$, discriminant du trinôme."),
        (f"Montrer que $\\lim_{{x \\to +\\infty}} xe^{{-x}} = 0$.",
         "Croissance comparée : $e^x \\gg x$",
         ["Croissance comparée : $e^x \\gg x$", "$= +\\infty$", "$= 1$"],
         "$\\lim_{x \\to +\\infty} \\frac{x}{e^x} = 0$"),
        (f"Population modélisée par $P(t) = {1000+V*200} e^{{0.0{V+2}t}}$. Temps de doublement ?",
         f"$t = \\frac{{\\ln 2}}{{0.0{V+2}}}$",
         [f"$t = \\frac{{\\ln 2}}{{0.0{V+2}}}$", f"$t = \\frac{{2}}{{0.0{V+2}}}$", f"$t = {1000+V*200}$"],
         "$P(t) = 2P(0) \\Rightarrow e^{kt} = 2 \\Rightarrow t = \\ln 2 / k$."),
        (f"Résoudre $e^x \\geq {V+1}$.", f"$x \\geq \\ln({V+1})$",
         [f"$x \\geq \\ln({V+1})$", f"$x \\geq {V+1}$", "$x \\geq 0$"],
         "$e^x \\geq k \\Leftrightarrow x \\geq \\ln(k)$ ($k > 0$, $e^x$ croissante)."),
        (f"Étudier les variations de $f(x) = e^{{2x}} - {2+V}x$.",
         "Décroissante puis croissante",
         ["Décroissante puis croissante", "Toujours croissante", "Croissante puis décroissante"],
         "$f'(x) = 2e^{2x} - k$, s'annule quand $e^{2x} = k/2$."),
        (f"Simplifier $\\ln(e^{{{V+3}}})$.", f"${V+3}$",
         [f"${V+3}$", f"$e^{{{V+3}}}$", f"$\\frac{{{V+3}}}{{e}}$"],
         "$\\ln(e^a) = a$"),
        (f"Vrai ou faux : $e^{{a+b}} = e^a + e^b$ ?", "Faux",
         ["Faux", "Vrai", "Vrai seulement si $a=b$"],
         "$e^{a+b} = e^a \\cdot e^b \\neq e^a + e^b$ en général."),
    ]
    for q, a, opts, f in l2_data:
        exos.append(_exo(2, q, a, opts, f, ["Identifier la propriété.", "Appliquer.", "Conclure."]))
    return exos[:20]


def _gen_trigo(variant=0):
    V = variant
    exos = []
    vals = [
        ("Que vaut $\\cos(0)$ ?", "$1$", ["$1$", "$0$", "$-1$"]),
        ("Que vaut $\\sin(\\pi/6)$ ?", "$1/2$", ["$1/2$", "$\\sqrt{3}/2$", "$\\sqrt{2}/2$"]),
        ("Que vaut $\\cos(\\pi/4)$ ?", "$\\sqrt{2}/2$", ["$\\sqrt{2}/2$", "$1/2$", "$\\sqrt{3}/2$"]),
        ("Que vaut $\\sin(\\pi/2)$ ?", "$1$", ["$1$", "$0$", "$1/2$"]),
        ("Que vaut $\\cos(\\pi)$ ?", "$-1$", ["$-1$", "$1$", "$0$"]),
        ("Que vaut $\\sin(\\pi/3)$ ?", "$\\sqrt{3}/2$", ["$\\sqrt{3}/2$", "$1/2$", "$\\sqrt{2}/2$"]),
        ("Que vaut $\\cos(\\pi/3)$ ?", "$1/2$", ["$1/2$", "$\\sqrt{3}/2$", "$0$"]),
        ("Que vaut $\\sin(\\pi)$ ?", "$0$", ["$0$", "$1$", "$-1$"]),
        ("Que vaut $\\cos(\\pi/6)$ ?", "$\\sqrt{3}/2$", ["$\\sqrt{3}/2$", "$1/2$", "$\\sqrt{2}/2$"]),
        (f"Quelle est la période de $\\cos(x)$ ?", "$2\\pi$", ["$2\\pi$", "$\\pi$", "$\\pi/2$"]),
    ]
    for q, a, opts in vals:
        exos.append(_exo(1, q, a, opts, "Valeurs remarquables du cercle trigonométrique.",
            ["Placer l'angle sur le cercle trigo.", "Lire la coordonnée.", "Conclure."]))

    # lvl 2
    l2 = [
        (f"Résoudre $\\cos(x) = \\frac{{1}}{{2}}$ sur $[0; 2\\pi]$.", "$x = \\pi/3$ ou $x = 5\\pi/3$",
         ["$x = \\pi/3$ ou $x = 5\\pi/3$", "$x = \\pi/6$", "$x = \\pi/3$ uniquement"],
         "$\\cos(x) = \\cos(a) \\Leftrightarrow x = \\pm a + 2k\\pi$"),
        (f"Résoudre $\\sin(x) = \\frac{{\\sqrt{{2}}}}{{2}}$ sur $[0; 2\\pi]$.", "$x = \\pi/4$ ou $x = 3\\pi/4$",
         ["$x = \\pi/4$ ou $x = 3\\pi/4$", "$x = \\pi/4$ uniquement", "$x = \\pi/2$"],
         "$\\sin(x) = \\sin(a) \\Leftrightarrow x = a + 2k\\pi$ ou $x = \\pi - a + 2k\\pi$"),
        ("Simplifier $\\cos^2(x) + \\sin^2(x)$.", "$1$",
         ["$1$", "$\\cos(2x)$", "$2$"],
         "$\\cos^2 x + \\sin^2 x = 1$ (identité fondamentale)"),
        (f"Résoudre $2\\sin(x) - {V+1} = 0$ sur $[0; 2\\pi]$.",
         f"$\\sin(x) = {(V+1)/2}$" if V+1 <= 2 else "Pas de solution",
         [f"$\\sin(x) = {(V+1)/2}$" if V+1 <= 2 else "Pas de solution",
          "$x = \\pi/" + str(V+2) + "$", f"$x = {V+1}$"],
         "$\\sin(x) = k$ a des solutions ssi $|k| \\leq 1$."),
        (f"Exprimer $\\cos(2x)$ en fonction de $\\cos(x)$.",
         "$2\\cos^2(x) - 1$",
         ["$2\\cos^2(x) - 1$", "$2\\cos(x) - 1$", "$\\cos^2(x) - \\sin^2(x)$ uniquement"],
         "$\\cos(2x) = 2\\cos^2 x - 1 = 1 - 2\\sin^2 x = \\cos^2 x - \\sin^2 x$"),
        ("Donner la dérivée de $\\sin(2x)$.", "$2\\cos(2x)$",
         ["$2\\cos(2x)$", "$\\cos(2x)$", "$-2\\sin(2x)$"],
         "$(\\sin(u))' = u'\\cos(u)$"),
        (f"$f(x) = \\sin(x) + \\cos(x)$. Calculer $f(\\pi/4)$.", "$\\sqrt{2}$",
         ["$\\sqrt{2}$", "$1$", "$\\sqrt{3}$"],
         "Remplacer par les valeurs en $\\pi/4$."),
        (f"Résoudre $\\cos(x) = -\\frac{{\\sqrt{{3}}}}{{2}}$ sur $[0; 2\\pi]$.",
         "$x = 5\\pi/6$ ou $x = 7\\pi/6$",
         ["$x = 5\\pi/6$ ou $x = 7\\pi/6$", "$x = \\pi/6$", "$x = 5\\pi/6$ uniquement"],
         "$\\cos(x) = -\\sqrt{3}/2 \\Rightarrow$ angle de référence $\\pi/6$, quadrants II et III."),
        (f"Montrer que $\\sin(\\pi - x) = \\sin(x)$.",
         "Vrai (symétrie par rapport à $\\pi/2$)",
         ["Vrai (symétrie par rapport à $\\pi/2$)", "Faux", "Vrai seulement si $x \\in [0;\\pi]$"],
         "$\\sin(\\pi - x) = \\sin x$ (formule d'addition)."),
        (f"Amplitude et période de $f(x) = 3\\sin(2x + \\pi/{V+3})$ ?",
         f"Amplitude $3$, période $\\pi$",
         [f"Amplitude $3$, période $\\pi$", f"Amplitude $2$, période $3\\pi$", f"Amplitude $3$, période $2\\pi$"],
         "Pour $A\\sin(Bx+C)$ : amplitude $|A|$, période $2\\pi/|B|$."),
    ]
    for q, a, opts, f in l2:
        exos.append(_exo(2, q, a, opts, f, ["Identifier la formule.", "Appliquer.", "Conclure."]))
    return exos[:20]


def _gen_produit_scalaire(variant=0):
    V = variant
    exos = []
    l1 = [
        (f"$\\vec{{u}}({V+2};{V+3})$ et $\\vec{{v}}({V+1};{V+4})$. Calculer $\\vec{{u}} \\cdot \\vec{{v}}$.",
         f"${(V+2)*(V+1)+(V+3)*(V+4)}$",
         [f"${(V+2)*(V+1)+(V+3)*(V+4)}$", f"${(V+2)*(V+4)+(V+3)*(V+1)}$", f"${(V+2)+(V+3)+(V+1)+(V+4)}$"],
         "$\\vec{u} \\cdot \\vec{v} = x_u x_v + y_u y_v$"),
        (f"$\\|\\vec{{u}}\\| = {V+3}$, $\\|\\vec{{v}}\\| = {V+2}$, angle $60°$. Calculer $\\vec{{u}} \\cdot \\vec{{v}}$.",
         f"${(V+3)*(V+2)//2}$" if (V+3)*(V+2) % 2 == 0 else f"$\\frac{{{(V+3)*(V+2)}}}{{2}}$",
         [f"${(V+3)*(V+2)//2}$" if (V+3)*(V+2) % 2 == 0 else f"$\\frac{{{(V+3)*(V+2)}}}{{2}}$",
          f"${(V+3)*(V+2)}$", f"$0$"],
         "$\\vec{u} \\cdot \\vec{v} = \\|u\\| \\|v\\| \\cos(\\theta)$"),
        (f"$\\vec{{u}}({V+1};{V+2})$ et $\\vec{{v}}({-(V+2)};{V+1})$. Sont-ils orthogonaux ?",
         "Oui",
         ["Oui", "Non", "On ne peut pas savoir"],
         "$\\vec{u} \\perp \\vec{v} \\Leftrightarrow \\vec{u} \\cdot \\vec{v} = 0$"),
        (f"Calculer $\\|\\vec{{u}}\\|$ avec $\\vec{{u}}({3+V};{4+V})$.",
         f"$\\sqrt{{{(3+V)**2+(4+V)**2}}}$",
         [f"$\\sqrt{{{(3+V)**2+(4+V)**2}}}$", f"${3+V+4+V}$", f"${(3+V)*(4+V)}$"],
         "$\\|\\vec{u}\\| = \\sqrt{x^2+y^2}$"),
        (f"$\\vec{{AB}} \\cdot \\vec{{AC}} = 0$. Que peut-on dire du triangle $ABC$ ?",
         "Rectangle en $A$",
         ["Rectangle en $A$", "Rectangle en $B$", "Équilatéral"],
         "$\\vec{AB} \\perp \\vec{AC} \\Leftrightarrow$ angle droit en $A$."),
    ]
    for q, a, opts, f in l1:
        exos.append(_exo(1, q, a, opts, f, ["Identifier la formule du produit scalaire.", "Remplacer.", "Calculer."]))

    # 5 more lvl 1
    for i in range(5):
        k = i + V + 1
        exos.append(_exo(1, f"$\\vec{{u}}({k};0)$ et $\\vec{{v}}(0;{k+1})$. Calculer $\\vec{{u}} \\cdot \\vec{{v}}$.",
            "$0$", ["$0$", f"${k*(k+1)}$", f"${k+k+1}$"],
            "$\\vec{u} \\cdot \\vec{v} = x_u x_v + y_u y_v$",
            ["$x_u x_v = " + str(k) + " \\times 0 = 0$.", "$y_u y_v = 0 \\times " + str(k+1) + " = 0$.", "$0 + 0 = 0$."]))

    # lvl 2
    l2 = [
        (f"Triangle $ABC$ avec $AB={3+V}$, $AC={4+V}$, $BC={5+V}$. Calculer $\\vec{{AB}} \\cdot \\vec{{AC}}$ (Al-Kashi).",
         f"${((3+V)**2+(4+V)**2-(5+V)**2)//2}$",
         [f"${((3+V)**2+(4+V)**2-(5+V)**2)//2}$", f"${(3+V)*(4+V)}$", "$0$"],
         "$\\vec{AB} \\cdot \\vec{AC} = \\frac{AB^2+AC^2-BC^2}{2}$ (Al-Kashi)"),
        (f"Projeté orthogonal de $\\vec{{u}}({V+4};{V+2})$ sur $\\vec{{v}}({V+1};0)$.",
         f"${V+4}$",
         [f"${V+4}$", f"${V+2}$", f"${(V+4)*(V+2)/(V+1):.1f}$"],
         "Projeté = $\\frac{\\vec{u} \\cdot \\vec{v}}{\\|\\vec{v}\\|}$"),
        (f"$A(0;0)$, $B({2+V};0)$, $C(1;{2+V})$. L'angle $\\widehat{{BAC}}$ est-il droit ?",
         f"Non, $\\vec{{AB}} \\cdot \\vec{{AC}} = {2+V} \\neq 0$",
         [f"Non, $\\vec{{AB}} \\cdot \\vec{{AC}} = {2+V} \\neq 0$", "Oui", "On ne peut pas savoir"],
         "$\\vec{AB} \\cdot \\vec{AC} = 0 \\Leftrightarrow$ angle droit."),
    ]
    for q, a, opts, f in l2:
        exos.append(_exo(2, q, a, opts, f, ["Identifier la formule adaptée.", "Calculer.", "Conclure."]))

    for i in range(7):
        k = V + i + 2
        exos.append(_exo(2, f"$\\vec{{u}}({k};{k+1})$, $\\vec{{v}}(1;-1)$. Trouver l'angle entre $\\vec{{u}}$ et $\\vec{{v}}$.",
            f"$\\cos(\\theta) = \\frac{{-1}}{{\\sqrt{{{2*(k**2+(k+1)**2)}}}}}$",
            [f"$\\cos(\\theta) = \\frac{{-1}}{{\\sqrt{{{2*(k**2+(k+1)**2)}}}}}$",
             f"$\\cos(\\theta) = \\frac{{{2*k+1}}}{{\\sqrt{{{k**2+(k+1)**2}}}}}$", "$\\theta = 90°$"],
            "$\\cos(\\theta) = \\frac{\\vec{u} \\cdot \\vec{v}}{\\|u\\| \\|v\\|}$",
            ["Calculer $\\vec{u} \\cdot \\vec{v}$.", "Calculer les normes.", "Appliquer la formule."]))
    return exos[:20]


def _gen_geometrie_repere(variant=0):
    V = variant
    exos = []
    for i in range(10):
        a, b, c = V+i+1, V+i+2, V+i+3
        if i < 3:
            exos.append(_exo(1, f"Donner un vecteur directeur de la droite $y = {a}x + {b}$.",
                f"$\\vec{{u}}(1;{a})$", [f"$\\vec{{u}}(1;{a})$", f"$\\vec{{u}}({a};1)$", f"$\\vec{{u}}({b};{a})$"],
                "Droite $y = mx + p$ → vecteur directeur $(1; m)$.",
                ["Coefficient directeur $m = " + str(a) + "$.", "Vecteur directeur $(1; m)$.", f"$(1; {a})$."]))
        elif i < 5:
            exos.append(_exo(1, f"Equation de la droite passant par $A({a};{b})$ de pente ${c}$.",
                f"$y = {c}x + {b-c*a}$",
                [f"$y = {c}x + {b-c*a}$", f"$y = {a}x + {c}$", f"$y = {c}x + {b}$"],
                "$y - y_A = m(x - x_A)$",
                [f"$y - {b} = {c}(x - {a})$.", f"$y = {c}x - {c*a} + {b}$.", f"$y = {c}x + {b-c*a}$."]))
        elif i < 7:
            exos.append(_exo(1, f"Vecteur normal à la droite ${a}x + {b}y + {c} = 0$ ?",
                f"$\\vec{{n}}({a};{b})$", [f"$\\vec{{n}}({a};{b})$", f"$\\vec{{n}}({b};{a})$", f"$\\vec{{n}}(-{b};{a})$"],
                "Droite $ax+by+c=0$ → vecteur normal $(a;b)$.",
                ["Forme $ax+by+c=0$.", "Le vecteur normal est $(a;b)$.", f"$({a};{b})$."]))
        elif i < 9:
            d = round(((a-c)**2 + (b-c)**2)**0.5, 2)
            exos.append(_exo(1, f"Distance entre $A({a};{b})$ et $B({c};{c})$.",
                f"$\\sqrt{{{(a-c)**2+(b-c)**2}}}$",
                [f"$\\sqrt{{{(a-c)**2+(b-c)**2}}}$", f"${abs(a-c)+abs(b-c)}$", f"${abs(a-c)*(b-c)}$"],
                "$d = \\sqrt{(x_B-x_A)^2+(y_B-y_A)^2}$",
                ["Différences de coordonnées.", "Élever au carré et additionner.", "Racine carrée."]))
        else:
            exos.append(_exo(1, f"Milieu de $[A({a};{b}), B({c};{a})]$ ?",
                f"$M({(a+c)/2};{(b+a)/2})$",
                [f"$M({(a+c)/2};{(b+a)/2})$", f"$M({a};{b})$", f"$M({c-a};{b-a})$"],
                "$M = (\\frac{x_A+x_B}{2}; \\frac{y_A+y_B}{2})$",
                ["Moyenne des abscisses.", "Moyenne des ordonnées.", "Conclure."]))

    for i in range(10):
        a, b = V+i+1, V+i+3
        if i < 3:
            exos.append(_exo(2, f"Equation du cercle de centre $C({a};{b})$ et rayon ${a+1}$.",
                f"$(x-{a})^2 + (y-{b})^2 = {(a+1)**2}$",
                [f"$(x-{a})^2 + (y-{b})^2 = {(a+1)**2}$", f"$(x+{a})^2 + (y+{b})^2 = {a+1}$", f"$x^2+y^2 = {(a+1)**2}$"],
                "$(x-a)^2+(y-b)^2 = R^2$",
                [f"Centre $({a};{b})$, rayon ${a+1}$.", "Appliquer la formule.", "Développer si nécessaire."]))
        elif i < 5:
            exos.append(_exo(2, f"Les droites $y = {a}x + 1$ et $y = {-1/a:.2f}x + {b}$ sont-elles perpendiculaires ?",
                "Oui",
                ["Oui", "Non", "Parallèles"],
                "Deux droites sont perpendiculaires ssi $m_1 m_2 = -1$.",
                [f"$m_1 = {a}$, $m_2 = {-1/a:.2f}$.", f"$m_1 \\times m_2 = {a*(-1/a):.0f}$.", "Conclure."]))
        elif i < 7:
            exos.append(_exo(2, f"Intersection des droites $y = {a}x + {b}$ et $y = {a+1}x + {b-1}$.",
                f"$({1}; {a+b})$",
                [f"$({1}; {a+b})$", f"$({b}; {a})$", "Pas d'intersection"],
                "Résoudre le système $y = m_1 x + p_1$ et $y = m_2 x + p_2$.",
                ["Égaliser les deux expressions.", f"${a}x + {b} = {a+1}x + {b-1}$.", "Résoudre."]))
        else:
            exos.append(_exo(2, f"Distance du point $P({a};{b})$ à la droite ${a+1}x + {b+1}y + {1} = 0$.",
                f"$\\frac{{|{(a+1)*a+(b+1)*b+1}|}}{{\\sqrt{{{(a+1)**2+(b+1)**2}}}}}$",
                [f"$\\frac{{|{(a+1)*a+(b+1)*b+1}|}}{{\\sqrt{{{(a+1)**2+(b+1)**2}}}}}$", f"${a+b}$", "$0$"],
                "$d = \\frac{|ax_0+by_0+c|}{\\sqrt{a^2+b^2}}$",
                ["Identifier $a, b, c$ de la droite.", "Remplacer les coordonnées du point.", "Calculer."]))
    return exos[:20]


def _gen_probas_cond(variant=0):
    V = variant
    exos = []
    # lvl 1
    for i in range(10):
        if i == 0:
            exos.append(_exo(1, f"$P(A) = 0.{V+5}$, $P(B|A) = 0.{V+3}$. Calculer $P(A \\cap B)$.",
                f"${(V+5)*(V+3)/100:.2f}$",
                [f"${(V+5)*(V+3)/100:.2f}$", f"$0.{V+5} + 0.{V+3}$", f"$0.{V+3}$"],
                "$P(A \\cap B) = P(A) \\times P(B|A)$",
                ["Formule du produit.", "Remplacer les valeurs.", "Calculer."]))
        elif i == 1:
            exos.append(_exo(1, f"$P(A \\cap B) = 0.{V+2}$, $P(A) = 0.{V+5}$. Calculer $P(B|A)$.",
                f"$\\frac{{0.{V+2}}}{{0.{V+5}}}$",
                [f"$\\frac{{0.{V+2}}}{{0.{V+5}}}$", f"$0.{V+2} \\times 0.{V+5}$", f"$0.{V+5} - 0.{V+2}$"],
                "$P(B|A) = \\frac{P(A \\cap B)}{P(A)}$",
                ["Formule de Bayes simplifiée.", "Remplacer.", "Calculer."]))
        elif i < 5:
            p = (V + i + 2) * 10
            exos.append(_exo(1, f"Un test est positif à ${p}$% si malade. $P(\\text{{malade}}) = 0.0{V+1}$. $P(\\text{{positif}} \\cap \\text{{malade}})$ = ?",
                f"${p/100 * (V+1)/100:.4f}$",
                [f"${p/100 * (V+1)/100:.4f}$", f"$0.{p//10}$", f"$0.0{V+1}$"],
                "$P(T^+ \\cap M) = P(T^+|M) \\times P(M)$",
                ["Identifier $P(T^+|M)$ et $P(M)$.", "Multiplier.", "Calculer."]))
        elif i < 8:
            exos.append(_exo(1, f"$A$ et $B$ indépendants, $P(A) = 0.{V+3}$, $P(B) = 0.{V+4}$. $P(A \\cap B)$ = ?",
                f"${(V+3)*(V+4)/100:.2f}$",
                [f"${(V+3)*(V+4)/100:.2f}$", f"$0.{V+3} + 0.{V+4}$", f"$0.{V+3}$"],
                "Indépendance : $P(A \\cap B) = P(A) \\times P(B)$.",
                ["$A$ et $B$ indépendants.", "$P(A \\cap B) = P(A) \\times P(B)$.", "Calculer."]))
        else:
            exos.append(_exo(1, f"Dans un arbre, $P(A) = 0.{V+4}$ et $P(\\bar{{A}}) = ?$",
                f"$0.{10-V-4}$",
                [f"$0.{10-V-4}$", f"$0.{V+4}$", f"$1$"],
                "$P(\\bar{A}) = 1 - P(A)$",
                ["Événement contraire.", "$P(\\bar{A}) = 1 - P(A)$.", f"$= 1 - 0.{V+4}$."]))

    # lvl 2
    for i in range(10):
        if i < 3:
            exos.append(_exo(2, f"$P(A)=0.{V+3}$, $P(B|A)=0.{V+6}$, $P(B|\\bar{{A}})=0.{V+1}$. Calculer $P(B)$ (prob. totales).",
                f"$P(B) = {((V+3)*(V+6)+(10-V-3)*(V+1))/100:.4f}$",
                [f"$P(B) = {((V+3)*(V+6)+(10-V-3)*(V+1))/100:.4f}$",
                 f"$P(B) = 0.{V+6}$", f"$P(B) = 0.{V+3} + 0.{V+1}$"],
                "$P(B) = P(A)P(B|A) + P(\\bar{A})P(B|\\bar{A})$",
                ["Formule des probabilités totales.", "Deux branches de l'arbre.", "Additionner."]))
        elif i < 5:
            exos.append(_exo(2, f"$A$ et $B$ sont-ils indépendants si $P(A)=0.{V+3}$, $P(B)=0.{V+5}$, $P(A \\cap B)={((V+3)*(V+5))/100:.2f}$ ?",
                "Oui",
                ["Oui", "Non", "Impossible à déterminer"],
                "$A$ et $B$ indépendants $\\Leftrightarrow P(A \\cap B) = P(A) \\times P(B)$.",
                [f"$P(A) \\times P(B) = 0.{V+3} \\times 0.{V+5}$.", f"$= {(V+3)*(V+5)/100:.2f}$.", "$= P(A \\cap B)$ → indépendants."]))
        else:
            exos.append(_exo(2, f"Urne : {V+3} rouges, {V+5} bleues. On tire 2 boules sans remise. $P(2 \\text{{ rouges}})$ ?",
                f"$\\frac{{{(V+3)*(V+2)}}}{{{(2*V+8)*(2*V+7)}}}$",
                [f"$\\frac{{{(V+3)*(V+2)}}}{{{(2*V+8)*(2*V+7)}}}$",
                 f"$(\\frac{{{V+3}}}{{{2*V+8}}})^2$", f"$\\frac{{{V+3}}}{{{2*V+8}}}$"],
                "Sans remise : la 2e probabilité est modifiée.",
                [f"$P(R_1) = \\frac{{{V+3}}}{{{2*V+8}}}$.", f"$P(R_2|R_1) = \\frac{{{V+2}}}{{{2*V+7}}}$.", "Multiplier."]))
    return exos[:20]


def _gen_var_aleatoires(variant=0):
    V = variant
    exos = []
    # lvl 1
    for i in range(10):
        if i < 3:
            vals = [i+V, i+V+1, i+V+2]
            probs = [0.2+V*0.01, 0.5, 0.3-V*0.01]
            E = sum(v*p for v,p in zip(vals, probs))
            exos.append(_exo(1, f"$X$ prend les valeurs ${vals[0]}, {vals[1]}, {vals[2]}$ avec probabilités ${probs[0]:.2f}, {probs[1]:.2f}, {probs[2]:.2f}$. $E(X)$ = ?",
                f"${E:.2f}$",
                [f"${E:.2f}$", f"${sum(vals)/3:.2f}$", f"${sum(probs):.2f}$"],
                "$E(X) = \\sum x_i p_i$",
                ["Multiplier chaque valeur par sa probabilité.", "Additionner les produits.", f"$E(X) = {E:.2f}$."]))
        elif i < 5:
            exos.append(_exo(1, f"$E(X) = {V+3}$. Calculer $E(2X + {V+1})$.",
                f"${2*(V+3)+V+1}$",
                [f"${2*(V+3)+V+1}$", f"${2*(V+3)*(V+1)}$", f"${V+3+V+1}$"],
                "$E(aX+b) = aE(X)+b$",
                ["$E(aX+b) = aE(X) + b$.", f"$= 2 \\times {V+3} + {V+1}$.", "Calculer."]))
        elif i < 7:
            exos.append(_exo(1, f"La somme des probabilités d'une loi est toujours égale à :", "$1$",
                ["$1$", "$E(X)$", "$V(X)$"],
                "$\\sum p_i = 1$",
                ["Propriété fondamentale.", "Somme de toutes les probabilités.", "$= 1$."]))
        else:
            exos.append(_exo(1, f"$V(X) = {(V+2)**2}$. Calculer $\\sigma(X)$.",
                f"${V+2}$",
                [f"${V+2}$", f"${(V+2)**2}$", f"${(V+2)/2}$"],
                "$\\sigma(X) = \\sqrt{V(X)}$",
                ["$\\sigma = \\sqrt{V(X)}$.", f"$= \\sqrt{{{(V+2)**2}}}$.", f"$= {V+2}$."]))

    # lvl 2
    for i in range(10):
        if i < 4:
            n, k = V+5, i+1
            from math import comb, factorial
            c = comb(n, k)
            exos.append(_exo(2, f"$X \\sim B({n}; 0.{V+3})$. Calculer $P(X = {k})$.",
                f"$\\binom{{{n}}}{{{k}}} (0.{V+3})^{k}(0.{10-V-3})^{{{n-k}}}$",
                [f"$\\binom{{{n}}}{{{k}}} (0.{V+3})^{k}(0.{10-V-3})^{{{n-k}}}$",
                 f"$0.{V+3}^{k}$", f"${n} \\times 0.{V+3}^{k}$"],
                "$P(X=k) = \\binom{n}{k} p^k (1-p)^{n-k}$",
                [f"$\\binom{{{n}}}{{{k}}} = {c}$.", f"$p = 0.{V+3}$, $1-p = 0.{10-V-3}$.", "Calculer."]))
        elif i < 7:
            vals = [0, 1, 2, 3]
            probs = [0.1, 0.3, 0.4, 0.2]
            E = sum(v*p for v,p in zip(vals,probs))
            E2 = sum(v**2*p for v,p in zip(vals,probs))
            Var = E2 - E**2
            exos.append(_exo(2, f"$X$ : valeurs $0,1,2,3$ avec probas $0.1, 0.3, 0.4, 0.2$. $V(X)$ = ?",
                f"${Var:.2f}$",
                [f"${Var:.2f}$", f"${E:.1f}$", f"${E2:.1f}$"],
                "$V(X) = E(X^2) - [E(X)]^2$",
                [f"$E(X) = {E:.1f}$.", f"$E(X^2) = {E2:.1f}$.", f"$V(X) = {E2:.1f} - {E:.1f}^2 = {Var:.2f}$."]))
        else:
            n = V + 8
            p_val = (V+3)/10
            exos.append(_exo(2, f"$X \\sim B({n}; {p_val})$. $E(X)$ et $V(X)$ ?",
                f"$E = {n*p_val:.1f}$, $V = {n*p_val*(1-p_val):.2f}$",
                [f"$E = {n*p_val:.1f}$, $V = {n*p_val*(1-p_val):.2f}$",
                 f"$E = {n*p_val:.1f}$, $V = {n*p_val:.1f}$",
                 f"$E = {n:.0f}$, $V = {p_val}$"],
                "$E(X)=np$, $V(X)=np(1-p)$",
                [f"$n={n}$, $p={p_val}$.", f"$E = {n} \\times {p_val} = {n*p_val:.1f}$.", f"$V = {n*p_val:.1f} \\times {1-p_val:.1f} = {n*p_val*(1-p_val):.2f}$."]))
    return exos[:20]


def _gen_algorithmique(variant=0):
    V = variant
    exos = []
    # lvl 1
    algos_l1 = [
        (f"Que renvoie ce code ?\n```python\nx = {V+3}\nfor i in range(4):\n    x = x + 2\nprint(x)\n```",
         f"${V+3+8}$", [f"${V+3+8}$", f"${V+3+2}$", f"${V+3}$"],
         "Boucle `for` : exécute le corps $n$ fois."),
        (f"Que renvoie `len([{V+1}, {V+2}, {V+3}, {V+4}])` ?", "$4$",
         ["$4$", f"${V+1+V+2+V+3+V+4}$", f"${V+4}$"],
         "`len(liste)` renvoie le nombre d'éléments."),
        (f"Que vaut `{V+7} // 3` en Python ?", f"${(V+7)//3}$",
         [f"${(V+7)//3}$", f"${(V+7)/3:.2f}$", f"${V+7 % 3}$"],
         "`//` = division entière (quotient sans décimales)."),
        (f"Que vaut `{V+7} % 3` en Python ?", f"${(V+7)%3}$",
         [f"${(V+7)%3}$", f"${(V+7)//3}$", f"${V+7}$"],
         "`%` = modulo (reste de la division euclidienne)."),
        (f"Écrire en Python : « si $x > {V+5}$ alors afficher 'grand' ».",
         f"`if x > {V+5}: print('grand')`",
         [f"`if x > {V+5}: print('grand')`", f"`if x > {V+5} print('grand')`", f"`while x > {V+5}: print('grand')`"],
         "Syntaxe `if condition: instruction`"),
        (f"Que fait `range({V+2}, {V+7})` ?", f"Entiers de ${V+2}$ à ${V+6}$",
         [f"Entiers de ${V+2}$ à ${V+6}$", f"Entiers de ${V+2}$ à ${V+7}$", f"Entiers de $0$ à ${V+7}$"],
         "`range(a, b)` → entiers de $a$ à $b-1$."),
        (f"Que renvoie `[i**2 for i in range(5)]` ?", "$[0, 1, 4, 9, 16]$",
         ["$[0, 1, 4, 9, 16]$", "$[1, 4, 9, 16, 25]$", "$[0, 2, 4, 8, 16]$"],
         "Compréhension de liste : applique `i**2` pour $i = 0, 1, 2, 3, 4$."),
        (f"Combien de fois s'exécute la boucle `for i in range({V+6})` ?", f"${V+6}$ fois",
         [f"${V+6}$ fois", f"${V+7}$ fois", f"${V+5}$ fois"],
         "`range(n)` → $n$ itérations ($i = 0$ à $n-1$)."),
        (f"Que vaut `sum([{V+1}, {V+2}, {V+3}])` ?", f"${3*V+6}$",
         [f"${3*V+6}$", f"$3$", f"${V+3}$"],
         "`sum(liste)` additionne tous les éléments."),
        (f"Compléter : `def carre(x): return ___` pour que `carre({V+3})` renvoie ${(V+3)**2}$.",
         "$x**2$", ["$x**2$", "$2*x$", "$x+x$"],
         "`**` = puissance en Python. `x**2` = $x^2$."),
    ]
    for q, a, opts, f in algos_l1:
        exos.append(_exo(1, q, a, opts, f, ["Lire le code ligne par ligne.", "Suivre les variables.", "Conclure."]))

    # lvl 2
    algos_l2 = [
        (f"Écrire un algo Python qui calcule $\\sum_{{k=1}}^{{{V+10}}} k^2$.",
         f"`sum(k**2 for k in range(1, {V+11}))`",
         [f"`sum(k**2 for k in range(1, {V+11}))`", f"`sum(k**2 for k in range({V+10}))`", f"`sum(range(1, {V+10}))**2`"],
         "`sum(expression for var in range(a, b))` = somme de $a$ à $b-1$."),
        (f"Que renvoie ce code ?\n```python\nn = {V+20}\nwhile n > 1:\n    if n % 2 == 0:\n        n = n // 2\n    else:\n        n = 3*n + 1\n    print(n, end=' ')\n```\nPremière valeur affichée ?",
         f"${(V+20)//2 if (V+20)%2==0 else 3*(V+20)+1}$",
         [f"${(V+20)//2 if (V+20)%2==0 else 3*(V+20)+1}$", f"${V+20}$", f"${V+19}$"],
         "Suite de Syracuse : si pair diviser par 2, si impair $3n+1$."),
        (f"Compléter pour trier une liste par ordre croissant :\n`L = [{V+5}, {V+1}, {V+8}, {V+3}]`\n`L._____()`",
         "`sort()`",
         ["`sort()`", "`order()`", "`sorted()`"],
         "`liste.sort()` trie en place. `sorted(liste)` renvoie une copie triée."),
        (f"Écrire une fonction `est_premier(n)` qui teste si $n$ est premier.",
         "Boucle de $2$ à $\\sqrt{n}$, tester `n % i == 0`",
         ["Boucle de $2$ à $\\sqrt{n}$, tester `n % i == 0`", "Tester `n % 2 == 0`", "Tester tous les nombres de $1$ à $n$"],
         "Un nombre premier n'a aucun diviseur entre $2$ et $\\sqrt{n}$."),
        (f"Que renvoie `max([{V+2}, {V+9}, {V+1}, {V+7}])` ?", f"${V+9}$",
         [f"${V+9}$", f"${V+7}$", f"${4*V+19}$"],
         "`max(liste)` renvoie le plus grand élément."),
    ]
    for q, a, opts, f in algos_l2:
        exos.append(_exo(2, q, a, opts, f, ["Analyser l'algorithme.", "Simuler l'exécution.", "Conclure."]))

    # 5 more lvl 2
    for i in range(5):
        k = V + i + 2
        exos.append(_exo(2, f"Combien d'itérations fait `while n > 0: n = n // 2` si $n = {2**k}$ ?",
            f"${k+1}$",
            [f"${k+1}$", f"${k}$", f"${2**k}$"],
            "Chaque itération divise $n$ par $2$. $\\log_2(n) + 1$ itérations.",
            [f"$n = {2**k}, {2**(k-1)}, ..., 1, 0$.", f"${k+1}$ divisions par 2.", "Compter les étapes."]))
    return exos[:20]


# ════════════════════════════════════════════════════════════
#  MAPPING CHAPITRES → GÉNÉRATEURS
# ════════════════════════════════════════════════════════════

GENERATORS = {
    "Second_Degre": _gen_second_degre,
    "Suites": _gen_suites,
    "Derivation": _gen_derivation,
    "Exponentielle": _gen_exponentielle,
    "Trigonometrie": _gen_trigo,
    "Produit_Scalaire": _gen_produit_scalaire,
    "Geometrie_Repere": _gen_geometrie_repere,
    "Probabilites_Cond": _gen_probas_cond,
    "Variables_Aleatoires": _gen_var_aleatoires,
    "Algorithmique": _gen_algorithmique,
}


# ════════════════════════════════════════════════════════════
#  ÉTAPE 1 — INSÉRER LES EXERCICES
# ════════════════════════════════════════════════════════════

def step1_insert_exercises():
    print("\n📚 ÉTAPE 1 — Insertion des exercices 1ERE")
    print("=" * 55)

    counts = {"Curriculum_Officiel": 0, "DiagnosticExos": 0, "BoostExos": 0}

    # --- Curriculum_Officiel ---
    print("\n→ Curriculum_Officiel...")
    existing = sh.read_raw("Curriculum_Officiel")
    header = existing[0] if existing else ["Niveau", "Categorie", "Titre", "Icone", "ExosJSON"]
    filtered = [header] + [r for r in existing[1:] if len(r) > 0 and r[0] != "1ERE"]

    for cat, titre, icone in CHAPTERS:
        gen = GENERATORS[cat]
        exos = gen(variant=0)
        row = ["1ERE", cat, titre, icone, json.dumps(exos, ensure_ascii=False)]
        filtered.append(row)
        counts["Curriculum_Officiel"] += 1

    sh.write_rows("Curriculum_Officiel", filtered)
    print(f"  ✅ {counts['Curriculum_Officiel']} chapitres 1ERE insérés")

    # --- DiagnosticExos ---
    print("\n→ DiagnosticExos...")
    existing = sh.read_raw("DiagnosticExos")
    header = existing[0] if existing else ["Niveau", "Categorie", "ExosJSON"]
    filtered = [header] + [r for r in existing[1:] if len(r) > 0 and r[0] != "1ERE"]

    for cat, _, _ in CHAPTERS:
        gen = GENERATORS[cat]
        full = gen(variant=5)  # variant différent pour exos différents
        diag = [full[0], full[10]]  # 1 lvl1 + 1 lvl2
        row = ["1ERE", cat, json.dumps(diag, ensure_ascii=False)]
        filtered.append(row)
        counts["DiagnosticExos"] += 1

    sh.write_rows("DiagnosticExos", filtered)
    print(f"  ✅ {counts['DiagnosticExos']} chapitres 1ERE insérés")

    # --- BoostExos ---
    print("\n→ BoostExos...")
    existing = sh.read_raw("BoostExos")
    header = existing[0] if existing else ["Niveau", "Categorie", "ExosJSON"]
    filtered = [header] + [r for r in existing[1:] if len(r) > 0 and r[0] != "1ERE"]

    for cat, _, _ in CHAPTERS:
        gen = GENERATORS[cat]
        full = gen(variant=10)  # variant encore différent
        boost = full[:5] + full[10:15]  # 5 lvl1 + 5 lvl2
        row = ["1ERE", cat, json.dumps(boost, ensure_ascii=False)]
        filtered.append(row)
        counts["BoostExos"] += 1

    sh.write_rows("BoostExos", filtered)
    print(f"  ✅ {counts['BoostExos']} chapitres 1ERE insérés")

    return counts


# ════════════════════════════════════════════════════════════
#  ÉTAPE 2 — CRÉER LE COMPTE AUGUSTE
# ════════════════════════════════════════════════════════════

def step2_create_auguste():
    print("\n👤 ÉTAPE 2 — Création du compte Auguste")
    print("=" * 55)

    email = "augustecapronm@icloud.com"
    pwd_hash = hashlib.sha256(f"{email}::auguste::AB22".encode()).hexdigest()

    # Vérifier si existe déjà
    users = sh.read("Users")
    existing_row = None
    for i, u in enumerate(users):
        if u.get("Code") == "AUG001" or u.get("Email", "").lower() == email:
            existing_row = i + 2  # 1-indexed + header
            break

    row_data = ["AUG001", "Auguste", "1ERE", email, pwd_hash,
                TODAY, "0", "1", TODAY, TOMORROW_30, "1", "", ""]

    if existing_row:
        # Mettre à jour la ligne existante
        col_end = chr(64 + len(row_data))
        sh.update_range("Users", f"A{existing_row}:{col_end}{existing_row}", [row_data])
        print(f"  ✅ Compte Auguste mis à jour (ligne {existing_row})")
    else:
        sh.append_row("Users", row_data)
        print("  ✅ Compte Auguste créé")

    return True


# ════════════════════════════════════════════════════════════
#  ÉTAPE 3 — SIMULER DIAGNOSTIC
# ════════════════════════════════════════════════════════════

def step3_simulate_diagnostic():
    print("\n🧪 ÉTAPE 3 — Simulation du diagnostic")
    print("=" * 55)

    scores_sim = {
        "Second_Degre": (75, 0), "Suites": (40, 1), "Derivation": (55, 1),
        "Exponentielle": (30, 1), "Trigonometrie": (50, 1), "Produit_Scalaire": (65, 0),
        "Geometrie_Repere": (70, 0), "Probabilites_Cond": (45, 1),
        "Variables_Aleatoires": (35, 1), "Algorithmique": (60, 0),
    }

    # --- Nettoyer Progress AUG001 ---
    existing_prog = sh.read_raw("Progress")
    header_p = existing_prog[0] if existing_prog else ["Code","Niveau","Chapitre","Score","NbExos","NbErreurs","DernierePratique","Statut","Streak"]
    filtered_p = [header_p] + [r for r in existing_prog[1:] if len(r) == 0 or r[0] != "AUG001"]

    for cat, (score, errors) in scores_sim.items():
        filtered_p.append(["AUG001", "1ERE", cat, str(score), "2", str(errors), YESTERDAY, "en_cours", "1"])

    sh.write_rows("Progress", filtered_p)
    print(f"  ✅ {len(scores_sim)} lignes Progress insérées")

    # --- Nettoyer Scores AUG001 ---
    existing_scores = sh.read_raw("Scores")
    header_s = existing_scores[0] if existing_scores else ["Code","Prénom","Niveau","Chapitre","NumExo","Énoncé","Résultat","Temps(sec)","NbIndices","FormuleVue","MauvaiseOption","Draft","Date","Source"]
    filtered_s = [header_s] + [r for r in existing_scores[1:] if len(r) == 0 or r[0] != "AUG001"]

    # Générer les scores avec les vrais énoncés du diag
    diag_data = sh.read_raw("DiagnosticExos")
    diag_by_cat = {}
    for row in diag_data[1:]:
        if len(row) >= 3 and row[0] == "1ERE":
            diag_by_cat[row[1]] = json.loads(row[2])

    scores_count = 0
    for cat, (score, errors) in scores_sim.items():
        diag_exos = diag_by_cat.get(cat, [{"q": "Question 1"}, {"q": "Question 2"}])
        for j, exo in enumerate(diag_exos[:2]):
            # Si erreur dans ce chapitre, le 1er exo est HARD
            if errors > 0 and j == 0:
                resultat = "HARD"
            else:
                resultat = "EASY"
            q_text = exo.get("q", f"Diagnostic {cat} Q{j+1}")[:60]
            filtered_s.append([
                "AUG001", "Auguste", "1ERE", cat, str(j+1), q_text,
                resultat, str(random.randint(15, 45)), "0", "0", "", "", YESTERDAY, "CALIBRAGE"
            ])
            scores_count += 1

    sh.write_rows("Scores", filtered_s)
    print(f"  ✅ {scores_count} lignes Scores insérées")

    return scores_count


# ════════════════════════════════════════════════════════════
#  ÉTAPE 4 — PRÉPARER LE BOOST
# ════════════════════════════════════════════════════════════

def step4_prepare_boost():
    print("\n⚡ ÉTAPE 4 — Préparation du boost")
    print("=" * 55)

    # Lire les BoostExos 1ERE pour Exponentielle et Suites
    boost_data = sh.read_raw("BoostExos")
    boost_by_cat = {}
    for row in boost_data[1:]:
        if len(row) >= 3 and row[0] == "1ERE":
            boost_by_cat[row[1]] = json.loads(row[2])

    expo_exos = boost_by_cat.get("Exponentielle", [])
    suites_exos = boost_by_cat.get("Suites", [])

    # 2 Exponentielle lvl1 + 2 Suites lvl1 + 1 Exponentielle lvl2
    boost_exos = []
    expo_l1 = [e for e in expo_exos if e.get("lvl") == 1][:2]
    suites_l1 = [e for e in suites_exos if e.get("lvl") == 1][:2]
    expo_l2 = [e for e in expo_exos if e.get("lvl") == 2][:1]
    boost_exos = expo_l1 + suites_l1 + expo_l2

    # Ajouter la catégorie pour le frontend
    for e in expo_l1 + expo_l2:
        e["categorie"] = "Exponentielle"
    for e in suites_l1:
        e["categorie"] = "Suites"

    boost_json = {
        "insight": "Auguste, tu maîtrises bien le second degré. Focus aujourd'hui sur la fonction exponentielle et les suites — deux notions clés pour la suite de l'année.",
        "exos": boost_exos
    }

    # Nettoyer DailyBoosts AUG001 du jour
    existing = sh.read_raw("DailyBoosts")
    header = existing[0] if existing else ["Code", "Date", "BoostJSON", "ExosDone"]
    filtered = [header] + [r for r in existing[1:] if not (len(r) > 1 and r[0] == "AUG001" and r[1] == TODAY)]
    filtered.append(["AUG001", TODAY, json.dumps(boost_json, ensure_ascii=False), "0"])

    sh.write_rows("DailyBoosts", filtered)
    print("  ✅ Boost du jour créé (Exponentielle + Suites)")
    return True


# ════════════════════════════════════════════════════════════
#  ÉTAPE 6 — VÉRIFICATION
# ════════════════════════════════════════════════════════════

def step6_verify():
    print("\n🔍 ÉTAPE 6 — Vérification")
    print("=" * 55)

    report = []
    all_ok = True

    # Curriculum
    curr = sh.read_raw("Curriculum_Officiel")
    c1ere = [r for r in curr[1:] if len(r) > 0 and r[0] == "1ERE"]
    ok = len(c1ere) == 10
    report.append(f"Curriculum_Officiel : {len(c1ere)} lignes 1ERE insérées (attendu: 10) {'✅' if ok else '❌'}")
    if not ok: all_ok = False

    # DiagnosticExos
    diag = sh.read_raw("DiagnosticExos")
    d1ere = [r for r in diag[1:] if len(r) > 0 and r[0] == "1ERE"]
    ok = len(d1ere) == 10
    report.append(f"DiagnosticExos      : {len(d1ere)} lignes 1ERE insérées (attendu: 10) {'✅' if ok else '❌'}")
    if not ok: all_ok = False

    # BoostExos
    boost = sh.read_raw("BoostExos")
    b1ere = [r for r in boost[1:] if len(r) > 0 and r[0] == "1ERE"]
    ok = len(b1ere) == 10
    report.append(f"BoostExos           : {len(b1ere)} lignes 1ERE insérées (attendu: 10) {'✅' if ok else '❌'}")
    if not ok: all_ok = False

    # Users
    users = sh.read("Users")
    aug = [u for u in users if u.get("Code") == "AUG001"]
    ok = len(aug) == 1
    report.append(f"Users Auguste       : {'✅' if ok else '❌'} (Code AUG001 {'trouvé' if ok else 'NON trouvé'})")
    if not ok: all_ok = False

    # Progress
    prog = sh.read_raw("Progress")
    p_aug = [r for r in prog[1:] if len(r) > 0 and r[0] == "AUG001"]
    ok = len(p_aug) == 10
    report.append(f"Progress Auguste    : {len(p_aug)} lignes (attendu: 10) {'✅' if ok else '❌'}")
    if not ok: all_ok = False

    # Scores
    scores = sh.read_raw("Scores")
    s_aug = [r for r in scores[1:] if len(r) > 0 and r[0] == "AUG001"]
    ok = len(s_aug) == 20
    report.append(f"Scores Auguste      : {len(s_aug)} lignes (attendu: 20) {'✅' if ok else '❌'}")
    if not ok: all_ok = False

    # DailyBoosts
    db = sh.read_raw("DailyBoosts")
    db_aug = [r for r in db[1:] if len(r) > 1 and r[0] == "AUG001" and r[1] == TODAY]
    ok = len(db_aug) >= 1
    report.append(f"DailyBoosts Auguste : {'✅' if ok else '❌'} (boost du jour {'présent' if ok else 'ABSENT'})")
    if not ok: all_ok = False

    # JSON validation
    json_ok = 0
    json_errors = []
    for tab_name, tab_data, json_col in [
        ("Curriculum_Officiel", c1ere, 4),
        ("DiagnosticExos", d1ere, 2),
        ("BoostExos", b1ere, 2)
    ]:
        for row in tab_data:
            try:
                if len(row) > json_col:
                    parsed = json.loads(row[json_col])
                    if isinstance(parsed, list) and len(parsed) > 0:
                        json_ok += 1
                    else:
                        json_errors.append(f"{tab_name}/{row[1] if len(row)>1 else '?'}: liste vide")
                else:
                    json_errors.append(f"{tab_name}/{row[1] if len(row)>1 else '?'}: colonne manquante")
            except Exception as e:
                json_errors.append(f"{tab_name}/{row[1] if len(row)>1 else '?'}: {e}")

    report.append(f"JSON valides        : {json_ok}/30 onglets vérifiés {'✅' if json_ok == 30 else '❌'}")
    if json_ok < 30: all_ok = False

    # backend.js
    with open("/home/nicolas/Bureau/algebra live/algebra/backend.js", "r") as f:
        backend = f.read()
    backend_ok = "'1ERE'" in backend
    report.append(f"backend.js patché   : {'✅' if backend_ok else '❌'}")
    if not backend_ok: all_ok = False

    print("\n=== RAPPORT INSERT_1ERE ===")
    for line in report:
        print(line)

    if json_errors:
        print("\nJSON INVALIDES :")
        for err in json_errors:
            print(f"  ❌ {err}")

    print(f"\n{'🎉' if all_ok else '⚠️'} PRÊT POUR LA VISIO : {'OUI' if all_ok else 'NON'}")
    return all_ok


# ════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🚀 INSERT_1ERE — Niveau 1ère Spé Maths + Compte Auguste")
    print("=" * 60)

    try:
        step1_insert_exercises()
    except Exception as e:
        print(f"  ❌ Étape 1 échouée : {e}")

    try:
        step2_create_auguste()
    except Exception as e:
        print(f"  ❌ Étape 2 échouée : {e}")

    try:
        step3_simulate_diagnostic()
    except Exception as e:
        print(f"  ❌ Étape 3 échouée : {e}")

    try:
        step4_prepare_boost()
    except Exception as e:
        print(f"  ❌ Étape 4 échouée : {e}")

    # Étape 5 = backend.js déjà patché manuellement
    print("\n🔧 ÉTAPE 5 — backend.js déjà patché (ALLOWED_LEVELS + niveauOrder)")

    try:
        step6_verify()
    except Exception as e:
        print(f"  ❌ Étape 6 échouée : {e}")

    print("\n📌 Étapes restantes (manuelles) :")
    print("  7. clasp push --force && clasp deploy --deploymentId AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF --description 'feat: niveau 1ERE + compte Auguste'")
    print("  8. Créer docs/rapport-1ere.md")
