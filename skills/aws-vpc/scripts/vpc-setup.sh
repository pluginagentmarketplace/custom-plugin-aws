#!/bin/bash
# VPC Quick Setup Script

set -e

echo "🌐 AWS VPC Quick Setup"
echo "======================"

# Configuration
VPC_CIDR="10.0.0.0/16"
PUBLIC_SUBNET_CIDR="10.0.1.0/24"
PRIVATE_SUBNET_CIDR="10.0.10.0/24"
REGION=$(aws configure get region)
AZ="${REGION}a"
NAME_PREFIX="my-vpc"

echo "Creating VPC in $REGION..."

# Create VPC
VPC_ID=$(aws ec2 create-vpc \
    --cidr-block $VPC_CIDR \
    --tag-specifications "ResourceType=vpc,Tags=[{Key=Name,Value=$NAME_PREFIX}]" \
    --query 'Vpc.VpcId' --output text)
echo "✅ VPC created: $VPC_ID"

# Enable DNS hostnames
aws ec2 modify-vpc-attribute --vpc-id $VPC_ID --enable-dns-hostnames

# Create Internet Gateway
IGW_ID=$(aws ec2 create-internet-gateway \
    --tag-specifications "ResourceType=internet-gateway,Tags=[{Key=Name,Value=$NAME_PREFIX-igw}]" \
    --query 'InternetGateway.InternetGatewayId' --output text)
aws ec2 attach-internet-gateway --internet-gateway-id $IGW_ID --vpc-id $VPC_ID
echo "✅ Internet Gateway: $IGW_ID"

# Create public subnet
PUBLIC_SUBNET=$(aws ec2 create-subnet \
    --vpc-id $VPC_ID \
    --cidr-block $PUBLIC_SUBNET_CIDR \
    --availability-zone $AZ \
    --tag-specifications "ResourceType=subnet,Tags=[{Key=Name,Value=$NAME_PREFIX-public}]" \
    --query 'Subnet.SubnetId' --output text)
aws ec2 modify-subnet-attribute --subnet-id $PUBLIC_SUBNET --map-public-ip-on-launch
echo "✅ Public Subnet: $PUBLIC_SUBNET"

# Create private subnet
PRIVATE_SUBNET=$(aws ec2 create-subnet \
    --vpc-id $VPC_ID \
    --cidr-block $PRIVATE_SUBNET_CIDR \
    --availability-zone $AZ \
    --tag-specifications "ResourceType=subnet,Tags=[{Key=Name,Value=$NAME_PREFIX-private}]" \
    --query 'Subnet.SubnetId' --output text)
echo "✅ Private Subnet: $PRIVATE_SUBNET"

# Create public route table
PUBLIC_RTB=$(aws ec2 create-route-table \
    --vpc-id $VPC_ID \
    --tag-specifications "ResourceType=route-table,Tags=[{Key=Name,Value=$NAME_PREFIX-public-rt}]" \
    --query 'RouteTable.RouteTableId' --output text)
aws ec2 create-route --route-table-id $PUBLIC_RTB --destination-cidr-block 0.0.0.0/0 --gateway-id $IGW_ID
aws ec2 associate-route-table --route-table-id $PUBLIC_RTB --subnet-id $PUBLIC_SUBNET
echo "✅ Public Route Table: $PUBLIC_RTB"

echo ""
echo "🎉 VPC Setup Complete!"
echo ""
echo "VPC ID:         $VPC_ID"
echo "Public Subnet:  $PUBLIC_SUBNET"
echo "Private Subnet: $PRIVATE_SUBNET"
echo ""
echo "Next steps:"
echo "  1. Create security groups"
echo "  2. Launch EC2 instances"
echo "  3. Add NAT Gateway for private subnet internet access"
