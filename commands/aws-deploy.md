---
name: aws_deploy
description: Deploy applications to AWS with automated infrastructure provisioning
allowed-tools: Bash, Read, Write
sasmp_version: "1.3.0"
---

# AWS Deploy Command

Intelligent application deployment with best-practice infrastructure patterns.

## Command Specification

| Attribute | Value |
|-----------|-------|
| Command | `/aws-deploy` |
| Category | Deployment |
| Exit Codes | 0=Success, 1=Validation Error, 2=Build Error, 3=Deploy Error, 4=Rollback |
| Timeout | 600 seconds (10 min) |

## Usage

```bash
/aws-deploy                           # Auto-detect and deploy
/aws-deploy --target lambda           # Deploy to Lambda
/aws-deploy --target ecs              # Deploy to ECS Fargate
/aws-deploy --target ec2              # Deploy to EC2
/aws-deploy --target s3               # Deploy static site to S3
/aws-deploy --env production          # Production deployment
/aws-deploy --dry-run                 # Preview changes only
/aws-deploy --rollback                # Rollback last deployment
```

## Input Validation

| Parameter | Type | Validation | Default |
|-----------|------|------------|---------|
| --target | string | lambda, ecs, ec2, s3, amplify, eb | auto-detect |
| --env | string | ^[a-z]{1,20}$ | dev |
| --region | string | Valid AWS region | from config |
| --stack | string | ^[a-zA-Z][-a-zA-Z0-9]{0,127}$ | app-{env} |
| --timeout | int | 60-1800 seconds | 600 |
| --approval | bool | true/false | false (prod=true) |

## Deployment Targets

### Auto-Detection Logic
```
Project Analysis
├── package.json + serverless.yml → Lambda (Serverless Framework)
├── package.json + Dockerfile → ECS Fargate
├── requirements.txt + lambda/ → Lambda (Python)
├── go.mod + main.go → Lambda (Go)
├── index.html only → S3 Static Site
├── Dockerfile only → ECS Fargate
├── buildspec.yml → CodePipeline
└── cdk.json → CDK Deploy
```

### Target Specifications

| Target | Use Case | Cold Start | Scaling | Cost Model |
|--------|----------|------------|---------|------------|
| Lambda | API, Events | 100-500ms | Auto (0-1000) | Per-request |
| ECS Fargate | Containers | N/A | Auto (1-100) | Per-second |
| EC2 + ALB | Traditional | N/A | Manual/ASG | Per-hour |
| S3 + CloudFront | Static sites | N/A | Auto | Per-request |
| Amplify | Full-stack web | N/A | Auto | Per-build + hosting |
| Elastic Beanstalk | Managed | N/A | Auto | Per-instance |

## Deployment Flow

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Validate   │────▶│    Build     │────▶│   Package   │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                 │
┌─────────────┐     ┌──────────────┐     ┌──────▼──────┐
│   Verify    │◀────│    Deploy    │◀────│   Upload    │
└──────┬──────┘     └──────────────┘     └─────────────┘
       │
       ▼
┌─────────────┐     ┌──────────────┐
│  Complete   │ or  │   Rollback   │
└─────────────┘     └──────────────┘
```

## Implementation

### Lambda Deployment
```bash
# Build and package
npm ci --production
zip -r function.zip .

# Deploy function
aws lambda update-function-code \
  --function-name $FUNCTION_NAME \
  --zip-file fileb://function.zip \
  --publish

# Wait for update
aws lambda wait function-updated \
  --function-name $FUNCTION_NAME

# Update alias for production
aws lambda update-alias \
  --function-name $FUNCTION_NAME \
  --name production \
  --function-version $VERSION
```

### ECS Fargate Deployment
```bash
# Build and push image
docker build -t $ECR_REPO:$TAG .
aws ecr get-login-password | docker login --username AWS --password-stdin $ECR_URI
docker push $ECR_REPO:$TAG

# Update service
aws ecs update-service \
  --cluster $CLUSTER \
  --service $SERVICE \
  --force-new-deployment

# Wait for stability
aws ecs wait services-stable \
  --cluster $CLUSTER \
  --services $SERVICE
```

### S3 Static Site Deployment
```bash
# Sync files
aws s3 sync ./dist s3://$BUCKET \
  --delete \
  --cache-control "max-age=31536000" \
  --exclude "index.html"

aws s3 cp ./dist/index.html s3://$BUCKET/index.html \
  --cache-control "no-cache"

# Invalidate CloudFront
aws cloudfront create-invalidation \
  --distribution-id $DIST_ID \
  --paths "/*"
