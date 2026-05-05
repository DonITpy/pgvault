import re
from .rules import COLUMN_PATTERNS, CONTENT_PATTERNS

def detect_pii_metadata(db_connection):
    cursor = db_connection.cursor()
    query = """
    SELECT c.relname, a.attname
    FROM pg_attribute a
    JOIN pg_class c ON a.attrelid = c.oid
    JOIN pg_namespace n ON c.relnamespace = n.oid
    WHERE a.attnum > 0 AND NOT a.attisdropped AND n.nspname = 'public';
    """
    cursor.execute(query)
    columns = cursor.fetchall()
    findings = []
    
    for table_name, column_name in columns:
        for rule_name, pattern in COLUMN_PATTERNS.items():
            if re.search(pattern, column_name):
                findings.append({
                    "modulo": "PII",
                    "tabla": table_name,
                    "columna": column_name,
                    "regla": rule_name,
                    "tipo_match": "Metadatos (Nombre)",
                    "confianza": 60,
                    "riesgo": "Alto" if "PCI" in rule_name else "Medio"
                })
    cursor.close()
    return findings

def get_text_columns(db_cursor):
    query = """
    SELECT c.relname, a.attname
    FROM pg_attribute a
    JOIN pg_class c ON a.attrelid = c.oid
    JOIN pg_namespace n ON c.relnamespace = n.oid
    JOIN pg_type t ON a.atttypid = t.oid
    WHERE a.attnum > 0 AND NOT a.attisdropped AND n.nspname = 'public'
    AND t.typname IN ('varchar', 'text', 'char');
    """
    db_cursor.execute(query)
    return db_cursor.fetchall()

def fetch_sample_data(db_cursor, table_name, column_name, sample_size=385):
    query = f"""
    SELECT "{column_name}"
    FROM "{table_name}" TABLESAMPLE SYSTEM(10)
    WHERE "{column_name}" IS NOT NULL
    LIMIT {sample_size};
    """
    try:
        db_cursor.execute(query)
        return [row[0] for row in db_cursor.fetchall()]
    except Exception:
        return []

def analyze_sample(sample_data, table_name, column_name):
    findings = []
    total_rows = len(sample_data)
    if total_rows == 0: return findings

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
                "modulo": "PII",
                "tabla": table_name,
                "columna": column_name,
                "regla": rule_name,
                "tipo_match": "Contenido (Sampling)",
                "porcentaje_coincidencia": round(match_percentage * 100, 2),
                "riesgo": "Alto" if "PCI" in rule_name else "Medio",
                "confianza": 95 if match_percentage > 0.8 else 75
            })
    return findings

def detect_pii_content(db_connection):
    cursor = db_connection.cursor()
    text_columns = get_text_columns(cursor)
    all_findings = []
    
    for table_name, column_name in text_columns:
        sample = fetch_sample_data(cursor, table_name, column_name)
        if sample:
            col_findings = analyze_sample(sample, table_name, column_name)
            all_findings.extend(col_findings)
            
    cursor.close()
    return all_findings

def run_pii_audit(db_connection):
    metadata_findings = detect_pii_metadata(db_connection)
    content_findings = detect_pii_content(db_connection)
    return metadata_findings + content_findings