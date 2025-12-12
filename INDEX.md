# 📚 Índice Completo - Despliegue a OpenShift

Bienvenido al sistema de despliegue automático a OpenShift. Esta es tu guía de navegación completa.

## 🎯 Empezar Aquí

**Si es tu primera vez**, empieza con:
1. **[`SETUP_SUMMARY.md`](SETUP_SUMMARY.md)** - Resumen de todo lo que se ha configurado (5 min)
2. **[`QUICKSTART.md`](QUICKSTART.md)** - Guía rápida de inicio (10 min)
3. **[`EXAMPLE_WALKTHROUGH.md`](EXAMPLE_WALKTHROUGH.md)** - Ejemplo paso a paso (20 min)

## 📖 Documentación Completa

### 1. Inicio Rápido
- **[`QUICKSTART.md`](QUICKSTART.md)** - Guía de 5 minutos para empezar
  - Variables de entorno necesarias
  - Cómo ejecutar los scripts
  - Verificación básica

### 2. Despliegue Detallado
- **[`OPENSHIFT_DEPLOYMENT.md`](OPENSHIFT_DEPLOYMENT.md)** - Documentación completa
  - Requisitos previos
  - Guía paso a paso
  - Estructura del despliegue
  - Solucionar problemas comunes
  - Monitoreo y logs
  - Actualizaciones y escalado

### 3. Configuración Avanzada
- **[`ADVANCED_CONFIGURATION.md`](ADVANCED_CONFIGURATION.md)** - Para producción
  - Gestión segura de secretos
  - Monitoreo y alertas
  - CI/CD avanzado
  - RBAC y seguridad
  - Despliegue canario
  - Multi-región

### 4. Ejemplo Paso a Paso
- **[`EXAMPLE_WALKTHROUGH.md`](EXAMPLE_WALKTHROUGH.md)** - Tutorial completo
  - Obtener el token
  - Configurar variables
  - Ejecutar el despliegue
  - Verificar resultados
  - Troubleshooting
  - Limpiar recursos

### 5. Resumen General
- **[`SETUP_SUMMARY.md`](SETUP_SUMMARY.md)** - Resumen ejecutivo
  - Descripción de archivos creados
  - Inicio rápido (3 pasos)
  - Características principales
  - Próximos pasos recomendados

## 🛠️ Scripts y Herramientas

### Scripts de Despliegue

```bash
# Windows (PowerShell)
.\deploy-openshift.ps1
.\deploy-openshift.ps1 -ImageTag "v1.0.0"

# Linux/macOS (Bash)
./deploy-openshift.sh
./deploy-openshift.sh v1.0.0 quay.io mi-usuario
```

### Herramienta de Monitoreo (Python)

```bash
python openshift-manager.py status        # Ver estado
python openshift-manager.py logs --follow # Ver logs
python openshift-manager.py describe      # Describir pod
python openshift-manager.py restart       # Reiniciar
python openshift-manager.py db-check      # Verificar BD
python openshift-manager.py health        # Health check
```

## 📁 Estructura de Archivos

### Scripts de Despliegue
```
deploy-openshift.ps1         ← Script para Windows
deploy-openshift.sh          ← Script para Linux/macOS
openshift-manager.py         ← Herramienta de monitoreo
```

### Configuración
```
openshift-deployment.yaml    ← Manifiestos de Kubernetes/OpenShift
.env.example                 ← Plantilla de variables de entorno
.github/workflows/*.yml      ← Pipeline CI/CD
```

### Documentación
```
SETUP_SUMMARY.md            ← Resumen (EMPEZAR AQUÍ)
QUICKSTART.md               ← Guía rápida
OPENSHIFT_DEPLOYMENT.md     ← Documentación detallada
ADVANCED_CONFIGURATION.md   ← Configuraciones avanzadas
EXAMPLE_WALKTHROUGH.md      ← Tutorial paso a paso
```

## 🚀 Flujos de Trabajo Comunes

### 1. Primer Despliegue
```
1. Lee QUICKSTART.md
2. Configura variables de entorno
3. Ejecuta deploy-openshift.ps1 o deploy-openshift.sh
4. Verifica con oc get all
5. Accede a la aplicación
```

### 2. Actualizar Aplicación
```
1. Haz cambios en el código
2. Ejecuta deploy-openshift.ps1 -ImageTag "v1.1.0"
3. OpenShift hace rolling update automático
4. Verifica con oc rollout status
```

### 3. Monitorear en Producción
```
1. Usa python openshift-manager.py status
2. Ve logs con python openshift-manager.py logs --follow
3. Describe pods con python openshift-manager.py describe
4. Reinicia si es necesario con python openshift-manager.py restart
```

### 4. Solucionar Problemas
```
1. Lee OPENSHIFT_DEPLOYMENT.md sección "Solucionar problemas"
2. Ejecuta oc logs deployment/microservicio
3. Describe el pod con oc describe pod <pod-name>
4. Ve eventos con oc get events
5. Usa openshift-manager.py para debugging
```

## 📋 Variables de Entorno Necesarias

```
OPENSHIFT_SERVER        ← https://api.tu-cluster.com:6443
OPENSHIFT_TOKEN         ← Tu token de autenticación
OPENSHIFT_NAMESPACE     ← Namespace donde desplegar
```

