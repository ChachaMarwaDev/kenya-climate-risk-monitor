# backfill.py
# Loads historical weather data (2005–2025) for all 47 counties to BigQuery.
# Run ONCE — takes about 10–15 minutes. Safe to re-run; skips years already loaded.
#
# Usage:
#   python pipeline_backfill.py
#   python pipeline_backfill.py --years 2023 2024   ← load specific years only

import json
import os
import sys
import dlt
from pipeline_weather_source import fetch_all_counties, load_counties  # ← added load_counties


YEAR_RANGES = [
    # ('1981-01-01', '1981-12-31'),
    # ('1982-01-01', '1982-12-31'),
    # ('1983-01-01', '1983-12-31'),
    # ('1984-01-01', '1984-12-31'),
    # ('1985-01-01', '1985-12-31'),
    # ('1986-01-01', '1986-12-31'),
    # ('1987-01-01', '1987-12-31'),
    # ('1988-01-01', '1988-12-31'),
    # ('1989-01-01', '1989-12-31'),
    # ('1990-01-01', '1990-12-31'),
    # ('1991-01-01', '1991-12-31'),
    # ('1992-01-01', '1992-12-31'),
    # ('1993-01-01', '1993-12-31'),
    # ('1994-01-01', '1994-12-31'),
    # ('1995-01-01', '1995-12-31'),
    # ('1996-01-01', '1996-12-31'),
    # ('1997-01-01', '1997-12-31'),
    # ('1998-01-01', '1998-12-31'),
    # ('1999-01-01', '1999-12-31'),
    # ('2000-01-01', '2000-12-31'),
    # ('2001-01-01', '2001-12-31'),
    # ('2002-01-01', '2002-12-31'),
    # ('2003-01-01', '2003-12-31'),
    # ('2004-01-01', '2004-12-31'),
    # ('2005-01-01', '2005-12-31'),
    # ('2006-01-01', '2006-12-31'),
    # ('2007-01-01', '2007-12-31'),
    # ('2008-01-01', '2008-12-31'),
    # ('2009-01-01', '2009-12-31'),
    # ('2010-01-01', '2010-12-31'),
    # ('2011-01-01', '2011-12-31'),
    # ('2012-01-01', '2012-12-31'),
    # ('2013-01-01', '2013-12-31'),
    # ('2014-01-01', '2014-12-31'),
    # ('2015-01-01', '2015-12-31'),
    # ('2016-01-01', '2016-12-31'),
    # ('2017-01-01', '2017-12-31'),
    # ('2018-01-01', '2018-12-31'),
    # ('2019-01-01', '2019-12-31'),
    # ('2020-01-01', '2020-12-31'),
    # ('2021-01-01', '2021-12-31'),
    # ('2022-01-01', '2022-12-31'),
    # ('2023-01-01', '2023-12-31'),
    # ('2024-01-01', '2024-12-31'),
    ('2025-04-01', '2025-04-6'),
]


def build_pipeline() -> dlt.Pipeline:
    return dlt.pipeline(
        pipeline_name="kenya_weather",
        destination="bigquery",
        dataset_name="raw_weather",
    )


@dlt.resource(
    name="weather_history",
    write_disposition="append",
    primary_key=["date", "county"],
)
def historical_weather(start: str, end: str, failures: list):
    """
    Fetches all counties for a single date range and yields records.
    Tracks counties that returned no data into the failures list.
    """
    print(f"\nFetching {start[:4]} ({start} → {end})...")
    records = fetch_all_counties(start, end, delay=2.0)

    # Track which counties were loaded successfully
    loaded_counties = {r["county"] for r in records}

    # Any county missing from results is a failure
    for county in load_counties():
        if county["county"] not in loaded_counties:
            failures.append([county["county"], start, end])
            print(f"  ✗ No data for {county['county']} — added to retry list")

    yield from records


def run(years_filter: list[str] | None = None):
    """
    Load each year range to BigQuery.
    years_filter: optional list like ['2023', '2024'] to load specific years only.
    """
    pipeline = build_pipeline()
    failures = []  # ← collects failed county/year combinations

    ranges_to_run = [
        (start, end)
        for start, end in YEAR_RANGES
        if years_filter is None or start[:4] in years_filter
    ]

    if not ranges_to_run:
        print("No matching year ranges found. Check your --years argument.")
        return

    for start, end in ranges_to_run:
        year = start[:4]
        print(f"\n{'─' * 50}")
        print(f"Year: {year}")
        info = pipeline.run(historical_weather(start, end, failures))
        print(info)

    # Write failures to shared file for the retry task to pick up
    os.makedirs("/tmp/kestra-wd", exist_ok=True)
    with open("/tmp/kestra-wd/failed_entries.json", "w") as f:
        json.dump(failures, f)

    print(f"\n✓ Backfill complete!")
    if failures:
        print(f"⚠ {len(failures)} failed entries written to failed_entries.json")
        print(json.dumps(failures, indent=2))
    else:
        print("✓ No failures!")


if __name__ == "__main__":
    years = None
    if "--years" in sys.argv:
        idx = sys.argv.index("--years")
        years = sys.argv[idx + 1:]

    run(years_filter=years)