---
name: data-engineering
description: Build scalable data pipelines, ETL/ELT systems, and data warehouses for processing and analyzing massive datasets efficiently.
---

# Data Engineering

## Quick Start

Build reliable, scalable data infrastructure for organizations.

## Data Pipeline Architecture

### ETL vs ELT

**ETL (Extract-Transform-Load)**
- Transform before loading
- Smaller data volume in warehouse
- Complex transformations before storage

**ELT (Extract-Load-Transform)**
- Load raw data first
- Transform in warehouse
- Scales better, modern approach

### Pipeline Components

**Source** → **Extraction** → **Transformation** → **Loading** → **Warehouse**

## Data Warehousing

### Concepts

**OLTP** (Online Transaction Processing)
- Real-time transactions
- Normalized schema
- Frequent updates

**OLAP** (Online Analytical Processing)
- Historical analysis
- Denormalized schema
- Infrequent updates

### Data Warehouse Schema

**Star Schema**
```
Fact table (transactions)
├── Dimension: Users
├── Dimension: Products
├── Dimension: Date
└── Dimension: Location
```

**Snowflake Schema** - Normalized dimensions

### Popular Warehouses

- **Snowflake** - Cloud-native, easy scaling
- **BigQuery** - Google's serverless warehouse
- **Redshift** - AWS data warehouse
- **Databricks** - Lakehouse platform
- **Synapse** - Azure's warehouse

## ETL Tools & Frameworks

### Apache Airflow

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

dag = DAG(
    'data_pipeline',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily'
)

def extract_data():
    # Extract from source
    pass

extract_task = PythonOperator(
    task_id='extract',
    python_callable=extract_data,
    dag=dag
)
```

### Other Tools

- **Spark** - Distributed processing
- **Kafka** - Real-time streaming
- **dbt** - Transform in warehouse
- **Talend** - Low-code ETL

## Data Quality & Validation

**Great Expectations**
```python
import great_expectations as ge

df = ge.read_csv("data.csv")
df.expect_column_values_to_be_in_set("status", ["active", "inactive"])
df.validate()
```

**Data Quality Checks**
- Completeness (null values)
- Accuracy (correct values)
- Consistency (referential integrity)
- Timeliness (fresh data)

## Streaming Data

### Apache Kafka

- Distributed event streaming
- High throughput, low latency
- Durable, replicated topics
- Consumer groups for scaling

### Real-Time Processing

**Flink** - Stream processing
**Spark Streaming** - Micro-batch processing
**Kinesis** - AWS streaming service

## Data Governance

**Metadata Management**
- Data catalogs (Collibra, Alation)
- Lineage tracking
- Documentation

**Data Quality**
- SLOs for data freshness
- Automated validation
- Monitoring dashboards

**Security & Compliance**
- Access controls (RBAC)
- Encryption (at rest, in transit)
- Audit logging
- GDPR/CCPA compliance

## Performance Optimization

**Partitioning**
- By date, region, customer
- Faster queries on subsets

**Indexing**
- Speed up lookups
- Trade-off: storage and write speed

**Compression**
- Parquet, ORC formats
- Columnar storage benefits
- Reduce storage costs

## Roadmaps Covered

- Data Engineer (https://roadmap.sh/data-engineer)
- Backend (https://roadmap.sh/backend)
