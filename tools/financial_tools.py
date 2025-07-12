import yfinance as yf
import json
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class StockInput(BaseModel):
    symbol: str = Field(..., description="Stock symbol (e.g., 'AAPL')")


class YFinanceStockTool(BaseTool):
    name: str = "stock_data_tool"
    description: str = "Fetches real-time stock market data."
    args_schema: type[BaseModel] = StockInput

    def _run(self, symbol: str) -> str:
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            hist = stock.history(period="1mo")
            latest_data = hist.iloc[-1]
            hist_1y = stock.history(period="1y")

            response = {
                "company": info.get("longName"),
                "latest_price": latest_data['Close'],
                "latest_date": latest_data.name.strftime('%Y-%m-%d'),
                "52wk_high": info.get("fiftyTwoWeekHigh"),
                "52wk_low": info.get("fiftyTwoWeekLow"),
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("forwardPE"),
                "rating": info.get("recommendationKey")
            }
            
            return json.dumps(response, indent=2)
        except Exception as e:
            return f"Error: {str(e)}"