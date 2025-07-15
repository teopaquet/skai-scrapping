"""
Script de visualisation des données de flotte
Nécessite matplotlib et seaborn pour les graphiques
"""

import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import glob

def install_visualization_packages():
    """
    Installe les packages nécessaires pour la visualisation
    """
    try:
        import matplotlib
        import seaborn
        print("✅ Packages de visualisation déjà installés")
        return True
    except ImportError:
        print("📦 Installation des packages de visualisation...")
        import subprocess
        import sys
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib", "seaborn"])
            print("✅ Packages installés avec succès")
            return True
        except subprocess.CalledProcessError:
            print("❌ Erreur lors de l'installation des packages")
            return False

def load_fleet_data():
    """
    Charge les données de flotte depuis les fichiers JSON ou CSV
    """
    print("🔍 Recherche des fichiers de données de flotte...")
    
    # Chercher les fichiers JSON de flotte
    json_files = glob.glob("fleet_analysis_*.json")
    csv_files = glob.glob("fleet_analysis_*.csv")
    
    if not json_files and not csv_files:
        print("❌ Aucun fichier de données de flotte trouvé")
        print("💡 Lancez d'abord 'python fleet_analyzer.py' pour générer des données")
        return None
    
    if json_files:
        # Utiliser le fichier JSON le plus récent
        latest_json = max(json_files, key=os.path.getctime)
        print(f"📁 Chargement du fichier JSON: {latest_json}")
        
        with open(latest_json, 'r', encoding='utf-8') as f:
            fleet_data = json.load(f)
        return fleet_data, 'json', latest_json
    
    elif csv_files:
        # Utiliser le fichier CSV le plus récent
        latest_csv = max(csv_files, key=os.path.getctime)
        print(f"📁 Chargement du fichier CSV: {latest_csv}")
        
        df = pd.read_csv(latest_csv)
        return df, 'csv', latest_csv
    
    return None

def create_fleet_visualizations(data, data_type, filename):
    """
    Crée des visualisations des données de flotte
    """
    if not install_visualization_packages():
        print("❌ Impossible de créer les visualisations sans les packages requis")
        return
    
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # Configuration du style
    plt.style.use('default')
    sns.set_palette("husl")
    
    fig = plt.figure(figsize=(20, 16))
    
    if data_type == 'json':
        create_json_visualizations(data, fig)
    else:
        create_csv_visualizations(data, fig)
    
    # Sauvegarder les graphiques
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"fleet_visualizations_{timestamp}.png"
    
    plt.tight_layout()
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"📊 Graphiques sauvegardés: {output_filename}")
    
    # Afficher les graphiques
    plt.show()

