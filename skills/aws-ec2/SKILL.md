---
name: aws-ec2
description: Master AWS EC2 - instances, AMIs, security groups, and compute management
sasmp_version: "1.3.0"
bonded_agent: aws-compute
bond_type: PRIMARY_BOND
---

# AWS EC2 Skill

## Instance Lifecycle

```bash
# Launch instance
aws ec2 run-instances \
    --image-id ami-0abcdef1234567890 \
    --instance-type t3.micro \
    --key-name my-key \
    --security-group-ids sg-12345678 \
    --subnet-id subnet-12345678 \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=MyServer}]'

# Start/Stop/Terminate
aws ec2 start-instances --instance-ids i-1234567890abcdef0
aws ec2 stop-instances --instance-ids i-1234567890abcdef0
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0

# Describe instances
aws ec2 describe-instances --instance-ids i-1234567890abcdef0
```

## Instance Types

| Category | Examples | Use Case |
|----------|----------|----------|
| General Purpose | t3, m6i | Web servers, dev |
| Compute Optimized | c6i, c7g | Batch, ML inference |
| Memory Optimized | r6i, x2idn | Databases, caching |
| Storage Optimized | i3, d3 | Data warehousing |
| Accelerated | p4, g5 | ML training, graphics |

## Security Groups

```bash
# Create security group
aws ec2 create-security-group \
    --group-name web-sg \
    --description "Web server security group" \
    --vpc-id vpc-12345678

# Add inbound rules
aws ec2 authorize-security-group-ingress \
    --group-id sg-12345678 \
    --protocol tcp \
    --port 443 \
    --cidr 0.0.0.0/0
```

## User Data Script

```bash
#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd
echo "Hello from EC2!" > /var/www/html/index.html
```

## Assets

- `user-data-scripts/` - Bootstrap scripts
- `security-group-templates/` - SG configurations

## References

- `EC2_GUIDE.md` - Complete EC2 reference
