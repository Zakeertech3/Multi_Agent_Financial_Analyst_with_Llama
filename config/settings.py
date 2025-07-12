import os
from typing import Dict, List


class AppConfig:
    """Application configuration settings"""
    
    # App Information
    APP_NAME = "Multi-Agent Financial Analyst"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "AI-powered financial analysis using multi-agent systems"
    
    # Page Configuration
    PAGE_TITLE = "Multi-Agent Financial Analyst"
    PAGE_ICON = "📈"
    LAYOUT = "wide"
    
    # API Configuration
    SAMBANOVA_MODEL = "sambanova/Llama-4-Maverick-17B-128E-Instruct"
    DEFAULT_API_BASE_URL = "https://api.sambanova.ai/v1"
    
    # Agent Configuration
    AGENT_VERBOSE = True
    AGENT_TIMEOUT = 300  # 5 minutes
    
    # Data Sources
    DEFAULT_STOCK_PERIOD = "6mo"
    CACHE_TTL = 300  # 5 minutes for data caching
    
    # UI Configuration
    SIDEBAR_STATE = "expanded"
    CHART_HEIGHT = 400
    CHART_TEMPLATE = "plotly_white"


class AgentConfig:
    """Agent-specific configuration"""
    
    # Stock Analyst Agent
    STOCK_ANALYST = {
        "role": "Wall Street Financial Analyst",
        "goal": "Analyze {symbol} stock using real-time data",
        "backstory": "Seasoned analyst focused on data-driven insights with 15+ years of experience in equity research and portfolio management.",
        "verbose": True,
        "max_execution_time": 180
    }
    
    # Report Writer Agent
    REPORT_WRITER = {
        "role": "Financial Report Specialist", 
        "goal": "Create a professional investment report",
        "backstory": "Expert financial writer specializing in institutional-grade investment reports with expertise in technical and fundamental analysis.",
        "verbose": True,
        "max_execution_time": 120
    }


class TaskConfig:
    """Task configuration templates"""
    
    ANALYSIS_TASK_DESCRIPTION = """
    Analyze {symbol} using the stock_data_tool. Your analysis must cover:
    
    1. **Current Price Analysis**
       - Latest price and trading date
       - Daily/weekly price movement
       - Volume analysis
    
    2. **52-Week Performance**
       - 52-week high and low prices
       - Current position within range
       - Performance vs benchmarks
    
    3. **Financial Metrics**
       - Market capitalization 
       - P/E ratio analysis
       - Valuation metrics
    
    4. **Analyst Sentiment**
       - Current analyst rating
       - Recommendation trends
       - Price targets if available
    
    5. **Risk Assessment**
       - Volatility analysis
       - Sector performance
       - Market conditions impact
    
    CRITICAL: You MUST use the stock_data_tool to fetch live, real-time data. 
    Do not rely on training data or assumptions.
    """
    
    REPORT_TASK_DESCRIPTION = """
    Transform the stock analysis into a comprehensive, professional investment report.
    
    **Report Structure:**
    
    # {symbol} Investment Analysis Report
    
    ## 🎯 Executive Summary
    - Key investment thesis (2-3 sentences)
    - Overall recommendation with rationale
    - Target audience considerations
    
    ## 📊 Key Metrics Dashboard
    | Metric | Value | Analysis |
    |--------|-------|----------|
    | Current Price | $X.XX | Commentary |
    | Market Cap | $X.XB | Size classification |
    | P/E Ratio | X.X | Valuation assessment |
    | 52-Week Range | $X.XX - $X.XX | Position analysis |
    
    ## 📈 Performance Analysis
    - **Price Action**: Recent trends and momentum
    - **Volume Patterns**: Trading activity insights
    - **Relative Performance**: vs. sector/market
    
    ## ⚖️ Risk Assessment
    - **Key Risks**: Primary concerns for investors
    - **Risk Level**: Low/Medium/High with justification
    - **Volatility**: Historical and implied volatility
    
    ## 🔮 Investment Outlook
    - **Short-term (1-3 months)**: Near-term catalysts
    - **Medium-term (3-12 months)**: Strategic positioning
    - **Key Factors to Watch**: Events, earnings, etc.
    
    ## 📋 Investment Recommendation
    - **Rating**: Buy/Hold/Sell with confidence level
    - **Target Price Range**: If applicable
    - **Investment Horizon**: Recommended holding period
    - **Portfolio Allocation**: Suggested position sizing
    
    **Formatting Requirements:**
    - Use markdown formatting with headers, tables, and emojis
    - Include bullet points for easy scanning
    - Bold key findings and recommendations
    - Professional yet accessible tone
    - Minimum 500 words, maximum 1500 words
    """


