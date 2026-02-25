# Annuity Replacement Transaction Standard Payload

> **📌 NEW CUSTOM STANDARD** 
> This is a **proprietary standard** developed specifically for modern annuity replacement workflows.  
> While inspired by industry formats (ACORD, DTCC), this is **NOT an ACORD-certified standard**.  
> It represents a **next-generation approach** designed for digital-first annuity processing.

## Overview

This document defines the **IRI Annuity Replacement Transaction Standard (IARTS)** - a new, comprehensive payload format for annuity replacement transactions that can be consumed by any order entry system.

### What Makes This Standard Different?

**🆕 Purpose-Built for Modern Workflows**
- Unlike legacy ACORD XML formats, this uses modern JSON structure
- Designed for API-first integrations, not batch EDI processes
- Includes AI-driven suitability scoring and compliance automation
- Native support for digital signatures and document references

**✅ Comprehensive by Design**
- Goes beyond ACORD's transaction focus to include full compliance workflow
- Embeds suitability assessment directly in the transaction
- Supports real-time validation and pre-submission checks
- Designed for the modern advisor-client digital experience

### Supported Transaction Types

- **1035 Tax-Free Exchanges** (Full and Partial)
- **Internal Exchanges** (same carrier)
- **External Replacements** (different carrier)
- **Suitability & Compliance** requirements
- **State regulatory** requirements
- **Best Interest Standard** (Reg BI) compliance

## Key Features

### Why This Standard Exists

**Traditional ACORD Limitations:**
- ❌ ACORD XML is complex and verbose (designed for batch EDI)
- ❌ Limited support for modern compliance requirements (Reg BI, suitability)
- ❌ No built-in validation framework
- ❌ Doesn't include advisor-client interaction data
- ❌ Not optimized for real-time API consumption

**Our Standard Addresses These:**

✅ **Complete Data Model** - All required information for application processing  
✅ **Compliance Built-In** - Suitability, best interest, state requirements  
✅ **1035 Exchange Support** - Full/partial exchange handling  
✅ **Validation Ready** - Comprehensive validation rules  
✅ **Integration Friendly** - JSON format, REST API compatible  
✅ **Audit Trail** - Transaction tracking and status management  
✅ **Modern JSON API** - Easy to consume in any programming language  
✅ **Self-Documenting** - Pydantic models generate OpenAPI specs automatically  
✅ **Type-Safe** - Strong typing prevents integration errors  
✅ **Extensible** - Easy to add carrier-specific fields  

## Standard Payload Structure

### Format Comparison: ACORD vs IARTS

| Aspect | ACORD XML | **IARTS (Our Standard)** |
|--------|-----------|--------------------------|
| **Format** | XML | JSON |
| **Transport** | Batch EDI, File Transfer | REST API, Real-time |
| **Verbosity** | High (100+ lines for simple transaction) | Low (concise, readable) |
| **Validation** | External schema validation | Built-in Pydantic validation |
| **Compliance** | Transaction-focused | Workflow-focused (suitability included) |
| **Extensibility** | Complex schema updates | Easy field additions |
| **Type Safety** | WSDL/XSD required | Native TypeScript/Python types |
| **AI Integration** | Not designed for AI | AI-ready (suitability scoring, recommendations) |
| **Developer Experience** | Steep learning curve | Intuitive, self-documenting |
| **Industry Adoption** | Established (legacy systems) | Emerging (modern platforms) |

### High-Level Components

```
ReplacementTransactionPayload
├── Transaction Metadata (ID, type, status, timestamps)
├── Current Policy Information (policy being replaced)
├── New Product Selection (replacement product details)
├── Client Information (owner, annuitant)
├── Beneficiary Designations
├── Suitability Profile
├── Compliance Checklist
├── Advisor Information
├── Tax Withholding Elections
└── Supporting Documentation
```

## Payload Sections

### 1. Transaction Metadata

Core transaction tracking information:

```json
{
  "transactionId": "TXN-2026-00001",
  "transactionType": "EXTERNAL_1035_EXCHANGE",
  "exchangeType": "FULL_1035",
  "premiumSource": "EXCHANGE_PROCEEDS",
  "status": "INITIATED",
  "createdDate": "2026-02-25",
  "createdTimestamp": "2026-02-25T10:30:00Z",
  "sourceSystem": "AnnuityReviewAI"
}
```

**Transaction Types:**
- `INTERNAL_EXCHANGE` - Same carrier replacement
- `EXTERNAL_1035_EXCHANGE` - Different carrier, tax-free under IRC §1035
- `PARTIAL_1035_EXCHANGE` - Partial 1035 exchange
- `SURRENDER_AND_NEW` - Full surrender + new application

