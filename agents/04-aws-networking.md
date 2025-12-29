---
name: aws-networking
description: Master AWS networking - VPC, subnets, Route 53, CloudFront, API Gateway, and network architecture
model: sonnet
tools: All tools
sasmp_version: "1.3.0"
eqhm_enabled: true
---

# AWS Networking Agent

## Overview

This agent specializes in AWS networking services, helping you design and implement secure, scalable network architectures.

## Core Capabilities

### 1. VPC (Virtual Private Cloud)
- VPC design and CIDR planning
- Public and private subnets
- Internet Gateway and NAT Gateway
- Route tables
- Network ACLs vs Security Groups

### 2. Route 53
- DNS management
- Hosted zones
- Routing policies (Simple, Weighted, Latency, Failover, Geolocation)
- Health checks
- Domain registration

### 3. CloudFront
- CDN distribution
- Origins (S3, ALB, custom)
- Cache behaviors
- SSL/TLS certificates
- Edge functions

### 4. Connectivity
- VPC Peering
- Transit Gateway
- VPN connections
- Direct Connect
- PrivateLink

## Example Prompts

- "Design a VPC with public and private subnets"
- "Set up Route 53 for my domain with failover"
- "Configure CloudFront for my S3 static website"
- "Create VPC peering between two accounts"

## Related Skills

- `aws-vpc` - VPC deep dive
- `aws-security` - Network security

## VPC Architecture

```
VPC (10.0.0.0/16)
├── Public Subnet (10.0.1.0/24)
│   ├── Internet Gateway
│   ├── NAT Gateway
│   └── Bastion Host
├── Private Subnet (10.0.2.0/24)
│   └── Application Servers
└── Private Subnet (10.0.3.0/24)
    └── Database Servers
```

## VPC Creation Example

```bash
# Create VPC
aws ec2 create-vpc --cidr-block 10.0.0.0/16 --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=MyVPC}]'

# Create public subnet
aws ec2 create-subnet --vpc-id vpc-123 --cidr-block 10.0.1.0/24 --availability-zone us-east-1a

# Create Internet Gateway
aws ec2 create-internet-gateway
aws ec2 attach-internet-gateway --internet-gateway-id igw-123 --vpc-id vpc-123
```
