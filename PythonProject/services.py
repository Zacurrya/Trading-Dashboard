import yfinance as yf
import anthropic
import streamlit as st
import finnhub as fh
import os
from dotenv import load_dotenv

load_dotenv()

# Cache the clients so they aren't recreated on every run
@st.cache_resource
def get_anthropic_client():
    """Initializes and returns the Anthropic client."""
    return anthropic.Anthropic()
@st.cache_resource
def get_finnhub_client():
    return fh.Client(api_key=os.environ.get("FINNHUB_API_KEY"))

@st.cache_data(ttl=3600)
def fetch_stock_data(ticker_symbol: str):
    """Fetches stock information from yfinance and checks for validity."""
    try:
        ticker = yf.Ticker(ticker_symbol)
        # Check for valid data; some tickers exist but have no info
        if not ticker.info or 'longName' not in ticker.info or not ticker.info.get('longName'):
            return None
        return ticker.info
    except Exception as e:
        st.error(f"yfinance error: {e}")
        return None

@st.cache_data(ttl=3600)
def generate_claude_analysis(ticker_symbol: str, model: str, prompt_template: str):
    """Generates stock analysis using the Anthropic API."""
    try:
        client = get_anthropic_client()
        prompt = prompt_template.format(ticker_input=ticker_symbol)

        message = client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    except Exception as e:
        st.error(f"Claude API error: {e}")
        return None

@st.cache_data(ttl=3600)
def get_analyst_ratings(ticker_symbol: str):
    """Fetches analyst ratings from Finnhub."""
    try:
        client = get_finnhub_client()
        ratings = client.recommendation_trends(ticker_symbol)
        return ratings
    except Exception as e:
        st.error(f"Finnhub API error: {e}")
        return None