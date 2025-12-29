# AWS Services Selection Guide

Comprehensive guide for selecting the right AWS services for your use case.

## Service Selection Decision Tree

```
What are you building?
│
├── Web Application
│   ├── Static Site → S3 + CloudFront
│   ├── Server-Rendered → EC2, ECS, or App Runner
│   └── Serverless → Lambda + API Gateway
│
├── API Backend
│   ├── REST API → API Gateway + Lambda
│   ├── GraphQL → AppSync
│   └── WebSocket → API Gateway WebSocket
│
├── Data Processing
│   ├── Batch Processing → AWS Batch or EMR
│   ├── Stream Processing → Kinesis or MSK
│   └── ETL → Glue
│
├── Database
│   ├── Relational → RDS (PostgreSQL, MySQL)
│   ├── NoSQL Key-Value → DynamoDB
│   ├── Document → DocumentDB
│   ├── Graph → Neptune
│   └── Time Series → Timestream
│
└── Machine Learning
    ├── Pre-built Models → Rekognition, Comprehend, Textract
    ├── Custom Training → SageMaker
    └── Inference → SageMaker Endpoints, Lambda
```

## Compute Services Comparison

| Service | Use Case | Scaling | Pricing Model |
|---------|----------|---------|---------------|
| EC2 | Full control VMs | Manual/Auto | Hourly/Second |
| ECS | Container orchestration | Auto | Pay for resources |
| EKS | Kubernetes workloads | Auto | Control plane + resources |
| Lambda | Event-driven functions | Automatic | Per invocation |
| Fargate | Serverless containers | Auto | Per vCPU/memory |
| App Runner | Simple container apps | Auto | Per request + resources |

## Database Selection Matrix

| Requirement | Best Choice | Why |
|-------------|-------------|-----|
| ACID transactions | RDS (PostgreSQL) | Full SQL support |
| High read/write throughput | DynamoDB | Automatic scaling |
| Complex queries | Redshift | OLAP optimized |
| Real-time analytics | Kinesis + Timestream | Streaming architecture |
| Full-text search | OpenSearch | Elasticsearch-compatible |
| Session storage | ElastiCache (Redis) | In-memory, fast |
| Graph relationships | Neptune | Native graph queries |

## Storage Classes Guide

### S3 Storage Classes

| Class | Access Pattern | Cost | Retrieval Time |
|-------|---------------|------|----------------|
| Standard | Frequent | Highest | Immediate |
| Intelligent-Tiering | Unknown | Optimized | Immediate |
| Standard-IA | Infrequent | Lower | Immediate |
| One Zone-IA | Infrequent, non-critical | Lowest IA | Immediate |
| Glacier Instant | Archival, rare access | Low | Milliseconds |
| Glacier Flexible | Archival | Very low | Minutes to hours |
| Glacier Deep Archive | Long-term archival | Lowest | 12-48 hours |

## Networking Best Practices

### VPC Design

```
Production VPC (10.0.0.0/16)
│
├── Public Subnets (10.0.0.0/20)
│   ├── NAT Gateway
│   ├── Load Balancers
│   └── Bastion Hosts
│
├── Private App Subnets (10.0.16.0/20)
│   ├── Application Servers
│   └── Container Services
│
├── Private Data Subnets (10.0.32.0/20)
│   ├── RDS Instances
│   └── ElastiCache
│
└── Reserved (10.0.48.0/20)
    └── Future expansion
```

### Security Groups vs NACLs

| Feature | Security Groups | NACLs |
|---------|----------------|-------|
| Level | Instance | Subnet |
| State | Stateful | Stateless |
| Rules | Allow only | Allow & Deny |
| Order | All evaluated | Numbered order |
| Default | Deny all in | Allow all |

## Cost Optimization Strategies

### EC2 Pricing Options

1. **On-Demand**: Full price, maximum flexibility
2. **Savings Plans**: 1-3 year commitment, up to 72% savings
3. **Reserved Instances**: Specific instance type, up to 75% savings
4. **Spot Instances**: Unused capacity, up to 90% savings (can be interrupted)

### Right-sizing Checklist

- [ ] Review CloudWatch CPU/Memory metrics
- [ ] Identify idle or underutilized resources
- [ ] Consider Graviton instances (up to 40% better price-performance)
- [ ] Use Cost Explorer recommendations
- [ ] Implement auto-scaling policies

## High Availability Patterns

### Multi-AZ Architecture

```
Region: us-east-1
│
├── AZ-a (10.0.0.0/18)
│   ├── ALB Node
│   ├── App Instance 1
│   └── RDS Primary
│
├── AZ-b (10.0.64.0/18)
│   ├── ALB Node
│   ├── App Instance 2
│   └── RDS Standby
│
└── AZ-c (10.0.128.0/18)
    ├── ALB Node
    └── App Instance 3
```

### Disaster Recovery Options

| Strategy | RTO | RPO | Cost |
|----------|-----|-----|------|
| Backup & Restore | Hours | Hours | $ |
| Pilot Light | 10-30 min | Minutes | $$ |
| Warm Standby | Minutes | Seconds | $$$ |
| Multi-Site Active | Near-zero | Near-zero | $$$$ |

## Security Best Practices

### IAM Guidelines

1. **Never use root account** for daily operations
2. **Enable MFA** on all user accounts
3. **Use roles** instead of long-term credentials
4. **Apply least privilege** principle
5. **Rotate credentials** regularly
6. **Use IAM Access Analyzer** to identify unused permissions

### Encryption Strategy

| Data State | Service | Key Type |
|------------|---------|----------|
| At Rest | KMS | AWS-managed or CMK |
| In Transit | ACM | TLS 1.2+ certificates |
| In Use | Nitro Enclaves | Isolated compute |

## Monitoring & Observability

### CloudWatch Metrics to Monitor

**EC2:**
- CPUUtilization > 80%
- StatusCheckFailed > 0
- NetworkIn/Out anomalies

**RDS:**
- FreeStorageSpace < 20%
- CPUUtilization > 80%
- ReadLatency/WriteLatency > 50ms

**Lambda:**
- Errors > 0
- Duration approaching timeout
- ConcurrentExecutions near limit

### Logging Architecture

```
Application Logs → CloudWatch Logs → Kinesis Firehose → S3 → Athena
                                                     ↓
                                              OpenSearch (real-time)
```

## Quick Reference Commands

```bash
# List EC2 instances
aws ec2 describe-instances --query 'Reservations[].Instances[].{ID:InstanceId,Type:InstanceType,State:State.Name}'

# Check S3 bucket sizes
aws s3 ls --summarize --human-readable s3://bucket-name

# View RDS instances
aws rds describe-db-instances --query 'DBInstances[].{ID:DBInstanceIdentifier,Status:DBInstanceStatus}'

# Get Lambda function list
aws lambda list-functions --query 'Functions[].{Name:FunctionName,Runtime:Runtime}'

# Check costs (last 7 days)
aws ce get-cost-and-usage --time-period Start=$(date -d '7 days ago' +%Y-%m-%d),End=$(date +%Y-%m-%d) --granularity DAILY --metrics UnblendedCost
```
