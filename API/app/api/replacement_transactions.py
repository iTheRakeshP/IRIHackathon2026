"""
Replacement Transaction API Endpoints

This module provides endpoints for creating, validating, and submitting
replacement transactions using the standard payload format.
"""
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime
import uuid

from app.models.replacement_transaction import (
    ReplacementTransactionPayload,
    TransactionSubmissionResponse,
    TransactionValidationResponse,
    TransactionStatus,
    TransactionType,
    ExchangeType
)
from app.models.policy import Policy
from app.models.product import Product
from app.models.client import ClientWithSuitability
from app.services.data_store import data_store


router = APIRouter(prefix="/replacement-transactions", tags=["Replacement Transactions"])


# In-memory storage for demo (replace with database in production)
transactions_db = {}


@router.post("/validate", response_model=TransactionValidationResponse)
async def validate_replacement_transaction(payload: ReplacementTransactionPayload):
    """
    Validate a replacement transaction payload without submitting it.
    
    Performs checks for:
    - Required field completeness
    - Suitability requirements
    - Compliance checklist items
    - State-specific rules
    - Premium calculations
    """
    errors = []
    warnings = []
    missing_fields = []
    compliance_flags = []
    
    # Basic validation
    if payload.newProduct.initialPremium != (
        payload.newProduct.exchangeAmount + payload.newProduct.additionalPremium
    ):
        errors.append("Initial premium does not equal exchange amount plus additional premium")
    
    # Suitability checks
    if not payload.suitabilityProfile.understandsReplacement:
        compliance_flags.append("Client understanding of replacement not confirmed")
    
    if not payload.suitabilityProfile.comparedAlternatives:
        warnings.append("Client did not compare multiple alternatives")
    
    # Compliance checks
    if not payload.complianceChecklist.replacementFormSigned:
        errors.append("State replacement form not signed")
    
    if not payload.complianceChecklist.suitabilityReviewCompleted:
        errors.append("Suitability review not completed")
    
    if not payload.complianceChecklist.isSuitable:
        errors.append("Transaction determined not suitable")
    
    # 1035 Exchange validation
    if payload.exchangeType in [ExchangeType.FULL_1035, ExchangeType.PARTIAL_1035]:
        if not payload.complianceChecklist.is1035Exchange:
            errors.append("Exchange type indicates 1035 but compliance checklist not marked")
        if not payload.complianceChecklist.exchangeFormCompleted:
            errors.append("1035 exchange form not completed")
    
    # Beneficiary validation
    primary_beneficiaries = [b for b in payload.beneficiaries if b.beneficiaryType == "PRIMARY"]
    if primary_beneficiaries:
        total_primary_percent = sum(b.allocationPercent for b in primary_beneficiaries)
        if abs(total_primary_percent - 100.0) > 0.01:
            errors.append(f"Primary beneficiary allocations total {total_primary_percent}%, must equal 100%")
    else:
        warnings.append("No primary beneficiaries designated")
    
    # Age validation for new product
    client_age = payload.client.age
    # Would check against product.ageMin and product.ageMax if we had product data
    if client_age < 18:
        errors.append("Client age below minimum (18)")
    if client_age > 85:
        warnings.append("Client age above typical maximum (85) - may require underwriting")
    
    # Surrender charge warning
    if payload.currentPolicy.surrenderCharge and payload.currentPolicy.surrenderCharge > 0:
        if not payload.currentPolicy.surrenderChargeJustification:
            warnings.append("Surrender charges apply but no justification provided")
    
    # State approval check
    if payload.complianceChecklist.stateApprovalRequired and not payload.complianceChecklist.stateApprovalReceived:
        errors.append("State approval required but not received")
    
    # Advisor licensing
    if not payload.advisor.hasCarrierAppointment:
        errors.append("Advisor does not have carrier appointment")
    
    if not payload.advisor.hasProductTraining:
        warnings.append("Advisor has not completed product training")
    
    # Tax withholding validation
    if payload.taxWithholding.federalWithholding:
        if not payload.taxWithholding.federalPercent and not payload.taxWithholding.federalFlatAmount:
            errors.append("Federal withholding elected but no percentage or amount specified")
    
    # W-9 requirement
    if not payload.taxWithholding.w9OnFile:
        errors.append("W-9 form not on file")
    
    is_valid = len(errors) == 0
    
    return TransactionValidationResponse(
        isValid=is_valid,
        errors=errors,
        warnings=warnings,
        missingFields=missing_fields,
        complianceFlags=compliance_flags
    )


