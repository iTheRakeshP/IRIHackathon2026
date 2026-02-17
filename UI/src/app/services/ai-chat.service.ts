import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp?: Date;
}

export interface ChatContext {
  policyId?: string;
  clientAccountNumber?: string;
  alertType?: string;
  alertId?: string;
  policy?: any;
  client?: any;
  alternatives?: any[];
  // Dynamic context for suggestions
  currentStep?: string; // e.g., 'why-flagged', 'suitability', 'alternatives'
  viewingAlternative?: any; // Specific alternative being viewed
  interactionType?: string; // e.g., 'viewing-comparison', 'reviewing-product'
}

export interface ChatRequest {
  message: string;
  context?: any;
  conversation_history?: ChatMessage[];
  temperature?: number;
}

export interface ChatResponse {
  message: string;
  role: string;
  timestamp?: string;
}

@Injectable({
  providedIn: 'root'
})
export class AiChatService {
  private readonly API_URL = 'http://localhost:8000/api';
  
  // Chat state
  messages = signal<ChatMessage[]>([]);
  context = signal<ChatContext>({});
  isOpen = signal<boolean>(false);
  isLoading = signal<boolean>(false);

  constructor(private http: HttpClient) {}

  openChat(context: ChatContext): void {
    this.context.set(context);
    this.isOpen.set(true);
    
    // Add welcome message if chat is empty
    if (this.messages().length === 0) {
      this.addWelcomeMessage(context);
    }
  }

  updateContext(contextUpdate: Partial<ChatContext>): void {
    // Update context dynamically as user interacts
    this.context.update(current => ({
      ...current,
      ...contextUpdate
    }));
  }

  closeChat(): void {
    this.isOpen.set(false);
  }

  toggleChat(): void {
    this.isOpen.set(!this.isOpen());
  }

  clearChat(): void {
    this.messages.set([]);
  }

  private addWelcomeMessage(context: ChatContext): void {
    const welcomeMsg: ChatMessage = {
      role: 'assistant',
      content: this.getWelcomeMessage(context),
      timestamp: new Date()
    };
    this.messages.set([welcomeMsg]);
  }

  private getWelcomeMessage(context: ChatContext): string {
    if (context.alertType === 'REPLACEMENT') {
      return "👋 Hi! I'm PolicyPilot, your intelligent guide. I can help you analyze this replacement opportunity, compare products, or answer compliance questions. What would you like to know?";
    } else if (context.alertType === 'INCOME_ACTIVATION') {
      return "👋 Hi! I'm PolicyPilot, your intelligent guide. I can help you understand income activation timing and options. What would you like to discuss?";
    } else if (context.alertType === 'SUITABILITY_DRIFT') {
      return "👋 Hi! I'm PolicyPilot, your intelligent guide. I can help you assess suitability changes and recommendations. How can I assist?";
    } else {
      return "👋 Hi! I'm PolicyPilot, your intelligent guide for in-force policy reviews. I can help analyze policies, compare products, and answer compliance questions. What would you like to know?";
    }
  }

  sendMessage(message: string): Observable<ChatResponse> {
    // Add user message immediately
    const userMessage: ChatMessage = {
      role: 'user',
      content: message,
      timestamp: new Date()
    };
    this.messages.update(msgs => [...msgs, userMessage]);
    this.isLoading.set(true);

    // Prepare context for API
    const currentContext = this.context();
    const apiContext = {
      policy_id: currentContext.policyId,
      client_account_number: currentContext.clientAccountNumber,
      alert_type: currentContext.alertType,
      alert_id: currentContext.alertId,
      policy: currentContext.policy,
      client: currentContext.client,
      alternatives: currentContext.alternatives
    };

    // Prepare request
    const request: ChatRequest = {
      message: message,
      context: apiContext,
      conversation_history: this.messages().slice(0, -1), // Exclude the message we just added
      temperature: 0.7
    };

    return this.http.post<ChatResponse>(`${this.API_URL}/ai/chat`, request).pipe(
      tap(response => {
        this.isLoading.set(false);
        // Add assistant response
        const assistantMessage: ChatMessage = {
          role: 'assistant',
          content: response.message,
          timestamp: new Date()
        };
        this.messages.update(msgs => [...msgs, assistantMessage]);
      })
    );
  }

  getQuickActions(alertType: string): string[] {
    const context = this.context();
    
    // Dynamic suggestions based on current interaction
    if (context.currentStep === 'alternatives' && context.alternatives && context.alternatives.length > 0) {
      return [
        'Which alternative is best for this client?',
        'Compare the top 2 alternatives',
        'What are the fee differences?',
        'Explain the cap rate improvements'
      ];
    }
    
    if (context.currentStep === 'suitability') {
      return [
        'What suitability factors are most important?',
        'Has the client profile changed significantly?',
        'What should I update in suitability?',
        'Explain the risk tolerance assessment'
      ];
    }
    
    if (context.currentStep === 'why-flagged') {
      return [
        'Why was this alert triggered?',
        'Is this a high priority alert?',
        'What regulation requires this review?',
        'What data triggered the flag?'
      ];
    }
    
    if (context.viewingAlternative) {
      const alt = context.viewingAlternative;
      return [
        `Why is ${alt.productName} a ${alt.suitabilityScore}% match?`,
        'What are the key benefits of this product?',
        'What are the risks or downsides?',
        'Draft a comparison summary'
      ];
    }
    
    // Default suggestions by alert type
    const actions: { [key: string]: string[] } = {
      'REPLACEMENT': [
        'Explain why this alert was triggered',
        'Compare current policy to alternatives',
        'What are the key differences in fees?',
        'Draft a best-interest summary'
      ],
      'INCOME_ACTIVATION': [
        'When should income be activated?',
        'What are the income options?',
        'Explain the guaranteed vs. variable income',
        'What are tax implications?'
      ],
      'SUITABILITY_DRIFT': [
        'Explain the suitability changes',
        'What actions should I take?',
        'How significant is this drift?',
        'Draft a review summary'
      ]
    };

    return actions[alertType] || [
      'Analyze this policy',
      'What should I review?',
      'Explain compliance requirements'
    ];
  }
}
