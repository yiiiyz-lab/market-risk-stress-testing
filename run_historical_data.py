import pandas as pd

from src.historical_data import (
    download_market_data,
    calculate_historical_returns,
)

from src.historical_scenarios import (
    load_historical_scenarios,
    validate_historical_scenarios,
)

from src.portfolio import load_portfolio, validate_portfolio
from src.historical_stress import (
    run_historical_stress,
    summarize_historical_stress,
)

tickers = [
    "SPY",
    "QQQ",
    "VGK",
    "IEF",
    "TLT",
    "LQD",
    "HYG",
    "GLD",
    "EURUSD=X",
    "USDJPY=X",
]

scenarios = load_historical_scenarios()
validate_historical_scenarios(scenarios)

scenario = scenarios["covid_crash"]

prices = download_market_data(
    tickers=tickers,
    start_date=scenario["start_date"],
    end_date=scenario["end_date"],
)

print(f"\nScenario: {scenario['name']}")
print(
    f"Window: {scenario['start_date']} "
    f"to {scenario['end_date']}"
)

print("\nFirst observations:")
print(prices.head())

print("\nLast observations:")
print(prices.tail())

historical_returns = calculate_historical_returns(prices)

print("\nHistorical Stress Returns:")
print(
    historical_returns
    .sort_values("historical_return")
    .to_string(
        formatters={
            "historical_return": lambda x: f"{x:.2%}",
        }
    )
)

portfolio_info, positions = load_portfolio()

validate_portfolio(
    portfolio_info,
    positions,
)

historical_results = run_historical_stress(
    positions,
    historical_returns,
)

historical_summary = summarize_historical_stress(
    historical_results,
    portfolio_info["nav"],
)

print("\nPosition-Level Historical Stress:")

print(
    historical_results[
        [
            "instrument",
            "asset_class",
            "exposure_usd",
            "historical_return",
            "historical_stress_pnl",
        ]
    ].to_string(
        index=False,
        formatters={
            "historical_return": lambda x: (
                f"{x:.2%}" if not pd.isna(x) else "N/A"
            ),
        },
    )
)

print("\nHistorical Stress Summary:")

print(
    f"Total Stress P&L: "
    f"${historical_summary['total_stress_pnl']:,.0f}"
)

print(
    f"Stress P&L as % of NAV: "
    f"{historical_summary['stress_pnl_pct_nav']:.2f}%"
)

print(
    f"Scenario Coverage: "
    f"{historical_summary['coverage_pct_nav']:.1f}% of NAV"
)