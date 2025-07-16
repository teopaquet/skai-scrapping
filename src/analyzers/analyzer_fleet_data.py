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
import streamlit as st

class FleetDataAnalyzer:
    def __init__(self, csv_file='fleet_data_2800.csv'):
        self.csv_file = csv_file
        self.df = None
        self.load_data()

    def load_data(self):
        """Charge les données depuis le fichier CSV uniquement"""
        try:
            self.df = pd.read_csv(self.csv_file)
            print(f"Données CSV chargées: {len(self.df)} lignes")
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
        print("RAPPORT D'ANALYSE DES FLOTTES AÉRIENNES - AIRCRAFT INDIVIDUELS")
        print("="*80)
        
        # Statistiques générales
        total_airlines = self.df['airline_name'].nunique()
        total_aircraft_types = self.df['detailed_aircraft_type'].nunique()
        total_aircraft = len(self.df)
        total_registrations = self.df['registration'].nunique()
        
        print(f"Nombre de compagnies analysées: {total_airlines}")
        print(f"Nombre d'aircraft individuels enregistrés: {total_aircraft}")
        print(f"Nombre d'immatriculations uniques: {total_registrations}")
        print(f"Nombre de types d'aircraft différents: {total_aircraft_types}")
        
        # Top 10 des compagnies par taille de flotte
        print(f"\nTOP 10 DES COMPAGNIES PAR TAILLE DE FLOTTE:")
        print("-" * 50)
        fleet_sizes = self.df.groupby('airline_name')['total_fleet_size'].first().sort_values(ascending=False)
        top_airlines = fleet_sizes.head(10)
        
        for airline_name, fleet_size in top_airlines.items():
            print(f"{airline_name:<30} {fleet_size:>5} aircraft")
        
        # Top 10 des types d'aircraft les plus communs
        print(f"\nTOP 10 DES TYPES D'AIRCRAFT LES PLUS COMMUNS:")
        print("-" * 50)
        aircraft_counts = self.df['detailed_aircraft_type'].value_counts()
        top_aircraft = aircraft_counts.head(10)
        
        for aircraft_type, count in top_aircraft.items():
            if aircraft_type != 'N/A':
                print(f"{aircraft_type:<40} {count:>5} aircraft")
        
        # Analyse des flottes par taille
        print(f"\nRÉPARTITION DES COMPAGNIES PAR TAILLE DE FLOTTE:")
        print("-" * 50)
        fleet_sizes_unique = fleet_sizes
        
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
        
        # Grouper par type d'aircraft détaillé
        aircraft_analysis = self.df.groupby('detailed_aircraft_type').agg({
            'registration': 'count',  # Nombre d'aircraft individuels
            'airline_name': 'nunique'  # Nombre de compagnies utilisant ce type
        }).round(2)

        aircraft_analysis.columns = ['Total_Aircraft', 'Num_Airlines']
        aircraft_analysis['Avg_Per_Airline'] = (aircraft_analysis['Total_Aircraft'] / aircraft_analysis['Num_Airlines']).round(2)
        aircraft_analysis = aircraft_analysis.sort_values('Total_Aircraft', ascending=False)
        
        # Top 15 avec statistiques détaillées
        print("TOP 15 DES TYPES D'AIRCRAFT (avec statistiques):")
        print("-" * 90)
        print(f"{'Type':<40} {'Total':<8} {'Compagnies':<12} {'Moy/Comp':<10}")
        print("-" * 90)
        
        for aircraft_type, row in aircraft_analysis.head(15).iterrows():
            if aircraft_type != 'N/A' and str(aircraft_type) != 'nan':
                print(f"{aircraft_type:<40} {int(row['Total_Aircraft']):<8} {int(row['Num_Airlines']):<12} {row['Avg_Per_Airline']:<10.1f}")
    
        # Analyse par code d'aircraft (plus général)
        print(f"\n\nANALYSE PAR CODE D'AIRCRAFT (GROUPÉ):")
        print("-" * 60)
        
        code_analysis = self.df.groupby('aircraft_type').agg({
            'registration': 'count',
            'airline_name': 'nunique'
        }).sort_values('registration', ascending=False)

        code_analysis.columns = ['Total_Aircraft', 'Num_Airlines']
        
        print(f"{'Code':<8} {'Total':<8} {'Compagnies':<12}")
        print("-" * 30)
        
        for code, row in code_analysis.head(10).iterrows():
            if code != 'N/A' and str(code) != 'nan':
                print(f"{code:<8} {int(row['Total_Aircraft']):<8} {int(row['Num_Airlines']):<12}")
    
    def find_aircraft_specialists(self):
        """Trouve les compagnies spécialisées dans certains types d'aircraft"""
        if self.df is None:
            return
        
        print("\n" + "="*60)
        print("COMPAGNIES SPÉCIALISÉES PAR TYPE D'AIRCRAFT")
        print("="*60)
        
        # Analyser les compagnies avec un seul type d'aircraft
        single_type_airlines = self.df.groupby('airline_name').agg({
            'detailed_aircraft_type': 'nunique',
            'total_fleet_size': 'first',
            'registration': 'count'
        })

        # Filtrer les compagnies avec un seul type et plus de 3 aircraft
        specialists = single_type_airlines[
            (single_type_airlines['detailed_aircraft_type'] == 1) & 
            (single_type_airlines['total_fleet_size'] > 3)
        ]
        
        if not specialists.empty:
            print("Compagnies mono-type (>3 aircraft):")
            print("-" * 60)
            
            for airline_name in specialists.index:
                airline_data = self.df[self.df['airline_name'] == airline_name].iloc[0]
                aircraft_type = airline_data['detailed_aircraft_type']
                fleet_size = airline_data['total_fleet_size']
                aircraft_count = specialists.loc[airline_name, 'registration']
                print(f"{airline_name:<25} {aircraft_type:<25} ({fleet_size} total, {aircraft_count} vus)")
        
        # Analyse des compagnies avec le plus d'aircraft d'un même type
        print(f"\nCOMPAGNIES AVEC LE PLUS D'AIRCRAFT D'UN MÊME TYPE:")
        print("-" * 60)
        
        type_specialists = self.df.groupby(['airline_name', 'detailed_aircraft_type']).size().reset_index(name='count')
        type_specialists = type_specialists.sort_values('count', ascending=False).head(10)
        
        for _, row in type_specialists.iterrows():
            print(f"{row['airline_name']:<25} {row['aircraft_type_detail']:<25} ({row['count']} aircraft)")
    
    def export_analysis_to_csv(self, filename='individual_aircraft_analysis_summary.csv'):
        """Exporte une analyse résumée en CSV"""
        if self.df is None:
            return
        
        try:
            # Créer un résumé par compagnie
            company_summary = self.df.groupby(['airline_name', 'sigle', 'total_fleet_size']).agg({
                'detailed_aircraft_type': lambda x: ', '.join([str(t) for t in x.unique() if str(t) != 'nan']),
                'aircraft_type': lambda x: ', '.join([str(t) for t in x.unique() if str(t) != 'nan']),
                'registration': 'count'
            }).reset_index()

            company_summary.columns = ['Airline_Name', 'IATA_ICAO', 'Total_Fleet_Size', 'Aircraft_Types_Detail', 'Aircraft_Codes', 'Aircraft_Count_Observed']

            # Ajouter le nombre de types différents
            company_summary['Number_of_Aircraft_Types'] = company_summary['Aircraft_Types_Detail'].apply(
                lambda x: len([t.strip() for t in x.split(',') if t.strip() != 'N/A'])
            )

            # Ajouter le pourcentage de la flotte observée
            company_summary['Fleet_Coverage_Percent'] = (
                company_summary['Aircraft_Count_Observed'] / company_summary['Total_Fleet_Size'] * 100
            ).round(2)

            company_summary = company_summary.sort_values('Total_Fleet_Size', ascending=False)
            company_summary.to_csv(filename, index=False, encoding='utf-8')
            print(f"\nAnalyse exportée vers: {filename}")

            # Créer aussi un export détaillé par aircraft
            detailed_filename = 'individual_aircraft_detailed_analysis.csv'
            aircraft_analysis = self.df.groupby('detailed_aircraft_type').agg({
                'registration': 'count',
                'airline_name': 'nunique',
                'aircraft_type': 'first'
            }).reset_index()

            aircraft_analysis.columns = ['Aircraft_Type_Detail', 'Total_Count', 'Airlines_Using', 'Aircraft_Code']
            aircraft_analysis = aircraft_analysis.sort_values('Total_Count', ascending=False)
            aircraft_analysis.to_csv(detailed_filename, index=False, encoding='utf-8')
            print(f"Analyse détaillée par type exportée vers: {detailed_filename}")
        except Exception as e:
            print(f"Erreur lors de l'export: {e}")
    
    def create_visualizations(self):
        """Crée des visualisations des données (nécessite matplotlib)"""
        if self.df is None:
            return
        
        try:
            plt.style.use('default')
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            fig.suptitle('Analyse des Aircraft Individuels - FlightRadar24', fontsize=16)

            # 1. Distribution des tailles de flotte
            fleet_sizes = self.df.drop_duplicates('airline_name')['total_fleet_size']
            axes[0, 0].hist(fleet_sizes, bins=30, edgecolor='black', alpha=0.7)
            axes[0, 0].set_title('Distribution des Tailles de Flotte')
            axes[0, 0].set_xlabel('Nombre d\'Aircraft')
            axes[0, 0].set_ylabel('Nombre de Compagnies')

            # 2. Top 10 des types d'aircraft (codes)
            top_aircraft = self.df['aircraft_type'].value_counts().head(10)
            top_aircraft = top_aircraft[top_aircraft.index != 'N/A']
            axes[0, 1].bar(range(len(top_aircraft)), top_aircraft.values)
            axes[0, 1].set_title('Top 10 des Codes d\'Aircraft')
            axes[0, 1].set_xlabel('Code d\'Aircraft')
            axes[0, 1].set_ylabel('Nombre d\'Aircraft Individuels')
            axes[0, 1].set_xticks(range(len(top_aircraft)))
            axes[0, 1].set_xticklabels(top_aircraft.index, rotation=45)

            # 3. Top 10 des compagnies par nombre d'aircraft observés
            company_counts = self.df.groupby('airline_name').size().sort_values(ascending=False).head(10)
            axes[1, 0].barh(range(len(company_counts)), company_counts.values)
            axes[1, 0].set_title('Top 10 Compagnies par Aircraft Observés')
            axes[1, 0].set_xlabel('Nombre d\'Aircraft Observés')
            axes[1, 0].set_yticks(range(len(company_counts)))
            axes[1, 0].set_yticklabels([name[:20] + '...' if len(name) > 20 else name for name in company_counts.index])

            # 4. Nombre de types d'aircraft par compagnie
            types_per_company = self.df.groupby('airline_name')['detailed_aircraft_type'].nunique()
            axes[1, 1].hist(types_per_company, bins=15, edgecolor='black', alpha=0.7)
            axes[1, 1].set_title('Diversité des Flottes (Types par Compagnie)')
            axes[1, 1].set_xlabel('Nombre de Types d\'Aircraft Différents')
            axes[1, 1].set_ylabel('Nombre de Compagnies')

            plt.tight_layout()
            plt.savefig('individual_aircraft_analysis_charts.png', dpi=300, bbox_inches='tight')
            print("\nGraphiques sauvegardés dans: individual_aircraft_analysis_charts.png")
        except ImportError:
            print("Matplotlib non disponible pour les visualisations")
        except Exception as e:
            print(f"Erreur lors de la création des graphiques: {e}")

