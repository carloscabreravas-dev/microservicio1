# 🚀 Despliegue Automático a OpenShift - Resumen Completo

## 📌 Descripción General

He creado un sistema completo y automatizado para desplegar tu microservicio a OpenShift usando las variables de entorno `OPENSHIFT_SERVER`, `OPENSHIFT_TOKEN` y `OPENSHIFT_NAMESPACE`.

## 📁 Archivos Creados

### Scripts de Despliegue

| Archivo | Descripción | Uso |
|---------|-------------|-----|
| **`deploy-openshift.ps1`** | Script PowerShell para Windows | `.\deploy-openshift.ps1 -ImageTag v1.0.0` |
| **`deploy-openshift.sh`** | Script Bash para Linux/macOS | `./deploy-openshift.sh v1.0.0` |

### Configuración de Kubernetes/OpenShift

| Archivo | Descripción |
|---------|-------------|
| **`openshift-deployment.yaml`** | Manifiestos completos (PostgreSQL, Deployment, Service, Route, HPA, NetworkPolicy) |
| **`.github/workflows/deploy-openshift.yml`** | Pipeline CI/CD automático con GitHub Actions |

### Herramientas Auxiliares

| Archivo | Descripción | Uso |
|---------|-------------|-----|
| **`openshift-manager.py`** | Gestor Python para monitoreo y troubleshooting | `python openshift-manager.py status` |
| **`.env.example`** | Plantilla de variables de entorno | `cp .env.example .env` |

### Documentación

| Archivo | Contenido |
|---------|----------|
| **`QUICKSTART.md`** | Guía rápida de inicio (inicio recomendado) |
| **`OPENSHIFT_DEPLOYMENT.md`** | Documentación detallada del despliegue |
| **`ADVANCED_CONFIGURATION.md`** | Configuraciones avanzadas para producción |

## 🎯 Inicio Rápido (3 pasos)

### Paso 1: Configurar variables de entorno

**Windows (PowerShell):**
```powershell
$env:OPENSHIFT_SERVER = "https://api.tu-cluster.com:6443"
$env:OPENSHIFT_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjJ3M..."
$env:OPENSHIFT_NAMESPACE = "tu-namespace"
```

**Linux/macOS (Bash):**
```bash
export OPENSHIFT_SERVER="https://api.tu-cluster.com:6443"
export OPENSHIFT_TOKEN="eyJhbGciOiJSUzI1NiIsImtpZCI6IjJ3M..."
export OPENSHIFT_NAMESPACE="tu-namespace"
```

### Paso 2: Ejecutar el script de despliegue

**Windows:**
```powershell
cd c:\Users\carlosc2\proyecto\microservicio1
.\deploy-openshift.ps1
```

**Linux/macOS:**
```bash
cd ~/proyecto/microservicio1
chmod +x deploy-openshift.sh
./deploy-openshift.sh
```

### Paso 3: Verificar el despliegue

```bash
# Ver estado
oc get all -n tu-namespace

# Ver logs
oc logs -f deployment/microservicio -n tu-namespace

# Obtener URL de acceso
oc get route microservicio -n tu-namespace -o jsonpath='{.spec.host}'
```

## ✨ Características Principales

### 🔐 Seguridad
- ✅ Variables de entorno obligatorias validadas
- ✅ Credenciales en Kubernetes Secrets
- ✅ SecurityContext sin privilegios
- ✅ NetworkPolicy para restricción de tráfico
- ✅ HTTPS automático con rutas de OpenShift

### 🚀 Despliegue
- ✅ Rolling updates sin downtime
- ✅ 2 réplicas por defecto
- ✅ Auto-escalado (HPA: 2-5 réplicas)
- ✅ Escalado por CPU (70%) y memoria (80%)

### 📊 Monitoreo
- ✅ Health checks (liveness + readiness)
- ✅ Logs centralizados
- ✅ Métricas de rendimiento
- ✅ Herramienta de troubleshooting integrada

### 🗄️ Base de Datos
- ✅ PostgreSQL 15 Alpine
- ✅ StatefulSet con almacenamiento persistente (5Gi)
- ✅ Credenciales seguras en Secret
- ✅ Health checks automáticos

### 🔄 CI/CD
- ✅ Pipeline de GitHub Actions automático
- ✅ Construcción y push de imágenes Docker
- ✅ Soporte para múltiples ambientes
- ✅ Despliegue automático en push a main

## 📖 Documentación Disponible

### Para Empezar Rápido
→ Lee **`QUICKSTART.md`** (10 min)

### Para Entender Todo
→ Lee **`OPENSHIFT_DEPLOYMENT.md`** (30 min)

