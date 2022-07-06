variable "resource_tags" {
  description = "Tags to set for all resources"
  type        = map(string)
  default = {
    project     = "atomos",
    environment = "dev",
  }
}

variable "aws_region" {
  description = "Default AWS region"
  type        = string
  default     = "us-east-1"
}

variable "root_domain_name" {
  description = "Root domain name"
  type        = string
  default     = "azard.io"
}

variable "application_subdomain" {
  description = "Application subdomain depending on the root domain name"
  type        = string
  default     = "atomos.azard.io"
}

variable "aws_s3_bucket_name" {
  description = "S3 bucket name"
  type        = string
  default     = "bucket-atomos-dev"
}