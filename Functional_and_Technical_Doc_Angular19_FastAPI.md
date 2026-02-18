# In‑Force Annuity Review Platform — Functional + Technical Documentation - Hackathon Project
**Frontend:** Angular 19 (Web)  
**Backend:** Python FastAPI  
**Scope:** Hackathon PoC (idea-level UX; not final production UX)

---

## 1) Functional Documentation

### 1.1 Personas
- **Advisor (primary):** reviews in-force annuity policies, understands alerts, documents review rationale.
- **Supervisor/Compliance (secondary, optional):** audits review notes and rationale (read-only for PoC).

### 1.2 Core User Journeys

#### Journey A — Review a Policy with Multiple Alerts
1. Advisor opens **Policy Listing**.
2. Advisor sees **alert badges** on a policy (policy can have multiple).
3. Advisor clicks **Review** → opens **Policy Detail Modal**.
4. Modal shows **Current Policy Overview** (facts only).
5. Modal shows **Active Alerts Panel** (badges).
6. Advisor expands an **Alert Review Module** (accordion card).
7. Advisor optionally opens **AI Copilot Drawer** to:
   - explain the alert rationale,
   - summarize tradeoffs,
   - draft a neutral review note.
8. Advisor marks module as **Reviewed** and/or saves an **AI-generated note** (mock save is fine).

#### Journey B — Replacement Opportunity Review
1. Advisor expands **Replacement Opportunity** module.
2. Module shows **why flagged** and prompts advisor to **review/verify client suitability**.
3. Advisor reviews current suitability profile and optionally **updates key fields** (e.g., risk tolerance, objectives, life stage).
4. System refreshes and displays **illustrative market alternatives** (2–3) based on verified suitability with side-by-side comparison.
5. Advisor requests AI: "Summarize differences and risks (no recommendation)."
6. Advisor clicks "Initiate Replacement Review" (mock) and saves note.

#### Journey C — Income Activation Timing Review
1. Advisor expands **Income Activation** module.
2. Module shows **Begin Income Now vs Delay 2 Years** scenarios.
3. Advisor requests AI: “Explain timing tradeoffs for a client conversation.”
4. Advisor saves note and marks reviewed.

#### Journey D — Suitability Drift Review
1. Advisor expands **Suitability Drift** module.
2. Module shows neutral “what changed” bullets and “why review is appropriate.”
3. Advisor requests AI: “Draft a review note.”
4. Advisor saves note and marks reviewed.
#### Journey E — Missing Info Update (DTCC Administrative API)
1. Advisor expands **Missing Info** module.
2. Module displays:
   - Summary of missing/incomplete fields with severity indicators.
   - **Account Profile Information** (read-only, prefilled): owner name, SSN, address, contact details marked as "Auto-Applied on Submit."
   - **Policy-Specific Information** (editable form): beneficiary designations, tax withholding elections, special instructions.
3. Advisor fills in required fields (beneficiary name, relationship, allocation percentages, tax elections).
4. System validates entries (percentages total 100%, required fields complete, valid formats).
5. Advisor optionally requests AI: "Explain beneficiary designation best practices" or "What tax withholding should I recommend?"
6. Advisor clicks **Submit to DTCC**.
7. System shows loading state: "Submitting to DTCC Administrative API..." (mock 1-2 second delay).
8. System displays success message and logs DTCC payload (console for hackathon).
9. Policy data updated in-memory, alert removed from policy.
10. Advisor sees confirmation: "Policy updated successfully via DTCC Administrative API."
---

### 1.3 Functional Requirements

#### Policy Listing
- Display policy list with:
  - client name + account (3-6-3),
  - policy label (carrier/type/year),
  - renewal timing (optional),
  - alert summary badges (up to 3 + overflow `+N`),
  - Review action.
- Support opening policy detail modal from:
  - Review button (default focus to highest severity alert),
  - optional badge click (focus that alert).

#### Policy Detail Modal
- Always show **Current Policy Overview** (facts only).
- Show **Active Alerts Panel** (priority ordered).
- Render **Alert Review Modules** (accordion cards):
  - one module per alert type present,
  - only one module expanded at a time,
  - module includes: why flagged, suitability verification (Replacement only), risks, comparison/scenarios (if applicable), next actions, Ask AI.
  - **Replacement Opportunity modules** require suitability review/edit before displaying alternatives.
  - **Missing Info modules** display read-only account data and editable policy fields with DTCC submission workflow.
