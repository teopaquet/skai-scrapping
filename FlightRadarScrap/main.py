"""
FlightRadar24 Fleet Analyzer - Version Simplifiée
Application dédiée uniquement à l'analyse des flottes des compagnies aériennes
"""

import requests
import json
import time
import pandas as pd
from datetime import datetime
import logging
from fake_useragent import UserAgent
from typing import Dict, List
import re

class FlightRadar24FleetAnalyzer:
    """
    Analyseur de flottes pour FlightRadar24
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.ua = UserAgent()
        self.api_url = "https://data-live.flightradar24.com"
        
        # Configuration des headers
        self.headers = {
            'User-Agent': self.ua.random,
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.flightradar24.com/',
        }
        self.session.headers.update(self.headers)
        
        # Configuration du logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def get_flights_in_bounds(self, bounds: Dict[str, float]) -> Dict:
        """
        Récupère tous les vols dans une zone géographique donnée
        
        Args:
            bounds: Dictionnaire avec les clés 'north', 'south', 'east', 'west'
        
        Returns:
            Dictionnaire contenant les données de vol
        """
        try:
            # Construction de l'URL avec les paramètres de zone
            url = f"{self.api_url}/zones/fcgi/feed.js"
            params = {
                'bounds': f"{bounds['north']},{bounds['south']},{bounds['west']},{bounds['east']}",
                'faa': '1',
                'satellite': '1',
                'mlat': '1',
                'flarm': '1',
                'adsb': '1',
                'gnd': '1',
                'air': '1',
                'vehicles': '1',
                'estimated': '1',
                'maxage': '14400',
                'gliders': '1',
                'stats': '1'
            }
            
            self.logger.info(f"Récupération des vols dans la zone: {bounds}")
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            # Parse JSON response
            data = response.json()
            return data
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Erreur lors de la requête: {e}")
            return {}
        except json.JSONDecodeError as e:
            self.logger.error(f"Erreur lors du parsing JSON: {e}")
            return {}
    
    def parse_flights_data(self, raw_data: Dict) -> List[Dict]:
        """
        Parse les données brutes des vols en format structuré
        
        Args:
            raw_data: Données brutes de l'API
        
        Returns:
            Liste de vols formatés
        """
        flights = []
        
        # Les données de vol sont dans les clés numériques
        for key, value in raw_data.items():
            if key.isdigit() and isinstance(value, list) and len(value) >= 13:
                flight = {
                    'flight_id': key,
                    'callsign': value[16] if len(value) > 16 else '',
                    'latitude': value[1],
                    'longitude': value[2],
                    'track': value[3],
                    'altitude': value[4],
                    'speed': value[5],
                    'radar': value[6],
                    'aircraft_type': value[8] if len(value) > 8 else '',
                    'registration': value[9] if len(value) > 9 else '',
                    'timestamp': value[10] if len(value) > 10 else '',
                    'origin': value[11] if len(value) > 11 else '',
                    'destination': value[12] if len(value) > 12 else '',
                    'flight_number': value[13] if len(value) > 13 else '',
                    'airline_icao': value[18] if len(value) > 18 else '',
                    'on_ground': value[14] if len(value) > 14 else 0
                }
                flights.append(flight)
        
        return flights
    
    def get_airline_fleet_analysis(self, bounds: Dict[str, float] = None, duration_minutes: int = 30) -> Dict:
        """
        Analyse la flotte d'avions par compagnie aérienne
        
        Args:
            bounds: Zone géographique à analyser (si None, utilise une grande zone)
            duration_minutes: Durée de collecte pour avoir plus de données
        
        Returns:
            Dictionnaire avec l'analyse des flottes par compagnie
        """
        if bounds is None:
            # Zone large pour capturer plus de données (Europe)
            bounds = {
                'north': 71.0,
                'south': 35.0,
                'east': 40.0,
                'west': -25.0
            }
        
        self.logger.info(f"Début de l'analyse des flottes pour {duration_minutes} minutes")
        
        # Collecter les données sur plusieurs cycles pour avoir plus de diversité
        all_flights = []
        cycles = max(1, duration_minutes // 2)  # Un cycle toutes les 2 minutes
        
        for cycle in range(cycles):
            try:
                self.logger.info(f"Cycle {cycle + 1}/{cycles} - Collecte des données...")
                raw_data = self.get_flights_in_bounds(bounds)
                flights = self.parse_flights_data(raw_data)
                all_flights.extend(flights)
                
                if cycle < cycles - 1:  # Pas de pause au dernier cycle
                    time.sleep(120)  # Attendre 2 minutes entre les cycles
                    
            except Exception as e:
                self.logger.error(f"Erreur lors du cycle {cycle + 1}: {e}")
                continue
        
        # Analyser les données collectées
        return self._analyze_fleet_data(all_flights)
    
    def _analyze_fleet_data(self, flights: List[Dict]) -> Dict:
        """
        Analyse les données de vol pour extraire les informations de flotte
        
        Args:
            flights: Liste des vols collectés
        
        Returns:
            Dictionnaire avec l'analyse des flottes
        """
        fleet_analysis = {}
        airline_names = {}
        
        # Dictionnaire pour mapper les codes ICAO vers les noms de compagnies
        airline_codes = {
            'AFR': 'Air France',
            'KLM': 'KLM Royal Dutch Airlines',
            'DLH': 'Lufthansa',
            'BAW': 'British Airways',
            'EZY': 'easyJet',
            'RYR': 'Ryanair',
            'VLG': 'Vueling',
            'IBE': 'Iberia',
            'SWR': 'Swiss International Air Lines',
            'AUA': 'Austrian Airlines',
            'TAP': 'TAP Air Portugal',
            'SAS': 'Scandinavian Airlines',
            'FIN': 'Finnair',
            'UAE': 'Emirates',
            'QTR': 'Qatar Airways',
            'ETD': 'Etihad Airways',
            'THY': 'Turkish Airlines',
            'MSR': 'EgyptAir',
            'AMC': 'Air Malta',
            'CTN': 'Croatia Airlines'
        }
        
        for flight in flights:
            airline_icao = flight.get('airline_icao', '').strip()
            aircraft_type = flight.get('aircraft_type', '').strip()
            registration = flight.get('registration', '').strip()
            callsign = flight.get('callsign', '').strip()
            
            # Extraire le code de compagnie du callsign si airline_icao n'est pas disponible
            if not airline_icao and callsign:
                # Extraire les lettres du début du callsign
                match = re.match(r'^([A-Z]{2,3})', callsign)
                if match:
                    airline_icao = match.group(1)
            
            # Ignorer si pas de données valides
            if not airline_icao or not aircraft_type:
                continue
            
            # Obtenir le nom de la compagnie
            airline_name = airline_codes.get(airline_icao, f"Compagnie {airline_icao}")
            airline_names[airline_icao] = airline_name
            
            # Initialiser la structure pour cette compagnie
            if airline_icao not in fleet_analysis:
                fleet_analysis[airline_icao] = {
                    'airline_name': airline_name,
                    'aircraft_types': {},
                    'total_aircraft': 0,
                    'registrations': set()
                }
            
            # Ajouter l'immatriculation pour éviter les doublons
            if registration:
                fleet_analysis[airline_icao]['registrations'].add(registration)
            
            # Compter les types d'avions
            if aircraft_type not in fleet_analysis[airline_icao]['aircraft_types']:
                fleet_analysis[airline_icao]['aircraft_types'][aircraft_type] = {
                    'count': 0,
                    'registrations': set()
                }
            
            fleet_analysis[airline_icao]['aircraft_types'][aircraft_type]['count'] += 1
            if registration:
                fleet_analysis[airline_icao]['aircraft_types'][aircraft_type]['registrations'].add(registration)
        
        # Nettoyer et finaliser les données
        for airline_icao in fleet_analysis:
            # Compter le total basé sur les immatriculations uniques par type
            total = 0
            for aircraft_type in fleet_analysis[airline_icao]['aircraft_types']:
                unique_registrations = len(fleet_analysis[airline_icao]['aircraft_types'][aircraft_type]['registrations'])
                if unique_registrations > 0:
                    fleet_analysis[airline_icao]['aircraft_types'][aircraft_type]['unique_count'] = unique_registrations
                    total += unique_registrations
                
                # Convertir les sets en listes pour la sérialisation
                fleet_analysis[airline_icao]['aircraft_types'][aircraft_type]['registrations'] = \
                    list(fleet_analysis[airline_icao]['aircraft_types'][aircraft_type]['registrations'])
            
            fleet_analysis[airline_icao]['total_aircraft'] = total
            fleet_analysis[airline_icao]['total_unique_registrations'] = len(fleet_analysis[airline_icao]['registrations'])
            fleet_analysis[airline_icao]['registrations'] = list(fleet_analysis[airline_icao]['registrations'])
        
        return fleet_analysis
    
    def save_fleet_analysis_to_csv(self, fleet_data: Dict, filename: str = None) -> str:
        """
        Sauvegarde l'analyse de flotte en CSV
        
        Args:
            fleet_data: Données d'analyse de flotte
            filename: Nom du fichier (optionnel)
        
        Returns:
            Nom du fichier sauvegardé
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"fleet_analysis_{timestamp}.csv"
        
        # Vérifier s'il y a des données
        if not fleet_data:
            self.logger.warning("Aucune donnée de flotte à sauvegarder")
            # Créer un fichier vide avec les headers
            empty_df = pd.DataFrame(columns=[
                'airline_icao', 'airline_name', 'aircraft_type', 
                'observed_count', 'unique_registrations', 'sample_registrations'
            ])
            empty_df.to_csv(filename, index=False, encoding='utf-8')
            return filename
        
        # Préparer les données pour le CSV
        csv_data = []
        for airline_icao, data in fleet_data.items():
            airline_name = data.get('airline_name', f'Compagnie {airline_icao}')
            aircraft_types = data.get('aircraft_types', {})
            
            if not aircraft_types:
                # Ajouter une ligne même si pas de types d'avions
                csv_data.append({
                    'airline_icao': airline_icao,
                    'airline_name': airline_name,
                    'aircraft_type': 'Aucun',
                    'observed_count': 0,
                    'unique_registrations': 0,
                    'sample_registrations': ''
                })
            else:
                for aircraft_type, type_data in aircraft_types.items():
                    registrations_list = type_data.get('registrations', [])
                    sample_registrations = ', '.join(list(registrations_list)[:5]) if registrations_list else ''
                    
                    csv_data.append({
                        'airline_icao': airline_icao,
                        'airline_name': airline_name,
                        'aircraft_type': aircraft_type or 'Type inconnu',
                        'observed_count': type_data.get('count', 0),
                        'unique_registrations': type_data.get('unique_count', 0),
                        'sample_registrations': sample_registrations
                    })
        
        # Créer le DataFrame
        df = pd.DataFrame(csv_data)
        
        # Vérifier que le DataFrame n'est pas vide avant de trier
        if not df.empty and 'airline_name' in df.columns and 'unique_registrations' in df.columns:
            df = df.sort_values(['airline_name', 'unique_registrations'], ascending=[True, False])
        
        # Sauvegarder
        df.to_csv(filename, index=False, encoding='utf-8')
        self.logger.info(f"Analyse de flotte sauvegardée dans {filename} ({len(csv_data)} entrées)")
        return filename
    
    def print_fleet_summary(self, fleet_data: Dict):
        """
        Affiche un résumé de l'analyse de flotte
        
        Args:
            fleet_data: Données d'analyse de flotte
        """
        print("\n" + "="*80)
        print("📊 ANALYSE DES FLOTTES PAR COMPAGNIE AÉRIENNE")
        print("="*80)
        
        # Trier par nombre total d'avions
        sorted_airlines = sorted(fleet_data.items(), 
                               key=lambda x: x[1]['total_unique_registrations'], 
                               reverse=True)
        
        for airline_icao, data in sorted_airlines:
            print(f"\n✈️  {data['airline_name']} ({airline_icao})")
            print(f"   Total d'avions observés: {data['total_unique_registrations']}")
            print(f"   Types d'aéronefs: {len(data['aircraft_types'])}")
            
            # Afficher les types d'avions triés par quantité
            aircraft_sorted = sorted(data['aircraft_types'].items(), 
                                   key=lambda x: x[1].get('unique_count', 0), 
                                   reverse=True)
            
            for aircraft_type, type_data in aircraft_sorted[:10]:  # Top 10
                unique_count = type_data.get('unique_count', 0)
                if unique_count > 0:
                    print(f"   • {aircraft_type}: {unique_count} avion(s)")
        
        # Statistiques globales
        total_airlines = len(fleet_data)
        total_aircraft = sum(data['total_unique_registrations'] for data in fleet_data.values())
        all_aircraft_types = set()
        for data in fleet_data.values():
            all_aircraft_types.update(data['aircraft_types'].keys())
        
        print(f"\n📈 STATISTIQUES GLOBALES")
        print(f"   Compagnies analysées: {total_airlines}")
        print(f"   Total d'avions observés: {total_aircraft}")
        print(f"   Types d'aéronefs différents: {len(all_aircraft_types)}")