**Cómo obtener el token:**
1. Abre consola web de OpenShift
2. Haz clic en tu usuario (esquina superior derecha)
3. Selecciona "Copy login command"
4. Extrae el token del comando

## ✨ Lo que se Despliega

- **PostgreSQL 15** - Base de datos con almacenamiento persistente
- **Microservicio** - 2 réplicas con auto-escalado (2-5 réplicas)
- **Health Checks** - Liveness y readiness probes
- **HTTPS** - Ruta segura automática
- **Monitoreo** - Logs centralizados y métricas
- **HPA** - Auto-escalado por CPU (70%) y memoria (80%)
- **Seguridad** - NetworkPolicy y SecurityContext

## 🔐 Seguridad

- ✅ Variables de entorno validadas
- ✅ Credenciales en Kubernetes Secrets
- ✅ Sin privilegios de root
- ✅ Restricción de tráfico con NetworkPolicy
- ✅ HTTPS automático

## 📊 Monitoreo

```bash
# Ver estado general
oc get all

# Ver pods en detalle
oc get pods -o wide

# Ver logs en tiempo real
oc logs -f deployment/microservicio

# Ver uso de recursos
oc top pods

# Ver auto-escalado
oc get hpa

# Ver eventos
oc get events
```

## 🎓 Documentos Recomendados por Rol

### Para DevOps/SRE
1. Lee `SETUP_SUMMARY.md`
2. Lee `OPENSHIFT_DEPLOYMENT.md`
3. Lee `ADVANCED_CONFIGURATION.md`
4. Configura CI/CD en GitHub Actions

### Para Desarrolladores
1. Lee `QUICKSTART.md`
2. Lee `EXAMPLE_WALKTHROUGH.md`
3. Ejecuta `deploy-openshift.ps1` o `deploy-openshift.sh`
4. Usa `openshift-manager.py` para monitoreo

### Para DevOps que Audita
1. Lee `OPENSHIFT_DEPLOYMENT.md`
2. Revisa `openshift-deployment.yaml`
3. Verifica seguridad en `ADVANCED_CONFIGURATION.md`
4. Revisa `.github/workflows/deploy-openshift.yml`

### Para Operaciones/Soporte
1. Lee `OPENSHIFT_DEPLOYMENT.md` sección "Monitoreo"
2. Usa `openshift-manager.py` para troubleshooting
3. Consulta `EXAMPLE_WALKTHROUGH.md` para soluciones

## 🔗 Enlaces Útiles

- [Documentación oficial de OpenShift](https://docs.openshift.com/)
- [OpenShift CLI Reference](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## ⚡ Comandos Rápidos

```bash
# Configurar variables (ajusta los valores)
export OPENSHIFT_SERVER="https://api.tu-cluster.com:6443"
export OPENSHIFT_TOKEN="tu-token-aqui"
export OPENSHIFT_NAMESPACE="tu-namespace"

# Ejecutar despliegue
./deploy-openshift.sh

# Ver estado
oc get all

# Ver logs
oc logs -f deployment/microservicio

# Obtener URL
oc get route microservicio -o jsonpath='{.spec.host}'

# Reiniciar
oc rollout restart deployment/microservicio

# Eliminar todo
oc delete namespace $OPENSHIFT_NAMESPACE
```

## 📞 Checklist de Verificación

- [ ] Variables de entorno configuradas
- [ ] OpenShift CLI instalado y funcionando
- [ ] Docker instalado y corriendo
- [ ] Script de despliegue ejecutado exitosamente
- [ ] Pods en estado Running (2/2)
- [ ] Servicios creados
- [ ] Ruta disponible
- [ ] Health check respondiendo
- [ ] Logs sin errores
- [ ] HPA activo

## 🎯 Próximos Pasos

1. **Inmediato:** Configura las variables de entorno
2. **Hoy:** Ejecuta el primer despliegue
3. **Esta semana:** Configura monitoreo y alertas
4. **Este mes:** Configura CI/CD en GitHub Actions

## 📚 Lecturas Adicionales

- **Kubernetes Best Practices:** https://kubernetes.io/docs/concepts/configuration/overview/
- **OpenShift Security:** https://docs.openshift.com/container-platform/latest/security/index.html
- **PostgreSQL on Kubernetes:** https://www.postgresql.org/
- **Docker Best Practices:** https://docs.docker.com/develop/dev-best-practices/

## ✅ Resumen

Has recibido un **sistema completo de despliegue a OpenShift** con:

✅ Scripts automáticos (PowerShell y Bash)
✅ Manifiestos de Kubernetes optimizados
✅ Pipeline CI/CD con GitHub Actions
✅ Herramienta de monitoreo en Python
✅ Documentación completa (5 guías)
✅ Ejemplos paso a paso
✅ Soluciones para producción
✅ Mejores prácticas de seguridad

**¿Por dónde empiezas?**
→ Lee [`QUICKSTART.md`](QUICKSTART.md) (10 minutos)
→ Ejecuta `.\deploy-openshift.ps1` o `./deploy-openshift.sh`
→ Verifica con `oc get all`
→ ¡Listo! 🚀

---

**Última actualización:** Diciembre 2024
**Versión:** 1.0.0
**Estado:** ✅ Listo para producción
