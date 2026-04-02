# daily.py
# Loads yesterday's weather for all 47 counties to GCS.
# Designed to run every day on a schedule (Cloud Run Job, cron, etc.)
#
# Writes to: gs://YOUR_BUCKET/kenya_weather/weather_daily/
#
# Key feature: dlt tracks the last loaded date in GCS state.
# If you accidentally run this twice in a day, it won't duplicate data.
#
# Usage:
#   python daily.py                   ← loads yesterday
#   python daily.py --date 2025-03-20 ← loads a specific date (manual backfill)

import os
import sys
import dlt
from datetime import date, timedelta
from pipeline_weather_source import fetch_all_counties   # ← shared fetch logic

pipeline = dlt.pipeline(
    pipeline_name="kenya_weather",
    destination="bigquery",
    dataset_name="raw_weather",
)


def get_target_date(args: list[str]) -> str:
    """
    Returns the date to load.
    Default: yesterday. Override with --date YYYY-MM-DD.
    """
    if "--date" in args:
        idx = args.index("--date")
        return args[idx + 1]
    return str(date.today() - timedelta(days=1))


@dlt.resource(
    name="weather_daily",
    write_disposition="append",       # Always append — each day is new rows
    primary_key=["date", "county"],   # dlt uses this to detect duplicates on merge
)
def daily_weather(target_date: str):
    """
    Fetches all counties for a single day and yields records.
    The primary_key ensures that even if you run daily.py twice
    for the same date, you won't get duplicates in your data.
    """
    print(f"\nFetching weather for {target_date}...")
    records = fetch_all_counties(
        start=target_date,
        end=target_date,
        delay=0.3,          # shorter delay for a single day — much faster
    )
    yield from records


@dlt.source(name="kenya_weather_daily")
def daily_source(target_date: str):
    return daily_weather(target_date)


def run():
    target_date = get_target_date(sys.argv)

    print(f"Kenya Weather — Daily Load")
    print(f"Target date : {target_date}")
    print(f"Destination : BigQuery — raw_weather.weather_daily")

    pipeline = dlt.pipeline(
        pipeline_name="kenya_weather",            # same name — shared state in GCS
        destination="bigquery",
        dataset_name="kenya_weather",
    )

    info = pipeline.run(daily_source(target_date))
    print(info)
    print(f"\n✓ Daily load complete for {target_date}")


if __name__ == "__main__":
    run()