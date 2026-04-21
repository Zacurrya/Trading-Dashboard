import yfinance as yf
import streamlit as st
import finnhub as fh
import os
import importlib
from dotenv import load_dotenv

load_dotenv()

# Cache the clients so they aren't recreated on every run
@st.cache_resource
def get_gemini_client():
    """Initializes and returns a configured Gemini client."""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY (or GOOGLE_API_KEY) in environment variables.")
    genai = importlib.import_module("google.genai")
    return genai.Client(api_key=api_key)
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
def generate_gemini_analysis(ticker_symbol: str, model: str, prompt_template: str):
    """Generates stock analysis using the Gemini API."""
    try:
        client = get_gemini_client()
        prompt = prompt_template.format(ticker_input=ticker_symbol)

        response = client.models.generate_content(model=model, contents=prompt)
        if response and getattr(response, "text", None):
            return response.text.strip()
        return None
    except Exception as e:
        st.error(f"Gemini API error: {e}")
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