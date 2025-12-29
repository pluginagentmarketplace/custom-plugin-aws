---
name: aws-cli
description: Master AWS CLI - installation, configuration, profiles, and productivity tips
sasmp_version: "1.3.0"
bonded_agent: aws-fundamentals
bond_type: PRIMARY_BOND
---

# AWS CLI Skill

## Essential Commands

```bash
# Configuration
aws configure                    # Set default credentials
aws configure --profile prod     # Named profile
aws configure list               # Show current config

# Identity
aws sts get-caller-identity      # Who am I?
aws iam get-user                 # Current user details

# Common operations
aws s3 ls                        # List buckets
aws ec2 describe-instances       # List EC2 instances
aws lambda list-functions        # List Lambda functions
```

## Profile Management

```bash
# ~/.aws/credentials
[default]
aws_access_key_id = AKIA...
aws_secret_access_key = secret...

[prod]
aws_access_key_id = AKIA...
aws_secret_access_key = secret...

# ~/.aws/config
[default]
region = us-east-1
output = json

[profile prod]
region = eu-west-1
output = table
```

## Useful Flags

```bash
--profile NAME    # Use named profile
--region REGION   # Override region
--output json     # Output format (json|table|text)
--query 'EXPR'    # JMESPath query
--no-cli-pager    # Disable pager
--dry-run         # Test without executing
```

## JMESPath Queries

```bash
# Get instance IDs
aws ec2 describe-instances --query 'Reservations[].Instances[].InstanceId'

# Get running instances
aws ec2 describe-instances --query 'Reservations[].Instances[?State.Name==`running`]'

# Format as table
aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId,State.Name]' --output table
```

## Assets

- `aws-aliases.sh` - Productivity aliases
- `aws-profiles.template` - Profile template

## References

- `CLI_GUIDE.md` - Complete CLI reference
