import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
from dotenv import load_dotenv

# Import your new modules
import config
from services import fetch_stock_data, generate_claude_analysis, get_analyst_ratings

# --- App Setup ---
load_dotenv()
st.set_page_config(page_title="Stock Analysis Dashboard", layout="wide")

# --- Session State Initialization ---
if 'processed_ticker' not in st.session_state:
    st.session_state.processed_ticker = ""
if 'analysis_content' not in st.session_state:
    st.session_state.analysis_content = ""
if 'stock_info' not in st.session_state:
    st.session_state.stock_info = None
if 'analyst_ratings' not in st.session_state:
    st.session_state.analyst_ratings = None
# ADDED: Set the default time period selection to "1D"
if 'selected_period' not in st.session_state:
    st.session_state.selected_period = "1D"

st.logo("images/logo.png", size="large")

# --- UI Layout ---
left_col, right_col = st.columns(2, gap="large")

# Determine the selected period from session state BEFORE the UI is drawn
selected = st.session_state.selected_period
time_period, interval = config.PERIOD_OPTIONS[selected]

with left_col:
    ticker_input = st.text_input("", placeholder="Search").upper()
    prepost = st.toggle("Include Pre-Market and After-Hours Data", value=True)
    # The radio buttons will now be drawn conditionally later in the script

# --- Logic ---
if ticker_input:
    if ticker_input != st.session_state.processed_ticker:
        st.session_state.processed_ticker = ticker_input
        stock_info = fetch_stock_data(ticker_input)
        st.session_state.stock_info = stock_info
        st.session_state.analyst_ratings = None  # Clear previous ratings

        if stock_info:
            with st.spinner('Generating stock analysis...'):
                st.session_state.analysis_content = generate_claude_analysis(
                    stock_info,
                    config.CLAUDE_MODEL,
                    config.ANALYSIS_PROMPT_TEMPLATE
                )
            st.session_state.analyst_ratings = get_analyst_ratings(ticker_input)
        else:
            st.session_state.analysis_content = ""

# --- Display Data ---
if st.session_state.stock_info:
    info = st.session_state.stock_info

    # CSS for Plotly charts
    st.markdown("""
        <style>
        .stPlotlyChart { margin-top: -30px !important; margin-bottom: -50px !important; }
        </style>
    """, unsafe_allow_html=True)

    # MOVED: Conditionally display the radio buttons in the left column
    with left_col:
        # This will only appear if a valid stock has been found
        st.radio(
            "Select time period",
            list(config.PERIOD_OPTIONS.keys()),
            horizontal=True,
            key="selected_period"  # Link the widget to the session state key
        )

    with right_col:
        st.subheader(f"{info.get('longName')} ({st.session_state.processed_ticker})")

        # Fetch and Display Price Data
        hist = yf.Ticker(st.session_state.processed_ticker).history(period=time_period, interval=interval,
                                                                    prepost=prepost)
        current_price = info.get('regularMarketPrice')
        currency = info.get('currency', '')
        time_period_map = {"1D": "Today", "1W": "in the last week", "3M": "in the last 3 months",
                           "1Y": "in the last year", "MAX": "since listing"}
        change_text_period = time_period_map.get(selected)
        reference_price = info.get('previousClose') if selected == '1D' else (
            hist['Close'].iloc[0] if not hist.empty else None)

        if current_price and reference_price:
            price_change = current_price - reference_price
            percentage_change = (price_change / reference_price) * 100
            color = "green" if price_change >= 0 else "red"
            arrow = "▲" if price_change >= 0 else "▼"
            price_display = f"""<div style="position: relative; z-index: 1; margin-top: -20px; margin-bottom: -80px; display: flex; align-items: baseline; gap: 15px;"><h2 style='margin: 0;'>{current_price:.2f} {currency}</h2><div style='font-size: 1.3rem; color: {color};'>{arrow} {abs(price_change):.2f} ({abs(percentage_change):.2f}%)<span style='font-size: 1rem; color: gray;'> {change_text_period}</span></div></div>"""
            st.markdown(price_display, unsafe_allow_html=True)

        # Candlestick Chart
        if not hist.empty:
            fig = go.Figure(data=[
                go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'],
                               name='Price')])
            fig.update_layout(dragmode=False, xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True),
                              template='plotly_dark')
            st.plotly_chart(fig, use_container_width=True, config={'displaylogo': False})
        else:
            st.write("No price history available for this period.")

        # Analyst Ratings Donut Chart
        if st.session_state.analyst_ratings:
            latest_ratings = st.session_state.analyst_ratings[0]
            labels = ['Strong Buy', 'Buy', 'Hold', 'Sell', 'Strong Sell']
            ratings = [latest_ratings['strongBuy'], latest_ratings['buy'], latest_ratings['hold'],
                       latest_ratings['sell'], latest_ratings['strongSell']]
            colors = ['#004d00', '#008000', '#ffa500', '#ff4500', '#8b0000']
            text_labels = [str(r) if r > 0 else '' for r in ratings]
            donut_chart = go.Figure(data=[
                go.Pie(labels=labels, values=ratings, text=text_labels, textinfo='text', hole=.68,
                       marker=dict(colors=colors), textfont=dict(size=27, weight=600),
                       insidetextorientation='horizontal')])
            donut_chart.update_layout(title_text="Analyst Ratings", title_font=dict(size=30), title_y=0.92,
                                      legend_title_text='Ratings')
            st.plotly_chart(donut_chart, use_container_width=True)

    with left_col:
        # Display Analysis
        if st.session_state.analysis_content:
            st.markdown("---")
            st.markdown(st.session_state.analysis_content)

elif st.session_state.processed_ticker:
    with right_col:
        st.warning(f"No results found for the ticker symbol: {st.session_state.processed_ticker}")