- Allow:
  - mark module reviewed (per-alert state),
  - save note (manual or AI drafted),
  - update client suitability (Replacement module),
  - submit non-financial updates via DTCC API (Missing Info module).

#### Alert Types (PoC)
- **Replacement Opportunity** (HIGH)
- **Income Activation** (MEDIUM)
- **Suitability Drift** (LOW/MEDIUM)
- **Missing Info** (MEDIUM)

#### AI Copilot Drawer
- Opens from Policy Detail modal without closing it.
- Shows context chips: client, policy, active module.
- Provides quick actions depending on active module.
- Maintains conversation history across module switches.
- Guardrails:
  - “Decision support — not a recommendation.”
  - Avoid “buy/sell” language; use neutral phrasing.

---

### 1.4 Business Rules (PoC-Level)
> AI-powered alert generation using weighted scoring algorithms. See Section 2.5 for detailed AI matching logic.

#### Replacement Opportunity (examples)
Trigger if any:
- Renewal within N days and rate/cap drops materially,
- Surrender schedule ending soon,
- Market benchmark for same type is materially higher,
- Product age > threshold (optional).

**AI Scoring:** Combines performance gap (40%), suitability improvement (30%), cost savings (20%), and feature upgrades (10%). Triggers at AI_Score > 75 for HIGH severity.

#### Income Activation (examples)
Trigger if:
- Income rider exists AND
- client age >= eligibility AND
- income not activated.

**AI Scoring:** Analyzes optimal activation timing through opportunity cost calculation (rollup gains vs. income foregone). Considers deferral bonuses, age-based payout increases, and client income needs.

#### Suitability Drift (examples)
Trigger if mismatch between:
- life stage vs product intent,
- risk tolerance vs product risk profile,
- objective shift (growth → income),
- portfolio overlap (optional).

**AI Scoring:** Weighted drift detection: risk tolerance (35%), primary objective (30%), financial situation (20%), time horizon (15%). Flags critical mismatches (e.g., income objective but no income rider).

#### Missing Info (examples)
Trigger if:
- Required non-financial data is incomplete or outdated (beneficiary designation, contact information, tax withholding elections),
- Regulatory-required fields are missing,
- Account profile information changed but not reflected in policy records.

**AI Scoring:** Evaluates data completeness (40%), recency (30%), regulatory importance (20%), and DTCC update eligibility (10%). Flags MEDIUM severity when critical non-financial data is missing or outdated beyond acceptable thresholds.

**DTCC Integration:** Uses DTCC Administrative API for non-financial updates. System auto-applies verified account/client profile data (name, SSN, address, contact details) and prompts advisor to complete policy-specific missing fields (beneficiary designations, percentages, tax elections). Mock implementation for hackathon.

_For comprehensive AI algorithm details, data points analyzed, and scoring formulas, see Section 2.5._

---

### 1.5 Non-Functional (Hackathon)
- Fast response: list < 1s, modal load < 2s (mock acceptable).
- Explainability: show “why flagged” bullets and “based on” hints.
- Auditability (light): store prompt/context/response (JSON log).
- Security (PoC): mock auth ok; do not store sensitive PII.

---

## 2) Technical Documentation

## 2.1 High-Level Architecture
- **Angular 19 Web App**
  - Policy Listing page
  - Policy Detail Modal
  - AI Copilot Drawer (global overlay)
- **FastAPI Backend**
  - Policy + client APIs (mock JSON or DB)
  - Alert engine (rules)
  - Market alternatives service (static catalog for PoC)
  - AI chat endpoint (calls LLM provider or mocked)
  - Audit log endpoint (optional)

