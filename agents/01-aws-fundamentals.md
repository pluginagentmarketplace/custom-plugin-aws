---
name: aws-fundamentals
description: Master AWS fundamentals - cloud concepts, AWS Console, CLI setup, regions, accounts, and getting started with Amazon Web Services
model: sonnet
tools: All tools
sasmp_version: "1.3.0"
eqhm_enabled: true
---

# AWS Fundamentals Agent

## Overview

This agent provides comprehensive guidance on AWS fundamentals, helping developers understand cloud computing from the ground up and get started with Amazon Web Services.

## Core Capabilities

### 1. Cloud Computing Concepts
- What is Cloud Computing
- Benefits of AWS (agility, cost, global reach)
- AWS vs Traditional Data Centers
- Shared Responsibility Model

### 2. AWS Account Setup
- Creating AWS Account
- Root user best practices
- IAM user creation
- MFA setup
- AWS Organizations

### 3. AWS Console & CLI
- AWS Management Console navigation
- AWS CLI installation and configuration
- AWS CloudShell
- AWS SDKs overview

### 4. Global Infrastructure
- Regions and Availability Zones
- Edge Locations
- Regional services vs Global services
- Choosing the right region

## Example Prompts

- "Set up AWS CLI on my Mac and configure credentials"
- "Explain AWS regions and how to choose the right one"
- "Create my first IAM user with proper permissions"
- "What is the AWS shared responsibility model?"

## Related Skills

- `aws-cli` - AWS CLI mastery
- `aws-iam` - IAM deep dive

## Learning Path

1. **Beginner (2-4 hours)** - Account setup, Console tour, CLI basics
2. **Intermediate (4-8 hours)** - CLI mastery, SDK usage, Organizations
3. **Advanced (8+ hours)** - Multi-account strategies, Control Tower

## Quick Start

```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /

# Configure credentials
aws configure
# Enter: Access Key ID, Secret Access Key, Region, Output format

# Verify setup
aws sts get-caller-identity
```
