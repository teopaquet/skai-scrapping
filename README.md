# 🛩️ Aircraft Fleet Data Scraper & Analyzer

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/teopaquet/skai-scrapping.svg)](https://github.com/teopaquet/skai-scrapping/stargazers)

Un système complet de collecte et d'analyse de données de flottes aériennes provenant de diverses sources publiques. Ce projet permet de scraper, analyser et visualiser les informations sur les avions individuels et les flottes des compagnies aériennes.

## 🚀 Fonctionnalités principales

- **🔍 Scraping automatisé** : Collecte de données depuis FlightRadar24 et d'autres sources
- **📊 Analyse avancée** : Statistiques détaillées sur les flottes et types d'avions
- **📈 Visualisations** : Graphiques et charts interactifs
- **📋 Export multi-format** : CSV, JSON, graphiques PNG
- **🔄 Données en temps réel** : Mise à jour automatique des informations

## 📁 Structure du projet


skai-scrapping/
├── src/                          # Code source principal
│   ├── scrapers/                 # Scripts de scraping
│   │   └── scraper_flightradar24.py
│   ├── analyzers/                # Outils d'analyse
│   │   ├── analyzer_fleet_data.py
│   │   └── analyse_airlines.py
│   └── utils/                    # Utilitaires communs
├── data/                         # Données collectées
│   ├── raw/                      # Données brutes
│   │   ├── individual_aircraft.csv
│   │   └── flightradar24.csv
│   ├── processed/                # Données traitées
│   │   ├── fleet_data_complete.json
│   │   └── fleet_data_detailed.csv
│   ├── exports/                  # Fichiers d'export
│   │   ├── individual_aircraft_analysis_summary.csv
│   │   └── individual_aircraft_detailed_analysis.csv
│   └── visualizations/           # Graphiques et charts
│       └── individual_aircraft_analysis_charts.png
├── docs/                         # Documentation
├── examples/                     # Exemples d'utilisation
└── requirements.txt              # Dépendances Python


## 🛠️ Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- 
# Cloner le repository
git clone https://github.com/teopaquet/skai-scrapping.git
cd skai-scrapping

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'analyseur principal
python src/analyzers/analyzer_fleet_data.py
`

## 📊 Utilisation

### 1. Scraping de données FlightRadar24

`python
from src.scrapers.scraper_flightradar24 import FlightRadar24Scraper

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

## 📈 Données actuelles

Le système analyse actuellement :
- **884 avions individuels** enregistrés
- **34 compagnies aériennes** différentes
- **177 types d'avions** distincts
- **Couverture géographique** : Mondiale

### Top compagnies par taille de flotte :
1. **Aeroflot** - 169 avions (97.04% de couverture)
2. **Aeromexico** - 125 avions (66.4% de couverture)
3. **AeroGuard Flight Training Center** - 113 avions (98.23% de couverture)

### Types d'avions les plus communs :
1. **Airbus A320-214** - 79 avions
2. **Piper Archer III** - 48 avions
3. **Airbus A321-211** - 32 avions

## 🔧 Configuration

Les fichiers de données sont organisés comme suit :
- **Données brutes** : data/raw/ - Données directement scrapées
- **Données traitées** : data/processed/ - Données nettoyées et formatées
- **Exports** : data/exports/ - Analyses et rapports CSV
- **Visualisations** : data/visualizations/ - Graphiques et charts

## 📚 Documentation

- [Guide d'installation détaillé](docs/installation.md)
- [Guide d'utilisation](docs/usage.md)
- [API Reference](docs/api.md)
- [Exemples avancés](examples/)

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créez votre branche feature (git checkout -b feature/AmazingFeature)
3. Committez vos changements (git commit -m 'Add some AmazingFeature')
4. Push vers la branche (git push origin feature/AmazingFeature)
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## ⚠️ Disclaimer

Ce projet est destiné à des fins éducatives et de recherche. Respectez les conditions d'utilisation des sites web scrapés et les réglementations locales sur la collecte de données.

## 📞 Contact

**Téo Paquet** - [@teopaquet](https://github.com/teopaquet)

Lien du projet : [https://github.com/teopaquet/skai-scrapping](https://github.com/teopaquet/skai-scrapping)

## 🙏 Remerciements

- [FlightRadar24](https://www.flightradar24.com/) pour les données en temps réel
- [Pandas](https://pandas.pydata.org/) pour l'analyse de données
- [Matplotlib](https://matplotlib.org/) pour les visualisations
- La communauté open source pour les outils et bibliothèques

---

⭐ N'hésitez pas à donner une étoile au projet si vous le trouvez utile !
