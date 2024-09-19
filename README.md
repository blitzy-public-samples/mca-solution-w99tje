# MCA Application Processing System

This project implements a comprehensive cloud-based solution for automating and streamlining the intake, processing, and management of Merchant Cash Advance (MCA) applications for Dollar Funding.

## Features

- Email Processing Module
- Document Classification Engine
- Advanced OCR and Data Extraction Service
- Secure Data Storage Solution
- RESTful API
- Web-based User Interface
- Webhook Notification System

## Technology Stack

- Backend: Python 3.9+, FastAPI
- Frontend: React.js
- Database: Amazon Aurora PostgreSQL
- Cloud Infrastructure: AWS (EC2, S3, Textract, VPC, IAM, CloudWatch)
- Containerization: Docker
- Orchestration: Kubernetes
- Infrastructure as Code: Terraform

## Getting Started

### Prerequisites

- Docker and Docker Compose
- AWS CLI configured with appropriate credentials
- Terraform CLI

### Installation

1. Clone the repository
2. Navigate to the project directory
3. Copy `.env.example` to `.env` and fill in the required environment variables
4. Run `docker-compose up --build` to start the application

## Usage

- Access the web interface at `http://localhost:3000`
- API documentation is available at `http://localhost:8000/docs`

## Deployment

1. Ensure AWS credentials are configured
2. Navigate to the `terraform` directory
3. Run `terraform init` to initialize Terraform
4. Run `terraform apply` to create the infrastructure
5. Use the deployment script: `./scripts/deploy.sh`

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.