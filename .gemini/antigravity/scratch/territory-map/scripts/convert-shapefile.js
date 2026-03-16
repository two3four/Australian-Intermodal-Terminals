const shapefile = require('shapefile');
const fs = require('fs');
const path = require('path');
const AdmZip = require('adm-zip');
const os = require('os');

const zipPath = path.join(__dirname, '..', 'data', 'counties_with_states.zip');
const outputPath = path.join(__dirname, '..', 'public', 'counties.geojson');

async function convert() {
  console.log(`Reading zipped shapefile from: ${zipPath}`);
  
  // Extract zip to a temp directory
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'shp-'));
  try {
    const zip = new AdmZip(zipPath);
    zip.extractAllTo(tmpDir, true);
    console.log(`Extracted zip to temp dir: ${tmpDir}`);

    // Find the .shp file inside the extracted directory
    const files = fs.readdirSync(tmpDir);
    const shpFile = files.find(f => f.endsWith('.shp'));
    if (!shpFile) {
      throw new Error('No .shp file found inside the zip archive!');
    }
    
    const shpPath = path.join(tmpDir, shpFile);
    console.log(`Reading shapefile: ${shpPath}`);

    const geojson = { type: "FeatureCollection", features: [] };
    const source = await shapefile.open(shpPath);

    while (true) {
      const result = await source.read();
      if (result.done) break;
      geojson.features.push(result.value);
    }

    console.log(`Successfully read ${geojson.features.length} features.`);

    // Ensure public directory exists
    const publicDir = path.join(__dirname, '..', 'public');
    if (!fs.existsSync(publicDir)) {
      fs.mkdirSync(publicDir, { recursive: true });
    }

    fs.writeFileSync(outputPath, JSON.stringify(geojson));
    console.log(`Successfully saved GeoJSON to: ${outputPath}`);
  } finally {
    // Cleanup temp dir
    fs.rmSync(tmpDir, { recursive: true, force: true });
  }
}

convert();
