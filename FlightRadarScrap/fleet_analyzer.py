"""
Script spécialisé pour l'analyse des flottes d'avions par compagnie aérienne
"""

from main import FlightRadar24Scraper
import json
import pandas as pd
from datetime import datetime
import time

def analyze_airline_fleets():
    """
    Analyse détaillée des flottes des compagnies aériennes
    """
    print("🛩️  Analyseur de Flottes FlightRadar24")
    print("="*50)
    
    scraper = FlightRadar24Scraper()
    
    # Zones prédéfinies pour l'analyse
    zones = {
        'europe': {
            'name': 'Europe',
            'bounds': {
                'north': 75.0,
                'south': 30.0,
                'east': 50.0,
                'west': -30.0
            }
        },
        'world': {
            'name': 'Monde (échantillon)',
            'bounds': {
                'north': 80.0,
                'south': -80.0,
                'east': 180.0,
                'west': -180.0
            }
        },
        'north_america': {
            'name': 'Amérique du Nord',
            'bounds': {
                'north': 70.0,
                'south': 20.0,
                'east': -50.0,
                'west': -180.0
            }
        },
        'asia': {
            'name': 'Asie',
            'bounds': {
                'north': 70.0,
                'south': 0.0,
                'east': 180.0,
                'west': 60.0
            }
        }
    }
    
    print("\nZones d'analyse disponibles:")
    for i, (key, zone) in enumerate(zones.items(), 1):
        print(f"{i}. {zone['name']}")
    
    # Sélection de la zone
    try:
        choice = int(input("\nChoisissez une zone (1-4): ")) - 1
        zone_keys = list(zones.keys())
        if 0 <= choice < len(zone_keys):
            selected_zone = zones[zone_keys[choice]]
            print(f"\n🌍 Zone sélectionnée: {selected_zone['name']}")
        else:
            print("❌ Choix invalide, utilisation de l'Europe par défaut")
            selected_zone = zones['europe']
    except ValueError:
        print("❌ Choix invalide, utilisation de l'Europe par défaut")
        selected_zone = zones['europe']
    
    # Durée d'analyse
    try:
        duration = int(input("\nDurée d'analyse en minutes (recommandé: 10-30): "))
        duration = max(5, min(60, duration))  # Entre 5 et 60 minutes
    except ValueError:
        duration = 15
        print("❌ Durée invalide, utilisation de 15 minutes par défaut")
    
    print(f"\n🔍 Début de l'analyse - Zone: {selected_zone['name']} - Durée: {duration} minutes")
    print("⏳ Collecte des données en cours... (Cela peut prendre du temps)")
    
    # Lancer l'analyse
    start_time = time.time()
    fleet_data = scraper.get_airline_fleet_analysis(
        bounds=selected_zone['bounds'],
        duration_minutes=duration
    )
    end_time = time.time()
    
    print(f"\n✅ Analyse terminée en {(end_time - start_time)/60:.1f} minutes")
    
    # Afficher le résumé
    scraper.print_fleet_summary(fleet_data)
    
    # Sauvegarder les résultats
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # CSV détaillé
    csv_filename = scraper.save_fleet_analysis_to_csv(
        fleet_data, 
        f"fleet_analysis_{selected_zone['name'].lower().replace(' ', '_')}_{timestamp}.csv"
    )
    
    # JSON complet
    json_filename = f"fleet_analysis_complete_{selected_zone['name'].lower().replace(' ', '_')}_{timestamp}.json"
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(fleet_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Fichiers sauvegardés:")
    print(f"   📊 CSV: {csv_filename}")
    print(f"   📋 JSON: {json_filename}")
    
    # Proposer une analyse comparative
    if input("\n❓ Voulez-vous comparer avec une autre zone? (o/n): ").lower() == 'o':
        compare_fleet_analysis(scraper, fleet_data, selected_zone['name'])
    
    return fleet_data

def compare_fleet_analysis(scraper, first_analysis, first_zone_name):
    """
    Compare l'analyse de flotte avec une autre zone
    """
    print("\n🔍 Analyse comparative")
    
    # Zone de comparaison rapide (plus petite)
    comparison_zones = {
        'paris': {'name': 'Paris', 'bounds': {'north': 49.5, 'south': 48.0, 'east': 3.0, 'west': 1.5}},
        'london': {'name': 'Londres', 'bounds': {'north': 52.0, 'south': 51.0, 'east': 0.5, 'west': -1.0}},
        'new_york': {'name': 'New York', 'bounds': {'north': 41.0, 'south': 40.0, 'east': -73.0, 'west': -75.0}},
        'dubai': {'name': 'Dubai', 'bounds': {'north': 26.0, 'south': 24.5, 'east': 56.0, 'west': 54.5}}
    }
    
    print("Zones de comparaison (analyse rapide 5 minutes):")
    for i, (key, zone) in enumerate(comparison_zones.items(), 1):
        print(f"{i}. {zone['name']}")
    
    try:
        choice = int(input("Choisissez une zone de comparaison (1-4): ")) - 1
        zone_keys = list(comparison_zones.keys())
        if 0 <= choice < len(zone_keys):
            comp_zone = comparison_zones[zone_keys[choice]]
        else:
            comp_zone = comparison_zones['paris']
    except ValueError:
        comp_zone = comparison_zones['paris']
    
    print(f"\n🔍 Analyse de comparaison: {comp_zone['name']} (5 minutes)")
    
    second_analysis = scraper.get_airline_fleet_analysis(
        bounds=comp_zone['bounds'],
        duration_minutes=5
    )
    
    # Comparaison des résultats
    print(f"\n📊 COMPARAISON: {first_zone_name} vs {comp_zone['name']}")
    print("="*60)
    
    # Statistiques comparatives
    first_airlines = len(first_analysis)
    second_airlines = len(second_analysis)
    
    first_total = sum(data['total_unique_registrations'] for data in first_analysis.values())
    second_total = sum(data['total_unique_registrations'] for data in second_analysis.values())
    
    print(f"Compagnies observées:")
    print(f"  {first_zone_name}: {first_airlines}")
    print(f"  {comp_zone['name']}: {second_airlines}")
    
    print(f"\nAvions uniques observés:")
    print(f"  {first_zone_name}: {first_total}")
    print(f"  {comp_zone['name']}: {second_total}")
    
    # Compagnies communes
    common_airlines = set(first_analysis.keys()) & set(second_analysis.keys())
    print(f"\nCompagnies présentes dans les deux zones: {len(common_airlines)}")
    
    if common_airlines:
        print("\n🔗 Compagnies communes:")
        for airline in sorted(common_airlines):
            first_count = first_analysis[airline]['total_unique_registrations']
            second_count = second_analysis[airline]['total_unique_registrations']
            airline_name = first_analysis[airline]['airline_name']
            print(f"  • {airline_name}: {first_count} vs {second_count} avions")

def generate_fleet_report(fleet_data, zone_name):
    """
    Génère un rapport détaillé de l'analyse de flotte
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"fleet_report_{zone_name.lower().replace(' ', '_')}_{timestamp}.txt"
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write("RAPPORT D'ANALYSE DE FLOTTE\n")
        f.write("="*50 + "\n\n")
        f.write(f"Zone analysée: {zone_name}\n")
        f.write(f"Date d'analyse: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
        
        # Statistiques globales
        total_airlines = len(fleet_data)
        total_aircraft = sum(data['total_unique_registrations'] for data in fleet_data.values())
        all_types = set()
        for data in fleet_data.values():
            all_types.update(data['aircraft_types'].keys())
        
        f.write("STATISTIQUES GLOBALES\n")
        f.write("-"*30 + "\n")
        f.write(f"Compagnies analysées: {total_airlines}\n")
        f.write(f"Total d'avions observés: {total_aircraft}\n")
        f.write(f"Types d'aéronefs différents: {len(all_types)}\n\n")
        
        # Détail par compagnie
        f.write("DÉTAIL PAR COMPAGNIE\n")
        f.write("-"*30 + "\n")
        
        sorted_airlines = sorted(fleet_data.items(), 
                               key=lambda x: x[1]['total_unique_registrations'], 
                               reverse=True)
        
        for airline_icao, data in sorted_airlines:
            f.write(f"\n{data['airline_name']} ({airline_icao})\n")
            f.write(f"  Total: {data['total_unique_registrations']} avions\n")
            f.write(f"  Types: {len(data['aircraft_types'])}\n")
            
            aircraft_sorted = sorted(data['aircraft_types'].items(), 
                                   key=lambda x: x[1].get('unique_count', 0), 
                                   reverse=True)
            
            for aircraft_type, type_data in aircraft_sorted:
                unique_count = type_data.get('unique_count', 0)
                if unique_count > 0:
                    f.write(f"    • {aircraft_type}: {unique_count}\n")
    
    print(f"\n📄 Rapport détaillé généré: {report_filename}")
    return report_filename

def main():
    """
    Point d'entrée principal pour l'analyse de flottes
    """
    try:
        fleet_data = analyze_airline_fleets()
        
        # Proposer de générer un rapport
        if input("\n❓ Générer un rapport détaillé? (o/n): ").lower() == 'o':
            zone_name = input("Nom de la zone analysée: ").strip() or "Zone_analysée"
            generate_fleet_report(fleet_data, zone_name)
        
        print("\n✅ Analyse terminée avec succès!")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Analyse interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors de l'analyse: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
