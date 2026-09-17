terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

module "networking" {
  source = "../../modules/networking"

  project_name        = var.project_name
  environment         = var.environment
  vpc_cidr            = var.vpc_cidr
  public_subnet_cidrs = var.public_subnet_cidrs
  availability_zones  = var.availability_zones
}

module "security" {
  source = "../../modules/security"

  project_name = var.project_name
  environment  = var.environment
  vpc_id       = module.networking.vpc_id
  app_port     = 8000
}

module "logging" {
  source = "../../modules/logging"

  project_name       = var.project_name
  environment        = var.environment
  log_retention_days = var.log_retention_days
}

module "load_balancer" {
  source = "../../modules/load_balancer"

  project_name          = var.project_name
  environment           = var.environment
  vpc_id                = module.networking.vpc_id
  public_subnet_ids     = module.networking.public_subnet_ids
  alb_security_group_id = module.security.alb_security_group_id
  app_port              = 8000
  health_check_path     = "/health"
}

module "ecr" {
  source = "../../modules/ecr"

  project_name = var.project_name
  environment  = var.environment
}

module "compute" {
  source = "../../modules/compute"

  project_name          = var.project_name
  environment           = var.environment
  aws_region            = var.aws_region
  container_image       = "${module.ecr.repository_url}:latest"
  app_port              = 8000
  log_group_name        = module.logging.log_group_name
  subnet_ids            = module.networking.public_subnet_ids
  ecs_security_group_id = module.security.ecs_security_group_id
  target_group_arn      = module.load_balancer.target_group_arn
  desired_count         = 1
}

module "github_oidc" {
  source = "../../modules/github_oidc"

  project_name       = var.project_name
  environment        = var.environment
  github_repository  = "HalitoKirt/secure-ai-learning-platform"
  ecr_repository_arn = module.ecr.repository_arn
  ecs_service_arn    = module.compute.service_arn
}
