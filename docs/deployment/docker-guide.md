# Docker Deployment Guide for Fintech Applications

## 🐳 Overview

This guide provides comprehensive Docker deployment strategies for fintech applications, focusing on security, scalability, and compliance requirements. Learn to containerize microservices, manage secrets, and implement production-ready deployments.

## 🏗️ Container Architecture

### Microservices Container Strategy

```yaml
# docker-compose.yml - Development Environment
version: '3.8'

services:
  # API Gateway
  api-gateway:
    build:
      context: ./backend/api-gateway
      dockerfile: Dockerfile
      target: development
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - JWT_SECRET=${JWT_SECRET}
    volumes:
      - ./backend/api-gateway:/app
      - /app/node_modules
    depends_on:
      - postgres
      - redis
    networks:
      - fintech-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # User Service
  user-service:
    build:
      context: ./backend/services/user-service
      dockerfile: Dockerfile
    environment:
      - NODE_ENV=development
      - DATABASE_URL=${DATABASE_URL}
      - KYC_SERVICE_URL=${KYC_SERVICE_URL}
    depends_on:
      - postgres
    networks:
      - fintech-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3001/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Payment Service
  payment-service:
    build:
      context: ./backend/services/payment-service
      dockerfile: Dockerfile
    environment:
      - NODE_ENV=development
      - DATABASE_URL=${DATABASE_URL}
      - STRIPE_SECRET_KEY=${STRIPE_SECRET_KEY}
      - PCI_COMPLIANCE_MODE=true
    depends_on:
      - postgres
      - redis
    networks:
      - fintech-network
    secrets:
      - stripe_secret_key
      - encryption_key
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3002/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Database
  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    networks:
      - fintech-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - fintech-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3

  # Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      target: development
    ports:
      - "3100:3100"
    environment:
      - REACT_APP_API_URL=http://localhost:3000
      - REACT_APP_ENVIRONMENT=development
    volumes:
      - ./frontend:/app
      - /app/node_modules
    depends_on:
      - api-gateway
    networks:
      - fintech-network

volumes:
  postgres_data:
  redis_data:

networks:
  fintech-network:
    driver: bridge

secrets:
  stripe_secret_key:
    file: ./secrets/stripe_secret_key.txt
  encryption_key:
    file: ./secrets/encryption_key.txt
```

## 🔒 Security-First Dockerfile

### Production-Ready Node.js Dockerfile

```dockerfile
# Multi-stage build for Node.js microservice
FROM node:18-alpine AS base

# Install security updates
RUN apk update && apk upgrade && apk add --no-cache dumb-init

# Create app user for security
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./
COPY tsconfig.json ./

# Development stage
FROM base AS development
ENV NODE_ENV=development
RUN npm ci --include=dev
COPY . .
USER nextjs
EXPOSE 3000
CMD ["dumb-init", "npm", "run", "dev"]

# Build stage
FROM base AS builder
ENV NODE_ENV=production
RUN npm ci --only=production && npm cache clean --force
COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine AS production

# Install security updates
RUN apk update && apk upgrade && apk add --no-cache dumb-init

# Create app user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

WORKDIR /app

# Copy built application
COPY --from=builder --chown=nextjs:nodejs /app/dist ./dist
COPY --from=builder --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nextjs:nodejs /app/package.json ./package.json

# Security: Remove unnecessary packages
RUN npm prune --production

# Security: Set proper file permissions
RUN chmod -R 755 /app

# Switch to non-root user
USER nextjs

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node healthcheck.js

# Expose port
EXPOSE 3000

# Use dumb-init for proper signal handling
CMD ["dumb-init", "node", "dist/index.js"]
```

### Security Scanning Integration

