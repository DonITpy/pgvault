# Documento de Negocio

## 2. Problema - 2.1 Descripción del problema

### Las fintech mexicanas que operan sobre bases de datos PostgreSQL manejan miles de registros con datos sensibles de clientes, pero carecen de una visibilidad continua sobre su postura de seguridad y cumplimiento. Hoy dependen de auditorías manuales que se realizan una o dos veces al año, en las que un consultor externo ejecuta queries sobre los catálogos del sistema, genera un PDF con hallazgos y desaparece. Entre una auditoría y otra, la base de datos cambia: se crean nuevos roles, se agregan columnas con datos personales y se modifican parámetros de configuración sin un control centralizado. Esto abre ventanas de riesgo donde un error de privilegios o una mala práctica de almacenamiento de datos puede pasar desapercibida durante meses.

### Cuando llega una auditoría regulatoria de la CNBV o se presenta una investigación por potencial incumplimiento de la LFPDPPP, el equipo de TI se ve obligado a trabajar bajo presión reuniendo evidencias, ejecutando consultas a mano y reconstruyendo el estado de seguridad de la base de datos a partir de logs incompletos. Este proceso consume días de trabajo de perfiles senior, genera estrés organizacional y aun así puede dejar huecos que deriven en multas costosas o pérdida de confianza. No existe, en el contexto local, una herramienta accesible y enfocada en el mercado latinoamericano que entregue un inventario actualizado de riesgos de seguridad y datos sensibles en PostgreSQL sin necesidad de instalar agentes ni modificar la base de datos del cliente.

## 2. Problema - 2.2 User persona principal

# | Atributo                  | Valor                                                                 |
## |---------------------------|-----------------------------------------------------------------------|
### | Nombre y rol              | Carlos Méndez, CISO en fintech mexicana                              |
### | Edad y experiencia        | 35 años, 10 años en seguridad de la información                      |
### | Tamaño de empresa         | 40 empleados, 2 equipos de desarrollo y 1 equipo de operaciones      |
### | Industria                 | Servicios financieros digitales (fintech regulada por CNBV)          |
### | Día típico de trabajo     | Revisa incidentes de seguridad, coordina auditorías, atiende comités |
### | Pain points principales   | Falta de visibilidad continua sobre privilegios y datos sensibles; dependencia de auditorías manuales y consultores externos; presión por cumplir LFPDPPP y PCI-DSS |
### | Cómo resuelve hoy el problema | Contrata auditorías puntuales una o dos veces al año, mantiene hojas de cálculo con inventarios parciales y revisa consultas ad hoc con el equipo de base de datos |
### | Costo del problema        | Semanas de trabajo acumulado al año, riesgo de multas altas por incumplimiento y desgaste del equipo técnico en cada ciclo de auditoría             |
