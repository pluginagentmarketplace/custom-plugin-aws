---
name: backend-frameworks
description: Master Node.js, Spring Boot, ASP.NET Core, and Laravel frameworks for building scalable, production-ready backend systems.
---

# Backend Frameworks

## Quick Start

Choose a backend framework based on language preference and project requirements.

## Node.js Ecosystem

### Express.js

**Basic Setup**
```javascript
const express = require('express');
const app = express();

app.use(express.json());

app.get('/api/users/:id', async (req, res) => {
  const user = await User.findById(req.params.id);
  res.json(user);
});
```

**Middleware Pattern**
- Authentication middleware
- Error handling middleware
- Logging and monitoring
- Request validation

### Modern Node.js Alternatives

**Fastify**
- Higher performance than Express
- Strong validation with JSON Schema
- Plugin ecosystem

**Nest.js**
- TypeScript-first framework
- Dependency injection
- Decorators for routing and middleware
- Built-in validation with class-validator

## Spring Boot

### Core Concepts

**Dependency Injection**
```java
@Service
public class UserService {
  private final UserRepository repository;

  public UserService(UserRepository repository) {
    this.repository = repository;
  }
}
```

**RESTful Endpoints**
```java
@RestController
@RequestMapping("/api/users")
public class UserController {
  @GetMapping("/{id}")
  public User getUser(@PathVariable Long id) {
    return service.findById(id);
  }
}
```

**Data Access with Spring Data**
- JPA repositories for ORM
- Query methods
- Custom queries with @Query

## ASP.NET Core

### Core Concepts

**Minimal APIs**
```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/users/{id}", GetUser);

async Task<User> GetUser(int id, IUserService service)
{
    return await service.GetUserAsync(id);
}
```

**Entity Framework**
- DbContext for data access
- LINQ queries
- Migrations for schema management

## Laravel

### Core Concepts

**Routing & Controllers**
```php
Route::get('/users/{id}', [UserController::class, 'show']);

class UserController extends Controller {
  public function show($id) {
    return User::find($id);
  }
}
```

**Eloquent ORM**
```php
$user = User::with('posts')->find($id);
$user->posts()->create(['title' => '...']);
```

**Middleware & Pipelines**
- Request/response middleware
- Pipeline for request processing

## Cross-Framework Patterns

### Authentication & Authorization

**JWT (JSON Web Tokens)**
- Stateless authentication
- Token generation and validation
- Refresh tokens for security

**Session-Based**
- Server-side session storage
- Cookie-based delivery
- More traditional approach

### Database Integration

**ORM Concepts**
- Entity mapping
- Query builders
- Relationships (One-to-many, Many-to-many)
- Lazy vs eager loading

**Query Optimization**
- Database indexing
- Query analysis
- N+1 problem prevention
- Caching strategies

### Error Handling

```javascript
// Centralized error handler
app.use((err, req, res, next) => {
  const status = err.status || 500;
  const message = err.message || 'Internal Server Error';
  res.status(status).json({ error: message });
});
```

### Logging & Monitoring

- Structured logging (JSON format)
- Log levels (debug, info, warn, error)
- APM integration
- Error tracking (Sentry, etc.)

## Deployment Considerations

### Environment Management

- Environment variables for configuration
- Separate dev/staging/production configs
- Secrets management

### Performance Optimization

- Caching strategies (Redis)
- Database connection pooling
- Async operations
- Load balancing

### Scaling Patterns

- Horizontal scaling with load balancers
- Database replication
- Message queues for async work
- Microservices decomposition

## Testing

**Unit Testing**
- Test business logic in isolation
- Mock external dependencies

**Integration Testing**
- Test with real database
- Test API endpoints

**E2E Testing**
- Full workflow testing
- User perspective

## Roadmaps Covered

- Node.js (https://roadmap.sh/nodejs)
- Spring Boot (https://roadmap.sh/spring-boot)
- ASP.NET Core (https://roadmap.sh/aspnet-core)
- Laravel (https://roadmap.sh/laravel)
- Backend (https://roadmap.sh/backend)
