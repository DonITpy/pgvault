# Documento de Negocio — PgVault

## 1. Resumen ejecutivo

PgVault es una herramienta de auditoría de seguridad y cumplimiento para bases de datos PostgreSQL dirigida a fintechs mexicanas. Detecta automáticamente vulnerabilidades de configuración, privilegios excesivos y columnas con datos sensibles sin modificar nada en la base de datos del cliente, y entrega un reporte descargable con score de seguridad, evidencia técnica y recomendaciones de remediación.

El problema que resuelve es concreto: los equipos de TI en fintechs reguladas por CNBV y LFPDPPP no tienen visibilidad continua sobre el estado de seguridad de su PostgreSQL. Dependen de auditorías manuales costosas y puntuales que quedan obsoletas en semanas. Cuando llega una revisión regulatoria, el equipo trabaja bajo presión reconstruyendo evidencias a mano, lo que consume días de trabajo senior y puede derivar en multas o pérdida de confianza.

PgVault resuelve esto conectándose en modo solo lectura, ejecutando módulos de detección sobre catálogos internos de Postgres y entregando resultados en un dashboard web con filtros y un PDF profesional listo para mostrar a un auditor.

El mercado objetivo son fintechs mexicanas de 20 a 200 empleados con PostgreSQL en producción. Los competidores directos (Satori, Cyral, Immuta, BigID) atienden el segmento enterprise con tickets de 50,000 a 200,000 USD anuales. PgVault entra desde 99 USD mensuales con enfoque exclusivo en PostgreSQL, soporte en español y mapeo regulatorio orientado a LFPDPPP, CNBV y PCI-DSS.

El equipo de 5 personas construyó el MVP completo en 3 semanas: backend FastAPI, módulos de detección sobre catálogos de Postgres, dashboard React, generación de PDF con ReportLab y documentación técnica y de negocio completa. Para crecer necesitamos acceso a 5 fintechs piloto dispuestas a correr PgVault en sus ambientes de staging durante 30 días.

## 2. Problema - 2.1 Descripción del problema

Las fintech mexicanas que operan sobre bases de datos PostgreSQL manejan miles de registros con datos sensibles de clientes, pero carecen de una visibilidad continua sobre su postura de seguridad y cumplimiento. Hoy dependen de auditorías manuales que se realizan una o dos veces al año, en las que un consultor externo ejecuta queries sobre los catálogos del sistema, genera un PDF con hallazgos y desaparece. Entre una auditoría y otra, la base de datos cambia: se crean nuevos roles, se agregan columnas con datos personales y se modifican parámetros de configuración sin un control centralizado. Esto abre ventanas de riesgo donde un error de privilegios o una mala práctica de almacenamiento de datos puede pasar desapercibida durante meses.

Cuando llega una auditoría regulatoria de la CNBV o se presenta una investigación por potencial incumplimiento de la LFPDPPP, el equipo de TI se ve obligado a trabajar bajo presión reuniendo evidencias, ejecutando consultas a mano y reconstruyendo el estado de seguridad de la base de datos a partir de logs incompletos. Este proceso consume días de trabajo de perfiles senior, genera estrés organizacional y aun así puede dejar huecos que deriven en multas costosas o pérdida de confianza. No existe, en el contexto local, una herramienta accesible y enfocada en el mercado latinoamericano que entregue un inventario actualizado de riesgos de seguridad y datos sensibles en PostgreSQL sin necesidad de instalar agentes ni modificar la base de datos del cliente.

## 2. Problema - 2.2 User persona principal

|-----------Atributo------------|--------------------------------------------------------------------------------Valor--------------------------------------------------------------------------------|
| Nombre y rol                  | Carlos Méndez, CISO en fintech mexicana                                                                                                                             |
| Edad y experiencia            | 35 años, 10 años en seguridad de la información                                                                                                                     |
| Tamaño de empresa             | 40 empleados, 2 equipos de desarrollo y 1 equipo de operaciones                                                                                                     |
| Industria                     | Servicios financieros digitales (fintech regulada por CNBV)                                                                                                         |
| Día típico de trabajo         | Revisa incidentes de seguridad, coordina auditorías, atiende comités                                                                                                |
| Pain points principales       | Falta de visibilidad continua sobre privilegios y datos sensibles; dependencia de auditorías manuales y consultores externos; presión por cumplir LFPDPPP y PCI-DSS |
| Cómo resuelve hoy el problema | Contrata auditorías puntuales una o dos veces al año, mantiene hojas de cálculo con inventarios parciales y revisa consultas ad hoc con el equipo de base de datos  |
| Costo del problema            | Semanas de trabajo acumulado al año, riesgo de multas altas por incumplimiento y desgaste del equipo técnico en cada ciclo de auditoría                             |

