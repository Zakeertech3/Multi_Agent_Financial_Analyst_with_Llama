from crewai import Task
from config.settings import TASK_CONFIG


class AnalysisTaskManager:
    """Manages analysis tasks for financial agents"""
    
    @staticmethod
    def create_stock_analysis_task(agent, symbol: str) -> Task:
        """
        Create a comprehensive stock analysis task
        
        Args:
            agent: The stock analyst agent
            symbol: Stock ticker symbol to analyze
            
        Returns:
            Task: Configured analysis task
        """
        
        description = f"""
        Conduct a comprehensive financial analysis of {symbol} using the stock_data_tool.
        
        **MANDATORY REQUIREMENTS:**
        1. **MUST** use the stock_data_tool to fetch real-time data - no assumptions or outdated information
        2. **MUST** analyze ALL key financial metrics available
        3. **MUST** provide data-driven insights, not generic commentary
        
        **Analysis Framework:**
        
        🎯 **Current Market Position**
        - Current stock price and latest trading date
        - Daily price movement (absolute and percentage)
        - Current trading volume vs average volume
        - Intraday trading range analysis
        
        📊 **52-Week Performance Analysis**
        - 52-week high and low prices with dates
        - Current price position within 52-week range (percentage)
        - Distance from 52-week high/low (dollar amount and percentage)
        - Performance momentum analysis
        
        💰 **Valuation Metrics**
        - Market capitalization analysis and company size classification
        - Forward P/E ratio assessment and sector comparison
        - Price-to-book ratio if available
        - Enterprise value metrics if accessible
        - Valuation premium/discount analysis
        
        📈 **Technical Indicators**
        - Price trend analysis (bullish/bearish/neutral)
        - Support and resistance levels identification
        - Volume trend analysis
        - Momentum indicators assessment
        
        🏆 **Analyst Sentiment & Ratings**
        - Current analyst recommendation (Buy/Hold/Sell)
        - Analyst rating distribution if available
        - Price target analysis if accessible
        - Recent rating changes or updates
        
        ⚠️ **Risk Assessment**
        - Stock volatility analysis
        - Sector-specific risks
        - Market condition impact assessment
        - Liquidity analysis based on volume
        
        🌍 **Market Context**
        - Sector performance comparison
        - Market cap peer analysis
        - Industry trends impact
        - Macroeconomic factors relevance
        
        **Output Requirements:**
        - Use bullet points and clear structure
        - Include specific numbers and percentages
        - Highlight key findings in **bold**
        - Provide context for all metrics
        - End with 3-5 key takeaways
        - Minimum 300 words of substantive analysis
        
        **Data Source:** All analysis MUST be based on live data from stock_data_tool.
        """
        
        expected_output = f"""
        Comprehensive analysis report for {symbol} including:
        
        1. **Executive Summary** (2-3 key sentences)
        2. **Current Market Data** (price, volume, movement)
        3. **Performance Metrics** (52-week range, trends)
        4. **Valuation Analysis** (P/E, market cap, classification)
        5. **Technical Assessment** (momentum, trends)
        6. **Risk Evaluation** (volatility, sector risks)
        7. **Key Takeaways** (3-5 bullet points)
        
        Format: Structured text with clear sections, bullet points, and bold highlights.
        Length: 300-500 words of substantive analysis.
        Data: 100% based on real-time stock_data_tool results.
        """
        
        return Task(
            description=description,
            expected_output=expected_output,
            agent=agent,
            tools=agent.tools if hasattr(agent, 'tools') else []
        )
    
    @staticmethod
    def create_sector_comparison_task(agent, symbol: str, sector_symbols: list = None) -> Task:
        """
        Create a sector comparison analysis task
        
        Args:
            agent: The stock analyst agent
            symbol: Primary stock symbol
            sector_symbols: List of sector peer symbols for comparison
            
        Returns:
            Task: Configured sector comparison task
        """
        
        if sector_symbols is None:
            sector_symbols = []
        
        description = f"""
        Perform a sector-relative analysis of {symbol} against its peers.
        
        **Primary Analysis:**
        1. Use stock_data_tool to analyze {symbol}
        2. Identify the company's sector and industry
        3. Compare key metrics against sector averages
        
        **Comparative Framework:**
        - Valuation multiples comparison (P/E ratios)
        - Market cap positioning within sector
        - Performance vs sector ETF or index
        - Relative strength analysis
        
        **Sector Context:**
        - Industry trends and outlook
        - Regulatory environment impact
        - Competitive positioning
        - Market share considerations
        
        **Risk-Adjusted Analysis:**
        - Beta comparison to sector
        - Volatility vs peers
        - Correlation analysis
        - Diversification benefits
        """
        
        expected_output = f"""
        Sector comparison report for {symbol}:
        1. Sector identification and classification
        2. Peer group comparison metrics
        3. Relative valuation assessment
        4. Competitive positioning analysis
        5. Sector-specific risk factors
        6. Investment recommendation within sector context
        """
        
        return Task(
            description=description,
            expected_output=expected_output,
            agent=agent
        )
    
    @staticmethod
    def create_technical_analysis_task(agent, symbol: str, period: str = "6mo") -> Task:
        """
        Create a technical analysis focused task
        
        Args:
            agent: The stock analyst agent
            symbol: Stock ticker symbol
            period: Analysis period for technical indicators
            
        Returns:
            Task: Configured technical analysis task
        """
        
        description = f"""
        Conduct technical analysis of {symbol} using {period} historical data.
        
        **Technical Analysis Requirements:**
        
        📈 **Price Action Analysis**
        - Trend identification (uptrend/downtrend/sideways)
        - Support and resistance level identification
        - Key price breakouts or breakdowns
        - Chart pattern recognition
        
        📊 **Volume Analysis**
        - Volume trend confirmation
        - Volume spikes and their significance
        - Volume-price relationship analysis
        - Accumulation/distribution patterns
        
        🎯 **Momentum Indicators**
        - Moving average analysis (20-day, 50-day trends)
        - RSI levels and overbought/oversold conditions
        - MACD signal analysis if calculable
        - Price momentum assessment
        
        ⚡ **Entry/Exit Signals**
        - Short-term trading signals
        - Medium-term investment signals
        - Stop-loss level recommendations
        - Target price projections
        
        🔄 **Risk Management**
        - Volatility assessment
        - Maximum drawdown analysis
        - Risk-reward ratio evaluation
        - Position sizing recommendations
        
        Use stock_data_tool for all price and volume data.
        """
        
        expected_output = f"""
        Technical analysis report for {symbol}:
        1. Overall trend assessment
        2. Key support/resistance levels
        3. Volume analysis insights
        4. Momentum indicator readings
        5. Trading signals and recommendations
        6. Risk management guidelines
        7. Technical price targets
        """
        
        return Task(
            description=description,
            expected_output=expected_output,
            agent=agent
        )
    
    @staticmethod
    def create_risk_assessment_task(agent, symbol: str) -> Task:
        """
        Create a comprehensive risk assessment task
        
        Args:
            agent: The stock analyst agent
            symbol: Stock ticker symbol
            
        Returns:
            Task: Configured risk assessment task
        """
        
        description = f"""
        Perform comprehensive risk assessment for {symbol} investment.
        
        **Risk Analysis Framework:**
        
        📊 **Quantitative Risk Metrics**
        - Historical volatility analysis
        - Beta coefficient assessment
        - Maximum drawdown calculation
        - Value at Risk (VaR) estimation if possible
        
        🏢 **Company-Specific Risks**
        - Business model risks
        - Financial health indicators
        - Management quality assessment
        - Competitive position vulnerabilities
        
        🌍 **Market & Sector Risks**
        - Sector-specific challenges
        - Market correlation risks
        - Economic cycle sensitivity
        - Regulatory and policy risks
        
        💰 **Financial Risks**
        - Liquidity risk assessment
        - Credit risk evaluation
        - Currency exposure if applicable
        - Interest rate sensitivity
        
        ⚠️ **Investment Risks**
        - Concentration risk
        - Timing risk factors
        - Event risk (earnings, announcements)
        - Black swan event vulnerability
        
        Use stock_data_tool for volatility and correlation data.
        """
        
        expected_output = f"""
        Risk assessment report for {symbol}:
        1. Risk level classification (Low/Medium/High)
        2. Key risk factors identification
        3. Quantitative risk metrics
        4. Risk mitigation strategies
        5. Scenario analysis (bull/base/bear cases)
        6. Investment suitability assessment
        7. Risk-adjusted return expectations
        """
        
        return Task(
            description=description,
            expected_output=expected_output,
            agent=agent
        )


