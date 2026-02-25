import { Component, Inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatDialogModule, MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatChipsModule } from '@angular/material/chips';
import { MatTableModule } from '@angular/material/table';
import { MatTooltipModule } from '@angular/material/tooltip';
import { AlertDetailModalComponent } from '../alert-detail/alert-detail-modal.component';
import { MatDialog } from '@angular/material/dialog';

export interface AcquisitionAlertsData {
  allAlerts: any[];
}

@Component({
  selector: 'app-acquisition-alerts-list',
  standalone: true,
  imports: [
    CommonModule,
    MatDialogModule,
    MatIconModule,
    MatButtonModule,
    MatChipsModule,
    MatTableModule,
    MatTooltipModule
  ],
  templateUrl: './acquisition-alerts-list.component.html',
  styleUrls: ['./acquisition-alerts-list.component.scss']
})
export class AcquisitionAlertsListComponent implements OnInit {
  displayedColumns: string[] = ['severity', 'client', 'type', 'title', 'summary', 'action'];
  clientAlerts: any[] = [];
  totalEstimatedAUM: number = 0;
  totalClients: number = 0;
  totalAlerts: number = 0;

  constructor(
    public dialogRef: MatDialogRef<AcquisitionAlertsListComponent>,
    @Inject(MAT_DIALOG_DATA) public data: AcquisitionAlertsData,
    private dialog: MatDialog
  ) {}

  ngOnInit(): void {
    this.processAlerts();
  }

  processAlerts(): void {
    // Flatten the structure: each row is one alert with client info
    this.clientAlerts = [];
    const clientsSet = new Set<string>();

    this.data.allAlerts.forEach((clientData: any) => {
      clientsSet.add(clientData.clientAccountNumber);
      
      if (clientData.alerts && clientData.alerts.length > 0) {
        clientData.alerts.forEach((alert: any) => {
          this.clientAlerts.push({
            ...alert,
            clientName: clientData.clientName,
            clientAccountNumber: clientData.clientAccountNumber,
            totalPortfolioValue: clientData.totalPortfolioValue
          });
        });
      }
    });

    this.totalClients = clientsSet.size;
    this.totalAlerts = this.clientAlerts.length;
    
    // Sort by severity (HIGH > MEDIUM > LOW)
    this.clientAlerts.sort((a, b) => {
      const severityOrder = { 'HIGH': 0, 'MEDIUM': 1, 'LOW': 2 };
      return (severityOrder[a.severity as keyof typeof severityOrder] || 3) - 
             (severityOrder[b.severity as keyof typeof severityOrder] || 3);
    });
  }

  close(): void {
    this.dialogRef.close();
  }

  getSeverityClass(severity: string): string {
    return `severity-${severity.toLowerCase()}`;
  }

  getAlertTypeLabel(type: string): string {
    const typeLabels: Record<string, string> = {
      'EXCESS_LIQUIDITY': '💰 Excess Cash',
      'PORTFOLIO_UNPROTECTED': '🎯 Unprotected Portfolio',
      'CD_MATURITY': '🔔 CD Maturing',
      'INCOME_GAP': '📊 Income Gap',
      'DIVERSIFICATION_GAP': '🔄 Diversification',
      'TAX_INEFFICIENCY': '💸 Tax Inefficiency',
      'QUALIFIED_OPPORTUNITY': '🏦 Qualified Opportunity',
      'BENEFICIARY_PLANNING': '👨‍👩‍👧 Beneficiary Planning'
    };
    return typeLabels[type] || type;
  }

  openAlertDetail(alert: any): void {
    const detailDialog = this.dialog.open(AlertDetailModalComponent, {
      width: '700px',
      maxWidth: '90vw',
      panelClass: 'alert-detail-dialog',
      disableClose: false,
      data: {
        alert: alert,
        clientName: alert.clientName,
        clientAccountNumber: alert.clientAccountNumber,
        totalPortfolioValue: alert.totalPortfolioValue
      }
    });
  }

  formatCurrency(value: number): string {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(value);
  }

  getHighPriorityCount(): number {
    return this.clientAlerts.filter(a => a.severity === 'HIGH').length;
  }

  getMediumPriorityCount(): number {
    return this.clientAlerts.filter(a => a.severity === 'MEDIUM').length;
  }

  getLowPriorityCount(): number {
    return this.clientAlerts.filter(a => a.severity === 'LOW').length;
  }
}