def create_json_visualizations(fleet_data, fig):
    """
    Crée des visualisations à partir des données JSON
    """
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # Préparer les données pour visualisation
    airlines_data = []
    aircraft_data = []
    
    for airline_icao, data in fleet_data.items():
        airlines_data.append({
            'airline': data['airline_name'],
            'icao': airline_icao,
            'total_aircraft': data['total_unique_registrations'],
            'aircraft_types': len(data['aircraft_types'])
        })
        
        for aircraft_type, type_data in data['aircraft_types'].items():
            aircraft_data.append({
                'airline': data['airline_name'],
                'aircraft_type': aircraft_type,
                'count': type_data.get('unique_count', 0)
            })
    
    airlines_df = pd.DataFrame(airlines_data)
    aircraft_df = pd.DataFrame(aircraft_data)
    
    # Graphique 1: Top 15 compagnies par nombre d'avions
    ax1 = plt.subplot(2, 3, 1)
    top_airlines = airlines_df.nlargest(15, 'total_aircraft')
    sns.barplot(data=top_airlines, y='airline', x='total_aircraft', ax=ax1)
    ax1.set_title('Top 15 Compagnies par Nombre d\'Avions', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Nombre d\'avions observés')
    
    # Graphique 2: Distribution des tailles de flottes
    ax2 = plt.subplot(2, 3, 2)
    airlines_df['total_aircraft'].hist(bins=20, ax=ax2, alpha=0.7)
    ax2.set_title('Distribution des Tailles de Flottes', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Nombre d\'avions')
    ax2.set_ylabel('Nombre de compagnies')
    
    # Graphique 3: Top 20 types d'avions les plus populaires
    ax3 = plt.subplot(2, 3, 3)
    aircraft_summary = aircraft_df.groupby('aircraft_type')['count'].sum().sort_values(ascending=False).head(20)
    aircraft_summary.plot(kind='bar', ax=ax3)
    ax3.set_title('Top 20 Types d\'Avions', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Type d\'avion')
    ax3.set_ylabel('Nombre total observé')
    ax3.tick_params(axis='x', rotation=45)
    
    # Graphique 4: Diversité des flottes (nombre de types par compagnie)
    ax4 = plt.subplot(2, 3, 4)
    top_diverse = airlines_df.nlargest(15, 'aircraft_types')
    sns.barplot(data=top_diverse, y='airline', x='aircraft_types', ax=ax4)
    ax4.set_title('Top 15 Compagnies par Diversité de Flotte', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Nombre de types d\'avions')
    
    # Graphique 5: Corrélation taille vs diversité
    ax5 = plt.subplot(2, 3, 5)
    sns.scatterplot(data=airlines_df, x='total_aircraft', y='aircraft_types', ax=ax5)
    ax5.set_title('Corrélation Taille vs Diversité', fontsize=14, fontweight='bold')
    ax5.set_xlabel('Nombre total d\'avions')
    ax5.set_ylabel('Nombre de types')
    
    # Graphique 6: Répartition des constructeurs (approximatif basé sur les codes)
    ax6 = plt.subplot(2, 3, 6)
    manufacturers = []
    for aircraft_type in aircraft_df['aircraft_type']:
        if aircraft_type.startswith(('A3', 'A2', 'A1')):
            manufacturers.append('Airbus')
        elif aircraft_type.startswith(('B7', 'B6', 'B5', 'B4', 'B3')):
            manufacturers.append('Boeing')
        elif aircraft_type.startswith('E'):
            manufacturers.append('Embraer')
        elif aircraft_type.startswith('CRJ'):
            manufacturers.append('Bombardier')
        elif aircraft_type.startswith('AT'):
            manufacturers.append('ATR')
        else:
            manufacturers.append('Autres')
    
    manufacturer_counts = pd.Series(manufacturers).value_counts()
    ax6.pie(manufacturer_counts.values, labels=manufacturer_counts.index, autopct='%1.1f%%')
    ax6.set_title('Répartition par Constructeur (approximatif)', fontsize=14, fontweight='bold')

