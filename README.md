# PgVault

Auditor de seguridad y cumplimiento para PostgreSQL. Detecta vulnerabilidades de configuración, privilegios excesivos y datos sensibles no protegidos sobre una base de datos PostgreSQL read-only y genera un reporte listo para auditoría.

## 1. Requisitos

- Docker y Docker Compose instalados.
- Puertos 5432, 8000 y 5173 disponibles localmente.

## 2. Cómo correr el proyecto

Clonar el repositorio:

```bash
git clone <URL_DEL_REPO>
cd <CARPETA_DEL_REPO>
```

Levantar FintechDB (BD demo oficial):

```bash
cd fintechdb
docker compose up -d
```

Levantar PgVault (backend y frontend):

```bash
cd ../pgvault/deploy
docker compose up --build
```

Esperar unos segundos a que los servicios arranquen. Luego:

- Backend FastAPI: http://localhost:8000
- Frontend React: http://localhost:5173

## 3. Endpoints principales

- `GET /health`: status simple del backend.
- `GET /db-info`: nombre de la base y usuario con el que PgVault se conecta.
- `GET /scan`: resultados de configuración y PII en bruto por módulo.
- `GET /scan/flat`: lista unificada de hallazgos con score y resumen.
- `GET /report/pdf`: reporte descargable con resumen y detalle de hallazgos.

## 4. Flujo típico de uso

1. Levantar FintechDB y PgVault con Docker.
2. Abrir el frontend en http://localhost:5173.
3. Esperar a que se cargue el dashboard con el score y la tabla de hallazgos.
4. Filtrar por severidad o módulo según lo que se quiera revisar.
5. Descargar el reporte desde el botón "Descargar reporte" para adjuntarlo a auditorías o QA.

## 5. Tecnologías

- Backend: Python, FastAPI, psycopg.
- Frontend: React + Vite.
- Base de datos demo: PostgreSQL (FintechDB).
- Contenedores: Docker Compose.

## 6. Uso de IA en el desarrollo

El equipo utilizó herramientas de IA generativa para acelerar la escritura de código boilerplate, proponer estructuras de módulos y redactar secciones del documento de negocio. La lógica de detección, calibración de reglas y justificación técnica se trabajaron manualmente y se revisaron para asegurar que el equipo entiende y puede defender cada parte del producto en el Demo Day.
