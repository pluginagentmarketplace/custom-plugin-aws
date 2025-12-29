---
name: aws-dynamodb
description: Master AWS DynamoDB - NoSQL tables, indexes, and data modeling
sasmp_version: "1.3.0"
bonded_agent: aws-databases
bond_type: SECONDARY_BOND
---

# AWS DynamoDB Skill

## Create Table

```bash
# Create table with on-demand billing
aws dynamodb create-table \
    --table-name Users \
    --attribute-definitions \
        AttributeName=UserId,AttributeType=S \
        AttributeName=Email,AttributeType=S \
        AttributeName=CreatedAt,AttributeType=S \
    --key-schema \
        AttributeName=UserId,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --global-secondary-indexes \
        "IndexName=EmailIndex,KeySchema=[{AttributeName=Email,KeyType=HASH}],Projection={ProjectionType=ALL}"
```

## CRUD Operations

```bash
# Put item
aws dynamodb put-item \
    --table-name Users \
    --item '{
        "UserId": {"S": "user123"},
        "Email": {"S": "user@example.com"},
        "Name": {"S": "John Doe"},
        "CreatedAt": {"S": "2024-01-01T00:00:00Z"}
    }'

# Get item
aws dynamodb get-item \
    --table-name Users \
    --key '{"UserId": {"S": "user123"}}'

# Query
aws dynamodb query \
    --table-name Users \
    --key-condition-expression "UserId = :uid" \
    --expression-attribute-values '{":uid": {"S": "user123"}}'

# Scan with filter
aws dynamodb scan \
    --table-name Users \
    --filter-expression "contains(Email, :domain)" \
    --expression-attribute-values '{":domain": {"S": "example.com"}}'

# Delete item
aws dynamodb delete-item \
    --table-name Users \
    --key '{"UserId": {"S": "user123"}}'
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| Partition Key | Primary key for distribution |
| Sort Key | Optional, enables range queries |
| GSI | Secondary index, different partition key |
| LSI | Secondary index, same partition key |

## Data Types

| Type | Code | Example |
|------|------|---------|
| String | S | `{"S": "hello"}` |
| Number | N | `{"N": "123"}` |
| Binary | B | `{"B": "base64=="}` |
| Boolean | BOOL | `{"BOOL": true}` |
| Null | NULL | `{"NULL": true}` |
| List | L | `{"L": [...]}` |
| Map | M | `{"M": {...}}` |
| String Set | SS | `{"SS": ["a","b"]}` |

## Assets

- `data-models/` - Common patterns
- `access-patterns/` - Query examples

## References

- `DYNAMODB_PATTERNS.md` - Design patterns
