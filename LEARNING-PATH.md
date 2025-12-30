# AWS Cloud Assistant - Learning Paths

## Guided AWS Learning Journeys

This guide provides 6 pre-designed learning paths for mastering AWS cloud services, from fundamentals to solutions architecture.

---

## Quick Path Selection

| Path | Duration | Level | Goal |
|------|----------|-------|------|
| [AWS Fundamentals](#path-1-aws-fundamentals) | 40 hrs | Beginner | Master AWS basics |
| [Compute Specialist](#path-2-compute-specialist) | 120 hrs | Intermediate | EC2 & container expertise |
| [Serverless Developer](#path-3-serverless-developer) | 100 hrs | Intermediate | Build serverless apps |
| [DevOps Engineer](#path-4-devops-engineer) | 180 hrs | Advanced | CI/CD & IaC mastery |
| [Security Specialist](#path-5-security-specialist) | 140 hrs | Advanced | Enterprise security |
| [Solutions Architect](#path-6-solutions-architect) | 400 hrs | Expert | Full AWS architecture |

---

## Path 1: AWS Fundamentals

**Duration:** 40 hours
**Level:** Beginner
**Agents:** 01-aws-fundamentals
**Skills:** aws-iam-setup, aws-cost-optimization

### Learning Objectives

- Understand AWS global infrastructure
- Configure IAM users, roles, and policies
- Navigate AWS Console and CLI
- Analyze and optimize costs

### Phase 1: AWS Basics (10 hours)

| Topic | Hours | Resources |
|-------|-------|-----------|
| AWS Global Infrastructure | 2 | Regions, AZs, Edge Locations |
| AWS Console Navigation | 2 | Services, dashboards |
| AWS CLI Setup | 3 | Installation, configuration |
| Account Best Practices | 3 | MFA, root account, Organizations |

### Phase 2: Identity & Access Management (15 hours)

**Skill:** aws-iam-setup

| Topic | Hours | Hands-on |
|-------|-------|----------|
| IAM Users & Groups | 3 | Create users, assign groups |
| IAM Policies | 5 | JSON policies, permissions |
| IAM Roles | 4 | Service roles, cross-account |
| Identity Federation | 3 | SSO, SAML, OIDC |

### Phase 3: Billing & Cost Management (15 hours)

**Skill:** aws-cost-optimization

| Topic | Hours | Hands-on |
|-------|-------|----------|
| AWS Pricing Models | 3 | On-demand, Reserved, Spot |
| Cost Explorer | 4 | Analysis, reports |
| Budgets & Alerts | 4 | Budget creation, notifications |
| Cost Optimization | 4 | Rightsizing, Savings Plans |

### Success Metrics

- [ ] Create IAM users with least privilege
- [ ] Write custom IAM policies
- [ ] Set up cost budgets and alerts
- [ ] Identify cost optimization opportunities

---

## Path 2: Compute Specialist

**Duration:** 120 hours
**Level:** Intermediate
**Agents:** 01-aws-fundamentals, 02-aws-compute, 04-aws-networking
**Skills:** aws-iam-setup, aws-vpc-design, aws-ec2-deployment, aws-ecs

### Learning Objectives

- Design and deploy VPC architectures
- Launch and manage EC2 instances
- Configure Auto Scaling
- Deploy containerized applications on ECS/Fargate

### Phase 1: Prerequisites (20 hours)

Complete AWS Fundamentals path or equivalent knowledge.

### Phase 2: Networking Foundation (25 hours)

**Skill:** aws-vpc-design

| Topic | Hours | Hands-on |
|-------|-------|----------|
| VPC Fundamentals | 5 | CIDR, subnets, routing |
| Security Groups & NACLs | 5 | Inbound/outbound rules |
| NAT Gateways | 3 | Private subnet internet access |
| VPC Peering | 4 | Cross-VPC connectivity |
| VPC Endpoints | 4 | Private AWS service access |
| Transit Gateway | 4 | Hub-spoke architecture |

### Phase 3: EC2 Mastery (40 hours)

**Skill:** aws-ec2-deployment

| Topic | Hours | Hands-on |
|-------|-------|----------|
| EC2 Instance Types | 5 | Choosing right instance |
| AMIs & Launch Templates | 5 | Custom images |
| EBS Volumes | 5 | Storage optimization |
| Auto Scaling | 10 | Policies, scaling patterns |
| Load Balancers | 10 | ALB, NLB, target groups |
| Spot Instances | 5 | Cost optimization |

### Phase 4: Container Orchestration (35 hours)

**Skill:** aws-ecs

| Topic | Hours | Hands-on |
|-------|-------|----------|
| Docker Fundamentals | 5 | Containers, images |
| ECR | 5 | Container registry |
| ECS Cluster Setup | 8 | EC2 vs Fargate |
| Task Definitions | 7 | Container configuration |
| Service Deployment | 5 | Rolling, blue/green |
| EKS Overview | 5 | Kubernetes on AWS |

### Success Metrics

- [ ] Design multi-tier VPC architecture
- [ ] Deploy Auto Scaling EC2 fleet
- [ ] Configure ALB with path-based routing
- [ ] Deploy containerized app on ECS Fargate

---

## Path 3: Serverless Developer

**Duration:** 100 hours
**Level:** Intermediate
**Agents:** 01-aws-fundamentals, 07-aws-serverless, 05-aws-database
**Skills:** aws-iam-setup, aws-lambda-functions, aws-rds-setup

### Learning Objectives

- Build event-driven serverless applications
- Design API Gateway endpoints
- Implement Step Functions workflows
- Connect to managed databases

### Phase 1: Prerequisites (15 hours)

Complete AWS Fundamentals path or equivalent.

### Phase 2: Lambda Mastery (35 hours)

**Skill:** aws-lambda-functions

| Topic | Hours | Hands-on |
|-------|-------|----------|
| Lambda Fundamentals | 5 | Runtime, handlers |
| Packaging & Deployment | 5 | ZIP, Layers, SAM |
| Triggers & Events | 8 | S3, API GW, EventBridge |
| Environment & Config | 5 | Variables, secrets |
| Performance Tuning | 7 | Memory, cold starts |
| Error Handling | 5 | DLQ, retry strategies |

### Phase 3: API Gateway (20 hours)

| Topic | Hours | Hands-on |
|-------|-------|----------|
| REST APIs | 6 | Resources, methods |
| HTTP APIs | 4 | Simplified design |
| Authorization | 5 | Cognito, Lambda authorizers |
| Throttling & Caching | 5 | Rate limits, cache |

### Phase 4: Step Functions (15 hours)

| Topic | Hours | Hands-on |
|-------|-------|----------|
| State Machine Basics | 5 | States, transitions |
| Error Handling | 5 | Catch, retry |
| Parallel Execution | 5 | Map, parallel states |

### Phase 5: Database Integration (15 hours)

**Skill:** aws-rds-setup

| Topic | Hours | Hands-on |
|-------|-------|----------|
| RDS Basics | 5 | Instance setup |
| DynamoDB | 5 | NoSQL patterns |
| Aurora Serverless | 5 | Scaling, Data API |

### Success Metrics

- [ ] Build REST API with Lambda backend
- [ ] Implement multi-step workflow
- [ ] Connect Lambda to RDS/DynamoDB
- [ ] Deploy using SAM/CloudFormation

---

## Path 4: DevOps Engineer

**Duration:** 180 hours
**Level:** Advanced
**Agents:** 01-aws-fundamentals, 02-aws-compute, 08-aws-devops
**Skills:** aws-iam-setup, aws-vpc-design, aws-ec2-deployment, aws-ecs, aws-cloudformation, aws-codepipeline, aws-cloudwatch

### Learning Objectives

- Implement Infrastructure as Code
- Build CI/CD pipelines
- Configure monitoring and alerting
- Manage container platforms

### Phase 1: Prerequisites (30 hours)

Complete Compute Specialist path or equivalent.

### Phase 2: Infrastructure as Code (45 hours)

**Skill:** aws-cloudformation

| Topic | Hours | Hands-on |
|-------|-------|----------|
| CloudFormation Basics | 8 | Templates, stacks |
| Intrinsic Functions | 7 | Ref, GetAtt, Sub |
| Nested Stacks | 5 | Modular design |
| Change Sets | 5 | Safe updates |
| AWS CDK | 10 | TypeScript/Python IaC |
| Terraform Basics | 10 | Multi-cloud IaC |

### Phase 3: CI/CD Pipelines (40 hours)

**Skill:** aws-codepipeline

| Topic | Hours | Hands-on |
|-------|-------|----------|
| CodeCommit | 5 | Git repository |
| CodeBuild | 10 | Build projects, buildspec |
| CodeDeploy | 10 | Deployment strategies |
| CodePipeline | 10 | Pipeline orchestration |
| GitHub Actions | 5 | Alternative CI/CD |

### Phase 4: Monitoring & Observability (35 hours)

**Skill:** aws-cloudwatch

| Topic | Hours | Hands-on |
|-------|-------|----------|
| CloudWatch Metrics | 8 | Custom metrics, dashboards |
| CloudWatch Logs | 8 | Log groups, insights |
| CloudWatch Alarms | 7 | Alerts, notifications |
| X-Ray | 7 | Distributed tracing |
| EventBridge | 5 | Event-driven automation |

### Phase 5: Container Platforms (30 hours)

**Skill:** aws-ecs

| Topic | Hours | Hands-on |
|-------|-------|----------|
| ECS with CI/CD | 10 | Pipeline integration |
| EKS Basics | 10 | Kubernetes on AWS |
| Service Discovery | 5 | Cloud Map |
| App Mesh | 5 | Service mesh |

### Success Metrics

- [ ] Deploy 3-tier app with CloudFormation
- [ ] Build complete CI/CD pipeline
- [ ] Create monitoring dashboard with alarms
- [ ] Implement blue/green deployment

---

## Path 5: Security Specialist

**Duration:** 140 hours
**Level:** Advanced
**Agents:** 01-aws-fundamentals, 04-aws-networking, 06-aws-security
**Skills:** aws-iam-setup, aws-vpc-design, aws-security-best-practices

### Learning Objectives

- Implement defense in depth
- Configure encryption and key management
- Design network security controls
- Achieve compliance frameworks

### Phase 1: Prerequisites (20 hours)

Complete AWS Fundamentals path or equivalent.

### Phase 2: Identity Security (30 hours)

**Skill:** aws-iam-setup

| Topic | Hours | Hands-on |
|-------|-------|----------|
| Advanced IAM Policies | 8 | Conditions, boundaries |
| AWS Organizations | 7 | SCPs, multi-account |
| AWS SSO | 5 | Identity Center |
| Secrets Management | 5 | Secrets Manager, Parameter Store |
| Certificate Management | 5 | ACM |

### Phase 3: Network Security (35 hours)

**Skill:** aws-vpc-design

| Topic | Hours | Hands-on |
|-------|-------|----------|
| Security Groups | 5 | Least privilege |
| NACLs | 5 | Stateless filtering |
| WAF | 10 | Web application firewall |
| Shield | 5 | DDoS protection |
| Network Firewall | 10 | Deep inspection |

### Phase 4: Data Protection (30 hours)

**Skill:** aws-security-best-practices

| Topic | Hours | Hands-on |
|-------|-------|----------|
| KMS | 10 | Key management |
| CloudHSM | 5 | Hardware security modules |
| S3 Encryption | 5 | Server-side, client-side |
| RDS Encryption | 5 | At-rest, in-transit |
| Macie | 5 | Data discovery |

### Phase 5: Detection & Response (25 hours)

| Topic | Hours | Hands-on |
|-------|-------|----------|
| GuardDuty | 7 | Threat detection |
| Security Hub | 8 | Centralized security |
| Inspector | 5 | Vulnerability scanning |
| Incident Response | 5 | Runbooks, automation |

### Success Metrics

- [ ] Design multi-account security architecture
- [ ] Implement WAF rules for OWASP Top 10
- [ ] Configure encryption with KMS CMKs
- [ ] Set up Security Hub with compliance

---

## Path 6: Solutions Architect

**Duration:** 400 hours
**Level:** Expert
**Agents:** All 8 agents
**Skills:** All 12 skills

### Learning Objectives

- Design highly available architectures
- Implement disaster recovery
- Optimize cost and performance
- Architect for compliance

### Phase 1: Foundation (40 hours)

Complete AWS Fundamentals path.

### Phase 2: Compute & Networking (80 hours)

Complete Compute Specialist path.

### Phase 3: Serverless & Database (60 hours)

| Topic | Hours | Skills |
|-------|-------|--------|
| Serverless Patterns | 30 | aws-lambda-functions |
| Database Selection | 15 | aws-rds-setup |
| Data Architecture | 15 | Multi-DB strategies |

### Phase 4: Security & Compliance (60 hours)

Complete Security Specialist path core modules.

### Phase 5: DevOps & Automation (80 hours)

Complete DevOps Engineer path core modules.

### Phase 6: Advanced Architecture (80 hours)

| Topic | Hours | Focus |
|-------|-------|-------|
| High Availability | 20 | Multi-AZ, multi-region |
| Disaster Recovery | 20 | RTO/RPO strategies |
| Cost Optimization | 20 | FinOps practices |
| Performance | 20 | Latency, throughput |

### Success Metrics

- [ ] Design multi-region active-active
- [ ] Implement DR with RPO < 1 hour
- [ ] Achieve 99.99% availability
- [ ] Optimize costs by 30%+
- [ ] Pass AWS Solutions Architect exam

---

## Skill Dependencies

```
aws-iam-setup (Foundation - Start Here)
    │
    ├── aws-vpc-design
    │   ├── aws-ec2-deployment
    │   │   ├── aws-rds-setup (needs VPC + EC2)
    │   │   └── aws-ecs (needs VPC + EC2)
    │   └── (direct VPC skills)
    │
    ├── aws-s3-management
    │
    ├── aws-lambda-functions
    │
    ├── aws-security-best-practices
    │
    ├── aws-cloudwatch
    │
    ├── aws-cloudformation
    │   └── aws-codepipeline (needs CFN)
    │
    └── aws-cost-optimization
```

---

## Assessment Checkpoints

Each path includes:

| Checkpoint | Type | Passing Score |
|------------|------|---------------|
| Knowledge Quiz | Multiple choice | 80% |
| Hands-on Lab | Practical | Complete all tasks |
| Architecture Review | Design | Meets requirements |
| Cost Analysis | FinOps | Optimized design |

---

## Certification Alignment

| Path | AWS Certification |
|------|-------------------|
| AWS Fundamentals | Cloud Practitioner |
| Compute Specialist | SysOps Administrator |
| Serverless Developer | Developer Associate |
| DevOps Engineer | DevOps Engineer Professional |
| Security Specialist | Security Specialty |
| Solutions Architect | Solutions Architect Professional |

---

## Tips for Success

1. **Follow prerequisites** - Each path builds on previous knowledge
2. **Hands-on practice** - Theory alone isn't enough
3. **Use AWS Free Tier** - Practice without cost
4. **Clean up resources** - Avoid surprise bills
5. **Join communities** - Learn from others
6. **Build projects** - Apply knowledge practically
7. **Review regularly** - Spaced repetition works

---

**Ready to start?** Choose your path and begin your AWS journey!

---

**Learning Paths Version:** 3.0.0
**Last Updated:** 2025-12-30
**Status:** Production Ready
