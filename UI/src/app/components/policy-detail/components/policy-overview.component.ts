import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatDividerModule } from '@angular/material/divider';
import { MatChipsModule } from '@angular/material/chips';
import { Policy } from '../../../models/policy.model';

@Component({
  selector: 'app-policy-overview',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatIconModule,
    MatDividerModule,
    MatChipsModule
  ],
  templateUrl: './policy-overview.component.html',
  styleUrls: ['./policy-overview.component.scss']
})
export class PolicyOverviewComponent {
  @Input() policy!: Policy;

  formatCurrency(value: number | undefined): string {
    if (value === undefined || value === null) return 'N/A';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(value);
  }

  formatDate(date: string | undefined): string {
    if (!date) return 'N/A';
    try {
      return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    } catch {
      return date;
    }
  }

  formatPercentage(value: number | undefined): string {
    if (value === undefined || value === null) return 'N/A';
    return `${value.toFixed(2)}%`;
  }

  getSurrenderStatus(): string {
    if (!this.policy.surrenderEndDate) return 'N/A';
    
    const endDate = new Date(this.policy.surrenderEndDate);
    const today = new Date();
    const diffTime = endDate.getTime() - today.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays < 0) {
      return 'Ended';
    } else if (diffDays === 0) {
      return 'Ends Today';
    } else if (diffDays <= 30) {
      return `Ends in ${diffDays} days`;
    } else {
      return `Ends ${this.formatDate(this.policy.surrenderEndDate)}`;
    }
  }

  getRiders(): string[] {
    if (!this.policy.riders || this.policy.riders.length === 0) {
      return ['None'];
    }
    return this.policy.riders;
  }
}
