# UI Specifications — In‑Force Annuity Review + AI Copilot - Hackathon Project

## 0. Goals
- Preserve existing UI theme and policy listing workflow.
- Support multiple alerts per policy without clutter.
- Open Policy Detail as a modal (no navigation).
- Provide AI Copilot as a right‑side drawer (no nested modals).
- Keep Policy Overview factual and static.
- Treat alerts as review modules, not actions.

---

## 1. Information Architecture

### Primary Surfaces
1. Policy Listing (Dashboard)
2. Policy Detail Modal
3. AI Copilot Drawer (Global)

---

## 2. Policy Listing (Dashboard)

### Purpose
Surface policies, show alert signals, and open policy review.

### Core Components
- Policy Table / List
- Columns:
  - Client Name
  - Client Account (3‑6‑3)
  - Policy (Carrier / Type)
  - Days to Renewal (if applicable)
  - Key KPI (rate impact, optional)
  - Alert Summary (badges)
  - Action: Review

### Alert Summary
- Up to 3 visible badges, overflow as +N
- Badge examples:
  - 🔴 Replacement Opportunity
  - 🟣 Income Activation
  - 🟡 Suitability Drift

### Interaction
- Review → opens Policy Detail Modal
- Clicking a badge (optional) → opens modal with that alert focused

---

## 3. Policy Detail Modal

### Purpose
Show current policy facts and allow structured review of alerts.

### Layout
Header
- Client Name + Account
- Policy Name / Carrier / Type
- Close (X)
- Ask AI button

Body
1. Current Policy Overview (always visible)
2. Active Alerts Panel
3. Review Modules (Accordion Cards)

---

### 3.1 Current Policy Overview
- Purely factual; does not change by alert.
- Examples:
  - Issue Date
  - Contract / Account Value
  - Surrender Schedule
  - Renewal terms / caps
  - Riders and fees

---

### 3.2 Active Alerts Panel
- Displays all alerts in priority order.
- Each alert shown as clickable pill:
  - [Severity] Title — short reason
- Clicking a pill:
  - Expands corresponding review module
  - Sets Active Review Context

---

## 4. Review Modules (Accordion Pattern)

### Rules
- One module per alert.
- Only one module expanded at a time.
- Expanded module may use internal scroll (max ~70vh).

### Module Header
- Severity icon + title
- One‑line reason
- Expand / collapse chevron

### Module Body Structure
1. Why this is flagged
2. Suitability verification (if applicable, e.g., Replacement Opportunity)
3. Key considerations / risks
4. Comparison or scenarios (if applicable)
5. Next‑step actions (mock allowed)
6. Ask AI about this module

**Note:** Replacement Opportunity modules use a multi-step workflow: flag reason → suitability review/edit → alternatives display.

---

## 5. Module Types

### 5.1 Replacement Opportunity (🔴)

#### Step 1: Why Flagged
- Display reasons/triggers (bullets)
- Compliance context for replacement reviews

#### Step 2: Verify Client Suitability
- Display current suitability profile (read-only fields + editable fields)
- Editable fields:
  - Risk Tolerance
  - Primary/Secondary Objectives
  - Current Income Need
  - Life Stage
  - Liquidity Importance
- Allow inline edit or modal edit form
- "Continue to Alternatives" button (disabled until suitability reviewed)
- Show last updated timestamp

#### Step 3: Market Alternatives
- Display after suitability verified
- Show 2–3 illustrative alternatives based on verified suitability
- Side‑by‑side comparison table
- Compliance note:
  - "Illustrative — Not a Recommendation"
  - "Based on suitability profile as of [timestamp]"

#### Actions
- Initiate Replacement Review
- Save Review Note
- Ask AI (available at each step)

---

### 5.2 Income Activation (🟣)
- Why flagged (eligibility + rider)
- Scenarios:
  - Begin Income Now
  - Delay Income (e.g., 2 years)
- Pros / Cons / Risks
- Actions:
  - Document Timing Decision
  - Generate Client Explanation (AI)

---

### 5.3 Suitability Drift (🟡)
- What changed (neutral bullets)
- Why review is appropriate
- No product comparison by default
- Actions:
  - Mark Reviewed
  - Save Review Note

---

## 6. Alert Severity & Default Focus

### Severity Order
1. 🔴 Replacement / Renewal critical
2. 🟣 Income Activation
3. 🟡 Suitability Drift
4. Informational

### Default Behavior
- Overview always visible
- Highest‑severity alert auto‑expanded
- Others collapsed

---

## 7. AI Copilot Drawer

### Placement
- Right‑side, fixed drawer
- Opens even when Policy Detail modal is open
- Never opens as a modal

### Header
- AI Copilot
- Context chips:
  - Client
  - Policy
  - Active Review Module
- Close (X)

### Chat Body
- Conversation thread
- Short, bullet‑first responses
- Optional Based on section

### Quick Actions (context‑aware)
- Replacement:
  - Explain alert
  - Review suitability changes (if any detected)
  - Compare options
  - Draft best‑interest summary
- Income:
  - Explain timing trade‑offs
  - Draft client explanation
- Drift:
  - Explain rationale
  - Draft review note

### Guardrails
- Decision support — not a recommendation label
- Copy / Save output buttons

---

## 8. Data Contracts (UI‑Facing)

### Alerts Object
```json
{
  "alertId": "ALT-001",
  "type": "REPLACEMENT | INCOME_ACTIVATION | SUITABILITY_DRIFT",
  "severity": "HIGH | MEDIUM | LOW",
  "title": "Replacement Opportunity",
  "reasonShort": "Renewal in 15 days; rate drops",
  "reasons": ["Surrender ending", "Market rates higher"],
  "createdAt": "2026-02-09"
}
```

### AI Chat Context Payload
```json
{
  "clientAccountNumber": "101-123456-001",
  "policyId": "POL-2016-839",
  "activeAlertType": "REPLACEMENT",
  "userMessage": "Draft best‑interest summary"
}
```

### Suitability Update Payload
```json
{
  "riskTolerance": "Moderate",
  "primaryObjective": "Income",
  "secondaryObjective": "Preservation",
  "currentIncomeNeed": "Now",
  "lifeStage": "Pre-Retirement",
  "liquidityImportance": "Medium",
  "updatedBy": "advisor-id",
  "updatedAt": "2026-02-16T14:30:00Z"
}
```

---

## 9. Acceptance Criteria

### Dashboard
- Policies show multiple alert badges
- Review opens modal with correct default alert

### Policy Detail Modal
- Overview always visible and unchanged
- All alerts shown
- One review module expanded at a time

### Replacement Opportunity Module
- Displays suitability verification step before showing alternatives
- Allows editing key suitability fields inline
- Refreshes alternatives after suitability update
- Shows timestamp of last suitability update
- Displays compliance disclaimer with alternatives

### AI Copilot
- Opens as side drawer without closing modal
- Context updates as active module changes
- Quick actions produce responses

---

## Design Principle (Final)
Overview = facts  
Alerts = reasons  
Review modules = investigation  
AI = explanation, not decisions
