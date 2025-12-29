# DevOps Patterns Guide

Best practices for DevOps, CI/CD, and deployment strategies.

## CI/CD Pipeline Stages

```
Code → Build → Test → Scan → Deploy → Monitor
 │      │       │      │       │        │
 │      │       │      │       │        └── Metrics, Logs, Alerts
 │      │       │      │       └── Blue/Green, Canary, Rolling
 │      │       │      └── SAST, DAST, Container Scan
 │      │       └── Unit, Integration, E2E
 │      └── Compile, Package, Container Build
 └── Commit, PR, Code Review
```

## Deployment Strategies

### Rolling Update

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 25%        # Extra pods during update
    maxUnavailable: 0    # Always maintain full capacity
```

**Pros:** Zero downtime, gradual rollout
**Cons:** Mixed versions during update

### Blue-Green Deployment

```
           ┌─────────────┐
           │   Router    │
           └──────┬──────┘
                  │
         ┌───────┴───────┐
         ▼               ▼
   ┌──────────┐    ┌──────────┐
   │  Blue    │    │  Green   │
   │ (v1.0)   │    │ (v2.0)   │
   │ ACTIVE   │    │ STANDBY  │
   └──────────┘    └──────────┘
```

**Pros:** Instant rollback, full testing in production-like env
**Cons:** Double resources needed

### Canary Deployment

```yaml
# Istio VirtualService
http:
  - route:
    - destination:
        host: myapp
        subset: stable
      weight: 90
    - destination:
        host: myapp
        subset: canary
      weight: 10
```

**Pros:** Gradual risk, real user testing
**Cons:** Complex routing, monitoring required

## GitOps Workflow

```
Developer → PR → Main Branch → Sync Tool → Cluster
    │                              │
    │                              ├── ArgoCD
    │                              ├── Flux
    │                              └── Jenkins X
    │
    └── Infrastructure as Code
        └── Helm, Kustomize, Terraform
```

### ArgoCD Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
spec:
  project: default
  source:
    repoURL: https://github.com/org/repo
    targetRevision: HEAD
    path: k8s/overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

## Monitoring & Observability

### Three Pillars

| Pillar | Purpose | Tools |
|--------|---------|-------|
| Metrics | Quantitative data over time | Prometheus, CloudWatch |
| Logs | Discrete events | ELK, Loki, CloudWatch |
| Traces | Request flow across services | Jaeger, X-Ray, Zipkin |

### Key Metrics (SRE Golden Signals)

1. **Latency** - Request duration (p50, p95, p99)
2. **Traffic** - Requests per second
3. **Errors** - Error rate percentage
4. **Saturation** - Resource utilization

### Alerting Best Practices

```yaml
# Prometheus alert example
groups:
- name: app-alerts
  rules:
  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "High error rate detected"
      description: "Error rate is {{ $value | humanizePercentage }}"
```

## Infrastructure as Code

### Environment Parity

```
                    ┌──────────┐
                    │  Module  │
                    └────┬─────┘
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐
    │   Dev    │   │ Staging  │   │   Prod   │
    │ tfvars   │   │  tfvars  │   │  tfvars  │
    └──────────┘   └──────────┘   └──────────┘
```

## Secret Management

### Workflow

```
Developer                    CI/CD                     Runtime
    │                          │                          │
    │  Store secret            │                          │
    ├─────────────────────────►│                          │
    │                          │  Retrieve secret         │
    │                          ├─────────────────────────►│
    │                          │                          │
    └──────────────────────────┴──────────────────────────┘
              Vault / AWS Secrets Manager / Azure KeyVault
```

## Disaster Recovery

### RTO/RPO Matrix

| Tier | RTO | RPO | Strategy |
|------|-----|-----|----------|
| 1 | <1 hour | <1 min | Multi-region active-active |
| 2 | <4 hours | <1 hour | Hot standby |
| 3 | <24 hours | <24 hours | Warm standby |
| 4 | <72 hours | <72 hours | Backup & restore |

## DevOps Maturity Model

| Level | Characteristics |
|-------|-----------------|
| 1 - Initial | Manual deployments, no automation |
| 2 - Managed | Basic CI, some automation |
| 3 - Defined | Full CI/CD, IaC |
| 4 - Measured | Metrics-driven, SLOs |
| 5 - Optimized | Self-healing, GitOps |

## Quick Reference Commands

```bash
# Kubernetes
kubectl rollout status deployment/myapp
kubectl rollout undo deployment/myapp
kubectl scale deployment/myapp --replicas=5

# Docker
docker build -t myapp:v1 .
docker push registry.io/myapp:v1

# Helm
helm upgrade myapp ./chart -f values-prod.yaml
helm rollback myapp 1

# ArgoCD
argocd app sync myapp
argocd app rollback myapp
```
