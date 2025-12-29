# AWS Container Guide

## ECS vs EKS Decision Matrix

| Factor | ECS | EKS |
|--------|-----|-----|
| Complexity | Lower | Higher |
| Kubernetes skills | Not needed | Required |
| Portability | AWS-specific | Multi-cloud |
| Cost | Lower | Higher (control plane) |
| Ecosystem | AWS native | Kubernetes ecosystem |

## Container Best Practices

### Dockerfile Optimization

```dockerfile
# Multi-stage build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Production image
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER node
EXPOSE 8080
CMD ["node", "dist/server.js"]
```

### Security

1. **Use non-root user** in containers
2. **Scan images** with ECR scanning
3. **Use secrets** from Secrets Manager
4. **Enable VPC** networking
5. **Limit capabilities** in task definition

### Logging

```json
{
    "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
            "awslogs-group": "/ecs/my-app",
            "awslogs-region": "us-east-1",
            "awslogs-stream-prefix": "ecs",
            "awslogs-create-group": "true"
        }
    }
}
```

### Health Checks

```json
{
    "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8080/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 60
    }
}
```

## ECS Service Patterns

### Rolling Update (Default)
```json
{
    "deploymentConfiguration": {
        "maximumPercent": 200,
        "minimumHealthyPercent": 100
    }
}
```

### Blue/Green with CodeDeploy
- Zero-downtime deployments
- Automatic rollback
- Traffic shifting

## EKS Add-ons

Essential add-ons:
- **CoreDNS** - DNS for pods
- **kube-proxy** - Network proxy
- **VPC CNI** - AWS VPC networking
- **EBS CSI** - Storage driver

Optional:
- **ALB Controller** - Ingress
- **Cluster Autoscaler** - Node scaling
- **External Secrets** - Secrets Manager integration

## Cost Optimization

1. **Use Spot instances** for EKS nodes
2. **Right-size Fargate** tasks
3. **Use ECR lifecycle policies** to clean old images
4. **Enable Savings Plans** for consistent usage
