#!/usr/bin/env python3
"""
sim_7days_messages.py — Simulation 7 jours · 4 élèves · Audit messages
========================================================================
Crée 4 élèves réalistes, simule 7 jours complets de vie (diagnostic,
boost, chapitres, admin), et trace CHAQUE message/toast/banner affiché.

Rapport final : incohérences, textes bizarres, axes de fix.

Usage : python3 sim_7days_messages.py
"""

import json, hashlib, time, random, sys, os
from datetime import datetime, timedelta
import urllib.request, urllib.error

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

GAS_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF/exec"
)

TODAY = datetime.now()
DATE_FMT = "%Y-%m-%d"

# Tracking
ISSUES = []       # Incohérences trouvées
MESSAGES = []     # Tous les messages affichés
API_CALLS = 0
API_ERRORS = 0

def issue(severity, student, day, context, msg, state=None):
    entry = {"severity": severity, "student": student, "day": day,
             "context": context, "msg": msg}
    if state: entry["state"] = str(state)[:300]
    ISSUES.append(entry)
    icon = "🔴" if severity == "CRITICAL" else "🟠" if severity == "HIGH" else "🟡"
    print(f"    {icon} [{severity}] J{day} {student} — {context}: {msg}")

def track_msg(student, day, context, msg_type, msg_text):
    MESSAGES.append({"student": student, "day": day, "context": context,
                     "type": msg_type, "text": msg_text})

# ═══════════════════════════════════════════════════════════════
# HELPERS RÉSEAU
# ═══════════════════════════════════════════════════════════════

def gas(payload, label="", retry=2, verbose=True):
    global API_CALLS, API_ERRORS
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(GAS_URL, data=body,
                                 headers={"Content-Type": "application/json"}, method="POST")
    API_CALLS += 1
    for attempt in range(retry + 1):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                d = json.loads(r.read().decode("utf-8"))
                status = d.get("status", "?")
                ok = "✅" if status == "success" else "❌"
                if verbose:
                    print(f"      {ok} {label or payload.get('action','?')} → {status}")
                return d
        except Exception as e:
            if attempt < retry:
                time.sleep(2)
            else:
                API_ERRORS += 1
                print(f"      ❌ {label} → ERREUR: {e}")
                return {"status": "error", "message": str(e)}
    return {"status": "error", "message": "retry exhausted"}

def h256(email, password):
    raw = f"{email.lower().strip()}::{password}::AB22"
    return hashlib.sha256(raw.encode()).hexdigest()

def pause(s=0.5):
    time.sleep(s)

# ═══════════════════════════════════════════════════════════════
# FRONTEND STATE MACHINE — Simule l'état S.* et les messages
# ═══════════════════════════════════════════════════════════════

