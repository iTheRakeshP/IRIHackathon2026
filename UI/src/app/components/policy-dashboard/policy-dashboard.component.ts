import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatChipsModule } from '@angular/material/chips';
import { MatIconModule } from '@angular/material/icon';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatCardModule } from '@angular/material/card';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { ApiService } from '../../services/api.service';
import { Policy } from '../../models/policy.model';
import { Alert, AlertBadge } from '../../models/alert.model';
import { PolicyDetailModalComponent } from '../policy-detail/policy-detail-modal.component';

@Component({
  selector: 'app-policy-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    MatTableModule,
    MatButtonModule,
    MatChipsModule,
    MatIconModule,
    MatTooltipModule,
    MatCardModule,
    MatProgressSpinnerModule,
    MatDialogModule,
    PolicyDetailModalComponent
  ],
  templateUrl: './policy-dashboard.component.html',
  styleUrls: ['./policy-dashboard.component.scss']
})
export class PolicyDashboardComponent implements OnInit {
  policies: Policy[] = [];
  groupedPolicies: any[] = [];
  displayedColumns: string[] = ['clientInfo', 'policy', 'daysToRenewal', 'alerts', 'actions'];
  loading = true;
  expandedClients: Set<string> = new Set(); // Track expanded clients
  allExpanded = true;

  constructor(
    private apiService: ApiService,
    private dialog: MatDialog
  ) {}

  ngOnInit(): void {
    this.loadPolicies();
  }

  loadPolicies(): void {
    this.loading = true;
    this.apiService.getPolicies().subscribe({
      next: (groupedPolicies) => {
        // Keep the grouped structure for display
        this.groupedPolicies = groupedPolicies.map((group: any) => ({
          ...group,
          policies: group.policies.map((policy: any) => ({
            ...policy,
            clientName: group.clientName,
            clientAccountNumber: group.clientAccountNumber
          }))
        }));
        // Expand all clients by default
        this.groupedPolicies.forEach(group => {
          this.expandedClients.add(group.clientAccountNumber);
        });
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading policies:', error);
        this.loading = false;
      }
    });
  }

  toggleClientExpansion(clientAccountNumber: string): void {
    if (this.expandedClients.has(clientAccountNumber)) {
      this.expandedClients.delete(clientAccountNumber);
    } else {
      this.expandedClients.add(clientAccountNumber);
    }
  }

  isClientExpanded(clientAccountNumber: string): boolean {
    return this.expandedClients.has(clientAccountNumber);
  }

  toggleExpandAll(): void {
    if (this.allExpanded) {
      // Collapse all
      this.expandedClients.clear();
      this.allExpanded = false;
    } else {
      // Expand all
      this.groupedPolicies.forEach(group => {
        this.expandedClients.add(group.clientAccountNumber);
      });
      this.allExpanded = true;
    }
  }

  // Dashboard stat methods
  getTotalAlerts(): number {
    return this.groupedPolicies.reduce((total, group) => {
      return total + group.policies.reduce((sum: number, policy: any) => {
        return sum + (policy.alerts?.length || 0);
      }, 0);
    }, 0);
  }

  getHighPriorityCount(): number {
    return this.groupedPolicies.reduce((total, group) => {
      return total + group.policies.reduce((sum: number, policy: any) => {
        return sum + (policy.alerts?.filter((a: Alert) => a.severity === 'HIGH').length || 0);
      }, 0);
    }, 0);
  }

  getUrgentRenewalsCount(): number {
    return this.groupedPolicies.reduce((total, group) => {
      return total + group.policies.filter((policy: any) => 
        policy.renewalDays !== undefined && policy.renewalDays !== null && policy.renewalDays <= 30
      ).length;
    }, 0);
  }

  getTotalAUM(): string {
    // Placeholder - would calculate from actual policy values
    return '$2.0M';
  }

  // Client-level helper methods
  getTotalAlertsForClient(group: any): number {
    return group.policies.reduce((sum: number, policy: any) => {
      return sum + (policy.alerts?.length || 0);
    }, 0);
  }

  getClientRenewalSummary(group: any): string {
    const urgentCount = group.policies.filter((policy: any) => 
      policy.renewalDays !== undefined && policy.renewalDays !== null && policy.renewalDays <= 15
    ).length;
    
    if (urgentCount > 0) {
      return `${urgentCount} urgent`;
    }
    
    const warningCount = group.policies.filter((policy: any) => 
      policy.renewalDays !== undefined && policy.renewalDays !== null && policy.renewalDays <= 30 && policy.renewalDays > 15
    ).length;
    
    if (warningCount > 0) {
      return `${warningCount} within 30 days`;
    }
    
    return '—';
  }

