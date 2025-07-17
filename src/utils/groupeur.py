import os
import pandas as pd

def main():
    base_dir = os.path.join(os.path.dirname(__file__), '../../data/raw/linkedin_list')
    all_dfs = []
    for i in range(1, 30):
        file_path = os.path.join(base_dir, f"{i}.xlsx")
        if os.path.exists(file_path):
            try:
                xls = pd.ExcelFile(file_path)
                for sheet_name in xls.sheet_names:
                    df = pd.read_excel(xls, sheet_name=sheet_name)
                    print(f"{file_path} - Feuille: {sheet_name} - Lignes lues: {len(df)}")
                    if df.empty:
                        print(f"ATTENTION: {file_path} - {sheet_name} est vide.")
                    all_dfs.append(df)
            except Exception as e:
                print(f"Erreur lors de la lecture de {file_path}: {e}")
        else:
            print(f"Fichier non trouvé: {file_path}")
    if all_dfs:
        merged_df = pd.concat(all_dfs, ignore_index=True)
        print(f"Nombre de colonnes détecté: {len(merged_df.columns)}")
        # Définir des noms de colonnes cohérents selon le nombre de colonnes
        base_names = ["company_name", "linkedin_url", "description", "col4", "col5", "col6", "col7", "col8", "col9", "col10"]
        n_cols = len(merged_df.columns)
        if n_cols <= len(base_names):
            merged_df.columns = base_names[:n_cols]
        else:
            merged_df.columns = base_names + [f"col{i}" for i in range(len(base_names)+1, n_cols+1)]
        # Décaler les valeurs des colonnes 4,5,6 vers 1,2,3 si les 3 premières sont vides
        mask = merged_df[["company_name", "linkedin_url", "description"]].isnull().all(axis=1)
        for c_from, c_to in zip(["col4", "col5", "col6"], ["company_name", "linkedin_url", "description"]):
            merged_df.loc[mask, c_to] = merged_df.loc[mask, c_from]
            merged_df.loc[mask, c_from] = None
        # Supprimer les colonnes col4, col5, col6 si elles existent
        cols_to_drop = [col for col in ["col4", "col5", "col6"] if col in merged_df.columns]
        if cols_to_drop:
            merged_df = merged_df.drop(columns=cols_to_drop)
            print(f"Colonnes supprimées : {cols_to_drop}")

        output_path = os.path.join(base_dir, "linkedin_list_merged.csv")
        merged_df.to_csv(output_path, index=False)
        print(f"Fichier fusionné sauvegardé sous: {output_path}")
        n_linkedin = merged_df[merged_df["linkedin_url"].notna() & (merged_df["linkedin_url"] != "")].shape[0]
        print(f"Nombre de lignes avec un linkedin_url non vide : {n_linkedin}")
    else:
        print("Aucun fichier à fusionner.")

if __name__ == "__main__":
    main()
