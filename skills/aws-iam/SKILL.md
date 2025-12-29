---
name: aws-iam
description: Master AWS IAM - policies, roles, users, groups, and security best practices
sasmp_version: "1.3.0"
bonded_agent: aws-iam
bond_type: PRIMARY_BOND
---

# AWS IAM Skill

## Policy Structure

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowS3Read",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::my-bucket",
                "arn:aws:s3:::my-bucket/*"
            ],
            "Condition": {
                "IpAddress": {
                    "aws:SourceIp": "192.168.1.0/24"
                }
            }
        }
    ]
}
```

## Common Actions

```bash
# Users
aws iam create-user --user-name developer
aws iam attach-user-policy --user-name developer --policy-arn arn:aws:iam::aws:policy/ReadOnlyAccess
aws iam create-access-key --user-name developer

# Roles
aws iam create-role --role-name MyRole --assume-role-policy-document file://trust-policy.json
aws iam attach-role-policy --role-name MyRole --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

# Groups
aws iam create-group --group-name Developers
aws iam add-user-to-group --group-name Developers --user-name developer

# Policies
aws iam create-policy --policy-name MyPolicy --policy-document file://policy.json
aws iam list-policies --scope Local
```

## Trust Policy Example

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "ec2.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

## Security Checklist

- [ ] Root user MFA enabled
- [ ] No root access keys
- [ ] Password policy configured
- [ ] Least privilege principle applied
- [ ] Access Analyzer enabled
- [ ] Credential rotation scheduled

## Assets

- `trust-policies/` - Common trust policy templates
- `iam-policies/` - Policy templates

## References

- `IAM_BEST_PRACTICES.md` - Security guidelines
