"""LLM model configuration for Stock Pulse."""

from langchain_openai import ChatOpenAI
from stock_pulse.config.settings import OPENAI_API_KEY, MODEL_NAME

def get_llm():
    """
    Initialize and return the LLM model.
    
    Returns:
        Configured LLM model
    """
    return ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model=MODEL_NAME,
        temperature=0.1  # Low temperature for more deterministic outputs
    )
