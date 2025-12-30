---
name: aws_check
description: Verify AWS CLI configuration, credentials, and service connectivity
allowed-tools: Bash, Read
sasmp_version: "1.3.0"
---

# AWS Check Command

Comprehensive AWS environment verification and health check.

## Command Specification

| Attribute | Value |
|-----------|-------|
| Command | `/aws-check` |
| Category | Diagnostics |
| Exit Codes | 0=Success, 1=CLI Error, 2=Auth Error, 3=Network Error |
| Timeout | 30 seconds |

## Usage

```bash
/aws-check                    # Full environment check
/aws-check --profile <name>   # Check specific profile
/aws-check --service <svc>    # Check specific service connectivity
/aws-check --quick            # Fast check (identity only)
/aws-check --verbose          # Detailed output with timing
```

## Input Validation

| Parameter | Type | Validation | Default |
|-----------|------|------------|---------|
| --profile | string | ^[a-zA-Z0-9_-]{1,64}$ | default |
| --service | string | ec2, s3, iam, sts, lambda | all |
| --region | string | ^[a-z]{2}-[a-z]+-[0-9]$ | from config |
| --timeout | int | 5-120 seconds | 30 |

## Verification Steps

### 1. CLI Installation Check
```bash
# Check AWS CLI version
aws --version
# Expected: aws-cli/2.x.x Python/3.x.x ...
```

### 2. Credential Verification
```bash
# Verify identity
aws sts get-caller-identity --output json
# Returns: UserId, Account, Arn
```

### 3. Configuration Check
```bash
# Check configured region
aws configure get region
# Check configured output format
aws configure get output
```

### 4. Service Connectivity Tests
```bash
# Test S3 connectivity
aws s3 ls --max-items 1

# Test EC2 connectivity
aws ec2 describe-regions --region-names us-east-1

# Test IAM connectivity
aws iam get-user 2>/dev/null || aws iam list-roles --max-items 1
```

## Output Format

### Success Output
```json
{
  "status": "healthy",
  "timestamp": "2025-01-15T10:30:00Z",
  "checks": {
    "cli_version": {"status": "pass", "value": "2.15.0"},
    "identity": {"status": "pass", "value": "arn:aws:iam::123456789012:user/admin"},
    "region": {"status": "pass", "value": "us-east-1"},
    "s3": {"status": "pass", "latency_ms": 150},
    "ec2": {"status": "pass", "latency_ms": 200},
    "iam": {"status": "pass", "latency_ms": 180}
  }
}
```

### Error Output
```json
{
  "status": "unhealthy",
  "error_code": 2,
  "error_type": "AuthenticationError",
  "message": "Unable to locate credentials",
  "resolution": "Run 'aws configure' or set AWS_ACCESS_KEY_ID environment variable"
}
```

## Exit Codes

| Code | Meaning | Common Cause |
|------|---------|--------------|
| 0 | All checks passed | Environment healthy |
| 1 | CLI not installed/misconfigured | AWS CLI not in PATH |
| 2 | Authentication failure | Invalid/expired credentials |
| 3 | Network connectivity error | Firewall/proxy issues |
| 4 | Service-specific error | IAM permission denied |
| 5 | Timeout exceeded | Slow network/endpoint |

## Troubleshooting

### Decision Tree
```
Check Failed?
├── CLI Error (Exit 1)
│   ├── "command not found" → Install AWS CLI v2
│   └── "Python error" → Reinstall CLI
├── Auth Error (Exit 2)
│   ├── "Unable to locate credentials"
│   │   ├── Using IAM User → aws configure
│   │   ├── Using IAM Role → Check instance profile
│   │   └── Using SSO → aws sso login
│   ├── "ExpiredToken" → Refresh credentials
│   └── "InvalidClientTokenId" → Regenerate access keys
├── Network Error (Exit 3)
│   ├── "Could not connect" → Check internet/proxy
│   └── "Connection timed out" → Check firewall rules
└── Permission Error (Exit 4)
    └── "AccessDenied" → Check IAM policies
```

### Common Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| "command not found" | CLI not installed | `curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"` |
| "Unable to locate credentials" | No credentials configured | `aws configure` or set env vars |
| "ExpiredToken" | Session token expired | `aws sso login` or refresh credentials |
| "InvalidClientTokenId" | Access key revoked | Generate new access keys in IAM |
| "SignatureDoesNotMatch" | Clock skew | Sync system time with NTP |
| "Connection timed out" | Network/firewall issue | Check proxy settings, VPN |

### Debug Checklist

- [ ] AWS CLI v2 installed? (`aws --version`)
- [ ] Credentials file exists? (`~/.aws/credentials`)
- [ ] Config file valid? (`~/.aws/config`)
- [ ] Environment variables set? (`AWS_ACCESS_KEY_ID`)
- [ ] Instance profile attached? (for EC2)
- [ ] SSO session valid? (`aws sso login`)
- [ ] Network allows HTTPS to AWS? (port 443)
- [ ] System clock synchronized?

## Implementation

```bash
#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

check_cli() {
    if ! command -v aws &> /dev/null; then
        echo -e "${RED}✗ AWS CLI not installed${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ AWS CLI $(aws --version | cut -d' ' -f1 | cut -d'/' -f2)${NC}"
}

check_identity() {
    if ! identity=$(aws sts get-caller-identity 2>&1); then
        echo -e "${RED}✗ Authentication failed: $identity${NC}"
        exit 2
    fi
    echo -e "${GREEN}✓ Authenticated as: $(echo $identity | jq -r '.Arn')${NC}"
}

check_region() {
    region=$(aws configure get region)
    if [ -z "$region" ]; then
        echo -e "${YELLOW}⚠ No default region configured${NC}"
    else
        echo -e "${GREEN}✓ Region: $region${NC}"
    fi
}

check_service() {
    local service=$1
    local start=$(date +%s%N)

    case $service in
        s3)  aws s3 ls --max-items 1 &>/dev/null ;;
        ec2) aws ec2 describe-regions --region-names us-east-1 &>/dev/null ;;
        iam) aws iam list-roles --max-items 1 &>/dev/null ;;
    esac

    local end=$(date +%s%N)
    local latency=$(( (end - start) / 1000000 ))
    echo -e "${GREEN}✓ $service connectivity: ${latency}ms${NC}"
}

# Run checks
check_cli
check_identity
check_region
check_service s3
check_service ec2
check_service iam

echo -e "\n${GREEN}All checks passed!${NC}"
exit 0
```

## Related Commands

- `/aws-debug` - Diagnose specific AWS issues
- `/aws-costs` - Check account costs
- `/aws-deploy` - Deploy applications

## References

- [AWS CLI Configuration](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)
- [Credential Providers](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)
