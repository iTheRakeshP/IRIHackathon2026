"""
OpenAI provider implementation
"""
from typing import List, Dict, Any, Optional
import json
from app.services.ai.base_provider import AIProvider, ChatMessage, ChatResponse
from app.config import settings

# OpenAI will be imported conditionally
try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class OpenAIProvider(AIProvider):
    """OpenAI GPT provider implementation"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        """
        Initialize OpenAI provider.
        
        Args:
            api_key: OpenAI API key (defaults to settings)
            model: Model to use (gpt-4, gpt-3.5-turbo, etc.)
        """
        if not OPENAI_AVAILABLE:
            raise ImportError(
                "OpenAI package not installed. "
                "Install with: pip install openai"
            )
        
        self.api_key = api_key or settings.AI_API_KEY
        self.model = model
        
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not configured. "
                "Set AI_API_KEY in .env file or pass to constructor."
            )
        
        self.client = AsyncOpenAI(api_key=self.api_key)
    
    async def chat(
        self,
        messages: List[ChatMessage],
        context: Optional[Dict[str, Any]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> ChatResponse:
        """
        Send chat request to OpenAI.
        """
        # Convert messages to OpenAI format
        openai_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        # Add system context if provided
        if context and not any(msg.role == "system" for msg in messages):
            system_prompt = self._build_system_prompt(context)
            openai_messages.insert(0, {"role": "system", "content": system_prompt})
        
        # Call OpenAI API
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=openai_messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            assistant_message = response.choices[0].message.content
            tokens_used = response.usage.total_tokens if response.usage else None
            
            # Build basedOn from context
            based_on = self._extract_based_on(context) if context else None
            
            return ChatResponse(
                message=assistant_message,
                conversationId=context.get("conversationId") if context else None,
                basedOn=based_on,
                provider="openai",
                tokensUsed=tokens_used
            )
            
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")
    
    def get_provider_name(self) -> str:
        return "openai"
    
    def _build_system_prompt(self, context: Dict[str, Any]) -> str:
        """Build system prompt from context"""
        prompt_parts = [
            "You are an AI assistant for financial advisors reviewing annuity policies.",
            "Your role is to provide decision support - not recommendations.",
            "Always maintain a neutral, educational tone.",
            "Avoid 'buy/sell' language. Focus on tradeoffs and considerations.",
            ""
        ]
        
        # Add context information
        if context.get("clientAccountNumber"):
            prompt_parts.append(f"Client Account: {context['clientAccountNumber']}")
        
        if context.get("policyId"):
            prompt_parts.append(f"Policy ID: {context['policyId']}")
        
        if context.get("activeAlertType"):
            prompt_parts.append(f"Active Alert: {context['activeAlertType']}")
        
        if context.get("clientSuitability"):
            suitability = context["clientSuitability"]
            prompt_parts.append(f"Client Age: {suitability.get('age')}")
            prompt_parts.append(f"Risk Tolerance: {suitability.get('riskTolerance')}")
            prompt_parts.append(f"Primary Objective: {suitability.get('primaryObjective')}")
        
        if context.get("policyDetails"):
            policy = context["policyDetails"]
            prompt_parts.append(f"Current Policy: {policy.get('policyLabel')}")
            if policy.get('currentCapRate'):
                prompt_parts.append(f"Current Cap: {policy['currentCapRate']}%")
        
        return "\n".join(prompt_parts)
    
    def _extract_based_on(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract 'based on' fields for transparency"""
        based_on = {}
        
        if context.get("clientSuitability"):
            based_on["clientFields"] = ["age", "riskTolerance", "primaryObjective", "incomeNeed"]
        
        if context.get("policyDetails"):
            based_on["policyFields"] = ["issueDate", "currentCapRate", "renewalRate", "surrenderSchedule"]
        
        if context.get("alternatives"):
            based_on["alternativesUsed"] = [
                alt.get("productId") for alt in context["alternatives"]
            ]
        
        return based_on if based_on else None
