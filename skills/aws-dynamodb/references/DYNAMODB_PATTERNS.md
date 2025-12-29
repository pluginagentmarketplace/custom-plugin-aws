# DynamoDB Design Patterns

## 1. Single-Table Design

Store multiple entity types in one table using composite keys.

```
PK          | SK              | Entity
------------|-----------------|--------
USER#123    | PROFILE         | User profile
USER#123    | ORDER#456       | User's order
ORDER#456   | DETAILS         | Order details
ORDER#456   | ITEM#789        | Order line item
PRODUCT#789 | DETAILS         | Product info
```

**Benefits:**
- Fewer tables to manage
- Efficient queries across entities
- Reduced latency

## 2. Adjacency List Pattern

For hierarchical data (org charts, file systems).

```
PK          | SK          | Data
------------|-------------|------
ORG#1       | METADATA    | {name: "Acme Corp"}
ORG#1       | DEPT#A      | {name: "Engineering"}
DEPT#A      | METADATA    | {name: "Engineering"}
DEPT#A      | EMP#100     | {name: "John"}
```

## 3. Materialized Graph Pattern

For many-to-many relationships.

```
# Users and Groups
PK          | SK          | Type
------------|-------------|------
USER#123    | GROUP#abc   | membership
GROUP#abc   | USER#123    | membership
```

## 4. Time-Series Pattern

For IoT, logs, metrics.

```
PK              | SK                  | Value
----------------|---------------------|-------
SENSOR#1#2024   | 2024-01-15T10:00:00 | 25.5
SENSOR#1#2024   | 2024-01-15T10:05:00 | 26.0
```

**Hot partition mitigation:**
- Include time period in PK
- Use write sharding

## 5. GSI Overloading

Multiple entity types in one GSI.

```
GSI1PK              | GSI1SK      | Use
--------------------|-------------|-----
EMAIL#user@test.com | USER#123    | User lookup by email
STATUS#PENDING      | ORDER#456   | Orders by status
CATEGORY#Books      | PRODUCT#789 | Products by category
```

## Access Pattern Checklist

Before designing:
1. List ALL access patterns
2. Identify read/write ratios
3. Consider hot partitions
4. Plan for growth

## Capacity Planning

### On-Demand
- Unpredictable traffic
- New applications
- Pay per request

### Provisioned
- Predictable traffic
- Cost optimization
- Reserved capacity available

## Performance Tips

1. **Avoid scans** - Use queries with indexes
2. **Distribute partition keys** - Avoid hot partitions
3. **Use sparse indexes** - Only project needed attributes
4. **Batch operations** - Use BatchWriteItem
5. **DAX caching** - For read-heavy workloads
