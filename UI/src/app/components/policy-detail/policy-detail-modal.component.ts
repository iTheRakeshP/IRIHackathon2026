import { Component, OnInit, OnDestroy, signal, computed, effect, ElementRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { MatTabsModule } from '@angular/material/tabs';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatCardModule } from '@angular/material/card';
import { MatDividerModule } from '@angular/material/divider';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { Policy } from '../../models/policy.model';
import { Alert } from '../../models/alert.model';
import { Client } from '../../models/client.model';
import { ApiService } from '../../services/api.service';
import { AiChatService } from '../../services/ai-chat.service';
import { PolicyOverviewComponent } from './components/policy-overview.component';
import { ReplacementModuleComponent } from './modules/replacement-module.component';
import { IncomeActivationModuleComponent } from './modules/income-activation-module.component';
import { SuitabilityDriftModuleComponent } from './modules/suitability-drift-module.component';
import { MissingInfoModuleComponent } from './modules/missing-info-module.component';
import { AiChatDrawerComponent } from '../ai-chat-drawer/ai-chat-drawer.component';

@Component({
  selector: 'app-policy-detail-modal',
  standalone: true,
  imports: [
    CommonModule,
    MatDialogModule,
    MatButtonModule,
    MatIconModule,
    MatChipsModule,
    MatTabsModule,
    MatExpansionModule,
    MatCardModule,
    MatDividerModule,
    MatProgressSpinnerModule,
    PolicyOverviewComponent,
    ReplacementModuleComponent,
    IncomeActivationModuleComponent,
    SuitabilityDriftModuleComponent,
    MissingInfoModuleComponent,
    AiChatDrawerComponent
  ],
  templateUrl: './policy-detail-modal.component.html',
  styleUrls: ['./policy-detail-modal.component.scss']
})
export class PolicyDetailModalComponent implements OnInit, OnDestroy {
  // ViewChild for scroll target
  @ViewChild('reviewModulesSection', { read: ElementRef }) reviewModulesSection?: ElementRef;
  
  // Signals for reactive state
  policy = signal<Policy | null>(null);
  client = signal<Client | null>(null);
  loading = signal<boolean>(true);
  expandedAlertId = signal<string | null>(null);
  activeAlertType = signal<string | null>(null);

  // Computed signals
  sortedAlerts = computed(() => {
    const pol = this.policy();
    if (!pol || !pol.alerts) return [];
    
    // Sort by severity: HIGH > MEDIUM > LOW
    const severityOrder: { [key: string]: number } = { 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3 };
    return [...pol.alerts].sort((a, b) => {
      return (severityOrder[a.severity] || 999) - (severityOrder[b.severity] || 999);
    });
  });

  highestSeverityAlert = computed(() => {
    const alerts = this.sortedAlerts();
    return alerts.length > 0 ? alerts[0] : null;
  });

  constructor(
    private dialogRef: MatDialogRef<PolicyDetailModalComponent>,
    private apiService: ApiService,
    public chatService: AiChatService
  ) {
    // Immediately close chat in constructor before anything else
    this.chatService.closeChat();
    this.chatService.clearChat();
  }

  ngOnInit(): void {
    // Double-check chat is closed when modal opens
    setTimeout(() => {
      this.chatService.closeChat();
      this.chatService.clearChat();
    }, 0);
  }

  ngOnDestroy(): void {
    // Always close and clear chat when modal is destroyed
    this.chatService.closeChat();
    this.chatService.clearChat();
  }

  // Method to set policy and client data from the dashboard
  setData(policyId: string, clientAccountNumber: string, focusAlertType?: string): void {
    console.log('Modal setData called with:', { policyId, clientAccountNumber, focusAlertType });
    this.loading.set(true);
    
    // Fetch policy details
    this.apiService.getPolicyById(policyId).subscribe({
      next: (policy) => {
        console.log('Policy loaded:', policy);
        this.policy.set(policy);
        
        // Fetch client details
        this.apiService.getClientByAccountNumber(clientAccountNumber).subscribe({
          next: (client) => {
            console.log('Client loaded:', client);
            this.client.set(client);
            this.loading.set(false);
            
            // Focus specific alert if requested
            if (focusAlertType) {
              const alert = policy.alerts?.find(a => a.type === focusAlertType);
              if (alert) {
                this.expandedAlertId.set(alert.alertId);
                this.activeAlertType.set(alert.type);
              }
            }
          },
          error: (error) => {
            console.error('Error loading client:', error);
            this.loading.set(false);
          }
        });
      },
      error: (error) => {
        console.error('Error loading policy:', error);
        this.loading.set(false);
      }
    });
  }

  onAlertPillClick(alert: Alert): void {
    // Toggle expansion - only one module open at a time
    if (this.expandedAlertId() === alert.alertId) {
      this.expandedAlertId.set(null);
      this.activeAlertType.set(null);
    } else {
      this.expandedAlertId.set(alert.alertId);
      this.activeAlertType.set(alert.type);
      
      // Scroll to the review modules section after a brief delay to allow DOM update
      setTimeout(() => {
        this.scrollToReviewModule();
      }, 100);
    }
  }

  private scrollToReviewModule(): void {
    if (this.reviewModulesSection) {
      this.reviewModulesSection.nativeElement.scrollIntoView({ 
        behavior: 'smooth', 
        block: 'start' 
      });
    }
  }

  isAlertExpanded(alertId: string): boolean {
    return this.expandedAlertId() === alertId;
  }

  getAlertIcon(alertType: string): string {
    switch (alertType) {
      case 'REPLACEMENT':
        return 'sync_alt';
      case 'INCOME_ACTIVATION':
        return 'payments';
      case 'SUITABILITY_DRIFT':
        return 'info';
      default:
        return 'notifications';
    }
  }

  getAlertSeverityClass(severity: string): string {
    return severity.toLowerCase();
  }

  onOpenAICopilot(): void {
    // Open AI Copilot drawer with full context
    this.chatService.openChat({
      policyId: this.policy()?.policyId,
      clientAccountNumber: this.client()?.clientAccountNumber,
      alertType: this.activeAlertType() || undefined,
      policy: this.policy(),
      client: this.client()
    });
  }

  onClose(): void {
    // Close chat drawer when modal closes
    this.chatService.closeChat();
    this.dialogRef.close();
  }

  onModuleActionComplete(action: any): void {
    // Handle module actions (e.g., mark reviewed, save note)
    console.log('Module action complete:', action);
  }
}
