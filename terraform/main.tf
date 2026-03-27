terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.25.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region

  # timeouts for TLS handshake issues
  request_timeout = "120s"
}