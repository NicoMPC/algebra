#!/usr/bin/env python3
"""
check_students.py — Health check données élèves (Supabase)
==========================================================
Vérifie la cohérence des données de TOUS les vrais élèves.
5 checks, 30 secondes, vert ou rouge.

Usage : python3 check_students.py
"""

from supabase_helper import sb
from collections import defaultdict
import json, sys

OK = 0
FAIL = 0

def check(cond, label):
    global OK, FAIL
    if cond:
        OK += 1
    else:
        FAIL += 1
        print(f"  ❌ {label}")

def warn(label):
    print(f"  ⚠️  {label}")

# ── Charger les données ──────────────────────────────────────

print("🔍 Chargement des données Supabase...")
profiles = sb.get_profiles(test=False, admin=False)
scores = sb.get_scores()
boosts = sb.read('daily_boosts')
suivi = sb.get_suivi()

print(f"📋 {len(profiles)} élèves à vérifier\n")

for user in profiles:
    code = user.get('code', '')
    name = user.get('prenom', '?')
    level = user.get('niveau', '')
    email = user.get('email', '')

    print(f"── {name} ({code}) {'─' * max(1, 40 - len(name) - len(code))}")

    # ── CHECK 1 : Champs critiques ──
    check(bool(code), "Code manquant")
    check(bool(level), "Niveau manquant")
    check(bool(email), "Email manquant")

    # ── CHECK 2 : Doublons scores ──
    my_scores = [s for s in scores if s.get('code') == code]
    seen = set()
    dupes = 0
    for s in my_scores:
        key = (s.get('code'), s.get('chapitre'), s.get('num_exo'), s.get('date'), s.get('source'))
        if key in seen:
            dupes += 1
        seen.add(key)
    check(dupes == 0, f"{dupes} doublon(s) dans Scores")

    # ── CHECK 3 : Suivi cohérent ──
    my_suivi = next((s for s in suivi if s.get('code') == code), None)
    if my_suivi:
        # Vérifier que les chapitres assignés sont valides
        for slot in ['chap1', 'chap2', 'chap3', 'chap4']:
            chap_data = my_suivi.get(slot)
            if chap_data:
                if isinstance(chap_data, str):
                    try:
                        chap_data = json.loads(chap_data)
                    except:
                        check(False, f"Suivi {slot}: JSON invalide")
                        continue
                if isinstance(chap_data, dict):
                    cat = chap_data.get('categorie', chap_data.get('chapter', ''))
                    if cat:
                        # Compter les scores curriculum pour ce chapitre
                        chap_scores = [s for s in my_scores
                                       if s.get('chapitre') == cat
                                       and s.get('source') not in ('BOOST', 'CALIBRAGE')]
                        # Info (pas un check bloquant)
                        print(f"  📝 {slot}: {cat} — {len(chap_scores)} scores curriculum")
    else:
        warn("Pas de ligne Suivi")

    # ── CHECK 4 : Boost cohérent ──
    my_boosts = [b for b in boosts if b.get('code') == code]
    for b in my_boosts:
        exos_done = b.get('exos_done', 0) or 0
        boost_date = b.get('date', '')
        if exos_done > 0:
            boost_scores = [s for s in my_scores
                           if s.get('source') == 'BOOST' and s.get('date') == boost_date]
            # ExosDone peut être >= nombre de scores BOOST si rattrapage
            if len(boost_scores) == 0:
                all_boost_scores = [s for s in my_scores if s.get('source') == 'BOOST']
                check(len(all_boost_scores) >= exos_done,
                      f"Boost {boost_date}: ExosDone={exos_done} mais {len(all_boost_scores)} scores BOOST total")

    # ── CHECK 5 : Progress cohérent ──
    progress = sb.read('progress', filters={'code': f'eq.{code}'})
    for p in progress:
        cat = p.get('categorie', '')
        nb_exos = p.get('nb_exos', 0)
        actual = len([s for s in my_scores
                      if s.get('chapitre') == cat
                      and s.get('source') not in ('BOOST', 'CALIBRAGE')])
        check(nb_exos == actual,
              f"Progress {cat}: nb_exos={nb_exos} vs Scores réels={actual}")

    # Résumé élève
    non_calib = [s for s in my_scores if s.get('source') not in ('CALIBRAGE',)]
    print(f"  📊 {len(my_scores)} scores ({len(non_calib)} hors calibrage), {len(my_boosts)} boost(s)")
    print()

# ── Verdict ──────────────────────────────────────────────────

print("=" * 50)
if FAIL == 0:
    print(f"✅ TOUT EST PROPRE — {OK} checks OK, 0 problème")
else:
    print(f"⚠️  {FAIL} PROBLÈME(S) DÉTECTÉ(S) — {OK} OK, {FAIL} KO")
print("=" * 50)

sys.exit(0 if FAIL == 0 else 1)
