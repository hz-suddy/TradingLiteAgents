"""
Example script using DeepSeek models with TradingAgents.

To use this:
1. Set DEEPSEEK_API_KEY in your .env file or environment
2. Run: python main_deepseek.py
"""

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create a custom config for DeepSeek
config = DEFAULT_CONFIG.copy()

# === OPTION 1: Balanced approach (recommended) ===
# Uses deepseek-reasoner for deep analysis and deepseek-chat for quick tasks
config["llm_provider"] = "deepseek"
config["deep_think_llm"] = "deepseek-reasoner"    # For complex analysis
config["quick_think_llm"] = "deepseek-chat"       # For quick tasks
config["max_debate_rounds"] = 2                   # More debate rounds for better insights

# === OPTION 2: Cost-optimized approach ===
# Uncomment to use this instead
# config["llm_provider"] = "deepseek"
# config["deep_think_llm"] = "deepseek-chat"
# config["quick_think_llm"] = "deepseek-chat"
# config["max_debate_rounds"] = 1

# === OPTION 3: Deep reasoning approach ===
# Uncomment to use this instead (slowest but most thorough)
# config["llm_provider"] = "deepseek"
# config["deep_think_llm"] = "deepseek-reasoner"
# config["quick_think_llm"] = "deepseek-reasoner"
# config["max_debate_rounds"] = 2

# Configure data vendors (default uses yfinance, no extra API keys needed)
config["data_vendors"] = {
    "core_stock_apis": "yfinance",           # Options: alpha_vantage, yfinance
    "technical_indicators": "yfinance",      # Options: alpha_vantage, yfinance
    "fundamental_data": "yfinance",          # Options: alpha_vantage, yfinance
    "news_data": "yfinance",                 # Options: alpha_vantage, yfinance
}

# Initialize with custom config
ta = TradingAgentsGraph(debug=True, config=config)

# Forward propagate - analyze a stock for a specific date
_, decision = ta.propagate("NVDA", "2024-05-10")
print("\n" + "="*80)
print("FINAL TRADING DECISION")
print("="*80)
print(decision)

# Optional: Reflect and remember from trading results
# This helps the agents learn from past decisions
# Example: if position returned 1000 (1% profit)
# ta.reflect_and_remember(1000)

# To analyze multiple stocks:
# stocks = ["AAPL", "GOOGL", "MSFT", "NVDA"]
# for stock in stocks:
#     print(f"\n{'='*80}")
#     print(f"Analyzing {stock}...")
#     print('='*80)
#     _, decision = ta.propagate(stock, "2024-05-10")
#     print(decision)
