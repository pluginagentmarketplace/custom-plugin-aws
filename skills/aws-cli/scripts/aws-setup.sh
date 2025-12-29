#!/bin/bash
# AWS CLI Setup Script
# Installs and configures AWS CLI v2

set -e

echo "🔧 AWS CLI Setup Script"
echo "======================="

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     PLATFORM=linux;;
    Darwin*)    PLATFORM=mac;;
    *)          echo "Unsupported OS: ${OS}"; exit 1;;
esac

# Check if AWS CLI is already installed
if command -v aws &> /dev/null; then
    echo "✅ AWS CLI already installed:"
    aws --version
    read -p "Do you want to reinstall? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
fi

# Install AWS CLI v2
echo "📦 Installing AWS CLI v2 for ${PLATFORM}..."

if [ "$PLATFORM" = "mac" ]; then
    curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
    sudo installer -pkg AWSCLIV2.pkg -target /
    rm AWSCLIV2.pkg
elif [ "$PLATFORM" = "linux" ]; then
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip -q awscliv2.zip
    sudo ./aws/install
    rm -rf awscliv2.zip aws
fi

# Verify installation
echo ""
echo "✅ AWS CLI installed successfully:"
aws --version

# Configure credentials
echo ""
echo "🔐 Configure AWS credentials:"
echo "   You'll need:"
echo "   - AWS Access Key ID"
echo "   - AWS Secret Access Key"
echo "   - Default region (e.g., us-east-1)"
echo ""

read -p "Configure now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    aws configure
fi

# Test connection
echo ""
echo "🧪 Testing AWS connection..."
if aws sts get-caller-identity &> /dev/null; then
    echo "✅ Successfully connected to AWS!"
    aws sts get-caller-identity
else
    echo "❌ Could not connect to AWS. Check your credentials."
    exit 1
fi

echo ""
echo "🎉 AWS CLI setup complete!"
echo ""
echo "Next steps:"
echo "  1. Run 'aws configure --profile <name>' to add more profiles"
echo "  2. Source the aws-aliases.sh file for productivity shortcuts"
echo "  3. Run 'aws sts get-caller-identity' to verify"
