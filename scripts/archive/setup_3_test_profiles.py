#!/usr/bin/env python3
"""
Crée 3 profils test variés pour tester l'admin cockpit.
Chaque profil : inscrit le 17 mars, diag fait, 1er boost fait, 1 chapitre complet, email J+0 envoyé.
"""

import json, hashlib, random, string
from datetime import datetime
from sheets import sh

TODAY = "2026-03-17"

def gen_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def hash_pwd(email, pwd):
    return hashlib.sha256(f"{email}::{pwd}::AB22".encode()).hexdigest()

PROFILES = [
    {
        "prenom": "Léa",
        "niveau": "6EME",
        "email": "lea.test@matheux.fr",
        "pwd": "leatest",
        "chapitres_choisis": ["Fractions", "Géométrie", "Nombres_entiers"],
        "chapitre_complet": "Fractions",  # 20 exos faits
        "boost_chap": "Fractions",
    },
    {
        "prenom": "Maxime",
        "niveau": "4EME",
        "email": "maxime.test@matheux.fr",
        "pwd": "maximetest",
        "chapitres_choisis": ["Équations", "Pythagore", "Puissances"],
        "chapitre_complet": "Équations",
        "boost_chap": "Équations",
    },
    {
        "prenom": "Sofia",
        "niveau": "3EME",
        "email": "sofia.test@matheux.fr",
        "pwd": "sofiatest",
        "chapitres_choisis": ["Trigonométrie", "Théorème_de_Thalès", "Fonctions"],
        "chapitre_complet": "Trigonométrie",
        "boost_chap": "Trigonométrie",
    },
]

def make_exo(q, a, opts, res, temps, indices=0, formula=False):
    return {
        "q": q, "a": a, "options": opts,
        "res": res, "temps": temps, "indices": indices, "formula": formula
    }

# Banques d'exos simples par chapitre
EXOS_BANK = {
    "Fractions": [
        ("Calcule $\\frac{1}{2} + \\frac{1}{3}$", "$\\frac{5}{6}$", ["$\\frac{5}{6}$", "$\\frac{2}{5}$", "$\\frac{1}{5}$"]),
        ("Simplifie $\\frac{6}{8}$", "$\\frac{3}{4}$", ["$\\frac{3}{4}$", "$\\frac{2}{3}$", "$\\frac{6}{4}$"]),
        ("Calcule $\\frac{2}{3} \\times \\frac{3}{4}$", "$\\frac{1}{2}$", ["$\\frac{1}{2}$", "$\\frac{6}{7}$", "$\\frac{2}{4}$"]),
        ("Calcule $\\frac{7}{4} - \\frac{1}{4}$", "$\\frac{3}{2}$", ["$\\frac{3}{2}$", "$\\frac{6}{4}$", "$\\frac{6}{8}$"]),
    ],
    "Équations": [
        ("Résous $2x + 3 = 7$", "$x = 2$", ["$x = 2$", "$x = 5$", "$x = -2$"]),
        ("Résous $3x - 1 = 8$", "$x = 3$", ["$x = 3$", "$x = 7$", "$x = 9$"]),
        ("Résous $5x = 20$", "$x = 4$", ["$x = 4$", "$x = 15$", "$x = 100$"]),
        ("Résous $x + 7 = 12$", "$x = 5$", ["$x = 5$", "$x = 19$", "$x = -5$"]),
    ],
    "Trigonométrie": [
        ("Dans un triangle rectangle, $\\sin(30°) = ?$", "$0{,}5$", ["$0{,}5$", "$\\frac{\\sqrt{3}}{2}$", "$\\frac{\\sqrt{2}}{2}$"]),
        ("$\\cos(60°) = ?$", "$0{,}5$", ["$0{,}5$", "$\\frac{\\sqrt{3}}{2}$", "$1$"]),
        ("$\\tan(45°) = ?$", "$1$", ["$1$", "$0$", "$\\sqrt{2}$"]),
        ("Si $\\cos(\\alpha) = 0{,}8$ et hyp = 10, adj = ?", "$8$", ["$8$", "$6$", "$10$"]),
    ],
}

