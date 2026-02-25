"""
Client Position data models for portfolio holdings analysis
Used to identify annuity ACQUISITION opportunities (not replacements)
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import date
from enum import Enum


class AssetClass(str, Enum):
    """Asset class categorization"""
    EQUITY = "EQUITY"
    FIXED_INCOME = "FIXED_INCOME"
    CASH = "CASH"
    ANNUITY = "ANNUITY"
    ALTERNATIVES = "ALTERNATIVES"
    REAL_ESTATE = "REAL_ESTATE"
    COMMODITIES = "COMMODITIES"


class AccountType(str, Enum):
    """Account type for tax treatment"""
    TAXABLE = "TAXABLE"
    IRA = "IRA"
    ROTH_IRA = "ROTH_IRA"
    TRADITIONAL_401K = "TRADITIONAL_401K"
    ROTH_401K = "ROTH_401K"
    SEP_IRA = "SEP_IRA"
    SIMPLE_IRA = "SIMPLE_IRA"
    INHERITED_IRA = "INHERITED_IRA"


class Position(BaseModel):
    """Individual investment position in client portfolio"""
    positionId: str = Field(..., description="Unique position identifier")
    assetClass: AssetClass = Field(..., description="Asset classification")
    accountType: AccountType = Field(..., description="Tax treatment category")
    symbol: Optional[str] = Field(default=None, description="Ticker symbol (if applicable)")
    description: str = Field(..., description="Position description")
    quantity: Optional[float] = Field(default=None, description="Number of shares/units")
    marketValue: float = Field(..., description="Current market value in USD")
    costBasis: Optional[float] = Field(default=None, description="Original cost basis")
    unrealizedGain: Optional[float] = Field(default=None, description="Unrealized gain/loss")
    currentYield: Optional[float] = Field(default=None, description="Current yield percentage (e.g., 0.045 = 4.5%)")
    maturityDate: Optional[date] = Field(default=None, description="Maturity date for CDs/bonds")
    currentRate: Optional[float] = Field(default=None, description="Current interest rate for CDs/fixed income")
    
    class Config:
        json_schema_extra = {
            "example": {
                "positionId": "POS-001",
                "assetClass": "EQUITY",
                "accountType": "TAXABLE",
                "symbol": "SPY",
                "description": "SPDR S&P 500 ETF",
                "quantity": 2000,
                "marketValue": 450000,
                "costBasis": 380000,
                "unrealizedGain": 70000
            }
        }


class PortfolioSummary(BaseModel):
    """Aggregated portfolio allocation summary"""
    equityAllocation: float = Field(..., description="Percentage allocated to equities (0.00-1.00)")
    fixedIncomeAllocation: float = Field(..., description="Percentage allocated to fixed income")
    cashAllocation: float = Field(..., description="Percentage allocated to cash/money market")
    annuityAllocation: float = Field(..., description="Percentage allocated to annuities")
    alternativesAllocation: float = Field(default=0.0, description="Percentage allocated to alternatives")
    taxableValue: float = Field(..., description="Total value in taxable accounts")
    qualifiedValue: float = Field(..., description="Total value in qualified accounts (IRA, 401k, etc.)")
    totalCash: float = Field(..., description="Total cash positions across all accounts")
    totalEquities: float = Field(..., description="Total equity positions across all accounts")
    totalFixedIncome: float = Field(..., description="Total fixed income positions")
    totalAnnuities: float = Field(default=0.0, description="Total annuity positions")


class ClientPosition(BaseModel):
    """Complete client portfolio position view"""
    clientAccountNumber: str = Field(..., description="Client account number")
    asOfDate: date = Field(..., description="Position snapshot date")
    totalPortfolioValue: float = Field(..., description="Total portfolio value in USD")
    positions: List[Position] = Field(default_factory=list, description="List of individual positions")
    summary: PortfolioSummary = Field(..., description="Portfolio allocation summary")
    
    class Config:
        json_schema_extra = {
            "example": {
                "clientAccountNumber": "101-123456-001",
                "asOfDate": "2026-02-25",
                "totalPortfolioValue": 1250000,
                "positions": [
                    {
                        "positionId": "POS-001",
                        "assetClass": "EQUITY",
                        "accountType": "TAXABLE",
                        "symbol": "SPY",
                        "description": "SPDR S&P 500 ETF",
                        "quantity": 2000,
                        "marketValue": 450000,
                        "costBasis": 380000,
                        "unrealizedGain": 70000
                    },
                    {
                        "positionId": "POS-002",
                        "assetClass": "CASH",
                        "accountType": "TAXABLE",
                        "description": "Money Market Fund",
                        "marketValue": 250000,
                        "currentYield": 0.005
                    }
                ],
                "summary": {
                    "equityAllocation": 0.68,
                    "fixedIncomeAllocation": 0.12,
                    "cashAllocation": 0.20,
                    "annuityAllocation": 0.00,
                    "alternativesAllocation": 0.00,
                    "taxableValue": 700000,
                    "qualifiedValue": 550000,
                    "totalCash": 250000,
                    "totalEquities": 850000,
                    "totalFixedIncome": 150000,
                    "totalAnnuities": 0
                }
            }
        }


class IncomeSource(BaseModel):
    """Guaranteed income source for income gap analysis"""
    sourceType: Literal["SOCIAL_SECURITY", "PENSION", "ANNUITY_INCOME", "RENTAL_INCOME", "OTHER"]
    description: str
    annualAmount: float
    startDate: Optional[date] = None
    guaranteed: bool = Field(default=True, description="Whether income is guaranteed")


class RetirementIncomePlan(BaseModel):
    """Client retirement income planning data"""
    clientAccountNumber: str
    targetRetirementYear: int
    estimatedAnnualExpenses: float
    guaranteedIncomeSources: List[IncomeSource] = Field(default_factory=list)
    totalGuaranteedIncome: float
    incomeGap: float = Field(..., description="Annual income shortfall")
    portfolioWithdrawalRate: float = Field(..., description="Required withdrawal rate to close gap")
    
    class Config:
        json_schema_extra = {
            "example": {
                "clientAccountNumber": "102-234567-002",
                "targetRetirementYear": 2026,
                "estimatedAnnualExpenses": 90000,
                "guaranteedIncomeSources": [
                    {
                        "sourceType": "SOCIAL_SECURITY",
                        "description": "Social Security benefits",
                        "annualAmount": 35000,
                        "startDate": "2026-06-01",
                        "guaranteed": True
                    },
                    {
                        "sourceType": "PENSION",
                        "description": "Corporate pension",
                        "annualAmount": 18000,
                        "startDate": "2026-01-01",
                        "guaranteed": True
                    }
                ],
                "totalGuaranteedIncome": 53000,
                "incomeGap": 37000,
                "portfolioWithdrawalRate": 0.045
            }
        }
