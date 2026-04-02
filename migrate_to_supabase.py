#!/usr/bin/env python3
"""
Migration Google Sheets → Supabase PostgreSQL
Exécuter APRÈS fix_schema.sql dans le SQL Editor
"""

import json, time, sys
from sheets import sh
from supabase import create_client

SUPABASE_URL = "https://xlfzhcanzmqqlxtavzrd.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhsZnpoY2Fuem1xcWx4dGF2enJkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NTEyMzU5NiwiZXhwIjoyMDkwNjk5NTk2fQ.PpLvQvrJGztv35MseEha-p-TqZDDTFrkXQT_B5fwhcc"

sb = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

def log(msg):
    print(f"  → {msg}")

def migrate_users():
    """Migre Users → auth.users + profiles"""
    print("\n══ 1/7 USERS ══")
    users = sh.read("Users")
    ok, skip, err = 0, 0, 0

    for u in users:
        code = str(u.get("Code", "")).strip()
        email = str(u.get("Email", "")).strip().lower()
        pw_hash = str(u.get("PasswordHash", "")).strip()
        name = str(u.get("Prénom", "")).strip()
        niveau = str(u.get("Niveau", "3EME")).strip().upper()
        is_admin = str(u.get("IsAdmin", "0")) in ("1", "TRUE", "True")
        premium = str(u.get("Premium", "0")) in ("1", "TRUE", "True")
        is_test = str(u.get("IsTest", "0")) in ("1", "TRUE", "True")
        date_inscription = str(u.get("DateInscription", "")).strip()[:10] or None
        trial_start = str(u.get("TrialStart", "")).strip()[:10] or None
        premium_end = str(u.get("PremiumEnd", "")).strip()[:10] or None
        objectif = str(u.get("Objectif", "")).strip()[:50]

        pending_brevet = None
        raw_pb = str(u.get("PendingBrevet", "")).strip()
        if raw_pb:
            try: pending_brevet = json.loads(raw_pb)
            except: pass

        revision_chapters = None
        raw_rc = str(u.get("RevisionChapters", "")).strip()
        if raw_rc:
            try: revision_chapters = json.loads(raw_rc)
            except: pass

        if not code or not email:
            log(f"SKIP (pas de code/email): {code}")
            skip += 1
            continue

        # Créer user Supabase Auth avec le hash SHA-256 comme "mot de passe"
        # Le frontend envoie le hash → signInWithPassword(email, hash) marchera
        try:
            auth_resp = sb.auth.admin.create_user({
                "email": email,
                "password": pw_hash if pw_hash else "temp_" + code,
                "email_confirm": True,
            })
            user_id = auth_resp.user.id
        except Exception as e:
            if "already been registered" in str(e):
                # User existe déjà — récupérer l'ID
                users_list = sb.auth.admin.list_users()
                user_id = None
                for au in users_list:
                    if hasattr(au, 'email') and au.email == email:
                        user_id = au.id
                        break
                if not user_id:
                    log(f"ERR {code} ({email}): existe mais ID introuvable")
                    err += 1
                    continue
            else:
                log(f"ERR {code} ({email}): {e}")
                err += 1
                continue

        # Insérer profil
        try:
            sb.table("profiles").upsert({
                "id": str(user_id),
                "code": code,
                "prenom": name,
                "niveau": niveau if niveau in ("6EME","5EME","4EME","3EME","1ERE") else "3EME",
                "email": email,
                "date_inscription": date_inscription,
                "is_admin": is_admin,
                "premium": premium,
                "trial_start": trial_start,
                "premium_end": premium_end,
                "is_test": is_test,
                "password_hash": pw_hash,
                "pending_brevet": pending_brevet,
                "revision_chapters": revision_chapters,
                "objectif": objectif,
            }).execute()
            ok += 1
            log(f"OK {code} {name} ({email})")
        except Exception as e:
            log(f"ERR profile {code}: {e}")
            err += 1

    print(f"  Users: {ok} OK, {skip} skip, {err} erreurs")

