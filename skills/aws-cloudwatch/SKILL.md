---
name: aws-cloudwatch
description: Master AWS CloudWatch - metrics, logs, alarms, and monitoring
sasmp_version: "1.3.0"
bonded_agent: aws-devops
bond_type: SECONDARY_BOND
---

# AWS CloudWatch Skill

## Metrics

```bash
# List metrics
aws cloudwatch list-metrics --namespace AWS/EC2

# Get metric data
aws cloudwatch get-metric-statistics \
    --namespace AWS/EC2 \
    --metric-name CPUUtilization \
    --dimensions Name=InstanceId,Value=i-1234567890abcdef0 \
    --start-time 2024-01-01T00:00:00Z \
    --end-time 2024-01-02T00:00:00Z \
    --period 3600 \
    --statistics Average

# Put custom metric
aws cloudwatch put-metric-data \
    --namespace MyApp \
    --metric-name PageLoadTime \
    --value 1.5 \
    --unit Seconds
```

## Alarms

```bash
# Create CPU alarm
aws cloudwatch put-metric-alarm \
    --alarm-name high-cpu \
    --metric-name CPUUtilization \
    --namespace AWS/EC2 \
    --statistic Average \
    --period 300 \
    --threshold 80 \
    --comparison-operator GreaterThanThreshold \
    --evaluation-periods 2 \
    --dimensions Name=InstanceId,Value=i-1234567890abcdef0 \
    --alarm-actions arn:aws:sns:us-east-1:123456789012:alerts

# List alarms
aws cloudwatch describe-alarms --state-value ALARM
```

## Logs

```bash
# Create log group
aws logs create-log-group --log-group-name /my-app/logs

# View log groups
aws logs describe-log-groups

# Tail logs
aws logs tail /aws/lambda/my-function --follow

# Filter logs
aws logs filter-log-events \
    --log-group-name /my-app/logs \
    --filter-pattern "ERROR"

# Log Insights query
aws logs start-query \
    --log-group-name /my-app/logs \
    --start-time $(date -v-1H +%s) \
    --end-time $(date +%s) \
    --query-string 'fields @timestamp, @message | filter @message like /ERROR/ | limit 20'
```

## Dashboards

```bash
# Create dashboard
aws cloudwatch put-dashboard \
    --dashboard-name MyDashboard \
    --dashboard-body file://dashboard.json
```

## Assets

- `dashboards/` - Dashboard definitions
- `alarms/` - Alarm templates

## References

- `MONITORING_GUIDE.md` - Best practices
