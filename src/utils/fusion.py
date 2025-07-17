import pandas as pd
import os

# Chemins absolus depuis ce script
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/raw'))
linkedin_path = os.path.join(base_dir, 'linkedin_list', 'linkedin_list_merged.csv')
aircraft_path = os.path.join(base_dir, 'individual_aircraft.csv')
output_path = os.path.join(base_dir, 'linkedin_list', 'linkedin_list_merged_with_fleet.csv')


# Vérifier l'existence des fichiers et afficher les chemins
print(f"Chemin linkedin : {linkedin_path}")
print(f"Chemin aircraft : {aircraft_path}")
if not os.path.exists(linkedin_path):
    raise FileNotFoundError(f"Fichier introuvable : {linkedin_path}")
if not os.path.exists(aircraft_path):
    raise FileNotFoundError(f"Fichier introuvable : {aircraft_path}")

linkedin_df = pd.read_csv(linkedin_path)
aircraft_df = pd.read_csv(aircraft_path)


# Normaliser les noms pour le matching
def normalize(s):
    if pd.isna(s):
        return ''
    return str(s).strip().lower()

aircraft_df['airline_name_norm'] = aircraft_df['airline_name'].apply(normalize)
linkedin_df['company_name_norm'] = linkedin_df['company_name'].apply(normalize)

# Dictionnaire sur noms normalisés
fleet_by_company = aircraft_df.groupby('airline_name_norm')['total_fleet_size'].max().to_dict()
linkedin_df['fleet_size'] = linkedin_df['company_name_norm'].map(fleet_by_company)

# Afficher quelques exemples de compagnies sans fleet_size
no_fleet = linkedin_df[linkedin_df['fleet_size'].isna()]['company_name'].drop_duplicates().head(10)
print("Exemples de compagnies sans fleet_size :")
print(no_fleet.to_list())

# Exporter le résultat
linkedin_df.to_csv(output_path, index=False)
print(f"Fichier créé : {output_path}")
print(f"Nombre de compagnies avec fleet_size renseigné : {linkedin_df['fleet_size'].notna().sum()}")
