import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatDividerModule } from '@angular/material/divider';
import { MatTooltipModule } from '@angular/material/tooltip';
import { Alert } from '../../../models/alert.model';
import { Policy } from '../../../models/policy.model';
import { Client } from '../../../models/client.model';
import { AiChatService } from '../../../services/ai-chat.service';

interface DriftItem {
  category: string;
  previous: string;
  current: string;
  impact: 'low' | 'medium' | 'high';
}

@Component({
  selector: 'app-suitability-drift-module',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatDividerModule,
    MatTooltipModule
  ],
  templateUrl: './suitability-drift-module.component.html',
  styleUrls: ['./suitability-drift-module.component.scss']
})
export class SuitabilityDriftModuleComponent {
  @Input() alert!: Alert;
  @Input() policy!: Policy;
  @Input() client!: Client;
  @Output() actionComplete = new EventEmitter<any>();

  constructor(private chatService: AiChatService) {}

  // Detected suitability changes
  driftItems: DriftItem[] = [
    {
      category: 'Primary Objective',
      previous: 'Growth',
      current: 'Income',
      impact: 'high'
    },
    {
      category: 'Life Stage',
      previous: 'Accumulation',
      current: 'Pre-Retirement',
      impact: 'medium'
    },
    {
      category: 'Risk Tolerance',
      previous: 'Moderate-Aggressive',
      current: 'Moderate',
      impact: 'medium'
    }
  ];

  onAskAI(): void {
    // Open AI chat with suitability drift context
    this.chatService.openChat({
      policyId: this.policy.policyId,
      clientAccountNumber: this.client.clientAccountNumber,
      alertType: this.alert.type,
      alertId: this.alert.alertId,
      policy: this.policy,
      client: this.client
    });
  }

  onMarkReviewed(): void {
    this.actionComplete.emit({
      action: 'mark_reviewed',
      alertId: this.alert.alertId
    });
  }

  onSaveNote(): void {
    this.actionComplete.emit({
      action: 'save_review_note',
      alertId: this.alert.alertId
    });
  }

  getImpactClass(impact: string): string {
    return `impact-${impact}`;
  }

  getImpactLabel(impact: string): string {
    return impact.charAt(0).toUpperCase() + impact.slice(1) + ' Impact';
  }
}
