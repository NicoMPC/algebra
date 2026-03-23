"""
Setup Léo (6OCZ3G) — 4EME — Simule onboarding complété
- Boost du jour → ExosDone=5 (terminé)
- Scores CALIBRAGE factices (4 chapitres)
- Scores BOOST factices (5 exos)
- Chapitre Statistiques injecté dans Suivi col G (prioritaire)
"""

import json, random
from datetime import datetime
from sheets import sh

CODE = "6OCZ3G"
PRENOM = "Léo"
NIVEAU = "4EME"
TODAY = datetime.now().strftime("%Y-%m-%d")

# ── 1. Boost existant → ExosDone=5 ────────────────────────────────
boosts_raw = sh.read_raw("DailyBoosts")
for i, row in enumerate(boosts_raw):
    if i == 0: continue  # header
    if len(row) > 0 and row[0] == CODE and (len(row) < 4 or str(row[3]) != "5"):
        # Col D = ExosDone (index 3, 0-based) → mettre à 5
        sh.update_cell("DailyBoosts", i + 1, 4, 5)  # 1-indexed
        boost_json = json.loads(row[2]) if len(row) > 2 else {}
        print(f"✅ Boost {row[1]} → ExosDone=5")
        break
else:
    print("⚠️  Pas de boost trouvé pour Léo")
    boost_json = {}

# ── 2. Scores CALIBRAGE factices ──────────────────────────────────
diag_chapters = ["Statistiques", "Calcul_Litteral", "Proportionnalite", "Equations"]
diag_exos = sh.read("DiagnosticExos")

for cat in diag_chapters:
    for dr in diag_exos:
        if dr.get("Niveau") == NIVEAU and dr.get("Categorie") == cat:
            exos = json.loads(dr["ExosJSON"])
            for i, exo in enumerate(exos[:2]):
                result = random.choice(["EASY", "EASY", "MEDIUM", "HARD"])
                sh.append_row("Scores", [
                    CODE, PRENOM, NIVEAU, cat, i + 1,
                    exo.get("q", "")[:60], result,
                    random.randint(15, 90), 0, 0, "", "", TODAY, "CALIBRAGE"
                ])
            break
print(f"✅ Scores CALIBRAGE créés pour {len(diag_chapters)} chapitres")

# ── 3. Scores BOOST factices (5 exos) ─────────────────────────────
boost_exos = boost_json.get("exos", [])
for i, exo in enumerate(boost_exos[:5]):
    result = random.choice(["EASY", "EASY", "MEDIUM", "HARD"])
    sh.append_row("Scores", [
        CODE, PRENOM, NIVEAU, exo.get("_cat", "Statistiques"), i + 1,
        exo.get("q", exo.get("enonce", ""))[:60], result,
        random.randint(20, 60), 0, 0, "", "", TODAY, "BOOST"
    ])
print(f"✅ {len(boost_exos[:5])} scores BOOST créés")

# ── 4. Chapitre Statistiques → Suivi col G ────────────────────────
# Récupérer le JSON complet depuis Curriculum_Officiel
curriculum = sh.read("Curriculum_Officiel")
stats_row = None
for r in curriculum:
    if r.get("Niveau") == NIVEAU and r.get("Categorie") == "Statistiques":
        stats_row = r
        break

if not stats_row:
    print("❌ Pas de chapitre Statistiques 4EME dans Curriculum_Officiel")
    exit(1)

stats_chapter = {
    "categorie": "Statistiques",
    "titre": stats_row.get("Titre", "Statistiques"),
    "icone": stats_row.get("Icone", "📊"),
    "exos": json.loads(stats_row["ExosJSON"]),
    "insight": "On commence par les statistiques — c'est le chapitre idéal pour ton contrôle ! 🎯"
}
print(f"✅ Chapitre Statistiques : {len(stats_chapter['exos'])} exos")

# Trouver Léo dans Suivi (Code en col U = index 20, 0-based)
suivi_raw = sh.read_raw("👁 Suivi")
leo_row_idx = None
for i, row in enumerate(suivi_raw):
    if len(row) > 20 and row[20] == CODE:
        leo_row_idx = i + 1  # 1-based
        break

if leo_row_idx:
    sh.update_cell("👁 Suivi", leo_row_idx, 7, json.dumps(stats_chapter, ensure_ascii=False))
    print(f"✅ Statistiques injecté dans Suivi ligne {leo_row_idx}, col G")
else:
    print("⚠️  Léo pas dans Suivi — il apparaîtra après son premier login (rebuildSuivi)")
    print(f"   JSON prêt : {json.dumps(stats_chapter, ensure_ascii=False)[:150]}...")

# ── Résumé ─────────────────────────────────────────────────────────
print(f"""
{'='*50}
SETUP LÉO — TERMINÉ
{'='*50}
Code        : {CODE}
Niveau      : {NIVEAU}

✅ Boost du jour    → terminé (5/5)
✅ CALIBRAGE        → 4 chapitres diagnostiqués
✅ Scores BOOST     → 5 exos enregistrés
✅ Prochain cours   → Statistiques (Suivi col G)

Quand il se connecte :
  → Boost marqué terminé → hero "demain"
  → Statistiques en premier (assignedByProf + tri pinné)
  → Les autres chapitres sont visibles normalement
{'='*50}
""")
