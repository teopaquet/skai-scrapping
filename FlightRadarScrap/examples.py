"""
Exemples d'utilisation avancée du scraper FlightRadar24
"""

from main import FlightRadar24Scraper
from config import Config
import time
import pandas as pd
from datetime import datetime

def example_basic_scraping():
    """Exemple de scraping basique"""
    print("=== Scraping basique des vols autour de Paris ===")
    
    scraper = FlightRadar24Scraper()
    
    # Utiliser la zone prédéfinie de Paris
    paris_bounds = Config.ZONES['paris']
    
    # Récupérer les vols
    raw_data = scraper.get_flights_in_bounds(paris_bounds)
    flights = scraper.parse_flights_data(raw_data)
    
    print(f"Nombre de vols trouvés: {len(flights)}")
    
    # Afficher quelques informations
    if flights:
        df = pd.DataFrame(flights)
        print("\nRésumé des données:")
        print(f"- Altitudes: {df['altitude'].min()} - {df['altitude'].max()} ft")
        print(f"- Vitesses: {df['speed'].min()} - {df['speed'].max()} kt")
        print(f"- Types d'aéronefs uniques: {df['aircraft_type'].nunique()}")
        
        # Top 5 des types d'aéronefs
        print("\nTop 5 des types d'aéronefs:")
        print(df['aircraft_type'].value_counts().head())
    
    return flights

def example_airline_specific():
    """Exemple de scraping spécifique à une compagnie"""
    print("\n=== Scraping spécifique Air France ===")
    
    scraper = FlightRadar24Scraper()
    
    # Rechercher les vols Air France
    search_results = scraper.search_flights("Air France")
    print(f"Résultats de recherche Air France: {len(search_results)}")
    
    # Récupérer les vols Air France dans la zone France
    france_bounds = Config.ZONES['france']
    raw_data = scraper.get_flights_in_bounds(france_bounds, airline="AFR")  # Code ICAO Air France
    flights = scraper.parse_flights_data(raw_data)
    
    print(f"Vols Air France en France: {len(flights)}")
    
    # Filtrer pour ne garder que les vols Air France
    af_flights = [f for f in flights if f['airline_icao'] == 'AFR' or 'AF' in f['callsign']]
    print(f"Vols Air France confirmés: {len(af_flights)}")
    
    return af_flights

def example_airport_monitoring():
    """Exemple de monitoring d'aéroport"""
    print("\n=== Monitoring CDG ===")
    
    scraper = FlightRadar24Scraper()
    
    # Arrivées à CDG
    arrivals = scraper.get_airport_arrivals("CDG")
    print(f"Données d'arrivées CDG: {type(arrivals)} - {len(arrivals) if isinstance(arrivals, dict) else 'N/A'}")
    
    # Départs de CDG
    departures = scraper.get_airport_departures("CDG")
    print(f"Données de départs CDG: {type(departures)} - {len(departures) if isinstance(departures, dict) else 'N/A'}")
    
    return arrivals, departures

def example_realtime_monitoring():
    """Exemple de monitoring en temps réel"""
    print("\n=== Monitoring temps réel (2 minutes) ===")
    
    scraper = FlightRadar24Scraper()
    
    # Zone de monitoring (Paris)
    bounds = Config.ZONES['paris']
    
    # Lancer le monitoring pour 2 minutes avec des intervalles de 20 secondes
    flights_data = scraper.monitor_flights_realtime(
        bounds=bounds,
        duration_minutes=2,
        interval_seconds=20
    )
    
    print(f"Monitoring terminé. Total d'entrées collectées: {len(flights_data)}")
    
    if flights_data:
        # Analyser les données collectées
        df = pd.DataFrame(flights_data)
        print(f"Vols uniques suivis: {df['flight_id'].nunique()}")
        print(f"Timestamps de collecte: {df['scrape_timestamp'].nunique()}")
    
    return flights_data

def example_data_analysis():
    """Exemple d'analyse de données"""
    print("\n=== Analyse des données de vol ===")
    
    scraper = FlightRadar24Scraper()
    
    # Récupérer des données de plusieurs zones
    zones_data = {}
    for zone_name, bounds in Config.ZONES.items():
        if zone_name in ['paris', 'london']:  # Limiter pour l'exemple
            print(f"Récupération des données pour {zone_name}...")
            raw_data = scraper.get_flights_in_bounds(bounds)
            flights = scraper.parse_flights_data(raw_data)
            zones_data[zone_name] = flights
            time.sleep(2)  # Pause entre les requêtes
    
    # Analyser les données
    for zone, flights in zones_data.items():
        if flights:
            df = pd.DataFrame(flights)
            print(f"\n--- Analyse {zone.upper()} ---")
            print(f"Nombre de vols: {len(flights)}")
            print(f"Altitude moyenne: {df['altitude'].mean():.0f} ft")
            print(f"Vitesse moyenne: {df['speed'].mean():.0f} kt")
            print(f"Vols au sol: {sum(1 for f in flights if f['on_ground'])}")
            print(f"Compagnies uniques: {df['airline_icao'].nunique()}")
    
    return zones_data

def example_flight_tracking():
    """Exemple de suivi d'un vol spécifique"""
    print("\n=== Suivi d'un vol spécifique ===")
    
    scraper = FlightRadar24Scraper()
    
    # D'abord, récupérer quelques vols pour avoir des IDs
    paris_bounds = Config.ZONES['paris']
    raw_data = scraper.get_flights_in_bounds(paris_bounds)
    flights = scraper.parse_flights_data(raw_data)
    
    if flights:
        # Prendre le premier vol trouvé
        sample_flight = flights[0]
        flight_id = sample_flight['flight_id']
        
        print(f"Suivi du vol ID: {flight_id}")
        print(f"Callsign: {sample_flight['callsign']}")
        print(f"Position actuelle: {sample_flight['latitude']}, {sample_flight['longitude']}")
        
        # Récupérer les détails complets
        details = scraper.get_flight_details(flight_id)
        print(f"Détails récupérés: {len(details) if details else 'Aucun'}")
        
        return sample_flight, details
    
    return None, None

def main():
    """Lancer tous les exemples"""
    print("🛩️  FlightRadar24 Scraper - Exemples d'utilisation\n")
    
    try:
        # Exemples de base
        flights = example_basic_scraping()
        af_flights = example_airline_specific()
        arrivals, departures = example_airport_monitoring()
        
        # Analyse des données
        zones_data = example_data_analysis()
        
        # Suivi de vol
        flight, details = example_flight_tracking()
        
        # Monitoring temps réel (décommenté si souhaité)
        # realtime_data = example_realtime_monitoring()
        
        print("\n✅ Tous les exemples ont été exécutés avec succès!")
        
        # Sauvegarder un exemple de données
        if flights:
            scraper = FlightRadar24Scraper()
            filename = scraper.save_to_csv(flights, "exemple_vols_paris.csv")
            print(f"📁 Données d'exemple sauvegardées: {filename}")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
