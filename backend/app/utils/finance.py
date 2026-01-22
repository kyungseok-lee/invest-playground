"""Financial calculation utilities."""

import numpy as np
import pandas as pd


def calculate_cagr(
    initial_value: float, final_value: float, years: float
) -> float:
    """
    Calculate Compound Annual Growth Rate (CAGR).

    Args:
        initial_value: Initial investment value
        final_value: Final portfolio value
        years: Number of years

    Returns:
        CAGR as a percentage
    """
    if initial_value <= 0 or years <= 0:
        return 0.0

    cagr = (pow(final_value / initial_value, 1 / years) - 1) * 100
    return round(cagr, 2)


def calculate_mdd(values: list[float]) -> float:
    """
    Calculate Maximum Drawdown (MDD).

    Args:
        values: List of portfolio values over time

    Returns:
        MDD as a percentage (negative value)
    """
    if not values:
        return 0.0

    arr = np.array(values)
    running_max = np.maximum.accumulate(arr)
    drawdowns = (arr - running_max) / running_max * 100

    mdd = np.min(drawdowns)
    return round(float(mdd), 2)


def calculate_total_return(
    initial_value: float, final_value: float
) -> float:
    """
    Calculate total return percentage.

    Args:
        initial_value: Initial investment value
        final_value: Final portfolio value

    Returns:
        Total return as a percentage
    """
    if initial_value <= 0:
        return 0.0

    return round(((final_value - initial_value) / initial_value) * 100, 2)


def get_years_between_dates(start_date: pd.Timestamp, end_date: pd.Timestamp) -> float:
    """
    Calculate years between two dates.

    Args:
        start_date: Start date
        end_date: End date

    Returns:
        Number of years as a float
    """
    days = (end_date - start_date).days
    return days / 365.25
