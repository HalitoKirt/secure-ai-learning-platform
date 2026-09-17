variable "aws_region" {
  description = "AWS region for the dev environment."
  type        = string
}

variable "project_name" {
  description = "Project name used for resource naming and tagging."
  type        = string
}

variable "environment" {
  description = "Deployment environment name."
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC."
  type        = string
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets."
  type        = list(string)
}

variable "availability_zones" {
  description = "Availability zones for public subnets."
  type        = list(string)
}

variable "log_retention_days" {
  description = "Number of days to retain CloudWatch logs."
  type        = number
  default     = 14
}

variable "container_image" {
  description = "Container image URI for the FastAPI application"
  type        = string
}
