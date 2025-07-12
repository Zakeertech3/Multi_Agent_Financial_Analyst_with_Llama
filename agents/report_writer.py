from crewai import Task
from datetime import datetime
from config.settings import TASK_CONFIG


class ReportTaskManager:
    """Manages report generation tasks for financial analysis"""
    
    @staticmethod
    def create_investment_report_task(agent, symbol: str, analysis_context: str = None) -> Task:
        """
        Create a comprehensive investment report generation task
        
        Args:
            agent: The report writer agent
            symbol: Stock ticker symbol
            analysis_context: Context from previous analysis (optional)
            
        Returns:
            Task: Configured report generation task
        """
        
        description = f"""
        Transform the stock analysis into a comprehensive, professional investment report for {symbol}.
        
        **Report Structure & Requirements:**
        
        # 📊 {symbol} Investment Analysis Report
        
        ## 🎯 Executive Summary
        **Requirements:**
        - Lead with clear investment thesis (2-3 sentences)
        - State overall recommendation (Strong Buy/Buy/Hold/Sell/Strong Sell)
        - Include confidence level and key risk factors
        - Target audience: Sophisticated investors and portfolio managers
        
        ## 📈 Key Metrics Dashboard
        **Format as professional table:**
        | Metric | Current Value | Analysis | Benchmark |
        |--------|---------------|----------|-----------|
        | Current Price | $X.XX | Price trend assessment | Sector median |
        | Market Cap | $X.XB | Size classification | Industry range |
        | P/E Ratio | X.X | Valuation assessment | Sector P/E |
        | 52-Week Range | $X.XX - $X.XX | Position analysis | % of range |
        | Volume | X.XM | Liquidity assessment | 30-day avg |
        | Analyst Rating | Rating | Consensus view | Rating distribution |
        
        ## 📊 Financial Performance Analysis
        
        ### 🎯 Current Market Position
        - **Price Action**: Recent momentum and trend analysis
        - **Volume Dynamics**: Trading activity and liquidity insights
        - **Market Sentiment**: Investor behavior and positioning
        
        ### 📈 Historical Performance
        - **52-Week Journey**: Key milestones and performance drivers
        - **Volatility Profile**: Risk-adjusted return characteristics
        - **Relative Performance**: vs. sector, market, and peers
        
        ### 💰 Valuation Assessment
        - **Multiple Analysis**: P/E, P/B, EV/EBITDA comparisons
        - **Fair Value Estimation**: Intrinsic value considerations
        - **Valuation Premium/Discount**: Market pricing efficiency
        
        ## ⚖️ Comprehensive Risk Assessment
        
        ### 🎯 Investment Risks (Prioritized)
        1. **Primary Risk**: Most significant concern with mitigation
        2. **Secondary Risks**: Additional factors to monitor
        3. **Tail Risks**: Low probability, high impact scenarios
        
        ### 📊 Risk Metrics
        - **Volatility Level**: Historical and implied volatility
        - **Beta Coefficient**: Market sensitivity analysis
        - **Downside Protection**: Support levels and risk buffers
        
        ### 🛡️ Risk Mitigation Strategies
        - Position sizing recommendations
        - Stop-loss level suggestions
        - Hedging considerations
        - Portfolio diversification impact
        
        ## 🔮 Investment Outlook & Scenarios
        
        ### 📅 Time Horizon Analysis
        **Short-term (1-3 months):**
        - Immediate catalysts and events
        - Technical support/resistance levels
        - Earnings expectations and guidance
        
        **Medium-term (3-12 months):**
        - Strategic initiatives and execution
        - Industry trends and positioning
        - Fundamental value realization
        
        **Long-term (1-3 years):**
        - Structural growth opportunities
        - Competitive moat development
        - Market expansion potential
        
        ### 🎭 Scenario Analysis
        **🐂 Bull Case (30% probability):**
        - Best-case drivers and catalysts
        - Upside price target and timeline
        - Key success metrics to monitor
        
        **🎯 Base Case (50% probability):**
        - Most likely outcome and drivers
        - Fair value target and rationale
        - Expected return and timeframe
        
        **🐻 Bear Case (20% probability):**
        - Downside risks and triggers
        - Downside price target and protection
        - Warning signals to watch
        
        ## 🎯 Investment Recommendation
        
        ### 📋 Final Rating & Rationale
        - **Investment Rating**: [Strong Buy/Buy/Hold/Sell/Strong Sell]
        - **Confidence Level**: [High/Medium/Low] with justification
        - **Price Target**: $X.XX (X-month horizon)
        - **Expected Return**: X.X% (risk-adjusted)
        
        ### 🎪 Portfolio Considerations
        - **Recommended Allocation**: X.X% of equity portfolio
        - **Investment Style Fit**: Growth/Value/Income/Defensive
        - **Risk Budget Impact**: Portfolio volatility contribution
        - **Correlation Benefits**: Diversification value
        
        ### ⏰ Action Items & Monitoring
        - **Entry Strategy**: Optimal timing and price levels
        - **Monitoring Checklist**: Key metrics and events to track
        - **Review Schedule**: Recommended analysis frequency
        - **Exit Criteria**: Conditions for position changes
        
        ## 📊 Appendix: Data Sources & Methodology
        - **Data Currency**: Report timestamp and data freshness
        - **Analysis Framework**: Methodologies and assumptions
        - **Limitations**: Known constraints and considerations
        
        **Formatting Standards:**
        - Use markdown headers, tables, and bullet points
        - Include relevant emojis for visual clarity
        - Bold key findings, ratings, and recommendations
        - Professional yet accessible language
        - Minimum 800 words, maximum 1500 words
        - Include specific numbers, percentages, and timeframes
        - End with clear, actionable recommendations
        
        **Quality Standards:**
        - Investment-grade analysis depth
        - Balanced risk-reward assessment
        - Specific, measurable recommendations
        - Professional institutional format
        """
        
        expected_output = f"""
        Professional investment report for {symbol} containing:
        
        ✅ **Executive Summary** with clear recommendation
        ✅ **Metrics Dashboard** with formatted table
        ✅ **Performance Analysis** (current position, historical, valuation)
        ✅ **Risk Assessment** (prioritized risks, metrics, mitigation)
        ✅ **Investment Outlook** (time horizons, scenarios)
        ✅ **Final Recommendation** (rating, targets, allocation)
        ✅ **Professional formatting** (markdown, tables, emojis)
        
        **Length**: 800-1500 words
        **Format**: Markdown with tables and structure
        **Tone**: Professional, institutional-grade
        **Audience**: Sophisticated investors and portfolio managers
        """
        
        return Task(
            description=description,
            expected_output=expected_output,
            agent=agent
        )
    
    @staticmethod
    def create_executive_summary_task(agent, symbol: str) -> Task:
        """
        Create a concise executive summary task
        
        Args:
            agent: The report writer agent
            symbol: Stock ticker symbol
            
        Returns:
            Task: Configured executive summary task
        """
        
        description = f"""
        Create a concise, high-impact executive summary for {symbol} analysis.
        
        **Executive Summary Requirements:**
        
        📋 **Investment Thesis** (50-75 words)
        - Core investment rationale in 2-3 sentences
        - Key value drivers and competitive advantages
        - Primary reason to invest or avoid
        
        🎯 **Recommendation & Rating**
        - Clear rating: Strong Buy/Buy/Hold/Sell/Strong Sell
        - Confidence level: High/Medium/Low
        - Target price with timeframe
        - Expected total return percentage
        
        📊 **Key Metrics Snapshot**
        - Current price and daily change
        - Market cap and valuation (P/E)
        - 52-week performance summary
        - Volume and liquidity assessment
        
        ⚠️ **Primary Risks** (3-4 bullet points)
        - Most significant investment risks
        - Probability and impact assessment
        - Mitigation strategies available
        
        ⏰ **Time-Sensitive Factors**
        - Upcoming catalysts or events
        - Seasonal or cyclical considerations
        - Optimal entry timing suggestions
        
        🎪 **Portfolio Fit**
        - Recommended allocation percentage
        - Investment style classification
        - Risk-return profile summary
        
        **Format Requirements:**
        - Maximum 300 words total
        - Bullet points and clear structure
        - Bold key recommendations
        - Professional, decisive tone
        - Actionable insights only
        """
        
        expected_output = f"""
        Executive summary for {symbol} including:
        1. Investment thesis (50-75 words)
        2. Clear recommendation with rating
        3. Key metrics snapshot
        4. Primary risk factors
        5. Time-sensitive considerations
        6. Portfolio allocation guidance
        
        Format: Concise, professional, maximum 300 words
        """
        
        return Task(
            description=description,
            expected_output=expected_output,
            agent=agent
        )
    
    @staticmethod
    def create_technical_report_task(agent, symbol: str) -> Task:
        """
        Create a technical analysis focused report task
        
        Args:
            agent: The report writer agent
            symbol: Stock ticker symbol
            
        Returns:
            Task: Configured technical report task
        """
        
        description = f"""
        Create a technical analysis report for {symbol} focused on price action and trading signals.
        
        **Technical Report Structure:**
        
        # 📈 {symbol} Technical Analysis Report
        
        ## 🎯 Technical Summary
        - **Overall Trend**: Bullish/Bearish/Neutral with strength
        - **Momentum**: Accelerating/Decelerating/Stable
        - **Signal Quality**: Strong/Moderate/Weak
        - **Time Horizon**: Optimal trading timeframe
        
        ## 📊 Price Action Analysis
        
        ### 🎪 Trend Analysis
        - **Primary Trend**: Direction and strength
        - **Secondary Trend**: Correction or continuation
        - **Trend Duration**: How long current trend has persisted
        - **Trend Reliability**: Quality of trend signals
        
        ### 🎯 Support & Resistance
        - **Key Support Levels**: Price levels with historical significance
        - **Resistance Zones**: Overhead supply areas
        - **Breakout Levels**: Critical price points to watch
        - **Risk Management**: Stop-loss placement guidance
        
        ## 📈 Technical Indicators
        
        ### 📊 Moving Averages
        - **20-day MA**: Short-term trend indication
        - **50-day MA**: Medium-term trend assessment
        - **MA Crossovers**: Signal strength and timing
        - **Price-MA Relationship**: Current positioning
        
        ### ⚡ Momentum Indicators
        - **RSI Reading**: Overbought/oversold conditions
        - **MACD Status**: Bullish/bearish divergences
        - **Volume Confirmation**: Price-volume relationship
        - **Momentum Quality**: Strength and sustainability
        
        ## 🎯 Trading Signals & Recommendations
        
        ### 📅 Short-term (1-4 weeks)
        - **Entry Signals**: Optimal buy/sell points
        - **Price Targets**: Realistic short-term objectives
        - **Stop Losses**: Risk management levels
        - **Position Sizing**: Recommended allocation
        
        ### 📈 Medium-term (1-6 months)
        - **Swing Trade Setup**: Position trade opportunities
        - **Target Zones**: Medium-term price objectives
        - **Trend Continuation**: Probability assessment
        - **Risk-Reward Ratio**: Trade quality metrics
        
        ## ⚠️ Risk Considerations
        - **Volatility Assessment**: Price movement expectations
        - **Market Correlation**: Broader market dependency
        - **Event Risk**: Earnings, announcements impact
        - **Technical Failure**: What invalidates the setup
        
        **Formatting Requirements:**
        - Clear section headers with emojis
        - Specific price levels and percentages
        - Visual descriptions of chart patterns
        - Actionable trading recommendations
        - Professional technical terminology
        - 400-600 words focused content
        """
        
        expected_output = f"""
        Technical analysis report for {symbol} with:
        1. Technical summary and trend assessment
        2. Support/resistance level identification
        3. Technical indicator analysis
        4. Trading signals and recommendations
        5. Risk management guidelines
        6. Time-horizon specific strategies
        
        Format: Technical focus, 400-600 words, actionable insights
        """
        
        return Task(
            description=description,
            expected_output=expected_output,
            agent=agent
        )
    
    @staticmethod
    def create_risk_report_task(agent, symbol: str) -> Task:
        """
        Create a risk-focused analysis report task
        
        Args:
            agent: The report writer agent
            symbol: Stock ticker symbol
            
        Returns:
            Task: Configured risk analysis report task
        """
        
        description = f"""
        Create a comprehensive risk analysis report for {symbol} investment.
        
        **Risk Report Framework:**
        
        # ⚠️ {symbol} Risk Analysis Report
        
        ## 🎯 Risk Profile Summary
        - **Overall Risk Level**: Low/Medium/High with justification
        - **Risk-Adjusted Return**: Expected Sharpe ratio estimate
        - **Volatility Classification**: Stable/Moderate/High volatility
        - **Investor Suitability**: Conservative/Moderate/Aggressive
        
        ## 📊 Quantitative Risk Metrics
        
        ### 📈 Historical Volatility
        - **30-day Volatility**: Recent price movement patterns
        - **1-year Volatility**: Longer-term risk assessment
        - **Volatility Percentile**: Relative to historical range
        - **Volatility Trends**: Increasing/decreasing/stable
        
        ### 🎪 Market Risk Factors
        - **Beta Coefficient**: Market sensitivity measurement
        - **Correlation Analysis**: Relationship with major indices
        - **Sector Beta**: Industry-specific risk exposure
        - **Systematic Risk**: Undiversifiable risk components
        
        ## ⚠️ Specific Risk Categories
        
        ### 🏢 Company-Specific Risks
        1. **Business Model Risk**: Revenue sustainability concerns
        2. **Financial Risk**: Leverage, liquidity, credit issues
        3. **Operational Risk**: Management, execution challenges
        4. **Competitive Risk**: Market share, pricing pressure
        
        ### 🌍 External Risk Factors
        1. **Sector Risk**: Industry-specific challenges
        2. **Economic Risk**: Cycle sensitivity, macro factors
        3. **Regulatory Risk**: Policy changes, compliance
        4. **Geopolitical Risk**: International exposure, trade
        
        ## 🛡️ Risk Mitigation Strategies
        
        ### 🎯 Portfolio Management
        - **Position Sizing**: Recommended maximum allocation
        - **Diversification**: Correlation with other holdings
        - **Hedging Options**: Available risk reduction tools
        - **Rebalancing**: Frequency and triggers
        
        ### ⏰ Monitoring & Controls
        - **Stop-Loss Levels**: Automatic risk controls
        - **Review Triggers**: Events requiring reassessment
        - **Exit Criteria**: Conditions for position closure
        - **Risk Budget**: Impact on overall portfolio risk
        
        ## 📊 Scenario Analysis
        
        ### 🐻 Downside Scenarios (Stress Testing)
        - **Market Crash**: -20% market decline impact
        - **Sector Rotation**: Industry out of favor
        - **Company-Specific**: Fundamental deterioration
        - **Maximum Drawdown**: Worst-case loss estimation
        
        ### 🛡️ Tail Risk Assessment
        - **Black Swan Events**: Low probability, high impact
        - **Liquidity Crisis**: Trading disruption scenarios
        - **Systematic Failures**: Market structure breakdown
        - **Recovery Timeline**: Expected rebound duration
        
        ## 🎯 Risk-Adjusted Recommendations
        
        ### 📋 Investment Guidelines
        - **Risk Tolerance Match**: Suitable investor types
        - **Allocation Limits**: Maximum position size
        - **Hold Period**: Recommended investment horizon
        - **Risk Monitoring**: Key metrics to track
        
        ### ⚡ Action Items
        - **Immediate Actions**: Risk control implementation
        - **Ongoing Monitoring**: Regular risk assessments
        - **Trigger Events**: When to reassess or exit
        - **Portfolio Integration**: How to fit with other holdings
        
        **Quality Standards:**
        - Quantitative risk metrics where possible
        - Specific risk scenarios and probabilities
        - Actionable risk management recommendations
        - Professional risk management terminology
        - 500-700 words comprehensive coverage
        """
        
        expected_output = f"""
        Risk analysis report for {symbol} including:
        1. Risk profile summary and classification
        2. Quantitative risk metrics and volatility
        3. Specific risk category analysis
        4. Risk mitigation strategies
        5. Scenario analysis and stress testing
        6. Risk-adjusted investment recommendations
        
        Format: Risk-focused, 500-700 words, actionable guidance
        """
        
        return Task(
            description=description,
            expected_output=expected_output,
            agent=agent
        )


