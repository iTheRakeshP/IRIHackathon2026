"""
Mock AI provider for testing and demo purposes
"""
from typing import List, Dict, Any, Optional
import random
from app.services.ai.base_provider import AIProvider, ChatMessage, ChatResponse


class MockAIProvider(AIProvider):
    """
    Mock AI provider with pre-scripted intelligent responses.
    Useful for hackathon demos and testing without API costs.
    """
    
    def __init__(self):
        """Initialize mock provider with response templates"""
        self.response_templates = {
            "REPLACEMENT": {
                "explain_alert": [
                    "This replacement opportunity alert was triggered because:\n\n"
                    "• The policy is approaching renewal with a material cap rate reduction\n"
                    "• Market conditions show higher cap rates available from competitive carriers\n"
                    "• The surrender schedule is ending soon, providing flexibility\n\n"
                    "A replacement review allows you to assess whether alternative products "
                    "better align with current client objectives and market conditions.",
                    
                    "The alert identifies a potential optimization opportunity based on:\n\n"
                    "• Renewal rate decline from {current_cap}% to {renewal_cap}%\n"
                    "• Current market rates averaging {market_rate}% for similar products\n"
                    "• Minimal surrender charges remaining\n\n"
                    "This doesn't mean replacement is necessary, but warrants a thorough review."
                ],
                "compare_options": [
                    "Comparing the current policy to alternatives:\n\n"
                    "**Current Policy Advantages:**\n"
                    "• Established relationship with carrier\n"
                    "• Known performance history\n"
                    "• Minimal fees remaining\n\n"
                    "**Alternative Product Advantages:**\n"
                    "• Higher cap rates (up to {alt_cap}%)\n"
                    "• Enhanced income rider options\n"
                    "• Shorter surrender schedules\n\n"
                    "**Key Considerations:**\n"
                    "• New surrender period if replaced\n"
                    "• Underwriting may be required\n"
                    "• Transaction costs and timing",
                    
                    "Here's a neutral comparison:\n\n"
                    "The current policy offers stability and known performance. "
                    "Alternative products show {cap_difference}% higher caps and enhanced features, "
                    "but would restart the surrender schedule.\n\n"
                    "**Tradeoffs:**\n"
                    "• Growth potential vs. liquidity timeline\n"
                    "• New product features vs. familiarity\n"
                    "• Market timing considerations"
                ],
                "draft_summary": [
                    "**Best Interest Review Summary**\n\n"
                    "After reviewing the client's current policy and available alternatives, "
                    "key considerations include:\n\n"
                    "1. **Performance**: Alternative products offer cap rates {cap_difference}% higher "
                    "than the renewal rate\n\n"
                    "2. **Client Objectives**: Client's {objective} objective aligns with products "
                    "offering {features}\n\n"
                    "3. **Tradeoffs**: Higher potential returns vs. new surrender period\n\n"
                    "4. **Suitability**: Client's {risk_tolerance} risk tolerance and {life_stage} "
                    "life stage were considered\n\n"
                    "This review identifies options for discussion with the client. "
                    "The final decision should reflect their preferences and circumstances."
                ]
            },
            "INCOME_ACTIVATION": {
                "explain_timing": [
                    "**Income Timing Considerations:**\n\n"
                    "**Begin Income Now:**\n"
                    "• Immediate cash flow\n"
                    "• Locks in current payout rate\n"
                    "• Reduces principal growth potential\n\n"
                    "**Delay Income (e.g., 2 years):**\n"
                    "• Income base continues to roll up\n"
                    "• Higher future payout amounts\n"
                    "• Requires other income sources meanwhile\n\n"
                    "The optimal timing depends on current income needs, "
                    "other retirement assets, and longevity expectations.",
                    
                    "Timing income activation involves balancing:\n\n"
                    "• **Current needs**: Does the client need income now?\n"
                    "• **Roll-up value**: Income base grows {rollup_rate}% annually if delayed\n"
                    "• **Break-even**: Delaying pays off if living beyond age {breakeven_age}\n"
                    "• **Flexibility**: Once activated, can't be reversed\n\n"
                    "This is a personal decision based on financial situation and health outlook."
                ],
                "draft_explanation": [
                    "**Income Activation Decision - Client Discussion Points**\n\n"
                    "Your income rider has reached eligibility. Here are your options:\n\n"
                    "**Option 1: Activate Now**\n"
                    "• Begin receiving ${monthly_now}/month for life\n"
                    "• Guaranteed income starts immediately\n"
                    "• Principal continues to participate in market growth\n\n"
                    "**Option 2: Delay Activation**\n"
                    "• Income base grows {rollup_rate}% each year you wait\n"
                    "• Future monthly income: ${monthly_future} if started at age {future_age}\n"
                    "• More flexibility if circumstances change\n\n"
                    "We should discuss your current income needs and other assets to determine "
                    "the best timing for your situation."
                ]
            },
            "SUITABILITY_DRIFT": {
                "explain_rationale": [
                    "This suitability review is recommended because:\n\n"
                    "• Time has passed since the original suitability assessment\n"
                    "• Life circumstances may have changed (age, objectives, needs)\n"
                    "• The product's features should still align with current goals\n\n"
                    "This is routine practice to ensure the policy remains appropriate. "
                    "It doesn't necessarily indicate any problem with the current policy.",
                    
                    "**Why Review Suitability Now:**\n\n"
                    "The client's situation when the policy was purchased may differ from today:\n\n"
                    "• Original Objective: {original_objective}\n"
                    "• Current Life Stage: {current_life_stage}\n"
                    "• Time Horizon: {years_held} years since issue\n\n"
                    "A suitability review confirms the product still fits or identifies "
                    "any adjustments needed."
                ],
                "draft_note": [
                    "**Suitability Review Documentation**\n\n"
                    "Reviewed client's current profile against existing policy:\n\n"
                    "• **Client Profile**: Age {age}, {life_stage}, {risk_tolerance} risk tolerance\n"
                    "• **Current Objectives**: {objectives}\n"
                    "• **Policy Features**: {product_type} with {features}\n\n"
                    "**Assessment**: Product features {alignment} with current client objectives. "
                    "{recommendation_text}\n\n"
                    "Documented in accordance with regulatory requirements."
                ]
            },
            "general": {
                "default": [
                    "I'm here to help explain this alert and discuss considerations. "
                    "Could you tell me more about what specific aspect you'd like to explore?\n\n"
                    "I can help with:\n"
                    "• Explaining why this alert was triggered\n"
                    "• Comparing options and tradeoffs\n"
                    "• Drafting review notes or client explanations",
                    
                    "I can assist with analyzing this situation. What would be most helpful?\n\n"
                    "• Walk through the alert rationale\n"
                    "• Discuss potential next steps\n"
                    "• Generate documentation for your review"
                ]
            }
        }
    
    async def chat(
        self,
        messages: List[ChatMessage],
        context: Optional[Dict[str, Any]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> ChatResponse:
        """
        Generate mock AI response based on context and user message.
        """
        # Get the last user message
        user_message = next(
            (msg.content for msg in reversed(messages) if msg.role == "user"),
            ""
        ).lower()
        
        # Determine alert type from context
        alert_type = context.get("activeAlertType", "general") if context else "general"
        
        # Select appropriate response template
        response_text = self._select_response(user_message, alert_type, context)
        
        # Fill in placeholders with context data
        response_text = self._fill_placeholders(response_text, context)
        
        # Build basedOn
        based_on = self._extract_based_on(context) if context else None
        
        return ChatResponse(
            message=response_text,
            conversationId=context.get("conversationId") if context else None,
            basedOn=based_on,
            provider="mock",
            tokensUsed=len(response_text) // 4  # Rough token estimate
        )
    
    def get_provider_name(self) -> str:
        return "mock"
    
    def _select_response(
        self, 
        user_message: str, 
        alert_type: str, 
        context: Optional[Dict[str, Any]]
    ) -> str:
        """Select appropriate response template based on user message"""
        
        templates = self.response_templates.get(alert_type, self.response_templates["general"])
        
        # Match user intent to template
        if any(word in user_message for word in ["explain", "why", "what", "rationale"]):
            if "explain_alert" in templates:
                return random.choice(templates["explain_alert"])
            elif "explain_timing" in templates:
                return random.choice(templates["explain_timing"])
            elif "explain_rationale" in templates:
                return random.choice(templates["explain_rationale"])
        
        elif any(word in user_message for word in ["compare", "difference", "options", "alternatives"]):
            if "compare_options" in templates:
                return random.choice(templates["compare_options"])
        
        elif any(word in user_message for word in ["draft", "write", "note", "summary", "document"]):
            if "draft_summary" in templates:
                return random.choice(templates["draft_summary"])
            elif "draft_explanation" in templates:
                return random.choice(templates["draft_explanation"])
            elif "draft_note" in templates:
                return random.choice(templates["draft_note"])
        
        # Default response
        return random.choice(templates.get("default", self.response_templates["general"]["default"]))
    
    def _fill_placeholders(self, text: str, context: Optional[Dict[str, Any]]) -> str:
        """Fill in placeholder variables with context data"""
        if not context:
            return text
        
        replacements = {
            "{current_cap}": str(context.get("currentCapRate", "3.9")),
            "{renewal_cap}": str(context.get("renewalCapRate", "3.4")),
            "{market_rate}": "5.5",
            "{alt_cap}": "6.0",
            "{cap_difference}": "1.5",
            "{objective}": context.get("clientObjective", "income"),
            "{features}": "guaranteed lifetime income",
            "{risk_tolerance}": context.get("clientRiskTolerance", "moderate"),
            "{life_stage}": context.get("clientLifeStage", "pre-retirement"),
            "{rollup_rate}": "7",
            "{breakeven_age}": "78",
            "{monthly_now}": "2,500",
            "{monthly_future}": "2,850",
            "{future_age}": "67",
            "{original_objective}": "growth",
            "{current_life_stage}": "pre-retirement",
            "{years_held}": "8",
            "{age}": str(context.get("clientAge", "62")),
            "{product_type}": "Fixed Index Annuity",
            "{alignment}": "align well",
            "{recommendation_text}": "No changes recommended at this time."
        }
        
        for placeholder, value in replacements.items():
            text = text.replace(placeholder, value)
        
        return text
    
    def _extract_based_on(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract 'based on' fields for transparency"""
        based_on = {}
        
        if context.get("clientAccountNumber"):
            based_on["clientFields"] = ["age", "riskTolerance", "primaryObjective"]
        
        if context.get("policyId"):
            based_on["policyFields"] = ["currentCapRate", "renewalRate"]
        
        if context.get("alternatives"):
            based_on["alternativesUsed"] = ["PROD-SYM-001", "PROD-BH-001"]
        
        return based_on if based_on else None
