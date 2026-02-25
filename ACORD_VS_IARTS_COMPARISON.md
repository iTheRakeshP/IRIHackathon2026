# ACORD XML vs IARTS (IRI Annuity Replacement Transaction Standard)

## Side-by-Side Format Comparison

This document compares traditional ACORD XML format with our new **IARTS (IRI Annuity Replacement Transaction Standard)** for the same annuity replacement transaction.

---

## Example: Simple 1035 Exchange Transaction

### ACORD XML Format (Traditional)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<TXLife xmlns="http://ACORD.org/Standards/Life/2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <UserAuthRequest>
    <VendorApp>
      <VendorName VendorCode="12345">
        <VendorName>Order Entry System</VendorName>
      </VendorName>
    </VendorApp>
  </UserAuthRequest>
  <TXLifeRequest>
    <TransRefGUID>TXN-2026-00001</TransRefGUID>
    <TransType tc="228">1035 Exchange</TransType>
    <TransExeDate>2026-02-25</TransExeDate>
    <TransExeTime>10:30:00</TransExeTime>
    
    <OLifE>
      <Holding id="Holding_1">
        <HoldingTypeCode tc="2">Annuity</HoldingTypeCode>
        <Policy>
          <PolNumber>OLD-12345678</PolNumber>
          <LineOfBusiness tc="4">Annuity</LineOfBusiness>
          <ProductCode>FIA</ProductCode>
          <ProductType tc="10">Fixed Index Annuity</ProductType>
          
          <ApplicationInfo>
            <SignedDate>2015-03-15</SignedDate>
          </ApplicationInfo>
          
          <FinancialInfo>
            <AccountValue>250000.00</AccountValue>
            <SurrenderValue>250000.00</SurrenderValue>
            <SurrenderCharge>0.00</SurrenderCharge>
            <CostBasis>200000.00</CostBasis>
          </FinancialInfo>
          
          <Life>
            <Coverage id="Coverage_1">
              <IndicatorCode tc="1">Primary</IndicatorCode>
              <LifeParticipant>
                <LifeParticipantRoleCode tc="1">Insured</LifeParticipantRoleCode>
                <Party id="Party_Annuitant">
                  <PartyTypeCode tc="1">Person</PartyTypeCode>
                  <Person>
                    <FirstName>John</FirstName>
                    <LastName>Smith</LastName>
                    <BirthDate>1960-05-20</BirthDate>
                    <GovtID>***-**-1234</GovtID>
                  </Person>
                </Party>
              </LifeParticipant>
            </Coverage>
          </Life>
          
          <Relation>
            <OriginatingObjectType tc="3">Party</OriginatingObjectType>
            <OriginatingObjectID>Party_Owner</OriginatingObjectID>
            <RelatedObjectType tc="6">Holding</RelatedObjectType>
            <RelatedObjectID>Holding_1</RelatedObjectID>
            <RelationRoleCode tc="8">Owner</RelationRoleCode>
          </Relation>
        </Policy>
      </Holding>
      
      <Holding id="Holding_2">
        <HoldingTypeCode tc="2">Annuity</HoldingTypeCode>
        <Policy>
          <PolNumber>NEW-87654321</PolNumber>
          <LineOfBusiness tc="4">Annuity</LineOfBusiness>
          <ProductCode>FIA</ProductCode>
          <CarrierCode>67890</CarrierCode>
          
          <ApplicationInfo>
            <ApplicationType tc="1">New Business</ApplicationType>
            <ApplicationJurisdiction tc="CA">California</ApplicationJurisdiction>
            <SignedDate>2026-02-24</SignedDate>
          </ApplicationInfo>
          
          <FinancialInfo>
            <InitialPremium>250000.00</InitialPremium>
            <ExchangeAmount>250000.00</ExchangeAmount>
          </FinancialInfo>
        </Policy>
      </Holding>
      
      <Party id="Party_Owner">
        <PartyTypeCode tc="1">Person</PartyTypeCode>
        <Person>
          <FirstName>John</FirstName>
          <MiddleName>A</MiddleName>
          <LastName>Smith</LastName>
          <BirthDate>1960-05-20</BirthDate>
          <Age>65</Age>
          <GovtID>123-45-6789</GovtID>
          <GovtIDTC tc="1">SSN</GovtIDTC>
          <Gender tc="1">Male</Gender>
          <Address>
            <AddressTypeCode tc="1">Residence</AddressTypeCode>
            <Line1>123 Main Street</Line1>
            <City>Anytown</City>
            <AddressStateTC tc="CA">California</AddressStateTC>
            <Zip>90210</Zip>
          </Address>
          <Phone>
            <AreaCode>555</AreaCode>
            <DialNumber>1234567</DialNumber>
          </Phone>
          <EMailAddress>john.smith@email.com</EMailAddress>
        </Person>
      </Party>
      
      <Party id="Party_Agent">
        <PartyTypeCode tc="1">Person</PartyTypeCode>
        <Producer>
          <CarrierAppointment>
            <CarrierCode>67890</CarrierCode>
            <CompanyProducerID>ADV-12345</CompanyProducerID>
          </CarrierAppointment>
        </Producer>
        <Person>
          <FirstName>Jane</FirstName>
          <LastName>Advisor</LastName>
        </Person>
      </Party>
      
      <FormInstance>
        <FormName>State Replacement Form</FormName>
        <CompletedDate>2026-02-24</CompletedDate>
        <SignatureInfo>
          <SignatureDate>2026-02-24</SignatureDate>
          <SignatureCity>Anytown</SignatureCity>
          <SignatureState tc="CA">California</SignatureState>
        </SignatureInfo>
      </FormInstance>
    </OLifE>
  </TXLifeRequest>
