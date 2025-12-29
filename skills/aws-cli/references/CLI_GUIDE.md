# AWS CLI Complete Guide

## Installation

### macOS
```bash
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
```

### Linux
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

### Windows
Download and run the MSI installer from AWS.

## Configuration

### Default Configuration
```bash
aws configure
# AWS Access Key ID: AKIA...
# AWS Secret Access Key: ...
# Default region name: us-east-1
# Default output format: json
```

### Named Profiles
```bash
aws configure --profile production
aws configure --profile staging
```

### Configuration Files

**~/.aws/credentials**
```ini
[default]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

[production]
aws_access_key_id = AKIAI44QH8DHBEXAMPLE
aws_secret_access_key = je7MtGbClwBF/2Zp9Utk/h3yCo8nvbEXAMPLEKEY
```

**~/.aws/config**
```ini
[default]
region = us-east-1
output = json

[profile production]
region = eu-west-1
output = table
role_arn = arn:aws:iam::123456789012:role/AdminRole
source_profile = default
```

## Common Commands

### EC2
```bash
# List instances
aws ec2 describe-instances

# Start/stop instance
aws ec2 start-instances --instance-ids i-1234567890abcdef0
aws ec2 stop-instances --instance-ids i-1234567890abcdef0

# Create security group
aws ec2 create-security-group --group-name MySecurityGroup --description "My security group"
```

### S3
```bash
# List buckets
aws s3 ls

# Copy file
aws s3 cp myfile.txt s3://mybucket/

# Sync directory
aws s3 sync ./local s3://mybucket/remote

# Presigned URL
aws s3 presign s3://mybucket/myfile.txt --expires-in 3600
```

### Lambda
```bash
# List functions
aws lambda list-functions

# Invoke function
aws lambda invoke --function-name MyFunction output.json

# Update code
aws lambda update-function-code --function-name MyFunction --zip-file fileb://function.zip
```

### CloudFormation
```bash
# Deploy stack
aws cloudformation deploy --template-file template.yaml --stack-name MyStack

# Delete stack
aws cloudformation delete-stack --stack-name MyStack

# List stacks
aws cloudformation list-stacks
```

## JMESPath Queries

```bash
# Filter by tag
aws ec2 describe-instances --query 'Reservations[].Instances[?Tags[?Key==`Environment` && Value==`Production`]]'

# Select specific fields
aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId,State.Name]'

# First item
aws ec2 describe-instances --query 'Reservations[0].Instances[0].InstanceId'

# Count
aws ec2 describe-instances --query 'length(Reservations[].Instances[])'
```

## Environment Variables

```bash
export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
export AWS_DEFAULT_REGION=us-east-1
export AWS_PROFILE=production
```

## Best Practices

1. **Use named profiles** for different environments
2. **Never hardcode credentials** in scripts
3. **Use IAM roles** on EC2 instead of access keys
4. **Enable MFA** for CLI access
5. **Rotate access keys** regularly
6. **Use --dry-run** to test commands safely
