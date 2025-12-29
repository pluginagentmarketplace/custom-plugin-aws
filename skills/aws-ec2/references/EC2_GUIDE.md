# EC2 Complete Guide

## Instance Types Overview

### General Purpose (t3, m6i)
- Balanced compute, memory, networking
- Burstable (t3) vs fixed performance (m6i)
- Use for: Web servers, development, small databases

### Compute Optimized (c6i, c7g)
- High-performance processors
- Use for: Batch processing, gaming, ML inference

### Memory Optimized (r6i, x2idn)
- Large memory-to-CPU ratio
- Use for: Databases, in-memory caching

### Storage Optimized (i3, d3)
- High sequential I/O
- Use for: Data warehousing, Hadoop

### Accelerated (p4, g5)
- GPU instances
- Use for: ML training, video encoding

## AMI Selection

```bash
# Latest Amazon Linux 2023
aws ec2 describe-images \
    --owners amazon \
    --filters "Name=name,Values=al2023-ami-*-x86_64" \
    --query 'sort_by(Images, &CreationDate)[-1].[ImageId,Name]' \
    --output table

# Latest Ubuntu 22.04
aws ec2 describe-images \
    --owners 099720109477 \
    --filters "Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*" \
    --query 'sort_by(Images, &CreationDate)[-1].[ImageId,Name]' \
    --output table
```

## Security Groups

### Web Server Example
```bash
# Create group
aws ec2 create-security-group \
    --group-name web-server \
    --description "Web server access" \
    --vpc-id vpc-xxx

# Allow SSH
aws ec2 authorize-security-group-ingress \
    --group-id sg-xxx \
    --protocol tcp --port 22 \
    --cidr YOUR_IP/32

# Allow HTTP/HTTPS
aws ec2 authorize-security-group-ingress \
    --group-id sg-xxx \
    --protocol tcp --port 80 --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
    --group-id sg-xxx \
    --protocol tcp --port 443 --cidr 0.0.0.0/0
```

## EBS Volumes

| Type | IOPS | Throughput | Use Case |
|------|------|------------|----------|
| gp3 | 3000-16000 | 125-1000 MB/s | General purpose |
| io2 | Up to 256000 | 4000 MB/s | Critical databases |
| st1 | 500 baseline | 500 MB/s | Streaming |
| sc1 | 250 baseline | 250 MB/s | Cold storage |

## Instance Metadata

```bash
# Inside EC2 instance
curl http://169.254.169.254/latest/meta-data/
curl http://169.254.169.254/latest/meta-data/instance-id
curl http://169.254.169.254/latest/meta-data/public-ipv4
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/
```

## Cost Optimization

1. **Right-sizing**: Use Compute Optimizer
2. **Spot Instances**: Up to 90% savings
3. **Reserved Instances**: 30-60% savings
4. **Savings Plans**: Flexible commitment
5. **Auto Scaling**: Scale based on demand
