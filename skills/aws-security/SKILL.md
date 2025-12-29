---
name: aws-security
description: Master AWS security - best practices, compliance, and security services
sasmp_version: "1.3.0"
bonded_agent: aws-iam
bond_type: SECONDARY_BOND
---

# AWS Security Skill

## Security Services

### AWS Security Hub

```bash
# Enable Security Hub
aws securityhub enable-security-hub

# Get findings
aws securityhub get-findings \
    --filters '{"SeverityLabel": [{"Value": "CRITICAL", "Comparison": "EQUALS"}]}'
```

### GuardDuty

```bash
# Enable GuardDuty
aws guardduty create-detector --enable

# List findings
aws guardduty list-findings --detector-id DETECTOR_ID
```

### AWS Config

```bash
# Create config rule
aws configservice put-config-rule --config-rule file://rule.json

# Check compliance
aws configservice get-compliance-details-by-config-rule \
    --config-rule-name required-tags
```

### AWS WAF

```bash
# Create Web ACL
aws wafv2 create-web-acl \
    --name my-web-acl \
    --scope REGIONAL \
    --default-action '{"Allow": {}}' \
    --visibility-config '{"SampledRequestsEnabled": true, "CloudWatchMetricsEnabled": true, "MetricName": "my-web-acl"}'
```

## Security Checklist

### Account Level
- [ ] Enable MFA on root account
- [ ] Remove root access keys
- [ ] Enable CloudTrail in all regions
- [ ] Enable AWS Config
- [ ] Enable GuardDuty
- [ ] Enable Security Hub

### Network Level
- [ ] Use VPC for all resources
- [ ] Use private subnets for databases
- [ ] Implement Security Groups properly
- [ ] Enable VPC Flow Logs
- [ ] Use PrivateLink for AWS services

### Data Level
- [ ] Enable encryption at rest (S3, RDS, EBS)
- [ ] Enable encryption in transit (TLS)
- [ ] Use KMS for key management
- [ ] Implement bucket policies
- [ ] Enable versioning for S3

## Assets

- `security-policies/` - IAM and resource policies
- `config-rules/` - AWS Config rules

## References

- `SECURITY_CHECKLIST.md` - Complete checklist
