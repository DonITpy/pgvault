import re
from typing import List, Dict, Any
from psycopg import Connection
from .rules import COLUMN_PATTERNS, CONTENT_PATTERNS

def detect_pii_metadata(conn: Connection) -> List[Dict]:
    findings: List[Dict] = []
    
    with conn.cursor() as cur:
        cur.execute("""
        SELECT c.relname, a.attname
        FROM pg_attribute a
        JOIN pg_class c ON a.attrelid = c.oid
        JOIN pg_namespace n ON c.relnamespace = n.oid
        WHERE a.attnum > 0 AND NOT a.attisdropped AND n.nspname = 'public';
        """)
        columns = cur.fetchall()

    for table_name, column_name in columns:
        for rule_name, pattern in COLUMN_PATTERNS.items():
            if re.search(pattern, column_name):
                findings.append({
                    "id": f"PII_META_{rule_name}",
                    "severity": "high" if "PCI" in rule_name else "medium",
                    "title": f"Posible PII en nombre de columna ({rule_name})",
                    "details": f"La columna '{column_name}' en la tabla '{table_name}' coincide con el patrón {rule_name}.",
                    "evidence": [f"{table_name}.{column_name}"]
                })
                
    return findings

def get_text_columns(conn: Connection) -> List[tuple]:
    with conn.cursor() as cur:
        cur.execute("""
        SELECT c.relname, a.attname
        FROM pg_attribute a
        JOIN pg_class c ON a.attrelid = c.oid
        JOIN pg_namespace n ON c.relnamespace = n.oid
        JOIN pg_type t ON a.atttypid = t.oid
        WHERE a.attnum > 0 AND NOT a.attisdropped AND n.nspname = 'public'
        AND t.typname IN ('varchar', 'text', 'char');
        """)
        return cur.fetchall()

def fetch_sample_data(conn: Connection, table_name: str, column_name: str, sample_size: int = 385) -> List[Any]:
    with conn.cursor() as cur:
        try:
            cur.execute(f"""
            SELECT "{column_name}"
            FROM "{table_name}" TABLESAMPLE SYSTEM(10)
            WHERE "{column_name}" IS NOT NULL
            LIMIT {sample_size};
            """)
            return [row[0] for row in cur.fetchall()]
        except Exception:
            return []

def analyze_sample(sample_data: List[Any], table_name: str, column_name: str) -> List[Dict]:
    findings: List[Dict] = []
    total_rows = len(sample_data)
    
    if total_rows == 0:
        return findings

    match_counts = {rule: 0 for rule in CONTENT_PATTERNS}
    for value in sample_data:
        str_value = str(value).strip()
        for rule_name, pattern in CONTENT_PATTERNS.items():
            if pattern.match(str_value):
                match_counts[rule_name] += 1

    for rule_name, count in match_counts.items():
        match_percentage = count / total_rows
        if match_percentage > 0.15:
            findings.append({
                "id": f"PII_DATA_{rule_name}",
                "severity": "high" if "PCI" in rule_name else "medium",
                "title": f"Datos sensibles detectados por sampling ({rule_name})",
                "details": f"El {round(match_percentage * 100, 2)}% de la muestra en '{table_name}.{column_name}' coincide con {rule_name}.",
                "evidence": [f"Muestra evaluada: {total_rows} registros"]
            })
            
    return findings

def detect_pii_content(conn: Connection) -> List[Dict]:
    text_columns = get_text_columns(conn)
    all_findings: List[Dict] = []
    
    for table_name, column_name in text_columns:
        sample = fetch_sample_data(conn, table_name, column_name)
        if sample:
            all_findings.extend(analyze_sample(sample, table_name, column_name))
            
    return all_findings

def run_pii_audit(conn: Connection) -> List[Dict]:
    return detect_pii_metadata(conn) + detect_pii_content(conn)