# Report utility functions
def get_available_report_types() -> list:
    """Return list of available report types"""
    return [
        "investment_report",
        "executive_summary",
        "technical_report", 
        "risk_report"
    ]


def create_report_task_by_type(report_type: str, agent, symbol: str, **kwargs) -> Task:
    """
    Factory function to create report tasks by type
    
    Args:
        report_type: Type of report to create
        agent: Report writer agent
        symbol: Stock symbol to analyze
        **kwargs: Additional parameters for specific report types
        
    Returns:
        Task: Configured report task instance
    """
    
    task_manager = ReportTaskManager()
    
    if report_type == "investment_report":
        return task_manager.create_investment_report_task(
            agent, symbol, kwargs.get('analysis_context')
        )
    elif report_type == "executive_summary":
        return task_manager.create_executive_summary_task(agent, symbol)
    elif report_type == "technical_report":
        return task_manager.create_technical_report_task(agent, symbol)
    elif report_type == "risk_report":
        return task_manager.create_risk_report_task(agent, symbol)
    else:
        raise ValueError(f"Unknown report type: {report_type}")


def validate_report_inputs(symbol: str, report_type: str) -> bool:
    """
    Validate inputs for report task creation
    
    Args:
        symbol: Stock ticker symbol
        report_type: Type of report
        
    Returns:
        bool: True if inputs are valid
    """
    
    if not symbol or len(symbol) > 10:
        return False
    
    if report_type not in get_available_report_types():
        return False
    
    return True


def get_report_metadata(symbol: str, report_type: str) -> dict:
    """
    Get metadata for report generation
    
    Args:
        symbol: Stock ticker symbol
        report_type: Type of report
        
    Returns:
        dict: Report metadata
    """
    
    return {
        'symbol': symbol,
        'report_type': report_type,
        'generated_at': datetime.now().isoformat(),
        'format': 'markdown',
        'version': '1.0',
        'estimated_length': {
            'investment_report': '800-1500 words',
            'executive_summary': '200-300 words',
            'technical_report': '400-600 words',
            'risk_report': '500-700 words'
        }.get(report_type, '400-800 words')
    }