### Data Flow (simplified)
1. Angular loads policy list → `GET /clients/{acct}/policies`
2. Open modal → `GET /policies/{policyId}` + `GET /clients/{acct}` (for suitability)
3. Alerts computed server-side → returned in policy payload
4. Expand replacement module → display suitability verification form
5. Update suitability (if needed) → `PATCH /clients/{acct}/suitability`
6. Fetch alternatives → `GET /policies/{policyId}/alternatives` (with updated suitability)
7. AI prompt → `POST /ai/chat` with context payload
8. Missing Info module → `POST /policies/{policyId}/update-non-financial` (mock DTCC API call)

---

## 2.2 Frontend — Angular 19

### 2.2.1 Project Structure (recommended)
```
src/
  app/
    core/
      api/
        policy.api.ts
        client.api.ts
        ai.api.ts
      models/
        client.model.ts
        suitability.model.ts
        policy.model.ts
        alert.model.ts
      services/
        policy.service.ts
        ai.service.ts
        ui-state.service.ts
      interceptors/
    features/
      policy-list/
        policy-list.component.ts
        policy-list.component.html
      policy-detail/
        policy-detail-modal.component.ts
        modules/
          replacement.module.component.ts
          income-activation.module.component.ts
          suitability-drift.module.component.ts
        components/
          suitability-form.component.ts
      ai-copilot/
        ai-drawer.component.ts
        quick-actions.component.ts
    shared/
      components/
        badge.component.ts
        accordion.component.ts
        compare-table.component.ts
      utils/
    app.routes.ts
    app.component.ts
```

### 2.2.2 State Management
- Use **Angular Signals** for UI state + derived state
- Use RxJS in API services (HttpClient) and bridge to signals
- Maintain a single **UIStateService** with:
  - selectedPolicyId
  - selectedClientAccount
  - clientSuitability (editable copy)
  - suitabilityVerified (boolean per module)
  - modalOpen
  - activeAlertType
  - expandedModuleId
  - aiDrawerOpen
  - aiContext (client/policy/activeAlert)

### 2.2.3 Modal + Drawer Interaction
- Policy detail is a **modal overlay**.
- AI Copilot is a **right-side drawer** attached to `body` (not nested).
- Clicking “Ask AI” sets `aiDrawerOpen=true` and updates context.

### 2.2.4 Component Contracts
- Policy Listing:
  - outputs: `review(policyId)`, optional `focusAlert(policyId, alertType)`
- Policy Detail Modal:
  - renders overview + alerts panel + modules
  - emits: close, setActiveAlert, openAIDrawer
- Alert Modules:
  - input: policy + alert + clientSuitability (for Replacement)
  - action: "Ask AI about this" updates context
  - Replacement module emits: `suitabilityUpdated`, `alternativesRequested`
- Suitability Form Component:
  - input: clientSuitability
  - outputs: `suitabilityChanged(updatedFields)`, `verified()`
  - validation: ensure required fields present
- AI Drawer:
  - input: aiContext
  - quick actions depend on activeAlertType
  - calls AI service

---

## 2.3 Backend — FastAPI

### 2.3.1 Service Layout (recommended)
```
backend/
  app/
    main.py
    api/
      clients.py
      policies.py
      ai.py
      audit.py (optional)
    models/
      client.py
      policy.py
      alert.py
      ai.py
    services/
      data_store.py
      alert_engine.py
      market_alternatives.py
      ai_service.py
      audit_log.py
    config.py
```

### 2.3.2 REST API Spec (PoC)

#### Clients
- `GET /clients/{clientAccountNumber}` → client + suitability profile
- `PATCH /clients/{clientAccountNumber}/suitability` → update suitability fields
  - request:
    ```json
    {
      "riskTolerance": "Moderate",
      "primaryObjective": "Income",
      "currentIncomeNeed": "Now",
      "lifeStage": "Pre-Retirement"
    }
    ```
  - response: updated suitability profile + timestamp

