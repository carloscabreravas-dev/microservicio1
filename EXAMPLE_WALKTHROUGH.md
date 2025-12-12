# Ejemplo Paso a Paso: Despliegue a OpenShift

Esta guía proporciona un ejemplo real de cómo desplegar el microservicio a OpenShift.

## 📋 Requisitos Previos

- OpenShift CLI (`oc`) instalado
- Docker instalado
- Acceso a un cluster de OpenShift
- Token de OpenShift válido
- Conexión a Internet

## 🎯 Ejemplo Completo: Desplegar a OpenShift

### Paso 1: Obtener el Token de OpenShift

1. **Abre la consola web de OpenShift** en tu navegador
   - URL: `https://tu-cluster.com:6443`

2. **Inicia sesión** con tus credenciales

3. **Haz clic en tu usuario** (esquina superior derecha)

4. **Selecciona "Copy login command"**

5. **Copia el comando que aparece**
   ```
   oc login --server=https://api.ejemplo.com:6443 --token=sha256~abcd1234...
   ```

6. **Extrae el token:**
   ```
   OPENSHIFT_TOKEN=sha256~abcd1234...
   OPENSHIFT_SERVER=https://api.ejemplo.com:6443
   ```

### Paso 2: Configurar Variables de Entorno

#### En Windows (PowerShell):

```powershell
# Abre PowerShell y ejecuta:
$env:OPENSHIFT_SERVER = "https://api.ejemplo.com:6443"
$env:OPENSHIFT_TOKEN = "sha256~abcd1234..."
$env:OPENSHIFT_NAMESPACE = "mi-microservicio"

# Verifica que están configuradas:
echo $env:OPENSHIFT_SERVER
echo $env:OPENSHIFT_TOKEN
echo $env:OPENSHIFT_NAMESPACE
```

#### En Linux/macOS (Bash):

```bash
# Abre terminal y ejecuta:
export OPENSHIFT_SERVER="https://api.ejemplo.com:6443"
export OPENSHIFT_TOKEN="sha256~abcd1234..."
export OPENSHIFT_NAMESPACE="mi-microservicio"

# Verifica que están configuradas:
echo $OPENSHIFT_SERVER
echo $OPENSHIFT_TOKEN
echo $OPENSHIFT_NAMESPACE
```

### Paso 3: Verificar la Conexión a Docker

```bash
# Verifica que Docker está ejecutándose
docker --version
docker ps

# Output esperado: Docker version 20.10.x
```

### Paso 4: Navegar al Directorio del Proyecto

#### Windows (PowerShell):
```powershell
cd c:\Users\carlosc2\proyecto\microservicio1
dir  # Verifica que ves los archivos del proyecto
```

#### Linux/macOS (Bash):
```bash
cd ~/proyecto/microservicio1
ls  # Verifica que ves los archivos del proyecto
```

### Paso 5: Ejecutar el Script de Despliegue

#### Windows (PowerShell):

```powershell
# Ejecutar con valores por defecto
.\deploy-openshift.ps1

# O con parámetros personalizados
.\deploy-openshift.ps1 -ImageTag "v1.0.0" -ImageRegistry "quay.io" -ImageNamespace "mi-usuario"
```

**Output esperado:**

```
🚀 Iniciando despliegue a OpenShift

Configuración:
  Servidor: https://api.ejemplo.com:6443
  Namespace: mi-microservicio
  Imagen: quay.io/mi-usuario/microservicio:latest

1️⃣  Autenticando con OpenShift...
   ✓ Autenticación exitosa

2️⃣  Seleccionando namespace...
   ✓ Namespace seleccionado

3️⃣  Construyendo imagen Docker...
   ✓ Imagen construida: quay.io/mi-usuario/microservicio:latest

4️⃣  Publicando imagen a registro...
   ✓ Imagen publicada

5️⃣  Aplicando configuración a OpenShift...
   ✓ Configuración aplicada

6️⃣  Esperando a que el despliegue esté listo...
   ✓ Despliegue completado

7️⃣  Información del despliegue:
NAME              READY   UP-TO-DATE   AVAILABLE   AGE
microservicio     2/2     2            2           45s

8️⃣  Rutas disponibles:
   - https://microservicio-mi-microservicio.ejemplo.com (servicio: microservicio)

9️⃣  Últimos logs:
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.

✅ Despliegue completado exitosamente
```

