"""Database operations for caching and historical data"""
import sqlite3
import pandas as pd
from datetime import datetime
from typing import Optional, List
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    """SQLite database for stock and crypto data"""
    
    def __init__(self, db_path: str = "data/stock_crypto.db"):
        """
        Initialize database
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_db()
    
    def init_db(self):
        """Initialize database tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Prices table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS prices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    asset_type TEXT NOT NULL,
                    date DATETIME NOT NULL,
                    open REAL NOT NULL,
                    high REAL NOT NULL,
                    low REAL NOT NULL,
                    close REAL NOT NULL,
                    volume REAL NOT NULL,
                    UNIQUE(symbol, asset_type, date)
                )
            """)
            
            # Alerts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    asset_type TEXT NOT NULL,
                    alert_type TEXT NOT NULL,
                    target_price REAL NOT NULL,
                    created_at DATETIME NOT NULL,
                    triggered BOOLEAN DEFAULT 0,
                    triggered_at DATETIME
                )
            """)
            
            # Portfolio table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS portfolio (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    asset_type TEXT NOT NULL,
                    quantity REAL NOT NULL,
                    purchase_price REAL NOT NULL,
                    purchase_date DATETIME NOT NULL,
                    created_at DATETIME NOT NULL
                )
            """)
            
            conn.commit()
            logger.info(f"Database initialized at {self.db_path}")
        
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
        
        finally:
            if conn:
                conn.close()
    
    def save_price_data(
        self,
        symbol: str,
        asset_type: str,
        data: pd.DataFrame
    ) -> bool:
        """
        Save price data to database
        
        Args:
            symbol: Asset symbol
            asset_type: 'stock' or 'crypto'
            data: DataFrame with OHLCV data
        
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for idx, row in data.iterrows():
                cursor.execute("""
                    INSERT OR REPLACE INTO prices
                    (symbol, asset_type, date, open, high, low, close, volume)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    symbol,
                    asset_type,
                    idx,
                    row['Open'],
                    row['High'],
                    row['Low'],
                    row['Close'],
                    row['Volume']
                ))
            
            conn.commit()
            logger.info(f"Saved {len(data)} rows for {symbol}")
            return True
        
        except Exception as e:
            logger.error(f"Error saving price data: {e}")
            return False
        
        finally:
            if conn:
                conn.close()
    
    def get_price_data(
        self,
        symbol: str,
        asset_type: str,
        limit: int = 100
    ) -> Optional[pd.DataFrame]:
        """
        Get price data from database
        
        Args:
            symbol: Asset symbol
            asset_type: 'stock' or 'crypto'
            limit: Number of recent rows to fetch
        
        Returns:
            DataFrame or None if not found
        """
        try:
            conn = sqlite3.connect(self.db_path)
            query = """
                SELECT date, open, high, low, close, volume
                FROM prices
                WHERE symbol = ? AND asset_type = ?
                ORDER BY date DESC
                LIMIT ?
            """
            df = pd.read_sql_query(query, conn, params=(symbol, asset_type, limit))
            conn.close()
            
            if df.empty:
                return None
            
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            df.set_index('date', inplace=True)
            
            return df
        
        except Exception as e:
            logger.error(f"Error retrieving price data: {e}")
            return None
    
    def add_alert(
        self,
        symbol: str,
        asset_type: str,
        alert_type: str,
        target_price: float
    ) -> bool:
        """
        Add a price alert
        
        Args:
            symbol: Asset symbol
            asset_type: 'stock' or 'crypto'
            alert_type: 'above' or 'below'
            target_price: Target price
        
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO alerts
                (symbol, asset_type, alert_type, target_price, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (symbol, asset_type, alert_type, target_price, datetime.now()))
            
            conn.commit()
            logger.info(f"Alert created for {symbol} at ${target_price}")
            return True
        
        except Exception as e:
            logger.error(f"Error creating alert: {e}")
            return False
        
        finally:
            if conn:
                conn.close()
    
    def get_active_alerts(self) -> List[dict]:
        """
        Get all active alerts
        
        Returns:
            List of alert dictionaries
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, symbol, asset_type, alert_type, target_price
                FROM alerts
                WHERE triggered = 0
            """)
            
            rows = cursor.fetchall()
            conn.close()
            
            alerts = [
                {
                    'id': row[0],
                    'symbol': row[1],
                    'asset_type': row[2],
                    'alert_type': row[3],
                    'target_price': row[4]
                }
                for row in rows
            ]
            
            return alerts
        
        except Exception as e:
            logger.error(f"Error retrieving alerts: {e}")
            return []
    
    def add_portfolio_item(
        self,
        symbol: str,
        asset_type: str,
        quantity: float,
        purchase_price: float
    ) -> bool:
        """
        Add item to portfolio
        
        Args:
            symbol: Asset symbol
            asset_type: 'stock' or 'crypto'
            quantity: Quantity purchased
            purchase_price: Price per unit
        
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO portfolio
                (symbol, asset_type, quantity, purchase_price, purchase_date, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (symbol, asset_type, quantity, purchase_price, datetime.now(), datetime.now()))
            
            conn.commit()
            logger.info(f"Added {quantity} {symbol} to portfolio")
            return True
        
        except Exception as e:
            logger.error(f"Error adding portfolio item: {e}")
            return False
        
        finally:
            if conn:
                conn.close()
    
    def get_portfolio(self) -> List[dict]:
        """
        Get all portfolio items
        
        Returns:
            List of portfolio items
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, symbol, asset_type, quantity, purchase_price, purchase_date
                FROM portfolio
                ORDER BY purchase_date DESC
            """)
            
            rows = cursor.fetchall()
            conn.close()
            
            items = [
                {
                    'id': row[0],
                    'symbol': row[1],
                    'asset_type': row[2],
                    'quantity': row[3],
                    'purchase_price': row[4],
                    'purchase_date': row[5]
                }
                for row in rows
            ]
            
            return items
        
        except Exception as e:
            logger.error(f"Error retrieving portfolio: {e}")
            return []
