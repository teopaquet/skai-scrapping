import requests as pyrequests  # pour éviter conflit avec requests de bs4
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
# Ajout du support .env pour Docker
try:
    from dotenv import load_dotenv
    # Recherche le .env à la racine du projet (2 niveaux au-dessus de ce fichier)
    dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../.env'))
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        print(f"[ENV] Fichier .env chargé depuis {dotenv_path}")
    else:
        print(f"[ENV] Aucun fichier .env trouvé à {dotenv_path}")
except ImportError:
    print("[ENV] python-dotenv non installé, les variables d'environnement doivent être définies manuellement.")

class FlightRadar24Scraper:

    def send_csv_telegram(self, file_path):
        """Envoie un fichier CSV via Telegram si les variables d'env sont définies."""
        bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        chat_id = os.environ.get('TELEGRAM_CHAT_ID')
        if not bot_token or not chat_id:
            print("[TELEGRAM] Variables d'environnement non définies, envoi ignoré.")
            return
        url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
        try:
            with open(file_path, 'rb') as f:
                files = {'document': f}
                data = {'chat_id': chat_id, 'caption': os.path.basename(file_path)}
                response = pyrequests.post(url, data=data, files=files, timeout=60)
            if response.status_code == 200:
                print(f"[TELEGRAM] Fichier envoyé avec succès : {file_path}")
            else:
                print(f"[TELEGRAM] Erreur lors de l'envoi : {response.text}")
        except Exception as e:
            print(f"[TELEGRAM] Exception lors de l'envoi : {e}")
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
            
            # Extraire les détails de la flotte avec registrations
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
                                
                                # Récupérer les détails des aircraft individuels
                                aircraft_details = []
                                dd = dt.find_next_sibling('dd')
                                if dd:
                                    table = dd.find('table')
                                    if table:
                                        tbody = table.find('tbody')
                                        if tbody:
                                            rows = tbody.find_all('tr')
                                            for row in rows:
                                                tds = row.find_all('td')
                                                if len(tds) >= 2:
                                                    # Registration - extraire le texte de l'élément <a>
                                                    reg_cell = tds[0]
                                                    reg_link = reg_cell.find('a', class_='regLinks')
                                                    registration = reg_link.text.strip() if reg_link else reg_cell.text.strip()
                                                    
                                                    # Aircraft type détaillé - récupérer le type complet
                                                    detailed_type_cell = tds[1]
                                                    detailed_type = detailed_type_cell.text.strip() if detailed_type_cell else aircraft_type
                                                    
                                                    # Informations supplémentaires si disponibles
                                                    serial_number = tds[2].text.strip() if len(tds) > 2 else 'N/A'
                                                    age = tds[3].text.strip() if len(tds) > 3 else 'N/A'
                                                    
                                                    aircraft_details.append({
                                                        'registration': registration,
                                                        'detailed_type': detailed_type,
                                                        'serial_number': serial_number,
                                                        'age': age
                                                    })
                                
                                fleet_details.append({
                                    'type': aircraft_type,
                                    'count': count,
                                    'aircraft_details': aircraft_details
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
        """Scrape toutes les compagnies aériennes avec retry et sauvegarde intermédiaire"""
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
        # Pour la sauvegarde intermédiaire
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(script_dir))
        processed_dir = os.path.join(project_root, "data", "processed")
        os.makedirs(processed_dir, exist_ok=True)
        for i, airline in enumerate(airline_codes, 1):
            print(f"Progression: {i}/{total}")
            # Retry automatique sur blocage réseau
            max_retries = 5
            retry_wait = 30  # secondes (attente initiale)
            for attempt in range(1, max_retries + 1):
                result = self.scrape_fleet_data(airline['code'], airline['name'])
                if result.get('status') == 'success':
                    break
                else:
                    print(f"[RETRY] Tentative {attempt}/{max_retries} pour {airline['name']} après blocage/erreur...")
                    if attempt < max_retries:
                        wait_time = retry_wait * attempt
                        print(f"Attente de {wait_time} secondes avant retry...")
                        time.sleep(wait_time)
            result['original_sigle'] = airline['sigle']
            result['original_aircraft_info'] = airline['aircraft_info']
            results.append(result)
            # Sauvegarde intermédiaire toutes les 100 compagnies
            if i % 100 == 0 or i == total:
                temp_json = os.path.join(processed_dir, f'fleet_data_partial_{i}.json')
                temp_csv = os.path.join(processed_dir, f'fleet_data_partial_{i}.csv')
                print(f"Sauvegarde intermédiaire après {i} compagnies...")
                self.save_results(results, temp_json)
                self.save_results_csv(results, temp_csv)
                self.send_csv_telegram(temp_csv)
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
        """Sauvegarde les résultats en CSV détaillé avec registrations"""
        try:
            rows = []
            for airline in results:
                if airline['fleet_details']:
                    for aircraft in airline['fleet_details']:
                        # Si on a des détails individuels d'aircraft
                        if aircraft.get('aircraft_details'):
                            for detail in aircraft['aircraft_details']:
                                rows.append({
                                    'airline_code': airline['code'],
                                    'airline_name': airline['name'],
                                    'sigle': airline['original_sigle'],
                                    'aircraft_type': aircraft['type'],
                                    'registration': detail['registration'],
                                    'detailed_aircraft_type': detail['detailed_type'],
                                    'serial_number': detail.get('serial_number', 'N/A'),
                                    'age': detail.get('age', 'N/A'),
                                    'total_fleet_size': airline['total_aircraft'],
                                    'status': airline['status']
                                })
                        else:
                            # Fallback pour les anciens formats
                            rows.append({
                                'airline_code': airline['code'],
                                'airline_name': airline['name'],
                                'sigle': airline['original_sigle'],
                                'aircraft_type': aircraft['type'],
                                'registration': 'N/A',
                                'detailed_aircraft_type': aircraft['type'],
                                'serial_number': 'N/A',
                                'age': 'N/A',
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
                        'registration': 'N/A',
                        'detailed_aircraft_type': 'N/A',
                        'serial_number': 'N/A',
                        'age': 'N/A',
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
        
        print("\n" + "="*80)
        print("RÉSUMÉ DU SCRAPING FLIGHTRADAR24")
        print("="*80)
        print(f"Compagnies traitées: {total_airlines}")
        print(f"Scraping réussi: {successful_scrapes}")
        print(f"Scraping échoué: {failed_scrapes}")
        print(f"Total aircraft scrapés: {total_aircraft_scraped}")
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
