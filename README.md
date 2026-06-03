# Local Intermodal Terminals Map

This project provides a local host environment for the Australian Intermodal Terminals Map, including the original data, and allows you to add and visualize your own custom Shapefiles directly from QGIS.

## Project Structure
- `app.py`: The Flask web server.
- `terminals.geojson`: The original terminal data downloaded from the infrastructure.gov.au portal.
- `user_data/`: A directory where you can drop any `.shp` files you edit in QGIS.
- `templates/index.html`: The web map interface.

## How to Run

1. Open your terminal or command prompt.
2. Navigate to the app directory:
   ```cmd
   cd "C:\Users\Siddique Akbar\.gemini\antigravity\scratch\local_map_app"
   ```
3. Run the Python app:
   ```cmd
   python app.py
   ```
4. Open your web browser and go to `http://127.0.0.1:5000`

## Adding Custom Data from QGIS
1. Create or edit a Shapefile (`.shp`) in QGIS.
2. Save or copy all the Shapefile components (`.shp`, `.shx`, `.dbf`, `.prj`) into the `user_data/` directory.
3. Refresh the web page (`http://127.0.0.1:5000`). The map will automatically parse your Shapefile and display it on the map in a distinct cyan color.

Enjoy your local spatial environment!
