"""Streamlit UI for Stock Pulse."""

import streamlit as st
import time
from typing import List

from stock_pulse.core.analyzer import analyze_stocks
from stock_pulse.config.settings import OPENAI_API_KEY

def display_banner():
    """Display the Stock Pulse banner."""
    st.markdown("""
    <style>
    .banner {
        font-family: monospace;
        color: #00BFFF;
        font-size: 12px;
        line-height: 1;
        white-space: pre;
    }
    .author {
        color: #FF00FF;
        font-size: 14px;
        margin-bottom: 20px;
    }
    </style>
    <div class="banner">
    ███████╗████████╗ ██████╗  ██████╗██╗  ██╗    ██████╗ ██╗   ██╗██╗     ███████╗███████╗
    ██╔════╝╚══██╔══╝██╔═══██╗██╔════╝██║ ██╔╝    ██╔══██╗██║   ██║██║     ██╔════╝██╔════╝
    ███████╗   ██║   ██║   ██║██║     █████╔╝     ██████╔╝██║   ██║██║     ███████╗█████╗  
    ╚════██║   ██║   ██║   ██║██║     ██╔═██╗     ██╔═══╝ ██║   ██║██║     ╚════██║██╔══╝  
    ███████║   ██║   ╚██████╔╝╚██████╗██║  ██╗    ██║     ╚██████╔╝███████╗███████║███████╗
    ╚══════╝   ╚═╝    ╚═════╝  ╚═════╝╚═╝  ╚═╝    ╚═╝      ╚═════╝ ╚══════╝╚══════╝╚══════╝
    </div>
    <div class="author">Made with ❤️ by Amit Wani</div>
    """, unsafe_allow_html=True)

def display_disclaimer():
    """Display the disclaimer."""
    st.warning("""
    **DISCLAIMER:** The analysis provided by Stock Pulse is for informational purposes only and does not 
    constitute investment advice. Stock market investments involve risk, and past performance is not indicative of 
    future results. Always conduct your own research and consult with a qualified financial advisor before making 
    investment decisions.
    """)

def validate_environment():
    """Validate that required environment variables are set."""
    if not OPENAI_API_KEY:
        st.error("""
        **Error:** OPENAI_API_KEY environment variable is not set.
        Please set it in a .env file or export it in your shell.
        """)
        st.stop()

def display_stock_analysis(ticker: str, result: dict):
    """Display analysis results for a single stock."""
    if result.get('success', False):
        signal = result['signal']
        signal_color = {
            'BUY': 'green',
            'SELL': 'red',
            'HOLD': 'orange'
        }.get(signal, 'blue')
        
        st.subheader(f"{ticker}: {result.get('name', ticker)}")
        
        # Display signal with appropriate color
        st.markdown(f"<h3 style='color: {signal_color};'>Signal: {signal}</h3>", unsafe_allow_html=True)
        
        # Display reasoning
        st.markdown("**Reasoning:**")
        st.write(result['reasoning'])
        
        # Create two columns for key factors and risks
        col1, col2 = st.columns(2)
        
        # Display key factors
        with col1:
            st.markdown("**Key Factors:**")
            for factor in result.get('key_factors', []):
                st.markdown(f"• {factor}")
        
        # Display risks
        with col2:
            st.markdown("**Risks:**")
            for risk in result.get('risks', []):
                st.markdown(f"• {risk}")
        
        # Display recent news
        if 'news' in result and result['news']:
            st.markdown("**Recent News:**")
            
            # Filter out news items with missing data
            valid_news = [article for article in result['news'] 
                         if article.get('title') and article.get('publisher')]
            
            if valid_news:
                # Display news in an expandable section
                with st.expander("View Recent News", expanded=True):
                    for i, article in enumerate(valid_news):
                        st.markdown(f"**{i+1}. [{article['title']}]({article['link']})**")
                        st.caption(f"{article['published']} - {article['publisher']}")
                        st.caption(f"URL: {article['link']}")
                        if i < len(valid_news) - 1:
                            st.markdown("---")
            else:
                st.info("No recent news available.")
        else:
            st.info("No recent news available.")
        
        st.markdown("---")
    else:
        st.error(f"**Error analyzing {ticker}:** {result.get('error', 'Unknown error')}")

def main():
    """Main entry point for the Streamlit app."""
    st.set_page_config(
        page_title="Stock Pulse - Stock Analysis Tool",
        page_icon="📈",
        layout="wide"
    )
    
    display_banner()
    
    st.markdown("### Feel the pulse of the market with AI-powered stock insights")
    st.markdown("Enter one or more stock ticker symbols separated by commas or spaces.")
    
    # Input for stock tickers
    ticker_input = st.text_input("Stock Tickers (e.g., AAPL, MSFT, GOOGL)")
    
    # Analyze button
    analyze_button = st.button("Analyze Stocks")
    
    if analyze_button and ticker_input:
        validate_environment()
        
        # Parse tickers
        tickers = [ticker.strip().upper() for ticker in ticker_input.replace(',', ' ').split() if ticker.strip()]
        
        if not tickers:
            st.error("Please enter at least one valid stock ticker.")
            return
        
        # Show progress
        with st.spinner(f"Analyzing {len(tickers)} stocks..."):
            results = analyze_stocks(tickers)
            
            # Display results
            for ticker, result in results.items():
                display_stock_analysis(ticker, result)
        
        st.success("Analysis complete!")
    
    # Always show disclaimer at the bottom
    display_disclaimer()

if __name__ == "__main__":
    main()
