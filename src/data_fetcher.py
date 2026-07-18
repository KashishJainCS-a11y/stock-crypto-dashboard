"""Data fetching from APIs"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataFetcher:
    """Fetch stock and crypto data from various sources"""
    
    def __init__(self):
        self.cache = {}
    
    def fetch_stock_data(
        self,
        symbol: str,
        days: int = 90,
        interval: str = "1d"
    ) -> Optional[pd.DataFrame]:
        """
        Fetch stock data using yfinance
        
        Args:
            symbol: Stock ticker (e.g., 'AAPL')
            days: Number of days of historical data
            interval: Data interval ('1d', '1h', '15m', '5m', '1m')
        
        Returns:
            DataFrame with OHLCV data or None if error
        """
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Fetch data
            data = yf.download(
                symbol,
                start=start_date,
                end=end_date,
                interval=interval,
                progress=False,
            )
            
            if data.empty:
                logger.warning(f"No data found for {symbol}")
                return None
            
            logger.info(f"Fetched {len(data)} rows for {symbol}")
            return data
        
        except Exception as e:
            logger.error(f"Error fetching stock data for {symbol}: {e}")
            return None
    
    def fetch_crypto_data(
        self,
        symbol: str,
        days: int = 90,
        interval: str = "1d"
    ) -> Optional[pd.DataFrame]:
        """
        Fetch cryptocurrency data
        
        Args:
            symbol: Crypto ticker (e.g., 'BTC', 'ETH')
            days: Number of days of historical data
            interval: Data interval
        
        Returns:
            DataFrame with OHLCV data or None if error
        """
        try:
            # Convert symbol to yfinance format (e.g., BTC -> BTC-USD)
            yf_symbol = f"{symbol}-USD"
            
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Fetch data
            data = yf.download(
                yf_symbol,
                start=start_date,
                end=end_date,
                interval=interval,
                progress=False,
            )
            
            if data.empty:
                logger.warning(f"No data found for {symbol}")
                return None
            
            logger.info(f"Fetched {len(data)} rows for {symbol}")
            return data
        
        except Exception as e:
            logger.error(f"Error fetching crypto data for {symbol}: {e}")
            return None
    
    def fetch_multiple_stocks(
        self,
        symbols: list,
        days: int = 90
    ) -> pd.DataFrame:
        """
        Fetch data for multiple stocks and combine
        
        Args:
            symbols: List of stock tickers
            days: Number of days of historical data
        
        Returns:
            DataFrame with Close prices for all symbols
        """
        data = {}
        for symbol in symbols:
            df = self.fetch_stock_data(symbol, days=days)
            if df is not None:
                data[symbol] = df['Close']
        
        if not data:
            return pd.DataFrame()
        
        combined = pd.DataFrame(data)
        return combined
    
    def get_current_price(self, symbol: str, is_crypto: bool = False) -> Optional[float]:
        """
        Get the current price of an asset
        
        Args:
            symbol: Asset ticker
            is_crypto: Whether it's a cryptocurrency
        
        Returns:
            Current price or None if error
        """
        try:
            if is_crypto:
                symbol = f"{symbol}-USD"
            
            data = yf.download(symbol, period="1d", progress=False)
            if data.empty:
                return None
            
            return float(data['Close'].iloc[-1])
        
        except Exception as e:
            logger.error(f"Error fetching current price for {symbol}: {e}")
            return None
