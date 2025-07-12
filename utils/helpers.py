import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import re
from datetime import datetime, timedelta
import streamlit as st


def validate_stock_symbol(symbol: str) -> bool:
    """
    Validate if a stock symbol exists and is tradeable
    """
    if not symbol or len(symbol) > 10:
        return False
    
    # Basic format validation
    if not re.match(r'^[A-Z]{1,5}$', symbol):
        return False
    
    try:
        # Quick check if ticker exists
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return 'regularMarketPrice' in info or 'currentPrice' in info
    except:
        return False


def format_response(response: str) -> str:
    """
    Format the AI agent response for better display
    """
    # Clean up any formatting issues
    response = response.strip()
    
    # Ensure proper markdown formatting
    if not response.startswith('#'):
        response = f"# Financial Analysis Report\n\n{response}"
    
    # Add timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    response += f"\n\n---\n*Report generated on {timestamp}*"
    
    return response


def create_stock_chart(symbol: str, period: str = "6mo") -> go.Figure:
    """
    Create an interactive stock price chart using Plotly
    """
    try:
        # Fetch stock data
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period)
        
        if data.empty:
            raise ValueError("No data available")
        
        # Create candlestick chart
        fig = go.Figure(data=go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name=symbol
        ))
        
        # Add volume subplot
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Volume'],
            mode='lines',
            name='Volume',
            yaxis='y2',
            line=dict(color='rgba(0,100,80,0.5)')
        ))
        
        # Update layout
        fig.update_layout(
            title=f"{symbol} Stock Price ({period})",
            yaxis_title="Price ($)",
            yaxis2=dict(
                title="Volume",
                overlaying='y',
                side='right',
                showgrid=False
            ),
            xaxis_title="Date",
            template="plotly_white",
            height=400,
            showlegend=True,
            hovermode='x unified'
        )
        
        # Remove range slider for cleaner look
        fig.update_layout(xaxis_rangeslider_visible=False)
        
        return fig
        
    except Exception as e:
        # Return empty figure with error message
        fig = go.Figure()
        fig.add_annotation(
            text=f"Unable to load chart: {str(e)}",
            x=0.5, y=0.5,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=16)
        )
        fig.update_layout(
            title=f"Chart Error - {symbol}",
            height=400
        )
        return fig


def format_currency(value: float) -> str:
    """
    Format currency values for display
    """
    if value is None:
        return "N/A"
    
    if value >= 1e12:
        return f"${value/1e12:.2f}T"
    elif value >= 1e9:
        return f"${value/1e9:.2f}B"
    elif value >= 1e6:
        return f"${value/1e6:.2f}M"
    elif value >= 1e3:
        return f"${value/1e3:.2f}K"
    else:
        return f"${value:.2f}"


def format_percentage(value: float) -> str:
    """
    Format percentage values for display
    """
    if value is None:
        return "N/A"
    return f"{value:.2f}%"


def get_stock_metrics(symbol: str) -> dict:
    """
    Get key stock metrics for quick display
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        hist = ticker.history(period="1d")
        
        current_price = info.get('currentPrice') or hist['Close'].iloc[-1]
        previous_close = info.get('previousClose') or hist['Close'].iloc[-2] if len(hist) > 1 else current_price
        
        change = current_price - previous_close
        change_percent = (change / previous_close) * 100 if previous_close else 0
        
        return {
            'symbol': symbol,
            'company_name': info.get('longName', symbol),
            'current_price': current_price,
            'change': change,
            'change_percent': change_percent,
            'volume': info.get('volume', 0),
            'market_cap': info.get('marketCap', 0),
            'pe_ratio': info.get('forwardPE'),
            'dividend_yield': info.get('dividendYield'),
            '52_week_high': info.get('fiftyTwoWeekHigh'),
            '52_week_low': info.get('fiftyTwoWeekLow'),
            'avg_volume': info.get('averageVolume'),
            'beta': info.get('beta'),
            'eps': info.get('forwardEps'),
            'book_value': info.get('bookValue'),
            'price_to_book': info.get('priceToBook'),
            'sector': info.get('sector'),
            'industry': info.get('industry')
        }
        
    except Exception as e:
        return {
            'error': f"Unable to fetch metrics: {str(e)}",
            'symbol': symbol
        }


def create_metrics_table(metrics: dict) -> pd.DataFrame:
    """
    Create a formatted metrics table for display
    """
    if 'error' in metrics:
        return pd.DataFrame({'Error': [metrics['error']]})
    
    table_data = {
        'Metric': [
            'Current Price',
            'Daily Change',
            'Daily Change %',
            'Market Cap',
            'P/E Ratio',
            '52-Week High',
            '52-Week Low',
            'Volume',
            'Average Volume',
            'Beta',
            'Dividend Yield',
            'EPS (Forward)',
            'Book Value',
            'Price to Book',
            'Sector',
            'Industry'
        ],
        'Value': [
            format_currency(metrics.get('current_price')),
            format_currency(metrics.get('change')),
            format_percentage(metrics.get('change_percent')),
            format_currency(metrics.get('market_cap')),
            f"{metrics.get('pe_ratio', 'N/A')}",
            format_currency(metrics.get('52_week_high')),
            format_currency(metrics.get('52_week_low')),
            f"{metrics.get('volume', 0):,}",
            f"{metrics.get('avg_volume', 0):,}",
            f"{metrics.get('beta', 'N/A')}",
            format_percentage(metrics.get('dividend_yield', 0) * 100) if metrics.get('dividend_yield') else 'N/A',
            format_currency(metrics.get('eps')),
            format_currency(metrics.get('book_value')),
            f"{metrics.get('price_to_book', 'N/A')}",
            metrics.get('sector', 'N/A'),
            metrics.get('industry', 'N/A')
        ]
    }
    
    return pd.DataFrame(table_data)


def export_analysis_to_pdf(content: str, filename: str):
    """
    Convert markdown content to PDF (placeholder for future implementation)
    """
    # This would require additional libraries like reportlab or weasyprint
    # For now, we'll just return the markdown content
    return content


@st.cache_data(ttl=300)  # Cache for 5 minutes
def cached_stock_data(symbol: str, period: str = "1mo"):
    """
    Cached version of stock data fetching to improve performance
    """
    try:
        ticker = yf.Ticker(symbol)
        return ticker.history(period=period)
    except:
        return pd.DataFrame()


def calculate_technical_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate basic technical indicators
    """
    if data.empty:
        return data
    
    # Simple Moving Averages
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    
    # RSI calculation
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    
    return data