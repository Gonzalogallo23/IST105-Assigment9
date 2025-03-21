from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

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
            coords = json_data["features"][0]["geometry"]["coordinates"]
            return coords
    return None

@app.route('/get_directions', methods=['GET'])
def get_directions():
    orig = request.args.get('origin')
    dest = request.args.get('destination')
    
    if not orig or not dest:
        return jsonify({"error": "Both origin and destination are required."}), 400

    orig_coords = geocode_address(orig)
    dest_coords = geocode_address(dest)
    
    if not orig_coords or not dest_coords:
        return jsonify({"error": "Unable to geocode one or both addresses."}), 400
    
    body = {"coordinates": [orig_coords, dest_coords]}
    headers = {"Authorization": key, "Content-Type": "application/json"}
    response = requests.post(directions_api, headers=headers, json=body)
    json_data = response.json()
    
    if response.status_code == 200 and 'routes' in json_data:
        return jsonify(json_data)
    return jsonify({"error": "Failed to retrieve route."}), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
