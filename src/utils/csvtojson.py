
import csv
import json
import os
from pathlib import Path


def csv_to_json(csv_path, json_path=None):
    data = []
    with open(csv_path, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    if not json_path:
        json_path = str(Path(csv_path).with_suffix('.json'))
    with open(json_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=2)
    print(f"JSON saved to {json_path}")



RELATIVE_CSV_PATH = os.path.join("..", "..", "data", "processed", "fleet_data_2800_with_country.csv")
CSV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), RELATIVE_CSV_PATH))
JSON_PATH = None  # ou un chemin absolu/relatif pour le JSON

if __name__ == "__main__":
    csv_to_json(CSV_PATH, JSON_PATH)
