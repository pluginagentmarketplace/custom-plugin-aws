# Backend Frameworks Guide

## Framework Comparison

| Framework | Language | Async | Use Case |
|-----------|----------|-------|----------|
| FastAPI | Python | Yes | APIs, ML |
| Express | Node.js | Yes | General |
| Django | Python | Partial | Full-stack |
| Spring Boot | Java | Yes | Enterprise |
| Go Gin | Go | Yes | High-perf |

## FastAPI Patterns

### Dependency Injection
```python
async def get_db():
    async with AsyncSession() as session:
        yield session

@app.get("/users")
async def list_users(db: AsyncSession = Depends(get_db)):
    return await crud.get_users(db)
```

### Repository Pattern
```python
class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: UUID) -> User:
        return await self.db.get(User, id)
```

## Express.js Patterns

### Middleware Chain
```javascript
app.use(cors());
app.use(express.json());
app.use(authenticate);
app.use('/api', routes);
app.use(errorHandler);
```

## Best Practices

1. **Layered Architecture**: Controller → Service → Repository
2. **Validation**: Validate at API boundary
3. **Error Handling**: Consistent error responses
4. **Logging**: Structured logging
5. **Health Checks**: /health and /ready endpoints
