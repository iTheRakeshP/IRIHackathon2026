"""
Client data models
"""
from pydantic import BaseModel, Field
from typing import Optional, Literal


class ClientSuitabilityProfile(BaseModel):
    """Client suitability profile"""
    age: int
    lifeStage: str = Field(..., description="Accumulation, Pre-Retirement, Retirement, etc.")
    maritalStatus: str
    dependents: int
    riskTolerance: str = Field(..., description="Conservative, Moderate, Aggressive")
    investmentExperience: str
    volatilityComfort: str
    primaryObjective: str = Field(..., description="Growth, Income, Preservation, etc.")
    secondaryObjective: str
    liquidityImportance: str = Field(..., description="High, Medium, Low")
    investmentHorizon: str = Field(..., description="Short, Medium, Long")
    withdrawalHorizon: str
    currentIncomeNeed: str = Field(..., description="Now, Later, etc.")
    annualIncomeRange: str
    netWorthRange: str
    liquidNetWorthRange: str
    taxBracket: str
    retirementTargetYear: Optional[int] = None
    state: str
    citizenship: str
    advisoryModel: str
    isFeeBasedAccount: bool


class Client(BaseModel):
    """Client basic information"""
    clientAccountNumber: str = Field(..., description="Client account number (3-6-3 format)")
    clientName: str = Field(..., description="Client full name")


class ClientWithSuitability(BaseModel):
    """Client with full suitability profile"""
    client: Client
    clientSuitabilityProfile: ClientSuitabilityProfile
    
    def to_frontend_format(self):
        """Transform to frontend-expected format"""
        return {
            "clientId": self.client.clientAccountNumber,
            "clientAccountNumber": self.client.clientAccountNumber,
            "accountNumber": self.client.clientAccountNumber,
            "name": self.client.clientName,
            "firstName": self.client.clientName.split()[0] if self.client.clientName else "",
            "lastName": " ".join(self.client.clientName.split()[1:]) if len(self.client.clientName.split()) > 1 else "",
            "email": f"{self.client.clientAccountNumber.lower().replace('-', '')}@example.com",
            "phone": "(555) 123-4567",
            "suitability": {
                "riskTolerance": self.clientSuitabilityProfile.riskTolerance,
                "primaryObjective": self.clientSuitabilityProfile.primaryObjective,
                "secondaryObjective": self.clientSuitabilityProfile.secondaryObjective,
                "currentIncomeNeed": self.clientSuitabilityProfile.currentIncomeNeed,
                "lifeStage": self.clientSuitabilityProfile.lifeStage,
                "liquidityImportance": self.clientSuitabilityProfile.liquidityImportance,
                "lastUpdated": "2026-02-15T10:30:00Z",
                "updatedBy": "System"
            },
            "suitabilityProfile": {
                "riskTolerance": self.clientSuitabilityProfile.riskTolerance,
                "primaryObjective": self.clientSuitabilityProfile.primaryObjective,
                "secondaryObjective": self.clientSuitabilityProfile.secondaryObjective,
                "currentIncomeNeed": self.clientSuitabilityProfile.currentIncomeNeed,
                "lifeStage": self.clientSuitabilityProfile.lifeStage,
                "liquidityImportance": self.clientSuitabilityProfile.liquidityImportance,
                "lastUpdated": "2026-02-15T10:30:00Z",
                "updatedBy": "System"
            }
        }


class SuitabilityUpdateRequest(BaseModel):
    """Request to update client suitability"""
    riskTolerance: Optional[str] = None
    primaryObjective: Optional[str] = None
    secondaryObjective: Optional[str] = None
    currentIncomeNeed: Optional[str] = None
    lifeStage: Optional[str] = None
    liquidityImportance: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "riskTolerance": "Moderate",
                "primaryObjective": "Income",
                "currentIncomeNeed": "Now"
            }
        }
