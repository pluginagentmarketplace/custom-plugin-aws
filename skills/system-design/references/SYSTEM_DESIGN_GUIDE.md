# System Design Guide

Essential patterns for designing scalable systems.

## Scalability Patterns

### Horizontal vs Vertical Scaling

| Aspect | Horizontal | Vertical |
|--------|------------|----------|
| How | Add more machines | Bigger machine |
| Cost | Linear | Exponential |
| Limit | Unlimited | Hardware limit |
| Complexity | Higher | Lower |

### Load Balancing Algorithms

```
Round Robin     → Equal distribution
Least Connections → Route to least busy
IP Hash         → Sticky sessions
Weighted        → Based on capacity
```

## Database Patterns

### Sharding Strategies

```
                     ┌─────────────┐
                     │   Router    │
                     └──────┬──────┘
          ┌──────────────┬──┴───────────────┐
          ▼              ▼                   ▼
    ┌──────────┐   ┌──────────┐       ┌──────────┐
    │ Shard 0  │   │ Shard 1  │  ...  │ Shard N  │
    │ A-M      │   │ N-Z      │       │          │
    └──────────┘   └──────────┘       └──────────┘
```

### CAP Theorem

```
Choose 2 of 3:
- Consistency: All nodes see same data
- Availability: Every request gets response
- Partition Tolerance: System works despite network failures

CP: MongoDB, HBase (sacrifice availability)
AP: Cassandra, DynamoDB (sacrifice consistency)
CA: Not possible in distributed systems
```

## Caching Strategies

| Strategy | Description | Use Case |
|----------|-------------|----------|
| Cache-Aside | App manages cache | General purpose |
| Read-Through | Cache fetches on miss | Simple reads |
| Write-Through | Write to cache and DB | Data consistency |
| Write-Behind | Async write to DB | High write throughput |

### Cache Invalidation

```python
# Time-based (TTL)
cache.set(key, value, ttl=3600)

# Event-based
def update_user(user_id, data):
    db.update(user_id, data)
    cache.delete(f"user:{user_id}")

# Version-based
cache.set(f"user:{user_id}:v{version}", data)
```

## Message Queue Patterns

### Pub/Sub

```
Publisher → Topic → Subscriber 1
                 → Subscriber 2
                 → Subscriber 3
```

### Work Queue

```
Producer → Queue → Worker 1
                → Worker 2
                → Worker 3
```

## Microservices Patterns

### Service Discovery

```
┌────────────┐     ┌───────────────┐
│  Service A │◄───►│   Registry    │
└────────────┘     │ (Consul, etcd)│
                   └───────────────┘
┌────────────┐            ▲
│  Service B │────────────┘
└────────────┘
```

### Circuit Breaker

```
States: CLOSED → OPEN → HALF_OPEN → CLOSED

CLOSED: Normal operation
OPEN: Fail fast (after threshold failures)
HALF_OPEN: Test if service recovered
```

## Rate Limiting

### Token Bucket

```python
class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.tokens = capacity
        self.capacity = capacity
        self.refill_rate = refill_rate

    def allow_request(self):
        self.refill()
        if self.tokens > 0:
            self.tokens -= 1
            return True
        return False
```

## Estimation Cheat Sheet

| Metric | Value |
|--------|-------|
| 1 day | 86,400 seconds |
| 1 month | ~2.5 million seconds |
| 1 year | ~31.5 million seconds |
| QPS to daily | QPS × 86,400 |
| 1 KB/s | 2.5 GB/month |
| 1 MB/s | 2.5 TB/month |

## Design Interview Framework

1. **Clarify Requirements** (5 min)
   - Functional requirements
   - Non-functional: scale, latency, availability

2. **Estimate Scale** (5 min)
   - Users, requests, data size
   - Read/write ratio

3. **High-Level Design** (10 min)
   - Core components
   - Data flow

4. **Deep Dive** (15 min)
   - Database schema
   - API design
   - Specific component details

5. **Bottlenecks & Trade-offs** (5 min)
   - Identify weaknesses
   - Discuss alternatives
