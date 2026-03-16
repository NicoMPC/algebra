#!/usr/bin/env python3
"""
sim_7days.py — Simulation complète 7 jours, 5 élèves réalistes.

5 profils :
  1. Emma Petit    (6EME) — Perfectionniste   : 7j sans faille, chapitre terminé J+5
  2. Lucas Martin  (5EME) — Procrastinateur   : commence J+0, absent J+2-J+3, chapitre commencé J+4 pas fini
  3. Inès Dupont   (3EME) — Bloquée           : 2j HARD, inactive → BLOQUÉ + email J+7
  4. Théo Bernard  (4EME) — Régulier          : 7j, chapitre terminé J+4, nouveau chapitre J+5
  5. Chloé Rousseau(5EME) — Arrivée tardive   : inscription J+0 sans diag, diag J+3, premier boost J+4

Log : chaque action GAS, chaque retour JSON, chaque action admin simulée.
À la fin : rapport complet par élève + liste des anomalies détectées.
"""

import json, hashlib, time, random, urllib.request, urllib.error, sys
from datetime import datetime

GAS_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF/exec"
)
ADMIN_EMAIL = "admin@matheux.fr"
ADMIN_HASH  = "dba3013d8ee56602f8da554bd6f5ff0108324c6d220f137d2181d9d24fa0ef62"

# ─────────────────────────────────────────────────────────
# Anomalies détectées — alimenté pendant la simulation
# ─────────────────────────────────────────────────────────
ANOMALIES = []

def flag(severity, context, msg, data=None):
    entry = {"severity": severity, "context": context, "msg": msg}
    if data:
        entry["data"] = data
    ANOMALIES.append(entry)
    icon = "🔴" if severity == "ERROR" else "🟡" if severity == "WARN" else "🔵"
    print(f"    {icon} [{severity}] {context} : {msg}")

# ─────────────────────────────────────────────────────────
# Helpers réseau
# ─────────────────────────────────────────────────────────

def sha256_hash(email, password):
    raw = f"{email.lower().strip()}::{password}::AB22"
    return hashlib.sha256(raw.encode()).hexdigest()

