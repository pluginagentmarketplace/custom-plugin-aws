# RDS Operations Guide

## Monitoring

### CloudWatch Metrics

Key metrics to monitor:

| Metric | Threshold | Action |
|--------|-----------|--------|
| CPUUtilization | >80% | Scale up |
| FreeStorageSpace | <20% | Increase storage |
| ReadIOPS/WriteIOPS | High | Check queries |
| DatabaseConnections | Near max | Connection pooling |
| FreeableMemory | <5% | Scale up |

### Performance Insights

```bash
# Enable Performance Insights
aws rds modify-db-instance \
    --db-instance-identifier mydb \
    --enable-performance-insights \
    --performance-insights-retention-period 7
```

## Scaling

### Vertical Scaling (Instance Class)

```bash
# Modify instance class (causes downtime)
aws rds modify-db-instance \
    --db-instance-identifier mydb \
    --db-instance-class db.r6g.xlarge \
    --apply-immediately
```

### Storage Scaling

```bash
# Increase storage (no downtime)
aws rds modify-db-instance \
    --db-instance-identifier mydb \
    --allocated-storage 100 \
    --apply-immediately
```

### Read Replicas

```bash
# Create read replica
aws rds create-db-instance-read-replica \
    --db-instance-identifier mydb-replica \
    --source-db-instance-identifier mydb \
    --db-instance-class db.t3.medium
```

## Maintenance

### Parameter Groups

```bash
# Create custom parameter group
aws rds create-db-parameter-group \
    --db-parameter-group-name my-pg15-params \
    --db-parameter-group-family postgres15 \
    --description "Custom PostgreSQL 15 parameters"

# Modify parameters
aws rds modify-db-parameter-group \
    --db-parameter-group-name my-pg15-params \
    --parameters "ParameterName=log_statement,ParameterValue=all,ApplyMethod=immediate"
```

### Maintenance Windows

```bash
# Set maintenance window
aws rds modify-db-instance \
    --db-instance-identifier mydb \
    --preferred-maintenance-window "Mon:04:00-Mon:05:00"
```

## Security

### Encryption

- Enable encryption at rest (KMS)
- Use SSL/TLS for connections
- Rotate credentials with Secrets Manager

### Network

- Use VPC and private subnets
- Configure security groups
- Enable VPC Flow Logs

### IAM Authentication

```bash
# Enable IAM authentication
aws rds modify-db-instance \
    --db-instance-identifier mydb \
    --enable-iam-database-authentication
```

## Backup Strategy

| Type | Frequency | Retention |
|------|-----------|-----------|
| Automated | Daily | 7-35 days |
| Manual Snapshots | Weekly | Indefinite |
| Point-in-Time | Continuous | 5 min granularity |

## Troubleshooting

### Common Issues

1. **Connection timeout** - Check security groups, subnet routing
2. **Too many connections** - Increase max_connections, use pooling
3. **Slow queries** - Enable Performance Insights, add indexes
4. **Storage full** - Enable autoscaling, archive old data
