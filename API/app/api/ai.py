"""
AI Chat API endpoints
"""
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.services.ai.ai_service import ai_service
from app.services.ai.base_provider import ChatMessage, ChatResponse


router = APIRouter(
    prefix="/api/ai",
    tags=["AI Copilot"]
)


class ChatRequest(BaseModel):
    """Request model for AI chat"""
    message: str = Field(..., description="User message/question")
    context: Optional[Dict[str, Any]] = Field(
        None,
        description="Context data: client_id, policy_id, alert details, etc."
    )
    conversation_history: Optional[List[ChatMessage]] = Field(
        None,
        description="Previous messages in the conversation"
    )
    temperature: Optional[float] = Field(
        0.7,
        ge=0.0,
        le=1.0,
        description="Sampling temperature (0-1, lower = more focused)"
    )


class QuickActionsResponse(BaseModel):
    """Response model for quick actions"""
    alert_type: str
    actions: List[str]


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Send a message to AI Copilot and get intelligent response.
    
    The AI provides context-aware guidance for annuity review tasks:
    - Policy replacement analysis
    - Income activation timing
    - Suitability drift explanations
    - Draft communication templates
    
    **Provider Configuration:**
    - Set AI_PROVIDER in .env (openai, mock)
    - Set AI_MOCK_MODE=true for demo mode (no API costs)
    - OpenAI requires AI_API_KEY environment variable
    
    **Context Data:**
    Include client_id, policy_id, and alert details for personalized responses.
    
    **Example Request:**
    ```json
    {
        "message": "Why was this replacement alert triggered?",
        "context": {
            "client_id": "C-90002",
            "policy_id": "POL-90002",
            "alert_type": "REPLACEMENT",
            "current_cap": "3.4%",
            "alert_severity": "HIGH"
        }
    }
    ```
    """
    try:
        response = await ai_service.chat(
            user_message=request.message,
            context=request.context,
            conversation_history=request.conversation_history,
            temperature=request.temperature
        )
        return response
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI chat error: {str(e)}"
        )


@router.get("/quick-actions/{alert_type}", response_model=QuickActionsResponse)
async def get_quick_actions(alert_type: str):
    """
    Get suggested quick action prompts for a specific alert type.
    
    These are displayed as clickable suggestions in the AI Copilot drawer UI
    to help users quickly ask common questions.
    
    **Supported Alert Types:**
    - REPLACEMENT
    - INCOME_ACTIVATION
    - SUITABILITY_DRIFT
    """
    actions = ai_service.get_quick_actions(alert_type)
    
    return QuickActionsResponse(
        alert_type=alert_type,
        actions=actions
    )


@router.get("/provider-info")
async def get_provider_info():
    """
    Get information about the current AI provider configuration.
    
    Useful for debugging and displaying provider status in the UI.
    """
    return ai_service.get_provider_info()
