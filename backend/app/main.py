from fastapi import FastAPI
from app.db.connection import get_pg_connection

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