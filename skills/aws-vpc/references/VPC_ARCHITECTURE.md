# VPC Architecture Patterns

## 1. Basic Public VPC

```
Internet
    │
Internet Gateway
    │
┌───────────────────────────────────┐
│  VPC (10.0.0.0/16)                │
│  ┌─────────────────────────────┐  │
│  │ Public Subnet (10.0.1.0/24) │  │
│  │    - EC2 instances          │  │
│  │    - ALB                    │  │
│  └─────────────────────────────┘  │
└───────────────────────────────────┘
```

## 2. Public + Private VPC (Recommended)

```
Internet
    │
Internet Gateway
    │
┌───────────────────────────────────────────────┐
│  VPC (10.0.0.0/16)                            │
│  ┌─────────────────┐  ┌─────────────────┐     │
│  │ Public Subnet   │  │ Public Subnet   │     │
│  │ (10.0.1.0/24)   │  │ (10.0.2.0/24)   │     │
│  │   - ALB         │  │   - NAT GW      │     │
│  │   - Bastion     │  │                 │     │
│  └────────┬────────┘  └────────┬────────┘     │
│           │                    │              │
│  ┌────────┴────────┐  ┌────────┴────────┐     │
│  │ Private Subnet  │  │ Private Subnet  │     │
│  │ (10.0.10.0/24)  │  │ (10.0.11.0/24)  │     │
│  │   - App servers │  │   - App servers │     │
│  └────────┬────────┘  └────────┬────────┘     │
│           │                    │              │
│  ┌────────┴────────┐  ┌────────┴────────┐     │
│  │ Private Subnet  │  │ Private Subnet  │     │
│  │ (10.0.20.0/24)  │  │ (10.0.21.0/24)  │     │
│  │   - Databases   │  │   - Databases   │     │
│  └─────────────────┘  └─────────────────┘     │
└───────────────────────────────────────────────┘
```

## 3. Multi-Account VPC (Transit Gateway)

```
┌─────────────────┐  ┌─────────────────┐
│ Production VPC  │  │ Development VPC │
│ 10.0.0.0/16     │  │ 10.1.0.0/16     │
└────────┬────────┘  └────────┬────────┘
         │                    │
         └──────┬─────────────┘
                │
        ┌───────┴───────┐
        │ Transit       │
        │ Gateway       │
        └───────┬───────┘
                │
        ┌───────┴───────┐
        │ Shared        │
        │ Services VPC  │
        │ 10.2.0.0/16   │
        └───────────────┘
```

## CIDR Planning

| VPC Size | CIDR | Hosts | Use Case |
|----------|------|-------|----------|
| Small | /24 | 256 | Dev/Test |
| Medium | /20 | 4096 | Small prod |
| Large | /16 | 65536 | Enterprise |

## Subnet Strategy

- **2+ AZs** for high availability
- **/24 per subnet** (251 usable IPs)
- **Separate tiers**: Public, Private, Database
- **Reserved CIDRs** for future growth

## Security Best Practices

1. **Public subnets**: Only for load balancers, bastion
2. **Private subnets**: Application servers
3. **Isolated subnets**: Databases (no NAT)
4. **VPC Flow Logs**: Enable for troubleshooting
5. **Security Groups**: Least privilege
