import os
import pandas as pd

# Charger le CSV
input_path = 'data/processed/fleet_data_2800.csv'
output_path = 'data/processed/fleet_data_2800_clean.csv'

if not os.path.exists(input_path):
    print(f"File not found: {input_path}")
    exit(1)

df = pd.read_csv(input_path)

# Supprimer les colonnes 'airline_code' et 'status' si elles existent
cols_to_remove = [col for col in ['airline_code', 'status'] if col in df.columns]
df = df.drop(columns=cols_to_remove)

# Sauvegarder le nouveau CSV
df.to_csv(output_path, index=False)
print(f"Fichier nettoyé sauvegardé dans {output_path}")
