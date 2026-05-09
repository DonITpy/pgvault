# Documento de Negocio

## 2. Problema - 2.1 Descripción del problema

Las fintech mexicanas que operan sobre bases de datos PostgreSQL manejan miles de registros con datos sensibles de clientes, pero carecen de una visibilidad continua sobre su postura de seguridad y cumplimiento. Hoy dependen de auditorías manuales que se realizan una o dos veces al año, en las que un consultor externo ejecuta queries sobre los catálogos del sistema, genera un PDF con hallazgos y desaparece. Entre una auditoría y otra, la base de datos cambia: se crean nuevos roles, se agregan columnas con datos personales y se modifican parámetros de configuración sin un control centralizado. Esto abre ventanas de riesgo donde un error de privilegios o una mala práctica de almacenamiento de datos puede pasar desapercibida durante meses.

Cuando llega una auditoría regulatoria de la CNBV o se presenta una investigación por potencial incumplimiento de la LFPDPPP, el equipo de TI se ve obligado a trabajar bajo presión reuniendo evidencias, ejecutando consultas a mano y reconstruyendo el estado de seguridad de la base de datos a partir de logs incompletos. Este proceso consume días de trabajo de perfiles senior, genera estrés organizacional y aun así puede dejar huecos que deriven en multas costosas o pérdida de confianza. No existe, en el contexto local, una herramienta accesible y enfocada en el mercado latinoamericano que entregue un inventario actualizado de riesgos de seguridad y datos sensibles en PostgreSQL sin necesidad de instalar agentes ni modificar la base de datos del cliente.

## 2. Problema - 2.2 User persona principal

| Atributo                  | Valor                                                                 |
|---------------------------|-----------------------------------------------------------------------|
| Nombre y rol              | Carlos Méndez, CISO en fintech mexicana                              |
| Edad y experiencia        | 35 años, 10 años en seguridad de la información                      |
| Tamaño de empresa         | 40 empleados, 2 equipos de desarrollo y 1 equipo de operaciones      |
| Industria                 | Servicios financieros digitales (fintech regulada por CNBV)          |
| Día típico de trabajo     | Revisa incidentes de seguridad, coordina auditorías, atiende comités |
| Pain points principales   | Falta de visibilidad continua sobre privilegios y datos sensibles; dependencia de auditorías manuales y consultores externos; presión por cumplir LFPDPPP y PCI-DSS |
| Cómo resuelve hoy el problema | Contrata auditorías puntuales una o dos veces al año, mantiene hojas de cálculo con inventarios parciales y revisa consultas ad hoc con el equipo de base de datos |
| Costo del problema        | Semanas de trabajo acumulado al año, riesgo de multas altas por incumplimiento y desgaste del equipo técnico en cada ciclo de auditoría             |

## 3. Investigación de usuarios - 3.2 Preguntas hechas

1. ¿Cómo auditas hoy los permisos, configuraciones y datos sensibles de tus bases PostgreSQL?
2. ¿Cada cuánto tiempo haces revisiones formales de seguridad o cumplimiento?
3. ¿Qué tipo de hallazgos te preocupa más: privilegios excesivos, configuraciones inseguras o datos sensibles expuestos?
4. ¿Qué tan costoso es para tu equipo preparar evidencia para una auditoría o revisión regulatoria?
5. ¿Qué herramientas usas hoy para detectar riesgos en PostgreSQL?
6. ¿Qué limitaciones tienen esas herramientas en el contexto de una fintech mexicana?
7. ¿Qué tan importante sería para ti contar con reportes listos para LFPDPPP, CNBV y PCI-DSS?
8. ¿Aceptarías una herramienta read-only que no instala agentes ni modifica tu base de datos?

## 3. Investigación de usuarios - 3.3 Estado actual de entrevistas

Las entrevistas y validaciones con usuarios objetivo aún se encuentran pendientes de realización. Actualmente se cuenta con una lista inicial de preguntas enfocadas en entender procesos de auditoría, cumplimiento y monitoreo de seguridad en entornos PostgreSQL dentro de fintechs mexicanas.

## 3. Investigación de usuarios - 3.4 Aprendizajes principales

Por completar una vez realizadas las entrevistas y recopilados los resultados.

## 4. Análisis competitivo - 4.1 Tabla comparativa

