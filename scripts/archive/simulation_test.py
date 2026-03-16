#!/usr/bin/env python3
"""
simulation_test.py — Test de simulation complet Matheux
Simule 10 profils test sur l'ensemble des workflows.
Ne modifie aucun fichier source.
Usage : python3 scripts/simulation_test.py
"""
import hashlib, json, os, sys, time, random
import requests
from datetime import datetime, date, timedelta
from google.oauth2.service_account import Credentials
import gspread

# ── Config ──────────────────────────────────────────────────────────────────
GAS_URL  = 'https://script.google.com/macros/s/AKfycbxGnWv7VilZ3_n7rZRNwT45jdTrTh6SlHq62SkS1a3M6_sxxh6s4-_7wHfDvHq1cLkF/exec'
SHEET_ID = '1SiE3lHf9dAKbExWPGNrk5cbLhDbKUKM4xvd1Th1frY4'
SA_FILE  = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'algebreboost-sheets-2595a71cadfb.json')
SCOPES   = ['https://www.googleapis.com/auth/spreadsheets']
PASSWORD = 'SimTest2026!'

# ── Helpers ─────────────────────────────────────────────────────────────────
call_log = []
start_time = time.time()

def sha256_hash(email, password):
    s = email.lower() + '::' + password + '::AB22'
    return hashlib.sha256(s.encode()).hexdigest()

def gas(action, payload, label=''):
    """POST to GAS, log result, return parsed JSON or None."""
    data = {'action': action, **payload}
    t0 = time.time()
    try:
        # GAS reads JSON.parse(e.postData.contents) — send as text/plain JSON body
        # NEVER set Content-Type: application/json (CORS issue with GAS)
        # GAS POST returns 302 → follow as GET (default requests behavior)
        r = requests.post(GAS_URL, data=json.dumps(data), timeout=30)
        dt = int((time.time() - t0) * 1000)
        try:
            j = r.json()
        except Exception:
            j = {'status': 'error', 'message': f'Non-JSON response: {r.text[:200]}'}
        status = j.get('status', '?')
        tag = '✅' if status == 'success' else '❌'
        msg = j.get('message', '')
        print(f'  {tag} [{dt}ms] {label or action} → {status}' + (f' ({msg})' if msg and status != 'success' else ''))
        call_log.append({'action': action, 'label': label, 'status': status, 'dt': dt})
        time.sleep(1.5)
        return j
    except Exception as e:
        dt = int((time.time() - t0) * 1000)
        print(f'  💥 [{dt}ms] {label or action} → EXCEPTION: {e}')
        call_log.append({'action': action, 'label': label, 'status': 'exception', 'dt': dt})
        time.sleep(1.5)
        return None

# ── Profiles ────────────────────────────────────────────────────────────────
PROFILES = [
    {'id': 'SIM01', 'prenom': 'Lucas',  'email': 'lucas.sim01@sim.matheux.fr',  'niveau': '6EME',  'chapitres_diag': ['Fractions', 'Proportionnalite'],          'objectif': 'lacunes',        'scenario': 'parcours_complet',  'jours_simules': 0,  'description': 'Élève standard J0 — tout le workflow de bienvenue'},
    {'id': 'SIM02', 'prenom': 'Emma',   'email': 'emma.sim02@sim.matheux.fr',   'niveau': '5EME',  'chapitres_diag': ['Nombres_relatifs', 'Puissances'],          'objectif': 'chapitre_jour',  'scenario': 'j3_email_due',      'jours_simules': 3,  'description': 'J+3 — email de relance doit apparaître dans admin'},
    {'id': 'SIM03', 'prenom': 'Hugo',   'email': 'hugo.sim03@sim.matheux.fr',   'niveau': '4EME',  'chapitres_diag': ['Equations', 'Fonctions_Lineaires'],        'objectif': 'brevet',         'scenario': 'j7_conversion',     'jours_simules': 7,  'description': 'J+7 — email de conversion avec lien Stripe'},
    {'id': 'SIM04', 'prenom': 'Lea',    'email': 'lea.sim04@sim.matheux.fr',    'niveau': '3EME',  'chapitres_diag': ['Trigonometrie', 'Probabilites'],            'objectif': 'brevet',         'scenario': 'boost_complete',    'jours_simules': 1,  'description': 'Boost terminé → action admin déclenchée'},
    {'id': 'SIM05', 'prenom': 'Nathan', 'email': 'nathan.sim05@sim.matheux.fr', 'niveau': '6EME',  'chapitres_diag': ['Nombres_entiers', 'Angles'],               'objectif': 'toutes_matieres','scenario': 'chapitre_termine',  'jours_simules': 2,  'description': 'Chapitre terminé (20 exos) → action admin'},
    {'id': 'SIM06', 'prenom': 'Chloe',  'email': 'chloe.sim06@sim.matheux.fr',  'niveau': '1ERE',  'chapitres_diag': ['Second_Degre', 'Derivation'],              'objectif': 'lacunes',        'scenario': 'inactif',           'jours_simules': 10, 'description': 'Inactif >7j → statut "Sans nouvelles" dans admin'},
    {'id': 'SIM07', 'prenom': 'Tom',    'email': 'tom.sim07@sim.matheux.fr',    'niveau': '3EME',  'chapitres_diag': ['Calcul_Litteral', 'Systemes_Equations'],    'objectif': 'brevet',         'scenario': 'brevet_pending',    'jours_simules': 4,  'description': 'Brevet blanc publié → visible côté élève au login'},
    {'id': 'SIM08', 'prenom': 'Sofia',  'email': 'sofia.sim08@sim.matheux.fr',  'niveau': '5EME',  'chapitres_diag': ['Calcul_Litteral', 'Pythagore'],             'objectif': 'chapitre_jour',  'scenario': 'cours_milestone',   'jours_simules': 1,  'description': 'Milestone 5 exos → cours disponible ou "en préparation"'},
    {'id': 'SIM09', 'prenom': 'Remi',   'email': 'remi.sim09@sim.matheux.fr',   'niveau': '4EME',  'chapitres_diag': ['Puissances', 'Inequations'],               'objectif': 'lacunes',        'scenario': 'boost_en_cours',    'jours_simules': 0,  'description': 'Boost en cours 2/5 → admin voit "En cours" pas "Terminé"'},
    {'id': 'SIM10', 'prenom': 'Jade',   'email': 'jade.sim10@sim.matheux.fr',   'niveau': '6EME',  'chapitres_diag': ['Symetrie_Axiale', 'Volumes'],              'objectif': 'toutes_matieres','scenario': 'j5_email_due',      'jours_simules': 5,  'description': 'J+5 — email urgence avant fin de trial'},
]