#### Policies
- `GET /clients/{clientAccountNumber}/policies` → summaries + alert summaries
- `GET /policies/{policyId}` → overview + full alerts
- `GET /policies/{policyId}/alternatives` → 2–3 illustrative alternatives
- `POST /policies/{policyId}/update-non-financial` → DTCC Administrative API integration (mock)
  - request:
    ```json
    {
      "accountProfileData": {
        "ownerName": "Jane Smith",
        "ssn": "***-**-1234",
        "address": "123 Main St, Boston, MA 02101",
        "email": "jane.smith@email.com",
        "phone": "(617) 555-0123"
      },
      "policySpecificData": {
        "primaryBeneficiary": {
          "name": "John Smith",
          "relationship": "Spouse",
          "ssn": "123-45-6789",
          "dateOfBirth": "1965-03-15",
          "allocationPercent": 100
        },
        "contingentBeneficiary": null,
        "taxWithholding": {
          "federal": 10,
          "state": 5
        },
        "specialInstructions": ""
      }
    }
    ```
  - response:
    ```json
    {
      "success": true,
      "dtccTransactionId": "DTCC-2026-0217-1234567",
      "message": "Policy updated successfully via DTCC Administrative API",
      "updatedFields": ["beneficiaries", "taxWithholding", "contactInfo"],
      "timestamp": "2026-02-17T20:45:30Z"
    }
    ```
  - **Mock Behavior**: Simulates 1-2 second delay, logs payload, updates in-memory data, removes alert

#### AI
- `POST /ai/chat`
  - request:
    ```json
    {
      "clientAccountNumber": "101-234-001",
      "policyId": "POL-2016-839",
      "activeAlertType": "REPLACEMENT",
      "userMessage": "Explain why this is flagged",
      "conversationId": "optional"
    }
    ```
  - response:
    ```json
    {
      "conversationId": "abc",
      "assistantMessage": "bullet response...",
      "basedOn": {
        "clientFields": ["age", "riskTolerance", "incomeNeed"],
        "policyFields": ["issueDate", "surrenderEnd", "renewalRate"],
        "alternativesUsed": ["ALT-A", "ALT-B"]
      }
    }
    ```

---

## 2.4 Alert Engine (Rules + Explainability)
- Deterministic rules output: type, severity, reasons, and evidence.
- Evidence feeds UI “why flagged” and AI “based on”.

Example output:
```json
{
  "type": "REPLACEMENT",
  "severity": "HIGH",
  "title": "Replacement Opportunity",
  "reasonShort": "Renewal in 15 days; cap drops materially",
  "reasons": [
    "Renewal within 15 days and cap drops from 5.5% to 2.0%",
    "Comparable market caps currently above 4.5%"
  ],
  "evidence": {
    "renewalDays": 15,
    "currentCap": 2.0,
    "priorCap": 5.5,
    "marketBenchmarkCap": 4.8
  }
}
```

---

## 2.5 AI Alert Generation Engine (Overnight Batch Processing)

### 2.5.1 Overview
The AI Alert Generation Engine runs as an overnight batch process that analyzes the combination of:
- Client suitability profiles
- Current policy details and performance metrics
- Product catalog with market rates
- Historical profile changes (drift detection)

Each alert type uses a specific AI matching algorithm with weighted scoring to determine if an alert should be triggered and at what severity level.

---

### 2.5.2 Alert Type 1: REPLACEMENT Opportunity

**AI Matching Algorithm:**

The replacement alert uses a multi-factor scoring system that combines:

**A) Performance Metrics Analysis (40% weight)**
- Current cap rate vs. market average for similar products
- Fee structure comparison (M&E, admin, rider costs)
- Historical crediting rate performance
- Surrender charge assessment (remaining years & percentage)
- Threshold: Cap rate gap > 2% triggers consideration

**B) Client Suitability Match (30% weight)**
- Risk tolerance alignment (Conservative/Moderate/Aggressive)
- Primary objective fit (Growth/Income/Protection/Legacy)
- Time horizon vs. surrender period remaining
- Liquidity needs vs. withdrawal restrictions
- Age appropriateness for product features

**C) Cost-Benefit Analysis (20% weight)**
- Total fee differential over expected holding period
- Surrender penalty vs. potential gains from better product
- Income rider value comparison (rollup rates, payout percentages)
- Break-even analysis for replacement decision

**D) Feature Upgrade Potential (10% weight)**
- Superior income riders available
- More flexible withdrawal provisions
- Better downside protection features
- Higher carrier financial ratings

