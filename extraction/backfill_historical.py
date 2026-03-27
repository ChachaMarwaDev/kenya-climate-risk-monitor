# backfill_historical.py
# Fetches daily weather data for all 47 counties from 2019 to 2025-03-23
# Run once — takes about 10-15 minutes total

import requests
import pandas as pd
import csv
import time
import os
from datetime import datetime

BASE_URL = "https://archive-api.open-meteo.com/v1/archive"
OUTPUT_DIR = "data/historical"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load the counties we just extracted
def load_counties(filepath="data\kenya_counties.csv") -> list:
    with open(filepath, newline="") as f:
        return list(csv.DictReader(f))

def fetch_county_history(county: dict, start: str, end: str) -> pd.DataFrame | None:
    """
    Fetch daily weather for one county over a date range.
    start/end format: 'YYYY-MM-DD'
    """
    params = {
        "latitude":  county["lat"],
        "longitude": county["lon"],
        "daily": [
            "precipitation_sum",       # rainfall mm
            "temperature_2m_max",      # max temp °C
            "temperature_2m_min",      # min temp °C
            "et0_fao_evapotranspiration",  # evapotranspiration mm
            "wind_speed_10m_max",      # wind speed km/h
        ],
        "timezone": "Africa/Nairobi",
        "start_date": start,
        "end_date":   end,
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=30)

        if response.status_code != 200:
            print(f"    ✗ HTTP {response.status_code} for {county['county']}")
            return None

        data = response.json()
        daily = data["daily"]

        records = []
        for i, date in enumerate(daily["time"]):
            records.append({
                "date":                   date,
                "county":                 county["county"],
                "latitude":               float(county["lat"]),
                "longitude":              float(county["lon"]),
                "rainfall_mm":            daily["precipitation_sum"][i],
                "temp_max_c":             daily["temperature_2m_max"][i],
                "temp_min_c":             daily["temperature_2m_min"][i],
                "temp_avg_c":             round(
                                            (daily["temperature_2m_max"][i] +
                                             daily["temperature_2m_min"][i]) / 2, 2
                                          ) if (daily["temperature_2m_max"][i] is not None
                                                and daily["temperature_2m_min"][i] is not None)
                                          else None,
                "evapotranspiration_mm":  daily["et0_fao_evapotranspiration"][i],
                "wind_speed_kmh":         daily["wind_speed_10m_max"][i],
                "data_source":            "open-meteo-archive",
            })

        return pd.DataFrame(records)

    except requests.exceptions.Timeout:
        print(f"    ✗ Timeout for {county['county']}")
        return None
    except Exception as e:
        print(f"    ✗ Error for {county['county']}: {e}")
        return None


def backfill_all_counties():
    counties = load_counties()
    print(f"Loaded {len(counties)} counties\n")

    # Fetch one year at a time to stay within API limits
    years = [
        # ("2019-01-01", "2019-12-31"),
        # ("2020-01-01", "2020-12-31"),
        # ("2021-01-01", "2021-12-31"),
        # ("2022-01-01", "2022-12-31"),
        # ("2023-01-01", "2023-12-31"),
        # ("2024-01-01", "2024-12-31"),
        ("2025-01-01", "2025-03-25"),
    ]

    for start, end in years:
        year = start[:4]
        output_file = f"{OUTPUT_DIR}/kenya_weather_{year}.csv"

        # Skip if already downloaded
        if os.path.exists(output_file):
            print(f"Year {year} already exists — skipping")
            continue

        print(f"\nFetching year {year}...")
        year_data = []

        for i, county in enumerate(counties):
            print(f"  [{i+1}/{len(counties)}] {county['county']}...", end=" ")
            df = fetch_county_history(county, start, end)

            if df is not None:
                year_data.append(df)
                print(f"✓ {len(df)} rows")
            else:
                print("✗ skipped")

            time.sleep(0.5)   # small delay between requests

        if year_data:
            combined = pd.concat(year_data, ignore_index=True)
            combined.to_csv(output_file, index=False)
            print(f"\nSaved {len(combined)} rows → {output_file}")
        else:
            print(f"\nNo data for {year}")

    print("\nBackfill complete!")


if __name__ == "__main__":
    backfill_all_counties()