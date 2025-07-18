import pandas as pd
import os

# Chemin du fichier à nettoyer (toujours relatif au script)
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, '../../data/raw/linkedin_list/linkedin_list_merged_with_fleet.csv')
csv_path = os.path.abspath(csv_path)
print(csv_path)

# Charger le CSV
df = pd.read_csv(csv_path)

# Supprimer les doublons stricts (toutes colonnes identiques)
df_clean = df.drop_duplicates()

# Réécrire le fichier (même nom, écrasement)
df_clean.to_csv(csv_path, index=False)
print(f"Doublons supprimés. Nouveau nombre de lignes : {len(df_clean)}")