#### Linux/macOS (Bash):

```bash
# Hacer el script ejecutable
chmod +x deploy-openshift.sh

# Ejecutar con valores por defecto
./deploy-openshift.sh

# O con parámetros personalizados
./deploy-openshift.sh v1.0.0 quay.io mi-usuario
```

### Paso 6: Verificar el Despliegue

```bash
# Verificar que estás en el namespace correcto
oc project

# Ver todos los recursos
oc get all

# Ver los pods en detalle
oc get pods -o wide

# Ver los servicios
oc get svc

# Ver las rutas
oc get routes

# Ver configuración y secretos
oc get configmap,secret
```

**Output esperado:**

```
NAME                           READY   STATUS    RESTARTS   AGE
pod/microservicio-6fd5fc567-d9f6j   1/1     Running   0          2m
pod/microservicio-6fd5fc567-k8l9m   1/1     Running   0          2m
pod/postgres-0                       1/1     Running   0          3m

NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)
service/microservicio    ClusterIP   172.30.200.1    <none>        80/TCP
service/postgres         ClusterIP   None            <none>        5432/TCP

NAME                                  HOST/PORT                                     PATH   SERVICES      PORT   TERMINATION   WILDCARD
route.route.openshift.io/microservicio   microservicio-mi-microservicio.ejemplo.com          microservicio   http   edge          None
```

### Paso 7: Obtener la URL de Acceso

```bash
# Obtener la URL completa
oc get route microservicio -o jsonpath='https://{.spec.host}/health'

# Output esperado:
# https://microservicio-mi-microservicio.ejemplo.com/health

# Acceder en el navegador (opcional, requiere que la app esté lista)
# https://microservicio-mi-microservicio.ejemplo.com/
```

### Paso 8: Ver Logs de la Aplicación

```bash
# Ver logs en tiempo real
oc logs -f deployment/microservicio

# Ver logs de los últimos 50 líneas
oc logs deployment/microservicio --tail=50

# Ver logs de un pod específico
oc logs pod/microservicio-6fd5fc567-d9f6j

# Ver logs de la base de datos
oc logs statefulset/postgres
```

### Paso 9: Verificar la Salud de la Aplicación

```bash
# Ejecutar un health check desde dentro del cluster
oc exec -it deployment/microservicio -- curl http://localhost:8000/health

# Output esperado:
# {"status": "ok", "database": "connected"}
```

### Paso 10: Monitorear el Despliegue

```bash
# Ver estado del HPA (auto-escalado)
oc get hpa

# Ver métricas en tiempo real
oc top pods
oc top nodes

# Describir un pod para ver eventos
oc describe pod pod/microservicio-6fd5fc567-d9f6j
```

## 🎁 Ejemplo Avanzado: Despliegue con Versión Específica

```bash
# Supongamos que quieres desplegar la versión v1.2.0
# en un registry personalizado

# Windows (PowerShell)
.\deploy-openshift.ps1 -ImageTag "v1.2.0" -ImageRegistry "tu-registry.com" -ImageNamespace "tu-usuario"

# Linux/macOS (Bash)
./deploy-openshift.sh v1.2.0 tu-registry.com tu-usuario
```

## 🔍 Ejemplo: Troubleshooting

### Problema: Pod no inicia

```bash
# Ver estado detallado del pod
oc describe pod microservicio-6fd5fc567-d9f6j

# Ver logs de error
oc logs pod/microservicio-6fd5fc567-d9f6j --previous

# Ver eventos del namespace
oc get events --sort-by='.lastTimestamp'
```