@router.post("/submit", response_model=TransactionSubmissionResponse)
async def submit_replacement_transaction(payload: ReplacementTransactionPayload):
    """
    Submit a replacement transaction for processing.
    
    This endpoint would typically:
    1. Validate the payload
    2. Submit to carrier's order entry system
    3. Initiate 1035 exchange process
    4. Create workflow tracking
    5. Store transaction record
    """
    # Validate first
    validation = await validate_replacement_transaction(payload)
    
    if not validation.isValid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Transaction validation failed",
                "errors": validation.errors,
                "warnings": validation.warnings
            }
        )
    
    # Store transaction
    transactions_db[payload.transactionId] = {
        "payload": payload.model_dump(),
        "status": TransactionStatus.SUBMITTED,
        "submittedAt": datetime.utcnow().isoformat(),
        "confirmationNumber": f"CONF-{uuid.uuid4().hex[:8].upper()}"
    }
    
    # Here you would integrate with actual order entry systems:
    # - Carrier API submission
    # - DTCC ACATS for transfer
    # - Document generation services
    # - Workflow management system
    
    next_steps = []
    if payload.exchangeType in [ExchangeType.FULL_1035, ExchangeType.PARTIAL_1035]:
        next_steps.append("1035 exchange form will be sent to surrendering carrier")
        next_steps.append("Client will receive confirmation within 2 business days")
    next_steps.append("Application will be submitted to new carrier")
    next_steps.append("Expect processing time of 5-10 business days")
    
    if payload.complianceChecklist.freeLookPeriodDisclosed:
        next_steps.append(f"Free look period: {payload.complianceChecklist.freeLookDays} days from delivery")
    
    return TransactionSubmissionResponse(
        success=True,
        transactionId=payload.transactionId,
        confirmationNumber=transactions_db[payload.transactionId]["confirmationNumber"],
        status=TransactionStatus.SUBMITTED,
        message="Transaction submitted successfully",
        nextSteps=next_steps,
        estimatedCompletionDate=None,  # Would calculate based on carrier SLA
        errors=[],
        warnings=validation.warnings
    )


@router.get("/{transaction_id}", response_model=dict)
async def get_replacement_transaction(transaction_id: str):
    """
    Retrieve a replacement transaction by ID.
    """
    if transaction_id not in transactions_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction {transaction_id} not found"
        )
    
    return transactions_db[transaction_id]


@router.get("/{transaction_id}/status")
async def get_transaction_status(transaction_id: str):
    """
    Get current status of a replacement transaction.
    """
    if transaction_id not in transactions_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction {transaction_id} not found"
        )
    
    txn = transactions_db[transaction_id]
    return {
        "transactionId": transaction_id,
        "status": txn["status"],
        "confirmationNumber": txn.get("confirmationNumber"),
        "submittedAt": txn.get("submittedAt"),
        "lastUpdated": txn.get("lastUpdated", txn.get("submittedAt"))
    }


