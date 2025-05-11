# Stock Pulse

Feel the pulse of the market—analyze stocks with news trends and emotional tone.

## Overview

Stock Pulse is a Python tool that analyzes stocks using financial metrics, news trends, and AI-powered sentiment analysis. It provides investment recommendations (BUY, SELL, HOLD) with detailed reasoning based on comprehensive analysis.

## Features

- Analyze multiple stocks at once
- Fetch financial metrics and news data using yfinance
- Utilize OpenAI's GPT-4o-mini model for intelligent analysis
- Generate investment signals with detailed reasoning
- Identify key factors and potential risks

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/stock-pulse.git
   cd stock-pulse
   ```

2. Install dependencies using Poetry:
   ```
   poetry install
   ```

3. Create a `.env` file with your OpenAI API key:
   ```
   cp .env.example .env
   ```
   Then edit the `.env` file to add your OpenAI API key.

## Usage

Analyze stocks using the command line:

```bash
# Analyze a single stock
poetry run python main.py AAPL

# Analyze multiple stocks
poetry run python main.py AAPL MSFT GOOGL AMZN

# Output results in JSON format
poetry run python main.py AAPL MSFT --json
```

## Project Structure

```
stock-pulse/
├── stock_pulse/
│   ├── core/           # Core functionality
│   ├── models/         # LLM models
│   ├── utils/          # Utility functions
│   ├── config/         # Configuration
│   └── cli.py          # Command-line interface
├── main.py             # Entry point
├── pyproject.toml      # Poetry configuration
└── README.md           # Documentation
```

## Requirements

- Python 3.8+
- OpenAI API key
- Internet connection for fetching stock data

## License

MIT
