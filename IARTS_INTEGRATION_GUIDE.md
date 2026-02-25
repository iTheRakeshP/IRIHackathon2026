# IARTS Ecosystem & Integration Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                   🆕 IARTS (IRI Annuity Replacement Transaction Standard)   │
│                                                                             │
│                         Modern JSON Standard for Annuity Replacements       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Data Flow Architecture

```
┌─────────────────┐
│                 │
│  Financial      │
│  Advisor        │
│                 │
└────────┬────────┘
         │
         │ Reviews policy
         │ Selects replacement product
         │
         v
┌─────────────────────────────────────┐
│                                     │
│  Annuity Review AI Platform (UI)   │
│  ─────────────────────────────────  │
│  • Policy Dashboard                 │
│  • AI Recommendations               │
│  • Product Comparison               │
│  • Suitability Assessment           │
│                                     │
└─────────────────┬───────────────────┘
                  │
                  │ Clicks "Start Replacement Transaction"
                  │
                  v
         ┌────────────────────┐
         │                    │
         │  API Endpoint      │
         │  ────────────      │
         │  POST /api/        │
         │  replacement-      │
         │  transactions/     │
         │  create-from-      │
         │  context           │
         │                    │
         └─────────┬──────────┘
                   │
                   │ Generates IARTS payload
                   │ from existing data:
                   │ • Current Policy
                   │ • Selected Product
                   │ • Client Profile
                   │
                   v
         ┌─────────────────────────────────┐
         │                                 │
         │  📋 IARTS JSON Payload          │
         │  ─────────────────────          │
         │  {                              │
         │    "transactionId": "...",      │
         │    "currentPolicy": {...},      │
         │    "newProduct": {...},         │
         │    "client": {...},             │
         │    "complianceChecklist": {...} │
         │  }                              │
         │                                 │
         └─────────┬───────────────────────┘
                   │
                   │ UI customizes:
                   │ • Index allocations
                   │ • Rider selections
                   │ • Beneficiaries
                   │ • Compliance forms
                   │
                   v
         ┌────────────────────┐
         │                    │
         │  API Endpoint      │
         │  ────────────      │
         │  POST /api/        │
         │  replacement-      │
         │  transactions/     │
         │  validate          │
         │                    │
         └─────────┬──────────┘
                   │
                   │ Validates:
                   │ • Required fields
                   │ • Business rules
                   │ • Compliance checklist
                   │ • Suitability
                   │
                   ├─── OK ──────────────┐
                   │                     │
                   │                     v
                   │           ┌────────────────────┐
                   │           │                    │
                   │           │  API Endpoint      │
                   │           │  ────────────      │
                   │           │  POST /api/        │
                   │           │  replacement-      │
                   │           │  transactions/     │
                   │           │  submit            │
                   │           │                    │
                   │           └─────────┬──────────┘
                   │                     │
                   │                     v
                   │           ┌─────────────────────────┐
                   │           │                         │
                   │           │  Order Entry Systems    │
                   │           │  ──────────────────     │
                   │           │                         │
                   v           │  Choose Integration:    │
        ┌──────────────┐      │                         │
        │              │      │  Option A: Direct       │
        │  Returns     │      │  ┌───────────────────┐  │
        │  Validation  │      │  │ Consume IARTS     │  │
        │  Errors      │      │  │ JSON directly     │  │
        │              │      │  └───────────────────┘  │
        │  UI shows    │      │                         │
        │  errors to   │      │  Option B: Convert      │
        │  advisor     │      │  ┌───────────────────┐  │
        │              │      │  │ Transform IARTS   │  │
        └──────────────┘      │  │ → ACORD XML       │  │
                              │  └───────────────────┘  │
                              │                         │
                              │  Option C: Hybrid       │
                              │  ┌───────────────────┐  │
                              │  │ Use IARTS API     │  │
                              │  │ Submit to carrier │  │
                              │  │ in their format   │  │
                              │  └───────────────────┘  │
                              │                         │
                              └─────────┬───────────────┘
                                        │
                                        │ Process Application
                                        │
                                        v
                              ┌─────────────────────────┐
                              │                         │
                              │  Insurance Carrier      │
                              │  ────────────────       │
                              │  • New policy issued    │
                              │  • 1035 exchange        │
                              │  • Old policy surrender │
                              │                         │
                              └─────────────────────────┘
```

---

## Integration Options for Order Entry Systems

### Option A: Native IARTS (Recommended for New Systems)

**Best for:** Modern platforms, new builds, API-first systems

```python
# Receive IARTS payload
iarts_payload = request.json

# Validate
validation = validate_iarts(iarts_payload)

if validation.is_valid:
    # Process directly
    application = create_application(iarts_payload)
    confirmation = submit_to_carrier(application)
    return {"success": True, "confirmation": confirmation}
```

**Advantages:**
- ✅ Simple, direct processing
- ✅ No conversion overhead
- ✅ Modern JSON handling
- ✅ Built-in validation

---

### Option B: IARTS → ACORD Conversion (For Legacy Systems)

**Best for:** Existing systems with ACORD XML requirements

```python
# Receive IARTS payload
iarts_payload = request.json

# Convert to ACORD XML
acord_xml = iarts_to_acord_converter(iarts_payload)

# Submit to existing ACORD processor
result = legacy_acord_processor.process(acord_xml)
return result
```

**Advantages:**
- ✅ Works with existing systems
- ✅ No changes to backend
- ✅ Gradual migration path
- ✅ Modern front-end, legacy back-end

---

### Option C: Gateway/Middleware Pattern

