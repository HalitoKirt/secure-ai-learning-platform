variable "project_name" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "aws_region" {
  description = "AWS region"
  type        = string
}

variable "container_name" {
  description = "Container name"
  type        = string
  default     = "secure-ai-platform-api"
}

variable "container_image" {
  description = "Container image URI"
  type        = string
}

variable "app_port" {
  description = "Application port"
  type        = number
  default     = 8000
}

variable "task_cpu" {
  description = "Fargate task CPU"
  type        = number
  default     = 512
}

variable "task_memory" {
  description = "Fargate task memory"
  type        = number
  default     = 1024
}

variable "log_group_name" {
  description = "CloudWatch log group name"
  type        = string
}

variable "subnet_ids" {
  description = "Subnet IDs for ECS tasks"
  type        = list(string)
}

variable "ecs_security_group_id" {
  description = "Security group ID for ECS tasks"
  type        = string
}

variable "target_group_arn" {
  description = "ALB target group ARN"
  type        = string
}

variable "desired_count" {
  description = "Number of ECS tasks to run"
  type        = number
  default     = 1
}
