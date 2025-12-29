# REST API Design Guide

Best practices for designing RESTful APIs.

## HTTP Methods

| Method | Purpose | Idempotent | Safe |
|--------|---------|------------|------|
| GET | Retrieve resource | Yes | Yes |
| POST | Create resource | No | No |
| PUT | Replace resource | Yes | No |
| PATCH | Update resource | No | No |
| DELETE | Remove resource | Yes | No |

## URL Design

```
# Resources (nouns, plural)
GET    /users           # List users
POST   /users           # Create user
GET    /users/{id}      # Get user
PUT    /users/{id}      # Replace user
PATCH  /users/{id}      # Update user
DELETE /users/{id}      # Delete user

# Nested resources
GET    /users/{id}/orders
POST   /users/{id}/orders

# Filtering, sorting, pagination
GET    /users?status=active&sort=-createdAt&page=2&limit=20
```

## Status Codes

| Code | Meaning | Use When |
|------|---------|----------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid request |
| 401 | Unauthorized | Missing auth |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Resource conflict |
| 422 | Unprocessable | Validation failed |
| 429 | Too Many Requests | Rate limited |
| 500 | Internal Error | Server error |

## Response Format

```json
// Success (single resource)
{
  "data": {
    "id": "123",
    "type": "user",
    "attributes": {
      "email": "user@example.com"
    }
  }
}

// Success (collection)
{
  "data": [...],
  "meta": {
    "total": 100,
    "page": 1,
    "limit": 20
  },
  "links": {
    "self": "/users?page=1",
    "next": "/users?page=2"
  }
}

// Error
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": [
      {"field": "email", "message": "Must be valid email"}
    ]
  }
}
```

## Versioning Strategies

| Strategy | Example | Pros | Cons |
|----------|---------|------|------|
| URL path | /v1/users | Clear, easy | Breaks caching |
| Header | Accept: application/vnd.api.v1+json | Clean URLs | Hidden |
| Query | /users?version=1 | Easy to use | URL pollution |

## Pagination Patterns

### Offset-based

```
GET /users?page=2&limit=20
```

**Pros:** Simple, random access
**Cons:** Inconsistent with data changes

### Cursor-based

```
GET /users?cursor=eyJpZCI6MTAwfQ&limit=20
```

**Pros:** Consistent, efficient
**Cons:** No random access

## Authentication

### JWT in Header

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### API Key

```
X-API-Key: your-api-key-here
```

## Rate Limiting Headers

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
Retry-After: 60
```

## HATEOAS

```json
{
  "id": "123",
  "name": "Order",
  "_links": {
    "self": {"href": "/orders/123"},
    "customer": {"href": "/customers/456"},
    "cancel": {"href": "/orders/123/cancel", "method": "POST"}
  }
}
```

## API Design Checklist

- [ ] Use nouns for resources
- [ ] Plural resource names
- [ ] Consistent naming convention
- [ ] Proper HTTP methods
- [ ] Correct status codes
- [ ] Pagination for lists
- [ ] Filtering and sorting
- [ ] Error responses with details
- [ ] Rate limiting
- [ ] Versioning strategy
- [ ] Authentication
- [ ] HTTPS only
- [ ] Documentation (OpenAPI)
