# Cártula del Proyecto — PgVault

## Datos académicos

| Campo | Valor |
|---|---|
| Universidad | Universidad Anáhuac Querétaro |
| Facultad | Facultad de Ingeniería |
| Materia | SIS2404 — Bases de Datos Avanzadas |
| Profesor | Mtro. Heber Lazcano |
| Tipo de entrega | Proyecto Final |
| Fecha de entrega | 14/05/2026 |

## Datos del proyecto

| Campo | Valor |
|---|---|
| Nombre del proyecto | PgVault |
| Nombre del equipo | SecureBase |
| Slogan | Detecta riesgos en PostgreSQL antes de que llegue el auditor |

## Miembros del equipo

| Nombre completo | Matrícula | Rol principal | Email |
|---|---|---|---|
| Santiago Alejandro Donnadieu Bórquez | 00491062 | Integración con PostgreSQL y Docker (DevOps) | santiagodonnadieu@gmail.com |
| Edgar Martín Rodríguez Orduño | 00472384 | Auditor de reglas y checks de seguridad | edgarmartinrodriguez04@gmail.com |
| Daniela Sarahí Paniagua Sosa | 00479332 | Detección de datos sensibles (PII) | danielasarahi.paniaguasosa@gmail.com |
| Héctor Carrillo Hernández | 00439893 | Reportes, dashboards y cálculo de score | hcarrilloh@outlook.com |
| Ricardo Uziel Cortez Ruiz | 00517898 | Producto y negocio | uziel.cortez@anahuac.mx |

## Enlaces a entregables

| Recurso | Enlace |
|---|---|
| Repositorio Git | https://github.com/DonITpy/pgvault.git |
| Video demo (3-5 min) | https://youtu.be/RZfD3HHQVZs |
| Landing page | No aplica — producto académico sin despliegue público |
| Producto desplegado | No aplica — se levanta localmente con Docker Compose |

## Resumen ejecutivo

PgVault es una herramienta de auditoría de seguridad y cumplimiento para bases de datos PostgreSQL dirigida a fintechs mexicanas. El problema que resuelve es concreto: los equipos de TI en empresas reguladas por CNBV y LFPDPPP no tienen visibilidad continua sobre el estado de seguridad de su PostgreSQL. Dependen de auditorías manuales costosas que se hacen una o dos veces al año, quedan obsoletas en semanas y dejan ventanas de riesgo donde vulnerabilidades como SSL desactivado, passwords en texto plano o roles con privilegios excesivos pasan desapercibidas durante meses.

PgVault se conecta en modo solo lectura a cualquier instancia de PostgreSQL, ejecuta módulos de detección sobre catálogos internos del sistema y entrega los resultados en un dashboard web con score de seguridad, filtros por severidad y módulo, y un reporte PDF descargable listo para presentar a un auditor. No instala agentes, no modifica nada en la base de datos del cliente y levanta completamente con un solo comando de Docker Compose.

El usuario objetivo es el CISO o responsable de TI de una fintech mexicana de 20 a 200 empleados que necesita evidencia de cumplimiento para LFPDPPP, CNBV o PCI-DSS sin contratar una auditoría manual de 5,000 a 30,000 USD. Los competidores directos como Satori, Cyral, Immuta y BigID atienden el segmento enterprise con tickets de 50,000 a 200,000 USD anuales. PgVault entra desde 99 USD mensuales con foco exclusivo en PostgreSQL, soporte en español y mapeo regulatorio orientado al contexto mexicano.

## Cobertura sobre BD demo oficial

| Campo | Valor |
|---|---|
| BD demo utilizada | FintechDB |
| Total de problemas plantados | Pendiente de lista maestra del profesor |
| Problemas detectados correctamente | 33 hallazgos sobre FintechDB |
| Falsos positivos reportados | 0 tras filtrado de índices y objetos internos |
| Porcentaje de cobertura | Pendiente de lista maestra del profesor |

## Declaración de uso de IA

### Herramientas utilizadas

- [x] Claude (Anthropic)
- [ ] ChatGPT / GPT-4 / GPT-5
- [ ] GitHub Copilot
- [ ] Cursor / Windsurf / similar
- [ ] Gemini
- [ ] Otras

### Áreas donde se usó IA

- [x] Generación de código boilerplate, funciones, scripts
- [x] Debugging y resolución de errores
- [x] Generación de queries SQL complejas
- [x] Documentación técnica
- [x] Documento de negocio
- [x] Diseño de arquitectura
- [ ] Generación de datos sintéticos para pruebas
- [ ] Como parte del producto en runtime
- [ ] Otra

### Descripción detallada

Utilizamos Claude como asistente principal durante el desarrollo del proyecto. La IA ayudó a estructurar la arquitectura del backend, generar el código base de los módulos de detección de configuración y PII, depurar errores de conexión con psycopg y Docker, y redactar secciones del documento de arquitectura y negocio. La lógica de detección fue revisada y calibrada manualmente por el equipo sobre FintechDB para ajustar umbrales, reducir falsos positivos y verificar que cada hallazgo corresponde a una vulnerabilidad real. Las entrevistas con usuarios, el análisis competitivo y la estrategia de negocio fueron desarrollados por el equipo de forma independiente usando la IA solo como apoyo en la redacción final.

## Checklist de entregables

- [x] README claro con instrucciones de instalación y uso
- [x] docker-compose.yml funcional probado en máquina limpia
- [x] Documento de arquitectura (docs/arquitectura.md)
- [x] Documento de negocio (business/negocio.md)
- [x] Catálogo de reglas (docs/rules/catalogo.md)
- [x] Video demo de 3-5 minutos accesible (https://youtu.be/RZfD3HHQVZs)
- [x] Historial de Git con contribuciones de los 5 miembros
- [x] Esta cártula completa con todos los datos