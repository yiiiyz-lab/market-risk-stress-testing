from pathlib import Path

import pandas as pd
import yaml


def load_portfolio(config_path: str = "config/portfolio.yaml"):
    """
    Load portfolio metadata and positions from a YAML configuration file.
    """
    path = Path(config_path)

    with path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    portfolio_info = config["portfolio"]
    positions = pd.DataFrame(config["positions"])

    return portfolio_info, positions


def validate_portfolio(portfolio_info, positions):
    """
    Validate basic portfolio consistency.
    """
    nav = portfolio_info["nav"]
    total_exposure = positions["exposure_usd"].sum()

    if total_exposure != nav:
        raise ValueError(
            f"Portfolio exposure mismatch: "
            f"positions total ${total_exposure:,.0f}, "
            f"but NAV is ${nav:,.0f}."
        )

    return True


def portfolio_summary(positions):
    """
    Summarize portfolio exposure by asset class.
    """
    summary = (
        positions.groupby("asset_class", as_index=False)["exposure_usd"]
        .sum()
        .sort_values("exposure_usd", ascending=False)
    )

    summary["weight_pct"] = (
        summary["exposure_usd"] / summary["exposure_usd"].sum() * 100
    )

    return summary