# Replacement Opportunities - Data Points & Scoring Documentation

## Overview
This document details the specific data points used from Policy, Client Profile, and Product sources to:
1. **Generate the Alert** (flag that opportunity exists) - **POLICY DATA ONLY**
2. **Score & Recommend** (determine priority and suggest products) - **POLICY + CLIENT PROFILE + PRODUCT**

---

## PART 1: Alert Generation (Policy Data Only)

### What is "Alert Generation"?

**Alert generation** is simply the automated identification that a policy MIGHT benefit from replacement. It's a flag that says:
> "This policy has characteristics suggesting a replacement review is warranted."

**At this stage, you are NOT:**
- Recommending any specific product
- Claiming it's suitable for the client
- Generating compliance paperwork
- Making any assertion about what should be done

**You ARE only saying:**
- "This policy shows a material performance gap vs. market"
- "Advisor should investigate this case"

---

### Minimum Data Required: POLICY ONLY

To **generate** a replacement opportunity alert, you need **ONLY 3 data points**:

| # | Source | Field Name | Data Type | Example Value |
|---|--------|------------|-----------|---------------|
| 1 | **Policy** | `currentCapRate` | number | 3.4 |
| 2 | **Policy** | `surrenderEndDate` | date | "2026-10-15" |
| 3 | **System Constant** | Market cap benchmark | number | 5.5 |

**That's it. You don't need client profile to generate the alert.**

---

### Alert Trigger Logic

```python
# Input: Policy data only
current_cap = policy.currentCapRate          # 3.4
surrender_end = policy.surrenderEndDate      # "2026-10-15"
market_cap = 5.5                             # System constant

# Calculate
cap_gap = market_cap - current_cap           # 5.5 - 3.4 = 2.1
days_to_surrender = (surrender_end - today).days  # 243 days
surrender_ending_soon = days_to_surrender < 365   # TRUE

# Decision: Generate alert?
if cap_gap > 2.0:
    generate_alert("REPLACEMENT_OPPORTUNITY", "Material performance gap")
elif surrender_ending_soon and cap_gap > 1.0:
    generate_alert("REPLACEMENT_OPPORTUNITY", "Surrender window + gap")
else:
    no_alert()
```

### Example: Alert Generation WITHOUT Client Profile

**Policy POL-001-2020 Data:**
- Current Cap Rate: 3.4%
- Surrender End Date: 2026-10-15 (8 months away)
- Account Value: $150,000

**Market Data:**
- Market Cap Benchmark: 5.5%

**Calculation:**
```
Cap gap: 5.5% - 3.4% = 2.1%
Trigger: 2.1% > 2.0% threshold? ✅ YES

ALERT GENERATED:
{
  "alertId": "ALT-POL-001-2020-REP",
  "type": "REPLACEMENT",
  "policyId": "POL-001-2020",
  "reason": "Material performance gap detected",
  "capGap": 2.1,
  "surrenderEndingSoon": true,
  "status": "NEEDS_REVIEW",
  "clientProfileRequired": true,  // For next step
  "generatedAt": "2026-02-24T09:00:00Z"
}
```

**No client data was used. No product was suggested. Just a flag raised.**

---

## PART 2: Alert Scoring & Product Recommendation (Requires Client Profile)

Once the alert is generated, you can optionally enhance it with additional data for scoring and product recommendations.

### Data Required for Full Scoring: POLICY + CLIENT PROFILE + PRODUCT

| Category | Data Points Needed | Source | Purpose |
|----------|-------------------|--------|---------|
| **Performance Gap** (40 pts) | Current cap, Best market cap | Policy + Product | Quantify opportunity size |
| **Suitability Match** (30 pts) | Age, Risk, Objectives, Time Horizon | **Client Profile** | Ensure suitable replacement |
| **Cost Savings** (20 pts) | Surrender charge, End date, Fees | Policy + Product | Financial benefit analysis |
| **Feature Upgrade** (10 pts) | Current riders, Available features | Policy + Product | Value-add opportunities |

### Without Client Profile: Limited Scoring

If you generate an alert **without client profile**, you can calculate a partial score:

