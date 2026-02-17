"""
Policy API endpoints
"""
from fastapi import APIRouter, HTTPException, Path, Query
from typing import List, Optional
from app.models.policy import Policy, PolicySummary, ClientPoliciesGroup
from app.models.alert import AlertSummary, AlertSeverity
from app.services.data_store import data_store

router = APIRouter()


@router.get("/policies", response_model=List[ClientPoliciesGroup])
async def get_policies_grouped_by_client():
    """
    Get all policies grouped by client account.
    This endpoint returns policies grouped by client for the policy listing dashboard.
    Each group includes client info, policy summaries, and alert counts.
    """
    # Get all policies
    all_policies = data_store.get_all_policies()
    
    # Get clients with policies
    clients_dict = data_store.get_clients_with_policies()
    
    # Group policies by client
    grouped: dict = {}
    
    for policy in all_policies:
        client_account = policy.clientAccountNumber
        
        if client_account not in grouped:
            # Get client info
            client_data = clients_dict.get(client_account)
            client_name = client_data.client.clientName if client_data else "Unknown Client"
            
            grouped[client_account] = {
                "clientAccountNumber": client_account,
                "clientName": client_name,
                "policies": [],
                "totalAlerts": 0,
                "highSeverityCount": 0,
                "mediumSeverityCount": 0,
                "lowSeverityCount": 0
            }
        
        # Create policy summary
        alert_summaries = [
            AlertSummary(
                alertId=alert.alertId,
                type=alert.type,
                severity=alert.severity,
                title=alert.title,
                reasonShort=alert.reasonShort
            )
            for alert in policy.alerts
        ]
        
        policy_summary = PolicySummary(
            policyId=policy.policyId,
            clientAccountNumber=policy.clientAccountNumber,
            policyLabel=policy.policyLabel,
            carrier=policy.carrier,
            productType=policy.productType,
            accountValue=policy.accountValue,
            renewalDays=policy.renewalDays,
            currentCapRate=policy.currentCapRate,
            renewalCapRate=policy.renewalCapRate,
            alerts=alert_summaries
        )
        
        grouped[client_account]["policies"].append(policy_summary)
        
        # Count alerts by severity
        for alert in policy.alerts:
            grouped[client_account]["totalAlerts"] += 1
            if alert.severity == AlertSeverity.HIGH:
                grouped[client_account]["highSeverityCount"] += 1
            elif alert.severity == AlertSeverity.MEDIUM:
                grouped[client_account]["mediumSeverityCount"] += 1
            elif alert.severity == AlertSeverity.LOW:
                grouped[client_account]["lowSeverityCount"] += 1
    
    # Convert to list and return
    result = [ClientPoliciesGroup(**group_data) for group_data in grouped.values()]
    
    # Sort by total alerts (descending) then by client name
    result.sort(key=lambda x: (-x.totalAlerts, x.clientName))
    
    return result


@router.get("/policies/{policy_id}", response_model=Policy)
async def get_policy_detail(
    policy_id: str = Path(..., description="Policy ID")
):
    """
    Get complete policy details including all alerts.
    This endpoint is used when opening the Policy Detail Modal.
    """
    policy = data_store.get_policy_by_id(policy_id)
    
    if not policy:
        raise HTTPException(status_code=404, detail=f"Policy {policy_id} not found")
    
    return policy


@router.get("/clients/{client_account_number}/policies", response_model=List[PolicySummary])
async def get_client_policies(
    client_account_number: str = Path(..., description="Client account number")
):
    """
    Get all policies for a specific client.
    Returns policy summaries with alert information.
    """
    policies = data_store.get_policies_by_client(client_account_number)
    
    if not policies:
        raise HTTPException(
            status_code=404, 
            detail=f"No policies found for client {client_account_number}"
        )
    
    # Convert to summaries
    summaries = []
    for policy in policies:
        alert_summaries = [
            AlertSummary(
                alertId=alert.alertId,
                type=alert.type,
                severity=alert.severity,
                title=alert.title,
                reasonShort=alert.reasonShort
            )
            for alert in policy.alerts
        ]
        
        summary = PolicySummary(
            policyId=policy.policyId,
            clientAccountNumber=policy.clientAccountNumber,
            policyLabel=policy.policyLabel,
            carrier=policy.carrier,
            productType=policy.productType,
            accountValue=policy.accountValue,
            renewalDays=policy.renewalDays,
            currentCapRate=policy.currentCapRate,
            renewalCapRate=policy.renewalCapRate,
            alerts=alert_summaries
        )
        summaries.append(summary)
    
    return summaries
