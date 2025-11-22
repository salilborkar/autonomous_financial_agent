from langchain_core.tools import tool
import yfinance as yf
from ddgs import DDGS

@tool
def get_stock_fundamentals(ticker: str):
    """
    Retrieves fundamental data for a stock ticker (e.g., AAPL, TSLA).
    Returns current price, 52-week high/low, and market cap.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        data = {
            "symbol": ticker,
            "current_price": info.get("currentPrice"),
            "market_cap": info.get("marketCap"),
            "52_week_high": info.get("fiftyTwoWeekHigh"),
            "52_week_low": info.get("fiftyTwoWeekLow"),
            "pe_ratio": info.get("trailingPE")
        }
        return str(data)
    except Exception as e:
        return f"Error fetching data for {ticker}: {e}"

@tool
def search_market_news(query: str):
    """
    Searches the web for real-time news using DuckDuckGo.
    Useful for finding sentiment, recent events, or analyst ratings.
    """
    try:
        results = DDGS().text(query, max_results=3)
        summary = ""
        for result in results:
            summary += f"- {result['title']}: {result['body']}\n"
        return summary
    except Exception as e:
        return f"Error searching news: {e}"