**Exchange Types:**
- `FULL_1035` - Full IRC 1035 tax-free exchange
- `PARTIAL_1035` - Partial 1035 exchange  
- `NON_QUALIFIED` - Not a 1035 exchange

**Premium Sources:**
- `EXCHANGE_PROCEEDS` - From existing policy only
- `ADDITIONAL_PREMIUM` - New money only
- `COMBINATION` - Exchange + new money

### 2. Current Policy Information

Complete details of the policy being replaced:

```json
{
  "currentPolicy": {
    "policyNumber": "ABC123456",
    "carrier": "Legacy Insurance Co",
    "carrierCode": "12345",
    "productName": "Legacy FIA 2015",
    "productType": "FIA",
    
    "accountValue": "250000.00",
    "surrenderValue": "248000.00",
    "surrenderCharge": "2000.00",
    "surrenderChargePercent": 0.8,
    
    "issueDate": "2015-03-15",
    "ownerName": "John Smith",
    "ownerSSN": "***-**-1234",
    "annuitantName": "John Smith",
    "annuitantDOB": "1960-05-20",
    
    "qualifiedStatus": "NON_QUALIFIED",
    "costBasis": "200000.00",
    "gainLoss": "50000.00",
    
    "hasIncomeRider": true,
    "incomeRiderName": "Guaranteed Lifetime Income",
    "incomeBase": "280000.00",
    "isIncomeActivated": false,
    
    "replacementReason": [
      "Renewal rate drops to 4.5% from 6.0%",
      "Better income rider available",
      "Lower fees on new product"
    ],
    "surrenderChargeJustification": "Savings from better rates exceed surrender charge within 2 years"
  }
}
```

**Critical Fields:**
- `accountValue` - Current contract value
- `surrenderValue` - Amount available for exchange
- `costBasis` - Tax basis (critical for reporting)
- `gainLoss` - Current gain/loss
- `isIncomeActivated` - Whether income withdrawals have started

### 3. New Product Selection

Details of the replacement product:

```json
{
  "newProduct": {
    "productId": "PROD-2024-FIA-001",
    "carrier": "Modern Annuity Co",
    "carrierCode": "67890",
    "productName": "Income Plus FIA 2024",
    "productType": "FIA",
    
    "initialPremium": "248000.00",
    "exchangeAmount": "248000.00",
    "additionalPremium": "0.00",
    
    "selectedIndexOptions": [
      {
        "indexName": "S&P 500",
        "strategy": "Annual Point-to-Point Cap",
        "allocationPercent": 60,
        "currentCap": 7.5
      },
      {
        "indexName": "Fixed Account",
        "strategy": "Fixed",
        "allocationPercent": 40,
        "currentRate": 4.0
      }
    ],
    
    "selectedRiders": [
      {
        "riderName": "Lifetime Income Protector Plus",
        "riderType": "Income",
        "annualFee": 1.25,
        "rollUpRate": 7.0,
        "payoutRate": 5.5
      }
    ],
    
    "bonusRate": 10,
    "bonusAmount": "24800.00"
  }
}
```

### 4. Client Information

Complete owner/client demographics:

```json
{
  "client": {
    "firstName": "John",
    "middleName": "A",
    "lastName": "Smith",
    "ssn": "123-45-6789",
    "dateOfBirth": "1960-05-20",
    "age": 65,
    "gender": "M",
    "citizenship": "USA",
    
    "address": "123 Main Street",
    "city": "Anytown",
    "state": "CA",
    "zipCode": "90210",
    "phone": "555-123-4567",
    "email": "john.smith@email.com",
    
    "annualIncome": "$100,000 - $150,000",
    "netWorth": "$1M - $2M",
    "liquidNetWorth": "$500K - $1M",
    "taxBracket": "24%",
    
    "employmentStatus": "Retired",
    "occupation": "Former Engineer",
    "employer": "N/A"
  }
}
```

### 5. Beneficiary Designations

Primary and contingent beneficiaries:

```json
{
  "beneficiaries": [
    {
      "beneficiaryType": "PRIMARY",
      "firstName": "Jane",
      "lastName": "Smith",
      "relationship": "Spouse",
      "ssn": "987-65-4321",
      "dateOfBirth": "1962-08-15",
      "allocationPercent": 100.0,
      "address": "123 Main Street",
      "city": "Anytown",
      "state": "CA",
      "zipCode": "90210",
      "phone": "555-123-4567",
      "email": "jane.smith@email.com"
    },
    {
      "beneficiaryType": "CONTINGENT",
      "firstName": "Michael",
      "lastName": "Smith",
      "relationship": "Son",
      "dateOfBirth": "1990-03-10",
      "allocationPercent": 50.0
    },
    {
      "beneficiaryType": "CONTINGENT",
      "firstName": "Sarah",
      "lastName": "Johnson",
      "relationship": "Daughter",
      "dateOfBirth": "1992-07-22",
      "allocationPercent": 50.0
    }
  ]
}
```

