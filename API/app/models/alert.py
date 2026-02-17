"""
Alert data models
"""
from pydantic import BaseModel, Field
from typing import List, Literal
from datetime import date
from enum import Enum


class AlertType(str, Enum):
    """Alert type enumeration"""
    REPLACEMENT = "REPLACEMENT"
    INCOME_ACTIVATION = "INCOME_ACTIVATION"
    SUITABILITY_DRIFT = "SUITABILITY_DRIFT"


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
