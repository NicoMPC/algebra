#!/usr/bin/env python3
"""
fix_lucas_ines.py — Ajuste les états de Lucas et Inès pour la démo admin.

Lucas (F3P5ZW, 5EME) :
  État actuel → BOOST TERMINÉ (boost J+1 exosDone=5)
  Cible       → CHAPITRE TERMINÉ seulement (NbExos ≥20, boost in-progress 2/5)

Inès  (8VCMMQ, 3EME) :
  État actuel → RAS (inactive simulée mais save_score récent)
  Cible       → BOOST TERMINÉ + CHAPITRE TERMINÉ (les deux pills)
"""

import json, hashlib, time, random, urllib.request, sys

GAS_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF/exec"
)

random.seed(99)


def sha256_hash(email, password):
    return hashlib.sha256(f"{email.lower().strip()}::{password}::AB22".encode()).hexdigest()


def gas(payload, label="", retry=2):
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        GAS_URL, data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    for attempt in range(retry + 1):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                d = json.loads(r.read().decode("utf-8"))
                status = d.get("status", "?")
                ok = "✅" if status == "success" else "❌"
                msg = d.get("message", "")
                print(f"  {ok} {label}: {status}" +
                      (f" ({msg})" if status != "success" and msg else ""))
                return d
        except Exception as e:
            if attempt < retry:
                print(f"  ⚠️  retry {attempt+1}: {e}")
                time.sleep(2)
            else:
                print(f"  ❌ ERREUR finale: {e}")
                return {}
    return {}


def get_active_chapter(code):
    """
    Récupère le chapitre le plus travaillé depuis get_progress.
    Exclut CALIBRAGE et BOOST.
    Retourne (categorie, nbExos) ou (None, 0).
    """
    r = gas({"action": "get_progress", "code": code}, f"get_progress")
    progress = r.get("progress", [])
    if not progress:
        # Fallback: essayer le champ 'chapitres' ou 'data'
        progress = r.get("chapitres", r.get("data", []))

    best_cat, best_nb = None, 0
    for p in progress:
        cat = p.get("categorie", p.get("chapitre", p.get("category", "")))
        nb  = int(p.get("nbExos", p.get("nb_exos", p.get("total", 0))) or 0)
        if cat and cat not in ("CALIBRAGE", "BOOST", "") and nb > best_nb:
            best_nb  = nb
            best_cat = cat

    return best_cat, best_nb


def add_chapter_exos(code, name, level, categorie, start_idx, nb_exos, hard_rate=0.2):
    """
    Ajoute des exercices de chapitre avec indices uniques (start_idx + i).
    Utilise des indices élevés (50+) pour éviter tout conflit avec les exos existants.
    """
    for i in range(nb_exos):
        resultat = "HARD" if random.random() < hard_rate else "EASY"
        gas({
            "action":       "save_score",
            "code":         code,
            "name":         name,
            "level":        level,
            "categorie":    categorie,
            "exercice_idx": start_idx + i,
            "resultat":     resultat,
            "q":            f"Exercice {start_idx + i + 1} — {categorie[:28]}",
            "time":         random.randint(20, 60),
            "source":       "chapter"
        }, f"ch_exo idx={start_idx+i} ({resultat})")
        time.sleep(0.35)


def do_boost_partial(code, level, errors, nb_exos_to_do):
    """
    Génère un nouveau boost et fait nb_exos_to_do exercices dessus.
    Retourne le boost généré (ou {} si erreur).
    """
    r = gas({
        "action": "generate_daily_boost",
        "code":   code,
        "level":  level,
        "errors": errors[:3]
    }, "generate_daily_boost")

    boost      = r.get("boost", {})
    boost_exos = boost.get("exos", [])
    nb         = len(boost_exos)
    print(f"  → {nb} exos dans le boost ({boost.get('categorie', '?')})")

    if not boost_exos:
        print("  ⚠️  Boost vide — vérifier generate_daily_boost")
        return {}

    for i in range(min(nb_exos_to_do, nb)):
        gas({
            "action": "save_boost",
            "code":   code,
            "boost":  boost,
            "exoIdx": i
        }, f"save_boost Q{i+1}")
        time.sleep(0.35)

    return boost


# ══════════════════════════════════════════════════════════════════════════════
# FIX 1 — LUCAS (F3P5ZW) → CHAPITRE TERMINÉ seulement
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "═" * 60)
print("🔧  FIX 1 — Lucas Martin (5EME) → CHAPITRE TERMINÉ seulement")
print("═" * 60)

LUCAS_EMAIL = "lucas.martin.2026@gmail.com"
LUCAS_PASS  = "Lucas2026!"
LUCAS_CODE  = "F3P5ZW"