## 2. Problema - 2.3 Frecuencia y severidad

| Dimensión | Estimación y razonamiento |
|---|---|
| Frecuencia | Las auditorías formales de seguridad en bases de datos ocurren 1 o 2 veces al año en la mayoría de fintechs mexicanas medianas. Entre auditorías, los cambios de configuración, roles y columnas ocurren continuamente sin revisión. Álvaro Campos (entrevistado) confirmó revisiones trimestrales por requerimiento de PCI-DSS, pero solo en proyectos con ese nivel de inversión. |
| Severidad | Alta. Un hallazgo no detectado como SSL desactivado, passwords en texto plano o roles con SUPERUSER innecesario puede resultar en una brecha de datos, multa de la CNBV o incumplimiento de PCI-DSS con consecuencias operativas y financieras graves. |
| Costo en tiempo | Preparar evidencia para una auditoría toma entre 2 horas y 2 semanas dependiendo del estado de documentación, según los tres entrevistados. Estimando un promedio de 8 horas por ciclo de auditoría y 2 ciclos al año, son 16 horas de trabajo senior por año solo en preparación de evidencia por instancia de base de datos. |
| Costo en dinero | Una auditoría manual de seguridad en base de datos con un consultor externo cuesta entre 5,000 y 30,000 USD por ejercicio según el brief del proyecto. PgVault reemplaza esa revisión inicial con un escaneo continuo desde 99 USD mensuales, representando un ahorro de hasta 29,000 USD al año en el escenario más conservador. |
| Costo en oportunidad | Cada día que pasa con una vulnerabilidad no detectada es un día de exposición regulatoria. Para una fintech regulada por CNBV, una multa por incumplimiento de LFPDPPP puede alcanzar hasta 320,000 días de salario mínimo según el artículo 64 de la ley. |

## 3. Investigación de usuarios - 3.1 Tabla de entrevistados

| Campo | Entrevistado 1 | Entrevistado 2 | Entrevistado 3 |
|-----------Campo------------|--------Entrevistado-1---------|---------------------Entrevistado-2----------------------|---------------------Entrevistado-3---------------------|
| Nombre                     | Ulises Millán                 | Álvaro Campos                                           | Eric González                                          |
| Perfil                     | Ingeniero en Machine Learning | Especialista en infraestructura y proyectos financieros | Cloud Architect con especialidad en seguridad y DevOps |
| Empresa                    | Beecker AI                    | Consultor independiente                                 | Beecker AI                                             |
| Experiencia con PostgreSQL | Sí, proyectos internos        | Sí, proyectos transaccionales en nube                   | Sí, segundo motor más usado en su carrera              |
| Fecha                      | 13/05/2026                    | 13/05/2026                                              | 13/05/2026                                             |
| Modalidad                  | Videollamada                  | Videollamada                                            | Videollamada                                           |

## 3. Investigación de usuarios - 3.2 Preguntas hechas

