variable "project_id" {
  description = "Project ID for GCP"
  type        = string
  default     = "my-portfolio-gcp-project"
}

variable "region" {
  description = "Region for GCP resources"
  type        = string
  default     = "europe-west1"
}

variable "gke_num_nodes" {
  description = "Number of nodes in the GKE node pool"
  type        = number
  default     = 2
}

variable "machine_type" {
  description = "Machine type for the GKE nodes"
  type        = string
  default     = "e2-medium"
}
