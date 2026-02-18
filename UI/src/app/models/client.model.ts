export interface Client {
  clientId: string;
  clientAccountNumber: string;
  accountNumber: string; // Legacy field for compatibility
  name: string; // Full name
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  suitability?: SuitabilityProfile;
  suitabilityProfile?: SuitabilityProfile; // Legacy field for compatibility
}

export interface SuitabilityProfile {
  age?: number;
  riskTolerance: string;
  primaryObjective: string;
  secondaryObjective: string;
  currentIncomeNeed: string;
  lifeStage: string;
  liquidityImportance: string;
  state?: string;
  maritalStatus?: string;
  dependents?: number;
  investmentExperience?: string;
  volatilityComfort?: string;
  investmentHorizon?: string;
  withdrawalHorizon?: string;
  annualIncomeRange?: string;
  netWorthRange?: string;
  liquidNetWorthRange?: string;
  taxBracket?: string;
  retirementTargetYear?: number;
  citizenship?: string;
  advisoryModel?: string;
  isFeeBasedAccount?: boolean;
  lastUpdated?: string;
  updatedBy?: string;
  updatedAt?: string;
}
