#!/bin/bash
# CloudFormation Deploy Script

set -e

echo "☁️ CloudFormation Deploy"
echo "========================"

usage() {
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Commands:"
    echo "  deploy <stack> <template>  Deploy or update stack"
    echo "  delete <stack>             Delete stack"
    echo "  status <stack>             Check stack status"
    echo "  events <stack>             Show stack events"
    echo "  outputs <stack>            Show stack outputs"
    echo "  validate <template>        Validate template"
    echo ""
    echo "Options:"
    echo "  --params KEY=VALUE         Parameter overrides"
    echo "  --tags KEY=VALUE           Stack tags"
}

if [ $# -lt 2 ]; then
    usage
    exit 1
fi

COMMAND=$1
shift

case $COMMAND in
    deploy)
        STACK_NAME=$1
        TEMPLATE=$2
        shift 2

        # Parse additional options
        PARAMS=""
        TAGS=""
        while [[ $# -gt 0 ]]; do
            case $1 in
                --params) PARAMS="$2"; shift 2 ;;
                --tags) TAGS="$2"; shift 2 ;;
                *) shift ;;
            esac
        done

        echo "🚀 Deploying stack: $STACK_NAME"

        # Validate first
        echo "Validating template..."
        aws cloudformation validate-template --template-body "file://$TEMPLATE"

        # Deploy
        CMD="aws cloudformation deploy \
            --stack-name $STACK_NAME \
            --template-file $TEMPLATE \
            --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM"

        if [ -n "$PARAMS" ]; then
            CMD="$CMD --parameter-overrides $PARAMS"
        fi

        if [ -n "$TAGS" ]; then
            CMD="$CMD --tags $TAGS"
        fi

        eval $CMD

        echo ""
        echo "✅ Deployment complete!"
        echo ""
        echo "Outputs:"
        aws cloudformation describe-stacks \
            --stack-name "$STACK_NAME" \
            --query 'Stacks[0].Outputs' \
            --output table
        ;;

    delete)
        STACK_NAME=$1
        echo "🗑️ Deleting stack: $STACK_NAME"

        read -p "Are you sure? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            aws cloudformation delete-stack --stack-name "$STACK_NAME"

            echo "Waiting for deletion..."
            aws cloudformation wait stack-delete-complete --stack-name "$STACK_NAME"

            echo "✅ Stack deleted!"
        fi
        ;;

    status)
        STACK_NAME=$1
        aws cloudformation describe-stacks \
            --stack-name "$STACK_NAME" \
            --query 'Stacks[0].{Name:StackName,Status:StackStatus,Updated:LastUpdatedTime}' \
            --output table
        ;;

    events)
        STACK_NAME=$1
        aws cloudformation describe-stack-events \
            --stack-name "$STACK_NAME" \
            --query 'StackEvents[0:10].[Timestamp,LogicalResourceId,ResourceStatus,ResourceStatusReason]' \
            --output table
        ;;

    outputs)
        STACK_NAME=$1
        aws cloudformation describe-stacks \
            --stack-name "$STACK_NAME" \
            --query 'Stacks[0].Outputs[].[OutputKey,OutputValue]' \
            --output table
        ;;

    validate)
        TEMPLATE=$1
        echo "Validating: $TEMPLATE"
        aws cloudformation validate-template --template-body "file://$TEMPLATE"
        echo "✅ Template is valid!"
        ;;

    *)
        echo "Unknown command: $COMMAND"
        usage
        exit 1
        ;;
esac
