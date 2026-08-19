import pandas as pd
from pathlib import Path

from src.portfolio import load_portfolio, validate_portfolio
from src.hypothetical_scenarios import (
    load_hypothetical_scenarios,
    validate_hypothetical_scenarios,
)
from src.hypothetical_stress import (
    run_hypothetical_stress,
    summarize_hypothetical_stress,
)
from src.historical_data import (
    download_market_data,
    calculate_historical_returns,
)
from src.historical_scenarios import (
    load_historical_scenarios,
    validate_historical_scenarios,
)
from src.historical_stress import (
    run_historical_stress,
    summarize_historical_stress,
)

from src.visualization import plot_stress_comparison

figure_dir = Path("outputs/figures")
figure_dir.mkdir(parents=True, exist_ok=True)

portfolio_info, positions = load_portfolio()

hypothetical_scenarios = load_hypothetical_scenarios()
historical_scenarios = load_historical_scenarios()

validate_portfolio(portfolio_info, positions)
validate_hypothetical_scenarios(hypothetical_scenarios)
validate_historical_scenarios(historical_scenarios)

comparison_rows = []


for scenario_id, scenario in hypothetical_scenarios.items():

    position_results, attribution = run_hypothetical_stress(
        positions,
        scenario,
    )

    summary = summarize_hypothetical_stress(
        position_results,
        portfolio_info["nav"],
    )

    comparison_rows.append(
        {
            "scenario_id": scenario_id,
            "scenario_name": scenario["name"],
            "scenario_type": "Hypothetical",
            "stress_pnl": summary["total_stress_pnl"],
            "stress_pnl_pct_nav": summary["stress_pnl_pct_nav"],
        }
    )

historical_tickers = [
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

for scenario_id, scenario in historical_scenarios.items():

    prices = download_market_data(
        tickers=historical_tickers,
        start_date=scenario["start_date"],
        end_date=scenario["end_date"],
    )

    historical_returns = calculate_historical_returns(
        prices
    )

    position_results = run_historical_stress(
        positions,
        historical_returns,
    )

    summary = summarize_historical_stress(
        position_results,
        portfolio_info["nav"],
    )

    comparison_rows.append(
        {
            "scenario_id": scenario_id,
            "scenario_name": scenario["name"],
            "scenario_type": "Historical",
            "stress_pnl": summary["total_stress_pnl"],
            "stress_pnl_pct_nav": summary["stress_pnl_pct_nav"],
        }
    )

comparison = pd.DataFrame(comparison_rows)

comparison = comparison.sort_values(
    "stress_pnl_pct_nav"
).reset_index(drop=True)

print("\nHistorical vs Hypothetical Stress Comparison:")

print(
    comparison[
        [
            "scenario_name",
            "scenario_type",
            "stress_pnl",
            "stress_pnl_pct_nav",
        ]
    ].to_string(
        index=False,
        formatters={
            "stress_pnl": lambda x: f"${x:,.0f}",
            "stress_pnl_pct_nav": lambda x: f"{x:.2f}%",
        },
    )
)

fig = plot_stress_comparison(comparison)

fig.write_image(
    figure_dir / "historical_vs_hypothetical.png",
    width=1500,
    height=850,
    scale=2,
)

fig.show()