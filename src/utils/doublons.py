import pandas as pd
import os

# Chemin du fichier à nettoyer
csv_path = '../../data/processed/fleet_data_2800.csv'
print(os.path.abspath(csv_path))

# Charger le CSV
df = pd.read_csv(csv_path)

# Supprimer les doublons stricts (toutes colonnes identiques)
df_clean = df.drop_duplicates()

# Réécrire le fichier (même nom, écrasement)
df_clean.to_csv(csv_path, index=False)
print(f"Doublons supprimés. Nouveau nombre de lignes : {len(df_clean)}")
