# Provider configuration
provider "aws" {
  # AWS provider configuration (region, credentials, etc.) should be specified here or through environment variables
}

# Data source for available Availability Zones
data "aws_availability_zones" "available" {
  state = "available"
}

# VPC for the MCA application
resource "aws_vpc" "mca_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "mca-vpc"
  }
}

# Public subnets for the MCA application
resource "aws_subnet" "mca_public_subnet" {
  count                   = 2
  vpc_id                  = aws_vpc.mca_vpc.id
  cidr_block              = "10.0.${count.index}.0/24"
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "mca-public-subnet-${count.index + 1}"
  }
}

# Internet Gateway for the VPC
resource "aws_internet_gateway" "mca_igw" {
  vpc_id = aws_vpc.mca_vpc.id

  tags = {
    Name = "mca-igw"
  }
}

# Route table for public subnets
resource "aws_route_table" "mca_public_rt" {
  vpc_id = aws_vpc.mca_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.mca_igw.id
  }

  tags = {
    Name = "mca-public-rt"
  }
}

# Associate public subnets with the route table
resource "aws_route_table_association" "mca_public_rt_association" {
  count          = 2
  subnet_id      = aws_subnet.mca_public_subnet[count.index].id
  route_table_id = aws_route_table.mca_public_rt.id
}

# Security group for the MCA application
resource "aws_security_group" "mca_sg" {
  name        = "mca-security-group"
  description = "Security group for MCA application"
  vpc_id      = aws_vpc.mca_vpc.id

  ingress {
    description = "HTTP from anywhere"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS from anywhere"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "mca-security-group"
  }
}

# Subnet group for RDS instance
resource "aws_db_subnet_group" "mca_db_subnet_group" {
  name       = "mca_db_subnet_group"
  subnet_ids = aws_subnet.mca_public_subnet[*].id

  tags = {
    Name = "mca-db-subnet-group"
  }
}

# RDS instance for the MCA application
resource "aws_db_instance" "mca_db" {
  identifier          = "mca-db"
  engine              = "postgres"
  engine_version      = "13.7"
  instance_class      = "db.t3.micro"
  allocated_storage   = 20
  db_name             = "mca_db"
  username            = "mca_admin"
  password            = var.db_password
  db_subnet_group_name = aws_db_subnet_group.mca_db_subnet_group.name
  vpc_security_group_ids = [aws_security_group.mca_sg.id]
  skip_final_snapshot = true

  tags = {
    Name = "mca-db"
  }
}

# ECS cluster for the MCA application
resource "aws_ecs_cluster" "mca_cluster" {
  name = "mca-cluster"

  tags = {
    Name = "mca-ecs-cluster"
  }
}

# ECS task definition for the MCA application
resource "aws_ecs_task_definition" "mca_task" {
  family                   = "mca-task"
  container_definitions    = file("task-definition.json")
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn
}

# ECS service for the MCA application
resource "aws_ecs_service" "mca_service" {
  name            = "mca-service"
  cluster         = aws_ecs_cluster.mca_cluster.id
  task_definition = aws_ecs_task_definition.mca_task.arn
  desired_count   = 2
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = aws_subnet.mca_public_subnet[*].id
    security_groups  = [aws_security_group.mca_sg.id]
    assign_public_ip = true
  }
}

# Note: The following resources are referenced but not defined in this file:
# - var.db_password: This should be defined in a variables.tf file or passed as an input variable
# - aws_iam_role.ecs_execution_role: This IAM role should be defined separately for ECS task execution