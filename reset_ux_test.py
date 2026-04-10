"""
reset_ux_test.py — Wipe Supabase, garde admin@matheux.fr, crée 4 profils UX test.
Usage: python3 reset_ux_test.py
"""
import hashlib, random, requests
from datetime import date, timedelta
from supabase_helper import sb, _SUPABASE_URL, _SUPABASE_KEY

random.seed(42)
AUTH_URL = f"{_SUPABASE_URL}/auth/v1/admin/users"
AH = {'apikey': _SUPABASE_KEY, 'Authorization': f'Bearer {_SUPABASE_KEY}', 'Content-Type': 'application/json'}

ADMIN_EMAIL = "admin@matheux.fr"
ADMIN_PASS = "Admin123"
TODAY = date.today()

def pwhash(email, password):
    return hashlib.sha256(f"{email}::{password}::AB22".encode()).hexdigest()

def day(offset):
    return (TODAY + timedelta(days=offset)).isoformat()

# ═══ 1. WIPE ═══
print("🧹 Wipe Supabase...")

# 1a. Delete all auth users except admin@matheux.fr (if exists)
users = requests.get(AUTH_URL, headers=AH).json().get('users', [])
for u in users:
    if u.get('email') != ADMIN_EMAIL:
        requests.delete(f"{AUTH_URL}/{u['id']}", headers=AH)
        print(f"  ✖ auth user {u.get('email')}")

# 1b. Delete leftover rows (cascade should handle most but belt-and-braces)
for tbl in ['scores','progress','daily_boosts','suivi','brevet_results','insights','emails']:
    try:
        sb.delete(tbl, {'id': 'gte.0'})
        print(f"  ✖ {tbl}")
    except Exception as e:
        print(f"  ⚠ {tbl}: {e}")

# 1c. Delete profiles except admin
sb.delete('profiles', {'email': f'neq.{ADMIN_EMAIL}'})
print(f"  ✖ profiles (non-admin)")

# ═══ 2. ADMIN ═══
print(f"\n👑 Admin {ADMIN_EMAIL}...")
users = requests.get(AUTH_URL, headers=AH).json().get('users', [])
admin_uid = next((u['id'] for u in users if u.get('email') == ADMIN_EMAIL), None)
if admin_uid:
    # Reset password
    requests.put(f"{AUTH_URL}/{admin_uid}", headers=AH, json={'password': ADMIN_PASS, 'email_confirm': True})
    print(f"  🔄 password reset")
else:
    r = requests.post(AUTH_URL, headers=AH, json={'email': ADMIN_EMAIL, 'password': ADMIN_PASS, 'email_confirm': True})
    admin_uid = r.json()['id']
    print(f"  ✅ auth créé")

existing_admin = sb.read_one('profiles', filters={'email': f'eq.{ADMIN_EMAIL}'})
admin_row = {
    'id': admin_uid, 'code': 'ADMIN1', 'prenom': 'Admin', 'niveau': '3EME',
    'email': ADMIN_EMAIL, 'password_hash': pwhash(ADMIN_EMAIL, ADMIN_PASS),
    'date_inscription': day(-30), 'is_admin': True, 'premium': True,
    'premium_end': '2027-06-30', 'is_test': False,
}
if existing_admin:
    sb.update('profiles', {'email': f'eq.{ADMIN_EMAIL}'}, admin_row)
else:
    sb.insert('profiles', admin_row)
print(f"  ✅ profile admin OK")

# ═══ 3. 4 TEST USERS ═══

CHAPS_3EME = [
    'Fractions_Brevet', 'Equations_Brevet', 'Calcul_Litteral_Brevet',
    'Pythagore_Brevet', 'Thales_Brevet', 'Trigonometrie_Brevet',
    'Fonctions_Brevet', 'Proportionnalite_Brevet', 'Puissances_Brevet',
    'Statistiques_Brevet',
]

def rand_score_row(code, prenom, chap, num, result, d, source=''):
    return {
        'code': code, 'prenom': prenom, 'niveau': '3EME',
        'chapitre': chap, 'num_exo': num,
        'enonce': f'Exo {num} test {chap}',
        'resultat': result, 'temps_sec': random.randint(20, 180),
        'nb_indices': 0 if result == 'EASY' else random.randint(1, 3),
        'formule_vue': result == 'HARD',
        'date': d, 'source': source,
    }

