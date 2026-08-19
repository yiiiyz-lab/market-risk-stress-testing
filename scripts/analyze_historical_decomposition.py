from pathlib import Path

import pandas as pd

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

output_dir = Path("outputs/tables")
output_dir.mkdir(parents=True, exist_ok=True)

position_tables = []
asset_class_tables = []


for scenario_id, scenario in scenarios.items():

    prices = download_market_data(
        tickers=tickers,
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

    summary = summarize_historical_stress(
        results,
        portfolio_info["nav"],
    )

    print("\n")
    print("=" * 80)
    print(
        f"{scenario['name']} "
        f"[{scenario_id}]"
    )
    print("=" * 80)

    print(
        f"\nWindow: "
        f"{scenario['start_date']} "
        f"to {scenario['end_date']}"
    )

    print(
        f"\nPortfolio Stress P&L: "
        f"${summary['total_stress_pnl']:,.0f} "
        f"({summary['stress_pnl_pct_nav']:.2f}% NAV)"
    )

    # --------------------------------------------------
    # Position-Level Attribution
    # --------------------------------------------------

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

    position_output["scenario_id"] = scenario_id
    position_output["scenario_name"] = scenario["name"]

    position_tables.append(position_output)

    print("\nPosition-Level Attribution:")

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

    # --------------------------------------------------
    # Asset-Class Attribution
    # --------------------------------------------------

    asset_class_summary = (
        results.groupby(
            "asset_class",
            as_index=False,
        )["historical_stress_pnl"]
        .sum()
        .sort_values("historical_stress_pnl")
    )

    asset_class_summary["pnl_pct_nav"] = (
        asset_class_summary["historical_stress_pnl"]
        / portfolio_info["nav"]
        * 100
    )

    asset_class_summary["scenario_id"] = scenario_id
    asset_class_summary["scenario_name"] = scenario["name"]

    asset_class_tables.append(asset_class_summary)

    print("\nAsset-Class Attribution:")

    print(
        asset_class_summary.to_string(
            index=False,
            formatters={
                "historical_stress_pnl": lambda x: f"${x:,.0f}",
                "pnl_pct_nav": lambda x: f"{x:.2f}%",
            },
        )
    )


# ------------------------------------------------------
# Consolidated Output Tables
# ------------------------------------------------------

all_positions = pd.concat(
    position_tables,
    ignore_index=True,
)

all_asset_classes = pd.concat(
    asset_class_tables,
    ignore_index=True,
)


all_positions.to_csv(
    output_dir / "historical_position_attribution.csv",
    index=False,
)

all_asset_classes.to_csv(
    output_dir / "historical_asset_class_attribution.csv",
    index=False,
)


print("\n")
print("=" * 80)
print("Historical decomposition tables saved")
print("=" * 80)

print(
    "\nSaved:"
    "\n- outputs/tables/historical_position_attribution.csv"
    "\n- outputs/tables/historical_asset_class_attribution.csv"
)