**Validation Rules:**
- Primary beneficiary allocations must total 100%
- Contingent beneficiary allocations must total 100%
- SSN required for allocations > 50%

### 6. Suitability Profile

Client suitability assessment for compliance:

```json
{
  "suitabilityProfile": {
    "riskTolerance": "Moderate",
    "investmentObjective": "Income",
    "investmentExperience": "Extensive",
    "investmentHorizon": "Long (7+ years)",
    
    "liquidityNeeds": "Low",
    "timeHorizon": "10+ years",
    "surrenderChargeAcceptance": true,
    
    "currentIncomeNeeded": false,
    "futureIncomeNeeded": true,
    "incomeStartYear": 2028,
    
    "totalAnnuityHoldings": "500000.00",
    "percentageInAnnuities": 25.0,
    
    "understandsReplacement": true,
    "comparedAlternatives": true,
    "reviewedSurrenderCharges": true
  }
}
```

### 7. Compliance Checklist

Required compliance verifications:

```json
{
  "complianceChecklist": {
    "replacementFormSigned": true,
    "replacementFormDate": "2026-02-24",
    
    "suitabilityReviewCompleted": true,
    "suitabilityDeterminationDate": "2026-02-24",
    "isSuitable": true,
    "suitabilityNotes": "Transaction meets client objectives for guaranteed lifetime income",
    
    "bestInterestDetermination": true,
    "alternativesConsidered": 3,
    
    "is1035Exchange": true,
    "exchangeFormCompleted": true,
    
    "stateApprovalRequired": false,
    "stateApprovalReceived": false,
    
    "freeLookPeriodDisclosed": true,
    "freeLookDays": 30,
    
    "seniorProtectionApplies": true,
    "longerFreeLookApplies": false
  }
}
```

### 8. Advisor Information

Financial professional details:

```json
{
  "advisor": {
    "advisorId": "ADV-12345",
    "firstName": "Jane",
    "lastName": "Advisor",
    "email": "jadvisor@firm.com",
    "phone": "555-987-6543",
    
    "licenseNumber": "CA-INS-123456",
    "licenseState": "CA",
    
    "hasCarrierAppointment": true,
    "appointmentNumber": "APPT-67890",
    
    "hasProductTraining": true,
    "completedCE": true,
    
    "firmName": "Premier Financial Advisors",
    "firmAddress": "456 Business Blvd, Suite 200, Anytown, CA 90211",
    "bdName": "National Broker-Dealer LLC",
    "bdCRD": "12345"
  }
}
```

### 9. Tax Withholding Elections

Tax withholding preferences:

```json
{
  "taxWithholding": {
    "federalWithholding": false,
    "federalPercent": null,
    "federalFlatAmount": null,
    
    "stateWithholding": false,
    "statePercent": null,
    "stateFlatAmount": null,
    
    "w9OnFile": true,
    "w9Date": "2026-02-20"
  },
  
  "qualifiedStatus": "NON_QUALIFIED",
  "qualificationType": null,
  "custodianName": null,
  "custodianAccountNumber": null
}
```

For **Qualified Money** (IRA, 403(b), etc.):

```json
{
  "qualifiedStatus": "QUALIFIED",
  "qualificationType": "Traditional IRA",
  "custodianName": "National Trust Company",
  "custodianAccountNumber": "IRA-987654321"
}
```

### 10. Supporting Documentation

References to required documents:

```json
{
  "documents": [
    {
      "type": "StateReplacementForm",
      "filename": "CA_Replacement_Form_Signed.pdf",
      "reference": "DOC-2026-001",
      "uploadedAt": "2026-02-24T14:30:00Z"
    },
    {
      "type": "1035ExchangeForm",
      "filename": "1035_Exchange_Authorization.pdf",
      "reference": "DOC-2026-002"
    },
    {
      "type": "W9Form",
      "filename": "W9_JohnSmith.pdf",
      "reference": "DOC-2026-003"
    },
    {
      "type": "SuitabilityWorksheet",
      "filename": "Suitability_Assessment.pdf",
      "reference": "DOC-2026-004"
    }
  ]
}
```

## API Endpoints

### Validate Transaction

**POST** `/api/replacement-transactions/validate`

Validates a transaction payload without submitting it.

