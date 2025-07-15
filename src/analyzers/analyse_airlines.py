#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Programme pour analyser les données des compagnies aériennes
depuis le fichier flightradar24.csv et afficher le nom, le sigle et le nombre d'aircraft
"""

import csv
import pandas as pd
import re

def analyser_airlines_csv(fichier_csv):
    """
    Analyse le fichier CSV des compagnies aériennes et affiche les informations formatées
    
    Args:
        fichier_csv (str): Chemin vers le fichier CSV
    """
    try:
        # Lire le fichier CSV
        df = pd.read_csv(fichier_csv)
        
        # Les colonnes sont: "text-center href", "smalloperatorsymbol src", "notranslate", "text-right", "text-right 2"
        # Nous nous intéressons aux colonnes: nom (notranslate), sigle (text-right), nombre d'aircraft (text-right 2)
        
        # Filtrer les lignes vides et les en-têtes
        df_filtered = df.dropna(subset=['notranslate'])
        df_filtered = df_filtered[df_filtered['notranslate'] != '']
        df_filtered = df_filtered[df_filtered['notranslate'] != 'notranslate']
        
        print("=" * 80)
        print("ANALYSE DES COMPAGNIES AÉRIENNES - FLIGHTRADAR24")
        print("=" * 80)
        print(f"{'NOM DE LA COMPAGNIE':<30} {'SIGLE':<15} {'NOMBRE D\'AIRCRAFT':<20}")
        print("-" * 80)
        
        total_aircraft = 0
        nombre_compagnies = 0
        
        for index, row in df_filtered.iterrows():
            nom = str(row['notranslate']).strip()
            sigle = str(row['text-right']).strip()
            aircraft_info = str(row['text-right 2']).strip()
            
            # Extraire le nombre d'aircraft
            if 'aircraft' in aircraft_info:
                nombre_aircraft = re.findall(r'\d+', aircraft_info)
                if nombre_aircraft:
                    nombre_aircraft_int = int(nombre_aircraft[0])
                    total_aircraft += nombre_aircraft_int
                    nombre_compagnies += 1
                    
                    print(f"{nom:<30} {sigle:<15} {aircraft_info:<20}")
        
        print("-" * 80)
        print(f"RÉSUMÉ:")
        print(f"Nombre total de compagnies: {nombre_compagnies}")
        print(f"Nombre total d'aircraft: {total_aircraft}")
        if nombre_compagnies > 0:
            print(f"Moyenne d'aircraft par compagnie: {total_aircraft/nombre_compagnies:.1f}")
        print("=" * 80)
        
    except FileNotFoundError:
        print(f"Erreur: Le fichier {fichier_csv} n'a pas été trouvé.")
    except Exception as e:
        print(f"Erreur lors de l'analyse du fichier: {e}")

def analyser_avec_csv_reader(fichier_csv):
    """
    Alternative avec le module csv standard pour une lecture plus robuste
    
    Args:
        fichier_csv (str): Chemin vers le fichier CSV
    """
    try:
        airlines_data = []
        
        with open(fichier_csv, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            
            # Ignorer les deux premières lignes (en-têtes)
            next(csv_reader, None)
            next(csv_reader, None)
            
            for row in csv_reader:
                if len(row) >= 5 and row[2] and row[2] != '' and 'aircraft' in row[4]:
                    nom = row[2].strip()
                    sigle = row[3].strip()
                    aircraft_info = row[4].strip()
                    
                    # Extraire le nombre d'aircraft
                    nombre_aircraft = re.findall(r'\d+', aircraft_info)
                    if nombre_aircraft:
                        airlines_data.append({
                            'nom': nom,
                            'sigle': sigle,
                            'aircraft_count': int(nombre_aircraft[0]),
                            'aircraft_info': aircraft_info
                        })
        
        # Trier par nombre d'aircraft (décroissant)
        airlines_data.sort(key=lambda x: x['aircraft_count'], reverse=True)
        
        print("=" * 80)
        print("COMPAGNIES AÉRIENNES TRIÉES PAR NOMBRE D'AIRCRAFT")
        print("=" * 80)
        print(f"{'NOM':<30} {'SIGLE':<15} {'AIRCRAFT':<10} {'INFO COMPLÈTE':<20}")
        print("-" * 80)
        
        total_aircraft = 0
        for airline in airlines_data:
            print(f"{airline['nom']:<30} {airline['sigle']:<15} {airline['aircraft_count']:<10} {airline['aircraft_info']:<20}")
            total_aircraft += airline['aircraft_count']
        
        print("-" * 80)
        print(f"STATISTIQUES:")
        print(f"Nombre de compagnies: {len(airlines_data)}")
        print(f"Total aircraft: {total_aircraft}")
        if airlines_data:
            print(f"Moyenne par compagnie: {total_aircraft/len(airlines_data):.1f}")
            print(f"Compagnie avec le plus d'aircraft: {airlines_data[0]['nom']} ({airlines_data[0]['aircraft_count']} aircraft)")
            print(f"Compagnie avec le moins d'aircraft: {airlines_data[-1]['nom']} ({airlines_data[-1]['aircraft_count']} aircraft)")
        print("=" * 80)
        
    except FileNotFoundError:
        print(f"Erreur: Le fichier {fichier_csv} n'a pas été trouvé.")
    except Exception as e:
        print(f"Erreur lors de l'analyse: {e}")

if __name__ == "__main__":
    fichier_csv = "flightradar24.csv"
    
    print("Choisissez la méthode d'analyse:")
    print("1. Analyse avec pandas")
    print("2. Analyse avec csv reader (recommandé)")
    
    choix = input("Votre choix (1 ou 2): ").strip()
    
    if choix == "1":
        analyser_airlines_csv(fichier_csv)
    else:
        analyser_avec_csv_reader(fichier_csv)
