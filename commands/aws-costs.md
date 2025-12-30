---
name: aws_costs
description: Analyze AWS costs, trends, and generate optimization recommendations
allowed-tools: Bash, Read
sasmp_version: "1.3.0"
---

# AWS Costs Command

Comprehensive cost analysis with actionable optimization insights.

## Command Specification

| Attribute | Value |
|-----------|-------|
| Command | `/aws-costs` |
| Category | FinOps |
| Exit Codes | 0=Success, 1=API Error, 2=Auth Error, 3=No Data |
| Timeout | 60 seconds |
| Required IAM | ce:GetCostAndUsage, ce:GetCostForecast |

## Usage

```bash
/aws-costs                        # Current month summary
/aws-costs --days 30              # Last 30 days breakdown
/aws-costs --service ec2          # Filter by service
/aws-costs --forecast             # Include cost forecast
/aws-costs --recommendations      # Include optimization tips
/aws-costs --export csv           # Export to CSV format
/aws-costs --compare              # Compare to previous period
```

## Input Validation

| Parameter | Type | Validation | Default |
|-----------|------|------------|---------|
| --days | int | 1-365 | current month |
| --service | string | Valid AWS service | all |
| --granularity | string | DAILY, MONTHLY | DAILY |
| --group-by | string | SERVICE, REGION, TAG | SERVICE |
| --format | string | json, csv, table | table |

## Implementation

### Cost Retrieval
```bash
# Get current month costs by service
aws ce get-cost-and-usage \
  --time-period Start=$(date -d "$(date +%Y-%m-01)" +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics "BlendedCost" "UnblendedCost" "UsageQuantity" \
  --group-by Type=DIMENSION,Key=SERVICE \
  --output json
```

### Cost Forecast
```bash
# Get 30-day forecast
aws ce get-cost-forecast \
  --time-period Start=$(date +%Y-%m-%d),End=$(date -d "+30 days" +%Y-%m-%d) \
  --metric BLENDED_COST \
  --granularity MONTHLY
```

### Optimization Recommendations
```bash
# Get right-sizing recommendations
aws ce get-rightsizing-recommendation \
  --service AmazonEC2 \
  --configuration RecommendationTarget=SAME_INSTANCE_FAMILY,BenefitsConsidered=true
```

## Output Format

### Summary Output
```
╔══════════════════════════════════════════════════════════════╗
║                  AWS COST ANALYSIS REPORT                     ║
║                   Period: Dec 1-30, 2025                      ║
╠══════════════════════════════════════════════════════════════╣
║ TOTAL SPEND        │ $2,847.32          │ ↑ 12% vs last month ║
║ DAILY AVERAGE      │ $94.91             │ ↓ 3% vs forecast    ║
║ FORECAST (EOM)     │ $2,950.00          │ Within budget       ║
╠══════════════════════════════════════════════════════════════╣
║ TOP 5 SERVICES                                                ║
╠════════════════════╤════════════╤═══════════╤════════════════╣
║ Service            │ Cost       │ % of Total│ Trend          ║
╟────────────────────┼────────────┼───────────┼────────────────╢
║ Amazon EC2         │ $1,245.67  │ 43.7%     │ ↑ 15%          ║
║ Amazon RDS         │ $567.89    │ 19.9%     │ → 0%           ║
║ Amazon S3          │ $234.56    │ 8.2%      │ ↓ 5%           ║
║ AWS Lambda         │ $189.45    │ 6.6%      │ ↑ 25%          ║
║ Amazon CloudWatch  │ $145.23    │ 5.1%      │ ↑ 8%           ║
╚════════════════════╧════════════╧═══════════╧════════════════╝
```

### JSON Output
```json
{
  "period": {
    "start": "2025-12-01",
    "end": "2025-12-30"
  },
  "summary": {
    "total_cost": 2847.32,
    "currency": "USD",
    "daily_average": 94.91,
    "forecast_eom": 2950.00,
    "budget_status": "within_budget"
  },
  "by_service": [
    {"service": "Amazon EC2", "cost": 1245.67, "percentage": 43.7, "trend": "+15%"},
    {"service": "Amazon RDS", "cost": 567.89, "percentage": 19.9, "trend": "0%"}
  ],
  "recommendations": [
    {
      "type": "rightsizing",
      "resource": "i-0abc123",
      "current": "m5.2xlarge",
      "recommended": "m5.xlarge",
      "monthly_savings": 125.00
    }
  ]
}
```

## Cost Categories

