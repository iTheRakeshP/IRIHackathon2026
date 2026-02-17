"""
AI Service - orchestrates AI provider usage
"""
from typing import List, Dict, Any, Optional
from app.services.ai.base_provider import AIProvider, ChatMessage, ChatResponse
from app.services.ai.openai_provider import OpenAIProvider
from app.services.ai.mock_provider import MockAIProvider
from app.config import settings


class AIService:
    """
    Main AI service that handles provider selection and chat operations.
    Provides a simple interface for AI interactions regardless of provider.
    """
    
    def __init__(self):
        """Initialize AI service with configured provider"""
        self._provider: Optional[AIProvider] = None
        self._initialize_provider()
    
    def _initialize_provider(self):
        """Initialize the AI provider based on configuration"""
        provider_name = settings.AI_PROVIDER.lower()
        
        if settings.AI_MOCK_MODE:
            # Use mock provider
            self._provider = MockAIProvider()
            print(f"AI Service initialized with Mock provider (AI_MOCK_MODE=True)")
        
        elif provider_name == "openai":
            try:
                self._provider = OpenAIProvider(
                    api_key=settings.AI_API_KEY,
                    model=settings.AI_MODEL
                )
                print(f"AI Service initialized with OpenAI provider (model: {settings.AI_MODEL})")
            except Exception as e:
                print(f"Failed to initialize OpenAI provider: {e}")
                print("Falling back to Mock provider")
                self._provider = MockAIProvider()
        
        # Add more providers here in the future:
        # elif provider_name == "anthropic":
        #     self._provider = AnthropicProvider(...)
        # elif provider_name == "azure-openai":
        #     self._provider = AzureOpenAIProvider(...)
        
        else:
            print(f"Unknown AI provider '{provider_name}', falling back to Mock provider")
            self._provider = MockAIProvider()
    
    async def chat(
        self,
        user_message: str,
        context: Optional[Dict[str, Any]] = None,
        conversation_history: Optional[List[ChatMessage]] = None,
        temperature: float = 0.7
    ) -> ChatResponse:
        """
        Send a chat message to the AI provider.
        
        Args:
            user_message: The user's message/question
            context: Context data (client, policy, alert info)
            conversation_history: Previous messages in the conversation
            temperature: Sampling temperature (0-1, lower = more focused)
            
        Returns:
            ChatResponse with AI-generated message
        """
        if not self._provider:
            raise RuntimeError("AI provider not initialized")
        
        # Build messages list
        messages = conversation_history.copy() if conversation_history else []
        
        # Add current user message
        messages.append(ChatMessage(role="user", content=user_message))
        
        # Get response from provider
        response = await self._provider.chat(
            messages=messages,
            context=context,
            temperature=temperature,
            max_tokens=1000
        )
        
        return response
    
    def get_quick_actions(self, alert_type: str) -> List[str]:
        """
        Get suggested quick actions based on alert type.
        These are displayed in the AI Copilot drawer UI.
        """
        quick_actions = {
            "REPLACEMENT": [
                "Explain why this alert was triggered",
                "Compare current policy to alternatives",
                "Draft best-interest summary",
                "Analyze suitability changes"
            ],
            "INCOME_ACTIVATION": [
                "Explain timing tradeoffs",
                "Draft client explanation",
                "Calculate break-even scenarios",
                "Compare now vs. delayed income"
            ],
            "SUITABILITY_DRIFT": [
                "Explain review rationale",
                "Draft suitability review note",
                "Summarize profile changes",
                "Document assessment"
            ]
        }
        
        return quick_actions.get(alert_type, [
            "Explain this alert",
            "Draft review note",
            "Provide guidance"
        ])
    
    def get_provider_info(self) -> Dict[str, str]:
        """Get information about the current AI provider"""
        if not self._provider:
            return {"provider": "none", "status": "not initialized"}
        
        return {
            "provider": self._provider.get_provider_name(),
            "mode": "mock" if settings.AI_MOCK_MODE else "live",
            "model": settings.AI_MODEL if self._provider.get_provider_name() == "openai" else "N/A"
        }


# Singleton instance
ai_service = AIService()
