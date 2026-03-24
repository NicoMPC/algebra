#!/usr/bin/env python3
"""
Stress-test Monsieur Exos — 10 jours simulés, 3 élèves fictifs.
Prouve l'adaptation, l'anti-doublon, la précision diagnostique.
"""

import json, os, sys, random, hashlib
from datetime import datetime, timedelta
from sheets import sh

# ── Config ────────────────────────────────────────────────────
BASE_DATE = datetime(2026, 3, 15)  # J1 = 15 mars
SALT = "AB22"

LOG_FILE = "/home/nicolas/Bureau/algebra live/algebra/stress_test_log.md"
EXOS_DIR = "/home/nicolas/Bureau/algebra live/algebra/stress_test_exos"
os.makedirs(EXOS_DIR, exist_ok=True)

# ── Helpers ───────────────────────────────────────────────────

def hash_pwd(email, pwd):
    return hashlib.sha256(f"{email}::{pwd}::{SALT}".encode()).hexdigest()

def date_str(day_offset):
    return (BASE_DATE + timedelta(days=day_offset)).strftime("%Y-%m-%d")

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg)

# ── CLEANUP before start ─────────────────────────────────────

def cleanup():
    """Remove all TEST_ users from Users, Scores, and Suivi."""
    print("🧹 Cleaning up TEST_ data...")

    # Users
    users_raw = sh.read_raw("Users")
    cleaned = [users_raw[0]] + [r for r in users_raw[1:] if not r[0].startswith("TEST_")]
    if len(cleaned) < len(users_raw):
        sh.write_rows("Users", cleaned)
        print(f"  Users: removed {len(users_raw) - len(cleaned)} test rows")

    # Scores
    scores_raw = sh.read_raw("Scores")
    cleaned = [scores_raw[0]] + [r for r in scores_raw[1:] if len(r) > 0 and not r[0].startswith("TEST_")]
    if len(cleaned) < len(scores_raw):
        sh.write_rows("Scores", cleaned)
        print(f"  Scores: removed {len(scores_raw) - len(cleaned)} test rows")

    # Suivi
    suivi_raw = sh.read_raw("👁 Suivi")
    cleaned = [suivi_raw[0]] + [r for r in suivi_raw[1:] if len(r) < 21 or not r[20].startswith("TEST_")]
    if len(cleaned) < len(suivi_raw):
        sh.write_rows("👁 Suivi", cleaned)
        print(f"  Suivi: removed {len(suivi_raw) - len(cleaned)} test rows")

    print("✅ Cleanup done")

# ── SETUP: Create test users ─────────────────────────────────

def setup_users():
    """Create 3 test users in Users sheet."""
    users = [
        ["TEST_LINA", "Lina", "6EME", "lina@test.fr", hash_pwd("lina@test.fr", "test"), date_str(0), "0", "", date_str(0), "", "1", "", "", "", "", ""],
        ["TEST_RAYAN", "Rayan", "4EME", "rayan@test.fr", hash_pwd("rayan@test.fr", "test"), date_str(0), "0", "", date_str(0), "", "1", "", "", "", "", ""],
        ["TEST_EMMA", "Emma", "3EME", "emma@test.fr", hash_pwd("emma@test.fr", "test"), date_str(0), "0", "", date_str(0), "", "1", "", "", "", "", ""],
    ]
    for u in users:
        sh.append_row("Users", u)
    print(f"✅ Created {len(users)} test users")

def setup_suivi():
    """Create Suivi rows for test users."""
    rows = [
        # ACTION, Prénom, Niveau, DernièreConnexion, Ch1, RésuméCh1, NouveauCh1, Ch2, RésuméCh2, NouveauCh2, Ch3, RésuméCh3, NouveauCh3, Ch4, RésuméCh4, NouveauCh4, Boost, RésuméBoost, NouveauBoost, Rapport, Code
        ["👍 RAS", "Lina", "6EME", date_str(0), "Fractions", "0/20", "", "Proportionnalité", "0/20", "", "", "", "", "", "", "", "—", "", "", "", "TEST_LINA"],
        ["👍 RAS", "Rayan", "4EME", date_str(0), "Puissances", "0/20", "", "Calcul_Littéral", "0/20", "", "", "", "", "", "", "", "—", "", "", "", "TEST_RAYAN"],
        ["👍 RAS", "Emma", "3EME", date_str(0), "Fonctions", "0/20", "", "Thalès", "0/20", "", "", "", "", "", "", "", "—", "", "", "", "TEST_EMMA"],
    ]
    for r in rows:
        sh.append_row("👁 Suivi", r)
    print(f"✅ Created {len(rows)} Suivi rows")


