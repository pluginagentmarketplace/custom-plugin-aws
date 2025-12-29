---
name: aws-cloudformation
description: Master AWS CloudFormation - Infrastructure as Code, templates, and stack management
sasmp_version: "1.3.0"
bonded_agent: aws-devops
bond_type: PRIMARY_BOND
---

# AWS CloudFormation Skill

## Template Structure

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: My CloudFormation template

Parameters:
  Environment:
    Type: String
    Default: dev
    AllowedValues: [dev, staging, prod]

Conditions:
  IsProd: !Equals [!Ref Environment, prod]

Resources:
  MyBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub my-bucket-${Environment}
      Tags:
        - Key: Environment
          Value: !Ref Environment

Outputs:
  BucketName:
    Value: !Ref MyBucket
    Export:
      Name: !Sub ${Environment}-BucketName
```

## Stack Operations

```bash
# Create stack
aws cloudformation create-stack \
    --stack-name my-stack \
    --template-body file://template.yaml \
    --parameters ParameterKey=Environment,ParameterValue=prod \
    --capabilities CAPABILITY_IAM

# Update stack
aws cloudformation update-stack \
    --stack-name my-stack \
    --template-body file://template.yaml

# Deploy (create or update)
aws cloudformation deploy \
    --stack-name my-stack \
    --template-file template.yaml \
    --parameter-overrides Environment=prod

# Delete stack
aws cloudformation delete-stack --stack-name my-stack

# List stacks
aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE
```

## Intrinsic Functions

| Function | Usage |
|----------|-------|
| !Ref | Reference parameter or resource |
| !Sub | String substitution |
| !GetAtt | Get resource attribute |
| !Join | Join strings |
| !If | Conditional value |
| !Equals | Compare values |
| !Select | Select from list |
| !Split | Split string |

## Assets

- `templates/` - Reusable templates
- `nested-stacks/` - Modular components

## References

- `CFN_BEST_PRACTICES.md` - IaC guidelines
