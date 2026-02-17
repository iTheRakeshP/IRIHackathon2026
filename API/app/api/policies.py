"""
Policy API endpoints
"""
from fastapi import APIRouter, HTTPException, Path, Query
from typing import List, Optional
from datetime import datetime, timedelta
from app.models.policy import Policy, PolicySummary, ClientPoliciesGroup, PolicyDetail
from app.models.alert import AlertSummary, AlertSeverity
from app.services.data_store import data_store

router = APIRouter()


def transform_policy_to_detail(policy: Policy, client_name: str = "") -> PolicyDetail:
    """
    Transform backend Policy model to frontend PolicyDetail format.
    """
    # Calculate cash surrender value (account value minus surrender charge)
    cash_surrender_value = None
    current_surrender_charge = None
    
    if policy.accountValue and policy.surrenderScheduleYears and policy.surrenderEndDate:
        # Calculate surrender charge percentage based on years remaining
        try:
            end_date = datetime.strptime(policy.surrenderEndDate, "%Y-%m-%d")
            today = datetime.now()
            days_until_end = (end_date - today).days
            
            if days_until_end > 0:
                # Calculate surrender charge (decreasing over time)
                # Assume max 10% at start, decreasing linearly
                total_days = policy.surrenderScheduleYears * 365
                days_elapsed = total_days - days_until_end
                current_surrender_charge = max(0, 10 * (days_until_end / total_days))
                cash_surrender_value = policy.accountValue * (1 - current_surrender_charge / 100)
            else:
                current_surrender_charge = 0
                cash_surrender_value = policy.accountValue
        except:
            pass
    
    if cash_surrender_value is None:
        cash_surrender_value = policy.accountValue
    
    # Calculate death benefit (typically 100% - 150% of account value)
    death_benefit = policy.accountValue * 1.0 if policy.accountValue else None
    
    # Convert riderType to riders array
    riders = []
    if policy.riderType and policy.riderType.lower() != 'none':
        riders = [policy.riderType]
    
    # Add income rider if applicable
    if policy.incomeActivated or policy.incomeBase:
        income_rider = "Income Rider"
        if policy.incomeBase:
            income_rider += f" (${policy.incomeBase:,.0f})"
        if income_rider not in riders:
            riders.append(income_rider)
    
    # Extract product name from policyLabel or use productType
    product_name = policy.policyLabel or policy.productType
    
    return PolicyDetail(
        policyId=policy.policyId,
        clientAccountNumber=policy.clientAccountNumber,
        clientName=client_name,
        carrier=policy.carrier,
        productType=policy.productType,
        productName=product_name,
        issueDate=policy.issueDate,
        renewalDate=None,  # Not in source data
        renewalDays=policy.renewalDays,
        daysToRenewal=policy.renewalDays,  # Alias
        contractValue=policy.accountValue,  # Map accountValue to contractValue
        accountValue=policy.accountValue,
        cashSurrenderValue=cash_surrender_value,
        deathBenefit=death_benefit,
        currentSurrenderCharge=current_surrender_charge,
        surrenderEndDate=policy.surrenderEndDate,
        currentCapRate=policy.currentCapRate,
        projectedRenewalRate=policy.renewalCapRate,
        riders=riders,
        annualFee=None,  # Not in source data
        riderFee=policy.fees.riderFee if policy.fees else None,
        meFee=policy.fees.m_e_fee if policy.fees else None,
        adminFee=None,  # Not in source data
        alerts=policy.alerts
    )


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


@router.get("/policies/{policy_id}", response_model=PolicyDetail)
async def get_policy_detail(
    policy_id: str = Path(..., description="Policy ID")
):
    """
    Get complete policy details including all alerts.
    This endpoint is used when opening the Policy Detail Modal.
    Returns transformed policy data matching frontend expectations.
    """
    policy = data_store.get_policy_by_id(policy_id)
    
    if not policy:
        raise HTTPException(status_code=404, detail=f"Policy {policy_id} not found")
    
    # Get client name
    client_name = ""
    clients_dict = data_store.get_clients_with_policies()
    client_data = clients_dict.get(policy.clientAccountNumber)
    if client_data:
        client_name = client_data.client.clientName
    
    # Transform to frontend format
    return transform_policy_to_detail(policy, client_name)


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
