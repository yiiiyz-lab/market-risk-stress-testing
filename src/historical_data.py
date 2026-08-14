from pathlib import Path

import pandas as pd
import yfinance as yf

from datetime import timedelta


def download_market_data(
    tickers,
    start_date,
    end_date,
    output_path=None,
):
    """
    Download historical adjusted market prices.

    Parameters
    ----------
    tickers : list[str]
        Yahoo Finance tickers.
    start_date : str
        Start date in YYYY-MM-DD format.
    end_date : str
        End date in YYYY-MM-DD format.
    output_path : str | None
        Optional CSV path for saving downloaded data.

    Returns
    -------
    pd.DataFrame
        Adjusted closing prices.
    """
    download_end_date = (
        pd.Timestamp(end_date) + timedelta(days=1)
    ).strftime("%Y-%m-%d")
    
    data = yf.download(
        tickers=tickers,
        start=start_date,
        end=download_end_date,
        auto_adjust=True,
        progress=False,
    )

    if data.empty:
        raise ValueError("No historical market data downloaded.")

    if isinstance(data.columns, pd.MultiIndex):
        prices = data["Close"].copy()
    else:
        prices = data[["Close"]].copy()
        prices.columns = tickers

    prices = prices.dropna(how="all")

    if output_path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        prices.to_csv(path)

    return prices

def calculate_historical_returns(prices):
    """
    Calculate cumulative instrument returns over a historical
    stress window using the first and last available prices.
    """
    start_prices = prices.iloc[0]
    end_prices = prices.iloc[-1]

    returns = end_prices / start_prices - 1

    result = pd.DataFrame(
        {
            "start_price": start_prices,
            "end_price": end_prices,
            "historical_return": returns,
        }
    )

    result.index.name = "instrument"

    return result