```

## Exit Codes

| Code | Meaning | Recovery Action |
|------|---------|-----------------|
| 0 | Deployment successful | None required |
| 1 | Validation failed | Fix configuration issues |
| 2 | Build failed | Check build logs |
| 3 | Deployment failed | Check CloudFormation events |
| 4 | Rollback executed | Previous version restored |
| 5 | Verification failed | Manual intervention needed |
| 6 | Timeout exceeded | Check deployment status manually |

## Output Format

### Success Output
```json
{
  "status": "success",
  "deployment_id": "d-ABC123XYZ",
  "target": "ecs",
  "environment": "production",
  "duration_seconds": 245,
  "resources": {
    "cluster": "prod-cluster",
    "service": "my-app-service",
    "task_definition": "my-app:42",
    "desired_count": 3,
    "running_count": 3
  },
  "endpoints": [
    "https://api.example.com",
    "https://prod-alb-123456.us-east-1.elb.amazonaws.com"
  ],
  "rollback_command": "/aws-deploy --rollback --deployment-id d-ABC123XYZ"
}
```

### Failure Output
```json
{
  "status": "failed",
  "exit_code": 3,
  "error_type": "DeploymentError",
  "error_message": "ECS service failed to stabilize",
  "failed_step": "deploy",
  "logs": [
    "Task stopped: CannotPullContainerError",
    "Image not found: 123456789012.dkr.ecr.us-east-1.amazonaws.com/app:v1.2.3"
  ],
  "resolution": "Verify ECR image exists and IAM role has ecr:GetDownloadUrlForLayer permission",
  "rollback_status": "automatic_rollback_complete"
}
```

## Troubleshooting

### Decision Tree
```
Deployment Failed?
├── Exit 1 (Validation)
│   ├── Missing files → Check project structure
│   ├── Invalid config → Validate serverless.yml/Dockerfile
│   └── Missing env vars → Set required variables
├── Exit 2 (Build)
│   ├── npm install failed → Check package.json
│   ├── Docker build failed → Check Dockerfile
│   └── Tests failed → Fix failing tests
├── Exit 3 (Deploy)
│   ├── CloudFormation error → Check stack events
│   ├── ECS task failed → Check task logs
│   ├── Lambda error → Check function logs
│   └── Permission denied → Check IAM role
├── Exit 4 (Rollback)
│   ├── Auto rollback → Check what triggered it
│   └── Manual rollback → Verify previous version
└── Exit 5 (Verification)
    ├── Health check failed → Check application health
    └── Endpoint unreachable → Check security groups
```

### Common Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| "CannotPullContainer" | ECR image missing | Build and push image first |
| "ResourceInitializationError" | VPC/SG misconfiguration | Check VPC endpoints, NAT |
| "Function timeout" | Code execution slow | Increase timeout, optimize |
| "ROLLBACK_COMPLETE" | CloudFormation failed | Check stack events for details |
| "Service unavailable" | Health check failing | Check target group health |
| "AccessDenied on S3" | Bucket policy issue | Update bucket policy |

### Debug Checklist

- [ ] AWS CLI configured correctly?
- [ ] Required IAM permissions granted?
- [ ] Docker daemon running (for container deploys)?
- [ ] ECR repository exists?
- [ ] VPC has internet access (NAT Gateway)?
- [ ] Security groups allow traffic?
- [ ] Target group health check configured?
- [ ] Environment variables set?
- [ ] Secrets available in Secrets Manager/SSM?

## Rollback Strategies

| Target | Rollback Method | Time |
|--------|-----------------|------|
| Lambda | Alias to previous version | Instant |
| ECS | Previous task definition | 2-5 min |
| EC2/ASG | Previous launch template | 5-10 min |
| S3 | Versioning restore | 1-2 min |
| CloudFormation | Stack rollback | 5-30 min |

### Automatic Rollback
```bash
# ECS automatic rollback on failure
aws ecs update-service \
  --cluster $CLUSTER \
  --service $SERVICE \
  --deployment-configuration "deploymentCircuitBreaker={enable=true,rollback=true}"
```

## Pre-deployment Checklist

```yaml
validation:
  - name: "AWS credentials valid"
    check: "aws sts get-caller-identity"
  - name: "Target exists"
    check: "aws {service} describe-{resource}"
  - name: "IAM permissions"
    check: "Required policies attached"

build:
  - name: "Dependencies installed"
    check: "npm ci / pip install"
  - name: "Tests passing"
    check: "npm test / pytest"
  - name: "Lint passing"
    check: "npm run lint / flake8"

security:
  - name: "No secrets in code"
    check: "git-secrets scan"
  - name: "Dependencies secure"
    check: "npm audit / safety check"
```

## Related Commands

- `/aws-check` - Verify AWS connectivity before deploy
- `/aws-debug` - Debug deployment issues
- `/aws-costs` - Estimate deployment costs

## References

- [Lambda Deployment](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-package.html)
- [ECS Deployment](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html)
- [CloudFormation Deployments](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/)
