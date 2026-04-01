# dims.py
# Loads Kenya county reference data (dimensions) to GCS.
# Run once, or whenever the counties list changes.
#
# Writes to: gs://YOUR_BUCKET/kenya_weather/dim_counties/
#
# Usage:
#   python dims.py

import os
import csv
import dlt

# ── Credentials come from your shell environment ──────────────────────────────
# export GCS_BUCKET_NAME="kenya-climate-risk-monitor-data"
# export GCS_PROJECT_ID="datazoomcamp-490302"
# Auth uses Application Default Credentials (ADC) — same as your Terraform setup.
# Run `gcloud auth application-default login` once if not already done.
# ─────────────────────────────────────────────────────────────────────────────

BUCKET = os.environ["GCS_BUCKET_NAME"]
COUNTIES_FILE = r"C:\dev\kenya-climate-risk-monitor\data\kenya_counties.csv"


@dlt.resource(
    name="dim_counties",
    write_disposition="replace",   # Always write fresh — this is a reference table
    primary_key="county_id",
)
def counties_resource(filepath: str = COUNTIES_FILE):
    """
    Yields one record per county with id, name, lat, lon, and region.
    write_disposition='replace' means each run overwrites the file in GCS —
    safe because this table rarely changes.
    """
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            yield {
                "county_id":   i + 1,
                "county":      row["county"],
                "latitude":    float(row["lat"]),
                "longitude":   float(row["lon"]),
                # Add a region column if your CSV has one, otherwise drop this:
                "region":      row.get("region", None),
            }


@dlt.source(name="kenya_weather_dims")
def dims_source():
    return counties_resource()


def run():
    pipeline = dlt.pipeline(
        pipeline_name="kenya_weather",            # shared name — ties state together
        destination=dlt.destinations.filesystem(
            bucket_url=f"gs://{BUCKET}"
        ),
        dataset_name="kenya_weather",             # top-level folder in your bucket
    )

    print("Loading county dimensions to GCS...")
    info = pipeline.run(dims_source())
    print(info)
    print("\nDone! Counties written to GCS.")


if __name__ == "__main__":
    run()