1. ¿Trabajas o has trabajado con bases de datos PostgreSQL en algún proyecto o empresa?
2. ¿Alguna vez has tenido que revisar o auditar quién tiene acceso a una base de datos, qué permisos tiene o cómo está configurada? ¿Cómo lo hiciste?
3. ¿Con qué frecuencia se revisan los permisos, configuraciones y datos sensibles en las bases de datos que conoces?
4. ¿Qué tan difícil o tardado es preparar evidencia de seguridad cuando alguien la pide (un auditor, un jefe, un cliente)?
5. ¿Sabes si en los proyectos o empresas que conoces se almacenan datos sensibles como correos, teléfonos, RFC, CURP o tarjetas directamente en la base de datos? ¿Hay algún control sobre eso?
6. ¿Conoces alguna herramienta que se use para detectar problemas de seguridad en bases de datos? ¿Cuál y qué tan útil fue?
7. Si existiera una herramienta que se conectara a tu PostgreSQL en modo solo lectura, detectara automáticamente problemas de configuración y columnas con datos sensibles, y generara un reporte listo para mostrar, ¿la usarías? ¿Qué te generaría desconfianza de ella?
8. ¿Qué tan importante sería para ti que el reporte hiciera referencia a regulaciones mexicanas como LFPDPPP o estándares como PCI-DSS?
9. ¿Cuánto estarías dispuesto a pagar mensualmente por algo así si funciona bien y no requiere instalar nada en el servidor?
10. ¿Qué le faltaría a una herramienta así para que la recomendaras a alguien más?

## 3. Investigación de usuarios - 3.3 Resumen por entrevistado

### Entrevistado 1 — Ulises Millán, Ingeniero ML en Beecker AI

Trabaja con Postgres para proyectos internos. La gestión de permisos y configuración recae en perfiles de arquitectura y cloud, no en desarrolladores. Desconoce herramientas específicas para auditar bases de datos, aunque menciona SonarCube como referente cercano, que su empresa ya usa en prueba gratuita pero limitada a 50,000 líneas de código. Usaría la herramienta a nivel de equipo, no individual. Su principal fuente de desconfianza es que los datos puedan usarse para entrenar modelos de IA o que el proveedor no sea transparente sobre qué hace con la información. Prefiere modelo de pago mensual porque traslada la responsabilidad de mantenimiento al proveedor. Para recomendar la herramienta necesitaría ver historial de uso en otras empresas, comunidad activa y documentación clara.

### Entrevistado 2 — Álvaro Campos, Especialista en infraestructura y proyectos financieros

Tiene experiencia directa con auditorías de seguridad en proyectos financieros regulados por PCI-DSS. Las revisiones de permisos y configuración se hacen cada 3 meses por requerimiento de certificación y el proceso es completamente manual: capturas de pantalla, revisión de matrices de acceso y validación contra la base de datos en vivo. Preparar evidencia tarda entre 2 y 3 horas mínimo por instancia. Conoce Tenable como herramienta de escaneo de vulnerabilidades pero señala que solo valida configuraciones, no datos sensibles en tablas. Usaría PgVault si cumple con estándares de seguridad y ofrece reportes diferenciados: uno ejecutivo para directivos y uno técnico detallado para auditores. Le interesa la modularidad por certificación (solo PCI, solo ISO 27001) porque reduce el costo y el tiempo de escaneo. Su principal preocupación es la confiabilidad del proveedor y que la herramienta tenga mantenimiento activo ante vulnerabilidades.

### Entrevistado 3 — Eric González, Cloud Architect en Beecker AI

Tiene 20 años de experiencia en TI con especialidad en seguridad, DevOps e infraestructura en nube. Trabaja con Postgres como segundo motor más usado. Las revisiones de acceso se hacen mensualmente usando access reviews, herramientas CDR de nube y queries manuales sobre roles y grants. Preparar evidencia de auditoría puede tomar desde una semana si no tienes la arquitectura documentada. Conoce y usa Microsoft Defender y Purview para detectar problemas de seguridad y datos sensibles. Usaría PgVault sobre una réplica read-only y valora que sea agnóstico (funcione en cualquier nube o on-premise). Considera que el reporte debe incluir pasos de remediación, no solo detección, porque los equipos no siempre tienen expertos en seguridad disponibles. Sugiere precio en torno a 30-40 USD mensuales para una versión intermedia con tier gratuito limitado y modelo SaaS por suscripción.

## 3. Investigación de usuarios - 3.4 Aprendizajes principales

*Aprendizaje 1: La gestión de seguridad en bases de datos es manual y costosa en tiempo.*
Los tres entrevistados confirmaron que las revisiones de permisos, configuraciones y datos sensibles se hacen a mano, ya sea con queries directas, capturas de pantalla o scripts propios. Álvaro Campos señaló que preparar evidencia para un auditor toma entre 2 y 3 horas por instancia y que los procesos de revalidación son trimestrales por requerimiento de certificación. Eric González indicó que si no tienes la arquitectura documentada desde el inicio, reunir evidencia puede tomar hasta dos semanas.

