import os
import json
from flask import Flask, render_template, jsonify, send_file
import geopandas as gpd

app = Flask(__name__)

USER_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user_data')
TERMINALS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'terminals.geojson')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/terminals')
def get_terminals():
    if os.path.exists(TERMINALS_FILE):
        return send_file(TERMINALS_FILE, mimetype='application/json')
    return jsonify({"error": "Data not found"}), 404

@app.route('/api/user_data')
def get_user_data():
    features = []
    if os.path.exists(USER_DATA_DIR):
        for file in os.listdir(USER_DATA_DIR):
            if file.endswith('.shp'):
                try:
                    shp_path = os.path.join(USER_DATA_DIR, file)
                    gdf = gpd.read_file(shp_path)
                    # Convert to WGS84 for web mapping
                    if gdf.crs and gdf.crs.to_epsg() != 4326:
                        gdf = gdf.to_crs(epsg=4326)
                    # Parse geojson feature collection
                    geojson = json.loads(gdf.to_json())
                    features.extend(geojson.get('features', []))
                except Exception as e:
                    print(f"Error reading {file}: {e}")
    
    return jsonify({
        "type": "FeatureCollection",
        "features": features
    })

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
