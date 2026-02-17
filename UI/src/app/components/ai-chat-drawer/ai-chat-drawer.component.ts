import { Component, OnInit, ViewChild, ElementRef, AfterViewChecked, effect } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatChipsModule } from '@angular/material/chips';
import { MatDividerModule } from '@angular/material/divider';
import { AiChatService, ChatMessage } from '../../services/ai-chat.service';

@Component({
  selector: 'app-ai-chat-drawer',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatIconModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatProgressSpinnerModule,
    MatChipsModule,
    MatDividerModule
  ],
  templateUrl: './ai-chat-drawer.component.html',
  styleUrls: ['./ai-chat-drawer.component.scss']
})
export class AiChatDrawerComponent implements OnInit, AfterViewChecked {
  @ViewChild('messagesContainer') private messagesContainer?: ElementRef;
  
  userInput = '';
  shouldScrollToBottom = false;
  currentSuggestions: string[] = [];

  constructor(public chatService: AiChatService) {
    // Update suggestions when context changes
    effect(() => {
      const context = this.chatService.context();
      this.currentSuggestions = this.chatService.getQuickActions(context.alertType || '');
    });
  }

  ngOnInit(): void {}

  ngAfterViewChecked(): void {
    if (this.shouldScrollToBottom) {
      this.scrollToBottom();
      this.shouldScrollToBottom = false;
    }
  }

  onClose(): void {
    this.chatService.closeChat();
  }

  onSendMessage(): void {
    const message = this.userInput.trim();
    if (!message) return;

    this.userInput = '';
    this.shouldScrollToBottom = true;

    this.chatService.sendMessage(message).subscribe({
      next: () => {
        this.shouldScrollToBottom = true;
      },
      error: (error) => {
        console.error('Error sending message:', error);
        // Add error message to chat
        const errorMsg: ChatMessage = {
          role: 'assistant',
          content: '❌ Sorry, I encountered an error. Please try again.',
          timestamp: new Date()
        };
        this.chatService.messages.update(msgs => [...msgs, errorMsg]);
        this.chatService.isLoading.set(false);
      }
    });
  }

  onQuickActionClick(action: string): void {
    this.userInput = action;
    this.onSendMessage();
  }

  onClearChat(): void {
    if (confirm('Clear all chat history?')) {
      this.chatService.clearChat();
      // Re-add welcome message
      const context = this.chatService.context();
      this.chatService.openChat(context);
    }
  }

  getQuickActions(): string[] {
    return this.currentSuggestions;
  }

  getContextLabel(): string {
    const context = this.chatService.context();
    
    if (context.currentStep) {
      const stepLabels: any = {
        'why-flagged': 'Reviewing Alert Reason',
        'suitability': 'Verifying Suitability',
        'alternatives': 'Comparing Alternatives'
      };
      return stepLabels[context.currentStep] || 'Policy Review';
    }
    
    if (context.viewingAlternative) {
      return `Reviewing: ${context.viewingAlternative.productName}`;
    }
    
    if (context.alertType) {
      return `Alert: ${context.alertType.replace('_', ' ')}`;
    }
    
    return 'General Policy Review';
  }

  private scrollToBottom(): void {
    try {
      if (this.messagesContainer) {
        this.messagesContainer.nativeElement.scrollTop = 
          this.messagesContainer.nativeElement.scrollHeight;
      }
    } catch (err) {
      console.error('Scroll error:', err);
    }
  }

  onKeyPress(event: KeyboardEvent): void {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.onSendMessage();
    }
  }
}
