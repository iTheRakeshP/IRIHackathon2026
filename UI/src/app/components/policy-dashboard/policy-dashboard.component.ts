import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatChipsModule } from '@angular/material/chips';
import { MatIconModule } from '@angular/material/icon';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatCardModule } from '@angular/material/card';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatMenuModule } from '@angular/material/menu';
import { ApiService } from '../../services/api.service';
import { Policy } from '../../models/policy.model';
import { Alert, AlertBadge, AlertType, AlertSeverity } from '../../models/alert.model';
import { PolicyDetailModalComponent } from '../policy-detail/policy-detail-modal.component';
import { AlertDetailModalComponent } from '../alert-detail/alert-detail-modal.component';
import { AcquisitionAlertsListComponent } from '../acquisition-alerts-list/acquisition-alerts-list.component';

@Component({
  selector: 'app-policy-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatTableModule,
    MatButtonModule,
    MatChipsModule,
    MatIconModule,
    MatTooltipModule,
    MatCardModule,
    MatProgressSpinnerModule,
    MatDialogModule,
    MatSelectModule,
    MatFormFieldModule,
    MatInputModule,
    MatAutocompleteModule,
    MatMenuModule,
    PolicyDetailModalComponent
  ],
  templateUrl: './policy-dashboard.component.html',
  styleUrls: ['./policy-dashboard.component.scss']
})
export class PolicyDashboardComponent implements OnInit {
  policies: Policy[] = [];
  groupedPolicies: any[] = [];
  filteredGroupedPolicies: any[] = [];
  displayedColumns: string[] = ['clientInfo', 'policy', 'daysToRenewal', 'alerts', 'actions'];
  loading = true;
  expandedClients: Set<string> = new Set(); // Track expanded clients
  allExpanded = true;

  // Filter properties
  selectedCarrier: string = '';
  selectedAlertTypes: AlertType[] = [];
  selectedPriorities: AlertSeverity[] = [];
  searchText: string = '';

