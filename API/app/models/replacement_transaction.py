"""
Replacement Transaction Standard Payload Models

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🆕 IRI ANNUITY REPLACEMENT TRANSACTION STANDARD (IARTS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This module defines a NEW, PROPRIETARY standard payload format for annuity 
replacement transactions. This is NOT an ACORD-compliant format.

📌 Standard Name: IARTS (IRI Annuity Replacement Transaction Standard)
📅 Version: 1.0.0
🏢 Owner: IRI Annuity Review AI Platform
📜 License: Proprietary (available for partner integration)
🔗 Spec: See REPLACEMENT_TRANSACTION_STANDARD.md

WHY A NEW STANDARD?
─────────────────────────────────────────────────────────────────────────────
Traditional ACORD XML is:
  ❌ Verbose and complex (100+ lines for simple transactions)
  ❌ Designed for batch EDI, not real-time APIs
  ❌ Lacks modern compliance & suitability structures
  ❌ Difficult to parse and validate
  ❌ Not optimized for AI/ML integration

IARTS is:
  ✅ Clean JSON format (50% smaller)
  ✅ REST API native (real-time processing)
  ✅ Compliance & suitability embedded
  ✅ Self-validating (Pydantic models)
  ✅ AI-ready (designed for recommendations)
  ✅ Developer-friendly

WHAT THIS STANDARD SUPPORTS:
─────────────────────────────────────────────────────────────────────────────
✓ 1035 Tax-Free Exchanges (Full, Partial, Non-Qualified)
✓ Internal Carrier Exchanges
✓ External Carrier Replacements
✓ Qualified Money (IRA, 403(b), etc.) & Non-Qualified
✓ Complete Suitability Assessment
✓ Compliance Checklist (State Forms, Reg BI, Best Interest)
✓ Beneficiary Designations
✓ Tax Withholding Elections
✓ Document References
✓ Approval Workflows

INTEGRATION:
─────────────────────────────────────────────────────────────────────────────
This format can be:
  → Consumed directly by modern order entry systems
  → Converted to ACORD XML for legacy systems (see converters)
  → Transformed to DTCC ACATS format for transfers
  → Used as API request/response payload

For complete documentation, see:
  - REPLACEMENT_TRANSACTION_STANDARD.md (full spec)
  - REPLACEMENT_TRANSACTION_QUICK_START.md (quick guide)
  - ACORD_VS_IARTS_COMPARISON.md (format comparison)
  - example_replacement_transactions.py (working examples)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Literal, Dict, Any
from datetime import datetime
from decimal import Decimal
from enum import Enum


class TransactionType(str, Enum):
    """Transaction type enumeration"""
    INTERNAL_EXCHANGE = "INTERNAL_EXCHANGE"  # Same carrier
    EXTERNAL_1035_EXCHANGE = "EXTERNAL_1035_EXCHANGE"  # Different carrier, tax-free
    PARTIAL_1035_EXCHANGE = "PARTIAL_1035_EXCHANGE"  # Partial exchange
    SURRENDER_AND_NEW = "SURRENDER_AND_NEW"  # Full surrender + new application


class ExchangeType(str, Enum):
    """IRS 1035 Exchange Types"""
    FULL_1035 = "FULL_1035"  # Full 1035 exchange
    PARTIAL_1035 = "PARTIAL_1035"  # Partial 1035 exchange
    NON_QUALIFIED = "NON_QUALIFIED"  # Non-1035 transaction


class PremiumSource(str, Enum):
    """Source of new premium"""
    EXCHANGE_PROCEEDS = "EXCHANGE_PROCEEDS"  # From existing policy
    ADDITIONAL_PREMIUM = "ADDITIONAL_PREMIUM"  # New money
    COMBINATION = "COMBINATION"  # Both exchange + new money


class TransactionStatus(str, Enum):
    """Transaction status"""
    INITIATED = "INITIATED"
    PENDING_REVIEW = "PENDING_REVIEW"
    APPROVED = "APPROVED"
    SUBMITTED = "SUBMITTED"
    IN_PROCESS = "IN_PROCESS"
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"


# ============================================================================
# CURRENT POLICY (Being Replaced)
# ============================================================================

class CurrentPolicyInfo(BaseModel):
    """Information about the policy being replaced"""
    policyNumber: str = Field(..., description="Current policy/contract number")
    carrier: str = Field(..., description="Current carrier name")
    carrierCode: Optional[str] = Field(default=None, description="Carrier NAIC code")
    productName: str = Field(..., description="Current product name")
    productType: str = Field(..., description="FIA, VA, Fixed, SPIA, DIA")
    
    # Financial details
    accountValue: Decimal = Field(..., description="Current account/cash value")
    surrenderValue: Decimal = Field(..., description="Current surrender value")
    surrenderCharge: Optional[Decimal] = Field(default=None, description="Surrender charge amount")
    surrenderChargePercent: Optional[float] = Field(default=None, description="Surrender charge percentage")    
    # Policy details
    issueDate: str = Field(..., description="Original issue date (YYYY-MM-DD)")
    ownerName: str = Field(..., description="Current policy owner name")
    ownerSSN: str = Field(..., description="Owner SSN/Tax ID")
    annuitantName: str = Field(..., description="Annuitant name")
    annuitantDOB: str = Field(..., description="Annuitant date of birth (YYYY-MM-DD)")
    
    # Tax status
    qualifiedStatus: Literal["QUALIFIED", "NON_QUALIFIED"] = Field(
        ..., 
        description="IRA/Qualified or Non-Qualified"
    )
    qualificationType: Optional[str] = Field(
        default=None, 
        description="Traditional IRA, Roth IRA, SEP, SIMPLE, 403(b), etc."
    )
    
    # Cost basis (critical for tax reporting)
    costBasis: Optional[Decimal] = Field(default=None, description="Tax cost basis")
    gainLoss: Optional[Decimal] = Field(default=None, description="Current gain/loss")
    
    # Income riders
    hasIncomeRider: bool = Field(default=False, description="Has living benefit rider")
    incomeRiderName: Optional[str] = Field(default=None, description="Rider name")
    incomeBase: Optional[Decimal] = Field(default=None, description="Income benefit base value")
    isIncomeActivated: bool = Field(default=False, description="Income already activated")
    
    # Replacement reason & suitability
    replacementReason: List[str] = Field(
        default_factory=list,
        description="Reasons for replacement (rate improvement, better features, etc.)"
    )
    surrenderChargeJustification: Optional[str] = Field(
        default=None,
        description="Justification if incurring surrender charges"
    )


# ============================================================================
# NEW PRODUCT (Replacement Product)
# ============================================================================

class NewProductSelection(BaseModel):
    """Selected new product details"""
    productId: str = Field(..., description="Product ID from catalog")
    carrier: str = Field(..., description="New carrier name")
    carrierCode: Optional[str] = Field(default=None, description="Carrier NAIC code")
    productName: str = Field(..., description="New product name")
    productType: str = Field(..., description="FIA, VA, Fixed, SPIA, DIA")
    
    # Premium allocation
    initialPremium: Decimal = Field(..., description="Total initial premium")
    exchangeAmount: Decimal = Field(..., description="Amount from 1035 exchange")
    additionalPremium: Decimal = Field(default=Decimal("0.00"), description="New money premium")
    
    # Selected index/investment options
    selectedIndexOptions: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Selected index crediting strategies with allocations"
    )
    
    # Selected riders
    selectedRiders: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Selected optional riders (income, death benefit, LTC, etc.)"
    )
    
    # Bonus (if applicable)
    bonusRate: Optional[float] = Field(default=None, description="Premium bonus rate")
    bonusAmount: Optional[Decimal] = Field(default=None, description="Calculated bonus amount")


# ============================================================================
# CLIENT INFORMATION
# ============================================================================

class ClientInfo(BaseModel):
    """Client/Owner information for the new policy"""
    # Identity
    firstName: str = Field(..., description="Owner first name")
    middleName: Optional[str] = Field(default=None, description="Owner middle name/initial")
    lastName: str = Field(..., description="Owner last name")
    suffix: Optional[str] = Field(default=None, description="Jr, Sr, III, etc.")
    ssn: str = Field(..., description="Social Security Number or Tax ID")
    dateOfBirth: str = Field(..., description="Date of birth (YYYY-MM-DD)")
    age: int = Field(..., description="Current age")
    gender: Literal["M", "F", "X"] = Field(..., description="Gender")
    citizenship: str = Field(default="USA", description="Citizenship")
    
    # Contact
    address: str = Field(..., description="Street address")
    city: str = Field(..., description="City")
    state: str = Field(..., description="State code (2-letter)")
    zipCode: str = Field(..., description="ZIP code")
    phone: str = Field(..., description="Primary phone number")
    email: str = Field(..., description="Email address")
    
    # Financial profile
    annualIncome: str = Field(..., description="Annual income range")
    netWorth: str = Field(..., description="Net worth range")
    liquidNetWorth: str = Field(..., description="Liquid net worth range")
    taxBracket: str = Field(..., description="Estimated tax bracket")
    
    # Employment
    employmentStatus: str = Field(..., description="Employed, Retired, Self-Employed, etc.")
    occupation: Optional[str] = Field(default=None, description="Occupation")
    employer: Optional[str] = Field(default=None, description="Employer name")


class AnnuitantInfo(BaseModel):
    """Annuitant information (if different from owner)"""
    isSameAsOwner: bool = Field(default=True, description="Annuitant is same as owner")
    firstName: Optional[str] = Field(default=None, description="Annuitant first name")
    middleName: Optional[str] = Field(default=None, description="Annuitant middle name")
    lastName: Optional[str] = Field(default=None, description="Annuitant last name")
    ssn: Optional[str] = Field(default=None, description="Annuitant SSN")
    dateOfBirth: Optional[str] = Field(default=None, description="Annuitant DOB (YYYY-MM-DD)")
    gender: Optional[Literal["M", "F", "X"]] = Field(default=None, description="Gender")
    relationship: Optional[str] = Field(default=None, description="Relationship to owner")


# ============================================================================
# BENEFICIARY INFORMATION
# ============================================================================

class BeneficiaryDesignation(BaseModel):
    """Beneficiary designation"""
    beneficiaryType: Literal["PRIMARY", "CONTINGENT"] = Field(..., description="Beneficiary type")
    firstName: str = Field(..., description="First name")
    middleName: Optional[str] = Field(default=None, description="Middle name")
    lastName: str = Field(..., description="Last name")
    suffix: Optional[str] = Field(default=None, description="Suffix")
    relationship: str = Field(..., description="Relationship to owner")
    ssn: Optional[str] = Field(default=None, description="SSN/Tax ID")
    dateOfBirth: Optional[str] = Field(default=None, description="Date of birth (YYYY-MM-DD)")
    allocationPercent: float = Field(..., description="Allocation percentage", ge=0, le=100)
    
    # Contact (for notification)
    address: Optional[str] = Field(default=None, description="Street address")
    city: Optional[str] = Field(default=None, description="City")
    state: Optional[str] = Field(default=None, description="State")
    zipCode: Optional[str] = Field(default=None, description="ZIP code")
    phone: Optional[str] = Field(default=None, description="Phone number")
    email: Optional[str] = Field(default=None, description="Email address")


# ============================================================================
# SUITABILITY & COMPLIANCE
# ============================================================================

class SuitabilityProfile(BaseModel):
    """Client suitability profile for compliance"""
    # Investment profile
    riskTolerance: Literal["Conservative", "Moderate", "Aggressive"] = Field(
        ..., 
        description="Risk tolerance"
    )
    investmentObjective: str = Field(..., description="Growth, Income, Preservation, etc.")
    investmentExperience: str = Field(..., description="Investment experience level")
    investmentHorizon: str = Field(..., description="Short (0-3y), Medium (3-7y), Long (7+y)")
    
    # Liquidity & time horizon
    liquidityNeeds: Literal["High", "Medium", "Low"] = Field(..., description="Liquidity needs")
    timeHorizon: str = Field(..., description="Expected holding period")
    surrenderChargeAcceptance: bool = Field(..., description="Understands surrender charges")
    
    # Income needs
    currentIncomeNeeded: bool = Field(default=False, description="Needs income now")
    futureIncomeNeeded: bool = Field(default=False, description="Needs income in future")
    incomeStartYear: Optional[int] = Field(default=None, description="Year income needed")
    
    # Other annuity holdings
    totalAnnuityHoldings: Optional[Decimal] = Field(default=None, description="Total annuity assets")
    percentageInAnnuities: Optional[float] = Field(default=None, description="% of net worth in annuities")
    
    # Replacement specific
    understandsReplacement: bool = Field(..., description="Understands replacement implications")
    comparedAlternatives: bool = Field(..., description="Compared multiple alternatives")
    reviewedSurrenderCharges: bool = Field(..., description="Reviewed surrender charges")


class ComplianceChecklist(BaseModel):
    """Compliance checklist for replacement transaction"""
    # Required disclosures
    replacementFormSigned: bool = Field(..., description="State replacement form signed")
    replacementFormDate: Optional[str] = Field(default=None, description="Form signature date")
    
    # Suitability
    suitabilityReviewCompleted: bool = Field(..., description="Suitability review done")
    suitabilityDeterminationDate: Optional[str] = Field(default=None, description="Review date")
    isSuitable: bool = Field(..., description="Transaction deemed suitable")
    suitabilityNotes: Optional[str] = Field(default=None, description="Suitability notes")
    
    # Best interest (Reg BI / state equivalents)
    bestInterestDetermination: bool = Field(..., description="Best interest standard met")
    alternativesConsidered: int = Field(..., description="Number of alternatives reviewed")
    
    # 1035 Exchange requirements
    is1035Exchange: bool = Field(..., description="Is this a 1035 exchange")
    exchangeFormCompleted: bool = Field(default=False, description="1035 form completed")
    
    # State-specific
    stateApprovalRequired: bool = Field(default=False, description="State approval needed")
    stateApprovalReceived: bool = Field(default=False, description="State approval received")
    
    # Free look disclosure
    freeLookPeriodDisclosed: bool = Field(..., description="Free look period disclosed")
    freeLookDays: int = Field(default=30, description="Free look period days")
    
    # Special situations
    seniorProtectionApplies: bool = Field(default=False, description="Senior protection rules apply")
    longerFreeLookApplies: bool = Field(default=False, description="Extended free look applies")


# ============================================================================
# ADVISOR INFORMATION
# ============================================================================

class AdvisorInfo(BaseModel):
    """Financial advisor/agent information"""
    advisorId: str = Field(..., description="Advisor ID/Writing agent number")
    firstName: str = Field(..., description="Advisor first name")
    lastName: str = Field(..., description="Advisor last name")
    email: str = Field(..., description="Advisor email")
    phone: str = Field(..., description="Advisor phone")
    
    # Licensing
    licenseNumber: str = Field(..., description="Insurance license number")
    licenseState: str = Field(..., description="License state")
    
    # Carrier appointments
    hasCarrierAppointment: bool = Field(..., description="Has appointment with new carrier")
    appointmentNumber: Optional[str] = Field(default=None, description="Appointment/contract number")
    
    # Compliance
    hasProductTraining: bool = Field(..., description="Completed product training")
    completedCE: bool = Field(default=True, description="CE requirements current")
    
    # Firm information
    firmName: str = Field(..., description="Advisory firm/agency name")
    firmAddress: Optional[str] = Field(default=None, description="Firm address")
    bdName: Optional[str] = Field(default=None, description="Broker-dealer name (if applicable)")
    bdCRD: Optional[str] = Field(default=None, description="BD CRD number")


# ============================================================================
# TAX WITHHOLDING & ELECTIONS
# ============================================================================

class TaxWithholdingElections(BaseModel):
    """Tax withholding elections for new policy"""
    federalWithholding: bool = Field(default=False, description="Elect federal withholding")
    federalPercent: Optional[float] = Field(default=None, description="Federal withholding %", ge=0, le=100)
    federalFlatAmount: Optional[Decimal] = Field(default=None, description="Federal flat $ amount")
    
    stateWithholding: bool = Field(default=False, description="Elect state withholding")
    statePercent: Optional[float] = Field(default=None, description="State withholding %", ge=0, le=100)
    stateFlatAmount: Optional[Decimal] = Field(default=None, description="State flat $ amount")
    
    # W-9 certification
    w9OnFile: bool = Field(..., description="W-9 form on file")
    w9Date: Optional[str] = Field(default=None, description="W-9 signature date")


# ============================================================================
# MAIN REPLACEMENT TRANSACTION PAYLOAD
# ============================================================================

class ReplacementTransactionPayload(BaseModel):
    """
    Standard payload for annuity replacement transactions.
    
    This structure can be consumed by any order entry system and includes
    all information required for:
    - Application processing
    - 1035 exchange processing
    - Suitability review
    - Compliance documentation
    - State filing requirements
    """
    
    # ========================================================================
    # TRANSACTION METADATA
    # ========================================================================
    transactionId: str = Field(..., description="Unique transaction identifier")
    transactionType: TransactionType = Field(..., description="Type of replacement")
    exchangeType: ExchangeType = Field(..., description="1035 exchange type")
    premiumSource: PremiumSource = Field(..., description="Source of premium")
    status: TransactionStatus = Field(default=TransactionStatus.INITIATED, description="Current status")
    
    createdDate: str = Field(..., description="Transaction creation date (YYYY-MM-DD)")
    createdTimestamp: str = Field(..., description="Creation timestamp (ISO 8601)")
    submittedDate: Optional[str] = Field(default=None, description="Submission date to carrier")
    
    # Source system tracking
    sourceSystem: str = Field(default="AnnuityReviewAI", description="Originating system")
    sourceSystemVersion: Optional[str] = Field(default=None, description="System version")
    
    # ========================================================================
    # CORE TRANSACTION DATA
    # ========================================================================
    currentPolicy: CurrentPolicyInfo = Field(..., description="Policy being replaced")
    newProduct: NewProductSelection = Field(..., description="New product selection")
    
    client: ClientInfo = Field(..., description="Client/owner information")
    annuitant: AnnuitantInfo = Field(..., description="Annuitant information")
    
    beneficiaries: List[BeneficiaryDesignation] = Field(
        default_factory=list,
        description="Beneficiary designations"
    )
    
    # ========================================================================
    # SUITABILITY & COMPLIANCE
    # ========================================================================
    suitabilityProfile: SuitabilityProfile = Field(..., description="Suitability assessment")
    complianceChecklist: ComplianceChecklist = Field(..., description="Compliance verification")
    
    advisor: AdvisorInfo = Field(..., description="Advisor information")
    
    # ========================================================================
    # TAX & FINANCIAL ELECTIONS
    # ========================================================================
    taxWithholding: TaxWithholdingElections = Field(..., description="Tax withholding elections")
    
    # Qualified money details
    qualifiedStatus: Literal["QUALIFIED", "NON_QUALIFIED"] = Field(
        ...,
        description="Qualified or non-qualified money"
    )
    qualificationType: Optional[str] = Field(
        default=None,
        description="IRA type: Traditional, Roth, SEP, SIMPLE, 403(b), etc."
    )
    custodianName: Optional[str] = Field(default=None, description="IRA custodian name")
    custodianAccountNumber: Optional[str] = Field(default=None, description="Custodian account #")
    
    # ========================================================================
    # SUPPORTING DOCUMENTATION
    # ========================================================================
    documents: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Supporting documents (type, filename, URL/reference)"
    )
    
    # ========================================================================
    # ADDITIONAL INSTRUCTIONS & NOTES
    # ========================================================================
    specialInstructions: Optional[str] = Field(default=None, description="Special processing instructions")
    internalNotes: Optional[str] = Field(default=None, description="Internal notes (not sent to carrier)")
    clientNotes: Optional[str] = Field(default=None, description="Client-facing notes")
    
    # ========================================================================
    # APPROVAL & WORKFLOW
    # ========================================================================
    approvalRequired: bool = Field(default=True, description="Requires approval")
    approvedBy: Optional[str] = Field(default=None, description="Approver ID/name")
    approvalDate: Optional[str] = Field(default=None, description="Approval date")
    approvalNotes: Optional[str] = Field(default=None, description="Approval notes")
    
    # ========================================================================
    # INTEGRATION METADATA
    # ========================================================================
    externalSystemRefs: Dict[str, str] = Field(
        default_factory=dict,
        description="References to external systems (CRM ID, order entry ID, etc.)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "transactionId": "TXN-2026-00001",
                "transactionType": "EXTERNAL_1035_EXCHANGE",
                "exchangeType": "FULL_1035",
                "premiumSource": "EXCHANGE_PROCEEDS",
                "status": "INITIATED",
                "createdDate": "2026-02-25",
                "createdTimestamp": "2026-02-25T10:30:00Z",
                "currentPolicy": {
                    "policyNumber": "ABC123456",
                    "carrier": "Legacy Insurance Co",
                    "productName": "Legacy FIA 2015",
                    "accountValue": "250000.00",
                    "surrenderValue": "248000.00",
                    "surrenderCharge": "2000.00",
                    "ownerName": "John Smith",
                    "ownerSSN": "***-**-1234"
                },
                "newProduct": {
                    "productId": "PROD-2024-FIA-001",
                    "carrier": "Modern Annuity Co",
                    "productName": "Income Plus FIA 2024",
                    "initialPremium": "248000.00",
                    "exchangeAmount": "248000.00"
                }
            }
        }


# ============================================================================
# RESPONSE MODELS
# ============================================================================

class TransactionSubmissionResponse(BaseModel):
    """Response from submitting a replacement transaction"""
    success: bool = Field(..., description="Was submission successful")
    transactionId: str = Field(..., description="Transaction ID")
    confirmationNumber: Optional[str] = Field(None, description="Confirmation/case number")
    status: TransactionStatus = Field(..., description="Current status")
    message: str = Field(..., description="Response message")
    nextSteps: List[str] = Field(default_factory=list, description="Next steps required")
    estimatedCompletionDate: Optional[str] = Field(None, description="Estimated completion")
    errors: List[str] = Field(default_factory=list, description="Any validation errors")
    warnings: List[str] = Field(default_factory=list, description="Any warnings")


class TransactionValidationResponse(BaseModel):
    """Response from validating a transaction payload"""
    isValid: bool = Field(..., description="Is payload valid")
    errors: List[str] = Field(default_factory=list, description="Validation errors")
    warnings: List[str] = Field(default_factory=list, description="Validation warnings")
    missingFields: List[str] = Field(default_factory=list, description="Required fields missing")
    complianceFlags: List[str] = Field(default_factory=list, description="Compliance issues")
