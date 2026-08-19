from src.hypothetical_scenarios import (
    load_hypothetical_scenarios,
    validate_hypothetical_scenarios,
)
from src.hypothetical_stress import run_hypothetical_stress
from src.portfolio import load_portfolio, validate_portfolio

from pathlib import Path

import pandas as pd

portfolio_info, positions = load_portfolio()
scenarios = load_hypothetical_scenarios()

validate_portfolio(portfolio_info, positions)
validate_hypothetical_scenarios(scenarios)

output_dir = Path("outputs/tables")
output_dir.mkdir(parents=True, exist_ok=True)

position_tables = []
asset_class_tables = []
factor_tables = []


for scenario_id, scenario in scenarios.items():

    position_results, attribution = run_hypothetical_stress(
        positions,
        scenario,
    )

    asset_class_summary = (
        position_results.groupby(
            "asset_class",
            as_index=False,
        )["stress_pnl"]
        .sum()
        .sort_values("stress_pnl")
    )

    asset_class_summary["pnl_pct_nav"] = (
        asset_class_summary["stress_pnl"]
        / portfolio_info["nav"]
        * 100
    )

    factor_summary = (
        attribution.groupby(
            "risk_factor",
            as_index=False,
        )["factor_pnl"]
        .sum()
        .sort_values("factor_pnl")
    )

    factor_summary["pnl_pct_nav"] = (
        factor_summary["factor_pnl"]
        / portfolio_info["nav"]
        * 100
    )

    total_pnl = position_results["stress_pnl"].sum()

    print("\n")
    print("=" * 80)
    print(
        f"{scenario['name']} "
        f"[{scenario_id}]"
    )
    print("=" * 80)

    print(
        f"\nPortfolio Stress P&L: "
        f"${total_pnl:,.0f} "
        f"({total_pnl / portfolio_info['nav'] * 100:.2f}% NAV)"
    )

    print("\nPosition Attribution:")

    position_output = position_results[
        [
            "instrument",
            "asset_class",
            "exposure_usd",
            "stress_pnl",
            "stress_return_pct",
        ]
    ].copy()

    position_output["pnl_pct_nav"] = (
        position_output["stress_pnl"]
        / portfolio_info["nav"]
        * 100
    )

    position_output["scenario_id"] = scenario_id
    position_output["scenario_name"] = scenario["name"]
    position_tables.append(position_output)

    asset_class_summary["scenario_id"] = scenario_id
    asset_class_summary["scenario_name"] = scenario["name"]
    asset_class_tables.append(asset_class_summary)

    factor_summary["scenario_id"] = scenario_id
    factor_summary["scenario_name"] = scenario["name"]
    factor_tables.append(factor_summary)

    print(
        position_output.sort_values(
            "stress_pnl"
        ).to_string(
            index=False,
            formatters={
                "stress_pnl": lambda x: f"${x:,.0f}",
                "stress_return_pct": lambda x: f"{x:.2f}%",
                "pnl_pct_nav": lambda x: f"{x:.2f}%",
            },
        )
    )

    print("\nAsset-Class Attribution:")

    print(
        asset_class_summary.to_string(
            index=False,
            formatters={
                "stress_pnl": lambda x: f"${x:,.0f}",
                "pnl_pct_nav": lambda x: f"{x:.2f}%",
            },
        )
    )

    print("\nRisk-Factor Attribution:")

    print(
        factor_summary.to_string(
            index=False,
            formatters={
                "factor_pnl": lambda x: f"${x:,.0f}",
                "pnl_pct_nav": lambda x: f"{x:.2f}%",
            },
        )
    )

all_positions = pd.concat(
    position_tables,
    ignore_index=True,
)

all_asset_classes = pd.concat(
    asset_class_tables,
    ignore_index=True,
)

all_factors = pd.concat(
    factor_tables,
    ignore_index=True,
)

all_positions.to_csv(
    output_dir / "hypothetical_position_attribution.csv",
    index=False,
)

all_asset_classes.to_csv(
    output_dir / "hypothetical_asset_class_attribution.csv",
    index=False,
)

all_factors.to_csv(
    output_dir / "hypothetical_risk_factor_attribution.csv",
    index=False,
)