import streamlit as st
import os
from dotenv import load_dotenv
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime
import time

# Load environment variables
load_dotenv()

# Import your custom modules
from crew.financial_crew import run_financial_analysis
from utils.helpers import format_response, create_stock_chart, validate_stock_symbol
from config.settings import APP_CONFIG

# Page configuration
st.set_page_config(
    page_title="Multi-Agent Financial Analyst",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.agent-card {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
}
.analysis-container {
    background-color: #ffffff;
    padding: 2rem;
    border-radius: 15px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.metric-card {
    background-color: #e8f4fd;
    padding: 1rem;
    border-radius: 8px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🤖 Multi-Agent Financial Analyst</h1>', unsafe_allow_html=True)
    st.markdown("### Powered by Llama-4 Maverick & SambaNova AI")
    
    # Sidebar
    with st.sidebar:
        st.header("🎯 Analysis Settings")
        
        # API Key check
        api_key = os.getenv("SAMBANOVA_API_KEY")
        if api_key:
            st.success("✅ SambaNova API Key Loaded")
        else:
            st.error("❌ SambaNova API Key Missing")
            st.stop()
        
        # Stock symbol input
        stock_symbol = st.text_input(
            "Enter Stock Symbol",
            value="AAPL",
            help="Enter a valid stock ticker (e.g., AAPL, GOOGL, MSFT)"
        ).upper().strip()
        
        # Validate symbol
        if stock_symbol and not validate_stock_symbol(stock_symbol):
            st.warning("⚠️ Please enter a valid stock symbol")
            return
        
        # Analysis button
        analyze_button = st.button("🚀 Start Analysis", type="primary")
        
        # Agent info
        st.markdown("---")
        st.subheader("🤖 Agents Working")
        st.markdown("""
        **🔍 Stock Analyst Agent**
        - Fetches real-time data
        - Analyzes key metrics
        - Provides insights
        
        **📝 Report Writer Agent**
        - Creates professional reports
        - Formats analysis
        - Generates recommendations
        """)

    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if analyze_button and stock_symbol:
            st.markdown('<div class="analysis-container">', unsafe_allow_html=True)
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step 1: Initialize agents
            status_text.text("🤖 Initializing AI agents...")
            progress_bar.progress(20)
            time.sleep(1)
            
            # Step 2: Fetch data
            status_text.text("📊 Fetching real-time stock data...")
            progress_bar.progress(40)
            time.sleep(1)
            
            # Step 3: Analysis
            status_text.text("🔍 Analyzing stock performance...")
            progress_bar.progress(60)
            
            try:
                # Run the multi-agent analysis
                result = run_financial_analysis(stock_symbol)
                
                # Ensure result is a string for display
                if not isinstance(result, str):
                    # Handle CrewOutput or other objects
                    if hasattr(result, 'raw'):
                        result = str(result.raw)
                    elif hasattr(result, 'output'):
                        result = str(result.output)
                    elif hasattr(result, 'result'):
                        result = str(result.result)
                    else:
                        result = str(result)
                
                progress_bar.progress(80)
                status_text.text("📝 Generating professional report...")
                time.sleep(1)
                
                progress_bar.progress(100)
                status_text.text("✅ Analysis complete!")
                
                # Display results
                st.markdown("## 📋 Financial Analysis Report")
                st.markdown(result)
                
                # Download button
                st.download_button(
                    label="📥 Download Report",
                    data=result,
                    file_name=f"{stock_symbol}_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                    mime="text/markdown"
                )
                
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
                st.info("💡 Try checking your API key or stock symbol")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        elif not stock_symbol:
            st.info("👈 Enter a stock symbol in the sidebar to begin analysis")
        
        else:
            # Show sample when no analysis is running
            st.markdown("## 🎯 How It Works")
            st.markdown("""
            1. **Enter Stock Symbol**: Input any valid ticker (AAPL, GOOGL, etc.)
            2. **AI Agents Activate**: Two specialized agents work together
            3. **Real-time Analysis**: Live market data fetching and analysis
            4. **Professional Report**: Get institutional-grade investment reports
            """)
            
            # Show example
            with st.expander("📖 See Example Analysis"):
                st.markdown("""
                ```markdown
                # AAPL Stock Analysis Report
                
                ## Executive Summary
                Apple Inc. (AAPL) shows strong fundamentals with...
                
                ## Key Metrics
                | Metric | Value |
                |--------|-------|
                | Current Price | $185.25 |
                | P/E Ratio | 28.5 |
                | Market Cap | $2.85T |
                ```
                """)

    with col2:
        if stock_symbol:
            # Display stock chart
            st.subheader(f"📈 {stock_symbol} Chart")
            try:
                chart = create_stock_chart(stock_symbol)
                st.plotly_chart(chart, use_container_width=True)
            except:
                st.error("Unable to load chart")
            
            # Quick metrics
            st.subheader("⚡ Quick Stats")
            try:
                stock = yf.Ticker(stock_symbol)
                info = stock.info
                
                metrics = {
                    "Current Price": f"${info.get('currentPrice', 'N/A')}",
                    "Market Cap": f"${info.get('marketCap', 0):,.0f}" if info.get('marketCap') else "N/A",
                    "P/E Ratio": f"{info.get('forwardPE', 'N/A')}",
                    "52W High": f"${info.get('fiftyTwoWeekHigh', 'N/A')}",
                    "52W Low": f"${info.get('fiftyTwoWeekLow', 'N/A')}"
                }
                
                for metric, value in metrics.items():
                    st.metric(metric, value)
                    
            except:
                st.info("Enter valid symbol for quick stats")

    # Footer
    st.markdown("---")
    st.markdown("**Built with CrewAI, SambaNova AI, and Streamlit** | 🚀 Multi-Agent Financial Analysis")

if __name__ == "__main__":
    main()