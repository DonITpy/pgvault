# Documento de Arquitectura - PgVault

## 1. Visión general

PgVault es un servicio B2B que se conecta en modo read-only a una base de datos PostgreSQL y ejecuta tres piezas de lógica principales: auditoría de configuración, descubrimiento de datos sensibles (PII/PCI) y cálculo de un score global de seguridad. El resultado se expone vía API REST en un backend FastAPI, se visualiza en un dashboard web en React y se empaqueta en un reporte descargable para soporte de auditorías y cumplimiento regulatorio.

## 2. Diagrama de arquitectura (descrito)

Componentes principales:

- Cliente web (React): dashboard que consume `/scan/flat` y `/report/pdf`, muestra score, filtros por módulo y severidad, y tabla de hallazgos.
- Backend (FastAPI): expone los endpoints, orquesta la ejecución de los módulos de auditoría y normaliza los hallazgos a un formato común.
- Módulo de auditoría de configuración (`config_audit`): consulta catálogos como `pg_settings`, `pg_roles`, `pg_extension` y `pg_proc` para detectar misconfiguraciones y patrones de riesgo.
- Módulo de descubrimiento de PII (`pii_discovery`): identifica columnas sensibles por nombre y por contenido usando expresiones regulares y muestreo de datos.
- Servicio de scoring (`services/scoring.py`): aplica una regla simple de penalización por severidad para calcular un score de 0 a 100.
- Generador de reporte (`reports/html.py`): construye un HTML con resumen y detalle de hallazgos que se sirve como archivo descargable.
- PostgreSQL FintechDB: base de datos demo con vulnerabilidades plantadas.

## 3. Componentes principales

|-----------Componente--------------|---------------Módulo--------------|---------------------------Responsabilidad----------------------------|-------------Tecnología------------|
| API HTTP                          | `app/main.py`                     | Endpoints, orquestación, normalización de hallazgos                  | FastAPI, Python                   |
| Auditoría de configuración        | `modules/config_audit/service.py` | Consultar catálogos de Postgres y generar hallazgos de configuración | PostgreSQL, psycopg               |
| Descubrimiento de datos sensibles | `modules/pii_discovery/*`         | Detectar PII/PCI por nombre de columna y contenido                   | PostgreSQL, expresiones regulares |
| Scoring                           | `services/scoring.py`             | Calcular score global y resumen por severidad                        | Python                            |
| Reportes                          | `reports/html.py`                 | Construir HTML con resumen y tabla de hallazgos                      | Python, HTML                      |
| Dashboard                         | `frontend/src/App.tsx`            | Mostrar score, filtros y tabla, descargar reporte                    | React, Vite                       |

## 4. Decisiones técnicas y trade-offs

### Decisión 1: FastAPI como backend

- Alternativas consideradas: Flask, Node + Express.
- Por qué elegimos esta: FastAPI ofrece tipado fuerte, documentación automática y un modelo sencillo para construir APIs síncronas que consumen psycopg.
- Trade-off aceptado: dependemos de Python para todo el backend, lo que puede limitar rendimiento frente a una solución altamente concurrente, pero simplifica el desarrollo y la integración con librerías orientadas a Postgres y PII.

### Decisión 2: psycopg y SQL crudo

- Alternativas consideradas: SQLAlchemy, asyncpg.
- Por qué elegimos esta: psycopg permite control directo sobre consultas a catálogos como `pg_settings`, `pg_roles` y `pg_proc` sin costo de abstracción adicional.
- Trade-off aceptado: escribimos más SQL crudo y tenemos menos ayuda del ORM, pero ganamos claridad sobre qué se ejecuta realmente en la base.

### Decisión 3: Patrones de PII por regex y sampling

- Alternativas consideradas: solo por nombre de columna, integración con LLM para clasificación.
- Por qué elegimos esta: combinar nombre + contenido da mejor cobertura que solo nombre y se mantiene determinístico sin depender de servicios externos.
- Trade-off aceptado: la detección no es perfecta y requiere calibración manual de patrones y umbrales, pero es transparente y defendible en el QA Battle.

### Decisión 4: HTML simple para reporte descargable

- Alternativas consideradas: librerías de generación de PDF completas (WeasyPrint, ReportLab, Puppeteer).
- Por qué elegimos esta: para el MVP, un HTML con estilo básico servido como archivo descargable es suficiente para demostrar el flujo de reporte sin agregar complejidad.
- Trade-off aceptado: el archivo se presenta como “PDF” pero internamente es HTML; la siguiente iteración podría sustituir la implementación por un generador real de PDF manteniendo la misma interfaz.

## 5. Flujo principal de datos

1. PgVault se conecta a la base de datos FintechDB en modo read-only usando psycopg.
2. El endpoint `/scan/flat` ejecuta el módulo de configuración y el módulo de PII para recolectar hallazgos en bruto.
3. El backend normaliza la salida de cada módulo a un esquema común de hallazgo (módulo, regla, riesgo, confianza, tabla, columna, detalle).
4. El servicio de scoring calcula un score global y un resumen por severidad.
5. El frontend consume `/scan/flat`, muestra el score, el resumen y la tabla de hallazgos, y permite filtrar por severidad y módulo.
6. Cuando el usuario solicita el reporte, el backend vuelve a ejecutar los módulos, recalcula el score, genera un HTML con resumen y detalle y lo devuelve como archivo descargable.

## 6. Limitaciones reconocidas

- Operativas: el cálculo del score y la generación de reportes vuelven a ejecutar los módulos de auditoría cada vez; para bases muy grandes, una estrategia de snapshots y almacenamiento de resultados podría ser necesaria.
- De alcance: el mapeo regulatorio se maneja de forma conceptual en el documento de negocio y en la descripción de hallazgos, pero no se incluye en la primera versión del reporte.
- Técnicas: el reporte se sirve como HTML en lugar de un PDF generado por una librería especializada; esto se priorizó para simplificar el MVP.
- De negocio: el producto está específicamente orientado a PostgreSQL; organizaciones con múltiples motores de base de datos requerirían extensiones significativas para otras tecnologías.
