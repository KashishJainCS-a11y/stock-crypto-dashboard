"""Application configuration"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "demo")

# Symbols
STOCK_SYMBOLS = os.getenv("STOCK_SYMBOLS", "AAPL,GOOGL,MSFT").split(",")
CRYPTO_SYMBOLS = os.getenv("CRYPTO_SYMBOLS", "BTC,ETH").split(",")

# Database
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/stock_crypto.db")

# Streamlit
REFRESH_INTERVAL = int(os.getenv("REFRESH_INTERVAL", "60"))

# Technical Analysis
SMA_PERIODS = [20, 50, 200]  # Days
EMA_PERIODS = [12, 26]
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
