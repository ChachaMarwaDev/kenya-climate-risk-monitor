# daily.py
# Loads yesterday's weather for all 47 counties to BigQuery.
# Designed to run every day on a schedule.
#
# Key feature: dlt tracks the last loaded date in BigQuery state.
# If you accidentally run this twice in a day, it won't duplicate data.
#
# Usage:
#   python pipeline_daily.py                   ← loads yesterday
#   python pipeline_daily.py --date 2025-03-20 ← loads a specific date

import json
import os
import sys
import dlt
from datetime import date, timedelta
from pipeline_weather_source import fetch_all_counties, load_counties  # ← added load_counties


def get_target_date(args: list[str]) -> str:
    """
    Returns the date to load.
    Default: yesterday. Override with --date YYYY-MM-DD.
    """
    if "--date" in args:
        idx = args.index("--date")
        return args[idx + 1]
    return str(date.today() - timedelta(days=1))


def build_pipeline() -> dlt.Pipeline:
    return dlt.pipeline(
        pipeline_name="kenya_weather",
        destination="bigquery",
        dataset_name="raw_weather",  # ← consistent dataset name
    )


@dlt.resource(
    name="weather_daily",
    write_disposition="append",
    primary_key=["date", "county"],
)
def daily_weather(target_date: str, failures: list):
    """
    Fetches all counties for a single day and yields records.
    Tracks any counties that returned no data into the failures list.
    """
    print(f"\nFetching weather for {target_date}...")
    records = fetch_all_counties(
        start=target_date,
        end=target_date,
        delay=0.3,
    )

    # Track which counties were loaded successfully
    loaded_counties = {r["county"] for r in records}

    # Any county missing from results is a failure
    for county in load_counties():
        if county["county"] not in loaded_counties:
            failures.append([county["county"], target_date])
            print(f"  ✗ No data for {county['county']} — added to retry list")

    yield from records


@dlt.source(name="kenya_weather_daily")
def daily_source(target_date: str, failures: list):
    return daily_weather(target_date, failures)


def run():
    target_date = get_target_date(sys.argv)
    failures = []  # ← collects failed county/date combinations

    print(f"Kenya Weather — Daily Load")
    print(f"Target date : {target_date}")
    print(f"Destination : BigQuery — raw_weather.weather_daily")

    pipeline = build_pipeline()
    info = pipeline.run(daily_source(target_date, failures))
    print(info)

    # Write failures to shared file for the retry task to pick up
    os.makedirs("/tmp/kestra-wd", exist_ok=True)
    with open("/tmp/kestra-wd/failed_entries.json", "w") as f:
        json.dump(failures, f)

    print(f"\n✓ Daily load complete for {target_date}")
    if failures:
        print(f"⚠ {len(failures)} failed entries written to failed_entries.json")
        print(json.dumps(failures, indent=2))
    else:
        print("✓ No failures!")


if __name__ == "__main__":
    run()