# Kubernetes Deployment Guide for Fintech Applications

## ☸️ Overview

This guide provides comprehensive Kubernetes deployment strategies for fintech applications, focusing on security, compliance, scalability, and high availability. Learn to deploy microservices, manage secrets, implement monitoring, and ensure regulatory compliance in Kubernetes environments.

## 🏗️ Architecture Overview

### Kubernetes Cluster Architecture

```yaml
# Architecture diagram in YAML format
apiVersion: v1
kind: ConfigMap
metadata:
  name: architecture-overview
data:
  architecture.yaml: |
    cluster:
      control-plane:
        - api-server
        - etcd
        - scheduler
        - controller-manager
      worker-nodes:
        - kubelet
        - kube-proxy
        - container-runtime
      
    namespaces:
      - fintech-prod
      - fintech-staging
      - fintech-monitoring
      - fintech-security
      
    services:
      api-gateway:
        replicas: 3
        resources: { cpu: "500m", memory: "1Gi" }
      payment-service:
        replicas: 2
        resources: { cpu: "1000m", memory: "2Gi" }
      user-service:
        replicas: 2
        resources: { cpu: "500m", memory: "1Gi" }
      notification-service:
        replicas: 1
        resources: { cpu: "250m", memory: "512Mi" }
```

## 🔐 Security-First Kubernetes Configuration

### Namespace and RBAC Setup

```yaml
# namespaces.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: fintech-prod
  labels:
    environment: production
    compliance: pci-dss
    data-classification: confidential
  annotations:
    audit.kubernetes.io/level: "Metadata"
    
---
apiVersion: v1
kind: Namespace
metadata:
  name: fintech-monitoring
  labels:
    environment: production
    purpose: monitoring

---
# RBAC Configuration
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: fintech-prod
  name: fintech-service-account
rules:
- apiGroups: [""]
  resources: ["pods", "services", "endpoints"]
  verbs: ["get", "list", "watch"]
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get"]
  resourceNames: ["payment-secrets", "database-secrets"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: fintech-service-binding
  namespace: fintech-prod
subjects:
- kind: ServiceAccount
  name: fintech-service-account
  namespace: fintech-prod
roleRef:
  kind: Role
  name: fintech-service-account
  apiGroup: rbac.authorization.k8s.io

---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: fintech-service-account
  namespace: fintech-prod
  annotations:
    iam.gke.io/gcp-service-account: fintech-workload-identity@project-id.iam.gserviceaccount.com
```

### Pod Security Standards

```yaml
# pod-security-policy.yaml
apiVersion: v1
kind: Pod
metadata:
  name: example-secure-pod
  namespace: fintech-prod
spec:
  serviceAccountName: fintech-service-account
  securityContext:
    runAsNonRoot: true
    runAsUser: 1001
    runAsGroup: 1001
    fsGroup: 1001
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: payment-service
    image: fintech/payment-service:v1.2.3
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
    resources:
      requests:
        memory: "1Gi"
        cpu: "500m"
      limits:
        memory: "2Gi"
        cpu: "1000m"
    volumeMounts:
    - name: tmp
      mountPath: /tmp
      readOnly: false
    - name: secrets-volume
      mountPath: /etc/secrets
      readOnly: true
  volumes:
  - name: tmp
    emptyDir: {}
  - name: secrets-volume
    secret:
      secretName: payment-secrets
      defaultMode: 0400
```

## 🔑 Secrets and Configuration Management

### Sealed Secrets Implementation

```yaml
# Install Sealed Secrets Controller
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sealed-secrets-controller
  namespace: kube-system
spec:
  replicas: 1
  selector:
    matchLabels:
      name: sealed-secrets-controller
  template:
    metadata:
      labels:
        name: sealed-secrets-controller
    spec:
      serviceAccountName: sealed-secrets-controller
      containers:
      - name: sealed-secrets-controller
        image: quay.io/bitnami/sealed-secrets-controller:v0.18.0
        command:
        - controller
        livenessProbe:
          httpGet:
            path: /healthz
            port: http
        readinessProbe:
          httpGet:
            path: /healthz
            port: http
        ports:
        - containerPort: 8080
          name: http
        securityContext:
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          runAsUser: 1001

---
# Sealed Secret for Payment Service
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: payment-secrets
  namespace: fintech-prod
spec:
  encryptedData:
    stripe-secret-key: AgBy3i4OJSWK+PiTySYZZA9rO5...  # Encrypted
    database-password: AgAR2F8H9K2L+XyZ1234567890...  # Encrypted
    jwt-signing-key: AgAK8J3M5N7P+QwE0987654321...   # Encrypted
  template:
    metadata:
      name: payment-secrets
      namespace: fintech-prod
    type: Opaque
```

