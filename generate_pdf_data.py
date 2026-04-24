import json

pdf_terminals = [
    "Moorebank", "Newcastle", "Grafton", "Coffs Harbour", "Wauchope", "Taree", "Tamworth", "Armidale", "Narrabri", "Moree", "Campbelltown", "Goulburn", "Yass / Canberra", "Cootamundra", "Wagga Wagga", "Albury", "St Marys", "Picton",
    "Melbourne", "Wangaratta", "Seymour", "Geelong", "Ballarat", "Ararat", "Horsham", "Nhill", "Little River", "Pakenham", "Beveridge", "Bendigo", "Echuca", "Swan Hill", "Colac", "Warrnambool", "Traralgon", "Mildura", "Bairnsdale", "Shepparton",
    "Adelaide", "Bordertown", "Murray Bridge", "Port Augusta", "Tarcoola",
    "Acacia Ridge", "Helensvale", "Toowoomba", "Cairns", "Landsborough", "Nambour", "Gympie", "Maryborough", "Bundaberg", "Gladstone", "Rockhampton", "Mackay", "Townsville",
    "Kalgoorlie", "Merredin", "Bunbury", "Perth",
    "Tennant Creek", "Katherine", "Darwin"
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
    "Kalgoorlie": [121.4667, -30.7500],
    "Warrnambool": [142.4833, -38.3833],
    "Traralgon": [146.5333, -38.1833],
    "Bairnsdale": [147.6167, -37.8167],
    "Swan Hill": [143.5500, -35.3333],
    "Echuca": [144.7500, -36.1333],
    "Colac": [143.5833, -38.3333],
    "Ararat": [142.9333, -37.2833],
    "Horsham": [142.2000, -36.7167],
    "Nhill": [141.6500, -36.3333],
    "Murray Bridge": [139.2667, -35.1167],
    "Port Augusta": [137.7667, -32.5000],
    "Tarcoola": [134.5667, -30.7000],
    "Katherine": [132.2667, -14.4667],
    "Tennant Creek": [134.1833, -19.6500],
    "Merredin": [118.2667, -31.4833],
    "Bunbury": [115.6333, -33.3333],
    "Moree": [149.8500, -29.4667],
    "Narrabri": [149.7833, -30.3333],
    "Armidale": [151.6667, -30.5167],
    "Tamworth": [150.9333, -31.0833],
    "Taree": [152.4667, -31.9000],
    "Wauchope": [152.7333, -31.4500],
    "Seymour": [145.1333, -37.0167],
    "Pakenham": [145.4833, -38.0667],
    "Campbelltown": [150.8167, -34.0667],
    "St Marys": [150.7667, -33.7667],
    "Picton": [150.6000, -34.1667],
    "Yass / Canberra": [149.1300, -35.2809], # Canberra coords
    "Goulburn": [149.7167, -34.7500],
    "Cootamundra": [148.0333, -34.6333],
    "Wagga Wagga": [147.3667, -35.1167],
    "Gympie": [152.6576, -26.1892],
    "Nambour": [152.9511, -26.6269],
    "Landsborough": [152.9660, -26.8080],
    "Casino": [153.0489, -28.8642],
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
    search_name = name.split('/')[0].strip().lower() # Handle "Yass / Canberra" -> "yass"
    
    # Try exact or substring match in locality or name
    for f in data['features']:
        props = f['properties']
        existing_name = props.get('name', '').lower()
        locality = props.get('locality_name', '').lower()
        
        if search_name in existing_name or search_name in locality:
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
