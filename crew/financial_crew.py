from crewai import Crew, Task, Process
from agents.stock_analyst import create_stock_analyst_agent, create_report_writer_agent


class FinancialCrew:
    def __init__(self):
        # Initialize agents
        self.stock_analysis_agent = create_stock_analyst_agent()
        self.report_writer_agent = create_report_writer_agent()
        
        # Initialize tasks
        self.analysis_task = None
        self.report_task = None
        self.crew = None

    def create_tasks(self, symbol: str):
        """Create tasks for the given stock symbol"""
        
        # Analysis Task
        self.analysis_task = Task(
            description=f"Analyze {symbol} using stock_data_tool. Cover: "
                       "1. Latest Price & Date "
                       "2. 52-Week High/Low & Dates "
                       "3. Financials (Market Cap, P/E) "
                       "4. Analyst Rating. "
                       "MUST use the tool for live data.",
            expected_output="Comprehensive analysis with real-time data.",
            agent=self.stock_analysis_agent
        )

        # Report Task (Simplified Description)
        self.report_task = Task(
            description="Transform analysis into a professional report. "
                       "Include: Executive Summary, Key Metrics Table, "
                       "52-Week Range Analysis, Risk Assessment, "
                       "Future Outlook. Use Markdown, tables, emojis.",
            expected_output="Polished report in markdown format.",
            agent=self.report_writer_agent
        )

    def create_crew(self):
        """Create and configure the crew"""
        self.crew = Crew(
            agents=[self.stock_analysis_agent, self.report_writer_agent],
            tasks=[self.analysis_task, self.report_task],
            process=Process.sequential,  # Tasks run in order
            verbose=True
        )

    def analyze_stock(self, symbol: str):
        """Main method to analyze a stock"""
        try:
            # Create tasks for the specific symbol
            self.create_tasks(symbol)
            
            # Create and run the crew
            self.create_crew()
            
            # Execute the analysis
            result = self.crew.kickoff()
            
            return result
            
        except Exception as e:
            return f"Error during analysis: {str(e)}"


# Convenience function for external use
def run_financial_analysis(symbol: str):
    """Run financial analysis for a given stock symbol"""
    crew = FinancialCrew()
    return crew.analyze_stock(symbol)