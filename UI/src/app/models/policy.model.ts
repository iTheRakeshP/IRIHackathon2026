import { Alert } from './alert.model';

export interface Beneficiary {
  name: string | null;
  relationship: string | null;
  ssn: string | null;
  dateOfBirth: string | null;
  allocationPercent: number | null;
}

export interface TaxWithholding {
  federal: number | null;
  state: number | null;
}

export interface ContactInfo {
  address: string | null;
  email: string | null;
  phone: string | null;
}

export interface NonFinancialData {
  ownerName: string | null;
  ownerSSN: string | null;
  primaryBeneficiary: Beneficiary | null;
  contingentBeneficiary: Beneficiary | null;
  contactInfo: ContactInfo | null;
  taxWithholding: TaxWithholding | null;
  specialInstructions: string | null;
  lastUpdated: string | null;
}

export interface Policy {
  policyId: string;
  clientAccountNumber: string;
  clientName: string;
  carrier: string;
  productType: string;
  productName?: string;
  issueDate: string;
  renewalDate?: string;
  renewalDays?: number;
  daysToRenewal?: number; // Alias for renewalDays
  contractValue: number;
  accountValue?: number;
  cashSurrenderValue?: number;
  deathBenefit?: number;
  currentSurrenderCharge?: number;
  surrenderEndDate?: string;
  currentCapRate?: number;
  projectedRenewalRate?: number;
  riders?: string[];
  annualFee?: number;
  riderFee?: number;
  meFee?: number;
  adminFee?: number;
  nonFinancialData?: NonFinancialData;
  alerts: Alert[];
}

export interface PolicyOverview extends Policy {
  surrenderSchedule?: string;
  renewalTerms?: string;
  fees?: {
    name: string;
    value: string;
  }[];
}