### Para Producción
→ Lee **`ADVANCED_CONFIGURATION.md`** (1 hora)

## 🛠️ Herramientas Auxiliares

### Script Python para Monitoreo

```bash
# Ver estado general
python openshift-manager.py status

# Ver logs en tiempo real
python openshift-manager.py logs --follow --tail 100

# Describir un pod
python openshift-manager.py describe

# Reiniciar deployment
python openshift-manager.py restart

# Verificar base de datos
python openshift-manager.py db-check

# Probar health check
python openshift-manager.py health
```

## 🔄 Flujo de Despliegue Completo

```
1. Autenticación en OpenShift
   ↓
2. Validación de namespace
   ↓
3. Construcción de imagen Docker
   ↓
4. Push a registry (opcional)
   ↓
5. Aplicación de manifiestos YAML
   ↓
6. Actualización de imagen en Deployment
   ↓
7. Espera a que esté listo (health checks)
   ↓
8. Verificación de pods y servicios
   ↓
9. Mostrar rutas de acceso
   ↓
10. Mostrar logs
```

## 🔍 Solucionar Problemas Comunes

### Error: "password authentication failed"
```bash
# Verificar credenciales
oc get secret postgres-credentials -o yaml

# Ver logs de PostgreSQL
oc logs statefulset/postgres -n tu-namespace
```

### Pod no inicia
```bash
# Ver eventos
oc describe pod <pod-name>

# Ver logs previos
oc logs <pod-name> --previous

# Ver estado detallado
oc get pod <pod-name> -o yaml
```

### Problemas de conectividad
```bash
# Verificar NetworkPolicy
oc get networkpolicy -n tu-namespace

# Verificar resolución de DNS
oc exec -it <pod-name> -- nslookup postgres

# Port forward para debugging
oc port-forward service/postgres 5432:5432
```

## 📊 Monitoreo en Producción

### Ver estado del HPA
```bash
oc get hpa -n tu-namespace
oc describe hpa microservicio-hpa -n tu-namespace
```

### Ver métricas
```bash
oc top nodes
oc top pods -n tu-namespace
```

### Ver logs centralizados
```bash
oc logs -f deployment/microservicio -n tu-namespace --all-containers=true
```

## 🚀 Próximos Pasos Recomendados

1. **Configurar el token:**
   - Obtén tu token desde la consola web de OpenShift
   - Configura las variables de entorno

2. **Ejecutar el despliegue:**
   - Ejecuta `./deploy-openshift.ps1` o `./deploy-openshift.sh`
   - Espera a que la aplicación esté lista

3. **Verificar acceso:**
   - Obtén la URL de la ruta
   - Accede a https://[host]/health

4. **Monitorear:**
   - Usa `python openshift-manager.py status`
   - Revisa los logs regularmente

5. **Configurar CI/CD (opcional):**
   - Configura los secrets en GitHub
   - El despliegue será automático en push a main

## 💡 Tips Importantes

- 🔐 **Seguridad:** Nunca guardes credenciales en archivos de configuración
- 📦 **Versionado:** Usa etiquetas semánticas para las imágenes (v1.0.0, v1.1.0)
- 📊 **Monitoreo:** Revisa los logs regularmente
- 🔄 **Updates:** Ejecuta el script nuevamente para actualizar a una nueva versión
- 🗑️ **Limpieza:** Usa `oc delete namespace tu-namespace` para eliminar todo

## 🆘 Soporte

### Para obtener más información:

```bash
# Login a OpenShift
oc login --server=$OPENSHIFT_SERVER --token=$OPENSHIFT_TOKEN

# Ver ayuda de oc
oc --help
oc describe --help

# Ver documentación oficial
echo "https://docs.openshift.com/"
```

## 📋 Checklist Antes de Producción

- [ ] Todas las variables de entorno configuradas
- [ ] Credenciales de base de datos seguras
- [ ] HTTPS habilitado (incluido)
- [ ] Health checks funcionando
- [ ] Logs centralizados
- [ ] HPA configurado
- [ ] Backups de base de datos configurados
- [ ] Monitoreo y alertas setup
- [ ] Runbook de troubleshooting listo
- [ ] Plan de rollback definido

## 📞 Contacto y Preguntas

Para más información, consulta:
- `OPENSHIFT_DEPLOYMENT.md` - Documentación detallada
- `ADVANCED_CONFIGURATION.md` - Configuraciones avanzadas
- [Documentación oficial de OpenShift](https://docs.openshift.com/)

---

**✅ Despliegue automático a OpenShift completamente configurado y listo para usar**
