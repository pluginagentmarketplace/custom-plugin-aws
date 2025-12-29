---
name: cloud-platforms
description: Master AWS, Azure, GCP, and cloud infrastructure for deploying and scaling applications globally with security and reliability.
sasmp_version: "1.3.0"
bonded_agent: devops-cloud
bond_type: PRIMARY_BOND
---

# Cloud Platforms & Services

## Quick Start

Choose a primary cloud provider and master its core services.

## AWS (Amazon Web Services)

### Compute Services

**EC2 (Elastic Compute Cloud)**
- Virtual machines with configurable resources
- Auto-scaling groups for dynamic capacity
- Load balancing across instances
- Security groups for network access

**Lambda**
- Serverless function execution
- Event-driven triggers (S3, API Gateway, SNS)
- Pay per invocation
- Max 15 minute execution time

**ECS/EKS**
- Container orchestration platforms
- ECS: AWS-managed, simpler
- EKS: Kubernetes-managed, more control

### Storage Services

**S3 (Simple Storage Service)**
- Object storage (files, images, backups)
- Versioning and lifecycle policies
- Server-side encryption
- CDN integration (CloudFront)

**EBS (Elastic Block Store)**
- Block storage for EC2
- Snapshots for backup
- Multiple volume types (gp3, io1, etc.)

**RDS (Relational Database Service)**
- Managed SQL databases (MySQL, PostgreSQL, MariaDB)
- Multi-AZ for high availability
- Automated backups
- Read replicas for scaling

**DynamoDB**
- NoSQL database, fully managed
- Pay per request or provisioned capacity
- Automatic scaling
- Global tables for multi-region

### Networking

**VPC (Virtual Private Cloud)**
- Isolated network environment
- Subnets, route tables, NACLs
- NAT gateways for outbound traffic
- VPC peering for cross-VPC communication

**API Gateway**
- Create and manage REST/WebSocket APIs
- Request transformation
- Rate limiting and caching
- Integration with Lambda, HTTP endpoints

**CloudFront**
- CDN (Content Delivery Network)
- Edge locations globally
- Cache control and invalidation
- DDoS protection

### Monitoring & Logging

**CloudWatch**
- Metrics and logs aggregation
- Alarms and notifications
- Dashboards
- Log retention and analysis

**X-Ray**
- Distributed tracing
- Service map visualization
- Performance analysis
- Error analysis

## Azure (Microsoft Azure)

### Compute

**App Service**
- Managed web app hosting
- Auto-scaling
- Built-in authentication
- Deployment slots

**Azure Functions**
- Serverless functions
- Multiple language support
- Bindings for integrations

**AKS (Azure Kubernetes Service)**
- Managed Kubernetes
- Integrated monitoring
- Network policies

### Data & Storage

**Cosmos DB**
- Multi-model NoSQL database
- Global distribution
- Automatic failover
- Multiple consistency levels

**Azure SQL**
- Managed SQL Server
- Elastic pools
- Point-in-time restore

**Blob Storage**
- Object storage
- Hot/cool/archive tiers
- Lifecycle management

## Google Cloud Platform (GCP)

### Compute

**Compute Engine**
- Virtual machines
- Preemptible instances (cheaper)
- Auto-scaling

**Cloud Run**
- Serverless container platform
- Scale from 0 to auto
- Pay per request
- Easy deployment from code

**GKE (Google Kubernetes Engine)**
- Managed Kubernetes
- Workload identity
- Network policies

### Data Services

**BigQuery**
- Data warehouse
- SQL analytics
- Petabyte scale
- Real-time analysis

**Cloud Datastore/Firestore**
- NoSQL document database
- Automatic scaling
- Real-time listeners

## Cloudflare

### CDN & Edge Computing

**Caching & Performance**
- Global CDN network
- Automatic cache optimization
- Image optimization

**Workers**
- Edge-computed serverless functions
- Run code at edge locations
- Low latency execution

**DDoS Protection**
- Automatic attack mitigation
- Rate limiting
- WAF (Web Application Firewall)

## Multi-Cloud Strategy

**Advantages**
- Avoid vendor lock-in
- Leverage best services from each
- Disaster recovery and redundancy

**Challenges**
- Increased complexity
- Skill requirements
- Cost management

**Best Practices**
- Use infrastructure as code (Terraform)
- Standardize API patterns
- Implement common monitoring
- Establish cost controls

## Cost Optimization

**Reserved Instances** - Commitment discounts
**Spot/Preemptible Instances** - Lower cost, interruptible
**Reserved Capacity** - Guaranteed capacity
**Auto-scaling** - Pay for what you use
**Consolidation** - Right-size resources

## Security Best Practices

**IAM (Identity & Access Management)**
- Principle of least privilege
- Role-based access control
- Service accounts for apps
- Regular access reviews

**Data Protection**
- Encryption in transit (TLS)
- Encryption at rest
- Key management services
- Secrets management (Vault, Secrets Manager)

**Network Security**
- VPCs and security groups
- NACLs and firewalls
- DDoS protection
- WAF (Web Application Firewall)

## Disaster Recovery

**Backup Strategy**
- Automated backups
- Multi-region replication
- Testing recovery procedures
- RTO/RPO targets

**High Availability**
- Multi-AZ/Region deployment
- Load balancing
- Auto-failover
- Health checks

## Roadmaps Covered

- AWS (https://roadmap.sh/aws)
- DevOps (https://roadmap.sh/devops)