</TXLife>
```

**Line Count**: ~130 lines  
**File Size**: ~4.8 KB  
**Readability**: Low (XML verbosity)  
**Parsing Complexity**: High (nested XML, namespaces, type codes)

---

### IARTS JSON Format (Our Standard) ✨

```json
{
  "transactionId": "TXN-2026-00001",
  "transactionType": "EXTERNAL_1035_EXCHANGE",
  "exchangeType": "FULL_1035",
  "premiumSource": "EXCHANGE_PROCEEDS",
  "status": "INITIATED",
  "createdDate": "2026-02-25",
  "createdTimestamp": "2026-02-25T10:30:00Z",
  "sourceSystem": "AnnuityReviewAI",
  
  "currentPolicy": {
    "policyNumber": "OLD-12345678",
    "carrier": "Legacy Insurance Co",
    "productName": "Legacy FIA 2015",
    "productType": "FIA",
    "accountValue": "250000.00",
    "surrenderValue": "250000.00",
    "surrenderCharge": "0.00",
    "issueDate": "2015-03-15",
    "ownerName": "John Smith",
    "ownerSSN": "***-**-1234",
    "qualifiedStatus": "NON_QUALIFIED",
    "costBasis": "200000.00",
    "replacementReason": [
      "Renewal rate drops to 4.5% from 6.0%",
      "Better income rider available"
    ]
  },
  
  "newProduct": {
    "productId": "PROD-2024-FIA-001",
    "carrier": "Modern Annuity Co",
    "carrierCode": "67890",
    "productName": "Income Plus FIA 2024",
    "productType": "FIA",
    "initialPremium": "250000.00",
    "exchangeAmount": "250000.00"
  },
  
  "client": {
    "firstName": "John",
    "middleName": "A",
    "lastName": "Smith",
    "ssn": "123-45-6789",
    "dateOfBirth": "1960-05-20",
    "age": 65,
    "gender": "M",
    "address": "123 Main Street",
    "city": "Anytown",
    "state": "CA",
    "zipCode": "90210",
    "phone": "555-123-4567",
    "email": "john.smith@email.com"
  },
  
  "complianceChecklist": {
    "replacementFormSigned": true,
    "replacementFormDate": "2026-02-24",
    "suitabilityReviewCompleted": true,
    "isSuitable": true,
    "is1035Exchange": true,
    "exchangeFormCompleted": true
  },
  
  "advisor": {
    "advisorId": "ADV-12345",
    "firstName": "Jane",
    "lastName": "Advisor",
    "email": "jadvisor@firm.com",
    "hasCarrierAppointment": true
  }
}
```

**Line Count**: ~65 lines  
**File Size**: ~1.2 KB  
**Readability**: High (clean JSON)  
**Parsing Complexity**: Low (any language can parse JSON natively)

---

## Key Differences

### 1. **Verbosity**

| Aspect | ACORD XML | IARTS JSON |
|--------|-----------|------------|
| Lines of code | 130+ | 65 |
| File size | 4.8 KB | 1.2 KB |
| Readability | Low | High |
| **Reduction** | Baseline | **50% smaller** |

### 2. **Structure**

**ACORD XML:**
- Deeply nested hierarchies
- Requires XML namespace declarations
- Type codes (tc attributes) reference external lookup tables
- Relation objects link entities indirectly
- Complex Party/Holding/Coverage model

**IARTS JSON:**
- Flat, logical groupings
- No namespace overhead
- Human-readable values (no type codes)
- Direct relationships (embedded objects)
- Simple entity model

### 3. **Developer Experience**

**ACORD XML:**
```java
// Parsing ACORD XML in Java
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
factory.setNamespaceAware(true);
DocumentBuilder builder = factory.newDocumentBuilder();
Document doc = builder.parse(xmlFile);
XPath xpath = XPathFactory.newInstance().newXPath();
xpath.setNamespaceContext(new ACORDNamespaceContext());
String policyNumber = xpath.evaluate("//Policy/PolNumber/text()", doc);
```

**IARTS JSON:**
```javascript
// Parsing IARTS JSON in JavaScript
const transaction = JSON.parse(jsonString);
const policyNumber = transaction.currentPolicy.policyNumber;
```

### 4. **Validation**

**ACORD XML:**
- Requires XSD schema files
- Must validate against complex schema
- Error messages reference line numbers and schema paths
- Schema updates require coordination

**IARTS JSON:**
- Pydantic models provide automatic validation
- Runtime type checking
- Clear, field-specific error messages
- Schema evolution is easier

### 5. **Compliance & Suitability**

**ACORD XML:**
- Limited compliance fields
- No suitability assessment structure
- External systems must handle compliance tracking
- Form completion tracked separately

**IARTS JSON:**
- Built-in `complianceChecklist` object
- Embedded `suitabilityProfile`
- Replacement reasons documented inline
- Complete audit trail in single payload

### 6. **API Integration**

**ACORD XML:**
```
POST /soap/endpoint
Content-Type: text/xml

