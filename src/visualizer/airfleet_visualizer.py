import streamlit as st
import pandas as pd

st.set_page_config(page_title="Visualisation Flotte Aérienne", layout="wide")

st.title("Visualisation des Données Aériennes")


# Chemins des CSVs
csv_path = 'data/processed/fleet_data_2800.csv'
linkedin_csv_path = 'data/raw/linkedin_list/linkedin_list_merged_with_fleet.csv'

def load_data(path):
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement du CSV: {e}")
        return None



# --- Navigation par onglets ---
tab1, tab2 = st.tabs(["Flotte Aérienne", "LinkedIn + Fleet Size"])

with tab1:
    df = load_data(csv_path)
    if df is not None:
        # Supprimer les colonnes inutiles
        df = df.drop(columns=[col for col in ['airline_code', 'status'] if col in df.columns])

        st.success(f"Données chargées: {len(df)} lignes")
        st.dataframe(df, use_container_width=True)
        st.markdown("---")
        st.subheader("Filtrer les colonnes")
        columns = st.multiselect("Sélectionnez les colonnes à afficher", options=list(df.columns), default=list(df.columns), key="columns_fleet")
        st.dataframe(df[columns], use_container_width=True)
        st.markdown("---")
        st.subheader("Recherche par compagnie")
        airline = st.selectbox("Compagnie:", options=["Toutes"] + sorted(df['airline_name'].unique()), key="airline_fleet")
        if airline != "Toutes":
            st.dataframe(df[df['airline_name'] == airline][columns], use_container_width=True)
    else:
        st.error("Impossible de charger le fichier CSV flotte aérienne.")

with tab2:
    linkedin_df = load_data(linkedin_csv_path)
    if linkedin_df is not None:
        st.success(f"Données LinkedIn chargées: {len(linkedin_df)} lignes")

        st.markdown("---")
        st.subheader("Filtres et tri LinkedIn")
        columns_options = list(linkedin_df.columns)
        default_columns = [col for col in linkedin_df.columns]
        with st.container():
            col1, col2, col3, col4 = st.columns([2,2,2,2])
            with col1:
                linkedin_columns = st.multiselect(
                    "Colonnes à afficher",
                    options=columns_options,
                    default=default_columns,
                    key="columns_linkedin"
                )
            with col2:
                # Min/max fleet_size
                if "fleet_size" in linkedin_columns and pd.api.types.is_numeric_dtype(linkedin_df["fleet_size"]):
                    min_val, max_val = int(linkedin_df["fleet_size"].min()), int(linkedin_df["fleet_size"].max())
                    min_input = st.number_input("Min fleet_size", min_value=min_val, max_value=max_val, value=min_val, key="min_fleet_size", step=1, format="%d")
                    max_input = st.number_input("Max fleet_size", min_value=min_val, max_value=max_val, value=max_val, key="max_fleet_size", step=1, format="%d")
                else:
                    min_input, max_input = None, None
            with col3:
                sort_col = st.selectbox("Trier par colonne", options=linkedin_columns, key="sort_col_linkedin")
            with col4:
                sort_order = st.radio("Ordre de tri", options=["Croissant", "Décroissant"], horizontal=True, key="sort_order_linkedin")

        # Filtrage par valeur sur chaque colonne sélectionnée
        filter_dict = {}
        for col in linkedin_columns:
            if col == "fleet_size" and pd.api.types.is_numeric_dtype(linkedin_df[col]) and min_input is not None and max_input is not None:
                filter_dict[col] = (int(min_input), int(max_input))
            elif pd.api.types.is_numeric_dtype(linkedin_df[col]):
                min_val, max_val = float(linkedin_df[col].min()), float(linkedin_df[col].max())
                filter_dict[col] = st.slider(f"Filtrer {col}", min_val, max_val, (min_val, max_val), key=f"slider_{col}")
            else:
                unique_vals = linkedin_df[col].dropna().unique()
                if len(unique_vals) < 50:
                    selected_vals = st.multiselect(f"Filtrer {col}", options=sorted(unique_vals), default=list(unique_vals), key=f"filter_{col}")
                    filter_dict[col] = selected_vals

        filtered_df = linkedin_df.copy()
        for col, filt in filter_dict.items():
            if col == "fleet_size" and pd.api.types.is_numeric_dtype(filtered_df[col]) and min_input is not None and max_input is not None:
                filtered_df = filtered_df[(filtered_df[col] >= filt[0]) & (filtered_df[col] <= filt[1])]
            elif pd.api.types.is_numeric_dtype(filtered_df[col]):
                filtered_df = filtered_df[(filtered_df[col] >= filt[0]) & (filtered_df[col] <= filt[1])]
            else:
                filtered_df = filtered_df[filtered_df[col].isin(filt)]

        ascending = sort_order == "Croissant"
        filtered_df = filtered_df.sort_values(by=sort_col, ascending=ascending)

        # Édition du DataFrame (ajout/suppression/édition)
        st.markdown("#### Modifier ou ajouter des liens LinkedIn")
        edited_df = st.data_editor(
            filtered_df[linkedin_columns],
            num_rows="dynamic",
            use_container_width=True,
            key="linkedin_editor"
        )

        # Sauvegarde intelligente : on fusionne les modifications dans le DataFrame d'origine
        if st.button("Enregistrer les modifications"):
            try:
                # On met à jour linkedin_df avec les valeurs éditées (en se basant sur l'index d'origine)
                for idx, row in edited_df.iterrows():
                    # On retrouve l'index d'origine dans linkedin_df (par exemple via company_name + linkedin_url)
                    mask = (
                        (linkedin_df['company_name'] == row.get('company_name')) &
                        (linkedin_df['linkedin_url'] == row.get('linkedin_url'))
                    )
                    if mask.any():
                        for col in linkedin_columns:
                            linkedin_df.loc[mask, col] = row[col]
                linkedin_df.to_csv(linkedin_csv_path, index=False)
                st.success("Modifications enregistrées avec succès !")
            except Exception as e:
                st.error(f"Erreur lors de la sauvegarde : {e}")

        st.markdown("---")
        st.subheader("Recherche par compagnie LinkedIn")
        if 'company_name' in edited_df.columns:
            linkedin_airline = st.selectbox(
                "Compagnie:",
                options=["Toutes"] + sorted(edited_df['company_name'].dropna().unique()),
                key="airline_linkedin"
            )
            if linkedin_airline != "Toutes":
                filtered = edited_df[edited_df['company_name'] == linkedin_airline][linkedin_columns]
                st.dataframe(filtered, use_container_width=True)
        else:
            st.info("Colonne 'company_name' absente des données.")
    else:
        st.error("Impossible de charger le fichier LinkedIn + Fleet.")
