from fastapi import FastAPI
from typing import List
from app.db.connection import get_pg_connection
from app.modules.config_audit.service import run_config_audit
from app.modules.pii.service import run_pii_audit
from app.models.findings import Finding
from app.services.scoring import calculate_security_score

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/db-info")
def db_info():
    with get_pg_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT current_database(), current_user;")
            db, user = cur.fetchone()
    return {"database": db, "user": user}


def normalize_config_findings(raw: List[dict]) -> List[Finding]:
    normalized: List[Finding] = []
    for f in raw:
        sev = f.get("severity", "medium")
        risk = "Medio"

        if sev == "high":
            risk = "Alto"
        elif sev == "critical":
            risk = "Crítico"
        elif sev == "low":
            risk = "Bajo"

        normalized.append(
            Finding(
                module="config",
                rule_id=f.get("id", "CONF_UNKNOWN"),
                risk=risk,
                confidence=85,
                match_type="Configuración",
                table=None,
                column=None,
                details=f.get("details", f.get("title", "")),
            )
        )
    return normalized


def normalize_pii_findings(raw: List[dict]) -> List[Finding]:
    normalized: List[Finding] = []
    for f in raw:
        normalized.append(
            Finding(
                module="pii",
                rule_id=f.get("regla", "PII_UNKNOWN"),
                risk=f.get("riesgo", "Medio"),
                confidence=int(f.get("confianza", 70)),
                match_type=f.get("tipo_match", "Desconocido"),
                table=f.get("tabla"),
                column=f.get("columna"),
                details=f.get("tipo_match", ""),
            )
        )
    return normalized


@app.get("/scan")
def scan():
    with get_pg_connection() as conn:
        config_findings = run_config_audit(conn)
        pii_findings = run_pii_audit(conn)

    return {
        "config": config_findings,
        "pii": pii_findings,
    }


@app.get("/scan/flat")
def scan_flat():
    with get_pg_connection() as conn:
        config_raw = run_config_audit(conn)
        pii_raw = run_pii_audit(conn)

    config_norm = normalize_config_findings(config_raw)
    pii_norm = normalize_pii_findings(pii_raw)
    findings = config_norm + pii_norm
    score_data = calculate_security_score(findings)

    return {
        "score": score_data["score"],
        "summary": score_data["summary"],
        "findings": findings,
    }