class FrontendState:
    """Simule l'état frontend (S.*) et évalue les messages affichés."""

    def __init__(self, student_name, day):
        self.name = student_name
        self.day = day
        self.boost = None
        self.boostConsumed = False
        self.boostEx = False
        self.boostPreping = False
        self.stk = 0
        self.xp = 0
        self.totalChapDone = 0  # Total exos faits hors calibrage/boost
        self.chapDone = {}      # { cat: True } chapitres terminés (20 exos)
        self.isNew = {}
        self.pendingManual = None
        self.trial = {"trialActive": True, "daysLeft": 7, "isPremium": False}
        self.diagInsight = None
        self.boostInsight = None
        self.isFirstDay = False
        self.history = []
        self.boostExosDone = 0
        self.res = {}           # { id: status }
        self.milestones = {}
        self.coach = {}
        self.toasts_shown = []  # Messages affichés cette session
        self.hero = None

    def load_from_login(self, d):
        """Charge l'état depuis la réponse login GAS."""
        self.boost = d.get("dailyBoost")
        self.boostEx = d.get("boostExistsInDB", False)
        self.isFirstDay = d.get("isFirstDay", False)
        self.boostExosDone = d.get("boostExosDone", 0)
        if self.boostExosDone >= 5:
            self.boostConsumed = True
        self.trial = d.get("trial", self.trial)
        self.history = d.get("history", [])
        self.xp = sum(int(h.get("xp", 0)) for h in self.history)
        # Compter exos par catégorie
        cat_counts = {}
        for h in self.history:
            cat = h.get("categorie", "")
            if cat not in ("CALIBRAGE", "BOOST", "BREVET"):
                cat_counts[cat] = cat_counts.get(cat, 0) + 1
                self.totalChapDone += 1
        for cat, count in cat_counts.items():
            if count >= 20:
                self.chapDone[cat] = True
        # Streak (simplifié)
        self.stk = d.get("profile", {}).get("streak", 0)
        # Remplir res
        for h in self.history:
            key = f"{h.get('niveau','')}-{h.get('categorie','')}-{int(h.get('exercice_idx',1))-1}"
            self.res[key] = h.get("resultat", "EASY")
        # nextChapter
        nc = d.get("nextChapter")
        if nc and isinstance(nc, dict):
            if nc.get("categorie") == "PENDING_MANUAL":
                self.pendingManual = nc.get("insight", "⏳ En préparation")
            else:
                self.pendingManual = None
                if nc.get("categorie"):
                    self.isNew[nc["categorie"]] = True
        elif nc and isinstance(nc, str):
            self.pendingManual = None
            self.isNew[nc] = True

    def eval_initapp_messages(self):
        """Évalue tous les messages affichés à initApp (login/refresh)."""
        msgs = []

        # S3 — Boost en cours
        if self.boostExosDone > 0 and self.boostExosDone < 5:
            n = 5 - self.boostExosDone
            msgs.append(("toast", f"Ton entraînement est en cours ⚡ — encore {n} exo{'s' if n>1 else ''} et c'est dans la boîte !"))

        # Trial warning
        t = self.trial
        if t.get("trialActive") and not t.get("isPremium"):
            dl = t.get("daysLeft", 7)
            if dl <= 3 and dl > 0:
                if dl == 1:
                    msgs.append(("toast", "⏰ Dernier jour d'essai — profite bien de ta session !"))
                else:
                    msgs.append(("toast", f"⏰ Plus que {dl} jours d'essai gratuit"))

        # Trial expired
        if not t.get("trialActive") and not t.get("isPremium"):
            msgs.append(("overlay", "Ton essai de 7 jours est terminé"))

        # S2 — Streak alert (après les fixes: stk >= 2 et pas de milestone dup)
        stk_mile_dup = (self.stk == 3 and 'streak_3' not in self.milestones) or \
                       (self.stk == 7 and 'streak_7' not in self.milestones)
        if self.stk >= 2 and not self.boostConsumed and not stk_mile_dup:
            msgs.append(("toast", f"🔥 Streak de {self.stk} jour{'s' if self.stk > 1 else ''} — fais ton entraînement pour le garder !"))

        # Trial badge
        if t.get("trialActive") and not t.get("isPremium"):
            dl = t.get("daysLeft", 7)
            if dl <= 5:
                if dl == 0:
                    msgs.append(("badge", "Essai terminé aujourd'hui ⏰"))
                elif dl <= 3:
                    msgs.append(("badge", f"J-{dl} · Essai se termine bientôt"))
                else:
                    msgs.append(("badge", f"Essai gratuit · J-{dl}"))

        return msgs

    def eval_hero(self, cats_available):
        """Évalue quel hero CTA est affiché. Retourne (priority, hero_dict) ou None."""

        # Calculer stats chapitres
        chapStats = {}
        for cat in cats_available:
            # Simulé : on utilise le nombre d'exos dans l'history pour ce cat
            done = sum(1 for h in self.history if h.get("categorie") == cat
                      and h.get("categorie") not in ("CALIBRAGE", "BOOST"))
            tot = 20  # Assume 20 exos par chapitre
            isDone = done >= tot or cat in self.chapDone
            chapStats[cat] = {"done": done, "tot": tot, "isDone": isDone}

        hero = None

        # P1: Boost pas fait (bouton générer)
        if self.boost and not self.boostConsumed and not self.boostEx:
            hero = ("P1", "Ton entraînement du jour")

        # P1b: Boost en cours (carte boost dans sortedKeys, pas hero mais carte active)
        if not hero and self.boostEx and self.boost and not self.boostConsumed:
            hero = ("P1b", "Boost actif — carte dans liste")

        # P2: Chapitre en cours
        if not hero:
            for cat, st in chapStats.items():
                if st["done"] > 0 and not st["isDone"]:
                    hero = ("P2", f"Continue {cat}")
                    break

        # P3: Chapitre recommandé (boost fait)
        if not hero and self.boostConsumed:
            for cat, st in chapStats.items():
                if st["done"] == 0 and not st["isDone"]:
                    hero = ("P3", f"C'est parti sur {cat}")
                    break

        # P4: Chapitre NEW
        if not hero:
            for cat in self.isNew:
                if self.isNew[cat] and cat in chapStats and not chapStats[cat]["isDone"]:
                    hero = ("P4", f"Nouveau : {cat}")
                    break

        # P5: Premier jour, 0 exos
        if not hero and self.totalChapDone == 0:
            for cat in cats_available:
                if cat not in self.chapDone:
                    hero = ("P5", f"Commence par {cat}")
                    break

        # Fallback: Session terminée
        if not hero and self.boostConsumed:
            hero = ("DONE", "Entraînement du jour terminé — continue sur tes chapitres ou reviens demain 💪")

        self.hero = hero
        return hero

    def eval_banners(self):
        """Évalue les banners affichés dans la section chapitres."""
        banners = []

        if self.pendingManual:
            banners.append(("pending", self.pendingManual))

        _showBoostInvite = self.totalChapDone == 0 and self.boostConsumed
        _showFirstGuide = self.totalChapDone == 0 and not self.boost and not self.boostConsumed and not _showBoostInvite

        if _showFirstGuide:
            banners.append(("guide", "Commence par là"))
        if _showBoostInvite:
            banners.append(("invite", "Chapitre recommandé par le boost"))

        return banners

    def eval_exercise_msgs(self, is_correct, is_first_wrong, exo_count):
        """Messages affichés pendant un exercice."""
        msgs = []

        if is_correct:
            msgs.append(("toast", "Bonne réponse (ok_*)"))
            msgs.append(("xp", "+100 XP"))
        else:
            if is_first_wrong and "tip_wrong" not in self.coach:
                self.coach["tip_wrong"] = True
                msgs.append(("toast", "Pas grave — les indices et la correction s'affichent pour t'aider"))
            else:
                msgs.append(("toast", "Mauvaise réponse (ko_*)"))

        # Milestones
        total_exos = len(self.res) + 1
        if total_exos >= 10 and "exos_10" not in self.milestones:
            self.milestones["exos_10"] = True
            msgs.append(("milestone", "10 exercices — tu prends le rythme 🔥"))

        return msgs

    def eval_boost_complete(self, easy, total):
        """Messages à la complétion du boost."""
        msgs = []
        self.boostConsumed = True
        self.xp += 200

        # Insight screen
        if easy == total:
            msgs.append(("insight", f"Parfait ! {easy}/{total} — garde ce rythme 🔥"))
        elif easy >= total * 0.6:
            msgs.append(("insight", f"Beau travail. {easy} exercices dans la boîte aujourd'hui."))
        else:
            msgs.append(("insight", f"Quelques notions à retravailler. Ton prochain boost sera encore plus ciblé."))

        msgs.append(("insight", "✨ Prochain entraînement demain — ton boost sera encore plus ciblé !"))

        # Milestone
        if "first_boost" not in self.milestones:
            self.milestones["first_boost"] = True
            msgs.append(("milestone", "Premier entraînement terminé — c'est le plus dur 💪"))

        return msgs

    def eval_chap_complete(self, cat, easy, total):
        """Messages à la complétion d'un chapitre."""
        msgs = []
        self.chapDone[cat] = True
        self.xp += 300

        msgs.append(("toast", "🏆 Chapitre terminé — bien joué !"))

        if "first_chap" not in self.milestones:
            self.milestones["first_chap"] = True
            msgs.append(("milestone", "Ton premier chapitre maîtrisé — la suite va aller plus vite ⭐"))

        return msgs

    def check_contradictions(self, day_label):
        """Vérifie les contradictions d'état."""
        problems = []

        # Contradiction : boostConsumed ET boost carte active
        if self.boostConsumed and self.boost and not self.boostEx:
            problems.append("boostConsumed=true mais boost non encore en DB")

        # Contradiction : pendingManual ET isNew sur même chapitre
        if self.pendingManual:
            for cat in self.isNew:
                if self.isNew[cat]:
                    problems.append(f"pendingManual actif ET isNew[{cat}]=true")

        # Contradiction : hero "Session terminée" mais chapitres pas encore commencés
        if self.hero and self.hero[0] == "DONE" and self.totalChapDone == 0:
            problems.append("Hero 'Session terminée' affiché mais 0 chapitre commencé — devrait encourager à commencer un chapitre")

        # Contradiction : streak toast + milestone streak même session
        # (déjà fixé par _stkMileDup mais vérifions)

        # Contradiction : diagInsight encore visible après avoir fermé

        return problems


