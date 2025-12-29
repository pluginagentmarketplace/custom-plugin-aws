---
name: aws-lambda
description: Master AWS Lambda - serverless functions, triggers, and event-driven architecture
sasmp_version: "1.3.0"
bonded_agent: aws-serverless
bond_type: PRIMARY_BOND
---

# AWS Lambda Skill

## Function Structure

```python
# lambda_function.py
import json

def lambda_handler(event, context):
    """
    event: Input data (varies by trigger)
    context: Runtime info (function_name, memory_limit, etc.)
    """
    print(f"Event: {json.dumps(event)}")

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'message': 'Success!'})
    }
```

## CLI Commands

```bash
# Create function
aws lambda create-function \
    --function-name my-function \
    --runtime python3.11 \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://function.zip \
    --role arn:aws:iam::123456789012:role/lambda-role

# Invoke function
aws lambda invoke \
    --function-name my-function \
    --payload '{"key": "value"}' \
    output.json

# Update code
aws lambda update-function-code \
    --function-name my-function \
    --zip-file fileb://function.zip

# View logs
aws logs tail /aws/lambda/my-function --follow
```

## Runtimes

| Runtime | Versions | Use Case |
|---------|----------|----------|
| Python | 3.11, 3.12 | General purpose, ML |
| Node.js | 18.x, 20.x | API, real-time |
| Java | 17, 21 | Enterprise |
| Go | 1.x | Performance |
| .NET | 6, 8 | Microsoft stack |
| Ruby | 3.2 | Web apps |
| Custom | AL2023 | Any language |

## Event Sources

- API Gateway (REST/HTTP)
- S3 (object events)
- DynamoDB (streams)
- SQS (queue messages)
- EventBridge (rules)
- CloudWatch (scheduled)
- Kinesis (streaming)
- SNS (notifications)

## Assets

- `function-templates/` - Starter functions
- `sam-templates/` - SAM configurations

## References

- `LAMBDA_PATTERNS.md` - Design patterns
