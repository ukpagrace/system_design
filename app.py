import os
import psycopg2
from fastapi import FastAPI

app = FastAPI()

# Get connection details from environment
DB_NAME = os.getenv("POSTGRES_DB", "postgres")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "pass")
DB_HOST = os.getenv("DB_HOST", "db-postgres")

@app.get("/")
def read_inventory():
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cur = conn.cursor()
        # Simulate checking the first item in our pgbench inventory
        cur.execute("SELECT abalance FROM pgbench_accounts WHERE aid = 1;")
        balance = cur.fetchone()[0]
        cur.close()
        conn.close()
        return {"status": "Sale Active", "item_id": 1, "stock_balance": balance}
    except Exception as e:
        return {"status": "Error", "message": str(e)}