# ═══════════════════════════════════════════════════════════════
# PROFILS ÉTUDIANTS
# ═══════════════════════════════════════════════════════════════

STUDENTS = [
    {
        "id": "WK01", "prenom": "Lina", "niveau": "6EME",
        "email": "wk01.lina@test-matheux.fr", "password": "TestLina2026!",
        "objectif": "lacunes",
        "scenario": "parfait",
        "desc": "Élève parfaite — boost chaque jour, chapitres le soir, streaks",
        "daily_plan": {
            # day: { "boost": True/False, "chap_exos": N, "skip": False, "admin_action": None }
            0: {"boost": True, "chap_exos": 5, "skip": False},
            1: {"boost": True, "chap_exos": 8, "skip": False},
            2: {"boost": True, "chap_exos": 7, "skip": False},
            3: {"boost": True, "chap_exos": 5, "skip": False},
            4: {"boost": True, "chap_exos": 5, "skip": False},
            5: {"boost": True, "chap_exos": 10, "skip": False},
            6: {"boost": True, "chap_exos": 5, "skip": False},
        }
    },
    {
        "id": "WK02", "prenom": "Samir", "niveau": "4EME",
        "email": "wk02.samir@test-matheux.fr", "password": "TestSamir2026!",
        "objectif": "chapitre_jour",
        "scenario": "irregulier",
        "desc": "Irrégulier — J0-J1 actif, J2-J3 absent, J4 retour, J5 actif, J6 absent",
        "daily_plan": {
            0: {"boost": True, "chap_exos": 3, "skip": False},
            1: {"boost": True, "chap_exos": 5, "skip": False},
            2: {"boost": False, "chap_exos": 0, "skip": True},   # Absent
            3: {"boost": False, "chap_exos": 0, "skip": True},   # Absent
            4: {"boost": True, "chap_exos": 2, "skip": False},   # Retour
            5: {"boost": True, "chap_exos": 8, "skip": False},
            6: {"boost": False, "chap_exos": 0, "skip": True},   # Absent
        }
    },
    {
        "id": "WK03", "prenom": "Jade", "niveau": "3EME",
        "email": "wk03.jade@test-matheux.fr", "password": "TestJade2026!",
        "objectif": "brevet",
        "scenario": "trial_convert",
        "desc": "Sérieuse — trial complet, convertit J+5, admin lui assigne chapitre J+3",
        "daily_plan": {
            0: {"boost": True, "chap_exos": 5, "skip": False},
            1: {"boost": True, "chap_exos": 5, "skip": False},
            2: {"boost": True, "chap_exos": 5, "skip": False},
            3: {"boost": True, "chap_exos": 5, "skip": False, "admin": "assign_chapter"},
            4: {"boost": True, "chap_exos": 10, "skip": False},
            5: {"boost": True, "chap_exos": 5, "skip": False},  # Conversion (simulée)
            6: {"boost": True, "chap_exos": 5, "skip": False},
        }
    },
    {
        "id": "WK04", "prenom": "Nolan", "niveau": "5EME",
        "email": "wk04.nolan@test-matheux.fr", "password": "TestNolan2026!",
        "objectif": "toutes_matieres",
        "scenario": "decrocheur",
        "desc": "Fait le diag + J0, puis abandonne — jamais de boost après J+1",
        "daily_plan": {
            0: {"boost": True, "chap_exos": 2, "skip": False},
            1: {"boost": True, "chap_exos": 0, "skip": False},
            2: {"boost": False, "chap_exos": 0, "skip": True},
            3: {"boost": False, "chap_exos": 0, "skip": True},
            4: {"boost": False, "chap_exos": 0, "skip": True},
            5: {"boost": False, "chap_exos": 0, "skip": True},
            6: {"boost": False, "chap_exos": 0, "skip": True},  # Trial expire
        }
    },
]

