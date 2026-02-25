# Annuity Acquisition Alert Strategy (NEW Business Growth)

## Problem Statement

**Current System:** Only generates replacement opportunity alerts (moving money from one annuity to another)  
**Business Impact:** Does NOT grow annuity AUM—just shifts existing business  
**Solution Needed:** Identify opportunities to **purchase NEW annuities** by analyzing client's entire investment portfolio

---

## Strategic Shift: Replacement vs. Acquisition

| Alert Category | Current Alerts | New Growth Alerts |
|---------------|----------------|-------------------|
| **What It Does** | Analyzes existing annuities | Analyzes entire portfolio (stocks, bonds, cash, CDs, etc.) |
| **Business Outcome** | Moves money between products | **ADDS new annuity AUM** |
| **Data Source** | Existing annuity policies | Full client position view |
| **Advisor Action** | Replace existing annuity | **Recommend NEW annuity purchase** |
| **Revenue Impact** | Neutral (shift existing assets) | **POSITIVE (grow AUM)** |

---

## New Alert Types for Annuity Acquisition

### 1. 💰 **EXCESS_LIQUIDITY** Alert
**Opportunity:** Client has too much cash earning minimal interest

**Detection Logic:**
- Cash/money market positions > 10% of total portfolio
- Amount > $50,000
- Client age < 75 (liquidity needs assessment)
- Low liquidity importance in suitability profile

**Example:**
```json
{
  "alertType": "EXCESS_LIQUIDITY",
  "severity": "HIGH",
  "title": "Excess Cash Alert: $250K Earning 0.5%",
  "opportunity": "Move $150K to fixed indexed annuity earning 5.5% cap with liquidity access",
  "annuityRecommendation": {
    "productType": "Fixed Indexed Annuity",
    "allocation": 150000,
    "expectedBenefit": "4-5% upside vs. 0.5% current yield",
    "liquidityProtection": "10% annual penalty-free withdrawals"
  }
}
```

**Business Value:** Converts low-yielding cash to annuity AUM

---

### 2. 🎯 **PORTFOLIO_UNPROTECTED** Alert
**Opportunity:** Client has high equity exposure approaching/in retirement with no guaranteed income

**Detection Logic:**
- Equity allocation > 60%
- Age 55+
- Life stage: Pre-Retirement or Retired
- Primary objective: Income or Preservation
- NO existing annuities with income riders

**Example:**
```json
{
  "alertType": "PORTFOLIO_UNPROTECTED",
  "severity": "HIGH",
  "title": "85% Equities at Age 64 with No Guaranteed Income",
  "opportunity": "Allocate $200K to annuity with GLWB for downside protection",
  "annuityRecommendation": {
    "productType": "Variable Annuity with GLWB",
    "allocation": 200000,
    "riderRecommendation": "Guaranteed Lifetime Withdrawal Benefit (5.5% payout)",
    "expectedBenefit": "$11,000/year guaranteed income regardless of market performance"
  }
}
```

**Business Value:** Adds guaranteed income layer to unprotected portfolios

---

### 3. 📊 **TAX_INEFFICIENCY** Alert
**Opportunity:** Client has taxable investments that would benefit from tax deferral

**Detection Logic:**
- Taxable account holdings > $100K in high-turnover funds or dividend-heavy stocks
- Tax bracket: High (32%+)
- No annuities in taxable accounts
- Investment horizon > 5 years

**Example:**
```json
{
  "alertType": "TAX_INEFFICIENCY",
  "severity": "MEDIUM",
  "title": "High-Tax Drag on $300K Taxable Account",
  "opportunity": "Defer taxes on $200K by moving to non-qualified annuity",
  "annuityRecommendation": {
    "productType": "Non-Qualified Deferred Annuity",
    "allocation": 200000,
    "expectedBenefit": "~$8,000/year in tax savings (32% bracket on 12% annual income)",
    "strategy": "Tax-deferred growth until retirement when in lower bracket"
  }
}
```

**Business Value:** Tax optimization drives annuity adoption

---

### 4. 🔔 **CD_MATURITY** Alert
**Opportunity:** Client has CDs maturing soon—annuity could offer better rates

**Detection Logic:**
- CD holdings with maturity date within 90 days
- CD amount > $50,000
- Current CD rate < 4.0%
- Best fixed annuity rate > CD rate + 1.0%

