---
name: system-design
description: Design large-scale systems with scalability, reliability, and performance using proven architectural patterns.
---

# System Design

## Quick Start

Design systems that scale to millions of users.

## Core Concepts

### Scalability Axes

**Horizontal** - Add more machines
- Easier to scale
- Requires load balancing
- Stateless services

**Vertical** - Add more resources
- Simpler initially
- Hardware limits
- Single point of failure

### Load Balancing

**Algorithms**
- Round-robin (simple)
- Least connections (even distribution)
- Consistent hashing (cache efficiency)
- Weighted distribution

**Sticky Sessions** - Route same user to same server

## Caching Strategies

### Cache Levels

**Browser Cache** - Client-side
**CDN Cache** - Edge locations
**Application Cache** - In-memory (Redis)
**Database Cache** - Query results

### Cache Invalidation

**Time-Based (TTL)**
- Simple but stale data
- Best for non-critical data

**Event-Based**
- Update on change
- More complex

**LRU (Least Recently Used)**
- Remove oldest when full
- Memory-efficient

## Database Scaling

### Vertical Scaling
- More powerful machine
- Limited by hardware

### Horizontal Scaling (Sharding)

**Shard Key Selection**
- User ID (user-based)
- Timestamp (time-based)
- Geographic (region-based)

**Challenges**
- Distributed transactions
- Cross-shard queries
- Rebalancing

### Replication

**Master-Slave**
- One writer, many readers
- Read replicas for queries

**Multi-Master**
- Multiple writers
- Conflict resolution needed

## Message Queues

**Use Cases**
- Decouple services
- Async processing
- Rate limiting
- Task distribution

**Popular Options**
- RabbitMQ (reliable)
- Kafka (high throughput)
- SQS (AWS managed)

## API Gateway Pattern

```
Clients → API Gateway → Backend Services
              ↓
         Rate limiting
         Authentication
         Request routing
```

**Benefits**
- Single entry point
- Request transformation
- Rate limiting
- Analytics

## Distributed Tracing

**Trace Components**
- Trace ID (request identifier)
- Span ID (operation)
- Parent span (call hierarchy)

**Tools** - Jaeger, Zipkin, X-Ray

## Consistency Models

**Strong Consistency**
- Immediate consistency
- Lower performance
- ACID databases

**Eventual Consistency**
- Delayed consistency
- Higher performance
- BASE model

**CAP Theorem**
- Consistency
- Availability
- Partition tolerance
(Choose 2 of 3)

## Microservices Architecture

**Benefits**
- Independent scaling
- Technology flexibility
- Team autonomy
- Fault isolation

**Challenges**
- Network latency
- Distributed transactions
- Operational complexity
- Testing difficulty

## Disaster Recovery

**RTO** - Recovery Time Objective
**RPO** - Recovery Point Objective

**Strategies**
- Backup and restore
- Pilot light (minimal setup)
- Warm standby (scaled down)
- Active-active (full redundancy)

## Roadmaps Covered

- System Design (https://roadmap.sh/system-design)
- Software Architecture (https://roadmap.sh/software-design-architecture)
