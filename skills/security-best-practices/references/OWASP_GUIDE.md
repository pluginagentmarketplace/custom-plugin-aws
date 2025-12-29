# OWASP Security Guide

Comprehensive security reference based on OWASP standards.

## OWASP Top 10 (2021)

### A01: Broken Access Control

**Description:** Restrictions on what authenticated users can do are not properly enforced.

**Prevention:**
```python
# BAD - Direct object reference
@app.get("/user/{user_id}")
def get_user(user_id: int):
    return db.get_user(user_id)  # Anyone can access any user!

# GOOD - Verify ownership
@app.get("/user/{user_id}")
def get_user(user_id: int, current_user: User = Depends(get_current_user)):
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(403, "Access denied")
    return db.get_user(user_id)
```

### A02: Cryptographic Failures

**Prevention:**
- Use TLS 1.3 for data in transit
- Use AES-256-GCM for data at rest
- Never store passwords in plain text
- Use proper key management (KMS, Vault)

```python
# Password hashing
from argon2 import PasswordHasher

ph = PasswordHasher()
hashed = ph.hash(password)
ph.verify(hashed, password)  # Returns True or raises exception
```

### A03: Injection

**Types:** SQL, NoSQL, OS Command, LDAP, XPath

```python
# BAD - SQL Injection
query = f"SELECT * FROM users WHERE id = {user_id}"

# GOOD - Parameterized query
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))

# GOOD - ORM
user = session.query(User).filter(User.id == user_id).first()
```

### A04: Insecure Design

**Prevention:**
- Threat modeling during design
- Secure design patterns
- Security requirements in user stories
- Defense in depth

### A05: Security Misconfiguration

**Checklist:**
- [ ] Remove default credentials
- [ ] Disable unnecessary features
- [ ] Update all components
- [ ] Proper error handling (no stack traces)
- [ ] Security headers configured

```nginx
# Nginx security headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Content-Security-Policy "default-src 'self'" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

### A06: Vulnerable Components

**Prevention:**
```bash
# Python - Check for vulnerabilities
pip install safety
safety check

# JavaScript - Check for vulnerabilities
npm audit
npm audit fix

# Container scanning
docker scout cves myimage:tag
trivy image myimage:tag
```

### A07: Authentication Failures

**Best Practices:**
- Multi-factor authentication
- Rate limiting on login attempts
- Secure password reset flow
- Session management

```python
# Rate limiting example
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/login")
@limiter.limit("5/minute")
def login(credentials: LoginRequest):
    # Authentication logic
    pass
```

### A08: Software & Data Integrity Failures

**Prevention:**
- Verify digital signatures
- Use integrity checks (checksums, SRI)
- Secure CI/CD pipelines

```html
<!-- Subresource Integrity -->
<script src="https://cdn.example.com/lib.js"
        integrity="sha384-oqVuAfXRKap7fdgcCY5uykM6+R9GqQ8K/uxy9rx7HNQlGYl1kPzQho1wx4JwY8wC"
        crossorigin="anonymous"></script>
```

### A09: Security Logging & Monitoring

**What to Log:**
- Authentication events (success/failure)
- Authorization failures
- Input validation failures
- Server-side errors
- High-value transactions

```python
import logging
from structlog import get_logger

logger = get_logger()

def login(username: str, password: str, request: Request):
    if authenticate(username, password):
        logger.info("login_success",
                   username=username,
                   ip=request.client.host,
                   user_agent=request.headers.get("User-Agent"))
    else:
        logger.warning("login_failure",
                      username=username,
                      ip=request.client.host,
                      reason="invalid_credentials")
```

### A10: Server-Side Request Forgery (SSRF)

**Prevention:**
```python
# BAD - User-controlled URL
@app.get("/fetch")
def fetch_url(url: str):
    return requests.get(url).content  # SSRF vulnerability!

# GOOD - Validate and restrict URLs
ALLOWED_DOMAINS = ["api.example.com", "cdn.example.com"]

def is_allowed_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.hostname in ALLOWED_DOMAINS

@app.get("/fetch")
def fetch_url(url: str):
    if not is_allowed_url(url):
        raise HTTPException(400, "URL not allowed")
    return requests.get(url).content
```

## Security Headers Quick Reference

| Header | Value | Purpose |
|--------|-------|---------|
| Content-Security-Policy | `default-src 'self'` | Prevent XSS |
| X-Frame-Options | `DENY` | Prevent clickjacking |
| X-Content-Type-Options | `nosniff` | Prevent MIME sniffing |
| Strict-Transport-Security | `max-age=31536000` | Force HTTPS |
| Referrer-Policy | `strict-origin-when-cross-origin` | Control referrer |
| Permissions-Policy | `geolocation=(), camera=()` | Feature control |

## JWT Security

```python
# Secure JWT configuration
import jwt
from datetime import datetime, timedelta

SECRET_KEY = os.environ["JWT_SECRET"]  # Never hardcode!
ALGORITHM = "RS256"  # Prefer RS256 over HS256

def create_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=1),
        "jti": str(uuid.uuid4())  # Unique token ID
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
```

## API Security Checklist

- [ ] Authentication on all endpoints
- [ ] Authorization checks
- [ ] Input validation
- [ ] Rate limiting
- [ ] HTTPS only
- [ ] CORS properly configured
- [ ] No sensitive data in URLs
- [ ] Proper error handling
- [ ] Security headers
- [ ] Audit logging