# ── SCORE INJECTION per profile ──────────────────────────────

# Score row: Code, Prénom, Niveau, Chapitre, NumExo, Énoncé, Résultat, Temps(sec), NbIndices, FormuleVue, MauvaiseOption, Draft, Date, Source

SCORE_BUFFER = []

def inject_score(code, prenom, niveau, chapitre, num_exo, enonce, resultat, temps, nb_indices, formule_vue, mauvaise_option, date, source=""):
    row = [code, prenom, niveau, chapitre, str(num_exo), enonce, resultat, str(temps), str(nb_indices), str(formule_vue), mauvaise_option, "", date, source]
    SCORE_BUFFER.append(row)

def flush_scores():
    """Write all buffered scores in a single batch."""
    global SCORE_BUFFER
    if not SCORE_BUFFER:
        return
    from sheets import SHEET_ID
    sh._api.values().append(
        spreadsheetId=SHEET_ID,
        range="Scores!A1",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body={"values": SCORE_BUFFER}
    ).execute()
    print(f"  💾 Flushed {len(SCORE_BUFFER)} scores")
    SCORE_BUFFER = []

# ── LINA's score profiles (slow but correct, formula-dependent) ──

LINA_FRACTIONS_ENONCES = {
    1: ("Calcule $\\frac{1}{2} + \\frac{1}{3}$.", "$\\frac{5}{6}$"),
    2: ("Simplifie $\\frac{6}{8}$.", "$\\frac{3}{4}$"),
    3: ("Calcule $\\frac{2}{5} + \\frac{1}{5}$.", "$\\frac{3}{5}$"),
    4: ("Lucas a mangé $\\frac{1}{4}$ d'un gâteau. Il en reste combien ?", "$\\frac{3}{4}$"),
    5: ("Calcule $\\frac{3}{4} - \\frac{1}{2}$.", "$\\frac{1}{4}$"),
    6: ("Simplifie $\\frac{12}{18}$.", "$\\frac{2}{3}$"),
    7: ("Calcule $\\frac{2}{3} \\times \\frac{3}{4}$.", "$\\frac{1}{2}$"),
    8: ("Marie partage $\\frac{3}{5}$ d'une pizza entre 3 amis. Chacun reçoit...", "$\\frac{1}{5}$"),
    9: ("Calcule $\\frac{7}{10} - \\frac{3}{10}$.", "$\\frac{2}{5}$"),
    10: ("Range $\\frac{1}{3}$, $\\frac{1}{4}$, $\\frac{1}{2}$ du plus petit au plus grand.", "$\\frac{1}{4} < \\frac{1}{3} < \\frac{1}{2}$"),
    11: ("Calcule $\\frac{2}{3} + \\frac{5}{6}$.", "$\\frac{3}{2}$"),
    12: ("Un réservoir est rempli aux $\\frac{3}{8}$. On ajoute $\\frac{1}{4}$. Remplissage total ?", "$\\frac{5}{8}$"),
    13: ("Calcule $\\frac{4}{5} \\times \\frac{5}{8}$.", "$\\frac{1}{2}$"),
    14: ("Simplifie $\\frac{15}{25}$.", "$\\frac{3}{5}$"),
    15: ("Calcule $\\frac{5}{6} - \\frac{1}{3}$.", "$\\frac{1}{2}$"),
    16: ("Hugo a $\\frac{2}{3}$ d'une tablette. Il en donne $\\frac{1}{6}$. Combien reste ?", "$\\frac{1}{2}$"),
    17: ("Calcule $\\frac{1}{2} + \\frac{1}{4} + \\frac{1}{8}$.", "$\\frac{7}{8}$"),
    18: ("Calcule $\\frac{3}{7} \\times \\frac{14}{9}$.", "$\\frac{2}{3}$"),
    19: ("Un parcours fait $\\frac{3}{4}$ km. Jade en fait $\\frac{2}{3}$. Distance parcourue ?", "$\\frac{1}{2}$ km"),
    20: ("Calcule $\\frac{5}{12} + \\frac{3}{8}$.", "$\\frac{19}{24}$"),
}

