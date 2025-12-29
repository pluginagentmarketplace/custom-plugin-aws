#!/bin/bash
# ECS Deployment Script

set -e

echo "🐳 ECS Deployment Script"
echo "========================"

# Configuration
CLUSTER=""
SERVICE=""
TASK_FAMILY=""
IMAGE=""
REGION=${AWS_DEFAULT_REGION:-us-east-1}

usage() {
    echo "Usage: $0 --cluster <name> --service <name> --image <uri>"
    echo ""
    echo "Options:"
    echo "  --cluster     ECS cluster name"
    echo "  --service     ECS service name"
    echo "  --image       Docker image URI"
    echo "  --task        Task definition family (optional, derived from service)"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --cluster) CLUSTER="$2"; shift 2 ;;
        --service) SERVICE="$2"; shift 2 ;;
        --image) IMAGE="$2"; shift 2 ;;
        --task) TASK_FAMILY="$2"; shift 2 ;;
        --region) REGION="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; usage; exit 1 ;;
    esac
done

if [ -z "$CLUSTER" ] || [ -z "$SERVICE" ] || [ -z "$IMAGE" ]; then
    usage
    exit 1
fi

# Get current task definition if not specified
if [ -z "$TASK_FAMILY" ]; then
    TASK_FAMILY=$(aws ecs describe-services \
        --cluster "$CLUSTER" \
        --services "$SERVICE" \
        --query 'services[0].taskDefinition' \
        --output text | sed 's/.*\///' | sed 's/:.*//')
fi

echo "📋 Configuration:"
echo "   Cluster: $CLUSTER"
echo "   Service: $SERVICE"
echo "   Task Family: $TASK_FAMILY"
echo "   Image: $IMAGE"
echo ""

# Get current task definition
echo "📥 Getting current task definition..."
TASK_DEF=$(aws ecs describe-task-definition \
    --task-definition "$TASK_FAMILY" \
    --query 'taskDefinition')

# Update image in container definitions
echo "🔄 Updating image..."
NEW_TASK_DEF=$(echo "$TASK_DEF" | jq --arg IMAGE "$IMAGE" \
    '.containerDefinitions[0].image = $IMAGE |
    del(.taskDefinitionArn, .revision, .status, .requiresAttributes, .compatibilities, .registeredAt, .registeredBy)')

# Register new task definition
echo "📝 Registering new task definition..."
NEW_REVISION=$(aws ecs register-task-definition \
    --cli-input-json "$NEW_TASK_DEF" \
    --query 'taskDefinition.revision' \
    --output text)

echo "   New revision: $TASK_FAMILY:$NEW_REVISION"

# Update service
echo "🚀 Updating service..."
aws ecs update-service \
    --cluster "$CLUSTER" \
    --service "$SERVICE" \
    --task-definition "$TASK_FAMILY:$NEW_REVISION" \
    --force-new-deployment \
    --query 'service.deployments[0].{Status:status,Desired:desiredCount,Running:runningCount}' \
    --output table

# Wait for deployment
echo ""
echo "⏳ Waiting for deployment to stabilize..."
aws ecs wait services-stable \
    --cluster "$CLUSTER" \
    --services "$SERVICE"

echo ""
echo "✅ Deployment complete!"
echo ""

# Show current state
aws ecs describe-services \
    --cluster "$CLUSTER" \
    --services "$SERVICE" \
    --query 'services[0].{Service:serviceName,Status:status,Desired:desiredCount,Running:runningCount,TaskDef:taskDefinition}' \
    --output table
