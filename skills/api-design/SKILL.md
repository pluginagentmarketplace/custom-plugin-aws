---
name: api-design
description: Master REST API design, GraphQL, gRPC, and API architecture patterns for building scalable, maintainable, and well-documented APIs.
---

# API Design & Architecture

## Quick Start

Design APIs that are intuitive, scalable, and developer-friendly.

## REST API Fundamentals

### Core Principles

**Resource-Oriented**: Use nouns, not verbs
```
✓ GET  /users
✓ POST /users
✗ GET  /getUsers
```

**HTTP Methods**
- GET: Retrieve (safe, idempotent)
- POST: Create (not idempotent)
- PUT: Replace (idempotent)
- PATCH: Partial update
- DELETE: Remove (idempotent)

### Status Codes

| Code | Meaning | Use Case |
|------|---------|----------|
| 200  | OK | Successful request |
| 201  | Created | Resource created |
| 204  | No Content | Success, no body |
| 400  | Bad Request | Invalid input |
| 401  | Unauthorized | Auth required |
| 403  | Forbidden | No permission |
| 404  | Not Found | Resource missing |
| 409  | Conflict | State conflict |
| 422  | Unprocessable | Validation failed |
| 500  | Server Error | Internal error |

### URL Design

```
GET    /api/v1/users
POST   /api/v1/users
GET    /api/v1/users/{id}
PUT    /api/v1/users/{id}
PATCH  /api/v1/users/{id}
DELETE /api/v1/users/{id}
GET    /api/v1/users/{id}/posts
GET    /api/v1/posts?status=draft&sort=-created
```

## Response Format

**Success**
```json
{
  "data": {
    "id": "123",
    "name": "John",
    "email": "john@example.com"
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

**Error**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [{
      "field": "email",
      "message": "Email invalid"
    }]
  }
}
```

## GraphQL Design

### Type Definition

```graphql
type User {
  id: ID!
  email: String!
  name: String!
  posts: [Post!]!
}

type Query {
  user(id: ID!): User
  users(first: Int, after: String): UserConnection!
}

type Mutation {
  createUser(input: CreateUserInput!): UserPayload!
}
```

### Optimization

- Query complexity analysis
- DataLoader for N+1 prevention
- Persisted queries
- Field-level caching
- Authorization directives

## API Security

**Authentication**
- API Keys for public APIs
- OAuth 2.0 for 3rd party
- JWT for microservices
- mTLS for service-to-service

**Rate Limiting**
- Token bucket (X req/Y sec)
- Sliding window (exact limits)
- Per-user and global limits

**Data Protection**
- TLS/HTTPS encryption
- Input validation
- Output sanitization
- Sensitive data masking

## Versioning

- **URL Path**: `/v1/`, `/v2/` (clearest)
- **Header**: Accept-Version header
- **Media Type**: Content-Type variation

## Documentation

- OpenAPI/Swagger specs
- ReDoc for beautiful docs
- Postman collections
- Interactive API explorers

## Monitoring

**Key Metrics**
- Request rate (RPS)
- Latency (p50, p95, p99)
- Error rates (4xx, 5xx)
- Endpoint usage patterns

**Request Tracking**
- Unique request IDs
- Distributed tracing
- Correlation across services

## Roadmaps Covered

- API Design (https://roadmap.sh/api-design)
- GraphQL (https://roadmap.sh/graphql)
