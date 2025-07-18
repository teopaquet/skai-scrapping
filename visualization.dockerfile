# Utilise une image officielle Python
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app


# Copier le code source
COPY src/visualizer/airfleet_visualizer.py ./

# Créer les dossiers nécessaires
RUN mkdir -p data/processed && mkdir -p data/raw/linkedin_list

# Copier les CSVs nécessaires
COPY data/processed/fleet_data_2800.csv data/processed/fleet_data_2800.csv
COPY data/raw/linkedin_list/linkedin_list_merged_with_fleet.csv data/raw/linkedin_list/linkedin_list_merged_with_fleet.csv

# Copier le requirements.txt
COPY requirements.txt ./

# Installer toutes les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port Streamlit
EXPOSE 8501

# Commande pour lancer l'app
CMD ["streamlit", "run", "airfleet_visualizer.py", "--server.port=8501", "--server.address=0.0.0.0"]
