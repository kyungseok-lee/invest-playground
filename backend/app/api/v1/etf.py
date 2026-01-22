"""ETF API endpoints."""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.etf import ETFDetail, ETFHistory, ETFSearchResponse
from app.services.etf_service import ETFService

router = APIRouter(prefix="/etf", tags=["etf"])


@router.get("/search", response_model=ETFSearchResponse)
def search_etfs(
    q: str = Query(..., min_length=1, description="Search query"),
    db: Session = Depends(get_db),
) -> ETFSearchResponse:
    """
    Search for ETFs by ticker or name.

    Args:
        q: Search query string
        db: Database session

    Returns:
        List of matching ETF search results
    """
    service = ETFService(db)
    results = service.search_etfs(q)
    return ETFSearchResponse(results=results)


@router.get("/{ticker}", response_model=ETFDetail)
def get_etf_detail(
    ticker: str,
    db: Session = Depends(get_db),
) -> ETFDetail:
    """
    Get detailed information about an ETF.

    Args:
        ticker: ETF ticker symbol
        db: Database session

    Returns:
        ETF detail information
    """
    service = ETFService(db)
    etf_detail = service.get_etf_detail(ticker)

    if not etf_detail:
        raise HTTPException(status_code=404, detail=f"ETF {ticker} not found")

    return etf_detail


@router.get("/{ticker}/history", response_model=ETFHistory)
def get_etf_history(
    ticker: str,
    start: date = Query(..., description="Start date"),
    end: date = Query(..., description="End date"),
    db: Session = Depends(get_db),
) -> ETFHistory:
    """
    Get price history for an ETF.

    Args:
        ticker: ETF ticker symbol
        start: Start date
        end: End date
        db: Database session

    Returns:
        ETF price history
    """
    if start >= end:
        raise HTTPException(
            status_code=400, detail="Start date must be before end date"
        )

    service = ETFService(db)
    prices = service.get_price_history(ticker, start, end)

    if not prices:
        raise HTTPException(
            status_code=404, detail=f"No price data found for {ticker}"
        )

    return ETFHistory(ticker=ticker, prices=prices)
