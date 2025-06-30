from fastapi import FastAPI
from pydantic import BaseModel
from agent import DoctorAppointmentAgent
from langchain_core.messages import HumanMessage
import os
import uuid
import streamlit as st

os.environ.pop("SSL_CERT_FILE", None)


app = FastAPI()

# Define Pydantic model to accept request body
class UserQuery(BaseModel):
    id_number: int
    messages: str
    thread_id : str

agent = DoctorAppointmentAgent()

@app.post("/execute")
def execute_agent(user_input: UserQuery):
    
    # Prepare agent state as expected by the workflow
    input = [HumanMessage(content=user_input.messages)]

    state = {
        "messages": input,
        "id_number": user_input.id_number,
        "next": "",
        "query": "",
        "current_reasoning": "",
        "follow_up_needed": False
    }

    thread_id = str(user_input.thread_id)

    response = agent.invoke(state=state,thread_id=thread_id)
    return {"messages": response["messages"]}