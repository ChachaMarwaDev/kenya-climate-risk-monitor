resource "google_bigquery_dataset" "weather_dataset" {
  dataset_id    = var.dataset_id
  friendly_name = var.friendly_name
  description   = var.description
  location      = var.region # Use your region variable

  # Default table expiration (optional)
  default_table_expiration_ms = null # No expiration for permanent tables

  labels = {
    environment = var.environment
    project     = var.dataset_id
  }
}