  // Available filter options
  availableCarriers: string[] = [];
  availableAlertTypes: { value: AlertType, label: string }[] = [
    // Policy-level alerts (annuity optimization)
    { value: 'REPLACEMENT', label: 'Replacement' },
    { value: 'INCOME_ACTIVATION', label: 'Income Activation' },
    { value: 'SUITABILITY_DRIFT', label: 'Suitability Drift' },
    { value: 'MISSING_INFO', label: 'Missing Info' },
    // Client-level acquisition alerts (NEW business growth)
    { value: 'EXCESS_LIQUIDITY', label: '💰 Excess Cash' },
    { value: 'PORTFOLIO_UNPROTECTED', label: '🎯 Unprotected Portfolio' },
    { value: 'CD_MATURITY', label: '🔔 CD Maturing' },
    { value: 'INCOME_GAP', label: '🚀 Income Gap' },
    { value: 'DIVERSIFICATION_GAP', label: '📊 Diversification Gap' }
  ];
  availablePriorities: { value: AlertSeverity, label: string }[] = [
    { value: 'HIGH', label: 'High Priority' },
    { value: 'MEDIUM', label: 'Medium Priority' },
    { value: 'LOW', label: 'Low Priority' }
  ];

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
          })),
          acquisitionAlerts: []  // Will be populated below
        }));

        // Load acquisition alerts for each client (parallel requests)
        const acquisitionAlertRequests = this.groupedPolicies.map(group =>
          this.apiService.getClientAcquisitionAlerts(group.clientAccountNumber)
        );

        // Wait for all acquisition alert requests to complete
        Promise.all(acquisitionAlertRequests.map(req => req.toPromise()))
          .then(results => {
            // Attach acquisition alerts to each client group
            results.forEach((result: any, index) => {
              if (result && result.alerts) {
                this.groupedPolicies[index].acquisitionAlerts = result.alerts;
              }
            });

            // Extract unique carriers and clients for filter options
            this.extractFilterOptions();

            // Apply initial filtering
            this.applyFilters();

            // Expand all clients by default
            this.filteredGroupedPolicies.forEach(group => {
              this.expandedClients.add(group.clientAccountNumber);
            });
            this.loading = false;
          })
          .catch(error => {
            console.warn('Error loading acquisition alerts:', error);
            // Continue anyway - policy data is already loaded
            this.extractFilterOptions();
            this.applyFilters();
            this.filteredGroupedPolicies.forEach(group => {
              this.expandedClients.add(group.clientAccountNumber);
            });
            this.loading = false;
          });
      },
      error: (error) => {
        console.error('Error loading policies:', error);
        this.loading = false;
      }
    });
  }

  extractFilterOptions(): void {
    // Extract unique carriers
    const carrierSet = new Set<string>();

    this.groupedPolicies.forEach(group => {
      // Extract carriers from policies
      group.policies.forEach((policy: any) => {
        if (policy.carrier) {
          carrierSet.add(policy.carrier);
        }
      });
    });

    this.availableCarriers = Array.from(carrierSet).sort();
  }

  applyFilters(): void {
    let filtered = [...this.groupedPolicies];

    // Filter by search text (client name or account number)
    if (this.searchText) {
      const searchLower = this.searchText.toLowerCase();
      filtered = filtered.filter(group => 
        group.clientName.toLowerCase().includes(searchLower) ||
        group.clientAccountNumber.toLowerCase().includes(searchLower)
      );
    }

    // Filter policies within each group
    filtered = filtered.map(group => {
      let filteredPolicies = [...group.policies];

      // Filter by carrier
      if (this.selectedCarrier) {
        filteredPolicies = filteredPolicies.filter((policy: any) => 
          policy.carrier === this.selectedCarrier
        );
      }

      // Filter by alert types
      if (this.selectedAlertTypes.length > 0) {
        filteredPolicies = filteredPolicies.filter((policy: any) => 
          policy.alerts && policy.alerts.some((alert: Alert) => 
            this.selectedAlertTypes.includes(alert.type)
          )
        );
      }

      // Filter by priorities
      if (this.selectedPriorities.length > 0) {
        filteredPolicies = filteredPolicies.filter((policy: any) => 
          policy.alerts && policy.alerts.some((alert: Alert) => 
            this.selectedPriorities.includes(alert.severity)
          )
        );
      }

      return {
        ...group,
        policies: filteredPolicies
      };
    }).filter(group => group.policies.length > 0); // Remove groups with no policies

    this.filteredGroupedPolicies = filtered;
  }

  onCarrierChange(): void {
    this.applyFilters();
  }

  onAlertTypeChange(): void {
    this.applyFilters();
  }

  onPriorityChange(): void {
    this.applyFilters();
  }

  onSearchTextChange(): void {
    this.applyFilters();
  }

  clearFilters(): void {
    this.selectedCarrier = '';
    this.selectedAlertTypes = [];
    this.selectedPriorities = [];
    this.searchText = '';
    this.applyFilters();
  }

  hasActiveFilters(): boolean {
    return !!(this.selectedCarrier || 
              this.selectedAlertTypes.length > 0 || 
              this.selectedPriorities.length > 0 ||
              this.searchText);
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
      this.filteredGroupedPolicies.forEach(group => {
        this.expandedClients.add(group.clientAccountNumber);
      });
      this.allExpanded = true;
    }
  }

  // Dashboard stat methods
  getTotalAlerts(): number {
    return this.filteredGroupedPolicies.reduce((total, group) => {
      // Policy-level alerts
      const policyAlerts = group.policies.reduce((sum: number, policy: any) => {
        return sum + (policy.alerts?.length || 0);
      }, 0);
      // Client-level acquisition alerts
      const acquisitionAlerts = group.acquisitionAlerts?.length || 0;
      return total + policyAlerts + acquisitionAlerts;
    }, 0);
  }

  getHighPriorityCount(): number {
    return this.filteredGroupedPolicies.reduce((total, group) => {
      // Policy-level high priority
      const policyHighPriority = group.policies.reduce((sum: number, policy: any) => {
        return sum + (policy.alerts?.filter((a: Alert) => a.severity === 'HIGH').length || 0);
      }, 0);
      // Client-level acquisition high priority
      const acquisitionHighPriority = group.acquisitionAlerts?.filter((a: Alert) => a.severity === 'HIGH').length || 0;
      return total + policyHighPriority + acquisitionHighPriority;
    }, 0);
  }

  getUrgentRenewalsCount(): number {
    return this.filteredGroupedPolicies.reduce((total, group) => {
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
    // Policy-level alerts
    const policyAlerts = group.policies.reduce((sum: number, policy: any) => {
      return sum + (policy.alerts?.length || 0);
    }, 0);
    // Client-level acquisition alerts
    const acquisitionAlerts = group.acquisitionAlerts?.length || 0;
    return policyAlerts + acquisitionAlerts;
  }

  getAcquisitionAlertsForClient(group: any): Alert[] {
    return group.acquisitionAlerts || [];
  }

  hasAcquisitionAlerts(group: any): boolean {
    return group.acquisitionAlerts && group.acquisitionAlerts.length > 0;
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

  getProductName(policy: any): string {
    // Return policyLabel if available, otherwise construct from carrier and type
    if (policy.policyLabel) {
      return policy.policyLabel;
    }
    // Fallback: construct a readable name
    return `${policy.carrier} ${policy.productType}`;
  }

  getAlertBadge(alertType: AlertType): AlertBadge {
    let icon = '';
    let color = '';
    let label = '';

    switch (alertType) {
      // Policy-level alerts (annuity optimization)
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
      case 'MISSING_INFO':
        icon = 'assignment_late';
        color = 'accent';
        label = 'Missing Info';
        break;
      // Client-level acquisition alerts (NEW business growth)
      case 'EXCESS_LIQUIDITY':
        icon = 'attach_money';
        color = 'success';
        label = 'Excess Cash';
        break;
      case 'PORTFOLIO_UNPROTECTED':
        icon = 'shield';
        color = 'warn';
        label = 'Unprotected';
        break;
      case 'CD_MATURITY':
        icon = 'schedule';
        color = 'accent';
        label = 'CD Maturing';
        break;
      case 'INCOME_GAP':
        icon = 'trending_down';
        color = 'warn';
        label = 'Income Gap';
        break;
      case 'DIVERSIFICATION_GAP':
        icon = 'pie_chart';
        color = 'primary';
        label = 'Diversify';
        break;
      case 'TAX_INEFFICIENCY':
        icon = 'account_balance';
        color = 'accent';
        label = 'Tax Savings';
        break;
      case 'QUALIFIED_OPPORTUNITY':
        icon = 'savings';
        color = 'success';
        label = 'IRA Opportunity';
        break;
      case 'BENEFICIARY_PLANNING':
        icon = 'family_restroom';
        color = 'primary';
        label = 'Estate Planning';
        break;
      default:
        icon = 'info';
        color = 'primary';
        label = 'Alert';
    }

    return {
      type: alertType,
      severity: 'MEDIUM',  // Default, will be overridden by actual alert
      icon,
      color,
      label
    };
  }

  getAlertBadges(alerts: Alert[]): AlertBadge[] {
    if (!alerts || !Array.isArray(alerts)) return [];
    return alerts.map(alert => {
      const badge = this.getAlertBadge(alert.type);
      return {
        ...badge,
        severity: alert.severity  // Use actual severity from alert
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

  onViewAcquisitionAlert(alert: any, group: any, event?: Event): void {
    if (event) {
      event.stopPropagation();
    }
    
    console.log('Opening acquisition alert detail:', alert);
    
    // Open the Alert Detail Modal
    const dialogRef = this.dialog.open(AlertDetailModalComponent, {
      width: '700px',
      maxWidth: '90vw',
      panelClass: 'alert-detail-dialog',
      disableClose: false,
      data: {
        alert: alert,
        clientName: group.clientName,
        clientAccountNumber: group.clientAccountNumber,
        totalPortfolioValue: group.totalPortfolioValue || 0
      }
    });

    // Handle dialog close if needed
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        console.log('Alert detail modal closed with result:', result);
      }
    });
  }

  getTotalAcquisitionAlerts(): number {
    let total = 0;
    this.groupedPolicies.forEach(group => {
      if (group.acquisitionAlerts) {
        total += group.acquisitionAlerts.length;
      }
    });
    return total;
  }

  openAllAcquisitionAlerts(): void {
    // Gather all acquisition alerts from all clients
    const allAlerts = this.groupedPolicies
      .filter(group => group.acquisitionAlerts && group.acquisitionAlerts.length > 0)
      .map(group => ({
        clientName: group.clientName,
        clientAccountNumber: group.clientAccountNumber,
        totalPortfolioValue: group.totalPortfolioValue || 0,
        alerts: group.acquisitionAlerts
      }));

    // Open the comprehensive acquisition alerts list
    const dialogRef = this.dialog.open(AcquisitionAlertsListComponent, {
      width: '95vw',
      maxWidth: '1600px',
      height: '90vh',
      maxHeight: '900px',
      panelClass: 'acquisition-alerts-list-dialog',
      disableClose: false,
      data: {
        allAlerts: allAlerts
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        console.log('Acquisition alerts list closed with result:', result);
      }
    });
  }
}