# Interface graphique moderne avec Streamlit


def main():
    st.set_page_config(page_title="Analyse Flotte Aérienne", layout="wide")
    st.title("Analyse de la Flotte Aérienne - FlightRadar24")
    st.markdown("""
        <style>
        .main {background-color: #f5f7fa;}
        </style>
    """, unsafe_allow_html=True)

    analyzer = FleetDataAnalyzer(csv_file='../../data/processed/fleet_data_2800.csv')

    if analyzer.df is not None:
        st.success(f"Données chargées: {len(analyzer.df)} lignes")

        # Statistiques générales
        st.header("Statistiques Générales")
        total_airlines = analyzer.df['airline_name'].nunique()
        total_aircraft_types = analyzer.df['detailed_aircraft_type'].nunique()
        total_aircraft = len(analyzer.df)
        total_registrations = analyzer.df['registration'].nunique()

        st.metric("Compagnies analysées", total_airlines)
        st.metric("Aircraft individuels enregistrés", total_aircraft)
        st.metric("Immatriculations uniques", total_registrations)
        st.metric("Types d'aircraft différents", total_aircraft_types)

        # Top compagnies par taille de flotte
        st.subheader("Top 10 des compagnies par taille de flotte")
        fleet_sizes = analyzer.df.groupby('airline_name')['total_fleet_size'].first().sort_values(ascending=False)
        top_airlines = fleet_sizes.head(10)
        st.dataframe(top_airlines.reset_index().rename(columns={"airline_name": "Compagnie", "total_fleet_size": "Taille de flotte"}))

        # Top types d'aircraft
        st.subheader("Top 10 des types d'aircraft les plus communs")
        aircraft_counts = analyzer.df['detailed_aircraft_type'].value_counts().head(10)
        st.bar_chart(aircraft_counts)

        # Diversité des flottes
        st.subheader("Diversité des flottes (types par compagnie)")
        types_per_company = analyzer.df.groupby('airline_name')['detailed_aircraft_type'].nunique()
        st.bar_chart(types_per_company)

        # Visualisation interactive
        st.subheader("Visualisation interactive")
        import plotly.express as px
        fig = px.scatter(
            analyzer.df,
            x="total_fleet_size",
            y="airline_name",
            color="detailed_aircraft_type",
            title="Répartition des compagnies par taille de flotte et type d'aircraft",
            labels={
                "total_fleet_size": "Taille de flotte",
                "airline_name": "Compagnie",
                "detailed_aircraft_type": "Type d'aircraft"
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Impossible de charger les données. Assurez-vous que le fichier fleet_data_2800.csv existe.")

if __name__ == "__main__":
    main()