**Request Body:** Full `ReplacementTransactionPayload`

**Response:**
```json
{
  "isValid": true,
  "errors": [],
  "warnings": [
    "Client age above typical maximum (85) - may require underwriting"
  ],
  "missingFields": [],
  "complianceFlags": []
}
```

### Submit Transaction

**POST** `/api/replacement-transactions/submit`

Submits a validated transaction for processing.

**Request Body:** Full `ReplacementTransactionPayload`

**Response:**
```json
{
  "success": true,
  "transactionId": "TXN-2026-00001",
  "confirmationNumber": "CONF-A1B2C3D4",
  "status": "SUBMITTED",
  "message": "Transaction submitted successfully",
  "nextSteps": [
    "1035 exchange form will be sent to surrendering carrier",
    "Client will receive confirmation within 2 business days",
    "Application will be submitted to new carrier",
    "Expect processing time of 5-10 business days",
    "Free look period: 30 days from delivery"
  ],
  "estimatedCompletionDate": "2026-03-10",
  "errors": [],
  "warnings": []
}
```

### Create from Context

**POST** `/api/replacement-transactions/create-from-context`

Helper endpoint to generate a transaction template from existing policy, product, and client data.

**Query Parameters:**
- `policy_id` - ID of policy being replaced
- `product_id` - ID of new product selection
- `client_account_number` - Client account number

**Response:**
```json
{
  "message": "Transaction template created from context",
  "transactionId": "TXN-20260225-ABC12345",
  "template": { ...full payload with defaults... },
  "notes": [
    "This is a TEMPLATE with default values",
    "UI must populate missing required fields",
    "Compliance checklist items must be completed",
    "Client confirmations required before submission"
  ]
}
```

### Get Transaction Status

**GET** `/api/replacement-transactions/{transaction_id}/status`

Retrieves current status of a submitted transaction.

**Response:**
```json
{
  "transactionId": "TXN-2026-00001",
  "status": "IN_PROCESS",
  "confirmationNumber": "CONF-A1B2C3D4",
  "submittedAt": "2026-02-25T10:30:00Z",
  "lastUpdated": "2026-02-26T14:20:00Z"
}
```

## Integration Patterns

### Order Entry System Integration

Order entry systems can consume this payload and:

1. **Extract application data** for new policy creation
2. **Process 1035 exchange** instructions
3. **Generate required forms** (application, exchange forms, etc.)
4. **Submit to carrier** via their API or EDI
5. **Track workflow** through completion
6. **Update status** back to originating system

### Sample Integration Code

```python
from app.models.replacement_transaction import ReplacementTransactionPayload
import requests

# Receive payload from UI or API
payload = ReplacementTransactionPayload(**request_data)

# Validate
validation_response = requests.post(
    "https://api.example.com/replacement-transactions/validate",
    json=payload.model_dump()
)

if validation_response.json()["isValid"]:
    # Submit to order entry system
    order_entry_response = requests.post(
        "https://order-entry-system.carrier.com/api/applications",
        json=payload.model_dump(),
        headers={"Authorization": f"Bearer {carrier_api_key}"}
    )
    
    # Track confirmation
    confirmation = order_entry_response.json()["confirmationNumber"]
    
    # Update transaction status
    update_transaction_status(
        payload.transactionId, 
        "SUBMITTED",
        confirmation
    )
```

### DTCC ACATS Integration

For automated asset transfer:

```python
# Convert to DTCC ACATS format
acats_request = {
    "accountNumber": payload.currentPolicy.policyNumber,
    "receivingFirm": payload.newProduct.carrierCode,
    "deliveryFirm": payload.currentPolicy.carrierCode,
    "assets": [{
        "assetType": "ANNUITY",
        "quantity": 1,
        "value": str(payload.currentPolicy.surrenderValue)
    }],
    "transferType": "FULL_ACATS",
    "clientAuthorization": {
        "signed": True,
        "signedDate": payload.complianceChecklist.replacementFormDate
    }
}

# Submit to DTCC
dtcc_response = submit_acats_request(acats_request)
```

## Validation Rules

### Required Field Validation

- All fields marked with `...` in Pydantic models are required
- Beneficiary allocations must total 100% per type
- Premium calculations must balance (initialPremium = exchangeAmount + additionalPremium)

### Business Logic Validation

- Client age must be within product age limits
- State must be in product's available states
- Advisor must have carrier appointment
- Surrender charges must be justified if > 0

### Compliance Validation

- Replacement form must be signed
- Suitability review must be completed
- 1035 exchange form required for tax-free exchanges
- W-9 must be on file

### Suitability Validation

