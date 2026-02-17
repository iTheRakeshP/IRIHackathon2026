import { Component, Input, Output, EventEmitter, signal, computed, effect } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatDividerModule } from '@angular/material/divider';
import { MatChipsModule } from '@angular/material/chips';
import { MatStepperModule } from '@angular/material/stepper';
import { MatTableModule } from '@angular/material/table';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { Alert } from '../../../models/alert.model';
import { Policy } from '../../../models/policy.model';
import { Client } from '../../../models/client.model';
import { SuitabilityFormComponent } from '../components/suitability-form.component';
import { ApiService } from '../../../services/api.service';
import { AiChatService } from '../../../services/ai-chat.service';

interface Alternative {
  productId: string;
  carrier: string;
  productName: string;
  productType: string;
  capRate: number;
  annualFee: number;
  riderFee: number;
  totalCost: number;
  incomeRider: boolean;
  suitabilityScore: number;
  highlights: string[];
}

@Component({
  selector: 'app-replacement-module',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatDividerModule,
    MatChipsModule,
    MatStepperModule,
    MatTableModule,
    MatTooltipModule,
    MatProgressSpinnerModule,
    SuitabilityFormComponent
  ],
  templateUrl: './replacement-module.component.html',
  styleUrls: ['./replacement-module.component.scss']
})
export class ReplacementModuleComponent {
  @Input() alert!: Alert;
  @Input() policy!: Policy;
  @Input() client!: Client;
  @Output() actionComplete = new EventEmitter<any>();

  // Signals for state management
  currentStep = signal<number>(0); // 0: Why Flagged, 1: Suitability, 2: Alternatives
  suitabilityVerified = signal<boolean>(false);
  alternatives = signal<Alternative[]>([]);
  loadingAlternatives = signal<boolean>(false);
  savedNote = signal<string>('');

  // Computed
  canProceedToAlternatives = computed(() => this.suitabilityVerified());

  displayedColumns: string[] = ['feature', 'current', 'alternative1', 'alternative2', 'alternative3'];

  constructor(
    private apiService: ApiService,
    private chatService: AiChatService
  ) {
    // Update chat context when step changes
    effect(() => {
      const step = this.currentStep();
      const stepNames = ['why-flagged', 'suitability', 'alternatives'];
      this.chatService.updateContext({ 
        currentStep: stepNames[step],
        alternatives: step === 2 ? this.alternatives() : undefined
      });
    });
  }

  onSuitabilityVerified(): void {
    this.suitabilityVerified.set(true);
    // Auto-advance to next step
    setTimeout(() => {
      this.currentStep.set(1);
    }, 300);
  }

  onContinueToAlternatives(): void {
    if (!this.suitabilityVerified()) {
      return;
    }
    
    this.loadingAlternatives.set(true);
    this.currentStep.set(2);
    
    // Fetch alternatives from API
    this.apiService.getPolicyAlternatives(this.policy.policyId).subscribe({
      next: (response: any) => {
        console.log('API Response:', response);
        // Map API response to Alternative interface
        const mappedAlternatives = this.mapApiResponseToAlternatives(response);
        this.alternatives.set(mappedAlternatives);
        this.loadingAlternatives.set(false);
      },
      error: (error) => {
        console.error('Error loading alternatives:', error);
        this.loadingAlternatives.set(false);
        // Set mock data for demo
        this.alternatives.set(this.getMockAlternatives());
      }
    });
  }

  private mapApiResponseToAlternatives(response: any): Alternative[] {
    if (!response || !response.alternatives) {
      return this.getMockAlternatives();
    }

    return response.alternatives.slice(0, 3).map((product: any, index: number) => {
      // Get highest cap rate from index options
      let capRate = 0;
      if (product.indexOptions && product.indexOptions.length > 0) {
        const capOptions = product.indexOptions.filter((opt: any) => 
          opt.strategy && opt.strategy.toLowerCase().includes('cap')
        );
        if (capOptions.length > 0) {
          capRate = Math.max(...capOptions.map((opt: any) => opt.currentValue || 0));
        }
      }
      if (capRate === 0 && product.currentFixedRate) {
        capRate = product.currentFixedRate;
      }

      // Calculate fees
      const annualFee = (product.fees?.m_e_fee || 0) + (product.fees?.administrativeFee || 0);
      
      // Get income rider fee if available
      let riderFee = 0;
      let hasIncomeRider = false;
      if (product.availableRiders && product.availableRiders.length > 0) {
        const incomeRider = product.availableRiders.find((r: any) => 
          r.riderType && r.riderType.toLowerCase().includes('income')
        );
        if (incomeRider) {
          riderFee = incomeRider.annualFee || 0;
          hasIncomeRider = true;
        }
      }

      return {
        productId: product.productId,
        carrier: product.carrier,
        productName: product.productName,
        productType: product.productType,
        capRate: capRate,
        annualFee: annualFee,
        riderFee: riderFee,
        totalCost: this.calculateTotalCostFromFees(annualFee, riderFee),
        incomeRider: hasIncomeRider,
        suitabilityScore: 90 - (index * 5), // Mock score, higher for first alternatives
        highlights: this.generateHighlights(product, capRate)
      };
    });
  }

  private calculateTotalCostFromFees(annualFee: number, riderFee: number): number {
    // Assume $100k contract value for fee calculation
    return (annualFee * 100000) + (riderFee * 100000 / 100);
  }

