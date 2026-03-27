# Terraform variables for Kenya Climate Risk Monitor project
# iam.tf variables
variable "account_id" {
  description = "Service account "
  default     = "terra-runner@datazoomcamp-490302.iam.gserviceaccount.com"
}

variable "member" {
  description = "Iam member to grant permissions to (e.g., serviceAccount:<email>)"
  default     = "serviceAccount:${data.google_service_account.terra_runner.email}"
}

# main.tf variables
variable "project_id" {
  description = "My GCP project ID"
  default     = "datazoomcamp-490302"
}

variable "region" {
  description = "My GCP region"
  default     = "europe-west1"
}

# Storage.tf variables
variable "bucket_name" {
  description = "My GCP bucket name"
  default     = "kenya-climate-risk-monitor-data"
}

variable "bucket_location" {
  description = "My GCP bucket location"
  type        = string
  default     = "europe-west1"
}

# bigquery.tf variables
variable "environment" {
  description = "Deployment environment (e.g., dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "dataset_id" {
  description = "My bigquery dataset ID"
  default     = "kenya_weather_analysis"
}

variable "friendly_name" {
  description = "Name of the bigquery dataset"
  type        = string
  default     = "Kenya Weather Analysis Dataset"
}
variable "description" {
  description = "Description of the bigquery dataset"
  type        = string
  default     = "Historical weather data and reference tables for Kenya"
}