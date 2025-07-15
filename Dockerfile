# Utilise une image Python officielle
FROM python:3.11-slim

# Définit le répertoire de travail
WORKDIR /app

# Copie les fichiers de dépendances
COPY requirements.txt ./

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie le code source
COPY src/ ./src/

# Copie les autres dossiers utiles
COPY data/ ./data/
COPY .env ./

# Commande par défaut : lance le scraper
CMD ["python", "src/scrapers/scraper_flightradar24.py", "1"]
