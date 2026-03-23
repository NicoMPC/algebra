"""Inject fig parameters into exercises in Curriculum_Officiel."""
import json, sys
sys.path.insert(0, "/home/nicolas/Bureau/algebra live/algebra")
from sheets import sh

# Load fig params
fig_data = {}
for f in ["/tmp/fig_params_5eme_4eme.json", "/tmp/fig_params_3eme_1ere.json", "/tmp/fig_params_6eme_5eme.json"]:
    with open(f) as fh:
        data = json.load(fh)
    for niveau, cats in data.items():
        fig_data.setdefault(niveau, {}).update(cats)

# Read sheet
raw = sh.read_raw("Curriculum_Officiel")
headers = raw[0]
exos_col_idx = headers.index("ExosJSON")  # 0-based
exos_col_1based = exos_col_idx + 1

summary = {}
total_updated = 0

for row_idx, row in enumerate(raw[1:], start=2):  # row_idx is 1-based sheet row
    if len(row) <= exos_col_idx:
        continue
    niveau = row[0]
    categorie = row[1]

    if niveau not in fig_data or categorie not in fig_data[niveau]:
        continue

    fig_map = fig_data[niveau][categorie]  # {exo_index_str: fig_obj}

    try:
        exos = json.loads(row[exos_col_idx])
    except json.JSONDecodeError:
        print(f"  ⚠️ JSON parse error row {row_idx}: {niveau}/{categorie}")
        continue

    modified = False
    count = 0
    for idx_str, fig_obj in fig_map.items():
        idx = int(idx_str)
        if idx >= len(exos):
            print(f"  ⚠️ Index {idx} out of range for {niveau}/{categorie} (has {len(exos)} exos)")
            continue
        exos[idx]["fig"] = fig_obj
        modified = True
        count += 1

    if modified:
        new_json = json.dumps(exos, ensure_ascii=False)
        sh.update_cell("Curriculum_Officiel", row_idx, exos_col_1based, new_json)
        key = f"{niveau}/{categorie}"
        summary[key] = count
        total_updated += count
        print(f"  ✅ {key}: {count} exercises updated (row {row_idx})")

print(f"\n{'='*50}")
print(f"TOTAL: {total_updated} exercises updated across {len(summary)} chapters")
for k, v in sorted(summary.items()):
    print(f"  {k}: {v} fig params")
