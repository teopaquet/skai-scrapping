# FlightRadar24 Scraper & Fleet Analyzer 🛩️

Un scraper Python complet pour récupérer des données de vols depuis FlightRadar24 et analyser les flottes des compagnies aériennes en temps réel.

## 🚀 Fonctionnalités

### Scraping de base
- **Récupération de vols par zone géographique** : Obtenez tous les vols dans une zone délimitée
- **Recherche de vols** : Recherchez par numéro de vol, compagnie aérienne, etc.
- **Monitoring d'aéroports** : Arrivées et départs en temps réel
- **Suivi de vols spécifiques** : Détails complets d'un vol donné
- **Monitoring en temps réel** : Surveillance continue avec sauvegarde
- **Export de données** : Sauvegarde en CSV avec timestamps

### 🆕 Analyse de flottes
- **Analyse des flottes par compagnie** : Types et quantités d'avions par compagnie aérienne
- **Identification automatique** : Basée sur les immatriculations uniques
- **Rapports détaillés** : Export CSV, JSON et rapports texte
- **Visualisations graphiques** : Graphiques interactifs et analyses comparatives
- **Monitoring étendu** : Collecte sur plusieurs cycles pour plus de précision

## 📦 Installation

### 1. Cloner le projet

```bash
git clone <repository-url>
cd FlightRadarScrap
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Démarrage rapide

```bash
python start.py
```

## 🛠️ Utilisation

### Démarrage rapide avec menu interactif

```bash
python start.py
```

Le script `start.py` vous guide à travers toutes les options disponibles :
- Analyse rapide des flottes (5 minutes)
- Analyse complète des flottes (15-30 minutes)  
- Visualisation des données existantes
- Exemples de base du scraper

### Analyse de flottes des compagnies aériennes

```python
from main import FlightRadar24Scraper

scraper = FlightRadar24Scraper()

# Analyse rapide (5 minutes)
fleet_data = scraper.get_airline_fleet_analysis(duration_minutes=5)

# Afficher le résumé
scraper.print_fleet_summary(fleet_data)

# Sauvegarder les données
scraper.save_fleet_analysis_to_csv(fleet_data)
```

### Script dédié à l'analyse de flottes

```bash
python fleet_analyzer.py
```

Ce script spécialisé offre :
- Choix de zones d'analyse prédéfinies
- Analyse comparative entre zones
- Rapports détaillés automatiques
- Paramètres personnalisables

### Visualisation des données

```bash
python fleet_visualizer.py
```

Génère automatiquement :
- Graphiques des flottes par compagnie
- Distribution des types d'avions
- Analyse des constructeurs
- Corrélations taille vs diversité

## 🛠️ Utilisation

### Utilisation basique

```python
from main import FlightRadar24Scraper

# Créer une instance du scraper
scraper = FlightRadar24Scraper()

# Définir une zone géographique (Paris)
bounds = {
    'north': 49.0,
    'south': 48.5,
    'east': 2.7,
    'west': 2.0
}

# Récupérer les vols dans la zone
raw_data = scraper.get_flights_in_bounds(bounds)
flights = scraper.parse_flights_data(raw_data)

print(f"Trouvé {len(flights)} vols")
```

### Recherche de vols

```python
# Rechercher par compagnie
results = scraper.search_flights("Air France")

# Rechercher par numéro de vol
results = scraper.search_flights("AF447")
```

### Monitoring d'aéroport

```python
# Arrivées à Charles de Gaulle
arrivals = scraper.get_airport_arrivals("CDG")

