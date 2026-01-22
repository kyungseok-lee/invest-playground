"""Simulation related Pydantic models for API."""

from datetime import date
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class InvestmentType(str, Enum):
    """Investment type enum."""

    LUMP_SUM = "lump_sum"
    DCA = "dca"


class RebalancingFrequency(str, Enum):
    """Rebalancing frequency enum."""

    NONE = "none"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


class PortfolioItem(BaseModel):
    """Single portfolio item with ticker and weight."""

    ticker: str = Field(..., max_length=10, description="ETF ticker symbol")
    weight: float = Field(..., ge=0, le=100, description="Portfolio weight (%)")


class SimulationRequest(BaseModel):
    """Simulation request model."""

    portfolio: list[PortfolioItem] = Field(
        ..., min_length=1, max_length=5, description="Portfolio items"
    )
    investment_type: InvestmentType = Field(..., description="Investment type")
    initial_amount: float = Field(..., ge=0, description="Initial investment amount")
    monthly_contribution: float = Field(
        0, ge=0, description="Monthly contribution (for DCA)"
    )
    start_date: date = Field(..., description="Simulation start date")
    end_date: date = Field(..., description="Simulation end date")
    rebalancing: RebalancingFrequency = Field(
        RebalancingFrequency.NONE, description="Rebalancing frequency"
    )

    @field_validator("portfolio")
    @classmethod
    def validate_portfolio_weights(cls, v: list[PortfolioItem]) -> list[PortfolioItem]:
        """Validate that portfolio weights sum to 100."""
        total_weight = sum(item.weight for item in v)
        if abs(total_weight - 100) > 0.01:  # Allow small floating point errors
            raise ValueError(f"Portfolio weights must sum to 100, got {total_weight}")
        return v


class MonthlySnapshot(BaseModel):
    """Monthly portfolio snapshot."""

    date: date = Field(..., description="Snapshot date")
    portfolio_value: float = Field(..., description="Total portfolio value")
    invested_amount: float = Field(..., description="Total invested amount")
    dividends_received: float = Field(..., description="Dividends received")


class SimulationSummary(BaseModel):
    """Simulation summary statistics."""

    total_invested: float = Field(..., description="Total invested amount")
    final_value: float = Field(..., description="Final portfolio value")
    total_return_pct: float = Field(..., description="Total return percentage")
    cagr: float = Field(..., description="Compound Annual Growth Rate (%)")
    mdd: float = Field(..., description="Maximum Drawdown (%)")
    total_dividends: float = Field(..., description="Total dividends received")


class SimulationResponse(BaseModel):
    """Simulation response model."""

    summary: SimulationSummary = Field(..., description="Summary statistics")
    monthly_data: list[MonthlySnapshot] = Field(..., description="Monthly snapshots")


class ComparisonScenario(BaseModel):
    """Single comparison scenario."""

    name: str = Field(..., max_length=100, description="Scenario name")
    portfolio: list[PortfolioItem] = Field(..., description="Portfolio items")
    investment_type: InvestmentType = Field(..., description="Investment type")
    initial_amount: float = Field(..., ge=0, description="Initial investment amount")
    monthly_contribution: float = Field(
        0, ge=0, description="Monthly contribution (for DCA)"
    )


class ComparisonRequest(BaseModel):
    """Comparison request model."""

    scenarios: list[ComparisonScenario] = Field(
        ..., min_length=2, max_length=5, description="Scenarios to compare"
    )
    start_date: date = Field(..., description="Comparison start date")
    end_date: date = Field(..., description="Comparison end date")
    rebalancing: RebalancingFrequency = Field(
        RebalancingFrequency.NONE, description="Rebalancing frequency"
    )


class ScenarioResult(BaseModel):
    """Single scenario comparison result."""

    name: str = Field(..., description="Scenario name")
    final_value: float = Field(..., description="Final portfolio value")
    total_invested: float = Field(..., description="Total invested amount")
    total_return_pct: float = Field(..., description="Total return percentage")
    cagr: float = Field(..., description="Compound Annual Growth Rate (%)")
    mdd: float = Field(..., description="Maximum Drawdown (%)")


class ComparisonResponse(BaseModel):
    """Comparison response model."""

    scenarios: list[ScenarioResult] = Field(..., description="Scenario results")