*Aprendizaje 2: Las herramientas existentes son costosas, genéricas o limitadas.*
Ulises Millán mencionó SonarCube como referente pero señaló que el tier gratuito está limitado y orientado a código, no a bases de datos. Álvaro Campos conoce Tenable pero aclaró que solo valida configuraciones del servidor, no detecta datos sensibles en tablas. Eric González usa Microsoft Defender y Purview, que son herramientas de nube propietarias que no aplican para entornos on-premise o multi-nube de forma agnóstica.

*Aprendizaje 3: La desconfianza principal es sobre qué hace la herramienta con los datos.*
Los tres entrevistados expresaron preocupación por la transparencia del proveedor. Ulises Millán teme que los datos se usen para entrenar modelos de IA. Álvaro Campos señaló que muchas empresas generan sus propios scripts por desconfianza a herramientas free o de fabricantes desconocidos. Eric González insistió en que la herramienta debe operar en instancia privada sin enviar datos al exterior. Este punto valida el enfoque self-hosted de PgVault como diferenciador clave.

*Aprendizaje 4: El mapeo regulatorio en el reporte tiene alto valor percibido.*
Álvaro Campos y Eric González coincidieron en que poder seleccionar una certificación específica (PCI-DSS, ISO 27001, HIPAA) y obtener un reporte alineado a esos controles reduce significativamente el esfuerzo de auditoría. Álvaro lo describió como pasar de revisar 20 puntos genéricos a revisar solo los 5 o 10 que aplican a su certificación. Eric mencionó que incluso herramientas enterprise como Purview ya ofrecen esto y que sería el diferenciador principal de PgVault frente a soluciones más simples.

*Aprendizaje 5: El modelo de precios ideal es SaaS mensual con tier gratuito limitado.*
Los tres entrevistados coincidieron en que el modelo de pago mensual es preferible porque traslada la responsabilidad de mantenimiento al proveedor. Álvaro sugirió precios en torno a 100-150 USD por 3-5 hosts para un escaneo de PCI. Eric mencionó 30-40 USD para una versión intermedia como referencia de mercado. Ulises señaló que el tier gratuito es indispensable para que las empresas prueben antes de comprometerse con un pago.

## 4. Solución

Carlos, el CISO de una fintech mexicana de 40 personas, lleva semanas posponiendo la revisión de seguridad de su base de datos PostgreSQL porque sabe que hacerlo manualmente le tomará días que no tiene. Recibe PgVault de un colega, sigue el README, corre dos comandos de Docker y en menos de 5 minutos tiene el producto funcionando conectado a su instancia de staging.

Abre el dashboard en el navegador y ve un score de 52 sobre 100. Debajo, una tabla con 33 hallazgos ordenados por severidad. Filtra por "Alto" y ve que SSL está desactivado, que hay dos roles con SUPERUSER que no deberían tenerlo y que una función SECURITY DEFINER tiene configuración insegura. Filtra por "PII" y descubre que hay columnas con tarjetas y contraseñas en texto plano que su equipo nunca había inventariado.

Hace clic en "Descargar reporte", obtiene un PDF con el score, el resumen ejecutivo y el detalle de cada hallazgo con la query de remediación incluida. Lo adjunta al correo que le pidió el auditor externo esa mañana. Total de tiempo invertido: 15 minutos.

A la semana siguiente repite el proceso después de que su equipo aplicó algunas remediaciones. El score subió a 71. Tiene evidencia de mejora continua documentada y lista para presentar en la próxima revisión regulatoria.

### 4.1 Funcionalidades core

| Feature | Beneficio para el usuario |
|---|---|
| Conexión read-only sin agentes | Se instala sin pasar por comité de cambios ni modificar producción |
| Auditoría de configuración (8 checks) | Detecta SSL, logging, extensiones peligrosas, SUPERUSER y funciones inseguras en minutos |
| Descubrimiento de PII por nombre | Inventario inmediato de columnas con datos personales sin revisar tabla por tabla a mano |
| Descubrimiento de PII por contenido | Confirma qué columnas realmente tienen datos sensibles aunque el nombre no lo indique |
| Score de seguridad 0-100 | Una sola cifra para comunicar el estado de seguridad a directivos sin tecnicismos |
| Dashboard con filtros | Permite priorizar por severidad o módulo para atacar primero lo más crítico |
| Reporte PDF descargable | Evidencia lista para entregar a auditores, directivos o reguladores en un clic |
| Docker Compose | Levanta todo el producto con un solo comando sin configuración adicional |

