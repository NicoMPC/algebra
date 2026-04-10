#!/usr/bin/env python3
"""
Test pipeline agent admin autonome.
Simule le cycle complet : analyse → diagnostic → génération → injection → validation.

4 profils test (TS1INE, TS2HUG, TS3JAD, TS4ADA) déjà dans Sheets.
Ce script génère les boosts + prescriptions chapitres, injecte avec publishDate = demain.

Usage : python3 test_pipeline_auto.py
"""

import json
import subprocess
import sys
from datetime import datetime, timedelta
from supabase_helper import sb

def _adapt_scores(rows):
    """Adapte les noms de colonnes Supabase → ancien format Sheets pour compatibilité."""
    adapted = []
    for r in rows:
        adapted.append({
            'Code': r.get('code', ''),
            'Prénom': r.get('prenom', ''),
            'Niveau': r.get('niveau', ''),
            'Chapitre': r.get('chapitre', ''),
            'NumExo': str(r.get('num_exo', '')),
            'Énoncé': r.get('enonce', ''),
            'Résultat': r.get('resultat', ''),
            'Temps(sec)': str(r.get('temps_sec', 0)),
            'NbIndices': str(r.get('nb_indices', 0)),
            'FormuleVue': '1' if r.get('formule_vue') else '0',
            'MauvaiseOption': r.get('mauvaise_option', ''),
            'Draft': r.get('draft', ''),
            'Date': str(r.get('date', '')),
            'Source': r.get('source', ''),
        })
    return adapted

def _adapt_boosts(rows):
    """Adapte daily_boosts Supabase → ancien format Sheets."""
    adapted = []
    for r in rows:
        adapted.append({
            'Code': r.get('code', ''),
            'Date': str(r.get('date', '')),
            'BoostJSON': r.get('boost_json', ''),
            'ExosDone': str(r.get('exos_done', 0)),
        })
    return adapted

TODAY = "2026-04-02"
TOMORROW = "2026-04-03"

# ═══════════════════════════════════════════════════════════════
# ÉTAPE 1 — ANALYSE DES SCORES
# ═══════════════════════════════════════════════════════════════

def analyze_profile(code, scores):
    """Analyse les scores d'un élève et retourne le diagnostic."""
    chap_scores = [s for s in scores if s['Code'] == code and s.get('Source', '') != 'BOOST']
    boost_scores = [s for s in scores if s['Code'] == code and s.get('Source', '') == 'BOOST']

    chapitre = chap_scores[0]['Chapitre'] if chap_scores else '?'
    prenom = chap_scores[0]['Prénom'] if chap_scores else '?'

    nb_easy = sum(1 for s in chap_scores if s['Résultat'] == 'EASY')
    nb_hard = sum(1 for s in chap_scores if s['Résultat'] == 'HARD')
    nb_medium = sum(1 for s in chap_scores if s['Résultat'] == 'MEDIUM')
    total = len(chap_scores)
    score_pct = round(nb_easy / total * 100) if total else 0

    # Patterns
    formule_vue = sum(1 for s in chap_scores if s.get('FormuleVue', '0') == '1')
    indices_high = sum(1 for s in chap_scores if int(s.get('NbIndices', '0')) >= 2)
    temps_moyen = sum(int(s.get('Temps(sec)', '0')) for s in chap_scores) / total if total else 0

    # Erreurs exactes
    erreurs = []
    for s in chap_scores:
        if s['Résultat'] == 'HARD' and s.get('MauvaiseOption', ''):
            erreurs.append({
                'num': s['NumExo'],
                'enonce': s['Énoncé'][:60],
                'repondu': s['MauvaiseOption']
            })

    # Pattern dominant
    patterns = []
    if formule_vue / total > 0.4 and nb_easy / total > 0.3:
        patterns.append("formule-dépendant")
    if any('$-' in e.get('repondu', '') or 'x=-' in e.get('repondu', '') for e in erreurs):
        patterns.append("erreur-de-signe")
    if nb_hard > 0 and temps_moyen < 60:
        patterns.append("confusion-conceptuelle")
    if nb_easy / total > 0.5 and temps_moyen > 120:
        patterns.append("lent-mais-juste")
    if indices_high / total > 0.4:
        patterns.append("bloqué-sans-indices")
    if nb_hard / total > 0.5:
        patterns.append("calcul-mental-fragile")
    if score_pct >= 80:
        patterns.append("quasi-maîtrisé")

    return {
        'code': code,
        'prenom': prenom,
        'chapitre': chapitre,
        'score_pct': score_pct,
        'nb_easy': nb_easy,
        'nb_hard': nb_hard,
        'nb_medium': nb_medium,
        'total': total,
        'formule_vue': formule_vue,
        'indices_high': indices_high,
        'temps_moyen': round(temps_moyen),
        'erreurs': erreurs,
        'patterns': patterns,
    }


