"""Stock analysis using LangChain and LangGraph."""

from typing import Dict, Any, List, TypedDict
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph
import json

# Define a TypedDict for state instead of using langgraph.graph.types.State
class State(TypedDict, total=False):
    tickers: List[str]
    stock_data: Dict[str, Any]
    analysis: Dict[str, Any]
    
# Define Pydantic model for structured output
class StockAnalysis(BaseModel):
    signal: str = Field(description="Investment signal: BUY, SELL, or HOLD")
    reasoning: str = Field(description="Explanation for the recommendation")
    key_factors: List[str] = Field(description="Key factors that influenced the decision")
    risks: List[str] = Field(description="Potential risks to the recommendation")

from stock_pulse.models.llm import get_llm
from stock_pulse.utils.stock_data import get_multiple_stocks_data
from stock_pulse.config.settings import LOOKBACK_PERIOD

def format_news(news_items: List[Dict[str, str]]) -> str:
    """Format news items for the prompt."""
    if not news_items:
        return "No recent news available."
    
    formatted_news = ""
    for i, item in enumerate(news_items, 1):
        formatted_news += f"{i}. {item['title']} ({item['published']} - {item['publisher']})\n"
    
    return formatted_news

def analyze_stock(ticker_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze a single stock using the LLM.
    
    Args:
        ticker_data: Stock data dictionary
        
    Returns:
        Analysis results
    """
    if not ticker_data.get('success', False):
        return {
            'ticker': ticker_data.get('ticker', 'Unknown'),
            'error': ticker_data.get('error', 'Failed to fetch stock data'),
            'success': False
        }
    
    metrics = ticker_data['metrics']
    news = format_news(ticker_data['news'])
    
    # Create parser for structured output
    parser = PydanticOutputParser(pydantic_object=StockAnalysis)
    
    # Create prompt with stock data and format instructions
    prompt_template = """
    You are a professional stock analyst with expertise in financial analysis and market trends.
    Analyze the following stock data and provide a clear investment recommendation.
    
    Stock Information:
    - Ticker: {ticker}
    - Company Name: {name}
    - Sector: {sector}
    - Industry: {industry}
    - Current Price: ${current_price}
    - Target Price: ${target_price}
    - Target Upside: {target_upside}%
    
    Financial Metrics:
    - 1-Year Return: {yearly_return}%
    - P/E Ratio: {pe_ratio}
    - Forward P/E: {forward_pe}
    - PEG Ratio: {peg_ratio}
    - Price-to-Book: {price_to_book}
    - Dividend Yield: {dividend_yield}%
    - EPS: ${eps}
    - ROE: {roe}%
    - ROA: {roa}%
    - Debt-to-Equity: {debt_to_equity}
    - Quick Ratio: {quick_ratio}
    - Current Ratio: {current_ratio}
    - Analyst Recommendation: {recommendation}
    
    Recent News:
    {news}
    
    Based on the above information, provide:
    1. A clear investment signal: BUY, SELL, or HOLD
    2. A concise explanation of your recommendation (3-5 sentences)
    3. Key factors that influenced your decision
    4. Potential risks to your recommendation
    
    {format_instructions}
    """
    
    # Get format instructions from the parser
    format_instructions = parser.get_format_instructions()
    
    # Create the prompt with format instructions
    prompt = ChatPromptTemplate.from_template(prompt_template)
    
    # Add news to metrics for the prompt
    metrics_with_news = {**metrics, 'news': news, 'format_instructions': format_instructions}
    
    # Get LLM
    llm = get_llm()
    
    # Create chain with structured output
    chain = prompt | llm | parser
    
    try:
        # Run analysis with structured output
        analysis = chain.invoke(metrics_with_news)
        
        return {
            'ticker': metrics['ticker'],
            'name': metrics['name'],
            'signal': analysis.signal,
            'reasoning': analysis.reasoning,
            'key_factors': analysis.key_factors,
            'risks': analysis.risks,
            'news': ticker_data['news'],  # Include the news articles in the result
            'metrics': metrics,  # Include all financial metrics
            'success': True
        }
    except Exception as e:
        return {
            'ticker': metrics['ticker'],
            'name': metrics['name'],
            'error': f"Failed to parse analysis: {str(e)}",
            'success': False
        }

def create_analysis_graph():
    """
    Create a LangGraph for stock analysis.
    
    Returns:
        Configured StateGraph
    """
    # Define the graph
    builder = StateGraph(State)
    
    # Define the nodes
    def fetch_stock_data(state: State) -> State:
        """Fetch stock data for all tickers."""
        tickers = state["tickers"]
        stock_data = get_multiple_stocks_data(tickers, LOOKBACK_PERIOD)
        return {"tickers": tickers, "stock_data": stock_data}
    
    def analyze_stocks(state: State) -> State:
        """Analyze all stocks."""
        stock_data = state["stock_data"]
        results = {}
        
        for ticker, data in stock_data.items():
            results[ticker] = analyze_stock(data)
            
        return {"tickers": state["tickers"], "stock_data": stock_data, "analysis": results}
    
    # Add nodes
    builder.add_node("fetch_data", fetch_stock_data)
    builder.add_node("analyze", analyze_stocks)
    
    # Add edges
    builder.add_edge("fetch_data", "analyze")
    builder.set_entry_point("fetch_data")
    builder.set_finish_point("analyze")
    
    # Compile the graph
    return builder.compile()

def analyze_stocks(tickers: List[str]) -> Dict[str, Any]:
    """
    Analyze multiple stocks.
    
    Args:
        tickers: List of stock ticker symbols
        
    Returns:
        Analysis results for all tickers
    """
    graph = create_analysis_graph()
    result = graph.invoke({"tickers": tickers})
    return result["analysis"]