```dockerfile
# Security scanning in multi-stage build
FROM aquasec/trivy:latest AS security-scanner

# Copy source code for vulnerability scanning
COPY . /app
WORKDIR /app

# Run security scan
RUN trivy fs --exit-code 1 --no-progress --format table .

# Scan for secrets
RUN trivy fs --scanners secret --exit-code 1 --no-progress .

FROM node:18-alpine AS secure-base
# ... rest of Dockerfile only runs if security scan passes
```

## 🔐 Secrets Management

### Docker Secrets Implementation

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  payment-service:
    image: fintech/payment-service:latest
    secrets:
      - source: stripe_secret_key
        target: stripe_secret_key
        uid: '1001'
        gid: '1001'
        mode: 0400
      - source: database_password
        target: database_password
        uid: '1001'
        gid: '1001'
        mode: 0400
      - source: jwt_signing_key
        target: jwt_signing_key
        uid: '1001'
        gid: '1001'
        mode: 0400
    environment:
      # Reference secrets by file path
      - STRIPE_SECRET_KEY_FILE=/run/secrets/stripe_secret_key
      - DATABASE_PASSWORD_FILE=/run/secrets/database_password
      - JWT_SIGNING_KEY_FILE=/run/secrets/jwt_signing_key

secrets:
  stripe_secret_key:
    external: true
    name: stripe_secret_key_v1
  database_password:
    external: true
    name: database_password_v2
  jwt_signing_key:
    external: true
    name: jwt_signing_key_v1
```

### Secrets Loading in Application

```typescript
// secrets.ts - Secure secrets loading
import { readFileSync } from 'fs';

class SecretsManager {
  private secrets: Map<string, string> = new Map();
  
  /**
   * Load secrets from Docker secrets or environment variables
   */
  loadSecrets(): void {
    const secretConfigs = [
      { name: 'STRIPE_SECRET_KEY', file: 'stripe_secret_key' },
      { name: 'DATABASE_PASSWORD', file: 'database_password' },
      { name: 'JWT_SIGNING_KEY', file: 'jwt_signing_key' },
      { name: 'ENCRYPTION_KEY', file: 'encryption_key' }
    ];
    
    for (const config of secretConfigs) {
      let secretValue: string;
      
      // Try to load from Docker secret file first
      const secretFilePath = `/run/secrets/${config.file}`;
      try {
        secretValue = readFileSync(secretFilePath, 'utf8').trim();
        console.log(`Loaded ${config.name} from Docker secret`);
      } catch (error) {
        // Fallback to environment variable
        secretValue = process.env[config.name];
        if (!secretValue) {
          throw new Error(`Secret ${config.name} not found in file or environment`);
        }
        console.log(`Loaded ${config.name} from environment variable`);
      }
      
      this.secrets.set(config.name, secretValue);
    }
  }
  
  getSecret(name: string): string {
    const secret = this.secrets.get(name);
    if (!secret) {
      throw new Error(`Secret ${name} not found`);
    }
    return secret;
  }
}

export const secretsManager = new SecretsManager();
secretsManager.loadSecrets();
```

## 🚀 Production Deployment

### Production Docker Compose

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - ./nginx/logs:/var/log/nginx
    depends_on:
      - api-gateway
    networks:
      - fintech-network
    restart: unless-stopped

  api-gateway:
    image: fintech/api-gateway:${VERSION}
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
        failure_action: rollback
      rollback_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
    environment:
      - NODE_ENV=production
      - LOG_LEVEL=info
    secrets:
      - database_url
      - jwt_secret
      - redis_url
    networks:
      - fintech-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  payment-service:
    image: fintech/payment-service:${VERSION}
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '1.0'
          memory: 1GB
        reservations:
          cpus: '0.5'
          memory: 512MB
    environment:
      - NODE_ENV=production
      - PCI_COMPLIANCE_MODE=true
    secrets:
      - database_url
      - stripe_secret_key
      - encryption_key
    networks:
      - fintech-network
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

networks:
  fintech-network:
    driver: overlay
    attachable: true
    encrypted: true

secrets:
  database_url:
    external: true
  jwt_secret:
    external: true
  redis_url:
    external: true
  stripe_secret_key:
    external: true
  encryption_key:
    external: true
```

