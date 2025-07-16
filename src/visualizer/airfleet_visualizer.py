import streamlit as st
import pandas as pd

st.set_page_config(page_title="Visualisation Flotte Aérienne", layout="wide")
st.title("Visualisation du CSV - Flotte Aérienne")

csv_path = 'data/processed/fleet_data_2800.csv'

def load_data(path):
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement du CSV: {e}")
        return None

df = load_data(csv_path)

if df is not None:
    st.success(f"Données chargées: {len(df)} lignes")
    st.dataframe(df, use_container_width=True)
    st.markdown("---")
    st.subheader("Filtrer les colonnes")
    columns = st.multiselect("Sélectionnez les colonnes à afficher", options=list(df.columns), default=list(df.columns))
    st.dataframe(df[columns], use_container_width=True)
    st.markdown("---")
    st.subheader("Recherche par compagnie")
    airline = st.selectbox("Compagnie:", options=["Toutes"] + sorted(df['airline_name'].unique()))
    if airline != "Toutes":
        st.dataframe(df[df['airline_name'] == airline][columns], use_container_width=True)
else:
    st.error("Impossible de charger le fichier CSV.")
