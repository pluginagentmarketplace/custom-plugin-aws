---
name: containerization
description: Master Docker containerization, image optimization, and container best practices for consistent deployment across environments.
---

# Containerization & Docker

## Quick Start

Package applications consistently using Docker containers.

## Docker Fundamentals

### Core Concepts

**Image** - Blueprint/template for containers
**Container** - Running instance of an image
**Registry** - Repository of images (Docker Hub, ECR, GCR)
**Dockerfile** - Instructions to build image
**Volumes** - Persistent data storage
**Networks** - Container communication

### Dockerfile Best Practices

```dockerfile
# Multi-stage build for optimization
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY package*.json ./
RUN npm install --production
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s CMD node healthcheck.js
CMD ["node", "dist/index.js"]
```

### Image Optimization

**Minimize Layers**
- Combine RUN commands
- Use && to chain operations
- Clean up in same layer

**Use Alpine Images**
- 5MB vs 800MB base sizes
- Security updates included

**Exclude Unnecessary Files**
```
.dockerignore
node_modules
.git
.env
*.md
```

### Container Security

**Run as Non-Root**
```dockerfile
RUN useradd -m appuser
USER appuser
```

**Read-Only Filesystem**
- Mount only necessary volumes
- Security context restrictions

**Image Scanning**
- Trivy, Grype for vulnerabilities
- Regular scanning in CI/CD

## Docker Compose

```yaml
version: '3.9'
services:
  api:
    build: .
    ports:
      - "3000:3000"
    environment:
      DB_HOST: db
      DB_PASSWORD: ${DB_PASSWORD}
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ./src:/app/src

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 10s

volumes:
  db_data:
```

## Container Registries

**Docker Hub** - Public registry
**ECR (AWS)** - Private, AWS-integrated
**GCR (GCP)** - Google Container Registry
**ACR (Azure)** - Azure Container Registry

### Registry Security

- Image signing
- Access control (IAM)
- Vulnerability scanning
- Image retention policies

## Container Orchestration Intro

### Why Orchestration?

- Auto scaling
- Load balancing
- Health management
- Rolling updates
- Resource optimization

### Kubernetes vs Docker Swarm

**Kubernetes** - Industry standard, complex
**Docker Swarm** - Simple, built-in
**ECS** - AWS-native, good integration
**Nomad** - HashiCorp, flexible

## Networking

**Bridge Network** - Default, container isolation
**Host Network** - Share host networking
**Overlay Network** - Multi-host communication
**Macvlan** - Direct MAC assignment

## Storage

**Volumes** - Persistent data, managed by Docker
**Bind Mounts** - Host directory mounted
**tmpfs** - In-memory storage
**Named Volumes** - Reusable, shareable

## Monitoring Containers

**Key Metrics**
- CPU usage
- Memory consumption
- Network I/O
- Disk I/O
- Container lifecycle events

**Tools**
- Docker stats
- Prometheus collectors
- cAdvisor
- Datadog, New Relic

## Development Workflow

1. Develop locally with Docker Compose
2. Build image with optimized Dockerfile
3. Tag and push to registry
4. Deploy to orchestration platform
5. Monitor and scale

## Roadmaps Covered

- Docker (https://roadmap.sh/docker)
- DevOps (https://roadmap.sh/devops)