# ═══════════════════════════════════════════════════════════════
# ÉTAPE 2 — DIAGNOSTICS
# ═══════════════════════════════════════════════════════════════

DIAGNOSTICS = {
    "TS1INE": {
        "resume": "Calcul mental fragile + ne possède pas les identités remarquables. Confond (a+b)², (a-b)² et a²-b² systématiquement. Factorise x²-9 en x(x-9) au lieu de (x-3)(x+3).",
        "decision": "V2_MEME_CHAPITRE",
        "next_chapitre": "Calcul_Littéral",
        "slots": [
            "Slot 1 : Distributivité simple — remettre en confiance",
            "Slot 2 : Les 3 identités remarquables — distinguer",
            "Slot 3 : Factorisation — reconnaître quelle identité",
            "Slot 4 : Synthèse — développer ET factoriser, pièges"
        ]
    },
    "TS2HUG": {
        "resume": "Maîtrise les équations positives, perd le signe dès qu'il divise par un nombre négatif ou regroupe des termes négatifs. Fractions dans équations = blocage.",
        "decision": "V2_MEME_CHAPITRE",
        "next_chapitre": "Équations",
        "slots": [
            "Slot 1 : Équations simples positives — confiance",
            "Slot 2 : Équations avec négatifs — cibler le signe",
            "Slot 3 : Équations avec fractions — dénominateur commun",
            "Slot 4 : Synthèse — négatifs + fractions + mise en équation"
        ]
    },
    "TS3JAD": {
        "resume": "Calculs fonctions toujours justes mais lente (90-160s). Toutes les erreurs sont sur la lecture graphique : image, antécédent, coefficient directeur. Calcul = OK, graphique = KO.",
        "decision": "V2_MEME_CHAPITRE",
        "next_chapitre": "Fonctions",
        "slots": [
            "Slot 1 : Calculs images/antécédents — confiance + vitesse",
            "Slot 2 : Lecture graphique — image et antécédent sur courbe",
            "Slot 3 : Coefficient directeur + ordonnée à l'origine graphiques",
            "Slot 4 : Synthèse — passer du graphique à la formule et inversement"
        ]
    },
    "TS4ADA": {
        "resume": "Maîtrise la trigonométrie (90%). Ses 2 seules erreurs sont des imprécisions d'arrondi. Prêt pour un nouveau chapitre.",
        "decision": "NOUVEAU_CHAPITRE",
        "next_chapitre": "Théorème_de_Thalès",
        "slots": [
            "Slot 1 : Config Thalès — identifier les droites parallèles",
            "Slot 2 : Calcul de longueur par Thalès direct",
            "Slot 3 : Réciproque de Thalès — prouver le parallélisme",
            "Slot 4 : Synthèse — Thalès + trigo combinés"
        ]
    }
}

# ═══════════════════════════════════════════════════════════════
# ÉTAPE 3 — BOOSTS GÉNÉRÉS (5 exos par profil)
# ═══════════════════════════════════════════════════════════════

