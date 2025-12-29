# S3 Best Practices

## Naming Conventions

```
# Good bucket names
my-company-production-assets
app-logs-2024
backup-us-east-1-12345678

# Avoid
MyBucket (no uppercase)
my.bucket.com (dots cause SSL issues)
```

## Security Best Practices

### 1. Block Public Access (Default)
```bash
aws s3api put-public-access-block \
    --bucket my-bucket \
    --public-access-block-configuration \
    "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

### 2. Enable Encryption
```bash
aws s3api put-bucket-encryption \
    --bucket my-bucket \
    --server-side-encryption-configuration \
    '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"aws:kms"}}]}'
```

### 3. Enable Versioning
```bash
aws s3api put-bucket-versioning \
    --bucket my-bucket \
    --versioning-configuration Status=Enabled
```

### 4. Enable Access Logging
```bash
aws s3api put-bucket-logging \
    --bucket my-bucket \
    --bucket-logging-status \
    '{"LoggingEnabled":{"TargetBucket":"my-logs-bucket","TargetPrefix":"s3-access-logs/"}}'
```

## Cost Optimization

### Lifecycle Policies
- Transition to IA after 30 days
- Transition to Glacier after 90 days
- Delete old versions after 365 days
- Abort incomplete multipart uploads

### Intelligent-Tiering
```bash
# For unknown access patterns
aws s3api put-bucket-intelligent-tiering-configuration \
    --bucket my-bucket \
    --id entire-bucket \
    --intelligent-tiering-configuration \
    '{"Id":"entire-bucket","Status":"Enabled","Tierings":[{"Days":90,"AccessTier":"ARCHIVE_ACCESS"},{"Days":180,"AccessTier":"DEEP_ARCHIVE_ACCESS"}]}'
```

## Performance

### Multipart Upload (files > 100MB)
```bash
aws s3 cp large-file.zip s3://my-bucket/ \
    --expected-size 5368709120 \
    --storage-class STANDARD
```

### S3 Transfer Acceleration
```bash
aws s3api put-bucket-accelerate-configuration \
    --bucket my-bucket \
    --accelerate-configuration Status=Enabled
```

## Replication

### Cross-Region Replication
- Disaster recovery
- Latency reduction
- Compliance requirements

### Same-Region Replication
- Log aggregation
- Data sharing between accounts
