import pandas as pd

from src.historical_data import (
    calculate_historical_returns,
    download_market_data,
)
from src.historical_scenarios import (
    load_historical_scenarios,
    validate_historical_scenarios,
)
from src.historical_stress import (
    run_historical_stress,
    summarize_historical_stress,
)
from src.portfolio import load_portfolio, validate_portfolio


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
historical_scenarios = load_historical_scenarios()

validate_portfolio(portfolio_info, positions)
validate_historical_scenarios(historical_scenarios)

scenario_results = []

for scenario_id, scenario in historical_scenarios.items():

    prices = download_market_data(
        tickers=tickers,
        start_date=scenario["start_date"],
        end_date=scenario["end_date"],
    )

    historical_returns = calculate_historical_returns(prices)

    position_results = run_historical_stress(
        positions,
        historical_returns,
    )

    summary = summarize_historical_stress(
        position_results,
        portfolio_info["nav"],
    )

    scenario_results.append(
        {
            "scenario_id": scenario_id,
            "scenario_name": scenario["name"],
            "start_date": scenario["start_date"],
            "end_date": scenario["end_date"],
            "stress_pnl": summary["total_stress_pnl"],
            "stress_pnl_pct_nav": summary["stress_pnl_pct_nav"],
            "coverage_pct_nav": summary["coverage_pct_nav"],
        }
    )


historical_summary = pd.DataFrame(scenario_results)

historical_summary = historical_summary.sort_values(
    "stress_pnl"
).reset_index(drop=True)

print("\nHistorical Stress Scenario Comparison:")
print(
    historical_summary.to_string(
        index=False,
        formatters={
            "stress_pnl": lambda x: f"${x:,.0f}",
            "stress_pnl_pct_nav": lambda x: f"{x:.2f}%",
            "coverage_pct_nav": lambda x: f"{x:.1f}%",
        },
    )
)