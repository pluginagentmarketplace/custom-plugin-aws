# AWS Cloud Assistant - Architecture

## System Design Overview

This document describes the architecture, integration patterns, and technical design of the AWS Cloud Assistant plugin.

---

## 1. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      AWS CLOUD ASSISTANT PLUGIN                          │
│                         SASMP v1.3.0 | EQHM Enabled                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                    COMMAND LAYER (4 Commands)                       │ │
│  ├────────────────────────────────────────────────────────────────────┤ │
│  │  /aws-check  │  /aws-costs  │  /aws-deploy  │  /aws-debug          │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                    ↓                                     │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                    AGENT LAYER (8 Agents)                           │ │
│  ├────────────────────────────────────────────────────────────────────┤ │
│  │ Fundamentals │ Compute │ Storage │ Networking │ Database │         │ │
│  │ Security     │ Serverless │ DevOps                                 │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                    ↓                                     │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                    SKILL LAYER (12 Skills)                          │ │
│  ├────────────────────────────────────────────────────────────────────┤ │
│  │ IAM │ EC2 │ S3 │ VPC │ RDS │ Lambda │ Security │ CloudFormation   │ │
│  │ CodePipeline │ CloudWatch │ ECS │ Cost Optimization                │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                    ↓                                     │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                    REGISTRY LAYER                                   │ │
│  ├────────────────────────────────────────────────────────────────────┤ │
│  │ Agent-Skill Mappings │ Skill Dependencies │ Learning Paths         │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                           AWS SERVICES                                   │
├─────────────────────────────────────────────────────────────────────────┤
│ IAM │ EC2 │ S3 │ VPC │ RDS │ Lambda │ ECS │ CloudFormation │ ...       │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Component Architecture

### 2.1 Command Layer

**Responsibility:** User interface and diagnostic operations

| Command | Category | Exit Codes | Tools |
|---------|----------|------------|-------|
| `/aws-check` | Diagnostics | 0-5 | Bash, Read |
| `/aws-costs` | FinOps | 0-4 | Bash, Read |
| `/aws-deploy` | Deployment | 0-6 | Bash, Read, Write |
| `/aws-debug` | Diagnostics | 0-5 | Bash, Read, WebSearch |

**Command Flow:**
```
User Input → Validate Parameters → Execute AWS CLI → Parse Output → Return Results
     ↓              ↓                    ↓              ↓             ↓
  Regex Check   Exit if Invalid    Retry Logic     Format JSON    Exit Code
```

### 2.2 Agent Layer

**Responsibility:** Domain-specific AWS architecture guidance

| Agent | Domain | Primary Skills | Secondary Skills |
|-------|--------|----------------|------------------|
| 01-aws-fundamentals | IAM, Billing | aws-iam-setup | aws-cost-optimization |
| 02-aws-compute | EC2, Containers | aws-ec2-deployment | aws-ecs |
| 03-aws-storage | S3, EBS, EFS | aws-s3-management | - |
| 04-aws-networking | VPC, DNS, CDN | aws-vpc-design | - |
| 05-aws-database | RDS, DynamoDB | aws-rds-setup | - |
| 06-aws-security | WAF, KMS | aws-security-best-practices | aws-iam-setup |
| 07-aws-serverless | Lambda, API GW | aws-lambda-functions | - |
| 08-aws-devops | IaC, CI/CD | aws-cloudformation, aws-ecs | aws-codepipeline, aws-cloudwatch |

**Agent Structure:**
```yaml
Agent Definition:
  ├── Role & Responsibilities
  │   ├── Primary Mission
  │   ├── IN SCOPE
  │   └── OUT OF SCOPE (delegations)
  ├── Input/Output Schema (JSON)
  ├── Skills Integration (PRIMARY/SECONDARY bonds)
  ├── Error Handling Table
  ├── Fallback Strategies
  ├── Troubleshooting
  │   ├── Decision Tree
  │   └── Debug Checklist
  └── Example Prompts
```

### 2.3 Skill Layer

**Responsibility:** Atomic, reusable AWS operations

