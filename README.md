# Kenya Climate Risk Monitor
### Drought & Flood Early Warning System

![GCP](https://img.shields.io/badge/Cloud-Google_Cloud_Platform-blue)
![BigQuery](https://img.shields.io/badge/Data_Warehouse-BigQuery-blue)
![GCS](https://img.shields.io/badge/Data_Lake-Google_Cloud_Storage-blue)
![Python](https://img.shields.io/badge/Language-Python_3.11-yellow)
![Looker](https://img.shields.io/badge/Visualization-Looker_Studio-green)
![Status](https://img.shields.io/badge/Status-Complete-green)

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
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

### Programming Languages
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=postgresql&logoColor=white)

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
### Overview of the dashboard
![An overview of the findings from my climate risk monitor.](docs/overview.jpg)
For the full dashboard here is the ![link](https://lookerstudio.google.com/reporting/a2678be8-184f-4898-b8a5-d68bd25627b5)


### dbt Lineage Dashboard
![dbt transformation lineage diagram showing data flow from source tables (daily_weather, kenya_counties, dim_counties, dim_agro_zones, dim_thresholds, rainy_seasons) through staging models (stg_daily_weather, stg_counties) to the final fact table (fct_climate_risk) in BigQuery. Nodes are color-coded by type: teal for source files, green for seed data, white for staging and mart models. Arrows indicate dependencies between models, illustrating the complete data transformation pipeline.](docs/dbt_lineage.jpg)

### Kestra Orchestration Dashboard
![Kestra workflow orchestration dashboard displaying an automated data pipeline with multiple scheduled tasks and their execution status. The interface shows job definitions, run history, logs, and performance metrics for the Kenya climate risk monitoring system, with tabs for problems, output, debug console, ports, lineage, query results, and terminal across the top of the screen.](docs/kestra_dashboard.jpg)


## Steps to Reproduce
<!-- fill in as you build -->
### Prerequisites
 
Make sure you have the following installed before you begin:
 
| Tool | Purpose |
|---|---|
| [Python 3.13.5](https://www.python.org/downloads/) | Running dlt pipelines |
| [Docker Desktop](https://www.docker.com/products/docker-desktop/) | Running Kestra orchestration |
| [Terraform](https://developer.hashicorp.com/terraform/install) | Provisioning GCP infrastructure |
| [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) (`gcloud`) | Authentication and GCP access |
| [dlt](https://dlthub.com/docs/intro) | Data ingestion pipeline |
| [dbt](https://docs.getdbt.com/docs/core/installation-overview) | Data transformation layer |
 
---
 
### 1. Clone the repository
 
```bash
git clone https://github.com/ChachaMarwaDev/kenya-climate-risk-monitor.git
cd kenya-climate-risk-monitor
```
 
---
 
### 2. Set up GCP
 
You will need a GCP project with billing enabled.
 
#### 2a. Authenticate with Application Default Credentials
 
```bash
gcloud auth application-default login
gcloud config set project YOUR_GCP_PROJECT_ID
```
 
#### 2b. Enable required APIs
 
```bash
gcloud services enable bigquery.googleapis.com
gcloud services enable storage.googleapis.com
```
 
#### 2c. Provision infrastructure with Terraform
 
```bash
cd terraform/
terraform init
terraform plan
terraform apply
```
 
This creates:
- A BigQuery dataset (`raw_weather`) in `europe-west1`
- A GCS bucket for pipeline state
 
> After `terraform apply`, note your project ID and bucket name — you will need them in the next steps.
 
---
 
### 3. Install Python dependencies
 
```bash
cd extraction/
pip install dlt[bigquery] dlt[filesystem] requests
```
 
---
 
### 4. Configure dlt
 
The dlt config file is at `extraction/.dlt/config.toml`. Update it with your GCP project details:
 
```toml
[destination.bigquery]
project_id = "your-gcp-project-id"
location = "europe-west1"
```
 
---
 
### 5. Run the dlt ingestion pipeline
 
All pipeline scripts live in the `extraction/` folder.
 
First load the dimension tables (counties, agro zones, thresholds, rainy seasons):
 
```bash
python pipeline_dims.py
```
 
Then run the historical backfill (loads weather data from 1981 to present — may take several minutes):
 
```bash
python pipeline_backfill.py
```
 
For ongoing daily updates:
 
```bash
python pipeline_daily.py
```
 
All pipelines load into BigQuery under the `raw_weather` dataset.
 
---
 
### 6. Run dbt transformations
 
The dbt project lives inside `dbt/kenya_climate_risk_monitor/`.
 
```bash
cd ../dbt/kenya_climate_risk_monitor/
dbt deps
dbt seed
dbt run
dbt test
```
 
> `dbt seed` loads the reference CSV files from the `seeds/` folder (counties, agro zones, thresholds, rainy seasons).
 
This builds the staging and mart layers, including `fct_climate_risk` — the final table used in the dashboard.
 
---
 
### 7. Start Kestra orchestration (optional)
 
Kestra automates the daily pipeline runs using Docker. From the project root:
 
```bash
docker compose up -d
```
 
Then open [http://localhost:8080](http://localhost:8080) to access the Kestra UI and trigger or schedule flows.
 
---
 
### 8. View the dashboard
 
The Looker Studio dashboard connects to `fct_climate_risk` in BigQuery.
 
- **Live dashboard:** [![Live Dashboard](https://img.shields.io/badge/Live_Dashboard-FF6D00?style=for-the-badge&logo=google&logoColor=white)](YOUR_DASHBOARD_URL)
- To connect your own BigQuery: open Looker Studio → Add data source → BigQuery → select your project → `raw_weather` → `fct_climate_risk`


## Contact
**Chacha Marwa** — Junior Data Engineer
- GitHub: [ChachaMarwaDev](https://github.com/ChachaMarwaDev)
- LinkedIn: [chacha-marwa-dev](https://linkedin.com/in/chacha-marwa-dev-355394257)
- X: [@chachamarwadev](https://x.com/chachamarwadev)
- Portfolio: [chachamarwadev.com](https://sites.google.com/view/chachamarwadev)