## 5. Análisis competitivo - 5.1 Tabla comparativa

| Característica | Satori | Cyral | Immuta | BigID | PgVault |
|---|---|---|---|---|---|
| Enfoque principal | Seguridad y acceso a datos | Data security y gobernanza de acceso | Gobernanza y control de acceso a datos | Descubrimiento y gobernanza de datos | Auditoría de seguridad y cumplimiento para PostgreSQL |
| Segmento objetivo | Enterprise | Enterprise | Enterprise | Enterprise | Fintechs mexicanas y equipos medianos con PostgreSQL |
| Soporte en español | Limitado | Limitado | Limitado | Limitado | Sí |
| Integración regulatoria local | No específica a México | No específica a México | No específica a México | No específica a México | Sí, orientada a LFPDPPP, CNBV y PCI-DSS |
| Read-only sobre PostgreSQL | Parcial según despliegue | Parcial según despliegue | Parcial según despliegue | Parcial según despliegue | Sí |
| Ticket esperado | Alto (50K-200K USD/año) | Alto | Alto | Alto | Medio (99-999 USD/mes) |
| Foco en PostgreSQL | No exclusivo | No exclusivo | No exclusivo | No exclusivo | Sí |
| On-premise sin agentes | No | No | No | No | Sí |

## 5. Análisis competitivo - 5.2 Análisis honesto

Satori, Cyral y BigID tienen mayor madurez comercial, más integraciones y capacidades enterprise que un MVP académico no puede igualar. Sin embargo, su enfoque es más amplio y su propuesta suele estar pensada para organizaciones con mayor presupuesto, procesos más pesados de compra y necesidades multibase o multinube.

PgVault compite desde otro ángulo: una herramienta más simple de adoptar, enfocada específicamente en PostgreSQL, con discurso de cumplimiento aterrizado al contexto mexicano y una experiencia read-only que reduce fricción técnica y política de instalación. Su debilidad actual frente a esos competidores está en la falta de features avanzadas de plataforma, automatización de remediación y madurez operativa.

## 5. Análisis competitivo - 5.3 Espacio en blanco

Nuestro nicho es el de fintechs mexicanas de 20 a 200 empleados que usan PostgreSQL, manejan datos sensibles y necesitan evidencia rápida de seguridad y cumplimiento sin comprar una plataforma enterprise internacional.

Los competidores no atienden bien este nicho porque suelen vender soluciones más amplias, más costosas y menos adaptadas al lenguaje regulatorio local.

Nosotros podemos servirlo bien porque ofrecemos una herramienta centrada en PostgreSQL, con instalación no invasiva, menor complejidad operativa y reportes orientados a regulaciones relevantes para el mercado mexicano.

## 6. Modelo de negocio - 6.1 Tipo de modelo de revenue

Suscripción mensual por instancia de base de datos monitoreada.

## 6. Modelo de negocio - 6.2 Tiers de pricing

|----Tier----|----Precio---|------------------Comprador objetivo------------------|---------------------------------------------Qué incluye---------------------------------------------|
| Starter    | 99 USD/mes  | Startup o fintech pequeña con 1 PostgreSQL principal | 1 instancia, dashboard, score y reporte ejecutivo básico                                            |
| Growth     | 299 USD/mes | Fintech mediana con varias bases o ambientes         | Hasta 5 instancias, reportes técnicos, priorización de hallazgos y exportación                      |
| Enterprise | 999 USD/mes | Institución con requerimientos fuertes de compliance | Instancias ilimitadas, soporte prioritario, plantillas regulatorias avanzadas y despliegue dedicado |

## 6. Modelo de negocio - 6.3 Justificación del precio

