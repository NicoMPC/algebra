#!/usr/bin/env python3
"""
setup_test_profiles.py
Configure 6 profils test avec des états variés pour valider le dashboard admin.
Usage : python3 setup_test_profiles.py
"""
import json, os, sys
from datetime import datetime, timedelta
from google.oauth2.service_account import Credentials
import gspread

SHEET_ID = '1SiE3lHf9dAKbExWPGNrk5cbLhDbKUKM4xvd1Th1frY4'
SA_FILE  = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'algebreboost-sheets-2595a71cadfb.json')
SCOPES   = ['https://www.googleapis.com/auth/spreadsheets']

PROFILES = [
    {'label': 'Test_1 J+0 6EME',     'days_offset': 0,   'boost_done': 0, 'chap_exos': 2,  'niveau': '6EME', 'cat': 'Fractions',  'desc': 'Mail bienvenue non envoyé, boost en attente'},
    {'label': 'Test_2 J+3 5EME',     'days_offset': -3,  'boost_done': 5, 'chap_exos': 8,  'niveau': '5EME', 'cat': 'Puissances', 'desc': 'Mail J+3 à envoyer, boost terminé'},
    {'label': 'Test_3 J+7 4EME',     'days_offset': -7,  'boost_done': 5, 'chap_exos': 20, 'niveau': '4EME', 'cat': 'Équations',  'desc': 'Mail J+7 + Stripe, chapitre terminé'},
    {'label': 'Test_4 J+5 3EME',     'days_offset': -5,  'boost_done': 2, 'chap_exos': 5,  'niveau': '3EME', 'cat': 'Fonctions',  'desc': 'Mail J+5, boost en cours'},
    {'label': 'Test_5 Cours 6EME',   'days_offset': -2,  'boost_done': 3, 'chap_exos': 5,  'niveau': '6EME', 'cat': 'Fractions',  'desc': 'Milestone cours atteint, section vide'},
    {'label': 'Test_6 Inactif 1ERE', 'days_offset': -10, 'boost_done': 0, 'chap_exos': 3,  'niveau': '1ERE', 'cat': 'Suites',     'desc': 'Sans nouvelles >7j, scores bas'},
]


def main():
    if not os.path.exists(SA_FILE):
        print(f'❌ Fichier service account introuvable : {SA_FILE}')
        sys.exit(1)

    creds = Credentials.from_service_account_file(SA_FILE, scopes=SCOPES)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(SHEET_ID)

    today = datetime.now().date()

    # --- Charger Users ---
    users_ws = sh.worksheet('Users')
    users = users_ws.get_all_values()
    header = users[0]

    # Trouver les index de colonnes
    col = {h: i for i, h in enumerate(header)}
    code_col     = col.get('Code', 0)
    name_col     = col.get('Nom', 1)
    level_col    = col.get('Niveau', col.get('Level', 3))
    trial_col    = col.get('TrialStart', col.get('DateInscription', 8))
    istest_col   = col.get('IsTest', 10)
    welcome_col  = col.get('WelcomeEmailSent', None)

    # Filtrer les comptes test
    test_users = []
    for i, row in enumerate(users[1:], start=2):  # 1-based row index
        try:
            if str(row[istest_col]).strip() == '1':
                test_users.append((i, row))
        except IndexError:
            pass

    print(f'📋 {len(test_users)} comptes test trouvés (besoin de {len(PROFILES)})')

    if len(test_users) < len(PROFILES):
        print(f'⚠️  Pas assez de comptes test. Création nécessaire ou réutilisation.')
        # Réutiliser les existants en boucle
        while len(test_users) < len(PROFILES):
            test_users.extend(test_users[:len(PROFILES) - len(test_users)])

    # --- Charger DailyBoosts ---
    boost_ws = sh.worksheet('DailyBoosts')
    boost_data = boost_ws.get_all_values()
    boost_header = boost_data[0] if boost_data else []
    boost_code_col = 0  # Code en colonne A
    boost_done_col = next((i for i, h in enumerate(boost_header) if h == 'ExosDone'), None)
    boost_date_col = next((i for i, h in enumerate(boost_header) if h == 'Date'), None)

    # --- Appliquer les profils ---
    updates_users = []
    updates_boosts = []

    for idx, ((row_num, row), prof) in enumerate(zip(test_users[:len(PROFILES)], PROFILES)):
        code = row[code_col]
        trial_date = (today + timedelta(days=prof['days_offset'])).strftime('%Y-%m-%d')

        # Mise à jour TrialStart
        updates_users.append({
            'range': f'{gspread.utils.rowcol_to_a1(row_num, trial_col + 1)}',
            'values': [[trial_date]],
        })

        # Mise à jour Niveau si différent
        if row[level_col] != prof['niveau']:
            updates_users.append({
                'range': f'{gspread.utils.rowcol_to_a1(row_num, level_col + 1)}',
                'values': [[prof['niveau']]],
            })

        # Reset WelcomeEmailSent pour J+0
        if welcome_col is not None and prof['days_offset'] == 0:
            updates_users.append({
                'range': f'{gspread.utils.rowcol_to_a1(row_num, welcome_col + 1)}',
                'values': [['']],
            })

        # Mise à jour boost ExosDone
        if boost_done_col is not None:
            for bi, brow in enumerate(boost_data[1:], start=2):
                try:
                    if brow[boost_code_col] == code:
                        updates_boosts.append({
                            'range': f'{gspread.utils.rowcol_to_a1(bi, boost_done_col + 1)}',
                            'values': [[str(prof['boost_done'])]],
                        })
                        # Mettre la date du boost au bon jour
                        if boost_date_col is not None:
                            updates_boosts.append({
                                'range': f'{gspread.utils.rowcol_to_a1(bi, boost_date_col + 1)}',
                                'values': [[trial_date]],
                            })
                        break
                except IndexError:
                    pass

        print(f'  ✅ [{prof["label"]}] {code} → TrialStart={trial_date}, '
              f'boost_done={prof["boost_done"]}, niveau={prof["niveau"]}')
        print(f'     {prof["desc"]}')

    # Batch update Users
    if updates_users:
        users_ws.batch_update(updates_users)
        print(f'\n📝 {len(updates_users)} cellules mises à jour dans Users')

    # Batch update DailyBoosts
    if updates_boosts:
        boost_ws.batch_update(updates_boosts)
        print(f'📝 {len(updates_boosts)} cellules mises à jour dans DailyBoosts')

    print('\n✅ Profils test configurés. Recharger le dashboard admin pour voir les états.')
    print('💡 Pour reconstruire le suivi : appeler rebuildSuivi depuis le dashboard admin.')


if __name__ == '__main__':
    main()
