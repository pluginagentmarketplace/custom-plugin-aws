---
name: aws_debug
description: Diagnose and troubleshoot AWS infrastructure issues with guided analysis
allowed-tools: Bash, Read, WebSearch
sasmp_version: "1.3.0"
---

# AWS Debug Command

Intelligent AWS issue diagnosis with root cause analysis and resolution guidance.

## Command Specification

| Attribute | Value |
|-----------|-------|
| Command | `/aws-debug` |
| Category | Diagnostics |
| Exit Codes | 0=Issue Resolved, 1=Issue Found, 2=No Issue, 3=Access Denied |
| Timeout | 120 seconds |

## Usage

```bash
/aws-debug                                    # Interactive diagnosis
/aws-debug ec2 i-0abc123def                   # Debug specific EC2
/aws-debug lambda my-function                 # Debug Lambda function
/aws-debug ecs cluster/service                # Debug ECS service
/aws-debug rds mydb-instance                  # Debug RDS instance
/aws-debug vpc vpc-12345678                   # Debug VPC connectivity
/aws-debug --error "timeout connecting"       # Debug by error message
/aws-debug --logs                             # Include CloudWatch logs
```

## Input Validation

| Parameter | Type | Validation | Default |
|-----------|------|------------|---------|
| resource_type | string | ec2, lambda, ecs, rds, vpc, s3, iam | required |
| resource_id | string | Valid resource ID/ARN/name | required |
| --error | string | Error message to analyze | optional |
| --logs | bool | Include log analysis | false |
| --depth | string | quick, standard, deep | standard |
| --region | string | Valid AWS region | from config |

## Supported Resources

| Resource | Common Issues | Debug Capabilities |
|----------|---------------|-------------------|
| EC2 | Connectivity, performance, status checks | Instance status, SG, metrics |
| Lambda | Timeouts, memory, cold starts | Logs, metrics, config |
| ECS | Task failures, deployment, scaling | Events, logs, task status |
| RDS | Connections, performance, storage | Metrics, logs, parameters |
| VPC | Routing, security groups, NAT | Flow logs, route tables |
| S3 | Access denied, replication, lifecycle | Policies, CORS, encryption |
| IAM | Permission denied, policy issues | Policy simulation, roles |

## Diagnostic Flow

```
┌─────────────────┐
│  Identify Issue │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│ Gather Context  │────▶│  Analyze Logs   │
└────────┬────────┘     └────────┬────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│  Check Metrics  │────▶│ Correlate Data  │
└────────┬────────┘     └────────┬────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│  Root Cause     │────▶│   Resolution    │
└─────────────────┘     └─────────────────┘
```

## Implementation

### EC2 Diagnostics
```bash
# Get instance status
aws ec2 describe-instance-status \
  --instance-ids $INSTANCE_ID \
  --include-all-instances

# Check system and instance status
aws ec2 describe-instances \
  --instance-ids $INSTANCE_ID \
  --query 'Reservations[].Instances[].{
    State: State.Name,
    StatusChecks: StateReason.Message,
    PublicIP: PublicIpAddress,
    PrivateIP: PrivateIpAddress,
    SecurityGroups: SecurityGroups[].GroupId,
    SubnetId: SubnetId
  }'

# Get recent metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=$INSTANCE_ID \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 300 \
  --statistics Average Maximum
```

### Lambda Diagnostics
```bash
# Get function configuration
aws lambda get-function-configuration \
  --function-name $FUNCTION_NAME

# Get recent invocations
aws logs filter-log-events \
  --log-group-name /aws/lambda/$FUNCTION_NAME \
  --start-time $(date -d '1 hour ago' +%s)000 \
  --filter-pattern "ERROR"

# Get metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --dimensions Name=FunctionName,Value=$FUNCTION_NAME \
  --metric-name Errors \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 300 \
  --statistics Sum
```

### ECS Diagnostics
```bash
# Get service events
aws ecs describe-services \
  --cluster $CLUSTER \
  --services $SERVICE \
  --query 'services[].events[:10]'

# Get stopped tasks
aws ecs list-tasks \
  --cluster $CLUSTER \
  --service-name $SERVICE \
  --desired-status STOPPED

# Get task stop reason
aws ecs describe-tasks \
  --cluster $CLUSTER \
  --tasks $TASK_ARN \
  --query 'tasks[].{
    StopCode: stopCode,
    StopReason: stoppedReason,
    Containers: containers[].{
      Name: name,
      ExitCode: exitCode,
      Reason: reason
    }
  }'
```

### RDS Diagnostics
```bash
# Get instance status
aws rds describe-db-instances \
  --db-instance-identifier $DB_INSTANCE \
  --query 'DBInstances[].{
    Status: DBInstanceStatus,
    Engine: Engine,
    Storage: AllocatedStorage,
    FreeStorage: FreeStorageSpace,
    Connections: DBInstanceClass
  }'

# Get recent events
aws rds describe-events \
  --source-identifier $DB_INSTANCE \
  --source-type db-instance \
  --duration 1440
```

## Output Format

