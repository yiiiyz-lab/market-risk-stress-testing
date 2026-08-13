import pandas as pd

from src.portfolio import load_portfolio, validate_portfolio
from src.scenarios import load_scenarios, validate_scenarios
from src.stress_engine import run_stress_scenario, summarize_stress


portfolio_info, positions = load_portfolio()
scenarios = load_scenarios()

validate_portfolio(portfolio_info, positions)
validate_scenarios(scenarios)

scenario_results = []

for scenario_id, scenario in scenarios.items():

    position_results, attribution = run_stress_scenario(
        positions,
        scenario,
    )

    summary = summarize_stress(
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
fig.show()