"""Technical analysis indicators and visualization"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TechnicalAnalyzer:
    """Technical analysis indicators"""
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize with price data
        
        Args:
            data: DataFrame with OHLCV columns
        """
        self.data = data.copy()
    
    def add_sma(self, data: pd.DataFrame, periods: list) -> pd.DataFrame:
        """
        Add Simple Moving Average
        
        Args:
            data: OHLCV DataFrame
            periods: List of periods (e.g., [20, 50, 200])
        
        Returns:
            DataFrame with SMA columns added
        """
        for period in periods:
            data[f'SMA_{period}'] = data['Close'].rolling(window=period).mean()
        return data
    
    def add_ema(self, data: pd.DataFrame, periods: list) -> pd.DataFrame:
        """
        Add Exponential Moving Average
        
        Args:
            data: OHLCV DataFrame
            periods: List of periods (e.g., [12, 26])
        
        Returns:
            DataFrame with EMA columns added
        """
        for period in periods:
            data[f'EMA_{period}'] = data['Close'].ewm(span=period, adjust=False).mean()
        return data
    
    def add_rsi(self, data: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """
        Add Relative Strength Index
        
        Args:
            data: OHLCV DataFrame
            period: RSI period (default 14)
        
        Returns:
            DataFrame with RSI column added
        """
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        data['RSI'] = 100 - (100 / (1 + rs))
        return data
    
    def add_macd(
        self,
        data: pd.DataFrame,
        fast: int = 12,
        slow: int = 26,
        signal: int = 9
    ) -> pd.DataFrame:
        """
        Add MACD (Moving Average Convergence Divergence)
        
        Args:
            data: OHLCV DataFrame
            fast: Fast EMA period
            slow: Slow EMA period
            signal: Signal line period
        
        Returns:
            DataFrame with MACD columns added
        """
        data['EMA_12'] = data['Close'].ewm(span=fast, adjust=False).mean()
        data['EMA_26'] = data['Close'].ewm(span=slow, adjust=False).mean()
        data['MACD'] = data['EMA_12'] - data['EMA_26']
        data['MACD_Signal'] = data['MACD'].ewm(span=signal, adjust=False).mean()
        data['MACD_Hist'] = data['MACD'] - data['MACD_Signal']
        return data
    
    def add_bollinger_bands(
        self,
        data: pd.DataFrame,
        period: int = 20,
        std_dev: float = 2
    ) -> pd.DataFrame:
        """
        Add Bollinger Bands
        
        Args:
            data: OHLCV DataFrame
            period: MA period
            std_dev: Standard deviation multiplier
        
        Returns:
            DataFrame with Bollinger Bands columns added
        """
        data['BB_MA'] = data['Close'].rolling(window=period).mean()
        data['BB_STD'] = data['Close'].rolling(window=period).std()
        data['BB_Upper'] = data['BB_MA'] + (data['BB_STD'] * std_dev)
        data['BB_Lower'] = data['BB_MA'] - (data['BB_STD'] * std_dev)
        return data
    
    def plot_candlestick_with_sma(
        self,
        data: pd.DataFrame,
        title: str
    ) -> go.Figure:
        """
        Plot candlestick chart with SMA
        
        Args:
            data: OHLCV DataFrame with SMA columns
            title: Chart title
        
        Returns:
            Plotly figure
        """
        fig = go.Figure()
        
        # Candlestick
        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name="Price",
        ))
        
        # SMAs
        if 'SMA_20' in data.columns:
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['SMA_20'],
                mode='lines',
                name='SMA 20',
                line=dict(color='orange', width=1),
            ))
        
        if 'SMA_50' in data.columns:
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['SMA_50'],
                mode='lines',
                name='SMA 50',
                line=dict(color='blue', width=1),
            ))
        
        if 'SMA_200' in data.columns:
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['SMA_200'],
                mode='lines',
                name='SMA 200',
                line=dict(color='red', width=1),
            ))
        
        fig.update_layout(
            title=f"{title} - Price Chart",
            yaxis_title="Price (USD)",
            xaxis_title="Date",
            template="plotly_dark",
            height=500,
            hovermode='x unified',
        )
        
        return fig
    
    def plot_rsi(self, data: pd.DataFrame) -> go.Figure:
        """
        Plot RSI indicator
        
        Args:
            data: DataFrame with RSI column
        
        Returns:
            Plotly figure
        """
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['RSI'],
            mode='lines',
            name='RSI',
            line=dict(color='purple', width=2),
        ))
        
        # Overbought/Oversold levels
        fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought")
        fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold")
        
        fig.update_layout(
            title="RSI (14)",
            yaxis_title="RSI Value",
            xaxis_title="Date",
            template="plotly_dark",
            height=300,
            hovermode='x unified',
            yaxis=dict(range=[0, 100]),
        )
        
        return fig
    
    def plot_macd(self, data: pd.DataFrame) -> go.Figure:
        """
        Plot MACD indicator
        
        Args:
            data: DataFrame with MACD columns
        
        Returns:
            Plotly figure
        """
        fig = make_subplots(specs=[[{"secondary_y": False}]])
        
        # MACD Line
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['MACD'],
            mode='lines',
            name='MACD',
            line=dict(color='blue', width=2),
        ))
        
        # Signal Line
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['MACD_Signal'],
            mode='lines',
            name='Signal',
            line=dict(color='red', width=2),
        ))
        
        # Histogram
        colors = ['green' if x > 0 else 'red' for x in data['MACD_Hist']]
        fig.add_trace(go.Bar(
            x=data.index,
            y=data['MACD_Hist'],
            name='Histogram',
            marker_color=colors,
            opacity=0.3,
        ))
        
        fig.update_layout(
            title="MACD",
            yaxis_title="MACD Value",
            xaxis_title="Date",
            template="plotly_dark",
            height=300,
            hovermode='x unified',
        )
        
        return fig
    
    def get_signals(self, data: pd.DataFrame) -> dict:
        """
        Generate trading signals based on technical indicators
        
        Args:
            data: DataFrame with indicators
        
        Returns:
            Dictionary with trading signals
        """
        signals = {
            'timestamp': data.index[-1],
            'current_price': data['Close'].iloc[-1],
            'signals': []
        }
        
        # RSI signals
        if data['RSI'].iloc[-1] > 70:
            signals['signals'].append(('RSI Overbought', 'SELL'))
        elif data['RSI'].iloc[-1] < 30:
            signals['signals'].append(('RSI Oversold', 'BUY'))
        
        # SMA Crossover
        if 'SMA_20' in data.columns and 'SMA_50' in data.columns:
            if data['SMA_20'].iloc[-1] > data['SMA_50'].iloc[-1]:
                signals['signals'].append(('SMA Bullish', 'BUY'))
            else:
                signals['signals'].append(('SMA Bearish', 'SELL'))
        
        # MACD signals
        if data['MACD'].iloc[-1] > data['MACD_Signal'].iloc[-1]:
            signals['signals'].append(('MACD Bullish', 'BUY'))
        else:
            signals['signals'].append(('MACD Bearish', 'SELL'))
        
        return signals
