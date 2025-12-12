# Script de despliegue automático a OpenShift
# Uso: .\deploy-openshift.ps1

param(
    [string]$ImageTag = "latest",
    [string]$ImageRegistry = "quay.io",
    [string]$ImageNamespace = "carloscabreravas"
)

# Validar variables de entorno requeridas
$requiredEnvVars = @("OPENSHIFT_SERVER", "OPENSHIFT_TOKEN", "OPENSHIFT_NAMESPACE")
$missingVars = @()

foreach ($var in $requiredEnvVars) {
    if (-not (Test-Path env:$var)) {
        $missingVars += $var
    }
}

if ($missingVars.Count -gt 0) {
    Write-Host "❌ Error: Las siguientes variables de entorno no están definidas:" -ForegroundColor Red
    $missingVars | ForEach-Object { Write-Host "   - $_" -ForegroundColor Red }
    Write-Host ""
    Write-Host "Por favor, defina estas variables antes de ejecutar el script:" -ForegroundColor Yellow
    Write-Host "   `$env:OPENSHIFT_SERVER = 'https://api.ejemplo.com:6443'" -ForegroundColor Cyan
    Write-Host "   `$env:OPENSHIFT_TOKEN = 'tu-token-aqui'" -ForegroundColor Cyan
    Write-Host "   `$env:OPENSHIFT_NAMESPACE = 'tu-namespace'" -ForegroundColor Cyan
    exit 1
}

# Variables locales
$appName = "microservicio"
$imageName = "${ImageRegistry}/${ImageNamespace}/${appName}:${ImageTag}"
$server = $env:OPENSHIFT_SERVER
$token = $env:OPENSHIFT_TOKEN
$namespace = $env:OPENSHIFT_NAMESPACE

Write-Host "🚀 Iniciando despliegue a OpenShift" -ForegroundColor Cyan
Write-Host ""
Write-Host "Configuración:" -ForegroundColor Green
Write-Host "  Servidor: $server"
Write-Host "  Namespace: $namespace"
Write-Host "  Imagen: $imageName"
Write-Host ""

try {
    # 1. Login a OpenShift
    Write-Host "1️⃣  Autenticando con OpenShift..." -ForegroundColor Yellow
    oc login --server=$server --token=$token --insecure-skip-tls-verify=true | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Error al autenticarse con OpenShift"
    }
    Write-Host "   ✓ Autenticación exitosa" -ForegroundColor Green
    Write-Host ""

    # 2. Seleccionar namespace
    Write-Host "2️⃣  Seleccionando namespace..." -ForegroundColor Yellow
    oc project $namespace
    if ($LASTEXITCODE -ne 0) {
        Write-Host "   ⚠️  Namespace no existe, creando..." -ForegroundColor Cyan
        oc create namespace $namespace
    }
    Write-Host "   ✓ Namespace seleccionado" -ForegroundColor Green
    Write-Host ""

    # 3. Construir imagen Docker
    Write-Host "3️⃣  Construyendo imagen Docker..." -ForegroundColor Yellow
    docker build -t $imageName -f Dockerfile .
    if ($LASTEXITCODE -ne 0) {
        throw "Error al construir la imagen Docker"
    }
    Write-Host "   ✓ Imagen construida: $imageName" -ForegroundColor Green
    Write-Host ""

    # 4. Publicar imagen (si es necesario)
    Write-Host "4️⃣  Publicando imagen a registro..." -ForegroundColor Yellow
    docker push $imageName
    if ($LASTEXITCODE -ne 0) {
        Write-Host "   ⚠️  Advertencia: No se pudo publicar la imagen" -ForegroundColor Yellow
        Write-Host "   Continuar sin publicar" -ForegroundColor Yellow
    } else {
        Write-Host "   ✓ Imagen publicada" -ForegroundColor Green
    }
    Write-Host ""

    # 5. Aplicar manifiestos de OpenShift
    Write-Host "5️⃣  Aplicando configuración a OpenShift..." -ForegroundColor Yellow
    
    # Crear/actualizar ConfigMaps y Secrets
    oc apply -f openshift-deployment.yaml -n $namespace
    if ($LASTEXITCODE -ne 0) {
        throw "Error al aplicar la configuración"
    }
    Write-Host "   ✓ Configuración aplicada" -ForegroundColor Green
    Write-Host ""

    # 6. Esperar a que el despliegue esté listo
    Write-Host "6️⃣  Esperando a que el despliegue esté listo..." -ForegroundColor Yellow
    oc rollout status deployment/$appName -n $namespace --timeout=10m
    if ($LASTEXITCODE -ne 0) {
        Write-Host "   ⚠️  Despliegue tardó más de lo esperado" -ForegroundColor Yellow
    } else {
        Write-Host "   ✓ Despliegue completado" -ForegroundColor Green
    }
    Write-Host ""

    # 7. Obtener información del despliegue
    Write-Host "7️⃣  Información del despliegue:" -ForegroundColor Yellow
    Write-Host ""
    oc get deployment,pods,svc -n $namespace | Select-Object -Index 0,1,2,3,4,5
    Write-Host ""

    # 8. Obtener ruta de acceso
    Write-Host "8️⃣  Rutas disponibles:" -ForegroundColor Yellow
    $routes = oc get routes -n $namespace -o json | ConvertFrom-Json
    if ($routes.items.Count -gt 0) {
        $routes.items | ForEach-Object {
            $host = $_.spec.host
            $service = $_.spec.to.name
            Write-Host "   - https://$host (servicio: $service)" -ForegroundColor Cyan
        }
    } else {
        Write-Host "   ⚠️  No hay rutas configuradas" -ForegroundColor Yellow
    }
    Write-Host ""

    # 9. Verificar logs
    Write-Host "9️⃣  Últimos logs:" -ForegroundColor Yellow
    $podName = oc get pods -n $namespace -l app=$appName -o jsonpath='{.items[0].metadata.name}'
    if ($podName) {
        oc logs $podName -n $namespace --tail=10
    }
    Write-Host ""

    Write-Host "✅ Despliegue completado exitosamente" -ForegroundColor Green
    
} catch {
    Write-Host ""
    Write-Host "❌ Error: $_" -ForegroundColor Red
    exit 1
}
