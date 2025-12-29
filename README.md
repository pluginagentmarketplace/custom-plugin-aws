<div align="center">

<!-- Animated Typing Banner -->
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=28&duration=3000&pause=1000&color=2E9EF7&center=true&vCenter=true&multiline=true&repeat=true&width=600&height=100&lines=Aws+Assistant;8+Agents+%7C+12+Skills;Claude+Code+Plugin" alt="Aws Assistant" />

<br/>

<!-- Badge Row 1: Status Badges -->
[![Version](https://img.shields.io/badge/Version-2.0.0-blue?style=for-the-badge)](https://github.com/pluginagentmarketplace/custom-plugin-aws/releases)
[![License](https://img.shields.io/badge/License-Custom-yellow?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-brightgreen?style=for-the-badge)](#)
[![SASMP](https://img.shields.io/badge/SASMP-v1.3.0-blueviolet?style=for-the-badge)](#)

<!-- Badge Row 2: Content Badges -->
[![Agents](https://img.shields.io/badge/Agents-8-orange?style=flat-square&logo=robot)](#-agents)
[![Skills](https://img.shields.io/badge/Skills-12-purple?style=flat-square&logo=lightning)](#-skills)
[![Commands](https://img.shields.io/badge/Commands-4-green?style=flat-square&logo=terminal)](#-commands)

<br/>

<!-- Quick CTA Row -->
[📦 **Install Now**](#-quick-start) · [🤖 **Explore Agents**](#-agents) · [📖 **Documentation**](#-documentation) · [⭐ **Star this repo**](https://github.com/pluginagentmarketplace/custom-plugin-aws)

---

### What is this?

> **Aws Assistant** is a Claude Code plugin with **8 agents** and **12 skills** for aws development.

</div>

---

## 📑 Table of Contents

<details>
<summary>Click to expand</summary>

- [Quick Start](#-quick-start)
- [Features](#-features)
- [Agents](#-agents)
- [Skills](#-skills)
- [Commands](#-commands)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

</details>

---

## 🚀 Quick Start

### Prerequisites

- Claude Code CLI v2.0.27+
- Active Claude subscription

### Installation (Choose One)

<details open>
<summary><strong>Option 1: From Marketplace (Recommended)</strong></summary>

```bash
# Step 1️⃣ Add the marketplace
/plugin add marketplace pluginagentmarketplace/custom-plugin-aws

# Step 2️⃣ Install the plugin
/plugin install aws-development-assistant@pluginagentmarketplace-aws

# Step 3️⃣ Restart Claude Code
# Close and reopen your terminal/IDE
```

</details>

<details>
<summary><strong>Option 2: Local Installation</strong></summary>

```bash
# Clone the repository
git clone https://github.com/pluginagentmarketplace/custom-plugin-aws.git
cd custom-plugin-aws

# Load locally
/plugin load .

# Restart Claude Code
```

</details>

### ✅ Verify Installation

After restart, you should see these agents:

```
aws-development-assistant:04-aws-networking
aws-development-assistant:02-aws-iam
aws-development-assistant:01-aws-fundamentals
aws-development-assistant:08-aws-devops
aws-development-assistant:03-aws-compute
... and 3 more
```

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **8 Agents** | Specialized AI agents for aws tasks |
| 🛠️ **12 Skills** | Reusable capabilities with Golden Format |
| ⌨️ **4 Commands** | Quick slash commands |
| 🔄 **SASMP v1.3.0** | Full protocol compliance |

---

## 🤖 Agents

### 8 Specialized Agents

| # | Agent | Purpose |
|---|-------|---------|
| 1 | **04-aws-networking** | Master AWS networking - VPC, subnets, Route 53, CloudFront,  |
| 2 | **02-aws-iam** | Master AWS IAM - Identity and Access Management, policies, r |
| 3 | **01-aws-fundamentals** | Master AWS fundamentals - cloud concepts, AWS Console, CLI s |
| 4 | **08-aws-devops** | Master AWS DevOps - CloudWatch, CloudFormation, CDK, CodePip |
| 5 | **03-aws-compute** | Master AWS compute services - EC2 instances, Auto Scaling, L |
| 6 | **07-aws-serverless** | Master AWS serverless - Lambda, API Gateway, Step Functions, |
| 7 | **05-aws-storage** | Master AWS storage services - S3, EBS, EFS, FSx, Storage Gat |
| 8 | **06-aws-databases** | Master AWS database services - RDS, Aurora, DynamoDB, Elasti |

---

## 🛠️ Skills

### Available Skills

| Skill | Description | Invoke |
|-------|-------------|--------|
| `aws-dynamodb` | Master AWS DynamoDB - NoSQL tables, indexes, and data modeli | `Skill("aws-development-assistant:aws-dynamodb")` |
| `aws-vpc` | Master AWS VPC - networking, subnets, route tables, and netw | `Skill("aws-development-assistant:aws-vpc")` |
| `aws-rds` | Master AWS RDS - relational databases, Aurora, and managed d | `Skill("aws-development-assistant:aws-rds")` |
| `aws-s3` | Master AWS S3 - buckets, objects, policies, and storage mana | `Skill("aws-development-assistant:aws-s3")` |
| `aws-ec2` | Master AWS EC2 - instances, AMIs, security groups, and compu | `Skill("aws-development-assistant:aws-ec2")` |
| `aws-iam` | Master AWS IAM - policies, roles, users, groups, and securit | `Skill("aws-development-assistant:aws-iam")` |
| `aws-security` | Master AWS security - best practices, compliance, and securi | `Skill("aws-development-assistant:aws-security")` |
| `aws-lambda` | Master AWS Lambda - serverless functions, triggers, and even | `Skill("aws-development-assistant:aws-lambda")` |
| `aws-cloudwatch` | Master AWS CloudWatch - metrics, logs, alarms, and monitorin | `Skill("aws-development-assistant:aws-cloudwatch")` |
| `aws-containers` | Master AWS containers - ECS, EKS, Fargate, and ECR | `Skill("aws-development-assistant:aws-containers")` |
| ... | +2 more | See skills/ directory |

---

## ⌨️ Commands

| Command | Description |
|---------|-------------|
| `/aws-debug` | Debug AWS issues and troubleshoot common problems |
| `/aws-costs` | Analyze AWS costs and get cost optimization recommendations |
| `/aws-deploy` | Deploy applications to AWS using various services |
| `/aws-check` | Check AWS CLI configuration and connectivity |

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [CHANGELOG.md](CHANGELOG.md) | Version history |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute |
| [LICENSE](LICENSE) | License information |

---

## 📁 Project Structure

<details>
<summary>Click to expand</summary>

```
custom-plugin-aws/
├── 📁 .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── 📁 agents/              # 8 agents
├── 📁 skills/              # 12 skills (Golden Format)
├── 📁 commands/            # 4 commands
├── 📁 hooks/
├── 📄 README.md
├── 📄 CHANGELOG.md
└── 📄 LICENSE
```

</details>

---

## 📅 Metadata

| Field | Value |
|-------|-------|
| **Version** | 2.0.0 |
| **Last Updated** | 2025-12-29 |
| **Status** | Production Ready |
| **SASMP** | v1.3.0 |
| **Agents** | 8 |
| **Skills** | 12 |
| **Commands** | 4 |

---

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md).

1. Fork the repository
2. Create your feature branch
3. Follow the Golden Format for new skills
4. Submit a pull request

---

## ⚠️ Security

> **Important:** This repository contains third-party code and dependencies.
>
> - ✅ Always review code before using in production
> - ✅ Check dependencies for known vulnerabilities
> - ✅ Follow security best practices
> - ✅ Report security issues privately via [Issues](../../issues)

---

## 📝 License

Copyright © 2025 **Dr. Umit Kacar** & **Muhsin Elcicek**

Custom License - See [LICENSE](LICENSE) for details.

---

## 👥 Contributors

<table>
<tr>
<td align="center">
<strong>Dr. Umit Kacar</strong><br/>
Senior AI Researcher & Engineer
</td>
<td align="center">
<strong>Muhsin Elcicek</strong><br/>
Senior Software Architect
</td>
</tr>
</table>

---

<div align="center">

**Made with ❤️ for the Claude Code Community**

[![GitHub](https://img.shields.io/badge/GitHub-pluginagentmarketplace-black?style=for-the-badge&logo=github)](https://github.com/pluginagentmarketplace)

</div>
