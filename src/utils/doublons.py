import pandas as pd
import os

# Chemin du fichier à nettoyer (toujours relatif au script)
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, '../../data/raw/airlines_name_clean.csv')
csv_path = os.path.abspath(csv_path)
print(csv_path)

# Charger le CSV
df = pd.read_csv(csv_path)


# Trouver les doublons stricts (toutes colonnes identiques)
duplicates = df[df.duplicated(keep=False)]
if not duplicates.empty:
    print("Lignes supprimées :")
    print(duplicates)
else:
    print("Aucune ligne supprimée.")

# Supprimer les doublons stricts
df_clean = df.drop_duplicates()

# Réécrire le fichier (même nom, écrasement)
df_clean.to_csv(csv_path, index=False)
print(f"Doublons supprimés. Nouveau nombre de lignes : {len(df_clean)}")
