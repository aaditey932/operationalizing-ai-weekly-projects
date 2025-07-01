"""
Agent definitions for the OpenAI Agents SDK demo.
This module contains all agent configurations and their specialized roles.
"""

from agents import Agent, function_tool
from pydantic import BaseModel
from typing import List, Optional
import random

# Pydantic models for structured outputs
class ProductRecommendation(BaseModel):
    name: str
    price: float
    category: str
    features: List[str]
    rating: float

class TechnicalSolution(BaseModel):
    issue: str
    solution_steps: List[str]
    difficulty: str  # "easy", "medium", "hard"
    estimated_time: str

class BillingInquiry(BaseModel):
    inquiry_type: str
    account_status: str
    recommended_action: str
    requires_human: bool

# Function tools for agents
@function_tool
def search_products(category: str, max_price: Optional[float] = None) -> List[ProductRecommendation]:
    """Search for products in a given category with optional price filter."""
    # Simulated product database
    products_db = {
        "laptop": [
            ProductRecommendation(
                name="Gaming Pro X1", 
                price=1299.99, 
                category="laptop",
                features=["RTX 4060", "16GB RAM", "512GB SSD", "144Hz Display"],
                rating=4.5
            ),
            ProductRecommendation(
                name="Business Elite", 
                price=899.99, 
                category="laptop",
                features=["Intel i7", "8GB RAM", "256GB SSD", "Business Grade"],
                rating=4.2
            ),
            ProductRecommendation(
                name="Budget Saver", 
                price=499.99, 
                category="laptop",
                features=["AMD Ryzen 5", "8GB RAM", "128GB SSD"],
                rating=3.8
            )
        ],
        "phone": [
            ProductRecommendation(
                name="SmartPhone Pro", 
                price=899.99, 
                category="phone",
                features=["108MP Camera", "5G", "256GB Storage", "6.7\" Display"],
                rating=4.6
            ),
            ProductRecommendation(
                name="Budget Phone Plus", 
                price=299.99, 
                category="phone",
                features=["64MP Camera", "4G", "128GB Storage", "6.1\" Display"],
                rating=4.0
            )
        ]
    }
    
    # Get products for category
    products = products_db.get(category.lower(), [])
    
    # Apply price filter if specified
    if max_price:
        products = [p for p in products if p.price <= max_price]
    
    return products

@function_tool
def get_technical_solution(issue_description: str) -> TechnicalSolution:
    """Get technical solution for a given issue."""
    # Simulated technical knowledge base
    solutions_db = {
        "wifi": TechnicalSolution(
            issue="WiFi connectivity issues",
            solution_steps=[
                "Restart your router by unplugging for 30 seconds",
                "Check if other devices can connect to the same network",
                "Forget and reconnect to the WiFi network on your device",
                "Update your device's network drivers",
                "Contact ISP if issue persists"
            ],
            difficulty="easy",
            estimated_time="10-15 minutes"
        ),
        "slow": TechnicalSolution(
            issue="Device running slowly",
            solution_steps=[
                "Close unnecessary applications and browser tabs",
                "Check available storage space (should have 10%+ free)",
                "Run antivirus scan if on Windows",
                "Clear browser cache and temporary files",
                "Restart your device",
                "Check for system updates"
            ],
            difficulty="easy",
            estimated_time="20-30 minutes"
        ),
        "crash": TechnicalSolution(
            issue="Application crashes",
            solution_steps=[
                "Update the application to latest version",
                "Restart the application",
                "Check system requirements compatibility",
                "Run application as administrator (Windows)",
                "Clear application cache/data",
                "Reinstall the application if needed"
            ],
            difficulty="medium",
            estimated_time="15-45 minutes"
        )
    }
    
    # Simple keyword matching for demo
    issue_lower = issue_description.lower()
    if "wifi" in issue_lower or "internet" in issue_lower or "connection" in issue_lower:
        return solutions_db["wifi"]
    elif "slow" in issue_lower or "performance" in issue_lower:
        return solutions_db["slow"]
    elif "crash" in issue_lower or "freeze" in issue_lower or "error" in issue_lower:
        return solutions_db["crash"]
    else:
        return TechnicalSolution(
            issue="General technical issue",
            solution_steps=[
                "Describe your issue in more detail",
                "Check if the problem is reproducible",
                "Note any error messages",
                "Try restarting the application/device",
                "Contact technical support with specific details"
            ],
            difficulty="medium",
            estimated_time="Varies"
        )

