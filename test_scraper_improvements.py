#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du scraper amélioré pour vérifier la récupération des registrations et types d'aircraft
"""

import sys
import os

# Ajouter le répertoire src au path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from scrapers.scraper_flightradar24 import FlightRadar24Scraper
import json

def test_single_airline():
    """Test sur une seule compagnie pour vérifier les améliorations"""
    scraper = FlightRadar24Scraper()
    
    # Test avec 21 Air (2i-csb) d'après l'exemple HTML fourni
    airline_code = "2i-csb"
    airline_name = "21 Air"
    
    print(f"Test du scraping pour {airline_name} ({airline_code})")
    print("="*50)
    
    result = scraper.scrape_fleet_data(airline_code, airline_name)
    
    # Afficher le résultat en format JSON pour voir la structure
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Analyser les résultats
    if result['status'] == 'success':
        print(f"\n✅ Scraping réussi!")
        print(f"Total aircraft: {result['total_aircraft']}")
        print(f"Types d'aircraft trouvés: {len(result['fleet_details'])}")
        
        for fleet in result['fleet_details']:
            print(f"\nType: {fleet['type']} (Quantité: {fleet['count']})")
            if fleet['aircraft_details']:
                print("Détails individuels:")
                for detail in fleet['aircraft_details']:
                    print(f"  - Registration: {detail['registration']}")
                    print(f"    Type détaillé: {detail['detailed_type']}")
                    print(f"    Numéro de série: {detail.get('serial_number', 'N/A')}")
                    print(f"    Âge: {detail.get('age', 'N/A')}")
            else:
                print("  Aucun détail individuel trouvé")
    else:
        print(f"❌ Erreur: {result.get('error', 'Erreur inconnue')}")

if __name__ == "__main__":
    test_single_airline()