def generate_scores(code, prenom, niveau, chapitre, n_exos, date):
    """Génère n_exos scores pour un chapitre."""
    rows = []
    bank = EXOS_BANK.get(chapitre, EXOS_BANK["Fractions"])
    results = ["EASY"] * int(n_exos * 0.6) + ["MEDIUM"] * int(n_exos * 0.25) + ["HARD"] * (n_exos - int(n_exos * 0.6) - int(n_exos * 0.25))
    random.shuffle(results)
    for i in range(n_exos):
        exo = bank[i % len(bank)]
        res = results[i]
        wrong = exo[2][1] if res == "HARD" else ""
        temps = random.randint(8, 45)
        indices = random.randint(0, 2) if res != "EASY" else 0
        formula = "1" if random.random() < 0.2 else "0"
        rows.append([
            code, prenom, niveau, chapitre, str(i + 1),
            exo[0][:60], res, str(temps), str(indices), formula,
            wrong, "", date, ""  # draft, date, source
        ])
    return rows

def generate_boost_scores(code, prenom, niveau, chapitre, date):
    """Génère 5 scores boost."""
    rows = []
    bank = EXOS_BANK.get(chapitre, EXOS_BANK["Fractions"])
    results = ["EASY", "EASY", "EASY", "MEDIUM", "HARD"]
    random.shuffle(results)
    for i in range(5):
        exo = bank[i % len(bank)]
        res = results[i]
        wrong = exo[2][1] if res == "HARD" else ""
        temps = random.randint(10, 40)
        indices = 1 if res == "HARD" else 0
        rows.append([
            code, prenom, niveau, chapitre, str(i + 1),
            exo[0][:60], res, str(temps), str(indices), "0",
            wrong, "", date, "BOOST"
        ])
    return rows