| Skill | Bonded Agent | Complexity | Time |
|-------|--------------|------------|------|
| aws-iam-setup | 01-fundamentals | Medium | 15-30 min |
| aws-ec2-deployment | 02-compute | Medium | 5-15 min |
| aws-s3-management | 03-storage | Medium | 10-20 min |
| aws-vpc-design | 04-networking | High | 30-60 min |
| aws-rds-setup | 05-database | Medium-High | 20-45 min |
| aws-lambda-functions | 07-serverless | Medium | 10-30 min |
| aws-security-best-practices | 06-security | High | 30-60 min |
| aws-cloudformation | 08-devops | Medium-High | 10-60 min |
| aws-codepipeline | 08-devops | Medium | 20-45 min |
| aws-cloudwatch | 08-devops | Medium | 15-30 min |
| aws-ecs | 08-devops | Medium-High | 20-45 min |
| aws-cost-optimization | 01-fundamentals | Medium | 15-30 min |

**Skill Structure:**
```yaml
Skill Definition:
  ├── Quick Reference Table
  ├── Parameters
  │   ├── Required (with validation)
  │   └── Optional (with defaults)
  ├── Implementation
  │   ├── Bash Examples
  │   ├── Python Examples
  │   └── CloudFormation Templates
  ├── Retry Logic (exponential backoff)
  ├── Troubleshooting Table
  ├── Debug Checklist
  ├── Test Template
  └── References (AWS docs)
```

### 2.4 Registry Layer

**Responsibility:** Agent-skill mappings and dependencies

```json
{
  "agents": [...],           // 8 agent definitions
  "skills": [...],           // 12 skill definitions
  "commands": [...],         // 4 command definitions
  "skill_dependencies": {},  // Prerequisite graph
  "agent_to_skill_mapping": {},
  "learning_paths": {}       // 6 learning journeys
}
```

---

## 3. Agent-Skill Bond System

### Bond Types

| Bond Type | Description | Invocation |
|-----------|-------------|------------|
| PRIMARY_BOND | Main skill for agent's domain | Always available |
| SECONDARY_BOND | Supporting skill | Available on request |

### Bond Matrix

```
                    Skills
                    ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
                    │ IAM │ EC2 │ S3  │ VPC │ RDS │ Lam │ Sec │ CFN │ Pipe│ CW  │ ECS │Cost │
Agents              ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
01-fundamentals     │  P  │     │     │     │     │     │     │     │     │     │     │  S  │
02-compute          │     │  P  │     │     │     │     │     │     │     │     │  S  │     │
03-storage          │     │     │  P  │     │     │     │     │     │     │     │     │     │
04-networking       │     │     │     │  P  │     │     │     │     │     │     │     │     │
05-database         │     │     │     │     │  P  │     │     │     │     │     │     │     │
06-security         │  S  │     │     │     │     │     │  P  │     │     │     │     │     │
07-serverless       │     │     │     │     │     │  P  │     │     │     │     │     │     │
08-devops           │     │     │     │     │     │     │     │  P  │  S  │  S  │  P  │     │
                    └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘
                    P = PRIMARY_BOND, S = SECONDARY_BOND
```

---

## 4. Skill Dependency Graph

```
                          aws-iam-setup
                               │
        ┌──────────┬───────────┼───────────┬──────────┬──────────┐
        ↓          ↓           ↓           ↓          ↓          ↓
   aws-vpc-design  aws-s3   aws-cost   aws-security  aws-cw   aws-cfn
        │          │                       │                     │
        ↓          ↓                       ↓                     ↓
   aws-ec2    (no deps)              (no deps)            aws-codepipeline
        │
   ┌────┴────┐
   ↓         ↓
aws-rds   aws-ecs
   │
   ↓
(needs VPC + Security)
```

---

## 5. Data Flow Architecture

### 5.1 Agent Invocation Flow

