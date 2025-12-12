# Despliegue Automático a OpenShift

Este proyecto incluye scripts automáticos para desplegar el microservicio a OpenShift usando variables de entorno.

## 📋 Archivos de Despliegue

- **`deploy-openshift.ps1`** - Script de despliegue para Windows (PowerShell)
- **`deploy-openshift.sh`** - Script de despliegue para Linux/macOS (Bash)
- **`openshift-deployment.yaml`** - Manifiestos de Kubernetes/OpenShift
- **`OPENSHIFT_DEPLOYMENT.md`** - Documentación detallada del despliegue
- **`.github/workflows/deploy-openshift.yml`** - Pipeline de CI/CD con GitHub Actions

## 🚀 Inicio Rápido

### Paso 1: Configurar Variables de Entorno

#### Windows (PowerShell):
```powershell
$env:OPENSHIFT_SERVER = "https://api.tu-cluster.com:6443"
$env:OPENSHIFT_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjJ3M..."
$env:OPENSHIFT_NAMESPACE = "tu-namespace"
```

#### Linux/macOS (Bash):
```bash
export OPENSHIFT_SERVER="https://api.tu-cluster.com:6443"
export OPENSHIFT_TOKEN="eyJhbGciOiJSUzI1NiIsImtpZCI6IjJ3M..."
export OPENSHIFT_NAMESPACE="tu-namespace"
```

### Paso 2: Ejecutar el Script de Despliegue

#### Windows:
```powershell
.\deploy-openshift.ps1
```

#### Linux/macOS:
```bash
chmod +x deploy-openshift.sh
./deploy-openshift.sh
```

### Paso 3: Verificar el Despliegue

```bash
# Ver estado
oc get all -n tu-namespace

# Ver logs
oc logs -f deployment/microservicio -n tu-namespace

# Obtener URL de acceso
oc get route microservicio -n tu-namespace
```

## 🔐 Seguridad

### Variables de Entorno Requeridas

| Variable | Descripción |
|----------|-------------|
| `OPENSHIFT_SERVER` | URL del API server de OpenShift (ej: https://api.cluster.com:6443) |
| `OPENSHIFT_TOKEN` | Token de autenticación de OpenShift |
| `OPENSHIFT_NAMESPACE` | Namespace donde desplegar |

### Obtener el Token

1. Abre la consola web de OpenShift
2. Haz clic en tu usuario (esquina superior derecha)
3. Selecciona "Copy login command"
4. Extrae el token del comando mostrado

## 📦 Lo que se Despliega

### Base de Datos
- ✅ PostgreSQL 15 (StatefulSet)
- ✅ Almacenamiento persistente (5Gi)
- ✅ Health checks automáticos
- ✅ Credenciales seguras en Secret

### Aplicación
- ✅ 2 réplicas del microservicio
- ✅ Auto-escalado (2-5 réplicas)
- ✅ Health checks (liveness + readiness)
- ✅ Rolling updates sin downtime
- ✅ Ruta HTTPS automática

### Seguridad
- ✅ NetworkPolicy para restricciones de tráfico
- ✅ SecurityContext sin privilegios
- ✅ RBAC automático
- ✅ Secrets para credenciales

## 🛠️ Opciones Avanzadas

### Cambiar Etiqueta de Imagen
```powershell
# Windows
.\deploy-openshift.ps1 -ImageTag "v1.1.0"
```

```bash
# Linux/macOS
./deploy-openshift.sh v1.1.0 quay.io tu-usuario
```

### Despliegue Manual Paso a Paso

```bash
# 1. Autenticarse
oc login --server=$OPENSHIFT_SERVER --token=$OPENSHIFT_TOKEN --insecure-skip-tls-verify=true

# 2. Crear namespace
oc create namespace $OPENSHIFT_NAMESPACE
oc project $OPENSHIFT_NAMESPACE

# 3. Crear base de datos
oc apply -f openshift-deployment.yaml

# 4. Ver estado
oc get all
```

## 📊 Monitoreo

```bash
# Ver logs en tiempo real
oc logs -f deployment/microservicio

# Ver todos los pods
oc get pods

# Ver estado del HPA
oc get hpa

# Describir un recurso
oc describe deployment microservicio

# Ver eventos
oc get events --sort-by='.lastTimestamp'
```

## 🔄 Actualizar Aplicación

```bash
# Simplemente ejecuta el script nuevamente con la nueva versión
.\deploy-openshift.ps1 -ImageTag "v1.2.0"

# OpenShift hará un rolling update automático
```

## ❌ Solucionar Problemas

### Error: "password authentication failed"
```bash
# Verificar credenciales en el Secret
oc get secret postgres-credentials -o yaml

# Conectar a PostgreSQL
oc exec -it postgres-0 -- psql -U usuario -d microservicio
```

### Pod no inicia
```bash
# Ver logs detallados
oc logs <pod-name> --previous

# Describir el pod
oc describe pod <pod-name>

# Ver eventos
oc get events
```

### Problemas de permisos
```bash
# Verificar permisos
oc auth can-i create deployments
oc auth can-i create statefulsets

# Ver RBAC actual
oc get rolebindings
oc get clusterrolebindings
```

## 🗑️ Limpiar Recursos

```bash
# Eliminar todo el despliegue
oc delete -f openshift-deployment.yaml

# Eliminar el namespace completo
oc delete namespace $OPENSHIFT_NAMESPACE

# Eliminar solo la aplicación
oc delete deployment microservicio
```

## 🔗 CI/CD con GitHub Actions

El proyecto incluye un workflow de GitHub Actions que:
- ✅ Construye la imagen Docker automáticamente
- ✅ Publica en el registry
- ✅ Despliega a OpenShift automáticamente
- ✅ Soporta múltiples ambientes (staging, production)

### Configurar GitHub Actions

1. **Ir a Settings → Secrets and variables → Actions**
2. **Agregar los siguientes secrets:**
   ```
   OPENSHIFT_SERVER = https://api.tu-cluster.com:6443
   OPENSHIFT_TOKEN = tu-token
   REGISTRY_PASSWORD = tu-password-docker
   ```
3. **Agregar las siguientes variables:**
   ```
   REGISTRY = quay.io
   IMAGE_NAMESPACE = tu-usuario
   OPENSHIFT_NAMESPACE = tu-namespace
   REGISTRY_USERNAME = tu-usuario
   ```

### Triggers del Pipeline

```yaml
# El pipeline se ejecuta en:
- Push a 'main' o 'develop'
- Pull requests a 'main'
- Manualmente desde Actions
```

## 📚 Recursos Adicionales

- [Documentación OpenShift](https://docs.openshift.com/)
- [OpenShift CLI Reference](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/index.html)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)

## 💡 Tips y Mejores Prácticas

1. **Usar archivos `.env` para desarrollo local**
   ```bash
   cp .env.example .env
   # Editar .env con tus valores locales
   ```

2. **Mantener varias versiones de la imagen**
   ```bash
   oc set image deployment/microservicio microservicio=quay.io/usuario/microservicio:latest
   oc set image deployment/microservicio microservicio=quay.io/usuario/microservicio:stable
   ```

3. **Usar etiquetas de imagen semánticas**
   ```bash
   v1.0.0, v1.1.0, latest, stable
   ```

4. **Verificar logs regularmente**
   ```bash
   oc logs -f deployment/microservicio --all-containers=true
   ```

5. **Usar namespaces para segregar ambientes**
   ```bash
   export OPENSHIFT_NAMESPACE="microservicio-prod"
   export OPENSHIFT_NAMESPACE="microservicio-staging"
   ```

---

**Creado con ❤️ para OpenShift**
