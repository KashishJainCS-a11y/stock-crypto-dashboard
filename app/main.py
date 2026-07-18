"""Main Streamlit Application"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.data_fetcher import DataFetcher
from src.technical_analysis import TechnicalAnalyzer
from app.config import STOCK_SYMBOLS, CRYPTO_SYMBOLS

# Page config
st.set_page_config(
    page_title="Stock & Crypto Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def main():
    st.title("📈 Live Stock & Crypto Dashboard")
    st.markdown("Real-time market data with technical analysis and trading signals")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        asset_type = st.radio("Select Asset Type", ["Stocks", "Crypto"])
        
        if asset_type == "Stocks":
            symbols = STOCK_SYMBOLS
            selected_symbol = st.selectbox("Select Stock", symbols)
        else:
            symbols = CRYPTO_SYMBOLS
            selected_symbol = st.selectbox("Select Crypto", symbols)
        
        # Date range
        days = st.slider("Days of History", 5, 365, 90)
        
        # Refresh button
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
    
    # Main content
    col1, col2, col3, col4 = st.columns(4)
    
    try:
        # Fetch data
        fetcher = DataFetcher()
        
        if asset_type == "Stocks":
            data = fetcher.fetch_stock_data(selected_symbol, days=days)
        else:
            data = fetcher.fetch_crypto_data(selected_symbol, days=days)
        
        if data is None or data.empty:
            st.error(f"Could not fetch data for {selected_symbol}")
            return
        
        # Calculate metrics
        current_price = data['Close'].iloc[-1]
        prev_price = data['Close'].iloc[0]
        price_change = current_price - prev_price
        price_change_pct = (price_change / prev_price) * 100
        
        # Display metrics
        with col1:
            st.metric(
                "Current Price",
                f"${current_price:.2f}",
                f"{price_change:.2f} ({price_change_pct:.2f}%)",
            )
        
        with col2:
            st.metric(
                "High (24h)",
                f"${data['High'].iloc[-1]:.2f}",
            )
        
        with col3:
            st.metric(
                "Low (24h)",
                f"${data['Low'].iloc[-1]:.2f}",
            )
        
        with col4:
            st.metric(
                "Volume",
                f"{data['Volume'].iloc[-1]:,.0f}",
            )
        
        # Technical Analysis
        st.subheader("📊 Technical Analysis")
        
        analyzer = TechnicalAnalyzer(data)
        data = analyzer.add_sma(data, [20, 50, 200])
        data = analyzer.add_ema(data, [12, 26])
        data = analyzer.add_rsi(data, 14)
        data = analyzer.add_macd(data)
        
        # Price chart with indicators
        st.plotly_chart(
            analyzer.plot_candlestick_with_sma(data, selected_symbol),
            use_container_width=True
        )
        
        # RSI chart
        st.plotly_chart(
            analyzer.plot_rsi(data),
            use_container_width=True
        )
        
        # MACD chart
        st.plotly_chart(
            analyzer.plot_macd(data),
            use_container_width=True
        )
        
        # Data table
        st.subheader("📋 Recent Data")
        display_data = data[['Open', 'High', 'Low', 'Close', 'Volume', 'SMA_20', 'RSI']].tail(10).copy()
        display_data = display_data.round(2)
        st.dataframe(display_data, use_container_width=True)
        
        # Footer
        st.markdown("---")
        st.markdown(
            f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
            f"Data source: yfinance"
        )
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.info("Please try refreshing the data or selecting a different symbol.")

if __name__ == "__main__":
    main()
