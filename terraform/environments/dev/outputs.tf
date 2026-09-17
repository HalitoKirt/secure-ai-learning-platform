output "vpc_id" {
  description = "VPC ID from networking module."
  value       = module.networking.vpc_id
}

output "public_subnet_ids" {
  description = "Public subnet IDs from networking module."
  value       = module.networking.public_subnet_ids
}

output "log_group_name" {
  description = "CloudWatch log group name for the application."
  value       = module.logging.log_group_name
}

output "ecr_repository_url" {
  description = "ECR repository URL for the application image."
  value       = module.ecr.repository_url
}

output "alb_dns_name" {
  description = "Application Load Balancer DNS name."
  value       = module.load_balancer.alb_dns_name
}

output "target_group_arn" {
  description = "ALB target group ARN for ECS service."
  value       = module.load_balancer.target_group_arn
}

output "ecs_service_name" {
  description = "ECS service name."
  value       = module.compute.service_name
}

output "api_key_secret_arn" {
  description = "ARN of the Secrets Manager secret used for API authentication."
  value       = module.compute.api_key_secret_arn
}

output "github_deploy_role_arn" {
  description = "IAM role ARN used by GitHub Actions for OIDC deployment."
  value       = module.github_oidc.role_arn
}
