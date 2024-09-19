# Output definitions for the Terraform configuration of the MCA application processing system

# Output the ID of the VPC
output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.mca_vpc.id
}

# Output the IDs of the public subnets
output "public_subnet_ids" {
  description = "The IDs of the public subnets"
  value       = aws_subnet.mca_public_subnet[*].id
}

# Output the IDs of the private subnets
output "private_subnet_ids" {
  description = "The IDs of the private subnets"
  value       = aws_subnet.mca_private_subnet[*].id
}

# Output the connection endpoint for the RDS instance
output "db_endpoint" {
  description = "The connection endpoint for the RDS instance"
  value       = aws_db_instance.mca_db.endpoint
}

# Output the name of the ECS cluster
output "ecs_cluster_name" {
  description = "The name of the ECS cluster"
  value       = aws_ecs_cluster.mca_cluster.name
}

# Output the name of the ECS service
output "ecs_service_name" {
  description = "The name of the ECS service"
  value       = aws_ecs_service.mca_service.name
}

# Output the DNS name of the Application Load Balancer
output "alb_dns_name" {
  description = "The DNS name of the Application Load Balancer"
  value       = aws_lb.mca_alb.dns_name
}

# Output the URL of the ECR repository
output "ecr_repository_url" {
  description = "The URL of the ECR repository"
  value       = aws_ecr_repository.mca_repo.repository_url
}