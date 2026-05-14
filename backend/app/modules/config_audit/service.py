from typing import List, Dict
from psycopg import Connection

def run_config_audit(conn: Connection) -> List[Dict]:
    findings: List[Dict] = []

    # Check 1: Roles con SUPERUSER innecesario
    with conn.cursor() as cur:
        cur.execute("""
            SELECT rolname
            FROM pg_roles
            WHERE rolsuper = true
            AND rolname NOT IN ('postgres');
        """)
        rows = cur.fetchall()
        if rows:
            findings.append({
                "id": "CONF_SUPERUSER_EXTRA",
                "severity": "high",
                "title": "Roles con SUPERUSER innecesario",
                "details": f"Se encontraron {len(rows)} roles con SUPERUSER además de 'postgres'.",
                "evidence": [r[0] for r in rows],
                "remediation_sql": "REVOKE SUPERUSER FROM nombre_rol;"
            })

    # Check 2: log_connections desactivado
    with conn.cursor() as cur:
        cur.execute("""
            SELECT setting
            FROM pg_settings
            WHERE name = 'log_connections';
        """)
        row = cur.fetchone()
        if row and row[0] != "on":
            findings.append({
                "id": "CONF_LOG_CONNECTIONS_OFF",
                "severity": "medium",
                "title": "El logging de conexiones no está habilitado",
                "details": "El parámetro log_connections no está configurado en 'on', lo que dificulta la trazabilidad de accesos a la base de datos.",
                "evidence": {"log_connections": row[0]},
                "remediation_sql": "ALTER SYSTEM SET log_connections = 'on';"
            })

    # Check 3: log_statement deshabilitado
    with conn.cursor() as cur:
        cur.execute("""
            SELECT setting
            FROM pg_settings
            WHERE name = 'log_statement';
        """)
        row = cur.fetchone()
        if row and row[0] == "none":
            findings.append({
                "id": "CONF_LOG_STATEMENT_NONE",
                "severity": "medium",
                "title": "No se está registrando ninguna sentencia SQL",
                "details": "El parámetro log_statement está en 'none', por lo que no se registran consultas SQL y se limita la capacidad de auditoria.",
                "evidence": {"log_statement": row[0]},
                "remediation_sql": "ALTER SYSTEM SET log_statement = 'ddl';"
            })

    # Check 4: logging_collector apagado
    with conn.cursor() as cur:
        cur.execute("""
            SELECT setting
            FROM pg_settings
            WHERE name = 'logging_collector';
        """)
        row = cur.fetchone()
        if row and row[0] != "on":
            findings.append({
                "id": "CONF_LOGGING_COLLECTOR_OFF",
                "severity": "medium",
                "title": "El logging_collector no está habilitado",
                "details": "Sin logging_collector, los eventos del servidor no se recopilan de forma adecuada para auditoria.",
                "evidence": {"logging_collector": row[0]},
                "remediation_sql": "ALTER SYSTEM SET logging_collector = 'on';"
            })

    # Check 5: ssl apagado
    with conn.cursor() as cur:
        cur.execute("""
            SELECT setting
            FROM pg_settings
            WHERE name = 'ssl';
        """)
        row = cur.fetchone()
        if row and row[0] != "on":
            findings.append({
                "id": "CONF_SSL_OFF",
                "severity": "high",
                "title": "SSL no está habilitado",
                "details": "La instancia no tiene SSL habilitado, por lo que las conexiones podrian viajar sin cifrado.",
                "evidence": {"ssl": row[0]},
                "remediation_sql": "Configurar ssl en on y certificados válidos en el servidor."
            })

    # Check 6: password_encryption débil
    with conn.cursor() as cur:
        cur.execute("""
            SELECT setting
            FROM pg_settings
            WHERE name = 'password_encryption';
        """)
        row = cur.fetchone()
        if row and row[0].lower() != "scram-sha-256":
            findings.append({
                "id": "CONF_PASSWORD_ENCRYPTION_WEAK",
                "severity": "high",
                "title": "password_encryption no usa SCRAM-SHA-256",
                "details": "La configuración de password_encryption no esta en SCRAM-SHA-256, lo que reduce la seguridad de autenticación.",
                "evidence": {"password_encryption": row[0]},
                "remediation_sql": "ALTER SYSTEM SET password_encryption = 'scram-sha-256';"
            })

    # Check 7: extensiones peligrosas instaladas
    with conn.cursor() as cur:
        cur.execute("""
            SELECT extname
            FROM pg_extension
            WHERE extname IN ('dblink', 'file_fdw', 'postgres_fdw', 'adminpack');
        """)
        rows = cur.fetchall()
        if rows:
            findings.append({
                "id": "CONF_DANGEROUS_EXTENSIONS",
                "severity": "high",
                "title": "Hay extensiones potencialmente peligrosas instaladas",
                "details": f"Se encontraron {len(rows)} extensiones que deben justificarse por riesgo operacional o de acceso.",
                "evidence": [r[0] for r in rows],
                "remediation_sql": "DROP EXTENSION nombre_extension;"
            })

    # Check 8: funciones SECURITY DEFINER
    with conn.cursor() as cur:
        cur.execute("""
            SELECT n.nspname, p.proname
            FROM pg_proc p
            JOIN pg_namespace n ON p.pronamespace = n.oid
            WHERE p.prosecdef = true
            AND n.nspname NOT IN ('pg_catalog', 'information_schema');
        """)
        rows = cur.fetchall()
        if rows:
            findings.append({
                "id": "CONF_SECURITY_DEFINER_PRESENT",
                "severity": "high",
                "title": "Existen funciones SECURITY DEFINER que deben revisarse",
                "details": f"Se encontraron {len(rows)} funciones SECURITY DEFINER fuera de esquemas del sistema.",
                "evidence": [f"{r[0]}.{r[1]}" for r in rows],
                "remediation_sql": "Revisar search_path fijo y privilegios mínimos sobre cada función SECURITY DEFINER."
            })

    # Check 9: métodos de autenticación inseguros en pg_hba
    with conn.cursor() as cur:
        cur.execute("""
            SELECT type, database, user_name, address, auth_method
            FROM pg_hba_file_rules
            WHERE auth_method IN ('trust', 'password')
              AND type != 'local';
        """)
        rows = cur.fetchall()
        if rows:
            findings.append({
                "id": "CONF_HBA_INSECURE_AUTH",
                "severity": "high",
                "title": "Métodos de autenticación inseguros detectados en pg_hba",
                "details": f"Se encontraron {len(rows)} reglas en pg_hba que usan métodos inseguros (trust o password en claro) para conexiones de red.",
                "evidence": [
                    {
                        "type": r[0],
                        "database": r[1],
                        "user": r[2],
                        "address": r[3],
                        "auth_method": r[4]
                    }
                    for r in rows
                ],
                "remediation_sql": "Cambiar el método de autenticación a scram-sha-256 en pg_hba.conf para todas las conexiones de red."
            })

    return findings