**Example:**
```json
{
  "alertType": "CD_MATURITY",
  "severity": "HIGH",
  "title": "$150K CD Maturing in 30 Days at 3.5%",
  "opportunity": "Multi-year guaranteed annuity (MYGA) offering 5.5%",
  "annuityRecommendation": {
    "productType": "Multi-Year Guaranteed Annuity (MYGA)",
    "allocation": 150000,
    "guaranteedRate": 5.5,
    "term": "5 years",
    "expectedBenefit": "$3,000/year additional income vs. renewing CD"
  }
}
```

**Business Value:** Captures CD renewals before they auto-renew

---

### 5. 🚀 **INCOME_GAP** Alert
**Opportunity:** Client approaching retirement without sufficient guaranteed income sources

**Detection Logic:**
- Age 60+
- Retirement target year ≤ 3 years
- Primary objective: Income
- Current income need: Now or Soon
- Guaranteed income sources (Social Security + pensions) < 50% of pre-retirement income
- NO existing annuities with income riders

**Example:**
```json
{
  "alertType": "INCOME_GAP",
  "severity": "HIGH",
  "title": "Retirement in 2 Years: $40K Income Gap Identified",
  "opportunity": "Immediate or deferred income annuity to close gap",
  "annuityRecommendation": {
    "productType": "Deferred Income Annuity (DIA)",
    "allocation": 400000,
    "incomeStart": "2028",
    "guaranteedIncome": "$40,000/year for life",
    "expectedBenefit": "Close 100% of income gap with guaranteed lifetime payment"
  }
}
```

**Business Value:** Positions annuity as essential retirement income tool

---

### 6. 💡 **QUALIFIED_OPPORTUNITY** Alert
**Opportunity:** Large IRA that could benefit from partial annuitization

**Detection Logic:**
- IRA balance > $500,000
- Age 65+
- NO annuities in IRA
- RMD strategy concern (large future RMDs)

**Example:**
```json
{
  "alertType": "QUALIFIED_OPPORTUNITY",
  "severity": "MEDIUM",
  "title": "$850K IRA with No Annuity Allocation",
  "opportunity": "Annuitize 30% for guaranteed income + RMD management",
  "annuityRecommendation": {
    "productType": "Qualified Longevity Annuity Contract (QLAC)",
    "allocation": 200000,
    "expectedBenefit": "Defer RMDs, guaranteed lifetime income starting age 75",
    "strategy": "Reduce taxable RMDs while securing longevity income"
  }
}
```

**Business Value:** Taps into large IRA balances for annuity AUM

---

### 7. 🏠 **BENEFICIARY_PLANNING** Alert
**Opportunity:** Client needs guaranteed death benefit for estate planning

**Detection Logic:**
- Estate value > $1M
- Dependents or spouse
- NO life insurance or annuity death benefits
- Age < 70

**Example:**
```json
{
  "alertType": "BENEFICIARY_PLANNING",
  "severity": "MEDIUM",
  "title": "No Death Benefit Protection for $1.5M Estate",
  "opportunity": "Annuity with enhanced death benefit rider",
  "annuityRecommendation": {
    "productType": "Fixed Indexed Annuity with Enhanced Death Benefit",
    "allocation": 300000,
    "deathBenefitType": "Return of Premium + Index Gains",
    "expectedBenefit": "Guaranteed minimum death benefit protects portfolio downside"
  }
}
```

**Business Value:** Leverages estate planning concerns to sell annuities

---

### 8. 📉 **DIVERSIFICATION_GAP** Alert
**Opportunity:** Client portfolio lacks insurance products entirely

**Detection Logic:**
- Total portfolio > $500K
- Zero allocation to annuities or structured products
- Age 50+
- Risk tolerance: Conservative or Moderate

**Example:**
```json
{
  "alertType": "DIVERSIFICATION_GAP",
  "severity": "LOW",
  "title": "$1.2M Portfolio with 0% Insurance Products",
  "opportunity": "Diversify with 15-20% annuity allocation",
  "annuityRecommendation": {
    "productType": "Fixed Indexed Annuity",
    "allocation": 200000,
    "expectedBenefit": "Downside protection, tax deferral, guaranteed growth floor",
    "strategy": "Balance equity risk with guaranteed principal protection"
  }
}
```

**Business Value:** Positions annuity as portfolio diversifier

---

## Data Requirements: Client Position View

To generate these alerts, the system needs access to the client's **full investment portfolio**:

### Required Data Structure: `ClientPosition`

