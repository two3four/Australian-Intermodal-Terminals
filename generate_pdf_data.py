import json

pdf_terminals = [
    "Moorebank", "Newcastle", "Grafton", "Coffs Harbour", "Wauchope", "Taree", "Tamworth", "Armidale", "Campbelltown", "Goulburn, NSW", "Yass / Canberra", "Wagga Wagga", "Albury", "St Marys", "Picton, NSW",
    "Dynon", "Wangaratta", "Geelong", "Ballarat", "Little River", "Pakenham", "Beveridge", "Bendigo", "Colac", "Warrnambool", "Traralgon", "Mildura", "Shepparton",
    "Adelaide", "Murray Bridge", "Tarcoola",
    "Acacia Ridge", "Helensvale", "Toowoomba", "Cairns", "Landsborough", "Nambour", "Gympie", "Maryborough, QLD", "Bundaberg", "Gladstone", "Rockhampton", "Mackay", "Townsville",
    "Bunbury", "Perth",
    "Darwin",
    "Caboolture, QLD", "Somerton, VIC", "Ipswich, QLD", "Altona, VIC", "Port Botany, NSW", "Port Kembla, NSW", "Enfield, NSW", "Dandenong South", "Bacchus Marsh, VIC", "Casino, NSW", "Gosford, NSW", "Nowra, NSW",
    "Bromelton, QLD", "Hornsby, NSW", "Dubbo, NSW"
]

# Fallback coordinates for common Australian locations if no match is found in the specific database
fallback_coords = {
    "Perth": [115.8605, -31.9505],
    "Darwin": [130.8444, -12.4634],
    "Geelong": [144.3617, -38.1499],
    "Bendigo": [144.2802, -36.7570],
    "Newcastle": [151.7789, -32.9283],
    "Grafton": [152.9333, -29.6833],
    "Coffs Harbour": [153.1167, -30.3000],
    "Bundaberg": [152.3500, -24.8500],
    "Albury": [146.9167, -36.0833],
    "Wangaratta": [146.3167, -36.3500],
    "Ballarat": [143.8500, -37.5667],
    "Mildura": [142.1500, -34.1833],
    "Shepparton": [145.4000, -36.3833],
    "Toowoomba": [151.9500, -27.5667],
    "Rockhampton": [150.5000, -23.3833],
    "Townsville": [146.8167, -19.2500],
    "Cairns": [145.7667, -16.9167],
    "Warrnambool": [142.4833, -38.3833],
    "Traralgon": [146.5333, -38.1833],
    "Colac": [143.5833, -38.3333],
    "Murray Bridge": [139.2667, -35.1167],
    "Tarcoola": [134.5667, -30.7000],
    "Bunbury": [115.6333, -33.3333],
    "Armidale": [151.6667, -30.5167],
    "Tamworth": [150.9333, -31.0833],
    "Taree": [152.4667, -31.9000],
    "Wauchope": [152.7333, -31.4500],
    "Pakenham": [145.4833, -38.0667],
    "Campbelltown": [150.8167, -34.0667],
    "St Marys": [150.7667, -33.7667],
    "Picton, NSW": [150.6000, -34.1667],
    "Yass / Canberra": [149.1300, -35.2809], # Canberra coords
    "Goulburn": [149.7167, -34.7500],
    "Wagga Wagga": [147.3667, -35.1167],
    "Gympie": [152.6576, -26.1892],
    "Nambour": [152.9511, -26.6269],
    "Landsborough": [152.9660, -26.8080],
    "Casino, NSW": [153.0489, -28.8642],
    "Caboolture, QLD": [152.9510, -27.0850],
    "Ipswich, QLD": [152.7600, -27.6100],
    "Port Kembla, NSW": [150.9000, -34.4800],
    "Bacchus Marsh, VIC": [144.4300, -37.6700],
    "Gosford, NSW": [151.3400, -33.4200],
    "Nowra, NSW": [150.6000, -34.8800],
    "Bromelton, QLD": [152.8833, -28.0000],
    "Hornsby, NSW": [151.0994, -33.7042],
    "Dubbo, NSW": [148.6011, -32.2569],
    "Maryborough, QLD": [152.7022, -25.5376],
}

with open('terminals.geojson', 'r') as f:
    data = json.load(f)

def get_centroid(geometry):
    if geometry['type'] == 'Point':
        return geometry['coordinates']
    elif geometry['type'] == 'Polygon':
        coords = geometry['coordinates'][0]
        return [sum(p[0] for p in coords) / len(coords), sum(p[1] for p in coords) / len(coords)]
    elif geometry['type'] == 'MultiPolygon':
        coords = geometry['coordinates'][0][0]
        return [sum(p[0] for p in coords) / len(coords), sum(p[1] for p in coords) / len(coords)]
    return [0, 0]

new_features = []

for name in pdf_terminals:
    best_match = None
    
    # Parse name and state
    parts = [p.strip() for p in name.split(',')]
    clean_name = parts[0].split('/')[0].strip().lower()
    target_state = parts[1].upper() if len(parts) > 1 else None
    
    # Try to find a match in the geojson
    for f in data['features']:
        props = f['properties']
        existing_name = props.get('name', '').lower()
        locality = props.get('locality_name', '').lower()
        feature_state = (props.get('state') or '').upper()
        
        # Match name
        name_match = clean_name in existing_name or clean_name in locality
        
        # Match state if specified
        state_match = True
        if target_state:
            state_match = (target_state == feature_state)
            
        if name_match and state_match:
            best_match = f
            break
            
    if best_match:
        centroid = get_centroid(best_match['geometry'])
        # Offset slightly North-East to avoid the ocean for coastal cities
        offset_centroid = [centroid[0] + 0.02, centroid[1] + 0.02]
        new_features.append({
            "type": "Feature",
            "properties": {
                "name": name, # Only name, no "PDF"
                "status": "New",
                "color": "purple"
            },
            "geometry": {
                "type": "Point",
                "coordinates": offset_centroid
            }
        })
    elif name in fallback_coords:
        # Use fallback coordinates
        coords = fallback_coords[name]
        new_features.append({
            "type": "Feature",
            "properties": {
                "name": name,
                "status": "New",
                "color": "purple"
            },
            "geometry": {
                "type": "Point",
                "coordinates": coords
            }
        })

output_geojson = {
    "type": "FeatureCollection",
    "features": new_features
}

with open('pdf_locations.geojson', 'w') as f:
    json.dump(output_geojson, f, indent=2)

print(f"Created pdf_locations.geojson with {len(new_features)} features.")
