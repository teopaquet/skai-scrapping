#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyseur des données de flotte scrapées depuis FlightRadar24
"""

import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import numpy as np

class FleetDataAnalyzer:
    def __init__(self, csv_file='fleet_data_detailed.csv', json_file='fleet_data_complete.json'):
        self.csv_file = csv_file
        self.json_file = json_file
        self.df = None
        self.raw_data = None
        self.load_data()
    
    def load_data(self):
        """Charge les données depuis les fichiers"""
        try:
            self.df = pd.read_csv(self.csv_file)
            print(f"Données CSV chargées: {len(self.df)} lignes")
            
            with open(self.json_file, 'r', encoding='utf-8') as f:
                self.raw_data = json.load(f)
            print(f"Données JSON chargées: {len(self.raw_data)} compagnies")
            
        except FileNotFoundError as e:
            print(f"Fichier non trouvé: {e}")
        except Exception as e:
            print(f"Erreur lors du chargement: {e}")
    
    def generate_summary_report(self):
        """Génère un rapport de synthèse"""
        if self.df is None:
            print("Aucune donnée chargée")
            return
        
        print("\n" + "="*80)
        print("RAPPORT D'ANALYSE DES FLOTTES AÉRIENNES")
        print("="*80)
        
        # Statistiques générales
        total_airlines = self.df['airline_name'].nunique()
        total_aircraft_types = self.df['aircraft_type'].nunique()
        total_aircraft = self.df['aircraft_count'].sum()
        
        print(f"Nombre de compagnies analysées: {total_airlines}")
        print(f"Nombre de types d'aircraft différents: {total_aircraft_types}")
        print(f"Nombre total d'aircraft: {total_aircraft}")
        
        # Top 10 des compagnies par taille de flotte
        print(f"\nTOP 10 DES COMPAGNIES PAR TAILLE DE FLOTTE:")
        print("-" * 50)
        fleet_sizes = self.df.groupby(['airline_name', 'total_fleet_size']).size().reset_index()
        fleet_sizes = fleet_sizes.drop_duplicates('airline_name')
        top_airlines = fleet_sizes.nlargest(10, 'total_fleet_size')
        
        for _, airline in top_airlines.iterrows():
            print(f"{airline['airline_name']:<30} {airline['total_fleet_size']:>5} aircraft")
        
        # Top 10 des types d'aircraft les plus communs
        print(f"\nTOP 10 DES TYPES D'AIRCRAFT LES PLUS COMMUNS:")
        print("-" * 50)
        aircraft_counts = self.df.groupby('aircraft_type')['aircraft_count'].sum().sort_values(ascending=False)
        top_aircraft = aircraft_counts.head(10)
        
        for aircraft_type, count in top_aircraft.items():
            if aircraft_type != 'N/A':
                print(f"{aircraft_type:<10} {count:>5} aircraft")
        
        # Analyse des flottes par taille
        print(f"\nRÉPARTITION DES COMPAGNIES PAR TAILLE DE FLOTTE:")
        print("-" * 50)
        fleet_sizes_unique = fleet_sizes['total_fleet_size']
        
        size_categories = [
            ("1 aircraft", (fleet_sizes_unique == 1).sum()),
            ("2-5 aircraft", ((fleet_sizes_unique >= 2) & (fleet_sizes_unique <= 5)).sum()),
            ("6-20 aircraft", ((fleet_sizes_unique >= 6) & (fleet_sizes_unique <= 20)).sum()),
            ("21-50 aircraft", ((fleet_sizes_unique >= 21) & (fleet_sizes_unique <= 50)).sum()),
            ("51+ aircraft", (fleet_sizes_unique > 50).sum())
        ]
        
        for category, count in size_categories:
            percentage = (count / total_airlines) * 100
            print(f"{category:<15} {count:>3} compagnies ({percentage:.1f}%)")
        
        print("="*80)
    
    def analyze_aircraft_types(self):
        """Analyse détaillée des types d'aircraft"""
        if self.df is None:
            return
        
        print("\n" + "="*80)
        print("ANALYSE DES TYPES D'AIRCRAFT")
        print("="*80)
        
        # Grouper par type d'aircraft
        aircraft_analysis = self.df.groupby('aircraft_type').agg({
            'aircraft_count': ['sum', 'mean', 'count'],
            'airline_name': 'nunique'
        }).round(2)
        
        aircraft_analysis.columns = ['Total_Aircraft', 'Avg_Per_Airline', 'Airlines_Using', 'Num_Airlines']
        aircraft_analysis = aircraft_analysis.sort_values('Total_Aircraft', ascending=False)
        
        # Top 15 avec statistiques détaillées
        print("TOP 15 DES TYPES D'AIRCRAFT (avec statistiques):")
        print("-" * 80)
        print(f"{'Type':<8} {'Total':<8} {'Compagnies':<12} {'Moy/Comp':<10} {'Airlines':<10}")
        print("-" * 80)
        
        for aircraft_type, row in aircraft_analysis.head(15).iterrows():
            if aircraft_type != 'N/A':
                print(f"{aircraft_type:<8} {int(row['Total_Aircraft']):<8} {int(row['Airlines_Using']):<12} {row['Avg_Per_Airline']:<10.1f} {int(row['Num_Airlines']):<10}")
    
    def find_aircraft_specialists(self):
        """Trouve les compagnies spécialisées dans certains types d'aircraft"""
        if self.df is None:
            return
        
        print("\n" + "="*60)
        print("COMPAGNIES SPÉCIALISÉES PAR TYPE D'AIRCRAFT")
        print("="*60)
        
        # Analyser les compagnies avec un seul type d'aircraft
        single_type_airlines = self.df.groupby('airline_name').agg({
            'aircraft_type': 'nunique',
            'total_fleet_size': 'first'
        })
        
        # Filtrer les compagnies avec un seul type et plus de 3 aircraft
        specialists = single_type_airlines[
            (single_type_airlines['aircraft_type'] == 1) & 
            (single_type_airlines['total_fleet_size'] > 3)
        ]
        
        if not specialists.empty:
            print("Compagnies mono-type (>3 aircraft):")
            print("-" * 40)
            
            for airline_name in specialists.index:
                airline_data = self.df[self.df['airline_name'] == airline_name].iloc[0]
                aircraft_type = airline_data['aircraft_type']
                fleet_size = airline_data['total_fleet_size']
                print(f"{airline_name:<25} {aircraft_type:<8} ({fleet_size} aircraft)")
    
    def export_analysis_to_csv(self, filename='fleet_analysis_summary.csv'):
        """Exporte une analyse résumée en CSV"""
        if self.df is None:
            return
        
        try:
            # Créer un résumé par compagnie
            company_summary = self.df.groupby(['airline_name', 'sigle', 'total_fleet_size']).agg({
                'aircraft_type': lambda x: ', '.join(x.astype(str)),
                'aircraft_count': 'sum'
            }).reset_index()
            
            company_summary.columns = ['Airline_Name', 'IATA_ICAO', 'Total_Fleet_Size', 'Aircraft_Types', 'Total_Count_Verified']
            
            # Ajouter le nombre de types différents
            company_summary['Number_of_Aircraft_Types'] = company_summary['Aircraft_Types'].apply(
                lambda x: len([t.strip() for t in x.split(',') if t.strip() != 'N/A'])
            )
            
            company_summary.to_csv(filename, index=False, encoding='utf-8')
            print(f"\nAnalyse exportée vers: {filename}")
            
        except Exception as e:
            print(f"Erreur lors de l'export: {e}")
    
    def create_visualizations(self):
        """Crée des visualisations des données (nécessite matplotlib)"""
        if self.df is None:
            return
        
        try:
            plt.style.use('default')
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            fig.suptitle('Analyse des Flottes Aériennes FlightRadar24', fontsize=16)
            
            # 1. Distribution des tailles de flotte
            fleet_sizes = self.df.drop_duplicates('airline_name')['total_fleet_size']
            axes[0, 0].hist(fleet_sizes, bins=30, edgecolor='black', alpha=0.7)
            axes[0, 0].set_title('Distribution des Tailles de Flotte')
            axes[0, 0].set_xlabel('Nombre d\'Aircraft')
            axes[0, 0].set_ylabel('Nombre de Compagnies')
            
            # 2. Top 10 des types d'aircraft
            top_aircraft = self.df.groupby('aircraft_type')['aircraft_count'].sum().sort_values(ascending=False).head(10)
            top_aircraft = top_aircraft[top_aircraft.index != 'N/A']
            axes[0, 1].bar(range(len(top_aircraft)), top_aircraft.values)
            axes[0, 1].set_title('Top 10 des Types d\'Aircraft')
            axes[0, 1].set_xlabel('Type d\'Aircraft')
            axes[0, 1].set_ylabel('Nombre Total')
            axes[0, 1].set_xticks(range(len(top_aircraft)))
            axes[0, 1].set_xticklabels(top_aircraft.index, rotation=45)
            
            # 3. Top 10 des compagnies par taille
            company_sizes = self.df.groupby('airline_name')['total_fleet_size'].first().sort_values(ascending=False).head(10)
            axes[1, 0].barh(range(len(company_sizes)), company_sizes.values)
            axes[1, 0].set_title('Top 10 des Compagnies par Taille')
            axes[1, 0].set_xlabel('Nombre d\'Aircraft')
            axes[1, 0].set_yticks(range(len(company_sizes)))
            axes[1, 0].set_yticklabels([name[:20] + '...' if len(name) > 20 else name for name in company_sizes.index])
            
            # 4. Nombre de types d'aircraft par compagnie
            types_per_company = self.df.groupby('airline_name')['aircraft_type'].nunique()
            axes[1, 1].hist(types_per_company, bins=15, edgecolor='black', alpha=0.7)
            axes[1, 1].set_title('Diversité des Flottes')
            axes[1, 1].set_xlabel('Nombre de Types d\'Aircraft')
            axes[1, 1].set_ylabel('Nombre de Compagnies')
            
            plt.tight_layout()
            plt.savefig('fleet_analysis_charts.png', dpi=300, bbox_inches='tight')
            print("\nGraphiques sauvegardés dans: fleet_analysis_charts.png")
            
        except ImportError:
            print("Matplotlib non disponible pour les visualisations")
        except Exception as e:
            print(f"Erreur lors de la création des graphiques: {e}")

def main():
    print("ANALYSEUR DE DONNÉES FLIGHTRADAR24")
    print("=" * 50)
    
    analyzer = FleetDataAnalyzer()
    
    if analyzer.df is not None:
        analyzer.generate_summary_report()
        analyzer.analyze_aircraft_types()
        analyzer.find_aircraft_specialists()
        analyzer.export_analysis_to_csv()
        
        # Demander si l'utilisateur veut des graphiques
        create_charts = input("\nCréer des graphiques de visualisation? (y/N): ").strip().lower()
        if create_charts == 'y':
            analyzer.create_visualizations()
        
        print("\nAnalyse terminée!")
    else:
        print("Impossible de charger les données. Assurez-vous d'avoir exécuté le scraper d'abord.")

if __name__ == "__main__":
    main()
