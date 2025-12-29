# CloudWatch Monitoring Guide

## Key Metrics by Service

### EC2
| Metric | Threshold | Action |
|--------|-----------|--------|
| CPUUtilization | >80% | Scale up |
| StatusCheckFailed | >0 | Investigate/replace |
| NetworkIn/Out | Baseline +50% | Review traffic |
| DiskReadOps | High | Check I/O patterns |

### Lambda
| Metric | Threshold | Action |
|--------|-----------|--------|
| Errors | >1% of invocations | Check logs |
| Duration | >80% of timeout | Optimize or increase timeout |
| Throttles | >0 | Increase concurrency |
| ConcurrentExecutions | Near limit | Request increase |

### RDS
| Metric | Threshold | Action |
|--------|-----------|--------|
| CPUUtilization | >80% | Scale up |
| FreeStorageSpace | <20% | Increase storage |
| DatabaseConnections | >80% max | Connection pooling |
| FreeableMemory | <10% | Scale up |
| ReadIOPS/WriteIOPS | Near provisioned | Upgrade storage |

### ALB
| Metric | Threshold | Action |
|--------|-----------|--------|
| HTTPCode_Target_5XX | >1% | Check target health |
| TargetResponseTime | >baseline | Check targets |
| HealthyHostCount | <desired | Check instances |
| RequestCount | Spike | Check for attack/issue |

## Log Insights Queries

### Find Errors
```
fields @timestamp, @message
| filter @message like /ERROR|Exception|Failed/
| sort @timestamp desc
| limit 100
```

### Lambda Cold Starts
```
filter @type = "REPORT"
| stats count(*) as invocations,
    sum(@initDuration)/1000 as totalColdStartMs,
    avg(@duration) as avgDuration
by bin(1h)
```

### API Latency Analysis
```
fields @timestamp, @message
| parse @message /latency=(?<latency>\d+)/
| stats avg(latency), max(latency), pct(latency, 95) by bin(5m)
```

### Error Rate by Endpoint
```
fields @timestamp, @message
| parse @message /path=(?<path>\S+).*status=(?<status>\d+)/
| filter status >= 400
| stats count(*) as errors by path
| sort errors desc
```

## Composite Alarms

```yaml
# CloudFormation
CompositeAlarm:
  Type: AWS::CloudWatch::CompositeAlarm
  Properties:
    AlarmName: production-critical
    AlarmRule: |
      ALARM(high-cpu) AND
      (ALARM(high-memory) OR ALARM(high-disk))
    AlarmActions:
      - !Ref CriticalSNSTopic
```

## Metric Math

```bash
# Error rate calculation
aws cloudwatch get-metric-data \
    --metric-data-queries '[
        {"Id": "errors", "MetricStat": {"Metric": {"Namespace": "AWS/Lambda", "MetricName": "Errors"}, "Period": 60, "Stat": "Sum"}},
        {"Id": "invocations", "MetricStat": {"Metric": {"Namespace": "AWS/Lambda", "MetricName": "Invocations"}, "Period": 60, "Stat": "Sum"}},
        {"Id": "errorRate", "Expression": "(errors/invocations)*100", "Label": "Error Rate %"}
    ]'
```

## Best Practices

1. **Create dashboards** for each environment
2. **Set up alarms** before going to production
3. **Use composite alarms** to reduce noise
4. **Enable detailed monitoring** for critical resources
5. **Set retention policies** on log groups
6. **Use metric filters** to create custom metrics from logs
7. **Export logs** to S3 for long-term storage