def plant_chapter(code, prenom, chap, nb_exos, score_pct, base_day=0):
    """Génère nb_exos scores sur un chapitre avec score_pct% EASY, étalés sur 3 jours."""
    rows = []
    nb_easy = int(nb_exos * score_pct / 100)
    results = ['EASY'] * nb_easy + ['HARD'] * (nb_exos - nb_easy)
    random.shuffle(results)
    for i, r in enumerate(results):
        d = day(base_day - (i // 7))  # étalé sur plusieurs jours
        rows.append(rand_score_row(code, prenom, chap, i+1, r, d))
    return rows

TEST_USERS = [
    {
        'email': 'test@test.fr1', 'code': 'TST001', 'prenom': 'Léa',
        'premium': False, 'free_chapter': 'Fractions_Brevet',
        'desc': 'Free — 1 chapitre gratuit terminé (80%) + 1 nouveau entamé (6 exos)',
        'plant': lambda c,p: (
            plant_chapter(c, p, 'Fractions_Brevet', 20, 80, base_day=-2) +
            plant_chapter(c, p, 'Equations_Brevet', 6, 50, base_day=0)
        ),
        'boost_today': False,
    },
    {
        'email': 'test@test.fr2', 'code': 'TST002', 'prenom': 'Tom',
        'premium': False, 'free_chapter': 'Equations_Brevet',
        'desc': 'Free — post-diag frais, aucun exo fait',
        'plant': lambda c,p: [],
        'boost_today': False,
    },
    {
        'email': 'test@test.fr3', 'code': 'TST003', 'prenom': 'Mia',
        'premium': True, 'free_chapter': None,
        'desc': 'Full — 3 chapitres avancés, streak 4j, boost du jour fait',
        'plant': lambda c,p: (
            plant_chapter(c, p, 'Fractions_Brevet', 20, 70, base_day=-3) +
            plant_chapter(c, p, 'Pythagore_Brevet', 18, 65, base_day=-2) +
            plant_chapter(c, p, 'Equations_Brevet', 12, 55, base_day=0)
        ),
        'boost_today': True,
    },
    {
        'email': 'test@test.fr4', 'code': 'TST004', 'prenom': 'Eli',
        'premium': True, 'free_chapter': None,
        'desc': 'Full heavy — 5 chapitres dont 2 terminés, streak 6j, gros XP',
        'plant': lambda c,p: (
            plant_chapter(c, p, 'Fractions_Brevet', 20, 85, base_day=-5) +
            plant_chapter(c, p, 'Calcul_Litteral_Brevet', 20, 75, base_day=-4) +
            plant_chapter(c, p, 'Thales_Brevet', 16, 70, base_day=-3) +
            plant_chapter(c, p, 'Pythagore_Brevet', 14, 60, base_day=-2) +
            plant_chapter(c, p, 'Fonctions_Brevet', 10, 50, base_day=0)
        ),
        'boost_today': True,
    },
]

print(f"\n👥 Création des 4 profils test...")

all_scores = []
all_progress = []
all_boosts = []

for u in TEST_USERS:
    email, code, prenom = u['email'], u['code'], u['prenom']
    # Auth create
    r = requests.post(AUTH_URL, headers=AH, json={'email': email, 'password': 'test123', 'email_confirm': True})
    if r.status_code not in (200, 201):
        print(f"  ⚠ auth {email}: {r.status_code} {r.text[:100]}")
        continue
    uid = r.json()['id']

    profile_row = {
        'id': uid, 'code': code, 'prenom': prenom, 'niveau': '3EME',
        'email': email, 'password_hash': pwhash(email, 'test123'),
        'date_inscription': day(-10), 'is_admin': False,
        'premium': u['premium'], 'is_test': True,
        'free_chapter': u['free_chapter'],
    }
    if u['premium']:
        profile_row['premium_end'] = '2026-06-30'
    else:
        profile_row['trial_start'] = day(-10)

    sb.insert('profiles', profile_row)
    print(f"  ✅ {code} {prenom} ({email}) — {u['desc']}")

    # Scores
    scores = u['plant'](code, prenom)
    all_scores.extend(scores)

    # Progress par chapitre
    by_chap = {}
    for s in scores:
        by_chap.setdefault(s['chapitre'], []).append(s)
    for chap, rows in by_chap.items():
        nb_easy = sum(1 for s in rows if s['resultat'] == 'EASY')
        nb_exos = len(rows)
        score_conf = int(nb_easy / nb_exos * 100) if nb_exos else 0
        all_progress.append({
            'code': code, 'niveau': '3EME', 'categorie': chap,
            'score': score_conf, 'nb_exos': nb_exos,
            'nb_erreurs': nb_exos - nb_easy,
            'derniere_pratique': max(s['date'] for s in rows),
            'statut': 'maitrise' if nb_exos >= 20 and score_conf >= 75 else 'en_cours',
            'streak': random.randint(2, 6) if u['premium'] else 0,
        })

    # Boost du jour
    if u['boost_today']:
        all_boosts.append({
            'code': code, 'date': day(0),
            'boost_json': {
                'insight': f'Boost ciblé pour {prenom}.',
                'exos': [{'q': f'Exo boost {i}', 'a': 'x', 'options': [], 'f': '', 'steps': []} for i in range(5)]
            },
            'exos_done': 5,
        })

# ═══ 4. BULK INSERT ═══
if all_scores:
    # Chunk by 100 to avoid payload limits
    for i in range(0, len(all_scores), 100):
        sb.insert('scores', all_scores[i:i+100])
    print(f"\n  ✅ {len(all_scores)} scores insérés")

for p in all_progress:
    sb.insert('progress', p)
print(f"  ✅ {len(all_progress)} progress insérées")

for b in all_boosts:
    sb.insert('daily_boosts', b)
print(f"  ✅ {len(all_boosts)} daily_boosts insérés")

print(f"\n═══════════════════════════════════════")
print(f"✅ RESET TERMINÉ")
print(f"═══════════════════════════════════════")
print(f"Admin : {ADMIN_EMAIL} / {ADMIN_PASS}")
for u in TEST_USERS:
    print(f"  • {u['email']} / test123 — {u['prenom']} — {u['desc']}")
