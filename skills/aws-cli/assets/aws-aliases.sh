#!/bin/bash
# AWS CLI Productivity Aliases
# Source this file in your .bashrc or .zshrc

# Identity
alias awswho='aws sts get-caller-identity'
alias awsaccount='aws sts get-caller-identity --query Account --output text'

# EC2
alias ec2ls='aws ec2 describe-instances --query "Reservations[].Instances[].[InstanceId,State.Name,InstanceType,PublicIpAddress,Tags[?Key==\`Name\`].Value|[0]]" --output table'
alias ec2running='aws ec2 describe-instances --filters "Name=instance-state-name,Values=running" --query "Reservations[].Instances[].[InstanceId,PublicIpAddress]" --output table'
alias ec2stop='aws ec2 stop-instances --instance-ids'
alias ec2start='aws ec2 start-instances --instance-ids'

# S3
alias s3ls='aws s3 ls'
alias s3size='aws s3 ls --summarize --human-readable --recursive'

# Lambda
alias lambdals='aws lambda list-functions --query "Functions[].[FunctionName,Runtime,MemorySize]" --output table'
alias lambdalogs='aws logs tail --follow /aws/lambda/'

# CloudFormation
alias cfnls='aws cloudformation list-stacks --query "StackSummaries[?StackStatus!=\`DELETE_COMPLETE\`].[StackName,StackStatus]" --output table'
alias cfnevents='aws cloudformation describe-stack-events --stack-name'

# Logs
alias cwlogs='aws logs describe-log-groups --query "logGroups[].[logGroupName]" --output table'

# Cost
alias awscost='aws ce get-cost-and-usage --time-period Start=$(date -v-30d +%Y-%m-%d),End=$(date +%Y-%m-%d) --granularity MONTHLY --metrics "BlendedCost"'

# Profile switching
awsp() {
    export AWS_PROFILE=$1
    echo "Switched to profile: $AWS_PROFILE"
    aws sts get-caller-identity
}

# Region switching
awsr() {
    export AWS_DEFAULT_REGION=$1
    echo "Switched to region: $AWS_DEFAULT_REGION"
}

echo "AWS aliases loaded! Use 'awsp <profile>' to switch profiles."
