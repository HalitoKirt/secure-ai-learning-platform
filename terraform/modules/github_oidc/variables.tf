variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
}

variable "environment" {
  description = "Deployment environment"
  type        = string
}

variable "github_repository" {
  description = "GitHub repository allowed to assume the deployment role"
  type        = string
}

variable "ecr_repository_arn" {
  description = "ARN of the ECR repository used for application images"
  type        = string
}

variable "ecs_service_arn" {
  description = "ARN of the ECS service GitHub Actions may deploy"
  type        = string
}