  getClientPriority(group: any): string {
    const hasHighSeverity = group.policies.some((policy: any) => 
      policy.alerts?.some((alert: Alert) => alert.severity === 'HIGH')
    );
    
    if (hasHighSeverity) return 'HIGH';
    
    const hasMediumSeverity = group.policies.some((policy: any) => 
      policy.alerts?.some((alert: Alert) => alert.severity === 'MEDIUM')
    );
    
    if (hasMediumSeverity) return 'MEDIUM';
    
    return 'LOW';
  }

  formatAccountNumber(accountNumber: string): string {
    // Format as 3-6-3 (e.g., 101-123456-001)
    if (accountNumber.length === 12) {
      return `${accountNumber.substring(0, 3)}-${accountNumber.substring(3, 9)}-${accountNumber.substring(9)}`;
    }
    return accountNumber;
  }

  getAlertBadges(alerts: Alert[]): AlertBadge[] {
    if (!alerts || !Array.isArray(alerts)) return [];
    return alerts.map(alert => {
      let icon = '';
      let color = '';
      let label = '';

      switch (alert.type) {
        case 'REPLACEMENT':
          icon = 'sync_alt';
          color = 'warn';
          label = 'Replacement';
          break;
        case 'INCOME_ACTIVATION':
          icon = 'payments';
          color = 'accent';
          label = 'Income';
          break;
        case 'SUITABILITY_DRIFT':
          icon = 'info';
          color = 'primary';
          label = 'Suitability';
          break;
      }

      return {
        type: alert.type,
        severity: alert.severity,
        icon,
        color,
        label
      };
    });
  }

  getVisibleBadges(alerts: Alert[]): AlertBadge[] {
    const badges = this.getAlertBadges(alerts);
    return badges.slice(0, 3);
  }

  getOverflowCount(alerts: Alert[]): number {
    if (!alerts || !Array.isArray(alerts)) return 0;
    return Math.max(0, alerts.length - 3);
  }

  getTotalAlertBadges(group: any): any[] {
    const alertCounts: { [key: string]: { count: number, severity: string, type: string } } = {};
    
    group.policies.forEach((policy: any) => {
      if (policy.alerts && Array.isArray(policy.alerts)) {
        policy.alerts.forEach((alert: Alert) => {
          const key = alert.severity;
          if (!alertCounts[key]) {
            alertCounts[key] = { count: 0, severity: alert.severity, type: alert.type };
          }
          alertCounts[key].count++;
        });
      }
    });

    return Object.values(alertCounts);
  }

  getDaysToRenewalText(days: number | undefined): string {
    if (days === undefined || days === null) {
      return 'N/A';
    }
    if (days < 0) {
      return 'Expired';
    }
    if (days === 0) {
      return 'Today';
    }
    if (days === 1) {
      return '1 day';
    }
    return `${days} days`;
  }

  getDaysToRenewalClass(days: number | undefined): string {
    if (days === undefined || days === null) {
      return '';
    }
    if (days <= 15) {
      return 'urgent';
    }
    if (days <= 30) {
      return 'warning';
    }
    return '';
  }

  onReviewPolicy(policy: Policy): void {
    console.log('Opening modal for policy:', policy);
    
    // Open the Policy Detail Modal
    const dialogRef = this.dialog.open(PolicyDetailModalComponent, {
      width: '95vw',
      maxWidth: '1400px',
      height: '85vh',
      maxHeight: '900px',
      panelClass: 'policy-detail-dialog',
      disableClose: false
    });

    console.log('Dialog opened, component instance:', dialogRef.componentInstance);

    // Set the policy and client data for the modal
    if (dialogRef.componentInstance) {
      dialogRef.componentInstance.setData(
        policy.policyId,
        policy.clientAccountNumber || '',
        undefined
      );
    }

    // Handle dialog close
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        // Refresh policies if needed
        console.log('Modal closed with result:', result);
      }
    });
  }

  onAlertBadgeClick(group: any, policy: any, event: Event): void {
    event.stopPropagation();
    // Open the Policy Detail Modal with specific alert focused
    const dialogRef = this.dialog.open(PolicyDetailModalComponent, {
      width: '95vw',
      maxWidth: '1400px',
      height: '85vh',
      maxHeight: '900px',
      panelClass: 'policy-detail-dialog',
      disableClose: false
    });

    // Set the policy and client data with first alert focused
    if (dialogRef.componentInstance && policy.alerts && policy.alerts.length > 0) {
      dialogRef.componentInstance.setData(
        policy.policyId,
        policy.clientAccountNumber || group.clientAccountNumber,
        policy.alerts[0].type
      );
    }
  }
}
