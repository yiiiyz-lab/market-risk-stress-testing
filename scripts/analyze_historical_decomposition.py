from src.historical_data import (
    calculate_historical_returns,
    download_market_data,
)
from src.historical_scenarios import (
    load_historical_scenarios,
)
from src.historical_stress import (
    run_historical_stress,
    summarize_historical_stress,
)
from src.portfolio import load_portfolio


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


portfolio_info, positions = load_portfolio()
scenarios = load_historical_scenarios()

scenario = scenarios["regional_banking_stress"]

prices = download_market_data(
    tickers=tickers,
    start_date=scenario["start_date"],
    end_date=scenario["end_date"],
)

historical_returns = calculate_historical_returns(prices)

results = run_historical_stress(
    positions,
    historical_returns,
)

summary = summarize_historical_stress(
    results,
    portfolio_info["nav"],
)


print(f"\nScenario: {scenario['name']}")
print(
    f"Window: {scenario['start_date']} "
    f"to {scenario['end_date']}"
)


print("\nPosition-Level Attribution:")

position_output = results[
    [
        "instrument",
        "asset_class",
        "exposure_usd",
        "historical_return",
        "historical_stress_pnl",
    ]
].copy()

position_output["pnl_pct_nav"] = (
    position_output["historical_stress_pnl"]
    / portfolio_info["nav"]
    * 100
)

print(
    position_output.sort_values(
        "historical_stress_pnl"
    ).to_string(
        index=False,
        formatters={
            "historical_return": lambda x: f"{x:.2%}",
            "historical_stress_pnl": lambda x: f"${x:,.0f}",
            "pnl_pct_nav": lambda x: f"{x:.2f}%",
        },
    )
)


asset_class_summary = (
    results.groupby(
        "asset_class",
        as_index=False,
    )["historical_stress_pnl"]
    .sum()
)

asset_class_summary["pnl_pct_nav"] = (
    asset_class_summary["historical_stress_pnl"]
    / portfolio_info["nav"]
    * 100
)

print("\nAsset-Class Attribution:")

print(
    asset_class_summary.sort_values(
        "historical_stress_pnl"
    ).to_string(
        index=False,
        formatters={
            "historical_stress_pnl": lambda x: f"${x:,.0f}",
            "pnl_pct_nav": lambda x: f"{x:.2f}%",
        },
    )
)


print("\nPortfolio Summary:")
print(
    f"Total Stress P&L: "
    f"${summary['total_stress_pnl']:,.0f}"
)

print(
    f"Stress P&L as % of NAV: "
    f"{summary['stress_pnl_pct_nav']:.2f}%"
)