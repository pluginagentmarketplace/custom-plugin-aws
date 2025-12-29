# Container Patterns Guide

Best practices for Docker and Kubernetes containerization.

## Dockerfile Best Practices

### Multi-Stage Build Pattern

```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

# Stage 2: Production
FROM node:20-alpine AS production
WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules

USER nodejs
EXPOSE 3000

CMD ["node", "dist/server.js"]
```

### Layer Optimization

```dockerfile
# BAD - Each RUN creates a layer, cache invalidation issues
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y vim
RUN rm -rf /var/lib/apt/lists/*

# GOOD - Single layer, better caching
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        vim && \
    rm -rf /var/lib/apt/lists/*
```

## Kubernetes Deployment Patterns

### Rolling Update

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: myapp
  template:
    spec:
      containers:
      - name: myapp
        image: myapp:v1
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 15
          periodSeconds: 20
```

### Blue-Green Deployment

```yaml
# Blue deployment (current)
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
    version: blue  # Switch to green when ready
  ports:
  - port: 80
    targetPort: 8080
```

### Canary Deployment (with Istio)

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp
spec:
  hosts:
  - myapp
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

## Resource Management

### Container Resources

```yaml
resources:
  requests:
    cpu: "100m"      # 0.1 CPU cores
    memory: "128Mi"  # 128 MiB
  limits:
    cpu: "500m"      # 0.5 CPU cores
    memory: "512Mi"  # 512 MiB
```

### Resource Sizing Guide

| Workload Type | CPU Request | Memory Request | CPU Limit | Memory Limit |
|--------------|-------------|----------------|-----------|--------------|
| API Service | 100m | 128Mi | 500m | 512Mi |
| Web App | 250m | 256Mi | 1000m | 1Gi |
| Worker | 500m | 512Mi | 2000m | 2Gi |
| Database | 1000m | 2Gi | 4000m | 8Gi |

## Security Patterns

### Pod Security Context

```yaml
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 2000
  containers:
  - name: app
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop: ["ALL"]
```

### Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-allow
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - port: 5432
```

## Observability

### Logging Pattern

```yaml
# Sidecar logging pattern
spec:
  containers:
  - name: app
    volumeMounts:
    - name: logs
      mountPath: /var/log/app

  - name: log-shipper
    image: fluent/fluent-bit
    volumeMounts:
    - name: logs
      mountPath: /var/log/app
      readOnly: true

  volumes:
  - name: logs
    emptyDir: {}
```

### Health Checks

| Check Type | Purpose | Failure Action |
|------------|---------|----------------|
| Startup | Wait for slow-starting apps | Keep trying |
| Liveness | Detect hung processes | Restart container |
| Readiness | Check if can serve traffic | Remove from service |

## Common Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Running as root | Security risk | `USER 1000` |
| Using :latest | Unpredictable deployments | Pin versions |
| No health checks | Dead containers serve traffic | Add probes |
| No resource limits | Noisy neighbor issues | Set limits |
| Storing secrets in images | Security breach | Use Secrets/Vault |
| Logging to files | Lost on restart | Log to stdout |
