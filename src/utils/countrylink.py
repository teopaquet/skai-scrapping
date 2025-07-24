import csv

# Fichiers d'entrée
FLEET_CSV = '../../data/processed/fleet_data_2800_with_country.csv'
LINKEDIN_CSV = '../../data/raw/linkedin_list/linkedin_list_merged_with_fleet.csv'
OUTPUT_CSV = '../../data/raw/linkedin_list/linkedin_list_with_country.csv'

# Charger le mapping company_name -> country depuis fleet_data
fleet_countries = {}
with open(FLEET_CSV, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row['airline_name'].strip()
        country = row['country'].strip() if row['country'] else ''
        if name and country:
            fleet_countries[name] = country

# Lire linkedin_list et ajouter la colonne country
with open(LINKEDIN_CSV, encoding='utf-8') as f_in, open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f_out:
    reader = csv.DictReader(f_in)
    fieldnames = reader.fieldnames + ['country']
    writer = csv.DictWriter(f_out, fieldnames=fieldnames)
    writer.writeheader()
    for row in reader:
        company = row['company_name'].strip()
        row['country'] = fleet_countries.get(company, '')
        writer.writerow(row)

print(f"Fichier créé : {OUTPUT_CSV}")