LINA_PROPORTIONNALITE_ENONCES = {
    1: ("3 cahiers coûtent 6 euros. Combien coûtent 5 cahiers ?", "10 euros"),
    2: ("Un plan a une échelle 1/100. 3 cm sur le plan = combien en réalité ?", "3 m"),
    3: ("4 kg de pommes coûtent 8 euros. Prix de 7 kg ?", "14 euros"),
    4: ("En 2h, Léa parcourt 10 km. Combien en 5h ?", "25 km"),
    5: ("5 ouvriers font un mur en 10 jours. Combien de jours pour 10 ouvriers ?", "5 jours"),
    6: ("Un recette pour 4 personnes demande 200 g de farine. Pour 6 personnes ?", "300 g"),
    7: ("Le tableau est-il proportionnel ? 2→6, 3→9, 5→15", "Oui"),
    8: ("Noé court 3 km en 15 min. Vitesse en km/h ?", "12 km/h"),
    9: ("Sur une carte 1/50000, 4 cm représentent ?", "2 km"),
    10: ("8 croissants coûtent 12 euros. Prix de 5 ?", "7,50 euros"),
    11: ("12 litres pour 100 km. Combien pour 250 km ?", "30 litres"),
    12: ("Un triangle réduit a un côté de 3 cm (original 9 cm). Rapport ?", "$\\frac{1}{3}$"),
    13: ("Adam gagne 45 euros pour 5h de travail. Salaire horaire ?", "9 euros"),
    14: ("Le pourcentage de filles dans une classe de 30 si 18 sont des filles ?", "60%"),
    15: ("Augmentation de 20% sur 50 euros ?", "60 euros"),
    16: ("Réduction de 25% sur 80 euros ?", "60 euros"),
    17: ("Inès achète 3 T-shirts à 12 euros. Prix pour 7 T-shirts ?", "28 euros"),
    18: ("Une maquette est au 1/200. La tour fait 5 cm. Hauteur réelle ?", "10 m"),
    19: ("2,5 kg de tomates à 3,60 euros le kg. Prix total ?", "9 euros"),
    20: ("Un trajet de 150 km en 2h. Vitesse moyenne ?", "75 km/h"),
}

# ── RAYAN's score profiles (fast, sign errors) ──

RAYAN_PUISSANCES_ENONCES = {
    1: ("Calcule $2^3$.", "8"),
    2: ("Simplifie $10^2 \\times 10^3$.", "$10^5$"),
    3: ("Calcule $(-3)^2$.", "9"),
    4: ("Simplifie $\\frac{5^4}{5^2}$.", "$5^2$"),
    5: ("Calcule $(-2)^3$.", "$-8$"),
    6: ("Écris $0{,}001$ comme puissance de 10.", "$10^{-3}$"),
    7: ("Simplifie $(2^3)^2$.", "$2^6$"),
    8: ("Calcule $4^0$.", "1"),
    9: ("Calcule $(-1)^{10}$.", "1"),
    10: ("Écris $3^{-2}$ sous forme de fraction.", "$\\frac{1}{9}$"),
    11: ("Simplifie $\\frac{2^5 \\times 2^3}{2^4}$.", "$2^4$"),
    12: ("Calcule $(-5)^2 - 5^2$.", "0"),
    13: ("Écris en notation scientifique : 0,00045.", "$4{,}5 \\times 10^{-4}$"),
    14: ("Simplifie $(3 \\times 10^2)^2$.", "$9 \\times 10^4$"),
    15: ("Calcule $2^{-3}$.", "$\\frac{1}{8}$"),
    16: ("Simplifie $\\frac{6^3 \\times 6}{6^2}$.", "$6^2$"),
    17: ("Écris $2{,}7 \\times 10^3$ en écriture décimale.", "2700"),
    18: ("Calcule $(-4)^3$.", "$-64$"),
    19: ("Simplifie $(10^{-2})^3$.", "$10^{-6}$"),
    20: ("Calcule $3^2 + (-3)^2$.", "18"),
}

