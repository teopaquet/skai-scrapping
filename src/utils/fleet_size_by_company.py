import pandas as pd
import os


# Chemin absolu du fichier source
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/processed'))
aircraft_path = os.path.join(base_dir, 'fleet_data_2800.csv')
output_path = os.path.join(base_dir, 'fleet_size_by_company.csv')

# Charger le fichier aircraft
print(f"Lecture : {aircraft_path}")
df = pd.read_csv(aircraft_path)

# Normaliser le nom de la compagnie
import unicodedata
import re
def normalize(s):
    if pd.isna(s):
        return ''
    s = str(s).strip().lower()
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    s = re.sub(r'[^a-z0-9 ]', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

df['airline_name_norm'] = df['airline_name'].apply(normalize)


# Diagnostic : combien de compagnies uniques dans le fichier ?
print(f"Compagnies uniques (nom normalisé) dans le CSV : {df['airline_name_norm'].nunique()}")

# Calculer la taille de la flotte par compagnie (une ligne par compagnie distincte)
result = df.groupby('airline_name_norm').size().reset_index(name='fleet_size')

# Convertir la taille de la flotte en int (pas de décimales)
result['fleet_size'] = result['fleet_size'].astype(int)

# Sauvegarder le résultat (seulement nom normalisé et taille de flotte)
result.to_csv(output_path, index=False)
print(f"Fichier créé : {output_path}")
print(f"Nombre de compagnies uniques : {result.shape[0]}")
