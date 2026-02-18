export type AlertType = 'REPLACEMENT' | 'INCOME_ACTIVATION' | 'SUITABILITY_DRIFT' | 'MISSING_INFO';
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
