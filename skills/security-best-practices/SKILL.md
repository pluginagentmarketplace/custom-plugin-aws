---
name: security-best-practices
description: Master cybersecurity, secure coding, authentication, encryption, and security best practices for protecting systems and data.
---

# Security Best Practices

## Quick Start

Build secure applications and infrastructure from the ground up.

## Cybersecurity Fundamentals

### Security Triad

**Confidentiality** - Only authorized access
- Encryption
- Access control
- Data classification

**Integrity** - Data not modified
- Hash verification
- Digital signatures
- Audit logs

**Availability** - System operational
- Redundancy
- DDoS protection
- Backup strategies

## Secure Coding

### Input Validation

**Never Trust User Input**
```python
# Bad: SQL Injection
query = f"SELECT * FROM users WHERE id = {user_id}"

# Good: Parameterized query
query = "SELECT * FROM users WHERE id = ?"
execute(query, (user_id,))
```

**Validation Rules**
- Type checking
- Length limits
- Pattern matching
- Whitelist approach

### Output Encoding

**XSS Prevention**
```python
# Bad: Direct output
return f"<div>{user_input}</div>"

# Good: Escaped output
return f"<div>{escape(user_input)}</div>"
```

### OWASP Top 10

1. **Injection** - SQL, command, NoSQL
2. **Broken Authentication** - Weak credentials
3. **Sensitive Data Exposure** - Unencrypted data
4. **XML External Entities (XXE)**
5. **Broken Access Control**
6. **Security Misconfiguration**
7. **XSS** - Cross-site scripting
8. **Insecure Deserialization**
9. **Using Components with Known Vulnerabilities**
10. **Insufficient Logging & Monitoring**

## Authentication & Authorization

### Authentication Methods

**Passwords** - Something you know
- Use strong hashing (bcrypt, Argon2)
- No plaintext storage
- MFA/2FA for defense

**Multi-Factor Authentication (MFA)**
- Something you have (phone, hardware key)
- Something you are (biometric)

**OAuth 2.0 / OpenID Connect**
- Industry standard
- 3rd party authentication
- Delegation of authority

### Authorization (Access Control)

**Role-Based Access Control (RBAC)**
- Users have roles
- Roles have permissions
- Principle of least privilege

**Attribute-Based Access Control (ABAC)**
- Fine-grained control
- Based on attributes
- More flexible

## Encryption

### Encryption in Transit

**TLS/SSL**
- HTTPS for web
- TLS 1.2 or later
- Strong cipher suites
- Certificate management

### Encryption at Rest

**Data Encryption**
- Database encryption
- File system encryption
- Key management service

**Key Management**
- Key rotation
- Secure storage
- Access control
- Audit logging

## Network Security

### Firewalls & Network Segmentation

**Firewall Rules**
- Whitelist approach
- Minimum ports/protocols
- Regular audits

**Network Segmentation**
- VPCs/Subnets
- Security groups
- NACLs (Network ACLs)

### DDoS Protection

**Rate Limiting** - Block excessive requests
**WAF** - Web Application Firewall
**CDN** - Edge protection
**IDS/IPS** - Intrusion detection/prevention

## API Security

**API Keys**
- Generate securely
- Rotate regularly
- Scope permissions

**Rate Limiting**
- Per user/IP
- Graceful degradation

**CORS** - Control cross-origin requests

## Vulnerability Management

**Dependency Scanning**
```
npm audit
pip safety check
```

**Regular Patching**
- Security updates priority
- Automated patching where possible
- Test before production

## Incident Response

**Preparation**
- Incident response plan
- Team training
- Tools ready

**Response Process**
1. Detect
2. Assess
3. Contain
4. Remediate
5. Recover
6. Review

## Compliance

**Standards**
- GDPR (EU data protection)
- HIPAA (healthcare)
- PCI-DSS (payment cards)
- SOC 2 (service organizations)

## Roadmaps Covered

- Cyber Security (https://roadmap.sh/cyber-security)
- API Security (https://roadmap.sh/best-practices/api-security)