# Départs d'Orly
departures = scraper.get_airport_departures("ORY")
```

### Monitoring en temps réel

```python
# Surveiller pendant 10 minutes avec des intervalles de 30 secondes
flights_data = scraper.monitor_flights_realtime(
    bounds=bounds,
    duration_minutes=10,
    interval_seconds=30
)
```

### Sauvegarde des données

```python
# Sauvegarder en CSV
filename = scraper.save_to_csv(flights, "mes_vols.csv")
```

## 📊 Structure des données

Chaque vol retourné contient les informations suivantes :

```python
{
    'flight_id': 'Identifiant unique',
    'callsign': 'Indicatif radio',
    'latitude': 'Latitude actuelle',
    'longitude': 'Longitude actuelle',
    'track': 'Cap en degrés',
    'altitude': 'Altitude en pieds',
    'speed': 'Vitesse en nœuds',
    'aircraft_type': 'Type d\'aéronef',
    'registration': 'Immatriculation',
    'origin': 'Aéroport de départ',
    'destination': 'Aéroport d\'arrivée',
    'flight_number': 'Numéro de vol',
    'airline_icao': 'Code ICAO compagnie',
    'on_ground': 'Au sol (1) ou en vol (0)'
}
```

## 🌍 Zones prédéfinies

Le fichier `config.py` contient des zones géographiques prêtes à utiliser :

- **Paris** : Zone métropolitaine parisienne
- **Londres** : Zone métropolitaine londonienne  
- **New York** : Zone métropolitaine new-yorkaise
- **France** : Territoire français complet

```python
from config import Config

# Utiliser une zone prédéfinie
paris_bounds = Config.ZONES['paris']
flights = scraper.get_flights_in_bounds(paris_bounds)
```

## ✈️ Aéroports supportés

Codes IATA des principaux aéroports :

- **CDG** : Charles de Gaulle (Paris)
- **ORY** : Orly (Paris)
- **LHR** : Heathrow (Londres)
- **JFK** : John F. Kennedy (New York)
- **LAX** : Los Angeles
- **DXB** : Dubai
- **NRT** : Narita (Tokyo)
- **FRA** : Frankfurt
- **AMS** : Amsterdam Schiphol
- **FCO** : Rome Fiumicino

## 📝 Exemples complets

Consultez le fichier `examples.py` pour des exemples d'utilisation avancée :

```bash
python examples.py
```

Ce script inclut :
- Scraping basique par zone
- Recherche spécifique par compagnie
- Monitoring d'aéroports
- Analyse comparative de données
- Suivi de vols individuels
- Monitoring temps réel

## ⚙️ Configuration

Le fichier `config.py` permet de personnaliser :

- URLs et endpoints API
- Timeouts et retry logic
- Zones géographiques personnalisées
- Dossiers de sortie
- Headers HTTP par défaut

## 📁 Structure du projet

```
FlightRadarScrap/
├── main.py              # Classe principale du scraper
├── config.py            # Configuration et paramètres
├── examples.py          # Exemples d'utilisation
├── requirements.txt     # Dépendances Python
├── README.md           # Documentation
├── data/               # Dossier des données exportées
└── logs/               # Dossier des logs
```

## 🚨 Limitations et considérations

### Respect des conditions d'utilisation
- Utilisez ce scraper de manière responsable
- Respectez les limites de taux de FlightRadar24
- N'abusez pas des requêtes API

### Gestion des erreurs
- Le scraper inclut une gestion robuste des erreurs
- Logs détaillés pour le debugging
- Retry automatique en cas d'échec temporaire

### Performance
- Pause recommandée entre les requêtes (minimum 1-2 secondes)
- Limitation du nombre de requêtes simultanées
- Monitoring temps réel avec intervalles raisonnables

## 🔧 Dépannage

### Erreurs communes

**Erreur 403/429** : Trop de requêtes
```python
# Augmenter les délais entre requêtes
time.sleep(5)  # 5 secondes entre requêtes
```

**Données vides** : API temporairement indisponible
```python
# Vérifier la connectivité et réessayer
if not flights:
    print("Aucune donnée récupérée, réessayer plus tard")
```

**Erreurs de parsing** : Format API modifié
```python
# Vérifier la structure des données retournées
print(raw_data.keys())  # Examiner la structure
```

## 📞 Support

Pour signaler des bugs ou demander des fonctionnalités :
1. Vérifiez les logs d'erreur
2. Testez avec les exemples fournis
3. Consultez la documentation de l'API FlightRadar24

## 📄 Licence

Ce projet est fourni à des fins éducatives. Respectez les conditions d'utilisation de FlightRadar24.

---

**⚠️ Avertissement** : Ce scraper utilise les APIs publiques de FlightRadar24. L'utilisation intensive peut être limitée ou bloquée. Utilisez avec modération et responsabilité.