CHAPITRES = {
    "6EME": ["Nombres_entiers", "Fractions", "Proportionnalité", "Géométrie", "Périmètres_Aires",
             "Angles", "Nombres_Décimaux", "Statistiques_6ème", "Symétrie_Axiale", "Volumes"],
    "5EME": ["Fractions", "Nombres_relatifs", "Proportionnalité", "Calcul_Littéral",
             "Pythagore", "Puissances", "Symétrie_Centrale", "Transformations"],
    "4EME": ["Puissances", "Fractions", "Proportionnalité", "Calcul_Littéral",
             "Équations", "Pythagore", "Fonctions_Linéaires", "Inéquations"],
    "3EME": ["Calcul_Littéral", "Équations", "Fonctions", "Théorème_de_Thalès",
             "Trigonométrie", "Statistiques", "Probabilités", "Racines_Carrées"],
}


# ═══════════════════════════════════════════════════════════════
# PHASE 1 : NETTOYAGE + INSCRIPTION
# ═══════════════════════════════════════════════════════════════

def cleanup_students():
    """Supprime les étudiants WK01-WK04 s'ils existent."""
    print("\n🧹 Nettoyage étudiants WK01-WK04...")
    from sheets import sh
    try:
        ws = sh.worksheet("Users")
        all_vals = ws.get_all_values()
        if len(all_vals) < 2:
            print("    Aucun utilisateur à nettoyer")
            return
        headers = all_vals[0]
        code_col = headers.index("Code") if "Code" in headers else 0
        rows_to_delete = []
        for i, row in enumerate(all_vals[1:], start=2):
            if len(row) > code_col and row[code_col].startswith("WK0"):
                rows_to_delete.append(i)
        if rows_to_delete:
            for r in sorted(rows_to_delete, reverse=True):
                ws.delete_rows(r)
                print(f"    Supprimé ligne {r}")
            pause(1)

        # Nettoyer Historique
        hs = sh.worksheet("Historique")
        h_vals = hs.get_all_values()
        if len(h_vals) > 1:
            h_headers = h_vals[0]
            h_code_col = h_headers.index("Code") if "Code" in h_headers else 0
            h_rows = []
            for i, row in enumerate(h_vals[1:], start=2):
                if len(row) > h_code_col and row[h_code_col].startswith("WK0"):
                    h_rows.append(i)
            if h_rows:
                for r in sorted(h_rows, reverse=True):
                    hs.delete_rows(r)
                print(f"    Supprimé {len(h_rows)} lignes Historique")

        # Nettoyer Suivi
        ss = sh.worksheet("Suivi")
        s_vals = ss.get_all_values()
        if len(s_vals) > 1:
            s_headers = s_vals[0]
            s_code_col = s_headers.index("Code") if "Code" in s_headers else 0
            s_rows = []
            for i, row in enumerate(s_vals[1:], start=2):
                if len(row) > s_code_col and row[s_code_col].startswith("WK0"):
                    s_rows.append(i)
            if s_rows:
                for r in sorted(s_rows, reverse=True):
                    ss.delete_rows(r)
                print(f"    Supprimé {len(s_rows)} lignes Suivi")

        print("    ✅ Nettoyage terminé")
    except Exception as e:
        print(f"    ⚠️ Nettoyage partiel: {e}")


