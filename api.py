from fastapi import FastAPI
import sqlite3
from datetime import datetime

app = FastAPI()

DB_NAME = "forex_data.db"

def get_latest_data():
    """Fetch the latest forex data from SQLite."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT currency_pair, ask_price, bid_price, spread_value, timestamp FROM forex_prices ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "currency_pair": row[0],
            "ask_price": row[1],
            "bid_price": row[2],
            "spread_value": row[3],
            "timestamp": row[4]
        }
    return {"error": "No data available"}

@app.get("/")
def home():
    return {"message": "Forex API is running!"}

@app.get("/latest")
def latest_forex_data():
    """API Endpoint to fetch latest forex price."""
    return get_latest_data()
