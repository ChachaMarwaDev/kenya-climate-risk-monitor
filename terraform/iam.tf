# iam.tf - Using existing service account

# ============================================
# REFERENCE EXISTING SERVICE ACCOUNT
# ============================================

# Data source to reference the existing service account
data "google_service_account" "terra_runner" {
  account_id = var.account_id
}

# ============================================
# STORAGE PERMISSIONS
# ============================================

resource "google_storage_bucket_iam_member" "storage_object_admin" {
  bucket = google_storage_bucket.weather_data_bucket.name
  role   = "roles/storage.objectAdmin"
  member = var.member
}

# ============================================
# BIGQUERY PERMISSIONS
# ============================================

resource "google_bigquery_dataset_iam_member" "dataset_editor" {
  dataset_id = google_bigquery_dataset.weather_dataset.dataset_id
  role       = "roles/bigquery.dataEditor"
  member     = var.member
}

resource "google_project_iam_member" "bigquery_job_user" {
  project = var.project_id
  role    = "roles/bigquery.jobUser"
  member  = var.member
}

# Optional: Add logging permissions if needed
resource "google_project_iam_member" "log_viewer" {
  project = var.project_id
  role    = "roles/logging.viewer"
  member  = var.member
}