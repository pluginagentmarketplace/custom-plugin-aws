#!/bin/bash
# EC2 Instance Launcher Script

echo "🚀 EC2 Instance Launcher"
echo "========================"

# Default values
INSTANCE_TYPE="t3.micro"
KEY_NAME=""
SECURITY_GROUP=""
SUBNET=""
AMI_ID=""
NAME="MyEC2Instance"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --type) INSTANCE_TYPE="$2"; shift 2 ;;
        --key) KEY_NAME="$2"; shift 2 ;;
        --sg) SECURITY_GROUP="$2"; shift 2 ;;
        --subnet) SUBNET="$2"; shift 2 ;;
        --ami) AMI_ID="$2"; shift 2 ;;
        --name) NAME="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

# Get latest Amazon Linux 2023 AMI if not specified
if [ -z "$AMI_ID" ]; then
    echo "Finding latest Amazon Linux 2023 AMI..."
    AMI_ID=$(aws ec2 describe-images \
        --owners amazon \
        --filters "Name=name,Values=al2023-ami-*-x86_64" \
                  "Name=state,Values=available" \
        --query 'sort_by(Images, &CreationDate)[-1].ImageId' \
        --output text)
    echo "Using AMI: $AMI_ID"
fi

# Validate required parameters
if [ -z "$KEY_NAME" ]; then
    echo "Error: --key is required"
    exit 1
fi

# Launch instance
echo ""
echo "Launching EC2 instance..."
INSTANCE_ID=$(aws ec2 run-instances \
    --image-id "$AMI_ID" \
    --instance-type "$INSTANCE_TYPE" \
    --key-name "$KEY_NAME" \
    ${SECURITY_GROUP:+--security-group-ids "$SECURITY_GROUP"} \
    ${SUBNET:+--subnet-id "$SUBNET"} \
    --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$NAME}]" \
    --query 'Instances[0].InstanceId' \
    --output text)

echo "Instance ID: $INSTANCE_ID"

# Wait for running state
echo "Waiting for instance to be running..."
aws ec2 wait instance-running --instance-ids "$INSTANCE_ID"

# Get public IP
PUBLIC_IP=$(aws ec2 describe-instances \
    --instance-ids "$INSTANCE_ID" \
    --query 'Reservations[0].Instances[0].PublicIpAddress' \
    --output text)

echo ""
echo "✅ Instance launched successfully!"
echo "   Instance ID: $INSTANCE_ID"
echo "   Public IP: $PUBLIC_IP"
echo ""
echo "Connect with: ssh -i ~/.ssh/$KEY_NAME.pem ec2-user@$PUBLIC_IP"
