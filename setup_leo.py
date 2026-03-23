"""
Setup compte Léo — 4EME — leoiozzia2012@gmail.com
- Crée le user dans Users
- Crée un boost "fait" aujourd'hui (ExosDone=5)
- Injecte "Statistiques" comme prochain chapitre dans Suivi col G
- Crée des scores CALIBRAGE factices
"""

import hashlib, json, random, string
from datetime import datetime
from sheets import sh

TODAY = datetime.now().strftime("%Y-%m-%d")
EMAIL = "leoiozzia2012@gmail.com"
PASSWORD = "leoleo"
PRENOM = "Léo"
NIVEAU = "4EME"

# ── 1. Générer le code unique ──────────────────────────────────────
existing_codes = {r["Code"] for r in sh.read("Users")}
while True:
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    if code not in existing_codes:
        break
print(f"Code généré : {code}")

# ── 2. Hash du mot de passe ────────────────────────────────────────
raw = f"{EMAIL}::{PASSWORD}::AB22"
pw_hash = hashlib.sha256(raw.encode()).hexdigest()

# ── 3. Insérer dans Users ──────────────────────────────────────────
# Code | Prénom | Niveau | Email | PasswordHash | DateInscription | IsAdmin | Premium | TrialStart | PremiumEnd | IsTest | PendingBrevet | RevisionChapters | Objectif
user_row = [
    code, PRENOM, NIVEAU, EMAIL, pw_hash,
    TODAY,   # DateInscription
    0,       # IsAdmin
    0,       # Premium
    TODAY,   # TrialStart
    "",      # PremiumEnd
    1,       # IsTest (compte test)
    "",      # PendingBrevet
    "",      # RevisionChapters
    "lacunes"  # Objectif
]
sh.append_row("Users", user_row)
print(f"✅ User {PRENOM} ({code}) créé dans Users")

# ── 4. Récupérer les exos Statistiques 4EME depuis Curriculum_Officiel ──
curriculum = sh.read("Curriculum_Officiel")
stats_row = None
for r in curriculum:
    if r.get("Niveau") == "4EME" and r.get("Categorie") == "Statistiques":
        stats_row = r
        break

if not stats_row:
    print("❌ Pas de chapitre Statistiques en 4EME dans Curriculum_Officiel !")
    exit(1)

stats_exos = json.loads(stats_row["ExosJSON"])
stats_chapter = {
    "categorie": "Statistiques",
    "titre": stats_row.get("Titre", "Statistiques"),
    "icone": stats_row.get("Icone", "📊"),
    "exos": stats_exos,
    "insight": "On commence par les statistiques — c'est le chapitre idéal pour reprendre confiance !"
}
print(f"✅ Chapitre Statistiques trouvé ({len(stats_exos)} exos)")

# ── 5. Créer un boost "fait" aujourd'hui ───────────────────────────
# On prend 5 exos depuis BoostExos ou Curriculum comme fallback
boost_exos_rows = sh.read("BoostExos")
boost_pool = None
for r in boost_exos_rows:
    if r.get("Niveau") == "4EME" and r.get("Categorie") == "Statistiques":
        boost_pool = json.loads(r["ExosJSON"])
        break

if not boost_pool:
    # Fallback : prendre les 5 premiers exos du curriculum
    boost_pool = stats_exos[:5]

boost_exos = boost_pool[:5]
boost_json = {
    "insight": "On fait le point sur tes bases en Statistiques !",
    "exos": boost_exos
}

# DailyBoosts : Code | Date | BoostJSON | ExosDone
sh.append_row("DailyBoosts", [
    code, TODAY, json.dumps(boost_json, ensure_ascii=False), 5  # ExosDone=5 = terminé
])
print(f"✅ Boost du jour créé (ExosDone=5, terminé)")

# ── 6. Créer des scores CALIBRAGE factices ─────────────────────────
# On simule 4 chapitres diagnostiqués (mix de résultats)
diag_chapters = ["Statistiques", "Calcul_Litteral", "Proportionnalite", "Equations"]
diag_exos = sh.read("DiagnosticExos")

for cat in diag_chapters:
    for dr in diag_exos:
        if dr.get("Niveau") == "4EME" and dr.get("Categorie") == cat:
            exos = json.loads(dr["ExosJSON"])
            for i, exo in enumerate(exos[:2]):
                result = random.choice(["EASY", "EASY", "MEDIUM", "HARD"])
                # Scores : Code | Prénom | Niveau | Chapitre | NumExo | Énoncé | Résultat | Temps | NbIndices | FormuleVue | MauvaiseOption | Draft | Date | Source
                sh.append_row("Scores", [
                    code, PRENOM, NIVEAU, cat, i + 1,
                    exo.get("q", "")[:60], result,
                    random.randint(15, 90), 0, 0, "", "", TODAY, "CALIBRAGE"
                ])
            break
print(f"✅ Scores CALIBRAGE créés pour {len(diag_chapters)} chapitres")

# ── 7. Créer des scores BOOST factices (5 exos faits) ─────────────
for i, exo in enumerate(boost_exos):
    result = random.choice(["EASY", "EASY", "MEDIUM", "HARD"])
    sh.append_row("Scores", [
        code, PRENOM, NIVEAU, exo.get("_cat", "Statistiques"), i + 1,
        exo.get("q", exo.get("enonce", ""))[:60], result,
        random.randint(20, 60), 0, 0, "", "", TODAY, "BOOST"
    ])
print(f"✅ 5 scores BOOST créés")

# ── 8. Injecter dans Suivi — col G (index 6) = prochain chapitre ──
# D'abord chercher si Léo existe déjà dans Suivi
suivi_raw = sh.read_raw("👁 Suivi")
leo_row_idx = None
for i, row in enumerate(suivi_raw):
    # Code est en colonne U (index 20, 0-based)
    if len(row) > 20 and row[20] == code:
        leo_row_idx = i + 1  # 1-based for Sheets API
        break

if leo_row_idx:
    # Mettre le chapitre dans col G (7ème colonne, 1-based)
    sh.update_cell("👁 Suivi", leo_row_idx, 7, json.dumps(stats_chapter, ensure_ascii=False))
    print(f"✅ Statistiques injecté dans Suivi ligne {leo_row_idx}, col G")
else:
    print("⚠️  Léo pas encore dans Suivi — le rebuildSuivi GAS le créera au prochain login.")
    print(f"   Tu peux aussi lancer rebuildSuivi manuellement ou injecter via l'admin panel.")
    print(f"   Chapitre JSON prêt à coller dans col G :")
    print(f"   {json.dumps(stats_chapter, ensure_ascii=False)[:200]}...")

# ── Résumé ─────────────────────────────────────────────────────────
print(f"""
{'='*50}
COMPTE LÉO — PRÊT
{'='*50}
Code        : {code}
Email       : {EMAIL}
MDP         : {PASSWORD}
Niveau      : {NIVEAU}
IsTest      : 1 (compte test)
Trial start : {TODAY}

État :
  ✅ Quiz diagnostic → fait (CALIBRAGE)
  ✅ Boost du jour   → fait (5/5)
  ✅ Prochain cours  → Statistiques (dans Suivi col G)

Quand il se connecte :
  → Le boost est marqué terminé
  → "Statistiques" apparaît en premier
  → Message : "On commence par les statistiques"
{'='*50}
""")