def register_student(s):
    """Inscrit un étudiant via GAS."""
    print(f"\n📝 Inscription {s['prenom']} ({s['id']}, {s['niveau']})...")
    pwd_hash = h256(s["email"], s["password"])
    d = gas({
        "action": "register",
        "name": s["prenom"],
        "email": s["email"],
        "password": pwd_hash,
        "level": s["niveau"],
        "objectif": s["objectif"]
    }, label=f"register {s['id']}")

    if d.get("status") != "success":
        # Peut-être déjà inscrit — essayer login
        print(f"    ⚠️ Register échoué, tentative login...")
        d = gas({
            "action": "login",
            "email": s["email"],
            "password": pwd_hash
        }, label=f"login {s['id']}")

    if d.get("status") == "success":
        code = d.get("profile", {}).get("code", d.get("code", ""))
        s["code"] = code
        print(f"    ✅ Code: {code}")
        return d
    else:
        print(f"    ❌ Échec inscription/login: {d.get('message','')}")
        return None


def login_student(s):
    """Login un étudiant via GAS."""
    pwd_hash = h256(s["email"], s["password"])
    d = gas({
        "action": "login",
        "email": s["email"],
        "password": pwd_hash
    }, label=f"login {s['id']}", verbose=False)
    return d


# ═══════════════════════════════════════════════════════════════
# PHASE 2 : SIMULATION BOOST QUOTIDIEN
# ═══════════════════════════════════════════════════════════════

def do_boost(s, state, day):
    """Génère et joue le boost quotidien."""
    print(f"    ⚡ Boost J{day}...")

    # Générer le boost
    d = gas({
        "action": "generate_daily_boost",
        "code": s["code"],
        "level": s["niveau"]
    }, label=f"boost {s['id']} J{day}")
    pause()

    if d.get("status") != "success":
        issue("HIGH", s["prenom"], day, "boost_gen", f"Échec génération: {d.get('message','')}")
        return

    boost = d.get("boost", {})
    exos = boost.get("exos", [])
    if not exos:
        issue("HIGH", s["prenom"], day, "boost_gen", "Boost sans exercices")
        return

    state.boost = boost
    state.boostEx = True

    # Coach tip first boost
    if "boost_first" not in state.coach:
        state.coach["boost_first"] = True
        track_msg(s["prenom"], day, "boost_start", "toast",
                  "⚡ C'est ton Entraînement du jour — 5 exos, ~10 min. C'est parti !")

    # Jouer les 5 exos
    easy = 0
    for i, exo in enumerate(exos):
        # Simuler réponse (70% correct pour parfait, 50% pour les autres)
        correct_rate = 0.7 if s["scenario"] == "parfait" else 0.5
        is_correct = random.random() < correct_rate
        resultat = "EASY" if is_correct else "HARD"
        if is_correct:
            easy += 1

        # Vérifier messages exercice
        is_first_wrong = not is_correct and "tip_wrong" not in state.coach
        ex_msgs = state.eval_exercise_msgs(is_correct, is_first_wrong, i+1)
        for mt, msg in ex_msgs:
            track_msg(s["prenom"], day, f"boost_exo_{i+1}", mt, msg)

        # Sauvegarder score
        gas({
            "action": "save_score",
            "code": s["code"],
            "name": s["prenom"],
            "level": s["niveau"],
            "categorie": exo.get("_cat", exo.get("oC", "BOOST")),
            "exercice_idx": i,
            "resultat": resultat,
            "q": exo.get("q", "Question")[:100],
            "time": random.randint(15, 90),
            "source": "BOOST"
        }, label=f"  score boost {i+1}", verbose=False)

        state.res[f"{s['niveau']}-BOOST-{i}"] = resultat
        pause(0.3)

    # Save boost
    gas({
        "action": "save_boost",
        "code": s["code"],
        "boost": boost,
        "exoIdx": len(exos) - 1
    }, label=f"save_boost {s['id']}", verbose=False)
    pause()

    # Messages complétion boost
    comp_msgs = state.eval_boost_complete(easy, len(exos))
    for mt, msg in comp_msgs:
        track_msg(s["prenom"], day, "boost_complete", mt, msg)

    print(f"      📊 Boost: {easy}/{len(exos)} réussis")