El precio se plantea por debajo de plataformas enterprise internacionales y muy por debajo del costo de una auditoría manual especializada, que puede costar miles de dólares por ejercicio. La lógica no es competir por ser "lo más barato", sino ofrecer una opción especializada, enfocada y más accesible para equipos que hoy no pueden justificar una suite global de gobierno de datos. Los tres entrevistados validaron que un rango de 30 a 150 USD mensuales es razonable dependiendo del número de instancias y el nivel de cumplimiento requerido.

## 7. Go-to-market - 7.1 Primeros 10 clientes

### Paso 1
Contactar fintechs mexicanas dentro de la red cercana del equipo, profesores, egresados y contactos profesionales relacionados con TI, seguridad o compliance.

### Paso 2
Ofrecer 5 pilotos gratuitos de 30 días a empresas con PostgreSQL y necesidad clara de revisión de seguridad o cumplimiento.

### Paso 3
Convertir esos pilotos en casos de uso con métricas concretas: tiempo ahorrado, hallazgos detectados y evidencia generada.

### Paso 4
Usar esos primeros casos para acercarse a despachos de compliance, consultores de seguridad y comunidades de tecnología financiera en México.

### Paso 5
Cerrar los primeros 10 clientes combinando venta directa, referidos y presencia en eventos o comunidades fintech.

*Timeline estimado:* 6 a 9 meses.

## 7. Go-to-market - 7.2 Estrategia de growth después de los 10

- Canal 1: alianzas con consultores y despachos de compliance.
- Canal 2: contenido técnico dirigido a equipos de TI y seguridad que usan PostgreSQL.
- Canal 3: referidos entre fintechs y verticales reguladas similares.

## 8. Tamaño de mercado — 8.1 TAM / SAM / SOM

### TAM — Mercado total disponible

El mercado global de herramientas de seguridad para bases de datos se estima en aproximadamente 1,500 millones de USD anuales para 2025, con una tasa de crecimiento anual del 12% impulsada por regulaciones de protección de datos y adopción de PostgreSQL como motor principal en startups y empresas medianas. PostgreSQL es el motor de base de datos más popular entre desarrolladores según el Stack Overflow Developer Survey 2024, con más del 49% de adopción global.

### SAM — Mercado disponible y direccionable

Enfocándonos en América Latina, el mercado de fintechs reguladas con uso de PostgreSQL representa un segmento más acotado. México cuenta con más de 650 fintechs activas registradas ante la CNBV según datos de Finnovista 2024, de las cuales aproximadamente el 60% usa PostgreSQL como motor principal o secundario. Sumando Colombia, Brasil y otros mercados latinoamericanos con regulaciones similares, el SAM estimado es de entre 80 y 120 millones de USD anuales para herramientas especializadas en auditoría y cumplimiento de bases de datos en este segmento.

### SOM — Mercado realista a capturar

En un horizonte de 12 a 18 meses, PgVault puede apuntar razonablemente a fintechs mexicanas de 20 a 200 empleados que usan PostgreSQL y necesitan evidencia de cumplimiento para CNBV o LFPDPPP. Estimando un universo inicial de 200 empresas objetivo en México, con un ticket promedio de 150 USD mensuales (tier Growth) y una tasa de conversión conservadora del 5% en el primer año, el SOM inicial sería de aproximadamente 180,000 USD anuales. Este número es alcanzable con una estrategia de ventas directa y pilotos gratuitos como los descritos en el plan de go-to-market.

## 8. Tamaño de mercado - 8.2 Tendencias relevantes

**Tendencia 1: Crecimiento acelerado de fintechs reguladas en México**
El ecosistema fintech mexicano creció más del 20% anual entre 2021 y 2024 según Finnovista. La Ley Fintech de 2018 y las disposiciones de la CNBV han aumentado la presión regulatoria sobre empresas que manejan datos financieros y personales, creando una necesidad creciente de herramientas de cumplimiento accesibles para equipos medianos.

**Tendencia 2: PostgreSQL como motor dominante en startups y fintechs**
PostgreSQL superó el 49% de adopción entre desarrolladores en el Stack Overflow Developer Survey 2024, posicionándose como el motor más popular por cuarto año consecutivo. La mayoría de fintechs mexicanas nuevas elige PostgreSQL por su costo cero de licencia y su robustez, lo que amplía el mercado direccionable de PgVault año con año.

