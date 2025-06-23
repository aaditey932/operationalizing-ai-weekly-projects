from langchain.chains import LLMChain
from langchain_community.llms import Bedrock
from langchain.prompts import PromptTemplate
import boto3
import json
import os
import streamlit as st
import uuid
import random
from botocore.exceptions import ClientError

os.environ["AWS_PROFILE"] = "aaditey-personal"

#bedrock client

bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

model_id = "amazon.nova-lite-v1:0"

def my_chatbot(user_input):

    conversation = [
        {"role": "user", "content": [{"text": user_input}]}
    ]

    try:
        response = bedrock_client.converse(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={
                "maxTokens": 512,
                "temperature": 0.7,
                "topP": 0.9
            }
        )

        # Extract response text
        return response["output"]["message"]["content"][0]["text"]

    except (ClientError, Exception) as e:
        return f"ERROR: Failed to invoke model: {str(e)}"

#print(my_chatbot("english","who is buddha?"))
# Streamlit UI
st.set_page_config(page_title="Bedrock Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 Bedrock Chatbot")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.markdown("### 📝 Instructions")
    st.markdown("- Type a message below and hit Enter")
    st.markdown("- The llm will respond based on your query")
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
                response = my_chatbot(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error = f"Sorry, there was an error: {str(e)}"
                st.error(error)
                st.session_state.messages.append({"role": "assistant", "content": error})

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #888;'>Powered by Amazon Bedrock Nova</div>", unsafe_allow_html=True)
