import yfinance as yf
import numpy as np
from typing import Optional, Tuple, List


def get_price_change(
    ticker: str,
    lookback: Optional[str] = "2d"
) -> Tuple[float, List]:
    """Gets price change for a particular ticker
    Args:
        ticker (str): Ticker of interest. E.g., BABA or Y92.SI
        lookback (str, optional): Price change period to evaluate on.
            Defaults to "2d".
    Returns:
        Tuple[float, List]: Percentage change in float.
    """

    stock = yf.Ticker(ticker)
    hist = stock.history(period=lookback).Close.values.tolist()
    # If not updated yet
    if len(hist) != int(lookback[0]):
        lookback = f"{int(lookback[0])+1}d"
        hist = stock.history(period=lookback).Close.values.tolist()

    if not hist:
        return f"Couldn't find history for ticker {ticker}", None
    pct_chng = ((hist[-1] - hist[0]) / hist[0]) * 100

    return np.round(pct_chng, 2), hist
