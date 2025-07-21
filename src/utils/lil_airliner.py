
import csv
import os

# Chemins relatifs basés sur l'emplacement du script
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_airlines = os.path.join(base_dir, "..", "..", "data", "raw", "airlines_name_clean_filtered.csv")
csv_linkedin = os.path.join(base_dir, "..", "..", "data", "raw", "linkedin_list", "linkedin_list_merged_with_fleet.csv")
output_csv = os.path.join(base_dir, "..", "..", "data", "exports", "airlines_fleet_leq_25.csv")

# Lecture des noms d'airlines du premier CSV

with open(csv_airlines, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    airlines_set = set(row["companies_name"].strip() for row in reader if row["companies_name"].strip())

# Lecture du second CSV et filtrage
selected_names = set()

with open(csv_linkedin, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row["company_name"].strip()
        fleet_size = row["fleet_size"].strip()
        if not name or name not in airlines_set:
            continue
        try:
            fs = int(fleet_size) if fleet_size else None
            if fs is not None and 2 < fs <= 25:
                selected_names.add(name)
        except ValueError:
            continue

# Écriture du résultat dans le nouveau CSV

os.makedirs(os.path.dirname(output_csv), exist_ok=True)
with open(output_csv, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["company_name"])
    for name in sorted(selected_names):
        writer.writerow([name])
