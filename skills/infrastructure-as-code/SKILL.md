---
name: infrastructure-as-code
description: Manage infrastructure using code with Terraform, Kubernetes manifests, and CloudFormation for reproducible, version-controlled deployments.
---

# Infrastructure as Code (IaC)

## Quick Start

Manage cloud infrastructure programmatically using declarative languages.

## Terraform Fundamentals

### Core Concepts

**Provider** - Cloud platform integration (AWS, Azure, GCP)
**Resource** - Infrastructure components (VMs, databases, networks)
**Module** - Reusable configuration bundle
**State** - Current infrastructure state tracking
**Variable** - Input parameters
**Output** - Export values from state

### Basic Terraform Structure

```hcl
terraform {
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

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
  tags = {
    Name = "web-server"
  }
}

output "instance_id" {
  value = aws_instance.web.id
}
```

### State Management

**Local State**
- Simple for development
- Not suitable for teams

**Remote State** (Recommended)
```hcl
terraform {
  backend "s3" {
    bucket         = "terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

**State Locking** - Prevent concurrent modifications

### Modules Best Practices

```
modules/
├── vpc/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── README.md
├── rds/
│   └── main.tf
└── eks/
    └── main.tf
```

### Terraform Workflow

1. **Write** - Create .tf files
2. **Init** - terraform init
3. **Plan** - terraform plan (preview)
4. **Apply** - terraform apply (execute)
5. **Destroy** - terraform destroy (cleanup)

### Common Best Practices

- Use modules for reusability
- Separate environments (dev/staging/prod)
- Use variables and locals
- Use outputs for integration
- Version lock providers
- Remote state with locking
- Use workspaces for variations

## CloudFormation (AWS)

### YAML Template Structure

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'RDS Database Stack'

Parameters:
  DBName:
    Type: String
    Default: myapp

Resources:
  MyDatabase:
    Type: AWS::RDS::DBInstance
    Properties:
      Engine: mysql
      DBName: !Ref DBName
      AllocatedStorage: 20
      DBInstanceClass: db.t3.micro

Outputs:
  DatabaseEndpoint:
    Value: !GetAtt MyDatabase.Endpoint.Address
    Export:
      Name: !Sub '${AWS::StackName}-endpoint'
```

## Kubernetes Manifests (YAML)

### Deployment Example

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: web
        image: myapp:1.0
        ports:
        - containerPort: 3000
        resources:
          limits:
            cpu: 500m
            memory: 512Mi
          requests:
            cpu: 250m
            memory: 256Mi
        env:
        - name: NODE_ENV
          value: "production"
```

### Service Exposure

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  type: LoadBalancer
  selector:
    app: web
  ports:
  - protocol: TCP
    port: 80
    targetPort: 3000
```

## Helm Charts

Package Kubernetes applications for easy deployment.

```
my-app-chart/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
└── README.md
```

## GitOps Workflow

**Infrastructure in Git**
1. Infrastructure defined in Git
2. Automated synchronization
3. Git as single source of truth
4. Automated deployments
5. Audit trail

**Tools**
- ArgoCD for Kubernetes
- Flux for Kubernetes
- Terraform Cloud

## Best Practices

- **Version Control** - All IaC in Git
- **Code Review** - PRs for infrastructure
- **Testing** - Validate before apply
- **Documentation** - Describe infrastructure
- **Security** - Encrypt secrets, use IAM
- **Modules** - Reusable, tested components
- **Automation** - CI/CD for deployments

## Roadmaps Covered

- Terraform (https://roadmap.sh/terraform)
- Kubernetes (https://roadmap.sh/kubernetes)
- DevOps (https://roadmap.sh/devops)
