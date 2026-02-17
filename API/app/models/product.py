"""
Product catalog data models
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class RiderOption(BaseModel):
    """Available rider option"""
    riderName: str = Field(..., description="Rider name")
    riderType: str = Field(..., description="Income, Death Benefit, LTC, etc.")
    annualFee: float = Field(..., description="Annual fee as percentage")
    features: List[str] = Field(default_factory=list, description="Key features")
    rollUpRate: Optional[float] = Field(None, description="Guaranteed roll-up rate if applicable")
    payoutRate: Optional[float] = Field(None, description="Income payout percentage if applicable")


class IndexOption(BaseModel):
    """Index crediting option"""
    indexName: str = Field(..., description="S&P 500, etc.")
    strategy: str = Field(..., description="Cap, Participation, etc.")
    currentValue: float = Field(..., description="Current cap/participation rate")
    floor: float = Field(default=0.0, description="Downside protection floor")


class ProductFees(BaseModel):
    """Product fee structure"""
    m_e_fee: float = Field(default=0.0, description="Mortality & Expense fee")
    administrativeFee: float = Field(default=0.0, description="Administrative fee")
    fundExpenses: Optional[float] = Field(None, description="Average fund expenses (VA only)")


class SurrenderSchedule(BaseModel):
    """Surrender charge schedule"""
    years: int = Field(..., description="Surrender period duration")
    schedule: List[float] = Field(..., description="Withdrawal charges by year")
    freeWithdrawalPercent: float = Field(default=10.0, description="Annual free withdrawal %")


class Product(BaseModel):
    """Market product in catalog"""
    productId: str = Field(..., description="Unique product identifier")
    carrier: str = Field(..., description="Insurance carrier")
    productName: str = Field(..., description="Product name")
    productType: str = Field(..., description="FIA, Fixed, VA")
    issueYear: int = Field(..., description="Year product was introduced")
    availableStates: List[str] = Field(default_factory=list, description="States where available")
    
    # Performance
    indexOptions: List[IndexOption] = Field(default_factory=list, description="Available index options")
    guaranteedMinimumRate: Optional[float] = Field(None, description="Guaranteed minimum rate")
    currentFixedRate: Optional[float] = Field(None, description="Current fixed rate (Fixed annuities)")
    
    # Fees
    fees: ProductFees = Field(..., description="Fee structure")
    
    # Riders
    availableRiders: List[RiderOption] = Field(default_factory=list, description="Available riders")
    
    # Rules
    surrenderSchedule: SurrenderSchedule = Field(..., description="Surrender schedule")
    minimumPremium: float = Field(default=10000.0, description="Minimum premium")
    maximumPremium: Optional[float] = Field(None, description="Maximum premium")
    ageMin: int = Field(default=0, description="Minimum issue age")
    ageMax: int = Field(default=85, description="Maximum issue age")
    
    # Features
    bonusRate: Optional[float] = Field(None, description="Premium bonus rate if applicable")
    liquidityFeatures: List[str] = Field(default_factory=list, description="Special liquidity features")
    keyBenefits: List[str] = Field(default_factory=list, description="Key product benefits")
    
    # Suitability
    suitableFor: List[str] = Field(default_factory=list, description="Suitable objectives: Growth, Income, Preservation")
    riskProfile: str = Field(default="Moderate", description="Conservative, Moderate, Aggressive")
    
    # Marketing
    isNewProduct: bool = Field(default=False, description="Highlight as new product")
    competitiveAdvantages: List[str] = Field(default_factory=list, description="Key selling points")


class ProductSummary(BaseModel):
    """Condensed product for comparison views"""
    productId: str
    carrier: str
    productName: str
    productType: str
    currentCapRate: Optional[float] = None
    currentFixedRate: Optional[float] = None
    totalFees: float = Field(default=0.0, description="Total annual fees")
    surrenderYears: int
    keyBenefits: List[str] = Field(default_factory=list, max_items=3)


class ProductComparison(BaseModel):
    """Product comparison for replacement module"""
    currentPolicy: Dict = Field(..., description="Current policy summary")
    alternatives: List[Product] = Field(..., description="Alternative products (2-3 max)")
    comparisonNotes: List[str] = Field(default_factory=list, description="Key comparison points")
    disclaimer: str = Field(
        default="Illustrative comparison only. Not a recommendation. Suitability review required.",
        description="Compliance disclaimer"
    )
