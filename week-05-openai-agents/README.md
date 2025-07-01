# Multi-Agent Assistant with Guardrails

A Streamlit application demonstrating a multi-agent system with built-in guardrails and tracing capabilities.

## Features

- **Multi-Agent Architecture**: Triage agent routes requests to specialized web search agent
- **Input Guardrails**: Automatically blocks math homework requests
- **Web Search Tool**: Simulated web search functionality
- **Agent Handoffs**: Seamless delegation between agents
- **Execution Tracing**: Built-in trace monitoring for debugging

## Architecture

- **TriageAgent**: Entry point that filters requests and delegates to appropriate agents
- **WebAgent**: Specialized agent for web search tasks
- **Guardrails**: Input validation to prevent unwanted requests
- **Tools**: Web search capability (simulated)

## Setup

```bash
pip install streamlit
# Install your agents library
```

## Usage

```bash
streamlit run app.py
```

1. Enter your query in the text input
2. Click "Submit" to process
3. View the response and check the Traces dashboard for execution details

## How It Works

1. User input is processed by the TriageAgent
2. Input guardrails check for blocked content (e.g., homework requests)
3. Valid requests are either handled directly or handed off to WebAgent
4. WebAgent performs web searches and returns summarized results
5. All execution is traced for monitoring and debugging

## Key Components

- `@function_tool`: Decorator for creating agent tools
- `@input_guardrail`: Decorator for input validation
- `Runner.run()`: Executes agent workflows
- `trace()`: Provides execution monitoring