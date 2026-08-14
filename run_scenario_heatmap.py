import pandas as pd

from src.portfolio import load_portfolio, validate_portfolio
from src.scenarios import load_scenarios, validate_scenarios
from src.stress_engine import run_stress_scenario
from src.visualization import plot_scenario_heatmap


portfolio_info, positions = load_portfolio()
scenarios = load_scenarios()

validate_portfolio(portfolio_info, positions)
validate_scenarios(scenarios)

rows = []

for scenario_id, scenario in scenarios.items():

    position_results, attribution = run_stress_scenario(
        positions,
        scenario,
    )

    asset_class_summary = (
        position_results.groupby(
            "asset_class",
            as_index=False,
        )["stress_pnl"]
        .sum()
    )

    asset_class_summary["pnl_pct_nav"] = (
        asset_class_summary["stress_pnl"]
        / portfolio_info["nav"]
        * 100
    )

    for _, row in asset_class_summary.iterrows():
        rows.append(
            {
                "scenario_id": scenario_id,
                "scenario_name": scenario["name"],
                "asset_class": row["asset_class"],
                "pnl_pct_nav": row["pnl_pct_nav"],
            }
        )


scenario_asset_class = pd.DataFrame(rows)

heatmap_data = scenario_asset_class.pivot(
    index="asset_class",
    columns="scenario_name",
    values="pnl_pct_nav",
)

print("\nScenario × Asset-Class P&L (% NAV):")
print(heatmap_data.round(2).to_string())

fig = plot_scenario_heatmap(heatmap_data)
fig.show()