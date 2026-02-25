import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Policy, PolicyOverview } from '../models/policy.model';
import { Client } from '../models/client.model';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private readonly API_URL = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  // Policy endpoints
  getPolicies(): Observable<Policy[]> {
    return this.http.get<Policy[]>(`${this.API_URL}/policies`);
  }

  getPolicyById(policyId: string): Observable<PolicyOverview> {
    return this.http.get<PolicyOverview>(`${this.API_URL}/policies/${policyId}`);
  }

  updatePolicyNonFinancialData(policyId: string, data: any): Observable<any> {
    return this.http.post<any>(`${this.API_URL}/policies/${policyId}/update-non-financial`, data);
  }

  // Client endpoints
  getClientById(clientId: string): Observable<Client> {
    return this.http.get<Client>(`${this.API_URL}/clients/${clientId}`);
  }

  getClientByAccountNumber(accountNumber: string): Observable<Client> {
    return this.http.get<Client>(`${this.API_URL}/clients/${accountNumber}`);
  }

  updateClientSuitability(accountNumber: string, suitability: any): Observable<Client> {
    return this.http.patch<Client>(`${this.API_URL}/clients/${accountNumber}/suitability`, suitability);
  }

  // Product endpoints
  getAlternativeProducts(policyId: string, suitabilityProfile: any): Observable<any[]> {
    return this.http.post<any[]>(`${this.API_URL}/products/alternatives`, {
      policyId,
      suitabilityProfile
    });
  }

  getPolicyAlternatives(policyId: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.API_URL}/policies/${policyId}/alternatives`);
  }

  // AI endpoints
  sendAiMessage(context: any, message: string): Observable<any> {
    return this.http.post<any>(`${this.API_URL}/ai/chat`, {
      ...context,
      userMessage: message
    });
  }

  // Acquisition alerts (client-level portfolio opportunities)
  getClientAcquisitionAlerts(clientAccountNumber: string): Observable<any> {
    return this.http.get<any>(`${this.API_URL}/clients/${clientAccountNumber}/acquisition-alerts`);
  }

  getAllAcquisitionAlerts(): Observable<any> {
    return this.http.get<any>(`${this.API_URL}/acquisition-alerts`);
  }
}
