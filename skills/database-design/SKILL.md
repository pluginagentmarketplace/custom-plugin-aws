---
name: database-design
description: Master database design, normalization, query optimization, and selection between SQL, NoSQL, and specialized databases.
---

# Database Design

## Quick Start

Design efficient, scalable databases for any use case.

## Relational Databases (SQL)

### Normalization

**1NF** - Atomic values, no repeating groups
**2NF** - No partial dependencies
**3NF** - No transitive dependencies
**BCNF** - Every determinant is a candidate key

**Denormalization** - Trade normalization for performance

### Schema Design

**Primary Keys**
- Unique identifier
- Clustered index (ordering)
- Should be immutable

**Foreign Keys**
- Referential integrity
- Relationship enforcement
- Index for performance

**Indexes**
- Speed up queries
- Slow down writes
- B-tree, Hash, Full-text

### Query Optimization

**EXPLAIN Plan**
```sql
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
```

**Optimization Techniques**
- Add indexes on WHERE clauses
- Avoid SELECT *
- Join optimization
- Subquery optimization
- Statistics for optimizer

### Transactions

**ACID Properties**
- **Atomicity** - All or nothing
- **Consistency** - Valid state
- **Isolation** - Concurrent independence
- **Durability** - Persistent

**Isolation Levels**
- Read Uncommitted (dirty reads)
- Read Committed (no dirty reads)
- Repeatable Read (no phantom reads)
- Serializable (fully isolated)

## NoSQL Databases

### Document Databases (MongoDB)

**Structure**
```json
{
  "_id": ObjectId(),
  "name": "John",
  "email": "john@example.com",
  "posts": [
    { "title": "...", "date": "..." }
  ]
}
```

**Advantages**
- Flexible schema
- Nested data
- Easy to scale

**Disadvantages**
- No transactions (historically)
- Data duplication
- No joins

### Key-Value Stores (Redis)

**Use Cases**
- Caching
- Session storage
- Real-time counters
- Message queues

**Data Structures**
- Strings
- Lists
- Sets
- Sorted Sets
- Hashes

### Time-Series Databases

**InfluxDB, Prometheus**
- Optimized for metrics
- High-write throughput
- Time-based queries

## Database Selection

| Type | SQL | MongoDB | Redis | Cassandra |
|------|-----|---------|-------|-----------|
| Transactions | ✓ | Limited | ✗ | ✗ |
| Scaling | Vertical | Horizontal | Horizontal | Horizontal |
| Consistency | Strong | Eventual | Strong | Eventual |
| Query | SQL | JSON | Commands | CQL |

## Scaling Strategies

### Replication

**Master-Slave**
- One writer
- Multiple readers
- Lag consideration

**Multi-Master**
- Multiple writers
- Conflict resolution
- Complexity

### Sharding (Partitioning)

**Shard Key Selection**
- User ID (user-based)
- Timestamp (time-based)
- Geographic (location-based)

**Challenges**
- Distributed joins
- Cross-shard queries
- Rebalancing

## PostgreSQL Specifics

### Advanced Features

**JSONB** - Efficient JSON storage
**Full-Text Search** - Text indexing
**Arrays** - Array data type
**Ranges** - Range types
**Extensions** - UUID, PostGIS, etc.

**Replication**
- Streaming replication
- Logical replication
- Slots for ordering

### Performance Tuning

**Configuration**
- shared_buffers
- effective_cache_size
- work_mem
- maintenance_work_mem

## Backup & Recovery

**Backup Types**
- Full backup
- Incremental backup
- Differential backup
- Continuous archiving

**Recovery**
- Point-in-time recovery (PITR)
- Testing recovery procedures
- RTO/RPO targets

## Monitoring

**Key Metrics**
- Query latency (p50, p95, p99)
- Slow queries
- Index usage
- Table bloat
- Connection count

## Roadmaps Covered

- SQL (https://roadmap.sh/sql)
- MongoDB (https://roadmap.sh/mongodb)
- PostgreSQL DBA (https://roadmap.sh/postgresql-dba)
- Redis (https://roadmap.sh/redis)
