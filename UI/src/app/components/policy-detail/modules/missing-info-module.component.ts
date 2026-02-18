import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatDividerModule } from '@angular/material/divider';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatChipsModule } from '@angular/material/chips';
import { Alert } from '../../../models/alert.model';
import { Policy, Beneficiary } from '../../../models/policy.model';
import { Client } from '../../../models/client.model';
import { ApiService } from '../../../services/api.service';

interface MissingField {
  field: string;
  label: string;
  status: string;
  priority: string;
}

@Component({
  selector: 'app-missing-info-module',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatDividerModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatTooltipModule,
    MatProgressSpinnerModule,
    MatChipsModule
  ],
  templateUrl: './missing-info-module.component.html',
  styleUrls: ['./missing-info-module.component.scss']
})
export class MissingInfoModuleComponent implements OnInit {
  @Input() alert!: Alert;
  @Input() policy!: Policy;
  @Input() client!: Client;
  @Output() actionComplete = new EventEmitter<any>();

  updateForm!: FormGroup;
  isSubmitting = false;
  submitSuccess = false;
  submitError: string | null = null;

  relationshipOptions = [
    'Spouse',
    'Child',
    'Parent',
    'Sibling',
    'Trust',
    'Estate',
    'Other'
  ];

  constructor(
    private fb: FormBuilder,
    private apiService: ApiService
  ) {}

  ngOnInit(): void {
    this.initializeForm();
  }

  initializeForm(): void {
    const nonFinancial = this.policy.nonFinancialData;
    const primaryBen = nonFinancial?.primaryBeneficiary;
    const contingentBen = nonFinancial?.contingentBeneficiary;
    const taxWith = nonFinancial?.taxWithholding;
    const contactInfo = nonFinancial?.contactInfo;

    // Pre-fill from policy first, then fallback to client profile data
    this.updateForm = this.fb.group({
      primaryBeneficiary: this.fb.group({
        name: [primaryBen?.name || '', Validators.required],
        relationship: [primaryBen?.relationship || '', Validators.required],
        ssn: [primaryBen?.ssn || '', Validators.pattern(/^\d{3}-\d{2}-\d{4}$/)],
        dateOfBirth: [primaryBen?.dateOfBirth || ''],
        allocationPercent: [primaryBen?.allocationPercent || 100, [Validators.required, Validators.min(0), Validators.max(100)]]
      }),
      contingentBeneficiary: this.fb.group({
        name: [contingentBen?.name || ''],
        relationship: [contingentBen?.relationship || ''],
        ssn: [contingentBen?.ssn || '', Validators.pattern(/^\d{3}-\d{2}-\d{4}$/)],
        dateOfBirth: [contingentBen?.dateOfBirth || ''],
        allocationPercent: [contingentBen?.allocationPercent || 0, [Validators.min(0), Validators.max(100)]]
      }),
      taxWithholding: this.fb.group({
        federal: [taxWith?.federal ?? 0, [Validators.min(0), Validators.max(100)]],
        state: [taxWith?.state ?? 0, [Validators.min(0), Validators.max(100)]]
      }),
      // Contact info - pull from policy, fallback to client profile
      contactInfo: this.fb.group({
        email: [contactInfo?.email || this.client.email || ''],
        phone: [contactInfo?.phone || this.client.phone || ''],
        address: [contactInfo?.address || this.getClientAddress()]
      }),
      specialInstructions: [nonFinancial?.specialInstructions || '']
    });
  }

  get accountProfileData() {
    return {
      ownerName: this.policy.nonFinancialData?.ownerName || this.client.name || '',
      ssn: this.policy.nonFinancialData?.ownerSSN || '***-**-****',
      address: this.policy.nonFinancialData?.contactInfo?.address || this.getClientAddress(),
      email: this.policy.nonFinancialData?.contactInfo?.email || this.client.email || '',
      phone: this.policy.nonFinancialData?.contactInfo?.phone || this.client.phone || ''
    };
  }

  getClientAddress(): string {
    // In a real app, this would come from client profile
    return `123 Main St, ${this.client.suitability?.state || 'State'}, 12345`;
  }

