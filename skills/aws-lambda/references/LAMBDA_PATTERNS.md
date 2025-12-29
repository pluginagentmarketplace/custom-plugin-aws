# Lambda Design Patterns

## 1. API Gateway + Lambda

```
Client → API Gateway → Lambda → DynamoDB
```

```yaml
# SAM Template
Resources:
  ApiFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: app.handler
      Runtime: python3.11
      Events:
        Api:
          Type: Api
          Properties:
            Path: /items
            Method: GET
```

## 2. S3 Event Processing

```
S3 Upload → Lambda → Process → Store Result
```

```python
def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        # Process file
```

## 3. SQS Queue Processing

```
Producer → SQS → Lambda → DynamoDB
```

```python
def lambda_handler(event, context):
    for record in event['Records']:
        body = json.loads(record['body'])
        # Process message
```

## 4. Scheduled Tasks (Cron)

```yaml
Events:
  Schedule:
    Type: Schedule
    Properties:
      Schedule: rate(1 hour)
```

## 5. Fan-Out Pattern

```
SNS Topic → [Lambda1, Lambda2, Lambda3]
```

## Best Practices

### Cold Starts

```python
# Initialize outside handler (warm start reuse)
import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('MyTable')

def lambda_handler(event, context):
    # Use pre-initialized client
    table.get_item(Key={'id': '123'})
```

### Error Handling

```python
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()
tracer = Tracer()

@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext):
    try:
        # Your logic
        pass
    except Exception as e:
        logger.exception("Error processing")
        raise
```

### Environment Variables

```python
import os

TABLE_NAME = os.environ['TABLE_NAME']
API_KEY = os.environ['API_KEY']
```

## Performance Tips

1. **Minimize package size** - Use Lambda layers
2. **Connection reuse** - Initialize outside handler
3. **Provisioned concurrency** - For consistent latency
4. **ARM64** - 20% cheaper, often faster
5. **Right-size memory** - More memory = more CPU
