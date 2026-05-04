from typing import List, Dict
from psycopg import Connection

def run_config_audit(conn: Connection) -> List[Dict]:
    findings: List[Dict] = []

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
        })

    return findings