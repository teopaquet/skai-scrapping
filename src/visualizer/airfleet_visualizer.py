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

        # Ajout d'une colonne cliquable pour le nom de la compagnie
        def make_link(row):
            if pd.notna(row['linkedin_url']) and pd.notna(row['company_name']):
                return f'<a href="{row["linkedin_url"]}" target="_blank">{row["company_name"]}</a>'
            elif pd.notna(row['company_name']):
                return row['company_name']
            else:
                return ""
        linkedin_df['company_name_link'] = linkedin_df.apply(make_link, axis=1)

        st.markdown("---")
        st.subheader("Filtrer les colonnes LinkedIn")
        # On ajoute la colonne cliquable dans les options
        columns_options = list(linkedin_df.columns) + ['company_name_link']
        default_columns = [col for col in linkedin_df.columns]
        linkedin_columns = st.multiselect("Sélectionnez les colonnes à afficher (LinkedIn)", options=columns_options, default=default_columns, key="columns_linkedin")

        # Si la colonne cliquable est sélectionnée, on affiche en HTML
        if 'company_name_link' in linkedin_columns:
            st.markdown("<b>Nom de la compagnie (cliquable)</b>", unsafe_allow_html=True)
            st.write(linkedin_df[linkedin_columns].to_html(escape=False, index=False), unsafe_allow_html=True)
        else:
            st.dataframe(linkedin_df[linkedin_columns], use_container_width=True)

        st.markdown("---")
        st.subheader("Recherche par compagnie LinkedIn")
        linkedin_airline = st.selectbox("Compagnie:", options=["Toutes"] + sorted(linkedin_df['company_name'].dropna().unique()), key="airline_linkedin")
        if linkedin_airline != "Toutes":
            filtered = linkedin_df[linkedin_df['company_name'] == linkedin_airline][linkedin_columns]
            if 'company_name_link' in linkedin_columns:
                st.write(filtered.to_html(escape=False, index=False), unsafe_allow_html=True)
            else:
                st.dataframe(filtered, use_container_width=True)
    else:
        st.error("Impossible de charger le fichier LinkedIn + Fleet.")
