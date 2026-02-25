export type AlertType = 
  // Policy-level alerts (existing annuity optimization)
  | 'REPLACEMENT' 
  | 'INCOME_ACTIVATION' 
  | 'SUITABILITY_DRIFT' 
  | 'MISSING_INFO'
  // Client-level acquisition alerts (NEW annuity business growth)
  | 'EXCESS_LIQUIDITY'           // Too much cash earning low interest
  | 'PORTFOLIO_UNPROTECTED'      // High equity exposure without guaranteed income
  | 'TAX_INEFFICIENCY'           // Taxable accounts benefiting from tax deferral
  | 'CD_MATURITY'                // CDs maturing - better rates available
  | 'INCOME_GAP'                 // Retirement income shortfall
  | 'QUALIFIED_OPPORTUNITY'      // Large IRA annuitization opportunity
  | 'BENEFICIARY_PLANNING'       // Estate planning death benefit need
  | 'DIVERSIFICATION_GAP';       // Missing insurance products in portfolio

export type AlertSeverity = 'HIGH' | 'MEDIUM' | 'LOW';

export interface Alert {
  alertId: string;
  type: AlertType;
  severity: AlertSeverity;
  title: string;
  reasonShort: string;
  reasons: string[];
  createdAt: string;
}

export interface AlertBadge {
  type: AlertType;
  severity: AlertSeverity;
  icon: string;
  color: string;
  label: string;
}
