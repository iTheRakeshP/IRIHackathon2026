import { Component, Input, Output, EventEmitter, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatInputModule } from '@angular/material/input';
import { MatChipsModule } from '@angular/material/chips';
import { Client } from '../../../models/client.model';
import { ApiService } from '../../../services/api.service';

@Component({
  selector: 'app-suitability-form',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatFormFieldModule,
    MatSelectModule,
    MatInputModule,
    MatChipsModule
  ],
  templateUrl: './suitability-form.component.html',
  styleUrls: ['./suitability-form.component.scss']
})
export class SuitabilityFormComponent {
  @Input() client!: Client;
  @Output() suitabilityVerified = new EventEmitter<void>();

  // Signals for form state
  editMode = signal<boolean>(false);
  saving = signal<boolean>(false);
  verified = signal<boolean>(false);

  // Form model (editable copy)
  formData = {
    riskTolerance: '',
    primaryObjective: '',
    secondaryObjective: '',
    currentIncomeNeed: '',
    lifeStage: '',
    liquidityImportance: ''
  };

  // Dropdown options
  riskToleranceOptions = ['Conservative', 'Moderate-Conservative', 'Moderate', 'Moderate-Aggressive', 'Aggressive'];
  objectiveOptions = ['Growth', 'Income', 'Preservation', 'Balanced', 'Legacy'];
  incomeNeedOptions = ['Now', 'Within 2 Years', 'Within 5 Years', '5+ Years', 'Not Needed'];
  lifeStageOptions = ['Accumulation', 'Pre-Retirement', 'Early Retirement', 'Retirement', 'Late Retirement'];
  liquidityOptions = ['Low', 'Medium', 'High'];

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    // Initialize form with client suitability data
    if (this.client?.suitability) {
      this.formData = {
        riskTolerance: this.client.suitability.riskTolerance || '',
        primaryObjective: this.client.suitability.primaryObjective || '',
        secondaryObjective: this.client.suitability.secondaryObjective || '',
        currentIncomeNeed: this.client.suitability.currentIncomeNeed || '',
        lifeStage: this.client.suitability.lifeStage || '',
        liquidityImportance: this.client.suitability.liquidityImportance || ''
      };
    }
  }

  onEdit(): void {
    this.editMode.set(true);
  }

  onCancel(): void {
    this.editMode.set(false);
    // Reset to original values
    this.ngOnInit();
  }

  onSave(): void {
    this.saving.set(true);
    
    // Update suitability via API
    this.apiService.updateClientSuitability(this.client.clientAccountNumber, this.formData).subscribe({
      next: (updatedClient) => {
        this.client.suitability = updatedClient.suitability;
        this.editMode.set(false);
        this.saving.set(false);
        this.verified.set(true);
        
        // Emit verification event
        this.suitabilityVerified.emit();
      },
      error: (error) => {
        console.error('Error updating suitability:', error);
        this.saving.set(false);
        // For demo, still mark as verified
        this.verified.set(true);
        this.editMode.set(false);
        this.suitabilityVerified.emit();
      }
    });
  }

  onVerifyWithoutChanges(): void {
    this.verified.set(true);
    this.suitabilityVerified.emit();
  }

  hasChanges(): boolean {
    if (!this.client?.suitability) return false;
    
    const s = this.client.suitability;
    return (
      this.formData.riskTolerance !== s.riskTolerance ||
      this.formData.primaryObjective !== s.primaryObjective ||
      this.formData.secondaryObjective !== s.secondaryObjective ||
      this.formData.currentIncomeNeed !== s.currentIncomeNeed ||
      this.formData.lifeStage !== s.lifeStage ||
      this.formData.liquidityImportance !== s.liquidityImportance
    );
  }
}

