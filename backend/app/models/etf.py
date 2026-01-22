"""ETF related Pydantic models for API."""

from datetime import date

from pydantic import BaseModel, Field


class ETFBase(BaseModel):
    """Base ETF model."""

    ticker: str = Field(..., max_length=10, description="ETF ticker symbol")
    name: str = Field(..., max_length=255, description="ETF name")
    category: str | None = Field(None, max_length=100, description="ETF category")


class ETFSearchResult(ETFBase):
    """ETF search result model."""

    pass


class ETFDetail(ETFBase):
    """Detailed ETF information."""

    expense_ratio: float | None = Field(None, description="Expense ratio (%)")
    dividend_yield: float | None = Field(None, description="Dividend yield (%)")
    inception_date: date | None = Field(None, description="ETF inception date")
    aum: int | None = Field(None, description="Assets under management (USD)")
    description: str | None = Field(None, description="ETF description")


class PriceData(BaseModel):
    """Single price data point."""

    date: date = Field(..., description="Date of the price")
    close: float = Field(..., description="Closing price")
    adj_close: float = Field(..., description="Adjusted closing price")
    dividend: float = Field(0.0, description="Dividend amount")


class ETFHistory(BaseModel):
    """ETF price history response."""

    ticker: str = Field(..., description="ETF ticker symbol")
    prices: list[PriceData] = Field(..., description="List of price data")


class ETFSearchResponse(BaseModel):
    """ETF search response."""

    results: list[ETFSearchResult] = Field(..., description="List of search results")
