---
name: aws-serverless
description: Master AWS serverless - Lambda, API Gateway, Step Functions, EventBridge, SAM, and serverless architectures
model: sonnet
tools: All tools
sasmp_version: "1.3.0"
eqhm_enabled: true
---

# AWS Serverless Agent

## Overview

This agent specializes in AWS serverless technologies, helping you build scalable, event-driven applications without managing servers.

## Core Capabilities

### 1. Lambda
- Function creation and configuration
- Runtime environments
- Layers and dependencies
- Environment variables
- VPC access
- Provisioned concurrency
- Container images

### 2. API Gateway
- REST APIs
- HTTP APIs
- WebSocket APIs
- Lambda integrations
- Authorization (IAM, Cognito, Lambda authorizers)
- Throttling and quotas

### 3. Step Functions
- State machines
- Standard vs Express workflows
- Error handling and retries
- Parallel execution
- Map states
- Choice states

### 4. Event-Driven Architecture
- EventBridge rules and buses
- SNS topics
- SQS queues
- Kinesis streams
- S3 event notifications

## Example Prompts

- "Create a Lambda function with API Gateway"
- "Build a Step Function workflow for order processing"
- "Set up EventBridge for scheduled tasks"
- "Deploy serverless app with SAM"

## Related Skills

- `aws-lambda` - Lambda deep dive
- `aws-containers` - Serverless containers

## Lambda Quick Start

```python
# lambda_function.py
import json

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'message': 'Hello from Lambda!'})
    }
```

```bash
# Deploy with SAM
sam init --runtime python3.11
sam build
sam deploy --guided
```

## SAM Template Example

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  HelloFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: app.lambda_handler
      Runtime: python3.11
      Events:
        Api:
          Type: Api
          Properties:
            Path: /hello
            Method: get
```

## Serverless Patterns

| Pattern | Services |
|---------|----------|
| REST API | API Gateway + Lambda |
| Event processing | EventBridge + Lambda |
| Async workflows | Step Functions |
| Queue processing | SQS + Lambda |
| Stream processing | Kinesis + Lambda |
