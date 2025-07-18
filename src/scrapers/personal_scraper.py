import csv
import os
import pandas as pd
from googleapiclient.discovery import build

# Vos identifiants API
API_KEY = "AIzaSyBhdixYmhA1dSlQY5m5kazn9dSYdGxx-6I"
SEARCH_ENGINE_ID = "150b558eb72454e0d"

# Rôle à rechercher
role = "operation director"  # À ajuster selon besoin

# Initialiser le client Custom Search API
service = build("customsearch", "v1", developerKey=API_KEY)


# Lire la liste des entreprises depuis le CSV (colonne 'companies_name', ignorer l'en-tête)
# Choix du nombre de requêtes à lancer :
RUN_ALL = True  # True pour toutes, False pour 10 premières

companies = []
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
csv_path = os.path.join(base_dir, 'data', 'raw', 'airlines_name_clean.csv')
with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)  # skip header
    for row in reader:
        if row and row[0].strip():
            companies.append(row[0].strip())

if not RUN_ALL:
    companies = companies[:10]

# Stockage des résultats
results_data = []


for idx, company in enumerate(companies, 1):
    query = f"{role} {company} LinkedIn"
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
