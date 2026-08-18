import pandas as pd

from src.historical_data import (
    calculate_historical_returns,
    download_market_data,
)
from src.historical_scenarios import (
    load_historical_scenarios,
)
from src.historical_stress import run_historical_stress
from src.portfolio import load_portfolio
from src.risk_profile import (
    build_cross_scenario_profile,
    build_executive_summary,
    build_historical_profile,
    build_hypothetical_profile,
)
from src.hypothetical_scenarios import (
    load_hypothetical_scenarios,
)
from src.hypothetical_stress import (
    run_hypothetical_stress,
)


portfolio_info, positions = load_portfolio()

hypothetical_scenarios = load_hypothetical_scenarios()
historical_scenarios = load_historical_scenarios()

scenario_profiles = []

for scenario_id, scenario in hypothetical_scenarios.items():

    position_results, attribution = run_hypothetical_stress(
        positions,
        scenario,
    )

    profile = build_hypothetical_profile(
        scenario_id=scenario_id,
        scenario=scenario,
        position_results=position_results,
        attribution=attribution,
        nav=portfolio_info["nav"],
    )

    scenario_profiles.append(profile)

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

    results = run_historical_stress(
        positions,
        historical_returns,
    )

    profile = build_historical_profile(
        scenario_id=scenario_id,
        scenario=scenario,
        results=results,
        nav=portfolio_info["nav"],
    )

    scenario_profiles.append(profile)

executive_summary = build_executive_summary(
    scenario_profiles
)

cross_scenario = build_cross_scenario_profile(
    scenario_profiles
)

print("\nEXECUTIVE SUMMARY")
print("=" * 70)

worst_hist = executive_summary["worst_historical"]

print(
    f"\nWorst Historical Scenario: "
    f"{worst_hist['scenario_name']} "
    f"{worst_hist['portfolio_pnl_pct_nav']:.2f}%"
)

worst_hyp = executive_summary["worst_hypothetical"]

print(
    f"Worst Hypothetical Scenario: "
    f"{worst_hyp['scenario_name']} "
    f"{worst_hyp['portfolio_pnl_pct_nav']:.2f}%"
)

for profile in scenario_profiles:

    print("\n")
    print("=" * 70)
    print(
        f"{profile['scenario_name']} "
        f"[{profile['scenario_type']}]"
    )
    print("=" * 70)

    print(
        f"\nPortfolio P&L: "
        f"${profile['portfolio_pnl']:,.0f} "
        f"({profile['portfolio_pnl_pct_nav']:.2f}% NAV)"
    )

    print("\nAsset-Class Attribution:")

    asset_class_table = profile[
        "asset_class_attribution"
    ].sort_values("pnl_pct_nav")

    print(
        asset_class_table.to_string(
            index=False,
            formatters={
                "pnl_pct_nav": lambda x: f"{x:.2f}%",
            },
        )
    )

    print("\nPosition Attribution:")

    position_table = profile[
        "position_attribution"
    ].sort_values("pnl_pct_nav")

    print(
        position_table.to_string(
            index=False,
            formatters={
                "pnl_pct_nav": lambda x: f"{x:.2f}%",
            },
        )
    )

    if profile["risk_factor_attribution"] is not None:

        print("\nRisk-Factor Attribution:")

        factor_table = profile[
            "risk_factor_attribution"
        ].sort_values("pnl_pct_nav")

        print(
            factor_table.to_string(
                index=False,
                formatters={
                    "pnl_pct_nav": lambda x: f"{x:.2f}%",
                },
            )
        )

print("\n")
print("=" * 70)
print("CROSS-SCENARIO RISK PROFILE")
print("=" * 70)

print("\nScenario Ranking:")

print(
    cross_scenario[
        "scenario_ranking"
    ].to_string(
        index=False,
        formatters={
            "portfolio_pnl": lambda x: f"${x:,.0f}",
            "portfolio_pnl_pct_nav": lambda x: f"{x:.2f}%",
        },
    )
)

print("\nAsset-Class × Scenario Matrix (% NAV):")

print(
    cross_scenario[
        "asset_class_matrix"
    ].round(2).to_string()
)