```python
# Scoring without client profile
performance_gap = 30   # Can calculate from policy + market data
suitability_match = 0  # ❌ CANNOT calculate (need client age, risk, objectives)
cost_savings = 16.8    # Can calculate from policy data
feature_upgrade = 5.5  # Can identify features, but not personalize

partial_score = 30 + 0 + 16.8 + 5.5 = 52.3 / 95
priority = "LOW" (incomplete data, needs review)
```

### With Client Profile: Full Scoring

```python
# Scoring with client profile
performance_gap = 30
suitability_match = 24.5  # ✅ Can validate using client profile
cost_savings = 16.8
feature_upgrade = 5.5

full_score = 30 + 24.5 + 16.8 + 5.5 = 76.8 / 95
priority = "HIGH" (complete analysis, ready for action)
```

---

## Summary: Two-Phase Process

### Phase 1: Alert Identification (Policy Data Only)

**Purpose:** Flag policies that warrant review  
**Data Required:** 
- ✅ `policy.currentCapRate`
- ✅ `policy.surrenderEndDate`
- ✅ Market benchmark

**Output:**
```
Alert: "Policy POL-001-2020 shows 2.1% cap gap. Review recommended."
Status: NEEDS_REVIEW
Next Step: Load client profile for scoring
```

**Client Profile Required?** ❌ NO

---

### Phase 2: Alert Scoring & Product Recommendation

**Purpose:** Prioritize alerts and suggest suitable products  
**Data Required:**
- ✅ Policy data (from Phase 1)
- ✅ **Client profile** (age, risk, objectives, time horizon)
- ✅ Product catalog (alternative products, features)

**Output:**
```
Alert: "High Priority Replacement Opportunity"
Score: 77/95
Suitability: Validated ✅
Suggested Products: 
  - Product A (6.0% cap, matches Moderate risk)
  - Product B (5.8% cap, 7% income rider)
Next Step: Contact client
```

**Client Profile Required?** ✅ YES (for scoring & recommendations)

---

## When is Client Profile Actually Required?

### Two-Stage Process: Alert vs. Recommendation

There's an important distinction between:
1. **Generating an Alert** (identifying an opportunity exists)
2. **Making a Recommendation** (advising the client what to do)

#### Stage 1: Alert Generation - Policy Data Sufficient

**You CAN generate a replacement opportunity alert with ONLY policy data.**

The trigger logic only requires:
- `policy.currentCapRate` (e.g., 3.4%)
- `policy.surrenderEndDate` (e.g., "2026-10-15")
- Market cap benchmark (e.g., 5.5%)

```
IF (market_cap - current_cap) > 2.0% THEN alert_triggered = TRUE
```

**This identifies that an opportunity EXISTS.** You're simply flagging:
- "This policy has a significant performance gap"
- "Surrender period is ending soon"
- "Advisor should review this case"

**At this stage, you're NOT:**
- ❌ Recommending a specific replacement product
- ❌ Claiming the replacement is suitable
- ❌ Advising client action
- ❌ Generating compliance paperwork

**You're only saying:** "Hey, there's a potential opportunity here worth investigating."

---

#### Stage 2: Product Recommendation - Client Profile MANDATORY

**Once the alert is generated, client profile becomes ESSENTIAL for:**

1. **Scoring the Alert Priority (30% of score)**
   - Without client profile: Alert score = max 70/95 (missing 30% suitability points)
   - With client profile: Full 95-point scoring including suitability match
   
2. **Determining Suitable Replacement Products**
   - Age → Product eligibility filters
   - Risk tolerance → Appropriate product categories
   - Objectives → Feature requirements (growth, income, protection)
   - Time horizon → Surrender period matching

3. **Advisor Review & Client Communication**
   - Understanding client context
   - Preparing suitable alternatives
   - Explaining how replacement serves client goals

4. **Compliance & Documentation**
   - Replacement form completion
   - Suitability justification
   - Best interest standard documentation
   - Regulatory filing requirements

### The Practical Flow

