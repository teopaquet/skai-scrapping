
def normalize(s):
    if pd.isna(s):
        return ''
    s = str(s).strip().lower()
    # Supprimer les accents
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    # Supprimer caractères spéciaux sauf lettres, chiffres et espaces
    s = re.sub(r'[^a-z0-9 ]', '', s)
    # Remplacer espaces multiples par un seul
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

import pandas as pd
import os
import unicodedata
import re

# Chemins absolus depuis ce script
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/raw'))
linkedin_path = os.path.join(base_dir, 'linkedin_list', 'linkedin_list_merged.csv')
fleet_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/processed/fleet_size_by_company.csv'))
output_path = os.path.join(base_dir, 'linkedin_list', 'linkedin_list_merged_with_fleet.csv')

# Charger les données
linkedin_df = pd.read_csv(linkedin_path)
fleet_df = pd.read_csv(fleet_path)

# Fonction de normalisation
def normalize(s):
    if pd.isna(s):
        return ''
    s = str(s).strip().lower()
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    s = re.sub(r'[^a-z0-9 ]', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

# Ajouter la colonne normalisée pour le merge
linkedin_df['company_name_norm'] = linkedin_df['company_name'].apply(normalize)


# Fusionner sur le nom normalisé
merged = pd.merge(linkedin_df, fleet_df, left_on='company_name_norm', right_on='airline_name_norm', how='left')


# Nettoyer le résultat (on garde les colonnes linkedin + fleet_size)
cols = [col for col in linkedin_df.columns if col != 'company_name_norm'] + ['fleet_size']
merged = merged[cols]

# Convertir fleet_size en int (mettre 0 si NaN)
merged['fleet_size'] = merged['fleet_size'].fillna(0).astype(int)

# Exporter le résultat
merged.to_csv(output_path, index=False)
print(f"Fichier créé : {output_path}")
print(f"Nombre de compagnies avec fleet_size renseigné : {merged['fleet_size'].notna().sum()}")
