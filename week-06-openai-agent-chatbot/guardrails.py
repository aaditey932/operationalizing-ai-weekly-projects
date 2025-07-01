"""
Guardrails implementation for the OpenAI Agents SDK demo.
This module contains safety checks and input validation.
"""

from agents import Agent, Runner, GuardrailFunctionOutput
from pydantic import BaseModel
from typing import Any

class ContentValidation(BaseModel):
    """Model for content validation results."""
    is_appropriate: bool
    contains_sensitive_info: bool
    is_spam: bool
    toxicity_level: str  # "low", "medium", "high"
    reasoning: str

class ContentGuardrail:
    """Content guardrail to validate user inputs."""
    
    def __init__(self):
        """Initialize the content validation agent."""
        self.validation_agent = Agent(
            name="Content Validator",
            instructions="""You are a content validation specialist who checks user messages for appropriateness.
            
            Analyze the input for:
            - Inappropriate content (profanity, harassment, threats)
            - Sensitive personal information (SSN, credit card numbers, passwords)
            - Spam or promotional content
            - Overall toxicity level
            
            Return your analysis with clear reasoning.
            
            Guidelines:
            - Mark as inappropriate if contains: threats, harassment, hate speech, explicit content
            - Mark as containing sensitive info if has: SSN, credit cards, passwords, API keys
            - Mark as spam if: excessive promotion, repetitive content, obvious marketing
            - Toxicity levels: low (normal conversation), medium (rude but not harmful), high (threatening/hateful)
            
            Be balanced - don't flag normal business conversations as inappropriate.""",
            output_type=ContentValidation,
            model="gpt-4o-mini"
        )
    
    async def validate_content(self, ctx, agent, input_data: str) -> GuardrailFunctionOutput:
        """
        Validate user input content.
        
        Args:
            ctx: Context from the agent run
            agent: The agent being protected
            input_data: User input to validate
            
        Returns:
            GuardrailFunctionOutput with validation results
        """
        try:
            # Run content validation
            result = await Runner.run(
                agent=self.validation_agent,
                input=f"Please validate this user message: {input_data}",
                context=ctx.context if hasattr(ctx, 'context') else None
            )
            
            validation_result = result.final_output_as(ContentValidation)
            
            # Determine if we should block the request
            should_block = (
                not validation_result.is_appropriate or
                validation_result.contains_sensitive_info or
                validation_result.is_spam or
                validation_result.toxicity_level == "high"
            )
            
            # Create appropriate response if blocking
            if should_block:
                block_reasons = []
                if not validation_result.is_appropriate:
                    block_reasons.append("inappropriate content")
                if validation_result.contains_sensitive_info:
                    block_reasons.append("sensitive information")
                if validation_result.is_spam:
                    block_reasons.append("spam content")
                if validation_result.toxicity_level == "high":
                    block_reasons.append("high toxicity")
                
                block_message = f"I cannot process this request due to: {', '.join(block_reasons)}. Please rephrase your message appropriately."
            else:
                block_message = None
            
            return GuardrailFunctionOutput(
                output_info=validation_result,
                tripwire_triggered=should_block,
                blocked_message=block_message
            )
            
        except Exception as e:
            # If validation fails, err on the side of caution but don't block
            return GuardrailFunctionOutput(
                output_info=ContentValidation(
                    is_appropriate=True,
                    contains_sensitive_info=False,
                    is_spam=False,
                    toxicity_level="low",
                    reasoning=f"Validation error: {str(e)}"
                ),
                tripwire_triggered=False
            )

class BusinessHoursGuardrail:
    """Guardrail to check if request is during business hours."""
    
    async def validate_business_hours(self, ctx, agent, input_data: str) -> GuardrailFunctionOutput:
        """
        Check if the request is during business hours.
        
        Note: This is a simplified demo - in real implementation you'd check actual time.
        """
        from datetime import datetime, time
        
        current_hour = datetime.now().hour
        business_start = 9  # 9 AM
        business_end = 17   # 5 PM
        
        is_business_hours = business_start <= current_hour < business_end
        
        if not is_business_hours:
            after_hours_message = (
                "Thank you for contacting us! Our customer service hours are 9 AM to 5 PM. "
                "Your message has been received and we'll respond during our next business day. "
                "For urgent technical issues, please visit our self-service help center."
            )
            return GuardrailFunctionOutput(
                output_info={"business_hours": is_business_hours, "current_hour": current_hour},
                tripwire_triggered=True,
                blocked_message=after_hours_message
            )
        
        return GuardrailFunctionOutput(
            output_info={"business_hours": is_business_hours, "current_hour": current_hour},
            tripwire_triggered=False
        )

def create_content_guardrail():
    """Create and return the content validation guardrail."""
    content_guardrail = ContentGuardrail()
    return content_guardrail.validate_content

def create_business_hours_guardrail():
    """Create and return the business hours guardrail."""
    hours_guardrail = BusinessHoursGuardrail()
    return hours_guardrail.validate_business_hours

# Example of how to create a simple keyword-based guardrail
async def simple_keyword_guardrail(ctx, agent, input_data: str) -> GuardrailFunctionOutput:
    """
    Simple keyword-based guardrail for demonstration.
    Blocks requests containing certain keywords.
    """
    blocked_keywords = ["hack", "exploit", "vulnerability", "bypass", "malware"]
    
    input_lower = input_data.lower()
    found_keywords = [keyword for keyword in blocked_keywords if keyword in input_lower]
    
    if found_keywords:
        return GuardrailFunctionOutput(
            output_info={"blocked_keywords": found_keywords},
            tripwire_triggered=True,
            blocked_message="I cannot assist with requests related to security exploits or malicious activities."
        )
    
    return GuardrailFunctionOutput(
        output_info={"status": "clean"},
        tripwire_triggered=False
    )