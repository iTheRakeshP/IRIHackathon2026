import { Alert } from './alert.model';

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