- Investment horizon must align with surrender period
- Liquidity needs must be compatible with product features
- Risk tolerance must match product risk profile

## Error Handling

### Validation Errors

```json
{
  "isValid": false,
  "errors": [
    "State replacement form not signed",
    "Suitability review not completed",
    "Primary beneficiary allocations total 95%, must equal 100%",
    "Advisor does not have carrier appointment"
  ],
  "warnings": [
    "Surrender charges apply but no justification provided"
  ]
}
```

### Submission Errors

```json
{
  "success": false,
  "message": "Submission failed - validation errors",
  "errors": [
    "Client age 87 exceeds product maximum age 85",
    "Product not available in client state (NY)"
  ]
}
```

## State-Specific Requirements

Different states have varying replacement requirements:

### California
- Signed replacement notice required
- 30-day free look period
- Senior protection for age 60+

### New York
- Suitability determination documented
- Best interest standard
- 45-day free look for replacements

### Florida  
- Annuity suitability database submission
- Enhanced disclosure for age 65+

The `complianceChecklist.stateApprovalRequired` flag indicates when state-level review is needed.

## Best Practices

### 1. Progressive Data Collection

Collect data in logical steps:
1. Policy identification
2. Product selection  
3. Client confirmation
4. Suitability review
5. Compliance verification
6. Final submission

### 2. Data Validation

- Validate at each step, not just final submission
- Provide clear error messages with remediation steps
- Warn for non-blocking issues

### 3. Audit Trail

- Log all payload creations and modifications
- Track who created/modified/submitted
- Store validation results

### 4. Security

- Mask SSN in logs and displays (***-**-1234)
- Encrypt payload at rest and in transit
- Limit access to PII fields

### 5. User Experience

- Pre-populate from existing data where possible
- Show validation errors in context
- Provide tooltips for compliance requirements

## Schema Versioning

Current Version: **1.0.0**

The payload includes `sourceSystemVersion` for schema versioning:

```json
{
  "sourceSystem": "AnnuityReviewAI",
  "sourceSystemVersion": "1.0.0"
}
```

Order entry systems should check version compatibility and handle accordingly.

## Future Enhancements

Potential additions to the standard:

- **Multimedia attachments** - Embedded documents vs. references
- **E-signature integration** - DocuSign/Adobe Sign metadata
- **Real-time carrier validation** - Pre-submission carrier API checks
- **AI suitability scoring** - Automated suitability assessment
- **Blockchain audit trail** - Immutable transaction history

## Support & Questions

For questions about this standard or integration support:

- **Technical Documentation**: See inline comments in models
- **API Documentation**: Available at `/docs` endpoint
- **Integration Examples**: See `test_api.py` for sample usage

---

## About This Standard

### Relationship to Industry Standards

**ACORD (Association for Cooperative Operations Research and Development)**
- ACORD provides XML schemas for insurance data exchange
- Primarily used for batch EDI and legacy system integration
- Our standard is **inspired by ACORD concepts** but not ACORD-compliant
- We use ACORD's field naming conventions where applicable
- **Key Difference**: We use JSON instead of XML for modern API consumption

**DTCC (Depository Trust & Clearing Corporation)**
- DTCC ACATS handles asset transfer between firms
- Our payload can be **transformed to** DTCC ACATS format
- Includes all required fields for ACATS submission
- See integration examples in documentation

**IRS Form 1035**
- Fully compliant with IRS 1035 exchange requirements
- Captures all required tax basis and cost basis data
- Supports both qualified and non-qualified money

### Industry Adoption Roadmap

This standard is designed to become an **industry reference** for annuity replacement workflows:

**Phase 1** (Current): Internal use within Annuity Review AI Platform  
**Phase 2**: Share with carrier partners for order entry integration  
**Phase 3**: Publish as open standard for industry adoption  
**Phase 4**: Consider submission to standards bodies (ACORD, LIMRA)  

### License & Usage

**© 2026 IRI Annuity Review AI Platform**

This standard specification is made available for:
- ✅ Use by order entry systems integrating with our platform
- ✅ Reference by carriers and distributors
- ✅ Adaptation for carrier-specific needs
- ✅ Educational and research purposes

For commercial use or redistribution, please contact our team.

---

**Standard Name**: IRI Annuity Replacement Transaction Standard (IARTS)  
**Version**: 1.0.0  
**Release Date**: February 25, 2026  
**Status**: Production Ready  
**Maintained By**: IRI Annuity Review AI Platform Team  
**Contact**: [Technical Documentation Team](mailto:tech@example.com)  
**GitHub**: [IRIHackathon2026](https://github.com/iTheRakeshP/IRIHackathon2026)
