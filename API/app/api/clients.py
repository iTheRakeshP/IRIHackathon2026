"""
Client API endpoints
"""
from fastapi import APIRouter, HTTPException, Path
from typing import List
from app.models.client import ClientWithSuitability, SuitabilityUpdateRequest
from app.services.data_store import data_store
from datetime import datetime

router = APIRouter()


@router.get("/clients/{client_account_number}")
async def get_client(
    client_account_number: str = Path(..., description="Client account number")
):
    """
    Get client information including suitability profile.
    Used when opening Policy Detail Modal for suitability verification.
    Returns data in frontend-expected format.
    """
    client = data_store.get_client(client_account_number)
    
    if not client:
        raise HTTPException(
            status_code=404,
            detail=f"Client {client_account_number} not found"
        )
    
    # Transform to frontend format
    return client.to_frontend_format()


@router.patch("/clients/{client_account_number}/suitability")
async def update_client_suitability(
    client_account_number: str,
    suitability_update: SuitabilityUpdateRequest
):
    """
    Update client suitability profile.
    Used in Replacement Opportunity module when advisor verifies/updates suitability.
    Returns the updated client profile with timestamp in frontend format.
    """
    # Get current client
    client = data_store.get_client(client_account_number)
    
    if not client:
        raise HTTPException(
            status_code=404,
            detail=f"Client {client_account_number} not found"
        )
    
    # Prepare updates - only include non-None values
    updates = suitability_update.model_dump(exclude_none=True)
    
    if not updates:
        raise HTTPException(
            status_code=400,
            detail="No suitability fields provided for update"
        )
    
    # Update the client suitability
    updated_client = data_store.update_client_suitability(client_account_number, updates)
    
    if not updated_client:
        raise HTTPException(
            status_code=500,
            detail="Failed to update client suitability"
        )
    
    # Note: In a real system, we'd save the timestamp and advisor ID
    # For hackathon PoC, we're just returning the updated profile
    
    # Transform to frontend format
    return updated_client.to_frontend_format()


@router.get("/clients")
async def get_all_clients():
    """
    Get all clients.
    Primarily for dev/testing purposes.
    Returns data in frontend-expected format.
    """
    clients = data_store.get_all_clients()
    return [client.to_frontend_format() for client in clients]


@router.get("/clients/{client_account_number}/acquisition-alerts")
async def get_client_acquisition_alerts(
    client_account_number: str = Path(..., description="Client account number")
):
    """
    Get acquisition alerts (portfolio opportunities) for a specific client.
    These are CLIENT-level alerts based on entire portfolio analysis,
    not POLICY-level alerts (which are annuity replacements).
    
    Examples:
    - EXCESS_LIQUIDITY: Too much cash earning low interest
    - PORTFOLIO_UNPROTECTED: High equity exposure without guaranteed income
    - CD_MATURITY: CDs maturing, better rates available
    - INCOME_GAP: Retirement income shortfall
    - DIVERSIFICATION_GAP: Missing annuity allocation
    """
    alerts = data_store.get_acquisition_alerts_by_client(client_account_number)
    
    return {
        "clientAccountNumber": client_account_number,
        "alerts": alerts,
        "count": len(alerts)
    }


@router.get("/acquisition-alerts")
async def get_all_acquisition_alerts():
    """
    Get all acquisition alerts across all clients.
    Used for dashboard summary or management reporting.
    """
    all_alerts = data_store.get_all_acquisition_alerts()
    
    # Calculate summary stats
    total_alerts = sum(len(client_data.get("alerts", [])) for client_data in all_alerts)
    total_potential_aum = sum(client_data.get("totalPortfolioValue", 0) * 0.15 for client_data in all_alerts)
    
    return {
        "clients": all_alerts,
        "summary": {
            "totalClients": len(all_alerts),
            "totalAlerts": total_alerts,
            "estimatedNewAUM": round(total_potential_aum, 2)
        }
    }
