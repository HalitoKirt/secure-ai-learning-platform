# Production Hardening Backlog

## ECS Networking

Current dev design:

* ALB in public subnets
* ECS tasks in public subnets
* ECS security group only allows inbound traffic from ALB security group
* assign_public_ip = true

Production target:

* ALB remains in public subnets
* ECS tasks move to private subnets
* assign_public_ip = false
* ECS outbound access through NAT Gateway or VPC endpoints
* Consider VPC endpoints for:

  * ECR
  * CloudWatch Logs
  * Secrets Manager
  * Systems Manager (SSM)

---

## Load Balancer

Current:

* HTTP listener on port 80

Future:

* Add ACM certificate
* Add HTTPS listener on port 443
* Redirect HTTP to HTTPS
* Add ALB access logging

---

## ECS Service

Current:

* desired_count = 1
* nginx:latest placeholder image

Future:

* Replace nginx:latest with FastAPI image from ECR
* Enable ECS Exec
* Add autoscaling policies
* Add deployment circuit breaker
* Add task health monitoring

---

## Monitoring

Current:

* CloudWatch Log Group configured

Future:

* CloudWatch Dashboard
* ECS Service alarms
* Target Group health alarms
* ALB 4XX/5XX alarms
* CPU and Memory alarms

---

## Security

Current:

* ALB Security Group
* ECS Security Group
* Network segmentation

Future:

* Add AWS WAF in front of ALB
* Review IAM permissions for least privilege
* Store secrets in AWS Secrets Manager
* Add security monitoring and alerting

---

## Outputs

Future:

* Add alb_dns_name output
* Add target_group_arn output
* Add ecs_service_name output

---

## Deployment

Future:

* Create ECR repository
* Build Docker image
* Push FastAPI image to ECR
* Deploy FastAPI task definition
* Verify /health endpoint through ALB

---

## Container

Container Management

Current:
- Image tag = latest

Production:
- Use immutable version tags
  - v1.0.0
  - v1.0.1
  - v1.1.0
- Avoid relying on latest in production
