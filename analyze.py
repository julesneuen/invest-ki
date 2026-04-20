import sys
import json
import os
from datetime import date
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / "TradingAgents/.env")

sys.path.insert(0, str(Path.home() / "TradingAgents"))

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

WATCHLIST_PATH = Path(__file__).parent / "config/watchlist.json"
REPORTS_DIR = Path(__file__).parent / "reports"

def load_watchlist():
    with open(WATCHLIST_PATH) as f:
        return json.load(f)["stocks"]

def run_analysis(ticker: str, analysis_date: str) -> str:
    config = DEFAULT_CONFIG.copy()
    config["quick_think_llm"] = "gpt-5.4-mini"
    config["deep_think_llm"] = "gpt-5.4-mini"
    config["max_debate_rounds"] = 1
    config["max_risk_discuss_rounds"] = 1
    config["data_vendors"] = {
        "core_stock_apis": "alpha_vantage",
        "technical_indicators": "alpha_vantage",
        "fundamental_data": "yfinance",
        "news_data": "yfinance",
    }

    ta = TradingAgentsGraph(debug=False, config=config)
    _, decision = ta.propagate(ticker, analysis_date)
    return decision

def save_report(ticker: str, analysis_date: str, decision: str):
    REPORTS_DIR.mkdir(exist_ok=True)
    filename = REPORTS_DIR / f"{ticker}_{analysis_date}.txt"
    filename.write_text(f"TradingAgents Report\nTicker: {ticker}\nDate: {analysis_date}\n\n{decision}\n")
    return filename

def pick_ticker(watchlist: list[str]) -> str:
    print("\nYour watchlist:")
    for i, t in enumerate(watchlist, 1):
        print(f"  {i}. {t}")
    print(f"  {len(watchlist)+1}. Run ALL")
    choice = input("\nPick a number (or type a ticker directly): ").strip().upper()
    if choice.isdigit():
        idx = int(choice) - 1
        if idx == len(watchlist):
            return "ALL"
        return watchlist[idx]
    return choice

def main():
    watchlist = load_watchlist()
    analysis_date = date.today().isoformat()

    if len(sys.argv) > 1:
        ticker = sys.argv[1].upper()
        if len(sys.argv) > 2:
            analysis_date = sys.argv[2]
    else:
        ticker = pick_ticker(watchlist)

    tickers = watchlist if ticker == "ALL" else [ticker]

    for t in tickers:
        print(f"\nAnalyzing {t} for {analysis_date}...")
        decision = run_analysis(t, analysis_date)
        report_path = save_report(t, analysis_date, decision)
        print(f"\n{'='*60}")
        print(f"VERDICT for {t}: {decision.splitlines()[-1]}")
        print(f"Full report saved to: {report_path}")

if __name__ == "__main__":
    main()