@function_tool
def check_billing_status(customer_id: str = "demo123") -> BillingInquiry:
    """Check billing status and provide account information."""
    # Simulated billing system
    billing_scenarios = [
        BillingInquiry(
            inquiry_type="Payment overdue",
            account_status="Past due - $156.99",
            recommended_action="Please update payment method or pay outstanding balance",
            requires_human=False
        ),
        BillingInquiry(
            inquiry_type="Duplicate charge",
            account_status="Investigation required",
            recommended_action="Duplicate charge found - refund will be processed in 3-5 business days",
            requires_human=True
        ),
        BillingInquiry(
            inquiry_type="Account in good standing",
            account_status="Current - Next bill: $89.99 on March 15th",
            recommended_action="No action required",
            requires_human=False
        )
    ]
    
    # Return random scenario for demo
    return random.choice(billing_scenarios)

def create_agents():
    """Create and configure all agents for the system."""
    
    # Product Specialist Agent
    product_agent = Agent(
        name="Product Specialist",
        handoff_description="Expert on product recommendations, features, and comparisons",
        instructions="""You are a knowledgeable product specialist who helps customers find the right products.
        
        Your expertise includes:
        - Product recommendations based on customer needs and budget
        - Detailed product comparisons and feature explanations
        - Pricing information and availability
        - Product specifications and compatibility
        
        Always:
        - Ask clarifying questions about budget and specific needs
        - Use the search_products tool to find relevant products
        - Provide honest comparisons including pros and cons
        - Be enthusiastic but not pushy
        - Mention key features that match customer requirements
        
        When helping customers:
        1. Understand their specific needs and budget
        2. Search for appropriate products
        3. Present options with clear explanations
        4. Help them make informed decisions""",
        tools=[search_products],
        model="gpt-4o-mini"
    )

    # Technical Support Agent
    technical_agent = Agent(
        name="Technical Support",
        handoff_description="Specialist for technical issues, troubleshooting, and device problems",
        instructions="""You are a skilled technical support specialist who helps customers resolve technical issues.
        
        Your expertise includes:
        - Troubleshooting device and software problems
        - Step-by-step technical guidance
        - Network connectivity issues
        - Performance optimization
        - Software installation and configuration
        
        Always:
        - Ask about the specific symptoms and when they started
        - Use the get_technical_solution tool for structured troubleshooting
        - Provide clear, step-by-step instructions
        - Check if the customer needs additional help after each major step
        - Be patient and use non-technical language when possible
        
        When helping customers:
        1. Gather details about the specific problem
        2. Get appropriate technical solution steps
        3. Guide them through the solution clearly
        4. Follow up to ensure the issue is resolved""",
        tools=[get_technical_solution],
        model="gpt-4o-mini"
    )

    # Billing Support Agent
    billing_agent = Agent(
        name="Billing Support",
        handoff_description="Specialist for billing inquiries, payments, and account issues",
        instructions="""You are a helpful billing support specialist who assists with account and payment issues.
        
        Your expertise includes:
        - Account balance and payment status
        - Billing cycle and payment method updates
        - Refunds and dispute resolution
        - Plan changes and upgrades
        - Payment troubleshooting
        
        Always:
        - Use the check_billing_status tool to get current account information
        - Be empathetic about billing concerns
        - Explain charges and billing cycles clearly
        - Escalate to human agents when required
        - Protect customer privacy and security
        
        When helping customers:
        1. Check their current billing status
        2. Address their specific concern
        3. Provide clear next steps
        4. Escalate complex issues appropriately""",
        tools=[check_billing_status],
        model="gpt-4o-mini"
    )

    # Main Triage Agent
    triage_agent = Agent(
        name="Customer Service Triage",
        instructions="""You are a friendly customer service representative who helps route customers to the right specialist.
        
        Your role is to:
        - Greet customers warmly and understand their needs
        - Determine which specialist can best help them
        - Route to the appropriate agent via handoffs
        - Handle simple general inquiries directly
        
        Route customers as follows:
        - Product questions, recommendations, shopping → Product Specialist
        - Technical issues, troubleshooting, device problems → Technical Support  
        - Billing, payments, account issues, charges → Billing Support
        
        If the request is unclear, ask a clarifying question before routing.
        For general company information (hours, policies, etc.), you can answer directly.
        
        Always be helpful, professional, and ensure customers feel heard.""",
        handoffs=[product_agent, technical_agent, billing_agent],
        model="gpt-4o-mini"
    )

    return {
        "triage": triage_agent,
        "product": product_agent,
        "technical": technical_agent,
        "billing": billing_agent
    }