| Característica | Satori | Cyral | BigID | PgVault |
|---|---|---|---|---|
| Enfoque principal | Seguridad y acceso a datos | Data security y gobernanza de acceso | Descubrimiento y gobernanza de datos | Auditoría de seguridad y cumplimiento para PostgreSQL |
| Segmento objetivo | Enterprise | Enterprise | Enterprise | Fintechs mexicanas y equipos medianos con PostgreSQL |
| Soporte en español | Limitado | Limitado | Limitado | Sí |
| Integración regulatoria local | No específica a México | No específica a México | No específica a México | Sí, orientada a LFPDPPP, CNBV y PCI-DSS |
| Read-only sobre PostgreSQL | Parcial según despliegue | Parcial según despliegue | Parcial según despliegue | Sí |
| Ticket esperado | Alto | Alto | Alto | Medio |
| Foco en PostgreSQL | No exclusivo | No exclusivo | No exclusivo | Sí |

## 4. Análisis competitivo - 4.2 Análisis honesto

Satori, Cyral y BigID tienen mayor madurez comercial, más integraciones y capacidades enterprise que un MVP académico no puede igualar. Sin embargo, su enfoque es más amplio y su propuesta suele estar pensada para organizaciones con mayor presupuesto, procesos más pesados de compra y necesidades multibase o multinube.

PgVault compite desde otro ángulo: una herramienta más simple de adoptar, enfocada específicamente en PostgreSQL, con discurso de cumplimiento aterrizado al contexto mexicano y una experiencia read-only que reduce fricción técnica y política de instalación. Su debilidad actual frente a esos competidores está en la falta de features avanzadas de plataforma, automatización de remediación y madurez operativa.

## 4. Análisis competitivo - 4.3 Espacio en blanco

Nuestro nicho es el de fintechs mexicanas de 20 a 200 empleados que usan PostgreSQL, manejan datos sensibles y necesitan evidencia rápida de seguridad y cumplimiento sin comprar una plataforma enterprise internacional.

Los competidores no atienden bien este nicho porque suelen vender soluciones más amplias, más costosas y menos adaptadas al lenguaje regulatorio local.

Nosotros podemos servirlo bien porque ofrecemos una herramienta centrada en PostgreSQL, con instalación no invasiva, menor complejidad operativa y reportes orientados a regulaciones relevantes para el mercado mexicano.

## 5. Modelo de negocio - 5.1 Tipo de modelo de revenue

Suscripción mensual por instancia de base de datos monitoreada.

## 5. Modelo de negocio - 5.2 Tiers de pricing

| Tier | Precio | Comprador objetivo | Qué incluye |
|---|---|---|---|
| Starter | 99 USD/mes | Startup o fintech pequeña con 1 PostgreSQL principal | 1 instancia, dashboard, score y reporte ejecutivo básico |
| Growth | 299 USD/mes | Fintech mediana con varias bases o ambientes | Hasta 5 instancias, reportes técnicos, priorización de hallazgos y exportación |
| Enterprise | 999 USD/mes | Institución con requerimientos fuertes de compliance | Instancias ilimitadas, soporte prioritario, plantillas regulatorias avanzadas y despliegue dedicado |

## 5. Modelo de negocio - 5.3 Justificación del precio

El precio se plantea por debajo de plataformas enterprise internacionales y muy por debajo del costo de una auditoría manual especializada, que puede costar miles de dólares por ejercicio. La lógica no es competir por ser “lo más barato”, sino ofrecer una opción especializada, enfocada y más accesible para equipos que hoy no pueden justificar una suite global de gobierno de datos.

## 6. Go-to-market - 6.1 Primeros 10 clientes

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

**Timeline estimado:** 6 a 9 meses.

## 6. Go-to-market - 6.2 Estrategia de growth después de los 10

- Canal 1: alianzas con consultores y despachos de compliance.
- Canal 2: contenido técnico dirigido a equipos de TI y seguridad que usan PostgreSQL.
- Canal 3: referidos entre fintechs y verticales reguladas similares.

## 7. Diferenciador defendible - 7.1 Diferenciador principal

Nuestro diferenciador es la combinación de foco exclusivo en PostgreSQL, despliegue read-only sin fricción y lenguaje de cumplimiento alineado con el contexto regulatorio mexicano.

Es defendible en el tiempo porque no depende únicamente del precio ni de una feature aislada, sino de una especialización vertical y regional que los competidores globales no priorizan de forma nativa.

## 7. Diferenciador defendible - 7.2 Ejemplos concretos

- Hallazgos pensados para PostgreSQL en vez de un enfoque genérico de data governance.
- Reportes orientados a conversaciones con equipos de seguridad y compliance en México.
- Adopción más simple para equipos medianos que no pueden pasar por compras enterprise complejas.