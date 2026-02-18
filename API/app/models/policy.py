"""
Policy data models
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from decimal import Decimal
from app.models.alert import Alert, AlertSummary


class Beneficiary(BaseModel):
    """Beneficiary information"""
    name: Optional[str] = Field(None, description="Beneficiary full name")
    relationship: Optional[str] = Field(None, description="Relationship to owner")
    ssn: Optional[str] = Field(None, description="Social Security Number")
    dateOfBirth: Optional[str] = Field(None, description="Date of birth")
    allocationPercent: Optional[float] = Field(None, description="Allocation percentage")


class TaxWithholding(BaseModel):
    """Tax withholding elections"""
    federal: Optional[float] = Field(None, description="Federal withholding percentage")
    state: Optional[float] = Field(None, description="State withholding percentage")


class ContactInfo(BaseModel):
    """Contact information"""
    address: Optional[str] = Field(None, description="Mailing address")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")


class NonFinancialData(BaseModel):
    """Non-financial policy data (DTCC Administrative API eligible)"""
    ownerName: Optional[str] = Field(None, description="Policy owner name")
    ownerSSN: Optional[str] = Field(None, description="Owner SSN (masked)")
    primaryBeneficiary: Optional[Beneficiary] = Field(None, description="Primary beneficiary")
    contingentBeneficiary: Optional[Beneficiary] = Field(None, description="Contingent beneficiary")
    contactInfo: Optional[ContactInfo] = Field(None, description="Contact information on file")
    taxWithholding: Optional[TaxWithholding] = Field(None, description="Tax withholding elections")
    specialInstructions: Optional[str] = Field(None, description="Special instructions or notes")
    lastUpdated: Optional[str] = Field(None, description="Last update timestamp")


class PolicyFees(BaseModel):
    """Policy fee structure"""
    m_e_fee: float = Field(default=0.0, description="Mortality & Expense fee")
    riderFee: float = Field(default=0.0, description="Rider fee")


class Policy(BaseModel):
    """Complete policy details"""
    policyId: str = Field(..., description="Unique policy identifier")
    clientAccountNumber: str = Field(..., description="Client account number")
    policyLabel: str = Field(..., description="Display label (Carrier + Type + Year)")
    carrier: str = Field(..., description="Insurance carrier")
    productType: str = Field(..., description="FIA, Fixed, VA, etc.")
    issueDate: str = Field(..., description="Policy issue date")
    applicationState: str = Field(..., description="State where policy was issued")
    accountValue: float = Field(..., description="Current account value")
    incomeBase: Optional[float] = Field(None, description="Income base value if applicable")
    riderType: str = Field(..., description="Rider type or 'None'")
    incomeActivated: bool = Field(default=False, description="Whether income is activated")
    surrenderScheduleYears: int = Field(..., description="Surrender schedule duration in years")
    surrenderEndDate: str = Field(..., description="Surrender schedule end date")
    currentCapRate: Optional[float] = Field(None, description="Current cap rate")
    renewalDays: Optional[int] = Field(None, description="Days until renewal")
    renewalCapRate: Optional[float] = Field(None, description="Renewal cap rate")
    fees: PolicyFees = Field(..., description="Fee structure")
    nonFinancialData: Optional[NonFinancialData] = Field(None, description="Non-financial data (beneficiaries, contact, tax)")
    notes: str = Field(default="", description="Additional notes")
    alerts: List[Alert] = Field(default_factory=list, description="Active alerts for this policy")


class PolicySummary(BaseModel):
    """Policy summary for listing views"""
    policyId: str
    clientAccountNumber: str
    policyLabel: str
    carrier: str
    productType: str
    accountValue: float
    renewalDays: Optional[int] = None
    currentCapRate: Optional[float] = None
    renewalCapRate: Optional[float] = None
    alerts: List[AlertSummary] = Field(default_factory=list, description="Alert summaries")


class ClientPoliciesGroup(BaseModel):
    """Policies grouped by client account - for listing view"""
    clientAccountNumber: str
    clientName: str
    policies: List[PolicySummary]
    totalAlerts: int = Field(default=0, description="Total number of alerts across all policies")
    highSeverityCount: int = Field(default=0, description="Count of HIGH severity alerts")
    mediumSeverityCount: int = Field(default=0, description="Count of MEDIUM severity alerts")
    lowSeverityCount: int = Field(default=0, description="Count of LOW severity alerts")


class PolicyDetail(BaseModel):
    """Policy detail for frontend - transformed format"""
    policyId: str
    clientAccountNumber: str
    clientName: str = Field(default="", description="Client name (populated from client data)")
    carrier: str
    productType: str
    productName: Optional[str] = Field(None, description="Product name derived from policyLabel")
    issueDate: str
    renewalDate: Optional[str] = None
    renewalDays: Optional[int] = None
    daysToRenewal: Optional[int] = None  # Alias for renewalDays
    contractValue: float = Field(..., description="Contract value (mapped from accountValue)")
    accountValue: Optional[float] = None
    cashSurrenderValue: Optional[float] = None
    deathBenefit: Optional[float] = None
    currentSurrenderCharge: Optional[float] = None
    surrenderEndDate: Optional[str] = None
    currentCapRate: Optional[float] = None
    projectedRenewalRate: Optional[float] = None  # Mapped from renewalCapRate
    riders: List[str] = Field(default_factory=list, description="Riders list")
    annualFee: Optional[float] = None
    riderFee: Optional[float] = None
    meFee: Optional[float] = None
    adminFee: Optional[float] = None
    nonFinancialData: Optional[NonFinancialData] = Field(None, description="Non-financial data")
    alerts: List[Alert] = Field(default_factory=list, description="Active alerts")
