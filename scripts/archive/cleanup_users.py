"""
Nettoyage base : supprime tous les users sauf admin, jerome, auguste, charlie
+ leurs données dans tous les onglets liés.
"""
from sheets import sh

# 1. Lire Users, identifier les codes à garder
users = sh.read("Users")
print(f"Users avant : {len(users)}")

KEEP_NAMES = {"admin", "jerome", "auguste", "charlie"}

keep_codes = set()
for u in users:
    prenom = (u.get("Prénom") or "").strip().lower()
    is_admin = str(u.get("IsAdmin", "0")).strip().lower() in ("1", "true")
    if prenom in KEEP_NAMES or is_admin:
        keep_codes.add(u.get("Code", ""))
        print(f"  ✅ GARDER : {u.get('Prénom')} ({u.get('Code')}) — {u.get('Niveau')}")

# Show who will be deleted
for u in users:
    if u.get("Code") not in keep_codes:
        print(f"  ❌ SUPPRIMER : {u.get('Prénom')} ({u.get('Code')}) — {u.get('Niveau')}")

if not keep_codes:
    print("⚠️ Aucun user à garder trouvé, abandon.")
    exit(1)

# 2. Clean Users
users_raw = sh.read_raw("Users")
header_users = users_raw[0]
kept_users = [header_users] + [r for r in users_raw[1:] if r and r[0] in keep_codes]
sh.write_rows("Users", kept_users)

# 3. Clean onglets avec Code en colonne A
for tab in ["Scores", "Progress", "DailyBoosts", "BrevetResults"]:
    try:
        raw = sh.read_raw(tab)
        if not raw:
            print(f"  {tab} : vide")
            continue
        header = raw[0]
        kept = [header] + [r for r in raw[1:] if r and r[0] in keep_codes]
        removed = len(raw) - len(kept)
        sh.write_rows(tab, kept)
        print(f"  {tab} : {removed} lignes supprimées")
    except Exception as e:
        print(f"  {tab} : erreur — {e}")

# 4. Clean 👁 Suivi (Code en col T = index 19, 0-based)
try:
    raw = sh.read_raw("👁 Suivi")
    if raw:
        header = raw[0]
        # Find Code column (should be T = index 19)
        code_idx = None
        for i, h in enumerate(header):
            if "Code" in str(h):
                code_idx = i
                break
        if code_idx is None:
            code_idx = 19  # fallback col T
        kept = [header] + [r for r in raw[1:] if len(r) > code_idx and r[code_idx] in keep_codes]
        removed = len(raw) - len(kept)
        sh.write_rows("👁 Suivi", kept)
        print(f"  👁 Suivi : {removed} lignes supprimées (Code col {code_idx})")
except Exception as e:
    print(f"  👁 Suivi : erreur — {e}")

# 5. Clean 📋 Historique (Code en col A normalement)
try:
    raw = sh.read_raw("📋 Historique")
    if raw:
        header = raw[0]
        # Find which col has Code
        code_idx = 0
        for i, h in enumerate(header):
            if "Code" in str(h):
                code_idx = i
                break
        kept = [header] + [r for r in raw[1:] if len(r) > code_idx and r[code_idx] in keep_codes]
        removed = len(raw) - len(kept)
        sh.write_rows("📋 Historique", kept)
        print(f"  📋 Historique : {removed} lignes supprimées")
except Exception as e:
    print(f"  📋 Historique : erreur — {e}")

# 6. Clean Insights (Code en col B = index 1)
try:
    raw = sh.read_raw("Insights")
    if raw:
        header = raw[0]
        kept = [header] + [r for r in raw[1:] if len(r) > 1 and r[1] in keep_codes]
        removed = len(raw) - len(kept)
        sh.write_rows("Insights", kept)
        print(f"  Insights : {removed} lignes supprimées")
except Exception as e:
    print(f"  Insights : erreur — {e}")

# 7. Clean 📧 Emails (check Code column)
try:
    raw = sh.read_raw("📧 Emails")
    if raw:
        header = raw[0]
        code_idx = None
        for i, h in enumerate(header):
            if "Code" in str(h):
                code_idx = i
                break
        if code_idx is not None:
            kept = [header] + [r for r in raw[1:] if len(r) > code_idx and r[code_idx] in keep_codes]
            removed = len(raw) - len(kept)
            sh.write_rows("📧 Emails", kept)
            print(f"  📧 Emails : {removed} lignes supprimées")
        else:
            print(f"  📧 Emails : pas de colonne Code trouvée, ignoré")
except Exception as e:
    print(f"  📧 Emails : erreur — {e}")

print("\n✅ Nettoyage terminé.")
