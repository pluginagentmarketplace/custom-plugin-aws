<div align="center">

<!-- Animated Typing Banner -->
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=28&duration=3000&pause=1000&color=FF9900&center=true&vCenter=true&multiline=true&repeat=true&width=700&height=100&lines=AWS+Cloud+Assistant;8+Agents+%7C+12+Skills+%7C+4+Commands;Production-Grade+Claude+Code+Plugin" alt="AWS Cloud Assistant" />

<br/>

<!-- Badge Row 1: Status Badges -->
[![Version](https://img.shields.io/badge/Version-3.0.0-FF9900?style=for-the-badge)](https://github.com/pluginagentmarketplace/custom-plugin-aws/releases)
[![License](https://img.shields.io/badge/License-Custom-yellow?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-brightgreen?style=for-the-badge)](#)
[![SASMP](https://img.shields.io/badge/SASMP-v1.3.0-blueviolet?style=for-the-badge)](#)
[![EQHM](https://img.shields.io/badge/EQHM-Enabled-blue?style=for-the-badge)](#)

<!-- Badge Row 2: Content Badges -->
[![Agents](https://img.shields.io/badge/Agents-8-orange?style=flat-square&logo=robot)](#-agents)
[![Skills](https://img.shields.io/badge/Skills-12-purple?style=flat-square&logo=lightning)](#-skills)
[![Commands](https://img.shields.io/badge/Commands-4-green?style=flat-square&logo=terminal)](#-commands)

<br/>

<!-- Quick CTA Row -->
[**Install Now**](#-quick-start) | [**Explore Agents**](#-agents) | [**View Skills**](#-skills) | [**Documentation**](#-documentation)

---

### What is this?

> **AWS Cloud Assistant** is a production-grade Claude Code plugin with **8 specialized agents**, **12 atomic skills**, and **4 diagnostic commands** for AWS cloud development, following **2024-2025 AWS best practices**.

</div>

---

## Table of Contents

- [Quick Start](#-quick-start)
- [Features](#-features)
- [Agents](#-agents)
- [Skills](#-skills)
- [Commands](#-commands)
- [Learning Paths](#-learning-paths)
- [Architecture](#-architecture)
- [Documentation](#-documentation)
- [Contributing](#-contributing)

---

## Quick Start

### Prerequisites

- Claude Code CLI v2.0.27+
- Active Claude subscription
- AWS CLI v2 installed and configured

### Installation

**Option 1: From Marketplace (Recommended)**

```bash
# Add the marketplace
/plugin marketplace add pluginagentmarketplace/custom-plugin-aws

# Install the plugin
/plugin install aws-cloud-assistant@pluginagentmarketplace-aws

# Restart Claude Code
```

**Option 2: Local Installation**

```bash
# Clone the repository
git clone https://github.com/pluginagentmarketplace/custom-plugin-aws.git
cd custom-plugin-aws

# Load locally
/plugin load .

# Restart Claude Code
```

### Verify Installation

After restart, verify agents are loaded:

```
aws-cloud-assistant:01-aws-fundamentals
aws-cloud-assistant:02-aws-compute
aws-cloud-assistant:03-aws-storage
aws-cloud-assistant:04-aws-networking
aws-cloud-assistant:05-aws-database
aws-cloud-assistant:06-aws-security
aws-cloud-assistant:07-aws-serverless
aws-cloud-assistant:08-aws-devops
```

---

## Features

| Feature | Description |
|---------|-------------|
| **8 Specialized Agents** | Domain-specific AWS architects with clear scope boundaries |
| **12 Atomic Skills** | Production-grade skills with retry logic and troubleshooting |
| **4 Diagnostic Commands** | CLI tools with exit codes and validation |
| **I/O Schemas** | JSON schemas for all agent inputs/outputs |
| **Error Handling** | Comprehensive error tables with recovery strategies |
| **Decision Trees** | Visual troubleshooting guides for common issues |
| **SASMP v1.3.0** | Full protocol compliance |
| **EQHM Enabled** | Ethical Quality Health Metrics active |

---

## Agents

### 8 Specialized AWS Agents

| # | Agent | Domain | Primary Skills |
|---|-------|--------|----------------|
| 1 | **01-aws-fundamentals** | IAM, Billing, Account Setup | aws-iam-setup, aws-cost-optimization |
| 2 | **02-aws-compute** | EC2, Auto Scaling, ECS/EKS | aws-ec2-deployment, aws-ecs |
| 3 | **03-aws-storage** | S3, EBS, EFS, Glacier | aws-s3-management |
| 4 | **04-aws-networking** | VPC, Route53, CloudFront | aws-vpc-design |
| 5 | **05-aws-database** | RDS, Aurora, DynamoDB | aws-rds-setup |
| 6 | **06-aws-security** | WAF, KMS, GuardDuty | aws-security-best-practices |
| 7 | **07-aws-serverless** | Lambda, API Gateway, Step Functions | aws-lambda-functions |
| 8 | **08-aws-devops** | CloudFormation, CodePipeline, CloudWatch | aws-cloudformation, aws-codepipeline |

### Agent Capabilities

Each agent includes:
- **Role & Responsibilities** with clear scope boundaries
- **Input/Output JSON Schemas** for structured interactions
- **Skills Integration** with PRIMARY/SECONDARY bonds
- **Error Handling Tables** with recovery strategies
- **Fallback Strategies** for graceful degradation
- **Troubleshooting Decision Trees** for issue diagnosis
- **Debug Checklists** for systematic verification

---

## Skills

### 12 Production-Grade Skills

| Skill | Agent Bond | Complexity | Time Estimate |
|-------|------------|------------|---------------|
| `aws-iam-setup` | 01-fundamentals | Medium | 15-30 min |
| `aws-ec2-deployment` | 02-compute | Medium | 5-15 min |
| `aws-s3-management` | 03-storage | Medium | 10-20 min |
| `aws-vpc-design` | 04-networking | High | 30-60 min |
| `aws-rds-setup` | 05-database | Medium-High | 20-45 min |
| `aws-lambda-functions` | 07-serverless | Medium | 10-30 min |
| `aws-security-best-practices` | 06-security | High | 30-60 min |
| `aws-cloudformation` | 08-devops | Medium-High | 10-60 min |
| `aws-codepipeline` | 08-devops | Medium | 20-45 min |
| `aws-cloudwatch` | 08-devops | Medium | 15-30 min |
| `aws-ecs` | 08-devops | Medium-High | 20-45 min |
| `aws-cost-optimization` | 01-fundamentals | Medium | 15-30 min |

### Skill Capabilities

Each skill includes:
- **Quick Reference Table** with complexity and time estimates
- **Required/Optional Parameters** with validation rules
- **Implementation Examples** (Bash, Python, CloudFormation)
- **Retry Logic** with exponential backoff patterns
- **Troubleshooting Tables** with symptom-cause-solution
- **Debug Checklists** for systematic verification
- **Test Templates** for validation
- **AWS Documentation References**

---

## Commands

### 4 Diagnostic Commands

| Command | Category | Description |
|---------|----------|-------------|
| `/aws-check` | Diagnostics | Verify AWS CLI, credentials, and connectivity |
| `/aws-costs` | FinOps | Analyze costs and get optimization recommendations |
| `/aws-deploy` | Deployment | Deploy applications to Lambda, ECS, EC2, S3 |
| `/aws-debug` | Diagnostics | Troubleshoot EC2, Lambda, ECS, RDS, VPC issues |

### Command Capabilities

Each command includes:
- **Command Specification** with exit codes
- **Input Validation** with regex patterns
- **Implementation Scripts** (Bash, Python)
- **Decision Tree Troubleshooting**
- **Debug Checklists**
- **Related Commands** cross-references

---

## Learning Paths

### 6 AWS Learning Journeys

| Path | Duration | Agents | Skills |
|------|----------|--------|--------|
| **AWS Fundamentals** | 40 hrs | 1 | 2 |
| **Compute Specialist** | 120 hrs | 3 | 4 |
| **Serverless Developer** | 100 hrs | 3 | 3 |
| **DevOps Engineer** | 180 hrs | 3 | 7 |
| **Security Specialist** | 140 hrs | 3 | 3 |
| **Solutions Architect** | 400 hrs | 8 | 12 |

---

## Architecture

```
custom-plugin-aws/
├── .claude-plugin/
│   ├── plugin.json          # Plugin manifest
│   └── marketplace.json     # Marketplace metadata
├── agents/                   # 8 specialized agents
│   ├── 01-aws-fundamentals.md
│   ├── 02-aws-compute.md
│   ├── 03-aws-storage.md
│   ├── 04-aws-networking.md
│   ├── 05-aws-database.md
│   ├── 06-aws-security.md
│   ├── 07-aws-serverless.md
│   └── 08-aws-devops.md
├── skills/                   # 12 atomic skills
│   ├── aws-iam-setup/
│   ├── aws-ec2-deployment/
│   ├── aws-s3-management/
│   ├── aws-vpc-design/
│   ├── aws-rds-setup/
│   ├── aws-lambda-functions/
│   ├── aws-security-best-practices/
│   ├── aws-cloudformation/
│   ├── aws-codepipeline/
│   ├── aws-cloudwatch/
│   ├── aws-ecs/
│   └── aws-cost-optimization/
├── commands/                 # 4 diagnostic commands
│   ├── aws-check.md
│   ├── aws-costs.md
│   ├── aws-deploy.md
│   └── aws-debug.md
├── config/
│   └── agent-registry.json   # Agent-skill mappings
├── hooks/
│   └── hooks.json
├── ARCHITECTURE.md
├── LEARNING-PATH.md
├── CHANGELOG.md
└── README.md
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design and component details |
| [LEARNING-PATH.md](LEARNING-PATH.md) | AWS learning journeys |
| [CHANGELOG.md](CHANGELOG.md) | Version history |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidelines |

---

## Metadata

| Field | Value |
|-------|-------|
| **Version** | 3.0.0 |
| **Last Updated** | 2025-12-30 |
| **Status** | Production Ready |
| **SASMP** | v1.3.0 |
| **EQHM** | Enabled |
| **Agents** | 8 |
| **Skills** | 12 |
| **Commands** | 4 |
| **Learning Paths** | 6 |

---

## Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md).

1. Fork the repository
2. Create feature branch
3. Follow SASMP v1.3.0 format
4. Submit pull request

---

## Security

> **Important:** This plugin interacts with AWS services.
>
> - Always review IAM permissions before use
> - Never commit AWS credentials
> - Follow AWS security best practices
> - Report security issues via [Issues](../../issues)

---

## License

Copyright 2025 **Dr. Umit Kacar** & **Muhsin Elcicek**

Custom License - See [LICENSE](LICENSE) for details.

---

## Contributors

| **Dr. Umit Kacar** | **Muhsin Elcicek** |
|:------------------:|:------------------:|
| Senior AI Researcher & Engineer | Senior Software Architect |

---

<div align="center">

**Made with care for the Claude Code Community**

[![GitHub](https://img.shields.io/badge/GitHub-pluginagentmarketplace-black?style=for-the-badge&logo=github)](https://github.com/pluginagentmarketplace)

</div>