def do_chapter_exos(s, state, day, n_exos):
    """Joue N exercices dans un chapitre."""
    if n_exos == 0:
        return

    chaps = CHAPITRES.get(s["niveau"], [])
    # Trouver le premier chapitre non terminé
    target_chap = None
    for ch in chaps:
        if ch not in state.chapDone:
            target_chap = ch
            break
    if not target_chap:
        track_msg(s["prenom"], day, "chapters", "info", "Tous les chapitres terminés")
        return

    print(f"    📘 Chapitre {target_chap} — {n_exos} exos...")

    easy = 0
    for i in range(n_exos):
        # Exercice idx = nombre d'exos déjà faits dans ce chapitre
        existing = sum(1 for h in state.history if h.get("categorie") == target_chap)
        idx = existing + i

        correct_rate = 0.75 if s["scenario"] == "parfait" else 0.55
        is_correct = random.random() < correct_rate
        resultat = "EASY" if is_correct else "HARD"
        if is_correct:
            easy += 1

        gas({
            "action": "save_score",
            "code": s["code"],
            "name": s["prenom"],
            "level": s["niveau"],
            "categorie": target_chap,
            "exercice_idx": idx,
            "resultat": resultat,
            "q": f"Exercice {target_chap} #{idx+1}",
            "time": random.randint(20, 120)
        }, label=f"  score chap {idx+1}", verbose=False)

        state.res[f"{s['niveau']}-{target_chap}-{idx}"] = resultat
        state.totalChapDone += 1
        state.history.append({
            "categorie": target_chap, "exercice_idx": str(idx+1),
            "resultat": resultat, "xp": "100" if is_correct else "10"
        })
        pause(0.2)

    # Vérifier complétion chapitre (20 exos)
    chap_exos = sum(1 for h in state.history if h.get("categorie") == target_chap)
    if chap_exos >= 20:
        comp_msgs = state.eval_chap_complete(target_chap, easy, chap_exos)
        for mt, msg in comp_msgs:
            track_msg(s["prenom"], day, "chap_complete", mt, msg)
        print(f"      🏆 Chapitre {target_chap} terminé !")
    else:
        print(f"      📊 Chapitre: {chap_exos}/20 exos")


# ═══════════════════════════════════════════════════════════════
# PHASE 3 : ADMIN ACTIONS
# ═══════════════════════════════════════════════════════════════

def admin_assign_chapter(s, state, day):
    """Simule Nicolas qui assigne un chapitre via l'admin."""
    print(f"    👨‍💻 Admin: assigne chapitre à {s['prenom']}...")
    chaps = CHAPITRES.get(s["niveau"], [])
    # Trouver un chapitre pas encore commencé
    target = None
    for ch in chaps:
        if ch not in state.chapDone and ch not in state.isNew:
            target = ch
            break
    if not target:
        print("      ⚠️ Aucun chapitre à assigner")
        return

    d = gas({
        "action": "publish_admin_chapter",
        "code": s["code"],
        "chapter_name": target
    }, label=f"admin assign {target}")

    if d.get("status") == "success":
        state.isNew[target] = True
        state.pendingManual = None  # Devrait être nettoyé
        track_msg(s["prenom"], day, "admin", "backend", f"Chapitre {target} assigné par Nicolas")
    pause()


# ═══════════════════════════════════════════════════════════════
# PHASE 4 : SIMULATION JOUR PAR JOUR
# ═══════════════════════════════════════════════════════════════

def simulate_day(s, state, day):
    """Simule une journée complète pour un étudiant."""
    plan = s["daily_plan"].get(day, {"boost": False, "chap_exos": 0, "skip": True})

    if plan.get("skip"):
        print(f"  📵 {s['prenom']} absent J{day}")
        # Vérifier les messages que l'élève verrait s'il revenait
        if day >= 3:
            track_msg(s["prenom"], day, "absent", "info",
                      f"Absent depuis {day - max(d for d in s['daily_plan'] if not s['daily_plan'][d].get('skip', True) and d < day) if any(not s['daily_plan'][d].get('skip', True) for d in range(day)) else day} jours")
        return

    print(f"\n  🎮 {s['prenom']} J{day} — {s['desc']}")

    # 1. Login
    d = login_student(s)
    if d.get("status") != "success":
        issue("CRITICAL", s["prenom"], day, "login", f"Échec login: {d.get('message','')}")
        return

    state.load_from_login(d)

    # 2. Messages initApp
    init_msgs = state.eval_initapp_messages()
    for mt, msg in init_msgs:
        track_msg(s["prenom"], day, "initApp", mt, msg)

    # 3. Trial badge check
    trial_days = state.trial.get("daysLeft", 7)
    if trial_days <= 0 and not state.trial.get("isPremium"):
        issue("HIGH", s["prenom"], day, "trial", "Trial expiré — overlay bloquant affiché")
        track_msg(s["prenom"], day, "trial", "overlay", "Essai terminé — upgrade")
        return  # Bloqué

    # 4. Hero CTA
    chaps = CHAPITRES.get(s["niveau"], [])
    hero = state.eval_hero(chaps)
    if hero:
        track_msg(s["prenom"], day, "hero", "hero_cta", f"[{hero[0]}] {hero[1]}")

    # 5. Banners
    banners = state.eval_banners()
    for bt, bm in banners:
        track_msg(s["prenom"], day, "banner", bt, bm)

    # 6. Admin action (avant boost/chapitre)
    if plan.get("admin") == "assign_chapter":
        admin_assign_chapter(s, state, day)

    # 7. Boost
    if plan.get("boost"):
        do_boost(s, state, day)
        pause()

        # Re-eval hero après boost
        hero2 = state.eval_hero(chaps)
        if hero2:
            track_msg(s["prenom"], day, "hero_post_boost", "hero_cta", f"[{hero2[0]}] {hero2[1]}")

    # 8. Chapitres
    if plan.get("chap_exos", 0) > 0:
        do_chapter_exos(s, state, day, plan["chap_exos"])

    # 9. Contradictions check
    problems = state.check_contradictions(f"J{day}")
    for p in problems:
        issue("CRITICAL", s["prenom"], day, "contradiction", p)

    # 10. Vérifier cohérence messages de la session
    session_msgs = [m for m in MESSAGES if m["student"] == s["prenom"] and m["day"] == day]

    # Vérifier : pas de "reviens demain" si l'élève a encore des chapitres à faire
    demain_msgs = [m for m in session_msgs if "demain" in m.get("text", "").lower()]
    has_chapters = len(state.chapDone) < len(chaps)
    for dm in demain_msgs:
        if has_chapters and "continue" not in dm.get("text", "").lower() and "boost" not in dm.get("context", ""):
            issue("HIGH", s["prenom"], day, "copy_demain",
                  f"Message '{dm['text'][:60]}' dit 'demain' mais il reste des chapitres à faire")

    # Vérifier : pas de message de streak si streak = 0 ou 1
    streak_msgs = [m for m in session_msgs if "streak" in m.get("text", "").lower()]
    if state.stk <= 1 and streak_msgs:
        issue("HIGH", s["prenom"], day, "streak_faux",
              f"Message streak alors que streak = {state.stk}")

    # Vérifier : pas de double toast dans le même contexte
    toast_contexts = {}
    for m in session_msgs:
        if m["type"] == "toast":
            ctx = m["context"]
            if ctx in toast_contexts:
                # C'est OK si c'est un contexte différent (boost_exo_1, boost_exo_2...)
                if not ctx.startswith("boost_exo_") and not ctx.startswith("chap_"):
                    pass  # La queue gère ça maintenant, pas un problème
            toast_contexts[ctx] = m