RAYAN_CALCUL_ENONCES = {
    1: ("Développe $(x+3)(x+2)$.", "$x^2 + 5x + 6$"),
    2: ("Factorise $3x + 12$.", "$3(x + 4)$"),
    3: ("Développe $(2x-1)^2$.", "$4x^2 - 4x + 1$"),
    4: ("Simplifie $5x - 3 + 2x + 7$.", "$7x + 4$"),
    5: ("Factorise $x^2 - 9$.", "$(x-3)(x+3)$"),
    6: ("Développe $(x+5)(x-5)$.", "$x^2 - 25$"),
    7: ("Résous $3x + 6 = 0$.", "$x = -2$"),
    8: ("Développe $-2(3x - 4)$.", "$-6x + 8$"),
    9: ("Factorise $x^2 - 4x$.", "$x(x-4)$"),
    10: ("Développe $(3x+1)^2$.", "$9x^2 + 6x + 1$"),
    11: ("Calcule pour $x=-2$ : $x^2 - 3x + 1$.", "11"),
    12: ("Développe $(x-4)^2$.", "$x^2 - 8x + 16$"),
    13: ("Factorise $25x^2 - 1$.", "$(5x-1)(5x+1)$"),
    14: ("Résous $5x - 3 = 2x + 9$.", "$x = 4$"),
    15: ("Développe $3(x+2) - 2(x-1)$.", "$x + 8$"),
    16: ("Factorise $4x^2 - 12x$.", "$4x(x-3)$"),
    17: ("Développe $(2x+3)(x-4)$.", "$2x^2 - 5x - 12$"),
    18: ("Simplifie $\\frac{6x^2}{3x}$.", "$2x$"),
    19: ("Résous $-4x + 8 = 0$.", "$x = 2$"),
    20: ("Développe $(x-3)(x+7)$.", "$x^2 + 4x - 21$"),
}

# ── EMMA's score profiles (strong, holes in graph reading & special cases) ──

EMMA_FONCTIONS_ENONCES = {
    1: ("Soit $f(x) = 2x - 3$. Calcule $f(4)$.", "5"),
    2: ("Soit $f(x) = -x + 5$. Calcule $f(0)$.", "5"),
    3: ("L'image de $3$ par $f(x) = x^2 - 1$ est :", "8"),
    4: ("Quel est l'antécédent de $7$ par $f(x) = 2x + 1$ ?", "3"),
    5: ("$f(x) = 3x - 6$. Pour quel $x$ a-t-on $f(x) = 0$ ?", "2"),
    6: ("Sur le graphique, lire $f(2)$.", "4"),  # graph reading - HARD
    7: ("Soit $f(x) = x^2$. Calcule $f(-3)$.", "9"),
    8: ("$f(x) = -2x + 8$. La fonction est-elle croissante ou décroissante ?", "Décroissante"),
    9: ("Lire graphiquement l'antécédent de $3$.", "1"),  # graph reading - HARD
    10: ("$f(x) = 4x - 2$. Calcule $f(-1)$.", "$-6$"),
    11: ("Détermine la fonction affine passant par $(0, 3)$ et $(2, 7)$.", "$f(x) = 2x + 3$"),
    12: ("Sur le graphique, déterminer si la fonction est affine.", "Oui"),  # graph reading
    13: ("$f(x) = -3x + 9$. Calcule l'antécédent de $0$.", "3"),
    14: ("$g(x) = x^2 - 4$. Calcule $g(0)$ et $g(2)$.", "$g(0)=-4$, $g(2)=0$"),
    15: ("Le coefficient directeur de la droite passant par $(1,5)$ et $(3,11)$ est :", "3"),
    16: ("$f(x) = |x - 2|$. Calcule $f(0)$.", "2"),  # special case
    17: ("$f(x) = \\frac{1}{x}$. Calcule $f(4)$.", "$\\frac{1}{4}$"),
    18: ("L'ordonnée à l'origine de $f(x) = -x + 7$ est :", "7"),
    19: ("Lire graphiquement les coordonnées du point d'intersection avec l'axe des abscisses.", "$(3, 0)$"),  # graph
    20: ("$f(x) = 2x^2 - 8$. Résous $f(x) = 0$.", "$x = 2$ ou $x = -2$"),
}

