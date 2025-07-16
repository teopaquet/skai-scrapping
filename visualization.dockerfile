# Utilise une image officielle Python
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le code source
COPY src/visualizer/airfleet_visualizer.py ./
RUN mkdir -p data/processed
COPY data/processed/fleet_data_2800.csv data/processed/fleet_data_2800.csv

# Installer les dépendances
RUN pip install --no-cache-dir streamlit pandas

# Exposer le port Streamlit
EXPOSE 8501

# Commande pour lancer l'app
CMD ["streamlit", "run", "airfleet_visualizer.py", "--server.port=8501", "--server.address=0.0.0.0"]
