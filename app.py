import os
import psycopg2
import redis
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Get connection details from environment
DB_NAME = os.getenv("POSTGRES_DB", "postgres")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "pass")
DB_HOST = os.getenv("DB_HOST", "db-postgres")


cache = redis.Redis(host='redis', port=6379, decode_responses=True)
@app.get("/read_inventory")
def read_inventory():
    # Check Redis first
    cached_val = cache.get("item_1")
    if cached_val:
        return {"source": "cache","status": "Sale Active", "item_id": 1, "stock_balance": cached_val}
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cur = conn.cursor()
        # Simulate checking the first item in our pgbench inventory
        cur.execute("SELECT abalance FROM pgbench_accounts WHERE aid = 1;")
        balance = cur.fetchone()[0]
        cur.close()
        conn.close()
        # Save to Redis for next time (expires in 10 seconds)
        cache.setex("item_1", 10, balance)
        return {"source": "database","status": "Sale Active", "item_id": 1, "stock_balance": balance}
#         return {"status": "Sale Active", "item_id": 1, "stock_balance": balance}
    except Exception as e:
        return {"status": "Error", "message": str(e)}
@app.get("/login")
def login_user():  # Renamed to avoid collision
    cache.set('user_logged_in', str(True))
    return "changed user logged in variable"

@app.get("/dashboard")
def get_dashboard():
    cached_val = cache.get("user_logged_in")
    if cached_val != "True":
       raise HTTPException(status_code=401, detail="Access denied")
    return "welcome user"
