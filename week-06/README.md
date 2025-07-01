# OpenAI Agents SDK Streamlit Demo

A comprehensive demonstration of the OpenAI Agents SDK fundamentals using a multi-agent customer service system built with Streamlit.

## Features Demonstrated

This demo showcases all the core concepts of the OpenAI Agents SDK:

### 🤖 **Agents**
- **Triage Agent**: Main entry point that routes requests to appropriate specialists
- **Product Agent**: Handles product recommendations and shopping assistance
- **Technical Agent**: Provides technical support and troubleshooting
- **Billing Agent**: Manages billing inquiries and account issues

### 🔄 **Handoffs**
- Intelligent routing between specialized agents based on user intent
- Seamless delegation of tasks to the most appropriate expert
- Context preservation across agent transitions

### 🛡️ **Guardrails**
- Content validation to filter inappropriate messages
- Sensitive information detection and blocking
- Spam and toxicity filtering
- Business hours enforcement (demo implementation)

### 🔧 **Function Tools**
- Product search and recommendations
- Technical troubleshooting solutions
- Billing status checks
- Order tracking and store location services

### 📊 **Built-in Tracing**
- Automatic tracking of agent runs and decisions
- Debugging capabilities for agent workflows
- Performance monitoring and optimization insights

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### 1. Clone or Download Files
Create a new directory and save all the provided Python files in the following structure:
```
agents-demo/
├── main.py
├── requirements.txt
├── README.md
└── agents/
    ├── __init__.py
    ├── agent_definitions.py
    ├── customer_service_system.py
    ├── guardrails.py
    └── tools.py
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables (Optional)
```bash
export OPENAI_API_KEY="your-api-key-here"
```

Alternatively, you can enter your API key directly in the Streamlit interface.

### 4. Run the Application
```bash
streamlit run main.py
```

## Usage

1. **Enter API Key**: Input your OpenAI API key in the sidebar
2. **Initialize System**: Click "Initialize System" to set up all agents
3. **Start Chatting**: Use the chat interface to interact with the agents
4. **Try Examples**: Click on example queries in the sidebar for quick testing

## Example Interactions

### Product Recommendations
- "I need a gaming laptop under $1000"
- "What phones have the best camera?"
- "Compare your laptop options for me"

### Technical Support  
- "My WiFi keeps disconnecting"
- "My computer is running slowly"
- "The application crashes when I open it"

### Billing Support
- "I have a question about my bill"
- "I was charged twice for my order"
- "How do I update my payment method?"

### General Inquiries
- "What are your store hours?"
- "What's your return policy?"
- "Where are your store locations?"

## Architecture Overview

### Agent Flow
1. **User Input** → **Content Guardrails** → **Triage Agent**
2. **Triage Agent** analyzes intent and routes to appropriate specialist:
   - Product inquiries → **Product Agent**
   - Technical issues → **Technical Agent** 
   - Billing questions → **Billing Agent**
3. **Specialist Agent** uses relevant tools and provides expert assistance
4. **Response** is returned to user with tracing information

### Key Components

- **`main.py`**: Streamlit interface and application logic
- **`agent_definitions.py`**: Agent configurations and function tools
- **`customer_service_system.py`**: Main orchestration system
- **`guardrails.py`**: Safety checks and input validation
- **`tools.py`**: Additional utility functions and tools

## Customization

### Adding New Agents
1. Define the agent in `agent_definitions.py`
2. Add handoff reference in the triage agent
3. Update the system initialization

### Creating Custom Tools
1. Use the `@function_tool` decorator
2. Define clear docstrings for the LLM
3. Add input validation with Pydantic models

### Implementing New Guardrails
1. Create validation logic in `guardrails.py`
2. Return `GuardrailFunctionOutput` with appropriate flags
3. Add to agent configuration

## Advanced Features

### Structured Outputs
Agents can return structured data using Pydantic models:
```python
class ProductRecommendation(BaseModel):
    name: str
    price: float
    features: List[str]
```

### Context Management
Customer context is maintained across interactions:
```python
class CustomerContext:
    customer_id: str
    session_data: Dict[str, Any]
    conversation_history: List[Dict]
```

### Error Handling
Robust error handling ensures the system continues operating even when individual components fail.

## Troubleshooting

### Common Issues

**"System not initialized"**
- Ensure you've entered a valid OpenAI API key
- Click the "Initialize System" button
- Check your internet connection

**"Error processing request"**
- Verify your API key has sufficient credits
- Check if the OpenAI service is available
- Try refreshing the page and reinitializing

**Slow responses**
- This is normal for complex agent workflows
- The system performs multiple LLM calls for routing and processing
- Response times depend on OpenAI API performance
