# Anthropic API settings
CLAUDE_MODEL = "claude-3-5-sonnet-20240620" # Using the latest model
ANALYSIS_PROMPT_TEMPLATE = (
    "You are a financial analyst providing a brief, neutral summary for a stock dashboard. "
    "Analyze the stock with ticker {ticker_input}, considering its recent performance, "
    "relevant news, and analyst ratings to summarize the investment outlook."
    "\n\n"
    "Your response MUST follow these rules exactly:\n"
    "1. The output must be a single, plain text paragraph.\n"
    "2. Do NOT use any markdown (no headings, bolding, bullet points, italics, etc.).\n"
    "3. Do NOT include a title, preamble, or any conversational text like 'Here is the summary:'.\n"
    "4. The entire summary must be under 120 words."
)
# UI settings
PERIOD_OPTIONS = {
    "1D": ("1d", "5m"),
    "1W": ("7d", "1h"),
    "3M": ("3mo", "1d"),
    "1Y": ("1y", "1d"),
    "MAX": ("max", "1wk")
}