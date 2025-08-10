"""
Módulo para consumir APIs do OpenStreetMap: Nominatim para geocodificação e OSRM para matriz de distâncias.
"""
import requests

NOMINATIM_BASE = "https://nominatim.openstreetmap.org/search"
OSRM_TABLE = "http://router.project-osrm.org/table/v1/driving"
HEADERS = {"User-Agent": "PO-Calculator/1.0 (a230424@dac.unicamp.br)"}

def geocode_address(addr):
    if not addr:
        return None
    params = {"q": addr, "format": "json", "limit": 1}
    try:
        r = requests.get(NOMINATIM_BASE, params=params, headers=HEADERS, timeout=10)
        r.raise_for_status()
        data = r.json()
        if not data:
            return None
        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        name = data[0].get("display_name", addr)
        return lat, lon, name
    except Exception:
        return None

import requests

def build_coord_str(points):
    return ";".join(f"{lon},{lat}" for lat, lon in points)

def get_osrm_matrix(orig_points, dest_points):
    all_points = orig_points + dest_points
    coord_str = build_coord_str(all_points)

    # CORREÇÃO: separação por ponto e vírgula
    sources = ";".join(str(i) for i in range(len(orig_points)))
    destinations = ";".join(str(i) for i in range(len(orig_points), len(all_points)))

    url = f"{OSRM_TABLE}/{coord_str}"
    params = {
        "sources": sources,
        "destinations": destinations,
        "annotations": "distance,duration"
    }

    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json()