### Diagnostic Report
```json
{
  "resource": {
    "type": "ec2",
    "id": "i-0abc123def456789",
    "region": "us-east-1",
    "name": "web-server-prod"
  },
  "diagnosis": {
    "status": "issue_found",
    "severity": "high",
    "category": "connectivity",
    "summary": "Instance unreachable due to security group misconfiguration"
  },
  "findings": [
    {
      "component": "security_group",
      "issue": "No inbound rule for port 443",
      "evidence": "sg-12345678 has no HTTPS ingress rule",
      "impact": "HTTPS traffic blocked"
    },
    {
      "component": "network_acl",
      "issue": "Ephemeral ports blocked",
      "evidence": "NACL denies 1024-65535 outbound",
      "impact": "Return traffic blocked"
    }
  ],
  "root_cause": "Security group sg-12345678 missing HTTPS ingress rule",
  "resolution": {
    "steps": [
      "Add inbound rule: HTTPS (443) from 0.0.0.0/0",
      "Verify NACL allows ephemeral ports"
    ],
    "commands": [
      "aws ec2 authorize-security-group-ingress --group-id sg-12345678 --protocol tcp --port 443 --cidr 0.0.0.0/0"
    ],
    "estimated_time": "2 minutes"
  },
  "prevention": [
    "Use security group templates with required ports",
    "Implement CloudFormation/Terraform for infrastructure",
    "Set up Config rules for security group compliance"
  ]
}
```

## Exit Codes

| Code | Meaning | Action |
|------|---------|--------|
| 0 | Issue identified and resolved | Document fix |
| 1 | Issue identified, needs manual fix | Follow resolution steps |
| 2 | No issue found | Resource healthy |
| 3 | Access denied | Check IAM permissions |
| 4 | Resource not found | Verify resource ID |
| 5 | Timeout during diagnosis | Retry with --depth quick |

## Troubleshooting Matrix

### EC2 Issues
| Symptom | Likely Cause | Diagnostic Check |
|---------|--------------|------------------|
| Instance unreachable | Security group | Check SG inbound rules |
| High CPU | Resource contention | Check CloudWatch metrics |
| Status check failed | Instance/system issue | Describe instance status |
| Can't SSH | Key pair/SG/NACL | Verify all three |
| Slow performance | EBS throttling | Check EBS metrics |

### Lambda Issues
| Symptom | Likely Cause | Diagnostic Check |
|---------|--------------|------------------|
| Timeout | Code/external deps | Check duration metric |
| OOM error | Memory too low | Check memory metric |
| Cold start slow | Package size/VPC | Check init duration |
| Permission denied | IAM role | Check execution role |
| Can't reach VPC | No NAT Gateway | Check VPC config |

### ECS Issues
| Symptom | Likely Cause | Diagnostic Check |
|---------|--------------|------------------|
| Task won't start | Image pull failed | Check ECR access |
| Task keeps stopping | Health check fail | Check target group |
| OOM killed | Memory limit | Check container memory |
| Can't schedule | No capacity | Check cluster resources |
| Slow deployment | Health check timeout | Adjust health check |

### RDS Issues
| Symptom | Likely Cause | Diagnostic Check |
|---------|--------------|------------------|
| Connection refused | Security group | Check SG/port |
| Too many connections | Connection limit | Check max_connections |
| Slow queries | Missing index | Check Performance Insights |
| Storage full | Disk space | Check FreeStorageSpace |
| High CPU | Query performance | Check slow query log |

## Debug Checklist by Resource

### EC2 Debug Checklist
- [ ] Instance state is "running"?
- [ ] Status checks passing?
- [ ] Security group allows traffic?
- [ ] NACL allows traffic?
- [ ] Route table correct?
- [ ] Key pair matches?
- [ ] Instance has public/Elastic IP?
- [ ] IAM role attached (if needed)?

### Lambda Debug Checklist
- [ ] Function exists and active?
- [ ] Memory/timeout adequate?
- [ ] Execution role has permissions?
- [ ] Environment variables set?
- [ ] VPC config correct (if VPC)?
- [ ] Dependencies packaged?
- [ ] Handler configured correctly?
- [ ] Triggers configured?

### ECS Debug Checklist
- [ ] Cluster has capacity?
- [ ] Task definition valid?
- [ ] Container image accessible?
- [ ] Task execution role valid?
- [ ] Security group allows traffic?
- [ ] Target group healthy?
- [ ] Service desired count > 0?
- [ ] Deployment circuit breaker?

## Advanced Diagnostics

### VPC Reachability Analyzer
```bash
# Create analysis
aws ec2 create-network-insights-path \
  --source $SOURCE_ENI \
  --destination $DEST_ENI \
  --protocol tcp \
  --destination-port 443

# Start analysis
aws ec2 start-network-insights-analysis \
  --network-insights-path-id $PATH_ID
```

### IAM Policy Simulator
```bash
# Simulate policy
aws iam simulate-principal-policy \
  --policy-source-arn $ROLE_ARN \
  --action-names s3:GetObject \
  --resource-arns arn:aws:s3:::my-bucket/*
```

### CloudWatch Log Insights
```bash
# Query error logs
aws logs start-query \
  --log-group-name /aws/lambda/$FUNCTION \
  --start-time $(date -d '1 hour ago' +%s) \
  --end-time $(date +%s) \
  --query-string 'fields @timestamp, @message | filter @message like /ERROR/ | limit 20'
```

## Related Commands

- `/aws-check` - Verify AWS environment health
- `/aws-deploy` - Deploy with automatic rollback
- `/aws-costs` - Analyze cost anomalies

## References

- [EC2 Troubleshooting](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-troubleshoot.html)
- [Lambda Troubleshooting](https://docs.aws.amazon.com/lambda/latest/dg/troubleshooting.html)
- [ECS Troubleshooting](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/troubleshooting.html)
- [RDS Troubleshooting](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Troubleshooting.html)
