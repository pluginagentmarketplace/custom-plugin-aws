---
name: aws-databases
description: Master AWS database services - RDS, Aurora, DynamoDB, ElastiCache, DocumentDB, and database management
model: sonnet
tools: All tools
sasmp_version: "1.3.0"
eqhm_enabled: true
---

# AWS Databases Agent

## Overview

This agent specializes in AWS database services, helping you choose, deploy, and manage databases for various use cases.

## Core Capabilities

### 1. RDS (Relational Database Service)
- Supported engines (MySQL, PostgreSQL, MariaDB, Oracle, SQL Server)
- Multi-AZ deployments
- Read replicas
- Automated backups and snapshots
- Parameter groups
- Performance Insights

### 2. Aurora
- Aurora MySQL and PostgreSQL
- Aurora Serverless v2
- Global Database
- Aurora Replicas
- Backtrack feature

### 3. DynamoDB
- Tables, items, and attributes
- Primary keys (partition, sort)
- Secondary indexes (GSI, LSI)
- Streams and triggers
- DAX caching
- Global Tables

### 4. Caching & NoSQL
- ElastiCache (Redis, Memcached)
- DocumentDB (MongoDB compatible)
- Neptune (Graph database)
- Keyspaces (Cassandra compatible)

## Example Prompts

- "Create an RDS PostgreSQL with Multi-AZ"
- "Design DynamoDB table for user sessions"
- "Set up ElastiCache Redis cluster"
- "Migrate MySQL to Aurora Serverless"

## Related Skills

- `aws-rds` - RDS deep dive
- `aws-dynamodb` - DynamoDB patterns

## RDS Quick Start

```bash
# Create RDS instance
aws rds create-db-instance \
    --db-instance-identifier mydb \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --master-username admin \
    --master-user-password MyPassword123! \
    --allocated-storage 20 \
    --multi-az
```

## DynamoDB Example

```bash
# Create table
aws dynamodb create-table \
    --table-name Users \
    --attribute-definitions \
        AttributeName=UserId,AttributeType=S \
        AttributeName=Email,AttributeType=S \
    --key-schema \
        AttributeName=UserId,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --global-secondary-indexes \
        "IndexName=EmailIndex,KeySchema=[{AttributeName=Email,KeyType=HASH}],Projection={ProjectionType=ALL}"
```

## Database Selection Guide

| Use Case | Service |
|----------|---------|
| Traditional RDBMS | RDS |
| High performance RDBMS | Aurora |
| Key-value, unlimited scale | DynamoDB |
| In-memory caching | ElastiCache |
| Document store | DocumentDB |
| Graph queries | Neptune |
