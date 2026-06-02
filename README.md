# Streamlit Trading Dashboard

A stock analysis dashboard built with Streamlit. Search tickers, view price charts, generate AI summaries, and check analyst ratings.

## Features

- Stock lookup by ticker symbol (for example: AAPL, GOOGL)
- AI-generated stock summary (Google Gemini)
- Analyst recommendation trends (Finnhub)
- Interactive candlestick charts (Plotly)

## Tech Stack

- Python
- Streamlit
- yfinance
- Plotly
- Google Gemini SDK
- finnhub-python

## How to Run

### 1. Open the project root

Use this folder:

`P:\trading-dashboard\Trading-Dashboard`

### 2. Install dependencies

From the project root:

```powershell
c:/python313/python.exe -m pip install -r PythonProject/requirements.txt
```

For deployment platforms that expect `requirements.txt` at the repository root, use:

```powershell
c:/python313/python.exe -m pip install -r requirements.txt
```

If you are already inside `PythonProject`, use:

```powershell
c:/python313/python.exe -m pip install -r requirements.txt
```

### 3. Set API keys

Create or update `.env` in the project root with:

```env
GEMINI_API_KEY=your_gemini_api_key
# or GOOGLE_API_KEY=your_gemini_api_key
FINNHUB_API_KEY=your_finnhub_api_key
```

### 4. Start the app

From the project root:

```powershell
c:/python313/python.exe -m streamlit run PythonProject/dashboard.py
```

For Streamlit Community Cloud, point the app to `streamlit_app.py` at the repository root.

Or from `PythonProject`:

```powershell
c:/python313/python.exe -m streamlit run dashboard.py
```

### 5. Open in browser

Go to:

`http://localhost:8501`

### 6. Stop the app

In the terminal running Streamlit, press `Ctrl+C`.