  private generateHighlights(product: any, productCap: number): string[] {
    const highlights: string[] = [];
    const currentCap = this.policy.currentCapRate || 0;
    
    if (productCap > currentCap) {
      highlights.push(`Higher cap rate (${productCap.toFixed(2)}% vs current ${currentCap.toFixed(2)}%)`);
    }
    
    // Check for income rider
    if (product.availableRiders && product.availableRiders.length > 0) {
      const incomeRider = product.availableRiders.find((r: any) => 
        r.riderType && r.riderType.toLowerCase().includes('income')
      );
      if (incomeRider) {
        const rollupRate = incomeRider.rollUpRate || 6;
        highlights.push(`Income rider with ${rollupRate}% rollup`);
      }
    }
    
    if (product.competitiveAdvantages && product.competitiveAdvantages.length > 0) {
      highlights.push(...product.competitiveAdvantages.slice(0, 2));
    }
    
    // Add key benefits if not enough highlights
    if (highlights.length < 3 && product.keyBenefits && product.keyBenefits.length > 0) {
      const remaining = 3 - highlights.length;
      highlights.push(...product.keyBenefits.slice(0, remaining));
    }
    
    return highlights.slice(0, 3);
  }

  onInitiateReplacementReview(): void {
    this.actionComplete.emit({
      action: 'initiate_replacement',
      alertId: this.alert.alertId,
      policyId: this.policy.policyId
    });
  }

  onInitiateReplacementReviewForProduct(alternative: Alternative): void {
    // Update context when user hovers or clicks on a specific product
    this.chatService.updateContext({
      viewingAlternative: alternative,
      interactionType: 'reviewing-product'
    });
    
    this.actionComplete.emit({
      action: 'initiate_replacement',
      alertId: this.alert.alertId,
      policyId: this.policy.policyId,
      selectedProduct: {
        productId: alternative.productId,
        productName: alternative.productName,
        carrier: alternative.carrier,
        suitabilityScore: alternative.suitabilityScore
      }
    });
    
    console.log('Initiating replacement review for:', {
      currentPolicy: this.policy.policyId,
      newProduct: alternative.productName,
      carrier: alternative.carrier,
      matchScore: alternative.suitabilityScore
    });
  }

  onAlternativeHover(alternative: Alternative): void {
    // Update chat suggestions when hovering over an alternative
    this.chatService.updateContext({
      viewingAlternative: alternative,
      interactionType: 'hovering-product'
    });
  }

  onAlternativeLeave(): void {
    // Reset to alternatives view when not hovering
    this.chatService.updateContext({
      viewingAlternative: undefined,
      interactionType: 'viewing-alternatives'
    });
  }

  onSaveNote(note: string): void {
    this.savedNote.set(note);
    this.actionComplete.emit({
      action: 'save_note',
      alertId: this.alert.alertId,
      note: note
    });
  }

  onAskAI(): void {
    // Open AI chat with replacement-specific context
    this.chatService.openChat({
      policyId: this.policy.policyId,
      clientAccountNumber: this.client.clientAccountNumber,
      alertType: this.alert.type,
      alertId: this.alert.alertId,
      policy: this.policy,
      client: this.client,
      alternatives: this.alternatives()
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

  formatPercentage(value: number): string {
    return `${value.toFixed(2)}%`;
  }

  private getMockAlternatives(): Alternative[] {
    return [
      {
        productId: 'ALT-001',
        carrier: 'Symetra',
        productName: 'Symetra Advantage Income Pro',
        productType: 'Fixed Index Annuity',
        capRate: 6.50,
        annualFee: 0,
        riderFee: 0.95,
        totalCost: 950,
        incomeRider: true,
        suitabilityScore: 92,
        highlights: [
          'Higher cap rate (6.50% vs current 4.25%)',
          'Income rider with 7% rollup',
          'Best-in-class features for income'
        ]
      },
      {
        productId: 'ALT-002',
        carrier: 'Brighthouse Financial',
        productName: 'Shield Level Select',
        productType: 'Fixed Index Annuity',
        capRate: 6.25,
        annualFee: 0,
        riderFee: 1.00,
        totalCost: 1000,
        incomeRider: true,
        suitabilityScore: 88,
        highlights: [
          'Higher cap rate (6.25% vs current 4.25%)',
          'Downside protection with upside potential',
          'Guaranteed lifetime income available'
        ]
      },
      {
        productId: 'ALT-003',
        carrier: 'American Equity',
        productName: 'AssetShield 10',
        productType: 'Fixed Index Annuity',
        capRate: 6.00,
        annualFee: 0,
        riderFee: 0.85,
        totalCost: 850,
        incomeRider: true,
        suitabilityScore: 85,
        highlights: [
          'Competitive cap rate (6.00%)',
          'Lower fees than current policy',
          'Flexible income options'
        ]
      }
    ];
  }

  getComparisonData(): any[] {
    const alts = this.alternatives();
    if (alts.length === 0) return [];

    const buildRow = (feature: string, current: any, getValue: (alt: Alternative) => any) => {
      const row: any = { feature, current };
      alts.forEach((alt, idx) => {
        row[`alt${idx + 1}`] = getValue(alt);
      });
      return row;
    };

    return [
      buildRow('Carrier', this.policy.carrier, alt => alt.carrier),
      buildRow('Product', this.policy.productName, alt => alt.productName),
      {
        ...buildRow('Cap Rate', this.formatPercentage(this.policy.currentCapRate || 0), alt => this.formatPercentage(alt.capRate)),
        highlight: 'rate'
      },
      buildRow('Annual Fee', this.formatCurrency(this.policy.annualFee || 0), alt => this.formatCurrency(alt.annualFee)),
      buildRow('Rider Fee', this.formatPercentage(this.policy.riderFee || 0), alt => this.formatPercentage(alt.riderFee)),
      buildRow('Income Rider', this.policy.riders?.includes('Income') ? 'Yes' : 'No', alt => alt.incomeRider ? 'Yes' : 'No'),
      {
        ...buildRow('Suitability Match', '—', alt => `${alt.suitabilityScore}%`),
        highlight: 'score'
      }
    ];
  }
}
