# Replacement Transaction Standard - Quick Start Guide

> **🚀 NEW STANDARD ALERT**  
> This is the **IRI Annuity Replacement Transaction Standard (IARTS)** - a modern, JSON-based standard for annuity replacements.  
> **Not ACORD-compliant** - This is a next-generation format designed for API-first workflows.

## What is this?

A **brand new, standardized JSON payload format** for annuity replacement transactions that can be consumed by any order entry system. 

### Why Create a New Standard?

**Legacy ACORD XML is outdated for modern workflows:**
- ❌ Verbose XML format (100+ lines for simple transactions)
- ❌ Designed for batch EDI, not real-time APIs
- ❌ No built-in suitability or compliance workflow
- ❌ Complex to parse and validate
- ❌ Not AI-friendly

**IARTS (Our Standard) is purpose-built for 2026:**
- ✅ Clean JSON format (easy for any developer)
- ✅ REST API native (real-time processing)
- ✅ Compliance & suitability embedded
- ✅ Self-validating (Pydantic models)
- ✅ AI-ready (designed for recommendations & scoring)
- ✅ Modern developer experience

Think of it as **"ACORD for the API generation"** - same concept, better execution.

## Why use it?

✅ **Eliminates integration headaches** - One format works with any order entry system  
✅ **Compliance built-in** - All required fields for suitability and regulation  
✅ **Reduces errors** - Comprehensive validation before submission  
✅ **Audit-ready** - Complete transaction history and documentation trail  
✅ **Flexible** - Supports all replacement scenarios (1035, internal, qualified, etc.)  

## Quick Start

### 1. Install Dependencies

```bash
cd API
pip install -r requirements.txt
```

### 2. Try the Examples

```bash
python example_replacement_transactions.py
```

This generates 3 sample transactions:
- **External 1035 Exchange** (different carrier, non-qualified)
- **Internal Exchange** (same carrier)
- **Qualified IRA Exchange** (traditional IRA)

### 3. Start the API Server

```bash
uvicorn main:app --reload
```

Visit: http://localhost:8000/docs

### 4. Test the Endpoints

#### Validate a Transaction
```bash
POST /api/replacement-transactions/validate
Content-Type: application/json

{
  "transactionId": "TXN-2026-00001",
  "transactionType": "EXTERNAL_1035_EXCHANGE",
  ...
}
```

#### Submit a Transaction
```bash
POST /api/replacement-transactions/submit
Content-Type: application/json

{
  "transactionId": "TXN-2026-00001",
  ...
}
```

#### Create from Existing Data
```bash
POST /api/replacement-transactions/create-from-context?policy_id=POL-001&product_id=PROD-2024-FIA-001&client_account_number=123-456-789
```

This generates a pre-populated template from your existing policy, product, and client data.

## Key Concepts

### Transaction Types

| Type | Description | Use When |
|------|-------------|----------|
| `EXTERNAL_1035_EXCHANGE` | Different carrier, tax-free | Replacing with better product from another carrier |
| `INTERNAL_EXCHANGE` | Same carrier | Upgrading within same carrier |
| `PARTIAL_1035_EXCHANGE` | Partial exchange | Moving only part of the policy value |
| `SURRENDER_AND_NEW` | Full surrender + new app | Not using 1035 exchange |

### Exchange Types

- **FULL_1035** - Full tax-free exchange under IRC §1035
- **PARTIAL_1035** - Partial 1035 exchange
- **NON_QUALIFIED** - Not a 1035 exchange (taxable event)

### Premium Sources

- **EXCHANGE_PROCEEDS** - Money from existing policy only
- **ADDITIONAL_PREMIUM** - New money only
- **COMBINATION** - Both exchange + new money

## Typical Workflow

```
1. User selects policy to replace
   ↓
2. System recommends replacement products
   ↓
3. User selects new product & configures options
   ↓
4. System generates transaction template
   ↓
5. User completes suitability review
   ↓
6. System validates payload
   ↓
7. User signs compliance forms
   ↓
8. System submits to order entry
   ↓
9. Transaction processed by carrier
```

## Integration Pattern

### UI → API → Order Entry System

```javascript
// Frontend calls backend
const response = await fetch('/api/replacement-transactions/create-from-context', {
  method: 'POST',
  body: JSON.stringify({
    policy_id: currentPolicyId,
    product_id: selectedProductId,
    client_account_number: clientAccount
  })
});

const { template } = await response.json();

// Customize template with user selections
template.newProduct.selectedIndexOptions = userIndexSelections;
template.newProduct.selectedRiders = userRiderSelections;
template.complianceChecklist = completedChecklist;

// Validate
const validation = await fetch('/api/replacement-transactions/validate', {
  method: 'POST',
  body: JSON.stringify(template)
});

if (validation.isValid) {
  // Submit
  const submission = await fetch('/api/replacement-transactions/submit', {
    method: 'POST',
    body: JSON.stringify(template)
  });
  
  console.log('Confirmation:', submission.confirmationNumber);
}
```

