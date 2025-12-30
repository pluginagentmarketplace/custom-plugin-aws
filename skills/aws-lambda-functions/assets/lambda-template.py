import json

def lambda_handler(event, context):
    """AWS Lambda function template"""
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Success'})
    }
