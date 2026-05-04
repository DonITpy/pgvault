# Documento de Arquitectura


## 1. Visión general


PgVault es un servicio B2B pensado para analizar la seguridad y el cumplimiento en bases de datos PostgreSQL. La idea es que se conecta a la base del cliente en modo read-only, o sea, solo lectura, para no modificar nada de la información mientras se hacen los análisis.

El sistema funciona con un backend en Python usando FastAPI. Desde ahí se hace la conexión a la base de datos con psycopg y se ejecutan distintos módulos, principalmente de auditoría de configuración (por ejemplo, permisos o settings inseguros) y detección de datos sensibles como información personal.

Toda esta información se expone a través de una API HTTP, que luego consume un frontend hecho en React. En esa parte se muestra un dashboard donde se puede ver un score de seguridad general y el detalle de los riesgos encontrados, para que sea fácil de entender.

Para correr todo el proyecto usamos Docker Compose, lo que permite levantar todos los servicios de forma sencilla. Como parte de las pruebas, trabajamos con las bases FintechDB y TiendaDB que se proporcionaron en la materia.
