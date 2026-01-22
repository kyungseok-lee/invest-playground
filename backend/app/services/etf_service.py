"""ETF data service using yfinance."""

from datetime import date, datetime

import yfinance as yf
from sqlalchemy.orm import Session

from app.db.models import ETF, PriceHistory
from app.models.etf import ETFDetail, ETFSearchResult, PriceData


class ETFService:
    """Service for ETF data operations."""

    # Popular ETFs for search
    POPULAR_ETFS = [
        {"ticker": "VOO", "name": "Vanguard S&P 500 ETF", "category": "Large Cap Blend"},
        {
            "ticker": "VTI",
            "name": "Vanguard Total Stock Market ETF",
            "category": "Total Market",
        },
        {"ticker": "QQQ", "name": "Invesco QQQ Trust", "category": "Technology"},
        {
            "ticker": "VEA",
            "name": "Vanguard FTSE Developed Markets ETF",
            "category": "Foreign Large Blend",
        },
        {
            "ticker": "VWO",
            "name": "Vanguard FTSE Emerging Markets ETF",
            "category": "Emerging Markets",
        },
        {
            "ticker": "BND",
            "name": "Vanguard Total Bond Market ETF",
            "category": "Intermediate Core Bond",
        },
        {"ticker": "VNQ", "name": "Vanguard Real Estate ETF", "category": "Real Estate"},
        {"ticker": "GLD", "name": "SPDR Gold Shares", "category": "Commodities"},
        {
            "ticker": "SCHD",
            "name": "Schwab US Dividend Equity ETF",
            "category": "Large Value",
        },
        {"ticker": "ARKK", "name": "ARK Innovation ETF", "category": "Innovation"},
        {"ticker": "SPY", "name": "SPDR S&P 500 ETF Trust", "category": "Large Cap Blend"},
        {
            "ticker": "IVV",
            "name": "iShares Core S&P 500 ETF",
            "category": "Large Cap Blend",
        },
    ]

    def __init__(self, db: Session):
        """Initialize ETF service with database session."""
        self.db = db

    def search_etfs(self, query: str) -> list[ETFSearchResult]:
        """
        Search for ETFs by ticker or name.

        Args:
            query: Search query string

        Returns:
            List of matching ETF search results
        """
        query = query.upper().strip()

        # First check database
        db_etfs = (
            self.db.query(ETF)
            .filter(
                (ETF.ticker.ilike(f"%{query}%")) | (ETF.name.ilike(f"%{query}%"))
            )
            .limit(10)
            .all()
        )

        if db_etfs:
            return [
                ETFSearchResult(
                    ticker=etf.ticker, name=etf.name, category=etf.category
                )
                for etf in db_etfs
            ]

        # If not in database, search from popular ETFs
        results = []
        for etf in self.POPULAR_ETFS:
            if query in etf["ticker"] or query.lower() in etf["name"].lower():
                results.append(
                    ETFSearchResult(
                        ticker=etf["ticker"],
                        name=etf["name"],
                        category=etf["category"],
                    )
                )

        return results

    def get_etf_detail(self, ticker: str) -> ETFDetail | None:
        """
        Get detailed information about an ETF.

        Args:
            ticker: ETF ticker symbol

        Returns:
            ETF detail or None if not found
        """
        ticker = ticker.upper()

        # Check database first
        db_etf = self.db.query(ETF).filter(ETF.ticker == ticker).first()
        if db_etf:
            return ETFDetail(
                ticker=db_etf.ticker,
                name=db_etf.name,
                category=db_etf.category,
                expense_ratio=db_etf.expense_ratio,
                dividend_yield=db_etf.dividend_yield,
                inception_date=db_etf.inception_date,
                aum=db_etf.aum,
                description=db_etf.description,
            )

        # If not in database, fetch from yfinance
        try:
            yf_ticker = yf.Ticker(ticker)
            info = yf_ticker.info

            # Extract relevant information
            name = info.get("longName", info.get("shortName", ticker))
            category = info.get("category", info.get("quoteType", "ETF"))
            expense_ratio = info.get("annualReportExpenseRatio")
            if expense_ratio:
                expense_ratio = expense_ratio * 100  # Convert to percentage

            dividend_yield = info.get("yield")
            if dividend_yield:
                dividend_yield = dividend_yield * 100  # Convert to percentage

            # Parse inception date
            inception_date = None
            fund_inception = info.get("fundInceptionDate")
            if fund_inception:
                try:
                    inception_date = datetime.fromtimestamp(fund_inception).date()
                except (ValueError, TypeError):
                    pass

            aum = info.get("totalAssets")

            etf_detail = ETFDetail(
                ticker=ticker,
                name=name,
                category=category,
                expense_ratio=expense_ratio,
                dividend_yield=dividend_yield,
                inception_date=inception_date,
                aum=aum,
                description=info.get("longBusinessSummary"),
            )

            # Cache in database
            self._cache_etf(etf_detail)

            return etf_detail

        except Exception:
            return None

    def get_price_history(
        self, ticker: str, start_date: date, end_date: date
    ) -> list[PriceData]:
        """
        Get price history for an ETF.

        Args:
            ticker: ETF ticker symbol
            start_date: Start date
            end_date: End date

        Returns:
            List of price data points
        """
        ticker = ticker.upper()

        # Check database first
        db_prices = (
            self.db.query(PriceHistory)
            .filter(
                PriceHistory.ticker == ticker,
                PriceHistory.date >= start_date,
                PriceHistory.date <= end_date,
            )
            .order_by(PriceHistory.date)
            .all()
        )

        if db_prices:
            return [
                PriceData(
                    date=price.date,
                    close=price.close,
                    adj_close=price.adj_close,
                    dividend=price.dividend,
                )
                for price in db_prices
            ]

        # If not in database, fetch from yfinance
        try:
            yf_ticker = yf.Ticker(ticker)
            hist = yf_ticker.history(
                start=start_date.isoformat(),
                end=end_date.isoformat(),
                auto_adjust=False,
            )

            if hist.empty:
                return []

            prices = []
            for idx, row in hist.iterrows():
                price_date = idx.date()
                dividend = row.get("Dividends", 0.0)

                price_data = PriceData(
                    date=price_date,
                    close=row["Close"],
                    adj_close=row["Adj Close"],
                    dividend=dividend,
                )
                prices.append(price_data)

                # Cache in database
                self._cache_price(ticker, price_date, row, dividend)

            return prices

        except Exception:
            return []

    def _cache_etf(self, etf_detail: ETFDetail) -> None:
        """Cache ETF detail in database."""
        try:
            existing = self.db.query(ETF).filter(ETF.ticker == etf_detail.ticker).first()

            if existing:
                # Update existing
                existing.name = etf_detail.name
                existing.category = etf_detail.category
                existing.expense_ratio = etf_detail.expense_ratio
                existing.dividend_yield = etf_detail.dividend_yield
                existing.inception_date = etf_detail.inception_date
                existing.aum = etf_detail.aum
                existing.description = etf_detail.description
                existing.updated_at = datetime.utcnow()
            else:
                # Create new
                new_etf = ETF(
                    ticker=etf_detail.ticker,
                    name=etf_detail.name,
                    category=etf_detail.category,
                    expense_ratio=etf_detail.expense_ratio,
                    dividend_yield=etf_detail.dividend_yield,
                    inception_date=etf_detail.inception_date,
                    aum=etf_detail.aum,
                    description=etf_detail.description,
                )
                self.db.add(new_etf)

            self.db.commit()
        except Exception:
            self.db.rollback()

    def _cache_price(
        self, ticker: str, price_date: date, row: dict, dividend: float
    ) -> None:
        """Cache price data in database."""
        try:
            existing = (
                self.db.query(PriceHistory)
                .filter(
                    PriceHistory.ticker == ticker, PriceHistory.date == price_date
                )
                .first()
            )

            if not existing:
                new_price = PriceHistory(
                    ticker=ticker,
                    date=price_date,
                    open=row["Open"],
                    high=row["High"],
                    low=row["Low"],
                    close=row["Close"],
                    adj_close=row["Adj Close"],
                    volume=int(row["Volume"]),
                    dividend=dividend,
                )
                self.db.add(new_price)
                self.db.commit()
        except Exception:
            self.db.rollback()
