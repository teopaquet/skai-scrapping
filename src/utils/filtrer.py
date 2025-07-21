import csv
import re

# Liste des mots à filtrer (insensible à la casse)
FILTER_WORDS = [
    'school',
    'university',
    'army',
    'air force',
    'college',
    'navy',
    'guard',
    'airbus'
]

# Fichier source et destination
INPUT_CSV = '../../data/raw/airlines_name_clean.csv'
OUTPUT_CSV = '../../data/raw/airlines_name_clean_filtered.csv'

# Compile une regex pour tous les mots à filtrer
pattern = re.compile(r'(' + '|'.join(re.escape(word) for word in FILTER_WORDS) + r')', re.IGNORECASE)

def filter_csv(input_path, output_path):
    removed = []
    with open(input_path, 'r', encoding='utf-8', newline='') as infile, \
         open(output_path, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        header = next(reader)
        writer.writerow(header)
        for row in reader:
            company = row[0]
            if pattern.search(company):
                removed.append(company)
            else:
                writer.writerow(row)
    print(f"Nombre de lignes supprimées : {len(removed)}")
    if removed:
        print("Détail des compagnies supprimées :")
        for name in removed:
            print(f"- {name}")

if __name__ == '__main__':
    filter_csv(INPUT_CSV, OUTPUT_CSV)