def migrate_scores():
    """Migre Scores → scores (batch par 500)"""
    print("\n══ 2/7 SCORES ══")
    rows = sh.read("Scores")
    batch = []
    ok, err, dup = 0, 0, 0

    for r in rows:
        code = str(r.get("Code", "")).strip()
        if not code or len(code) != 6:
            continue

        date_val = str(r.get("Date", "")).strip()[:10]
        if not date_val:
            date_val = "2026-01-01"

        batch.append({
            "code": code,
            "prenom": str(r.get("Prénom", "")),
            "niveau": str(r.get("Niveau", "3EME")),
            "chapitre": str(r.get("Chapitre", "")),
            "num_exo": int(r.get("NumExo", 0) or 0),
            "enonce": str(r.get("Énoncé", ""))[:500],
            "resultat": str(r.get("Résultat", "HARD")),
            "temps_sec": int(r.get("Temps(sec)", 0) or 0),
            "nb_indices": int(r.get("NbIndices", 0) or 0),
            "formule_vue": str(r.get("FormuleVue", "0")) in ("1", "TRUE"),
            "mauvaise_option": str(r.get("MauvaiseOption", "")),
            "draft": str(r.get("Draft", "")),
            "date": date_val,
            "source": str(r.get("Source", "")),
        })

        if len(batch) >= 500:
            try:
                sb.table("scores").upsert(batch, on_conflict="code,chapitre,num_exo,date,source").execute()
                ok += len(batch)
            except Exception as e:
                # Fallback : insérer un par un
                for item in batch:
                    try:
                        sb.table("scores").upsert(item, on_conflict="code,chapitre,num_exo,date,source").execute()
                        ok += 1
                    except Exception as e2:
                        if "duplicate" in str(e2).lower():
                            dup += 1
                        else:
                            err += 1
                            log(f"ERR score: {e2}")
            batch = []

    # Reste
    if batch:
        try:
            sb.table("scores").upsert(batch, on_conflict="code,chapitre,num_exo,date,source").execute()
            ok += len(batch)
        except Exception as e:
            for item in batch:
                try:
                    sb.table("scores").upsert(item, on_conflict="code,chapitre,num_exo,date,source").execute()
                    ok += 1
                except:
                    dup += 1

    print(f"  Scores: {ok} OK, {dup} dups, {err} erreurs (total {len(rows)})")

def migrate_progress():
    """Migre Progress → progress"""
    print("\n══ 3/7 PROGRESS ══")
    rows = sh.read("Progress")
    batch = []

    for r in rows:
        code = str(r.get("Code", "")).strip()
        if not code or len(code) != 6:
            continue

        derniere = str(r.get("DernierePratique", "")).strip()[:10] or None

        batch.append({
            "code": code,
            "niveau": str(r.get("Niveau", "3EME")),
            "categorie": str(r.get("Chapitre", "")),
            "score": int(r.get("Score", 0) or 0),
            "nb_exos": int(r.get("NbExos", 0) or 0),
            "nb_erreurs": int(r.get("NbErreurs", 0) or 0),
            "derniere_pratique": derniere,
            "statut": str(r.get("Statut", "en_cours")),
            "streak": int(r.get("Streak", 0) or 0),
        })

    try:
        sb.table("progress").upsert(batch, on_conflict="code,categorie").execute()
        print(f"  Progress: {len(batch)} OK")
    except Exception as e:
        print(f"  Progress batch error, fallback un par un: {e}")
        ok = 0
        for item in batch:
            try:
                sb.table("progress").upsert(item, on_conflict="code,categorie").execute()
                ok += 1
            except Exception as e2:
                log(f"ERR: {item['code']} {item['categorie']}: {e2}")
        print(f"  Progress: {ok}/{len(batch)} OK")

def migrate_daily_boosts():
    """Migre DailyBoosts → daily_boosts"""
    print("\n══ 4/7 DAILY_BOOSTS ══")
    rows = sh.read("DailyBoosts")
    batch = []

    for r in rows:
        code = str(r.get("Code", "")).strip()
        date_val = str(r.get("Date", "")).strip()[:10]
        if not code or len(code) != 6 or not date_val:
            continue

        boost_raw = r.get("BoostJSON", "{}")
        try:
            boost_json = json.loads(str(boost_raw)) if isinstance(boost_raw, str) else boost_raw
        except:
            boost_json = {}

        batch.append({
            "code": code,
            "date": date_val,
            "boost_json": boost_json,
            "exos_done": int(r.get("ExosDone", 0) or 0),
        })

    # Insert par batch de 100
    ok = 0
    for i in range(0, len(batch), 100):
        chunk = batch[i:i+100]
        try:
            sb.table("daily_boosts").upsert(chunk, on_conflict="code,date").execute()
            ok += len(chunk)
        except Exception as e:
            for item in chunk:
                try:
                    sb.table("daily_boosts").upsert(item, on_conflict="code,date").execute()
                    ok += 1
                except:
                    pass

    print(f"  DailyBoosts: {ok}/{len(batch)} OK")

