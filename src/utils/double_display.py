import pandas as pd
import os

def display_duplicates(csv_path):
    # Lecture du CSV
    df = pd.read_csv(csv_path)
    # Recherche des doublons sur toutes les colonnes
    duplicates = df[df.duplicated(keep=False)]
    if duplicates.empty:
        print("Aucun doublon trouvé.")
    else:
        print("Doublons trouvés :")
        print(duplicates)
        # Sauvegarde des doublons dans un nouveau CSV
        output_path = os.path.join(os.path.dirname(csv_path), "linkedin_list_merged_duplicates.csv")
        duplicates.to_csv(output_path, index=False)
        print(f"Doublons sauvegardés dans : {output_path}")

if __name__ == "__main__":
    # Modifier le chemin si besoin
    csv_file = r"c:/Users/henry/OneDrive/Documents/SkaiTech/skai-scrapping/data/raw/linkedin_list/linkedin_list_merged.csv"
    display_duplicates(csv_file)