# Étape 1 — Détection état actuel
print("\n  [1/4] Détection du chapitre actif…")
cat_l, nb_l = get_active_chapter(LUCAS_CODE)
print(f"  → Chapitre : {cat_l or 'non détecté'} ({nb_l} exos)")

if not cat_l:
    print("  ⚠️  Aucun chapitre détecté — on utilisera 'Fractions' 5EME par défaut")
    cat_l = "Fractions"
    nb_l  = 0

# Étape 2 — Compléter le chapitre à ≥ 20 exos (idx 50+)
needed_l = max(0, 20 - nb_l)
print(f"\n  [2/4] Ajout de {needed_l} exos pour atteindre 20 (idx 50→{49+needed_l})…")
if needed_l > 0:
    add_chapter_exos(LUCAS_CODE, "Lucas Martin", "5EME", cat_l,
                     start_idx=50, nb_exos=needed_l, hard_rate=0.15)
else:
    print("  → Déjà ≥ 20 exos — rien à faire")

# Étape 3 — Reset boost : simulate_next_day
print(f"\n  [3/4] Reset boost (simulate_next_day)…")
gas({"action": "simulate_next_day", "code": LUCAS_CODE}, "simulate_next_day Lucas")
time.sleep(0.6)

# Étape 4 — Nouveau boost in-progress (2/5, pas BOOST TERMINÉ)
print(f"\n  [4/4] Nouveau boost in-progress (2/5)…")
do_boost_partial(LUCAS_CODE, "5EME", [cat_l], nb_exos_to_do=2)

print("\n  ✅ Lucas → CHAPITRE TERMINÉ ✓ | Boost en cours 2/5 (pas d'action boost)")


# ══════════════════════════════════════════════════════════════════════════════
# FIX 2 — INÈS (8VCMMQ) → BOOST TERMINÉ + CHAPITRE TERMINÉ
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "═" * 60)
print("🔧  FIX 2 — Inès Dupont (3EME) → BOOST TERMINÉ + CHAPITRE TERMINÉ")
print("═" * 60)

INES_EMAIL = "ines.dupont.2026@gmail.com"
INES_PASS  = "Ines2026!"
INES_CODE  = "8VCMMQ"

# Étape 1 — Détection
print("\n  [1/4] Détection du chapitre actif…")
cat_i, nb_i = get_active_chapter(INES_CODE)
print(f"  → Chapitre : {cat_i or 'non détecté'} ({nb_i} exos)")

if not cat_i:
    # Inès n'a que des exos CALIBRAGE → on lui attribue le premier chapitre 3EME
    print("  ⚠️  Que du CALIBRAGE — on cherche via login pour récupérer un chapitre…")
    r_login = gas({
        "action":   "login",
        "email":    INES_EMAIL,
        "password": sha256_hash(INES_EMAIL, INES_PASS)
    }, "login Inès fallback")
    # Essayer d'extraire un chapitre diagnostiqué
    diag = r_login.get("profile", {}).get("chapitresDiag", [])
    if diag:
        cat_i = diag[0]
    else:
        cat_i = "Calcul littéral"  # fallback 3EME
    nb_i = 0
    print(f"  → Chapitre utilisé : {cat_i}")

# Étape 2 — Compléter chapitre à ≥ 20 exos (idx 50+)
needed_i = max(0, 20 - nb_i)
print(f"\n  [2/4] Ajout de {needed_i} exos pour atteindre 20 (idx 50→{49+needed_i})…")
if needed_i > 0:
    add_chapter_exos(INES_CODE, "Inès Dupont", "3EME", cat_i,
                     start_idx=50, nb_exos=needed_i, hard_rate=0.40)  # Inès a du mal
else:
    print("  → Déjà ≥ 20 exos — rien à faire")

# Étape 3 — Reset boost : simulate_next_day
print(f"\n  [3/4] Reset boost (simulate_next_day)…")
gas({"action": "simulate_next_day", "code": INES_CODE}, "simulate_next_day Inès")
time.sleep(0.6)

# Étape 4 — Nouveau boost COMPLET (5/5 → BOOST TERMINÉ)
print(f"\n  [4/4] Boost complet (5/5) → BOOST TERMINÉ…")
do_boost_partial(INES_CODE, "3EME", [cat_i], nb_exos_to_do=5)

print("\n  ✅ Inès → CHAPITRE TERMINÉ ✓ | BOOST TERMINÉ ✓")


# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "═" * 60)
print("✅  Fix terminé — vérifier dans le panel admin (triple-clic logo)")
print("   → Lucas : onglet 'À faire' → CHAPITRE TERMINÉ seulement")
print("   → Inès  : onglet 'À faire' → BOOST TERMINÉ + CHAPITRE TERMINÉ (2 pills)")
print("═" * 60 + "\n")