**Best for:** Large enterprises with multiple carriers

```python
# API Gateway receives IARTS
iarts_payload = request.json

# Route based on carrier
carrier = iarts_payload["newProduct"]["carrier"]

if carrier in modern_carriers:
    # Send IARTS directly
    result = send_iarts(carrier, iarts_payload)
elif carrier in legacy_carriers:
    # Convert to ACORD
    acord_xml = convert_to_acord(iarts_payload)
    result = send_acord(carrier, acord_xml)
else:
    # Custom integration
    custom_format = convert_to_custom(carrier, iarts_payload)
    result = send_custom(carrier, custom_format)

return result
```

**Advantages:**
- ✅ Supports all carriers
- ✅ Single API interface
- ✅ Flexible routing
- ✅ Easy to add new carriers

---

## Ecosystem Components

```
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│                    IARTS Ecosystem                             │
│                                                                │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  [Source Systems]          [IARTS Core]         [Target Systems] │
│                                                                │
│  • Annuity Review AI   →   • JSON Payload   →   • Order Entry  │
│  • CRM Systems         →   • Pydantic Models →  • Carriers     │
│  • Portfolio Tools     →   • REST API       →   • Custodians   │
│  • Compliance Systems  →   • Validation     →   • DTCC         │
│                                                                │
│                                                                │
│  [Converters & Tools]                                         │
│                                                                │
│  • IARTS → ACORD XML Converter                                │
│  • IARTS → DTCC ACATS Converter                               │
│  • JSON Schema Generator                                       │
│  • TypeScript Type Definitions                                 │
│  • OpenAPI Documentation                                       │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## Real-World Integration Examples

### Example 1: SaaS Order Entry Platform

**Scenario:** Modern cloud-based order entry system

```javascript
// Frontend sends IARTS payload
const transaction = {
  transactionId: generateId(),
  transactionType: "EXTERNAL_1035_EXCHANGE",
  currentPolicy: {...},
  newProduct: {...},
  compliance: {...}
};

await fetch('https://api.orderentry.com/v1/transactions', {
  method: 'POST',
  headers: { 
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${apiKey}`
  },
  body: JSON.stringify(transaction)
});
```

**Result:** Direct processing, no conversion needed.

---

### Example 2: Legacy Carrier Integration

**Scenario:** Carrier requires ACORD XML format

```python
# Middleware receives IARTS
from converters import IARTStoACORD

iarts_data = request.json

# Convert to ACORD
converter = IARTStoACORD()
acord_xml = converter.convert(iarts_data)

# Submit via SOAP
soap_client.submit_application(acord_xml)
```

**Result:** IARTS front-end, ACORD back-end, best of both worlds.

---

### Example 3: Multi-Carrier Distribution Platform

**Scenario:** Distribute to 50+ carriers with different formats

```python
# Smart routing gateway
class CarrierGateway:
    def submit_transaction(self, iarts_payload):
        carrier = iarts_payload['newProduct']['carrier']
        
        # Modern carriers - send IARTS
        if carrier in ['ModernLife', 'TechInsurance', 'CloudAnnuity']:
            return self.send_json(carrier, iarts_payload)
        
        # ACORD carriers - convert
        elif carrier in ['LegacyCorp', 'TraditionalIns']:
            acord_xml = self.convert_to_acord(iarts_payload)
            return self.send_xml(carrier, acord_xml)
        
        # Custom carriers - map fields
        else:
            custom_payload = self.map_to_custom(carrier, iarts_payload)
            return self.send_custom(carrier, custom_payload)
```

**Result:** Single IARTS input, flexible output routing.

---

## Migration Path

### Phase 1: Adoption
```
Your System (Today) → Add IARTS API → Continue ACORD backend
                                    → Build converter layer
```

### Phase 2: Dual Format
```
Your System → Accept both IARTS & ACORD → Route appropriately
            → IARTS: Modern carriers
            → ACORD: Legacy carriers
```

### Phase 3: Native IARTS
```
Your System → IARTS everywhere → Legacy carriers via converter
            → New carriers: native IARTS
            → Old carriers: auto-convert
```

---

## Benefits Summary

| Stakeholder | Benefit |
|------------|---------|
| **Advisors** | Fast, intuitive transactions |
| **Developers** | 50% less code, easier integration |
| **Compliance** | Built-in checklists, audit trails |
| **Carriers** | Real-time submissions, less errors |
| **Industry** | Modern standard for digital age |

---

## Getting Started with IARTS

1. **Read the Spec**: [Full Documentation](REPLACEMENT_TRANSACTION_STANDARD.md)
2. **Try Examples**: `python example_replacement_transactions.py`
3. **Test API**: `http://localhost:8000/docs`
4. **Integrate**: Choose your integration pattern above
5. **Deploy**: Submit real transactions

---

## Support & Resources

- 📖 **Full Spec**: [REPLACEMENT_TRANSACTION_STANDARD.md](REPLACEMENT_TRANSACTION_STANDARD.md)
- 🚀 **Quick Start**: [REPLACEMENT_TRANSACTION_QUICK_START.md](REPLACEMENT_TRANSACTION_QUICK_START.md)
- 🆚 **ACORD Comparison**: [ACORD_VS_IARTS_COMPARISON.md](ACORD_VS_IARTS_COMPARISON.md)
- 💻 **Code Examples**: [example_replacement_transactions.py](API/example_replacement_transactions.py)
- 🔌 **API Docs**: http://localhost:8000/docs (when running)

---

**IARTS v1.0.0** | © 2026 IRI Annuity Review AI Platform
