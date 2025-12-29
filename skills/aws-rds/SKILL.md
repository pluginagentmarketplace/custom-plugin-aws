---
name: aws-rds
description: Master AWS RDS - relational databases, Aurora, and managed database operations
sasmp_version: "1.3.0"
bonded_agent: aws-databases
bond_type: PRIMARY_BOND
---

# AWS RDS Skill

## Create RDS Instance

```bash
# Create PostgreSQL instance
aws rds create-db-instance \
    --db-instance-identifier mydb \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --engine-version 15.4 \
    --master-username admin \
    --master-user-password MyPassword123! \
    --allocated-storage 20 \
    --storage-type gp3 \
    --vpc-security-group-ids sg-12345678 \
    --db-subnet-group-name my-subnet-group \
    --multi-az \
    --backup-retention-period 7

# List instances
aws rds describe-db-instances --query 'DBInstances[].[DBInstanceIdentifier,Engine,DBInstanceStatus]' --output table

# Get endpoint
aws rds describe-db-instances --db-instance-identifier mydb --query 'DBInstances[0].Endpoint' --output json
```

## Supported Engines

| Engine | Versions | Use Case |
|--------|----------|----------|
| PostgreSQL | 12-16 | General RDBMS |
| MySQL | 5.7, 8.0 | Web applications |
| MariaDB | 10.x | MySQL compatible |
| Oracle | 19c, 21c | Enterprise |
| SQL Server | 2017-2022 | Microsoft stack |
| Aurora | MySQL, PostgreSQL | High performance |

## Instance Classes

| Class | vCPU | Memory | Use Case |
|-------|------|--------|----------|
| db.t3.micro | 2 | 1 GB | Dev/Test |
| db.t3.medium | 2 | 4 GB | Small prod |
| db.r6g.large | 2 | 16 GB | Production |
| db.r6g.xlarge | 4 | 32 GB | High memory |

## Backup & Snapshots

```bash
# Create manual snapshot
aws rds create-db-snapshot \
    --db-instance-identifier mydb \
    --db-snapshot-identifier mydb-snapshot-$(date +%Y%m%d)

# Restore from snapshot
aws rds restore-db-instance-from-db-snapshot \
    --db-instance-identifier mydb-restored \
    --db-snapshot-identifier mydb-snapshot-20240101
```

## Assets

- `rds-templates/` - CloudFormation templates
- `connection-strings/` - Driver examples

## References

- `RDS_OPERATIONS.md` - Maintenance guide
