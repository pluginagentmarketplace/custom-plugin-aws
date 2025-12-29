---
description: Check AWS CLI configuration and connectivity
allowed-tools: Bash, Read
---

# AWS Check Command

Verify AWS CLI is properly configured and can connect to AWS services.

## What This Command Does

1. Checks if AWS CLI is installed
2. Verifies credentials are configured
3. Tests connectivity to AWS
4. Shows current identity and region

## Usage

```
/aws-check
```

## Expected Output

- AWS CLI version
- Current IAM identity (user/role ARN)
- Default region
- Account ID

## Troubleshooting

If the check fails:
1. Run `aws configure` to set up credentials
2. Ensure access keys are valid
3. Check internet connectivity
4. Verify IAM permissions
