# Kenya Climate Risk Monitor
### Drought & Flood Early Warning System

![GCP](https://img.shields.io/badge/Cloud-Google_Cloud_Platform-blue)
![BigQuery](https://img.shields.io/badge/Data_Warehouse-BigQuery-blue)
![GCS](https://img.shields.io/badge/Data_Lake-Google_Cloud_Storage-blue)
![Python](https://img.shields.io/badge/Language-Python_3.11-yellow)
![Looker](https://img.shields.io/badge/Visualization-Looker_Studio-green)
![Status](https://img.shields.io/badge/Status-In_Progress-orange)

## Problem Statement
Kenya's 47 counties face recurring drought and flood crises that affect
millions of people, particularly in ASAL (Arid and Semi-Arid) regions.
Early warning systems can give communities and authorities days or weeks
of advance notice to prepare. This project builds an automated data
pipeline that ingests daily weather data for all 47 Kenyan counties,
detects anomalies against 40+ year historical baselines, and surfaces
risk scores on an interactive dashboard.

## Project Architecture
![Architecture](docs/kenya_weather_gcp_architecture.svg)


## Tech Stack
<!-- fill this in as you add tools -->
### Cloud Infrastructure
![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![BigQuery](https://img.shields.io/badge/BigQuery-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![Cloud Storage](https://img.shields.io/badge/Cloud_Storage-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)

### Data Engineering
![dlt](https://img.shields.io/badge/dlt-FF6B6B?style=for-the-badge&logo=data&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white)
![Kestra](https://img.shields.io/badge/Kestra-4A154B?style=for-the-badge&logo=kestra&logoColor=white)

### Infrastructure as Code
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)

### Containerization
![Docker][https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white]

### Programming Languages
![Python|66][https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white]
![SQL|44][https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=postgresql&logoColor=white]


### Key Libraries
- `dlt` - Data extraction and loading
- `pandas` - Data manipulation
- `pyarrow` - Efficient data processing
- `google-cloud-bigquery` - BigQuery client
- `google-cloud-storage` - Cloud Storage client
- `pydantic` - Data validation
- `tenacity` - Retry logic
- `sqlparse` - SQL parsing

## Project Structure
```text
kenya-climate-risk-monitor/
│
├── .gitignore
├── LICENSE
├── README.md
├── docker-compose.yaml
├── dockerfile
│
├── data/
│   ├── historical/
│   │   └── kenya_weather_2019.csv
│   ├── KenyaRegions.json
│   └── kenya_counties.csv
│
├── docs/
│   ├── dbt_lineage.jpg
│   ├── entity_relationship_diagram.svg
│   ├── kenya_weather_gcp_architecture.svg
│   ├── kestra_dashboard.jpg
│   └── methodology.md
│
├── extraction/
│   ├── .dlt/
│   │   └── config.toml
│   ├── .gitignore
│   ├── backfill_historical.py
│   ├── pipeline_backfill.py
│   ├── pipeline_daily.py
│   ├── pipeline_dims.py
│   ├── pipeline_weather_source.py
│   ├── retry_failed.py
│   ├── wasp_mining.py
│   └── wasp_test.py
│
├── dbt/
│   ├── .gitignore
│   ├── dbt_env/              # Python virtual environment (ignored)
│   ├── kenya_climate_risk_monitor/
│   │   ├── .gitignore
│   │   ├── README.md
│   │   ├── dbt_project.yml
│   │   ├── analyses/
│   │   │   └── .gitkeep
│   │   ├── macros/
│   │   │   └── .gitkeep
│   │   ├── models/
│   │   │   ├── mart/
│   │   │   │   ├── fct_climate_risk.sql
│   │   │   │   └── schema.yml
│   │   │   └── staging/
│   │   │       ├── sources.yml
│   │   │       ├── stg_counties.sql
│   │   │       └── stg_daily_weather.sql
│   │   ├── seeds/
│   │   │   ├── dim_agro_zones.csv
│   │   │   ├── dim_thresholds.csv
│   │   │   ├── kenya_counties.csv
│   │   │   └── rainy_seasons.csv
│   │   ├── snapshots/
│   │   │   └── .gitkeep
│   │   ├── tests/
│   │   │   └── .gitkeep
│   │   └── logs/
│   │       └── query_log.sql
│   └── logs/
│       └── query_log.sql
│
├── terraform/
│   ├── .gitignore
│   ├── .terraform.lock.hcl
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── bigquery.tf
│   ├── storage.tf
│   ├── iam.tf
│   ├── terraform.tfstate
│   └── terraform.tfstate.backup
│
└── logs/
    └── query_log.sql
```

## Data Sources
| Source | Type | Coverage | Used for |
|--------|------|---------|---------|
| Open-Meteo Archive API | Daily weather | 1981–present | Historical baseline |
| Open-Meteo Forecast API | Daily weather | Real-time | Daily ingestion |
| KMD ENACTS Portal | Rainfall | 1981–2022 | Validation |

## Pipeline Phases
- [x] Phase 1: Data gathering & reference tables
- [x] Phase 2: BigQuery schema & historical load
- [x] Phase 3: Automation & orchestration
- [x] Phase 4: Dashboard

## Dashboard
<!-- add screenshots here when ready -->
### dbt lineage
![dbt lineage](docs/dbt_lineage.jpg)

![kestra dashboard](docs/kestra_dashboard.jpg)

## Steps to Reproduce
<!-- fill in as you build -->

## Contact
**Chacha Marwa** — Junior Data Engineer
- GitHub: [ChachaMarwaDev](https://github.com/ChachaMarwaDev)
- LinkedIn: [chacha-marwa-dev](https://linkedin.com/in/chacha-marwa-dev-355394257)
- X: [@chachamarwadev](https://x.com/chachamarwadev)
- Portfolio: [chachamarwadev.com](https://sites.google.com/view/chachamarwadev)
