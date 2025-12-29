# CloudFormation Best Practices

## Template Organization

### Use Parameters
```yaml
Parameters:
  Environment:
    Type: String
    AllowedValues: [dev, staging, prod]
    Default: dev

  # Use AWS-specific parameter types
  VpcId:
    Type: AWS::EC2::VPC::Id

  SubnetIds:
    Type: List<AWS::EC2::Subnet::Id>
```

### Use Mappings for Region-Specific Values
```yaml
Mappings:
  RegionAMI:
    us-east-1:
      HVM64: ami-0abc123
    us-west-2:
      HVM64: ami-0def456
```

### Use Conditions
```yaml
Conditions:
  IsProd: !Equals [!Ref Environment, prod]
  CreateReplica: !And
    - !Condition IsProd
    - !Equals [!Ref AWS::Region, us-east-1]
```

## Nested Stacks

```yaml
Resources:
  VPCStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://s3.amazonaws.com/bucket/vpc.yaml
      Parameters:
        Environment: !Ref Environment

  AppStack:
    Type: AWS::CloudFormation::Stack
    DependsOn: VPCStack
    Properties:
      TemplateURL: https://s3.amazonaws.com/bucket/app.yaml
      Parameters:
        VpcId: !GetAtt VPCStack.Outputs.VpcId
```

## Change Sets

```bash
# Create change set (preview changes)
aws cloudformation create-change-set \
    --stack-name my-stack \
    --change-set-name my-changes \
    --template-body file://template.yaml

# Review changes
aws cloudformation describe-change-set \
    --stack-name my-stack \
    --change-set-name my-changes

# Execute changes
aws cloudformation execute-change-set \
    --stack-name my-stack \
    --change-set-name my-changes
```

## Drift Detection

```bash
# Detect drift
aws cloudformation detect-stack-drift --stack-name my-stack

# Check drift status
aws cloudformation describe-stack-drift-detection-status \
    --stack-drift-detection-id ID

# Get drifted resources
aws cloudformation describe-stack-resource-drifts \
    --stack-name my-stack
```

## Security

### Use IAM Roles
```yaml
Resources:
  LambdaRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

### Protect Sensitive Data
```yaml
Parameters:
  DBPassword:
    Type: String
    NoEcho: true  # Hide in console
```

## Deletion Policies

```yaml
Resources:
  Database:
    Type: AWS::RDS::DBInstance
    DeletionPolicy: Snapshot  # Create snapshot before delete
    UpdateReplacePolicy: Snapshot

  ImportantBucket:
    Type: AWS::S3::Bucket
    DeletionPolicy: Retain  # Keep on stack delete
```

## Stack Policy

```json
{
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "Update:*",
      "Principal": "*",
      "Resource": "*"
    },
    {
      "Effect": "Deny",
      "Action": "Update:Replace",
      "Principal": "*",
      "Resource": "LogicalResourceId/ProductionDatabase"
    }
  ]
}
```