### Backend → Order Entry System

```python
# Receive payload from UI
payload = ReplacementTransactionPayload(**request_data)

# Validate
is_valid = validate_transaction(payload)

if is_valid:
    # Submit to carrier's order entry system
    carrier_response = carrier_api.submit_application(
        payload.model_dump()
    )
    
    # Track in your system
    db.save_transaction(
        id=payload.transactionId,
        status='SUBMITTED',
        confirmation=carrier_response.confirmation_number
    )
```

## Required Fields Checklist

Before submission, ensure these are complete:

### Transaction Metadata
- [ ] Transaction ID
- [ ] Transaction type
- [ ] Exchange type
- [ ] Created date/timestamp

### Current Policy
- [ ] Policy number
- [ ] Account value
- [ ] Surrender value
- [ ] Owner name & SSN
- [ ] Replacement reasons

### New Product
- [ ] Product ID
- [ ] Initial premium (must equal exchange + additional)
- [ ] Selected index options (with allocations totaling 100%)
- [ ] Selected riders

### Client
- [ ] Full name, SSN, DOB, age
- [ ] Complete address
- [ ] Contact info (phone, email)
- [ ] Financial profile

### Beneficiaries
- [ ] At least one primary beneficiary
- [ ] Allocations total 100% per type

### Suitability
- [ ] Risk tolerance
- [ ] Investment objective
- [ ] Client confirmations (understands replacement, compared alternatives)

### Compliance
- [ ] Replacement form signed
- [ ] Suitability review completed & marked suitable
- [ ] 1035 form completed (if applicable)
- [ ] W-9 on file

### Advisor
- [ ] License number & state
- [ ] Carrier appointment confirmed
- [ ] Product training completed

## Common Validation Errors & Fixes

| Error | Fix |
|-------|-----|
| "Primary beneficiary allocations total 95%" | Ensure allocations sum to exactly 100% |
| "State replacement form not signed" | Mark `replacementFormSigned: true` and provide date |
| "Initial premium does not equal exchange + additional" | Recalculate: initialPremium = exchangeAmount + additionalPremium |
| "Advisor does not have carrier appointment" | Set `hasCarrierAppointment: true` or get appointment |
| "Surrender charges apply but no justification" | Provide `surrenderChargeJustification` text |

## Files in This System

| File | Purpose |
|------|---------|
| `app/models/replacement_transaction.py` | Complete data model definitions |
| `app/api/replacement_transactions.py` | API endpoints (validate, submit, etc.) |
| `example_replacement_transactions.py` | Sample payload generation code |
| `REPLACEMENT_TRANSACTION_STANDARD.md` | Full documentation |
| `REPLACEMENT_TRANSACTION_QUICK_START.md` | This file |

## Sample Payload Structure

```json
{
  "transactionId": "TXN-2026-00001",
  "transactionType": "EXTERNAL_1035_EXCHANGE",
  "exchangeType": "FULL_1035",
  "currentPolicy": {
    "policyNumber": "ABC123",
    "carrier": "Old Carrier",
    "accountValue": "250000.00",
    ...
  },
  "newProduct": {
    "productId": "PROD-001",
    "carrier": "New Carrier",
    "initialPremium": "250000.00",
    "selectedIndexOptions": [...],
    "selectedRiders": [...]
  },
  "client": {
    "firstName": "John",
    "lastName": "Smith",
    "age": 65,
    ...
  },
  "beneficiaries": [...],
  "suitabilityProfile": {...},
  "complianceChecklist": {...},
  "advisor": {...},
  "taxWithholding": {...}
}
```

## Next Steps

1. **Review Full Documentation**: See `REPLACEMENT_TRANSACTION_STANDARD.md`
2. **Run Examples**: `python example_replacement_transactions.py`
3. **Test API**: Start server and try endpoints at `/docs`
4. **Integrate**: Use the payload format in your UI and order entry systems
5. **Customize**: Extend the model for your specific carrier requirements

## Support

- **Full API Docs**: http://localhost:8000/docs (when server running)
- **Model Reference**: See `app/models/replacement_transaction.py`
- **Examples**: See `example_replacement_transactions.py`
- **Complete Guide**: See `REPLACEMENT_TRANSACTION_STANDARD.md`

---

**Version**: 1.0.0  
**Last Updated**: February 25, 2026
