# 🛩️ Skai-Scrapping

## ✈️ Présentation du projet

Skai-Scrapping est une suite d’outils pour l’extraction, l’analyse et la visualisation de données sur les compagnies aériennes et leur flotte, à partir de sources publiques (FlightRadar24, LinkedIn, etc.). Le projet inclut des scripts de scraping, de traitement de données, d’analyse, ainsi qu’une interface web moderne pour l’exploration des résultats.

## ⚙️ Installation et prérequis

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/teopaquet/skai-scrapping
   ```
2. **Installer les dépendances Python**
   ```bash
   pip install -r requirements.txt
   ```
3. **Installer Node.js** (pour l’interface web)
4. **Configurer les accès Firebase et variables d’environnement** (voir `.env`)

## 📁 Structure des dossiers

- `src/` : scripts principaux (scraping, analyse, utils, visualisation)
- `data/` : données brutes, traitées, exports
- `src/interface/auth-material-ui/` : interface web (React + Vite)

## 🧩 Explication des scripts principaux

### 🧮 Analyseurs

- **`analyzers/analyse_airlines.py`** : Analyse les données CSV des compagnies aériennes extraites de FlightRadar24, affiche le nom, le sigle et le nombre d’avions par compagnie, calcule des statistiques globales.
- **`analyzers/analyzer_fleet_data.py`** : Classe d’analyse avancée des flottes (statistiques, top compagnies/types, export CSV, visualisations avec matplotlib/seaborn, interface Streamlit).

### 🤖 Scrapers

- **`scrapers/scraper_flightradar24.py`** : Scraping automatisé des flottes sur FlightRadar24 (récupération des détails, gestion des retries, sauvegarde intermédiaire, export JSON/CSV, envoi Telegram).
- **`scrapers/main.py`** : Interface graphique Tkinter pour lancer le scraping LinkedIn selon des critères (taille de flotte, rôle, etc.).
- **`scrapers/linkedin_scraper.py`** : (non détaillé ici) Scraping ciblé de profils LinkedIn selon les compagnies et rôles.

### 🛠️ Utils (traitement de données)

- **`utils/csvtojson.py`** : Conversion de CSV en JSON.
- **`utils/double_display.py`** : Détection et export des doublons dans un CSV.
- **`utils/filtrer.py`** : Filtrage des compagnies selon des mots-clés (exclusion écoles, armée, etc.).
- **`utils/fixer.py`** : Correction des tailles de flotte dans les données LinkedIn à partir des données réelles.
- **`utils/fleet_size_by_company.py`** : Calcul de la taille de flotte par compagnie (normalisation des noms).
- **`utils/fusion.py`** : Fusion des données LinkedIn et flotte par nom de compagnie normalisé.
- **`utils/groupeur.py`** : Agrégation de plusieurs fichiers Excel LinkedIn en un seul DataFrame.
- **`utils/pays.py`** : Ajout du pays d’immatriculation à chaque avion à partir d’un mapping.
- **`utils/remove_columns.py`** : Suppression de colonnes inutiles dans les CSV.
- **`utils/remove_useless.py`** : Suppression de lignes inutiles dans les CSV.
- **`utils/remove_void.py`** : Nettoyage des lignes vides ou incomplètes.
- **`utils/split.py`** : Découpage d’un gros CSV en petits fichiers.

## 🖥️ Interface web Refine (React + Vite)

L’interface web, située dans `src/interface/auth-material-ui/`, permet d’explorer les données traitées via une interface moderne (React, Material UI, Vite). Elle propose :

- Authentification sécurisée (Material UI, gestion des rôles)
- Visualisation des flottes, des profils LinkedIn, des statistiques
- Filtres avancés, recherche, export CSV
- Intégration directe avec la base de données Firebase Realtime pour la synchronisation des données et la gestion des utilisateurs

### 🔥 Fonctionnement avec Firebase Realtime Database

La base de données Firebase Realtime est utilisée pour :

- Stocker les résultats de scraping : Linkedin_list_with_country et fleet_data2800
- Permettre d'associer un ou plusieurs tags à une compagnie aérienne
- Permettre la mise à jour en temps réel de l’interface lors de l’ajout/modification de données

## 📝 Exemples d’utilisation

### 🚀 Lancer le scraping Flightradar24

```bash
python src/scrapers/scraper_flightradar24.py
```

### 🌐 Lancer l’interface web

```bash
cd src/interface/auth-material-ui
npm install
npm run dev
```

## 👨‍💻 Auteurs et contact

Projet développé par SkaiTech

# Créer une instance du scraper

scraper = FlightRadar24Scraper()

# Lancer le scraping

data = scraper.scrape_fleet_data()
`

### 2. Analyse des données

`python
from src.analyzers.analyzer_fleet_data import FleetDataAnalyzer

# Créer une instance de l'analyseur

analyzer = FleetDataAnalyzer()

# Générer un rapport complet

analyzer.generate_summary_report()
analyzer.analyze_aircraft_types()
analyzer.find_aircraft_specialists()

# Créer des visualisations

analyzer.create_visualizations()

# Exporter les résultats

analyzer.export_analysis_to_csv()
`

## 📊Données actuelles

Le système analyse actuellement :

- **884 avions individuels** enregistrés
- **34 compagnies aériennes** différentes
- **177 types d'avions** distincts
- **Couverture géographique** : Mondiale

### 🏆 Top compagnies par taille de flotte :

1. **Aeroflot** - 169 avions (97.04% de couverture)
2. **Aeromexico** - 125 avions (66.4% de couverture)
3. **AeroGuard Flight Training Center** - 113 avions (98.23% de couverture)

### ✈️ Types d'avions les plus communs :

1. **Airbus A320-214** - 79 avions
2. **Piper Archer III** - 48 avions
3. **Airbus A321-211** - 32 avions

## ⚙️Configuration

Les fichiers de données sont organisés comme suit :

- **Données brutes** : data/raw/ - Données directement scrapées
- **Données traitées** : data/processed/ - Données nettoyées et formatées
- **Exports** : data/exports/ - Analyses et rapports CSV
- **Visualisations** : data/visualizations/ - Graphiques et charts

## 📚 Documentation

- [Guide d&#39;installation détaillé](docs/installation.md)
- [Guide d&#39;utilisation](docs/usage.md)
- [API Reference](docs/api.md)
- [Exemples avancés](examples/)

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