### Docker Swarm Deployment

```bash
#!/bin/bash
# deploy.sh - Production deployment script

set -e

# Configuration
STACK_NAME="fintech-app"
VERSION="${VERSION:-latest}"
ENVIRONMENT="${ENVIRONMENT:-production}"

echo "🚀 Deploying Fintech Application Stack"
echo "Stack: $STACK_NAME"
echo "Version: $VERSION"
echo "Environment: $ENVIRONMENT"

# Pre-deployment checks
echo "📋 Running pre-deployment checks..."

# Check if secrets exist
REQUIRED_SECRETS=(
  "database_url"
  "jwt_secret"
  "redis_url" 
  "stripe_secret_key"
  "encryption_key"
)

for secret in "${REQUIRED_SECRETS[@]}"; do
  if ! docker secret ls | grep -q "$secret"; then
    echo "❌ Required secret '$secret' not found"
    exit 1
  fi
  echo "✅ Secret '$secret' found"
done

# Check if images exist
REQUIRED_IMAGES=(
  "fintech/api-gateway:$VERSION"
  "fintech/payment-service:$VERSION"
  "fintech/user-service:$VERSION"
  "fintech/frontend:$VERSION"
)

for image in "${REQUIRED_IMAGES[@]}"; do
  if ! docker image inspect "$image" >/dev/null 2>&1; then
    echo "❌ Required image '$image' not found"
    exit 1
  fi
  echo "✅ Image '$image' found"
done

# Deploy stack
echo "🔄 Deploying stack..."
export VERSION
export ENVIRONMENT

docker stack deploy \
  --compose-file docker-compose.prod.yml \
  --prune \
  "$STACK_NAME"

echo "⏳ Waiting for services to be ready..."
sleep 30

# Health checks
echo "🏥 Running health checks..."
MAX_RETRIES=30
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
  if curl -f http://localhost/health >/dev/null 2>&1; then
    echo "✅ Health check passed"
    break
  fi
  
  RETRY_COUNT=$((RETRY_COUNT + 1))
  echo "⏳ Health check attempt $RETRY_COUNT/$MAX_RETRIES..."
  sleep 10
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
  echo "❌ Health check failed after $MAX_RETRIES attempts"
  exit 1
fi

echo "🎉 Deployment completed successfully!"
echo "📊 Stack status:"
docker stack services "$STACK_NAME"
```

## 📊 Container Monitoring

### Monitoring Stack

```yaml
# monitoring/docker-compose.monitoring.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--web.enable-lifecycle'
    networks:
      - monitoring

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3200:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards:ro
      - ./grafana/datasources:/etc/grafana/provisioning/datasources:ro
    networks:
      - monitoring

  node-exporter:
    image: prom/node-exporter:latest
    ports:
      - "9100:9100"
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.rootfs=/rootfs'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.ignored-mount-points=^/(sys|proc|dev|host|etc)($$|/)'
    networks:
      - monitoring

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    ports:
      - "8080:8080"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
      - /dev/disk/:/dev/disk:ro
    privileged: true
    devices:
      - /dev/kmsg
    networks:
      - monitoring

volumes:
  prometheus_data:
  grafana_data:

networks:
  monitoring:
    driver: bridge
```

### Application Metrics

