"""Utility functions for fetching and processing stock data."""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

def get_stock_data(ticker: str, period: str = "1y") -> Dict[str, Any]:
    """
    Fetch stock data for a given ticker.
    
    Args:
        ticker: Stock ticker symbol
        period: Time period for historical data (default: 1y)
        
    Returns:
        Dictionary containing stock data and metrics
    """
    try:
        # Get stock info
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Get historical data
        hist = stock.history(period=period)
        
        # Calculate 1-year return
        if not hist.empty:
            start_price = hist['Close'].iloc[0]
            end_price = hist['Close'].iloc[-1]
            yearly_return = ((end_price - start_price) / start_price) * 100
        else:
            yearly_return = None
            
        # Extract key financial metrics
        metrics = {
            'ticker': ticker,
            'name': info.get('shortName', ticker),
            'sector': info.get('sector', 'Unknown'),
            'industry': info.get('industry', 'Unknown'),
            'current_price': info.get('currentPrice', None),
            'target_price': info.get('targetMeanPrice', None),
            'yearly_return': round(yearly_return, 2) if yearly_return is not None else None,
            'pe_ratio': info.get('trailingPE', None),
            'forward_pe': info.get('forwardPE', None),
            'peg_ratio': info.get('pegRatio', None),
            'price_to_book': info.get('priceToBook', None),
            'dividend_yield': info.get('dividendYield', None) * 100 if info.get('dividendYield') else None,
            'eps': info.get('trailingEps', None),
            'roe': info.get('returnOnEquity', None) * 100 if info.get('returnOnEquity') else None,
            'roa': info.get('returnOnAssets', None) * 100 if info.get('returnOnAssets') else None,
            'debt_to_equity': info.get('debtToEquity', None),
            'quick_ratio': info.get('quickRatio', None),
            'current_ratio': info.get('currentRatio', None),
            'recommendation': info.get('recommendationKey', 'N/A').upper(),
            'target_upside': ((info.get('targetMeanPrice', 0) / info.get('currentPrice', 1)) - 1) * 100 
                            if info.get('targetMeanPrice') and info.get('currentPrice') else None
        }
        
        # Get recent news
        news = stock.news
        processed_news = []
        
        for article in news[:5]:  # Limit to 5 most recent news
            processed_news.append({
                'title': article.get('title', ''),
                'publisher': article.get('publisher', ''),
                'link': article.get('link', ''),
                'published': datetime.fromtimestamp(article.get('providerPublishTime', 0)).strftime('%Y-%m-%d')
            })
            
        return {
            'metrics': metrics,
            'news': processed_news,
            'success': True
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def get_multiple_stocks_data(tickers: List[str], period: str = "1y") -> Dict[str, Dict[str, Any]]:
    """
    Fetch data for multiple stock tickers.
    
    Args:
        tickers: List of stock ticker symbols
        period: Time period for historical data
        
    Returns:
        Dictionary mapping tickers to their respective data
    """
    results = {}
    for ticker in tickers:
        results[ticker] = get_stock_data(ticker, period)
    return results
