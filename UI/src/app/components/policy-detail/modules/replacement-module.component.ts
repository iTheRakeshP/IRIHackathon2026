import { Component, Input, Output, EventEmitter, signal, computed, effect, ElementRef } from '@angular/core';
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
import { MatRadioModule } from '@angular/material/radio';
import { Alert } from '../../../models/alert.model';
import { Policy } from '../../../models/policy.model';
import { Client } from '../../../models/client.model';
import { SuitabilityFormComponent } from '../components/suitability-form.component';
import { PerformanceChartsComponent } from '../components/performance-charts.component';
import { ApiService } from '../../../services/api.service';
import { AiChatService } from '../../../services/ai-chat.service';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

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
  keyBenefits: string[];
  considerations: string[];
  optionType: 'renewal' | 'replacement';
  optionTitle: string;
  hasLicense?: boolean;
  hasAppointment?: boolean;
  hasTraining?: boolean;
  canSell?: boolean;
  complianceNotes?: string | null;
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
    MatRadioModule,
    PerformanceChartsComponent,
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
  exportingPDF = signal<boolean>(false);

  // Selection & Documentation flow
  selectedAlternativeId = signal<string | null>(null);
  documentationSummary = signal<string>('');
  documentationConfirmed = signal<boolean>(false);
  generatingDocumentation = signal<boolean>(false);

  // Computed
  canProceedToAlternatives = computed(() => this.suitabilityVerified());

  displayedColumns: string[] = ['feature', 'current', 'alternative1', 'alternative2', 'alternative3'];

  constructor(
    private apiService: ApiService,
    private chatService: AiChatService,
    private elementRef: ElementRef
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
        suitabilityScore: 90 - (index * 5),
        highlights: this.generateHighlights(product, capRate),
        keyBenefits: this.generateKeyBenefits(product, capRate),
        considerations: this.generateConsiderations(product),
        optionType: 'replacement' as const,
        optionTitle: this.generateOptionTitle(product, capRate),
        hasLicense: product.hasLicense ?? true,
        hasAppointment: product.hasAppointment ?? true,
        hasTraining: product.hasTraining ?? true,
        canSell: product.canSell ?? true,
        complianceNotes: product.complianceNotes || null
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

  private generateKeyBenefits(product: any, productCap: number): string[] {
    const benefits: string[] = [];
    const currentCap = this.policy.currentCapRate || this.policy.projectedRenewalRate || 0;

    // Rate improvement
    if (productCap > currentCap) {
      benefits.push(`Rate improvement: ${(productCap - currentCap).toFixed(1)}% increase (${currentCap.toFixed(1)}% → ${productCap.toFixed(1)}%)`);
    }

    // Premium bonus
    if (product.bonusRate) {
      benefits.push(`${product.bonusRate}% premium bonus on entire account value`);
    }

    // Enhanced features
    if (product.availableRiders && product.availableRiders.length > 0) {
      benefits.push('Enhanced features including death benefit protection');
    }

    // Carrier strength
    benefits.push(`Strong carrier rating (${product.carrier})`);

    // Income rider specifics
    if (product.availableRiders) {
      const incomeRider = product.availableRiders.find((r: any) =>
        r.riderType && r.riderType.toLowerCase().includes('income')
      );
      if (incomeRider && incomeRider.rollUpRate) {
        benefits.push(`Income rider with ${incomeRider.rollUpRate}% guaranteed rollup`);
      }
    }

    // From product data
    if (product.keyBenefits) {
      for (const b of product.keyBenefits) {
        if (!benefits.some(existing => existing.toLowerCase().includes(b.toLowerCase().substring(0, 20)))) {
          benefits.push(b);
        }
      }
    }

    return benefits.slice(0, 4);
  }

  private generateConsiderations(product: any): string[] {
    const considerations: string[] = [];

    // New surrender period
    if (product.surrenderSchedule?.years) {
      considerations.push(`New ${product.surrenderSchedule.years}-year surrender period begins`);
    }

    // 1035 exchange
    considerations.push('Requires 1035 exchange paperwork');

    // State replacement forms
    considerations.push('State replacement forms and review period');

    // Client acknowledgment
    considerations.push('Client must acknowledge new terms and conditions');

    // Minimum premium
    if (product.minimumPremium && product.minimumPremium > 25000) {
      considerations.push(`Minimum premium requirement: $${product.minimumPremium.toLocaleString()}`);
    }

    return considerations.slice(0, 4);
  }

  private generateOptionTitle(product: any, capRate: number): string {
    const productType = product.productType === 'MYGA' || product.productType === 'Fixed'
      ? 'MYGA' : product.productType;
    let title = `1035 exchange to ${product.carrier} ${product.productName} ${productType} at ${capRate.toFixed(2)}%`;
    if (product.bonusRate) {
      title += ` with ${product.bonusRate}% premium bonus`;
    }
    return title;
  }

  getRenewalOption(): Alternative {
    const currentRate = this.policy.projectedRenewalRate || this.policy.currentCapRate || 0;
    return {
      productId: 'RENEWAL',
      carrier: this.policy.carrier,
      productName: `${this.policy.carrier} ${this.policy.productType}`,
      productType: this.policy.productType,
      capRate: currentRate,
      annualFee: this.policy.annualFee || 0,
      riderFee: this.policy.riderFee || 0,
      totalCost: 0,
      incomeRider: this.policy.riders?.includes('Income') || false,
      suitabilityScore: 0,
      highlights: [],
      keyBenefits: [
        'No new paperwork or underwriting',
        'Maintains existing carrier relationship',
        'Surrender period already expired or minimal remaining'
      ],
      considerations: [
        `Significant rate drop to guaranteed minimum ${currentRate}%`,
        `Missing opportunity to capture higher market rates`,
        'Lower returns for client over policy term'
      ],
      optionType: 'renewal',
      optionTitle: `Continue with ${this.policy.carrier} at renewal rate of ${currentRate}%`,
      hasLicense: true,
      hasAppointment: true,
      hasTraining: true,
      canSell: true,
      complianceNotes: null
    };
  }

  onSelectOption(alternativeId: string): void {
    this.selectedAlternativeId.set(alternativeId);
    this.documentationConfirmed.set(false);
    this.generatingDocumentation.set(true);
    this.documentationSummary.set('');

    // Find the selected alternative
    const selected = alternativeId === 'renewal'
      ? this.getRenewalOption()
      : this.alternatives().find(a => a.productId === alternativeId);

    if (selected) {
      this.chatService.updateContext({
        viewingAlternative: selected,
        interactionType: 'reviewing-product'
      });
    }

    // Simulate AI generation delay
    setTimeout(() => {
      this.documentationSummary.set(this.generateDocumentationSummary(alternativeId));
      this.generatingDocumentation.set(false);
    }, 1200);
  }

  private generateDocumentationSummary(alternativeId: string): string {
    const clientName = `${this.client.firstName} ${this.client.lastName}`;
    const riskTolerance = this.client.suitability?.riskTolerance || 'moderate';
    const horizon = this.client.suitability?.investmentHorizon || 'long-term';
    const objective = this.client.suitability?.primaryObjective || 'growth with income';
    const experience = this.client.suitability?.investmentExperience || 5;
    const liquidity = this.client.suitability?.liquidityImportance || 'moderate';

    if (alternativeId === 'renewal') {
      return `Based on comprehensive suitability analysis, the renewal of ${clientName}'s existing ${this.policy.carrier} ${this.policy.productType} policy aligns with the client's ${riskTolerance} risk tolerance and ${horizon} investment horizon. ` +
        `Continuing the current policy maintains established guarantees and avoids new surrender periods. ` +
        `However, the projected renewal rate of ${(this.policy.projectedRenewalRate || this.policy.currentCapRate || 0).toFixed(2)}% represents a reduction from the current cap rate, ` +
        `which may not optimally serve the client's ${objective} objective. ` +
        `Client demonstrates suitable investment experience (${experience}/10) and confirmed understanding of all product features and limitations.`;
    }

    const alt = this.alternatives().find(a => a.productId === alternativeId);
    if (!alt) return '';

    return `Based on comprehensive suitability analysis, this annuity recommendation aligns with ${clientName}'s ${riskTolerance} risk tolerance and ${horizon} investment horizon. ` +
      `The ${alt.carrier} ${alt.productName} provides ${alt.capRate.toFixed(2)}% cap rate${alt.keyBenefits.find(b => b.includes('bonus')) ? ' with premium bonus' : ''}, ` +
      `offering appropriate guarantees while maintaining flexibility for ${liquidity} liquidity needs. ` +
      `The 1035 exchange from ${this.policy.carrier} ${this.policy.productType} to ${alt.productName} results in a rate improvement of ${(alt.capRate - (this.policy.currentCapRate || 0)).toFixed(2)}% ` +
      `and enhanced product features suited to the client's ${objective} objective. ` +
      `Client demonstrates suitable investment experience (${experience}/10) and confirmed understanding of all product features and limitations.`;
  }

  onConfirmDocumentation(): void {
    this.documentationConfirmed.set(true);
  }

  onContinue(): void {
    const selectedId = this.selectedAlternativeId();
    if (!selectedId) return;

    const selected = selectedId === 'renewal'
      ? this.getRenewalOption()
      : this.alternatives().find(a => a.productId === selectedId);

    if (!selected) return;

    this.actionComplete.emit({
      action: selectedId === 'renewal' ? 'continue_renewal' : 'initiate_replacement',
      alertId: this.alert.alertId,
      policyId: this.policy.policyId,
      selectedProduct: {
        productId: selected.productId,
        productName: selected.productName,
        carrier: selected.carrier,
        suitabilityScore: selected.suitabilityScore
      },
      documentation: {
        summary: this.documentationSummary(),
        confirmedAt: new Date().toISOString()
      }
    });

    console.log('Continuing with selected option:', {
      currentPolicy: this.policy.policyId,
      selectedProduct: selected.productName,
      carrier: selected.carrier,
      matchScore: selected.suitabilityScore,
      documentationConfirmed: true
    });
  }

  getSelectedAlternative(): Alternative | null {
    const id = this.selectedAlternativeId();
    if (!id) return null;
    if (id === 'renewal') return this.getRenewalOption();
    return this.alternatives().find(a => a.productId === id) || null;
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
    const currentCap = this.policy.currentCapRate || this.policy.projectedRenewalRate || 1.5;
    return [
      {
        productId: 'ALT-001',
        carrier: 'Great American',
        productName: 'FlexGrowth Plus',
        productType: 'Fixed Index Annuity',
        capRate: 4.25,
        annualFee: 0,
        riderFee: 0.95,
        totalCost: 950,
        incomeRider: true,
        suitabilityScore: 92,
        highlights: [
          `Higher cap rate (4.25% vs current ${currentCap}%)`,
          'Income rider with 7% rollup',
          'Best-in-class features for income'
        ],
        keyBenefits: [
          `Rate improvement: ${(4.25 - currentCap).toFixed(1)}% increase (${currentCap}% → 4.25%)`,
          '3.0% premium bonus on entire account value',
          'Enhanced features including death benefit protection',
          'Strong carrier rating (Great American)'
        ],
        considerations: [
          'New 7-year surrender period begins',
          'Requires 1035 exchange paperwork',
          'State replacement forms and review period',
          'Client must acknowledge new terms and conditions'
        ],
        optionType: 'replacement',
        optionTitle: `1035 exchange to Great American FlexGrowth Plus MYGA at 4.25% with 3.0% premium bonus`,
        hasLicense: true,
        hasAppointment: true,
        hasTraining: true,
        canSell: true,
        complianceNotes: null
      },
      {
        productId: 'ALT-002',
        carrier: 'North American',
        productName: 'Secure Income Pro',
        productType: 'Fixed Index Annuity',
        capRate: 3.95,
        annualFee: 0,
        riderFee: 1.00,
        totalCost: 1000,
        incomeRider: true,
        suitabilityScore: 88,
        highlights: [
          `Higher cap rate (3.95% vs current ${currentCap}%)`,
          'Downside protection with upside potential',
          'Guaranteed lifetime income available'
        ],
        keyBenefits: [
          `Rate improvement: ${(3.95 - currentCap).toFixed(1)}% increase (${currentCap}% → 3.95%)`,
          'Enhanced features including death benefit protection',
          'Strong carrier rating (North American)'
        ],
        considerations: [
          'New 5-year surrender period begins',
          'Requires 1035 exchange paperwork',
          'State replacement forms and review period',
          'Client must acknowledge new terms and conditions'
        ],
        optionType: 'replacement',
        optionTitle: `1035 exchange to North American Secure Income Pro MYGA at 3.95%`,
        hasLicense: true,
        hasAppointment: true,
        hasTraining: true,
        canSell: true,
        complianceNotes: null
      },
      {
        productId: 'ALT-003',
        carrier: 'American Equity',
        productName: 'Premium Shield',
        productType: 'Fixed Index Annuity',
        capRate: 4.10,
        annualFee: 0,
        riderFee: 0.85,
        totalCost: 850,
        incomeRider: true,
        suitabilityScore: 85,
        highlights: [
          `Competitive cap rate (4.10%)`,
          'Lower fees than current policy',
          'Flexible income options'
        ],
        keyBenefits: [
          `Rate improvement: ${(4.10 - currentCap).toFixed(1)}% increase (${currentCap}% → 4.10%)`,
          '2.0% premium bonus on entire account value',
          'Enhanced features including death benefit protection',
          'Strong carrier rating (American Equity)'
        ],
        considerations: [
          'New 6-year surrender period begins',
          'Requires 1035 exchange paperwork',
          'State replacement forms and review period',
          'Client must acknowledge new terms and conditions'
        ],
        optionType: 'replacement',
        optionTitle: `1035 exchange to American Equity Premium Shield MYGA at 4.10% with 2.0% premium bonus`,
        hasLicense: true,
        hasAppointment: true,
        hasTraining: false,
        canSell: false,
        complianceNotes: 'Product training required. Contact compliance@yourfirm.com to request American Equity Premium Shield certification.'
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

  async exportToPDF(): Promise<void> {
    this.exportingPDF.set(true);
    
    try {
      // Create a new PDF document
      const pdf = new jsPDF('p', 'mm', 'a4');
      const pageWidth = pdf.internal.pageSize.getWidth();
      const pageHeight = pdf.internal.pageSize.getHeight();
      const margin = 15;
      
      // Add header with logo and title
      pdf.setFillColor(25, 118, 210); // Material Blue
      pdf.rect(0, 0, pageWidth, 35, 'F');
      
      pdf.setTextColor(255, 255, 255);
      pdf.setFontSize(22);
      pdf.setFont('helvetica', 'bold');
      pdf.text('Replacement Opportunity Analysis', margin, 20);
      
      pdf.setFontSize(10);
      pdf.setFont('helvetica', 'normal');
      pdf.text(`Generated on ${new Date().toLocaleDateString('en-US', { 
        year: 'numeric', month: 'long', day: 'numeric', 
        hour: '2-digit', minute: '2-digit' 
      })}`, margin, 28);
      
      // Reset text color for body
      pdf.setTextColor(0, 0, 0);
      let yPos = 45;
      
      // Client & Policy Information
      pdf.setFontSize(14);
      pdf.setFont('helvetica', 'bold');
      pdf.text('Client & Policy Information', margin, yPos);
      yPos += 8;
      
      pdf.setFontSize(10);
      pdf.setFont('helvetica', 'normal');
      pdf.text(`Client: ${this.client.firstName} ${this.client.lastName} (${this.client.clientAccountNumber})`, margin, yPos);
      yPos += 6;
      pdf.text(`Policy: ${this.policy.policyId} - ${this.policy.carrier} ${this.policy.productName || this.policy.productType}`, margin, yPos);
      yPos += 6;
      pdf.text(`Account Value: ${this.formatCurrency(this.policy.accountValue || 0)}`, margin, yPos);
      yPos += 10;
      
      // Alert Details
      pdf.setFontSize(14);
      pdf.setFont('helvetica', 'bold');
      pdf.text('Alert Details', margin, yPos);
      yPos += 8;
      
      pdf.setFontSize(10);
      pdf.setFont('helvetica', 'normal');
      pdf.text(`Alert Type: ${this.alert.title}`, margin, yPos);
      yPos += 6;
      
      // Reasons
      const reasons = this.alert.reasons || [];
      reasons.forEach((reason, idx) => {
        if (yPos > pageHeight - 30) {
          pdf.addPage();
          yPos = margin;
        }
        pdf.text(`  ${idx + 1}. ${reason}`, margin, yPos);
        yPos += 6;
      });
      yPos += 5;
      
      // Suitability Profile
      if (this.suitabilityVerified()) {
        pdf.setFontSize(14);
        pdf.setFont('helvetica', 'bold');
        pdf.text('Suitability Profile (Verified)', margin, yPos);
        yPos += 8;
        
        pdf.setFontSize(10);
        pdf.setFont('helvetica', 'normal');
        const suitability = this.client.suitability;
        if (suitability) {
          pdf.text(`Risk Tolerance: ${suitability.riskTolerance}`, margin, yPos);
          yPos += 6;
          pdf.text(`Primary Objective: ${suitability.primaryObjective}`, margin, yPos);
          yPos += 6;
          pdf.text(`Income Needs: ${suitability.currentIncomeNeed}`, margin, yPos);
          yPos += 6;
          pdf.text(`Liquidity Importance: ${suitability.liquidityImportance}`, margin, yPos);
          yPos += 10;
        }
      }
      
      // Capture comparison table as image
      if (this.currentStep() === 2 && this.alternatives().length > 0) {
        // Add new page in LANDSCAPE for comparison table
        pdf.addPage('a4', 'landscape');
        const landscapeWidth = pdf.internal.pageSize.getWidth();
        const landscapeHeight = pdf.internal.pageSize.getHeight();
        yPos = margin;
        
        pdf.setFontSize(16);
        pdf.setFont('helvetica', 'bold');
        pdf.text('Market Alternatives Comparison', margin, yPos);
        yPos += 12;
        
        const comparisonTable = this.elementRef.nativeElement.querySelector('.comparison-table-wrapper');
        if (comparisonTable) {
          try {
            const canvas = await html2canvas(comparisonTable, {
              scale: 3,
              backgroundColor: '#ffffff',
              logging: false,
              width: comparisonTable.scrollWidth,
              windowWidth: comparisonTable.scrollWidth
            });
            
            const imgData = canvas.toDataURL('image/png');
            const imgWidth = landscapeWidth - (2 * margin);
            const imgHeight = (canvas.height * imgWidth) / canvas.width;
            
            // If too tall, scale to fit page height
            let finalWidth = imgWidth;
            let finalHeight = imgHeight;
            if (imgHeight > landscapeHeight - yPos - margin) {
              finalHeight = landscapeHeight - yPos - margin;
              finalWidth = (canvas.width * finalHeight) / canvas.height;
            }
            
            pdf.addImage(imgData, 'PNG', margin, yPos, finalWidth, finalHeight, undefined, 'FAST');
            yPos += finalHeight + 10;
          } catch (error) {
            console.error('Error capturing comparison table:', error);
          }
        }
        
        // Back to portrait for charts
        pdf.addPage('a4', 'portrait');
        yPos = margin;
        
        // Capture performance charts with higher quality
        const performanceSection = this.elementRef.nativeElement.querySelector('.performance-section');
        if (performanceSection) {
          try {
            pdf.setFontSize(16);
            pdf.setFont('helvetica', 'bold');
            pdf.text('Performance & Rates Analysis', margin, yPos);
            yPos += 12;
            
            const canvas = await html2canvas(performanceSection, {
              scale: 2.5,
              backgroundColor: '#ffffff',
              logging: false,
              width: performanceSection.scrollWidth,
              windowWidth: performanceSection.scrollWidth + 100
            });
            
            const imgData = canvas.toDataURL('image/png', 0.95);
            const imgWidth = pageWidth - (2 * margin);
            const imgHeight = (canvas.height * imgWidth) / canvas.width;
            
            // Split into multiple pages if needed
            let heightLeft = imgHeight;
            let position = yPos;
            
            pdf.addImage(imgData, 'PNG', margin, position, imgWidth, imgHeight);
            heightLeft -= (pageHeight - position - margin);
            
            while (heightLeft > 0) {
              position = heightLeft - imgHeight + margin;
              pdf.addPage();
              pdf.addImage(imgData, 'PNG', margin, position, imgWidth, imgHeight);
              heightLeft -= (pageHeight - margin);
            }
          } catch (error) {
            console.error('Error capturing performance charts:', error);
          }
        }
        
        // Alternative Products Summary
        pdf.addPage();
        yPos = margin;
        
        pdf.setFontSize(16);
        pdf.setFont('helvetica', 'bold');
        pdf.setTextColor(0, 0, 0);
        pdf.text('Alternative Products Summary', margin, yPos);
        yPos += 15;
        
        this.alternatives().forEach((alt, index) => {
          if (yPos > pageHeight - 70) {
            pdf.addPage();
            yPos = margin;
          }
          
          // Product number badge
          pdf.setFillColor(25, 118, 210); // Blue
          pdf.circle(margin + 4, yPos - 1, 4, 'F');
          pdf.setTextColor(255, 255, 255);
          pdf.setFontSize(11);
          pdf.setFont('helvetica', 'bold');
          pdf.text(`${index + 1}`, margin + 4, yPos + 1, { align: 'center' });
          
          // Product name
          pdf.setTextColor(26, 26, 26);
          pdf.setFontSize(13);
          pdf.setFont('helvetica', 'bold');
          pdf.text(alt.productName, margin + 12, yPos);
          yPos += 7;
          
          // Carrier info
          pdf.setFontSize(10);
          pdf.setFont('helvetica', 'normal');
          pdf.setTextColor(80, 80, 80);
          pdf.text(`Carrier: ${alt.carrier}`, margin + 12, yPos);
          yPos += 6;
          
          // Cap Rate and Suitability
          pdf.setTextColor(0, 0, 0);
          pdf.text(`Cap Rate: `, margin + 12, yPos);
          pdf.setFont('helvetica', 'bold');
          pdf.setTextColor(25, 118, 210);
          pdf.text(this.formatPercentage(alt.capRate), margin + 32, yPos);
          pdf.setFont('helvetica', 'normal');
          pdf.setTextColor(0, 0, 0);
          pdf.text(` | Suitability Match: `, margin + 48, yPos);
          pdf.setFont('helvetica', 'bold');
          const scoreColor = alt.suitabilityScore >= 90 ? [76, 175, 80] : alt.suitabilityScore >= 85 ? [255, 152, 0] : [100, 100, 100];
          pdf.setTextColor(scoreColor[0], scoreColor[1], scoreColor[2]);
          pdf.text(`${alt.suitabilityScore}%`, margin + 86, yPos);
          yPos += 8;
          
          // Compliance status badge
          pdf.setFont('helvetica', 'bold');
          pdf.setFontSize(9);
          if (alt.canSell === false) {
            // Orange warning box
            pdf.setFillColor(255, 243, 224);
            pdf.setDrawColor(255, 152, 0);
            pdf.rect(margin + 12, yPos - 4, 70, 6, 'FD');
            pdf.setTextColor(230, 81, 0);
            pdf.text('⚠ CANNOT SELL', margin + 15, yPos);
            yPos += 7;
            
            // Compliance notes
            if (alt.complianceNotes) {
              pdf.setFillColor(255, 248, 240);
              const notesHeight = 6 + Math.ceil(alt.complianceNotes.length / 80) * 5;
              pdf.rect(margin + 12, yPos - 3, pageWidth - 2 * margin - 12, notesHeight, 'F');
              
              pdf.setFont('helvetica', 'italic');
              pdf.setFontSize(9);
              pdf.setTextColor(100, 50, 0);
              const noteLines = pdf.splitTextToSize(alt.complianceNotes, pageWidth - 2 * margin - 20);
              pdf.text(noteLines, margin + 15, yPos);
              yPos += noteLines.length * 5 + 4;
            }
          } else {
            // Green success box
            pdf.setFillColor(232, 245, 233);
            pdf.setDrawColor(76, 175, 80);
            pdf.rect(margin + 12, yPos - 4, 40, 6, 'FD');
            pdf.setTextColor(56, 142, 60);
            pdf.text('✓ CAN SELL', margin + 15, yPos);
            yPos += 8;
          }
          
          pdf.setTextColor(0, 0, 0);
          yPos += 2;
          
          // Key Benefits section
          if (alt.highlights && alt.highlights.length > 0) {
            pdf.setFont('helvetica', 'bold');
            pdf.setFontSize(10);
            pdf.setTextColor(40, 40, 40);
            pdf.text('Key Benefits:', margin + 12, yPos);
            yPos += 6;
            
            pdf.setFont('helvetica', 'normal');
            pdf.setFontSize(9);
            pdf.setTextColor(0, 0, 0);
            alt.highlights.forEach((highlight, idx) => {
              if (yPos > pageHeight - 20) {
                pdf.addPage();
                yPos = margin;
              }
              // Checkmark bullet
              pdf.setTextColor(76, 175, 80);
              pdf.setFont('helvetica', 'bold');
              pdf.text('✓', margin + 14, yPos);
              
              pdf.setFont('helvetica', 'normal');
              pdf.setTextColor(0, 0, 0);
              const wrappedText = pdf.splitTextToSize(highlight, pageWidth - 2 * margin - 25);
              pdf.text(wrappedText, margin + 20, yPos);
              yPos += Math.max(wrappedText.length * 5, 5);
            });
          }
          
          // Separator line between products
          yPos += 5;
          pdf.setDrawColor(220, 220, 220);
          pdf.setLineWidth(0.5);
          pdf.line(margin + 10, yPos, pageWidth - margin - 10, yPos);
          yPos += 10;
        });
      }
      
      // Footer on last page
      const lastPageNum = pdf.getNumberOfPages();
      for (let i = 1; i <= lastPageNum; i++) {
        pdf.setPage(i);
        pdf.setFontSize(8);
        pdf.setTextColor(128, 128, 128);
        pdf.text(
          `Page ${i} of ${lastPageNum}`,
          pageWidth / 2,
          pageHeight - 10,
          { align: 'center' }
        );
        pdf.text(
          'Confidential - For Advisor Review Only',
          pageWidth - margin,
          pageHeight - 10,
          { align: 'right' }
        );
      }
      
      // Save the PDF
      const fileName = `Replacement_Analysis_${this.policy.policyId}_${new Date().getTime()}.pdf`;
      pdf.save(fileName);
      
    } catch (error) {
      console.error('Error generating PDF:', error);
      alert('Error generating PDF. Please try again.');
    } finally {
      this.exportingPDF.set(false);
    }
  }
}
