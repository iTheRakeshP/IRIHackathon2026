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
  riskTolerance: string;
  primaryObjective: string;
  secondaryObjective: string;
  currentIncomeNeed: string;
  lifeStage: string;
  liquidityImportance: string;
  lastUpdated?: string;
  updatedBy?: string;
  updatedAt?: string;
}
