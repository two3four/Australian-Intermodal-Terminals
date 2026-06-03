import json
import difflib

pdf_terminals = [
    "Moorebank", "Newcastle", "Casino", "Grafton", "Coffs Harbour", "Wauchope", "Taree", "Tamworth", "Armidale", "Narrabri", "Moree", "Campbelltown", "Goulburn", "Yass / Canberra", "Cootamundra", "Wagga Wagga", "Albury / Wodonga", "St Marys", "Picton",
    "Melbourne", "Albury / Wodonga", "Wangaratta", "Seymour", "Geelong", "Ballarat", "Ararat", "Horsham", "Nhill", "Little River", "Pakenham", "Beveridge", "Bendigo", "Echuca", "Swan Hill", "Colac", "Warrnambool", "Traralgon", "Mildura", "Bairnsdale", "Shepparton",
    "Adelaide", "Bordertown", "Murray Bridge", "Port Augusta", "Tarcoola",
    "Acacia Ridge", "Helensvale", "Toowoomba", "Cairns", "Landsborough", "Nambour", "Gympie", "Maryborough", "Bundaberg", "Gladstone", "Rockhampton", "Mackay", "Townsville",
    "Kalgoorlie", "Merredin", "Bunbury", "Perth",
    "Tennant Creek", "Katherine", "Darwin"
]

with open('terminals.geojson', 'r') as f:
    data = json.load(f)

existing_names = [f['properties'].get('name', '') for f in data['features']]

matches = []
not_found = []

for name in pdf_terminals:
    # Look for close matches
    close_matches = difflib.get_close_matches(name, existing_names, n=1, cutoff=0.6)
    if close_matches:
        # Find the feature
        for f in data['features']:
            if f['properties'].get('name') == close_matches[0]:
                matches.append({
                    "pdf_name": name,
                    "matched_name": close_matches[0],
                    "geometry": f['geometry'],
                    "exists": True
                })
                break
    else:
        not_found.append(name)

print(json.dumps({"matches": matches, "not_found": not_found}, indent=2))