**Tendencia 3: Endurecimiento regulatorio en protección de datos personales**
La LFPDPPP y sus reglamentos están siendo aplicados con mayor rigor desde 2022. El INAI ha incrementado el número de procedimientos de verificación y las multas por incumplimiento. Paralelamente, PCI-DSS v4.0 entró en vigencia en 2024 con requisitos más estrictos sobre monitoreo continuo y evidencia de controles, lo que hace más urgente contar con herramientas que generen evidencia automatizada y actualizada.

## 9. Diferenciador defendible - 9.1 Diferenciador principal

Nuestro diferenciador es la combinación de foco exclusivo en PostgreSQL, despliegue read-only sin fricción y lenguaje de cumplimiento alineado con el contexto regulatorio mexicano.

Es defendible en el tiempo porque no depende únicamente del precio ni de una feature aislada, sino de una especialización vertical y regional que los competidores globales no priorizan de forma nativa. Las entrevistas confirmaron que el enfoque self-hosted y la transparencia sobre el manejo de datos son los factores de confianza más importantes para empresas del sector financiero mexicano.

## 9. Diferenciador defendible - 9.2 Ejemplos concretos

- Hallazgos pensados para PostgreSQL en vez de un enfoque genérico de data governance.
- Reportes orientados a conversaciones con equipos de seguridad y compliance en México.
- Adopción más simple para equipos medianos que no pueden pasar por compras enterprise complejas.
- Operación self-hosted que garantiza que los datos del cliente nunca salen de su infraestructura.

## 10. Por qué nuestro equipo

Nuestro equipo combina perfiles con experiencia en backend, seguridad, frontend y producto, lo que permitió construir un MVP funcional end-to-end en tres semanas. Además de implementar detectores sobre catálogos de Postgres y un dashboard operativo, trabajamos un documento de negocio enfocado en el contexto regulatorio mexicano y en las necesidades reales de fintechs con PostgreSQL en producción. Las tres entrevistas realizadas con profesionales activos en el sector tecnológico y financiero validaron tanto el problema como el enfoque de solución.

## 11. Roadmap técnico post-MVP

*Próximos 3 meses:*
- Añadir mapeo regulatorio directo en cada hallazgo (LFPDPPP, CNBV, PCI-DSS).
- Implementar almacenamiento de snapshots históricos para comparar runs.
- Mejorar cobertura de checks de configuración basada en CIS Benchmarks para PostgreSQL.

*Próximos 6 meses:*
- Soportar múltiples instancias de PostgreSQL por cliente con vista consolidada de riesgos.
- Incorporar pasos de remediación por hallazgo, validado como necesidad clave en entrevistas.
- Afinar heurísticas de PII para reducir falsos positivos usando métricas de uso real.

*Visión a 1 año:*
- Convertir PgVault en una plataforma de monitoreo continuo de seguridad para PostgreSQL en fintechs LATAM, con integraciones hacia herramientas de ticketing y flujos de remediación automatizada.

## 12. Preguntas de QA Battle que esperamos

- ¿Cómo justifican el tamaño de muestra y los patrones usados para detectar PII por contenido?
- ¿Qué pasaría con el performance de PgVault si la base del cliente tiene millones de filas en varias tablas?
- ¿Cómo evitarían falsos positivos masivos cuando se agregan nuevas reglas de detección?
- Si un cliente ya usa una herramienta enterprise como BigID, ¿en qué escenarios tendría sentido además usar PgVault?
- ¿Qué cambios harían primero si quisieran soportar un segundo motor de base de datos además de PostgreSQL?

## 13. Mapeo regulatorio explícito

PgVault está diseñado para generar evidencia directamente utilizable en auditorías regulatorias. La siguiente tabla muestra cómo cada módulo del producto soporta los controles específicos de las regulaciones más relevantes para fintechs mexicanas.

