# wasp_mining.py — reads local files instead of hitting the server
import json
import pandas as pd

def get_kenya_counties():
    """Read county bounding boxes from the locally saved file."""
    
    with open("KenyaRegions.json", "r") as f:
        data = json.load(f)

    counties = []
    for item in data["iridl:values"]:
        label = item["label"].replace(", Kenya", "").replace("0", "").strip()
        bbox  = item["bbox"]

        parts   = bbox.split(":")
        lon_min = float(parts[1])
        lat_min = float(parts[2])
        lon_max = float(parts[3])
        lat_max = float(parts[4])

        counties.append({
            "county":  label,
            "lat":     round((lat_min + lat_max) / 2, 4),
            "lon":     round((lon_min + lon_max) / 2, 4),
            "lat_min": lat_min,
            "lat_max": lat_max,
            "lon_min": lon_min,
            "lon_max": lon_max,
        })

    return counties

# Test it
counties = get_kenya_counties()
print(f"Found {len(counties)} counties\n")
for c in counties:
    print(f"  {c['county']:<20} lat={c['lat']:>7}  lon={c['lon']:>7}")

# Add to wasp_mining.py
import csv

counties = get_kenya_counties()

# Save to CSV for reuse in all future scripts
with open("kenya_counties.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["county","lat","lon","lat_min","lat_max","lon_min","lon_max"])
    writer.writeheader()
    writer.writerows(counties)

print("Saved kenya_counties.csv")