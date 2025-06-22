import boto3
import os
import re
import streamlit as st
import uuid

# Use your named AWS profile
os.environ["AWS_PROFILE"] = "aaditey-personal"

# Initialize Bedrock Agent Runtime client
agent_client = boto3.client("bedrock-agent-runtime", region_name="us-east-1")

# Set your agent and alias IDs
agent_id = "SYDHEELWTH"
agent_alias_id = "NV9MMGMZ43"

def my_chatbot(language, user_input):
    # Combine language preference with user query
    input_text = f"Please respond in {language}. {user_input}"
    
    # A unique session ID — you can also use the user ID if you want to persist memory
    session_id = str(uuid.uuid4())

    # Call the agent
    response = agent_client.invoke_agent(
        agentId=agent_id,
        agentAliasId=agent_alias_id,
        sessionId=session_id,
        inputText=input_text
    )

    # Read streaming chunks
    full_output = ""
    for chunk in response["completion"]:
        if "chunk" in chunk:
            full_output += chunk["chunk"]["bytes"].decode("utf-8")

    # Extract from <final_response> tag if used in post-processing
    match = re.search(r"<final_response>(.*?)</final_response>", full_output, re.DOTALL)
    if match:
        return {"text": match.group(1).strip()}
    else:
        return {"text": full_output.strip()}

# Streamlit UI
st.set_page_config(page_title="Bedrock Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 Bedrock Chatbot")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    language = st.selectbox("Select Language:", ["english", "spanish"], index=0)
    st.markdown("---")
    st.markdown("### 📝 Instructions")
    st.markdown("- Type a message below and hit Enter")
    st.markdown("- The agent will respond based on your query")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = my_chatbot(language, prompt)
                st.markdown(response["text"])
                st.session_state.messages.append({"role": "assistant", "content": response["text"]})
            except Exception as e:
                error = f"Sorry, there was an error: {str(e)}"
                st.error(error)
                st.session_state.messages.append({"role": "assistant", "content": error})

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #888;'>Powered by Amazon Bedrock Agent</div>", unsafe_allow_html=True)
