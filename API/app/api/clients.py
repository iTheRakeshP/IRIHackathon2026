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