<soap:Envelope>
  <soap:Body>
    <TXLife>...</TXLife>
  </soap:Body>
</soap:Envelope>
```

**IARTS JSON:**
```
POST /api/replacement-transactions/submit
Content-Type: application/json

{ "transactionId": "TXN-001", ... }
```

---

## When to Use Each Standard

### Use ACORD XML When:
- ✅ Integrating with legacy insurance systems
- ✅ Carrier requires ACORD format
- ✅ Batch EDI file transfers
- ✅ Regulatory requirement for ACORD compliance

### Use IARTS JSON When:
- ✅ Building modern API integrations
- ✅ Real-time transaction processing
- ✅ Web/mobile application backends
- ✅ AI/ML integration (recommendations, scoring)
- ✅ Developer-friendly integrations
- ✅ Rapid prototyping and iteration

---

## Converting Between Formats

We provide converters to transform IARTS → ACORD XML when needed:

```python
from app.converters import iarts_to_acord

# Convert our format to ACORD for legacy system submission
acord_xml = iarts_to_acord(iarts_payload)
submit_to_legacy_system(acord_xml)
```

This gives you:
- **Modern development** with IARTS
- **Legacy compatibility** when needed
- **Best of both worlds**

---

## What ACORD Cannot Do (But IARTS Can)

ACORD XML was designed for basic transaction processing, but modern annuity replacements require compliance, suitability assessment, and regulatory documentation that **ACORD simply does not support**. Here's what's missing:

### ❌ ACORD Gaps vs ✅ IARTS Support

| Feature | ACORD XML | Our JSON | Why It Matters |
|---------|-----------|------------|----------------|
| **Structured Suitability Profile** | ❌ None | ✅ Full Support | Reg BI & Best Interest requirements |
| **Replacement Narrative/Justification** | ❌ None | ✅ Required Field | State insurance dept. compliance |
| **Compliance Checklist** | ❌ None | ✅ Built-in | Pre-submission validation |
| **Index/Rider Details** | ⚠️ Generic | ✅ Structured | Accurate product configuration |
| **Client Financial Profile** | ⚠️ Basic | ✅ Comprehensive | Know Your Customer (KYC) |
| **Document Management** | ❌ None | ✅ Full Support | Form tracking & e-delivery |
| **Workflow Status Tracking** | ❌ None | ✅ Real-time | Order entry system integration |
| **AI Integration Fields** | ❌ None | ✅ Native | AI-powered review & recommendations |
| **Real-Time Validation** | ⚠️ Limited | ✅ Comprehensive | Pydantic schema validation |
| **State-Specific Compliance** | ❌ None | ✅ Per-state rules | Free-look periods, notifications |

---

### 1. ❌ ACORD: No Suitability Profile Structure

**ACORD** has no standardized way to pass client suitability information. You might find scattered fields but nothing structured.

**IARTS Solution:**
```json
{
  "suitability_profile": {
    "risk_tolerance": "MODERATE",
    "investment_objectives": ["INCOME_GENERATION", "TAX_DEFERRAL"],
    "time_horizon_years": 15,
    "liquidity_needs": "LOW",
    "replacement_suitability_score": 92,
    "advisor_suitability_determination": "SUITABLE",
    "suitability_notes": "Client has sufficient liquid assets, low liquidity needs, and seeks guaranteed income. Replacement improves death benefit and income guarantees.",
    "best_interest_confirmation": true,
    "reg_bi_compliance_confirmed": true
  }
}
```

**Impact:** ACORD cannot demonstrate Reg BI compliance or suitability assessment—critical for regulatory reviews.

---

### 2. ❌ ACORD: No Replacement Narrative/Justification

**ACORD** has no field for explaining *why* the replacement is occurring and whether it benefits the client.

**IARTS Solution:**
```json
{
  "current_policy": {
    "replacement_reason": "BETTER_BENEFITS",
    "replacement_narrative": "Replacing 15-year-old fixed annuity with modern indexed annuity providing better death benefit protection and guaranteed income rider. Current policy has no living benefits. New policy offers 6% income rollup and enhanced death benefit.",
    "surrender_charge_amount": 2500.00,
    "surrender_charge_justification": "Surrender charge offset by increased death benefit value and guaranteed income stream over next 10 years."
  }
}
```

**Impact:** State insurance departments require replacement justification—ACORD provides no standard way to document this.

---

### 3. ❌ ACORD: No Compliance Checklist

**ACORD** assumes you've done compliance manually but provides no way to document it in the payload.

**IARTS Solution:**
```json
{
  "compliance_checklist": {
    "replacement_form_completed": true,
    "replacement_form_signed_date": "2026-02-20",
    "comparative_info_provided": true,
    "best_interest_documented": true,
    "state_approval_required": false,
    "free_look_period_days": 30,
    "compliance_notes": "Client reviewed comparison document showing current vs new policy benefits. Signed replacement acknowledgment form."
  }
}
```

**Impact:** Without documented compliance, order entry systems cannot verify regulatory requirements were met.

---

### 4. ❌ ACORD: No Index/Rider Selection Details

**ACORD** might have a generic "rider" field but no structured way to configure index strategies or living benefit riders.

**IARTS Solution:**
```json
{
  "new_product": {
    "selected_index_options": [
      {
        "index_name": "S&P 500 Annual Point-to-Point",
        "allocation_percentage": 60.0,
        "cap_rate": 5.5,
        "participation_rate": 100.0
      },
      {
        "index_name": "Fixed Account",
        "allocation_percentage": 40.0,
        "guaranteed_rate": 3.0
      }
    ],
    "selected_riders": [
      {
        "rider_code": "GLWB",
        "rider_name": "Guaranteed Lifetime Withdrawal Benefit",
        "rider_premium": 0.95,
        "rider_details": {
          "rollup_rate": 6.0,
          "payout_percentage": 5.0
        }
      }
    ]
  }
}
```

**Impact:** Order entry systems need precise product configuration—ACORD's generic structure leads to manual re-entry.

---

### 5. ❌ ACORD: No Client Financial Profile

**ACORD** has basic demographic fields but no comprehensive financial situation assessment.

**IARTS Solution:**
```json
{
  "client_info": {
    "annual_income": 95000.00,
    "net_worth": 850000.00,
    "liquid_assets": 250000.00,
    "tax_bracket": "24%",
    "employment_status": "EMPLOYED",
    "financial_profile_complete": true
  }
}
```

**Impact:** Suitability assessments require understanding client's full financial picture—ACORD doesn't capture this.

---

### 6. ❌ ACORD: No Document Management

**ACORD** has no way to track what forms were signed, when they were delivered, or how they should be stored.

**IARTS Solution:**
```json
{
  "required_documents": [
    {
      "document_type": "REPLACEMENT_FORM",
      "document_name": "State Replacement Notice",
      "required": true,
      "completed": true,
      "signed_date": "2026-02-20",
      "delivery_method": "EMAIL"
    },
    {
      "document_type": "BEST_INTEREST_FORM",
      "document_name": "Reg BI Best Interest Disclosure",
      "required": true,
      "completed": true,
      "signed_date": "2026-02-20"
    }
  ]
}
```

**Impact:** Compliance depends on document tracking—ACORD provides no structure for this.

---

### 7. ❌ ACORD: No Workflow Status Management

**ACORD** is a one-time submission format with no built-in status tracking.

**IARTS Solution:**
```json
{
  "transaction_id": "TXN-2026-00001",
  "status": "PENDING_CARRIER_APPROVAL",
  "workflow_history": [
    {
      "status": "DRAFT",
      "timestamp": "2026-02-20T14:30:00Z",
      "user": "advisor@example.com"
    },
    {
      "status": "SUBMITTED",
      "timestamp": "2026-02-21T09:15:00Z",
      "user": "advisor@example.com"
    }
  ]
}
```

**Impact:** Real-time order entry integration requires status tracking—ACORD is fire-and-forget.

---

### 8. ❌ ACORD: No AI Integration Fields

**ACORD** was designed in the early 2000s—long before AI-powered analysis.

**IARTS Solution:**
```json
{
  "ai_analysis": {
    "recommendation_score": 92,
    "risk_assessment": "LOW",
    "compliance_flags": [],
    "improvement_suggestions": [
      "Consider allocating 10% to Fixed Account for guaranteed growth floor"
    ]
  }
}
```

**Impact:** Modern platforms use AI for real-time recommendations—ACORD has no mechanism for this.

---

### 9. ❌ ACORD: No Real-Time Validation Support

**ACORD** relies on XSD schema validation, but doesn't enforce business rules (e.g., "surrender charge must be justified").

**IARTS Solution:**
- Pydantic models with field-level validation
- Business rule enforcement (e.g., `replacement_narrative` required when `replacement_reason` is present)
- API-level validation with detailed error messages

**Impact:** ACORD submissions often fail downstream validation—IARTS validates before submission.

---

### 10. ❌ ACORD: No State-Specific Compliance

**ACORD** is generic and doesn't account for state-specific regulations (free-look periods, notification requirements, etc.).

**IARTS Solution:**
```json
{
  "compliance_checklist": {
    "state_approval_required": false,
    "state_specific_requirements": {
      "CA": {
        "free_look_period_days": 30,
        "requires_insurance_dept_notification": true
      }
    }
  }
}
```

**Impact:** Compliance varies by state—ACORD provides no structure for jurisdiction-specific rules.

---

## Summary: Why ACORD Falls Short for Modern Annuity Replacements

**ACORD XML was built for basic transaction processing in an era before:**
- Reg BI (Regulation Best Interest)
- AI-powered suitability analysis
- Real-time API integration
- Comprehensive compliance documentation
- Modern KYC/AML requirements

**For advisors:** ACORD cannot demonstrate suitability or best interest determination  
**For compliance teams:** ACORD lacks structured checklists and replacement justification  
**For order entry systems:** ACORD requires manual data re-entry for riders/index options  
**For auditors:** ACORD provides no document tracking or workflow history  

**IARTS fills these gaps** by providing a comprehensive, modern standard designed specifically for today's regulatory environment and technological capabilities.

---

## Conclusion

**IARTS** is designed for the modern insurance technology stack:
- Simpler, cleaner, more maintainable
- 50% less code for the same transaction
- Native JSON (universally supported)
- Built-in compliance & validation
- AI-ready architecture

While ACORD XML remains the established standard for batch processing, **IARTS represents the future of real-time annuity transaction processing**.

---

**IARTS**: IRI Annuity Replacement Transaction Standard  
**Version**: 1.0.0  
**License**: Proprietary (available for partner integration)  
**Maintained By**: IRI Annuity Review AI Platform Team