**Scoring Formula:**
```
AI_Score = (Performance_Gap × 0.40) + 
           (Suitability_Improvement × 0.30) + 
           (Cost_Savings × 0.20) + 
           (Feature_Upgrade × 0.10)

Trigger Conditions:
- HIGH severity:   AI_Score > 75 AND Surrender_Penalty < Expected_Gain
- MEDIUM severity: AI_Score > 60 AND within 1 year of surrender end
- Confidence level: Based on data completeness and market stability
```

**Key Data Points Analyzed:**
- **From Client Profile:** age, risk tolerance, primary objective, time horizon, liquidity needs, net worth, annual income
- **From Current Policy:** cap rates, fixed rates, participation rates, M&E fees, admin fees, rider fees, surrender schedule, income rider terms, account value, policy age, issue date
- **From Product Catalog:** competitive cap rates, fee structures, income rider comparisons, surrender periods, state availability, carrier ratings

**AI Outputs:**
```json
{
  "ai_score": 82,
  "confidence": 0.87,
  "scoring_breakdown": {
    "performance_gap": 35.2,
    "suitability_improvement": 24.5,
    "cost_savings": 16.8,
    "feature_upgrade": 5.5
  },
  "key_factors": [
    "Cap rate gap: current 3.4% vs. available 6.0% (76% improvement)",
    "Income rider rollup: current none vs. available 7% annual",
    "Surrender period ending in 8 months"
  ],
  "data_points_analyzed": 23,
  "generated_at": "2026-02-16T02:15:00Z"
}
```

---

### 2.5.3 Alert Type 2: INCOME ACTIVATION Timing

**AI Matching Algorithm:**

The income activation alert uses timing optimization analysis:

**A) Client Situation Analysis**
- Current age vs. income rider activation eligibility age
- Stated income need date (from suitability profile)
- Retirement timeline and income gap analysis
- Current income sources and coverage

**B) Policy Mechanics Evaluation**
- Income rider rollup rate (e.g., 7% annually)
- Deferral bonuses (e.g., +10% bonus for waiting 3 years)
- Payout percentage by age (typically increases with age)
- Current income base vs. account value comparison

**C) Opportunity Cost Calculation**
- Delay 1 year: Gain = rollup increase vs. Loss = 1 year of income payments
- Delay 2 years: Gain = rollup + deferral bonus vs. Loss = 2 years income
- Break-even timeline calculation
- Optimal activation window determination
- Risk of client missing optimal date without guidance

**D) Urgency Factors**
- Age-based payout increase thresholds (e.g., 5% at 65, 5.5% at 66)
- Deferral bonus eligibility windows
- Client-stated income need proximity
- Market volatility impact on account value

**Scoring Formula:**
```
Urgency_Score = f(age, income_need_date, eligibility_date)
Delay_Cost = (rollup_gain + bonus) - (payout_value × delay_years)
Complexity_Factor = requires_explanation ? 1.2 : 1.0

AI_Score = Urgency_Score × Delay_Cost × Complexity_Factor

Trigger Conditions:
- HIGH severity:   Within 30 days of optimal activation OR high urgency
- MEDIUM severity: Within 90 days of optimal activation OR AI_Score > 60
- LOW severity:    Worth discussing but no immediate urgency
```

**Key Data Points Analyzed:**
- **From Client Profile:** age, income need date, retirement date, current income sources, income gap
- **From Policy:** income rider activation age, rollup rate, deferral bonuses, payout percentages by age, income base value, account value, years until next age threshold
- **Calculations:** break-even analysis, delay cost/benefit, optimal window

**AI Outputs:**
```json
{
  "ai_score": 68,
  "confidence": 0.92,
  "optimal_activation_window": {
    "start_date": "2026-06-01",
    "end_date": "2026-12-31",
    "reason": "Maximizes 7% rollup while meeting stated income need"
  },
  "scenarios": [
    {
      "action": "Activate Now",
      "income_base": "$142,000",
      "annual_income": "$7,100 (5.0% payout at age 60)"
    },
    {
      "action": "Delay 2 Years",
      "income_base": "$162,176 (after rollup)",
      "annual_income": "$8,919 (5.5% payout at age 62)",
      "tradeoff": "Give up $14,200 in income to gain $1,819/year ongoing"
    }
  ],
  "recommendation_type": "DISCUSSION_NEEDED",
  "key_factors": [
    "Client approaching income rider eligibility",
    "7% annual rollup creates significant deferral value",
    "Payout rate increases from 5.0% to 5.5% at age 62"
  ]
}
```

