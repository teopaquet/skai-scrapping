import csv
from collections import defaultdict

def check_fleet_size(linkedin_file, fleet_file):

    # Charger les fleet sizes réels depuis fleet_data_2800.csv
    fleet_sizes = defaultdict(list)
    with open(fleet_file, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['airline_name'].strip()
            try:
                size = int(row['total_fleet_size'])
            except (ValueError, KeyError):
                continue
            fleet_sizes[name].append(size)

    # Pour chaque compagnie, on prend la valeur la plus fréquente (mode)
    from statistics import mode, StatisticsError
    fleet_mode = {}
    for name, sizes in fleet_sizes.items():
        try:
            fleet_mode[name] = mode(sizes)
        except StatisticsError:
            # S'il n'y a pas de mode, on prend la première valeur
            fleet_mode[name] = sizes[0] if sizes else None

    # Charger et corriger les données linkedin
    with open(linkedin_file, encoding='utf-8') as f:
        reader = list(csv.DictReader(f))
        fieldnames = reader[0].keys() if reader else []
    updated = False
    for row in reader:
        company = row['company_name'].strip()
        if company in fleet_mode and fleet_mode[company] is not None:
            correct_size = fleet_mode[company]
            try:
                linkedin_size = int(row['fleet_size'])
            except (ValueError, KeyError):
                linkedin_size = None
            if linkedin_size != correct_size:
                row['fleet_size'] = str(correct_size)
                updated = True
        # Si la compagnie n'est pas trouvée dans fleet_data, on ne modifie pas

    # Réécrire le fichier si modifié
    if updated:
        with open(linkedin_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(reader)
        print("Fichier corrigé : incohérences de fleet_size mises à jour.")
    else:
        print("Aucune correction nécessaire : tous les fleet_size sont cohérents.")

if __name__ == "__main__":
    linkedin_file = "src/interface/auth-material-ui/public/linkedin_list_merged_with_fleet.csv"
    fleet_file = "src/interface/auth-material-ui/public/fleet_data_2800.csv"
    check_fleet_size(linkedin_file, fleet_file)
