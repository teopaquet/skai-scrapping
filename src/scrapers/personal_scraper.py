import csv
import os
import pandas as pd
import random
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")


# Rôle à rechercher
role = "operation director"  # À ajuster selon besoin

# Initialiser le client Custom Search API
service = build("customsearch", "v1", developerKey=API_KEY)


# Lire la liste des entreprises depuis le CSV (colonne 'companies_name', ignorer l'en-tête)

# Choix du nombre de requêtes à lancer :
print("Combien de requêtes voulez-vous lancer ?")
print("1: Une seule\n5: Cinq\n10: Dix\n100: Cent\n0: Toutes")
try:
    choix = int(input("Votre choix (1/5/10/0): ").strip())
except Exception:
    choix = 0

companies = []
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
csv_path = os.path.join(base_dir, 'data', 'raw', 'airlines_name_clean_filtered.csv')
with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)  # skip header
    for row in reader:
        if row and row[0].strip():
            companies.append(row[0].strip())

if choix in [1, 5, 10, 100]:
    companies = random.sample(companies, k=choix)
# 0 ou autre = toutes

# Stockage des résultats
results_data = []


for idx, company in enumerate(companies, 1):
    query = f"{company} {role} LinkedIn"
    try:
        res = service.cse().list(q=query, cx=SEARCH_ENGINE_ID, num=3).execute()
        title, link = '', ''
        if 'items' in res:
            for item in res['items']:
                lnk = item.get('link', '')
                if 'linkedin.com/in/' in lnk:
                    title = item.get('title', '')
                    link = lnk
                    break
        # Si aucun résultat LinkedIn trouvé, laisser vide
    except Exception as e:
        print(f"Erreur pour {company}: {e}")
        title, link = '', ''
    results_data.append({
        'Company': company,
        'Role': role,
        'Name': title,
        'LinkedIn': link
    })
    if idx % 10 == 0 or idx == len(companies):
        print(f"Progression: {idx}/{len(companies)} compagnies traitées.")

# Sauvegarder les résultats dans un CSV dans le dossier exports
export_dir = os.path.join(base_dir, 'data', 'exports')
os.makedirs(export_dir, exist_ok=True)
export_path = os.path.join(export_dir, 'results.csv')
df = pd.DataFrame(results_data)
df.to_csv(export_path, index=False, encoding='utf-8')

print(f"Extraction terminée. Résultats dans '{export_path}'")
