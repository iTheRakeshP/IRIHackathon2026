"""
Sample usage examples for the Replacement Transaction Standard Payload

This file demonstrates how to create, validate, and submit replacement
transactions using the standard payload format.
"""

from datetime import datetime
import json
from decimal import Decimal

from app.models.replacement_transaction import (
    ReplacementTransactionPayload,
    TransactionType,
    ExchangeType,
    PremiumSource,
    TransactionStatus,
    CurrentPolicyInfo,
    NewProductSelection,
    ClientInfo,
    AnnuitantInfo,
    BeneficiaryDesignation,
    SuitabilityProfile,
    ComplianceChecklist,
    AdvisorInfo,
    TaxWithholdingElections
)


def create_sample_external_1035_exchange():
    """
    Example 1: External 1035 Exchange (Different Carrier)
    
    Scenario:
    - Client has an existing FIA with high fees and low renewal rate
    - Replacing with a better performing product from different carrier
    - No surrender charges (out of surrender period)
    - Full 1035 tax-free exchange
    """
    
    transaction = ReplacementTransactionPayload(
        # Transaction metadata
        transactionId="TXN-20260225-EXT001",
        transactionType=TransactionType.EXTERNAL_1035_EXCHANGE,
        exchangeType=ExchangeType.FULL_1035,
        premiumSource=PremiumSource.EXCHANGE_PROCEEDS,
        status=TransactionStatus.INITIATED,
        createdDate="2026-02-25",
        createdTimestamp=datetime.utcnow().isoformat() + "Z",
        sourceSystem="AnnuityReviewAI",
        sourceSystemVersion="1.0.0",
        
        # Current policy being replaced
        currentPolicy=CurrentPolicyInfo(
            policyNumber="OLD-12345678",
            carrier="Legacy Insurance Co",
            carrierCode="12345",
            productName="Legacy FIA 2015",
            productType="FIA",
            accountValue=Decimal("250000.00"),
            surrenderValue=Decimal("250000.00"),  # No surrender charge
            surrenderCharge=Decimal("0.00"),
            surrenderChargePercent=0.0,
            issueDate="2015-03-15",
            ownerName="John Smith",
            ownerSSN="***-**-1234",
            annuitantName="John Smith",
            annuitantDOB="1960-05-20",
            qualifiedStatus="NON_QUALIFIED",
            costBasis=Decimal("200000.00"),
            gainLoss=Decimal("50000.00"),
            hasIncomeRider=True,
            incomeRiderName="Legacy Income Rider",
            incomeBase=Decimal("280000.00"),
            isIncomeActivated=False,
            replacementReason=[
                "Renewal rate drops to 4.5% from 6.0%",
                "Higher fees (2.5% total vs 1.8% on new product)",
                "Better income rider with higher payout rate available"
            ]
        ),
        
        # New product selection
        newProduct=NewProductSelection(
            productId="PROD-2024-FIA-001",
            carrier="Modern Annuity Co",
            carrierCode="67890",
            productName="Income Plus FIA 2024",
            productType="FIA",
            initialPremium=Decimal("250000.00"),
            exchangeAmount=Decimal("250000.00"),
            additionalPremium=Decimal("0.00"),
            selectedIndexOptions=[
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
            selectedRiders=[
                {
                    "riderName": "Lifetime Income Protector Plus",
                    "riderType": "Income",
                    "annualFee": 1.25,
                    "rollUpRate": 7.0,
                    "payoutRate": 5.5,
                    "features": [
                        "7% annual roll-up for 10 years",
                        "5.5% lifetime payout rate at age 65",
                        "Doubles for nursing home care"
                    ]
                }
            ],
            bonusRate=10.0,
            bonusAmount=Decimal("25000.00")
        ),
        
        # Client information
        client=ClientInfo(
            firstName="John",
            middleName="A",
            lastName="Smith",
            ssn="123-45-6789",
            dateOfBirth="1960-05-20",
            age=65,
            gender="M",
            citizenship="USA",
            address="123 Main Street",
            city="Anytown",
            state="CA",
            zipCode="90210",
            phone="555-123-4567",
            email="john.smith@email.com",
            annualIncome="$100,000 - $150,000",
            netWorth="$1M - $2M",
            liquidNetWorth="$500K - $1M",
            taxBracket="24%",
            employmentStatus="Retired",
            occupation="Former Engineer",
            employer="N/A"
        ),
        
        # Annuitant (same as owner)
        annuitant=AnnuitantInfo(
            isSameAsOwner=True
        ),
        
        # Beneficiaries
        beneficiaries=[
            BeneficiaryDesignation(
                beneficiaryType="PRIMARY",
                firstName="Jane",
                lastName="Smith",
                relationship="Spouse",
                ssn="987-65-4321",
                dateOfBirth="1962-08-15",
                allocationPercent=100.0,
                address="123 Main Street",
                city="Anytown",
                state="CA",
                zipCode="90210",
                phone="555-123-4567",
                email="jane.smith@email.com"
            ),
            BeneficiaryDesignation(
                beneficiaryType="CONTINGENT",
                firstName="Michael",
                lastName="Smith",
                relationship="Son",
                dateOfBirth="1990-03-10",
                allocationPercent=50.0
            ),
            BeneficiaryDesignation(
                beneficiaryType="CONTINGENT",
                firstName="Sarah",
                lastName="Johnson",
                relationship="Daughter",
                dateOfBirth="1992-07-22",
                allocationPercent=50.0
            )
        ],
        
        # Suitability profile
        suitabilityProfile=SuitabilityProfile(
            riskTolerance="Moderate",
            investmentObjective="Income",
            investmentExperience="Extensive",
            investmentHorizon="Long (7+ years)",
            liquidityNeeds="Low",
            timeHorizon="10+ years",
            surrenderChargeAcceptance=True,
            currentIncomeNeeded=False,
            futureIncomeNeeded=True,
            incomeStartYear=2028,
            totalAnnuityHoldings=Decimal("500000.00"),
            percentageInAnnuities=25.0,
            understandsReplacement=True,
            comparedAlternatives=True,
            reviewedSurrenderCharges=True
        ),
        
        # Compliance checklist
        complianceChecklist=ComplianceChecklist(
            replacementFormSigned=True,
            replacementFormDate="2026-02-24",
            suitabilityReviewCompleted=True,
            suitabilityDeterminationDate="2026-02-24",
            isSuitable=True,
            suitabilityNotes="Transaction meets client objectives for guaranteed lifetime income with lower fees",
            bestInterestDetermination=True,
            alternativesConsidered=3,
            is1035Exchange=True,
            exchangeFormCompleted=True,
            stateApprovalRequired=False,
            freeLookPeriodDisclosed=True,
            freeLookDays=30,
            seniorProtectionApplies=True
        ),
        
        # Advisor information
        advisor=AdvisorInfo(
            advisorId="ADV-12345",
            firstName="Jane",
            lastName="Advisor",
            email="jadvisor@firm.com",
            phone="555-987-6543",
            licenseNumber="CA-INS-123456",
            licenseState="CA",
            hasCarrierAppointment=True,
            appointmentNumber="APPT-67890",
            hasProductTraining=True,
            completedCE=True,
            firmName="Premier Financial Advisors",
            firmAddress="456 Business Blvd, Suite 200, Anytown, CA 90211",
            bdName="National Broker-Dealer LLC",
            bdCRD="12345"
        ),
        
        # Tax withholding
        taxWithholding=TaxWithholdingElections(
            federalWithholding=False,
            stateWithholding=False,
            w9OnFile=True,
            w9Date="2026-02-20"
        ),
        
        # Qualified status
        qualifiedStatus="NON_QUALIFIED",
        
        # Supporting documents
        documents=[
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
        ],
        
        # Notes
        specialInstructions="Please expedite processing - client retirement date is approaching",
        
        # External system references
        externalSystemRefs={
            "policyId": "POL-001",
            "productId": "PROD-2024-FIA-001",
            "clientAccountNumber": "123-456-789",
            "alertId": "ALT-001"
        }
    )
    
    return transaction


def create_sample_internal_exchange():
    """
    Example 2: Internal Exchange (Same Carrier)
    
    Scenario:
    - Client has older product with same carrier
    - Moving to newer product with better features
    - Carrier allows internal exchange without surrender charges
    - Preserving cost basis
    """
    
    transaction = ReplacementTransactionPayload(
        transactionId="TXN-20260225-INT001",
        transactionType=TransactionType.INTERNAL_EXCHANGE,
        exchangeType=ExchangeType.FULL_1035,
        premiumSource=PremiumSource.EXCHANGE_PROCEEDS,
        status=TransactionStatus.INITIATED,
        createdDate="2026-02-25",
        createdTimestamp=datetime.utcnow().isoformat() + "Z",
        sourceSystem="AnnuityReviewAI",
        
        currentPolicy=CurrentPolicyInfo(
            policyNumber="INT-OLD-99999",
            carrier="Modern Annuity Co",
            carrierCode="67890",
            productName="Modern FIA 2018",
            productType="FIA",
            accountValue=Decimal("150000.00"),
            surrenderValue=Decimal("150000.00"),
            surrenderCharge=Decimal("0.00"),  # Waived for internal exchange
            issueDate="2018-06-01",
            ownerName="Mary Johnson",
            ownerSSN="***-**-5678",
            annuitantName="Mary Johnson",
            annuitantDOB="1958-09-12",
            qualifiedStatus="NON_QUALIFIED",
            costBasis=Decimal("120000.00"),
            gainLoss=Decimal("30000.00"),
            hasIncomeRider=False,
            isIncomeActivated=False,
            replacementReason=[
                "Internal exchange to newer product with better features",
                "No surrender charges for internal moves",
                "Access to new index options"
            ]
        ),
        
        newProduct=NewProductSelection(
            productId="PROD-2024-FIA-002",
            carrier="Modern Annuity Co",
            carrierCode="67890",
            productName="Modern FIA Elite 2024",
            productType="FIA",
            initialPremium=Decimal("150000.00"),
            exchangeAmount=Decimal("150000.00"),
            additionalPremium=Decimal("0.00"),
            selectedIndexOptions=[
                {
                    "indexName": "S&P 500",
                    "strategy": "Monthly Sum Cap",
                    "allocationPercent": 100,
                    "currentCap": 1.75
                }
            ],
            selectedRiders=[]
        ),
        
        client=ClientInfo(
            firstName="Mary",
            lastName="Johnson",
            ssn="234-56-7890",
            dateOfBirth="1958-09-12",
            age=67,
            gender="F",
            citizenship="USA",
            address="789 Oak Avenue",
            city="Springfield",
            state="TX",
            zipCode="75001",
            phone="555-234-5678",
            email="mary.j@email.com",
            annualIncome="$75,000 - $100,000",
            netWorth="$750K - $1M",
            liquidNetWorth="$250K - $500K",
            taxBracket="22%",
            employmentStatus="Retired"
        ),
        
        annuitant=AnnuitantInfo(isSameAsOwner=True),
        
        beneficiaries=[
            BeneficiaryDesignation(
                beneficiaryType="PRIMARY",
                firstName="David",
                lastName="Johnson",
                relationship="Son",
                dateOfBirth="1985-04-15",
                allocationPercent=100.0
            )
        ],
        
        suitabilityProfile=SuitabilityProfile(
            riskTolerance="Moderate",
            investmentObjective="Growth",
            investmentExperience="Moderate",
            investmentHorizon="Long (7+ years)",
            liquidityNeeds="Medium",
            timeHorizon="7+ years",
            surrenderChargeAcceptance=True,
            currentIncomeNeeded=False,
            futureIncomeNeeded=True,
            understandsReplacement=True,
            comparedAlternatives=True,
            reviewedSurrenderCharges=True
        ),
        
        complianceChecklist=ComplianceChecklist(
            replacementFormSigned=True,
            replacementFormDate="2026-02-24",
            suitabilityReviewCompleted=True,
            suitabilityDeterminationDate="2026-02-24",
            isSuitable=True,
            bestInterestDetermination=True,
            alternativesConsidered=2,
            is1035Exchange=True,
            exchangeFormCompleted=True,
            stateApprovalRequired=False,
            freeLookPeriodDisclosed=True,
            freeLookDays=30
        ),
        
        advisor=AdvisorInfo(
            advisorId="ADV-67890",
            firstName="Robert",
            lastName="Planner",
            email="rplanner@advisory.com",
            phone="555-345-6789",
            licenseNumber="TX-INS-789012",
            licenseState="TX",
            hasCarrierAppointment=True,
            hasProductTraining=True,
            completedCE=True,
            firmName="Retirement Planning Group"
        ),
        
        taxWithholding=TaxWithholdingElections(
            federalWithholding=False,
            stateWithholding=False,
            w9OnFile=True,
            w9Date="2026-01-15"
        ),
        
        qualifiedStatus="NON_QUALIFIED",
        
        documents=[
            {
                "type": "InternalExchangeForm",
                "filename": "Internal_Exchange_Auth.pdf",
                "reference": "DOC-2026-100"
            }
        ]
    )
    
    return transaction


def create_sample_qualified_ira_exchange():
    """
    Example 3: Qualified IRA 1035 Exchange
    
    Scenario:
    - Traditional IRA annuity
    - Moving to better performing IRA annuity
    - Custodian-to-custodian transfer
    """
    
    transaction = ReplacementTransactionPayload(
        transactionId="TXN-20260225-IRA001",
        transactionType=TransactionType.EXTERNAL_1035_EXCHANGE,
        exchangeType=ExchangeType.FULL_1035,
        premiumSource=PremiumSource.EXCHANGE_PROCEEDS,
        status=TransactionStatus.INITIATED,
        createdDate="2026-02-25",
        createdTimestamp=datetime.utcnow().isoformat() + "Z",
        sourceSystem="AnnuityReviewAI",
        
        currentPolicy=CurrentPolicyInfo(
            policyNumber="IRA-OLD-555",
            carrier="Traditional Insurance Co",
            productName="IRA Fixed Annuity",
            productType="Fixed",
            accountValue=Decimal("300000.00"),
            surrenderValue=Decimal("297000.00"),
            surrenderCharge=Decimal("3000.00"),
            surrenderChargePercent=1.0,
            issueDate="2019-01-10",
            ownerName="Robert Williams",
            ownerSSN="***-**-9012",
            annuitantName="Robert Williams",
            annuitantDOB="1955-11-30",
            qualifiedStatus="QUALIFIED",
            qualificationType="Traditional IRA",
            hasIncomeRider=False,
            isIncomeActivated=False,
            replacementReason=[
                "Current rate 3.0% vs 5.5% available on new product",
                "Savings outweigh 1% surrender charge within 1 year"
            ],
            surrenderChargeJustification="Rate differential of 2.5% annually exceeds the 1% surrender charge immediately"
        ),
        
        newProduct=NewProductSelection(
            productId="PROD-2024-FIXED-001",
            carrier="High Yield Annuity Co",
            productName="Traditional IRA Fixed 5-Year",
            productType="Fixed",
            initialPremium=Decimal("297000.00"),
            exchangeAmount=Decimal("297000.00"),
            additionalPremium=Decimal("0.00"),
            selectedIndexOptions=[
                {
                    "indexName": "Fixed Account",
                    "strategy": "Fixed",
                    "allocationPercent": 100,
                    "currentRate": 5.5
                }
            ],
            selectedRiders=[]
        ),
        
        client=ClientInfo(
            firstName="Robert",
            lastName="Williams",
            ssn="345-67-8901",
            dateOfBirth="1955-11-30",
            age=70,
            gender="M",
            citizenship="USA",
            address="321 Elm Street",
            city="Portland",
            state="OR",
            zipCode="97201",
            phone="555-456-7890",
            email="robert.w@email.com",
            annualIncome="$50,000 - $75,000",
            netWorth="$500K - $750K",
            liquidNetWorth="$100K - $250K",
            taxBracket="12%",
            employmentStatus="Retired"
        ),
        
        annuitant=AnnuitantInfo(isSameAsOwner=True),
        
        beneficiaries=[
            BeneficiaryDesignation(
                beneficiaryType="PRIMARY",
                firstName="Susan",
                lastName="Williams",
                relationship="Spouse",
                dateOfBirth="1957-03-25",
                allocationPercent=100.0
            )
        ],
        
        suitabilityProfile=SuitabilityProfile(
            riskTolerance="Conservative",
            investmentObjective="Preservation",
            investmentExperience="Limited",
            investmentHorizon="Medium (3-7y)",
            liquidityNeeds="Low",
            timeHorizon="5+ years",
            surrenderChargeAcceptance=True,
            currentIncomeNeeded=True,
            futureIncomeNeeded=True,
            understandsReplacement=True,
            comparedAlternatives=True,
            reviewedSurrenderCharges=True
        ),
        
        complianceChecklist=ComplianceChecklist(
            replacementFormSigned=True,
            replacementFormDate="2026-02-24",
            suitabilityReviewCompleted=True,
            suitabilityDeterminationDate="2026-02-24",
            isSuitable=True,
            bestInterestDetermination=True,
            alternativesConsidered=3,
            is1035Exchange=True,
            exchangeFormCompleted=True,
            stateApprovalRequired=False,
            freeLookPeriodDisclosed=True,
            freeLookDays=30,
            seniorProtectionApplies=True
        ),
        
        advisor=AdvisorInfo(
            advisorId="ADV-11111",
            firstName="Emily",
            lastName="Financial",
            email="emily@retirement.com",
            phone="555-567-8901",
            licenseNumber="OR-INS-345678",
            licenseState="OR",
            hasCarrierAppointment=True,
            hasProductTraining=True,
            completedCE=True,
            firmName="Retirement Solutions LLC"
        ),
        
        taxWithholding=TaxWithholdingElections(
            federalWithholding=False,
            stateWithholding=False,
            w9OnFile=True,
            w9Date="2026-02-01"
        ),
        
        qualifiedStatus="QUALIFIED",
        qualificationType="Traditional IRA",
        custodianName="National Trust Company",
        custodianAccountNumber="IRA-987654321",
        
        documents=[
            {
                "type": "1035ExchangeForm",
                "filename": "IRA_1035_Exchange.pdf",
                "reference": "DOC-2026-200"
            },
            {
                "type": "IRATransferForm",
                "filename": "Custodian_Transfer_Auth.pdf",
                "reference": "DOC-2026-201"
            }
        ]
    )
    
    return transaction


if __name__ == "__main__":
    # Example 1: External 1035 Exchange
    print("=" * 80)
    print("EXAMPLE 1: External 1035 Exchange (Non-Qualified)")
    print("=" * 80)
    
    txn1 = create_sample_external_1035_exchange()
    print("\nTransaction ID:", txn1.transactionId)
    print("Type:", txn1.transactionType)
    print("Current Policy:", txn1.currentPolicy.policyNumber, "-", txn1.currentPolicy.carrier)
    print("New Product:", txn1.newProduct.productName, "-", txn1.newProduct.carrier)
    print("Amount:", f"${txn1.newProduct.initialPremium:,.2f}")
    print("\nJSON Preview (first 500 chars):")
    json_str = txn1.model_dump_json(indent=2)
    print(json_str[:500] + "...\n")
    
    # Example 2: Internal Exchange
    print("=" * 80)
    print("EXAMPLE 2: Internal Exchange (Same Carrier)")
    print("=" * 80)
    
    txn2 = create_sample_internal_exchange()
    print("\nTransaction ID:", txn2.transactionId)
    print("Type:", txn2.transactionType)
    print("Carrier:", txn2.currentPolicy.carrier, "→", txn2.newProduct.carrier)
    print("Amount:", f"${txn2.newProduct.initialPremium:,.2f}")
    
    # Example 3: Qualified IRA
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Qualified IRA 1035 Exchange")
    print("=" * 80)
    
    txn3 = create_sample_qualified_ira_exchange()
    print("\nTransaction ID:", txn3.transactionId)
    print("Type:", txn3.transactionType)
    print("Qualified:", txn3.qualifiedStatus, "-", txn3.qualificationType)
    print("Custodian:", txn3.custodianName)
    print("Amount:", f"${txn3.newProduct.initialPremium:,.2f}")
    
    # Save examples to JSON files
    print("\n" + "=" * 80)
    print("Saving examples to JSON files...")
    print("=" * 80)
    
    with open("example_external_1035_exchange.json", "w") as f:
        f.write(txn1.model_dump_json(indent=2))
    print("✓ Saved: example_external_1035_exchange.json")
    
    with open("example_internal_exchange.json", "w") as f:
        f.write(txn2.model_dump_json(indent=2))
    print("✓ Saved: example_internal_exchange.json")
    
    with open("example_qualified_ira_exchange.json", "w") as f:
        f.write(txn3.model_dump_json(indent=2))
    print("✓ Saved: example_qualified_ira_exchange.json")
    
    print("\n" + "=" * 80)
    print("Examples created successfully!")
    print("=" * 80)
    print("\nThese payloads can be:")
    print("  1. Sent to POST /api/replacement-transactions/validate for validation")
    print("  2. Sent to POST /api/replacement-transactions/submit for processing")
    print("  3. Used as templates for your own integrations")
    print("  4. Consumed by any order entry system")
