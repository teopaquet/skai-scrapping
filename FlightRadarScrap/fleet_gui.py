"""
FlightRadar24 Fleet Analyzer - Interface Graphique Simplifiée
Application dédiée uniquement à l'analyse des flottes des compagnies aériennes
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import requests
import json
import pandas as pd
from datetime import datetime
import logging
from fake_useragent import UserAgent
from typing import Dict, List
import re
import os

class FlightRadar24FleetAnalyzer:
    """
    Analyseur de flottes simplifié pour FlightRadar24
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
        
        # Variables pour l'interface
        self.is_analyzing = False
        self.progress_callback = None
        self.status_callback = None
    
    def get_flights_in_bounds(self, bounds: Dict[str, float]) -> Dict:
        """Récupère tous les vols dans une zone géographique donnée"""
        try:
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
            
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la requête: {e}")
            return {}
    
    def parse_flights_data(self, raw_data: Dict) -> List[Dict]:
        """Parse les données brutes des vols en format structuré"""
        flights = []
        
        for key, value in raw_data.items():
            if key.isdigit() and isinstance(value, list) and len(value) >= 13:
                flight = {
                    'flight_id': key,
                    'callsign': value[16] if len(value) > 16 else '',
                    'latitude': value[1],
                    'longitude': value[2],
                    'aircraft_type': value[8] if len(value) > 8 else '',
                    'registration': value[9] if len(value) > 9 else '',
                    'airline_icao': value[18] if len(value) > 18 else '',
                }
                flights.append(flight)
        
        return flights
    
    def analyze_fleet(self, bounds: Dict[str, float], duration_minutes: int, progress_callback=None, status_callback=None):
        """Analyse la flotte avec callbacks pour l'interface"""
        self.is_analyzing = True
        self.progress_callback = progress_callback
        self.status_callback = status_callback
        
        try:
            if status_callback:
                status_callback("Début de l'analyse des flottes...")
            
            all_flights = []
            cycles = max(1, duration_minutes // 2)  # Un cycle toutes les 2 minutes
            
            for cycle in range(cycles):
                if not self.is_analyzing:  # Vérifier si l'analyse a été annulée
                    break
                
                if status_callback:
                    status_callback(f"Cycle {cycle + 1}/{cycles} - Collecte des données...")
                
                raw_data = self.get_flights_in_bounds(bounds)
                flights = self.parse_flights_data(raw_data)
                all_flights.extend(flights)
                
                # Mise à jour de la progression
                progress = int((cycle + 1) / cycles * 100)
                if progress_callback:
                    progress_callback(progress)
                
                if cycle < cycles - 1:  # Pas de pause au dernier cycle
                    if status_callback:
                        status_callback(f"Attente avant le prochain cycle... ({cycle + 1}/{cycles})")
                    time.sleep(120)  # Attendre 2 minutes entre les cycles
            
            if status_callback:
                status_callback("Analyse des données collectées...")
            
            fleet_data = self._analyze_fleet_data(all_flights)
            
            if status_callback:
                status_callback("Analyse terminée avec succès!")
            
            return fleet_data
            
        except Exception as e:
            if status_callback:
                status_callback(f"Erreur lors de l'analyse: {e}")
            return {}
        finally:
            self.is_analyzing = False
    
    def _analyze_fleet_data(self, flights: List[Dict]) -> Dict:
        """Analyse les données de vol pour extraire les informations de flotte"""
        fleet_analysis = {}
        
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
                match = re.match(r'^([A-Z]{2,3})', callsign)
                if match:
                    airline_icao = match.group(1)
            
            # Ignorer si pas de données valides
            if not airline_icao or not aircraft_type:
                continue
            
            # Obtenir le nom de la compagnie
            airline_name = airline_codes.get(airline_icao, f"Compagnie {airline_icao}")
            
            # Initialiser la structure pour cette compagnie
            if airline_icao not in fleet_analysis:
                fleet_analysis[airline_icao] = {
                    'airline_name': airline_name,
                    'aircraft_types': {},
                    'registrations': set()
                }
            
            # Ajouter l'immatriculation pour éviter les doublons
            if registration:
                fleet_analysis[airline_icao]['registrations'].add(registration)
            
            # Compter les types d'avions
            if aircraft_type not in fleet_analysis[airline_icao]['aircraft_types']:
                fleet_analysis[airline_icao]['aircraft_types'][aircraft_type] = {
                    'registrations': set()
                }
            
            if registration:
                fleet_analysis[airline_icao]['aircraft_types'][aircraft_type]['registrations'].add(registration)
        
        # Nettoyer et finaliser les données
        for airline_icao in fleet_analysis:
            total = 0
            for aircraft_type in fleet_analysis[airline_icao]['aircraft_types']:
                unique_count = len(fleet_analysis[airline_icao]['aircraft_types'][aircraft_type]['registrations'])
                fleet_analysis[airline_icao]['aircraft_types'][aircraft_type]['count'] = unique_count
                total += unique_count
            
            fleet_analysis[airline_icao]['total_aircraft'] = total
            fleet_analysis[airline_icao]['total_unique_registrations'] = len(fleet_analysis[airline_icao]['registrations'])
        
        return fleet_analysis
    
    def save_fleet_data(self, fleet_data: Dict, filename: str = None) -> str:
        """Sauvegarde l'analyse de flotte"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"fleet_analysis_{timestamp}"
        
        # Sauvegarder en JSON
        json_filename = f"{filename}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            # Convertir les sets en listes pour la sérialisation JSON
            json_data = {}
            for airline_icao, data in fleet_data.items():
                json_data[airline_icao] = {
                    'airline_name': data['airline_name'],
                    'total_aircraft': data['total_aircraft'],
                    'total_unique_registrations': data['total_unique_registrations'],
                    'aircraft_types': {}
                }
                for aircraft_type, type_data in data['aircraft_types'].items():
                    json_data[airline_icao]['aircraft_types'][aircraft_type] = {
                        'count': type_data['count'],
                        'registrations': list(type_data['registrations'])
                    }
            
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        # Sauvegarder en CSV
        csv_filename = f"{filename}.csv"
        csv_data = []
        for airline_icao, data in fleet_data.items():
            for aircraft_type, type_data in data['aircraft_types'].items():
                csv_data.append({
                    'airline_icao': airline_icao,
                    'airline_name': data['airline_name'],
                    'aircraft_type': aircraft_type,
                    'count': type_data['count'],
                    'sample_registrations': ', '.join(list(type_data['registrations'])[:5])
                })
        
        if csv_data:
            df = pd.DataFrame(csv_data)
            df = df.sort_values(['airline_name', 'count'], ascending=[True, False])
            df.to_csv(csv_filename, index=False, encoding='utf-8')
        
        return json_filename, csv_filename
    
    def stop_analysis(self):
        """Arrête l'analyse en cours"""
        self.is_analyzing = False


class FleetAnalyzerGUI:
    """Interface graphique pour l'analyseur de flottes"""
    
    def __init__(self):
        self.analyzer = FlightRadar24FleetAnalyzer()
        self.current_data = None
        self.analysis_thread = None
        
        # Zones prédéfinies
        self.zones = {
            'Monde entier': {
                'north': 80.0,
                'south': -80.0,
                'east': 180.0,
                'west': -180.0
            },
            'Europe': {
                'north': 75.0,
                'south': 30.0,
                'east': 50.0,
                'west': -30.0
            },
            'Amérique du Nord': {
                'north': 70.0,
                'south': 20.0,
                'east': -50.0,
                'west': -180.0
            },
            'Asie': {
                'north': 70.0,
                'south': 0.0,
                'east': 180.0,
                'west': 60.0
            },
            'France': {
                'north': 51.1,
                'south': 42.3,
                'east': 9.6,
                'west': -5.1
            }
        }
        
        self.setup_gui()
    
    def setup_gui(self):
        """Configure l'interface graphique"""
        self.root = tk.Tk()
        self.root.title("FlightRadar24 - Analyseur de Flottes")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuration du grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Titre
        title_label = ttk.Label(main_frame, text="🛩️ Analyseur de Flottes FlightRadar24", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Notebook pour les onglets
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Onglet Scraping
        self.setup_scraping_tab()
        
        # Onglet Visualisation
        self.setup_visualization_tab()
        
        # Frame pour la progression
        self.progress_frame = ttk.LabelFrame(main_frame, text="Progression", padding="10")
        self.progress_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        self.progress_frame.columnconfigure(0, weight=1)
        
        # Barre de progression
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.progress_frame, 
                                          variable=self.progress_var, 
                                          maximum=100)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Label de statut
        self.status_var = tk.StringVar(value="Prêt à analyser")
        self.status_label = ttk.Label(self.progress_frame, textvariable=self.status_var)
        self.status_label.grid(row=1, column=0, sticky=tk.W)
        
        # Bouton d'arrêt
        self.stop_button = ttk.Button(self.progress_frame, text="Arrêter", 
                                    command=self.stop_analysis, state='disabled')
        self.stop_button.grid(row=2, column=0, pady=(5, 0))
    
    def setup_scraping_tab(self):
        """Configure l'onglet de scraping"""
        scraping_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(scraping_frame, text="Scraper")
        
        # Zone géographique
        zone_frame = ttk.LabelFrame(scraping_frame, text="Zone géographique", padding="10")
        zone_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        zone_frame.columnconfigure(1, weight=1)
        
        ttk.Label(zone_frame, text="Zone:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.zone_var = tk.StringVar(value="Europe")
        zone_combo = ttk.Combobox(zone_frame, textvariable=self.zone_var, 
                                 values=list(self.zones.keys()), state='readonly')
        zone_combo.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Durée
        duration_frame = ttk.LabelFrame(scraping_frame, text="Durée d'analyse", padding="10")
        duration_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        duration_frame.columnconfigure(1, weight=1)
        
        ttk.Label(duration_frame, text="Durée:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.duration_var = tk.StringVar(value="Rapide (10 min)")
        duration_combo = ttk.Combobox(duration_frame, textvariable=self.duration_var,
                                    values=["Rapide (10 min)", "Moyen (20 min)", "Long (30 min)", "Maximum (60 min)"],
                                    state='readonly')
        duration_combo.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Bouton de lancement
        self.start_button = ttk.Button(scraping_frame, text="🚀 Commencer l'analyse", 
                                     command=self.start_analysis)
        self.start_button.grid(row=2, column=0, pady=20)
        
        # Résultats
        results_frame = ttk.LabelFrame(scraping_frame, text="Résultats", padding="10")
        results_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        scraping_frame.rowconfigure(3, weight=1)
        
        # Zone de texte pour les résultats
        self.results_text = tk.Text(results_frame, height=10, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Bouton de sauvegarde
        self.save_button = ttk.Button(scraping_frame, text="💾 Sauvegarder les résultats", 
                                    command=self.save_results, state='disabled')
        self.save_button.grid(row=4, column=0, pady=(10, 0))
    
    def setup_visualization_tab(self):
        """Configure l'onglet de visualisation"""
        viz_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(viz_frame, text="Visualiser")
        
        # Boutons de chargement
        load_frame = ttk.Frame(viz_frame)
        load_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Button(load_frame, text="📁 Charger fichier JSON", 
                  command=self.load_json_file).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(load_frame, text="📊 Créer graphiques", 
                  command=self.create_visualizations).grid(row=0, column=1)
        
        # Zone d'affichage des données chargées
        data_frame = ttk.LabelFrame(viz_frame, text="Données chargées", padding="10")
        data_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        data_frame.columnconfigure(0, weight=1)
        data_frame.rowconfigure(0, weight=1)
        viz_frame.rowconfigure(1, weight=1)
        
        # Treeview pour afficher les données
        self.tree = ttk.Treeview(data_frame, columns=('Compagnie', 'Avions', 'Types'), show='headings')
        self.tree.heading('Compagnie', text='Compagnie')
        self.tree.heading('Avions', text='Nb Avions')
        self.tree.heading('Types', text='Nb Types')
        
        tree_scrollbar = ttk.Scrollbar(data_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
    
    def start_analysis(self):
        """Démarre l'analyse en arrière-plan"""
        if self.analysis_thread and self.analysis_thread.is_alive():
            messagebox.showwarning("Analyse en cours", "Une analyse est déjà en cours.")
            return
        
        # Obtenir les paramètres
        zone_name = self.zone_var.get()
        bounds = self.zones[zone_name]
        
        duration_text = self.duration_var.get()
        duration_map = {
            "Rapide (10 min)": 10,
            "Moyen (20 min)": 20,
            "Long (30 min)": 30,
            "Maximum (60 min)": 60
        }
        duration = duration_map[duration_text]
        
        # Désactiver le bouton de démarrage
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.save_button.config(state='disabled')
        
        # Vider les résultats précédents
        self.results_text.delete(1.0, tk.END)
        
        # Lancer l'analyse dans un thread séparé
        self.analysis_thread = threading.Thread(
            target=self._run_analysis,
            args=(bounds, duration, zone_name)
        )
        self.analysis_thread.daemon = True
        self.analysis_thread.start()
    
    def _run_analysis(self, bounds, duration, zone_name):
        """Exécute l'analyse dans un thread séparé"""
        try:
            fleet_data = self.analyzer.analyze_fleet(
                bounds, duration,
                progress_callback=self.update_progress,
                status_callback=self.update_status
            )
            
            if fleet_data:
                self.current_data = fleet_data
                self.root.after(0, self._display_results, fleet_data, zone_name)
            else:
                self.root.after(0, self.update_status, "Aucune donnée collectée")
                
        except Exception as e:
            self.root.after(0, self.update_status, f"Erreur: {e}")
        finally:
            self.root.after(0, self._analysis_finished)
    
    def _analysis_finished(self):
        """Appelé quand l'analyse est terminée"""
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        if self.current_data:
            self.save_button.config(state='normal')
    
    def _display_results(self, fleet_data, zone_name):
        """Affiche les résultats dans l'interface"""
        self.results_text.delete(1.0, tk.END)
        
        # Titre
        self.results_text.insert(tk.END, f"📊 ANALYSE DES FLOTTES - {zone_name.upper()}\n")
        self.results_text.insert(tk.END, "="*60 + "\n\n")
        
        # Statistiques globales
        total_airlines = len(fleet_data)
        total_aircraft = sum(data['total_aircraft'] for data in fleet_data.values())
        
        self.results_text.insert(tk.END, f"📈 STATISTIQUES GLOBALES\n")
        self.results_text.insert(tk.END, f"   Compagnies analysées: {total_airlines}\n")
        self.results_text.insert(tk.END, f"   Total d'avions observés: {total_aircraft}\n\n")
        
        # Top compagnies
        sorted_airlines = sorted(fleet_data.items(), 
                               key=lambda x: x[1]['total_aircraft'], 
                               reverse=True)
        
        self.results_text.insert(tk.END, f"🏆 TOP 15 COMPAGNIES\n")
        self.results_text.insert(tk.END, "-"*40 + "\n")
        
        for i, (airline_icao, data) in enumerate(sorted_airlines[:15], 1):
            self.results_text.insert(tk.END, 
                f"{i:2d}. {data['airline_name']:<25} {data['total_aircraft']:3d} avions "
                f"({len(data['aircraft_types'])} types)\n")
        
        # Détail par compagnie
        self.results_text.insert(tk.END, f"\n📋 DÉTAIL PAR COMPAGNIE\n")
        self.results_text.insert(tk.END, "-"*40 + "\n")
        
        for airline_icao, data in sorted_airlines[:10]:  # Top 10 détaillé
            self.results_text.insert(tk.END, f"\n✈️ {data['airline_name']} ({airline_icao})\n")
            self.results_text.insert(tk.END, f"   Total: {data['total_aircraft']} avions\n")
            
            # Types d'avions
            aircraft_sorted = sorted(data['aircraft_types'].items(), 
                                   key=lambda x: x[1]['count'], 
                                   reverse=True)
            
            for aircraft_type, type_data in aircraft_sorted[:5]:  # Top 5 types
                self.results_text.insert(tk.END, 
                    f"   • {aircraft_type}: {type_data['count']} avion(s)\n")
        
        # Mettre à jour le treeview
        self.update_treeview(fleet_data)
    
    def update_treeview(self, fleet_data):
        """Met à jour le treeview avec les données"""
        # Vider le treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Ajouter les données
        sorted_airlines = sorted(fleet_data.items(), 
                               key=lambda x: x[1]['total_aircraft'], 
                               reverse=True)
        
        for airline_icao, data in sorted_airlines:
            self.tree.insert('', 'end', values=(
                data['airline_name'],
                data['total_aircraft'],
                len(data['aircraft_types'])
            ))
    
    def update_progress(self, value):
        """Met à jour la barre de progression"""
        self.progress_var.set(value)
    
    def update_status(self, message):
        """Met à jour le message de statut"""
        self.status_var.set(message)
    
    def stop_analysis(self):
        """Arrête l'analyse en cours"""
        self.analyzer.stop_analysis()
        self.update_status("Analyse arrêtée par l'utilisateur")
    
    def save_results(self):
        """Sauvegarde les résultats"""
        if not self.current_data:
            messagebox.showwarning("Aucune donnée", "Aucune donnée à sauvegarder.")
            return
        
        # Demander le nom du fichier
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")],
            title="Sauvegarder l'analyse de flotte"
        )
        
        if filename:
            try:
                # Enlever l'extension si présente
                if filename.endswith('.json'):
                    filename = filename[:-5]
                
                json_file, csv_file = self.analyzer.save_fleet_data(self.current_data, filename)
                messagebox.showinfo("Sauvegarde réussie", 
                                  f"Données sauvegardées:\n• {json_file}\n• {csv_file}")
            except Exception as e:
                messagebox.showerror("Erreur de sauvegarde", f"Erreur lors de la sauvegarde: {e}")
    
    def load_json_file(self):
        """Charge un fichier JSON existant"""
        filename = filedialog.askopenfilename(
            filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")],
            title="Charger une analyse de flotte"
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.current_data = data
                self.update_treeview(data)
                self.save_button.config(state='normal')
                messagebox.showinfo("Chargement réussi", "Données chargées avec succès!")
                
            except Exception as e:
                messagebox.showerror("Erreur de chargement", f"Erreur lors du chargement: {e}")
    
    def create_visualizations(self):
        """Crée des visualisations des données"""
        if not self.current_data:
            messagebox.showwarning("Aucune donnée", "Veuillez d'abord charger ou analyser des données.")
            return
        
        try:
            import matplotlib.pyplot as plt
            import numpy as np
            
            # Préparer les données
            airlines = []
            aircraft_counts = []
            type_counts = []
            
            sorted_airlines = sorted(self.current_data.items(), 
                                   key=lambda x: x[1]['total_aircraft'], 
                                   reverse=True)[:15]  # Top 15
            
            for airline_icao, data in sorted_airlines:
                airlines.append(data['airline_name'][:20])  # Tronquer les noms longs
                aircraft_counts.append(data['total_aircraft'])
                type_counts.append(len(data['aircraft_types']))
            
            # Créer les graphiques
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
            
            # Graphique 1: Nombre d'avions par compagnie
            y_pos = np.arange(len(airlines))
            ax1.barh(y_pos, aircraft_counts, color='skyblue')
            ax1.set_yticks(y_pos)
            ax1.set_yticklabels(airlines)
            ax1.set_xlabel('Nombre d\'avions')
            ax1.set_title('Top 15 Compagnies par Nombre d\'Avions')
            ax1.invert_yaxis()
            
            # Graphique 2: Diversité des flottes
            ax2.barh(y_pos, type_counts, color='lightcoral')
            ax2.set_yticks(y_pos)
            ax2.set_yticklabels(airlines)
            ax2.set_xlabel('Nombre de types d\'avions')
            ax2.set_title('Diversité des Flottes')
            ax2.invert_yaxis()
            
            plt.tight_layout()
            plt.show()
            
        except ImportError:
            messagebox.showerror("Matplotlib requis", 
                               "Veuillez installer matplotlib pour créer des visualisations:\n"
                               "pip install matplotlib")
        except Exception as e:
            messagebox.showerror("Erreur de visualisation", f"Erreur lors de la création des graphiques: {e}")
    
    def run(self):
        """Lance l'interface graphique"""
        self.root.mainloop()


def main():
    """Point d'entrée principal"""
    app = FleetAnalyzerGUI()
    app.run()


if __name__ == "__main__":
    main()
