# Database Design Patterns Guide

Best practices for database design and optimization.

## Normalization Levels

| Level | Description | Use When |
|-------|-------------|----------|
| 1NF | Atomic values, no repeating groups | Always |
| 2NF | 1NF + No partial dependencies | OLTP systems |
| 3NF | 2NF + No transitive dependencies | Most applications |
| BCNF | 3NF + Every determinant is a key | Critical data integrity |

## Common Design Patterns

### Soft Delete

```sql
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMPTZ;
CREATE INDEX idx_users_active ON users (id) WHERE deleted_at IS NULL;

-- Query active records
SELECT * FROM users WHERE deleted_at IS NULL;
```

### Audit Trail

```sql
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    table_name VARCHAR(100),
    record_id UUID,
    action VARCHAR(10),
    old_data JSONB,
    new_data JSONB,
    user_id UUID,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Trigger function
CREATE FUNCTION audit_trigger() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_log (table_name, record_id, action, old_data, new_data)
    VALUES (TG_TABLE_NAME, COALESCE(NEW.id, OLD.id),
            TG_OP, to_jsonb(OLD), to_jsonb(NEW));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

### Temporal Tables

```sql
CREATE TABLE products (
    id UUID PRIMARY KEY,
    name VARCHAR(255),
    price DECIMAL(10,2),
    valid_from TIMESTAMPTZ DEFAULT NOW(),
    valid_to TIMESTAMPTZ DEFAULT 'infinity'
);

-- Query at specific point in time
SELECT * FROM products
WHERE valid_from <= '2024-01-15' AND valid_to > '2024-01-15';
```

## Indexing Strategies

### B-Tree (Default)

```sql
-- Equality and range queries
CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_orders_date ON orders (created_at DESC);
```

### Hash

```sql
-- Equality only, smaller size
CREATE INDEX idx_users_id_hash ON users USING hash (id);
```

### GIN (Generalized Inverted)

```sql
-- JSONB, arrays, full-text
CREATE INDEX idx_settings ON users USING gin (settings);
CREATE INDEX idx_tags ON posts USING gin (tags);
```

### Partial Index

```sql
-- Index subset of data
CREATE INDEX idx_active_orders ON orders (created_at)
WHERE status = 'active';
```

### Composite Index

```sql
-- Order matters!
CREATE INDEX idx_orders_user_date ON orders (user_id, created_at DESC);
-- Supports: user_id = X
-- Supports: user_id = X AND created_at > Y
-- Does NOT support: created_at > Y (without user_id)
```

## Query Optimization

### EXPLAIN Analysis

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM orders
WHERE user_id = 'abc' AND created_at > '2024-01-01';

-- Look for:
-- Seq Scan → Add index
-- High cost → Optimize query
-- Loops > 1 → Check join strategy
```

### Common Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| SELECT * | Fetches unnecessary data | Select specific columns |
| N+1 queries | Multiple round trips | Use JOINs or batch |
| OR conditions | Can't use indexes | UNION or restructure |
| Functions on columns | Index not used | Index expression |

## Partitioning

### Range Partitioning

```sql
CREATE TABLE events (
    id UUID,
    event_type VARCHAR(50),
    created_at TIMESTAMPTZ
) PARTITION BY RANGE (created_at);

CREATE TABLE events_2024_01
    PARTITION OF events
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

### List Partitioning

```sql
CREATE TABLE logs (
    id UUID,
    level VARCHAR(10),
    message TEXT
) PARTITION BY LIST (level);

CREATE TABLE logs_error PARTITION OF logs FOR VALUES IN ('ERROR');
CREATE TABLE logs_info PARTITION OF logs FOR VALUES IN ('INFO', 'DEBUG');
```

## Connection Pooling

### PgBouncer Configuration

```ini
[databases]
mydb = host=localhost port=5432 dbname=mydb

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
```

## Replication Strategies

| Type | Use Case | Latency |
|------|----------|---------|
| Streaming | Hot standby | <1s |
| Logical | Selective replication | Seconds |
| Synchronous | Zero data loss | Higher |

## Performance Checklist

- [ ] Appropriate indexes for queries
- [ ] No N+1 query problems
- [ ] Connection pooling configured
- [ ] Query timeout set
- [ ] Vacuum and analyze scheduled
- [ ] Slow query logging enabled
- [ ] Connection limits set
- [ ] Statement timeout configured
