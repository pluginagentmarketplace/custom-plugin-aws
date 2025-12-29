# Data Engineering Patterns

## ETL vs ELT

| Aspect | ETL | ELT |
|--------|-----|-----|
| Transform | Before load | After load |
| Best for | Small data | Big data |
| Tools | Informatica | dbt, Spark |

## Data Quality Dimensions

1. **Completeness** - No missing values
2. **Accuracy** - Correct values
3. **Consistency** - Same across systems
4. **Timeliness** - Up to date
5. **Uniqueness** - No duplicates

## Pipeline Patterns

### Batch Processing
```
Source → Extract → Transform → Load → Warehouse
         (daily)
```

### Stream Processing
```
Source → Kafka → Flink → Transform → Sink
         (real-time)
```

## Data Modeling

### Star Schema
```
         ┌─────────┐
         │  Fact   │
         │  Table  │
         └────┬────┘
    ┌─────────┼─────────┐
    ▼         ▼         ▼
┌───────┐ ┌───────┐ ┌───────┐
│ Dim 1 │ │ Dim 2 │ │ Dim 3 │
└───────┘ └───────┘ └───────┘
```

## Tools

| Category | Tools |
|----------|-------|
| Orchestration | Airflow, Prefect |
| Processing | Spark, Flink |
| Transformation | dbt |
| Streaming | Kafka, Kinesis |
