from agents import Agent, function_tool, input_guardrail, GuardrailFunctionOutput

@function_tool
def compute_square(x: int) -> int:
    return x * x

@input_guardrail
async def limit_numbers(ctx, agent, inp: str) -> GuardrailFunctionOutput:
    # Guard against large numeric requests
    if "million" in inp:
        return GuardrailFunctionOutput(trip=True, payload={"message": "Too big numbers not allowed."})
    return GuardrailFunctionOutput(trip=False)

compute_agent = Agent(
    name="ComputeAgent",
    instructions="Calculate square of a provided integer using compute_square.",
    tools=[compute_square],
    input_guardrails=[limit_numbers],
)

# Another agent to handle general chat
chat_agent = Agent(
    name="ChatAgent",
    instructions="Answer casually if it's not a computation question. Otherwise allow handoff.",
    handoffs=[compute_agent],
)
