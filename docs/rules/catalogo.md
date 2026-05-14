# Catálogo de reglas — PgVault

Este documento describe todas las reglas implementadas en PgVault para la detección
de problemas de configuración y datos sensibles sobre bases de datos PostgreSQL.
Cada regla incluye su identificador, descripción, severidad, lógica de detección,
query utilizada y regulación asociada.

---

## Módulo 1 — Auditoría de configuración

### CONF_SUPERUSER_EXTRA

| Campo | Valor |
|---|---|
| ID | CONF_SUPERUSER_EXTRA |
| Severidad | Alto |
| Categoría | Privilegios |
| Descripción | Detecta roles con privilegio SUPERUSER además del rol postgres nativo. |
| Regulación asociada | LFPDPPP Art. 19, PCI-DSS Req. 7, CIS PostgreSQL Benchmark |
| Remediación | REVOKE SUPERUSER FROM nombre_rol; |

**Lógica de detección:**

```sql
SELECT rolname
FROM pg_roles
WHERE rolsuper = true
  AND rolname NOT IN ('postgres');
```

Si la consulta devuelve uno o más roles, se genera un hallazgo con la lista de roles afectados.

---

### CONF_SSL_OFF

| Campo | Valor |
|---|---|
| ID | CONF_SSL_OFF |
| Severidad | Alto |
| Categoría | Cifrado en tránsito |
| Descripción | Detecta que el parámetro SSL no está habilitado en el servidor, lo que permite conexiones sin cifrado. |
| Regulación asociada | PCI-DSS Req. 4.2.1, LFPDPPP Art. 19, CIS PostgreSQL Benchmark |
| Remediación | Configurar ssl = on y certificados válidos en postgresql.conf. |

**Lógica de detección:**

```sql
SELECT setting
FROM pg_settings
WHERE name = 'ssl';
```

Si el valor devuelto es diferente de `on`, se genera el hallazgo.

---

### CONF_DANGEROUS_EXTENSIONS

| Campo | Valor |
|---|---|
| ID | CONF_DANGEROUS_EXTENSIONS |
| Severidad | Alto |
| Categoría | Extensiones |
| Descripción | Detecta extensiones instaladas que pueden representar riesgo operacional o de acceso no autorizado. |
| Extensiones evaluadas | dblink, file_fdw, postgres_fdw, adminpack |
| Regulación asociada | CIS PostgreSQL Benchmark, PCI-DSS Req. 6.3 |
| Remediación | DROP EXTENSION nombre_extension; si no está justificada su presencia. |

**Lógica de detección:**

```sql
SELECT extname
FROM pg_extension
WHERE extname IN ('dblink', 'file_fdw', 'postgres_fdw', 'adminpack');
```

Si la consulta devuelve una o más extensiones, se genera el hallazgo con la lista.

---

### CONF_SECURITY_DEFINER_PRESENT

| Campo | Valor |
|---|---|
| ID | CONF_SECURITY_DEFINER_PRESENT |
| Severidad | Alto |
| Categoría | Funciones privilegiadas |
| Descripción | Detecta funciones con atributo SECURITY DEFINER fuera de esquemas del sistema, que ejecutan con los permisos del creador y pueden elevar privilegios si no están bien controladas. |
| Regulación asociada | CIS PostgreSQL Benchmark, PCI-DSS Req. 7 |
| Remediación | Revisar search_path fijo y privilegios mínimos sobre cada función SECURITY DEFINER. |

**Lógica de detección:**

```sql
SELECT n.nspname, p.proname
FROM pg_proc p
JOIN pg_namespace n ON p.pronamespace = n.oid
WHERE p.prosecdef = true
  AND n.nspname NOT IN ('pg_catalog', 'information_schema');
```

Si la consulta devuelve una o más funciones, se genera el hallazgo con la lista de esquema y nombre.

---

### CONF_LOG_CONNECTIONS_OFF

| Campo | Valor |
|---|---|
| ID | CONF_LOG_CONNECTIONS_OFF |
| Severidad | Medio |
| Categoría | Logging y trazabilidad |
| Descripción | Detecta que el parámetro log_connections no está habilitado, lo que dificulta la trazabilidad de accesos a la base de datos. |
| Regulación asociada | PCI-DSS Req. 10.2, CNBV Circular Única de Bancos |
| Remediación | ALTER SYSTEM SET log_connections = 'on'; |