### External Secrets Operator

```yaml
# external-secrets-operator.yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
  namespace: fintech-prod
spec:
  provider:
    vault:
      server: "https://vault.company.com"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "fintech-role"
          serviceAccountRef:
            name: "fintech-service-account"

---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: payment-service-secrets
  namespace: fintech-prod
spec:
  refreshInterval: 5m
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: payment-secrets
    creationPolicy: Owner
  data:
  - secretKey: stripe-secret-key
    remoteRef:
      key: payment-service
      property: stripe-secret-key
  - secretKey: database-password
    remoteRef:
      key: database
      property: password
  - secretKey: jwt-signing-key
    remoteRef:
      key: auth
      property: jwt-signing-key
```

## 🚀 Microservices Deployment

### API Gateway Deployment

```yaml
# api-gateway-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway
  namespace: fintech-prod
  labels:
    app: api-gateway
    version: v1.2.3
    component: gateway
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: api-gateway
  template:
    metadata:
      labels:
        app: api-gateway
        version: v1.2.3
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "3000"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: fintech-service-account
      securityContext:
        runAsNonRoot: true
        runAsUser: 1001
        fsGroup: 1001
      containers:
      - name: api-gateway
        image: fintech/api-gateway:v1.2.3
        ports:
        - containerPort: 3000
          name: http
        env:
        - name: NODE_ENV
          value: "production"
        - name: PORT
          value: "3000"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: database-secrets
              key: connection-string
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: redis-secrets
              key: connection-string
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 5
          failureThreshold: 3
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
        volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: cache
          mountPath: /app/cache
      volumes:
      - name: tmp
        emptyDir: {}
      - name: cache
        emptyDir: {}
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - api-gateway
              topologyKey: kubernetes.io/hostname

---
apiVersion: v1
kind: Service
metadata:
  name: api-gateway-service
  namespace: fintech-prod
  labels:
    app: api-gateway
spec:
  selector:
    app: api-gateway
  ports:
  - name: http
    port: 80
    targetPort: 3000
  type: ClusterIP
```

### Payment Service with PCI Compliance

```yaml
# payment-service-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service
  namespace: fintech-prod
  labels:
    app: payment-service
    compliance: pci-dss
    data-classification: restricted
spec:
  replicas: 2
  selector:
    matchLabels:
      app: payment-service
  template:
    metadata:
      labels:
        app: payment-service
        compliance: pci-dss
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "3002"
        vault.hashicorp.com/agent-inject: "true"
        vault.hashicorp.com/role: "payment-service"
        vault.hashicorp.com/agent-inject-secret-stripe: "secret/payment/stripe"
    spec:
      serviceAccountName: fintech-service-account
      securityContext:
        runAsNonRoot: true
        runAsUser: 1001
        fsGroup: 1001
        seccompProfile:
          type: RuntimeDefault
      containers:
      - name: payment-service
        image: fintech/payment-service:v1.2.3
        ports:
        - containerPort: 3002
          name: http
        env:
        - name: NODE_ENV
          value: "production"
        - name: PCI_COMPLIANCE_MODE
          value: "true"
        - name: LOG_LEVEL
          value: "info"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: payment-secrets
              key: database-password
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 45
          periodSeconds: 30
          timeoutSeconds: 10
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: http
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 5
          failureThreshold: 3
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
        volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: vault-secrets
          mountPath: /vault/secrets
          readOnly: true
      volumes:
      - name: tmp
        emptyDir: {}
      - name: vault-secrets
        emptyDir: {}
      nodeSelector:
        node-type: compute-optimized
        compliance: pci-dss
      tolerations:
      - key: "fintech.com/pci-dss"
        operator: "Equal"
        value: "true"
        effect: "NoSchedule"

---
apiVersion: v1
kind: Service
metadata:
  name: payment-service
  namespace: fintech-prod
  labels:
    app: payment-service
spec:
  selector:
    app: payment-service
  ports:
  - name: http
    port: 80
    targetPort: 3002
  type: ClusterIP
```

## 🔄 GitOps Deployment with ArgoCD

### ArgoCD Application Configuration

