# Australian Intermodal Terminals - Project Summary

This document summarizes all the work completed on the Australian Intermodal Terminals mapping application.

## Project Overview
A web-based mapping application built with **Flask (Backend)** and **Leaflet.js (Frontend)** to visualize intermodal terminals across Australia.

## Key Features Implemented

### 1. Basemaps & Visuals
*   **Default Basemap**: Switched to **Carto Light (Gray)** for a clean, professional look.
*   **Layer Switcher**: Includes Carto Light, OSM, Google Hybrid, and Dark Mode.
*   **Status-based Coloring**: Terminals are color-coded by status (Operational, Proposed, etc.).
*   **Total Count Badge**: Real-time count of terminals displayed in the header.

### 2. PDF Data Integration ("New location")
*   **Extracted 56 Locations**: Sourced from `map b (2).pdf` and user requests.
*   **Smart Mapping**: Matched city names to actual terminal coordinates with state-aware filtering (e.g., Goulburn, NSW vs Goulburn Valley, VIC).
*   **Side-by-Side View**: Purple dots ("New location") are offset to the **North-East** of original terminals to prevent overlapping.
*   **Styled Labels**: "New location" labels are **underlined** and colored **purple**.
*   **Recent Updates**: 
    - Added: Caboolture, Somerton, Ipswich, Altona, Port Botany, Port Kembla, Enfield, Dandenong South, Bacchus Marsh, Casino, Gosford, Nowra.
    - Removed: Echuca, Kalgoorlie, Horsham, Bairnsdale, Port Augusta, Ararat, Seymour, Swan Hill, Cootamundra, Moree, Narrabri, Katherine, Bordertown, Tennant Creek, Merredin, Nhill.
    - Fixed: Picton (now NSW), Melbourne (renamed to Dynon), Goulburn (ensured NSW).

### 3. Professional Search & Navigation
*   **Advanced Search Bar**: Glassmorphism design with backdrop blur, SVG icon, and smooth expansion on focus.
*   **Autocomplete**: Search by Name or Terminal ID.
*   **Auto-Zoom**: Clicking a search result zooms the map to level 15 and opens the info popup.

### 4. Technical Architecture
*   **Backend (Flask)**:
    - `/api/terminals`: Serves `terminals.geojson`.
    - `/api/pdf_locations`: Serves `pdf_locations.geojson` (the purple dots).
    - `/api/user_data`: Dynamically processes `.shp` files from the `user_data/` folder.
*   **Data Processing**: `generate_pdf_data.py` script handles the matching, coordinate fallbacks, and offset logic.

## Deployment
*   **Vercel**: Fully configured with `vercel.json` and deployed to [GitHub Repository](https://github.com/two3four/Australian-Intermodal-Terminals).

## Instructions for Resuming
1.  **To add more SHP data**: Place `.shp`, `.dbf`, `.shx` files in the `user_data/` folder.
2.  **To update PDF locations**: Edit the `pdf_terminals` list in `generate_pdf_data.py` and run `python generate_pdf_data.py`.
3.  **Local Run**: Run `python app.py` and open `http://127.0.0.1:5000`.

---
*Last Updated: 2026-04-24*