**Lógica de detección:**

```sql
SELECT setting
FROM pg_settings
WHERE name = 'log_connections';
```

Si el valor devuelto es diferente de `on`, se genera el hallazgo.

---

### CONF_LOG_STATEMENT_NONE

| Campo | Valor |
|---|---|
| ID | CONF_LOG_STATEMENT_NONE |
| Severidad | Medio |
| Categoría | Logging y trazabilidad |
| Descripción | Detecta que el parámetro log_statement está en none, lo que significa que ninguna sentencia SQL se registra en los logs del servidor. |
| Regulación asociada | PCI-DSS Req. 10.2, CNBV Circular Única de Bancos |
| Remediación | ALTER SYSTEM SET log_statement = 'ddl'; |

**Lógica de detección:**

```sql
SELECT setting
FROM pg_settings
WHERE name = 'log_statement';
```

Si el valor devuelto es `none`, se genera el hallazgo.

---

### CONF_LOGGING_COLLECTOR_OFF

| Campo | Valor |
|---|---|
| ID | CONF_LOGGING_COLLECTOR_OFF |
| Severidad | Medio |
| Categoría | Logging y trazabilidad |
| Descripción | Detecta que logging_collector no está habilitado, lo que impide que los eventos del servidor se recopilen en archivos de log. |
| Regulación asociada | PCI-DSS Req. 10.5, CNBV Circular Única de Bancos |
| Remediación | ALTER SYSTEM SET logging_collector = 'on'; |

**Lógica de detección:**

```sql
SELECT setting
FROM pg_settings
WHERE name = 'logging_collector';
```

Si el valor devuelto es diferente de `on`, se genera el hallazgo.

---

### CONF_PASSWORD_ENCRYPTION_WEAK

| Campo | Valor |
|---|---|
| ID | CONF_PASSWORD_ENCRYPTION_WEAK |
| Severidad | Alto |
| Categoría | Autenticación |
| Descripción | Detecta que el parámetro password_encryption no está configurado en scram-sha-256, el método más seguro disponible en PostgreSQL 14+. |
| Regulación asociada | PCI-DSS Req. 8.3, CIS PostgreSQL Benchmark |
| Remediación | ALTER SYSTEM SET password_encryption = 'scram-sha-256'; |

**Lógica de detección:**

```sql
SELECT setting
FROM pg_settings
WHERE name = 'password_encryption';
```

Si el valor devuelto es diferente de `scram-sha-256`, se genera el hallazgo.

---

## Módulo 2 — Descubrimiento de datos sensibles (PII/PCI)

### Detección por nombre de columna

Las siguientes reglas se aplican sobre los nombres de columnas de todas las tablas
reales del esquema público. Se usa expresiones regulares sobre el nombre de la columna
para identificar candidatos con confianza media (60%).

| ID de regla | Patrón regex | Qué detecta | Riesgo | Regulación |
|---|---|---|---|---|
| PII_RFC | `(?i).*(rfc\|tax_id).*` | RFC mexicano | Medio | LFPDPPP Art. 3 |
| PII_CURP | `(?i).*(curp\|id_nacional).*` | CURP mexicano | Medio | LFPDPPP Art. 3 |
| PII_EMAIL | `(?i).*(email\|correo).*` | Correo electrónico | Medio | LFPDPPP Art. 3 |
| PCI_TARJETA | `(?i).*(tarjeta\|card_number\|pan\|ccn).*` | Número de tarjeta de pago | Alto | PCI-DSS Req. 3 |
| PCI_CVV | `(?i).*(cvv\|cvc\|codigo_seguridad).*` | Código de seguridad de tarjeta | Alto | PCI-DSS Req. 3 |
| PII_TELEFONO | `(?i).*(telefono\|phone\|celular).*` | Número de teléfono | Medio | LFPDPPP Art. 3 |
| SEC_PASSWORD | `(?i).*(password\|contrase[ñn]a\|pwd).*` | Contraseña en texto plano | Medio | LFPDPPP Art. 19 |
| PII_NOMBRE | `(?i).*(nombre\|name\|full_name).*` | Nombre de persona | Medio | LFPDPPP Art. 3 |
| PII_APELLIDO | `(?i).*(apellido\|lastname\|surname).*` | Apellido de persona | Medio | LFPDPPP Art. 3 |
| PII_DIRECCION | `(?i).*(direccion\|address\|domicilio).*` | Dirección física | Medio | LFPDPPP Art. 3 |
| PII_FECHA_NACIMIENTO | `(?i).*(fecha_nacimiento\|birth_date\|dob).*` | Fecha de nacimiento | Medio | LFPDPPP Art. 3 |
| PII_CP | `(?i).*(codigo_postal\|cp\|zip).*` | Código postal | Medio | LFPDPPP Art. 3 |

