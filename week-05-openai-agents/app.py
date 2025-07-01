import streamlit as st
import asyncio
from agents import Agent, Runner, trace
from agents import function_tool, input_guardrail, GuardrailFunctionOutput

# Tool: Web search
@function_tool
def web_search(query: str) -> str:
    """Search the web via LLM-backed tool."""
    return f"Simulated search result for: '{query}'"

# Guardrail: Prevent math homework
@input_guardrail
async def no_math_homework(ctx, agent, inp: str) -> GuardrailFunctionOutput:
    if "solve my homework" in inp.lower():
        return GuardrailFunctionOutput(
            output_info="Homework requests not allowed.",
            tripwire_triggered=True
        )
    return GuardrailFunctionOutput(
        output_info="Input passed guardrail.",
        tripwire_triggered=False
    )

# Agent A: Triage
triage_agent = Agent(
    name="TriageAgent",
    instructions="If this is a math homework request, don't allow it. Otherwise, use web_search or delegate.",
    tools=[web_search],
    handoffs=[],  # to be added below
    input_guardrails=[no_math_homework],
)

# Agent B: Web specialist
web_agent = Agent(
    name="WebAgent",
    instructions="Use web_search to fetch and summarize web information.",
    tools=[web_search],
)

# Define handoffs
triage_agent.handoffs = [web_agent]

# Main app
async def main():
    st.title("🤖 Multi-Agent Assistant with Guardrails")
    prompt = st.text_input("Ask something:")
    if st.button("Submit") and prompt:
        with trace("streamlit-multi-agent"):
            result = await Runner.run(triage_agent, input=prompt)
        st.write("### 💬 Response:")
        st.markdown(result.final_output)
        st.caption("✅ Check the Traces dashboard to inspect execution flow, handoffs, and guardrails.")

if __name__ == "__main__":
    asyncio.run(main())
