"""
AI Provider base interface
Abstract base class for AI provider implementations
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class ChatMessage(BaseModel):
    """Chat message model"""
    role: str  # "system", "user", "assistant"
    content: str


class ChatResponse(BaseModel):
    """AI chat response"""
    message: str
    conversationId: Optional[str] = None
    basedOn: Optional[Dict[str, Any]] = None
    provider: str = "unknown"
    tokensUsed: Optional[int] = None


class AIProvider(ABC):
    """
    Abstract base class for AI providers.
    All AI provider implementations must inherit from this class.
    """
    
    @abstractmethod
    async def chat(
        self,
        messages: List[ChatMessage],
        context: Optional[Dict[str, Any]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> ChatResponse:
        """
        Send a chat request to the AI provider.
        
        Args:
            messages: List of chat messages (system, user, assistant)
            context: Optional context data (client, policy, alert info)
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens in response
            
        Returns:
            ChatResponse with AI-generated message
        """
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """Return the provider name (e.g., 'openai', 'anthropic')"""
        pass
