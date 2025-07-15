#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scraper pour récupérer les détails de flotte des compagnies aériennes depuis FlightRadar24
"""

import csv
import requests
from bs4 import BeautifulSoup
import time
import re
import json
import pandas as pd
from urllib.parse import urljoin
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os
import sys

class FlightRadar24Scraper:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://www.flightradar24.com"
        self.setup_session()
        self.airlines_data = []
        
    def setup_session(self):
        """Configure la session avec des headers et retry strategy"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.session.headers.update(headers)
        
        # Configuration retry
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def extract_airline_codes_from_csv(self, csv_file):
        """Extrait les codes des compagnies aériennes depuis le fichier CSV"""
        airline_codes = []
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                
                # Ignorer les en-têtes
                next(csv_reader, None)
                next(csv_reader, None)
                
                for row in csv_reader:
                    if len(row) >= 5 and row[0] and 'airlines' in row[0]:
                        # Extraire le code de l'URL
                        url = row[0]
                        # Format: https://www.flightradar24.com/data/airlines/2i-csb
                        code_match = re.search(r'/airlines/([^"]+)', url)
                        if code_match:
                            code = code_match.group(1)
                            airline_name = row[2].strip() if row[2] else "Unknown"
                            sigle = row[3].strip() if row[3] else "Unknown"
                            aircraft_info = row[4].strip() if row[4] else "0 aircraft"
                            
                            airline_codes.append({
                                'code': code,
                                'name': airline_name,
                                'sigle': sigle,
                                'aircraft_info': aircraft_info,
                                'url': url
                            })
            
            print(f"Trouvé {len(airline_codes)} compagnies aériennes avec codes")
            return airline_codes
            
        except Exception as e:
            print(f"Erreur lors de l'extraction des codes: {e}")
            return []

    def scrape_fleet_data(self, airline_code, airline_name):
        """Scrape les données de flotte pour une compagnie donnée"""
        fleet_url = f"{self.base_url}/data/airlines/{airline_code}/fleet"
        
        try:
            print(f"Scraping {airline_name} ({airline_code})...")
            
            response = self.session.get(fleet_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraire le nombre total d'aircraft
            total_aircraft_span = soup.find('span', class_='number-of-aircraft')
            total_aircraft = 0
            if total_aircraft_span:
                strong_tag = total_aircraft_span.find('strong')
                if strong_tag:
                    total_aircraft = int(strong_tag.text.strip())
            
            # Extraire les détails de la flotte
            fleet_details = []
            aircraft_list = soup.find('dl', id='list-aircraft')
            
            if aircraft_list:
                # Trouver tous les éléments dt qui contiennent les types d'aircraft
                aircraft_types = aircraft_list.find_all('dt')
                
                for dt in aircraft_types:
                    if 'header' not in dt.get('class', []):
                        divs = dt.find_all('div')
                        if len(divs) >= 2:
                            aircraft_type = divs[0].text.strip()
                            aircraft_count = divs[1].text.strip()
                            
                            try:
                                count = int(aircraft_count)
                                fleet_details.append({
                                    'type': aircraft_type,
                                    'count': count
                                })
                            except ValueError:
                                continue
            
            return {
                'code': airline_code,
                'name': airline_name,
                'total_aircraft': total_aircraft,
                'fleet_details': fleet_details,
                'status': 'success'
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Erreur réseau pour {airline_name}: {e}")
            return {
                'code': airline_code,
                'name': airline_name,
                'total_aircraft': 0,
                'fleet_details': [],
                'status': 'error',
                'error': str(e)
            }
        except Exception as e:
            print(f"Erreur lors du scraping de {airline_name}: {e}")
            return {
                'code': airline_code,
                'name': airline_name,
                'total_aircraft': 0,
                'fleet_details': [],
                'status': 'error',
                'error': str(e)
            }

    def scrape_all_airlines(self, csv_file, max_airlines=None, delay_range=(1, 3)):
        """Scrape toutes les compagnies aériennes"""
        airline_codes = self.extract_airline_codes_from_csv(csv_file)
        
        if not airline_codes:
            print("Aucun code de compagnie trouvé")
            return []
        
        # Limiter le nombre de compagnies si spécifié
        if max_airlines:
            airline_codes = airline_codes[:max_airlines]
            print(f"Limitation à {max_airlines} compagnies pour test")
        
        results = []
        total = len(airline_codes)
        
        for i, airline in enumerate(airline_codes, 1):
            print(f"Progression: {i}/{total}")
            
            result = self.scrape_fleet_data(airline['code'], airline['name'])
            result['original_sigle'] = airline['sigle']
            result['original_aircraft_info'] = airline['aircraft_info']
            
            results.append(result)
            
            # Délai aléatoire entre les requêtes
            if i < total:
                delay = random.uniform(delay_range[0], delay_range[1])
                print(f"Attente de {delay:.1f}s...")
                time.sleep(delay)
        
        return results

    def save_results(self, results, filename='fleet_data.json'):
        """Sauvegarde les résultats en JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"Résultats sauvegardés dans {filename}")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")

    def save_results_csv(self, results, filename='fleet_data.csv'):
        """Sauvegarde les résultats en CSV détaillé"""
        try:
            rows = []
            for airline in results:
                if airline['fleet_details']:
                    for aircraft in airline['fleet_details']:
                        rows.append({
                            'airline_code': airline['code'],
                            'airline_name': airline['name'],
                            'sigle': airline['original_sigle'],
                            'aircraft_type': aircraft['type'],
                            'aircraft_count': aircraft['count'],
                            'total_fleet_size': airline['total_aircraft'],
                            'status': airline['status']
                        })
                else:
                    # Compagnie sans détails de flotte
                    rows.append({
                        'airline_code': airline['code'],
                        'airline_name': airline['name'],
                        'sigle': airline['original_sigle'],
                        'aircraft_type': 'N/A',
                        'aircraft_count': 0,
                        'total_fleet_size': airline['total_aircraft'],
                        'status': airline['status']
                    })
            
            df = pd.DataFrame(rows)
            df.to_csv(filename, index=False, encoding='utf-8')
            print(f"Résultats CSV sauvegardés dans {filename}")
            
        except Exception as e:
            print(f"Erreur lors de la sauvegarde CSV: {e}")

    def generate_summary(self, results):
        """Génère un résumé des résultats"""
        total_airlines = len(results)
        successful_scrapes = len([r for r in results if r['status'] == 'success'])
        failed_scrapes = total_airlines - successful_scrapes
        
        total_aircraft_scraped = sum(r['total_aircraft'] for r in results if r['status'] == 'success')
        
        # Types d'aircraft les plus communs
        aircraft_types = {}
        for airline in results:
            if airline['status'] == 'success':
                for aircraft in airline['fleet_details']:
                    aircraft_type = aircraft['type']
                    if aircraft_type in aircraft_types:
                        aircraft_types[aircraft_type] += aircraft['count']
                    else:
                        aircraft_types[aircraft_type] = aircraft['count']
        
        # Top 10 des types d'aircraft
        top_aircraft = sorted(aircraft_types.items(), key=lambda x: x[1], reverse=True)[:10]
        
        print("\n" + "="*80)
        print("RÉSUMÉ DU SCRAPING FLIGHTRADAR24")
        print("="*80)
        print(f"Compagnies traitées: {total_airlines}")
        print(f"Scraping réussi: {successful_scrapes}")
        print(f"Scraping échoué: {failed_scrapes}")
        print(f"Total aircraft scrapés: {total_aircraft_scraped}")
        
        if top_aircraft:
            print(f"\nTop 10 des types d'aircraft:")
            for aircraft_type, count in top_aircraft:
                print(f"  {aircraft_type}: {count} aircraft")
        
        print("="*80)

def main():
    print("SCRAPER FLIGHTRADAR24 - DONNÉES DE FLOTTE")
    print("="*50)
    
    scraper = FlightRadar24Scraper()
    # Chemin absolu vers le fichier CSV
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    csv_file = os.path.join(project_root, "data", "raw", "flightradar24.csv")
    
    # Vérifier que le fichier CSV existe
    if not os.path.exists(csv_file):
        print(f"Erreur: Le fichier {csv_file} n'existe pas!")
        return
    
    # Options pour le test
    print("Options de scraping:")
    print("1. Test avec 10 compagnies")
    print("2. Test avec 50 compagnies")
    print("3. Scraper toutes les compagnies (ATTENTION: très long!)")
    
    # Accepter un argument en ligne de commande ou demander à l'utilisateur
    if len(sys.argv) > 1:
        choice = sys.argv[1]
        print(f"Choix automatique: {choice}")
    else:
        choice = input("Votre choix (1-3): ").strip()
    
    if choice == "1":
        max_airlines = 10
        delay_range = (0.5, 1.5)
    elif choice == "2":
        max_airlines = 50
        delay_range = (1, 2)
    else:
        max_airlines = None
        delay_range = (2, 4)
    
    print(f"\nDémarrage du scraping...")
    results = scraper.scrape_all_airlines(csv_file, max_airlines, delay_range)
    
    if results:
        # Sauvegarder les résultats dans le dossier processed
        processed_dir = os.path.join(project_root, "data", "processed")
        os.makedirs(processed_dir, exist_ok=True)
        
        json_file = os.path.join(processed_dir, 'fleet_data_complete.json')
        csv_file_output = os.path.join(processed_dir, 'fleet_data_detailed.csv')
        
        scraper.save_results(results, json_file)
        scraper.save_results_csv(results, csv_file_output)
        scraper.generate_summary(results)
        
        print(f"\nScraping terminé! {len(results)} compagnies traitées.")
    else:
        print("Aucun résultat obtenu.")

if __name__ == "__main__":
    main()
