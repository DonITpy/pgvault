from fastapi import FastAPI
from app.db.connection import get_pg_connection
from app.modules.config_audit.service import run_config_audit
from app.modules.pii.service import run_pii_audit

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


@app.get("/scan")
def scan():
    with get_pg_connection() as conn:
        config_findings = run_config_audit(conn)
        pii_findings = run_pii_audit(conn)

    return {
        "config": config_findings,
        "pii": pii_findings,
    }