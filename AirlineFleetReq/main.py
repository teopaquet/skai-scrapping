import requests
import time
import json

API_KEY = "TA_CLE"
BASE = "https://airlabs.co/api/v9/fleets"
limit = 50
offset = 0
all_data = []

while True:
    params = {"api_key": API_KEY, "limit": limit, "offset": offset}
    r = requests.get(BASE, params=params)
    data = r.json().get("response", [])
    if not data:
        break
    all_data.extend(data)
    offset += limit
    time.sleep(0.2)  # pause pour éviter d’être bloqué

# Résumé par compagnie/modèle
summary = {}
for a in all_data:
    key = (a["airline_icao"], a["model"])
    summary[key] = summary.get(key, 0) + 1

for (icaocode, model), count in summary.items():
    print(f"{icaocode} – {model} : {count} appareils")