class DataConfig:
    """Data and API configuration"""
    
    # YFinance settings
    YFINANCE_PERIODS = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
    YFINANCE_INTERVALS = ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]
    
    # Required fields for stock analysis
    REQUIRED_STOCK_FIELDS = [
        "longName", "currentPrice", "previousClose", "marketCap", 
        "forwardPE", "fiftyTwoWeekHigh", "fiftyTwoWeekLow", 
        "volume", "averageVolume", "recommendationKey"
    ]
    
    # API rate limits
    API_RATE_LIMITS = {
        "sambanova": {
            "requests_per_minute": 60,
            "tokens_per_minute": 100000
        },
        "yfinance": {
            "requests_per_second": 2,
            "requests_per_hour": 2000
        }
    }


class UIConfig:
    """User interface configuration"""
    
    # Color scheme
    COLORS = {
        "primary": "#1f77b4",
        "secondary": "#ff7f0e", 
        "success": "#2ca02c",
        "warning": "#ff7f0e",
        "danger": "#d62728",
        "background": "#f0f2f6",
        "text": "#262730"
    }
    
    # Custom CSS styles
    CUSTOM_CSS = """
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
    }
    .agent-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #1f77b4;
    }
    .analysis-container {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem 0;
    }
    .status-success {
        color: #2ca02c;
        font-weight: 600;
    }
    .status-error {
        color: #d62728;
        font-weight: 600;
    }
    .status-warning {
        color: #ff7f0e;
        font-weight: 600;
    }
    </style>
    """
    
    # Example stock symbols for quick testing
    EXAMPLE_SYMBOLS = [
        "AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", 
        "META", "NVDA", "NFLX", "ORCL", "CRM"
    ]
    
    # Help text and tooltips
    HELP_TEXT = {
        "stock_symbol": "Enter a valid stock ticker symbol (e.g., AAPL for Apple Inc.)",
        "analysis_period": "Select the time period for historical analysis",
        "agent_verbose": "Enable to see detailed agent reasoning and tool usage",
        "api_key": "Your SambaNova API key for accessing Llama-4 Maverick model"
    }


class ErrorMessages:
    """Standardized error messages"""
    
    API_KEY_MISSING = "❌ SambaNova API key is missing. Please check your .env file."
    INVALID_SYMBOL = "⚠️ Invalid stock symbol. Please enter a valid ticker."
    NETWORK_ERROR = "🌐 Network error. Please check your internet connection."
    API_ERROR = "🔧 API error. Please try again later."
    DATA_ERROR = "📊 Unable to fetch stock data. Symbol may not exist."
    ANALYSIS_ERROR = "🤖 Analysis failed. Please try with a different symbol."
    GENERAL_ERROR = "❌ An unexpected error occurred. Please try again."


class SuccessMessages:
    """Standardized success messages"""
    
    API_KEY_LOADED = "✅ SambaNova API Key loaded successfully"
    ANALYSIS_COMPLETE = "✅ Analysis completed successfully"
    DATA_FETCHED = "📊 Stock data fetched successfully"
    REPORT_GENERATED = "📋 Report generated successfully"
    EXPORT_COMPLETE = "📥 Report exported successfully"


# Global configuration instance
APP_CONFIG = AppConfig()
AGENT_CONFIG = AgentConfig()
TASK_CONFIG = TaskConfig()
DATA_CONFIG = DataConfig()
UI_CONFIG = UIConfig()
ERROR_MESSAGES = ErrorMessages()
SUCCESS_MESSAGES = SuccessMessages()


def get_environment_config() -> Dict:
    """Get environment-specific configuration"""
    return {
        "environment": os.getenv("ENVIRONMENT", "development"),
        "debug": os.getenv("DEBUG", "False").lower() == "true",
        "api_key": os.getenv("SAMBANOVA_API_KEY"),
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
        "cache_enabled": os.getenv("CACHE_ENABLED", "True").lower() == "true"
    }


def validate_config() -> bool:
    """Validate essential configuration"""
    env_config = get_environment_config()
    
    if not env_config["api_key"]:
        return False
    
    # Add more validation as needed
    return True