import csv
import os

def load_immat_mapping(immat_path):
    mapping = {}
    with open(immat_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            prefix = row['tablescraper-selected-row'].strip('"')
            country = row['datasortkey'].strip('"')
            if prefix:
                mapping[prefix] = country
    return mapping

def find_country(registration, mapping):
    # Try to match the longest prefix first
    registration = registration.strip().upper()
    for length in range(5, 0, -1):
        prefix = registration[:length]
        if prefix in mapping:
            return mapping[prefix]
    return ''

def add_country_to_fleet_data(fleet_path, immat_path, output_path):
    mapping = load_immat_mapping(immat_path)
    with open(fleet_path, encoding='utf-8') as fin, open(output_path, 'w', newline='', encoding='utf-8') as fout:
        reader = csv.DictReader(fin)
        fieldnames = reader.fieldnames + ['country']
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            reg = row.get('registration', '').strip()
            country = find_country(reg, mapping) if reg else ''
            row['country'] = country
            writer.writerow(row)

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    fleet_path = os.path.join(base_dir, 'data', 'processed', 'fleet_data_2800.csv')
    immat_path = os.path.join(base_dir, 'data', 'exports', 'immat.csv')
    output_path = os.path.join(base_dir, 'data', 'processed', 'fleet_data_2800_with_country.csv')
    add_country_to_fleet_data(fleet_path, immat_path, output_path)
