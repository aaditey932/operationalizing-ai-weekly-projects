"""
Customer Service System using OpenAI Agents SDK.
This module orchestrates the multi-agent customer service workflow.
"""

import asyncio
from typing import Optional, Dict, Any
from agents import Agent, Runner, InputGuardrail, GuardrailFunctionOutput
from pydantic import BaseModel
from agent_definitions import create_agents
from guardrails import create_content_guardrail

class CustomerContext:
    """Context object to maintain customer session data."""
    def __init__(self, customer_id: str = "demo_customer"):
        self.customer_id = customer_id
        self.session_data: Dict[str, Any] = {}
        self.conversation_history = []

class CustomerServiceSystem:
    """Main customer service system that coordinates multiple agents."""
    
    def __init__(self):
        """Initialize the customer service system with all agents and guardrails."""
        self.agents = create_agents()
        self.triage_agent = self.agents["triage"]
        self.content_guardrail = create_content_guardrail()
        
        # Add content guardrail to the triage agent
        self.triage_agent_with_guardrails = Agent(
            name=self.triage_agent.name,
            instructions=self.triage_agent.instructions,
            handoffs=self.triage_agent.handoffs,
            model=self.triage_agent.model,
            input_guardrails=[self.content_guardrail]
        )
    
    async def process_request(self, user_input: str, customer_id: str = "demo_customer") -> str:
        """
        Process a customer request through the agent system.
        
        Args:
            user_input: The customer's message
            customer_id: Unique identifier for the customer
            
        Returns:
            The agent's response as a string
        """
        try:
            # Create customer context
            context = CustomerContext(customer_id)
            context.conversation_history.append({"role": "user", "content": user_input})
            
            # Run the request through the triage agent with guardrails
            result = await Runner.run(
                agent=self.triage_agent_with_guardrails,
                input=user_input,
                context=context
            )
            
            # Store the response in conversation history
            response = result.final_output
            context.conversation_history.append({"role": "assistant", "content": response})
            
            return response
            
        except Exception as e:
            error_message = f"I apologize, but I encountered an error while processing your request: {str(e)}"
            return error_message
    
    def get_agent_info(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all available agents."""
        agent_info = {}
        for name, agent in self.agents.items():
            agent_info[name] = {
                "name": agent.name,
                "description": getattr(agent, 'handoff_description', 'No description available'),
                "tools": [tool.__name__ if hasattr(tool, '__name__') else str(tool) 
                         for tool in getattr(agent, 'tools', [])],
                "model": getattr(agent, 'model', 'Not specified')
            }
        return agent_info
    
    async def test_individual_agent(self, agent_name: str, test_input: str) -> str:
        """
        Test an individual agent directly (useful for debugging).
        
        Args:
            agent_name: Name of the agent to test
            test_input: Input to send to the agent
            
        Returns:
            The agent's response
        """
        if agent_name not in self.agents:
            return f"Agent '{agent_name}' not found. Available agents: {list(self.agents.keys())}"
        
        try:
            context = CustomerContext()
            result = await Runner.run(
                agent=self.agents[agent_name],
                input=test_input,
                context=context
            )
            return result.final_output
        except Exception as e:
            return f"Error testing agent '{agent_name}': {str(e)}"
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get the current status of the system and all agents."""
        status = {
            "system_status": "operational",
            "total_agents": len(self.agents),
            "agents": {},
            "guardrails_active": True
        }
        
        # Test each agent with a simple query
        for name, agent in self.agents.items():
            try:
                test_result = await self.test_individual_agent(name, "Hello, can you help me?")
                status["agents"][name] = {
                    "status": "operational" if test_result and not test_result.startswith("Error") else "error",
                    "last_test": "Hello, can you help me?",
                    "response_length": len(test_result) if test_result else 0
                }
            except Exception as e:
                status["agents"][name] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return status