```
User Request
    ↓
┌─────────────────┐
│ Parse Intent    │ → Identify AWS domain
└────────┬────────┘
         ↓
┌─────────────────┐
│ Route to Agent  │ → Select appropriate agent
└────────┬────────┘
         ↓
┌─────────────────┐
│ Load I/O Schema │ → Validate input structure
└────────┬────────┘
         ↓
┌─────────────────┐
│ Invoke Skills   │ → Execute PRIMARY then SECONDARY
└────────┬────────┘
         ↓
┌─────────────────┐
│ Error Handling  │ → Fallback if needed
└────────┬────────┘
         ↓
┌─────────────────┐
│ Format Output   │ → Return JSON response
└─────────────────┘
```

### 5.2 Skill Execution Flow

```
Skill Invocation
    ↓
┌─────────────────┐
│ Validate Params │ → Check required/optional
└────────┬────────┘
         ↓
┌─────────────────┐
│ Check Deps      │ → Verify prerequisites met
└────────┬────────┘
         ↓
┌─────────────────┐
│ Execute Action  │ → Run AWS CLI/SDK
└────────┬────────┘
    ↓    ↓ (on error)
    │    ┌─────────────────┐
    │    │ Retry Logic     │ → Exponential backoff
    │    └────────┬────────┘
    │             ↓
    │    ┌─────────────────┐
    │    │ Troubleshoot    │ → Decision tree
    │    └────────┬────────┘
    ↓             ↓
┌─────────────────┐
│ Return Result   │ → Success/Error with details
└─────────────────┘
```

---

## 6. Error Handling Architecture

### Error Categories

| Category | Exit Code | Recovery Strategy |
|----------|-----------|-------------------|
| Validation Error | 1 | Fix input parameters |
| Authentication Error | 2 | Refresh credentials |
| Permission Error | 3 | Check IAM policies |
| Resource Error | 4 | Verify resource exists |
| Network Error | 5 | Retry with backoff |
| Timeout Error | 6 | Increase timeout |

### Fallback Chain

```
Primary Action Failed
    ↓
┌─────────────────┐
│ Retry (3x)      │ → Exponential backoff: 2s, 4s, 8s
└────────┬────────┘
         ↓ (still failing)
┌─────────────────┐
│ Alternative     │ → Try different approach
└────────┬────────┘
         ↓ (still failing)
┌─────────────────┐
│ Manual Fallback │ → Provide manual steps
└────────┬────────┘
         ↓
┌─────────────────┐
│ Escalate        │ → Suggest AWS Support
└─────────────────┘
```

---

## 7. File Structure

```
custom-plugin-aws/
├── .claude-plugin/
│   ├── plugin.json              # Plugin manifest (2 KB)
│   └── marketplace.json         # Marketplace metadata (1 KB)
│
├── agents/                       # 8 agents (~150 lines each)
│   ├── 01-aws-fundamentals.md   # IAM, Billing
│   ├── 02-aws-compute.md        # EC2, Containers
│   ├── 03-aws-storage.md        # S3, EBS, EFS
│   ├── 04-aws-networking.md     # VPC, Route53
│   ├── 05-aws-database.md       # RDS, DynamoDB
│   ├── 06-aws-security.md       # WAF, KMS
│   ├── 07-aws-serverless.md     # Lambda, API Gateway
│   └── 08-aws-devops.md         # CloudFormation, CI/CD
│
├── skills/                       # 12 skills (~200 lines each)
│   ├── aws-iam-setup/SKILL.md
│   ├── aws-ec2-deployment/SKILL.md
│   ├── aws-s3-management/SKILL.md
│   ├── aws-vpc-design/SKILL.md
│   ├── aws-rds-setup/SKILL.md
│   ├── aws-lambda-functions/SKILL.md
│   ├── aws-security-best-practices/SKILL.md
│   ├── aws-cloudformation/SKILL.md
│   ├── aws-codepipeline/SKILL.md
│   ├── aws-cloudwatch/SKILL.md
│   ├── aws-ecs/SKILL.md
│   └── aws-cost-optimization/SKILL.md
│
├── commands/                     # 4 commands (~250 lines each)
│   ├── aws-check.md             # Diagnostics
│   ├── aws-costs.md             # FinOps
│   ├── aws-deploy.md            # Deployment
│   └── aws-debug.md             # Troubleshooting
│
├── config/
│   └── agent-registry.json      # Registry (15 KB)
│
├── hooks/
│   └── hooks.json               # Hook configuration
│
├── ARCHITECTURE.md              # This file
├── LEARNING-PATH.md             # Learning journeys
├── CHANGELOG.md                 # Version history
├── CONTRIBUTING.md              # Contribution guide
├── LICENSE                      # License file
└── README.md                    # Project overview
```

