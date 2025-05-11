"""Settings for Stock Pulse."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Model settings
MODEL_NAME = "gpt-4o-mini"

# Stock data settings
LOOKBACK_PERIOD = "1y"  # 1 year of historical data
