# Variable definitions for the Terraform configuration of the MCA application processing system

# Define the AWS region for resource deployment
variable "aws_region" {
  type        = string
  description = "The AWS region to deploy the resources"
  default     = "us-west-2"
}

# Define the project name for tagging and naming resources
variable "project_name" {
  type        = string
  description = "The name of the project, used for tagging and naming resources"
  default     = "mca-application-processor"
}

# Define the deployment environment
variable "environment" {
  type        = string
  description = "The deployment environment (e.g., dev, staging, prod)"
  default     = "dev"
}

# Define the CIDR block for the VPC
variable "vpc_cidr" {
  type        = string
  description = "The CIDR block for the VPC"
  default     = "10.0.0.0/16"
}

# Define the CIDR blocks for public subnets
variable "public_subnet_cidrs" {
  type        = list(string)
  description = "The CIDR blocks for the public subnets"
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

# Define the CIDR blocks for private subnets
variable "private_subnet_cidrs" {
  type        = list(string)
  description = "The CIDR blocks for the private subnets"
  default     = ["10.0.3.0/24", "10.0.4.0/24"]
}

# Define the database name
variable "db_name" {
  type        = string
  description = "The name of the database"
  default     = "mca_db"
}

# Define the database username
variable "db_username" {
  type        = string
  description = "The username for the database"
  default     = "mca_admin"
}

# Define the database password (marked as sensitive)
variable "db_password" {
  type        = string
  description = "The password for the database"
  sensitive   = true
}

# Define the RDS instance class
variable "db_instance_class" {
  type        = string
  description = "The instance class for the RDS instance"
  default     = "db.t3.micro"
}

# Define the CPU units for the ECS task
variable "ecs_task_cpu" {
  type        = number
  description = "The number of CPU units for the ECS task"
  default     = 256
}

# Define the memory for the ECS task
variable "ecs_task_memory" {
  type        = number
  description = "The amount of memory (in MiB) for the ECS task"
  default     = 512
}

# Define the desired count of ECS tasks
variable "ecs_task_desired_count" {
  type        = number
  description = "The desired number of instances of the ECS task"
  default     = 2
}

# Define the application port
variable "app_port" {
  type        = number
  description = "The port the application listens on"
  default     = 8000
}

# Define the health check path
variable "health_check_path" {
  type        = string
  description = "The path for the health check endpoint"
  default     = "/health"
}