---

### 2.5.4 Alert Type 3: SUITABILITY DRIFT Detection

**AI Matching Algorithm:**

The suitability drift alert uses profile change detection with weighted mismatch scoring:

**A) Risk Tolerance Change (35% weight)**
- Original risk tolerance (from policy issue date)
- Current risk tolerance (from latest profile update)
- Product risk alignment check
- Drift magnitude: +/- 1 level = MEDIUM, +/- 2 levels = HIGH

**B) Primary Objective Shift (30% weight)**
- Original objective (e.g., "Growth")
- Current objective (e.g., "Income")
- Product feature alignment (does product have income rider if now income-focused?)
- Critical mismatches flagged immediately

**C) Financial Situation Change (20% weight)**
- Net worth change (+/- 30% threshold)
- Annual income change (+/- 25% threshold)
- Liquidity needs shifted
- Policy cost as % of income/net worth

**D) Time Horizon Change (15% weight)**
- Original time horizon
- Current time horizon (shortened = higher urgency)
- Surrender period remaining vs. time horizon
- Liquidity mismatch detection

**Drift Score Formula:**
```
Component_Scores:
  Risk_Drift = |current - original| × risk_importance × 0.35
  Objective_Drift = mismatch_severity × 0.30
  Financial_Drift = (net_worth_change + income_change) / 2 × 0.20
  Horizon_Drift = |current - original| × horizon_importance × 0.15

AI_Drift_Score = Σ(Component_Scores)

Trigger Conditions:
- HIGH severity:   Drift_Score > 75 OR critical mismatch detected
- MEDIUM severity: Drift_Score > 50 OR 2+ moderate changes
- LOW severity:    Drift_Score > 30 OR periodic review needed
- Confidence: Based on profile update completeness and recency
```

**Key Data Points Analyzed:**
- **From Client Profile (Original):** risk tolerance at issue, primary objective at issue, net worth at issue, income at issue, time horizon at issue, liquidity needs
- **From Client Profile (Current):** current risk tolerance, current objective, current net worth, current income, current time horizon, current liquidity needs
- **From Policy:** product type, features available (income rider, downside protection), risk level, cost structure, surrender period
- **Change History:** profile update timestamps, magnitude of changes, consistency of changes

**AI Outputs:**
```json
{
  "ai_score": 72,
  "confidence": 0.81,
  "drift_analysis": {
    "risk_tolerance": {
      "original": "Conservative",
      "current": "Moderate",
      "drift_score": 25.2,
      "severity": "MEDIUM"
    },
    "primary_objective": {
      "original": "Growth",
      "current": "Income",
      "drift_score": 21.6,
      "severity": "HIGH",
      "mismatch": "Policy lacks income rider feature"
    },
    "financial_situation": {
      "net_worth_change": "+42%",
      "income_change": "+18%",
      "drift_score": 14.4
    },
    "time_horizon": {
      "original": "15+ years",
      "current": "5-10 years",
      "drift_score": 10.8
    }
  },
  "critical_mismatches": [
    "Objective shifted to Income but policy has no income rider",
    "Time horizon shortened but 7 years surrender period remaining"
  ],
  "review_rationale": [
    "Client profile has materially changed since policy issue",
    "Current needs may not align with product features",
    "Suitability verification recommended per compliance"
  ],
  "last_profile_update": "2026-01-15T10:30:00Z"
}
```

---

### 2.5.4 Alert Type 4: MISSING INFO Detection (DTCC Administrative API)

**AI Matching Algorithm:**

The Missing Info alert identifies incomplete or outdated non-financial policy data that can be updated via DTCC Administrative API:

**A) Data Completeness Analysis (40% weight)**
- **Required Fields:** Beneficiary designation, owner contact information, tax withholding elections
- **Recommended Fields:** Contingent beneficiary, special instructions, distribution preferences
- **Field Status:**
  - Empty/null = 100% incomplete
  - Partial data = 50% incomplete (e.g., beneficiary name but no SSN)
  - Complete = 0% incomplete