| Category | Services | Typical % |
|----------|----------|-----------|
| Compute | EC2, Lambda, ECS, Fargate, Batch | 40-50% |
| Storage | S3, EBS, EFS, Glacier, FSx | 15-25% |
| Database | RDS, DynamoDB, ElastiCache, Redshift | 15-25% |
| Network | Data Transfer, NAT Gateway, VPN, CloudFront | 5-15% |
| Management | CloudWatch, CloudTrail, Config, SSM | 3-8% |
| Security | WAF, Shield, KMS, Secrets Manager | 1-5% |

## Exit Codes

| Code | Meaning | Common Cause |
|------|---------|--------------|
| 0 | Analysis complete | Successful run |
| 1 | API error | Rate limiting or API issues |
| 2 | Authentication failure | Missing ce:* permissions |
| 3 | No cost data | New account or no usage |
| 4 | Invalid parameters | Bad date range or filter |

## Troubleshooting

### Decision Tree
```
Command Failed?
├── Exit 1 (API Error)
│   ├── "Rate exceeded" → Wait and retry with backoff
│   └── "ServiceException" → Check AWS service status
├── Exit 2 (Auth Error)
│   ├── "AccessDeniedException"
│   │   └── Need: ce:GetCostAndUsage, ce:GetCostForecast
│   └── "UnauthorizedAccess" → Check credential validity
├── Exit 3 (No Data)
│   ├── New account? → Wait 24h for data
│   └── No usage? → Expected if no resources
└── Exit 4 (Invalid Params)
    ├── Date in future → Adjust date range
    └── Invalid service → Check service name spelling
```

### Common Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| "AccessDeniedException" | Missing Cost Explorer permissions | Attach `ce:*` IAM policy |
| Empty results | Cost Explorer not enabled | Enable in Billing Console |
| Delayed data | CE updates lag | Data available after 24h |
| "ValidationException" | Invalid date format | Use YYYY-MM-DD format |
| Stale forecast | Insufficient history | Need 30+ days of data |

### Debug Checklist

- [ ] Cost Explorer enabled in account?
- [ ] IAM has `ce:GetCostAndUsage` permission?
- [ ] Account has billing access enabled?
- [ ] Date range valid and not in future?
- [ ] Linked accounts included if using Organizations?
- [ ] Cost allocation tags activated?

## Optimization Strategies

### Immediate Actions (0-30 days)
| Strategy | Potential Savings | Effort |
|----------|------------------|--------|
| Delete unused resources | 5-20% | Low |
| Right-size over-provisioned | 10-30% | Low |
| Enable S3 Intelligent-Tiering | 5-15% | Low |
| Stop non-production after hours | 10-40% | Medium |

### Medium-term (1-6 months)
| Strategy | Potential Savings | Effort |
|----------|------------------|--------|
| Reserved Instances (1yr) | 30-40% | Medium |
| Savings Plans (1yr) | 25-35% | Medium |
| Graviton migration | 15-40% | High |
| Spot for fault-tolerant | 60-90% | High |

### Long-term (6+ months)
| Strategy | Potential Savings | Effort |
|----------|------------------|--------|
| Reserved Instances (3yr) | 50-60% | Medium |
| Architecture optimization | 20-50% | High |
| Multi-region optimization | 10-30% | High |

## Implementation Script

```python
import boto3
from datetime import datetime, timedelta

def analyze_costs(days=30, group_by='SERVICE'):
    ce = boto3.client('ce')

    end = datetime.today()
    start = end - timedelta(days=days)

    response = ce.get_cost_and_usage(
        TimePeriod={
            'Start': start.strftime('%Y-%m-%d'),
            'End': end.strftime('%Y-%m-%d')
        },
        Granularity='DAILY',
        Metrics=['BlendedCost', 'UnblendedCost'],
        GroupBy=[{'Type': 'DIMENSION', 'Key': group_by}]
    )

    # Calculate totals
    total = sum(
        float(day['Total']['BlendedCost']['Amount'])
        for day in response['ResultsByTime']
    )

    # Get forecast
    forecast = ce.get_cost_forecast(
        TimePeriod={
            'Start': end.strftime('%Y-%m-%d'),
            'End': (end + timedelta(days=30)).strftime('%Y-%m-%d')
        },
        Metric='BLENDED_COST',
        Granularity='MONTHLY'
    )

    return {
        'total': round(total, 2),
        'daily_avg': round(total / days, 2),
        'forecast': float(forecast['Total']['Amount'])
    }
```

## Related Commands

- `/aws-check` - Verify AWS connectivity
- `/aws-debug` - Debug cost anomalies
- `/aws-deploy` - Deploy cost-optimized resources

## References

- [AWS Cost Explorer API](https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/)
- [Cost Optimization Pillar](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/)
- [Savings Plans](https://aws.amazon.com/savingsplans/)