```yaml
# argocd-application.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: fintech-app
  namespace: argocd
  annotations:
    notifications.argoproj.io/subscribe.on-sync-succeeded.slack: fintech-deployments
    notifications.argoproj.io/subscribe.on-health-degraded.slack: fintech-alerts
spec:
  project: fintech-project
  source:
    repoURL: https://github.com/company/fintech-k8s-manifests
    targetRevision: main
    path: overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: fintech-prod
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
    - CreateNamespace=true
    - PrunePropagationPolicy=foreground
    - PruneLast=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
  ignoreDifferences:
  - group: apps
    kind: Deployment
    jsonPointers:
    - /spec/replicas
  revisionHistoryLimit: 10

---
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: fintech-project
  namespace: argocd
spec:
  description: Fintech Application Project
  sourceRepos:
  - 'https://github.com/company/fintech-k8s-manifests'
  destinations:
  - namespace: 'fintech-*'
    server: https://kubernetes.default.svc
  clusterResourceWhitelist:
  - group: ''
    kind: Namespace
  - group: 'rbac.authorization.k8s.io'
    kind: ClusterRole
  - group: 'rbac.authorization.k8s.io'
    kind: ClusterRoleBinding
  namespaceResourceWhitelist:
  - group: ''
    kind: Service
  - group: ''
    kind: ConfigMap
  - group: ''
    kind: Secret
  - group: 'apps'
    kind: Deployment
  - group: 'apps'
    kind: StatefulSet
  - group: 'networking.k8s.io'
    kind: Ingress
  roles:
  - name: developer
    description: Developer role
    policies:
    - p, proj:fintech-project:developer, applications, get, fintech-project/*, allow
    - p, proj:fintech-project:developer, applications, sync, fintech-project/*, allow
    groups:
    - fintech-developers
```

### Kustomization for Environment Management

```yaml
# base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- api-gateway-deployment.yaml
- payment-service-deployment.yaml
- user-service-deployment.yaml
- notification-service-deployment.yaml
- database-statefulset.yaml
- services.yaml
- configmaps.yaml

commonLabels:
  app.kubernetes.io/name: fintech-app
  app.kubernetes.io/version: v1.2.3

---
# overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: fintech-prod

resources:
- ../../base

patchesStrategicMerge:
- production-patches.yaml

replicas:
- name: api-gateway
  count: 3
- name: payment-service
  count: 2
- name: user-service
  count: 2

images:
- name: fintech/api-gateway
  newTag: v1.2.3
- name: fintech/payment-service
  newTag: v1.2.3
- name: fintech/user-service
  newTag: v1.2.3

configMapGenerator:
- name: app-config
  literals:
  - NODE_ENV=production
  - LOG_LEVEL=info
  - RATE_LIMIT_ENABLED=true

secretGenerator:
- name: database-credentials
  files:
  - credentials.env
```

## 📊 Monitoring and Observability

### Prometheus Configuration

```yaml
# prometheus-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: fintech-monitoring
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
      evaluation_interval: 15s
    
    rule_files:
    - "fintech-rules.yml"
    
    scrape_configs:
    - job_name: 'kubernetes-pods'
      kubernetes_sd_configs:
      - role: pod
      relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
    
    - job_name: 'fintech-services'
      kubernetes_sd_configs:
      - role: endpoints
        namespaces:
          names:
          - fintech-prod
      relabel_configs:
      - source_labels: [__meta_kubernetes_service_label_app]
        action: keep
        regex: (api-gateway|payment-service|user-service)
    
    alerting:
      alertmanagers:
      - static_configs:
        - targets:
          - alertmanager:9093

---
# Alerting Rules
apiVersion: v1
kind: ConfigMap
metadata:
  name: fintech-rules
  namespace: fintech-monitoring
data:
  fintech-rules.yml: |
    groups:
    - name: fintech.rules
      rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is above 10% for {{ $labels.service }}"
      
      - alert: PaymentServiceDown
        expr: up{job="payment-service"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Payment service is down"
          description: "Payment service has been down for more than 1 minute"
      
      - alert: DatabaseConnectionHigh
        expr: database_connections_active > 80
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High database connection usage"
          description: "Database connections are at {{ $value }}"
```

### Service Mesh with Istio

