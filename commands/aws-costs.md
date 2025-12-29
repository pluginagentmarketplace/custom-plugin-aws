---
description: Analyze AWS costs and get cost optimization recommendations
allowed-tools: Bash, Read
---

# AWS Costs Command

Get a summary of your AWS costs and identify optimization opportunities.

## What This Command Does

1. Retrieves current month's spending
2. Compares to previous months
3. Breaks down costs by service
4. Identifies top spending areas
5. Suggests cost optimization strategies

## Usage

```
/aws-costs
/aws-costs [days]  # Last N days
```

## Cost Categories

- **Compute**: EC2, Lambda, ECS, EKS
- **Storage**: S3, EBS, EFS, Glacier
- **Database**: RDS, DynamoDB, ElastiCache
- **Network**: Data transfer, NAT Gateway, VPN
- **Other**: CloudWatch, Secrets Manager, etc.

## Optimization Tips

Based on the analysis, this command will suggest:
- Right-sizing EC2 instances
- Reserved Instances or Savings Plans
- S3 lifecycle policies
- Unused resource cleanup
- Architecture improvements
