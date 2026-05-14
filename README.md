# PgVault

PgVault es un auditor de seguridad y cumplimiento para PostgreSQL. Se conecta en modo read-only a una base de datos PostgreSQL, detecta vulnerabilidades de configuración, privilegios excesivos y datos sensibles no protegidos, y genera un dashboard con score de seguridad y un reporte descargable.

## 1. Requisitos

Antes de ejecutar el proyecto, se necesita lo siguiente:

- Docker instalado.
- Docker Compose instalado.
- Puertos 5432, 8000 y 5173 disponibles localmente.
- Git instalado para clonar el repositorio. 

## 2. Estructura general del proyecto

La estructura esperada del repositorio es la siguiente:

```bash
/
├── fintechdb/              # Base de datos demo oficial
├── pgvault/
│   ├── backend/            # API y lógica de análisis
│   ├── frontend/           # Dashboard web
│   ├── docs/               # Arquitectura y documentación técnica
│   ├── business/           # Documento de negocio
│   └── deploy/             # Docker Compose del producto
└── README.md
```

Si la estructura del repositorio cambia, también deben actualizarse las rutas descritas en este documento. 

## 3. Cómo correr el proyecto

### 3.1 Clonar el repositorio

```bash
git clone <URL_DEL_REPO>
cd <CARPETA_DEL_REPO>
```

### 3.2 Levantar FintechDB

La base de datos demo oficial debe iniciarse primero.

```bash
cd fintechdb
docker compose up -d
```

### 3.3 Levantar PgVault

Una vez arriba la base de datos demo, se debe iniciar el producto.

```bash
cd ../pgvault/deploy
docker compose up --build -d
```

Esperar unos segundos a que los contenedores terminen de iniciar correctamente.

## 4. Verificación básica de funcionamiento

Una vez levantados los servicios, se puede validar el backend con los siguientes endpoints:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/db-info
curl http://localhost:8000/scan
curl http://localhost:8000/scan/flat
```

Resultados esperados:

- `GET /health` devuelve el estado básico del backend.
- `GET /db-info` devuelve el nombre de la base y el usuario conectado.
- `GET /scan` devuelve los hallazgos separados por módulo.
- `GET /scan/flat` devuelve una lista unificada de hallazgos con score y resumen. 

Luego se puede abrir el frontend en:

- Backend FastAPI: [http://localhost:8000](http://localhost:8000)
- Frontend React: [http://localhost:5173](http://localhost:5173)

## 5. Endpoints principales

- `GET /health`: estado simple del backend.
- `GET /db-info`: nombre de la base de datos y usuario con el que PgVault se conecta.
- `GET /scan`: resultados de configuración y PII en bruto por módulo.
- `GET /scan/flat`: lista unificada de hallazgos con score y resumen.
- `GET /report/pdf`: reporte descargable con resumen y detalle de hallazgos.

## 6. Flujo típico de uso

1. Levantar FintechDB con Docker Compose.
2. Levantar PgVault con Docker Compose.
3. Abrir el frontend en [http://localhost:5173](http://localhost:5173).
4. Esperar a que cargue el dashboard con el score general y la tabla de hallazgos.
5. Filtrar por severidad o módulo según el tipo de revisión deseada.
6. Descargar el reporte desde el botón **Descargar reporte** para usarlo como evidencia técnica o apoyo en auditorías.

## 7. Detener o reiniciar el proyecto

Para detener los servicios:

### Detener PgVault

```bash
cd pgvault/deploy
docker compose down
```

### Detener FintechDB

```bash
cd fintechdb
docker compose down
```

Si se hicieron cambios al código y se requiere reconstruir imágenes:

```bash
cd pgvault/deploy
docker compose up --build -d
```

Para revisar logs del backend:

```bash
docker compose logs -f backend
```

Para revisar logs del frontend:

```bash
docker compose logs -f frontend
```

## 8. Tecnologías utilizadas

- Backend: Python, FastAPI, psycopg.
- Frontend: React + Vite.
- Base de datos demo: PostgreSQL (FintechDB).
- Contenedores: Docker Compose.

## 9. Problemas comunes

### 9.1 El frontend no carga

Verificar que el contenedor del frontend esté corriendo:

```bash
docker ps
```

También revisar que el puerto 5173 no esté ocupado por otra aplicación.

### 9.2 El backend no responde

Verificar que el contenedor del backend esté arriba y revisar logs:

```bash
cd pgvault/deploy
docker compose logs -f backend
```

### 9.3 El backend no se conecta a PostgreSQL

Verificar primero que FintechDB esté levantada correctamente:

```bash
cd fintechdb
docker compose ps
```

Si la base no está arriba, volver a iniciarla:

```bash
docker compose up -d
```

### 9.4 Los cambios no se reflejan

Reconstruir servicios con:

```bash
cd pgvault/deploy
docker compose up --build -d
```

## 10. Consideraciones sobre configuración

Este proyecto está diseñado para correr con la configuración incluida en Docker Compose. Si en una máquina distinta se requieren cambios de puertos, variables o credenciales, deberán ajustarse los archivos de despliegue correspondientes antes de ejecutar el sistema. 

## 11. Sobre el reporte descargable

El endpoint `GET /report/pdf` entrega un archivo descargable con el resumen y detalle de hallazgos detectados por PgVault. En el contexto del MVP, este reporte forma parte del flujo de evidencia del producto y permite demostrar la exportación de resultados desde la interfaz.

## 12. Uso de IA en el desarrollo

El equipo utilizó herramientas de IA generativa para acelerar la escritura de código boilerplate, proponer estructuras de módulos y redactar secciones del documento de negocio. La lógica de detección, calibración de reglas y justificación técnica se trabajaron manualmente y se revisaron para asegurar que el equipo entiende y puede defender cada parte del producto en el Demo Day.

## 13. Video Demo
https://youtu.be/RZfD3HHQVZs