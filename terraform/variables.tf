locals {
  data_lake_bucket = "covid_canada_data_lake"
}

variable "project" {
  description = "GCP Project ID"
  default = "sinuous-gist-339116"
  type = string
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default = "northamerica-northeast1"
  type = string
}

variable "zone" {
  description = "Your project zone"
  default     = "northamerica-northeast1-a"
  type        = string
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default = "STANDARD"
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type = string
  default = "covid_CA_data"
}


variable "vm_image" {
  description = "Image for VM"
  default     = "ubuntu-os-cloud/ubuntu-2004-lts"
  type        = string
}

variable "network" {
  description = "Network for your instance/cluster"
  default     = "default"
  type        = string
}