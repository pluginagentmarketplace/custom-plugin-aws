# Infrastructure as Code Patterns Guide

Best practices and patterns for managing infrastructure as code.

## Tool Selection

```
IaC Tool Decision Tree
│
├── Multi-Cloud Required?
│   ├── Yes → Terraform or Pulumi
│   └── No → Continue
│
├── AWS-Only?
│   ├── Yes → CloudFormation or CDK
│   └── No → Continue
│
├── Team Prefers Programming?
│   ├── Yes → Pulumi or CDK
│   └── No → Terraform (HCL)
│
└── Need Drift Detection?
    ├── Yes → Terraform or AWS Config
    └── No → Any tool works
```

## Module Design Patterns

### 1. Composition Pattern

```hcl
# Root module composes smaller modules
module "networking" {
  source = "./modules/vpc"
  cidr   = var.vpc_cidr
}

module "compute" {
  source    = "./modules/ec2"
  vpc_id    = module.networking.vpc_id
  subnet_id = module.networking.private_subnet_ids[0]
}

module "database" {
  source    = "./modules/rds"
  vpc_id    = module.networking.vpc_id
  subnet_ids = module.networking.private_subnet_ids
}
```

### 2. Environment Abstraction

```
infrastructure/
├── modules/           # Reusable modules
│   ├── vpc/
│   ├── ec2/
│   └── rds/
├── environments/      # Environment configs
│   ├── dev/
│   │   ├── main.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   └── prod/
└── global/           # Shared resources
    ├── iam/
    └── s3-backend/
```

### 3. Workspace Strategy

| Pattern | Use Case | Pros | Cons |
|---------|----------|------|------|
| Directory per env | Clear separation | Isolated state | Code duplication |
| Workspaces | Same code, diff state | DRY | Complex conditionals |
| Terragrunt | Multi-env orchestration | Very DRY | Additional tool |

## State Management Best Practices

### Remote State Configuration

```hcl
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "project/env/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

### State Locking

```hcl
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}
```

## Security Patterns

### Secrets Management

```hcl
# Never hardcode secrets!

# Option 1: AWS Secrets Manager
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "prod/database/password"
}

# Option 2: SSM Parameter Store
data "aws_ssm_parameter" "db_password" {
  name = "/prod/database/password"
}

# Option 3: Vault
data "vault_generic_secret" "db_creds" {
  path = "secret/data/prod/database"
}
```

### Encryption at Rest

```hcl
resource "aws_s3_bucket_server_side_encryption_configuration" "example" {
  bucket = aws_s3_bucket.example.id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.mykey.arn
      sse_algorithm     = "aws:kms"
    }
  }
}
```

## Testing Strategies

### Unit Testing with Terratest

```go
func TestVpcModule(t *testing.T) {
    terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
        TerraformDir: "../modules/vpc",
        Vars: map[string]interface{}{
            "vpc_cidr": "10.0.0.0/16",
        },
    })

    defer terraform.Destroy(t, terraformOptions)
    terraform.InitAndApply(t, terraformOptions)

    vpcId := terraform.Output(t, terraformOptions, "vpc_id")
    assert.NotEmpty(t, vpcId)
}
```

### Policy Testing with OPA

```rego
# policy/terraform.rego
package terraform

deny[msg] {
    resource := input.planned_values.root_module.resources[_]
    resource.type == "aws_s3_bucket"
    not resource.values.versioning[0].enabled
    msg := sprintf("S3 bucket '%s' must have versioning enabled", [resource.address])
}
```

## CI/CD Integration

### GitHub Actions Pipeline

```yaml
name: Terraform

on:
  pull_request:
    paths: ['infrastructure/**']

jobs:
  plan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: hashicorp/setup-terraform@v3

      - name: Terraform Init
        run: terraform init
        working-directory: infrastructure

      - name: Terraform Plan
        run: terraform plan -out=tfplan
        working-directory: infrastructure

      - name: Upload Plan
        uses: actions/upload-artifact@v3
        with:
          name: tfplan
          path: infrastructure/tfplan
```

## Drift Detection

### Automated Drift Monitoring

```python
# Run daily to detect drift
import subprocess
import json

result = subprocess.run(
    ["terraform", "plan", "-detailed-exitcode", "-json"],
    capture_output=True, text=True
)

if result.returncode == 2:
    # Drift detected - alert team
    send_alert("Terraform drift detected!")
```

## Cost Optimization

### Infracost Integration

```yaml
# .github/workflows/infracost.yml
- name: Generate Infracost diff
  run: |
    infracost diff --path=. \
      --format=json \
      --out-file=/tmp/infracost.json
```

## Common Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Hardcoded values | No reusability | Use variables |
| No remote state | State conflicts | S3 + DynamoDB |
| Manual changes | Drift | Policy enforcement |
| Monolithic configs | Hard to manage | Module composition |
| No versioning | Breaking changes | Semantic versioning |
