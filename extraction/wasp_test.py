# wasp_test.py
import requests

# Test different URL patterns to find what works
urls_to_try = [
    "http://kmddl.meteo.go.ke:8081/SOURCES/.KMD/.Kenya_v02/month/.wasp/data.csv",
    "http://kmddl.meteo.go.ke:8081/SOURCES/.KMD/.Kenya_v02/.month/.wasp/data.csv",
    "http://kmddl.meteo.go.ke:8081/SOURCES/.KMD/.Kenya_v02/",
    "http://kmddl.meteo.go.ke:8081/SOURCES/.KMD/",
    "http://kmddl.meteo.go.ke:8081/SOURCES/.KMD/.Kenya_v02/month/.wasp/",
]

for url in urls_to_try:
    try:
        response = requests.get(url, timeout=15)
        print(f"{response.status_code} → {url}")
    except Exception as e:
        print(f"ERROR    → {url} | {e}")


