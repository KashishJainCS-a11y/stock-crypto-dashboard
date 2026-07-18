"""Utility functions"""
import logging
from datetime import datetime, timedelta
import pandas as pd

logger = logging.getLogger(__name__)

def format_price(price: float) -> str:
    """Format price with currency symbol"""
    return f"${price:,.2f}"

def format_change(change: float, change_pct: float) -> str:
    """Format price change"""
    symbol = "▲" if change >= 0 else "▼"
    color = "green" if change >= 0 else "red"
    return f"{symbol} {change:,.2f} ({change_pct:.2f}%)"

def calculate_portfolio_value(
    portfolio_items: list,
    current_prices: dict
) -> dict:
    """
    Calculate total portfolio value
    
    Args:
        portfolio_items: List of portfolio items
        current_prices: Dict of current prices {symbol: price}
    
    Returns:
        Dict with portfolio metrics
    """
    total_value = 0
    total_cost = 0
    positions = []
    
    for item in portfolio_items:
        symbol = item['symbol']
        quantity = item['quantity']
        purchase_price = item['purchase_price']
        
        cost = quantity * purchase_price
        total_cost += cost
        
        if symbol in current_prices:
            current_price = current_prices[symbol]
            value = quantity * current_price
            total_value += value
            
            gain = value - cost
            gain_pct = (gain / cost) * 100 if cost > 0 else 0
            
            positions.append({
                'symbol': symbol,
                'quantity': quantity,
                'cost': cost,
                'value': value,
                'gain': gain,
                'gain_pct': gain_pct
            })
    
    total_gain = total_value - total_cost
    total_gain_pct = (total_gain / total_cost) * 100 if total_cost > 0 else 0
    
    return {
        'total_value': total_value,
        'total_cost': total_cost,
        'total_gain': total_gain,
        'total_gain_pct': total_gain_pct,
        'positions': positions
    }

def get_date_range(days: int) -> tuple:
    """
    Get date range for data fetching
    
    Args:
        days: Number of days back from today
    
    Returns:
        Tuple of (start_date, end_date)
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return (start_date, end_date)

def validate_symbol(symbol: str) -> bool:
    """
    Validate symbol format
    
    Args:
        symbol: Stock or crypto symbol
    
    Returns:
        True if valid, False otherwise
    """
    if not symbol or not isinstance(symbol, str):
        return False
    
    symbol = symbol.strip().upper()
    
    # Basic validation: 1-10 characters, alphanumeric
    if len(symbol) > 10 or not symbol.isalnum():
        return False
    
    return True
