from typing import List, Dict
from psycopo import Connection

def run_config_audit(conn: Connection) -> List[Dict]:
    findings: List[Dict] = []
    
    # Check 1: Roles con SUPERUSER innecesario
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT rolname
            FROM pg_roles
            WHERE rolsuper = true
            AND rolname NOT IN ('postgres');
            """
        )
        rows = cur.fetchall()
        if rows:
            findings.append(
                {
                    "id": "CONF_SUPERUSER_EXTRA",
                    "severity": "high",
                    "title": "Roles con SUPERUSER innecesario",
                    "details": f"Se encontraron {len(rows)} roles con SUPERUSER además de postgres.",
                    "evidence": [r[0] for r in rows],
                }
            )

    # Check 2: log_connections desactivado
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT setting
            FROM pg_settings
            WHERE name = 'log_connections';
            """
        )
        row = cur.fetchone()
        if row and row[0] != "on":
            findings.append(
                {
                    "id": "CONF_LOG_CONNECTIONS_OFF",
                    "severity": "medium",
                    "title": "El logging de conexiones no está habilitado",
                    "details": "El parámetro log_connections no está configurado en 'on', lo que dificulta la trazabilidad de accesos a la base de datos.",
                    "evidence": {"log_connections": row[0]},
                }
            )

    # Check 3: log_statement demasiado laxo
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT setting
            FROM pg_settings
            WHERE name = 'log_statement';
            """
        )
        row = cur.fetchone()
        if row and row[0] == "none":
            findings.append(
                {
                    "id": "CONF_LOG_STATEMENT_NONE",
                    "severity": "medium",
                    "title": "No se está registrando ninguna sentencia SQL",
                    "details": "El parametro log_statement está en 'none', por lo que no se registran consultas SQL y se limite la capacidad de auditoria.",
                    "evidence": {"log_statement": row[0]},
                }
            )

    return findings