def gas(payload, label="", retry=2, verbose=True):
    body = json.dumps(payload).encode("utf-8")
    req  = urllib.request.Request(
        GAS_URL, data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    for attempt in range(retry + 1):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                d = json.loads(r.read().decode("utf-8"))
                status = d.get("status", "?")
                ok = "✅" if status == "success" else "⚠️" if status == "waitlist" else "❌"
                if verbose:
                    msg = d.get("message", "")
                    print(f"      {ok} {label or payload.get('action','?')} → {status}"
                          + (f" ({msg[:60]})" if msg and status != "success" else ""))
                return d
        except Exception as e:
            if attempt < retry:
                time.sleep(2)
            else:
                print(f"      ❌ {label} → RÉSEAU : {e}")
                flag("ERROR", label, f"Erreur réseau : {e}")
                return {}
    return {}

def sleep(s=0.6):
    time.sleep(s)

# ─────────────────────────────────────────────────────────
# Helpers JSON simulés (boost publié par Nicolas)
# ─────────────────────────────────────────────────────────

SIMULATED_BOOST_JSONS = {
    "Fractions": {
        "insight": "Tu confonds encore numérateur et dénominateur — concentration sur les additions de fractions.",
        "motProf": "T'es sur la bonne voie, continue !",
        "exos": [
            {"q": "$\\frac{1}{2} + \\frac{1}{4} = ?$", "a": "$\\frac{3}{4}$",
             "options": ["$\\frac{3}{4}$","$\\frac{1}{4}$","$\\frac{2}{6}$","$\\frac{3}{6}$"],
             "steps": ["Cherche le dénominateur commun","Additionne les numérateurs"],
             "f": "Dénominateur commun = PPCM", "lvl": 1, "oC": "Fractions"},
            {"q": "$\\frac{3}{4} - \\frac{1}{8} = ?$", "a": "$\\frac{5}{8}$",
             "options": ["$\\frac{5}{8}$","$\\frac{2}{4}$","$\\frac{1}{2}$","$\\frac{4}{8}$"],
             "steps": ["Réduis $\\frac{3}{4}$ au dénominateur 8","Soustrait"],
             "f": "$\\frac{3}{4} = \\frac{6}{8}$", "lvl": 1, "oC": "Fractions"},
            {"q": "$\\frac{2}{3} \\times \\frac{3}{4} = ?$", "a": "$\\frac{1}{2}$",
             "options": ["$\\frac{1}{2}$","$\\frac{6}{12}$","$\\frac{2}{4}$","$\\frac{5}{7}$"],
             "steps": ["Multiplie numérateurs entre eux","Multiplie dénominateurs","Simplifie"],
             "f": "$\\frac{a}{b} \\times \\frac{c}{d} = \\frac{a \\cdot c}{b \\cdot d}$", "lvl": 2, "oC": "Fractions"},
            {"q": "Simplifie $\\frac{12}{18}$", "a": "$\\frac{2}{3}$",
             "options": ["$\\frac{2}{3}$","$\\frac{6}{9}$","$\\frac{4}{6}$","$\\frac{1}{2}$"],
             "steps": ["PGCD(12,18)=6","Divise les deux par 6"],
             "f": "PGCD", "lvl": 1, "oC": "Fractions"},
            {"q": "$\\frac{5}{6} \\div \\frac{2}{3} = ?$", "a": "$\\frac{5}{4}$",
             "options": ["$\\frac{5}{4}$","$\\frac{10}{18}$","$\\frac{3}{2}$","$\\frac{5}{9}$"],
             "steps": ["Division = multiplication par l'inverse","$\\frac{5}{6} \\times \\frac{3}{2}$"],
             "f": "$a \\div \\frac{b}{c} = a \\times \\frac{c}{b}$", "lvl": 2, "oC": "Fractions"}
        ]
    },
    "Équations": {
        "insight": "Tu perds des points sur les équations du 2nd degré — reviens sur la méthode.",
        "motProf": "Relis la méthode avant de commencer, tu vas y arriver.",
        "exos": [
            {"q": "Résous : $2x + 5 = 13$", "a": "$x = 4$",
             "options": ["$x = 4$","$x = 9$","$x = 3$","$x = 6$"],
             "steps": ["$2x = 13 - 5$","$2x = 8$","$x = 4$"],
             "f": "Isoler x : opérations inverses", "lvl": 1, "oC": "Équations"},
            {"q": "Résous : $3x - 7 = 2x + 1$", "a": "$x = 8$",
             "options": ["$x = 8$","$x = -8$","$x = 6$","$x = 2$"],
             "steps": ["$3x - 2x = 1 + 7$","$x = 8$"],
             "f": "Regrouper les x d'un côté", "lvl": 1, "oC": "Équations"},
            {"q": "Résous : $x^2 = 9$", "a": "$x = \\pm 3$",
             "options": ["$x = \\pm 3$","$x = 3$","$x = 9$","$x = \\pm 9$"],
             "steps": ["$\\sqrt{x^2} = \\sqrt{9}$","$|x| = 3$","$x = 3$ ou $x = -3$"],
             "f": "$x^2 = a \\Rightarrow x = \\pm\\sqrt{a}$", "lvl": 2, "oC": "Équations"},
            {"q": "Résous : $\\frac{x}{3} + 2 = 5$", "a": "$x = 9$",
             "options": ["$x = 9$","$x = 3$","$x = 7$","$x = 21$"],
             "steps": ["$\\frac{x}{3} = 3$","$x = 9$"],
             "f": "Multiplier des deux côtés par 3", "lvl": 1, "oC": "Équations"},
            {"q": "Résous : $(x+2)(x-3) = 0$", "a": "$x = -2$ ou $x = 3$",
             "options": ["$x = -2$ ou $x = 3$","$x = 2$ ou $x = -3$","$x = 1$","$x = 0$"],
             "steps": ["Produit nul : l'un des facteurs est 0","$x+2=0 \\Rightarrow x=-2$","$x-3=0 \\Rightarrow x=3$"],
             "f": "Règle du produit nul", "lvl": 2, "oC": "Équations"}
        ]
    },
    "Nombres_relatifs": {
        "insight": "Difficultés sur les règles des signes — priorité aux soustractions avec négatifs.",
        "motProf": "Les nombres relatifs c'est souvent la source d'erreurs — à toi de jouer !",
        "exos": [
            {"q": "$(-3) + (-5) = ?$", "a": "$-8$",
             "options": ["$-8$","$8$","$-2$","$2$"],
             "steps": ["Même signe → addition et on garde le signe"],
             "f": "$(-a) + (-b) = -(a+b)$", "lvl": 1, "oC": "Nombres_relatifs"},
            {"q": "$(-6) - (+2) = ?$", "a": "$-8$",
             "options": ["$-8$","$-4$","$4$","$8$"],
             "steps": ["Soustraire un positif = additionner un négatif","$-6 + (-2) = -8$"],
             "f": "$a - b = a + (-b)$", "lvl": 1, "oC": "Nombres_relatifs"},
            {"q": "$(-4) \\times (-3) = ?$", "a": "$12$",
             "options": ["$12$","$-12$","$7$","$-7$"],
             "steps": ["Négatif × négatif = positif"],
             "f": "$(-)(-)= (+)$", "lvl": 1, "oC": "Nombres_relatifs"},
            {"q": "$|{-7}| = ?$", "a": "$7$",
             "options": ["$7$","$-7$","$0$","$49$"],
             "steps": ["Valeur absolue = distance à 0, toujours positive"],
             "f": "$|x| = x$ si $x \\geq 0$, $|x| = -x$ si $x < 0$", "lvl": 1, "oC": "Nombres_relatifs"},
            {"q": "$\\frac{-12}{-4} = ?$", "a": "$3$",
             "options": ["$3$","$-3$","$8$","$-8$"],
             "steps": ["Négatif ÷ négatif = positif"],
             "f": "$\\frac{-a}{-b} = \\frac{a}{b}$", "lvl": 2, "oC": "Nombres_relatifs"}
        ]
    },
    "Calcul_Littéral": {
        "insight": "Développement et factorisation : tu mélanges les deux — focus sur la méthode.",
        "motProf": "Bien joué, continue à pratiquer !",
        "exos": [
            {"q": "Développe : $3(x + 2)$", "a": "$3x + 6$",
             "options": ["$3x + 6$","$3x + 2$","$x + 6$","$3x + 5$"],
             "steps": ["Distribue le 3 : $3 \\times x + 3 \\times 2$"],
             "f": "$a(b+c) = ab + ac$", "lvl": 1, "oC": "Calcul_Littéral"},
            {"q": "Développe : $(x+3)^2$", "a": "$x^2 + 6x + 9$",
             "options": ["$x^2 + 6x + 9$","$x^2 + 9$","$x^2 + 3x + 9$","$2x + 6$"],
             "steps": ["$(a+b)^2 = a^2 + 2ab + b^2$","$x^2 + 2 \\cdot x \\cdot 3 + 9$"],
             "f": "$(a+b)^2 = a^2 + 2ab + b^2$", "lvl": 2, "oC": "Calcul_Littéral"},
            {"q": "Factorise : $4x + 8$", "a": "$4(x + 2)$",
             "options": ["$4(x + 2)$","$4(x + 4)$","$2(2x + 8)$","$4x(1 + 2)$"],
             "steps": ["Facteur commun = 4","$4 \\times x + 4 \\times 2$"],
             "f": "Chercher le PGCD des termes", "lvl": 1, "oC": "Calcul_Littéral"},
            {"q": "Simplifie : $2x + 3x - x$", "a": "$4x$",
             "options": ["$4x$","$5x$","$6x$","$x$"],
             "steps": ["$2 + 3 - 1 = 4$","Regrouper les termes en $x$"],
             "f": "$ax + bx = (a+b)x$", "lvl": 1, "oC": "Calcul_Littéral"},
            {"q": "Développe : $(2x - 1)(x + 3)$", "a": "$2x^2 + 5x - 3$",
             "options": ["$2x^2 + 5x - 3$","$2x^2 + 6x - 3$","$2x^2 - 3$","$3x - 3$"],
             "steps": ["$2x \\cdot x + 2x \\cdot 3 + (-1) \\cdot x + (-1) \\cdot 3$","$2x^2 + 6x - x - 3$"],
             "f": "$(a+b)(c+d) = ac + ad + bc + bd$", "lvl": 2, "oC": "Calcul_Littéral"}
        ]
    },
    "Probabilités": {
        "insight": "Attention aux probabilités conditionnelles — relis la définition.",
        "motProf": "Tu progresses bien sur les probabilités !",
        "exos": [
            {"q": "P(A) = 0.4, P(B) = 0.3 — si A et B indépendants : P(A∩B) = ?", "a": "0.12",
             "options": ["0.12","0.7","0.1","0.04"],
             "steps": ["Indépendants → P(A∩B) = P(A) × P(B)","0.4 × 0.3 = 0.12"],
             "f": "P(A∩B) = P(A)×P(B) si indépendants", "lvl": 2, "oC": "Probabilités"},
            {"q": "Un dé est lancé. P(nombre pair) = ?", "a": "1/2",
             "options": ["1/2","1/3","1/6","2/3"],
             "steps": ["Faces paires : {2,4,6}","P = 3/6 = 1/2"],
             "f": "P(A) = nbr de cas favorables / nbr de cas possibles", "lvl": 1, "oC": "Probabilités"},
            {"q": "P(A) = 0.6 — P(Ā) = ?", "a": "0.4",
             "options": ["0.4","0.6","0.36","1.6"],
             "steps": ["P(Ā) = 1 - P(A)","= 1 - 0.6 = 0.4"],
             "f": "P(Ā) = 1 - P(A)", "lvl": 1, "oC": "Probabilités"},
            {"q": "Sac : 3 rouges + 7 bleues. P(rouge) = ?", "a": "3/10",
             "options": ["3/10","7/10","3/7","1/3"],
             "steps": ["Total = 10","P(rouge) = 3/10"],
             "f": "Équiprobabilité", "lvl": 1, "oC": "Probabilités"},
            {"q": "A et B : P(A∪B) = P(A)+P(B) si ?", "a": "A et B incompatibles",
             "options": ["A et B incompatibles","A et B indépendants","Toujours","A⊂B"],
             "steps": ["Incompatibles = A∩B = ∅","Alors P(A∪B) = P(A) + P(B)"],
             "f": "P(A∪B) = P(A)+P(B)-P(A∩B)", "lvl": 2, "oC": "Probabilités"}
        ]
    }
}

def make_boost(categorie):
    """Retourne un boost JSON simulé pour une catégorie."""
    base = SIMULATED_BOOST_JSONS.get(categorie, SIMULATED_BOOST_JSONS["Fractions"])
    return dict(base, categorie=categorie)

def make_chapter_exos(categorie, count=20):
    """Génère des exos de chapitre simulés."""
    base = SIMULATED_BOOST_JSONS.get(categorie, SIMULATED_BOOST_JSONS["Fractions"])
    exos = base["exos"] * 4  # repeat to get 20
    return exos[:count]

# ─────────────────────────────────────────────────────────
# Classe Student
# ─────────────────────────────────────────────────────────

class Student:
    def __init__(self, prenom, email, password, level, desc):
        self.prenom   = prenom
        self.email    = email
        self.password = password
        self.hash     = sha256_hash(email, password)
        self.level    = level
        self.desc     = desc
        self.code     = None
        self.errors   = []   # catégories faibles au diag
        self.boosts_done = 0
        self.chapter_exos = {}  # {cat: count}
        self.log = []

    def note(self, msg):
        self.log.append(msg)
        print(f"    ℹ️  {msg}")

    def register(self):
        r = gas({
            "action": "register",
            "name": self.prenom,
            "email": self.email,
            "level": self.level,
            "password": self.hash,
            "consent": True
        }, f"register {self.prenom}")

        status = r.get("status", "")
        if status == "waitlist":
            flag("ERROR", f"register {self.prenom}", "Quota bêta atteint — en liste d'attente !")
            return False
        if status not in ("success",) and "existe" not in r.get("message",""):
            flag("ERROR", f"register {self.prenom}", f"Échec inscription : {r.get('message','?')}")
            return False

        self.code = r.get("profile", {}).get("code", "")
        # Vérifier les champs retournés
        profile = r.get("profile", {})
        for f_ in ["code", "name", "level", "isAdmin"]:
            if f_ not in profile:
                flag("WARN", f"register {self.prenom}", f"Champ manquant dans profile.register : {f_}")
        if profile.get("isAdmin"):
            flag("WARN", f"register {self.prenom}", "isAdmin=true sur un compte élève !")
        self.note(f"Inscrit → code={self.code}")
        return True

    def login(self, check_trial=True, check_boost=None):
        r = gas({
            "action": "login",
            "email": self.email,
            "password": self.hash
        }, f"login {self.prenom}")

        if r.get("status") != "success":
            flag("ERROR", f"login {self.prenom}", f"Login échoué : {r.get('message','?')}")
            return None

        profile = r.get("profile", {})
        if not profile.get("code"):
            flag("ERROR", f"login {self.prenom}", "profile.code absent au login")

        # Vérifier trial
        trial = r.get("trial", {})
        if check_trial:
            if not trial.get("trialActive"):
                flag("WARN", f"login {self.prenom}", f"Trial inactif à J0 ? isPremium={trial.get('isPremium')}, daysLeft={trial.get('daysLeft')}")
            days_left = trial.get("daysLeft", -1)
            if days_left < 0:
                flag("WARN", f"login {self.prenom}", f"daysLeft négatif : {days_left}")

        # Vérifier curriculum
        curriculum = r.get("curriculumOfficiel", [])
        if not curriculum:
            flag("WARN", f"login {self.prenom}", "curriculumOfficiel vide au login")

        # Vérifier dailyBoost
        daily_boost = r.get("dailyBoost")
        boost_done  = r.get("boostExosDone", 0)
        next_boost  = r.get("nextBoost")

        if check_boost == "expected" and not daily_boost and not next_boost:
            flag("WARN", f"login {self.prenom}", "Boost attendu au login mais absent (dailyBoost=null, nextBoost=null)")
        if check_boost == "not_expected" and (daily_boost or next_boost):
            flag("INFO", f"login {self.prenom}", "Boost présent au login (attendu absent?)")

        return r

    def do_diagnostic(self, hard_rate=0.3):
        """Génère et simule le diagnostic. Retourne catégories faibles."""
        sleep()
        r = gas({"action": "generate_diagnostic", "level": self.level}, f"generate_diag {self.prenom}")
        if r.get("status") != "success":
            flag("ERROR", f"diag {self.prenom}", f"Génération diag échouée : {r.get('message','?')}")
            return []

        exos = r.get("exos", [])
        if not exos:
            flag("ERROR", f"diag {self.prenom}", "Diagnostic retourne 0 exos")
            return []

        # Vérifier structure des exos
        for i, exo in enumerate(exos[:3]):
            for field in ["q", "a", "options", "categorie"]:
                if field not in exo:
                    flag("WARN", f"diag exo {i}", f"Champ manquant : {field}")
            opts = exo.get("options", [])
            if len(opts) < 2:
                flag("WARN", f"diag exo {i}", f"Moins de 2 options : {opts}")
            if exo.get("a") not in opts:
                flag("WARN", f"diag exo {i} ({exo.get('categorie','')})",
                     f"Bonne réponse '{exo.get('a','')}' absente des options {opts}")

        errors = []
        for i, exo in enumerate(exos):
            cat = exo.get("categorie", exo.get("oC", ""))
            if not cat:
                flag("WARN", f"diag exo {i}", "Pas de categorie dans exo diagnostic")
                continue
            resultat = "HARD" if random.random() < hard_rate else "EASY"
            if resultat == "HARD" and cat not in errors:
                errors.append(cat)
            sleep(0.3)
            r2 = gas({
                "action":       "save_score",
                "code":         self.code,
                "name":         self.prenom,
                "level":        self.level,
                "categorie":    cat,
                "exercice_idx": i + 1,
                "q":            exo.get("q", "")[:80],
                "resultat":     resultat,
                "time":         random.randint(10, 60),
                "indices":      random.randint(0, 1) if resultat == "HARD" else 0,
                "formule":      resultat == "HARD",
                "source":       "CALIBRAGE"
            }, f"  diag_score {cat[:20]} ({resultat})", verbose=False)
            if r2.get("status") != "success":
                flag("WARN", f"save_score CALIBRAGE", f"save_score échoué pour {self.prenom}")

        self.errors = errors[:3]
        self.note(f"Diagnostic : {len(exos)} exos, {len(errors)} chapitres faibles : {errors[:3]}")
        return errors

    def do_boost_exos(self, boost_json, nb_exos=5, hard_rate=0.2):
        """Simule les exercices du boost (save_score source=BOOST seulement)."""
        exos = boost_json.get("exos", [])
        done = min(nb_exos, len(exos))
        for i in range(done):
            exo = exos[i]
            cat = exo.get("oC", boost_json.get("categorie", "BOOST"))
            resultat = "HARD" if random.random() < hard_rate else "EASY"
            sleep(0.3)
            r = gas({
                "action":       "save_score",
                "code":         self.code,
                "name":         self.prenom,
                "level":        self.level,
                "categorie":    cat,
                "exercice_idx": i + 1,
                "q":            exo.get("q", "")[:80],
                "resultat":     resultat,
                "time":         random.randint(15, 90),
                "indices":      random.randint(0, 2) if resultat == "HARD" else 0,
                "formule":      resultat == "HARD",
                "source":       "BOOST"
            }, f"  boost_score Q{i+1} ({resultat})", verbose=False)
            # Aussi save_boost pour mettre à jour ExosDone dans DailyBoosts
            r2 = gas({
                "action": "save_boost",
                "code":   self.code,
                "boost":  boost_json,
                "exoIdx": i
            }, f"  save_boost Q{i+1}", verbose=False)

        self.boosts_done += 1
        self.note(f"Boost : {done}/{len(exos)} exos faits (hard_rate={hard_rate})")
        return done

    def do_chapter_exos(self, categorie, count, hard_rate=0.25, start_idx=0):
        """Simule des exercices de chapitre."""
        n = self.chapter_exos.get(categorie, 0)
        for i in range(count):
            resultat = "HARD" if random.random() < hard_rate else "EASY"
            sleep(0.25)
            r = gas({
                "action":       "save_score",
                "code":         self.code,
                "name":         self.prenom,
                "level":        self.level,
                "categorie":    categorie,
                "exercice_idx": start_idx + n + i + 1,
                "q":            f"Exercice {n+i+1} — {categorie[:25]}",
                "resultat":     resultat,
                "time":         random.randint(20, 90),
                "indices":      random.randint(0, 2) if resultat == "HARD" else 0,
                "formule":      False,
                "source":       "chapter"
            }, f"  ch_exo {n+i+1}/{n+count} {categorie[:20]} ({resultat})", verbose=False)
            if r.get("status") != "success":
                flag("WARN", f"chapter {categorie}", f"save_score chapitre échoué à l'exo {n+i+1}")
        self.chapter_exos[categorie] = n + count
        total = self.chapter_exos[categorie]
        self.note(f"Chapitre {categorie} : {total} exos total ({count} ce jour)")

    def check_trial_status(self):
        r = gas({"action": "check_trial_status", "code": self.code},
                f"check_trial {self.prenom}")
        if r.get("status") != "success":
            flag("WARN", f"trial {self.prenom}", "check_trial_status échoué")
            return {}
        if not r.get("trialActive"):
            flag("INFO", f"trial {self.prenom}", f"Trial expiré : daysLeft={r.get('daysLeft')}")
        return r

    def get_progress(self):
        r = gas({"action": "get_progress", "code": self.code},
                f"progress {self.prenom}", verbose=False)
        if r.get("status") != "success":
            flag("WARN", f"progress {self.prenom}", "get_progress échoué")
        return r

    def simulate_next_day(self):
        r = gas({"action": "simulate_next_day", "code": self.code},
                f"next_day {self.prenom}", verbose=False)
        if r.get("status") != "success":
            flag("WARN", f"simulate_next_day {self.prenom}", r.get("message","?"))

# ─────────────────────────────────────────────────────────
# Admin helper
# ─────────────────────────────────────────────────────────

class Admin:
    def __init__(self):
        self.code = None

    def login(self):
        r = gas({"action": "login", "email": ADMIN_EMAIL, "password": ADMIN_HASH},
                "login admin")
        if r.get("status") != "success":
            flag("ERROR", "admin_login", "Login admin échoué !")
            sys.exit(1)
        self.code = r.get("profile", {}).get("code", "")
        print(f"    → Admin code : {self.code}")
        return self.code

    def overview(self, context=""):
        r = gas({"action": "get_admin_overview", "adminCode": self.code},
                f"admin_overview {context}")
        if r.get("status") != "success":
            flag("ERROR", "admin_overview", f"Échec : {r.get('message','?')}")
            return {}

        students = r.get("students", [])
        real_count = r.get("realCount", 0)

        # Vérifier structure
        for st in students:
            for field in ["code", "prenom", "niveau", "actionPriority", "chapitresDetail", "boostHistory"]:
                if field not in st:
                    flag("WARN", "admin_overview", f"Champ manquant dans student : {field}")
                    break

        return r

    def find_student(self, overview, code):
        return next((s for s in overview.get("students", []) if s.get("code") == code), None)

    def publish_boost(self, target_code, boost_json):
        exos = boost_json.get("exos", [])
        r = gas({
            "action":     "publish_admin_boost",
            "adminCode":  self.code,
            "targetCode": target_code,
            "exos":       exos,
            "insight":    boost_json.get("insight", ""),
            "motProf":    boost_json.get("motProf", "")
        }, f"publish_boost → {target_code}")

        if r.get("status") != "success":
            flag("ERROR", f"publish_boost {target_code}", f"Échec : {r.get('message','?')}")
            return False
        return True

    def publish_chapter(self, target_code, categorie, exos, insight="", mot_prof=""):
        r = gas({
            "action":     "publish_admin_chapter",
            "adminCode":  self.code,
            "targetCode": target_code,
            "categorie":  categorie,
            "exos":       exos,
            "insight":    insight or f"Nouveau chapitre : {categorie}",
            "motProf":    mot_prof or "Nouveau chapitre — vas-y !"
        }, f"publish_chapter {categorie} → {target_code}")

        if r.get("status") != "success":
            flag("ERROR", f"publish_chapter {target_code}", f"Échec : {r.get('message','?')}")
            return False
        return True

    def check_action(self, overview, code, expected_action, context=""):
        st = self.find_student(overview, code)
        if not st:
            flag("WARN", context, f"Élève {code} introuvable dans overview")
            return
        ap = st.get("actionPriority", "")
        if expected_action not in ap:
            flag("WARN", context, f"Action attendue '{expected_action}' mais obtenu '{ap[:60]}'")
        else:
            print(f"    ✅ Admin OK : action = '{ap[:60]}'")

    def check_email_indicators(self, overview, code, context=""):
        """Vérifie les indicateurs email J0/J3/J5/J7 dans l'overview."""
        st = self.find_student(overview, code)
        if not st:
            return
        # Les indicateurs email sont dans category, emailsDue, j0Sent, etc.
        j0 = st.get("j0Sent")
        email_due = st.get("emailsDue", [])
        cat = st.get("category", "")
        print(f"    📧 Email admin ({context}) : j0={j0}, emailsDue={email_due}, category={cat}")
        if j0 is None:
            flag("WARN", f"email {code}", "j0Sent absent dans student overview")


# ══════════════════════════════════════════════════════════
# SCÉNARIOS 7 JOURS
# ══════════════════════════════════════════════════════════

def scenario_emma(admin):
    """
    Emma Petit (6EME) — La perfectionniste
    J0 : inscription + diagnostic (peu d'erreurs) + admin publie boost J0
    J1-J4 : boost quotidien 5/5 + quelques exos chapitre
    J5 : chapitre terminé (20 exos), admin publie nouveau chapitre
    J6-J7 : nouveau chapitre entamé
    """
    print(f"\n{'═'*60}")
    print("👩‍🎓  EMMA PETIT (6EME) — La perfectionniste")
    print(f"{'═'*60}")

    random.seed(1)
    s = Student("Emma", "emma.petit.test@gmail.com", "Emma2026!", "6EME",
                "La perfectionniste — 7j sans faille")

    # ── J0 ────────────────────────────────────────────────
    print("\n  📅 J+0 — Inscription + diagnostic")
    if not s.register(): return None
    sleep()

    r_login0 = s.login(check_trial=True, check_boost="not_expected")
    if not r_login0: return None

    # Diagnostic (peu d'erreurs, 10%)
    errors = s.do_diagnostic(hard_rate=0.10)
    sleep()

    # Admin voit Emma
    ov = admin.overview("J0 après diag Emma")
    emma_st = admin.find_student(ov, s.code)
    if not emma_st:
        flag("ERROR", "admin J0", f"Emma ({s.code}) introuvable dans overview !")
    else:
        print(f"    👁️  Admin voit Emma : action={emma_st.get('actionPriority','?')[:60]}")
        admin.check_email_indicators(ov, s.code, "J0")
        # Vérifier j0Sent (email bienvenue doit avoir été envoyé)
        if not emma_st.get("j0Sent"):
            flag("WARN", "email Emma J0", "j0Sent=false — email de bienvenue non envoyé ?")

    # Admin publie boost J0
    cat_boost = errors[0] if errors else "Fractions"
    boost_j0 = make_boost(cat_boost)
    print(f"\n    🤖 Nicolas simule : copie prompt Claude → génère JSON 5 exos")
    print(f"    JSON simulé : boost {cat_boost} — insight: '{boost_j0['insight'][:50]}...'")
    admin.publish_boost(s.code, boost_j0)

    # Emma se reconnecte et voit le boost
    r_after = s.login(check_boost="expected")
    if r_after:
        nb = r_after.get("nextBoost") or r_after.get("dailyBoost")
        if nb:
            print(f"    ✅ Emma reçoit bien le boost ({len(nb.get('exos',[]))} exos)")
        else:
            flag("WARN", "login Emma post-publish", "Boost publié mais non reçu au login !")
            nb = boost_j0  # fallback pour la sim

    boost_to_use = (r_after or {}).get("nextBoost") or (r_after or {}).get("dailyBoost") or boost_j0

    # Emma fait son boost J0 (5/5, top)
    done = s.do_boost_exos(boost_to_use, nb_exos=5, hard_rate=0.05)
    sleep()

    # Vérifier ExosDone dans overview
    ov2 = admin.overview("J0 après boost Emma")
    admin.check_action(ov2, s.code, "BOOST TERMINÉ", "Emma J0 après boost")

    # ── J1-J4 ─────────────────────────────────────────────
    cat_chap = errors[0] if errors else "Fractions"
    for day in range(1, 5):
        print(f"\n  📅 J+{day}")
        s.simulate_next_day()

        # Admin voit BOOST TERMINÉ → publie nouveau boost
        ov_d = admin.overview(f"J{day} avant boost Emma")
        admin.check_action(ov_d, s.code, "BOOST TERMINÉ", f"Emma J{day}")

        boost = make_boost(cat_chap)
        admin.publish_boost(s.code, boost)

        # Emma se connecte et fait le boost
        r = s.login(check_boost="expected")
        bt = (r or {}).get("nextBoost") or (r or {}).get("dailyBoost") or boost
        done = s.do_boost_exos(bt, nb_exos=5, hard_rate=0.05)

        # J1-J4 : quelques exos chapitre (5 par jour)
        s.do_chapter_exos(cat_chap, count=5, hard_rate=0.10)

        # Vérifier progress après chaque jour
        prog = s.get_progress()
        chaps = prog.get("chapitres", [])
        if chaps:
            fc = next((c for c in chaps if c.get("categorie") == cat_chap), None)
            if fc:
                print(f"    📊 Progress {cat_chap} : score={fc.get('score',0)}, nbExos={fc.get('nbExos',0)}, statut={fc.get('statut','?')}")

    # ── J5 : chapitre terminé (5j × 5 exos = 25 exos chap) ──
    print(f"\n  📅 J+5 — Chapitre terminé → admin assigne le suivant")
    s.simulate_next_day()

    ov5 = admin.overview("J5 Emma")
    emma5 = admin.find_student(ov5, s.code)
    if emma5:
        ap = emma5.get("actionPriority", "")
        print(f"    👁️  Admin J5 : action={ap[:70]}")
        if "CHAPITRE TERMINÉ" not in ap:
            flag("WARN", "Emma J5", f"CHAPITRE TERMINÉ attendu mais : {ap[:70]}")

    # Admin publie nouveau boost + nouveau chapitre
    boost5 = make_boost(cat_chap)
    admin.publish_boost(s.code, boost5)
    cat_chap2 = "Proportionnalité"
    exos_chap2 = make_chapter_exos(cat_chap2, 20)
    admin.publish_chapter(s.code, cat_chap2, exos_chap2,
                          insight=f"Tu maîtrises {cat_chap} — passons à {cat_chap2} !",
                          mot_prof=f"Excellent travail sur {cat_chap} — continue !")

    r5 = s.login(check_boost="expected")
    rt5 = (r5 or {}).get("nextBoost") or (r5 or {}).get("dailyBoost") or boost5
    s.do_boost_exos(rt5, nb_exos=5, hard_rate=0.05)

    # Vérifier nextChapter reçu
    next_chap = (r5 or {}).get("nextChapter")
    if next_chap:
        print(f"    ✅ Emma reçoit le chapitre : {next_chap.get('categorie','?')}")
    else:
        flag("WARN", "Emma J5", "nextChapter non reçu au login malgré publication admin")

    # ── J6-J7 : nouveau chapitre ──────────────────────────
    for day in [6, 7]:
        print(f"\n  📅 J+{day}")
        s.simulate_next_day()
        ov_d = admin.overview(f"J{day} Emma")
        boost = make_boost(cat_chap)
        admin.publish_boost(s.code, boost)
        r = s.login(check_boost="expected")
        bt = (r or {}).get("nextBoost") or (r or {}).get("dailyBoost") or boost
        s.do_boost_exos(bt, nb_exos=5, hard_rate=0.05)
        s.do_chapter_exos(cat_chap2, count=8, hard_rate=0.10)

    # Trial check J7
    s.simulate_next_day()
    t = s.check_trial_status()
    days = t.get("daysLeft", -1)
    if days <= 0:
        flag("WARN", "Emma trial J7", f"Trial expiré ou négatif daysLeft={days}")
    print(f"    ⏳ Trial : trialActive={t.get('trialActive')}, daysLeft={days}")

    return s


def scenario_lucas(admin):
    """
    Lucas Martin (5EME) — Le procrastinateur
    J0 : inscription + diagnostic + boost partiel (3/5)
    J1 : absent (pas de connexion)
    J2 : absent (toujours)
    J3 : revient, reprend, finit boost + commence chapitre (8 exos)
    J4-J5 : régulier (boost + chapitre)
    J6 : chapitre quasi-terminé (18/20) mais pas fini
    J7 : finit le chapitre (20/20)
    """
    print(f"\n{'═'*60}")
    print("👨‍🎓  LUCAS MARTIN (5EME) — Le procrastinateur")
    print(f"{'═'*60}")

    random.seed(2)
    s = Student("Lucas", "lucas.martin.test@gmail.com", "Lucas2026!", "5EME",
                "Le procrastinateur")

    print("\n  📅 J+0 — Inscription + diagnostic + boost partiel")
    if not s.register(): return None
    sleep()

    r0 = s.login(check_trial=True)
    errors = s.do_diagnostic(hard_rate=0.40)
    cat = errors[0] if errors else "Fractions"

    # Admin publie boost J0
    boost_j0 = make_boost(cat)
    admin.publish_boost(s.code, boost_j0)
    r_after = s.login(check_boost="expected")
    bt0 = (r_after or {}).get("nextBoost") or (r_after or {}).get("dailyBoost") or boost_j0

    # Lucas fait seulement 3/5 exos (distrait)
    done = s.do_boost_exos(bt0, nb_exos=3, hard_rate=0.40)
    s.note("S'arrête en cours de boost (3/5) — distrait")

    # Vérifier que admin voit bien 3/5 et PAS BOOST TERMINÉ
    ov0 = admin.overview("J0 après boost partiel Lucas")
    luc_st = admin.find_student(ov0, s.code)
    if luc_st:
        ap = luc_st.get("actionPriority", "")
        bh = luc_st.get("boostHistory", [])
        if bh:
            last_bh = bh[-1] if bh else {}
            exos_done = last_bh.get("exosDone", "?")
            print(f"    👁️  Admin J0 : action={ap[:60]}, lastBoost exosDone={exos_done}")
            if "BOOST TERMINÉ" in ap:
                flag("WARN", "Lucas J0 partiel", "Admin dit BOOST TERMINÉ alors que 3/5 seulement !")
        else:
            flag("WARN", "Lucas boostHistory", "boostHistory vide dans overview admin")

    # J1, J2 : absent (simulate_next_day mais pas de connexion)
    for day in [1, 2]:
        print(f"\n  📅 J+{day} — Lucas absent (pas de connexion)")
        s.simulate_next_day()
        s.note(f"J+{day} : pas connecté")

    # J3 : revient
    print(f"\n  📅 J+3 — Lucas revient")
    s.simulate_next_day()

    ov3 = admin.overview("J3 Lucas")
    luc3 = admin.find_student(ov3, s.code)
    if luc3:
        ap3 = luc3.get("actionPriority", "")
        print(f"    👁️  Admin J3 : action={ap3[:70]}")
        inact = luc3.get("inactivityDays", "?")
        print(f"    ⏱️  inactivityDays={inact}")
        if inact != "?" and inact >= 7:
            flag("WARN", "Lucas J3", f"Marqué BLOQUÉ après seulement J+3 ? inactivityDays={inact}")

    # Admin publie nouveau boost
    boost3 = make_boost(cat)
    admin.publish_boost(s.code, boost3)
    r3 = s.login()
    bt3 = (r3 or {}).get("nextBoost") or (r3 or {}).get("dailyBoost") or boost3
    s.do_boost_exos(bt3, nb_exos=5, hard_rate=0.35)
    s.do_chapter_exos(cat, count=8, hard_rate=0.30)

    # J4-J5
    for day in [4, 5]:
        print(f"\n  📅 J+{day}")
        s.simulate_next_day()
        ov_d = admin.overview(f"J{day} Lucas")
        admin.check_action(ov_d, s.code, "BOOST TERMINÉ", f"Lucas J{day}")
        boost = make_boost(cat)
        admin.publish_boost(s.code, boost)
        r = s.login()
        bt = (r or {}).get("nextBoost") or (r or {}).get("dailyBoost") or boost
        s.do_boost_exos(bt, nb_exos=5, hard_rate=0.30)
        s.do_chapter_exos(cat, count=5, hard_rate=0.25)

    # J6 : chapitre quasi-terminé (18/20 en cumulé)
    print(f"\n  📅 J+6 — Chapitre presque terminé (objectif 18/20)")
    s.simulate_next_day()
    # Calculer combien manque pour arriver à 18
    current_chap_count = s.chapter_exos.get(cat, 0)
    target = 18
    to_do = max(0, target - current_chap_count)
    if to_do > 0:
        s.do_chapter_exos(cat, count=to_do, hard_rate=0.25)
    s.note(f"Chapitre {cat} : {s.chapter_exos.get(cat,0)}/20 exos")

    # Vérifier que admin ne voit PAS CHAPITRE TERMINÉ
    ov6 = admin.overview("J6 Lucas")
    admin_check = admin.find_student(ov6, s.code)
    if admin_check:
        ap6 = admin_check.get("actionPriority", "")
        if "CHAPITRE TERMINÉ" in ap6:
            flag("WARN", "Lucas J6", f"CHAPITRE TERMINÉ à 18/20 ? action={ap6[:60]}")
        else:
            print(f"    ✅ Correct : pas encore CHAPITRE TERMINÉ ({ap6[:60]})")

    # J7 : finit le chapitre
    print(f"\n  📅 J+7 — Finit le chapitre")
    s.simulate_next_day()
    current_chap_count = s.chapter_exos.get(cat, 0)
    to_do = max(0, 20 - current_chap_count)
    if to_do > 0:
        s.do_chapter_exos(cat, count=to_do, hard_rate=0.25)

    ov7 = admin.overview("J7 Lucas")
    admin_check7 = admin.find_student(ov7, s.code)
    if admin_check7:
        ap7 = admin_check7.get("actionPriority", "")
        print(f"    👁️  Admin J7 : action={ap7[:70]}")
        if "CHAPITRE TERMINÉ" not in ap7:
            flag("WARN", "Lucas J7", f"CHAPITRE TERMINÉ attendu à 20+ exos, mais : {ap7[:60]}")
        else:
            print(f"    ✅ CHAPITRE TERMINÉ détecté correctement !")

    return s


def scenario_ines(admin):
    """
    Inès Dupont (3EME) — La bloquée
    J0 : inscription + diagnostic mauvais (70% HARD)
    J1 : boost 2/5, tous HARD, découragée
    J2-J7 : inactive
    → Doit déclencher BLOQUÉ dans admin + email J+7
    """
    print(f"\n{'═'*60}")
    print("👩‍🎓  INÈS DUPONT (3EME) — La bloquée")
    print(f"{'═'*60}")

    random.seed(3)
    s = Student("Inès", "ines.dupont.test@gmail.com", "Ines2026!", "3EME",
                "La bloquée")

    print("\n  📅 J+0 — Inscription + diagnostic difficile")
    if not s.register(): return None
    sleep()

    r0 = s.login(check_trial=True)
    errors = s.do_diagnostic(hard_rate=0.70)  # 70% HARD
    cat = errors[0] if errors else "Équations"

    # Admin voit Inès
    ov0 = admin.overview("J0 Inès")
    ines_st = admin.find_student(ov0, s.code)
    if ines_st:
        print(f"    👁️  Admin J0 Inès : action={ines_st.get('actionPriority','?')[:60]}")

    # Admin publie boost initial
    boost_j0 = make_boost(cat)
    admin.publish_boost(s.code, boost_j0)
    r_after = s.login(check_boost="expected")
    bt0 = (r_after or {}).get("nextBoost") or (r_after or {}).get("dailyBoost") or boost_j0

    # Inès fait 2 exos, tous HARD
    done = s.do_boost_exos(bt0, nb_exos=2, hard_rate=1.0)
    s.note("2 exos HARD — découragée, abandonne le boost")

    # J1 : tentative 1 exo, abandonne
    print(f"\n  📅 J+1 — Un seul exo, abandonne")
    s.simulate_next_day()
    ov1 = admin.overview("J1 Inès")
    ines1 = admin.find_student(ov1, s.code)
    if ines1:
        print(f"    👁️  Admin J1 : action={ines1.get('actionPriority','?')[:60]}")

    boost1 = make_boost(cat)
    admin.publish_boost(s.code, boost1)
    r1 = s.login()
    bt1 = (r1 or {}).get("nextBoost") or (r1 or {}).get("dailyBoost") or boost1
    s.do_boost_exos(bt1, nb_exos=1, hard_rate=1.0)
    s.note("1 exo HARD — abandonne totalement")

    # J2-J7 : inactive
    print(f"\n  📅 J+2 à J+7 — Inactive")
    for day in range(2, 8):
        s.simulate_next_day()
        s.note(f"J+{day} : pas connectée")

    # Vérifier état admin après J+7 d'inactivité
    ov_final = admin.overview("J7 Inès — finale")
    ines_final = admin.find_student(ov_final, s.code)
    if ines_final:
        ap = ines_final.get("actionPriority", "")
        inact = ines_final.get("inactivityDays", "?")
        cat_admin = ines_final.get("category", "?")
        ed = ines_final.get("emailsDue", [])
        print(f"    👁️  Admin J7 Inès : action={ap[:60]}")
        print(f"    ⏱️  inactivityDays={inact}, category={cat_admin}, emailsDue={ed}")

        if "BLOQUÉ" not in ap:
            flag("WARN", "Inès J7", f"BLOQUÉ attendu après 6j inactivité + 100% HARD, mais : {ap[:60]}")
        else:
            print(f"    ✅ 🔴 BLOQUÉ détecté correctement après inactivité")

        if "J+7" not in str(ed):
            flag("WARN", "Inès email J7", f"Email J+7 dû mais absent de emailsDue : {ed}")
        else:
            print(f"    ✅ Email J+7 dans emailsDue correctement")

    return s


def scenario_theo(admin):
    """
    Théo Bernard (4EME) — Le régulier
    J0-J3 : boost quotidien 5/5 parfait
    J4 : chapitre terminé (20 exos répartis sur 4j), admin assigne chapitre 2
    J5-J6 : nouveau chapitre
    J7 : vérif trial + état final
    """
    print(f"\n{'═'*60}")
    print("👨‍🎓  THÉO BERNARD (4EME) — Le régulier")
    print(f"{'═'*60}")

    random.seed(4)
    s = Student("Théo", "theo.bernard.test@gmail.com", "Theo2026!", "4EME",
                "Le régulier")

    print("\n  📅 J+0 — Inscription + diagnostic + boost")
    if not s.register(): return None
    sleep()

    r0 = s.login(check_trial=True)
    errors = s.do_diagnostic(hard_rate=0.25)
    cat = errors[0] if errors else "Calcul_Littéral"

    ov0 = admin.overview("J0 Théo")
    boost0 = make_boost(cat)
    admin.publish_boost(s.code, boost0)
    r_after = s.login()
    bt0 = (r_after or {}).get("nextBoost") or (r_after or {}).get("dailyBoost") or boost0
    s.do_boost_exos(bt0, nb_exos=5, hard_rate=0.20)
    s.do_chapter_exos(cat, count=5, hard_rate=0.20)

    # J1-J3 : régulier
    for day in range(1, 4):
        print(f"\n  📅 J+{day}")
        s.simulate_next_day()
        ov_d = admin.overview(f"J{day} Théo")
        admin.check_action(ov_d, s.code, "BOOST TERMINÉ", f"Théo J{day}")
        boost = make_boost(cat)
        admin.publish_boost(s.code, boost)
        r = s.login()
        bt = (r or {}).get("nextBoost") or (r or {}).get("dailyBoost") or boost
        s.do_boost_exos(bt, nb_exos=5, hard_rate=0.20)
        s.do_chapter_exos(cat, count=5, hard_rate=0.20)

    # J4 : chapitre terminé (5j × 5 = 25 exos)
    print(f"\n  📅 J+4 — Chapitre terminé + nouveau chapitre assigné")
    s.simulate_next_day()
    ov4 = admin.overview("J4 Théo")
    theo4 = admin.find_student(ov4, s.code)
    if theo4:
        ap4 = theo4.get("actionPriority", "")
        print(f"    👁️  Admin J4 : action={ap4[:70]}")
        if "CHAPITRE TERMINÉ" in ap4:
            print(f"    ✅ CHAPITRE TERMINÉ détecté à J4")
        else:
            flag("WARN", "Théo J4", f"CHAPITRE TERMINÉ attendu mais : {ap4[:60]}")

    boost4 = make_boost(cat)
    admin.publish_boost(s.code, boost4)
    cat2 = "Équations"
    exos2 = make_chapter_exos(cat2, 20)
    admin.publish_chapter(s.code, cat2, exos2,
                          insight=f"Excellent {cat} — place à {cat2} !",
                          mot_prof="Tu gères super bien, prêt pour le suivant ?")

    r4 = s.login()
    next_chap = (r4 or {}).get("nextChapter")
    if next_chap:
        print(f"    ✅ nextChapter reçu : {next_chap.get('categorie','?')}")
    else:
        flag("WARN", "Théo J4", "nextChapter non reçu après publication admin")

    bt4 = (r4 or {}).get("nextBoost") or (r4 or {}).get("dailyBoost") or boost4
    s.do_boost_exos(bt4, nb_exos=5, hard_rate=0.20)
    s.do_chapter_exos(cat2, count=8, hard_rate=0.20)

    # J5-J6
    for day in [5, 6]:
        print(f"\n  📅 J+{day}")
        s.simulate_next_day()
        ov_d = admin.overview(f"J{day} Théo")
        admin.check_action(ov_d, s.code, "BOOST TERMINÉ", f"Théo J{day}")
        boost = make_boost(cat2)
        admin.publish_boost(s.code, boost)
        r = s.login()
        bt = (r or {}).get("nextBoost") or (r or {}).get("dailyBoost") or boost
        s.do_boost_exos(bt, nb_exos=5, hard_rate=0.20)
        s.do_chapter_exos(cat2, count=6, hard_rate=0.20)

    # J7 : vérif finale
    print(f"\n  📅 J+7 — Vérification finale")
    s.simulate_next_day()
    t = s.check_trial_status()
    print(f"    ⏳ Trial : active={t.get('trialActive')}, daysLeft={t.get('daysLeft')}")

    ov7 = admin.overview("J7 Théo finale")
    theo7 = admin.find_student(ov7, s.code)
    if theo7:
        ap7 = theo7.get("actionPriority", "")
        chaps = theo7.get("chapitresDetail", [])
        print(f"    👁️  Admin J7 Théo : action={ap7[:60]}, {len(chaps)} chapitres")
        for c in chaps:
            print(f"       📘 {c.get('categorie','?')} : score={c.get('score',0)}, exos={c.get('nbExos',0)}, statut={c.get('statut','?')}")

    return s


def scenario_chloe(admin):
    """
    Chloé Rousseau (5EME) — L'arrivée tardive
    J0 : inscription SANS diagnostic (s'arrête après register)
    J1-J2 : absent
    J3 : revient, fait le diagnostic
    J4 : premier boost (admin publie)
    J5-J7 : routine normale
    """
    print(f"\n{'═'*60}")
    print("👩‍🎓  CHLOÉ ROUSSEAU (5EME) — L'arrivée tardive")
    print(f"{'═'*60}")

    random.seed(5)
    s = Student("Chloé", "chloe.rousseau.test@gmail.com", "Chloe2026!", "5EME",
                "L'arrivée tardive")

    print("\n  📅 J+0 — Inscription seulement (pas de diagnostic)")
    if not s.register(): return None
    sleep()

    r0 = s.login(check_trial=True, check_boost="not_expected")
    s.note("Inscrite mais ne fait pas le diagnostic — ferme l'appli")

    # Vérifier état admin : Chloé inscrite mais jamais commencé
    ov0 = admin.overview("J0 Chloé inscrite sans diag")
    chloe_st = admin.find_student(ov0, s.code)
    if chloe_st:
        ap = chloe_st.get("actionPriority", "")
        never_started = chloe_st.get("neverStarted", False)
        cat_admin = chloe_st.get("category", "?")
        print(f"    👁️  Admin J0 Chloé : action={ap[:60]}, neverStarted={never_started}, category={cat_admin}")
        if never_started is False:
            flag("WARN", "Chloé J0", "neverStarted devrait être true (pas de scores du tout)")

    # J1-J2 : absent
    for day in [1, 2]:
        print(f"\n  📅 J+{day} — Chloé absente")
        s.simulate_next_day()

    # J3 : Chloé revient et fait le diagnostic
    print(f"\n  📅 J+3 — Chloé fait le diagnostic")
    s.simulate_next_day()
    r3 = s.login()
    errors = s.do_diagnostic(hard_rate=0.50)
    cat = errors[0] if errors else "Fractions"

    ov3 = admin.overview("J3 Chloé post-diag")
    chloe3 = admin.find_student(ov3, s.code)
    if chloe3:
        ap3 = chloe3.get("actionPriority", "?")
        never_started3 = chloe3.get("neverStarted", "?")
        print(f"    👁️  Admin J3 après diag : action={ap3[:60]}, neverStarted={never_started3}")
        # Après diag, neverStarted devrait être false si diag = CALIBRAGE seulement
        # (le diag ne crée pas de Progress — donc toujours "jamais commencé" au sens boost ?)

    # J4 : admin publie premier boost
    print(f"\n  📅 J+4 — Premier boost pour Chloé")
    s.simulate_next_day()
    boost4 = make_boost(cat)
    admin.publish_boost(s.code, boost4)
    r4 = s.login(check_boost="expected")
    bt4 = (r4 or {}).get("nextBoost") or (r4 or {}).get("dailyBoost") or boost4

    if not bt4:
        flag("ERROR", "Chloé J4", "Boost publié mais Chloé ne le reçoit pas au login !")
    else:
        s.do_boost_exos(bt4, nb_exos=5, hard_rate=0.45)

    # J5-J6
    for day in [5, 6]:
        print(f"\n  📅 J+{day}")
        s.simulate_next_day()
        ov_d = admin.overview(f"J{day} Chloé")
        admin.check_action(ov_d, s.code, "BOOST TERMINÉ", f"Chloé J{day}")
        boost = make_boost(cat)
        admin.publish_boost(s.code, boost)
        r = s.login()
        bt = (r or {}).get("nextBoost") or (r or {}).get("dailyBoost") or boost
        s.do_boost_exos(bt, nb_exos=5, hard_rate=0.40)

    # J7 : trial status (début J0 = J+7 depuis inscription)
    print(f"\n  📅 J+7 — Trial status Chloé")
    s.simulate_next_day()
    t = s.check_trial_status()
    days = t.get("daysLeft", -1)
    is_active = t.get("trialActive", False)
    print(f"    ⏳ Trial : active={is_active}, daysLeft={days}")
    if is_active and days <= 0:
        flag("WARN", "Chloé trial J7", f"trialActive=True mais daysLeft={days}")

    # Vérifier que l'overlay trial J7 devrait s'afficher
    if not is_active:
        print(f"    ✅ Trial expiré à J7 — overlay Stripe devrait s'afficher")
    else:
        print(f"    ⚠️  Trial encore actif à J7 (daysLeft={days})")

    return s


# ══════════════════════════════════════════════════════════
# RAPPORT FINAL
# ══════════════════════════════════════════════════════════

def print_report(students, admin):
    print("\n\n" + "═"*70)
    print("  📊  RAPPORT FINAL — SIMULATION 7 JOURS")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("═"*70)

    # Vue d'ensemble admin finale
    print("\n🔭 ÉTAT FINAL ADMIN (get_admin_overview)\n")
    ov = admin.overview("rapport final")
    students_admin = ov.get("students", [])
    real_count = ov.get("realCount", 0)
    print(f"  Total élèves : {len(students_admin)} | Vrais élèves : {real_count}")

    for sa in students_admin:
        code    = sa.get("code", "?")
        prenom  = sa.get("prenom", "?")
        niveau  = sa.get("niveau", "?")
        ap      = sa.get("actionPriority", "?")
        chaps   = sa.get("chapitresDetail", [])
        bh      = sa.get("boostHistory", [])
        j0      = sa.get("j0Sent", "?")
        ed      = sa.get("emailsDue", [])
        cat_a   = sa.get("category", "?")
        inact   = sa.get("inactivityDays", "?")
        trial_d = sa.get("trialDays", "?")
        is_test = sa.get("isTest", "?")

        print(f"\n  ─── {prenom} ({niveau}) [{code}] ─────────────────────")
        print(f"    ⚡ Action : {ap[:70]}")
        print(f"    📧 J0envoyé={j0} | emailsDue={ed} | category={cat_a}")
        print(f"    ⏱️  Inactivité={inact}j | TrialDays={trial_d} | IsTest={is_test}")
        if chaps:
            print(f"    📚 Chapitres ({len(chaps)}) :")
            for c in chaps:
                print(f"       • {c.get('categorie','?'):<30} score={c.get('score',0):>3} exos={c.get('nbExos',0):>3} statut={c.get('statut','?')}")
        if bh:
            last = bh[-1] if bh else {}
            print(f"    🚀 Dernier boost : date={last.get('date','?')} exosDone={last.get('exosDone','?')}/5")

    # Log par élève
    print("\n\n📋  LOG PAR ÉLÈVE\n")
    for s in students:
        if not s: continue
        print(f"\n  {s.prenom} ({s.level}) [{s.code}] — {s.desc}")
        for line in s.log:
            print(f"    • {line}")

    # Anomalies
    print("\n\n⚠️  ANOMALIES DÉTECTÉES\n")
    if not ANOMALIES:
        print("  ✅ Aucune anomalie détectée !")
    else:
        errors = [a for a in ANOMALIES if a["severity"] == "ERROR"]
        warns  = [a for a in ANOMALIES if a["severity"] == "WARN"]
        infos  = [a for a in ANOMALIES if a["severity"] == "INFO"]

        if errors:
            print(f"  🔴 ERREURS ({len(errors)}) :")
            for a in errors:
                print(f"    [{a['context']}] {a['msg']}")
        if warns:
            print(f"\n  🟡 AVERTISSEMENTS ({len(warns)}) :")
            for a in warns:
                print(f"    [{a['context']}] {a['msg']}")
        if infos:
            print(f"\n  🔵 INFOS ({len(infos)}) :")
            for a in infos:
                print(f"    [{a['context']}] {a['msg']}")

    print("\n" + "═"*70)
    print("  FIN DE LA SIMULATION")
    print("═"*70 + "\n")


# ══════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════

def main():
    random.seed(42)
    print("\n" + "═"*70)
    print("  🏫  SIMULATION 7 JOURS — MATHEUX.FR")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("═"*70)

    print("\n🔑 Connexion admin…")
    admin = Admin()
    admin.login()

    students = []

    # Scénario 1 — Emma
    s1 = scenario_emma(admin)
    students.append(s1)

    # Scénario 2 — Lucas
    s2 = scenario_lucas(admin)
    students.append(s2)

    # Scénario 3 — Inès
    s3 = scenario_ines(admin)
    students.append(s3)

    # Scénario 4 — Théo
    s4 = scenario_theo(admin)
    students.append(s4)

    # Scénario 5 — Chloé
    s5 = scenario_chloe(admin)
    students.append(s5)

    # Rapport final
    print_report(students, admin)


if __name__ == "__main__":
    main()
