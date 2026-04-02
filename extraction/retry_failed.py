# retry_failed.py
# Retries specific county + year combinations that failed with 502 errors.
# Appends results to the same weather_history table in GCS.
#
# Usage:
#   python retry_failed.py

import os
import dlt
from pipeline_weather_source import fetch_county_weather, load_counties

pipeline = dlt.pipeline(
    pipeline_name="kenya_weather",
    destination="bigquery",
    dataset_name="raw_weather",
)

# Add any failed county + year combinations here
FAILED = [
    ("Taita-Taveta", "2007-01-01", "2007-12-31"),
    ("Kajiado",      "2008-01-01", "2008-12-31"),
    ("Uasin Gishu",  "2008-01-01", "2008-12-31"),
    ("Bomet",        "2009-01-01", "2009-12-31"),
    ("Wajir",        "2009-01-01", "2009-12-31"),
    ("Nyeri",        "2013-01-01", "2013-12-31"),
    ("Nyeri",        "2017-01-01", "2017-12-31"),
]


@dlt.resource(
    name="weather_history",          # same table name — appends to existing data
    write_disposition="append",
    primary_key=["date", "county"],
)
def retry_resource():
    # Build a lookup so we can find county lat/lon by name
    counties = load_counties()
    county_lookup = {c["county"]: c for c in counties}

    for county_name, start, end in FAILED:
        county = county_lookup.get(county_name)

        if not county:
            print(f"  ✗ '{county_name}' not found in counties CSV — check spelling")
            continue

        print(f"  Retrying {county_name} {start[:4]}...", end=" ", flush=True)
        records = fetch_county_weather(county, start, end)

        if records:
            print(f"✓ {len(records)} rows")
            yield from records
        else:
            print("✗ failed again — try later")


def run():
    pipeline = dlt.pipeline(
        pipeline_name="kenya_weather",
        destination="bigquery",
        dataset_name="kenya_weather",
    )

    print("Retrying failed counties...\n")
    info = pipeline.run(retry_resource())
    print(info)
    print("\n✓ Retry complete!")


if __name__ == "__main__":
    run()