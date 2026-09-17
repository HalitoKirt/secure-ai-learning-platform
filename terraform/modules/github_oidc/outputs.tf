output "role_arn" {
  description = "ARN of the IAM role assumed by GitHub Actions through OIDC"
  value       = aws_iam_role.github_deploy.arn
}