```typescript
// metrics.ts - Application metrics collection
import promClient from 'prom-client';

class MetricsCollector {
  private static instance: MetricsCollector;
  
  // Metrics definitions
  private httpRequestDuration = new promClient.Histogram({
    name: 'http_request_duration_seconds',
    help: 'Duration of HTTP requests in seconds',
    labelNames: ['method', 'route', 'status_code'],
    buckets: [0.1, 0.3, 0.5, 0.7, 1, 3, 5, 7, 10]
  });
  
  private httpRequestsTotal = new promClient.Counter({
    name: 'http_requests_total',
    help: 'Total number of HTTP requests',
    labelNames: ['method', 'route', 'status_code']
  });
  
  private paymentTransactionsTotal = new promClient.Counter({
    name: 'payment_transactions_total',
    help: 'Total number of payment transactions',
    labelNames: ['status', 'payment_method']
  });
  
  private databaseConnectionsActive = new promClient.Gauge({
    name: 'database_connections_active',
    help: 'Number of active database connections'
  });
  
  private complianceChecksTotal = new promClient.Counter({
    name: 'compliance_checks_total',
    help: 'Total number of compliance checks performed',
    labelNames: ['check_type', 'result']
  });
  
  constructor() {
    // Register default metrics
    promClient.register.registerMetric(this.httpRequestDuration);
    promClient.register.registerMetric(this.httpRequestsTotal);
    promClient.register.registerMetric(this.paymentTransactionsTotal);
    promClient.register.registerMetric(this.databaseConnectionsActive);
    promClient.register.registerMetric(this.complianceChecksTotal);
    
    // Collect default metrics
    promClient.collectDefaultMetrics({ prefix: 'fintech_app_' });
  }
  
  static getInstance(): MetricsCollector {
    if (!MetricsCollector.instance) {
      MetricsCollector.instance = new MetricsCollector();
    }
    return MetricsCollector.instance;
  }
  
  recordHttpRequest(method: string, route: string, statusCode: number, duration: number): void {
    const labels = { method, route, status_code: statusCode.toString() };
    this.httpRequestDuration.observe(labels, duration);
    this.httpRequestsTotal.inc(labels);
  }
  
  recordPaymentTransaction(status: string, paymentMethod: string): void {
    this.paymentTransactionsTotal.inc({ status, payment_method: paymentMethod });
  }
  
  updateDatabaseConnections(count: number): void {
    this.databaseConnectionsActive.set(count);
  }
  
  recordComplianceCheck(checkType: string, result: string): void {
    this.complianceChecksTotal.inc({ check_type: checkType, result });
  }
  
  getMetrics(): Promise<string> {
    return promClient.register.metrics();
  }
}

export const metricsCollector = MetricsCollector.getInstance();
```

## 🔍 Debugging and Troubleshooting

### Container Debugging Tools

```bash
#!/bin/bash
# debug-container.sh - Container debugging utilities

SERVICE_NAME=$1
STACK_NAME="fintech-app"

if [ -z "$SERVICE_NAME" ]; then
  echo "Usage: $0 <service-name>"
  echo "Available services:"
  docker stack services "$STACK_NAME" --format "table {{.Name}}"
  exit 1
fi

echo "🔍 Debugging service: $SERVICE_NAME"

# Get service information
echo "📊 Service status:"
docker service ps "${STACK_NAME}_${SERVICE_NAME}"

# Show service logs
echo "📝 Recent logs:"
docker service logs --tail 50 "${STACK_NAME}_${SERVICE_NAME}"

# Get container ID for detailed inspection
CONTAINER_ID=$(docker ps --filter "label=com.docker.swarm.service.name=${STACK_NAME}_${SERVICE_NAME}" -q | head -1)

if [ -n "$CONTAINER_ID" ]; then
  echo "🐳 Container details:"
  docker inspect "$CONTAINER_ID" | jq '.[] | {
    Id: .Id[0:12],
    State: .State,
    NetworkSettings: .NetworkSettings.Networks,
    Mounts: .Mounts
  }'
  
  echo "💻 Container processes:"
  docker exec "$CONTAINER_ID" ps aux
  
  echo "🧠 Container memory usage:"
  docker stats "$CONTAINER_ID" --no-stream
  
  echo "🌐 Network connectivity test:"
  docker exec "$CONTAINER_ID" wget -q --spider http://localhost:3000/health && echo "✅ Health endpoint accessible" || echo "❌ Health endpoint not accessible"
else
  echo "❌ No running container found for service $SERVICE_NAME"
fi
```

