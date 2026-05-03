import os
import psycopg

def get_pg_connection():
    host = os.getenv("PG_HOST", "localhost")
    port = int(os.getenv("PG_PORT", "5433"))
    dbname = os.getenv("PG_DATABASE", "fintechdb")
    user = os.getenv("PG_USER", "fintech_user")
    password = os.getenv("PG_PASSWORD", "fintech_pass")

    conn = psycopg.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password,
        autocommit=True,
    )
    return conn