### Problema: Error de autenticación en base de datos

```bash
# Verificar credenciales
oc get secret postgres-credentials -o yaml

# Conectar directamente a PostgreSQL
oc exec -it postgres-0 -- psql -U usuario -d microservicio -c "SELECT 1"

# Ver logs de PostgreSQL
oc logs statefulset/postgres --tail=100
```

### Problema: Aplicación lenta

```bash
# Ver uso de recursos
oc top pods
oc top nodes

# Ver estado del HPA
oc get hpa -w  # -w para watch (actualización en tiempo real)

# Ver latencia con metricas
oc describe hpa microservicio-hpa
```

## 🔄 Ejemplo: Actualizar la Aplicación

```bash
# Despliegue una nueva versión
.\deploy-openshift.ps1 -ImageTag "v1.2.1"

# El script automáticamente:
# 1. Construye la imagen
# 2. La publica
# 3. Actualiza el deployment
# 4. Hace un rolling update sin downtime
# 5. Verifica que está listo

# Verificar que la actualización completó
oc rollout status deployment/microservicio
```

## 🔧 Ejemplo: Usar la Herramienta de Monitoreo

```bash
# Ver estado general
python openshift-manager.py status

# Ver logs en tiempo real
python openshift-manager.py logs --follow

# Describir un pod
python openshift-manager.py describe

# Reiniciar la aplicación
python openshift-manager.py restart

# Verificar la base de datos
python openshift-manager.py db-check

# Probar el endpoint de salud
python openshift-manager.py health
```

## 📊 Ejemplo: Verificar Métricas

```bash
# Recursos del nodo
oc describe node <node-name>

# Recursos de los pods
oc top pods --all-namespaces

# PVC (almacenamiento)
oc describe pvc postgres-storage-postgres-0
oc get pvc

# Almacenamiento usado
oc exec -it postgres-0 -- df -h
```

## 🗑️ Ejemplo: Limpiar Recursos

```bash
# Eliminar solo la aplicación (mantiene datos)
oc delete deployment microservicio
oc delete service microservicio
oc delete route microservicio

# Eliminar todo el despliegue
oc delete -f openshift-deployment.yaml

# Eliminar el namespace completo
oc delete namespace mi-microservicio

# Verificar que se eliminó
oc get all
```

## ✅ Checklist de Verificación

Después de desplegar, verifica que:

- [ ] Los 2 pods están en estado `Running`
- [ ] Los pods están listos (`1/1`)
- [ ] El servicio tiene una ClusterIP asignada
- [ ] La ruta existe y tiene un host asignado
- [ ] El HPA está activo y monitoreando
- [ ] Los logs muestran que la app inició correctamente
- [ ] El health check responde `200 OK`
- [ ] La base de datos está conectada
- [ ] Puedes acceder a la URL de la ruta en el navegador

## 🎓 Resumen del Flujo Completo

```
1. Obtener token de OpenShift
   ↓
2. Configurar variables de entorno
   ↓
3. Ejecutar script de despliegue
   ↓
4. Esperar a que construya y despliegue
   ↓
5. Verificar que todo está running
   ↓
6. Obtener URL de acceso
   ↓
7. Acceder a la aplicación
   ↓
8. Monitorear logs y salud
```

## 🆘 Si Algo No Funciona

1. **Verifica las variables de entorno:**
   ```bash
   echo $OPENSHIFT_SERVER
   echo $OPENSHIFT_TOKEN
   echo $OPENSHIFT_NAMESPACE
   ```

2. **Verifica la conexión a OpenShift:**
   ```bash
   oc status
   ```

3. **Verifica los logs:**
   ```bash
   oc logs -f deployment/microservicio
   ```

4. **Describe el pod con problemas:**
   ```bash
   oc describe pod <pod-name>
   ```

5. **Revisa `OPENSHIFT_DEPLOYMENT.md`** para soluciones específicas

---

**¡Listo! Tu microservicio está desplegado en OpenShift** 🎉
