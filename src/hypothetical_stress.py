import pandas as pd


DIRECT_RETURN_FACTORS = {
    "SPX",
    "NASDAQ",
    "EU_EQUITY",
    "GOLD",
    "EURUSD",
    "USDJPY",
}

RATE_FACTORS = {
    "USD_5Y_RATE",
    "USD_7Y_RATE",
    "USD_10Y_RATE",
    "USD_20Y_RATE",
}

SPREAD_FACTORS = {
    "IG_SPREAD",
    "HY_SPREAD",
}


def calculate_factor_pnl(position, risk_factor, shock, sensitivity):
    """
    Calculate stressed P&L contribution from one risk factor.
    """
    exposure = position["exposure_usd"]

    if risk_factor in DIRECT_RETURN_FACTORS:
        return exposure * sensitivity * shock

    if risk_factor in RATE_FACTORS:
        duration = position.get("modified_duration")

        if pd.isna(duration):
            raise ValueError(
                f"Missing modified_duration for "
                f"{position['instrument']}."
            )

        return -exposure * duration * sensitivity * shock

    if risk_factor in SPREAD_FACTORS:
        spread_duration = position.get("spread_duration")

        if pd.isna(spread_duration):
            raise ValueError(
                f"Missing spread_duration for "
                f"{position['instrument']}."
            )

        return -exposure * spread_duration * sensitivity * shock

    raise ValueError(
        f"Unsupported risk factor: {risk_factor}"
    )


def calculate_position_stress(position, shocks):
    """
    Calculate total stressed P&L and factor attribution
    for one portfolio position.
    """
    factor_results = []

    for risk_factor, sensitivity in position["risk_factors"].items():
        shock = shocks.get(risk_factor, 0.0)

        factor_pnl = calculate_factor_pnl(
            position=position,
            risk_factor=risk_factor,
            shock=shock,
            sensitivity=sensitivity,
        )

        factor_results.append(
            {
                "instrument": position["instrument"],
                "asset_class": position["asset_class"],
                "risk_factor": risk_factor,
                "sensitivity": sensitivity,
                "shock": shock,
                "factor_pnl": factor_pnl,
            }
        )

    return factor_results


def run_hypothetical_stress(positions, scenario):
    """
    Run one stress scenario and return both position-level
    results and factor-level attribution.
    """
    shocks = scenario["shocks"]

    attribution_rows = []

    for _, position in positions.iterrows():
        attribution_rows.extend(
            calculate_position_stress(position, shocks)
        )

    attribution = pd.DataFrame(attribution_rows)

    position_pnl = (
        attribution.groupby(
            ["instrument", "asset_class"],
            as_index=False,
        )["factor_pnl"]
        .sum()
        .rename(columns={"factor_pnl": "stress_pnl"})
    )

    position_results = positions.merge(
        position_pnl,
        on=["instrument", "asset_class"],
        how="left",
    )

    position_results["stress_return_pct"] = (
        position_results["stress_pnl"]
        / position_results["exposure_usd"]
        * 100
    )

    return position_results, attribution


def summarize_hypothetical_stress(position_results, nav):
    """
    Summarize portfolio-level stress results.
    """
    total_pnl = position_results["stress_pnl"].sum()

    return {
        "total_stress_pnl": total_pnl,
        "stress_pnl_pct_nav": total_pnl / nav * 100,
    }