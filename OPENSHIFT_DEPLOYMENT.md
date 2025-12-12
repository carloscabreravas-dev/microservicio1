# Guía de Despliegue en OpenShift

Esta guía proporciona instrucciones para desplegar automáticamente el microservicio a OpenShift.

## Requisitos previos

- OpenShift CLI (`oc`) instalado
- Docker instalado (para construir la imagen)
- Acceso a un cluster de OpenShift
- Credenciales de OpenShift (token de acceso)

## Variables de Entorno Requeridas

Antes de ejecutar el script de despliegue, debes configurar las siguientes variables de entorno:

### En Windows (PowerShell):
```powershell
$env:OPENSHIFT_SERVER = "https://api.tu-cluster.com:6443"
$env:OPENSHIFT_TOKEN = "tu-token-aqui"
$env:OPENSHIFT_NAMESPACE = "tu-namespace"
```

### En Linux/macOS (Bash):
```bash
export OPENSHIFT_SERVER="https://api.tu-cluster.com:6443"
export OPENSHIFT_TOKEN="tu-token-aqui"
export OPENSHIFT_NAMESPACE="tu-namespace"
```

## Obtener el Token de OpenShift

1. Inicia sesión en la consola web de OpenShift
2. Haz clic en tu usuario (esquina superior derecha)
3. Selecciona "Copy login command"
4. El comando contendrá tu token: `--token=xxx`

## Desplegar la Aplicación

### Opción 1: Usando PowerShell (Windows)

```powershell
# Navegar al directorio del proyecto
cd c:\Users\carlosc2\proyecto\microservicio1

# Ejecutar el script de despliegue
.\deploy-openshift.ps1

# Opcional: especificar etiqueta de imagen y registro personalizado
.\deploy-openshift.ps1 -ImageTag "v1.0.0" -ImageRegistry "quay.io" -ImageNamespace "tu-usuario"
```

### Opción 2: Usando Bash (Linux/macOS)

```bash
# Navegar al directorio del proyecto
cd ~/proyecto/microservicio1

# Hacer el script ejecutable
chmod +x deploy-openshift.sh

# Ejecutar el script de despliegue
./deploy-openshift.sh

# Opcional: especificar etiqueta de imagen
./deploy-openshift.sh v1.0.0 quay.io tu-usuario
```

### Opción 3: Despliegue Manual paso a paso

```bash
# 1. Autenticarse
oc login --server=$OPENSHIFT_SERVER --token=$OPENSHIFT_TOKEN --insecure-skip-tls-verify=true

# 2. Crear/seleccionar namespace
oc create namespace $OPENSHIFT_NAMESPACE
oc project $OPENSHIFT_NAMESPACE

# 3. Aplicar manifiestos
oc apply -f openshift-deployment.yaml

# 4. Verificar estado
oc get all
oc logs -f deployment/microservicio
```

## Estructura de Despliegue

El despliegue configura los siguientes recursos en OpenShift:

### Base de Datos (PostgreSQL)
- **StatefulSet**: `postgres` (1 réplica)
- **Service**: `postgres`
- **Storage**: 5Gi PersistentVolume
- **Credenciales**: Secret `postgres-credentials`

### Aplicación (Microservicio)
- **Deployment**: `microservicio` (2 réplicas)
- **Service**: `microservicio`
- **Route**: Acceso HTTPS automático
- **HPA**: Auto-escalado (2-5 réplicas)
- **Probes**: Liveness y readiness checks

### Seguridad
- **NetworkPolicy**: Restricciones de tráfico
- **SecurityContext**: Ejecución sin privilegios
- **ConfigMaps**: Variables de configuración
- **Secrets**: Credenciales seguras

## Verificar el Despliegue

```bash
# Ver todos los recursos
oc get all

# Ver pods
oc get pods

# Ver logs de la aplicación
oc logs -f deployment/microservicio

# Ver logs de PostgreSQL
oc logs -f statefulset/postgres

# Ver servicios y rutas
oc get svc,routes

# Describir un pod
oc describe pod <pod-name>

# Acceder a la aplicación
oc get route microservicio -o jsonpath='{.spec.host}'
# Luego acceder a https://<host-obtenido>
```

## Solucionar Problemas

### Error de autenticación
```bash
# Verificar el token
echo $OPENSHIFT_TOKEN

# Probar la conexión
oc status
```

### Pod no inicia
```bash
# Ver eventos
oc describe pod <pod-name>

# Ver logs de error
oc logs <pod-name> --previous
```

### Problemas de base de datos
```bash
# Verificar credenciales
oc get secret postgres-credentials -o yaml

# Conectar a PostgreSQL
oc exec -it postgres-0 -- psql -U usuario -d microservicio
```

### Despliegue atascado
```bash
# Rollback a versión anterior
oc rollout undo deployment/microservicio

# Eliminar y reimplementar
oc delete deployment microservicio
oc apply -f openshift-deployment.yaml
```

## Actualizar la Aplicación

Para actualizar la aplicación con una nueva versión:

```powershell
# Windows
.\deploy-openshift.ps1 -ImageTag "v1.1.0"
```

```bash
# Linux/macOS
./deploy-openshift.sh v1.1.0 quay.io tu-usuario
```

## Configuración de Credenciales en OpenShift

Las credenciales están almacenadas en el Secret `postgres-credentials`. Para cambiarlas:

```bash
# Ver credenciales actuales
oc get secret postgres-credentials -o yaml

# Actualizar credenciales
oc edit secret postgres-credentials

# O eliminar y recrear con nuevas credenciales
oc delete secret postgres-credentials
oc create secret generic postgres-credentials \
  --from-literal=db-user=nuevo-usuario \
  --from-literal=db-password=nueva-contraseña
```

## Monitoreo y Logs

```bash
# Ver logs en tiempo real
oc logs -f deployment/microservicio

# Ver logs de los últimos 100 líneas
oc logs deployment/microservicio --tail=100

# Ver logs de un pod específico
oc logs <pod-name>

# Ver eventos del namespace
oc get events
```

## Escalado Manual

```bash
# Escalar manualmente
oc scale deployment microservicio --replicas=3

# Ver estado del HPA
oc get hpa
```

## Eliminar el Despliegue

```bash
# Eliminar todos los recursos del despliegue
oc delete -f openshift-deployment.yaml

# O eliminar por namespace
oc delete namespace $OPENSHIFT_NAMESPACE
```

## Notas Importantes

- ✅ El script valida todas las variables de entorno antes de ejecutar
- ✅ Implementa reinicio ordenado (rolling updates)
- ✅ Incluye health checks (liveness y readiness probes)
- ✅ Auto-escalado basado en CPU y memoria
- ✅ Políticas de red para mayor seguridad
- ✅ Almacenamiento persistente para la base de datos
- ✅ Ruta HTTPS automática con OpenShift
- ✅ Credenciales seguras en Secrets

## Recursos Adicionales

- [Documentación oficial de OpenShift](https://docs.openshift.com/)
- [OpenShift CLI Guide](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/index.html)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
