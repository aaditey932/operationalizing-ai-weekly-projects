import streamlit as st
from typing import Annotated, List
from typing_extensions import TypedDict

from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from tools import tools
from rag import retrieve_docs, format_docs
import os

MODEL = "gpt-4o-mini"
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

class State(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]


@st.cache_resource
def initialize_llm():
    """Initialize LLM with tools (cached for performance)."""
    llm = ChatOpenAI(model=MODEL, api_key=OPENAI_API_KEY)
    return llm.bind_tools(tools)


@st.cache_resource
def create_graph():
    """Create and cache the LangGraph workflow."""
    llm_with_tools = initialize_llm()
    
    def should_retrieve(state: State) -> bool:
        """Check if we should retrieve documents based on the last message."""
        messages = state["messages"]
        if not messages:
            return False
        
        last_message = messages[-1].content.lower()
        
        # Keywords that suggest we need RAG
        rag_keywords = ["what is", "tell me about", "explain", "describe"]
        return any(keyword in last_message for keyword in rag_keywords)

    def assistant(state: State):
        """Main assistant node."""
        messages = state["messages"]
        
        if should_retrieve(state):
            query = messages[-1].content
            docs = retrieve_docs(query)
            context = format_docs(docs)
            
            context_message = f"Based on the following context: {context}\n\nUser question: {query}"
            messages_with_context = messages[:-1] + [messages[-1].__class__(content=context_message)]
            response = llm_with_tools.invoke(messages_with_context)
        else:
            response = llm_with_tools.invoke(messages)
        
        return {"messages": [response]}

    # Create tool node
    tool_node = ToolNode(tools)

    # Build the graph
    workflow = StateGraph(State)
    
    # Add nodes
    workflow.add_node("assistant", assistant)
    workflow.add_node("tools", tool_node)
    
    # Set entry point
    workflow.add_edge(START, "assistant")
    
    # Conditional edges
    workflow.add_conditional_edges(
        "assistant",
        tools_condition,
        {
            "tools": "tools",
            END: END,
        },
    )
    
    workflow.add_edge("tools", "assistant")
    
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)


def chat_with_assistant(message: str, thread_id: str = "streamlit_session"):
    """Chat with the assistant using the LangGraph."""
    graph = create_graph()
    
    config_dict = {"configurable": {"thread_id": thread_id}}
    
    try:
        result = graph.invoke(
            {"messages": [("user", message)]},
            config_dict
        )
        return result["messages"][-1].content
    except Exception as e:
        return f"Error: {str(e)}"


def main():
    """Main Streamlit app."""
    st.set_page_config(
        page_title="LangGraph Chat Assistant",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 LangGraph Chat Assistant")
    st.markdown("A simple chat interface with **Tools**, **RAG**, and **Memory**")
    
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        This app demonstrates:
        - **🛠️ Tools**: Calculator, time, search
        - **📚 RAG**: Document retrieval for knowledge questions  
        - **🧠 Memory**: Conversation history persistence
        """)
        
        st.header("🎯 Try These Examples")
        examples = [
            "What is LangGraph?",
            "Calculate 25 * 4",
            "What time is it?",
            "Tell me about Python",
            "Search for AI news"
        ]
        
        for example in examples:
            if st.button(example, key=f"example_{example}"):
                st.session_state.example_query = example
        
        st.header("🔄 Session")
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
        
        session_id = st.session_state.get('session_id', 'streamlit_session')
        st.text(f"Session ID: {session_id}")
    

    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if "example_query" in st.session_state:
        user_input = st.session_state.example_query
        del st.session_state.example_query
    else:
        user_input = None
    
    if prompt := st.chat_input("Type your message here...") or user_input:

        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Get unique session ID
                session_id = st.session_state.get('session_id', f"streamlit_{id(st.session_state)}")
                st.session_state.session_id = session_id
                
                response = chat_with_assistant(prompt, session_id)
                
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    with st.expander("🔧 Technical Details", expanded=False):
        st.markdown("""
        **Graph Structure:**
        ```
        START → Assistant → Tools (if needed) → Assistant → END
        ```
        
        **RAG Triggers:** Questions starting with "what is", "explain", "tell me about", "describe"
        
        **Available Tools:**
        - Calculator (safe math evaluation)
        - Current time
        - Web search (mock implementation)
        
        **Memory:** Conversations are persisted using thread IDs
        """)


if __name__ == "__main__":
    main()