BOOSTS = {
    "TS1INE": {
        "insight": "Tes exos du jour ciblent les identités remarquables — on commence doucement pour bien les distinguer.",
        "publishDate": TOMORROW,
        "diagnostic": {
            "resume": "Confond les 3 identités remarquables, factorise x²-9 en x(x-9)",
            "erreurs": ["Q3: (x+5)²=x²+25 (oublie 2ab)", "Q4: x²-9=x(x-9) (confond factorisation)", "Q10: (a-b)²=a²-b² (confond)"],
            "slots": ["Confiance distributivité", "Identité (a+b)²", "Identité a²-b²", "Factorisation", "Piège V/F"]
        },
        "exos": [
            {
                "q": "Développe $3(2x+5)$.",
                "a": "$6x+15$",
                "type": "fill",
                "options": [],
                "f": "$k(a+b) = ka + kb$",
                "f_disabled": False,
                "steps": [
                    "On distribue le $3$ sur chaque terme entre parenthèses",
                    "$3 \\times 2x + 3 \\times 5 = ?$"
                ],
                "lvl": 1
            },
            {
                "q": "Développe $(x+4)^2$.",
                "a": "$x^2+8x+16$",
                "type": "qcm",
                "options": ["$x^2+8x+16$", "$x^2+16$", "$x^2+4x+16$"],
                "f": "$(a+b)^2 = a^2 + 2ab + b^2$",
                "f_disabled": False,
                "steps": [
                    "Identité remarquable $(a+b)^2$ avec $a=x$ et $b=4$",
                    "$x^2 + 2 \\times x \\times 4 + 4^2 = ?$"
                ],
                "lvl": 1
            },
            {
                "q": "Factorise $x^2 - 25$.",
                "a": "$(x-5)(x+5)$",
                "type": "qcm",
                "options": ["$(x-5)(x+5)$", "$x(x-25)$", "$(x-5)^2$"],
                "f": "$a^2 - b^2 = (a-b)(a+b)$",
                "f_disabled": False,
                "steps": [
                    "On reconnaît une différence de deux carrés : $x^2 = x^2$ et $25 = 5^2$",
                    "On applique $a^2 - b^2 = (a-b)(a+b)$ avec $a = x$ et $b = ?$"
                ],
                "lvl": 1
            },
            {
                "q": "Factorise $9x^2 - 4$.",
                "a": "$(3x-2)(3x+2)$",
                "type": "fill",
                "options": [],
                "f": "$a^2 - b^2 = (a-b)(a+b)$",
                "f_disabled": False,
                "steps": [
                    "$9x^2 = (3x)^2$ et $4 = 2^2$ — c'est une différence de carrés",
                    "$(3x)^2 - 2^2 = (3x - ?)(3x + ?)$"
                ],
                "lvl": 1
            },
            {
                "q": "$(x-3)^2 = x^2 - 9$. Vrai ou Faux ?",
                "a": "Faux",
                "type": "vf",
                "options": ["Vrai", "Faux"],
                "f": "",
                "f_disabled": True,
                "steps": [
                    "Développe $(x-3)^2$ avec l'identité $(a-b)^2 = a^2 - 2ab + b^2$",
                    "$x^2 - 2 \\times x \\times 3 + 9 = x^2 - 6x + 9$ — est-ce la même chose que $x^2 - 9$ ?"
                ],
                "lvl": 1
            }
        ]
    },

    "TS2HUG": {
        "insight": "Tes exos du jour ciblent les équations avec des nombres négatifs — le piège classique du signe.",
        "publishDate": TOMORROW,
        "diagnostic": {
            "resume": "Perd le signe quand il divise par un négatif ou regroupe des termes négatifs",
            "erreurs": ["Q7: -3x+9=0 → x=-3 (signe inversé)", "Q9: -2x+4=-x-3 → x=-7 (regroupement)", "Q13: -x/2+3=0 → x=-6 (signe)"],
            "slots": ["Confiance", "Négatif simple", "Regroupement négatif", "Fraction+négatif", "Piège V/F"]
        },
        "exos": [
            {
                "q": "Résous $4x - 12 = 0$.",
                "a": "$x = 3$",
                "type": "fill",
                "options": [],
                "f": "",
                "f_disabled": True,
                "steps": [
                    "Isole $x$ : $4x = 12$",
                    "$x = \\frac{12}{4} = ?$"
                ],
                "lvl": 1
            },
            {
                "q": "Résous $-5x + 20 = 0$.",
                "a": "$x = 4$",
                "type": "qcm",
                "options": ["$x = 4$", "$x = -4$", "$x = -20$"],
                "f": "",
                "f_disabled": True,
                "steps": [
                    "On isole : $-5x = -20$",
                    "On divise par $-5$ (attention au signe !) : $x = \\frac{-20}{-5} = ?$"
                ],
                "lvl": 1
            },
            {
                "q": "Résous $-3x + 7 = x - 5$.",
                "a": "$x = 3$",
                "type": "qcm",
                "options": ["$x = 3$", "$x = -3$", "$x = \\frac{1}{2}$"],
                "f": "",
                "f_disabled": True,
                "steps": [
                    "Regroupe les $x$ à gauche : $-3x - x = -5 - 7$, soit $-4x = ?$",
                    "$-4x = -12$, donc $x = \\frac{-12}{-4} = ?$"
                ],
                "lvl": 1
            },
            {
                "q": "Résous $\\frac{-x + 6}{3} = 1$.",
                "a": "$x = 3$",
                "type": "fill",
                "options": [],
                "f": "",
                "f_disabled": True,
                "steps": [
                    "Multiplie les deux côtés par $3$ : $-x + 6 = ?$",
                    "$-x = -3$, donc $x = ?$"
                ],
                "lvl": 1
            },
            {
                "q": "Si $-2x = 8$, alors $x = 4$. Vrai ou Faux ?",
                "a": "Faux",
                "type": "vf",
                "options": ["Vrai", "Faux"],
                "f": "",
                "f_disabled": True,
                "steps": [
                    "On divise $8$ par $-2$ (pas par $2$)",
                    "$x = \\frac{8}{-2} = ?$ — le signe compte !"
                ],
                "lvl": 1
            }
        ]
    },

    "TS3JAD": {
        "insight": "Tes exos du jour ciblent la lecture graphique — lire une image et un antécédent sur une courbe.",
        "publishDate": TOMORROW,
        "diagnostic": {
            "resume": "Calculs fonctions OK mais toutes les erreurs sont sur lecture graphique",
            "erreurs": ["Q7: f(3) lu incorrect", "Q12: antécédent de 2 faux", "Q13: intersection graphique faux"],
            "slots": ["Confiance calcul", "Lire image", "Lire antécédent", "Coeff directeur graphique", "Piège V/F"]
        },
        "exos": [
            {
                "q": "Calcule $f(4)$ si $f(x) = -3x + 10$.",
                "a": "$-2$",
                "type": "fill",
                "options": [],
                "f": "",
                "f_disabled": True,
                "steps": [
                    "Remplace $x$ par $4$ : $f(4) = -3 \\times 4 + 10$",
                    "$= -12 + 10 = ?$"
                ],
                "lvl": 1
            },
            {
                "q": "Sur le graphique d'une fonction affine, le point $(2 ; 5)$ est sur la courbe. Que vaut $f(2)$ ?",
                "a": "$5$",
                "type": "qcm",
                "options": ["$5$", "$2$", "$7$"],
                "f": "",
                "f_disabled": True,
                "steps": [
                    "Un point $(x ; y)$ sur la courbe signifie que $f(x) = y$",
                    "Donc si $(2 ; 5)$ est sur la courbe, $f(2) = ?$"
                ],
                "lvl": 1
            },
            {
                "q": "Sur le graphique, la droite passe par $(0 ; 3)$ et $(4 ; 7)$. Quel est l'antécédent de $7$ ?",
                "a": "$4$",
                "type": "qcm",
                "options": ["$4$", "$7$", "$3$"],
                "f": "",
                "f_disabled": True,
                "steps": [
                    "L'antécédent de $7$ est la valeur de $x$ telle que $f(x) = 7$",
                    "On lit sur le graphique : quand $y = 7$, $x = ?$"
                ],
                "lvl": 1
            },
            {
                "q": "Une droite passe par $(0 ; 1)$ et $(3 ; 7)$. Calcule son coefficient directeur.",
                "a": "$2$",
                "type": "fill",
                "options": [],
                "f": "$a = \\frac{y_B - y_A}{x_B - x_A}$",
                "f_disabled": False,
                "steps": [
                    "Le coefficient directeur $a = \\frac{\\Delta y}{\\Delta x}$",
                    "$a = \\frac{7 - 1}{3 - 0} = \\frac{?}{?}$"
                ],
                "lvl": 1
            },
            {
                "q": "Sur un graphique, si la droite descend de gauche à droite, alors $a > 0$. Vrai ou Faux ?",
                "a": "Faux",
                "type": "vf",
                "options": ["Vrai", "Faux"],
                "f": "",
                "f_disabled": True,
                "steps": [
                    "Une droite qui descend de gauche à droite a un coefficient directeur négatif",
                    "Donc $a < 0$, pas $a > 0$. C'est vrai ou faux ?"
                ],
                "lvl": 1
            }
        ]
    },

    "TS4ADA": {
        "insight": "Bravo pour la trigo ! On passe au théorème de Thalès — nouveau chapitre pour toi.",
        "publishDate": TOMORROW,
        "diagnostic": {
            "resume": "Trigo maîtrisée (90%), 2 erreurs d'arrondi mineures. Prêt pour nouveau chapitre.",
            "erreurs": ["Q12: arrondi 9,17 vs correct", "Q17: arrondi 115,7 vs correct"],
            "slots": ["Confiance Thalès direct", "Calcul longueur", "Réciproque", "Agrandissement/réduction", "Synthèse"]
        },
        "exos": [
            {
                "q": "Dans un triangle $ABC$ avec $(MN) \\parallel (BC)$, $AM = 4$, $AB = 10$, $AN = 3$. Calcule $AC$.",
                "a": "$7{,}5$",
                "type": "fill",
                "options": [],
                "f": "$\\frac{AM}{AB} = \\frac{AN}{AC}$",
                "f_disabled": False,
                "steps": [
                    "Par le théorème de Thalès : $\\frac{AM}{AB} = \\frac{AN}{AC}$",
                    "$\\frac{4}{10} = \\frac{3}{AC}$, donc $AC = \\frac{3 \\times 10}{4} = ?$"
                ],
                "lvl": 1
            },
            {
                "q": "$(MN) \\parallel (BC)$, $AM = 6$, $MB = 9$, $MN = 4$. Calcule $BC$.",
                "a": "$10$",
                "type": "qcm",
                "options": ["$10$", "$6$", "$15$"],
                "f": "$\\frac{AM}{AB} = \\frac{MN}{BC}$",
                "f_disabled": False,
                "steps": [
                    "$AB = AM + MB = 6 + 9 = 15$. Par Thalès : $\\frac{AM}{AB} = \\frac{MN}{BC}$",
                    "$\\frac{6}{15} = \\frac{4}{BC}$, donc $BC = \\frac{4 \\times 15}{6} = ?$"
                ],
                "lvl": 1
            },
            {
                "q": "$\\frac{AM}{AB} = \\frac{3}{5}$ et $\\frac{AN}{AC} = \\frac{6}{10}$. Les droites $(MN)$ et $(BC)$ sont-elles parallèles ?",
                "a": "Vrai",
                "type": "vf",
                "options": ["Vrai", "Faux"],
                "f": "",
                "f_disabled": True,
                "steps": [
                    "On compare les rapports : $\\frac{3}{5} = 0{,}6$ et $\\frac{6}{10} = ?$",
                    "Les rapports sont-ils égaux ? Si oui, la réciproque de Thalès confirme le parallélisme"
                ],
                "lvl": 1
            },
            {
                "q": "Un poteau de $2$ m projette une ombre de $3$ m. Un arbre voisin projette une ombre de $12$ m. Quelle est la hauteur de l'arbre ?",
                "a": "$8$",
                "type": "fill",
                "options": [],
                "f": "",
                "f_disabled": True,
                "steps": [
                    "Situation de Thalès (rayons solaires parallèles) : $\\frac{\\text{poteau}}{\\text{ombre poteau}} = \\frac{\\text{arbre}}{\\text{ombre arbre}}$",
                    "$\\frac{2}{3} = \\frac{h}{12}$, donc $h = \\frac{2 \\times 12}{3} = ?$"
                ],
                "lvl": 1
            },
            {
                "q": "$(MN) \\parallel (BC)$, $AM = 3$, $AB = 5$, $BC = 8$. Calcule $MN$.",
                "a": "$4{,}8$",
                "type": "qcm",
                "options": ["$4{,}8$", "$4{,}5$", "$5{,}2$"],
                "f": "$\\frac{AM}{AB} = \\frac{MN}{BC}$",
                "f_disabled": False,
                "steps": [
                    "Par Thalès : $\\frac{AM}{AB} = \\frac{MN}{BC}$",
                    "$\\frac{3}{5} = \\frac{MN}{8}$, donc $MN = \\frac{3 \\times 8}{5} = ?$"
                ],
                "lvl": 1
            }
        ]
    }
}