```
SCENARIO: Policy Analysis Identifies Opportunity

Policy POL-001-2020:
├─ Current cap rate: 3.4%
├─ Market cap: 5.5%
├─ Cap gap: 2.1% → EXCEEDS 2.0% THRESHOLD
└─ Surrender ends: 8 months

DECISION: Generate Alert? YES
Reason: Policy data shows material performance gap
Alert Type: "Replacement Opportunity - Performance Gap"
Priority: To be determined (needs client profile for full scoring)

CLIENT PROFILE STATUS:
├─ Option A: Client profile available
│   ├─ Age: 62
│   ├─ Risk: Moderate
│   ├─ Objectives: Growth with Protection
│   └─ Action: Calculate full score (77/95 HIGH), suggest suitable products
│
└─ Option B: Client profile missing
    ├─ Alert generated: YES (opportunity identified)
    ├─ Full score: NO (capped at 70/95, missing suitability)
    ├─ Product suggestions: NO (cannot validate suitability)
    └─ Action: "Client profile required to proceed with recommendation"
```

---

### Alert Scoring Without Client Profile

**Limited Scoring Capability:**

| Category | Without Client Profile | With Client Profile |
|----------|----------------------|---------------------|
| Performance Gap | ✅ 30 points | ✅ 30 points |
| Suitability Match | ❌ 0 points (unknown) | ✅ 24.5 points |
| Cost Savings | ✅ 16.8 points | ✅ 16.8 points |
| Feature Upgrade | ⚠️ 5.5 points (generic) | ✅ 5.5 points (personalized) |
| **TOTAL SCORE** | **52.3 / 95** | **76.8 / 95** |
| **Priority Level** | **LOW** (incomplete data) | **HIGH** (complete analysis) |

**Key Difference:**
- Alert WITHOUT client profile: "There might be an opportunity, but we can't assess if it's suitable"
- Alert WITH client profile: "There IS an opportunity, it's suitable, and here are the right products"

---

### Why This Matters: The Two Schools of Thought

#### Approach 1: "Alert Generation Only Needs Policy Data" ✅ VALID

**Philosophy:** Cast a wide net, let advisors investigate

- Generate alerts based purely on policy metrics
- Flag all policies with performance gaps
- Let advisors pull client profiles during review
- Advisor determines suitability during conversation

**Pros:**
- Simpler system requirements
- No dependency on client data quality
- Identifies ALL potential opportunities

**Cons:**
- Many low-quality alerts (unsuitable scenarios)
- Advisor time wasted on dead-ends
- Client calls that go nowhere
- Lower advisor productivity

---

#### Approach 2: "Alert Generation Requires Full Context" ✅ ALSO VALID

**Philosophy:** Quality over quantity, advisor efficiency first

- Generate alerts only when full picture is available
- Pre-validate suitability before alerting
- Provide actionable, high-confidence opportunities
- Include suitable product suggestions in alert

**Pros:**
- High-quality, actionable alerts
- Advisor time spent efficiently
- Better client conversations
- Built-in compliance validation

**Cons:**
- Depends on current client profile data
- May miss opportunities if profiles are stale
- Requires data governance processes

---

### Recommendation: Hybrid Approach

**Best Practice: Use Policy Data to Generate Alerts, BUT Require Client Profile to Score Priority**

1. **Alert Trigger:** Policy data only
   - Identifies opportunities broadly
   - Low barrier to flag potential cases

2. **Alert Scoring:** Policy + Client profile
   - WITHOUT client profile → LOW priority (needs investigation)
   - WITH client profile → Accurate priority (HIGH/MEDIUM/LOW)

3. **Alert Actionability:**
   - WITHOUT client profile → "Review needed - update client profile"
   - WITH client profile → "Ready for client outreach - suitable products listed"

### Updated System Design

```
ALERT GENERATION LOGIC:

Step 1: Policy Analysis
├─ Load policy data
├─ Calculate cap gap
└─ IF gap > 2.0% OR (surrender ending AND gap > 1.0%)
    THEN generate_base_alert()

Step 2: Alert Scoring & Enrichment
├─ TRY load client profile
│   ├─ SUCCESS:
│   │   ├─ Calculate full 95-point score
│   │   ├─ Validate suitability
│   │   ├─ Suggest suitable products
│   │   └─ Priority: HIGH/MEDIUM/LOW based on full score
│   │
│   └─ FAILURE (client profile missing):
│       ├─ Calculate partial score (52/95 max)
│       ├─ Add flag: "client_profile_required": true
│       ├─ Suggest suitable products: NONE
│       └─ Priority: LOW (needs client data)
│
└─ Return enriched alert

Step 3: Advisor Workflow
├─ IF client_profile_required == true:
│   └─ Action: "Update client profile before proceeding"
│
└─ ELSE:
    └─ Action: "Ready for client outreach"
```