```json
{
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
    },
    {
      "positionId": "POS-003",
      "assetClass": "FIXED_INCOME",
      "accountType": "IRA",
      "description": "5-Year CD",
      "marketValue": 150000,
      "maturityDate": "2026-03-15",
      "currentRate": 0.035
    },
    {
      "positionId": "POS-004",
      "assetClass": "EQUITY",
      "accountType": "IRA",
      "symbol": "VTI",
      "description": "Vanguard Total Stock Market ETF",
      "quantity": 1200,
      "marketValue": 400000,
      "costBasis": 320000
    }
  ],
  "summary": {
    "equityAllocation": 0.68,
    "fixedIncomeAllocation": 0.12,
    "cashAllocation": 0.20,
    "annuityAllocation": 0.00,
    "taxable": 700000,
    "qualified": 550000
  }
}
```

### Minimum Data Points Required by Alert Type

| Alert Type | Required Data Points |
|------------|----------------------|
| **EXCESS_LIQUIDITY** | Cash positions, total portfolio value, client age |
| **PORTFOLIO_UNPROTECTED** | Equity allocation %, age, life stage, existing annuities |
| **TAX_INEFFICIENCY** | Taxable account holdings, tax bracket, dividend yield |
| **CD_MATURITY** | CD holdings, maturity dates, current CD rates, available MYGA rates |
| **INCOME_GAP** | Retirement target year, income objective, guaranteed income sources, portfolio value |
| **QUALIFIED_OPPORTUNITY** | IRA balance, age, existing IRA annuities |
| **BENEFICIARY_PLANNING** | Estate value, dependents, existing death benefits |
| **DIVERSIFICATION_GAP** | Full allocation breakdown, annuity allocation % |

---

## Implementation Priority

### Phase 1: Quick Wins (Implement First)
1. **EXCESS_LIQUIDITY** - Easy to detect, high conversion rate
2. **CD_MATURITY** - Time-sensitive, clear alternative product
3. **PORTFOLIO_UNPROTECTED** - Strong value proposition for retirees

### Phase 2: Strategic Growth
4. **INCOME_GAP** - Requires income planning calculation
5. **TAX_INEFFICIENCY** - Needs tax modeling
6. **DIVERSIFICATION_GAP** - Educational sell, lower urgency

### Phase 3: Advanced Opportunities
7. **QUALIFIED_OPPORTUNITY** - Complex IRA rules, QLAC education
8. **BENEFICIARY_PLANNING** - Requires estate planning integration

---

## Business Impact Projection

**Scenario:** Book of 500 clients with average $1.5M portfolio

| Alert Type | Detection Rate | Avg. Annuity Allocation | Annual New AUM |
|------------|----------------|------------------------|----------------|
| EXCESS_LIQUIDITY | 35% | $100K | $17.5M |
| PORTFOLIO_UNPROTECTED | 25% | $150K | $18.75M |
| CD_MATURITY | 15% | $120K | $9M |
| INCOME_GAP | 20% | $250K | $25M |
| TAX_INEFFICIENCY | 30% | $80K | $12M |
| **TOTAL** | - | - | **$82.25M** |

**Conservative Conversion Rate:** 20% of alerts result in annuity purchase  
**Projected New Annuity AUM:** $16.45M annually vs. $0 from replacement-only alerts

---

## Comparison: Replacement vs. Acquisition Alerts

| Metric | Replacement Alerts | Acquisition Alerts |
|--------|-------------------|--------------------|
| **Net New AUM** | $0 (moves existing) | $16.45M/year |
| **Client Experience** | Disruptive (surrender, new contract) | Additive (new allocation) |
| **Compliance Risk** | High (replacement forms) | Lower (new purchase) |
| **Revenue** | Shift commissions | **NEW commissions** |
| **Conversation** | "Your product is bad" | "You have an opportunity" |

---

## Next Steps

1. **Define Client Position Data Model**
   - Create Pydantic models for portfolio holdings
   - Define asset classes (equity, fixed income, cash, annuities, alternatives)
   - Add account type tracking (taxable, IRA, Roth, 401k)

2. **Expand Alert Type Enum**
   - Add 8 new acquisition alert types to `AlertType` enum
   - Update severity and scoring algorithms

3. **Create Alert Generation Logic**
   - Build detection functions for each new alert type
   - Implement scoring based on opportunity size and urgency

4. **Generate Sample Data**
   - Create `client_positions.json` with realistic portfolios
   - Include mix of allocation scenarios

5. **Update Batch Generator**
   - Extend overnight process to analyze position data
   - Generate acquisition alerts alongside replacement alerts

6. **UI Updates**
   - Add acquisition alert badges/icons
   - Create "Growth Opportunities" dashboard section
   - Separate replacement vs. acquisition alert views

---

**Key Insight:** This transforms the platform from a **portfolio management tool** (replacing existing annuities) to an **annuity sales platform** (identifying opportunities to GROW the annuity book of business).