@router.post("/create-from-context")
async def create_transaction_from_context(
    policy_id: str,
    product_id: str,
    client_account_number: str
):
    """
    Helper endpoint to create a replacement transaction payload from existing
    policy, product, and client data.
    
    This serves as a convenience method for the UI to generate the standard payload
    from the current context (policy being replaced, selected product, client profile).
    """
    # Get policy data
    policy = data_store.get_policy_by_id(policy_id)
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Policy {policy_id} not found"
        )
    
    # Get product data
    product = data_store.get_product_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {product_id} not found"
        )
    
    # Get client data
    client = data_store.get_client(client_account_number)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client {client_account_number} not found"
        )
    
    # Generate transaction ID
    transaction_id = f"TXN-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
    
    # Create payload structure (with defaults - UI would customize)
    # This is a TEMPLATE that the UI can populate with actual user selections
    template = {
        "transactionId": transaction_id,
        "transactionType": "EXTERNAL_1035_EXCHANGE",
        "exchangeType": "FULL_1035",
        "premiumSource": "EXCHANGE_PROCEEDS",
        "status": "INITIATED",
        "createdDate": datetime.now().strftime("%Y-%m-%d"),
        "createdTimestamp": datetime.utcnow().isoformat() + "Z",
        "sourceSystem": "AnnuityReviewAI",
        
        # Current policy info (from policy data)
        "currentPolicy": {
            "policyNumber": policy.policyId,
            "carrier": policy.carrier,
            "productName": policy.policyLabel,
            "productType": policy.productType,
            "accountValue": str(policy.accountValue),
            "surrenderValue": str(policy.accountValue),  # Would calculate actual surrender value
            "surrenderCharge": "0.00",  # Would calculate from policy.surrenderScheduleYears
            "issueDate": policy.issueDate,
            "ownerName": policy.nonFinancialData.ownerName if policy.nonFinancialData else "",
            "ownerSSN": policy.nonFinancialData.ownerSSN if policy.nonFinancialData else "",
            "annuitantName": policy.nonFinancialData.ownerName if policy.nonFinancialData else "",
            "annuitantDOB": "",  # Would need from client data
            "qualifiedStatus": "NON_QUALIFIED",  # Would determine from policy
            "costBasis": str(policy.accountValue * 0.8),  # Example - would need actual
            "hasIncomeRider": policy.riderType != "None",
            "incomeRiderName": policy.riderType if policy.riderType != "None" else None,
            "incomeBase": str(policy.incomeBase) if policy.incomeBase else None,
            "isIncomeActivated": policy.incomeActivated,
            "replacementReason": [alert.reasonShort for alert in policy.alerts[:3]] if policy.alerts else []
        },
        
        # New product info
        "newProduct": {
            "productId": product.productId,
            "carrier": product.carrier,
            "productName": product.productName,
            "productType": product.productType,
            "initialPremium": str(policy.accountValue),
            "exchangeAmount": str(policy.accountValue),
            "additionalPremium": "0.00",
            "selectedIndexOptions": [],  # UI would populate
            "selectedRiders": [],  # UI would populate
            "bonusRate": product.bonusRate,
            "bonusAmount": str(policy.accountValue * (product.bonusRate or 0) / 100) if product.bonusRate else None
        },
        
        # Client info (from client profile)
        "client": {
            "firstName": client.client.clientName.split()[0] if client.client.clientName else "",
            "lastName": " ".join(client.client.clientName.split()[1:]) if len(client.client.clientName.split()) > 1 else "",
            "ssn": "***-**-****",  # Masked
            "dateOfBirth": "",  # Would need
            "age": client.clientSuitabilityProfile.age,
            "gender": "M",  # Would need
            "citizenship": client.clientSuitabilityProfile.citizenship,
            "state": client.clientSuitabilityProfile.state,
            "address": "",  # Would need
            "city": "",
            "zipCode": "",
            "phone": "",
            "email": "",
            "annualIncome": client.clientSuitabilityProfile.annualIncomeRange,
            "netWorth": client.clientSuitabilityProfile.netWorthRange,
            "liquidNetWorth": client.clientSuitabilityProfile.liquidNetWorthRange,
            "taxBracket": client.clientSuitabilityProfile.taxBracket,
            "employmentStatus": "Employed",  # Would derive from lifeStage
        },
        
        # Annuitant (same as owner for simplicity)
        "annuitant": {
            "isSameAsOwner": True
        },
        
        # Beneficiaries (from policy if available)
        "beneficiaries": [],
        
        # Suitability (from client profile)
        "suitabilityProfile": {
            "riskTolerance": client.clientSuitabilityProfile.riskTolerance,
            "investmentObjective": client.clientSuitabilityProfile.primaryObjective,
            "investmentExperience": client.clientSuitabilityProfile.investmentExperience,
            "investmentHorizon": client.clientSuitabilityProfile.investmentHorizon,
            "liquidityNeeds": client.clientSuitabilityProfile.liquidityImportance,
            "timeHorizon": client.clientSuitabilityProfile.investmentHorizon,
            "surrenderChargeAcceptance": True,  # UI would confirm
            "currentIncomeNeeded": client.clientSuitabilityProfile.currentIncomeNeed == "Now",
            "futureIncomeNeeded": True,
            "incomeStartYear": client.clientSuitabilityProfile.retirementTargetYear,
            "understandsReplacement": False,  # UI must confirm
            "comparedAlternatives": False,  # UI must confirm
            "reviewedSurrenderCharges": False  # UI must confirm
        },
        
        # Compliance checklist (defaults - UI must complete)
        "complianceChecklist": {
            "replacementFormSigned": False,
            "suitabilityReviewCompleted": False,
            "isSuitable": False,
            "bestInterestDetermination": False,
            "alternativesConsidered": 0,
            "is1035Exchange": True,
            "exchangeFormCompleted": False,
            "stateApprovalRequired": False,
            "stateApprovalReceived": False,
            "freeLookPeriodDisclosed": False,
            "freeLookDays": 30
        },
        
        # Advisor info (would come from session/user context)
        "advisor": {
            "advisorId": "ADV-12345",
            "firstName": "Jane",
            "lastName": "Advisor",
            "email": "jadvisor@firm.com",
            "phone": "555-1234",
            "licenseNumber": "LIC-12345",
            "licenseState": client.clientSuitabilityProfile.state,
            "hasCarrierAppointment": product.hasAppointment,
            "hasProductTraining": product.hasTraining,
            "completedCE": True,
            "firmName": "Advisory Firm LLC"
        },
        
        # Tax withholding
        "taxWithholding": {
            "federalWithholding": False,
            "stateWithholding": False,
            "w9OnFile": False
        },
        
        # Qualified status
        "qualifiedStatus": "NON_QUALIFIED",
        
        "documents": [],
        "externalSystemRefs": {
            "policyId": policy_id,
            "productId": product_id,
            "clientAccountNumber": client_account_number
        }
    }
    
    return {
        "message": "Transaction template created from context",
        "transactionId": transaction_id,
        "template": template,
        "notes": [
            "This is a TEMPLATE with default values",
            "UI must populate missing required fields",
            "Compliance checklist items must be completed",
            "Client confirmations required before submission"
        ]
    }


@router.get("/")
async def list_transactions(
    client_account_number: Optional[str] = None,
    status: Optional[TransactionStatus] = None,
    limit: int = 50
):
    """
    List replacement transactions with optional filters.
    """
    results = []
    for txn_id, txn_data in transactions_db.items():
        payload_dict = txn_data.get("payload", {})
        
        # Apply filters
        if client_account_number and payload_dict.get("client", {}).get("accountNumber") != client_account_number:
            continue
        if status and txn_data.get("status") != status:
            continue
        
        results.append({
            "transactionId": txn_id,
            "status": txn_data.get("status"),
            "createdAt": payload_dict.get("createdTimestamp"),
            "submittedAt": txn_data.get("submittedAt"),
            "confirmationNumber": txn_data.get("confirmationNumber"),
            "client": payload_dict.get("client", {}).get("firstName", "") + " " + payload_dict.get("client", {}).get("lastName", ""),
            "newCarrier": payload_dict.get("newProduct", {}).get("carrier"),
            "amount": payload_dict.get("newProduct", {}).get("initialPremium")
        })
        
        if len(results) >= limit:
            break
    
    return {
        "total": len(results),
        "transactions": results
    }