```yaml
# istio-configuration.yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: fintech-istio
spec:
  values:
    global:
      meshID: fintech-mesh
      network: fintech-network
  components:
    pilot:
      k8s:
        resources:
          requests:
            cpu: 500m
            memory: 2048Mi
    ingressGateways:
    - name: istio-ingressgateway
      enabled: true
      k8s:
        service:
          type: LoadBalancer
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 2000m
            memory: 1024Mi

---
# Virtual Service for API Gateway
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: fintech-api
  namespace: fintech-prod
spec:
  hosts:
  - api.fintech.company.com
  gateways:
  - fintech-gateway
  http:
  - match:
    - uri:
        prefix: /api/v1/payments
    route:
    - destination:
        host: payment-service
        port:
          number: 80
    fault:
      delay:
        percentage:
          value: 0.1
        fixedDelay: 5s
    retries:
      attempts: 3
      perTryTimeout: 10s
  - match:
    - uri:
        prefix: /api/v1/users
    route:
    - destination:
        host: user-service
        port:
          number: 80
  - route:
    - destination:
        host: api-gateway-service
        port:
          number: 80

---
# Destination Rule with Circuit Breaker
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: payment-service-dr
  namespace: fintech-prod
spec:
  host: payment-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 50
        maxRequestsPerConnection: 10
    circuitBreaker:
      consecutiveGatewayErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
    tls:
      mode: ISTIO_MUTUAL
```

## 🔒 Network Policies and Security

### Network Security Policies

```yaml
# network-policies.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: fintech-default-deny
  namespace: fintech-prod
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress

---
# Allow ingress to API Gateway
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-gateway-ingress
  namespace: fintech-prod
spec:
  podSelector:
    matchLabels:
      app: api-gateway
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: istio-system
    ports:
    - protocol: TCP
      port: 3000

---
# Payment service isolation
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: payment-service-policy
  namespace: fintech-prod
spec:
  podSelector:
    matchLabels:
      app: payment-service
      compliance: pci-dss
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: api-gateway
    ports:
    - protocol: TCP
      port: 3002
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: postgres
    ports:
    - protocol: TCP
      port: 5432
  - to: []
    ports:
    - protocol: TCP
      port: 443  # HTTPS to external payment processors
```

### Pod Security Policies

```yaml
# pod-security-policy.yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: fintech-psp
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
    - ALL
  volumes:
    - 'configMap'
    - 'emptyDir'
    - 'projected'
    - 'secret'
    - 'downwardAPI'
    - 'persistentVolumeClaim'
  runAsUser:
    rule: 'MustRunAsNonRoot'
  runAsGroup:
    rule: 'MustRunAs'
    ranges:
      - min: 1
        max: 65535
  seLinux:
    rule: 'RunAsAny'
  fsGroup:
    rule: 'RunAsAny'
  readOnlyRootFilesystem: true

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: fintech-psp-user
rules:
- apiGroups: ['policy']
  resources: ['podsecuritypolicies']
  verbs: ['use']
  resourceNames:
  - fintech-psp

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: fintech-psp-binding
roleRef:
  kind: ClusterRole
  name: fintech-psp-user
  apiGroup: rbac.authorization.k8s.io
subjects:
- kind: ServiceAccount
  name: fintech-service-account
  namespace: fintech-prod
```

## 📈 Autoscaling and Performance

### Horizontal Pod Autoscaler

```yaml
# hpa-configuration.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-gateway-hpa
  namespace: fintech-prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-gateway
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
      - type: Pods
        value: 2
        periodSeconds: 60
      selectPolicy: Max

---
# Vertical Pod Autoscaler
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: payment-service-vpa
  namespace: fintech-prod
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: payment-service
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
    - containerName: payment-service
      minAllowed:
        cpu: 100m
        memory: 128Mi
      maxAllowed:
        cpu: 2000m
        memory: 4Gi
      controlledResources: ["cpu", "memory"]
```

### Cluster Autoscaler

```yaml
# cluster-autoscaler.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cluster-autoscaler
  namespace: kube-system
  labels:
    app: cluster-autoscaler
spec:
  selector:
    matchLabels:
      app: cluster-autoscaler
  template:
    metadata:
      labels:
        app: cluster-autoscaler
    spec:
      serviceAccountName: cluster-autoscaler
      containers:
      - image: k8s.gcr.io/autoscaling/cluster-autoscaler:v1.21.0
        name: cluster-autoscaler
        resources:
          limits:
            cpu: 100m
            memory: 300Mi
          requests:
            cpu: 100m
            memory: 300Mi
        command:
        - ./cluster-autoscaler
        - --v=4
        - --stderrthreshold=info
        - --cloud-provider=gce
        - --skip-nodes-with-local-storage=false
        - --expander=least-waste
        - --node-group-auto-discovery=mig:name=fintech-node-group
        - --scale-down-enabled=true
        - --scale-down-delay-after-add=10m
        - --scale-down-unneeded-time=10m
        env:
        - name: GOOGLE_APPLICATION_CREDENTIALS
          value: /etc/gcp/service-account.json
        volumeMounts:
        - name: gcp-service-account
          mountPath: /etc/gcp
          readOnly: true
      volumes:
      - name: gcp-service-account
        secret:
          secretName: cluster-autoscaler-gcp-key
```