# ── Results tracking ────────────────────────────────────────────────────────
results = {}  # id → {status, frictions, details}
frictions_critiques = []
frictions_jaunes = []
verifs_ok = []
edge_results = []
sheet_checks = []

def friction(level, msg, profil=''):
    entry = f'[{profil}] {msg}' if profil else msg
    if level == 'rouge':
        frictions_critiques.append(entry)
    else:
        frictions_jaunes.append(entry)

def ok(msg):
    verifs_ok.append(msg)


def main():
    global ADMIN_CODE

    print('═' * 60)
    print('  SIMULATION MATHEUX — 10 profils test')
    print('═' * 60)

    # ── Phase 0: Setup ──────────────────────────────────────────────────
    print('\n▶ PHASE 0 — Setup')

    creds = Credentials.from_service_account_file(SA_FILE, scopes=SCOPES)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(SHEET_ID)
    users_ws = sh.worksheet('Users')

    # 0A — Get admin code
    users_data = users_ws.get_all_values()
    header = users_data[0]
    col = {h: i for i, h in enumerate(header)}
    ADMIN_CODE = None
    for row in users_data[1:]:
        if row[col.get('IsAdmin', -1)].strip().upper() in ('1', 'TRUE', 'OUI'):
            ADMIN_CODE = row[col['Code']]
            break
    if not ADMIN_CODE:
        print('❌ Aucun admin trouvé dans Users → arrêt')
        sys.exit(1)
    print(f'  🔑 Admin code: {ADMIN_CODE}')

    # 0D — Cleanup old sim profiles
    print('  🧹 Nettoyage anciens profils @sim.matheux.fr...')
    email_col_idx = col['Email']
    rows_to_delete = []
    for i, row in enumerate(users_data[1:], start=2):
        if '@sim.matheux.fr' in row[email_col_idx]:
            rows_to_delete.append(i)
    if rows_to_delete:
        # Delete from bottom to preserve indices
        for row_idx in sorted(rows_to_delete, reverse=True):
            users_ws.delete_rows(row_idx)
        print(f'  🗑  {len(rows_to_delete)} anciens profils supprimés')
        # Also clean Scores, DailyBoosts, Progress, Suivi, Emails for sim emails
        for sheet_name in ['Scores', 'DailyBoosts', 'Progress']:
            try:
                ws = sh.worksheet(sheet_name)
                all_vals = ws.get_all_values()
                if len(all_vals) <= 1:
                    continue
                sh_header = all_vals[0]
                code_ci = next((i for i, h in enumerate(sh_header) if h == 'Code'), None)
                if code_ci is None:
                    continue
                # Collect sim codes from deleted users
                sim_codes = set()
                for ri in rows_to_delete:
                    if ri - 1 < len(users_data):
                        sim_codes.add(users_data[ri - 1][col['Code']])
                del_rows = []
                for i, r in enumerate(all_vals[1:], start=2):
                    if r[code_ci] in sim_codes:
                        del_rows.append(i)
                for ri in sorted(del_rows, reverse=True):
                    ws.delete_rows(ri)
                if del_rows:
                    print(f'    🗑  {len(del_rows)} lignes nettoyées dans {sheet_name}')
            except Exception as e:
                print(f'    ⚠ Nettoyage {sheet_name}: {e}')
        time.sleep(2)
    else:
        print('  (aucun ancien profil)')

    # ── Phase 1+2: Register & run scenarios ─────────────────────────────
    codes = {}  # id → code

    print('\n▶ PHASE 2 — Inscription et scénarios')

    for prof in PROFILES:
        pid = prof['id']
        print(f'\n── {pid} {prof["prenom"]} ({prof["niveau"]}) — {prof["description"]}')
        results[pid] = {'status': '?', 'frictions': [], 'details': {}}

        # ÉTAPE A — Inscription
        pw_hash = sha256_hash(prof['email'], PASSWORD)
        r = gas('register', {
            'name': prof['prenom'],
            'email': prof['email'],
            'level': prof['niveau'],
            'password': pw_hash,
            'objectif': prof['objectif'],
            'test': True
        }, f'{pid} register')

        if not r or r.get('status') != 'success':
            results[pid]['status'] = '❌ inscription échouée'
            if r and r.get('status') == 'waitlist':
                friction('rouge', 'Inscription en waitlist — limite 50 atteinte?', pid)
            else:
                friction('rouge', f'Inscription échouée: {r}', pid)
            continue

        code = r.get('profile', {}).get('code', '')
        if not code or len(code) != 6:
            friction('rouge', f'Code invalide retourné: {code}', pid)
            results[pid]['status'] = '❌ code invalide'
            continue
        codes[pid] = code
        ok(f'{pid} inscription OK → {code}')

        # ÉTAPE B — Diagnostic
        r = gas('generate_diagnostic', {
            'level': prof['niveau'],
            'selectedChapters': prof['chapitres_diag']
        }, f'{pid} diagnostic')

        diag_exos = []
        if r and r.get('status') == 'success':
            diag_exos = r.get('exos', [])
            if not diag_exos:
                friction('jaune', 'Diagnostic retourne 0 exos', pid)
            else:
                # Validate exo structure
                for i, exo in enumerate(diag_exos[:4]):
                    if not all(k in exo for k in ('q', 'a', 'options')):
                        friction('jaune', f'Exo diag {i} manque q/a/options', pid)
                    elif exo['a'] not in exo['options']:
                        friction('rouge', f'Exo diag {i}: réponse absente des options', pid)
                ok(f'{pid} diagnostic OK — {len(diag_exos)} exos')
        else:
            friction('jaune', f'Diagnostic échoué: {r}', pid)

        # ÉTAPE C — Simuler réponses diagnostic (max 4)
        for idx, exo in enumerate(diag_exos[:4]):
            resultat = 'HARD' if idx % 2 == 0 else 'EASY'
            wrong = ''
            if resultat == 'HARD' and exo.get('options'):
                opts = [o for o in exo['options'] if o != exo.get('a')]
                wrong = opts[0] if opts else ''
            gas('save_score', {
                'code': code,
                'name': prof['prenom'],
                'level': prof['niveau'],
                'categorie': 'CALIBRAGE',
                'exercice_idx': str(idx),
                'resultat': resultat,
                'time': '45',
                'indices': '1' if resultat == 'HARD' else '0',
                'formule': 'false',
                'wrongOpt': wrong,
                'source': 'CALIBRAGE'
            }, f'{pid} save_score diag {idx}')

        # ÉTAPE D — Boost initial
        r = gas('generate_daily_boost', {
            'code': code,
            'level': prof['niveau'],
            'chapters': prof['chapitres_diag']
        }, f'{pid} generate_boost')

        boost_exos = []
        if r and r.get('status') == 'success':
            boost = r.get('boost', {})
            boost_exos = boost.get('exos', [])
            if not boost_exos or len(boost_exos) != 5:
                friction('jaune', f'Boost retourne {len(boost_exos)} exos au lieu de 5', pid)
            if not boost.get('insight'):
                friction('jaune', 'Boost sans insight', pid)
            for i, exo in enumerate(boost_exos):
                if exo.get('a') and exo.get('options') and exo['a'] not in exo['options']:
                    friction('rouge', f'Boost exo {i}: réponse absente des options', pid)
            ok(f'{pid} boost OK — {len(boost_exos)} exos')
        else:
            friction('jaune', f'Boost échoué: {r}', pid)

        # ÉTAPE E — Décalage temporel
        if prof['jours_simules'] > 0:
            trial_start = (date.today() - timedelta(days=prof['jours_simules'])).strftime('%Y-%m-%d')
            # Re-read users to find row
            users_data = users_ws.get_all_values()
            for i, row in enumerate(users_data[1:], start=2):
                if row[col['Code']] == code:
                    trial_col = col.get('TrialStart', col.get('TrialStart'))
                    users_ws.update_cell(i, trial_col + 1, trial_start)
                    # Also update DateInscription
                    date_col = col.get('DateInscription')
                    if date_col is not None:
                        users_ws.update_cell(i, date_col + 1, trial_start)
                    print(f'  📅 TrialStart → {trial_start} (J+{prof["jours_simules"]})')
                    break
            time.sleep(1)

        # ÉTAPE F — Scénarios spécifiques
        if prof['scenario'] == 'parcours_complet':
            # SIM01: save 5 boost scores
            for i in range(min(5, len(boost_exos))):
                exo = boost_exos[i]
                gas('save_score', {
                    'code': code, 'name': prof['prenom'], 'level': prof['niveau'],
                    'categorie': prof['chapitres_diag'][i % len(prof['chapitres_diag'])],
                    'exercice_idx': str(i), 'resultat': 'EASY',
                    'time': '30', 'source': 'BOOST'
                }, f'{pid} boost score {i}')
            # Login to verify
            r = gas('login', {
                'email': prof['email'],
                'password': pw_hash
            }, f'{pid} login post-boost')
            if r and r.get('status') == 'success':
                done = r.get('boostExosDone', 0)
                if done >= 5:
                    ok(f'{pid} boostExosDone={done} après 5 scores')
                else:
                    friction('jaune', f'boostExosDone={done} attendu ≥5', pid)
            results[pid]['status'] = '✅'

        elif prof['scenario'] == 'boost_complete':
            # SIM04: save 5 boost scores
            for i in range(min(5, len(boost_exos))):
                gas('save_score', {
                    'code': code, 'name': prof['prenom'], 'level': prof['niveau'],
                    'categorie': prof['chapitres_diag'][i % len(prof['chapitres_diag'])],
                    'exercice_idx': str(i), 'resultat': 'EASY',
                    'time': '25', 'source': 'BOOST'
                }, f'{pid} boost score {i}')
            results[pid]['status'] = '✅'

        elif prof['scenario'] == 'chapitre_termine':
            # SIM05: 20 scores for Nombres_entiers
            chap = prof['chapitres_diag'][0]
            for i in range(20):
                gas('save_score', {
                    'code': code, 'name': prof['prenom'], 'level': prof['niveau'],
                    'categorie': chap,
                    'exercice_idx': str(i),
                    'resultat': random.choice(['EASY', 'MEDIUM']),
                    'time': str(random.randint(20, 60)),
                    'source': ''
                }, f'{pid} curriculum {chap} #{i}')
            results[pid]['status'] = '✅'

        elif prof['scenario'] == 'brevet_pending':
            # SIM07: publish brevet
            r = gas('publish_admin_brevet', {
                'adminCode': ADMIN_CODE,
                'targetCode': code,
                'message': 'Brevet blanc de simulation — teste tes acquis !',
                'chapitres': prof['chapitres_diag']
            }, f'{pid} publish_brevet')
            if r and r.get('status') == 'success':
                ok(f'{pid} brevet publié')
            else:
                friction('jaune', f'publish_brevet échoué: {r}', pid)
            # Login to check pendingBrevet
            r = gas('login', {'email': prof['email'], 'password': pw_hash}, f'{pid} login post-brevet')
            if r and r.get('status') == 'success':
                pb = r.get('pendingBrevet')
                if pb:
                    ok(f'{pid} pendingBrevet présent au login')
                else:
                    friction('jaune', 'pendingBrevet absent au login après publish', pid)
            results[pid]['status'] = '✅'

        elif prof['scenario'] == 'cours_milestone':
            # SIM08: 5 curriculum scores
            chap = prof['chapitres_diag'][0]
            for i in range(5):
                gas('save_score', {
                    'code': code, 'name': prof['prenom'], 'level': prof['niveau'],
                    'categorie': chap,
                    'exercice_idx': str(i),
                    'resultat': 'EASY', 'time': '35', 'source': ''
                }, f'{pid} curriculum {chap} #{i}')
            results[pid]['status'] = '✅'

        elif prof['scenario'] == 'boost_en_cours':
            # SIM09: 2 boost scores only
            for i in range(min(2, len(boost_exos))):
                gas('save_score', {
                    'code': code, 'name': prof['prenom'], 'level': prof['niveau'],
                    'categorie': prof['chapitres_diag'][i % len(prof['chapitres_diag'])],
                    'exercice_idx': str(i), 'resultat': 'EASY',
                    'time': '30', 'source': 'BOOST'
                }, f'{pid} boost score {i}')
            results[pid]['status'] = '✅'

        elif prof['scenario'] in ('j3_email_due', 'j5_email_due', 'j7_conversion', 'inactif'):
            # These just need the time offset (already done)
            results[pid]['status'] = '✅'
        else:
            results[pid]['status'] = '✅'

    # ── Phase 3: Admin overview ─────────────────────────────────────────
    print('\n▶ PHASE 3 — Vérification admin')
    time.sleep(2)
    admin = gas('get_admin_overview', {'adminCode': ADMIN_CODE}, 'admin_overview')

    admin_checks = {}
    if admin and admin.get('status') == 'success':
        users_list = admin.get('users', admin.get('eleves', []))
        # Build lookup by code
        admin_by_code = {}
        for u in users_list:
            c = u.get('code', '')
            admin_by_code[c] = u

        for prof in PROFILES:
            pid = prof['id']
            code = codes.get(pid, '')
            u = admin_by_code.get(code, {})
            admin_checks[pid] = u

            if not u:
                friction('jaune', f'Code {code} absent du admin overview', pid)
                continue

            if prof['scenario'] == 'parcours_complet':
                if u.get('boostExosDone', 0) >= 5 or u.get('boostDone'):
                    ok(f'{pid} admin: boost done')
                else:
                    friction('jaune', f'Admin: boostDone non visible, boostExosDone={u.get("boostExosDone")}', pid)

            elif prof['scenario'] == 'j3_email_due':
                emails_due = u.get('emailsDue', u.get('emailsToSend', []))
                if isinstance(emails_due, str):
                    emails_due = [emails_due]
                if any('3' in str(e) for e in emails_due):
                    ok(f'{pid} admin: J+3 dans emailsDue')
                else:
                    friction('jaune', f'Admin: J+3 absent de emailsDue={emails_due}', pid)

            elif prof['scenario'] == 'j7_conversion':
                emails_due = u.get('emailsDue', u.get('emailsToSend', []))
                if isinstance(emails_due, str):
                    emails_due = [emails_due]
                if any('7' in str(e) for e in emails_due):
                    ok(f'{pid} admin: J+7 dans emailsDue')
                else:
                    friction('jaune', f'Admin: J+7 absent de emailsDue={emails_due}', pid)

            elif prof['scenario'] == 'boost_complete':
                action = str(u.get('actionPriority', u.get('actions', '')))
                if 'BOOST' in action.upper() or 'TERMINÉ' in action.upper() or u.get('boostDone'):
                    ok(f'{pid} admin: boost terminé visible')
                else:
                    friction('jaune', f'Admin: boost terminé non détecté, action={action}', pid)

            elif prof['scenario'] == 'chapitre_termine':
                chaps = u.get('chapitresDetail', u.get('chapitres', {}))
                ok(f'{pid} admin: chapitresDetail présent') if chaps else friction('jaune', 'Admin: chapitresDetail absent', pid)

            elif prof['scenario'] == 'inactif':
                action = str(u.get('actionPriority', u.get('actions', u.get('statut', ''))))
                if any(w in action.lower() for w in ['sans nouvelles', 'bloqué', 'inactif', '💤']):
                    ok(f'{pid} admin: statut inactif détecté')
                else:
                    friction('jaune', f'Admin: statut inactif non détecté, action={action}', pid)

            elif prof['scenario'] == 'brevet_pending':
                pb = u.get('pendingBrevet', u.get('brevet', ''))
                if pb:
                    ok(f'{pid} admin: pendingBrevet visible')
                else:
                    friction('jaune', 'Admin: pendingBrevet absent dans overview', pid)

            elif prof['scenario'] == 'boost_en_cours':
                in_prog = u.get('boostInProgress', u.get('boostExosDone', 0))
                done = u.get('currentBoostExosDone', u.get('boostExosDone', 0))
                if done == 2 or in_prog:
                    ok(f'{pid} admin: boost en cours 2/5 détecté')
                else:
                    friction('jaune', f'Admin: boost en cours non détecté, exosDone={done}', pid)

            elif prof['scenario'] == 'j5_email_due':
                emails_due = u.get('emailsDue', u.get('emailsToSend', []))
                if isinstance(emails_due, str):
                    emails_due = [emails_due]
                if any('5' in str(e) for e in emails_due):
                    ok(f'{pid} admin: J+5 dans emailsDue')
                else:
                    friction('jaune', f'Admin: J+5 absent de emailsDue={emails_due}', pid)
    else:
        friction('rouge', f'get_admin_overview échoué: {admin}')

    # ── Phase 4: Sheet data coherence ───────────────────────────────────
    print('\n▶ PHASE 4 — Cohérence données Sheets')
    time.sleep(1)

    # 4A — Users
    users_data = users_ws.get_all_values()
    header = users_data[0]
    col = {h: i for i, h in enumerate(header)}
    sim_codes = set(codes.values())
    found_codes = set()
    for row in users_data[1:]:
        if row[col['Code']] in sim_codes:
            found_codes.add(row[col['Code']])
            if row[col.get('IsTest', -1)] != '1':
                friction('jaune', f'Users: {row[col["Code"]]} IsTest != 1')
    if found_codes == sim_codes:
        ok(f'Users: {len(found_codes)}/{len(sim_codes)} profils trouvés avec IsTest=1')
        sheet_checks.append(('Users', f'{len(found_codes)} lignes IsTest=1', '✅'))
    else:
        missing = sim_codes - found_codes
        friction('jaune', f'Users: codes manquants: {missing}')
        sheet_checks.append(('Users', f'{len(found_codes)}/{len(sim_codes)} trouvés', '❌'))

    # 4B — Scores
    try:
        scores_ws = sh.worksheet('Scores')
        scores_data = scores_ws.get_all_values()
        if len(scores_data) > 1:
            sh_header = scores_data[0]
            sc_col = {h: i for i, h in enumerate(sh_header)}
            code_ci = sc_col.get('Code', 0)
            source_ci = sc_col.get('Source', sc_col.get('source', -1))
            cat_ci = sc_col.get('Catégorie', sc_col.get('Categorie', sc_col.get('Chapitre', -1)))
            score_counts = {}
            for row in scores_data[1:]:
                c = row[code_ci]
                if c in sim_codes:
                    score_counts[c] = score_counts.get(c, 0) + 1
                    # Check CALIBRAGE source
                    if cat_ci >= 0 and row[cat_ci] == 'CALIBRAGE':
                        if source_ci >= 0 and row[source_ci] != 'CALIBRAGE':
                            friction('jaune', f'Scores: {c} CALIBRAGE avec source={row[source_ci]}')
            total = sum(score_counts.values())
            ok(f'Scores: {total} lignes pour {len(score_counts)} profils sim')
            sheet_checks.append(('Scores', f'{total} scores cohérents', '✅'))
        else:
            sheet_checks.append(('Scores', 'Onglet vide', '⚠'))
    except Exception as e:
        sheet_checks.append(('Scores', f'Erreur: {e}', '❌'))

    # 4C — DailyBoosts
    try:
        boosts_ws = sh.worksheet('DailyBoosts')
        boosts_data = boosts_ws.get_all_values()
        if len(boosts_data) > 1:
            bh = boosts_data[0]
            bc = {h: i for i, h in enumerate(bh)}
            boost_count = 0
            for row in boosts_data[1:]:
                if row[bc.get('Code', 0)] in sim_codes:
                    boost_count += 1
            ok(f'DailyBoosts: {boost_count} entrées sim')
            sheet_checks.append(('DailyBoosts', f'{boost_count} entrées', '✅'))
        else:
            sheet_checks.append(('DailyBoosts', 'Onglet vide', '⚠'))
    except Exception as e:
        sheet_checks.append(('DailyBoosts', f'Erreur: {e}', '❌'))

    # 4F — Progress
    try:
        prog_ws = sh.worksheet('Progress')
        prog_data = prog_ws.get_all_values()
        if len(prog_data) > 1:
            ph = prog_data[0]
            pc = {h: i for i, h in enumerate(ph)}
            sim05_code = codes.get('SIM05', '')
            found_prog = False
            for row in prog_data[1:]:
                if row[pc.get('Code', 0)] == sim05_code:
                    found_prog = True
                    nb = row[pc.get('NbExos', -1)] if pc.get('NbExos', -1) >= 0 else '?'
                    print(f'  Progress SIM05: NbExos={nb}')
            if found_prog:
                ok('Progress: SIM05 entrée trouvée')
                sheet_checks.append(('Progress', 'SIM05 présent', '✅'))
            else:
                friction('jaune', 'Progress: SIM05 absent')
                sheet_checks.append(('Progress', 'SIM05 absent', '❌'))
        else:
            sheet_checks.append(('Progress', 'Onglet vide', '⚠'))
    except Exception as e:
        sheet_checks.append(('Progress', f'Erreur: {e}', '❌'))

    # ── Phase 5: Edge cases ─────────────────────────────────────────────
    print('\n▶ PHASE 5 — Tests de robustesse')

    # 5A — Double inscription
    r = gas('register', {
        'name': 'Lucas', 'email': 'lucas.sim01@sim.matheux.fr',
        'level': '6EME', 'password': sha256_hash('lucas.sim01@sim.matheux.fr', PASSWORD),
        'test': True
    }, 'EDGE double inscription')
    if r and r.get('status') == 'error':
        ok('Double inscription rejetée')
        edge_results.append(('Double inscription', 'error', r.get('status'), '✅'))
    else:
        friction('rouge', f'Double inscription acceptée! → {r}')
        edge_results.append(('Double inscription', 'error', r.get('status') if r else 'null', '❌'))

    # 5B — Mauvais MDP
    r = gas('login', {
        'email': 'emma.sim02@sim.matheux.fr',
        'password': sha256_hash('emma.sim02@sim.matheux.fr', 'MauvaisPass!')
    }, 'EDGE mauvais MDP')
    if r and r.get('status') == 'error':
        ok('Mauvais MDP rejeté')
        edge_results.append(('Mauvais MDP', 'error', r.get('status'), '✅'))
    else:
        friction('rouge', f'Mauvais MDP accepté! → {r}')
        edge_results.append(('Mauvais MDP', 'error', r.get('status') if r else 'null', '❌'))

    # 5C — Code inexistant
    r = gas('save_score', {
        'code': 'XXXXXX', 'name': 'Ghost', 'level': '6EME',
        'categorie': 'Fractions', 'exercice_idx': '0', 'resultat': 'EASY'
    }, 'EDGE code inexistant')
    if r and r.get('status') == 'error':
        ok('Code inexistant rejeté')
        edge_results.append(('Code inexistant', 'error', r.get('status'), '✅'))
    else:
        friction('jaune', f'save_score avec code inexistant accepté → {r}')
        edge_results.append(('Code inexistant', 'error', r.get('status') if r else 'null', '❌'))

    # 5D — Boost avec exo invalide (a absent des options)
    sim01_code = codes.get('SIM01', '')
    if sim01_code:
        r = gas('publish_admin_boost', {
            'adminCode': ADMIN_CODE,
            'targetCode': sim01_code,
            'exos': [{'q': 'Test', 'a': 'X', 'options': ['A', 'B', 'C']}],
            'insight': 'Test invalide'
        }, 'EDGE exo invalide')
        if r and r.get('status') == 'error':
            ok('Exo invalide (a absent) rejeté')
            edge_results.append(('Exos invalides', 'error', r.get('status'), '✅'))
        else:
            friction('jaune', f'Exo invalide accepté → {r}')
            edge_results.append(('Exos invalides', 'error', r.get('status') if r else 'null', '❌'))
    else:
        edge_results.append(('Exos invalides', 'error', 'skip', '⚠'))

    # 5E — Admin sans code
    r = gas('get_admin_overview', {'adminCode': ''}, 'EDGE admin sans code')
    if r and r.get('status') == 'error':
        ok('Admin sans code rejeté')
        edge_results.append(('Admin sans code', 'error', r.get('status'), '✅'))
    else:
        friction('rouge', f'Admin sans code accepté! → {r}')
        edge_results.append(('Admin sans code', 'error', r.get('status') if r else 'null', '❌'))

    # ── Phase 6: Email verification ─────────────────────────────────────
    print('\n▶ PHASE 6 — Vérification emails')

    # 6A — Check J+0 log for SIM01
    try:
        emails_ws = sh.worksheet('📧 Emails')
        emails_data = emails_ws.get_all_values()
        if len(emails_data) > 1:
            eh = emails_data[0]
            ec = {h: i for i, h in enumerate(eh)}
            email_ci = ec.get('Email', ec.get('email', 0))
            type_ci = ec.get('Type', ec.get('type', 1))
            sim01_email = 'lucas.sim01@sim.matheux.fr'
            found_j0 = False
            for row in emails_data[1:]:
                if row[email_ci] == sim01_email and 'J+0' in row[type_ci]:
                    found_j0 = True
            if found_j0:
                ok('SIM01 J+0 email loggé')
            else:
                friction('jaune', 'SIM01 J+0 email non loggé — sendMarketingSequence ne logge peut-être pas à l\'inscription')
        sheet_checks.append(('📧 Emails', 'Vérifié', '✅' if found_j0 else '⚠'))
    except Exception as e:
        print(f'  ⚠ Onglet Emails: {e}')
        sheet_checks.append(('📧 Emails', f'Erreur: {e}', '❌'))

    # 6B — Log manual emails for due profiles
    for pid, email_type in [('SIM02', 'J+3-manuel'), ('SIM03', 'J+7-manuel'), ('SIM10', 'J+5-manuel')]:
        prof = next(p for p in PROFILES if p['id'] == pid)
        r = gas('log_manual_email', {
            'adminCode': ADMIN_CODE,
            'userEmail': prof['email'],
            'type': email_type
        }, f'{pid} log_manual_email {email_type}')
        if r and r.get('status') == 'success':
            ok(f'{pid} log_manual_email OK')
        else:
            friction('jaune', f'{pid} log_manual_email échoué: {r}')

    # 6C — Verify SIM01 has no premature emails
    # Already checked above — SIM01 is J0 so only J+0 should exist

    # ── Phase 7: Report ─────────────────────────────────────────────────
    print('\n▶ PHASE 7 — Génération du rapport')

    elapsed = int(time.time() - start_time)
    elapsed_str = f'{elapsed // 60}min {elapsed % 60}s'
    today_str = date.today().strftime('%Y-%m-%d')
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M')

    nb_ok = sum(1 for r in results.values() if r['status'] == '✅')
    nb_total = len(PROFILES)

    report = f"""# Rapport de simulation — {now_str}

## Résumé exécutif
- Profils créés : {len(codes)}/10
- Scénarios OK : {nb_ok}/10
- Frictions identifiées : {len(frictions_critiques) + len(frictions_jaunes)}
- Bugs critiques : {len(frictions_critiques)}
- Durée totale : {elapsed_str}
- Appels GAS : {len(call_log)}

## Résultats par profil

| Profil | Scénario | Statut | Frictions |
|--------|----------|--------|-----------|
"""
    for prof in PROFILES:
        pid = prof['id']
        status = results.get(pid, {}).get('status', '?')
        fr = [f for f in frictions_critiques + frictions_jaunes if pid in f]
        fr_str = '; '.join(fr) if fr else '—'
        report += f"| {pid} - {prof['prenom']} {prof['niveau']} | {prof['scenario']} | {status} | {fr_str[:80]} |\n"

    report += """
## Frictions détaillées

### 🔴 Bugs critiques (bloquants)
"""
    if frictions_critiques:
        for i, f in enumerate(frictions_critiques, 1):
            report += f'{i}. {f}\n'
    else:
        report += 'Aucun\n'

    report += """
### 🟡 Incohérences (non bloquantes)
"""
    if frictions_jaunes:
        for i, f in enumerate(frictions_jaunes, 1):
            report += f'{i}. {f}\n'
    else:
        report += 'Aucune\n'

    report += """
### 🟢 Comportements vérifiés OK
"""
    for i, v in enumerate(verifs_ok, 1):
        report += f'{i}. {v}\n'

    report += """
## Cohérence des données Sheets

| Onglet | Vérification | Résultat |
|--------|-------------|---------|
"""
    for name, verif, res in sheet_checks:
        report += f'| {name} | {verif} | {res} |\n'

    report += """
## Tests edge cases

| Test | Attendu | Reçu | OK? |
|------|---------|------|-----|
"""
    for name, attendu, recu, ok_str in edge_results:
        report += f'| {name} | {attendu} | {recu} | {ok_str} |\n'

    report += f"""
## État des profils après simulation
(pour inspection manuelle dans l'admin panel)

| Code | Profil | État admin attendu |
|------|--------|-------------------|
"""
    for prof in PROFILES:
        pid = prof['id']
        code = codes.get(pid, '—')
        report += f"| {code} | {pid} {prof['prenom']} | {prof['description']} |\n"

    report += """
## Recommandations
"""
    if frictions_critiques:
        report += '### Priorité haute\n'
        for f in frictions_critiques:
            report += f'- **FIX** {f}\n'
    if frictions_jaunes:
        report += '### Priorité moyenne\n'
        for f in frictions_jaunes:
            report += f'- {f}\n'
    if not frictions_critiques and not frictions_jaunes:
        report += 'Aucune action requise — tous les tests passent.\n'

    report_path = f'docs/rapport-simulation-{today_str}.md'
    with open(report_path, 'w') as f:
        f.write(report)
    print(f'  📄 Rapport écrit dans {report_path}')

    # ── Summary ─────────────────────────────────────────────────────────
    print(f'\n{"═" * 60}')
    print(f'  SIMULATION TERMINÉE — {elapsed_str}')
    print(f'  {len(codes)}/10 profils | {nb_ok}/10 OK | {len(frictions_critiques)} critiques | {len(frictions_jaunes)} jaunes')
    print(f'  {len(call_log)} appels GAS')
    print(f'{"═" * 60}')

    # ── Phase 8: Cleanup ────────────────────────────────────────────────
    print()
    try:
        answer = input('Nettoyage des 10 profils test ? (o/N) : ').strip().lower()
    except EOFError:
        answer = 'n'
        print('(non-interactif → pas de nettoyage)')
    if answer == 'o':
        print('🧹 Nettoyage en cours...')
        users_data = users_ws.get_all_values()
        header = users_data[0]
        col = {h: i for i, h in enumerate(header)}
        rows_del = []
        for i, row in enumerate(users_data[1:], start=2):
            if row[col['Code']] in sim_codes:
                rows_del.append(i)
        for ri in sorted(rows_del, reverse=True):
            users_ws.delete_rows(ri)
        print(f'  Users: {len(rows_del)} lignes supprimées')

        for sheet_name in ['Scores', 'DailyBoosts', 'Progress']:
            try:
                ws = sh.worksheet(sheet_name)
                all_vals = ws.get_all_values()
                if len(all_vals) <= 1:
                    continue
                sh_h = all_vals[0]
                sci = next((i for i, h in enumerate(sh_h) if h == 'Code'), 0)
                del_rows = [i for i, r in enumerate(all_vals[1:], start=2) if r[sci] in sim_codes]
                for ri in sorted(del_rows, reverse=True):
                    ws.delete_rows(ri)
                if del_rows:
                    print(f'  {sheet_name}: {len(del_rows)} lignes supprimées')
            except Exception as e:
                print(f'  ⚠ {sheet_name}: {e}')

        print('✅ Nettoyage terminé')
    else:
        print('💡 Profils conservés pour inspection dans le dashboard admin.')


if __name__ == '__main__':
    main()