EMMA_THALES_ENONCES = {
    1: ("Dans un triangle $ABC$, $M \\in [AB]$, $N \\in [AC]$, $(MN) \\parallel (BC)$. $AM=3$, $AB=9$, $AN=2$. Calcule $AC$.", "6"),
    2: ("$AM=4$, $AB=12$, $BC=15$. Calcule $MN$.", "5"),
    3: ("Vérifie que $(MN) \\parallel (BC)$ si $AM=2$, $AB=6$, $AN=3$, $AC=9$.", "Oui"),
    4: ("$AM=5$, $MB=10$, $AN=3$. Calcule $NC$.", "6"),
    5: ("$AM=4$, $AB=8$, $MN=6$. Calcule $BC$.", "12"),
    6: ("Deux droites parallèles coupées par deux sécantes : $a=3$, $b=4$, $c=6$. Calcule $d$.", "8"),
    7: ("$\\frac{AM}{AB} = \\frac{AN}{AC}$. Si $AM=2$, $AB=10$, $AC=15$, calcule $AN$.", "3"),
    8: ("Démontre que $(MN)$ n'est PAS parallèle à $(BC)$ si $\\frac{AM}{AB} = \\frac{2}{5}$ et $\\frac{AN}{AC} = \\frac{3}{8}$.", "Non parallèle"),  # special case
    9: ("Dans un agrandissement, $k = \\frac{3}{2}$. Un côté mesure 4 cm. Mesure de l'image ?", "6 cm"),
    10: ("$AM = 3$, $AB = 7$, $AN = 4$. Calcule $AC$ arrondi au dixième.", "$\\frac{28}{3} \\approx 9{,}3$"),
    11: ("Thalès réciproque : $\\frac{AM}{AB} = \\frac{2}{6}$, $\\frac{AN}{AC} = \\frac{3}{9}$. Conclusion ?", "$(MN) \\parallel (BC)$"),  # reciprocal
    12: ("Dans un triangle, $AM=6$, $AB=18$, $BC=24$. Calcule $MN$.", "8"),
    13: ("Deux poteaux : ombre 3m (hauteur 2m) et ombre 7,5m. Hauteur du 2e ?", "5 m"),
    14: ("$AM=4$, $MB=8$, $MN=5$. Calcule $BC$.", "15"),
    15: ("$(MN) \\parallel (BC)$, $AM=x$, $AB=3x$, $MN=4$, $BC=12$. Vérifier la cohérence.", "Oui, $\\frac{1}{3}$ dans les deux cas"),
    16: ("Thalès réciproque : $\\frac{AM}{AB} = \\frac{4}{10}$ et $\\frac{AN}{AC} = \\frac{6}{16}$. Parallèles ?", "Non"),  # reciprocal trap
    17: ("$k=\\frac{2}{5}$ réduction. Côté original 20 cm. Image ?", "8 cm"),
    18: ("$AM=3$, $AB=9$, $AN=2$, $AC=6$, $MN=4$. Calcule $BC$.", "12"),
    19: ("Configuration papillon : $\\frac{OA}{OC} = \\frac{OB}{OD}$ ? $OA=3, OC=6, OB=4, OD=8$.", "Oui, $(AB) \\parallel (CD)$"),
    20: ("Cas particulier : $M$ milieu de $[AB]$. $AB=10$, $BC=14$. Calcule $MN$.", "7"),
}


# ── Day-by-day score simulation ──────────────────────────────