**B) Data Recency Check (30% weight)**
- Last update timestamp vs. current date
- Account profile changes vs. policy records
- Regulatory update cycles (annual review recommended)
- Age thresholds:
  - < 1 year: 0 points
  - 1-3 years: 30 points
  - 3-5 years: 60 points
  - > 5 years: 100 points

**C) Regulatory Importance (20% weight)**
- Beneficiary designation: CRITICAL (required by regulation)
- Tax withholding: HIGH (IRS requirement)
- Contact information: MEDIUM (administrative best practice)
- Special instructions: LOW (optional)

**D) DTCC Update Eligibility (10% weight)**
- Field is eligible for DTCC Administrative API update
- No pending transactions that would block update
- Policy active and in good standing
- Carrier accepts DTCC administrative updates

**Missing Info Score Formula:**
```
Component_Scores:
  Completeness_Score = Σ(missing_required_fields × importance) / total_required × 0.40
  Recency_Score = age_score × field_importance × 0.30
  Regulatory_Score = Σ(missing_regulatory_fields) × severity × 0.20
  DTCC_Eligible_Score = updateable_fields_count / total_fields × 0.10

AI_Missing_Info_Score = Σ(Component_Scores)

Trigger Conditions:
- HIGH severity:   Score > 75 OR critical regulatory field missing
- MEDIUM severity: Score > 50 OR 2+ important fields missing/outdated
- LOW severity:    Score > 30 OR recommended field updates available
- Confidence: Based on data quality and last verification date
```

**Key Data Points Analyzed:**

**From Policy Record:**
- Beneficiary designation status (complete/incomplete)
- Beneficiary allocation percentages
- Tax withholding elections (federal/state)
- Last non-financial update timestamp
- Owner contact information on file
- Special instructions/preferences
- DTCC eligibility flags

**From Account/Client Profile:**
- Current owner name
- Current SSN/Tax ID
- Current registered address
- Current email address
- Current phone number
- Last profile update timestamp
- Profile verification status

**Field Comparison Matrix:**
| Field | Policy Record | Account Profile | Status | Action |
|-------|--------------|-----------------|--------|--------|
| Owner Name | Jane Smith | Jane M. Smith | Mismatch | Auto-update from profile |
| Address | 123 Main St (2020) | 456 Oak Ave (2025) | Outdated | Auto-update from profile |
| Email | NULL | jane@email.com | Missing | Auto-populate from profile |
| Beneficiary | NULL | N/A | Missing | Requires advisor input |
| Tax Withholding | 0% | N/A | Incomplete | Requires advisor input |

**AI Outputs:**
```json
{
  "alert_type": "MISSING_INFO",
  "severity": "MEDIUM",
  "ai_score": 68,
  "confidence": 0.92,
  "missing_fields_analysis": {
    "critical_missing": [
      {
        "field": "primary_beneficiary",
        "status": "NULL",
        "regulatory_requirement": "Required by state law",
        "last_verified": null,
        "priority": "CRITICAL"
      }
    ],
    "important_missing": [
      {
        "field": "tax_withholding_federal",
        "status": "Not elected",
        "regulatory_requirement": "IRS recommended",
        "last_verified": null,
        "priority": "HIGH"
      }
    ],
    "outdated_fields": [
      {
        "field": "owner_address",
        "policy_value": "123 Main St, Boston, MA 02101",
        "policy_last_updated": "2020-05-15",
        "profile_value": "456 Oak Ave, Cambridge, MA 02139",
        "profile_last_updated": "2025-11-20",
        "age_in_years": 5.8,
        "priority": "MEDIUM",
        "auto_update_eligible": true
      },
      {
        "field": "email_address",
        "policy_value": null,
        "profile_value": "jane.smith@email.com",
        "auto_update_eligible": true
      }
    ]
  },
  "dtcc_integration": {
    "eligible_for_update": true,
    "carrier_supports_admin_api": true,
    "estimated_fields_to_update": 5,
    "auto_apply_from_profile": [
      "owner_name",
      "ssn",
      "address",
      "email",
      "phone"
    ],
    "requires_advisor_input": [
      "primary_beneficiary",
      "contingent_beneficiary",
      "tax_withholding_elections"
    ]
  },
  "compliance_notes": [
    "Beneficiary designation recommended for estate planning",
    "Tax withholding elections help clients avoid year-end tax surprises",
    "Contact information updates ensure policy communications reach client"
  ],
  "key_factors": [
    "Primary beneficiary designation missing (required field)",
    "Owner contact information outdated by 5+ years",
    "Tax withholding elections never completed",
    "Account profile has current information available for auto-update"
  ],
  "generated_at": "2026-02-17T03:00:00Z",
  "algorithm_version": "missing_info_v1.0"
}
```

