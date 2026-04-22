import google.genai
import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

"""Initialize and cache a Gemini client."""
@st.cache_resource
def get_gemini_client():
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY (or GOOGLE_API_KEY) in environment variables.")
    return google.genai.Client(api_key=api_key)

"""Generate stock analysis text using the Gemini API."""
@st.cache_data(ttl=3600)
def generate_gemini_analysis(ticker_symbol: str, model: str, prompt_template: str):
    try:
        client = get_gemini_client()
        prompt = prompt_template.format(ticker_input=ticker_symbol)
        response = client.models.generate_content(model=model, contents=prompt)
        if response and getattr(response, "text", None):
            return response.text
        return None
    except Exception as e:
        st.error(f"Gemini API error: {e}")
        return None
