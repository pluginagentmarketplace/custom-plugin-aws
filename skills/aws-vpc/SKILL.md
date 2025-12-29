---
name: aws-vpc
description: Master AWS VPC - networking, subnets, route tables, and network architecture
sasmp_version: "1.3.0"
bonded_agent: aws-networking
bond_type: PRIMARY_BOND
---

# AWS VPC Skill

## VPC Architecture

```
VPC (10.0.0.0/16)
├── Public Subnet AZ-a (10.0.1.0/24)
│   └── Internet Gateway → Route Table
├── Public Subnet AZ-b (10.0.2.0/24)
│   └── NAT Gateway
├── Private Subnet AZ-a (10.0.10.0/24)
│   └── Application Servers
├── Private Subnet AZ-b (10.0.11.0/24)
│   └── Application Servers
└── Private Subnet AZ-a (10.0.20.0/24)
    └── Database Servers
```

## Create VPC

```bash
# Create VPC
VPC_ID=$(aws ec2 create-vpc \
    --cidr-block 10.0.0.0/16 \
    --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=MyVPC}]' \
    --query 'Vpc.VpcId' --output text)

# Enable DNS hostnames
aws ec2 modify-vpc-attribute --vpc-id $VPC_ID --enable-dns-hostnames

# Create Internet Gateway
IGW_ID=$(aws ec2 create-internet-gateway \
    --query 'InternetGateway.InternetGatewayId' --output text)
aws ec2 attach-internet-gateway --internet-gateway-id $IGW_ID --vpc-id $VPC_ID

# Create public subnet
PUBLIC_SUBNET=$(aws ec2 create-subnet \
    --vpc-id $VPC_ID \
    --cidr-block 10.0.1.0/24 \
    --availability-zone us-east-1a \
    --query 'Subnet.SubnetId' --output text)
```

## Route Tables

```bash
# Create route table
RTB_ID=$(aws ec2 create-route-table \
    --vpc-id $VPC_ID \
    --query 'RouteTable.RouteTableId' --output text)

# Add route to Internet Gateway
aws ec2 create-route \
    --route-table-id $RTB_ID \
    --destination-cidr-block 0.0.0.0/0 \
    --gateway-id $IGW_ID

# Associate with subnet
aws ec2 associate-route-table \
    --route-table-id $RTB_ID \
    --subnet-id $PUBLIC_SUBNET
```

## Security Groups vs NACLs

| Feature | Security Groups | NACLs |
|---------|----------------|-------|
| Level | Instance | Subnet |
| Rules | Allow only | Allow & Deny |
| State | Stateful | Stateless |
| Evaluation | All rules | Order matters |

## Assets

- `vpc-templates/` - CloudFormation templates
- `cidr-calculator.py` - CIDR planning tool

## References

- `VPC_ARCHITECTURE.md` - Design patterns
