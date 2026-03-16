"use client";

import { useEffect, useRef } from "react";
import { MapContainer, TileLayer, Marker, Popup, GeoJSON } from "react-leaflet";
import L from "leaflet";
import * as turf from "@turf/turf";
import { MarkerData } from "@/lib/googleSheets";

// Fix for default marker icons in Next.js + Leaflet
const DefaultIcon = L.icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;

interface MapComponentProps {
  markers: MarkerData[];
  geojson: any;
}

export default function MapComponent({ markers, geojson }: MapComponentProps) {
  const geoJsonLayerRef = useRef<L.GeoJSON>(null);

  // Helper to check if a feature contains any of our markers
  const containsMarker = (feature: any) => {
    if (!feature || !feature.geometry) return false;
    
    // Create points from markers
    const points = turf.featureCollection(
      markers.map(m => turf.point([m.Longitude, m.Latitude]))
    );

    try {
      // Find points within the feature (county polygon)
      const ptsWithin = turf.pointsWithinPolygon(points, feature);
      return ptsWithin.features.length > 0;
    } catch (e) {
      // Sometimes invalid geometries might fail turf checks
      return false;
    }
  };

  const styleFeature = (feature: any) => {
    const hasMarker = containsMarker(feature);
    return {
      fillColor: hasMarker ? "var(--brand-accent)" : "#d1d5db", // Blue if has marker, else gray
      weight: 1,
      opacity: 1,
      color: "white",
      dashArray: "3",
      fillOpacity: hasMarker ? 0.7 : 0.4
    };
  };

  const onEachFeature = (feature: any, layer: L.Layer) => {
    const countyName = feature.properties?.NAME || "Unknown County";
    const stateName = feature.properties?.STATE_NAME || "";
    
    const hasMarker = containsMarker(feature);
    const statusText = hasMarker ? "<strong>Contains Marker(s)</strong>" : "No markers";

    layer.bindTooltip(`
      <div class="text-sm font-sans">
        <b>${countyName} ${stateName ? `, ${stateName}` : ""}</b><br/>
        ${statusText}
      </div>
    `, {
      sticky: true,
      className: "bg-white p-2 rounded shadow border border-gray-200"
    });

    layer.on({
      mouseover: (e) => {
        const target = e.target;
        target.setStyle({
          weight: 2,
          color: "#666",
          dashArray: "",
          fillOpacity: 0.9
        });
        target.bringToFront();
      },
      mouseout: (e) => {
        if (geoJsonLayerRef.current) {
          geoJsonLayerRef.current.resetStyle(e.target);
        }
      }
    });
  };

  // Center US roughly
  const defaultCenter: [number, number] = [39.8283, -98.5795];

  return (
    <div className="h-full w-full z-0 relative">
      <MapContainer 
        center={defaultCenter} 
        zoom={4} 
        className="h-full w-full"
        zoomControl={true}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        {geojson && (
          <GeoJSON 
            data={geojson} 
            style={styleFeature}
            onEachFeature={onEachFeature}
            ref={geoJsonLayerRef}
            // Add a key to force re-render when markers change so styles update
            key={markers.length} 
          />
        )}

        {markers.map((marker, idx) => (
          <Marker 
            key={idx} 
            position={[marker.Latitude, marker.Longitude]}
          >
            <Popup>
              <div className="font-sans">
                <h3 className="font-bold text-[var(--brand-primary)]">{marker.Name}</h3>
                <p>Status: {marker.Status}</p>
                <p className="text-xs text-gray-500">{marker.Latitude.toFixed(4)}, {marker.Longitude.toFixed(4)}</p>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}