---

### The Truth: It Depends on Your Business Model

**For High-Touch Advisory Practices:**
- Generate alerts with policy data only
- Advisors review each case individually
- Client profile updated during discovery call
- **Decision: Client profile optional for alert generation**

**For Scalable, Automated Practices:**
- Pre-validate everything
- Only show high-quality, actionable alerts
- Minimize advisor time per alert
- **Decision: Client profile required for meaningful alerts**

**For Compliance-Heavy Firms:**
- Document suitability upfront
- Create audit trail before client contact
- Reduce compliance review burden
- **Decision: Client profile mandatory**

---

### Final Answer to "Do You Need Client Profile to Generate Alerts?"

**Short Answer: No, but...**

You can generate a replacement opportunity alert with ONLY policy data. The alert will say:
> "Policy POL-001-2020 has a 2.1% cap rate gap. Surrender ends in 8 months. This may be a replacement opportunity."

**However, without client profile, you CANNOT:**
- ✅ Assign accurate priority (score limited to 52/95)
- ✅ Validate suitability (violates best interest standard)
- ✅ Recommend specific products (don't know client needs)
- ✅ Generate compliance documentation (missing required data)
- ✅ Enable advisor to call client with confidence (incomplete picture)

**So the real question is:**
- Do you want to generate *alerts* (data available: policy only)? OR
- Do you want to generate *actionable recommendations* (data required: policy + client profile)?

**Most firms choose the latter because advisor time is expensive and compliance is mandatory.**

---

## Alert Trigger Logic

### Data Points Required to Generate Alert

| Source | Field Name | Data Type | Purpose |
|--------|------------|-----------|---------|
| **Policy** | `currentCapRate` | number | Primary performance metric |
| **Policy** | `surrenderEndDate` | date | Timing optimization |
| **Calculated** | Market cap average | number (5.5%) | Performance benchmark |

### Trigger Conditions

Alert is generated when **EITHER** condition is true:

**Condition 1: Material Performance Gap**
```
cap_gap = market_cap_average (5.5%) - policy.currentCapRate
IF cap_gap > 2.0% THEN generate_alert()
```

**Condition 2: Surrender Window + Performance Gap**
```
days_to_surrender_end = (policy.surrenderEndDate - today).days
surrender_ending_soon = days_to_surrender_end < 365

IF surrender_ending_soon AND cap_gap > 1.0% THEN generate_alert()
```

**Example:**
- Policy cap rate: 3.4%
- Market cap: 5.5%
- Cap gap: 2.1%
- Result: ✓ Alert triggered (Condition 1 met: 2.1% > 2.0%)

---

## AI Scoring Algorithm (0-95 Points)

Once an alert is triggered, the system calculates a confidence score using 31 data points across 4 weighted categories.

### Category 1: Performance Gap (40% weight, max 40 points)

**Purpose:** Quantify the improvement potential from replacement

#### Data Points Used:

| Source | Field | How It's Used |
|--------|-------|---------------|
| **Policy** | `currentCapRate` | Current policy performance baseline |
| **Product Catalog** | Best available cap rate | Target replacement performance |
| **Calculated** | Cap improvement % | `(target_cap - current_cap) / current_cap * 100` |

#### Scoring Formula:
```python
current_cap = policy.currentCapRate  # e.g., 3.4%
market_cap = 6.0  # Best alternative from product catalog

cap_improvement_pct = ((market_cap - current_cap) / current_cap) * 100
# Example: (6.0 - 3.4) / 3.4 * 100 = 76% improvement

performance_gap_score = min(40, (cap_improvement_pct / 100) * 40)
# Example: (76 / 100) * 40 = 30.4 points
```

**Example Result:** 30 points out of 40

---

### Category 2: Suitability Match (30% weight, max 30 points)

**Purpose:** Ensure replacement maintains or improves client suitability

#### Data Points Used:

| Source | Field | How It's Used | Sub-Score |
|--------|-------|---------------|-----------|
| **Client Profile** | `clientSuitabilityProfile.riskTolerance` | Match replacement risk level | 0-10 pts |
| **Client Profile** | `clientSuitabilityProfile.objectives` | Align with investment goals | 0-8 pts |
| **Client Profile** | `clientSuitabilityProfile.timeHorizon` | Match product term to timeline | 0-6.5 pts |
| **Client Profile** | `clientSuitabilityProfile.age` | Age-appropriate products | 0-5.5 pts |

#### Scoring Logic:
```python
suitability = client.clientSuitabilityProfile

# Risk Match (0-10 points)
risk_match = 10  # if replacement matches or improves risk profile
             = 5   # if partial match
             = 0   # if mismatch

# Objective Match (0-8 points)
objective_match = 8   # if objectives perfectly aligned
                = 5   # if some improvement
                = 0   # if misaligned

# Time Horizon Match (0-6.5 points)
time_horizon_match = 6.5  # if horizon matches
                   = 3.0  # if partial match
                   = 0    # if mismatch

suitability_score = risk_match + objective_match + time_horizon_match
# Max: 10 + 8 + 6.5 = 24.5 points (scaled to 30 max)
```

**Example Result:** 24.5 points out of 30

---

### Category 3: Cost Savings (20% weight, max 20 points)

**Purpose:** Assess financial impact considering surrender penalties and timing

#### Data Points Used:

| Source | Field | How It's Used |
|--------|-------|---------------|
| **Policy** | `surrenderEndDate` | Calculate time remaining |
| **Policy** | `surrenderCharge` | Current penalty amount |
| **Calculated** | Years remaining | Timing score modifier |
| **Product** | Fee differential | Cost comparison |

#### Scoring Formula:
```python
surrender_end = policy.surrenderEndDate
surrender_years_remaining = (surrender_end - today).days / 365

if surrender_years_remaining < 1.0:
    cost_savings_score = 16.8  # Low/no penalty
else:
    cost_savings_score = 10.0  # Penalty exists

# Additional fee savings bonus
fee_savings = current_fees - replacement_fees
if fee_savings > 0.3:  # 0.3% savings
    cost_savings_score += 3.2

# Max: 20 points
```

**Example Result:** 16.8 points out of 20 (surrender ending in 8 months)

---

### Category 4: Feature Upgrade (10% weight, max 10 points)

**Purpose:** Identify valuable features available in replacement products

#### Data Points Used:

| Source | Field | How It's Used |
|--------|-------|---------------|
| **Policy** | `riderType` | Current rider status |
| **Policy** | `incomeBase` | Income rider presence |
| **Product** | Income rider availability | Feature comparison |
| **Product** | Rollup rate | Income rider quality (e.g., 7%) |
| **Product** | Enhanced benefits | Additional features |

#### Scoring Formula:
```python
has_income_rider = "income" in policy.riderType.lower() or policy.incomeBase is not None
income_rider_available = True  # From product catalog

if income_rider_available and not has_income_rider:
    feature_score = 5.5  # Major feature addition
elif income_rider_available and has_income_rider:
    feature_score = 3.0  # Improved income rider
else:
    feature_score = 1.5  # Other enhancements

# Additional feature bonuses
if better_death_benefit:
    feature_score += 2.0
if better_liquidity:
    feature_score += 1.5

# Max: 10 points
```

**Example Result:** 5.5 points out of 10 (income rider opportunity)

---

## Complete Data Point Inventory

### From Policy Record (10 fields)

| # | Field Name | Data Type | Used In | Example |
|---|------------|-----------|---------|---------|
| 1 | `policyId` | string | Alert ID generation | "POL-001-2020" |
| 2 | `currentCapRate` | number | ⭐ Trigger, Performance scoring | 3.4 |
| 3 | `surrenderEndDate` | date | ⭐ Trigger, Cost scoring | "2026-10-15" |
| 4 | `surrenderCharge` | number/percent | Cost scoring | 2.0 (%) |
| 5 | `accountValue` | number | Context | 150000 |
| 6 | `issueDate` | date | Policy age calculation | "2020-02-15" |
| 7 | `riderType` | string | Feature scoring | "None" or "Income Rider" |
| 8 | `incomeBase` | number | Feature scoring | 142000 |
| 9 | `incomeActivated` | boolean | Feature scoring | false |
| 10 | `productType` | string | Product matching | "Fixed Indexed Annuity" |

⭐ = Critical fields required for alert generation

---

### From Client Profile (9 fields)

| # | Field Name | Data Type | Used In | Example |
|---|------------|-----------|---------|---------|
| 11 | `clientAccountNumber` | string | Identification | "ACC-8765-2019" |
| 12 | `firstName`, `lastName` | string | Identification | "Sarah", "Johnson" |
| 13 | `age` | number | ⭐ Suitability scoring | 62 |
| 14 | `riskTolerance` | string | ⭐ Suitability scoring | "Moderate" |
| 15 | `objectives` | string | ⭐ Suitability scoring | "Growth with Protection" |
| 16 | `timeHorizon` | string | ⭐ Suitability scoring | "Long-term (10+ years)" |
| 17 | `currentIncomeNeed` | string | Feature prioritization | "Soon" |
| 18 | `netWorth` | string | Context | "$500K - $1M" |
| 19 | `liquidityNeeds` | string | Cost tolerance | "Low" |

⭐ = Critical fields required for suitability validation

---

### From Product Catalog (8 fields)

| # | Field Name | Source | Used In | Example |
|---|------------|--------|---------|---------|
| 20 | Market cap average | Benchmark | ⭐ Trigger calculation | 5.5 |
| 21 | Best available cap | Product database | ⭐ Performance scoring | 6.0 |
| 22 | Income rider availability | Product features | Feature scoring | true |
| 23 | Income rider rollup rate | Product specs | Feature scoring | 7.0 (%) |
| 24 | Payout percentage | Product specs | Income calculations | 5.5 (%) |
| 25 | Fee structure | Product pricing | Cost scoring | 0.95 (%) |
| 26 | Death benefit options | Product features | Feature scoring | Enhanced |
| 27 | Withdrawal provisions | Product terms | Feature scoring | 10% penalty-free |

⭐ = Critical fields required for performance comparison

---

### Calculated/Derived Fields (4 fields)

| # | Field Name | Calculation | Used In | Example |
|---|------------|-------------|---------|---------|
| 28 | Days to surrender end | `(surrenderEndDate - today).days` | Trigger | 243 days |
| 29 | Cap rate gap | `market_cap - currentCapRate` | ⭐ Trigger, Scoring | 2.1% |
| 30 | Cap improvement % | `(gap / currentCapRate) * 100` | Performance scoring | 76% |
| 31 | Surrender years remaining | `days / 365` | Cost scoring | 0.67 years |

**Total: 31 data points analyzed**

---

## Scoring Example with Real Data

### Input Data

**Policy POL-001-2020:**
- `currentCapRate`: 3.4
- `surrenderEndDate`: "2026-10-15" (243 days away)
- `surrenderCharge`: 2.0
- `riderType`: "None"
- `accountValue`: 150000

**Client ACC-8765-2019:**
- `age`: 62
- `riskTolerance`: "Moderate"
- `objectives`: "Growth with Protection"  
- `timeHorizon`: "Long-term"

**Product Catalog:**
- Best cap rate: 6.0
- Income rider: Available (7% rollup)
- Fees: 0.95% (vs current 1.25%)

### Scoring Calculation

| Category | Calculation | Points | Weight |
|----------|-------------|--------|--------|
| **Performance Gap** | Cap improvement 76% → 30.4 pts | 30 | 40% |
| **Suitability Match** | All factors aligned → 24.5 pts | 24.5 | 30% |
| **Cost Savings** | Surrender ending soon → 16.8 pts | 16.8 | 20% |
| **Feature Upgrade** | Income rider available → 5.5 pts | 5.5 | 10% |
| **TOTAL AI SCORE** | Sum of all categories | **76.8** | 100% |

**Final Score:** 77 points (rounded)  
**Severity:** HIGH (≥75)  
**Confidence:** 87% (85% base + 2% for score above 75)

---

## Score-to-Severity Mapping

| AI Score | Severity | Confidence | Description |
|----------|----------|------------|-------------|
| **75-95** | HIGH | 85-95% | Strong replacement case |
| **60-74** | MEDIUM | 75-84% | Good opportunity |
| **0-59** | LOW | 65% | Marginal benefit |

**Confidence Formula:**
```python
if ai_score >= 75:
    confidence = 0.85 + (ai_score - 75) * 0.01  # 85-95%
elif ai_score >= 60:
    confidence = 0.75 + (ai_score - 60) * 0.01  # 75-84%
else:
    confidence = 0.65  # 65%
```

---

## Technical Reference

**Implementation:** [API/batch_alert_generator.py](API/batch_alert_generator.py)
- Trigger logic: `_should_generate_replacement_alert()` (Line 310)
- Scoring logic: `_calculate_replacement_score()` (Line 63)
- Alert creation: `_create_replacement_alert()` (Line 383)

**Algorithm Version:** 1.0.0  
**Last Updated:** February 24, 2026

---

## Key Takeaways

### Critical Data Points (Must Have)
These fields are essential for alert generation:
- ⭐ `policy.currentCapRate` - Triggers alert, scores performance
- ⭐ `policy.surrenderEndDate` - Triggers alert, scores timing
- ⭐ `client.age` - Ensures suitability
- ⭐ `client.riskTolerance` - Ensures suitability
- ⭐ `client.objectives` - Ensures suitability
- ⭐ Market cap benchmark - Triggers alert

**Without these fields, alerts cannot be generated.**

### Scoring Weights
- Performance Gap: **40%** (most important)
- Suitability Match: **30%** (compliance critical)
- Cost Savings: **20%** (financial benefit)
- Feature Upgrade: **10%** (value-add)

### Alert Quality Indicators
Higher scores indicate:
- Larger performance gaps
- Better timing (low/no surrender penalty)
- Valuable feature additions
- Maintained suitability alignment

---

## Summary: Understanding Data Requirements

### The Bottom Line

**Alert Generation:** Policy data is sufficient to identify opportunities  
**Actionable Recommendations:** Client profile is required for suitability validation

### The Three Data Layers

```
Layer 1: POLICY DATA (Identifies Opportunity)
├─ Cap rate gaps
├─ Surrender timing
└─ Feature limitations
    ↓ ALERT CAN BE GENERATED HERE
    ↓
Layer 2: CLIENT PROFILE (Validates Suitability & Scores Priority)
├─ Age, risk tolerance, objectives
├─ Time horizon, income needs
└─ Financial situation
    ↓ FULL SCORING & SUITABILITY VALIDATION
    ↓
Layer 3: PRODUCT CATALOG (Provides Solutions)
├─ Alternative products
├─ Better features
└─ Competitive pricing
    ↓
RESULT: Compliant, High-Confidence Replacement Recommendation
```

### Key Principles

1. **Two valid approaches:**
   - **Alert without client profile:** Possible, but limited (52/95 score max)
   - **Alert with client profile:** Full scoring and suitability validation (95/95 score max)

2. **Compliance is for recommendations, not alerts:**
   - Generating an alert = "There's an opportunity to investigate"
   - Making a recommendation = "You should replace with Product X"
   - Compliance requirements apply to recommendations, not alerts

3. **Business decision:**
   - High-touch firms: May prefer broader alerts, validate during advisor review
   - Scalable firms: May prefer validated alerts only, maximize advisor efficiency

### For Implementers

**Option A: Policy-Only Alert Generation**
- ✅ Trigger alerts based on policy data
- ⚠️ Score limited without client profile (max 52/95)
- ⚠️ Mark as "requires client profile review"
- ⚠️ No suitability validation or product suggestions

**Option B: Full-Context Alert Generation (Recommended)**
- ✅ Trigger alerts based on policy data
- ✅ Enhance with client profile for full scoring
- ✅ Validate suitability before showing to advisors  
- ✅ Include suitable product suggestions
- ✅ Generate compliance documentation

### Final Word

**The question "Do you need client profile?" depends on your goal:**

- Goal: Identify ALL potential opportunities → **Policy data sufficient**
- Goal: Provide actionable, compliant recommendations → **Client profile required**

Most firms choose the second approach because:
- Advisor time is expensive
- Compliance failures are costly
- Client trust requires proper validation
- Quality alerts drive better outcomes than quantity alerts