| Regulación | Artículo o control | Qué detecta PgVault que soporta evidencia |
|---|---|---|
| LFPDPPP | Art. 3 — Datos personales | Columnas con RFC, CURP, nombre, email, teléfono, dirección, fecha de nacimiento detectadas por nombre y contenido |
| LFPDPPP | Art. 19 — Medidas de seguridad | Passwords en texto plano, SSL desactivado, password_encryption débil, roles con privilegios excesivos |
| LFPDPPP | Art. 20 — Niveles de seguridad | Logging insuficiente (log_connections, log_statement, logging_collector), ausencia de trazabilidad |
| PCI-DSS | Req. 3 — Protección de datos de tarjeta | Columnas con PAN, CVV detectadas por nombre y contenido; números de tarjeta en texto plano |
| PCI-DSS | Req. 4 — Cifrado en tránsito | SSL desactivado en el servidor |
| PCI-DSS | Req. 7 — Acceso con privilegio mínimo | Roles con SUPERUSER innecesario, privilegios excesivos |
| PCI-DSS | Req. 8 — Autenticación fuerte | password_encryption débil, métodos inseguros en pg_hba (trust, password en claro) |
| PCI-DSS | Req. 10 — Logging y monitoreo | log_connections desactivado, log_statement en none, logging_collector apagado |
| CNBV Circular Única | Disposiciones de seguridad de la información | Configuración insegura del servidor, extensiones peligrosas, funciones SECURITY DEFINER sin control |

PgVault no reemplaza una auditoría regulatoria formal ni certifica el cumplimiento de ninguna regulación. Genera el inventario de evidencia técnica que un equipo de TI o un auditor externo puede usar para demostrar controles implementados o identificar brechas que requieren remediación antes de una revisión regulatoria.

## 14. Roadmap a 12 meses

| Trimestre | Producto | Negocio | Operativo |
|---|---|---|---|
| Q1 (meses 1-3) | Mapeo regulatorio directo en cada hallazgo (LFPDPPP, PCI-DSS por artículo). Snapshots históricos para comparar runs. Más checks de configuración basados en CIS Benchmarks. | Cerrar 5 pilotos gratuitos de 30 días con fintechs mexicanas. Documentar casos de uso con métricas reales. | Configurar infraestructura SaaS básica. Definir proceso de soporte para pilotos. |
| Q2 (meses 4-6) | Soporte para múltiples instancias de PostgreSQL por cliente. Pasos de remediación detallados por hallazgo. Reducción de falsos positivos con retroalimentación de pilotos. | Convertir al menos 3 de los 5 pilotos en clientes de pago. Iniciar alianzas con 2 consultores de compliance. | Contratar primer perfil de ventas o customer success part-time. |
| Q3 (meses 7-9) | Dashboard histórico con comparación de runs y tendencias de score. Exportación de evidencia mapeada por regulación seleccionable. | Llegar a 10 clientes de pago. Presentar en un evento fintech mexicano. | Formalizar estructura legal y fiscal de la empresa. |
| Q4 (meses 10-12) | Soporte experimental para un segundo motor de base de datos (MySQL o MariaDB). Integración con herramientas de ticketing (Jira, Linear) para flujo de remediación. | Iniciar expansión a Colombia y Brasil con adaptaciones regulatorias locales. | Evaluar ronda de inversión seed con métricas de los primeros 12 meses. |

## 15. Ask

Si esto fuera un pitch real ante inversionistas o mentores, esto es lo que necesitaríamos para llegar al siguiente nivel:

**Primero: 5 clientes piloto**
Buscamos fintechs mexicanas reguladas por CNBV o con requerimientos PCI-DSS que estén dispuestas a correr PgVault en su ambiente de staging durante 30 días sin costo. A cambio les entregamos el reporte completo y retroalimentación técnica detallada. Esto nos da datos reales para calibrar el producto y los primeros casos de uso para vender.

**Segundo: Mentores con acceso al sector fintech y compliance**
Necesitamos contactos que nos puedan conectar con CISOs, Compliance Officers o responsables de TI en fintechs mexicanas. No buscamos ventas inmediatas, buscamos conversaciones para validar el producto en contextos reales antes de escalar.

**Tercero: Validación del modelo de precios**
¿Es 99 USD mensuales el precio correcto para el tier Starter en el mercado mexicano? ¿O el modelo por instancia tiene más tracción que el modelo por empresa? Buscamos mentores con experiencia en pricing de SaaS B2B en LATAM que nos ayuden a calibrar esto con datos reales del mercado.