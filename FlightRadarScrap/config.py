# Configuration pour FlightRadar24 Scraper
import os

class Config:
    """Configuration du scraper FlightRadar24"""
    
    # URLs de base
    BASE_URL = "https://www.flightradar24.com"
    API_URL = "https://data-live.flightradar24.com"
    
    # Paramètres de requête
    REQUEST_TIMEOUT = 30
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # secondes
    
    # Paramètres de monitoring
    DEFAULT_MONITORING_INTERVAL = 30  # secondes
    DEFAULT_MONITORING_DURATION = 10  # minutes
    
    # Zones prédéfinies (bounds)
    ZONES = {
        'paris': {
            'north': 49.0,
            'south': 48.5,
            'east': 2.7,
            'west': 2.0
        },
        'london': {
            'north': 51.7,
            'south': 51.3,
            'east': 0.2,
            'west': -0.5
        },
        'new_york': {
            'north': 40.9,
            'south': 40.5,
            'east': -73.7,
            'west': -74.3
        },
        'france': {
            'north': 51.1,
            'south': 42.3,
            'east': 9.6,
            'west': -5.1
        }
    }
    
    # Aéroports principaux
    AIRPORTS = {
        'CDG': 'Charles de Gaulle',
        'ORY': 'Orly',
        'LHR': 'Heathrow',
        'JFK': 'John F. Kennedy',
        'LAX': 'Los Angeles',
        'DXB': 'Dubai',
        'NRT': 'Narita',
        'FRA': 'Frankfurt',
        'AMS': 'Amsterdam Schiphol',
        'FCO': 'Rome Fiumicino'
    }
    
    # Headers par défaut
    DEFAULT_HEADERS = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': 'https://www.flightradar24.com/',
    }
    
    # Dossiers de sortie
    OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'data')
    LOGS_DIR = os.path.join(os.path.dirname(__file__), 'logs')
    
    @classmethod
    def ensure_directories(cls):
        """Créer les dossiers nécessaires s'ils n'existent pas"""
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
        os.makedirs(cls.LOGS_DIR, exist_ok=True)
