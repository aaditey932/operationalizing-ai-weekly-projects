from typing import Literal, Any
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from langgraph.types import Command
from langgraph.graph.message import add_messages
from langgraph.graph import START, StateGraph, END
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from typing_extensions import Annotated, TypedDict

# --- project‑local imports ----------------------------------------------------
from prompt_library.prompt import system_prompt
from utils.llms import LLMModel
from toolkit.toolkits import (
    check_availability_by_doctor,
    check_availability_by_specialization,
    set_appointment,
    cancel_appointment,
    reschedule_appointment,
)

# -----------------------------------------------------------------------------
# State & routing schema
# -----------------------------------------------------------------------------

class Router(TypedDict):
    """Schema for the LLM‑based router response."""

    next: Literal["information_node", "booking_node", "FINISH"]
    reasoning: str


class AgentState(TypedDict):
    """State object that flows through LangGraph."""

    messages: Annotated[list[Any], add_messages]
    id_number: int
    next: str
    query: str
    current_reasoning: str
    follow_up_needed: bool


# -----------------------------------------------------------------------------
# Main agent class
# -----------------------------------------------------------------------------


class DoctorAppointmentAgent:
    """Multi‑node LangGraph agent for doctor scheduling workflows."""

    # ------------------------------------------------------------------
    # constructor and workflow compilation
    # ------------------------------------------------------------------

    def __init__(self, memory: MemorySaver | None = None):
        self.llm_model = LLMModel().get_model()
        self.memory = memory or MemorySaver()

        # build graph
        self.graph = StateGraph(AgentState)
        self.graph.add_node("supervisor", self.supervisor_node)
        self.graph.add_node("information_node", self.information_node)
        self.graph.add_node("booking_node", self.booking_node)
        self.graph.add_edge(START, "supervisor")
        self.app = self.graph.compile(checkpointer=self.memory)

    # ------------------------------------------------------------------
    # public entrypoint
    # ------------------------------------------------------------------

    def invoke(self, state: AgentState, *, thread_id: str) -> AgentState:
        """Invoke the LangGraph run bound to a stable thread id."""
        config = {"configurable": {"thread_id": thread_id}}
        return self.app.invoke(state, config=config)  # type: ignore[return-value]

    # ------------------------------------------------------------------
    # Graph nodes
    # ------------------------------------------------------------------

    # ------------------------ supervisor --------------------------------

    def supervisor_node(
        self, state: AgentState
    ) -> Command[Literal["information_node", "booking_node", "__end__"]]:
        print("\n================ SUPERVISOR ENTER ================")
        print("Incoming state →", state)

        # 1. waiting for user follow‑up ------------------------------
        if state.get("follow_up_needed"):
            print("Follow‑up flag set ➜ not routing, waiting for user input…")
            return Command(goto="__end__", update={"follow_up_needed": False})

        # 2. build routing prompt -----------------------------------
        router_messages = [
            SystemMessage(
                content=f"{system_prompt}\nUser's identification number is {state['id_number']}"
            )
        ] + state["messages"]

        last_user_query = state["messages"][-1].content if state["messages"] else ""
        print("Router prompt messages →", router_messages)
        print("Last user query →", last_user_query)

        router_response = (
            self.llm_model.with_structured_output(Router).invoke(router_messages)
        )

        next_node = router_response["next"]
        reasoning = router_response["reasoning"]
        print("Router decided next →", next_node)
        print("Router reasoning →", reasoning)

        if next_node == "FINISH":
            next_node = END
            print("Router says FINISH: ending run.")

        # 3. propagate state ----------------------------------------
        print("Supervisor exiting, routing to →", next_node)
        return Command(
            goto=next_node,
            update={
                "next": next_node,
                "query": last_user_query,
                "current_reasoning": reasoning,
            },
        )

    # --------------------- information specialist ----------------------

    def information_node(self, state: AgentState) -> Command[Literal["supervisor"]]:
        print("\n>>>>>>>> INFORMATION NODE <<<<<<<<")

        sys_prompt = f"""
            You are an assistant specialized in answering questions about doctor
            availability and hospital‑related FAQs. Use the provided tools to
            check schedules.

            The user's identification number is {state['id_number']}. Never ask
            for it again. If date, time, doctor name, or specialization is
            missing, politely ask for it. Current year is 2025.
        """

        agent_prompt = ChatPromptTemplate.from_messages(
            [("system", sys_prompt), MessagesPlaceholder(variable_name="messages")]
        )

        info_agent = create_react_agent(
            model=self.llm_model,
            tools=[check_availability_by_doctor, check_availability_by_specialization],
            prompt=agent_prompt,
        )

        result = info_agent.invoke(state)
        follow_up_msg = result["messages"][-1].content
        tool_was_used = any(getattr(msg, "role", None) == "tool" for msg in result["messages"])

        print("information_node → tool_was_used:", tool_was_used)
        print("information_node → follow_up_msg:", follow_up_msg)

        return Command(
            goto="supervisor",
            update={
                "messages": state["messages"]
                + [AIMessage(content=follow_up_msg, name="information_node")],
                "follow_up_needed": not tool_was_used,
            },
        )

    # ----------------------- booking specialist ------------------------

    def booking_node(self, state: AgentState) -> Command[Literal["supervisor"]]:
        print("\n>>>>>>>> BOOKING NODE <<<<<<<<")
        print("User id →", state.get("id_number"))

        sys_prompt = f"""
            You manage doctor appointments (set, cancel, reschedule) via tools.
            The user's identification number is {state['id_number']}; never ask
            for it again. If date, time, or doctor name is missing, ask
            clarifying questions. Assume year 2025.
        """

        agent_prompt = ChatPromptTemplate.from_messages(
            [("system", sys_prompt), MessagesPlaceholder(variable_name="messages")]
        )

        booking_agent = create_react_agent(
            model=self.llm_model,
            tools=[set_appointment, cancel_appointment, reschedule_appointment],
            prompt=agent_prompt,
        )

        result = booking_agent.invoke(state)
        follow_up_msg = result["messages"][-1].content
        tool_was_used = any(getattr(msg, "role", None) == "tool" for msg in result["messages"])

        print("booking_node → tool_was_used:", tool_was_used)
        print("booking_node → follow_up_msg:", follow_up_msg)

        return Command(
            goto="supervisor",
            update={
                "messages": state["messages"]
                + [AIMessage(content=follow_up_msg, name="booking_node")],
                "follow_up_needed": not tool_was_used,
            },
        )
