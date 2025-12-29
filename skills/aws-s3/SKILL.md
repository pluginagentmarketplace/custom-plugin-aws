---
name: aws-s3
description: Master AWS S3 - buckets, objects, policies, and storage management
sasmp_version: "1.3.0"
bonded_agent: aws-storage
bond_type: PRIMARY_BOND
---

# AWS S3 Skill

## Bucket Operations

```bash
# Create bucket
aws s3 mb s3://my-unique-bucket-name

# List buckets
aws s3 ls

# Delete bucket
aws s3 rb s3://my-bucket --force

# Enable versioning
aws s3api put-bucket-versioning \
    --bucket my-bucket \
    --versioning-configuration Status=Enabled
```

## Object Operations

```bash
# Upload file
aws s3 cp myfile.txt s3://my-bucket/

# Download file
aws s3 cp s3://my-bucket/myfile.txt ./

# Sync directory
aws s3 sync ./local s3://my-bucket/remote

# List objects
aws s3 ls s3://my-bucket/ --recursive

# Delete object
aws s3 rm s3://my-bucket/myfile.txt

# Generate presigned URL
aws s3 presign s3://my-bucket/myfile.txt --expires-in 3600
```

## Storage Classes

| Class | Use Case | Retrieval |
|-------|----------|-----------|
| Standard | Frequent access | Immediate |
| Standard-IA | Infrequent access | Immediate |
| One Zone-IA | Reproducible data | Immediate |
| Glacier Instant | Archive, fast retrieval | Milliseconds |
| Glacier Flexible | Archive | 1-12 hours |
| Glacier Deep | Long-term archive | 12-48 hours |

## Bucket Policy Example

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::my-bucket/*"
        }
    ]
}
```

## Static Website Hosting

```bash
# Enable website hosting
aws s3 website s3://my-bucket \
    --index-document index.html \
    --error-document error.html
```

## Assets

- `bucket-policies/` - Policy templates
- `lifecycle-rules/` - Lifecycle configurations

## References

- `S3_BEST_PRACTICES.md` - Storage optimization
