import { Component, Inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatDialogModule, MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatChipsModule } from '@angular/material/chips';

export interface AlertDetailData {
  alert: any;
  clientName: string;
  clientAccountNumber: string;
  totalPortfolioValue: number;
}

@Component({
  selector: 'app-alert-detail-modal',
  standalone: true,
  imports: [
    CommonModule,
    MatDialogModule,
    MatIconModule,
    MatButtonModule,
    MatChipsModule
  ],
  templateUrl: './alert-detail-modal.component.html',
  styleUrls: ['./alert-detail-modal.component.scss']
})
export class AlertDetailModalComponent {
  constructor(
    public dialogRef: MatDialogRef<AlertDetailModalComponent>,
    @Inject(MAT_DIALOG_DATA) public data: AlertDetailData
  ) {}

  close(): void {
    this.dialogRef.close();
  }

  getSeverityClass(): string {
    return `severity-${this.data.alert.severity.toLowerCase()}`;
  }

  getAlertTypeLabel(): string {
    const typeLabels: Record<string, string> = {
      'EXCESS_LIQUIDITY': '💰 Excess Cash',
      'PORTFOLIO_UNPROTECTED': '🎯 Unprotected Portfolio',
      'CD_MATURITY': '🔔 CD Maturing',
      'INCOME_GAP': '📊 Income Gap',
      'DIVERSIFICATION_GAP': '🔄 Diversification',
      'TAX_INEFFICIENCY': '💸 Tax Inefficiency',
      'QUALIFIED_OPPORTUNITY': '🏦 Qualified Opportunity',
      'BENEFICIARY_PLANNING': '👨‍👩‍👧 Beneficiary Planning',
      'REPLACEMENT': '🔄 Replacement',
      'INCOME_ACTIVATION': '💵 Income Activation',
      'SUITABILITY_DRIFT': '⚠️ Suitability Drift',
      'MISSING_INFO': '📋 Missing Info'
    };
    return typeLabels[this.data.alert.type] || this.data.alert.type;
  }

  formatCurrency(value: number): string {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(value);
  }
}
