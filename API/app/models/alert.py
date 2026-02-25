"""
Alert data models
"""
from pydantic import BaseModel, Field
from typing import List, Literal
from datetime import date
from enum import Enum


class AlertType(str, Enum):
    """Alert type enumeration"""
    # Existing annuity optimization alerts (replacement-focused)
    REPLACEMENT = "REPLACEMENT"
    INCOME_ACTIVATION = "INCOME_ACTIVATION"
    SUITABILITY_DRIFT = "SUITABILITY_DRIFT"
    MISSING_INFO = "MISSING_INFO"
    
    # NEW: Annuity acquisition alerts (growth-focused)
    EXCESS_LIQUIDITY = "EXCESS_LIQUIDITY"  # Too much cash earning low interest
    PORTFOLIO_UNPROTECTED = "PORTFOLIO_UNPROTECTED"  # High equity exposure without guaranteed income
    TAX_INEFFICIENCY = "TAX_INEFFICIENCY"  # Taxable accounts that would benefit from tax deferral
    CD_MATURITY = "CD_MATURITY"  # CDs maturing, annuity could offer better rates
    INCOME_GAP = "INCOME_GAP"  # Approaching retirement without sufficient guaranteed income
    QUALIFIED_OPPORTUNITY = "QUALIFIED_OPPORTUNITY"  # Large IRA that could benefit from annuitization
    BENEFICIARY_PLANNING = "BENEFICIARY_PLANNING"  # Need for guaranteed death benefit
    DIVERSIFICATION_GAP = "DIVERSIFICATION_GAP"  # Missing insurance products in portfolio


class AlertSeverity(str, Enum):
    """Alert severity levels"""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class Alert(BaseModel):
    """Alert model matching UI specs"""
    alertId: str = Field(..., description="Unique alert identifier")
    type: AlertType = Field(..., description="Alert type")
    severity: AlertSeverity = Field(..., description="Alert severity")
    title: str = Field(..., description="Alert title")
    reasonShort: str = Field(..., description="Short reason for the alert")
    reasons: List[str] = Field(default_factory=list, description="Detailed reasons")
    createdAt: str = Field(..., description="Alert creation date")

    class Config:
        json_schema_extra = {
            "example": {
                "alertId": "ALT-001",
                "type": "REPLACEMENT",
                "severity": "HIGH",
                "title": "Replacement Opportunity",
                "reasonShort": "Renewal in 15 days; rate drops",
                "reasons": ["Surrender ending", "Market rates higher"],
                "createdAt": "2026-02-09"
            }
        }


class AlertSummary(BaseModel):
    """Condensed alert for listing views"""
    alertId: str
    type: AlertType
    severity: AlertSeverity
    title: str
    reasonShort: str
