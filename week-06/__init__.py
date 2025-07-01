"""
OpenAI Agents SDK Demo Package

This package demonstrates the fundamental concepts of the OpenAI Agents SDK:
- Agents: LLMs configured with instructions, tools, guardrails, and handoffs
- Handoffs: Specialized tool calls for transferring control between agents
- Guardrails: Configurable safety checks for input and output validation
- Tracing: Built-in tracking of agent runs for debugging and optimization

The demo implements a customer service system with multiple specialized agents
that can handle different types of customer inquiries through intelligent routing.
"""

from .agent_definitions import create_agents
from .customer_service_system import CustomerServiceSystem
from .guardrails import create_content_guardrail, create_business_hours_guardrail
from .tools import setup_tools

__all__ = [
    'create_agents',
    'CustomerServiceSystem', 
    'create_content_guardrail',
    'create_business_hours_guardrail',
    'setup_tools'
]

__version__ = "1.0.0"
__author__ = "OpenAI Agents SDK Demo"
__description__ = "Multi-agent customer service system demonstrating OpenAI Agents SDK fundamentals"