---

## 8. Size Metrics

| Component | Files | Lines | Size |
|-----------|-------|-------|------|
| Agents | 8 | ~1,200 | ~40 KB |
| Skills | 12 | ~2,400 | ~80 KB |
| Commands | 4 | ~1,000 | ~35 KB |
| Registry | 1 | ~450 | ~15 KB |
| Documentation | 4 | ~800 | ~25 KB |
| **Total** | **29** | **~5,850** | **~195 KB** |

---

## 9. Integration with AWS

### AWS CLI Integration

```bash
# All skills use AWS CLI v2
aws <service> <command> --options

# Standard patterns:
--output json          # JSON output for parsing
--query 'Expression'   # JMESPath filtering
--profile $PROFILE     # Multi-account support
--region $REGION       # Region targeting
```

### AWS SDK Integration (Python)

```python
import boto3
from botocore.config import Config

# Standard configuration
config = Config(
    retries={'max_attempts': 3, 'mode': 'adaptive'},
    connect_timeout=5,
    read_timeout=30
)

client = boto3.client('service', config=config)
```

---

## 10. Security Architecture

### Credential Handling

```
┌─────────────────┐
│ AWS Credentials │
├─────────────────┤
│ 1. Env Vars     │ → AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
│ 2. Profile      │ → ~/.aws/credentials
│ 3. IAM Role     │ → Instance profile / ECS task role
│ 4. SSO          │ → aws sso login
└─────────────────┘
```

### Permission Requirements

| Agent | Minimum IAM Permissions |
|-------|------------------------|
| 01-fundamentals | iam:*, ce:*, organizations:* |
| 02-compute | ec2:*, autoscaling:*, ecs:*, ecr:* |
| 03-storage | s3:*, ebs:*, efs:* |
| 04-networking | ec2:*Vpc*, route53:*, cloudfront:* |
| 05-database | rds:*, dynamodb:*, elasticache:* |
| 06-security | waf:*, kms:*, secretsmanager:*, guardduty:* |
| 07-serverless | lambda:*, apigateway:*, states:* |
| 08-devops | cloudformation:*, codepipeline:*, cloudwatch:* |

---

## 11. Extensibility

### Adding New Agents

1. Create `agents/XX-aws-newdomain.md`
2. Define Role, I/O Schema, Skills Integration
3. Add to `config/agent-registry.json`
4. Create linked skills

### Adding New Skills

1. Create `skills/aws-newskill/SKILL.md`
2. Define parameters, implementation, troubleshooting
3. Add to agent's Skills Integration table
4. Add to `config/agent-registry.json`
5. Define dependencies

### Adding New Commands

1. Create `commands/aws-newcommand.md`
2. Define specification, validation, exit codes
3. Add to `config/agent-registry.json`

---

## 12. Quality Assurance

### SASMP v1.3.0 Compliance

- [x] Agents have clear scope boundaries
- [x] Skills are atomic and reusable
- [x] I/O schemas defined for all agents
- [x] Error handling tables complete
- [x] Troubleshooting decision trees present
- [x] Debug checklists included
- [x] References to official AWS docs

### EQHM (Ethical Quality Health Metrics)

- [x] No hardcoded credentials
- [x] Security best practices promoted
- [x] Cost optimization awareness
- [x] IAM least privilege guidance
- [x] Compliance frameworks referenced

---

**Architecture Version:** 3.0.0
**Last Updated:** 2025-12-30
**Status:** Production Ready
