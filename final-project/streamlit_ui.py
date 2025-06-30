import streamlit as st
import requests
import uuid

# API Configuration
API_URL = "http://127.0.0.1:8003/execute"

# Page configuration
st.set_page_config(page_title="Doctor Appointment Assistant", page_icon="🩺")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_id" not in st.session_state:
    st.session_state.user_id = ""
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# Title and header
st.title("🩺 Doctor Appointment Assistant")
st.markdown("*Your personal healthcare scheduling assistant*")

# Sidebar for user ID
with st.sidebar:
    st.header("👤 User Information")
    user_id = st.text_input(
        "Enter your ID number:", 
        value=st.session_state.user_id,
        placeholder="e.g., 12345"
    )
    if user_id != st.session_state.user_id:
        st.session_state.user_id = user_id
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Main chat interface
st.markdown("---")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about appointments, availability, or healthcare services..."):
    if not st.session_state.user_id:
        st.error("⚠️ Please enter your ID number in the sidebar first.")
        st.stop()
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get assistant response
    with st.chat_message("assistant"):
        with st.spinner("Processing your request..."):
            try:
                response = requests.post(
                    API_URL, 
                    json={
                        'messages': prompt, 
                        'id_number': int(st.session_state.user_id),
                        'thread_id': st.session_state.thread_id
                    },
                    verify=False,
                    timeout=30
                )
                
                if response.status_code == 200:
                    messages = response.json().get("messages", [])
                    
                    if messages:
                        # Get the last AI message with type 'ai'
                        last_ai_msg = next((msg for msg in reversed(messages) if msg["type"] == "ai"), None)
                        content = last_ai_msg["content"] if last_ai_msg else "No assistant response found."

                        st.markdown(content)

                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": content
                        })
                    else:
                        st.error("No messages returned from the agent.")
                    
                else:
                    error_msg = f"❌ Error {response.status_code}: Could not process the request."
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": error_msg
                    })
                    
            except requests.exceptions.Timeout:
                error_msg = "⏰ Request timed out. Please try again."
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_msg
                })
                
            except Exception as e:
                error_msg = f"❌ An error occurred: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_msg
                })

# Quick action buttons
if st.session_state.user_id:
    st.markdown("---")
    st.markdown("**Quick Actions:**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📅 Check Availability"):
            quick_query = "What appointments are available today?"
            st.session_state.messages.append({"role": "user", "content": quick_query})
            st.rerun()
    
    with col2:
        if st.button("🦷 Find Dentist"):
            quick_query = "I need to book a dentist appointment"
            st.session_state.messages.append({"role": "user", "content": quick_query})
            st.rerun()
    
    with col3:
        if st.button("👨‍⚕️ General Doctor"):
            quick_query = "I need to see a general practitioner"
            st.session_state.messages.append({"role": "user", "content": quick_query})
            st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <small>💡 Tip: Ask about specific times, doctors, or medical services</small>
    </div>
    """, 
    unsafe_allow_html=True
)