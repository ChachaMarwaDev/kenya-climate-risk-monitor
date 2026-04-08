# weather_source.py
# Shared module — imported by dims.py, backfill.py, and daily.py
# Contains the API fetch logic so it's never duplicated

import csv
import requests
import time

BASE_URL = "https://archive-api.open-meteo.com/v1/archive"

DAILY_VARIABLES = [
    "precipitation_sum",           # rainfall mm
    "temperature_2m_max",          # max temp °C
    "temperature_2m_min",          # min temp °C
    "et0_fao_evapotranspiration",  # evapotranspiration mm
    "wind_speed_10m_max",          # wind speed km/h
]


def load_counties(filepath: str = "/app/data/kenya_counties.csv") -> list[dict]:
    """Load all 47 counties with lat/lon from CSV."""
    with open(filepath, newline="") as f:
        return list(csv.DictReader(f))


def fetch_county_weather(county: dict, start: str, end: str, retries: int = 3) -> list[dict] | None:
    """
    Fetch daily weather for one county over a date range.
    Retries up to 3 times on 429 rate limit, waiting longer each time.

    Args:
        county:  dict with keys 'county', 'lat', 'lon'
        start:   'YYYY-MM-DD'
        end:     'YYYY-MM-DD'
        retries: how many times to retry on 429

    Returns:
        List of daily weather record dicts, or None on failure.
    """
    # params is defined once, outside the retry loop
    params = {
        "latitude":   county["lat"],
        "longitude":  county["lon"],
        "daily":      DAILY_VARIABLES,
        "timezone":   "Africa/Nairobi",
        "start_date": start,
        "end_date":   end,
    }

    for attempt in range(retries):
        try:
            response = requests.get(BASE_URL, params=params, timeout=30)

            if response.status_code == 429:
                wait = 10 * (attempt + 1)   # 10s, then 20s, then 30s
                print(f"  ⏳ Rate limited, waiting {wait}s (attempt {attempt + 1}/{retries})...")
                time.sleep(wait)
                continue                     # go back to top of loop and retry

            if response.status_code != 200:
                print(f"  ✗ HTTP {response.status_code} for {county['county']}")
                return None

            data = response.json()
            daily = data["daily"]

            records = []
            for i, date in enumerate(daily["time"]):
                max_t = daily["temperature_2m_max"][i]
                min_t = daily["temperature_2m_min"][i]

                records.append({
                    "date":                  date,
                    "county":                county["county"],
                    "latitude":              float(county["lat"]),
                    "longitude":             float(county["lon"]),
                    "rainfall_mm":           daily["precipitation_sum"][i],
                    "temp_max_c":            max_t,
                    "temp_min_c":            min_t,
                    "temp_avg_c":            round((max_t + min_t) / 2, 2)
                                             if (max_t is not None and min_t is not None)
                                             else None,
                    "evapotranspiration_mm": daily["et0_fao_evapotranspiration"][i],
                    "wind_speed_kmh":        daily["wind_speed_10m_max"][i],
                    "data_source":           "open-meteo-archive",
                })

            return records   # success — exit the retry loop

        except requests.exceptions.Timeout:
            print(f"  ✗ Timeout for {county['county']}")
            return None
        except Exception as e:
            print(f"  ✗ Error for {county['county']}: {e}")
            return None

    # only reached if all retries were 429s
    print(f"  ✗ Failed after {retries} retries for {county['county']}")
    return None


def fetch_all_counties(start: str, end: str, delay: float = 2.0) -> list[dict]:
    """
    Fetch weather for all counties over a date range.
    Requests one county at a time with a delay to avoid rate limiting.

    Used by both backfill.py and daily.py.
    """
    counties = load_counties()
    all_records = []

    for i, county in enumerate(counties):
        print(f"  [{i+1}/{len(counties)}] {county['county']}...", end=" ", flush=True)
        records = fetch_county_weather(county, start, end)

        if records:
            all_records.extend(records)
            print(f"✓ {len(records)} rows")
        else:
            print("✗ skipped")

        time.sleep(delay)   # 2 second pause between counties

    return all_records