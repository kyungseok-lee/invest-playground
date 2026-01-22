"""Simulation API endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.simulation import (
    ComparisonRequest,
    ComparisonResponse,
    ScenarioResult,
    SimulationRequest,
    SimulationResponse,
)
from app.services.simulation_service import SimulationService

router = APIRouter(prefix="/simulation", tags=["simulation"])


@router.post("/run", response_model=SimulationResponse)
def run_simulation(
    request: SimulationRequest,
    db: Session = Depends(get_db),
) -> SimulationResponse:
    """
    Run investment simulation.

    Args:
        request: Simulation request parameters
        db: Database session

    Returns:
        Simulation results with summary and monthly data
    """
    if request.start_date >= request.end_date:
        raise HTTPException(
            status_code=400, detail="Start date must be before end date"
        )

    try:
        service = SimulationService(db)
        summary, monthly_data = service.run_simulation(
            portfolio=request.portfolio,
            investment_type=request.investment_type,
            initial_amount=request.initial_amount,
            monthly_contribution=request.monthly_contribution,
            start_date=request.start_date,
            end_date=request.end_date,
            rebalancing=request.rebalancing,
        )

        return SimulationResponse(summary=summary, monthly_data=monthly_data)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Simulation failed: {str(e)}"
        )


@router.post("/compare", response_model=ComparisonResponse)
def compare_scenarios(
    request: ComparisonRequest,
    db: Session = Depends(get_db),
) -> ComparisonResponse:
    """
    Compare multiple investment scenarios.

    Args:
        request: Comparison request with multiple scenarios
        db: Database session

    Returns:
        Comparison results for all scenarios
    """
    if request.start_date >= request.end_date:
        raise HTTPException(
            status_code=400, detail="Start date must be before end date"
        )

    try:
        service = SimulationService(db)
        results = []

        for scenario in request.scenarios:
            summary, _ = service.run_simulation(
                portfolio=scenario.portfolio,
                investment_type=scenario.investment_type,
                initial_amount=scenario.initial_amount,
                monthly_contribution=scenario.monthly_contribution,
                start_date=request.start_date,
                end_date=request.end_date,
                rebalancing=request.rebalancing,
            )

            results.append(
                ScenarioResult(
                    name=scenario.name,
                    final_value=summary.final_value,
                    total_invested=summary.total_invested,
                    total_return_pct=summary.total_return_pct,
                    cagr=summary.cagr,
                    mdd=summary.mdd,
                )
            )

        return ComparisonResponse(scenarios=results)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Comparison failed: {str(e)}"
        )
