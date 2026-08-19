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

figure_dir = Path("outputs/figures")
figure_dir.mkdir(parents=True, exist_ok=True)

portfolio_info, positions = load_portfolio()
scenarios = load_hypothetical_scenarios()

validate_portfolio(portfolio_info, positions)
validate_hypothetical_scenarios(scenarios)

scenario_results = []

for scenario_id, scenario in scenarios.items():

    position_results, attribution = run_hypothetical_stress(
        positions,
        scenario,
    )

    summary = summarize_hypothetical_stress(
        position_results,
        portfolio_info["nav"],
    )

    scenario_results.append(
        {
            "scenario_id": scenario_id,
            "scenario_name": scenario["name"],
            "stress_pnl": summary["total_stress_pnl"],
            "stress_pnl_pct_nav": summary["stress_pnl_pct_nav"],
        }
    )


scenario_summary = pd.DataFrame(scenario_results)

scenario_summary = scenario_summary.sort_values(
    "stress_pnl"
).reset_index(drop=True)


print("\nScenario Comparison:")
print(scenario_summary.to_string(index=False))

from src.visualization import plot_scenario_comparison

fig = plot_scenario_comparison(scenario_summary)

fig.write_image(
    figure_dir / "hypothetical_scenario_comparison.png",
    width=1400,
    height=800,
    scale=2,
)

fig.show()