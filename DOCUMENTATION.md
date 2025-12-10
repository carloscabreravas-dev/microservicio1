# Microservicio API con FastAPI y PostgreSQL

Microservicio completo en Python con FastAPI para gestionar usuarios y productos en PostgreSQL, incluye Docker, Kubernetes y CI/CD.

## 🚀 Características

- **FastAPI**: Framework moderno y rápido para APIs REST
- **PostgreSQL**: Base de datos relacional robusta
- **SQLAlchemy**: ORM para gestión de datos
- **Pydantic**: Validación de datos automática
- **Docker**: Containerización de la aplicación
- **Kubernetes**: Orquestación y escalado automático
- **GitHub Actions**: CI/CD automático a Docker Hub
- **Health Checks**: Sondeos de salud para monitoreo

## 📋 Requisitos Previos

- Python 3.11+
- Docker y Docker Compose
- Kubernetes CLI (kubectl)
- PostgreSQL (o usar Docker)
- Git

## 🏗️ Estructura del Proyecto

```
microservicio1/
├── app.py                 # Aplicación principal FastAPI
├── config.py             # Configuración de la aplicación
├── database.py           # Modelos y conexión a BD
├── schemas.py            # Esquemas Pydantic
├── routes.py             # Rutas de la API
├── requirements.txt      # Dependencias Python
├── Dockerfile            # Configuración Docker
├── .dockerignore         # Archivos a ignorar en Docker
├── k8s.yaml             # Configuración Kubernetes
├── .github/
│   └── workflows/
│       └── ci-cd.yaml   # Workflow de GitHub Actions
├── .env.example         # Variables de entorno de ejemplo
└── README.md            # Este archivo
```

## ⚙️ Instalación Local

### 1. Clonar el repositorio

```bash
git clone https://github.com/carloscabreravas-dev/microservicio1.git
cd microservicio1
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

### 5. Iniciar PostgreSQL (con Docker)

```bash
docker run -d \
  --name postgres \
  -e POSTGRES_USER=usuario \
  -e POSTGRES_PASSWORD=contraseña \
  -e POSTGRES_DB=microservicio \
  -p 5432:5432 \
  postgres:15-alpine
```

### 6. Ejecutar la aplicación

```bash
python app.py
# O con uvicorn directamente:
# uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en `http://localhost:8000`

## 📚 Documentación de la API

### Acceder a la documentación interactiva

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Endpoints Principales

#### Usuarios

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/usuarios` | Obtener todos los usuarios |
| GET | `/usuarios/{id}` | Obtener usuario por ID |
| POST | `/usuarios` | Crear nuevo usuario |
| PUT | `/usuarios/{id}` | Actualizar usuario |
| DELETE | `/usuarios/{id}` | Eliminar usuario |

#### Productos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/productos` | Obtener todos los productos |
| GET | `/productos/{id}` | Obtener producto por ID |
| POST | `/productos` | Crear nuevo producto |
| PUT | `/productos/{id}` | Actualizar producto |
| DELETE | `/productos/{id}` | Eliminar producto |

#### Health Check

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health` | Verificar estado del servicio |

### Ejemplos de Uso

**Crear un usuario:**

```bash
curl -X POST "http://localhost:8000/usuarios" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez",
    "email": "juan@example.com"
  }'
```

**Crear un producto:**

```bash
curl -X POST "http://localhost:8000/productos" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Laptop",
    "descripcion": "Laptop de alta performance",
    "precio": 1500000,
    "stock": 10
  }'
```

**Obtener usuarios:**

```bash
curl "http://localhost:8000/usuarios"
```

## 🐳 Docker

### Construir la imagen

```bash
docker build -t microservicio:latest .
```

### Ejecutar con Docker

```bash
docker run -d \
  --name microservicio \
  -p 8000:8000 \
  -e DATABASE_URL="postgresql://usuario:contraseña@postgres:5432/microservicio" \
  microservicio:latest
```

### Docker Compose

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: usuario
      POSTGRES_PASSWORD: contraseña
      POSTGRES_DB: microservicio
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://usuario:contraseña@postgres:5432/microservicio
    depends_on:
      - postgres

volumes:
  postgres_data:
```

Ejecutar:
```bash
docker-compose up -d
```

## ☸️ Kubernetes

### Desplegar en Kubernetes

```bash
# Aplicar la configuración
kubectl apply -f k8s.yaml

# Verificar el estado
kubectl get pods
kubectl get services

# Ver logs
kubectl logs -l app=microservicio

# Portwarding para acceder localmente
kubectl port-forward svc/microservicio 8000:80
```

### Actualizar imagen

```bash
kubectl set image deployment/microservicio \
  microservicio=carloscabreravas-dev/microservicio:v1.0.0
```

### Escalar manualmente

```bash
kubectl scale deployment microservicio --replicas=5
```

## 🔄 GitHub Actions CI/CD

El workflow automático hace lo siguiente:

1. **Build**: Construye la imagen Docker
2. **Push**: Envía la imagen a Docker Hub
3. **Test**: Ejecuta pruebas y análisis de código
4. **Deploy**: Despliega a Kubernetes (solo en main)

### Configurar Secretos en GitHub

Necesitas agregar estos secretos en tu repositorio:

```
DOCKER_USERNAME      # Tu usuario de Docker Hub
DOCKER_PASSWORD      # Tu token de Docker Hub
KUBE_CONFIG          # Tu kubeconfig en base64
```

**Para obtener tu kubeconfig en base64:**

```bash
cat ~/.kube/config | base64 -w 0
```

## 📊 Variables de Entorno

Copia `.env.example` a `.env` y actualiza:

```env
DEBUG=False
APP_NAME=Microservicio API
API_VERSION=1.0.0
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/microservicio
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]
```

## 🧪 Pruebas

### Instalar pytest

```bash
pip install pytest pytest-cov
```

### Ejecutar pruebas

```bash
pytest
```

### Con cobertura

```bash
pytest --cov=. --cov-report=html
```

## 📝 Logging

La aplicación registra eventos en la consola con diferentes niveles:

- **INFO**: Eventos importantes
- **ERROR**: Errores que requieren atención
- **DEBUG**: Información detallada (solo si DEBUG=True)

## 🔐 Seguridad

- Las credenciales se manejan con variables de entorno
- Se utilizan secrets en Kubernetes
- Validación de datos con Pydantic
- CORS configurado
- Health checks habilitados

## 🐛 Troubleshooting

### Error de conexión a PostgreSQL

Verificar que PostgreSQL está corriendo:
```bash
docker ps | grep postgres
```

### Error: "email already registered"

El email ya existe en la base de datos. Usar uno diferente.

### Puerto 8000 ya está en uso

```bash
# Cambiar puerto
uvicorn app:app --port 8001
```

## 📈 Monitoreo

### Health Check

```bash
curl http://localhost:8000/health
```

Respuesta esperada:
```json
{"status": "healthy", "service": "microservicio-api"}
```

## 🤝 Contribuir

1. Fork el repositorio
2. Crear una rama (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## ✉️ Contacto

Carlos Cabrera - [GitHub](https://github.com/carloscabreravas-dev)

## 🙏 Agradecimientos

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
- [Kubernetes](https://kubernetes.io/)
