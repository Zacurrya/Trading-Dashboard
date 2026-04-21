import os

import finnhub as fh
import streamlit as st
import yfinance as yf
from dotenv import load_dotenv

load_dotenv()


@st.cache_resource
def get_finnhub_client():
    """Initialize and cache a Finnhub client."""
    return fh.Client(api_key=os.environ.get("FINNHUB_API_KEY"))


@st.cache_data(ttl=3600)
def fetch_stock_data(ticker_symbol: str):
    """Fetch stock information from yfinance and validate it."""
    try:
        ticker = yf.Ticker(ticker_symbol)
        if not ticker.info or "longName" not in ticker.info or not ticker.info.get("longName"):
            return None
        return ticker.info
    except Exception as e:
        st.error(f"yfinance error: {e}")
        return None


@st.cache_data(ttl=900)
def fetch_price_history(ticker_symbol: str, period: str, interval: str, prepost: bool):
    """Fetch historical OHLC data for charting."""
    try:
        return yf.Ticker(ticker_symbol).history(period=period, interval=interval, prepost=prepost)
    except Exception as e:
        st.error(f"Price history error: {e}")
        return None


@st.cache_data(ttl=3600)
def get_analyst_ratings(ticker_symbol: str):
    """Fetch analyst recommendation trends from Finnhub."""
    try:
        client = get_finnhub_client()
        return client.recommendation_trends(ticker_symbol)
    except Exception as e:
        st.error(f"Finnhub API error: {e}")
        return None
