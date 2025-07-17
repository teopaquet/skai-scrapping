
import pandas as pd

csv_path = '../../data/raw/linkedin_list/linkedin_list_merged_with_fleet.csv'

# Charger le CSV
df = pd.read_csv(csv_path)

# Supprimer les lignes où company_name == 'companies_name'
df = df[df['company_name'] != 'companies_name']

# Réécrire le fichier (même nom, écrasement)
df.to_csv(csv_path, index=False)
print(f"Lignes supprimées. Nouveau nombre de lignes : {len(df)}")