def migrate_curriculum():
    """Migre Curriculum_Officiel → curriculum"""
    print("\n══ 5/7 CURRICULUM ══")
    rows = sh.read("Curriculum_Officiel")
    batch = []

    for r in rows:
        niveau = str(r.get("Niveau", "")).strip()
        categorie = str(r.get("Categorie", "")).strip()
        if not niveau or not categorie:
            continue

        exos_raw = r.get("ExosJSON", "[]")
        try:
            exos = json.loads(str(exos_raw)) if isinstance(exos_raw, str) else exos_raw
        except:
            exos = []

        timer_val = r.get("Timer", "")
        timer = int(timer_val) if timer_val and str(timer_val).isdigit() else 60
        ordered = str(r.get("Ordered", "")).upper() in ("TRUE", "1", "OUI")

        batch.append({
            "niveau": niveau,
            "categorie": categorie,
            "titre": str(r.get("Titre", categorie)),
            "icone": str(r.get("Icone", "📘")),
            "exos_json": exos,
            "timer": timer,
            "ordered": ordered,
        })

    try:
        sb.table("curriculum").upsert(batch, on_conflict="niveau,categorie").execute()
        print(f"  Curriculum: {len(batch)} OK")
    except Exception as e:
        print(f"  Curriculum error: {e}")
        ok = 0
        for item in batch:
            try:
                sb.table("curriculum").upsert(item, on_conflict="niveau,categorie").execute()
                ok += 1
            except Exception as e2:
                log(f"ERR: {item['niveau']} {item['categorie']}: {e2}")
        print(f"  Curriculum: {ok}/{len(batch)} OK")

def migrate_diagnostic_exos():
    """Migre DiagnosticExos → diagnostic_exos"""
    print("\n══ 6/7 DIAGNOSTIC_EXOS ══")
    rows = sh.read("DiagnosticExos")
    batch = []

    for r in rows:
        niveau = str(r.get("Niveau", "")).strip()
        categorie = str(r.get("Categorie", "")).strip()
        if not niveau or not categorie:
            continue

        exos_raw = r.get("ExosJSON", "[]")
        try:
            exos = json.loads(str(exos_raw)) if isinstance(exos_raw, str) else exos_raw
        except:
            exos = []

        batch.append({
            "niveau": niveau,
            "categorie": categorie,
            "exos_json": exos,
        })

    try:
        sb.table("diagnostic_exos").upsert(batch, on_conflict="niveau,categorie").execute()
        print(f"  DiagnosticExos: {len(batch)} OK")
    except Exception as e:
        print(f"  DiagnosticExos error: {e}")

def migrate_cours():
    """Migre Cours → cours"""
    print("\n══ 7/7 COURS ══")
    rows = sh.read("Cours")
    batch = []

    for r in rows:
        niveau = str(r.get("Niveau", "")).strip()
        categorie = str(r.get("Categorie", "")).strip()
        if not niveau or not categorie:
            continue

        batch.append({
            "niveau": niveau,
            "categorie": categorie,
            "section_10": str(r.get("Section10", "") or ""),
            "section_20": str(r.get("Section20", "") or ""),
            "date_maj": str(r.get("DateMaj", "")).strip()[:10] or None,
        })

    if batch:
        try:
            sb.table("cours").upsert(batch, on_conflict="niveau,categorie").execute()
            print(f"  Cours: {len(batch)} OK")
        except Exception as e:
            print(f"  Cours error: {e}")
    else:
        print("  Cours: 0 lignes")


if __name__ == "__main__":
    print("╔══════════════════════════════════════════════╗")
    print("║  MIGRATION SHEETS → SUPABASE                ║")
    print("╚══════════════════════════════════════════════╝")

    t0 = time.time()

    migrate_users()
    migrate_scores()
    migrate_progress()
    migrate_daily_boosts()
    migrate_curriculum()
    migrate_diagnostic_exos()
    migrate_cours()

    elapsed = time.time() - t0
    print(f"\n✅ Migration terminée en {elapsed:.1f}s")
    print("Vérifier dans le dashboard Supabase : https://supabase.com/dashboard/project/xlfzhcanzmqqlxtavzrd/editor")
