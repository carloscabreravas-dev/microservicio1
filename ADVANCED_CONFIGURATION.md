# Configuración Avanzada para OpenShift

Esta guía contiene configuraciones avanzadas y mejores prácticas para producción.

## 🔒 Gestión Segura de Secretos

### Usando Sealed Secrets (recomendado para producción)

```bash
# Instalar sealed-secrets controller
oc apply -f https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.18.0/controller.yaml -n kube-system

# Crear un sealed secret
echo -n "mi-contraseña-secreta" | oc create secret generic db-password \
  --dry-run=client --from-file=/dev/stdin \
  -o yaml | kubeseal -o yaml > db-password-sealed.yaml

# Aplicar el sealed secret
oc apply -f db-password-sealed.yaml
```

### Usando External Secrets Operator

```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
  namespace: default
spec:
  provider:
    vault:
      server: "https://vault.ejemplo.com"
      path: "secret"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "default"

---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-credentials
  namespace: default
spec:
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: postgres-credentials
    creationPolicy: Owner
  data:
  - secretKey: db-user
    remoteRef:
      key: database/username
  - secretKey: db-password
    remoteRef:
      key: database/password
```

## 📊 Monitoreo y Alertas Avanzadas

### ServiceMonitor para Prometheus

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: microservicio-monitor
  namespace: default
  labels:
    app: microservicio
spec:
  selector:
    matchLabels:
      app: microservicio
  endpoints:
  - port: http
    interval: 30s
    path: /metrics
```

### PrometheusRule para Alertas

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: microservicio-alerts
  namespace: default
spec:
  groups:
  - name: microservicio
    interval: 30s
    rules:
    - alert: MicroservicioPodCrashLooping
      expr: rate(kube_pod_container_status_restarts_total{pod=~"microservicio-.*"}[5m]) > 0.1
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "Pod {{ $labels.pod }} restarting frequently"
        
    - alert: MicroservicioHighErrorRate
      expr: rate(http_requests_total{job="microservicio",status=~"5.."}[5m]) > 0.05
      for: 10m
      labels:
        severity: warning
      annotations:
        summary: "High error rate detected"
        
    - alert: MicroservicioHighLatency
      expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
      for: 10m
      labels:
        severity: warning
      annotations:
        summary: "High latency detected"
```

## 🔄 CI/CD Avanzado

### GitOps con ArgoCD

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: microservicio
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/tu-usuario/microservicio.git
    targetRevision: main
    path: k8s/
  destination:
    server: https://kubernetes.default.svc
    namespace: microservicio
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
```

### Tekton Pipeline

```yaml
apiVersion: tekton.dev/v1
kind: Pipeline
metadata:
  name: microservicio-build-deploy
  namespace: ci-cd
spec:
  params:
  - name: git-url
    type: string
  - name: git-revision
    type: string
    default: main
  - name: image-tag
    type: string
    
  tasks:
  - name: clone
    taskRef:
      name: git-clone
    params:
    - name: url
      value: $(params.git-url)
    - name: revision
      value: $(params.git-revision)
      
  - name: build-and-push
    runAfter: [clone]
    taskRef:
      name: buildah
    params:
    - name: IMAGE
      value: quay.io/tu-usuario/microservicio:$(params.image-tag)
      
  - name: deploy
    runAfter: [build-and-push]
    taskRef:
      name: openshift-deploy
    params:
    - name: NAMESPACE
      value: microservicio-prod
```

## 🔐 RBAC y Pod Security

### ServiceAccount con permisos limitados

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: microservicio
  namespace: default

---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: microservicio-role
  namespace: default
rules:
- apiGroups: [""]
  resources: ["configmaps", "secrets"]
  verbs: ["get", "list"]
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: microservicio-rolebinding
  namespace: default
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: microservicio-role
subjects:
- kind: ServiceAccount
  name: microservicio
  namespace: default
```

### Pod Security Policy

```yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: restricted
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
  hostNetwork: false
  hostIPC: false
  hostPID: false
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'MustRunAs'
    seLinuxOptions:
      level: "s0:c123,c456"
  fsGroup:
    rule: 'MustRunAs'
    ranges:
    - min: 1000
      max: 65535
  readOnlyRootFilesystem: true
```

## 🚀 Despliegue Canario y Blue-Green

### Despliegue Canario con Flagger

```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: microservicio
  namespace: default
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: microservicio
  service:
    port: 80
    targetPort: 8000
  analysis:
    interval: 1m
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    metrics:
    - name: request-success-rate
      thresholdRange:
        min: 99
      interval: 1m
    - name: request-duration
      thresholdRange:
        max: 500
      interval: 1m
    webhooks:
    - name: acceptance-test
      url: http://flagger-loadtester/
      timeout: 30s
      metadata:
        type: smoke
        cmd: "curl -sd 'test' http://microservicio-canary/test"
```

## 📦 Multi-Región

### Instalación en múltiples clusters

```bash
#!/bin/bash
# deploy-to-multiple-clusters.sh

CLUSTERS=("cluster-us-east" "cluster-eu-west" "cluster-ap-south")
NAMESPACE="microservicio"

for cluster in "${CLUSTERS[@]}"; do
    echo "Desplegando en $cluster..."
    
    oc login --server=$(get_server $cluster) --token=$(get_token $cluster)
    oc project $NAMESPACE || oc create namespace $NAMESPACE
    
    oc apply -f openshift-deployment.yaml
    
    # Esperar a que esté listo
    oc rollout status deployment/microservicio --timeout=10m
    
    # Verificar
    oc get all
    
    echo "✓ Deployment completado en $cluster"
done

echo "✓ Deployment multi-región completado"
```

## 🔍 Debugging Avanzado

### Port Forward para debugging local

```bash
# Acceder a la base de datos localmente
oc port-forward service/postgres 5432:5432 &

# Conectar localmente
psql -h localhost -U usuario -d microservicio

# Acceder a la aplicación
oc port-forward service/microservicio 8000:8000 &
curl http://localhost:8000/health
```

### Remote Debugging

```bash
# Habilitar debugging remoto
oc set env deployment/microservicio \
  DEBUG=true \
  PYTHONUNBUFFERED=1

# Port forward para debugger
oc port-forward deployment/microservicio 5678:5678

# Conectar debugger desde IDE
# host: localhost, port: 5678
```

### Análisis de recursos

```bash
# Ver uso de recursos
oc top nodes
oc top pods -n default

# Ver límites y requests
oc describe node <node-name>

# Analizar PVC
oc describe pvc postgres-storage-postgres-0
```

## 📈 Performance Tuning

### Optimizar recursos de PostgreSQL

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  template:
    spec:
      containers:
      - name: postgres
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        env:
        - name: POSTGRES_INITDB_ARGS
          value: "-c shared_buffers=256MB -c max_connections=200"
```

### Caché con Redis

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
spec:
  template:
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
```

## 🔗 Referencias

- [OpenShift Advanced Configuration](https://docs.openshift.com/container-platform/latest/rest_api/)
- [Kubernetes Security](https://kubernetes.io/docs/concepts/security/)
- [Prometheus Operator](https://github.com/prometheus-operator/prometheus-operator)
- [ArgoCD](https://argo-cd.readthedocs.io/)
- [Flagger Canary Deployments](https://flagger.app/)