def main():
    print("🚀 Création de 3 profils test admin...\n")

    all_scores = []
    all_progress = []
    all_boosts = []
    all_emails = []

    for p in PROFILES:
        code = gen_code()
        p["code"] = code
        hashed = hash_pwd(p["email"], p["pwd"])

        # 1. Users
        # Cols: Code, Prénom, Niveau, Email, PasswordHash, DateInscription, IsAdmin, Premium, TrialStart, PremiumEnd, IsTest, PendingBrevet, RevisionChapters, Objectif
        user_row = [
            code, p["prenom"], p["niveau"], p["email"], hashed,
            TODAY, "0", "0", TODAY, "", "1",  # IsTest=1 (emails @matheux.fr)
            "", "", "lacunes"
        ]
        sh.append_row("Users", user_row)
        print(f"  ✅ User {p['prenom']} ({p['niveau']}) — code {code}")

        # 2. Scores — chapitre complet (20 exos)
        chap_scores = generate_scores(code, p["prenom"], p["niveau"], p["chapitre_complet"], 20, TODAY)
        all_scores.extend(chap_scores)

        # 3. Scores — diag (2 exos par chapitre choisi)
        for ch in p["chapitres_choisis"]:
            diag_scores = generate_scores(code, p["prenom"], p["niveau"], ch, 2, TODAY)
            for row in diag_scores:
                row[13] = "CALIBRAGE"  # source
            all_scores.extend(diag_scores)

        # 4. Scores — boost (5 exos)
        boost_scores = generate_boost_scores(code, p["prenom"], p["niveau"], p["boost_chap"], TODAY)
        all_scores.extend(boost_scores)

        # 5. Progress — chapitre complet
        chap_easy = len([s for s in chap_scores if s[6] == "EASY"])
        chap_rate = round(chap_easy * 100 / 20)
        all_progress.append([
            code, p["niveau"], p["chapitre_complet"],
            str(chap_rate), "20", str(20 - chap_easy), TODAY, "maitrise", "3"
        ])
        # Progress — chapitres diagnostiqués (juste 2 exos)
        for ch in p["chapitres_choisis"]:
            if ch == p["chapitre_complet"]:
                continue
            all_progress.append([
                code, p["niveau"], ch,
                "50", "2", "1", TODAY, "en_cours", "0"
            ])

        # 6. DailyBoosts — boost terminé (5/5)
        boost_json = {
            "insight": f"Super travail {p['prenom']} ! Continue comme ça 💪",
            "exos": [
                {"q": e[0], "a": e[1], "options": e[2],
                 "steps": ["Étape 1", "Étape 2"], "f": "Formule clé", "lvl": 1}
                for e in (EXOS_BANK.get(p["boost_chap"], EXOS_BANK["Fractions"])[:5])
            ]
        }
        # Pad to 5 exos if bank is short
        while len(boost_json["exos"]) < 5:
            boost_json["exos"].append(boost_json["exos"][0])
        all_boosts.append([code, TODAY, json.dumps(boost_json, ensure_ascii=False), "5"])

        # 7. Email J+0 envoyé
        all_emails.append([
            TODAY, p["email"], p["prenom"], "J+0", "envoyé"
        ])

        print(f"  ✅ {p['chapitre_complet']} terminé (20 exos), boost 5/5, diag fait, J+0 envoyé")

    # Écriture batch — utiliser update_range pour éviter rate limits
    print("\n📝 Écriture batch dans les onglets...")

    # Scores — read current row count, then batch append
    scores_raw = sh.read_raw("Scores")
    start_row = len(scores_raw) + 1
    if all_scores:
        end_col = chr(64 + len(all_scores[0]))
        sh.update_range("Scores", f"A{start_row}:{end_col}{start_row + len(all_scores) - 1}", all_scores)
    print(f"  ✅ Scores : {len(all_scores)} lignes ajoutées")

    # Progress
    prog_raw = sh.read_raw("Progress")
    start_row = len(prog_raw) + 1
    if all_progress:
        end_col = chr(64 + len(all_progress[0]))
        sh.update_range("Progress", f"A{start_row}:{end_col}{start_row + len(all_progress) - 1}", all_progress)
    print(f"  ✅ Progress : {len(all_progress)} lignes ajoutées")

    # DailyBoosts
    boost_raw = sh.read_raw("DailyBoosts")
    start_row = len(boost_raw) + 1
    if all_boosts:
        end_col = chr(64 + len(all_boosts[0]))
        sh.update_range("DailyBoosts", f"A{start_row}:{end_col}{start_row + len(all_boosts) - 1}", all_boosts)
    print(f"  ✅ DailyBoosts : {len(all_boosts)} lignes ajoutées")

    # Emails
    email_raw = sh.read_raw("📧 Emails")
    start_row = len(email_raw) + 1
    if all_emails:
        end_col = chr(64 + len(all_emails[0]))
        sh.update_range("📧 Emails", f"A{start_row}:{end_col}{start_row + len(all_emails) - 1}", all_emails)
    print(f"  ✅ Emails : {len(all_emails)} lignes ajoutées")

    # Appeler rebuildSuivi via API pour chaque profil
    print("\n🔄 Rebuild Suivi via GAS...")
    import requests
    GAS_URL = "https://script.google.com/macros/s/AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF/exec"

    for p in PROFILES:
        # Trigger rebuildSuivi via save_score (un score factice qui rebuild)
        # Actually, the simplest way is to call save_score which triggers rebuildSuivi
        # But we already wrote scores. Let's just trigger login to rebuild.
        r = requests.post(GAS_URL, json={
            "action": "login",
            "email": p["email"],
            "password": hash_pwd(p["email"], p["pwd"])
        })
        d = r.json()
        if d.get("status") == "success":
            print(f"  ✅ {p['prenom']} login OK — Suivi rebuilt")
        else:
            print(f"  ⚠️ {p['prenom']} login: {d.get('message', 'erreur')}")

    print("\n🎉 3 profils créés !")
    print("\nRécap :")
    for p in PROFILES:
        print(f"  {p['prenom']} ({p['niveau']}) — {p['code']} — {p['email']} / {p['pwd']}")
        print(f"    Chapitre complet : {p['chapitre_complet']}")
        print(f"    Boost terminé : {p['boost_chap']} (5/5)")
        print(f"    Diag : {', '.join(p['chapitres_choisis'])}")
    print("\n⚠️ IsTest=1 (emails @matheux.fr) — apparaîtront dans l'onglet À FAIRE quand même")
    print("  Pour les voir dans À FAIRE : vérifier que _computeActions détecte bien boost terminé + chapitre terminé")

if __name__ == "__main__":
    main()
