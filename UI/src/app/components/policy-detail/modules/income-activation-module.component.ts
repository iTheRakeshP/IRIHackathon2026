import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import {MatDividerModule } from '@angular/material/divider';
import { MatTableModule } from '@angular/material/table';
import { MatTooltipModule } from '@angular/material/tooltip';
import { Alert } from '../../../models/alert.model';
import { Policy } from '../../../models/policy.model';
import { Client } from '../../../models/client.model';

interface IncomeScenario {
  option: string;
  description: string;
  monthlyIncome: number;
  annualIncome: number;
  lifetimeProjection: number;
  pros: string[];
  cons: string[];
}

@Component({
  selector: 'app-income-activation-module',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatDividerModule,
    MatTableModule,
    MatTooltipModule
  ],
  templateUrl: './income-activation-module.component.html',
  styleUrls: ['./income-activation-module.component.scss']
})
export class IncomeActivationModuleComponent {
  @Input() alert!: Alert;
  @Input() policy!: Policy;
  @Input() client!: Client;
  @Output() actionComplete = new EventEmitter<any>();

  scenarios: IncomeScenario[] = [
    {
      option: 'Begin Income Now',
      description: 'Start receiving guaranteed lifetime income immediately',
      monthlyIncome: 842,
      annualIncome: 10104,
      lifetimeProjection: 252600,
      pros: [
        'Immediate income stream starting this month',
        'Guaranteed for life regardless of market performance',
        'Current payout rate: 5.2%'
      ],
      cons: [
        'Lower payout rate than waiting',
        'Reduces accumulation potential',
        'Cannot reverse once activated'
      ]
    },
    {
      option: 'Delay Income (2 Years)',
      description: 'Wait 2 years to activate with higher payout rate and deferral bonuses',
      monthlyIncome: 1053,
      annualIncome: 12636,
      lifetimeProjection: 315900,
      pros: [
        '25% higher monthly income ($211/month more)',
        'Additional 2 years of 6% deferral bonus',
        'Higher lifetime income projection'
      ],
      cons: [
        'No income for 2 years',
        'Assumes client can wait',
        'Market risk during deferral period'
      ]
    }
  ];

  formatCurrency(value: number): string {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(value);
  }

  onDocumentDecision(): void {
    this.actionComplete.emit({
      action: 'document_timing_decision',
      alertId: this.alert.alertId,
      policyId: this.policy.policyId
    });
  }

  onAskAI(): void {
    console.log('Ask AI about income activation timing');
  }

  onMarkReviewed(): void {
    this.actionComplete.emit({
      action: 'mark_reviewed',
      alertId: this.alert.alertId
    });
  }
}
