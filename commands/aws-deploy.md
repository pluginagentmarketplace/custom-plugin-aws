---
description: Deploy applications to AWS using various services
allowed-tools: Bash, Read, Write
---

# AWS Deploy Command

Deploy your application to AWS infrastructure.

## What This Command Does

1. Analyzes your project structure
2. Recommends deployment strategy
3. Guides through deployment steps
4. Validates deployment success

## Usage

```
/aws-deploy [service]
```

## Supported Deployment Targets

### Serverless
- **Lambda + API Gateway** - API endpoints
- **Lambda + S3** - Static website with backend

### Containers
- **ECS Fargate** - Containerized applications
- **EKS** - Kubernetes workloads

### Traditional
- **EC2 + ALB** - Virtual machines
- **Elastic Beanstalk** - Managed platform

### Static Sites
- **S3 + CloudFront** - Static websites
- **Amplify** - Full-stack web apps

## Prerequisites

- AWS CLI configured
- Docker (for container deployments)
- Application code ready

## Example Flow

1. Detect project type (Node.js, Python, etc.)
2. Recommend deployment target
3. Create necessary AWS resources
4. Deploy application
5. Verify and provide access URL
