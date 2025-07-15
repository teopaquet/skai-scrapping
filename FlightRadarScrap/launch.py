"""
Script de lancement simplifié pour FlightRadar24 Fleet Analyzer
"""

import sys
import os

def main():
    print("🛩️ FlightRadar24 Fleet Analyzer")
    print("=" * 40)
    
    # Vérifier les dépendances
    try:
        import requests
        import pandas
        import fake_useragent
        print("✅ Dépendances de base OK")
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        print("💡 Installez avec: pip install -r requirements.txt")
        return
    
    # Tenter de lancer l'interface graphique
    try:
        import tkinter as tk
        print("✅ Interface graphique disponible")
        print("🚀 Lancement de l'interface...")
        
        # Lancer l'interface graphique
        from fleet_gui import FleetAnalyzerGUI
        app = FleetAnalyzerGUI()
        app.run()
        
    except ImportError:
        print("❌ Tkinter non disponible")
        print("🔄 Basculement vers le mode console...")
        
        # Mode console de base
        from main import FlightRadar24FleetAnalyzer
        
        analyzer = FlightRadar24FleetAnalyzer()
        
        print("\n📍 Zones d'analyse disponibles:")
        print("1. Europe (recommandé)")
        print("2. France") 
        print("3. Monde entier")
        
        try:
            choice = input("\nChoisissez une zone (1-3): ").strip()
            
            zones = {
                '1': ('Europe', {'north': 75.0, 'south': 30.0, 'east': 50.0, 'west': -30.0}),
                '2': ('France', {'north': 51.1, 'south': 42.3, 'east': 9.6, 'west': -5.1}),
                '3': ('Monde', {'north': 80.0, 'south': -80.0, 'east': 180.0, 'west': -180.0})
            }
            
            if choice in zones:
                zone_name, bounds = zones[choice]
                print(f"\n🔍 Analyse de la zone: {zone_name}")
                print("⏳ Collecte des données en cours (10 minutes)...")
                print("   Vous pouvez interrompre avec Ctrl+C")
                
                fleet_data = analyzer.get_airline_fleet_analysis(bounds, 10)
                
                if fleet_data:
                    analyzer.print_fleet_summary(fleet_data)
                    
                    # Sauvegarder
                    json_file, csv_file = analyzer.save_fleet_data(fleet_data)
                    print(f"\n💾 Données sauvegardées:")
                    print(f"   📋 JSON: {json_file}")
                    print(f"   📊 CSV: {csv_file}")
                else:
                    print("❌ Aucune donnée collectée")
            else:
                print("❌ Choix invalide")
                
        except KeyboardInterrupt:
            print("\n⏹️ Analyse interrompue par l'utilisateur")
        except Exception as e:
            print(f"\n❌ Erreur: {e}")
    
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")

if __name__ == "__main__":
    main()
