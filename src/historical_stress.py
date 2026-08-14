import pandas as pd

HISTORICAL_TICKER_MAP = {
    "EURUSD": "EURUSD=X",
    "USDJPY": "USDJPY=X",
}

def run_historical_stress(positions, historical_returns):
    """
    Apply observed historical instrument returns to the current portfolio.

    Historical stress P&L:
        exposure × observed historical return
    """
    results = positions.copy()

    return_map = historical_returns["historical_return"].to_dict()

    results["historical_ticker"] = results["instrument"].replace(
        HISTORICAL_TICKER_MAP
    )

    results["historical_return"] = (
        results["historical_ticker"].map(return_map)
    )

    results["historical_stress_pnl"] = (
        results["exposure_usd"]
        * results["historical_return"]
    )

    return results


def summarize_historical_stress(results, nav):
    """
    Summarize portfolio-level historical stress results.
    """
    covered_results = results.dropna(
        subset=["historical_stress_pnl"]
    )

    total_pnl = covered_results["historical_stress_pnl"].sum()

    covered_exposure = covered_results["exposure_usd"].sum()

    return {
        "total_stress_pnl": total_pnl,
        "stress_pnl_pct_nav": total_pnl / nav * 100,
        "covered_exposure": covered_exposure,
        "coverage_pct_nav": covered_exposure / nav * 100,
    }