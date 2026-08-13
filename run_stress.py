from src.portfolio import load_portfolio, validate_portfolio
from src.scenarios import load_scenarios, validate_scenarios
from src.stress_engine import run_stress_scenario, summarize_stress


portfolio_info, positions = load_portfolio()
scenarios = load_scenarios()

validate_portfolio(portfolio_info, positions)
validate_scenarios(scenarios)

scenario_id = "risk_off"
scenario = scenarios[scenario_id]

results, attribution = run_stress_scenario(
    positions,
    scenario,
)

summary = summarize_stress(
    results,
    portfolio_info["nav"],
)

print(f"\nScenario: {scenario['name']}")

print("\nPosition-Level Stress Results:")
print(
    results[
        [
            "instrument",
            "asset_class",
            "exposure_usd",
            "stress_pnl",
            "stress_return_pct",
        ]
    ]
)

print("\nPortfolio Stress Summary:")
print(
    f"Total Stress P&L: "
    f"${summary['total_stress_pnl']:,.0f}"
)

print(
    f"Stress P&L as % of NAV: "
    f"{summary['stress_pnl_pct_nav']:.2f}%"
)

print("\nFactor-Level Attribution:")
print(
    attribution[
        [
            "instrument",
            "risk_factor",
            "sensitivity",
            "shock",
            "factor_pnl",
        ]
    ]
)

print("\nRisk-Factor Summary:")
factor_summary = (
    attribution.groupby("risk_factor")["factor_pnl"]
    .sum()
    .sort_values()
)

print(factor_summary)