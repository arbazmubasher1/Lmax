import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime

# Set up SQLite database
DB_NAME = "forex_data.db"

def setup_database():
    """Creates the database and table if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS forex_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            currency_pair TEXT,
            ask_price REAL,
            bid_price REAL,
            spread_value REAL,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_to_database(currency_pair, ask_price, bid_price, spread_value):
    """Saves extracted forex data into SQLite."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO forex_prices (currency_pair, ask_price, bid_price, spread_value, timestamp) VALUES (?, ?, ?, ?, ?)", 
                   (currency_pair, ask_price, bid_price, spread_value, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

# Set up Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

service = Service("chromedriver")  # Update path if needed
driver = webdriver.Chrome()

market_closed = False  
market_closed_time = None  
market_open_time = None  

setup_database()  # Ensure database setup

try:
    # Open the target URL
    url = "https://assets.app.lmax.com/vwap/widget-flex.html?brokt1=1&noslash=1&red=1&hidef=1&bodycss=showchart&hidega=1"
    driver.get(url)

    time.sleep(5)  
    
    while True:
        try:
            # Extract data
            currency_pair_element = driver.find_element(By.CLASS_NAME, "lw_instru_name")  
            ask_price_element = driver.find_element(By.CLASS_NAME, "ask_price_0")
            bid_price_element = driver.find_element(By.CLASS_NAME, "bid_price_0")
            spread_value_element = driver.find_element(By.CLASS_NAME, "lw_instru_spread_value")

            currency_pair = currency_pair_element.text.strip()
            ask_price = ask_price_element.text.strip()
            bid_price = bid_price_element.text.strip()
            spread_value = spread_value_element.text.strip()

            # Convert to float safely
            try:
                ask_price_float = float(ask_price) if ask_price else 0
                bid_price_float = float(bid_price) if bid_price else 0
                spread_value_float = float(spread_value) if spread_value else 0
            except ValueError:
                ask_price_float = bid_price_float = spread_value_float = 0  

            # Check for market closure
            if ask_price_float == 0 and bid_price_float == 0 and spread_value_float == 0:
                if not market_closed:
                    market_closed = True
                    market_closed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"[{currency_pair}] Market Closed at: {market_closed_time}")
            else:
                if market_closed:
                    market_closed = False
                    market_open_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"[{currency_pair}] Market Opened at: {market_open_time}")

            # Save to database when market is open
            if not market_closed:
                save_to_database(currency_pair, ask_price_float, bid_price_float, spread_value_float)
                print(f"Saved Data: {currency_pair}, Ask: {ask_price_float}, Bid: {bid_price_float}, Spread: {spread_value_float}")

        except Exception as e:
            print(f"Error extracting data: {e}")

        time.sleep(0.01)  

finally:
    driver.quit()