### Performance Profiling

```dockerfile
# Dockerfile.debug - Debug version with profiling tools
FROM node:18-alpine AS debug

# Install debugging tools
RUN apk add --no-cache curl htop strace

# Install Node.js profiling tools
RUN npm install -g clinic autocannon

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

# Expose debugging ports
EXPOSE 3000 9229 8080

# Start with debugging enabled
CMD ["node", "--inspect=0.0.0.0:9229", "dist/index.js"]
```

## 🧪 Testing Container Builds

### Automated Testing Pipeline

```yaml
# .github/workflows/docker-test.yml
name: Docker Build and Test

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  docker-test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Build development image
      run: |
        docker build \
          --target development \
          --tag fintech/api-gateway:dev \
          ./backend/api-gateway
    
    - name: Test development container
      run: |
        docker run -d \
          --name api-gateway-test \
          --env NODE_ENV=test \
          --env DATABASE_URL=sqlite://memory \
          -p 3000:3000 \
          fintech/api-gateway:dev
        
        # Wait for container to start
        sleep 10
        
        # Run health check
        curl -f http://localhost:3000/health
        
        # Run tests inside container
        docker exec api-gateway-test npm test
        
        # Stop container
        docker stop api-gateway-test
    
    - name: Build production image
      run: |
        docker build \
          --target production \
          --tag fintech/api-gateway:prod \
          ./backend/api-gateway
    
    - name: Test production container
      run: |
        docker run -d \
          --name api-gateway-prod-test \
          --env NODE_ENV=production \
          --env DATABASE_URL=sqlite://memory \
          -p 3001:3000 \
          fintech/api-gateway:prod
        
        sleep 10
        curl -f http://localhost:3001/health
        docker stop api-gateway-prod-test
    
    - name: Security scan
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: 'fintech/api-gateway:prod'
        format: 'table'
        exit-code: '1'
```

## 📋 Docker Best Practices Checklist

### Security Checklist

- [ ] **Base Images**
  - [ ] Use official, minimal base images (Alpine)
  - [ ] Pin specific image versions
  - [ ] Regularly update base images
  - [ ] Scan images for vulnerabilities

- [ ] **User Security**
  - [ ] Run containers as non-root user
  - [ ] Use specific user IDs (not default)
  - [ ] Set proper file permissions
  - [ ] Use read-only root filesystem where possible

- [ ] **Secrets Management**
  - [ ] Use Docker secrets for sensitive data
  - [ ] Never include secrets in images
  - [ ] Load secrets from files, not environment variables
  - [ ] Rotate secrets regularly

- [ ] **Network Security**
  - [ ] Use custom networks instead of default bridge
  - [ ] Enable network encryption in Swarm mode
  - [ ] Limit container communications
  - [ ] Use reverse proxy for external access

### Performance Checklist

- [ ] **Image Optimization**
  - [ ] Use multi-stage builds
  - [ ] Minimize layer count
  - [ ] Use .dockerignore files
  - [ ] Cache npm dependencies separately

- [ ] **Resource Management**
  - [ ] Set memory and CPU limits
  - [ ] Configure proper restart policies
  - [ ] Use health checks
  - [ ] Monitor resource usage

### Compliance Checklist

- [ ] **Audit and Logging**
  - [ ] Enable audit logging
  - [ ] Centralize log collection
  - [ ] Secure log storage
  - [ ] Monitor security events

- [ ] **Data Protection**
  - [ ] Encrypt data at rest and in transit
  - [ ] Use secure communication between services
  - [ ] Implement proper backup strategies
  - [ ] Ensure data retention compliance

---

*This guide is part of the comprehensive AI-driven development course. For Kubernetes deployment, see the [Kubernetes Guide](./kubernetes-guide.md).*