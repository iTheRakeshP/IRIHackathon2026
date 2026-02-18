"""
Policy API endpoints
"""
from fastapi import APIRouter, HTTPException, Path, Query, Body
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import asyncio
from app.models.policy import Policy, PolicySummary, ClientPoliciesGroup, PolicyDetail, NonFinancialData
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
        nonFinancialData=policy.nonFinancialData,
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


@router.post("/policies/{policy_id}/update-non-financial")
async def update_policy_non_financial_data(
    policy_id: str = Path(..., description="Policy ID"),
    update_data: Dict[str, Any] = Body(..., description="Non-financial data update payload")
):
    """
    Update policy non-financial data via DTCC Administrative API (Mock for hackathon).
    
    This endpoint simulates DTCC Administrative API integration for updating:
    - Beneficiary designations
    - Contact information (auto-applied from account profile)
    - Tax withholding elections
    - Special instructions
    
    For hackathon purposes, this is a mock implementation that:
    1. Simulates 1-2 second API delay
    2. Logs the would-be DTCC payload
    3. Updates in-memory data store
    4. Removes MISSING_INFO alert from the policy
    5. Returns success with mock transaction ID
    """
    # Get the policy
    policy = data_store.get_policy_by_id(policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail=f"Policy {policy_id} not found")
    
    # Simulate DTCC API processing delay (1-2 seconds)
    await asyncio.sleep(1.5)
    
    # Extract data from request
    account_profile_data = update_data.get("accountProfileData", {})
    policy_specific_data = update_data.get("policySpecificData", {})
    
    # Build DTCC payload (for logging/demonstration)
    dtcc_payload = {
        "policy_id": policy_id,
        "carrier": policy.carrier,
        "transaction_type": "ADMINISTRATIVE_UPDATE",
        "timestamp": datetime.now().isoformat(),
        "updates": {
            "owner_name": account_profile_data.get("ownerName"),
            "owner_ssn": account_profile_data.get("ssn"),
            "contact_address": account_profile_data.get("address"),
            "contact_email": account_profile_data.get("email"),
            "contact_phone": account_profile_data.get("phone"),
            "primary_beneficiary": policy_specific_data.get("primaryBeneficiary"),
            "contingent_beneficiary": policy_specific_data.get("contingentBeneficiary"),
            "tax_withholding": policy_specific_data.get("taxWithholding"),
            "special_instructions": policy_specific_data.get("specialInstructions")
        }
    }
    
    # Log the DTCC payload (for hackathon demonstration)
    print("\n" + "=" * 60)
    print("🔵 DTCC ADMINISTRATIVE API - MOCK SUBMISSION")
    print("=" * 60)
    print(f"Policy ID: {policy_id}")
    print(f"Carrier: {policy.carrier}")
    print(f"Transaction Type: Administrative Update (Non-Financial)")
    print("\nPayload that would be sent to DTCC:")
    import json
    print(json.dumps(dtcc_payload, indent=2))
    print("=" * 60 + "\n")
    
    # Update policy's nonFinancialData
    from app.models.policy import Beneficiary, ContactInfo, TaxWithholding
    
    primary_ben_data = policy_specific_data.get("primaryBeneficiary")
    contingent_ben_data = policy_specific_data.get("contingentBeneficiary")
    tax_data = policy_specific_data.get("taxWithholding")
    
    # Build NonFinancialData object
    updated_non_financial = NonFinancialData(
        ownerName=account_profile_data.get("ownerName"),
        ownerSSN=account_profile_data.get("ssn"),
        primaryBeneficiary=Beneficiary(**primary_ben_data) if primary_ben_data else None,
        contingentBeneficiary=Beneficiary(**contingent_ben_data) if contingent_ben_data else None,
        contactInfo=ContactInfo(
            address=account_profile_data.get("address"),
            email=account_profile_data.get("email"),
            phone=account_profile_data.get("phone")
        ),
        taxWithholding=TaxWithholding(**tax_data) if tax_data else None,
        specialInstructions=policy_specific_data.get("specialInstructions", ""),
        lastUpdated=datetime.now().isoformat()
    )
    
    # Update the policy
    policy.nonFinancialData = updated_non_financial
    
    # Remove MISSING_INFO alert from policy
    policy.alerts = [alert for alert in policy.alerts if alert.type != "MISSING_INFO"]
    
    # Update in data store
    data_store.update_policy(policy)
    
    # Generate mock DTCC transaction ID
    mock_transaction_id = f"DTCC-{datetime.now().strftime('%Y%m%d')}-{policy_id[-6:]}"
    
    # Track which fields were updated
    updated_fields = []
    if primary_ben_data:
        updated_fields.append("beneficiaries")
    if tax_data:
        updated_fields.append("taxWithholding")
    if account_profile_data.get("address") or account_profile_data.get("email"):
        updated_fields.append("contactInfo")
    
    # Return success response
    return {
        "success": True,
        "dtccTransactionId": mock_transaction_id,
        "message": "Policy updated successfully via DTCC Administrative API",
        "updatedFields": updated_fields,
        "timestamp": datetime.now().isoformat(),
        "mockNote": "This is a simulated DTCC integration for hackathon purposes"
    }
