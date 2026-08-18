from src.portfolio import load_portfolio, validate_portfolio
from src.hypothetical_scenarios import (
    load_hypothetical_scenarios,
    validate_hypothetical_scenarios,
)
from src.hypothetical_stress import (
    run_hypothetical_stress,
)
from src.visualization import (
    plot_asset_class_attribution,
    plot_factor_attribution,
)


portfolio_info, positions = load_portfolio()
scenarios = load_hypothetical_scenarios()

validate_portfolio(portfolio_info, positions)
validate_hypothetical_scenarios(scenarios)

scenario = scenarios["stagflation"]

position_results, attribution = run_hypothetical_stress(
    positions,
    scenario,
)

asset_class_summary = (
    position_results.groupby("asset_class", as_index=False)["stress_pnl"]
    .sum()
    .sort_values("stress_pnl")
)

asset_class_summary["pnl_pct_nav"] = (
    asset_class_summary["stress_pnl"]
    / portfolio_info["nav"]
    * 100
)

factor_summary = (
    attribution.groupby("risk_factor", as_index=False)["factor_pnl"]
    .sum()
    .sort_values("factor_pnl")
)

factor_summary["pnl_pct_nav"] = (
    factor_summary["factor_pnl"]
    / portfolio_info["nav"]
    * 100
)

print(f"\nScenario: {scenario['name']}")

print("\nAsset-Class Attribution:")
print(asset_class_summary.to_string(index=False))

print("\nRisk-Factor Attribution:")
print(factor_summary.to_string(index=False))

asset_class_fig = plot_asset_class_attribution(
    asset_class_summary,
    scenario["name"],
)

asset_class_fig.show()


factor_fig = plot_factor_attribution(
    factor_summary,
    scenario["name"],
)

factor_fig.show()