def main():
    """
    Point d'entrée principal - Lance l'interface graphique
    """
    print("🛩️ FlightRadar24 Fleet Analyzer")
    print("Lancement de l'interface graphique...")
    
    try:
        import tkinter
        print("✅ Interface graphique disponible")
        
        # Importer et lancer l'interface graphique
        from fleet_gui import FleetAnalyzerGUI
        app = FleetAnalyzerGUI()
        app.run()
        
    except ImportError:
        print("❌ Tkinter non disponible, mode console")
        
        # Mode console simple
        analyzer = FlightRadar24FleetAnalyzer()
        
        print("\n📍 Zones disponibles:")
        zones = {
            '1': ('Europe', {'north': 75.0, 'south': 30.0, 'east': 50.0, 'west': -30.0}),
            '2': ('France', {'north': 51.1, 'south': 42.3, 'east': 9.6, 'west': -5.1}),
            '3': ('Monde', {'north': 80.0, 'south': -80.0, 'east': 180.0, 'west': -180.0})
        }
        
        for key, (name, _) in zones.items():
            print(f"{key}. {name}")
        
        choice = input("\nChoisissez une zone (1-3): ").strip()
        if choice in zones:
            zone_name, bounds = zones[choice]
            print(f"\n� Analyse de la zone: {zone_name}")
            print("⏳ Analyse en cours (10 minutes)...")
            
            fleet_data = analyzer.get_airline_fleet_analysis(bounds, 10)
            
            if fleet_data:
                analyzer.print_fleet_summary(fleet_data)
                filename = analyzer.save_fleet_analysis_to_csv(fleet_data)
                print(f"\n💾 Données sauvegardées: {filename}")
            else:
                print("❌ Aucune donnée collectée")
        else:
            print("❌ Choix invalide")


if __name__ == "__main__":
    main()