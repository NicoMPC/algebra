#!/usr/bin/env python3
"""
setup_test_profiles.py
Configure 6 profils test avec des états variés pour valider le dashboard admin.
Crée les comptes test s'ils n'existent pas.
Usage : python3 setup_test_profiles.py
"""
import hashlib, os, random, string, sys
from datetime import datetime, timedelta
from google.oauth2.service_account import Credentials
import gspread

SHEET_ID = '1SiE3lHf9dAKbExWPGNrk5cbLhDbKUKM4xvd1Th1frY4'
SA_FILE  = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'algebreboost-sheets-2595a71cadfb.json')
SCOPES   = ['https://www.googleapis.com/auth/spreadsheets']

PROFILES = [
    {'label': 'Test_1', 'name': 'Emma',    'email': 'test1@matheux.fr', 'days_offset': 0,   'niveau': '6EME', 'desc': 'J+0 — mail bienvenue non envoyé'},
    {'label': 'Test_2', 'name': 'Lucas',   'email': 'test2@matheux.fr', 'days_offset': -3,  'niveau': '5EME', 'desc': 'J+3 — mail J+3 à envoyer'},
    {'label': 'Test_3', 'name': 'Léa',     'email': 'test3@matheux.fr', 'days_offset': -7,  'niveau': '4EME', 'desc': 'J+7 — mail J+7 + Stripe'},
    {'label': 'Test_4', 'name': 'Hugo',    'email': 'test4@matheux.fr', 'days_offset': -5,  'niveau': '3EME', 'desc': 'J+5 — mail J+5, boost en cours'},
    {'label': 'Test_5', 'name': 'Chloé',   'email': 'test5@matheux.fr', 'days_offset': -2,  'niveau': '6EME', 'desc': 'J+2 — milestone cours atteint'},
    {'label': 'Test_6', 'name': 'Nathan',  'email': 'test6@matheux.fr', 'days_offset': -10, 'niveau': '1ERE', 'desc': 'Inactif >7j — Sans nouvelles'},
]


def gen_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()


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
    col = {h: i for i, h in enumerate(header)}

    # Colonnes nécessaires
    code_col    = col['Code']
    name_col    = col['Prénom']
    level_col   = col['Niveau']
    email_col   = col['Email']
    pw_col      = col['PasswordHash']
    date_col    = col['DateInscription']
    isadmin_col = col['IsAdmin']
    premium_col = col['Premium']
    trial_col   = col['TrialStart']
    end_col     = col['PremiumEnd']
    istest_col  = col['IsTest']

    # Emails existants
    existing_emails = {r[email_col]: i for i, r in enumerate(users[1:], start=2)}

    print(f'📋 {len(header)} colonnes, {len(users)-1} utilisateurs existants')

    new_rows = []
    updates = []

    for prof in PROFILES:
        trial_date = (today + timedelta(days=prof['days_offset'])).strftime('%Y-%m-%d')

        if prof['email'] in existing_emails:
            # Mettre à jour le compte existant
            row_num = existing_emails[prof['email']]
            updates.append({'range': gspread.utils.rowcol_to_a1(row_num, trial_col + 1), 'values': [[trial_date]]})
            updates.append({'range': gspread.utils.rowcol_to_a1(row_num, level_col + 1), 'values': [[prof['niveau']]]})
            updates.append({'range': gspread.utils.rowcol_to_a1(row_num, date_col + 1),  'values': [[trial_date]]})
            print(f'  🔄 [{prof["label"]}] {prof["email"]} → maj TrialStart={trial_date}, niveau={prof["niveau"]}')
        else:
            # Créer le compte
            code = gen_code()
            row = [''] * len(header)
            row[code_col]    = code
            row[name_col]    = prof['name']
            row[level_col]   = prof['niveau']
            row[email_col]   = prof['email']
            row[pw_col]      = hash_pw('test1234')
            row[date_col]    = trial_date
            row[isadmin_col] = ''
            row[premium_col] = 'trial'
            row[trial_col]   = trial_date
            row[end_col]     = (today + timedelta(days=7 + prof['days_offset'])).strftime('%Y-%m-%d')
            row[istest_col]  = '1'
            new_rows.append(row)
            print(f'  ✨ [{prof["label"]}] {code} {prof["name"]} ({prof["email"]}) → créé, TrialStart={trial_date}')

        print(f'     {prof["desc"]}')

    # Batch update existing
    if updates:
        users_ws.batch_update(updates)
        print(f'\n📝 {len(updates)} cellules mises à jour')

    # Append new users
    if new_rows:
        users_ws.append_rows(new_rows, value_input_option='RAW')
        print(f'📝 {len(new_rows)} comptes test créés')

    print('\n✅ Profils test configurés.')
    print('🔑 Mot de passe commun : test1234')
    print('💡 Recharger le dashboard admin pour voir les états.')


if __name__ == '__main__':
    main()
