# outputs.tf
# Prints useful info to the terminal after terraform apply runs

output "bucket_name" {
  description = "GCS bucket name for raw weather data"
  value       = google_storage_bucket.weather_data_bucket.name
}

output "bucket_url" {
  description = "Full GCS bucket URL to use in ingestion scripts"
  value       = "gs://${google_storage_bucket.weather_data_bucket.name}"
}

output "bigquery_dataset_id" {
  description = "BigQuery dataset ID"
  value       = google_bigquery_dataset.weather_dataset.dataset_id
}

output "bigquery_dataset_location" {
  description = "BigQuery dataset location/region"
  value       = google_bigquery_dataset.weather_dataset.location
}

output "service_account_email" {
  description = "The email of the service account being used"
  # OLD: value = google_service_account.terra_runner.email
  # NEW: value = data.google_service_account.terra_runner.email
  value = data.google_service_account.terra_runner.email
}

# If you have other service account outputs, update them too:
output "service_account_name" {
  description = "The name of the service account"
  value       = data.google_service_account.terra_runner.name
}
