#!/bin/bash
# Lambda Deployment Script

set -e

echo "🚀 Lambda Deployment Script"
echo "==========================="

# Configuration
FUNCTION_NAME=""
RUNTIME="python3.11"
HANDLER="lambda_function.lambda_handler"
ROLE_ARN=""
MEMORY=256
TIMEOUT=30
SOURCE_DIR="."

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --name) FUNCTION_NAME="$2"; shift 2 ;;
        --runtime) RUNTIME="$2"; shift 2 ;;
        --handler) HANDLER="$2"; shift 2 ;;
        --role) ROLE_ARN="$2"; shift 2 ;;
        --memory) MEMORY="$2"; shift 2 ;;
        --timeout) TIMEOUT="$2"; shift 2 ;;
        --source) SOURCE_DIR="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

if [ -z "$FUNCTION_NAME" ]; then
    echo "Error: --name is required"
    exit 1
fi

# Create deployment package
echo "📦 Creating deployment package..."
TEMP_DIR=$(mktemp -d)
ZIP_FILE="$TEMP_DIR/function.zip"

# Copy source files
cp -r "$SOURCE_DIR"/*.py "$TEMP_DIR/" 2>/dev/null || true

# Install dependencies if requirements.txt exists
if [ -f "$SOURCE_DIR/requirements.txt" ]; then
    echo "📦 Installing dependencies..."
    pip install -r "$SOURCE_DIR/requirements.txt" -t "$TEMP_DIR" --quiet
fi

# Create zip
cd "$TEMP_DIR"
zip -r "$ZIP_FILE" . -x "*.pyc" -x "__pycache__/*" >/dev/null

# Check if function exists
if aws lambda get-function --function-name "$FUNCTION_NAME" 2>/dev/null; then
    echo "📤 Updating existing function..."
    aws lambda update-function-code \
        --function-name "$FUNCTION_NAME" \
        --zip-file "fileb://$ZIP_FILE" \
        --query 'FunctionArn' --output text

    # Update configuration if needed
    aws lambda update-function-configuration \
        --function-name "$FUNCTION_NAME" \
        --runtime "$RUNTIME" \
        --handler "$HANDLER" \
        --memory-size "$MEMORY" \
        --timeout "$TIMEOUT" \
        --query 'FunctionArn' --output text
else
    echo "🆕 Creating new function..."
    if [ -z "$ROLE_ARN" ]; then
        echo "Error: --role is required for new functions"
        exit 1
    fi

    aws lambda create-function \
        --function-name "$FUNCTION_NAME" \
        --runtime "$RUNTIME" \
        --handler "$HANDLER" \
        --role "$ROLE_ARN" \
        --zip-file "fileb://$ZIP_FILE" \
        --memory-size "$MEMORY" \
        --timeout "$TIMEOUT" \
        --query 'FunctionArn' --output text
fi

# Cleanup
rm -rf "$TEMP_DIR"

echo ""
echo "✅ Deployment complete!"
echo "Function: $FUNCTION_NAME"
echo ""
echo "Test with:"
echo "  aws lambda invoke --function-name $FUNCTION_NAME --payload '{}' output.json"
