import streamlit as st
import asyncio
import os
from typing import Dict, Any
from customer_service_system import CustomerServiceSystem
from agent_definitions import create_agents
from tools import setup_tools

# Configure Streamlit page
st.set_page_config(
    page_title="OpenAI Agents SDK Demo",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'system_initialized' not in st.session_state:
    st.session_state.system_initialized = False
if 'customer_service' not in st.session_state:
    st.session_state.customer_service = None

def initialize_system():
    """Initialize the customer service system with all agents"""
    try:
        # Create the customer service system
        customer_service = CustomerServiceSystem()
        st.session_state.customer_service = customer_service
        st.session_state.system_initialized = True
        return True
    except Exception as e:
        st.error(f"Failed to initialize system: {str(e)}")
        return False

async def process_user_input(user_input: str) -> str:
    """Process user input through the agent system"""
    try:
        if not st.session_state.customer_service:
            return "System not initialized. Please check your OpenAI API key."
        
        result = await st.session_state.customer_service.process_request(user_input)
        return result
    except Exception as e:
        return f"Error processing request: {str(e)}"

def main():
    st.title("🤖 OpenAI Agents SDK Demo")
    st.markdown("### Multi-Agent Customer Service System")
    
    # Sidebar for configuration and information
    with st.sidebar:
        st.header("Configuration")
        
        # API Key input
        api_key = st.text_input(
            "OpenAI API Key", 
            type="password", 
            value=os.getenv("OPENAI_API_KEY", ""),
            help="Enter your OpenAI API key to use the agents"
        )
        
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
            if not st.session_state.system_initialized:
                if st.button("Initialize System"):
                    with st.spinner("Initializing agents..."):
                        if initialize_system():
                            st.success("System initialized successfully!")
                            st.rerun()
        
        st.markdown("---")
        
        # System information
        st.header("System Overview")
        st.markdown("""
        **Agents in this system:**
        - 🎯 **Triage Agent**: Routes requests to appropriate specialists
        - 🛒 **Product Agent**: Handles product inquiries and recommendations
        - 🔧 **Technical Agent**: Provides technical support and troubleshooting
        - 💳 **Billing Agent**: Manages billing and payment issues
        
        **Features demonstrated:**
        - Agent handoffs between specialists
        - Function tools for external data
        - Input guardrails for content filtering
        - Structured outputs with Pydantic models
        - Built-in tracing and debugging
        """)
        
        st.markdown("---")
        
        # Example queries
        st.header("Try These Examples")
        example_queries = [
            "I'm looking for a laptop for gaming",
            "My wifi keeps disconnecting",
            "I have a question about my bill",
            "What's your return policy?",
            "My account was charged twice",
            "Can you recommend a phone under $500?"
        ]
        
        for query in example_queries:
            if st.button(query, key=f"example_{hash(query)}"):
                st.session_state.example_query = query

    # Main chat interface
    if not st.session_state.system_initialized:
        st.warning("⚠️ Please enter your OpenAI API key in the sidebar and initialize the system to start chatting.")
        st.info("💡 You can get your API key from [platform.openai.com](https://platform.openai.com/api-keys)")
        return

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "agent_info" in message:
                st.caption(f"Handled by: {message['agent_info']}")

    # Handle example query from sidebar
    if hasattr(st.session_state, 'example_query'):
        user_input = st.session_state.example_query
        del st.session_state.example_query
    else:
        # Chat input
        user_input = st.chat_input("Ask me anything about products, technical issues, or billing...")

    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)

        # Process the request and display response
        with st.chat_message("assistant"):
            with st.spinner("Processing your request..."):
                # Run the async function
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    response = loop.run_until_complete(process_user_input(user_input))
                finally:
                    loop.close()
                
                st.markdown(response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response,
                    "agent_info": "Multi-Agent System"
                })

    # Clear chat button
    if st.session_state.messages:
        if st.button("🗑️ Clear Chat", type="secondary"):
            st.session_state.messages = []
            st.rerun()

if __name__ == "__main__":
    main()