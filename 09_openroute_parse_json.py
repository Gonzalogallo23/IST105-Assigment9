#!/usr/bin/env python3
import cgi
import requests
import json

print("Content-Type: text/html\n")

# OpenRouteService API Key
directions_api = "https://api.openrouteservice.org/v2/directions/driving-car"
geocode_api = "https://api.openrouteservice.org/geocode/search?"
key = "5b3ce3597851110001cf6248d3b2e69446f14da6897f95686576108e"

def geocode_address(address):
    url = f"{geocode_api}api_key={key}&text={address}"
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        if json_data["features"]:
            return json_data["features"][0]["geometry"]["coordinates"]
    return None

# Leer parámetros del formulario
form = cgi.FieldStorage()
orig = form.getvalue("origin")
dest = form.getvalue("destination")

if not orig or not dest:
    result = {"error": "Both origin and destination are required."}
else:
    orig_coords = geocode_address(orig)
    dest_coords = geocode_address(dest)

    if not orig_coords or not dest_coords:
        result = {"error": "Unable to geocode one or both addresses."}
    else:
        body = {"coordinates": [orig_coords, dest_coords]}
        headers = {"Authorization": key, "Content-Type": "application/json"}
        response = requests.post(directions_api, headers=headers, json=body)
        json_data = response.json()

        if response.status_code == 200 and 'routes' in json_data:
            segment = json_data['routes'][0]['segments'][0]
            result = {
                "duration": segment.get('duration', 'N/A'),
                "distance": segment.get('distance', 'N/A'),
                "steps": [{"instruction": step["instruction"], "distance": step["distance"]}
                          for step in segment.get("steps", [])]
            }
        else:
            result = {"error": "Failed to retrieve route."}

# Guardar el resultado en un archivo JSON
with open("result.json", "w") as f:
    json.dump(result, f)

# Redirigir de vuelta a la página principal
print("<script>window.location.href = 'index.html';</script>")
