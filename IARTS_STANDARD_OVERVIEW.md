# 🆕 NEW STANDARD: IARTS

## IRI Annuity Replacement Transaction Standard

![Status: Production Ready](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Version: 1.0.0](https://img.shields.io/badge/Version-1.0.0-blue)
![Format: JSON](https://img.shields.io/badge/Format-JSON-yellow)
![License: Proprietary](https://img.shields.io/badge/License-Proprietary-orange)

---

## 📋 Quick Facts

| Property | Value |
|----------|-------|
| **Standard Name** | IARTS (IRI Annuity Replacement Transaction Standard) |
| **Version** | 1.0.0 |
| **Release Date** | February 25, 2026 |
| **Format** | JSON (not XML) |
| **ACORD Compliant?** | ❌ No - This is a NEW proprietary standard |
| **Status** | Production Ready |
| **Open Source?** | Spec available, implementation proprietary |

---

## 🎯 What Is This?

**IARTS** is a **brand new, modern standard** for annuity replacement transaction payloads. It's designed from the ground up for:

- ✅ **API-first workflows** (not batch EDI)
- ✅ **Real-time processing** (not overnight files)
- ✅ **Compliance automation** (built-in suitability & reg checks)
- ✅ **AI integration** (recommendations, scoring, validation)
- ✅ **Developer experience** (clean JSON, self-documenting)

---

## 🆚 ACORD vs IARTS

| Feature | ACORD XML | **IARTS** |
|---------|-----------|-----------|
| Format | XML | **JSON** |
| Lines of Code | 130+ | **65 (50% less)** |
| Transport | Batch/EDI | **REST API** |
| Compliance | External | **Built-in** |
| AI-Ready | No | **Yes** |
| Type Safety | XSD Schema | **Pydantic Models** |
| Validation | External | **Automatic** |

**Result:** Same transaction, half the code, modern architecture.

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [**Full Standard Spec**](REPLACEMENT_TRANSACTION_STANDARD.md) | Complete field-by-field documentation |
| [**Quick Start Guide**](REPLACEMENT_TRANSACTION_QUICK_START.md) | Get started in 5 minutes |
| [**ACORD Comparison**](ACORD_VS_IARTS_COMPARISON.md) | Side-by-side format comparison |
| [**Examples**](API/example_replacement_transactions.py) | Working code examples |

---

## 💡 Key Innovations

### 1. **Compliance Built-In**
Unlike ACORD, compliance isn't an afterthought:
```json
{
  "complianceChecklist": {
    "replacementFormSigned": true,
    "suitabilityReviewCompleted": true,
    "isSuitable": true,
    "bestInterestDetermination": true,
    "is1035Exchange": true
  }
}
```

### 2. **Suitability Assessment Embedded**
Complete suitability profile in the transaction:
```json
{
  "suitabilityProfile": {
    "riskTolerance": "Moderate",
    "investmentObjective": "Income",
    "understandsReplacement": true,
    "comparedAlternatives": true
  }
}
```

### 3. **Replacement Justification**
AI-generated reasons documented inline:
```json
{
  "currentPolicy": {
    "replacementReason": [
      "Renewal rate drops to 4.5% from 6.0%",
      "Better income rider available",
      "Lower fees (2.5% → 1.8%)"
    ]
  }
}
```

### 4. **Type-Safe Validation**
Pydantic models catch errors before submission:
```python
# This will fail validation automatically
payload = ReplacementTransactionPayload(
    initialPremium=Decimal("250000"),
    exchangeAmount=Decimal("200000"),  # ❌ Doesn't equal initialPremium
    additionalPremium=Decimal("0")
)
# ValidationError: Initial premium must equal exchange + additional
```

---

## 🚀 API Endpoints

```bash
# Validate transaction
POST /api/replacement-transactions/validate

# Submit transaction
POST /api/replacement-transactions/submit

# Create from context (auto-populate from existing data)
POST /api/replacement-transactions/create-from-context
  ?policy_id=POL-001
  &product_id=PROD-2024-FIA-001
  &client_account_number=123-456-789

# Get transaction status
GET /api/replacement-transactions/{id}/status
```

---

## 🔌 Integration Examples

### JavaScript/TypeScript
```typescript
const transaction = {
  transactionId: "TXN-2026-00001",
  transactionType: "EXTERNAL_1035_EXCHANGE",
  currentPolicy: { ... },
  newProduct: { ... },
  client: { ... }
};

const response = await fetch('/api/replacement-transactions/submit', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(transaction)
});
```

### Python
```python
from app.models.replacement_transaction import ReplacementTransactionPayload

payload = ReplacementTransactionPayload(
    transactionId="TXN-2026-00001",
    transactionType="EXTERNAL_1035_EXCHANGE",
    # ... all fields
)

# Automatic validation
if payload.is_valid():
    submit_transaction(payload)
```

### Java
```java
ObjectMapper mapper = new ObjectMapper();
ReplacementTransaction txn = mapper.readValue(
    jsonString, 
    ReplacementTransaction.class
);
```

---

## 🏆 Benefits Over ACORD

### For Developers
- ✅ **50% less code** to write and maintain
- ✅ **Native JSON** - every language supports it
- ✅ **Self-documenting** - field names are clear
- ✅ **Auto-validation** - catch errors early
- ✅ **No XML parsing** - simple object mapping

### For Compliance Teams
- ✅ **Built-in checklist** - nothing gets missed
- ✅ **Audit trail** - complete transaction history
- ✅ **Suitability embedded** - review before submission
- ✅ **State-specific rules** - validated automatically

### For Business
- ✅ **Faster integration** - days instead of weeks
- ✅ **Real-time processing** - no batch delays
- ✅ **Lower error rates** - validation catches issues
- ✅ **AI-ready** - enables smart recommendations

---

## 📊 Adoption Roadmap

```
Phase 1: Internal Use (Current)
   └─ Annuity Review AI Platform uses IARTS

Phase 2: Partner Integration (Q2 2026)
   └─ Share spec with carrier partners
   └─ Build IARTS → ACORD converters

Phase 3: Industry Evangelism (Q3 2026)
   └─ Publish as open standard
   └─ Present at industry conferences
   └─ Build community around standard

Phase 4: Standards Body Submission (Q4 2026)
   └─ Consider ACORD/LIMRA submission
   └─ Potentially become official ACORD alternative
```

---

## 🤝 Partner Integration

Interested in using IARTS for your order entry system?

**Contact:**
- 📧 Email: [tech@example.com](mailto:tech@example.com)
- 💼 GitHub: [@iTheRakeshP](https://github.com/iTheRakeshP)
- 📖 Docs: [Full Specification](REPLACEMENT_TRANSACTION_STANDARD.md)

**We Provide:**
- ✅ Complete API documentation
- ✅ Integration examples (Python, JavaScript, Java)
- ✅ ACORD XML converters (for legacy systems)
- ✅ Technical support during integration
- ✅ Sample payloads and test data

---

## 📜 License

**Proprietary Standard - Available for Partner Use**

The IARTS specification is:
- ✅ **Freely viewable** - read the full spec
- ✅ **Free for integration** - use with our platform
- ✅ **Adaptable** - customize for your needs
- ⚠️ **Attribution required** - credit IRI when documenting

Contact us for commercial licensing or redistribution.

---

## 🌟 Why This Matters

The insurance industry has been using ACORD XML since the 1990s. While ACORD solved the batch processing problem, it's not designed for modern, real-time, API-driven workflows.

**IARTS represents a generational leap:**
- From **batch → real-time**
- From **XML → JSON**
- From **transaction → workflow**
- From **system-centric → human-centric**

This is our contribution to modernizing annuity processing. 🚀

---

<div align="center">

**IARTS v1.0.0** | © 2026 IRI Annuity Review AI Platform | [Full Documentation →](REPLACEMENT_TRANSACTION_STANDARD.md)

</div>
