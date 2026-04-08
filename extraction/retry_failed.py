# retry_failed.py
# Retries specific county + date combinations that failed.
# Reads failed entries from:
#   1. FAILED_ENTRIES env var (set by Kestra flow input)
#   2. /tmp/kestra-wd/failed_entries.json (written by backfill/daily)
#   3. Falls back to empty list if neither exists
#
# Usage:
#   python retry_failed.py

import json
import os
import dlt
from pipeline_weather_source import fetch_county_weather, load_counties


def build_pipeline() -> dlt.Pipeline:
    return dlt.pipeline(
        pipeline_name="kenya_weather",
        destination="bigquery",
        dataset_name="raw_weather",  # ← consistent dataset name
    )


# Load failed entries from env var, file, or empty list
_failed_env = os.environ.get("FAILED_ENTRIES")
if _failed_env:
    FAILED = json.loads(_failed_env)
    print(f"Loading {len(FAILED)} failed entries from FAILED_ENTRIES env var")
elif os.path.exists("/tmp/kestra-wd/failed_entries.json"):
    with open("/tmp/kestra-wd/failed_entries.json") as f:
        FAILED = json.load(f)
    print(f"Loading {len(FAILED)} failed entries from failed_entries.json")
else:
    FAILED = []
    print("No failed entries found — nothing to retry")


@dlt.resource(
    name="weather_history",
    write_disposition="append",
    primary_key=["date", "county"],
)
def retry_resource():
    counties = load_counties()
    county_lookup = {c["county"]: c for c in counties}

    for entry in FAILED:
        if len(entry) == 3:
            # Historical format: [county, start_date, end_date]
            county_name, start, end = entry
            label = f"{county_name} {start[:4]}"
        elif len(entry) == 2:
            # Daily format: [county, date]
            county_name, start = entry
            end = start  # same day
            label = f"{county_name} {start}"
        else:
            print(f"  ✗ Unrecognised entry format: {entry}")
            continue

        county = county_lookup.get(county_name)
        if not county:
            print(f"  ✗ '{county_name}' not found in counties CSV — check spelling")
            continue

        print(f"  Retrying {label}...", end=" ", flush=True)
        records = fetch_county_weather(county, start, end)

        if records:
            print(f"✓ {len(records)} rows")
            yield from records
        else:
            print("✗ failed again — try later")


def run():
    if not FAILED:
        print("Nothing to retry — exiting cleanly")
        return

    pipeline = build_pipeline()
    print(f"Retrying {len(FAILED)} failed entries...\n")
    info = pipeline.run(retry_resource())
    print(info)
    print("\n✓ Retry complete!")


if __name__ == "__main__":
    run()