import os
import pandas as pd

# Charger le CSV
input_path = 'data/raw/airlines_name.csv'
output_path = 'data/raw/airlines_name_clean.csv'

if not os.path.exists(input_path):
    print(f"File not found: {input_path}")
    exit(1)

df = pd.read_csv(input_path)

# Supprimer les lignes NaN ou avec seulement des espaces
clean_df = df.dropna(subset=['companies_name'])
clean_df = clean_df[clean_df['companies_name'].str.strip() != ""]

# Sauvegarder le nouveau CSV avec séparateur virgule
import csv
clean_df.to_csv(output_path, index=False, sep=',', quoting=csv.QUOTE_ALL)
print(f"Fichier nettoyé sauvegardé dans {output_path}")
