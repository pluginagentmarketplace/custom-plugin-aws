# AWS Security Checklist

## 🔴 Critical (Do First)

### Account Security
- [ ] Enable MFA on root account
- [ ] Delete root account access keys
- [ ] Create IAM admin user
- [ ] Enable CloudTrail in all regions
- [ ] Configure IAM password policy

### Data Protection
- [ ] Enable S3 default encryption
- [ ] Block S3 public access (account level)
- [ ] Enable EBS default encryption
- [ ] Enable RDS encryption

## 🟠 High Priority

### IAM
- [ ] Enforce MFA for all users
- [ ] Review IAM policies (least privilege)
- [ ] Enable IAM Access Analyzer
- [ ] Set up credential rotation
- [ ] Remove unused IAM users/roles

### Network
- [ ] Use VPC for all resources
- [ ] Configure security groups properly
- [ ] Enable VPC Flow Logs
- [ ] Use private subnets for databases
- [ ] Implement WAF for public endpoints

### Monitoring
- [ ] Enable GuardDuty
- [ ] Enable Security Hub
- [ ] Enable AWS Config
- [ ] Set up CloudWatch alarms
- [ ] Configure SNS notifications

## 🟡 Medium Priority

### Encryption
- [ ] Use KMS for key management
- [ ] Enable encryption in transit
- [ ] Implement secrets rotation
- [ ] Use ACM for SSL certificates

### Compliance
- [ ] Enable AWS Config rules
- [ ] Set up compliance dashboard
- [ ] Document security controls
- [ ] Regular access reviews

### Backup & Recovery
- [ ] Enable automated backups
- [ ] Test disaster recovery
- [ ] Document recovery procedures
- [ ] Cross-region backup strategy

## 🟢 Maintenance

### Regular Tasks
- [ ] Weekly: Review GuardDuty findings
- [ ] Monthly: Review IAM permissions
- [ ] Quarterly: Rotate access keys
- [ ] Annually: Security assessment

### Automation
- [ ] Automated security scanning
- [ ] Infrastructure as Code reviews
- [ ] Compliance automation
- [ ] Incident response automation

## Quick Remediation Commands

### Enable S3 Public Access Block
```bash
aws s3control put-public-access-block \
    --account-id ACCOUNT_ID \
    --public-access-block-configuration \
    "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

### Enable EBS Encryption Default
```bash
aws ec2 enable-ebs-encryption-by-default
```

### Enable IAM Access Analyzer
```bash
aws accessanalyzer create-analyzer \
    --analyzer-name account-analyzer \
    --type ACCOUNT
```

### Password Policy
```bash
aws iam update-account-password-policy \
    --minimum-password-length 14 \
    --require-symbols \
    --require-numbers \
    --require-uppercase-characters \
    --require-lowercase-characters \
    --max-password-age 90 \
    --password-reuse-prevention 24
```
