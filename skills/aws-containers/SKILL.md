---
name: aws-containers
description: Master AWS containers - ECS, EKS, Fargate, and ECR
sasmp_version: "1.3.0"
bonded_agent: aws-compute
bond_type: SECONDARY_BOND
---

# AWS Containers Skill

## ECR (Elastic Container Registry)

```bash
# Create repository
aws ecr create-repository --repository-name my-app

# Get login command
aws ecr get-login-password | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

# Push image
docker tag my-app:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:latest
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:latest

# List images
aws ecr describe-images --repository-name my-app
```

## ECS (Elastic Container Service)

```bash
# Create cluster
aws ecs create-cluster --cluster-name my-cluster

# Register task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create service
aws ecs create-service \
    --cluster my-cluster \
    --service-name my-service \
    --task-definition my-task:1 \
    --desired-count 2 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-123],securityGroups=[sg-123]}"

# Update service
aws ecs update-service \
    --cluster my-cluster \
    --service my-service \
    --force-new-deployment
```

## EKS (Elastic Kubernetes Service)

```bash
# Create cluster
eksctl create cluster \
    --name my-cluster \
    --region us-east-1 \
    --nodegroup-name workers \
    --node-type t3.medium \
    --nodes 3

# Update kubeconfig
aws eks update-kubeconfig --name my-cluster

# Deploy application
kubectl apply -f deployment.yaml
```

## Fargate

No infrastructure to manage - specify CPU/memory and deploy.

| CPU | Memory Options |
|-----|----------------|
| 256 | 512MB, 1GB, 2GB |
| 512 | 1-4GB |
| 1024 | 2-8GB |
| 2048 | 4-16GB |
| 4096 | 8-30GB |

## Assets

- `task-definitions/` - ECS task templates
- `k8s-manifests/` - Kubernetes YAML

## References

- `CONTAINER_GUIDE.md` - Best practices