# ═══════════════════════════════════════════════════════════════
# ÉTAPE 4 — VALIDATION
# ═══════════════════════════════════════════════════════════════

def validate_boost(code, boost_data):
    """Valide un boost via validate_exos.py."""
    filename = f"/tmp/boost_{code}.json"
    with open(filename, 'w') as f:
        json.dump(boost_data['exos'], f, ensure_ascii=False, indent=2)

    result = subprocess.run(
        ['python3', 'validate_exos.py', filename],
        capture_output=True, text=True
    )
    return result.stdout, result.stderr, result.returncode


# ═══════════════════════════════════════════════════════════════
# ÉTAPE 5 — INJECTION
# ═══════════════════════════════════════════════════════════════

def inject_boosts(boosts_data):
    """Injecte les boosts dans DailyBoosts avec publishDate = demain."""
    rows = []
    for code, boost in boosts_data.items():
        boost_json = json.dumps(boost, ensure_ascii=False)
        # DailyBoosts: Code, Date, BoostJSON, ExosDone
        rows.append([code, TOMORROW, boost_json, 0])

    sb.insert("daily_boosts", [{"code": r[0], "date": r[1], "boost_json": r[2], "exos_done": int(r[3])} for r in rows])
    return len(rows)


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("🤖 PIPELINE AGENT ADMIN AUTONOME — TEST")
    print(f"   Date : {TODAY} | publishDate : {TOMORROW}")
    print("=" * 60)

    # ── Étape 1 : Lire les Scores ──
    print("\n📊 ÉTAPE 1 — Lecture des Scores...")
    all_scores = _adapt_scores(sb.get_scores())
    test_codes = ["TS1INE", "TS2HUG", "TS3JAD", "TS4ADA"]

    analyses = {}
    for code in test_codes:
        a = analyze_profile(code, all_scores)
        analyses[code] = a
        print(f"\n  {a['prenom']:8s} ({code}) — {a['chapitre']}")
        print(f"    Score: {a['score_pct']}% ({a['nb_easy']}/{a['total']} EASY)")
        print(f"    Patterns: {', '.join(a['patterns']) or 'aucun détecté'}")
        print(f"    FormuleVue: {a['formule_vue']}/{a['total']} | Indices≥2: {a['indices_high']}/{a['total']} | Temps moy: {a['temps_moyen']}s")
        if a['erreurs']:
            print(f"    Erreurs clés:")
            for e in a['erreurs'][:3]:
                print(f"      ❌ Q{e['num']}: {e['enonce']} → {e['repondu']}")

    # ── Étape 2 : Diagnostics ──
    print("\n\n📋 ÉTAPE 2 — Diagnostics...")
    for code in test_codes:
        d = DIAGNOSTICS[code]
        a = analyses[code]
        print(f"\n  {a['prenom']} — {d['decision']}")
        print(f"    Diagnostic: {d['resume'][:80]}...")
        print(f"    Prochain: {d['next_chapitre']}")
        for s in d['slots']:
            print(f"      • {s}")

    # ── Étape 3 : Validation des boosts ──
    print("\n\n✅ ÉTAPE 3 — Validation qualité boosts...")
    all_ok = True
    for code in test_codes:
        stdout, stderr, rc = validate_boost(code, BOOSTS[code])
        prenom = analyses[code]['prenom']
        if rc == 0:
            print(f"  ✅ {prenom} ({code}) — PASS")
        else:
            print(f"  ❌ {prenom} ({code}) — FAIL")
            print(f"     {stdout}")
            print(f"     {stderr}")
            all_ok = False

    if not all_ok:
        print("\n⛔ Validation échouée — pas d'injection")
        sys.exit(1)

    # ── Étape 4 : Injection ──
    print("\n\n💉 ÉTAPE 4 — Injection dans DailyBoosts...")
    nb = inject_boosts(BOOSTS)
    print(f"  ✅ {nb} boosts injectés avec publishDate = {TOMORROW}")

    # ── Étape 5 : Vérification ──
    print("\n\n🔍 ÉTAPE 5 — Vérification publishDate...")
    boosts = _adapt_boosts(sb.read("daily_boosts"))
    for code in test_codes:
        tomorrow_boosts = [b for b in boosts if b['Code'] == code and b.get('Date', '') == TOMORROW]
        if tomorrow_boosts:
            boost_json = json.loads(tomorrow_boosts[0]['BoostJSON'])
            has_publish = boost_json.get('publishDate') == TOMORROW
            prenom = analyses[code]['prenom']
            print(f"  {'✅' if has_publish else '⚠️'} {prenom} — DailyBoosts row pour {TOMORROW}, publishDate={'OK' if has_publish else 'MANQUANT'}")
            print(f"     ExosDone: {tomorrow_boosts[0].get('ExosDone', '?')}")
            print(f"     Insight: {boost_json.get('insight', '?')[:60]}...")
        else:
            print(f"  ❌ {code} — Pas de boost trouvé pour {TOMORROW}")

    # ── Résumé ──
    print("\n\n" + "=" * 60)
    print("📊 RÉSUMÉ PIPELINE")
    print("=" * 60)
    for code in test_codes:
        a = analyses[code]
        d = DIAGNOSTICS[code]
        print(f"  {a['prenom']:8s} | {a['score_pct']:3d}% | {d['decision']:20s} | → {d['next_chapitre']}")

    print(f"\n  Boosts injectés : {nb} | publishDate : {TOMORROW}")
    print(f"  Prochaine connexion élève : les boosts seront livrés le {TOMORROW}")
    print()
    print("  🎯 Pour les CHAPITRES (20 exos), l'agent devrait :")
    print("     - Inès/Hugo/Jade : V2 même chapitre (ciblé lacunes)")
    print("     - Adam : Nouveau chapitre (Théorème de Thalès)")
    print("     → À générer dans une 2ème passe (80 exos)")


if __name__ == "__main__":
    main()