  getMissingFields(): MissingField[] {
    const fields: MissingField[] = [];
    const nonFinancial = this.policy.nonFinancialData;
    const contactInfo = nonFinancial?.contactInfo;

    // Check PRIMARY BENEFICIARY - be specific about what's missing
    if (!nonFinancial?.primaryBeneficiary) {
      fields.push({
        field: 'primaryBeneficiary',
        label: 'Primary Beneficiary',
        status: 'Not Designated',
        priority: 'CRITICAL'
      });
    } else {
      const primaryBen = nonFinancial.primaryBeneficiary;
      if (!primaryBen.ssn) {
        fields.push({
          field: 'primaryBeneficiarySSN',
          label: 'Primary Beneficiary SSN',
          status: 'Missing',
          priority: 'HIGH'
        });
      }
      if (!primaryBen.dateOfBirth) {
        fields.push({
          field: 'primaryBeneficiaryDOB',
          label: 'Primary Beneficiary Date of Birth',
          status: 'Missing',
          priority: 'HIGH'
        });
      }
    }

    // Check TAX WITHHOLDING
    if (!nonFinancial?.taxWithholding || (nonFinancial.taxWithholding.federal === null && nonFinancial.taxWithholding.state === null)) {
      fields.push({
        field: 'taxWithholding',
        label: 'Tax Withholding Elections',
        status: 'Not Selected',
        priority: 'HIGH'
      });
    }

    // Check CONTACT INFO - specific fields
    if (!contactInfo?.email && !this.client.email) {
      fields.push({
        field: 'email',
        label: 'Owner Email Address',
        status: 'Missing',
        priority: 'MEDIUM'
      });
    }

    if (!contactInfo?.phone && !this.client.phone) {
      fields.push({
        field: 'phone',
        label: 'Owner Phone Number',
        status: 'Missing',
        priority: 'MEDIUM'
      });
    }

    if (!contactInfo?.address) {
      fields.push({
        field: 'address',
        label: 'Owner Mailing Address',
        status: 'Missing',
        priority: 'MEDIUM'
      });
    }

    return fields;
  }

  getLastUpdatedText(): string {
    const lastUpdated = this.policy.nonFinancialData?.lastUpdated;
    if (!lastUpdated) {
      return 'Never updated';
    }

    const date = new Date(lastUpdated);
    const now = new Date();
    const years = (now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24 * 365);

    if (years > 5) {
      return `Last updated ${Math.floor(years)} years ago (${date.toLocaleDateString()})`;
    } else if (years > 1) {
      return `Last updated ${Math.floor(years)} year(s) ago (${date.toLocaleDateString()})`;
    } else {
      return `Last updated ${date.toLocaleDateString()}`;
    }
  }

  validateAllocations(): boolean {
    const primaryAlloc = this.updateForm.get('primaryBeneficiary.allocationPercent')?.value || 0;
    const contingentAlloc = this.updateForm.get('contingentBeneficiary.allocationPercent')?.value || 0;
    const total = primaryAlloc + contingentAlloc;

    // Allow 100% if only primary, or require total to equal 100 if contingent is present
    const contingentName = this.updateForm.get('contingentBeneficiary.name')?.value;
    if (!contingentName) {
      return primaryAlloc === 100;
    }

    return total === 100;
  }

  async onSubmit(): Promise<void> {
    if (this.updateForm.invalid || !this.validateAllocations()) {
      this.submitError = 'Please fill in all required fields and ensure allocations total 100%';
      return;
    }

    this.isSubmitting = true;
    this.submitError = null;

    // Simulate submission delay for demo purposes (UI capabilities only)
    setTimeout(() => {
      this.submitSuccess = true;
      this.isSubmitting = false;

      // Log the form data that would be submitted (for demo verification)
      console.log('Policy Update Data (Demo Mode):', {
        policyId: this.policy.policyId,
        alertId: this.alert.alertId,
        formData: this.updateForm.value
      });

      // Emit success event
      setTimeout(() => {
        this.actionComplete.emit({
          action: 'update_complete',
          alertId: this.alert.alertId,
          policyId: this.policy.policyId,
          demo: true
        });
      }, 2000);
    }, 1500); // Simulate processing time
  }

  onSaveDraft(): void {
    // In a full implementation, this would save to local storage or backend
    console.log('Saving draft:', this.updateForm.value);
  }

  getPriorityIcon(priority: string): string {
    switch (priority) {
      case 'CRITICAL': return 'error';
      case 'HIGH': return 'warning';
      case 'MEDIUM': return 'info';
      default: return 'info';
    }
  }

  getPriorityColor(priority: string): string {
    switch (priority) {
      case 'CRITICAL': return 'warn';
      case 'HIGH': return 'accent';
      case 'MEDIUM': return 'primary';
      default: return '';
    }
  }
}