## 🧪 Testing and Validation

### Chaos Engineering with Chaos Mesh

```yaml
# chaos-experiments.yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: payment-service-failure
  namespace: fintech-prod
spec:
  action: pod-failure
  mode: one
  duration: "30s"
  selector:
    labelSelectors:
      app: payment-service
  scheduler:
    cron: "0 */6 * * *"  # Every 6 hours

---
apiVersion: chaos-mesh.org/v1alpha1
kind: NetworkChaos
metadata:
  name: network-partition
  namespace: fintech-prod
spec:
  action: partition
  mode: all
  duration: "2m"
  selector:
    labelSelectors:
      app: api-gateway
  direction: both
  target:
    selector:
      labelSelectors:
        app: payment-service

---
# Stress test
apiVersion: chaos-mesh.org/v1alpha1
kind: StressChaos
metadata:
  name: memory-stress
  namespace: fintech-prod
spec:
  mode: one
  selector:
    labelSelectors:
      app: payment-service
  duration: "5m"
  stressors:
    memory:
      workers: 4
      size: '256MB'
```

### Load Testing

```yaml
# load-test-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: load-test
  namespace: fintech-prod
spec:
  template:
    spec:
      containers:
      - name: load-test
        image: loadimpact/k6:latest
        command: ["/bin/sh"]
        args: ["-c", "k6 run --vus 100 --duration 10m /scripts/load-test.js"]
        volumeMounts:
        - name: test-scripts
          mountPath: /scripts
        env:
        - name: API_ENDPOINT
          value: "http://api-gateway-service/api/v1"
      volumes:
      - name: test-scripts
        configMap:
          name: load-test-scripts
      restartPolicy: Never
  backoffLimit: 3

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: load-test-scripts
  namespace: fintech-prod
data:
  load-test.js: |
    import http from 'k6/http';
    import { check, sleep } from 'k6';
    
    export let options = {
      vus: 100,
      duration: '10m',
      thresholds: {
        http_req_duration: ['p(95)<500'],
        http_req_failed: ['rate<0.1'],
      },
    };
    
    export default function () {
      let response = http.get(`${__ENV.API_ENDPOINT}/health`);
      check(response, {
        'status is 200': (r) => r.status === 200,
        'response time < 500ms': (r) => r.timings.duration < 500,
      });
      sleep(1);
    }
```

## 📋 Production Readiness Checklist

### Security Checklist

- [ ] **Authentication & Authorization**
  - [ ] RBAC configured for all service accounts
  - [ ] Pod Security Standards enforced
  - [ ] Network policies implemented
  - [ ] Service mesh with mTLS enabled

- [ ] **Secrets Management**
  - [ ] External secrets operator configured
  - [ ] Secrets encrypted at rest
  - [ ] Secret rotation implemented
  - [ ] No secrets in container images

- [ ] **Network Security**
  - [ ] Network policies deny-by-default
  - [ ] Ingress properly configured with TLS
  - [ ] Service mesh traffic encryption
  - [ ] Private container registry

### Compliance Checklist

- [ ] **Audit and Logging**
  - [ ] Audit logging enabled
  - [ ] Centralized log aggregation
  - [ ] Log retention policies
  - [ ] Security event monitoring

- [ ] **Data Protection**
  - [ ] Encryption in transit and at rest
  - [ ] PII data handling procedures
  - [ ] Backup and disaster recovery
  - [ ] Data sovereignty compliance

### Operations Checklist

- [ ] **Monitoring and Alerting**
  - [ ] Prometheus metrics collection
  - [ ] Grafana dashboards configured
  - [ ] Alert manager rules defined
  - [ ] On-call procedures documented

- [ ] **Scaling and Performance**
  - [ ] HPA configured for all services
  - [ ] VPA enabled where appropriate
  - [ ] Cluster autoscaler configured
  - [ ] Resource limits properly set

- [ ] **Deployment and Recovery**
  - [ ] GitOps workflow implemented
  - [ ] Rolling update strategy configured
  - [ ] Rollback procedures tested
  - [ ] Disaster recovery plan validated

---

*This guide is part of the comprehensive AI-driven development course. For Docker containerization basics, see the [Docker Guide](./docker-guide.md).*