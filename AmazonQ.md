# Stock Pulse - Amazon Q Developer Project

This project was created with the assistance of Amazon Q Developer. It demonstrates how to build a stock analysis tool using LangChain, LangGraph, and OpenAI's GPT-4o-mini model.

## Project Overview

Stock Pulse analyzes stocks using financial metrics, news trends, and AI-powered sentiment analysis. It provides investment recommendations (BUY, SELL, HOLD) with detailed reasoning.

## Key Components

1. **LangChain Integration**: Uses LangChain for orchestrating the LLM workflow
2. **LangGraph**: Implements a graph-based workflow for stock analysis
3. **OpenAI GPT-4o-mini**: Powers the intelligent analysis of stock data
4. **yfinance**: Fetches financial metrics and news data
5. **Rich**: Provides beautiful terminal output formatting
6. **Streamlit**: Offers an intuitive web interface

## Implementation Details

- **Stock Data Collection**: Fetches comprehensive financial metrics and recent news
- **LLM Analysis**: Processes the data through a carefully crafted prompt
- **Signal Generation**: Produces clear investment signals with reasoning
- **Risk Assessment**: Identifies potential risks to the recommendation
- **Dual Interfaces**: Command-line and web-based UI options

## Usage

```bash
# Analyze a single stock via CLI
poetry run python main.py AAPL

# Analyze multiple stocks via CLI
poetry run python main.py AAPL MSFT GOOGL AMZN

# Output results in JSON format
poetry run python main.py AAPL MSFT --json

# Launch the Streamlit web interface
poetry run streamlit run streamlit_app.py
```
