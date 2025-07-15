# FlightRadar24 Fleet Analyzer 🛩️

Application graphique dédiée à l'analyse des flottes des compagnies aériennes basée sur les données FlightRadar24 en temps réel.

## 🚀 Fonctionnalités

### Interface Graphique Moderne
- **Interface utilisateur intuitive** avec Tkinter
- **Barre de progression en temps réel** pendant l'analyse
- **Deux onglets principaux** : Scraper et Visualiser
- **Affichage des résultats** en temps réel

### Analyse de Flottes
- **Zones prédéfinies** : Monde entier, Europe, Amérique du Nord, Asie, France
- **Durées d'analyse flexibles** : 10, 20, 30 ou 60 minutes
- **Identification automatique** des types d'avions par compagnie
- **Comptage basé sur immatriculations uniques** pour éviter les doublons
- **Statistiques détaillées** par compagnie aérienne

### Sauvegarde et Visualisation
- **Export automatique** en JSON et CSV
- **Graphiques intégrés** avec matplotlib
- **Chargement de données existantes** pour visualisation
- **Rapports détaillés** avec statistiques complètes

## 📦 Installation

### 1. Prérequis

```bash
# Python 3.7+ requis
python --version
```

### 2. Installation des dépendances

```bash
pip install -r requirements.txt
```

### 3. Lancement de l'application

```bash
python main.py
```

ou

```bash
python fleet_gui.py
```

## 🖥️ Utilisation de l'Interface Graphique

### Onglet "Scraper"

1. **Choisir une zone géographique** :
   - Monde entier (analyse globale)
   - Europe (zone européenne)
   - Amérique du Nord
   - Asie
   - France

2. **Sélectionner la durée** :
   - Rapide (10 min) - Aperçu rapide
   - Moyen (20 min) - Analyse équilibrée
   - Long (30 min) - Analyse détaillée
   - Maximum (60 min) - Analyse complète

3. **Lancer l'analyse** :
   - Cliquer sur "🚀 Commencer l'analyse"
   - Suivre la progression en temps réel
   - Voir les résultats s'afficher automatiquement

4. **Sauvegarder les résultats** :
   - Cliquer sur "💾 Sauvegarder les résultats"
   - Choisir l'emplacement et le nom du fichier

### Onglet "Visualiser"

1. **Charger des données** :
   - Cliquer sur "📁 Charger fichier JSON"
   - Sélectionner un fichier d'analyse précédent

2. **Créer des graphiques** :
   - Cliquer sur "📊 Créer graphiques"
   - Visualiser les données sous forme de graphiques

## 📊 Types de Données Collectées

Pour chaque compagnie aérienne détectée :

```
✈️ Air France (AFR)
   Total d'avions observés: 125
   Types d'aéronefs: 8
   • A320: 45 avions
   • A330: 25 avions
   • B777: 20 avions
   • A350: 15 avions
   ...
```

### Structure des données sauvegardées

**Fichier CSV** :
| airline_icao | airline_name | aircraft_type | count | sample_registrations |
|--------------|--------------|---------------|-------|---------------------|
| AFR | Air France | A320 | 45 | F-GKXN, F-GKXO, F-GKXP... |

**Fichier JSON** :
```json
{
  "AFR": {
    "airline_name": "Air France",
    "total_aircraft": 125,
    "aircraft_types": {
      "A320": {
        "count": 45,
        "registrations": ["F-GKXN", "F-GKXO", ...]
      }
    }
  }
}
```

## 🌍 Zones d'Analyse Disponibles

| Zone | Couverture | Recommandation |
|------|------------|---------------|
| **Monde entier** | Globale | Analyse complète (60 min) |
| **Europe** | Europe élargie | Analyse détaillée (30 min) |
| **Amérique du Nord** | USA + Canada | Analyse équilibrée (20 min) |
| **Asie** | Asie orientale | Analyse équilibrée (20 min) |
| **France** | Territoire français | Analyse rapide (10 min) |

## 📈 Graphiques et Visualisations

L'application génère automatiquement :

1. **Top 15 Compagnies par Nombre d'Avions**
   - Graphique horizontal des plus grandes flottes

2. **Diversité des Flottes**
   - Nombre de types d'avions différents par compagnie

3. **Données interactives**
   - Zoom et navigation dans les graphiques
   - Export des graphiques en PNG

## ⚙️ Mode Console (Backup)

Si l'interface graphique n'est pas disponible, l'application bascule automatiquement en mode console :

```bash
🛩️ FlightRadar24 Fleet Analyzer
Lancement de l'interface graphique...
❌ Tkinter non disponible, mode console

📍 Zones disponibles:
1. Europe
2. France  
3. Monde

Choisissez une zone (1-3): 1
```

## 🔧 Structure du Projet

```
FlightRadarScrap/
├── main.py              # Point d'entrée principal
├── fleet_gui.py         # Interface graphique complète
├── requirements.txt     # Dépendances Python
├── README.md           # Documentation
├── config.py           # Configuration (legacy)
├── examples.py         # Exemples (legacy)
└── fleet_analyzer.py   # Analyseur console (legacy)
```

## 🚨 Considérations Importantes

### Respect de FlightRadar24
- **Utilisation responsable** des APIs publiques
- **Intervalles respectueux** entre les requêtes (2 minutes)
- **Pas d'abus** du service gratuit

### Performance et Précision
- **Plus l'analyse est longue, plus elle est précise**
- **Les données dépendent du trafic aérien actuel**
- **Évitez les doublons** grâce aux immatriculations uniques

### Limitations Techniques
- **Dépend de la connectivité internet**
- **Peut être affecté par les restrictions API**
- **Données en temps réel uniquement**

## 🏃‍♂️ Démarrage Rapide

1. **Installation** :
   ```bash
   git clone <repo>
   cd FlightRadarScrap
   pip install -r requirements.txt
   ```

2. **Analyse rapide** :
   ```bash
   python main.py
   ```
   - Choisir "Europe" + "Rapide (10 min)"
   - Attendre les résultats
   - Sauvegarder si souhaité

3. **Visualisation** :
   - Aller dans l'onglet "Visualiser"
   - Charger le fichier JSON généré
   - Créer les graphiques

## 📞 Support

En cas de problème :
1. Vérifier la connectivité internet
2. Contrôler les logs dans la console
3. Essayer une zone plus petite ou une durée plus courte
4. Redémarrer l'application

---

**⚠️ Avertissement** : Cette application utilise les APIs publiques de FlightRadar24. Respectez les conditions d'utilisation et utilisez avec modération.