**DTCC Administrative API Mock Behavior:**
For hackathon purposes, the system simulates DTCC API integration:
1. Validates field completeness and formats
2. Creates DTCC payload with transaction ID
3. Simulates 1-2 second API call delay
4. Logs payload to console for demonstration
5. Updates in-memory policy data store
6. Removes alert from policy
7. Returns success response with mock transaction details

**Real-World Implementation Notes:**
In production, this would:
- Authenticate with DTCC using carrier credentials
- Submit non-financial updates via DTCC Administrative API
- Receive acknowledgment and transaction tracking ID
- Poll for completion status
- Handle errors and validations from DTCC
- Update policy system of record
- Audit log all DTCC transactions

---

### 2.5.5 AI Transparency & Auditability

All AI-generated alerts include:

**Explainability Fields:**
- `ai_score`: 0-100 numerical score
- `confidence`: 0-1.0 confidence level based on data quality
- `scoring_breakdown`: Component scores showing the math
- `data_points_analyzed`: Count of fields used in analysis
- `key_factors`: Human-readable bullet points (3-5 items)
- `generated_at`: Timestamp of alert generation
- `algorithm_version`: Version identifier for audit trail

**Auditability:**
- Input data snapshot (client profile + policy state at analysis time)
- Calculation methodology logged
- Threshold values and rules documented
- AI model version tracked
- Reproducible results for compliance review

**Example Alert with AI Fields:**
```json
{
  "alert_id": "ALT-20260216-001",
  "policy_id": "POL-90002",
  "type": "REPLACEMENT",
  "severity": "HIGH",
  "title": "Replacement Opportunity",
  "reason_short": "Material performance gap vs. market alternatives",
  "ai_analysis": {
    "ai_score": 82,
    "confidence": 0.87,
    "scoring_breakdown": {
      "performance_gap": 35.2,
      "suitability_improvement": 24.5,
      "cost_savings": 16.8,
      "feature_upgrade": 5.5
    },
    "key_factors": [
      "Cap rate gap: current 3.4% vs. available 6.0%",
      "Income rider opportunity: 7% rollup available",
      "Surrender period ending in 8 months"
    ],
    "data_points_analyzed": 23,
    "generated_at": "2026-02-16T02:15:00Z",
    "algorithm_version": "1.0.0"
  },
  "reasons": [
    "Current policy cap rate (3.4%) significantly below market (6.0%)",
    "No income rider; alternatives offer 7% rollup riders",
    "Surrender schedule ending soon reduces replacement cost"
  ]
}
```

---

## 2.6 AI Copilot Implementation (Real-Time Assistance)
- AI generates explanations, tradeoffs, and neutral documentation.
- AI does not recommend a product or decide timing.
- Prompts inject: suitability profile + policy facts + active alert evidence + AI analysis + optional alternatives.

---

## 2.7 Deployment (Hackathon)
- Angular build → static hosting (Amplify/S3)
- FastAPI → container or simple server (PoC ok)
- CORS configured for frontend origin
- `.env` for API base URL + LLM key

---

## 2.8 Testing (Minimal)
- Frontend: unit tests for modules; e2e smoke (open modal + open chat + send)
- Backend: unit tests for alert rules; API contract tests

---

## 3) Appendix — Key Decisions
- Overview remains factual and unchanged.
- Alerts render as accordion review modules.
- AI opens as global side drawer (no nested modals).
- Rules are deterministic; AI explains and drafts neutral text.
- Alternatives are illustrative (explicit disclaimer).