# Utility functions for task management
def get_available_task_types() -> list:
    """Return list of available task types"""
    return [
        "stock_analysis",
        "sector_comparison", 
        "technical_analysis",
        "risk_assessment"
    ]


def create_task_by_type(task_type: str, agent, symbol: str, **kwargs) -> Task:
    """
    Factory function to create tasks by type
    
    Args:
        task_type: Type of task to create
        agent: Agent to assign the task to
        symbol: Stock symbol to analyze
        **kwargs: Additional parameters for specific task types
        
    Returns:
        Task: Configured task instance
    """
    
    task_manager = AnalysisTaskManager()
    
    if task_type == "stock_analysis":
        return task_manager.create_stock_analysis_task(agent, symbol)
    elif task_type == "sector_comparison":
        return task_manager.create_sector_comparison_task(
            agent, symbol, kwargs.get('sector_symbols', [])
        )
    elif task_type == "technical_analysis":
        return task_manager.create_technical_analysis_task(
            agent, symbol, kwargs.get('period', '6mo')
        )
    elif task_type == "risk_assessment":
        return task_manager.create_risk_assessment_task(agent, symbol)
    else:
        raise ValueError(f"Unknown task type: {task_type}")


def validate_task_inputs(symbol: str, task_type: str) -> bool:
    """
    Validate inputs for task creation
    
    Args:
        symbol: Stock ticker symbol
        task_type: Type of task
        
    Returns:
        bool: True if inputs are valid
    """
    
    if not symbol or len(symbol) > 10:
        return False
    
    if task_type not in get_available_task_types():
        return False
    
    return True