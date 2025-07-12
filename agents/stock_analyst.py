from crewai import Agent, LLM
from tools.financial_tools import YFinanceStockTool
import os


def create_stock_analyst_agent():
    """Creates and returns the Stock Analyst Agent"""
    
    # Initialize tool & LLM
    stock_tool = YFinanceStockTool()
    llm = LLM(
        model="sambanova/Llama-4-Maverick-17B-128E-Instruct",
        api_key=os.getenv("SAMBANOVA_API_KEY")
    )

    # Stock Analysis Agent
    stock_analysis_agent = Agent(
        role="Wall Street Financial Analyst",
        goal="Analyze {symbol} stock using real-time data",
        backstory="Seasoned analyst focused on data-driven insights.",
        llm=llm,
        tools=[stock_tool],
        verbose=True
    )
    
    return stock_analysis_agent


def create_report_writer_agent():
    """Creates and returns the Report Writer Agent"""
    
    llm = LLM(
        model="sambanova/Llama-4-Maverick-17B-128E-Instruct",
        api_key=os.getenv("SAMBANOVA_API_KEY")
    )

    # Report Writing Agent
    report_writer_agent = Agent(
        role="Financial Report Specialist",
        goal="Create a professional investment report",
        backstory="Expert writer for institutional-grade reports.",
        llm=llm,
        verbose=True
    )
    
    return report_writer_agent