# ═══════════════════════════════════════════════════════════════
# PHASE 5 : SIMULATION ADMIN OVERVIEW
# ═══════════════════════════════════════════════════════════════

def check_admin_view(day):
    """Vérifie la vue admin après simulation."""
    print(f"\n  👨‍💻 Admin overview J{day}...")
    d = gas({
        "action": "get_admin_overview"
    }, label=f"admin overview J{day}")

    if d.get("status") != "success":
        issue("HIGH", "Admin", day, "admin_overview", f"Échec: {d.get('message','')}")
        return

    students = d.get("students", [])
    wk_students = [s for s in students if s.get("code", "").startswith("WK0")]

    for ws in wk_students:
        code = ws.get("code", "")
        name = ws.get("name", "")
        exos = ws.get("exosDone", 0)
        streak = ws.get("streak", 0)
        premium = ws.get("premium", "")
        trial_end = ws.get("trialEnd", "")

        track_msg("Admin", day, "overview", "admin_card",
                  f"{name} ({code}): {exos} exos, streak {streak}, premium={premium}")

        # Vérifier cohérence
        if premium == "1" and trial_end:
            issue("WARN", "Admin", day, "admin_data",
                  f"{name} premium=1 mais trial_end={trial_end} — devrait être vide")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("  SIMULATION 7 JOURS · 4 ÉLÈVES · AUDIT MESSAGES")
    print("  " + datetime.now().strftime("%Y-%m-%d %H:%M"))
    print("=" * 70)

    # Phase 0 : Nettoyage
    cleanup_students()
    pause(2)

    # Phase 1 : Inscription des 4 élèves
    print("\n" + "─" * 50)
    print("  PHASE 1 — INSCRIPTIONS")
    print("─" * 50)

    states = {}
    for s in STUDENTS:
        d = register_student(s)
        if d and d.get("status") == "success":
            states[s["id"]] = FrontendState(s["prenom"], 0)
            states[s["id"]].load_from_login(d)

            # Messages initApp post-inscription
            init_msgs = states[s["id"]].eval_initapp_messages()
            for mt, msg in init_msgs:
                track_msg(s["prenom"], 0, "register_init", mt, msg)
        pause(1)

    # Phase 2 : Simulation 7 jours
    for day in range(7):
        print("\n" + "═" * 60)
        print(f"  JOUR {day} — {(TODAY + timedelta(days=day)).strftime('%A %d %B')}")
        print("═" * 60)

        for s in STUDENTS:
            if s["id"] not in states:
                continue
            state = states[s["id"]]
            state.day = day
            simulate_day(s, state, day)
            pause(0.5)

        # Admin overview en fin de journée
        if day in (0, 2, 4, 6):
            check_admin_view(day)

        # Jour 3 : admin assigne chapitre à Jade (via daily_plan)
        # (déjà dans le daily_plan)

    # ═══════════════════════════════════════════════════════════════
    # RAPPORT FINAL
    # ═══════════════════════════════════════════════════════════════

    print("\n\n")
    print("█" * 70)
    print("  RAPPORT FINAL — SIMULATION 7 JOURS")
    print("█" * 70)

    # Stats
    print(f"\n📊 Statistiques :")
    print(f"   API calls : {API_CALLS}")
    print(f"   API errors : {API_ERRORS}")
    print(f"   Messages trackés : {len(MESSAGES)}")
    print(f"   Issues trouvées : {len(ISSUES)}")

    # Messages par élève par jour
    print(f"\n📋 Messages par élève :")
    for s in STUDENTS:
        student_msgs = [m for m in MESSAGES if m["student"] == s["prenom"]]
        print(f"\n   {s['prenom']} ({s['id']}, {s['niveau']}, {s['scenario']}) — {len(student_msgs)} messages :")
        for day in range(7):
            day_msgs = [m for m in student_msgs if m["day"] == day]
            if day_msgs:
                print(f"      J{day}:")
                for m in day_msgs:
                    print(f"         [{m['type']:12}] {m['context']:20} → {m['text'][:70]}")

    # Issues
    if ISSUES:
        print(f"\n🔍 ISSUES DÉTECTÉES ({len(ISSUES)}) :")
        by_severity = {}
        for i in ISSUES:
            sev = i["severity"]
            if sev not in by_severity:
                by_severity[sev] = []
            by_severity[sev].append(i)

        for sev in ["CRITICAL", "HIGH", "WARN"]:
            items = by_severity.get(sev, [])
            if items:
                icon = "🔴" if sev == "CRITICAL" else "🟠" if sev == "HIGH" else "🟡"
                print(f"\n   {icon} {sev} ({len(items)}) :")
                for i in items:
                    print(f"      J{i['day']} {i['student']} — {i['context']}: {i['msg']}")
    else:
        print("\n✅ AUCUNE ISSUE DÉTECTÉE — système cohérent")

    # Analyse contradictions messages "demain"
    print(f"\n📝 Audit copie 'demain' :")
    demain_all = [m for m in MESSAGES if "demain" in m.get("text", "").lower()]
    if demain_all:
        for m in demain_all:
            print(f"   J{m['day']} {m['student']} [{m['context']}]: {m['text'][:80]}")
    else:
        print("   Aucun message 'demain'")

    # Audit toasts par session (vérifier queue)
    print(f"\n📝 Audit queue toasts (sessions avec >2 toasts) :")
    for s in STUDENTS:
        for day in range(7):
            toasts = [m for m in MESSAGES if m["student"] == s["prenom"]
                     and m["day"] == day and m["type"] == "toast"]
            if len(toasts) > 2:
                print(f"   {s['prenom']} J{day}: {len(toasts)} toasts (queue gère)")
                for t in toasts:
                    print(f"      [{t['context']}] {t['text'][:60]}")

    # Vérifier hero CTA jamais vide
    print(f"\n📝 Audit hero CTA :")
    for s in STUDENTS:
        for day in range(7):
            heroes = [m for m in MESSAGES if m["student"] == s["prenom"]
                     and m["day"] == day and m["type"] == "hero_cta"]
            plan = s["daily_plan"].get(day, {})
            if not plan.get("skip") and not heroes:
                issue("WARN", s["prenom"], day, "hero_missing", "Aucun hero CTA affiché")

    # Save rapport
    rapport_path = os.path.join(os.path.dirname(__file__), "docs", "rapport-sim-7j-messages.md")
    with open(rapport_path, "w") as f:
        f.write(f"# Rapport Simulation 7 jours — Audit Messages\n\n")
        f.write(f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(f"## Stats\n")
        f.write(f"- API calls : {API_CALLS}\n")
        f.write(f"- API errors : {API_ERRORS}\n")
        f.write(f"- Messages trackés : {len(MESSAGES)}\n")
        f.write(f"- Issues : {len(ISSUES)}\n\n")

        f.write(f"## Élèves\n\n")
        for s in STUDENTS:
            f.write(f"### {s['prenom']} ({s['id']}, {s['niveau']}, {s['scenario']})\n\n")
            f.write(f"{s['desc']}\n\n")
            student_msgs = [m for m in MESSAGES if m["student"] == s["prenom"]]
            for day in range(7):
                day_msgs = [m for m in student_msgs if m["day"] == day]
                if day_msgs:
                    f.write(f"**J{day}:**\n")
                    for m in day_msgs:
                        f.write(f"- `[{m['type']}]` {m['context']} → {m['text']}\n")
                    f.write("\n")

        if ISSUES:
            f.write(f"## Issues ({len(ISSUES)})\n\n")
            for i in ISSUES:
                sev = i["severity"]
                icon = "🔴" if sev == "CRITICAL" else "🟠" if sev == "HIGH" else "🟡"
                f.write(f"- {icon} **{sev}** J{i['day']} {i['student']} — {i['context']}: {i['msg']}\n")
        else:
            f.write("## ✅ Aucune issue\n")

        f.write(f"\n## Audit 'demain'\n\n")
        if demain_all:
            for m in demain_all:
                f.write(f"- J{m['day']} {m['student']} [{m['context']}]: {m['text']}\n")
        else:
            f.write("Aucun usage de 'demain' problématique.\n")

    print(f"\n📄 Rapport sauvé : {rapport_path}")

    # Code de sortie
    critical = len([i for i in ISSUES if i["severity"] == "CRITICAL"])
    if critical > 0:
        print(f"\n❌ {critical} issue(s) CRITIQUE(S)")
        sys.exit(1)
    else:
        print(f"\n✅ Simulation terminée — {len(ISSUES)} issue(s) mineures")
        sys.exit(0)


if __name__ == "__main__":
    main()