def inject_day_scores(day):
    """Inject realistic scores for each student on given day."""
    d = date_str(day)

    # ── LINA: slow, correct, formula-dependent ──
    # Days 1-5: doing Fractions (4 exos/day), always EASY, slow (130-180s), FormuleVue=1
    # Day 5 SPECIAL: all HARD (bad day)
    # Days 6-10: speeds up (80-100s), starts without formula

    if day <= 5:
        start_exo = (day - 1) * 4 + 1
        end_exo = min(start_exo + 3, 20)
        base_time = max(130, 180 - day * 10)  # slowly gets faster

        for i in range(start_exo, end_exo + 1):
            if i > 20: break
            enonce, reponse = LINA_FRACTIONS_ENONCES.get(i, (f"Exo fractions #{i}", "?"))

            if day == 5:  # PIÈGE J5: tout HARD
                inject_score("TEST_LINA", "Lina", "6EME", "Fractions", i, enonce,
                           "HARD", random.randint(40, 80), 0, 1,
                           f"Mauvaise réponse #{i}", d)
            else:
                t = base_time + random.randint(-15, 25)
                inject_score("TEST_LINA", "Lina", "6EME", "Fractions", i, enonce,
                           "EASY", t, 0, 1, "", d)
    else:
        # Days 6-10: Proportionnalité
        start_exo = (day - 6) * 4 + 1
        end_exo = min(start_exo + 3, 20)
        base_time = max(60, 110 - (day - 5) * 12)  # accelerating

        for i in range(start_exo, end_exo + 1):
            if i > 20: break
            enonce, reponse = LINA_PROPORTIONNALITE_ENONCES.get(i, (f"Exo proportionnalité #{i}", "?"))
            fv = 1 if day <= 7 else 0  # starts dropping formula dependency
            t = base_time + random.randint(-10, 20)
            inject_score("TEST_LINA", "Lina", "6EME", "Proportionnalité", i, enonce,
                       "EASY", t, 0, fv, "", d)

    # Also inject boost scores for Lina
    if day >= 2:
        for b in range(1, 6):
            chap = "Fractions" if day <= 5 else "Proportionnalité"
            enonce = f"Boost J{day} exo {b} — {chap}"
            if day == 5:  # bad day
                inject_score("TEST_LINA", "Lina", "6EME", chap, 100+day*10+b, enonce,
                           "HARD", random.randint(30, 60), 0, 1, f"Erreur boost J5 #{b}", d, "BOOST")
            else:
                t = max(50, 150 - day * 15) + random.randint(-10, 20)
                inject_score("TEST_LINA", "Lina", "6EME", chap, 100+day*10+b, enonce,
                           "EASY", t, 0, 1 if day <= 7 else 0, "", d, "BOOST")

    # ── RAYAN: fast, 40% HARD, sign errors ──
    if day <= 5:
        start_exo = (day - 1) * 4 + 1
        end_exo = min(start_exo + 3, 20)

        rayan_sign_errors = {
            3: ("$(-3)^2$", "-9", "Confond $(-3)^2$ et $-(3^2)$"),
            5: ("$(-2)^3$", "8", "Oublie le signe négatif du cube"),
            10: ("$3^{-2}$", "$-9$", "Confond exposant négatif et signe"),
            12: ("$(-5)^2 - 5^2$", "-50", "Calcule $-(5^2) - 5^2$"),
            18: ("$(-4)^3$", "64", "Oublie le négatif"),
        }

        for i in range(start_exo, end_exo + 1):
            if i > 20: break
            enonce, reponse = RAYAN_PUISSANCES_ENONCES.get(i, (f"Exo puissances #{i}", "?"))
            t = random.randint(12, 28)

            if i in rayan_sign_errors:
                _, mauvaise, _ = rayan_sign_errors[i]
                inject_score("TEST_RAYAN", "Rayan", "4EME", "Puissances", i, enonce,
                           "HARD", t, 0, 0, mauvaise, d)
            elif random.random() < 0.4:
                inject_score("TEST_RAYAN", "Rayan", "4EME", "Puissances", i, enonce,
                           "HARD", t, 0, 0, f"Erreur calcul #{i}", d)
            else:
                inject_score("TEST_RAYAN", "Rayan", "4EME", "Puissances", i, enonce,
                           "EASY", t, 0, 0, "", d)
    else:
        start_exo = (day - 6) * 4 + 1
        end_exo = min(start_exo + 3, 20)

        rayan_calcul_errors = {
            3: ("$(2x-1)^2$", "$4x^2 + 4x + 1$", "Erreur signe double produit"),  # sign error!
            8: ("$-2(3x - 4)$", "$-6x - 8$", "Ne distribue pas le - sur le -4"),
            10: ("$(3x+1)^2$", "$9x^2 + 1$", "Oublie le double produit"),
            12: ("$(x-4)^2$", "$x^2 + 16$", "Oublie le double produit et se trompe de signe"),
            17: ("$(2x+3)(x-4)$", "$2x^2 - 5x + 12$", "Erreur signe dernier terme"),
        }

        for i in range(start_exo, end_exo + 1):
            if i > 20: break
            enonce, reponse = RAYAN_CALCUL_ENONCES.get(i, (f"Exo calcul littéral #{i}", "?"))
            t = random.randint(10, 25)

            # J8 PIÈGE: refait les mêmes erreurs de signe qu'au début
            if day == 8 and i in [3, 8]:
                _, mauvaise, _ = rayan_calcul_errors.get(i, ("", "erreur", ""))
                if mauvaise:
                    inject_score("TEST_RAYAN", "Rayan", "4EME", "Calcul_Littéral", i, enonce,
                               "HARD", t, 0, 0, mauvaise, d)
                    continue

            if i in rayan_calcul_errors and day != 9:  # J9: starts correcting
                _, mauvaise, _ = rayan_calcul_errors[i]
                inject_score("TEST_RAYAN", "Rayan", "4EME", "Calcul_Littéral", i, enonce,
                           "HARD", t, 0, 0, mauvaise, d)
            elif random.random() < 0.25:  # fewer errors on calcul littéral
                inject_score("TEST_RAYAN", "Rayan", "4EME", "Calcul_Littéral", i, enonce,
                           "HARD", t, 0, 0, f"Erreur calcul #{i}", d)
            else:
                inject_score("TEST_RAYAN", "Rayan", "4EME", "Calcul_Littéral", i, enonce,
                           "EASY", t, 0, 0, "", d)

    # Rayan boost — J3 special: 5/5 EASY
    if day >= 2:
        chap = "Puissances" if day <= 5 else "Calcul_Littéral"
        for b in range(1, 6):
            enonce = f"Boost J{day} exo {b} — {chap}"
            t = random.randint(10, 25)
            if day == 3:  # PIÈGE J3: 5/5 EASY
                inject_score("TEST_RAYAN", "Rayan", "4EME", chap, 100+day*10+b, enonce,
                           "EASY", t, 0, 0, "", d, "BOOST")
            elif day == 8:  # J8: sign errors again
                if b in [2, 4]:
                    inject_score("TEST_RAYAN", "Rayan", "4EME", chap, 100+day*10+b, enonce,
                               "HARD", t, 0, 0, "Erreur signe J8", d, "BOOST")
                else:
                    inject_score("TEST_RAYAN", "Rayan", "4EME", chap, 100+day*10+b, enonce,
                               "EASY", t, 0, 0, "", d, "BOOST")
            else:
                res = "HARD" if random.random() < 0.35 else "EASY"
                mo = f"Erreur signe boost J{day}" if res == "HARD" else ""
                inject_score("TEST_RAYAN", "Rayan", "4EME", chap, 100+day*10+b, enonce,
                           res, t, 0, 0, mo, d, "BOOST")

    # ── EMMA: strong, holes in graph reading & reciprocal Thalès ──
    if day <= 5:
        start_exo = (day - 1) * 4 + 1
        end_exo = min(start_exo + 3, 20)

        emma_hard_exos = {6, 9, 12, 16, 19}  # graph reading exos

        for i in range(start_exo, end_exo + 1):
            if i > 20: break
            enonce, reponse = EMMA_FONCTIONS_ENONCES.get(i, (f"Exo fonctions #{i}", "?"))
            t = random.randint(25, 60)

            if i in emma_hard_exos:
                inject_score("TEST_EMMA", "Emma", "3EME", "Fonctions", i, enonce,
                           "HARD", t, 0, 0, f"Mauvaise lecture graphique #{i}", d)
            else:
                inject_score("TEST_EMMA", "Emma", "3EME", "Fonctions", i, enonce,
                           "EASY", t, 0, 0, "", d)
    else:
        start_exo = (day - 6) * 4 + 1
        end_exo = min(start_exo + 3, 20)

        emma_thales_hard = {8, 11, 16, 19}  # reciprocal + special cases

        for i in range(start_exo, end_exo + 1):
            if i > 20: break
            enonce, reponse = EMMA_THALES_ENONCES.get(i, (f"Exo Thalès #{i}", "?"))
            t = random.randint(30, 70)

            if i in emma_thales_hard and day <= 8:
                inject_score("TEST_EMMA", "Emma", "3EME", "Thalès", i, enonce,
                           "HARD", t, 0, 0, f"Erreur réciproque/cas particulier #{i}", d)
            else:
                # Emma plugs holes after J8
                inject_score("TEST_EMMA", "Emma", "3EME", "Thalès", i, enonce,
                           "EASY", t, 0, 0, "", d)

    # Emma boost
    if day >= 2:
        chap = "Fonctions" if day <= 5 else "Thalès"
        for b in range(1, 6):
            enonce = f"Boost J{day} exo {b} — {chap}"
            t = random.randint(20, 50)
            if b in [2, 3] and day <= 7:  # graph/reciprocal holes
                inject_score("TEST_EMMA", "Emma", "3EME", chap, 100+day*10+b, enonce,
                           "HARD", t, 0, 0, f"Erreur ciblée boost J{day}", d, "BOOST")
            else:
                inject_score("TEST_EMMA", "Emma", "3EME", chap, 100+day*10+b, enonce,
                           "EASY", t, 0, 0, "", d, "BOOST")

    flush_scores()
    print(f"  📊 Scores J{day} injectés")


