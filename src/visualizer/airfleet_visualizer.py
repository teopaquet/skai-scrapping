
import streamlit as st
import pandas as pd
from streamlit_extras.badges import badge


st.set_page_config(page_title="Visualisation Flotte Aérienne", layout="wide", page_icon="✈️")

st.markdown("""
<style>
.stApp {
    background: #fff !important;
    color: #111 !important;
}
.blue-header {
    color: #111;
    font-size: 2.5rem;
    font-weight: bold;
    margin-bottom: 0.5em;
    letter-spacing: 1px;
}
.blue-subheader {
    color: #1a237e;
    font-size: 1.3rem;
    font-weight: 600;
    margin-top: 1em;
    margin-bottom: 0.5em;
}
.stButton>button {
    background-color: #1a237e;
    color: white;
    border-radius: 8px;
    border: none;
    font-weight: 600;
    transition: 0.2s;
}
.stButton>button:hover {
    background-color: #3949ab;
    color: #fff;
}
.stDataFrame {
    border-radius: 10px;
    border: 1px solid #1a237e;
}
/* Onglets Streamlit */
div[data-testid="stTabs"] > div > div {
    background: #1a237e !important;
    border-radius: 8px 8px 0 0;
}
div[data-testid="stTabs"] button {
    color: #fff !important;
    background: #1a237e !important;
    border: none !important;
    font-weight: 600;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    background: #3949ab !important;
    color: #fff !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="blue-header">✈️ Visualisation des Données Aériennes</div>', unsafe_allow_html=True)
badge(type="github", name="teopaquet/skai-scrapping")


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

        st.info(f"<span style='color:#1976d2;font-weight:bold;'>📊 Données chargées: {len(df)} lignes</span>", icon="ℹ️", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown("---")
        st.markdown('<div class="blue-subheader">🔎 Filtrer les colonnes</div>', unsafe_allow_html=True)
        columns = st.multiselect("Sélectionnez les colonnes à afficher", options=list(df.columns), default=list(df.columns), key="columns_fleet")
        st.dataframe(df[columns], use_container_width=True, hide_index=True)
        st.markdown("---")
        st.markdown('<div class="blue-subheader">🏢 Recherche par compagnie</div>', unsafe_allow_html=True)
        airline = st.selectbox("Compagnie:", options=["Toutes"] + sorted(df['airline_name'].unique()), key="airline_fleet")
        if airline != "Toutes":
            st.dataframe(df[df['airline_name'] == airline][columns], use_container_width=True, hide_index=True)
    else:
        st.error("Impossible de charger le fichier CSV flotte aérienne.")

with tab2:
    linkedin_df = load_data(linkedin_csv_path)
    if linkedin_df is not None:
        st.info(f"<span style='color:#1976d2;font-weight:bold;'>🔗 Données LinkedIn chargées: {len(linkedin_df)} lignes</span>", icon="ℹ️", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div class="blue-subheader">🔎 Filtrer les colonnes LinkedIn</div>', unsafe_allow_html=True)
        columns_options = list(linkedin_df.columns)
        default_columns = [col for col in linkedin_df.columns]
        linkedin_columns = st.multiselect(
            "Sélectionnez les colonnes à afficher (LinkedIn)",
            options=columns_options,
            default=default_columns,
            key="columns_linkedin"
        )

        # Filtrage par valeur sur chaque colonne sélectionnée
        filter_dict = {}
        for col in linkedin_columns:
            if col == "fleet_size" and pd.api.types.is_numeric_dtype(linkedin_df[col]):
                min_val, max_val = int(linkedin_df[col].min()), int(linkedin_df[col].max())
                min_input = st.number_input(f"Valeur minimale pour {col}", min_value=min_val, max_value=max_val, value=min_val, key=f"min_{col}", step=1, format="%d")
                max_input = st.number_input(f"Valeur maximale pour {col}", min_value=min_val, max_value=max_val, value=max_val, key=f"max_{col}", step=1, format="%d")
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
            if col == "fleet_size" and pd.api.types.is_numeric_dtype(filtered_df[col]):
                filtered_df = filtered_df[(filtered_df[col] >= filt[0]) & (filtered_df[col] <= filt[1])]
            elif pd.api.types.is_numeric_dtype(filtered_df[col]):
                filtered_df = filtered_df[(filtered_df[col] >= filt[0]) & (filtered_df[col] <= filt[1])]
            else:
                filtered_df = filtered_df[filtered_df[col].isin(filt)]

        # Tri des colonnes
        st.markdown('<div class="blue-subheader">↕️ Tri des colonnes</div>', unsafe_allow_html=True)
        sort_col = st.selectbox("Trier par colonne", options=linkedin_columns, key="sort_col_linkedin")
        sort_order = st.radio("Ordre de tri", options=["Croissant", "Décroissant"], horizontal=True, key="sort_order_linkedin")
        ascending = sort_order == "Croissant"
        filtered_df = filtered_df.sort_values(by=sort_col, ascending=ascending)

        # Édition du DataFrame (ajout/suppression/édition)
        st.markdown('<div class="blue-subheader">✏️ Modifier ou ajouter des liens LinkedIn</div>', unsafe_allow_html=True)
        edited_df = st.data_editor(
            filtered_df[linkedin_columns],
            num_rows="dynamic",
            use_container_width=True,
            key="linkedin_editor"
        )

        # Sauvegarde si modifié
        if st.button("💾 Enregistrer les modifications"):
            try:
                # On sauvegarde tout le DataFrame édité (tu peux adapter pour ne sauvegarder que la colonne linkedin_url si besoin)
                edited_df.to_csv(linkedin_csv_path, index=False)
                st.success("✅ Modifications enregistrées avec succès !")
            except Exception as e:
                st.error(f"❌ Erreur lors de la sauvegarde : {e}")

        st.markdown("---")
        st.markdown('<div class="blue-subheader">🏢 Recherche par compagnie LinkedIn</div>', unsafe_allow_html=True)
        if 'company_name' in edited_df.columns:
            linkedin_airline = st.selectbox(
                "Compagnie:",
                options=["Toutes"] + sorted(edited_df['company_name'].dropna().unique()),
                key="airline_linkedin"
            )
            if linkedin_airline != "Toutes":
                filtered = edited_df[edited_df['company_name'] == linkedin_airline][linkedin_columns]
                st.dataframe(filtered, use_container_width=True, hide_index=True)
        else:
            st.info("ℹ️ Colonne 'company_name' absente des données.")
    else:
        st.error("Impossible de charger le fichier LinkedIn + Fleet.")
