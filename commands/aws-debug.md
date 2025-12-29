---
description: Debug AWS issues and troubleshoot common problems
allowed-tools: Bash, Read, WebSearch
---

# AWS Debug Command

Diagnose and troubleshoot AWS-related issues.

## What This Command Does

1. Identifies the type of issue
2. Gathers relevant logs and metrics
3. Analyzes error patterns
4. Suggests solutions

## Usage

```
/aws-debug [resource-type] [resource-id]
/aws-debug                    # Interactive troubleshooting
```

## Supported Resources

- **EC2**: Connection issues, performance problems
- **Lambda**: Execution errors, timeout issues
- **RDS**: Connection failures, performance
- **ECS/EKS**: Container failures, scheduling issues
- **S3**: Access denied, permission issues
- **VPC**: Network connectivity problems
- **IAM**: Permission errors, access issues

## Common Issues Diagnosed

### EC2
- Instance unreachable
- High CPU/memory usage
- Disk space issues

### Lambda
- Timeout errors
- Memory exhaustion
- Cold start latency

### RDS
- Connection limits exceeded
- Slow queries
- Storage full

### Network
- Security group misconfigurations
- Route table issues
- VPC peering problems

## Output

- Root cause analysis
- Affected resources
- Step-by-step resolution guide
- Prevention recommendations