# ── ANALYSIS helper ──────────────────────────────────────────

def analyze_student(code, prenom, niveau):
    """Analyze a student's scores and return diagnostic info."""
    scores = sh.read("Scores")
    student_scores = [s for s in scores if s.get("Code") == code
                      and s.get("Source", "") != "CALIBRAGE"
                      and s.get("Chapitre", "") != "CALIBRAGE"]

    # Group by chapter
    chapters = {}
    for s in student_scores:
        ch = s.get("Chapitre", "")
        if ch not in chapters:
            chapters[ch] = []
        chapters[ch].append(s)

    analysis = {}
    for ch, ch_scores in chapters.items():
        total = len(ch_scores)
        easy = sum(1 for s in ch_scores if s.get("Résultat") == "EASY")
        hard = sum(1 for s in ch_scores if s.get("Résultat") == "HARD")
        fv = sum(1 for s in ch_scores if str(s.get("FormuleVue", "0")) == "1")
        indices = sum(1 for s in ch_scores if int(s.get("NbIndices", 0) or 0) >= 1)
        times = [int(s.get("Temps(sec)", 0) or 0) for s in ch_scores]
        avg_time = sum(times) / len(times) if times else 0

        hard_details = [(s.get("Énoncé", ""), s.get("MauvaiseOption", ""))
                       for s in ch_scores if s.get("Résultat") == "HARD"]

        # Seen exercises (anti-doublon)
        seen_enonces = [s.get("Énoncé", "") for s in ch_scores]

        analysis[ch] = {
            "total": total,
            "easy": easy,
            "hard": hard,
            "p8": round(easy / total * 100) if total > 0 else 0,
            "fv_rate": round(fv / total * 100) if total > 0 else 0,
            "indices_rate": round(indices / total * 100) if total > 0 else 0,
            "avg_time": round(avg_time),
            "hard_details": hard_details,
            "seen_enonces": seen_enonces,
        }

    return analysis


# ── MAIN ─────────────────────────────────────────────────────

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "run"

    if cmd == "cleanup":
        cleanup()
    elif cmd == "setup":
        cleanup()
        setup_users()
        setup_suivi()
    elif cmd == "inject":
        day = int(sys.argv[2])
        inject_day_scores(day)
    elif cmd == "analyze":
        code = sys.argv[2]
        prenom = sys.argv[3]
        niveau = sys.argv[4]
        analysis = analyze_student(code, prenom, niveau)
        for ch, data in analysis.items():
            print(f"\n=== {ch} ===")
            for k, v in data.items():
                if k == "hard_details":
                    print(f"  HARD errors:")
                    for e, m in v:
                        print(f"    - {e[:60]}... → {m}")
                elif k == "seen_enonces":
                    print(f"  Seen: {len(v)} enonces")
                else:
                    print(f"  {k}: {v}")
    elif cmd == "run":
        print("Usage: python3 stress_test.py [setup|inject N|analyze CODE PRENOM NIVEAU|cleanup]")
