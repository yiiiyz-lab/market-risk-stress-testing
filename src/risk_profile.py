import pandas as pd


def build_hypothetical_profile(
    scenario_id,
    scenario,
    position_results,
    attribution,
    nav,
):
    """
    Build a detailed profile for one hypothetical scenario.
    """
    portfolio_pnl = position_results["stress_pnl"].sum()

    position_table = position_results[
        [
            "instrument",
            "asset_class",
            "exposure_usd",
            "stress_pnl",
            "stress_return_pct",
        ]
    ].copy()

    position_table["pnl_pct_nav"] = (
        position_table["stress_pnl"] / nav * 100
    )

    asset_class_table = (
        position_results.groupby(
            "asset_class",
            as_index=False,
        )["stress_pnl"]
        .sum()
    )

    asset_class_table["pnl_pct_nav"] = (
        asset_class_table["stress_pnl"] / nav * 100
    )

    factor_table = (
        attribution.groupby(
            "risk_factor",
            as_index=False,
        )["factor_pnl"]
        .sum()
    )

    factor_table["pnl_pct_nav"] = (
        factor_table["factor_pnl"] / nav * 100
    )

    return {
        "scenario_id": scenario_id,
        "scenario_name": scenario["name"],
        "scenario_type": "Hypothetical",
        "description": scenario.get("description", ""),
        "portfolio_pnl": portfolio_pnl,
        "portfolio_pnl_pct_nav": portfolio_pnl / nav * 100,
        "position_attribution": position_table,
        "asset_class_attribution": asset_class_table,
        "risk_factor_attribution": factor_table,
    }


def build_historical_profile(
    scenario_id,
    scenario,
    results,
    nav,
):
    """
    Build a detailed profile for one historical scenario.
    """
    portfolio_pnl = results["historical_stress_pnl"].sum()

    position_table = results[
        [
            "instrument",
            "asset_class",
            "exposure_usd",
            "historical_return",
            "historical_stress_pnl",
        ]
    ].copy()

    position_table["pnl_pct_nav"] = (
        position_table["historical_stress_pnl"] / nav * 100
    )

    asset_class_table = (
        results.groupby(
            "asset_class",
            as_index=False,
        )["historical_stress_pnl"]
        .sum()
    )

    asset_class_table["pnl_pct_nav"] = (
        asset_class_table["historical_stress_pnl"]
        / nav
        * 100
    )

    return {
        "scenario_id": scenario_id,
        "scenario_name": scenario["name"],
        "scenario_type": "Historical",
        "description": scenario.get("description", ""),
        "start_date": scenario["start_date"],
        "end_date": scenario["end_date"],
        "portfolio_pnl": portfolio_pnl,
        "portfolio_pnl_pct_nav": portfolio_pnl / nav * 100,
        "position_attribution": position_table,
        "asset_class_attribution": asset_class_table,
        "risk_factor_attribution": None,
    }


def build_scenario_ranking(scenario_profiles):
    """
    Build portfolio-level ranking across all scenarios.
    """
    rows = []

    for profile in scenario_profiles:
        rows.append(
            {
                "scenario_id": profile["scenario_id"],
                "scenario_name": profile["scenario_name"],
                "scenario_type": profile["scenario_type"],
                "portfolio_pnl": profile["portfolio_pnl"],
                "portfolio_pnl_pct_nav": (
                    profile["portfolio_pnl_pct_nav"]
                ),
            }
        )

    return (
        pd.DataFrame(rows)
        .sort_values("portfolio_pnl_pct_nav")
        .reset_index(drop=True)
    )


def build_asset_class_matrix(scenario_profiles):
    """
    Build scenario x asset-class P&L contribution matrix.
    """
    rows = []

    for profile in scenario_profiles:
        table = profile["asset_class_attribution"]

        pnl_column = (
            "stress_pnl"
            if profile["scenario_type"] == "Hypothetical"
            else "historical_stress_pnl"
        )

        for _, row in table.iterrows():
            rows.append(
                {
                    "scenario_name": profile["scenario_name"],
                    "scenario_type": profile["scenario_type"],
                    "asset_class": row["asset_class"],
                    "pnl": row[pnl_column],
                    "pnl_pct_nav": row["pnl_pct_nav"],
                }
            )

    long_table = pd.DataFrame(rows)

    matrix = long_table.pivot(
        index="asset_class",
        columns="scenario_name",
        values="pnl_pct_nav",
    )

    return long_table, matrix


def calculate_loss_concentration(
    attribution_table,
    pnl_column,
):
    """
    Share of total negative contribution from the largest loss bucket.
    """
    negative = attribution_table[
        attribution_table[pnl_column] < 0
    ]

    if negative.empty:
        return 0.0

    total_negative = negative[pnl_column].abs().sum()
    largest_negative = negative[pnl_column].abs().max()

    return largest_negative / total_negative * 100


def build_executive_summary(scenario_profiles):
    """
    Extract headline portfolio risk conclusions.
    """
    ranking = build_scenario_ranking(scenario_profiles)

    historical = ranking[
        ranking["scenario_type"] == "Historical"
    ]

    hypothetical = ranking[
        ranking["scenario_type"] == "Hypothetical"
    ]

    worst_historical = historical.iloc[0]
    worst_hypothetical = hypothetical.iloc[0]

    return {
        "worst_historical": worst_historical.to_dict(),
        "worst_hypothetical": worst_hypothetical.to_dict(),
    }


def build_cross_scenario_profile(scenario_profiles):
    """
    Build reusable cross-scenario analytics.
    """
    ranking = build_scenario_ranking(scenario_profiles)

    asset_class_long, asset_class_matrix = (
        build_asset_class_matrix(scenario_profiles)
    )

    return {
        "scenario_ranking": ranking,
        "asset_class_long": asset_class_long,
        "asset_class_matrix": asset_class_matrix,
    }