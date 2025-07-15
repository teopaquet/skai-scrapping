"""
🛩️ FlightRadar24 Fleet Analyzer - Guide de Démarrage Rapide
===========================================================

Ce script vous guide pour analyser les flottes des compagnies aériennes
"""

import os
import sys
import subprocess

def check_dependencies():
    """Vérifie et installe les dépendances nécessaires"""
    print("🔍 Vérification des dépendances...")
    
    try:
        import requests
        import pandas
        import fake_useragent
        print("✅ Dépendances de base installées")
        return True
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        
        response = input("📦 Installer les dépendances automatiquement? (o/n): ")
        if response.lower() == 'o':
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
                print("✅ Dépendances installées avec succès")
                return True
            except subprocess.CalledProcessError:
                print("❌ Erreur lors de l'installation")
                return False
        return False

def show_menu():
    """Affiche le menu principal"""
    print("\n" + "="*60)
    print("🛩️  ANALYSEUR DE FLOTTES FLIGHTRADAR24")
    print("="*60)
    print()
    print("Que voulez-vous faire ?")
    print()
    print("1. 🚀 Analyse rapide des flottes (5 minutes)")
    print("   → Analyse rapide d'une zone géographique")
    print()
    print("2. 🔍 Analyse complète des flottes (15-30 minutes)")
    print("   → Analyse détaillée avec plus de données")
    print()
    print("3. 📊 Visualiser des données existantes")
    print("   → Créer des graphiques à partir de données sauvegardées")
    print()
    print("4. 📋 Exemples de base du scraper")
    print("   → Tester les fonctionnalités de base")
    print()
    print("5. ❓ Aide et documentation")
    print()
    print("0. 🚪 Quitter")
    print()

def run_quick_analysis():
    """Lance une analyse rapide"""
    print("\n🚀 ANALYSE RAPIDE DES FLOTTES")
    print("-" * 40)
    print("Cette analyse collecte des données pendant 5 minutes")
    print("sur la zone Europe pour identifier les flottes.")
    print()
    
    confirm = input("Continuer? (o/n): ")
    if confirm.lower() == 'o':
        os.system(f'"{sys.executable}" fleet_analyzer.py')
    else:
        print("❌ Analyse annulée")

def run_full_analysis():
    """Lance une analyse complète"""
    print("\n🔍 ANALYSE COMPLÈTE DES FLOTTES")
    print("-" * 40)
    print("Cette analyse collecte des données pendant 15-30 minutes")
    print("pour obtenir une vue plus complète des flottes.")
    print()
    
    confirm = input("Continuer? (o/n): ")
    if confirm.lower() == 'o':
        os.system(f'"{sys.executable}" fleet_analyzer.py')
    else:
        print("❌ Analyse annulée")

def run_visualization():
    """Lance la visualisation"""
    print("\n📊 VISUALISATION DES DONNÉES")
    print("-" * 40)
    print("Crée des graphiques à partir des données d'analyse existantes")
    print()
    
    # Vérifier s'il y a des fichiers de données
    import glob
    json_files = glob.glob("fleet_analysis_*.json")
    csv_files = glob.glob("fleet_analysis_*.csv")
    
    if not json_files and not csv_files:
        print("❌ Aucune donnée d'analyse trouvée")
        print("💡 Lancez d'abord une analyse (option 1 ou 2)")
        return
    
    print(f"📁 Trouvé {len(json_files)} fichiers JSON et {len(csv_files)} fichiers CSV")
    
    confirm = input("Créer des visualisations? (o/n): ")
    if confirm.lower() == 'o':
        os.system(f'"{sys.executable}" fleet_visualizer.py')
    else:
        print("❌ Visualisation annulée")

def run_basic_examples():
    """Lance les exemples de base"""
    print("\n📋 EXEMPLES DE BASE")
    print("-" * 40)
    print("Test des fonctionnalités de base du scraper FlightRadar24")
    print()
    
    confirm = input("Lancer les exemples? (o/n): ")
    if confirm.lower() == 'o':
        os.system(f'"{sys.executable}" main.py')
    else:
        print("❌ Exemples annulés")

def show_help():
    """Affiche l'aide"""
    print("\n❓ AIDE ET DOCUMENTATION")
    print("-" * 40)
    print()
    print("📖 FONCTIONNALITÉS DISPONIBLES:")
    print()
    print("🔍 ANALYSE DES FLOTTES")
    print("   • Collecte automatique de données de vols")
    print("   • Identification des types d'avions par compagnie")
    print("   • Comptage basé sur les immatriculations uniques")
    print("   • Export en CSV et JSON")
    print()
    print("📊 VISUALISATIONS")
    print("   • Graphiques des flottes par compagnie")
    print("   • Distribution des types d'avions")
    print("   • Analyse comparative des constructeurs")
    print("   • Rapports de synthèse")
    print()
    print("⚙️ FICHIERS DU PROJET:")
    print("   • main.py - Scraper principal")
    print("   • fleet_analyzer.py - Analyseur de flottes")
    print("   • fleet_visualizer.py - Créateur de graphiques")
    print("   • config.py - Configuration")
    print("   • examples.py - Exemples avancés")
    print()
    print("📁 DONNÉES GÉNÉRÉES:")
    print("   • fleet_analysis_*.csv - Données tabulaires")
    print("   • fleet_analysis_*.json - Données complètes")
    print("   • fleet_visualizations_*.png - Graphiques")
    print("   • fleet_report_*.txt - Rapports texte")
    print()
    print("⚠️ LIMITATIONS:")
    print("   • Respectez les limites d'usage de FlightRadar24")
    print("   • Les données dépendent du trafic aérien actuel")
    print("   • Plus l'analyse est longue, plus elle est précise")
    print()
    print("🔗 POUR PLUS D'INFORMATIONS:")
    print("   Consultez le fichier README.md")
    print()

def main():
    """Point d'entrée principal"""
    print("🛩️ Initialisation de l'analyseur de flottes FlightRadar24...")
    
    # Vérifier les dépendances
    if not check_dependencies():
        print("❌ Impossible de continuer sans les dépendances")
        return
    
    while True:
        show_menu()
        
        try:
            choice = input("Votre choix (0-5): ").strip()
            
            if choice == "0":
                print("\n👋 Au revoir!")
                break
            elif choice == "1":
                run_quick_analysis()
            elif choice == "2":
                run_full_analysis()
            elif choice == "3":
                run_visualization()
            elif choice == "4":
                run_basic_examples()
            elif choice == "5":
                show_help()
            else:
                print("❌ Choix invalide. Veuillez choisir entre 0 et 5.")
            
            # Pause avant de revenir au menu
            if choice != "0":
                input("\n⏎ Appuyez sur Entrée pour revenir au menu...")
                
        except KeyboardInterrupt:
            print("\n\n⏹️ Programme interrompu par l'utilisateur")
            break
        except Exception as e:
            print(f"\n❌ Erreur inattendue: {e}")
            input("⏎ Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
