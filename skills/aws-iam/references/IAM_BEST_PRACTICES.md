# IAM Best Practices

## 1. Root Account Protection

- **Enable MFA** on root account immediately
- **Never use root** for daily operations
- **Delete root access keys** if they exist
- **Use AWS Organizations** for multi-account

## 2. Least Privilege Principle

```json
// ❌ Too permissive
{
    "Effect": "Allow",
    "Action": "s3:*",
    "Resource": "*"
}

// ✅ Least privilege
{
    "Effect": "Allow",
    "Action": [
        "s3:GetObject",
        "s3:ListBucket"
    ],
    "Resource": [
        "arn:aws:s3:::my-bucket",
        "arn:aws:s3:::my-bucket/*"
    ]
}
```

## 3. Use Roles Instead of Access Keys

- **EC2 instances**: Use instance profiles
- **Lambda functions**: Use execution roles
- **Cross-account**: Use assume role
- **External apps**: Use IAM Identity Center

## 4. Policy Types

| Type | Use Case |
|------|----------|
| AWS Managed | Quick start, standard permissions |
| Customer Managed | Custom, reusable policies |
| Inline | One-off, tightly coupled |

## 5. Conditions

```json
{
    "Condition": {
        "IpAddress": {"aws:SourceIp": "10.0.0.0/8"},
        "Bool": {"aws:MultiFactorAuthPresent": "true"},
        "DateGreaterThan": {"aws:CurrentTime": "2024-01-01T00:00:00Z"},
        "StringEquals": {"aws:RequestedRegion": "us-east-1"}
    }
}
```

## 6. Access Analyzer

Enable IAM Access Analyzer to:
- Identify resources shared externally
- Validate policies against best practices
- Generate least-privilege policies

## 7. Credential Rotation

- Rotate access keys every 90 days
- Use AWS Secrets Manager for automation
- Monitor with CloudTrail

## 8. Permission Boundaries

Use permission boundaries to:
- Delegate admin tasks safely
- Limit maximum permissions
- Prevent privilege escalation
