from fastapi import FastAPI
from app.db.connection import get_pg_connection
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

@app.get("/audit/pii")
def audit_pii():
    with get_pg_connection() as conn:
        hallazgos = run_pii_audit(conn)
    return {"total_hallazgos": len(hallazgos), "hallazgos": hallazgos}