"""Portfolio simulation service."""

from datetime import date, timedelta

import pandas as pd
from sqlalchemy.orm import Session

from app.models.simulation import (
    InvestmentType,
    MonthlySnapshot,
    PortfolioItem,
    RebalancingFrequency,
    SimulationSummary,
)
from app.services.etf_service import ETFService
from app.utils.finance import (
    calculate_cagr,
    calculate_mdd,
    calculate_total_return,
    get_years_between_dates,
)


class SimulationService:
    """Service for portfolio simulation operations."""

    def __init__(self, db: Session):
        """Initialize simulation service with database session."""
        self.db = db
        self.etf_service = ETFService(db)

    def run_simulation(
        self,
        portfolio: list[PortfolioItem],
        investment_type: InvestmentType,
        initial_amount: float,
        monthly_contribution: float,
        start_date: date,
        end_date: date,
        rebalancing: RebalancingFrequency,
    ) -> tuple[SimulationSummary, list[MonthlySnapshot]]:
        """
        Run investment simulation.

        Args:
            portfolio: List of portfolio items with ticker and weight
            investment_type: Type of investment (lump_sum or dca)
            initial_amount: Initial investment amount
            monthly_contribution: Monthly contribution for DCA
            start_date: Simulation start date
            end_date: Simulation end date
            rebalancing: Rebalancing frequency

        Returns:
            Tuple of (simulation summary, monthly snapshots)
        """
        # Fetch price data for all tickers
        price_data = self._fetch_portfolio_prices(portfolio, start_date, end_date)

        if not price_data:
            raise ValueError("Failed to fetch price data for portfolio")

        # Run simulation based on investment type
        if investment_type == InvestmentType.LUMP_SUM:
            return self._simulate_lump_sum(
                portfolio, initial_amount, price_data, start_date, end_date, rebalancing
            )
        else:
            return self._simulate_dca(
                portfolio,
                initial_amount,
                monthly_contribution,
                price_data,
                start_date,
                end_date,
                rebalancing,
            )

    def _fetch_portfolio_prices(
        self, portfolio: list[PortfolioItem], start_date: date, end_date: date
    ) -> dict[str, pd.DataFrame]:
        """Fetch price data for all tickers in portfolio."""
        price_data = {}

        for item in portfolio:
            prices = self.etf_service.get_price_history(
                item.ticker, start_date, end_date
            )

            if not prices:
                continue

            # Convert to DataFrame
            df = pd.DataFrame([p.model_dump() for p in prices])
            df["date"] = pd.to_datetime(df["date"])
            df.set_index("date", inplace=True)
            df.sort_index(inplace=True)

            price_data[item.ticker] = df

        return price_data

    def _simulate_lump_sum(
        self,
        portfolio: list[PortfolioItem],
        initial_amount: float,
        price_data: dict[str, pd.DataFrame],
        start_date: date,
        end_date: date,
        rebalancing: RebalancingFrequency,
    ) -> tuple[SimulationSummary, list[MonthlySnapshot]]:
        """Simulate lump sum investment."""
        # Get all unique dates
        all_dates = sorted(
            set().union(*[set(df.index) for df in price_data.values()])
        )

        if not all_dates:
            raise ValueError("No price data available")

        # Initialize portfolio with initial investment
        shares = {}
        for item in portfolio:
            if item.ticker not in price_data:
                continue

            allocation = initial_amount * (item.weight / 100)
            first_price = price_data[item.ticker].iloc[0]["adj_close"]
            shares[item.ticker] = allocation / first_price

        # Track portfolio value over time
        portfolio_values = []
        invested_amounts = []
        total_dividends = 0.0
        monthly_snapshots = []

        last_rebalance_date = all_dates[0]

        for current_date in all_dates:
            # Calculate current portfolio value
            portfolio_value = 0.0
            for ticker, num_shares in shares.items():
                if ticker not in price_data:
                    continue

                df = price_data[ticker]
                if current_date not in df.index:
                    continue

                current_price = df.loc[current_date]["adj_close"]
                portfolio_value += num_shares * current_price

                # Add dividends
                dividend = df.loc[current_date]["dividend"]
                if dividend > 0:
                    dividend_amount = num_shares * dividend
                    total_dividends += dividend_amount
                    # Reinvest dividends
                    shares[ticker] += dividend_amount / current_price

            portfolio_values.append(portfolio_value)
            invested_amounts.append(initial_amount)

            # Rebalancing
            if self._should_rebalance(
                current_date, last_rebalance_date, rebalancing
            ):
                shares = self._rebalance_portfolio(
                    portfolio, shares, price_data, current_date, portfolio_value
                )
                last_rebalance_date = current_date

            # Monthly snapshot
            if current_date.day == 1 or current_date == all_dates[-1]:
                monthly_snapshots.append(
                    MonthlySnapshot(
                        date=current_date.date(),
                        portfolio_value=portfolio_value,
                        invested_amount=initial_amount,
                        dividends_received=total_dividends,
                    )
                )

        # Calculate summary statistics
        final_value = portfolio_values[-1] if portfolio_values else 0.0
        total_return_pct = calculate_total_return(initial_amount, final_value)
        years = get_years_between_dates(
            pd.Timestamp(start_date), pd.Timestamp(end_date)
        )
        cagr = calculate_cagr(initial_amount, final_value, years)
        mdd = calculate_mdd(portfolio_values)

        summary = SimulationSummary(
            total_invested=initial_amount,
            final_value=final_value,
            total_return_pct=total_return_pct,
            cagr=cagr,
            mdd=mdd,
            total_dividends=total_dividends,
        )

        return summary, monthly_snapshots

    def _simulate_dca(
        self,
        portfolio: list[PortfolioItem],
        initial_amount: float,
        monthly_contribution: float,
        price_data: dict[str, pd.DataFrame],
        start_date: date,
        end_date: date,
        rebalancing: RebalancingFrequency,
    ) -> tuple[SimulationSummary, list[MonthlySnapshot]]:
        """Simulate dollar cost averaging (DCA) investment."""
        # Get all unique dates
        all_dates = sorted(
            set().union(*[set(df.index) for df in price_data.values()])
        )

        if not all_dates:
            raise ValueError("No price data available")

        # Initialize portfolio
        shares = {item.ticker: 0.0 for item in portfolio}
        total_invested = 0.0
        total_dividends = 0.0

        # Initial investment
        if initial_amount > 0:
            for item in portfolio:
                if item.ticker not in price_data:
                    continue

                allocation = initial_amount * (item.weight / 100)
                first_price = price_data[item.ticker].iloc[0]["adj_close"]
                shares[item.ticker] += allocation / first_price

            total_invested = initial_amount

        # Track portfolio value over time
        portfolio_values = []
        invested_amounts = []
        monthly_snapshots = []

        last_contribution_month = None
        last_rebalance_date = all_dates[0]

        for current_date in all_dates:
            current_month = (current_date.year, current_date.month)

            # Monthly contribution
            if (
                monthly_contribution > 0
                and current_month != last_contribution_month
            ):
                for item in portfolio:
                    if item.ticker not in price_data:
                        continue

                    df = price_data[item.ticker]
                    if current_date not in df.index:
                        continue

                    allocation = monthly_contribution * (item.weight / 100)
                    current_price = df.loc[current_date]["adj_close"]
                    shares[item.ticker] += allocation / current_price

                total_invested += monthly_contribution
                last_contribution_month = current_month

            # Calculate current portfolio value
            portfolio_value = 0.0
            for ticker, num_shares in shares.items():
                if ticker not in price_data:
                    continue

                df = price_data[ticker]
                if current_date not in df.index:
                    continue

                current_price = df.loc[current_date]["adj_close"]
                portfolio_value += num_shares * current_price

                # Add dividends
                dividend = df.loc[current_date]["dividend"]
                if dividend > 0:
                    dividend_amount = num_shares * dividend
                    total_dividends += dividend_amount
                    # Reinvest dividends
                    shares[ticker] += dividend_amount / current_price

            portfolio_values.append(portfolio_value)
            invested_amounts.append(total_invested)

            # Rebalancing
            if self._should_rebalance(
                current_date, last_rebalance_date, rebalancing
            ):
                shares = self._rebalance_portfolio(
                    portfolio, shares, price_data, current_date, portfolio_value
                )
                last_rebalance_date = current_date

            # Monthly snapshot (first day of month or last day)
            if current_date.day == 1 or current_date == all_dates[-1]:
                monthly_snapshots.append(
                    MonthlySnapshot(
                        date=current_date.date(),
                        portfolio_value=portfolio_value,
                        invested_amount=total_invested,
                        dividends_received=total_dividends,
                    )
                )

        # Calculate summary statistics
        final_value = portfolio_values[-1] if portfolio_values else 0.0
        total_return_pct = calculate_total_return(total_invested, final_value)
        years = get_years_between_dates(
            pd.Timestamp(start_date), pd.Timestamp(end_date)
        )
        cagr = calculate_cagr(total_invested, final_value, years)
        mdd = calculate_mdd(portfolio_values)

        summary = SimulationSummary(
            total_invested=total_invested,
            final_value=final_value,
            total_return_pct=total_return_pct,
            cagr=cagr,
            mdd=mdd,
            total_dividends=total_dividends,
        )

        return summary, monthly_snapshots

    def _should_rebalance(
        self,
        current_date: pd.Timestamp,
        last_rebalance_date: pd.Timestamp,
        rebalancing: RebalancingFrequency,
    ) -> bool:
        """Check if portfolio should be rebalanced."""
        if rebalancing == RebalancingFrequency.NONE:
            return False

        days_diff = (current_date - last_rebalance_date).days

        if rebalancing == RebalancingFrequency.QUARTERLY:
            return days_diff >= 90
        elif rebalancing == RebalancingFrequency.YEARLY:
            return days_diff >= 365

        return False

    def _rebalance_portfolio(
        self,
        portfolio: list[PortfolioItem],
        shares: dict[str, float],
        price_data: dict[str, pd.DataFrame],
        current_date: pd.Timestamp,
        portfolio_value: float,
    ) -> dict[str, float]:
        """Rebalance portfolio to target weights."""
        new_shares = {}

        for item in portfolio:
            if item.ticker not in price_data:
                continue

            df = price_data[item.ticker]
            if current_date not in df.index:
                new_shares[item.ticker] = shares.get(item.ticker, 0.0)
                continue

            target_value = portfolio_value * (item.weight / 100)
            current_price = df.loc[current_date]["adj_close"]
            new_shares[item.ticker] = target_value / current_price

        return new_shares