**Query base para detección por nombre:**

```sql
SELECT c.relname, a.attname
FROM pg_attribute a
JOIN pg_class c ON a.attrelid = c.oid
JOIN pg_namespace n ON c.relnamespace = n.oid
WHERE a.attnum > 0
  AND NOT a.attisdropped
  AND n.nspname = 'public'
  AND c.relkind IN ('r', 'p')
  AND c.relname NOT LIKE 'dblink%'
  AND c.relname NOT LIKE 'idx_%'
  AND c.relname NOT LIKE '%_pkey'
  AND c.relname NOT LIKE '%_key';
```

---

### Detección por contenido con sampling estadístico

Las siguientes reglas se aplican sobre el contenido real de columnas de tipo texto.
Se toma una muestra de hasta 385 filas por columna usando `TABLESAMPLE SYSTEM(10)`,
lo que corresponde al tamaño mínimo para un nivel de confianza del 95% con margen
de error del 5% sobre una población grande. Si más del 15% de los valores de la
muestra coinciden con el patrón, se genera un hallazgo con confianza alta (75-95%).

| ID de regla | Expresión regular | Qué valida | Riesgo | Regulación |
|---|---|---|---|---|
| PII_RFC_DATA | `^[A-ZÑ&]{3,4}\d{6}[A-V1-9][A-Z1-9][0-9A]$` | Formato RFC mexicano | Medio | LFPDPPP Art. 3 |
| PII_EMAIL_DATA | `^[\w\.-]+@[\w\.-]+\.\w+$` | Formato de correo electrónico | Medio | LFPDPPP Art. 3 |
| PCI_TARJETA_DATA | `^\d{13,19}$` | Secuencia numérica de 13 a 19 dígitos (número de tarjeta) | Alto | PCI-DSS Req. 3 |
| PII_TELEFONO_DATA | `^\+?\d{10,15}$` | Secuencia numérica de 10 a 15 dígitos (teléfono) | Medio | LFPDPPP Art. 3 |
| PII_CP_DATA | `^\d{5}$` | Secuencia numérica de exactamente 5 dígitos (código postal) | Medio | LFPDPPP Art. 3 |

**Query base para obtener columnas de texto candidatas:**

```sql
SELECT c.relname, a.attname
FROM pg_attribute a
JOIN pg_class c ON a.attrelid = c.oid
JOIN pg_namespace n ON c.relnamespace = n.oid
JOIN pg_type t ON a.atttypid = t.oid
WHERE a.attnum > 0
  AND NOT a.attisdropped
  AND n.nspname = 'public'
  AND c.relkind IN ('r', 'p')
  AND t.typname IN ('varchar', 'text', 'char');
```

**Query de sampling por columna:**

```sql
SELECT "nombre_columna"
FROM "nombre_tabla" TABLESAMPLE SYSTEM(10)
WHERE "nombre_columna" IS NOT NULL
LIMIT 385;
```

---

## Resumen de cobertura sobre FintechDB

| Módulo | Tipo | Hallazgos detectados |
|---|---|---|
| Config | Auditoría de configuración | 7 |
| PII | Detección por nombre | 19 |
| PII | Detección por contenido | 7 |
| **Total** | | **33** |

**Score resultante sobre FintechDB: 55/100**