def create_csv_visualizations(df, fig):
    """
    Crée des visualisations à partir des données CSV
    """
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # Graphique 1: Top 15 compagnies par nombre d'avions uniques
    ax1 = plt.subplot(2, 3, 1)
    airline_totals = df.groupby('airline_name')['unique_registrations'].sum().sort_values(ascending=False).head(15)
    airline_totals.plot(kind='bar', ax=ax1)
    ax1.set_title('Top 15 Compagnies par Nombre d\'Avions', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Compagnie')
    ax1.set_ylabel('Nombre d\'avions')
    ax1.tick_params(axis='x', rotation=45)
    
    # Graphique 2: Types d'avions les plus populaires
    ax2 = plt.subplot(2, 3, 2)
    aircraft_totals = df.groupby('aircraft_type')['unique_registrations'].sum().sort_values(ascending=False).head(20)
    aircraft_totals.plot(kind='bar', ax=ax2)
    ax2.set_title('Top 20 Types d\'Avions', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Type d\'avion')
    ax2.set_ylabel('Nombre total')
    ax2.tick_params(axis='x', rotation=45)
    
    # Graphique 3: Distribution des observations
    ax3 = plt.subplot(2, 3, 3)
    df['observed_count'].hist(bins=30, ax=ax3, alpha=0.7)
    ax3.set_title('Distribution des Observations', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Nombre d\'observations')
    ax3.set_ylabel('Fréquence')
    
    # Graphique 4: Diversité par compagnie
    ax4 = plt.subplot(2, 3, 4)
    diversity = df.groupby('airline_name')['aircraft_type'].nunique().sort_values(ascending=False).head(15)
    diversity.plot(kind='bar', ax=ax4)
    ax4.set_title('Diversité de Flotte par Compagnie', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Compagnie')
    ax4.set_ylabel('Nombre de types')
    ax4.tick_params(axis='x', rotation=45)
    
    # Graphique 5: Corrélation observations vs unique
    ax5 = plt.subplot(2, 3, 5)
    sns.scatterplot(data=df, x='observed_count', y='unique_registrations', ax=ax5)
    ax5.set_title('Observations vs Immatriculations Uniques', fontsize=14, fontweight='bold')
    ax5.set_xlabel('Nombre d\'observations')
    ax5.set_ylabel('Immatriculations uniques')
    
    # Graphique 6: Top compagnies par observations totales
    ax6 = plt.subplot(2, 3, 6)
    obs_totals = df.groupby('airline_name')['observed_count'].sum().sort_values(ascending=False).head(10)
    obs_totals.plot(kind='pie', ax=ax6, autopct='%1.1f%%')
    ax6.set_title('Top 10 Compagnies par Observations', fontsize=14, fontweight='bold')

def generate_summary_report(data, data_type, filename):
    """
    Génère un rapport de synthèse
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"fleet_summary_report_{timestamp}.txt"
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write("RAPPORT DE SYNTHÈSE - ANALYSE DE FLOTTE\n")
        f.write("="*50 + "\n\n")
        f.write(f"Fichier source: {filename}\n")
        f.write(f"Date de génération: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
        
        if data_type == 'json':
            write_json_summary(data, f)
        else:
            write_csv_summary(data, f)
    
    print(f"📄 Rapport de synthèse généré: {report_filename}")

def write_json_summary(fleet_data, f):
    """Écrit le résumé pour les données JSON"""
    total_airlines = len(fleet_data)
    total_aircraft = sum(data['total_unique_registrations'] for data in fleet_data.values())
    all_types = set()
    for data in fleet_data.values():
        all_types.update(data['aircraft_types'].keys())
    
    f.write("STATISTIQUES GÉNÉRALES\n")
    f.write("-"*30 + "\n")
    f.write(f"Compagnies analysées: {total_airlines}\n")
    f.write(f"Total d'avions observés: {total_aircraft}\n")
    f.write(f"Types d'aéronefs différents: {len(all_types)}\n")
    f.write(f"Moyenne d'avions par compagnie: {total_aircraft/total_airlines:.1f}\n\n")
    
    # Top 10 compagnies
    f.write("TOP 10 COMPAGNIES (par taille de flotte)\n")
    f.write("-"*40 + "\n")
    sorted_airlines = sorted(fleet_data.items(), 
                           key=lambda x: x[1]['total_unique_registrations'], 
                           reverse=True)
    
    for i, (airline_icao, data) in enumerate(sorted_airlines[:10], 1):
        f.write(f"{i:2d}. {data['airline_name']:25} {data['total_unique_registrations']:3d} avions\n")

def write_csv_summary(df, f):
    """Écrit le résumé pour les données CSV"""
    total_airlines = df['airline_name'].nunique()
    total_unique = df['unique_registrations'].sum()
    total_types = df['aircraft_type'].nunique()
    
    f.write("STATISTIQUES GÉNÉRALES\n")
    f.write("-"*30 + "\n")
    f.write(f"Compagnies analysées: {total_airlines}\n")
    f.write(f"Total d'avions observés: {total_unique}\n")
    f.write(f"Types d'aéronefs différents: {total_types}\n")
    f.write(f"Moyenne d'avions par compagnie: {total_unique/total_airlines:.1f}\n\n")
    
    # Top 10 compagnies
    f.write("TOP 10 COMPAGNIES (par taille de flotte)\n")
    f.write("-"*40 + "\n")
    top_airlines = df.groupby('airline_name')['unique_registrations'].sum().sort_values(ascending=False).head(10)
    
    for i, (airline, count) in enumerate(top_airlines.items(), 1):
        f.write(f"{i:2d}. {airline:25} {count:3d} avions\n")

def main():
    """
    Point d'entrée principal pour la visualisation
    """
    print("📊 Visualisateur de Données de Flotte")
    print("="*40)
    
    # Charger les données
    result = load_fleet_data()
    if not result:
        return
    
    data, data_type, filename = result
    print(f"✅ Données chargées: {data_type.upper()}")
    
    # Menu d'options
    print("\nOptions disponibles:")
    print("1. Créer des visualisations graphiques")
    print("2. Générer un rapport de synthèse")
    print("3. Les deux")
    
    try:
        choice = input("\nVotre choix (1-3): ").strip()
        
        if choice in ['1', '3']:
            print("\n📊 Création des visualisations...")
            create_fleet_visualizations(data, data_type, filename)
        
        if choice in ['2', '3']:
            print("\n📄 Génération du rapport de synthèse...")
            generate_summary_report(data, data_type, filename)
        
        print("\n✅ Visualisation terminée avec succès!")
        
    except KeyboardInterrupt:
        print("\n⏹️  Visualisation interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors de la visualisation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
